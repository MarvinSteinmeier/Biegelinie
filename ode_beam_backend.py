from classes import MatchingConditionSymbol, System

from system import change_bearings_to_connections, data_for_boundary_conditions_sympy, determine_MC_bearings, create_new_beam, create_new_connections_and_bonds, \
    create_dependencies, data_for_ansatz_ode, data_for_boundary_conditions, data_for_matching_conditions, check_positions_of_system, normalize_coordinates, check_degree_of_indeterminacy
from exceptions import NoElementsInSystemError

def odebeam_backend(data, h, To, Tu, calculate_thermal_load=False, material=None):
    #print(data)
    if not data:
        raise NoElementsInSystemError("Erstellen Sie bitte ein System bestehend aus Balken und Lagern bevor Sie auf 'System berechnen' klicken!")
    

    if calculate_thermal_load and material:
        if material == "steel":
            material_alpha = 1.2e-5
        elif material == "aluminium":
            material_alpha = 2.3e-5
        else:
            raise ValueError("Invalid material choice")
        
        
    # create a new empty system
    system = System()

    for i in range(len(data)-1):
        element = data[i]
        
        element_type = element.get("type")

        # at first beams must be created, they are responsible for the positions and joints
        if element_type == "straight_beam" or element_type == "rigid_beam":
            start_point = normalize_coordinates(element.get("endpoint")[1], data[-1].get('length_normalization'))
            end_point = normalize_coordinates(element.get("endpoint")[0], data[-1].get('length_normalization'))
            create_new_beam([start_point, end_point], element.get("line_load"), element_type, element.get("coordinate_system_position"), element.get("coordinate_system_orientation"), system)
    
    for i in range(len(data)):
        element = data[i]
        element_type = element.get("type")

        if element_type in ["fixed_bearing","floating_bearing","rigid_support","guided_support_vertical","guided_support_vertical",
                            "torsional_spring","linear_spring", "joint", "free_end"]:
            position = normalize_coordinates(element.get("endpoint")[0], data[-1].get('length_normalization'))
            
            create_new_connections_and_bonds([position], element_type, "", system)

        elif element_type in ["single_moment", "single_force"]:
            position = normalize_coordinates(element.get("endpoint")[0], data[-1].get('length_normalization'))
            positive = element.get("positive")
            
            create_new_connections_and_bonds([position], element_type, positive, system)

        elif element_type in ["rigid_connection","linear_spring_MC", "fixed_rigid_MC"]:
            start_point = normalize_coordinates(element.get("endpoint")[0], data[-1].get('length_normalization'))
            end_point = normalize_coordinates(element.get("endpoint")[1], data[-1].get('length_normalization'))
            if element_type == "fixed_rigid_MC":
                rigid_right = element.get("rigid_right")
            else:
                rigid_right = ""
            
            create_new_connections_and_bonds([start_point, end_point], element_type, rigid_right, system)

        
    create_dependencies(system)
    determine_MC_bearings(system)
    change_bearings_to_connections(system)
    
    check_positions_of_system(system)
    check_degree_of_indeterminacy(system)
    
    
    for beam in system.beam_list:
        for bond in beam.bond_list:
            if isinstance(bond, MatchingConditionSymbol):
                system.set_up_matching_conditions(beam, bond)
            else:
                system.set_up_boundary_conditions(beam, bond)  

    data_list_ode = data_for_ansatz_ode(system)
    # print(data_list_ode)

    data_list_bc = data_for_boundary_conditions(system)
    #data_list_bc=data_for_boundary_conditions_sympy(system)
    #print(data_list_bc)
    #data_for_boundary_conditions_sympy(system)
    data_list_mc = data_for_matching_conditions(system)
    #print(data_list_mc)

    
    return data_list_ode, data_list_bc, data_list_mc
