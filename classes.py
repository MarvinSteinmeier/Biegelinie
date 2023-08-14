import sympy as sp


class System:
    """this class is the main class for the ode beam backend; it contains the topology of the beam system"""
    
    def __init__(self):
        self.beam_list = []
        self.bond_list = []
        self.connection_list = []
        self.position_list = []


    def add_beam(self, new_beam):
        """this method adds a beam to the beam list"""
        
        self.beam_list.append(new_beam)


    def add_bond(self, new_bond):
        """this method adds a bond to the bond list"""
        
        self.bond_list.append(new_bond)


    def add_connection(self, new_connection):
        """this method adds a connection to the connection list"""
        
        self.connection_list.append(new_connection)


    def add_position(self, new_position):
        """this method adds a position to the position list"""
        
        for position in self.position_list:
            if new_position == position:
                return position

        self.position_list.append(new_position)
        return new_position
    
    
    def determine_conditions(self):
        """this method determines the boundary and matching conditions of the beam system"""
        
        for beam in self.beam_list:
            for bond in beam.bond_list:
                if isinstance(bond, MatchingConditionSymbol):
                    determine_matching_conditions(beam, bond)
                else:
                    determine_boundary_conditions(beam, bond)  
 
    
def determine_boundary_conditions(beam, bond):
    """this function determines the boundary conditions of the committed bond at the committed beam"""
    
    x_position, sign_cross_section, position, _, _, _ = determine_position(beam, bond)
    
    bond.eva_pt = f"(x_{beam.beam_index}={x_position})"
    for index, entry in enumerate(bond.constraints):
        if entry:
            bond.bc_cons[index] += f"{bond.eva_pt}"

    for connection in position.connection_list:
        if not connection.in_condition_considered:
            connection.in_condition_considered = True
            if isinstance(connection, RigidBeam):
                if len(position.bond_list) > 0:  # rigid beam is "outside"
                    for pos in connection.position_list:
                        for con in pos.connection_list:
                            if not con.in_condition_considered:
                                con.in_condition_considered = True
                                if isinstance(con, LinearSpring):
                                    if position != pos:
                                        bond.bc_cons[1] += f"{translate_plus_minus(not sign_cross_section)}{con.spring_constant}\\,\\varphi{bond.eva_pt}{{{connection.length}}}^2"
                                elif isinstance(con, SingleForce):
                                    if position != pos:
                                        if all([con.positive, sign_cross_section]) or all([con.positive, not sign_cross_section]):
                                            sign_force = True
                                        else:
                                            sign_force = False
                                        if not beam.coordinate_system_orientation:  # the sign needs to be changed, when the orientation of the z-axis is upwards
                                            sign_force = not sign_force 
                                        bond.bc_cons[1] += f"{translate_plus_minus(sign_force)}{con.symbol}\\,{connection.length}"
                                        
                                else:
                                    extend_boundary_condition(beam, bond, con, sign_cross_section)
                else:  # rigid beam is "inside"
                    bond.bc_cons[1] += f"{translate_plus_minus((not sign_cross_section))}Q{bond.eva_pt}\\,{connection.length}"
                    bond.bc_cons[3] += f"{translate_plus_minus((sign_cross_section))}{connection.length}\\,\\varphi{bond.eva_pt}"
                    for pos in connection.position_list:
                        for con in pos.connection_list:
                            if not con.in_condition_considered:
                                con.in_condition_considered = True
                                if isinstance(con, LinearSpring):
                                    if position == pos:
                                        bond.bc_cons[1] += f"{translate_plus_minus(True)}{con.spring_constant}\\,w{bond.eva_pt}\\,{connection.length}"
                                elif isinstance(con, SingleForce):
                                    if position == pos:
                                        if all([con.positive, sign_cross_section]) or all([con.positive, not sign_cross_section]):
                                            sign_force = False
                                        else:
                                            sign_force = True
                                        if not beam.coordinate_system_orientation:  # the sign needs to be changed, when the orientation of the z-axis is upwards
                                            sign_force = not sign_force 
                                        bond.bc_cons[1] += f"{translate_plus_minus(sign_force)}{con.symbol}\\,{connection.length}"
                                else:
                                    extend_boundary_condition(beam, bond, con, sign_cross_section)
            else:
                extend_boundary_condition(beam, bond, connection, sign_cross_section)


def extend_boundary_condition(beam, bond, connection, sign_cross_section):
    """this function extends the boundary condition based on the committed connection and sign"""
    
    if isinstance(connection, TorsionalSpring):
        bond.bc_cons[1] += f"{translate_plus_minus((not sign_cross_section))}{connection.spring_constant}\\,\\varphi{bond.eva_pt}"
    elif isinstance(connection, LinearSpring):
        bond.bc_cons[0] += f"{translate_plus_minus((not sign_cross_section))}{connection.spring_constant}\\,w{bond.eva_pt}"
    elif isinstance(connection, SingleMoment):
        if not sign_cross_section:  # the single moment is subtracted at the negative cross section
            sign_moment = False
        else:  # the single moment is added at the positive cross section
            sign_moment = True
        if not beam.coordinate_system_position:  # the sign needs to be changed, when the coordinate system is on the other side
            sign_moment = not sign_moment  
        if not connection.positive:  # the sign needs to be changed, when the moment is negative
            sign_moment = not sign_moment 
        if not beam.coordinate_system_orientation:  # the sign needs to be changed, when the orientation of the z-axis is upwards
            sign_moment = not sign_moment 
        bond.bc_cons[1] += f"{translate_plus_minus(sign_moment)}{connection.symbol}"
    elif isinstance(connection, SingleForce):
        if not sign_cross_section:  # the single force is subtracted at the negative cross section
            sign_force = False
        else:
            sign_force = True
        if not connection.positive:  # the sign needs to be changed, when the force is negative
            sign_force = not sign_force
        if not beam.coordinate_system_orientation:  # the sign needs to be changed, when the orientation of the z-axis is upwards
            sign_force = not sign_force 
        bond.bc_cons[0] += f"{translate_plus_minus(sign_force)}{connection.symbol}"


def determine_matching_conditions(beam, bond):
    """this function determines the matching conditions of the committed bond at the committed beam"""
        
    cross_section_is_default = True
    x_position, sign_cross_section, position, pos_id, rigid, rigid_beam = determine_position(beam, bond)

    if len(bond.position_list)>1 and not isinstance(bond, RigidBeamMC):
        if beam.position_list[0].z_coordinate == bond.position_list[0].z_coordinate and beam.position_list[0].x_coordinate >= bond.position_list[0].x_coordinate:
            cross_section_is_default = False  
            if x_position == 0:
                sign_cross_section = False                 
            else:
                sign_cross_section = True
                                    
        if beam.position_list[0].z_coordinate == bond.position_list[1].z_coordinate and beam.position_list[0].x_coordinate < bond.position_list[1].x_coordinate:
            cross_section_is_default = False
            if x_position == 0:
                sign_cross_section = False
            else:
                sign_cross_section = True                  
    else:
        if x_position == 0:
            sign_cross_section = True
        else:
            sign_cross_section = False 

    id_mc = int(sign_cross_section) # 0 is the negative cross section, 1 is the positive cross section

    if not beam.coordinate_system_position:
        cross_section_is_default = not cross_section_is_default
        id_mc = not id_mc
    if not beam.coordinate_system_orientation:
        cross_section_is_default = not cross_section_is_default
        
    bond.cross_sections_default[id_mc] = cross_section_is_default
    bond.mc_position[id_mc]["position"] = sp.latex(x_position)
    bond.mc_position[id_mc]["index"] = (beam.beam_index)
    bond.eva_pt[id_mc] = f"(x_{beam.beam_index}={x_position})"

    # is needed for some of the matching conditions that are set in the frontend
    if isinstance(bond, RigidBeamMC):
        bond.beam_direction[0] = bond.beam_list[0].coordinate_system_orientation
        bond.beam_direction[1] = bond.beam_list[1].coordinate_system_orientation
    else:
        if len(bond.position_list)>1:
            if position.z_coordinate == bond.position_list[0].z_coordinate:
                bond.beam_direction[0] = beam.coordinate_system_orientation
            else:
                bond.beam_direction[1] = beam.coordinate_system_orientation
        else:
            if len(bond.beam_list)>1:
                if bond.beam_list[1].position_list[0].x_coordinate >= beam.position_list[0].x_coordinate:
                    bond.beam_direction[0] = beam.coordinate_system_orientation
                else:
                    bond.beam_direction[1] = beam.coordinate_system_orientation
            else:
                if beam.position_list[0].x_coordinate < bond.position_list[0].x_coordinate:
                    bond.beam_direction[0] = beam.coordinate_system_orientation
                else:
                    bond.beam_direction[1] = beam.coordinate_system_orientation
    
    for index, entry in enumerate(bond.constraints):
        if entry:
            bond.matching_conditions[id_mc][index]["value"].append(str(0))
            if len(bond.mc_cons[id_mc][index])<2: # due to bearing connection
                if index != 3:
                    bond.mc_cons[id_mc][index] += f"{bond.eva_pt[id_mc]}"
                else:
                    bond.mc_cons[id_mc][index] = f"{translate_empty_minus(bond.beam_direction[id_mc])}w{bond.eva_pt[id_mc]}"
    if isinstance(bond, LinearSpringMC): # in order to define the spring force, the deflection is set with the evaluation point and the sign of the beam direction
        bond.mc_cons[id_mc][3] = f"{translate_empty_minus(bond.beam_direction[id_mc])}w{bond.eva_pt[id_mc]}"
        bond.deflection[id_mc] = bond.mc_cons[id_mc][3]
        
    if isinstance(bond, RigidBeamMC): # this is a special matching condition
        if position == bond.position_list[1]: # one needs to account for the change of the shear force and the displacement, which is incorporated on the "right side" of the rigid beam
            bond.matching_conditions[id_mc][1]["value"].append([not sign_cross_section, "rigid_beam"])
            # append the moment due to the shear force on the "positive cross section" to the moment condition (of the positive cross section)
            bond.mc_cons[1][1] += f"{translate_plus_minus((not sign_cross_section))}Q{bond.eva_pt[1]}\\,{bond.length}"
            for pos in bond.position_list:
                if pos.beam_list:
                    if pos.beam_list[0] != beam:
                        other_beam = pos.beam_list[0]
            if other_beam.coordinate_system_orientation:
                bond.matching_conditions[id_mc][3]["value"].append([True, "rigid_beam"])        
            else:
                bond.matching_conditions[id_mc][3]["value"].append([False, "rigid_beam"])
            bond.mc_cons[1][3] += f"{translate_plus_minus(other_beam.coordinate_system_orientation)}{bond.length}\\varphi{bond.eva_pt[1]}"
            # set the evaluation point for the angle condition
            bond.mc_cons[0][2] += f"{bond.eva_pt[0]}"
            bond.mc_cons[1][2] += f"{bond.eva_pt[1]}"

    for connection in position.connection_list:
        if not connection.in_condition_considered:
            connection.in_condition_considered = True
            if isinstance(connection, LinearSpring):
                if not id_mc: # negative cross section, position_list[0] in bond
                    sign = True # the spring force is always showing "up" (against default z)
                else:
                    sign = False
                if not beam.coordinate_system_orientation:
                    sign = not sign # the sign needs to be changed, when the orientation is flipped
                bond.matching_conditions[id_mc][0]["value"].append([sign, "linear_spring"])
                bond.mc_cons[id_mc][0] += f"{translate_plus_minus((sign))}{connection.spring_constant}\\,w{bond.eva_pt[id_mc]}"
                
                # if the bond is a rigid beam as matching condition, a linear spring is also (and only on the right side of the rigid beam) accounted for the moment condition
                if isinstance(bond, RigidBeamMC) and position == bond.position_list[1]: # the appearing spring force is accounted a the shear force and must not be incorporated for the moment condition - the reference point is the "left" side of the rigid beam
                    bond.matching_conditions[id_mc][1]["value"].append([not sign, "rigid_beam_MC"])
                    bond.mc_cons[id_mc][1] += f"{translate_plus_minus((not sign))}{connection.spring_constant}\\,w{bond.eva_pt[id_mc]}\\,{bond.length}"

            elif isinstance(connection, TorsionalSpring):
                if not id_mc:
                    sign = True # the default for the negative cross section is a positive moment
                else:
                    sign = False # the default for the positive cross section is a negative moment
                if not cross_section_is_default:
                    sign = not sign
                if not beam.coordinate_system_orientation:
                    sign = not sign # the sign needs to be changed, when the orientation is flipped (due to cross_section_default)
                bond.matching_conditions[id_mc][1]["value"].append([sign, "torsional_spring"])
                bond.mc_cons[id_mc][1] += f"{translate_plus_minus((sign))}{connection.spring_constant}\\,\\varphi{bond.eva_pt[id_mc]}"

            elif isinstance(connection, SingleMoment):
                if not id_mc:
                    sign = False
                else:
                    sign = True
                if not cross_section_is_default:
                    sign = not sign
                if not beam.coordinate_system_position:
                    sign = not sign # the sign needs to be changed, when the coordinate system is on the other side
                if not connection.positive:
                    sign = not sign # the sign needs to be changed, when the moment is negative
                bond.matching_conditions[id_mc][1]["value"].append([sign, "single_moment"])
                bond.mc_cons[id_mc][1] += f"{translate_plus_minus(sign)}{connection.symbol}"

            elif isinstance(connection, SingleForce):
                if not id_mc:
                    sign = False
                else:
                    sign = True
                if not connection.positive:
                    sign = not sign
                bond.matching_conditions[id_mc][0]["value"].append([sign, "single_force"])
                bond.mc_cons[id_mc][0] += f"{translate_plus_minus(sign)}{connection.symbol}"
                # if the bond is a rigid beam as matching condition, a linear spring is also (and only on the right side of the rigid beam) accounted for the moment condition
                if isinstance(bond, RigidBeamMC) and position == bond.position_list[1]: # the appearing spring force is accounted a the shear force and must not be incorporated for the moment condition - the reference point is the "left" side of the rigid beam
                    bond.matching_conditions[id_mc][1]["value"].append([not sign, "single_force"])
                    bond.mc_cons[id_mc][1] += f"{translate_plus_minus((not sign))}{connection.symbol}\\,{bond.length}"

            elif isinstance(connection, RigidBeam):
                # if rigid:
                if isinstance(bond, FixedBearingMC) or isinstance(bond, FloatingBearingMC): # the conditions of bearing MC change if there is a rigid beam
                    bond.rigid_lever = f"{connection.length}" # this is used as a True/False case in results.py
                    # set the evaluation point for the angle condition
                    for pos in connection.position_list:
                        if pos.beam_list:
                            if pos.beam_list[0] != beam:
                                other_beam = pos.beam_list[0]
                    eva_pt_other = f"(x_{other_beam.beam_index}={determine_position(other_beam, bond)[0]})"
                    bond.mc_cons[0][2] += f"{bond.eva_pt[0]}"
                    bond.mc_cons[1][2] += f"{eva_pt_other}"
                    bond.matching_conditions[0][2]["value"].append(str(0))
                    bond.matching_conditions[1][2]["value"].append(str(0))
                if isinstance(bond, LinearSpringMC):  # due to the implementation in the frontend, this is necessary for the linear spring MC
                    bond.matching_conditions[id_mc][3]["value"].append(str(0))
                
                if beam.position_list[pos_id] == connection.position_list[(not pos_id)]:
                    sign_rigid = False
                else:
                    sign_rigid = True

                bond.matching_conditions[id_mc][1]["value"].append([sign_rigid, "rigid_beam"])
                
                # append the moment due to the shear force to the moment condition if there is no bearing connection; the bearing connection sits at "other_pos"
                other_pos = [po for po in connection.position_list if po not in bond.position_list][0]
                if any(isinstance(con, BearingConnection) for con in other_pos.connection_list):
                    if isinstance(bond, LinearSpringMC): # if the bond is a linear spring mc, update the deflection (at the linear spring)
                        bond.mc_cons[id_mc][3] = f"{translate_plus_minus((not sign_rigid))}{connection.length}\\,\\varphi{bond.eva_pt[id_mc]}"
                        bond.deflection[id_mc] = bond.mc_cons[id_mc][3]
                else: # if there is no bearing connection that set the shear force based on sign rigid
                    bond.mc_cons[id_mc][1] += f"{translate_plus_minus((sign_rigid))}Q{bond.eva_pt[id_mc]}\\,{connection.length}"
                    bond.mc_cons[id_mc][3] += f"{translate_plus_minus((not sign_rigid))}{connection.length}\\,\\varphi{bond.eva_pt[id_mc]}"
                
                bond.matching_conditions[id_mc][3]["value"].append([not sign_rigid, "rigid_beam"])
                
                for pos in connection.position_list:
                    for con in pos.connection_list:
                        if not con.in_condition_considered:
                            con.in_condition_considered = True
                            
                            if isinstance(con, LinearSpring):
                                if pos == position: # the linear spring is at the beam (and separated from the bond via the rigid beam)
                                    
                                    addition_for_shear_force = ""
                                    # the determination of the sign was taken from above
                                    if not id_mc: # negative cross section, position_list[0] in bond
                                        sign_linear_spring = True # the spring force is always showing "up" (against default z)
                                    else:
                                        sign_linear_spring = False
                                    if not beam.coordinate_system_orientation:
                                        sign_linear_spring = not sign_linear_spring # the sign needs to be changed, when the orientation is flipped
                                    
                                    # it seems that the moment is always positive
                                    bond.matching_conditions[id_mc][1]["value"].append([True, "linear_spring"])
                                    # append the shear force due to the linear spring to the shear force condition
                                    bond.mc_cons[id_mc][0] += f"{translate_plus_minus(sign_linear_spring)}{con.spring_constant}\\,w{bond.eva_pt[id_mc]}"
                                    # append the moment due to the linear spring to the moment condition
                                    bond.mc_cons[id_mc][1] += f"{translate_plus_minus(True)}{con.spring_constant}\\,w{bond.eva_pt[id_mc]}\\,{connection.length}"
                                else: # the linear spring is directly at the bond
                                    addition_for_shear_force = "_rigid" 

                                    sign_linear_spring = sign_rigid
                                    if not beam.coordinate_system_orientation:  # the change of the sign with the following two ifs was trial and error
                                        sign_linear_spring = not sign_linear_spring
                                    if not beam.coordinate_system_position:
                                        sign_linear_spring = not sign_linear_spring
                                    # append the shear force due to the linear spring to the shear force condition
                                    bond.mc_cons[id_mc][0] += f"{translate_plus_minus(sign_linear_spring)}{con.spring_constant}\\,\\left[{translate_plus_minus((bond.beam_direction[id_mc]))}{bond.mc_cons[id_mc][3]['condition']}\\right]"

                                bond.matching_conditions[id_mc][0]["value"].append([sign_linear_spring, "linear_spring"+addition_for_shear_force])
                                
                            elif isinstance(con, SingleForce):
                                if not id_mc:
                                    sign_force = False
                                else:
                                    sign_force = True
                                if not con.positive:
                                    sign_force = not sign_force
                                bond.matching_conditions[id_mc][0]["value"].append([sign_force, "single_force"])
                                bond.mc_cons[id_mc][0] += f"{translate_plus_minus(sign_force)}{con.symbol}"

                                sign_moment = not con.positive
                                if not beam.coordinate_system_orientation:
                                    sign_moment = not sign_moment
                                if pos == position:
                                    bond.matching_conditions[id_mc][1]["value"].append([sign_moment, "single_force"])
                                    bond.mc_cons[id_mc][1] += f"{translate_plus_minus(sign_moment)}{con.symbol}\\,{connection.length}"
                                else:
                                    if any(isinstance(conne, BearingConnection) for conne in position.connection_list):
                                        bond.mc_cons[id_mc][1] += f"{translate_plus_minus(not sign_moment)}{con.symbol}\\,{connection.length}"
                                        
                            elif isinstance(con, TorsionalSpring):
                                sign_torsional_spring = sign_rigid
                                if not beam.coordinate_system_orientation:  # is necessary due to the change of the sign above (with not beam.coordinate_system_orientation)
                                    sign_torsional_spring = not sign_torsional_spring
                                bond.matching_conditions[id_mc][1]["value"].append([sign_torsional_spring, "torsional_spring"])
                                bond.mc_cons[id_mc][1] += f"{translate_plus_minus((sign_torsional_spring))}{con.spring_constant}\\,\\varphi{bond.eva_pt[id_mc]}"
                                
                            elif isinstance(con, SingleMoment):
                                if not id_mc:
                                    sign_moment = False
                                else:
                                    sign_moment = True
                                if not cross_section_is_default:
                                    sign_moment = not sign_moment
                                if not beam.coordinate_system_position:
                                    sign_moment = not sign_moment # the sign needs to be changed, when the coordinate system is on the other side
                                if not con.positive:
                                    sign_moment = not sign_moment # the sign needs to be changed, when the moment is negative

                                bond.matching_conditions[id_mc][1]["value"].append([sign_moment, "single_moment"])
                                bond.mc_cons[id_mc][1] += f"{translate_plus_minus(sign_moment)}{con.symbol}"

                            elif isinstance(con, BearingConnection):
                                bond.with_bearing[id_mc] = True
                                
                                # set the evaluation point for the angle condition - needed for bearing connection at both sides
                                bond.mc_cons[id_mc][2] += f"{bond.eva_pt[id_mc]}"
                                
                                for pos in bond.position_list:
                                    if pos.beam_list:
                                        if pos.beam_list[0] != beam:
                                            other_beam = pos.beam_list[0]
                                    else:
                                        for conne in pos.connection_list:
                                            if isinstance(conne, RigidBeam):
                                                if conne.beam_list[0] != beam:
                                                    other_beam = conne.beam_list[0]
                                
                                if isinstance(bond, LinearSpringMC):
                                    if beam.coordinate_system_position:
                                        sign_moment = not sign_rigid
                                    else:
                                        sign_moment = sign_rigid
                                    
                                    bond.rigid_lever = f"{connection.length}"
                                    bond.moment_sign[id_mc] = sign_moment
                                    bond.deflection[id_mc] = bond.mc_cons[id_mc][3]['condition']
                                    
                                    bond.matching_conditions[id_mc][1]["value"].append([sign_moment, "bearing_connection"])
                                    bond.matching_conditions[id_mc][3]["value"].append([not sign_rigid, "bearing_connection"])
                                    
                                else:
                                    bearing_con_other_side = False
                                    if isinstance(bond, RigidConnection):
                                        bond_other_pos = bond.position_list[not id_mc]
                                    else: # isinstance(bond, Joint)
                                        bond_other_pos = bond.position_list[0]
                                    for conne in bond_other_pos.connection_list:
                                        if isinstance(conne, RigidBeam):
                                            if conne != connection:
                                                other_pos = [po for po in conne.position_list if po not in bond.position_list][0]
                                                if any(isinstance(connec, BearingConnection) for connec in other_pos.connection_list):
                                                    bearing_con_other_side = True
                                    if beam.coordinate_system_orientation:
                                        sign_moment = other_beam.coordinate_system_position
                                    else:
                                        sign_moment = not other_beam.coordinate_system_position
                                    if not other_beam.coordinate_system_orientation:
                                        sign_moment = not sign_moment
                                    if not bearing_con_other_side:
                                        if not id_mc:
                                            eva_pt_other = f"(x_{other_beam.beam_index}={determine_position(other_beam, bond)[0]})"
                                            bond.mc_cons[id_mc][1] += f"{translate_plus_minus(sign_moment)}Q{eva_pt_other}\\,{connection.length}"
                                            bond.mc_cons[id_mc][3] = f"{translate_plus_minus((not sign_rigid))}{connection.length}\\,\\varphi{bond.eva_pt[id_mc]}"
                                        else:
                                            bond.mc_cons[id_mc][1] += f"{translate_plus_minus(not sign_moment)}Q{bond.eva_pt[not id_mc]}\\,{connection.length}"
                                            bond.mc_cons[id_mc][3] = f"{translate_plus_minus((not sign_rigid))}{connection.length}\\,\\varphi{bond.eva_pt[id_mc]}"
                                                
                                    bond.matching_conditions[id_mc][3]["value"].append([sign_rigid, "bearing_connection"])
                                    if not id_mc:
                                        bond.matching_conditions[id_mc][1]["value"].append([sign_moment, "bearing_connection"])
                                    else:
                                        bond.matching_conditions[id_mc][1]["value"].append([not sign_moment, "bearing_connection"])
                                if beam.coordinate_system_orientation:
                                    bond.matching_conditions[id_mc][1]["value"].remove([sign_rigid, "rigid_beam"])  # the moment condition is different, therefore it is removed
                                else:
                                    try:
                                        bond.matching_conditions[id_mc][1]["value"].remove([not sign_rigid, "rigid_beam"])  # the moment condition is different, therefore it is removed
                                    except:
                                        pass
                                
                                bond.matching_conditions[id_mc][3]["value"].remove([not sign_rigid, "rigid_beam"])  # the deflection condition is different, therefore it is removed

                                
                            elif isinstance(con, RigidBeam): # i think this is just necessary for the joint
                                con.in_condition_considered = False 
                # else:
                #     connection.in_condition_considered = False 
                    

def determine_position(beam, bond):
    """this function determines 'where we are' considering the beam and the bond"""
    
    rigid = False
    rigid_beam = None
    position = None
    position_intersection = [pos for pos in beam.position_list if pos in bond.position_list]
    if not position_intersection:  # there is a rigid beam between the bond and the beam
        for posi in bond.position_list:
            for con in posi.connection_list:
                if isinstance(con, RigidBeam):
                    other_pos = [po for po in con.position_list if po not in bond.position_list][0]
                    if any(other_pos == p for p in beam.position_list):
                        rigid_beam = con
                        rigid = True
                        position_int = [rpos for rpos in beam.position_list if rpos in rigid_beam.position_list]
                        if position_int:
                            position = position_int[0]
                        break
    else:
        position = position_intersection[0]

    if beam.coordinate_system_position:
        pos_id = 0
    else:
        pos_id = 1

    if position == beam.position_list[pos_id]:
        x_position = 0
        sign_cross_section = True  # positive cross section; default "sign" is positive = True
    else:
        x_position = beam.length
        sign_cross_section = False  # negative cross section; default "sign" is negative = False
    
    return x_position, sign_cross_section, position, pos_id, rigid, rigid_beam

                    
def translate_empty_minus(boolean):
    """this functions translates a boolean value into a string value of '' and '-'"""
    
    if boolean:
        return ""
    else:
        return "-"

    
def translate_plus_minus(boolean):
    """this functions translates a boolean value into a string value of '+' and '-'"""
    
    if boolean:
        return "+"
    else:
        return "-"


class Truss:
    """this class is the base class for beams and rigid beams"""

    def __init__(self, position_list):
        self.position_list = position_list
        self.bond_list = []
        self.connection_list = []

    def add_connection(self, new_connection):
        """this method adds a connection to the connection list"""
        
        if self.connection_list:
            if not (any(new_connection == c for c in self.connection_list)):
                self.connection_list.append(new_connection)
        else:
            self.connection_list.append(new_connection)

    def add_bond(self, new_bond):
        """this method adds a bond to the bond list"""
        
        if self.bond_list:
            if not any(new_bond == b for b in self.bond_list):
                self.bond_list.append(new_bond)
        else:
            self.bond_list.append(new_bond)


class Beam(Truss):
    """this class is the class for beams"""
    
    symbolic_length = sp.symbols("l")
    
    def __init__(self, position_list, coordinate_system_position, coordinate_system_orientation):
        super().__init__(position_list)
        self.position_list = position_list
        self.length = self.set_length(position_list)
        self.coordinate_system_position = coordinate_system_position
        self.coordinate_system_orientation = coordinate_system_orientation

        # ansatz of ode
        self.line_load = ""#self.determine_correct_symbolic_line_load(line_load)  # streckenlast
        self.shear_force = ""#self.set_shear_force_of_x()
        self.moment = ""#self.set_moment_of_x()
        self.angle_phi = ""#self.set_angle_phi_of_x()
        self.deflection = ""#self.set_deflection_of_x()

        self.beam_index = 0

        self.bcs = []
        self.mcs = []

    
    def set_length(self, positions):
        """this method calculates and sets the length of the beam"""
        return sp.nsimplify(abs(positions[0].x_coordinate - positions[1].x_coordinate), constants=[sp.sqrt(2), sp.sqrt(3)]) * self.symbolic_length
    
    
    def determine_correct_symbolic_line_load(self, line_load_string):
        """this method returns the symbolic line load based on the committed string"""
        
        q_0 = sp.symbols("q_0")
        x_i = sp.symbols(f"x_{self.beam_index}")
        l = self.length
        
        if line_load_string == "":
            return 0
        elif line_load_string == "constant":
            return q_0
        elif line_load_string == "linear_ascending":
            return q_0/l*x_i
        elif line_load_string == "linear_descending":
            return q_0*(1-x_i/l)


    def calc_ansatz_for_ODE_of_beam(self, line_load):
        """this method calculates and sets the ansatz for the ode of the beam"""
        
        x_i = sp.symbols(f"x_{self.beam_index}")
        
        self.line_load = self.determine_correct_symbolic_line_load(line_load)
        self.shear_force = sp.integrate(self.line_load, x_i)
        self.moment = sp.integrate(self.shear_force, x_i)
        self.angle_phi = sp.integrate(self.moment, x_i)
        self.deflection = sp.integrate(self.angle_phi, x_i)
        

class RigidBeam(Truss):
    """this class is the class for rigid beams"""
    
    constraints = [True, True, True, True]  # don't know if this is correct, is needed for the calculation
    
    symbolic_length = sp.symbols("a")

    def __init__(self, position_list):
        super().__init__(position_list)
        self.length = self.set_length(position_list)
        self.bond = False
        self.beam_list = []
        self.in_condition_considered = False


    def set_length(self, positions):
        """this method calculates and sets the length of the rigid beam"""
        return sp.nsimplify(abs(positions[0].x_coordinate - positions[1].x_coordinate),
                            constants=[sp.sqrt(2), sp.sqrt(3)]) * self.symbolic_length*sp.Rational(3,2) # multiply by 3/2 so that the default length is "a"


    def add_beam(self, new_beam):
        """this method adds a beam to the beam list"""
        if self.beam_list:
            if not any(new_beam == b for b in self.beam_list):
                self.beam_list.append(new_beam)
        else:
            self.beam_list.append(new_beam)


class Connection:
    """this class is the base class of connections (every other element but beams)"""
    
    bond = False

    def __init__(self, position_list):
        self.position_list = position_list
        self.beam_list = []
        self.in_condition_considered = False


    def add_beam(self, new_beam):
        """this method adds a beam to the beam list"""
        if self.beam_list:
            if not any(new_beam == b for b in self.beam_list):
                self.beam_list.append(new_beam)
        else:
            self.beam_list.append(new_beam)


class BoundaryConditionSymbol(Connection):
    """this class is the base class of boundary condition elements"""
    
    bond = True

    def __init__(self, position_list):
        super().__init__(position_list)
        # self.bc_position = {"position": ""}
        # self.bc_conditions = [{"condition": "Q", "value": []},
        #                       {"condition": "M", "value": []},
        #                       {"condition": "\\varphi", "value": []},
        #                       {"condition": "w", "value": []}]
        self.eva_pt = "" # evaluation point, is set in set_up_boundary_conditions
        
        self.bc_cons = ["Q","M","\\varphi","w"]


class FixedBearing(BoundaryConditionSymbol):
    """this class is for fixed bearings (='Festlager')"""
    
    constraints = [False, True, False, True]

    def __init__(self, position_list):
        super().__init__(position_list)


class FloatingBearing(BoundaryConditionSymbol):
    """this class is for floating bearings (='Loslager')"""
    
    constraints = [False, True, False, True]

    def __init__(self, position_list):
        super().__init__(position_list)


class RigidSupport(BoundaryConditionSymbol):
    """this class is for rigid supports (='feste Einspannung')"""
    
    constraints = [False, False, True, True]

    def __init__(self, position_list):
        super().__init__(position_list)


class GuidedSupportVertical(BoundaryConditionSymbol):
    """this class is for guided supports (vertical) (='Parallelfuehrung')"""
    
    constraints = [True, False, True, False]

    def __init__(self, position_list):
        super().__init__(position_list)


class FreeEnd(BoundaryConditionSymbol):
    """this class is for free ends (='freies Ende')"""
    
    constraints = [True, True, False, False]

    def __init__(self, position_list):
        super().__init__(position_list)


class TorsionalSpring(Connection):
    """this class is for torsional springs (='Drehfeder')"""
    
    constraints = [False, False, True, False]
    
    spring_constant = sp.symbols("k_\\varphi")

    def __init__(self, position_list):
        super().__init__(position_list)


class LinearSpring(Connection):
    """this class is for linear springs (='Wegfeder')"""
    
    constraints = [False, False, True, True]
    
    spring_constant = sp.symbols("k_w")

    def __init__(self, position_list):
        super().__init__(position_list)


class SingleMoment(Connection):
    """this class is for single moments (='Einzelmoment')"""
    
    constraints = [False, False, False, False]
    
    symbol = sp.symbols("M")
    
    def __init__(self, position_list, positive):
        super().__init__(position_list)
        self.positive = positive  # True = counter-clockwise, False = clockwise


class SingleForce(Connection):
    """this class is for single forces (='Einzelkraefte')"""
    
    constraints = [False, False, False, False]
    
    symbol = sp.symbols("F")

    def __init__(self, position_list, positive):
        super().__init__(position_list)
        self.positive = positive  # True = in positive z-direction ('down'), False = against z


class BearingConnection(Connection):
    """this class is for bearing connections"""

    def __init__(self, position_list, forces):
        super().__init__(position_list)
        self.forces = forces  # for calculation of degree of indeterminacy, 1 for floating, 2 for fixed


class MatchingConditionSymbol(Connection):
    """base class of matching condition elements"""
    
    bond = True
    
    def __init__(self, position_list):
        super().__init__(position_list)

        self.eva_pt = ["", ""] # evaluation point, is set in set_up_matching_conditions, # 0: negative cross section 1: positive cross section
        self.mc_position = [{"position": "", "index": ""}, {"position": "", "index": ""}] # 0: negative cross section 1: positive cross section
        self.cross_sections_default = [True, True] # 0: negative cross section 1: positive cross section

        # the first entry (0) is the negative cross section, the second entry is the positive cross section
        self.matching_conditions = [[{"condition": "Q", "value": []},
                                     {"condition": "M", "value": []},
                                     {"condition": "\\varphi", "value": []},
                                     {"condition": "w", "value": []}],
                                    [{"condition": "Q", "value": []},
                                     {"condition": "M", "value": []},
                                     {"condition": "\\varphi", "value": []},
                                     {"condition": "w", "value": []}]]
        self.mc_cons = [["Q","M","\\varphi","w"],
                        ["Q","M","\\varphi","w"]]
        self.with_bearing = [False, False]
        self.beam_direction = [True, True] # is needed inter alia for displacement conditions
        self.rigid_lever = "" # needed for the matching conditions of bearing connections


class Joint(MatchingConditionSymbol):
    """this class is for joints (='Gelenk')"""
    
    constraints = [True, True, False, True]

    def __init__(self, position_list):
        super().__init__(position_list)


class RigidConnection(MatchingConditionSymbol):
    """this class is for rigid connections (='starre Verbindung')"""
    
    constraints = [True, True, False, True]

    def __init__(self, position_list):
        super().__init__(position_list)


class LinearSpringMC(MatchingConditionSymbol):
    """this class is for linear springs placed as matching condition (=Übergangsbedingung')"""
    
    constraints = [True, True, False, False]
    
    spring_constant = sp.symbols("k_w")
    
    def __init__(self, position_list):
        super().__init__(position_list)
        self.deflection = ["",""] # 0 is negative cross section, 1 is positive cross section
        self.moment_sign = ["",""] # 0 is negative cross section, 1 is positive cross section
        self.shear_force_sign = ["",""] # 0 is negative cross section, 1 is positive cross section


class FixedBearingMC(MatchingConditionSymbol):
    """this class is for fixed bearings placed as matching condition (=Übergangsbedingung')"""
    
    constraints = [False, True, False, True]

    def __init__(self, position_list):
        super().__init__(position_list)


class FloatingBearingMC(MatchingConditionSymbol):
    """this class is for flaoting bearings placed as matching condition (=Übergangsbedingung')"""
    
    constraints = [False, True, False, True]

    def __init__(self, position_list):
        super().__init__(position_list)


class RigidBeamMC(MatchingConditionSymbol):
    """this class is for rigid beams placed as matching condition (=Übergangsbedingung)"""
    
    constraints = [True, True, True, True]
    
    symbolic_length = sp.symbols("a")

    def __init__(self, position_list):
        super().__init__(position_list)
        self.length = self.set_length(position_list)
     
        
    def set_length(self, positions):
        """this method calculates and sets the length of the rigid beam"""
        return sp.nsimplify(abs(positions[0].x_coordinate - positions[1].x_coordinate),
                            constants=[sp.sqrt(2), sp.sqrt(3)]) * self.symbolic_length*sp.Rational(3,2) # multiply by 3/2 so that the default length is "a"


class Position:
    """this class specifies all the positions in the system"""

    def __init__(self, coordinates):
        self.x_coordinate = coordinates[0]
        self.z_coordinate = coordinates[1]
        self.beam_list = []
        self.bond_list = []
        self.connection_list = []

    def __eq__(self, other):
        return abs(self.x_coordinate - other.x_coordinate) < 1e-3 and abs(self.z_coordinate - other.z_coordinate) < 1e-3

    def add_beam(self, new_beam):
        """adds a beam to the beam list"""
        self.beam_list.append(new_beam)


    def add_bond(self, new_bond):
        """adds a bond (='Bindung') to the bond list"""
        self.bond_list.append(new_bond)


    def add_connection(self, new_connection):
        """adds a connection (='Connection') to the connection list"""
        self.connection_list.append(new_connection)
        