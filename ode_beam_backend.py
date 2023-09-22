from classes import System

from system import change_bearings_to_connections, determine_MC_bearings_and_MC_rigid_beams, create_new_beam, create_new_connections_and_bonds, \
    create_dependencies, data_for_matching_conditions, check_positions_of_system, check_degree_of_indeterminacy
from exceptions import NoElementsInSystemError
from results import data_for_ansatz_ode, data_bc, data_mc, data_bc_evaluated

def odebeam_backend(data):
    """this function processes the data of the frontend for the backend of ode beam"""
    
    # print(data)
    if len(data)<2:
        raise NoElementsInSystemError()
    
    system = System()
    
    length_normalization = data[-1].get('length_normalization')
    
    # as the last element is the length normalization, the data is iterated till length-1
    for i in range(len(data) - 1):
        element = data[i]

        # at first beams must be created, they are responsible for the positions and joints
        if element.get("type") in ["straight_beam", "rigid_beam"]:
            start_point = normalize_values(element.get("endpoint")[0], length_normalization)
            end_point = normalize_values(element.get("endpoint")[1], length_normalization)
            create_new_beam([start_point, end_point],
                            element.get("line_load"),
                            element.get("type"),
                            element.get("coordinate_system_position"),
                            element.get("coordinate_system_orientation"),
                            element.get("thermal_load"),
                            system)
    
    for i in range(len(data) - 1):
        element = data[i]
        
        element_type = element.get("type")
        
        # after that, the rest of the elements is created
        if element_type in ["fixed_bearing", "floating_bearing", "rigid_support", "guided_support_vertical", "free_end",
                            "joint",
                            "torsional_spring", "linear_spring",  
                            "single_moment", "single_force"]:
            position = normalize_values(element.get("endpoint")[0], length_normalization)
            
            if element_type in ["single_moment", "single_force"]:
                positive = element.get("positive")
            else:
                positive = None
            
            create_new_connections_and_bonds([position], element_type, positive, system)

        elif element_type in ["rigid_connection","linear_spring_MC"]:
            start_point = normalize_values(element.get("endpoint")[0], length_normalization)
            end_point = normalize_values(element.get("endpoint")[1], length_normalization)
            
            create_new_connections_and_bonds([start_point, end_point], element_type, None, system)

        
    create_dependencies(system)
    determine_MC_bearings_and_MC_rigid_beams(system)
    change_bearings_to_connections(system)
    
    check_positions_of_system(system)
    check_degree_of_indeterminacy(system)
    system.determine_conditions()
    
    data_list_ode = data_for_ansatz_ode(system)
    # print(data_list_ode)

    # data_list_bc = data_for_boundary_conditions(system)
    #data_list_bc=data_for_boundary_conditions_sympy(system)
    #print(data_list_bc)
    #data_for_boundary_conditions_sympy(system)
    data_list_mc = data_for_matching_conditions(system)
    data_listbc = data_bc(system)
    data_list_bc_evaluated = data_bc_evaluated(system)
    data_listmc = data_mc(system)
    # print(data_list_mc)

    
    return data_list_ode, data_list_mc, data_listbc, data_listmc, data_list_bc_evaluated


def normalize_values(values, normalization):
    """this function normalizes the committed value wrt the normalization values"""
    
    try:
        for i in range(len(values)):
            values[i] = values[i]/normalization
    except:
        values = values / normalization

    return values
