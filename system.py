import sympy as sp
from classes import BearingConnection, FreeEnd, RigidBeamMC, Position, Beam, RigidBeam, FixedBearing, FloatingBearing, RigidSupport, GuidedSupportVertical, LinearSpring, SingleMoment, TorsionalSpring, Joint, RigidConnection, LinearSpringMC, FixedBearingMC, FloatingBearingMC, MatchingConditionSymbol, SingleForce
from exceptions import NoValidBondsInSystemError, BondsAtPositionError, ToLessBeamsAtMatchingConditionPositionError, RigidBeamEndsInNothingError, TorsionalSpringAtJointError, JointAndFreeEndConfusionError, DegreeOfIndeterminacyError


def create_new_beam(start_and_end_coordinates, line_load, type_string, coordinate_system_position, coordinate_system_orientation, system):
    positions_for_beam = []

    for position in start_and_end_coordinates:
        new_position = Position(position)
        new_position = system.add_position(new_position)
        positions_for_beam.append(new_position)
    new_beam = create_either_beam_or_rigid_beam(positions_for_beam, line_load, type_string, coordinate_system_position, coordinate_system_orientation)
   
    if isinstance(new_beam, Beam):
        system.add_beam(new_beam)
        new_beam.beam_index = str(system.beam_list.index(new_beam) + 1)
        set_correct_index_for_variable(new_beam)

    else:  # rigid beams are gathered in the connection list
        system.add_connection(new_beam)

    if isinstance(new_beam, Beam):
        for position in positions_for_beam:
            position.add_beam(new_beam)
    else:
        for position in positions_for_beam:
            position.add_connection(new_beam)


def set_correct_index_for_variable(beam):
        if beam.line_load != 0:
            beam.line_load = beam.line_load.subs(sp.symbols("x"), sp.symbols("x_"+str(beam.beam_index)))
            beam.shear_force = beam.shear_force.subs(sp.symbols("x"), sp.symbols("x_"+str(beam.beam_index)))
            beam.moment = beam.moment.subs(sp.symbols("x"), sp.symbols("x_"+str(beam.beam_index)))
            beam.angle_phi = beam.angle_phi.subs(sp.symbols("x"), sp.symbols("x_"+str(beam.beam_index)))
            beam.deflection = beam.deflection.subs(sp.symbols("x"), sp.symbols("x_"+str(beam.beam_index)))


def create_either_beam_or_rigid_beam(position_list_for_beam, line_load, type_string, coordinate_system_position, coordinate_system_orientation):
    if type_string == "straight_beam":
        new_beam = Beam(position_list_for_beam, line_load, coordinate_system_position, coordinate_system_orientation)
    else:
        new_beam = RigidBeam(position_list_for_beam)
    return new_beam


def create_new_connections_and_bonds(positions, type_string, positive, system):
    positions_for_connection_or_bond = []
    for position in positions:
        new_position = Position(position)
        new_position = system.add_position(new_position)
        positions_for_connection_or_bond.append(new_position)
    new_connection_or_bond = create_correct_type_of_connection_or_bond(positions_for_connection_or_bond, type_string, positive)

    if new_connection_or_bond.bond:
        system.add_bond(new_connection_or_bond)
        for position in positions_for_connection_or_bond:
            position.add_bond(new_connection_or_bond)
    else:
        system.add_connection(new_connection_or_bond)
        for position in positions_for_connection_or_bond:
            position.add_connection(new_connection_or_bond)


def create_correct_type_of_connection_or_bond(position, type_string, positive):
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
        new_connection_or_bond = RigidBeamMC(position, positive)
    elif type_string == "single_moment":
        new_connection_or_bond = SingleMoment(position, positive)
    elif type_string == "single_force":
        new_connection_or_bond = SingleForce(position, positive)
    elif type_string == "bearing_connection":
        new_connection_or_bond = BearingConnection(position, positive)
    elif type_string == "free_end":
        new_connection_or_bond = FreeEnd(position)
    else:
        print("This type of connection was not implemented yet. Please check function "
              "create_correct_type_of_connection_or_bond")
        new_connection_or_bond = None
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


def determine_MC_bearings(system):
    MC_bearing_list = []
    for bond in system.bond_list:
        if bond.type == "floating_bearing" or bond.type == "fixed_bearing":
            if len(bond.position_list[0].beam_list) > 1:
                MC_bearing_list.append(bond)
                # create_MC_bearing(bond, system)
            elif len(bond.position_list[0].beam_list) == 1 and bond.position_list[0].connection_list:
                if isinstance(bond.position_list[0].connection_list[0], RigidBeam):
                    rigid = bond.position_list[0].connection_list[0]
                    for pos in rigid.position_list:
                        if pos.x_coordinate != bond.position_list[0].x_coordinate and (len(pos.beam_list) > 0 or len(pos.bond_list) > 0):
                            MC_bearing_list.append(bond)
                            # create_MC_bearing(bond, system)
            elif bond.position_list[0].connection_list: # two rigid beams at the bearing
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
    if bond.type == "fixed_bearing":
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
    position_0 = connection.position_list[0]
    position_1 = connection.position_list[1]
    create_new_connections_and_bonds(
        [[position_0.x_coordinate, position_0.z_coordinate], [position_1.x_coordinate, position_1.z_coordinate]],
        "rigid_beam_MC", "", system)
    system.connection_list.remove(connection)
    for position in connection.position_list:
        position.connection_list.remove(connection)
    for beam in system.beam_list:
        if any(connection == con for con in beam.connection_list):
            beam.connection_list.remove(connection)


def change_bearings_to_connections(system):
    # this function changes a bearing_MC that is a matching condition symbol to a connection. this may only be done, if there are more than "number of beams -1" matching condition symbols in the bond list!
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
                                    if bd.type == "floating_bearing" or bd.type == "fixed_bearing" or bd.type == "bearing_MC" or bd.type == "bearing_MC":
                                        system.bond_list.remove(bd)
                                        pos.bond_list.remove(bd)
                                        for beam in pos.beam_list:
                                            beam.bond_list.remove(bd)
                                        if isinstance(bd, FloatingBearing) or isinstance(bd, FloatingBearingMC):
                                            forces = 1
                                        if isinstance(bd, FixedBearing) or isinstance(bd, FixedBearingMC):
                                            forces = 2
                                        create_new_connections_and_bonds([[pos.x_coordinate, pos.z_coordinate]], "bearing_connection", forces, system)

def check_positions_of_system(system):
    for position in system.position_list:
        if not position.bond_list and not any(isinstance(rigid, RigidBeam) for rigid in position.connection_list):
            raise NoValidBondsInSystemError(
                "Sie müssen für alle eingefügten Balken auch einen passenden Systemrand oder -übergang einfügen.")
        if len(position.bond_list) > 1:
            raise BondsAtPositionError(
                "An einer Position darf nur ein Symbol für einen Systemrand oder -übergang sitzen.")

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
                raise ToLessBeamsAtMatchingConditionPositionError(
                    "Übergangselemente müssen an ihren beiden Enden jeweils mit einem Balken verbunden sein.")
        if isinstance(bond, Joint):
            rigid_counter = 0
            for connection in bond.position_list[0].connection_list:
                if isinstance(connection, RigidBeam):
                    rigid_counter += 1
            number_of_beams = rigid_counter + len(bond.beam_list)
            if number_of_beams < 2:
                raise JointAndFreeEndConfusionError(
                    "Sie haben ein Gelenk, das zwei Balken verbinden sollte, an den Systemrand gesetzt. Tauschen Sie es durch das 'freies Ende'-Symbol aus. Sie finden es bei den Randelementen.")
            for position in bond.position_list:
                if any(isinstance(con, TorsionalSpring) for con in position.connection_list):
                    raise TorsionalSpringAtJointError(
                        "Ein Platzieren von Torsionsfedern an einem Gelenk ist nicht möglich, da sie (zurzeit) nicht eindeutig einem der Balken zugeordnet werden kann.")
        if isinstance(bond, FloatingBearingMC) or isinstance(bond, FixedBearingMC):
            for position in bond.position_list:
                if any(isinstance(con, TorsionalSpring) for con in position.connection_list):
                    raise TorsionalSpringAtJointError(
                        "Ein Platzieren von Torsionsfedern an einem Lager als Übergangselement ist nicht möglich, da sie (zurzeit) nicht eindeutig einem der Balken zugeordnet werden kann.")
        if isinstance(bond, FreeEnd):
            if len(bond.beam_list) > 1:
                raise JointAndFreeEndConfusionError(
                    "Sie haben ein freies Ende, das am Rand eines Balkens sitzt, inmitten des Systems gesetzt. Tauschen Sie es durch das 'Gelenk'-Symbol aus. Sie finden es bei den Übergangselementen.")

    for connection in system.connection_list:
        if isinstance(connection, RigidBeam):
            for position in connection.position_list:
                if not position.bond_list and not position.beam_list and not position.connection_list:
                    raise RigidBeamEndsInNothingError(
                        "An einem starren Balkenteil muss etwas an beiden Enden angreifen.")

def check_degree_of_indeterminacy(system):
    equations = len(system.beam_list)*3
    unknowns = 0

    for bond in system.bond_list:
        if any(bond.type == x for x in ["floating_bearing", "rigid_connection", "linear_spring_MC"]):
            unknowns += 1
        elif any(bond.type == x for x in ["fixed_bearing", "guided_support_vertical", "joint", "fixed_bearing_MC", "floating_bearing_MC" ]):
            unknowns += 2
        elif bond.type == "rigid_support":
            unknowns += 3
        elif bond.type == "rigid_beam_MC":
            equations -= 3  # because they connect two beams to be as one
    for connection in system.connection_list:
        if connection.type == "linear_spring" or connection.type == "torsional_spring":
            unknowns += 1
        elif isinstance(connection, BearingConnection):
            unknowns += connection.forces
          
    if (unknowns-equations<0):
        raise DegreeOfIndeterminacyError("Das eingegebene System ist statisch unterbestimmt (n_s<0). Eine Berechnung ist nicht zielführend.")
      


def data_for_ansatz_ode(system):
    data_list = []

    for beam in system.beam_list:
        eiw4 = sp.latex(beam.line_load)
        eiw3 = sp.latex(beam.shear_force)
        eiw2 = sp.latex(beam.moment)
        eiw1 = sp.latex(beam.angle_phi)
        eiw = sp.latex(beam.deflection)

        data_list.append([eiw4, eiw3, eiw2, eiw1, eiw])
        print("Data entry:", [eiw4, eiw3, eiw2, eiw1, eiw])
    return data_list


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

def data_for_boundary_conditions_sympy(system):
    data_list = []
    for bond in system.bond_list:
        list_conditions = []
        if not isinstance(bond, MatchingConditionSymbol):
            if bond.beam_list:
                beam_index = bond.beam_list[0].beam_index
            else:
                beam_index = bond.position_list[0].connection_list[0].beam_list[0].beam_index
            for condition in bond.bc_conditions:
                if condition["value"]:
                    fun = get_function_evaluated_at(condition["condition"], beam_index, bond.bc_position["position"])
                    value = get_value_of_condition(condition["value"], condition["condition"], beam_index, bond.bc_position["position"])

                    if sp.latex(value) != "0":
                        if sp.latex(value)[0] == "-":
                            sign = " "
                        else:
                            sign = " + "
                        value = sign+sp.latex(value, mul_symbol='\,')
                    else:
                        value = ""
                        
                    list_conditions.append(sp.latex(fun)+value+" = 0")
        data_list.append(list_conditions)
    return data_list

def get_function_evaluated_at(condition, beam_number, evaluation):
    x_i = sp.symbols("x_"+str(beam_number))

    if condition == "w":
        function = sp.Function("w")
    elif condition == "\\varphi":
        function = sp.Function("varphi")
    elif condition == "M":
        function = sp.Function("M")
    elif condition == "Q":
        function = sp.Function("Q")
    return function(sp.Eq(x_i, evaluation))

def get_value_of_condition(values, condition, beam_number, evaluation, spring_force="determine when matching conditions"):
    expression = sp.Integer(0)
    if len(values) > 1:
        for i in range(1, len(values)): # the first entry (0) is ommitted
            if values[i][1] == "torsional_spring":
                value = sp.symbols("k_varphi")*get_function_evaluated_at("\\varphi", beam_number, evaluation)

            if values[i][1] == "linear_spring":
                if condition == "M":
                    value = sp.Mul(*(sp.symbols("k_w")*get_function_evaluated_at("w", beam_number, evaluation), sp.symbols("a")), evaluate=False)
                else:  # condition == 'Q'
                    value = sp.symbols("k_w")*get_function_evaluated_at("w", beam_number, evaluation)
            elif values[i][1] == "rigid_linear_spring":
                if condition == "M":
                    value = sp.symbols("k_w")* get_function_evaluated_at("\\varphi", beam_number, evaluation)*sp.symbols("a")**2
            elif values[i][1] == "linear_spring_rigid":
                if condition == "Q":
                    value = spring_force

            elif values[i][1] == "single_moment":
                value = sp.symbols("M")
            elif values[i][1] == "single_force":
                value = sp.symbols("F")*sp.symbols("a")
            elif values[i][1] == "rigid_beam":
                if condition == "M":
                    value = sp.Mul(*(get_function_evaluated_at("Q", beam_number, evaluation), sp.symbols("a")), evaluate=False)
                else:  # condition == 'w'
                    value = sp.symbols("a")*get_function_evaluated_at("\\varphi", beam_number, evaluation)
            elif values[i][1] == "bearing_connection":
                if condition == "M":
                    value = sp.Mul(*(spring_force, sp.symbols("a")), evaluate=False)
                if condition == "w":
                    value = sp.symbols("a")*get_function_evaluated_at("\\varphi", beam_number, evaluation)
            if values[i][0]:
                expression += value
            else:
                expression -= value
    return expression

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
            if bond.with_bearing:
                bond_type = bond.type + "_bearing"
            else:
                bond_type = bond.type

            matching_condition = [bond_type, cross_sections, bond.beam_direction]
            data_list.append(matching_condition)
            #print(bond.cross_sections_default)
            #print(bond.mc_position)

    return data_list


def normalize_coordinates(values, normalization):
    normalized_values = [0, 0]
    for i in range(len(values)):
        normalized_values[i] = values[i] / normalization

    return normalized_values
