import sympy as sp
from classes import RigidBeamMC, Joint, RigidConnection, LinearSpringMC, MatchingConditionSymbol


def data_for_ansatz_ode(system):
    """this function extracts the data for the display of the ansatz for the frontend"""
    data_list = []

    for idx, beam in enumerate(system.beam_list):
        x_i = beam.beam_index
        C_i = idx*4 + 1 # index of first constant of beam (others are iterated in f-string)
        if sp.latex(beam.line_load) != "0": # the vphantom command helps to get the same height for each line of the ansatz
            ansatz = f"\\begin{{align}} \
                EIw''''(x_{{{x_i}}})&={sp.latex(beam.line_load)}&&=q(x_{{{x_i}}}) \\vphantom{{\\frac{{1}}{{2}}}} \\\\ \
                    EIw'''(x_{{{x_i}}})&={sp.latex(beam.shear_force)}+C_{{{C_i}}}&&=-Q(x_{{{x_i}}}) \\vphantom{{\\frac{{1}}{{2}}}} \\\\ \
                        EIw''(x_{{{x_i}}})&={sp.latex(beam.moment)}+C_{{{C_i}}}x_{{{x_i}}} + C_{{{C_i+1}}}&&=-M(x_{{{x_i}}}) \\\\ \
                            EIw'(x_{{{x_i}}})&={sp.latex(beam.angle_phi)}+C_{{{C_i}}}\\frac{{x_{{{x_i}}}^2}}{{2}} + C_{{{C_i+1}}}x_{{{x_i}}} + C_{{{C_i+2}}}&&=-\\varphi(x_{{{x_i}}}) \\\\ \
                                EIw(x_{{{x_i}}})&={sp.latex(beam.deflection)}+C_{{{C_i}}}\\frac{{x_{{{x_i}}}^3}}{{6}} + C_{{{C_i+1}}}\\frac{{x_{{{x_i}}}^2}}{{2}} + C_{{{C_i+2}}}+C_{{{C_i+3}}} \
                                    \\end{{align}}"
        else:
            ansatz = f"\\begin{{align}} \
                EIw''''(x_{{{x_i}}})&=0&&=q(x_{{{x_i}}}) \\vphantom{{\\frac{{1}}{{2}}}} \\\\ \
                    EIw'''(x_{{{x_i}}})&=C_{{{C_i}}}&&=-Q(x_{{{x_i}}}) \\vphantom{{\\frac{{1}}{{2}}}} \\\\ \
                        EIw''(x_{{{x_i}}})&=C_{{{C_i}}}x_{{{x_i}}} + C_{{{C_i+1}}}&&=-M(x_{{{x_i}}}) \\vphantom{{\\frac{{1}}{{2}}}} \\\\ \
                            EIw'(x_{{{x_i}}})&=C_{{{C_i}}}\\frac{{x_{{{x_i}}}^2}}{{2}} + C_{{{C_i+1}}}x_{{{x_i}}} + C_{{{C_i+2}}}&&=-\\varphi(x_{{{x_i}}}) \\\\ \
                                EIw(x_{{{x_i}}})&=C_{{{C_i}}}\\frac{{x_{{{x_i}}}^3}}{{6}} + C_{{{C_i+1}}}\\frac{{x_{{{x_i}}}^2}}{{2}} + C_{{{C_i+2}}}+C_{{{C_i+3}}} \
                                    \\end{{align}}"
        data_list.append(ansatz)

    return data_list


def data_bc(system):
    """this function extracts all boundary conditions for the display in the frontend"""
    
    data_list = []
    for bond in system.bond_list:
        if not isinstance(bond, MatchingConditionSymbol):
            conditions = f"\\begin{{align}}{get_symbolic_condition(bond)}\\end{{align}}"
            data_list.append(conditions)
    return data_list
    

def get_symbolic_condition(bond):
    conditions = ""
    for index, entry in enumerate(bond.constraints):
        if entry:
            conditions += f"{bond.bc_cons[index]} &= 0 \\\\"
    return conditions


def data_mc(system):
    """this function extracts all matching conditions for the display in the frontend"""
    
    data_list = []
    for bond in system.bond_list:
        if isinstance(bond, MatchingConditionSymbol):
            conditions = f"\\begin{{align}}{get_symbolic_condition_mc(bond)}\\end{{align}}"
            data_list.append(conditions)
    print(data_list)
    return data_list
    

def get_symbolic_condition_mc(bond):
    """this function gets the symbolic matching condition based on the instance of the object"""
    
    conditions = ""
    for index, entry in enumerate(bond.constraints_frontend):
        if entry:
            if isinstance(bond, RigidConnection) or isinstance(bond, Joint):
                if bond.with_bearing: # it is a rigid connection with at least one bearing at a rigid beam
                    if index != 0: # there is no condition for the shear force
                        if index != 3:
                            for i in (0,1):
                                conditions += bond.mc_cons[i][index]["condition"] + "&=0 \\\\"
                        else:
                            print(bond.beam_direction)
                            for i in (0,1):
                                conditions += translate_boolean(bond.beam_direction[i]) + bond.mc_cons[i][index]["condition"] + "&=0 \\\\"
                else: # regular rigid connection
                    if index != 1: # all conditions except for the moment condition
                        if index == 3: # for shear force and the deflection the sign can be changed due to the orientation of the coordinate system
                            conditions += translate_boolean(bond.beam_direction[0]) + bond.mc_cons[0][index]["condition"] + "&=" \
                                + translate_boolean(bond.beam_direction[1]) + bond.mc_cons[1][index]["condition"] + "\\\\"
                        elif index == 0:
                            conditions += translate_boolean(bond.cross_sections_default[0]) + bond.mc_cons[0][index]["condition"] + "&=" \
                                + translate_boolean(bond.cross_sections_default[1]) + bond.mc_cons[1][index]["condition"] + "\\\\"
                        else:
                            conditions += bond.mc_cons[0][index]["condition"] + "&=" + bond.mc_cons[1][index]["condition"] + "\\\\"
                    else: # moment conditions are set separately to zero
                        for i in (0,1):
                            conditions += bond.mc_cons[i][index]["condition"] + "&=0 \\\\"
            elif isinstance(bond, LinearSpringMC):
                if any(bond.with_bearing):
                    print(bond.with_bearing)
                    for i in range(len(bond.with_bearing)):
                        print(i)
                        if bond.with_bearing[i]:
                            if index==0: # set the respective shear force conditions
                                conditions += f"{translate_boolean(bond.cross_sections_default[not i])}{bond.mc_cons[not i][index]['condition']}&={bond.spring_constant}\\,\\left(\\left[{bond.mc_cons[1][3]['condition']}\\right] \
                                        -\\left[{bond.mc_cons[0][3]['condition']}\\right]\\right) \\\\"
                            if index==1: # set the moment conditions
                                conditions += bond.mc_cons[not i][index]["condition"] + "&=0 \\\\"
                                conditions += bond.mc_cons[i][index]["condition"] + f"&={translate_boolean(bond.cross_sections_default[i])}{bond.spring_constant}\\,\\left(\\left[{bond.mc_cons[1][3]['condition']}\\right] \
                                        -\\left[{bond.mc_cons[0][3]['condition']}\\right]\\right)\\,{bond.rigid_lever} \\\\"
                            # plus set the deflection condition
                                conditions += f"{translate_boolean((bond.beam_direction[i]))}w{bond.eva_pt[i]}&=0 \\\\"    
                            
                else:
                    for i in (0,1):
                        if index == 1: # moment conditions are set separately to zero
                            conditions += bond.mc_cons[i][index]["condition"] + "&=0 \\\\"
                        else: # shear forces are set separately to the spring force
                            conditions += f"{translate_boolean(bond.cross_sections_default[i])}{bond.mc_cons[i][index]['condition']}&= \
                                {bond.spring_constant}\\,\\left(\\left[{translate_boolean((bond.beam_direction[1]))}{bond.mc_cons[1][3]['condition']}\\right] \
                                    -\\left[{translate_boolean((bond.beam_direction[0]))}{bond.mc_cons[0][3]['condition']}\\right]\\right) \\\\"
            elif isinstance(bond, RigidBeamMC):
                if index == 0: # consider sign of cross sections default for shear forces
                    conditions += f"{translate_boolean(bond.cross_sections_default[0])}{bond.mc_cons[0][index]['condition']}&={translate_boolean(bond.cross_sections_default[1])}{bond.mc_cons[1][index]['condition']} \\\\"
                elif index == 1: # for moments on the side of the negative cross section a minus is added, if the coordinate system z-directions are not the same for the beams
                    sign = ""
                    if bond.beam_direction[0] != bond.beam_direction[1]:
                        sign = "-"
                    conditions += f"{sign}{bond.mc_cons[0][index]['condition']}&={bond.mc_cons[1][index]['condition']} \\\\"
                elif index == 2: # for the angle on the side of the positive cross section a minus is added, if the default cross sections are not the same
                    sign = ""
                    if bond.cross_sections_default[0] != bond.cross_sections_default[1]:
                        sign = "-"
                    conditions += f"{bond.mc_cons[0][index]['condition']}&={sign}{bond.mc_cons[1][index]['condition']} \\\\"
                else: # index == 3; for the deflection consider the beam direction for the sign
                    conditions +=  f"{translate_boolean((bond.beam_direction[0]))}{bond.mc_cons[0][index]['condition']}&={translate_boolean((bond.beam_direction[1]))}{bond.mc_cons[1][index]['condition']} \\\\"
    return conditions
            
            
def translate_boolean(boolean):
    """this functions translates a boolean value into a string value of '' and '-'"""
    
    if boolean:
        return ""
    else:
        return "-"
