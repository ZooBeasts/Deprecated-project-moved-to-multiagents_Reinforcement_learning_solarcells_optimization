
import numpy as np

eps=1e-5

def get_env_fn(env_name, **kwargs):
    if env_name == 'visnir':
        try:
            return vis_nir(**kwargs)
        except:
            print("Env error!")
    elif env_name == 'sloarcell':
            return solarcell(**kwargs)
    else:
       raise NotImplementedError


def vis_nir(**kwargs):


    wavelengths = np.arange(0.4, 1.8, 0.01)
    materials = ['Ag', 'Al', 'Al2O3', 'Ge', 'HfO2', 'MgF2', 'Ni', 'Si', 'SiO2', 'Ti', 'TiO2',
                 'ZnO', 'ZnS', 'ZnSe', 'Fe2O3','Pt','ITO','Au']
    simulator = TMM_sim(materials, wavelengths, substrate='Glass', substrate_thick=500)
    thickness_list = np.arange(15, 255, 5)

    # we maximize the total absorption in the whole wavelength range
    target = {'A': np.ones_like(wavelengths)}

    config = {'wavelengths': wavelengths,
              "materials": materials,
              'target': target,
              "merit_func": cal_reward,
              "simulator": simulator,
              **kwargs}

    if kwargs['discrete_thick']:
        config['discrete_thick'] = True
        config['thickness_list'] = thickness_list

    def make():
        env = TMM(**config)

        return env

    return make


def solarcell(**kwargs):


    wavelengths = np.arange(0.4, 1.0, 0.01)
    materials = ['Al2O3','TiO2','ITO','ZnO','WO3','Nb2O5','MAPbBr3','BaTiO3','CuO','Au']
    #SrTiO3,'PbTiO3,'MAPbl3'
    simulator = TMM_sim(materials, wavelengths, substrate='Au', substrate_thick=50)
    thickness_list = np.arange(20, 400, 10)


    target = {'A': np.ones_like(wavelengths)}

    config = {'wavelengths': wavelengths,
              "materials": materials,
              'target': target,
              "merit_func": cal_reward,
              "simulator": simulator,
              **kwargs}

    if kwargs['discrete_thick']:
        config['discrete_thick'] = True
        config['thickness_list'] = thickness_list

    def make():
        env = TMM(**config)
        return env

    return make



