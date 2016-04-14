from classy import Class
import numpy as np 
import itertools
from nose_parameterized import parameterized



def m_Pk(k=np.logspace(-3, 0., 100), z=0.53, nl_model='trg'):
    print k
    cosmo = Class()

    CLASS_INPUT = {}

    CLASS_INPUT['Mnu'] = ([{'N_eff': 0.0, 'N_ncdm': 1, 'm_ncdm': 0.06, 'deg_ncdm': 3.0}], 'normal')
    CLASS_INPUT['Output_spectra'] = ([{'output': 'mPk', 'P_k_max_1/Mpc': 1, 'z_pk': z}], 'power')

    CLASS_INPUT['Nonlinear'] = ([{'non linear': nl_model}], 'power')
            
    verbose = {}
    #    'input_verbose': 1,
    #    'background_verbose': 1,
    #    'thermodynamics_verbose': 1,
    #    'perturbations_verbose': 1,
    #    'transfer_verbose': 1,
    #    'primordial_verbose': 1,
    #    'spectra_verbose': 1,
    #    'nonlinear_verbose': 1,
    #    'lensing_verbose': 1,
    #    'output_verbose': 1
    #    }

    cosmo.struct_cleanup()
    cosmo.empty()


    INPUTPOWER = []
    INPUTNORMAL = [{}]
    for key, value in CLASS_INPUT.iteritems():
        models, state = value
        if state == 'power':
            INPUTPOWER.append([{}]+models)
        else:
            INPUTNORMAL.extend(models)

        PRODPOWER = list(itertools.product(*INPUTPOWER))

        DICTARRAY = []
        for normelem in INPUTNORMAL:
            for powelem in PRODPOWER:  # itertools.product(*modpower):
                temp_dict = normelem.copy()
                for elem in powelem:
                    temp_dict.update(elem)
                DICTARRAY.append(temp_dict)

    scenario = {}
    for dic in DICTARRAY:
        scenario.update(dic)
    setting = cosmo.set(dict(verbose.items()+scenario.items()))
    cosmo.compute()
    pk_out = [] 
    for k_i in k: 
        pk_out.append(cosmo.pk(k_i,z))
    return pk_out 

if __name__=='__main__': 
    print m_Pk(nl_model='halofit') 
    print m_Pk(nl_model='trg') 
