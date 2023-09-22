# this file mimics the frontend; if you run it, it will call all functions of the backend of "ode_beam"
from ode_beam_backend import odebeam_backend
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['text.usetex'] = True

def test_case_data(test_case):
    """this function is the setup for the ode_beam backend. By defining a test_case it calls all the necessary functions of ode_beam"""
    if test_case == 1:
        data = [{'type': 'straight_beam', 'endpoint': [[237.5, 480], [362.5, 480]], 'line_load': 'constant', 'coordinate_system_position': True, 'coordinate_system_orientation': True},
                {'type': 'fixed_bearing', 'endpoint': [[237.5, 480]]},
                {'type': 'fixed_bearing', 'endpoint': [[362.5, 480]]},
                {'length_normalization': 125}]
    elif test_case == 2:
        data = [{'type': 'straight_beam', 'endpoint': [[237.5, 480], [362.5, 480]], 'line_load': 'linear_descending', 'coordinate_system_position': True, 'coordinate_system_orientation': True, 'thermal_load':True},
                {'type': 'fixed_bearing', 'endpoint': [[237.5, 480]]}, 
                {'type': 'straight_beam', 'endpoint': [[362.5, 373.375], [487.5, 373.375]], 'line_load': 'constant', 'coordinate_system_position': True, 'coordinate_system_orientation': True, 'thermal_load':True},
                {'type': 'linear_spring_MC', 'endpoint': [[362.5, 480], [362.5, 373.375]]},
                {'type': 'rigid_support', 'endpoint': [[487.5, 373.375]]}, 
                {'length_normalization': 125}]
    else:
        print("something went wrong, no execution")
    return data


# run a test case:
#data_list_ode, data_list_bc, data_list_mc = odebeam_backend(test_case_data(1))

#Thermal Test Case:
calculate_thermal_load = False  # Set to True to calculate thermal load
#material = "steel"  # Choose between "steel" or "aluminium" Metial is now fix as steel can be reimplemented if needed
data_list_ode, data_list_mc, data_listbc, data_listmc, data_list_bc_evaluated = odebeam_backend(test_case_data(2))
for i in range(len(data_list_ode)):
    print(f"the ansatz for beam {i+1} is {data_list_ode[i]}")
print("the boundary conditions are", data_listbc)
print("the boundary conditions inserted in the ansatz provide", data_list_bc_evaluated)
print("the matching conditions are", data_listmc)
