import sympy as sp
from classes import BearingConnection, FreeEnd, RigidBeamMC, Position, Beam, RigidBeam, FixedBearing, FloatingBearing, RigidSupport, GuidedSupportVertical, LinearSpring, SingleMoment, TorsionalSpring, Joint, RigidConnection, LinearSpringMC, FixedBearingMC, FloatingBearingMC, MatchingConditionSymbol, SingleForce
from exceptions import NoValidBondsInSystemError, BondsAtPositionError, ToLessBeamsAtMatchingConditionPositionError, RigidBeamEndsInNothingError, TorsionalSpringAtJointError, JointAndFreeEndConfusionError, DegreeOfIndeterminacyError, GeneralUserError


def create_new_beam(start_and_end_coordinates, line_load, type_string, coordinate_system_position, coordinate_system_orientation, thermal_load, system):
    """this function either creates a beam or rigid beam based on the committed values"""
    
    position_list = []
    for position in start_and_end_coordinates:
        new_position = Position(position)
        new_position = system.add_position(new_position)
        position_list.append(new_position)
        
    new_beam = create_either_beam_or_rigid_beam(position_list, type_string, coordinate_system_position, coordinate_system_orientation, thermal_load)
   
    if isinstance(new_beam, Beam):
        system.add_beam(new_beam)
        new_beam.beam_index = (system.beam_list.index(new_beam) + 1)
        new_beam.calc_ansatz_for_ODE_of_beam(line_load)
        new_beam.calc_ansatz_for_ODE_of_beam_constants()

        for position in position_list:
            position.add_beam(new_beam)

    else:  # rigid beams are gathered in the connection list
        system.add_connection(new_beam)
        
        for position in position_list:
            position.add_connection(new_beam)


def create_either_beam_or_rigid_beam(position_list_for_beam, type_string, coordinate_system_position, coordinate_system_orientation, thermal_load):
    """this function creates an instance of the object Beam or RigidBeam based on the committed type string"""
    
    if type_string == "straight_beam":
        new_beam = Beam(position_list_for_beam, coordinate_system_position, coordinate_system_orientation, thermal_load)
    else:
        new_beam = RigidBeam(position_list_for_beam)
    return new_beam


def create_new_connections_and_bonds(positions, type_string, positive, system):
    """this function either creates connections or bonds based on the committed values"""
    
    position_list = []
    for position in positions:
        new_position = Position(position)
        new_position = system.add_position(new_position)
        position_list.append(new_position)
        
    new_connection_or_bond = create_correct_type_of_connection_or_bond(position_list, type_string, positive)

    if new_connection_or_bond.bond:
        system.add_bond(new_connection_or_bond)
        for position in position_list:
            position.add_bond(new_connection_or_bond)
    else:
        system.add_connection(new_connection_or_bond)
        for position in position_list:
            position.add_connection(new_connection_or_bond)


def create_correct_type_of_connection_or_bond(position, type_string, positive):
    """this function creates an instance of the respective bond or connection object based on the committed type string"""
    
    if type_string == "fixed_bearing":
        new_connection_or_bond = FixedBearing(position)
    elif type_string == "floating_bearing":
        new_connection_or_bond = FloatingBearing(position)
    elif type_string == "rigid_support":
        new_connection_or_bond = RigidSupport(position)
    elif type_string == "guided_support_vertical":
        new_connection_or_bond = GuidedSupportVertical(position)
    elif type_string == "linear_spring":
        new_connection_or_bond = LinearSpring(position)
    elif type_string == "torsional_spring":
        new_connection_or_bond = TorsionalSpring(position)
    elif type_string == "joint":
        new_connection_or_bond = Joint(position)
    elif type_string == "rigid_connection":
        new_connection_or_bond = RigidConnection(position)
    elif type_string == "linear_spring_MC":
        new_connection_or_bond = LinearSpringMC(position)
    elif type_string == "fixed_bearing_MC":
        new_connection_or_bond = FixedBearingMC(position)
    elif type_string == "floating_bearing_MC":
        new_connection_or_bond = FloatingBearingMC(position)
    elif type_string == "rigid_beam_MC":
        new_connection_or_bond = RigidBeamMC(position)
    elif type_string == "single_moment":
        new_connection_or_bond = SingleMoment(position, positive)
    elif type_string == "single_force":
        new_connection_or_bond = SingleForce(position, positive)
    elif type_string == "bearing_connection":
        new_connection_or_bond = BearingConnection(position, positive)
    elif type_string == "free_end":
        new_connection_or_bond = FreeEnd(position)
    return new_connection_or_bond


def create_dependencies(system):
    """this function creates needed dependencies between all occuring system elements"""

    for beam in system.beam_list:
        for position in beam.position_list:
            if any(position == pt for pt in system.position_list):
                for connection in position.connection_list:
                    beam.add_connection(connection)
                    connection.add_beam(beam)

                    # add the bond of the rigid beam to the beam
                    if isinstance(connection, RigidBeam):
                        for pos in connection.position_list:
                            if pos.bond_list:
                                beam.add_bond(pos.bond_list[0])
                for bond in position.bond_list:
                    beam.add_bond(bond)
                    bond.add_beam(beam)


def determine_MC_bearings_and_MC_rigid_beams(system):
    """this function determines if floating and/or fixed bearings or rigid beams are 'inside' the system and therefore have effect on matching conditions"""
    
    MC_bearing_list = []
    for bond in system.bond_list:
        if isinstance(bond, FloatingBearing) or isinstance(bond, FixedBearing):
            # if at the position of the bearing are more than one beam, it is a MC bearing
            if len(bond.position_list[0].beam_list) > 1:
                MC_bearing_list.append(bond)

            # if there is a rigid beam at the bearing, check if at the other position is a beam; if yes, the bearing is a MC bearing
            elif len(bond.position_list[0].beam_list) == 1 and bond.position_list[0].connection_list:
                if isinstance(bond.position_list[0].connection_list[0], RigidBeam): # i am not sure if there is a case that a rigid beam is not at connection list position zero
                    rigid = bond.position_list[0].connection_list[0]
                    for pos in rigid.position_list:
                        if pos.x_coordinate != bond.position_list[0].x_coordinate and (len(pos.beam_list) > 0 or len(pos.bond_list) > 0):
                            MC_bearing_list.append(bond)
            
            # the last case is that there are two rigid beams at the bearing
            elif bond.position_list[0].connection_list: 
                rigid_counter = 0
                for connection in bond.position_list[0].connection_list:
                    if isinstance(connection, RigidBeam):
                        rigid_counter += 1
                if rigid_counter == 2:
                    MC_bearing_list.append(bond)
                    
    for bearing in MC_bearing_list:
        create_MC_bearing(bearing, system)
    create_dependencies(system)
    
    for connection in system.connection_list:
        if isinstance(connection, RigidBeam):
            if len(connection.beam_list) > 1:
                # for position in connection.position_list:
                if all(not pos.bond_list for pos in connection.position_list):
                    create_MC_rigid_beam(connection, system)
    create_dependencies(system)


def create_MC_bearing(bond, system):
    """this function creates the new instance of the MC bearing and removes the old one from the system"""
    
    if isinstance(bond, FixedBearing):
        string = "fixed_bearing_MC"
    else:
        string = "floating_bearing_MC"
    
    position = bond.position_list[0]
    
    create_new_connections_and_bonds([[position.x_coordinate, position.z_coordinate]], string, "", system)
    
    system.bond_list.remove(bond)
    position.bond_list.remove(bond)
    
    for beam in system.beam_list:
        if any(bond == b for b in beam.bond_list):
            beam.bond_list.remove(bond)


def create_MC_rigid_beam(connection, system):
    """this function creates the new instance of the MC rigid beam and removes the old one from the system"""
    
    position_0 = connection.position_list[0]
    position_1 = connection.position_list[1]
    
    create_new_connections_and_bonds([[position_0.x_coordinate, position_0.z_coordinate],
                                      [position_1.x_coordinate, position_1.z_coordinate]],
                                     "rigid_beam_MC", "", system)
    
    system.connection_list.remove(connection)
    
    for position in connection.position_list:
        position.connection_list.remove(connection)
    for beam in system.beam_list:
        if any(connection == con for con in beam.connection_list):
            beam.connection_list.remove(connection)


def change_bearings_to_connections(system):
    """this function changes a bearing_MC that is a matching condition symbol to a connection. this may only be done, if there are more than "number of beams -1" matching condition symbols in the bond list!"""
    
    number_matching_condtions = 0
    for bond in system.bond_list:
        if isinstance(bond, MatchingConditionSymbol):
            number_matching_condtions += 1
            
    if number_matching_condtions > len(system.beam_list) -1:
        for bond in system.bond_list:
            if isinstance(bond, MatchingConditionSymbol):
                for position in bond.position_list:
                    if position.connection_list:
                        if isinstance(position.connection_list[0], RigidBeam):
                            rigid = position.connection_list[0]
                            for pos in rigid.position_list:
                                for bd in pos.bond_list:
                                    if isinstance(bd, FloatingBearing) or isinstance(bd, FixedBearing) or isinstance(bd, FloatingBearingMC) or isinstance(bd, FixedBearingMC):
                                        system.bond_list.remove(bd)
                                        pos.bond_list.remove(bd)
                                        for beam in bond.beam_list:
                                            try:
                                                beam.bond_list.remove(bd)
                                            except:
                                                pass
                                        if isinstance(bd, FloatingBearing) or isinstance(bd, FloatingBearingMC):
                                            forces = 1
                                        if isinstance(bd, FixedBearing) or isinstance(bd, FixedBearingMC):
                                            forces = 2
                                        create_new_connections_and_bonds([[pos.x_coordinate, pos.z_coordinate]], "bearing_connection", forces, system)

def check_positions_of_system(system):
    """this function checks the positions of the system and raises errors if necessary"""
    
    for position in system.position_list:
        if not position.bond_list and not any(isinstance(rigid, RigidBeam) for rigid in position.connection_list):
            raise NoValidBondsInSystemError()
        if len(position.bond_list) > 1:
            raise BondsAtPositionError()

    for bond in system.bond_list:
        if isinstance(bond, MatchingConditionSymbol):
            rigid_counter = 0
            for position in bond.position_list:
                if isinstance(bond, Joint) or isinstance(bond, FloatingBearingMC) or isinstance(bond, FixedBearingMC):
                    for connection in position.connection_list:
                        if isinstance(connection, RigidBeam):
                            rigid_counter += 1
                else:
                    if any(isinstance(rigid, RigidBeam) for rigid in position.connection_list):
                        rigid_counter += 1
            if len(bond.beam_list) + rigid_counter < 2:
                raise ToLessBeamsAtMatchingConditionPositionError()
        if isinstance(bond, Joint):
            rigid_counter = 0
            for connection in bond.position_list[0].connection_list:
                if isinstance(connection, RigidBeam):
                    rigid_counter += 1
            number_of_beams = rigid_counter + len(bond.beam_list)
            if number_of_beams < 2:
                raise JointAndFreeEndConfusionError("Sie haben ein Gelenk, das zwei Balken verbinden sollte, an den Systemrand gesetzt. Tauschen Sie es durch das 'freies Ende'-Symbol aus. Sie finden es bei den Randelementen.")
            for position in bond.position_list:
                if any(isinstance(con, TorsionalSpring) for con in position.connection_list):
                    raise TorsionalSpringAtJointError("Ein Platzieren von Torsionsfedern an einem Gelenk ist nicht möglich, da sie (zurzeit) nicht eindeutig einem der Balken zugeordnet werden kann.")
        if isinstance(bond, FloatingBearingMC) or isinstance(bond, FixedBearingMC):
            for position in bond.position_list:
                if any(isinstance(con, TorsionalSpring) for con in position.connection_list):
                    raise TorsionalSpringAtJointError("Ein Platzieren von Torsionsfedern an einem Lager als Übergangselement ist nicht möglich, da sie (zurzeit) nicht eindeutig einem der Balken zugeordnet werden kann.")
        if isinstance(bond, FreeEnd):
            if len(bond.beam_list) > 1:
                raise JointAndFreeEndConfusionError("Sie haben ein freies Ende, das am Rand eines Balkens sitzt, inmitten des Systems gesetzt. Tauschen Sie es durch das 'Gelenk'-Symbol aus. Sie finden es bei den Übergangselementen.")              
    for connection in system.connection_list:
        if isinstance(connection, RigidBeam):
            for position in connection.position_list:
                if not position.bond_list and not position.beam_list and len(position.connection_list)<2:
                    raise RigidBeamEndsInNothingError()


def check_degree_of_indeterminacy(system):
    """this function checks the degree of indeterminacy of the system and raises an error if necessary"""
    
    equations = len(system.beam_list)*3
    unknowns = 0

    for bond in system.bond_list:
        if any(isinstance(bond, x) for x in [FloatingBearing, RigidConnection, LinearSpringMC]):
            unknowns += 1
        elif any(isinstance(bond, x) for x in [FixedBearing, GuidedSupportVertical, Joint, FixedBearingMC, FloatingBearingMC]):
            unknowns += 2
        elif isinstance(bond, RigidSupport):
            unknowns += 3
        elif isinstance(bond, RigidBeamMC):
            equations -= 3  # because they connect two beams to be as one
    for connection in system.connection_list:
        if isinstance(connection, LinearSpring) or isinstance(connection, TorsionalSpring):
            unknowns += 1
        elif isinstance(connection, BearingConnection):
            unknowns += connection.forces
          
    if (unknowns-equations<0):
        raise DegreeOfIndeterminacyError()


def data_for_boundary_conditions(system):
    data_list = []
    # for beam in system.beam_list:
    for bond in system.bond_list:
        list_conditions = []
        if not isinstance(bond, MatchingConditionSymbol):
            for condition in bond.bc_conditions:
                if condition["value"]:
                    list_conditions.append(bond.bc_conditions[bond.bc_conditions.index(condition)])
            if bond.beam_list:
                beam_index = bond.beam_list[0].beam_index
            else:
                beam_index = bond.position_list[0].connection_list[0].beam_list[0].beam_index
            bond.bc_position["position"] = sp.latex(bond.bc_position["position"])
            bond_BC = [beam_index, bond.bc_position, list_conditions]
            data_list.append(bond_BC)
        # data = {"beam": list_conditions}
        # data_list.append(data)
    return data_list


def data_for_matching_conditions(system):
    data_list = []

    for bond in system.bond_list:
        cross_sections = []
        list_conditions_negative = []
        list_conditions_positive = []
        if isinstance(bond, MatchingConditionSymbol):
            for condition in bond.matching_conditions[0]:
                if condition["value"]:
                    list_conditions_negative.append(bond.matching_conditions[0][bond.matching_conditions[0].index(condition)])

            data_minus = {"negative_cross_section": [bond.mc_position[0], list_conditions_negative],
                          "is_default": bond.cross_sections_default[0]}
            cross_sections.append(data_minus)
            for condition in bond.matching_conditions[1]:
                if condition["value"]:
                    list_conditions_positive.append(bond.matching_conditions[1][bond.matching_conditions[1].index(condition)])
            data_plus = {"positive_cross_section": [bond.mc_position[1], list_conditions_positive],
                         "is_default": bond.cross_sections_default[1]}
            cross_sections.append(data_plus)
            if isinstance(bond, RigidConnection):
                    typus = "rigid_connection"
            elif isinstance(bond, Joint):
                typus = "joint"
            elif isinstance(bond, LinearSpringMC):
                typus = "linear_spring_MC"
            elif isinstance(bond, RigidBeamMC):
                typus = "rigid_beam_MC"
            else:
                typus = "bearing_MC"
            if any(bond.with_bearing):
                bond_type = typus + "_bearing"
            else:
                bond_type = typus

            matching_condition = [bond_type, cross_sections, bond.beam_direction]
            data_list.append(matching_condition)
            #print(bond.cross_sections_default)
            #print(bond.mc_position)

    return data_list
