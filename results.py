import sympy as sp
from classes import RigidBeamMC, Joint, RigidConnection, LinearSpringMC, MatchingConditionSymbol, FixedBearingMC, FloatingBearingMC


def data_for_ansatz_ode(system):
    """this function extracts the data for the display of the ansatz for the frontend"""
    data_list = []

    for idx, beam in enumerate(system.beam_list):
        x_i = beam.beam_index
        C_i = idx*4 + 1 # index of first constant of beam (others are iterated in f-string)
        if sp.latex(beam.line_load) != "0": # the vphantom command helps to get the same height for each line of the ansatz
            if beam.thermal_load:
                ansatz = f"\\begin{{align}} \
                    (EIw''(x_{{{x_i}}})+EI{sp.latex(beam.material_alpha)})''&={sp.latex(beam.line_load)}&&=q(x_{{{x_i}}}) \\vphantom{{\\frac{{1}}{{2}}}} \\\\ \
                        (EIw''(x_{{{x_i}}})+EI{sp.latex(beam.material_alpha)})'&={sp.latex(beam.shear_force)}+C_{{{C_i}}}&&=-Q(x_{{{x_i}}}) \\vphantom{{\\frac{{1}}{{2}}}} \\\\ \
                            EIw''(x_{{{x_i}}})+EI{sp.latex(beam.material_alpha)}&={sp.latex(beam.moment)}+C_{{{C_i}}}x_{{{x_i}}} + C_{{{C_i+1}}}&&=-M(x_{{{x_i}}}) \\\\ \
                                w''(x_{{{x_i}}})&=\\frac{{1}}{{EI}}{sp.latex(beam.moment)}{sp.latex(beam.thermalMoment)}+\\frac{{1}}{{EI}}C_{{{C_i}}}x_{{{x_i}}} + \\frac{{1}}{{EI}}C_{{{C_i+1}}} \\\\ \
                                    w'(x_{{{x_i}}})&=\\frac{{1}}{{EI}}{sp.latex(beam.angle_phi)}{sp.latex(beam.thermalAngle)}+\\frac{{1}}{{EI}}C_{{{C_i}}}\\frac{{x_{{{x_i}}}^2}}{{2}} + \\frac{{1}}{{EI}}C_{{{C_i+1}}}x_{{{x_i}}} + \\frac{{1}}{{EI}}C_{{{C_i+2}}} \\\\ \
                                        w(x_{{{x_i}}})&=\\frac{{1}}{{EI}}{sp.latex(beam.deflection)}{sp.latex(beam.thermalDeflection)}+\\frac{{1}}{{EI}}C_{{{C_i}}}\\frac{{x_{{{x_i}}}^3}}{{6}} + \\frac{{1}}{{EI}}C_{{{C_i+1}}}\\frac{{x_{{{x_i}}}^2}}{{2}} + \\frac{{1}}{{EI}}C_{{{C_i+2}}}+\\frac{{1}}{{EI}}C_{{{C_i+3}}} \
                                            \\end{{align}}"
            else:
                 ansatz = f"\\begin{{align}} \
                    EIw''''(x_{{{x_i}}})&={sp.latex(beam.line_load)}&&=q(x_{{{x_i}}}) \\vphantom{{\\frac{{1}}{{2}}}} \\\\ \
                        EIw'''(x_{{{x_i}}})&={sp.latex(beam.shear_force)}+C_{{{C_i}}}&&=-Q(x_{{{x_i}}}) \\vphantom{{\\frac{{1}}{{2}}}} \\\\ \
                            EIw''(x_{{{x_i}}})&={sp.latex(beam.moment)}+C_{{{C_i}}}x_{{{x_i}}} + C_{{{C_i+1}}}&&=-M(x_{{{x_i}}}) \\\\ \
                                w''(x_{{{x_i}}})&=\\frac{{1}}{{EI}} {sp.latex(beam.moment)}+\\frac{{1}}{{EI}}C_{{{C_i}}}x_{{{x_i}}} + \\frac{{1}}{{EI}}C_{{{C_i+1}}}) \\\\ \
                                    w'(x_{{{x_i}}})&=\\frac{{1}}{{EI}}{sp.latex(beam.angle_phi)}+\\frac{{1}}{{EI}}C_{{{C_i}}}\\frac{{x_{{{x_i}}}^2}}{{2}} + \\frac{1}{{EI}}C_{{{C_i+1}}}x_{{{x_i}}} + \\frac{{1}}{{EI}}C_{{{C_i+2}}}) \\\\ \
                                        w(x_{{{x_i}}})&=\\frac{{1}}{{EI}}{sp.latex(beam.deflection)}+\\frac{{1}}{{EI}}C_{{{C_i}}}\\frac{{x_{{{x_i}}}^3}}{{6}} + \\frac{{1}}{{EI}}C_{{{C_i+1}}}\\frac{{x_{{{x_i}}}^2}}{{2}} + \\frac{{1}}{{EI}}C_{{{C_i+2}}}+\\frac{{1}}{{EI}}C_{{{C_i+3}}} \
                                            \\end{{align}}"
        else:
            if beam.thermal_load:
                ansatz = f"\\begin{{align}} \
                    EIw''''(x_{{{x_i}}})&=0&&=q(x_{{{x_i}}}) \\vphantom{{\\frac{{1}}{{2}}}} \\\\ \
                        EIw'''(x_{{{x_i}}})&=C_{{{C_i}}}&&=-Q(x_{{{x_i}}}) \\vphantom{{\\frac{{1}}{{2}}}} \\\\ \
                            EIw''(x_{{{x_i}}})&=C_{{{C_i}}}x_{{{x_i}}} + C_{{{C_i+1}}}&&=-M(x_{{{x_i}}}) \\vphantom{{\\frac{{1}}{{2}}}} \\\\ \
                                w''(x_{{{x_i}}})&=C_{{{C_i}}}x_{{{x_i}}} + \\frac{{1}}{{EI}}C_{{{C_i+1}}}) \\vphantom{{\\frac{{1}}{{2}}}} \\\\ \
                                    w'(x_{{{x_i}}})&=C_{{{C_i}}}\\frac{{x_{{{x_i}}}^2}}{{2}} + \\frac{{1}}{{EI}}C_{{{C_i+1}}}x_{{{x_i}}} + \\frac{{1}}{{EI}}C_{{{C_i+2}}}) \\\\ \
                                        w(x_{{{x_i}}})&=C_{{{C_i}}}\\frac{{x_{{{x_i}}}^3}}{{6}} + \\frac{{1}}{{EI}}C_{{{C_i+1}}}\\frac{{x_{{{x_i}}}^2}}{{2}} + \\frac{{1}}{{EI}}C_{{{C_i+2}}}+ \\frac{{1}}{{EI}}C_{{{C_i+3}}} \
                                            \\end{{align}}"
            else:
                ansatz = f"\\begin{{align}} \
                    EIw''''(x_{{{x_i}}})&=0&&=q(x_{{{x_i}}}) \\vphantom{{\\frac{{1}}{{2}}}} \\\\ \
                        EIw'''(x_{{{x_i}}})&=C_{{{C_i}}}&&=-Q(x_{{{x_i}}}) \\vphantom{{\\frac{{1}}{{2}}}} \\\\ \
                            EIw''(x_{{{x_i}}})&=C_{{{C_i}}}x_{{{x_i}}} + C_{{{C_i+1}}}&&=-M(x_{{{x_i}}}) \\vphantom{{\\frac{{1}}{{2}}}} \\\\ \
                                w''(x_{{{x_i}}})&=\\frac{{1}}{{EI}}C_{{{C_i}}}x_{{{x_i}}} + \\frac{{1}}{{EI}}C_{{{C_i+1}}}) \\vphantom{{\\frac{{1}}{{2}}}} \\\\ \
                                    w'(x_{{{x_i}}})&=\\frac{{1}}{{EI}}C_{{{C_i}}}\\frac{{x_{{{x_i}}}^2}}{{2}} + \\frac{{1}}{{EI}}C_{{{C_i+1}}}x_{{{x_i}}} + \\frac{{1}}{{EI}}C_{{{C_i+2}}}) \\\\ \
                                        w(x_{{{x_i}}})&=\\frac{{1}}{{EI}}C_{{{C_i}}}\\frac{{x_{{{x_i}}}^3}}{{6}} + \\frac{{1}}{{EI}}C_{{{C_i+1}}}\\frac{{x_{{{x_i}}}^2}}{{2}} + \\frac{{1}}{{EI}}C_{{{C_i+2}}}+ \\frac{{1}}{{EI}}C_{{{C_i+3}}} \
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
    """this function gets the symbolic boundary condition based on the instance of the object"""
    
    conditions = ""
    for index, entry in enumerate(bond.constraints):
        if entry:
            conditions += f"{bond.bc_cons[index]} &= 0 \\\\"
    return conditions


def data_bc_evaluated(system):
    """this function extracts all boundary conditions for the display in the frontend"""
    
    data_list = []
    for bond in system.bond_list:
        if not isinstance(bond, MatchingConditionSymbol):
            conditions = f"\\begin{{align}}{get_evaluated_condition(bond)}\\end{{align}}"
            data_list.append(conditions)
    return data_list


def get_evaluated_condition(bond):
    """this function gets the symbolic boundary condition based on the instance of the object"""
    
    conditions = ""
    for index, entry in enumerate(bond.constraints):
        if entry:
            conditions += f"{sp.latex(sp.collect(sp.expand(bond.evaluated_cons_lhs[index]), {'C_1', 'C_2', 'C_3', 'C_4', 'C_5', 'C_6', 'C_7', 'C_8'}))} &= {sp.latex(bond.evaluated_cons_rhs[index])} \\\\"
    return conditions


def data_mc(system):
    """this function extracts all matching conditions for the display in the frontend"""
    
    data_list = []
    data_list_matching=[]
    for bond in system.bond_list:
        if isinstance(bond, MatchingConditionSymbol):
            conditions, conditions_mc =get_symbolic_condition_mc(bond)
            conditions = f"\\begin{{align}}{conditions}\\end{{align}}"
            conditions_mc = f"\\begin{{align}}{conditions_mc}\\end{{align}}"
            data_list.append(conditions)
            data_list_matching.append(conditions_mc)
    return data_list, data_list_matching
    

def get_symbolic_condition_mc(bond):
    """this function gets the symbolic matching condition based on the instance of the object"""
    b = True
    conditions = ""
    conditions_mc = ""
    for index, entry in enumerate(bond.constraints):
        if entry:
            if isinstance(bond, RigidConnection) or isinstance(bond, Joint):
                if all(bond.with_bearing): # at both sides there is a bearing connection
                    if index == 1: # set the moment condition
                        moment_sign = "+"
                        if bond.beam_direction[0] != bond.beam_direction[1]:
                            moment_sign = "-"
                        conditions += f"{bond.mc_cons[0][index]}{moment_sign}\\left({bond.mc_cons[1][index]}\\right) &= 0\\\\"
                        conditions_mc += f"{bond.evaluated_cons_lhs[0][index]}\\left({bond.evaluated_cons_lhs[1][index]}\\right) &= 0\\\\"
                        print(conditions_mc)
                        print("Fertig")
                    if index == 3: # set the deflection conditions
                        # set the angle condition
                        sign_angle = "-"
                        if bond.cross_sections_default[0] != bond.cross_sections_default[1]:
                            sign_angle = ""
                        conditions += bond.mc_cons[0][2] + "&=" + sign_angle + bond.mc_cons[1][2] + "\\\\"
                        conditions_mc += bond.evaluated_cons_lhs[0][2] + "&=" + bond.evaluated_cons_rhs[1][2] + "\\\\"
                        print(conditions_mc)
                        print("Fertig")
                        for i in (0,1):
                                conditions += bond.mc_cons[i][index] + "&=0 \\\\"
                                conditions_mc += bond.evaluated_cons_lhs[i][index] + "&=" + bond.evaluated_cons_lhs[i][index] + "\\\\"
                                print(conditions_mc)
                                print("Fertig")

                elif any(bond.with_bearing): # there is a bearing connection either on one side
                    if index != 0: # there is no condition for the shear force
                        if index != 3:
                            for i in (0,1):
                                conditions += bond.mc_cons[i][index] + "&=0 \\\\"
                                conditions_mc += bond.evaluated_cons_lhs[i][index] + "&=" + bond.evaluated_cons_rhs[i][index] + "\\\\"
                                print(conditions_mc)
                                print("Fertig")
                        else: # deflection conditions
                            for i in range(len(bond.with_bearing)):
                                if bond.with_bearing[i]:
                                    conditions += bond.mc_cons[not i][index] + "&=" + bond.mc_cons[i][index] +"\\\\"
                                    conditions_mc += bond.evaluated_cons_lhs[not i][index] + "&=" + bond.evaluated_cons_rhs[i][index] + "\\\\"
                                    print(conditions_mc)
                                    print("Fertig")
                                    conditions += f"{translate_empty_minus((bond.beam_direction[i]))}w{bond.eva_pt[i]}&=0 \\\\"
                else: # there is no bearing connection
                    if index == 0: # set shear force condition
                        conditions += translate_empty_minus(bond.cross_sections_default[0]) + bond.mc_cons[0][index] + "&=" \
                            + translate_empty_minus(bond.cross_sections_default[1]) + bond.mc_cons[1][index] + "\\\\"
                        
                        conditions_mc += f"{get_evaluated_condition_mc(sign_evaluation(bond.cross_sections_default[0])*bond.evaluated_cons_lhs[0][index]-sign_evaluation(bond.cross_sections_default[1])*bond.evaluated_cons_lhs[1][index])}" + "&=" + f"{get_evaluated_condition_mc(sign_evaluation(bond.cross_sections_default[0])*bond.evaluated_cons_rhs[0][index]-sign_evaluation(bond.cross_sections_default[1])*bond.evaluated_cons_rhs[1][index])}" + "\\\\" #Hier Mal Kucken
                        # print(conditions_mc)
                        # print("Fertig")
                    elif index == 1: # set moment conditions separately to zero
                        for i in (0,1):
                            conditions += bond.mc_cons[i][index] + "&=0 \\\\"
                            conditions_mc += f"{get_evaluated_condition_mc(bond.evaluated_cons_lhs[i][index])}" + "&=" f"{get_evaluated_condition_mc(bond.evaluated_cons_rhs[i][index])}" + "\\\\" # passt
                            # print(conditions_mc)
                            # print("Fertig")
                    elif index == 3: # set the deflection condition
                        conditions += bond.mc_cons[0][index] + "&=" + bond.mc_cons[1][index] + "\\\\"
                        conditions_mc += f"{get_evaluated_condition_mc(bond.evaluated_cons_lhs[0][index]-bond.evaluated_cons_lhs[1][index])}" + "&=" + f"{get_evaluated_condition_mc(bond.evaluated_cons_rhs[0][index]-bond.evaluated_cons_rhs[1][index])}" + "\\\\"
                        # print(conditions_mc)
                        # print("Fertig")
                     
            elif isinstance(bond, LinearSpringMC):
                if all(bond.with_bearing): # at both sides there is a bearing connection
                    # set the moment conditions
                    if index==1: # set the moment conditions
                        for i in (0,1):
                            conditions += bond.mc_cons[i][index] + f"{translate_plus_minus(bond.moment_sign[i])}{bond.spring_constant}\\left(\\left[{bond.deflection[1]}\\right]-\\left[{bond.deflection[0]}\\right]\\right)\\,{bond.rigid_lever} &= 0 \\\\"
                            conditions_mc += f"{-bond.evaluated_cons_lhs[0][index]}"+ f"{bond.evaluated_cons_lhs[0][index]}{bond.spring_constant}+{bond.evaluated_cons_lhs[1][index]}{bond.spring_constant}" + "&=" + f"{bond.evaluated_cons_rhs[0][index]}" + "\\\\"
                            print(conditions_mc)

                            print("Fertig")
                        # plus set the deflection condition
                            conditions += f"{translate_empty_minus((bond.beam_direction[i]))}w{bond.eva_pt[i]}&=0 \\\\"
                            
                            print("Fertig")

                elif any(bond.with_bearing): # there is a bearing connection either on one side
                    for i in range(len(bond.with_bearing)):
                        if bond.with_bearing[i]:
                            if index==0: # set the respective shear force conditions
                                conditions += f"{bond.mc_cons[not i][index]}{translate_plus_minus(not bond.cross_sections_default[not i])}{bond.spring_constant}\\,\\left(\\left[{bond.deflection[1]}\\right] \
                                        -\\left[{bond.deflection[0]}\\right]\\right) &= 0 \\\\"
                                conditions_mc += f"{bond.evaluated_cons_lhs[not i][index]}{bond.spring_constant}\\  &=" +f"{bond.evaluated_cons_rhs[not i][index]}"
                                print(conditions_mc)
                                print("Fertig")

                            if index==1: # set the moment conditions
                                conditions += bond.mc_cons[not i][index]  +  "&= 0 \\\\"
                                conditions_mc += bond.evaluated_cons_lhs[not i][index] + "&=" +  bond.evaluated_cons_rhs[not i][index] + "\\\\"
                                print(conditions_mc)
                                print("Fertig")
                                conditions += bond.mc_cons[i][index]+ f"{translate_plus_minus(bond.moment_sign[i])}{bond.spring_constant}\\left(\\left[{bond.deflection[1]}\\right]-\\left[{bond.deflection[0]}\\right]\\right)\\,{bond.rigid_lever} &= 0 \\\\"
                                conditions_mc += bond.evaluated_cons_lhs[i][index] + f"{bond.spring_constant}"+"&=" + f"{bond.evaluated_cons_rhs[i][index]}" + "\\\\"
                                print(conditions_mc)
                                print("Fertig")
                            # plus set the deflection condition
                                conditions += f"{translate_empty_minus((bond.beam_direction[i]))}w{bond.eva_pt[i]}&=0 \\\\"    
                                print("Fertig")

                            
                else: # there is no bearing connection
                    for i in (0,1):
                        if index == 1: # moment conditions are set separately to zero
                            conditions += bond.mc_cons[i][index] + "&=0 \\\\"
                            conditions_mc += f"{bond.evaluated_cons_lhs[i][index]}" + "&="+ f"{bond.evaluated_cons_rhs[i][index]}" +" \\\\"
                            print(conditions_mc)
                            print("Fertig")
                        else: # shear forces are set separately to the spring force; with cross_sections_default one considers the direction/position of the coordinate system
                            conditions += f"{bond.mc_cons[i][index]}&={translate_plus_minus(not bond.cross_sections_default[i])} \
                                {bond.spring_constant}\\,\\left(\\left[{bond.deflection[1]}\\right]-\\left[{bond.deflection[0]}\\right]\\right) &= 0 \\\\"
                            conditions_mc += f"{bond.evaluated_cons_lhs[i][index]}{translate_plus_minus(not bond.cross_sections_default[i])} \
                                {bond.spring_constant}\\,\\left(\\left[{get_evaluated_condition_mc(bond.evaluated_cons_lhs[1][3])}\\right]-\\left[{get_evaluated_condition_mc(bond.evaluated_cons_lhs[0][3])}\\right]\\right)&=\
                                    {get_evaluated_condition_mc(bond.evaluated_cons_rhs[i][index]+sign_evaluation(bond.cross_sections_default[i])*bond.spring_constant*(bond.evaluated_cons_rhs[1][3]-bond.evaluated_cons_rhs[0][3]))}\\\\"
                            print(conditions_mc)
                            print("Fertig")

                            #if b:
                            #    conditions += f"Ergebniss: {bond.evaluated_cons_lhs[0][1]}&={bond.evaluated_cons_rhs[0][1]} \\,\\left(\\left[{bond.evaluated_cons_lhs[0][0]}+{bond.evaluated_cons_lhs[0][3]}{bond.spring_constant}-{bond.evaluated_cons_lhs[1][3]}{bond.spring_constant}&={bond.evaluated_cons_rhs[0][0]}-{bond.evaluated_cons_rhs[0][3]}\\right]\\right) \\, \
                            #     \\left(\\left[{bond.evaluated_cons_lhs[1][1]}&={bond.evaluated_cons_rhs[1][1]}\\right]\\right)\\,\\left(\\left[{bond.evaluated_cons_lhs[0][3]}{bond.spring_constant}-{bond.evaluated_cons_lhs[1][0]}{bond.spring_constant}-{bond.evaluated_cons_lhs[1][3]}{bond.spring_constant}&=-{bond.evaluated_cons_rhs[0][3]}\\right)\\right \\\\"
                            #    b=False
                            #else:
                            #    b=True
                    
                    print("Fertig Ausgabe Configurieren")
                    #print(conditions)
                    

            elif isinstance(bond, RigidBeamMC):
                if index == 0: # consider sign of cross sections default for shear forces
                    conditions += f"{translate_empty_minus(bond.cross_sections_default[0])}{bond.mc_cons[0][index]}&={translate_empty_minus(bond.cross_sections_default[1])}{bond.mc_cons[1][index]} \\\\"
                    conditions_mc += f"{bond.evaluated_cons_lhs[0][index]}&={bond.evaluated_cons_rhs[1][index]} \\\\"
                    print(conditions_mc)
                    print("Fertig")
                elif index == 1: # for moments on the side of the negative cross section a minus is added, if the coordinate system z-directions are not the same for the beams
                    sign = ""
                    if bond.beam_direction[0] != bond.beam_direction[1]:
                        sign = "-"
                    conditions += f"{sign}{bond.mc_cons[0][index]}&={bond.mc_cons[1][index]} \\\\"
                    conditions_mc += f"{bond.evaluated_cons_lhs[0][index]}&={bond.evaluated_cons_rhs[1][index]} \\\\"
                    print(conditions_mc)
                    print("Fertig")
                elif index == 2: # for the angle on the side of the positive cross section a minus is added, if the default cross sections are not the same
                    sign = ""
                    if bond.cross_sections_default[0] != bond.cross_sections_default[1]:
                        sign = "-"
                    conditions += f"{bond.mc_cons[0][index]}&={sign}{bond.mc_cons[1][index]} \\\\"
                    conditions_mc += f"{bond.evaluated_cons_lhs[0][index]}&={bond.evaluated_cons_rhs[1][index]} \\\\"
                    print(conditions_mc)
                    print("Fertig")
                else: # index == 3; for the deflection consider the beam direction for the sign
                    conditions +=  f"{bond.mc_cons[0][index]}&={bond.mc_cons[1][index]} \\\\"
                    conditions_mc += f"{bond.evaluated_cons_lhs[0][index]}&={bond.evaluated_cons_rhs[1][index]} \\\\"
                    print(conditions_mc)
                    print("Fertig")

                    #if b:
                    #    conditions += f"Ergebniss: {bond.evaluated_cons_lhs[0][1]}&={bond.evaluated_cons_rhs[0][1]} \\,\\left(\\left[{bond.evaluated_cons_lhs[0][0]}+{bond.evaluated_cons_lhs[1][0]}&=-{bond.evaluated_cons_rhs[0][0]}\\right]\\right) \\, \
                    #             \\left(\\left[{bond.evaluated_cons_lhs[1][1]}&={bond.evaluated_cons_rhs[1][1]}\\right]\\right)\\,\\left(\\left[{bond.evaluated_cons_lhs[0][3]}-{bond.evaluated_cons_lhs[1][3]}&=-{bond.evaluated_cons_rhs[0][3]}\\right)\\right \\\\"
                    #    b=False
                    #else:
                    #    b=True

                    
            elif isinstance(bond, FixedBearingMC) or isinstance(bond, FloatingBearingMC):
                if not bond.rigid_lever: # if there is a rigid beam at the bearing
                    for i in (0,1):
                        if index == 1: # moment conditions are set separately to zero
                            conditions += bond.mc_cons[i][index] + "&=0 \\\\"
                            conditions_mc += bond.evaluated_cons_lhs[i][index] + "&=0 \\\\"
                            print(conditions_mc)
                            print("Fertig")
                        if index == 3: # deflection conditions are set separately to zero
                            conditions += bond.mc_cons[i][index] + "&=0 \\\\"
                            conditions_mc += bond.evaluated_cons_lhs[i][index] + "&=0 \\\\"
                            print(conditions_mc)
                            print("Fertig")
                else: # if not
                    if index == 1:
                        sign = ""
                        if bond.beam_direction[0] != bond.beam_direction[1]:
                            sign = "-" 
                        conditions += sign + bond.mc_cons[0][index] + "&=" + bond.mc_cons[1][index] + "\\\\"
                        conditions_mc += bond.evaluated_cons_lhs[0][index] + "&=" + bond.evaluated_cons_rhs[1][index]+ "\\\\"
                        print(conditions_mc)
                        print("Fertig")
                    if index == 3: 
                        # set angle condition
                        sign_angle = ""
                        if bond.cross_sections_default[0] != bond.cross_sections_default[1]:
                            sign_angle = "-"
                        conditions += bond.mc_cons[0][2] + "&=" + sign_angle + bond.mc_cons[1][2] + "\\\\"
                        conditions_mc += bond.evaluated_cons_lhs[0][2] + "&=" + bond.evaluated_cons_rhs[1][2]+ "\\\\"
                        print(conditions_mc)
                        print("Fertig")
                        for i in (0,1):# deflection conditions are set separately to zero
                            conditions += bond.mc_cons[i][index] + "&=0 \\\\"   
                            conditions_mc += bond.evaluated_cons_lhs[i][index]+ "&=0 \\\\"
                            print(conditions_mc)
                            print("Fertig")

                        #if b:
                        #    conditions += f"Ergebniss: {bond.evaluated_cons_lhs[0][1]}&={bond.evaluated_cons_rhs[0][1]} \\,\\left(\\left[{bond.evaluated_cons_lhs[0][0]}-{bond.evaluated_cons_lhs[1][0]}&=-{bond.evaluated_cons_rhs[0][0]}\\right]\\right) \\, \
                        #         \\left(\\left[{bond.evaluated_cons_lhs[1][1]}&={bond.evaluated_cons_rhs[1][1]}\\right]\\right)\\,\\left(\\left[{bond.evaluated_cons_lhs[0][3]}-{bond.evaluated_cons_lhs[1][3]}&=-{bond.evaluated_cons_rhs[0][3]}\\right)\\right \\\\"
                        #    b=False
                        #else:
                        #    b=True           
    return conditions, conditions_mc
            
            
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
    
def sign_evaluation(boolean):
    if boolean:
        return 1
    else:
        return -1
    
def get_evaluated_condition_mc(condition):
    return f"{sp.latex(sp.collect(sp.expand(condition), {'C_1', 'C_2', 'C_3', 'C_4', 'C_5', 'C_6', 'C_7', 'C_8'}))}"
