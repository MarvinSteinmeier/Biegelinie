# this file mimics the frontend; if you run it, it will call all functions of the backend of "ode_beam"
from ode_beam_backend import odebeam_backend
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['text.usetex'] = True

def test_case_data(test_case):
    """this function is the setup for the ode_beam backend. By defining a test_case it calls all the necessary functions of ode_beam"""
    if test_case == 1:
        data = [{'type': 'straight_beam', 'endpoint': [[362.5, 343], [237.5, 343]], 'line_load': 'constant', 'coordinate_system_position': True, 'coordinate_system_orientation': True,  'material': 'steel'},
                {'type': 'fixed_bearing', 'endpoint': [[362.5, 343]]},
                {'type': 'fixed_bearing', 'endpoint': [[237.5, 343]]},
                {'length_normalization': 125}]
    elif test_case == 2:
        data = [{'type': 'straight_beam', 'endpoint': [[362.5, 343], [237.5, 343]], 'line_load': 'linear_descending', 'coordinate_system_position': True, 'coordinate_system_orientation': True},
                {'type': 'fixed_bearing', 'endpoint': [[237.5, 343]]},
                {'type': 'straight_beam', 'endpoint': [[487.5, 236.375], [362.5, 236.375]], 'line_load': 'constant', 'coordinate_system_position': True, 'coordinate_system_orientation': True},
                {'type': 'linear_spring_MC', 'endpoint': [[362.5, 343], [362.5, 236.375]]},
                {'type': 'rigid_support', 'endpoint': [[487.5, 236.375]]},
                {'length_normalization': 125}]
    elif test_case == 3:
        data = [{'type': 'straight_beam', 'endpoint': [[362.5, 329.25], [237.5, 329.25]], 'line_load': 'linear_descending', 'coordinate_system_position': False, 'coordinate_system_orientation': True},
                {'type': 'straight_beam', 'endpoint': [[487.5, 236.375], [362.5, 236.375]], 'line_load': 'constant', 'coordinate_system_position': True, 'coordinate_system_orientation': False},
                {'type': 'guided_support_vertical', 'endpoint': [[237.5, 329.25]]},
                {'type': 'rigid_connection', 'endpoint': [[362.5, 329.25], [362.5, 236.375]]},
                {'type': 'rigid_beam', 'endpoint': [[570.8333333333334, 236.375], [487.50000000000006, 236.375]]},
                {'type': 'fixed_bearing', 'endpoint': [[570.8333333333334, 236.375]]},
                {'type': 'linear_spring', 'endpoint': [[362.5, 236.375]]},
                {'type': 'torsional_spring', 'endpoint': [[570.8333333333334, 236.375]]},
                {'length_normalization': 125}]
    else:
        print("something went wrong, no execution")
    return data


# run a test case:
#data_list_ode, data_list_bc, data_list_mc = odebeam_backend(test_case_data(1))

#Thermal Test Case:
calculate_thermal_load = False  # Set to True to calculate thermal load
material = "steel"  # Choose between "steel" or "aluminium"
data_list_ode, data_list_mc, data_listbc, data_listmc = odebeam_backend(test_case_data(2))

print("the ansatz is", data_list_ode[0])
print("the boundary conditions are", data_listbc)
print("the matching conditions are", data_listmc)
