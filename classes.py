import sympy as sp


class System:
    def __init__(self):
        self.beam_list = []
        self.bond_list = []
        self.connection_list = []
        self.position_list = []
        # self.conditions_evaluated = []
        # self.conditions_evaluated_finished = []
        # self.conditions_evaluated_connections = []  # Liste für Vbg. bei RB
        # self.conditions_evaluated_connections_MC = []  # In diese Liste werden Gleichungen von Verbindungen eingefügt,
        # die an der Position von ÜB vorkommen. Die Liste darf nicht mit der Liste conditions_evaluated_connections
        # verwechselt werden. Denn in diese werden Gleichungen von Verbindungselementen eingefügt, an deren Pos. keine
        # Übergangsbedingung vorhanden ist. Diese Liste muss vorhanden sein, weil in die Liste glg_eingesetzt_verbgen
        # (Name abgekürzt) dann bei den Randbedingungen auch die Glg von Verbindungselementen hinein kommen. Das wäre
        # dann nicht mehr auseinanderzuhalten (und weiters wird mit der zuvor genannten Liste auch bei den RB gerechnet)
        # und deshalb werden die Glg der Verb. bei der ÜB dabei in eine extrige Liste verschoben.
        # self.conditions_evaluated_MC = []
        # self.added_values_MC = []
        # self.added_values_connections = []

        # self.solution = []

    def add_beam(self, new_beam):
        """adds a beam to the beam list"""
        self.beam_list.append(new_beam)

    def add_bond(self, new_bond):
        """adds a bond (='Bindung') to the bond list"""
        self.bond_list.append(new_bond)

    def add_connection(self, new_connection):
        """adds a connection (='Connection') to the connection list"""
        self.connection_list.append(new_connection)

    def add_position(self, new_position):
        """adds a position to the system"""
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

    

    #     if position.connection_list:
    #         for connection in position.connection_list:
    #             if isinstance(connection, RigidBeam):
    #                 other_position = 0
    #                 for pos in connection.position_list:
    #                     if pos != position:
    #                         other_position = pos
    #                 beam = other_position.beam_list[0]
    #                 if other_position == beam.position_left:
    #                     beam_right = beam
    #                     # position_plus = other_position
    #                     length_plus = 0
    #                     for bond_of_rigid_beam in other_position.bond_list:
    #                         self.bond_list.remove(bond_of_rigid_beam)
    # # Mit dem remove Befehl darüber wird ein Lager, welches sich beim jeweiligen starren Beam befindet aus der Bindungs-
    # # liste des Systems gelöscht. Das wird gemacht, weil sich dieses noch in der Bindungsliste der jeweiligen Position be-
    # # findet und damit dann unterschieden werden kann, ob das Lager zu einer RB gehört oder zu einer ÜB. Nur wenn ein Lager
    # # in der Bindungsliste des Systems und in der Bindungsliste der Position ist, gehört es zu einer RB.
    #                 else:
    #                     beam_left = beam
    #                     # position_minus = other_position
    #                     length_minus = beam.length
    #                     for bond_of_rigid_beam in other_position.bond_list:
    #                         self.bond_list.remove(bond_of_rigid_beam)
    #     self.fill_lists_conditions_evaluated(bond, length_minus, beam_left)
    #     self.fill_lists_conditions_evaluated(bond, length_plus, beam_right)
    #
    #             self.fill_lists_conditions_evaluated(connection, length_minus, beam_left)
    #             self.fill_lists_conditions_evaluated(connection, length_plus, beam_right)
    #             for element in self.conditions_evaluated_connections:
    #                 self.conditions_evaluated_connections_MC.append(element)
    #             self.conditions_evaluated_connections.clear()
    # # Nachdem die Glg. für die Beam ausgegeben wurden wird auch noch geprüft, ob ein Verbindungselement an der ÜB sitzt.
    # # Wenn ja, dann werden auch dafür die Glg. ausgegeben und in die dafür vorgesehene Liste gleichungen_eingesetzt_verbdg
    # # _bei_ueb gespeichert. Das wird deshalb gemacht, damit die Listeneinträge von Verbindungselementen von ÜB nicht mit den
    # # Einträgen von Verbindungselementen von RB vermischt werden.
    #
    # # Die obere Funktion stelle_UEB_auf funktioniert generell so, dass zuerst die Glg. der Beam ausgegeben werden. Dazu
    # # wird zuerst untersucht welche Position zu welchem Beam gehört. Erst danach werden Glg. ausgegeben und in Listen
    # # zur weiteren Rechnung gespeichert. Danach wird auch noch geprüft ob an der Stelle der ÜB weitere Verbindungselemente
    # # sitzen. Wenn ja, werden auch deren Glg. ausgegeben und in Listen abgelegt.

    @staticmethod
    def evaluate_condition(condition, x_position):
        """this method evaluates the committed condition at the committed x-position"""
        evaluated_condition = []
        if condition:
            for index, entry in enumerate(condition):
                evaluated_condition.append(entry * (x_position ** index))
        else:
            evaluated_condition = [False]
        return evaluated_condition

    # def change_constraints_variable_for_bearings(self):
    #     """this method changes the entries in the variable constraints for bearings"""
    #     for position in self.position_list:
    #         for bond in position.bond_list:
    #             if not isinstance(bond, MatchingConditionSymbol):
    #                 for index, constraint in enumerate(bond.constraints):
    #                     if constraint:
    #                         bond.constraints[index] = 0

    def calculations_rigid_beam_with_bearing_outside(self, bond, connection, x_position, beam):
        if isinstance(connection, RigidBeam):
            if bond.name == "fixed_bearing" or bond.name == "floating_bearing":
                # print(self.conditions_evaluated)
                self.fill_lists_conditions_evaluated(connection, x_position, beam)
                # print(self.conditions_evaluated_connections)
                while len(self.conditions_evaluated_connections[0]) < len(self.conditions_evaluated[1]):
                    self.conditions_evaluated_connections[0].insert(0, 0)
                while len(self.conditions_evaluated_connections[2]) < len(self.conditions_evaluated[3]):
                    self.conditions_evaluated_connections[2].insert(0, 0)
                if x_position == 0:
                    for index, entry in enumerate(self.conditions_evaluated[1]):
                        self.conditions_evaluated[1][index] -= connection.length * \
                                                               self.conditions_evaluated_connections[0][index]
                    for index, entry in enumerate(self.conditions_evaluated[3]):
                        self.conditions_evaluated[3][index] += connection.length * \
                                                               self.conditions_evaluated_connections[2][index]
                    self.conditions_evaluated_connections.clear()
                    for vb in connection.position_left.connection_list:
                        if vb.name == "torsional_spring":
                            self.fill_lists_conditions_evaluated(vb, x_position, beam)
                            while len(self.conditions_evaluated[1]) < \
                                    len(self.conditions_evaluated_connections[2]):
                                self.conditions_evaluated[1].insert(0, 0)
                            for index, entry in enumerate(self.conditions_evaluated[1]):
                                self.conditions_evaluated[1][index] -= vb.spring_constant * \
                                                                       self.conditions_evaluated_connections[2][index]
                            self.conditions_evaluated_connections.clear()
                        elif vb.name == "rigid_beam":
                            pass  # Absichtliches pass hier.
                        else:
                            print("This connection element at a rigid beam was not implemented yet."
                                  "Please check function calculations_rigid_beam_with_bearing_outside")
                    for vb in connection.position_right.connection_list:
                        if vb.name == "linear_spring":
                            self.fill_lists_conditions_evaluated(vb, x_position, beam)
                            while len(self.conditions_evaluated[1]) < \
                                    len(self.conditions_evaluated_connections[3]):
                                self.conditions_evaluated[1].insert(0, 0)
                            for index, entry in enumerate(self.conditions_evaluated[1]):
                                self.conditions_evaluated[1][index] -= connection.length * vb.spring_constant * \
                                                                       self.conditions_evaluated_connections[3][index]
                            self.conditions_evaluated_connections.clear()
                        elif vb.name == "rigid_beam":
                            pass  # Absichtliches pass hier.
                        else:
                            print("This connection element at a rigid beam was not implemented yet."
                                  "Please check function calculations_rigid_beam_with_bearing_outside")
                else:
                    for index, entry in enumerate(self.conditions_evaluated[1]):
                        self.conditions_evaluated[1][index] += connection.length * \
                                                               self.conditions_evaluated_connections[0][index]
                    for index, entry in enumerate(self.conditions_evaluated[3]):
                        self.conditions_evaluated[3][index] -= connection.length * \
                                                               self.conditions_evaluated_connections[2][index]
                    self.conditions_evaluated_connections.clear()
                    for vb in connection.position_right.connection_list:
                        if vb.name == "torsional_spring":
                            self.fill_lists_conditions_evaluated(vb, x_position, beam)
                            while len(self.conditions_evaluated[1]) < \
                                    len(self.conditions_evaluated_connections[2]):
                                self.conditions_evaluated[1].insert(0, 0)
                            for index, entry in enumerate(self.conditions_evaluated[1]):
                                self.conditions_evaluated[1][index] += vb.spring_constant * \
                                                                       self.conditions_evaluated_connections[2][index]
                            self.conditions_evaluated_connections.clear()
                        elif vb.name == "rigid_beam":
                            pass  # Absichtliches pass hier.
                        else:
                            print("This connection element at a rigid beam was not implemented yet."
                                  "Please check function calculations_rigid_beam_with_bearing_outside")
                    for vb in connection.position_left.connection_list:
                        if vb.name == "linear_spring":
                            self.fill_lists_conditions_evaluated(vb, x_position, beam)
                            while len(self.conditions_evaluated[1]) < \
                                    len(self.conditions_evaluated_connections[3]):
                                self.conditions_evaluated[1].insert(0, 0)
                            for index, entry in enumerate(self.conditions_evaluated[1]):
                                self.conditions_evaluated[1][index] += connection.length * vb.spring_constant * \
                                                                       self.conditions_evaluated_connections[3][index]
                            self.conditions_evaluated_connections.clear()
                        elif vb.name == "rigid_beam":
                            pass  # Absichtliches pass hier.
                        else:
                            print("This connection element at a rigid beam was not implemented yet."
                                  "Please check function calculations_rigid_beam_with_bearing_outside")
            else:
                print("This bearing element at a rigid beam was not implemented yet."
                      "Please check function calculations_rigid_beam_with_bearing_outside")
        # print("Addierte GLG", self.conditions_evaluated)
        self.conditions_evaluated_connections.clear()

    # perhaps not needed
    def paginate_spring_constants_ascending(self):
        """this method is currently not used. If it is necessary that there are different spring constants in the
        system, this method numbers/paginates the constants ascending"""
        counter_linear_spring = 1
        counter_torsional_spring = 1
        for position in self.position_list:
            for connection in position.connection_list:
                if connection.name == "torsional_spring":
                    connection.spring_constant = sp.symbols(
                        str(connection.spring_constant) + str(counter_torsional_spring))
                    counter_torsional_spring += 1
                elif connection.name == "linear_spring":
                    connection.spring_constant = sp.symbols(
                        str(connection.spring_constant) + str(counter_linear_spring))
                    counter_linear_spring += 1

            for bond in position.bond_list:
                if bond.name == "linear_spring_MC":
                    bond.spring_constant = sp.symbols(str(bond.spring_constant) + str(counter_linear_spring))
                    counter_linear_spring += 1

    def gleichungen_vereinen(self):
        """Hier werden die konstanten Anteile aus den eingesetzten Belastungen (A,B,C Anteile) addiert und anschließend
        mit den jeweiligen Werten der Einschränkungen subtrahiert (da die Gleichungen nach dem "=" umgestellt werden,
        muss auch ein Vorzeichenwechsel stattfinden)."""
        i = 0  # Hier müssen alle Variablen stehen bleiben, da diese zu unterschiedlichen Zeiten +1 gerechnet werden
        j = 0  # müssen.
        k = 0
        # Diese Variablen sind dafür da, weil prinzipiell pro Lager, ÜB oder Connection und pro Balken 4 Glg. ausgegeben werden,
        # welche in der jeweiligen Liste abgespeichert werden. Diese 4 Einträge kommen von daher, weil von der jeweiligen
        # Bedingung die Einschränkungen betrachtet werden. Diese sind ja auch 4 lang und daher die 4 Glg. Hat man jetzt mehrere
        # Bedingungen, dann hat man auch mehrere dieser 4er Blöcke. Und immer wenn für eine Bedingung die konst. Werte aus den
        # Streckenlasten abgezogen wurden, wird der jeweilige 4er Block dann übersprungen bei der nächsten Bedingung, weil er
        # ja schon berücksichtigt wurde. Deshalb wird in dem Fall dann die jeweilige Variable +1 gerechnet. Wie man in der
        # Funktion unterhalb sehen kann, gibt es auch dementsprechend unterschiedliche Fälle, wann diese Variablen erhöht
        # werden. Das dient aber immer dem genannten Grund, einen bereits gerechneten Block zu überspringen. Deshalb gibt es
        # für die Randbedingungen die Variable i, für die ÜB j und für die Verbindungselemente bei ÜB dabei k.
        for beam in self.beam_list:
            for position in beam.position_list:
                if len(beam.line_load) > 1 or beam.line_load[0] != 0:  # Hier passiert ein Vergleich, ob die
                    if len(position.bond_list) < 1:  # Streckenlast != 0 ist. Wenn ja, werden die konst. Anteile aus
                        for connection in position.connection_list:  # den Gleichungen subtrahiert und in die
                            if isinstance(connection, RigidBeam):  # Störvektoren addiert.
                                if position == beam.position_left:
                                    for bond in connection.position_left.bond_list:
                                        if bond.typ != "matching_condition":
                                            for index, entry in enumerate(bond.constraints):
                                                if entry is not False:
                                                    constant_part = 0
                                                    for constant in beam.line_load:
                                                        constant_part += \
                                                            self.conditions_evaluated_finished[index + (4 * i)][-1]
                                                        del self.conditions_evaluated_finished[index + (4 * i)][-1]
                                                    bond.constraints[index] -= constant_part
                                            i += 1
                                        # In der for Schleife mit der Laufvariablen "constant" nicht wundern, dass diese nicht verwendet wird. Diese ist nur
                                        # dafür da, dass so oft wie in der Streckenlast des Balkens ein konst. Wert vorkommt, diese Werte auch wirklich aus den
                                        # Gleichungen aufsummiert und dann entfernt werden und in eine andere Liste zur späteren Berechnung gespeichert werden.
                                        # Bei den Lagern sind das zB die Einschränkungseinträge. Diese werden zuerst an den True Stellen =0 gesetzt und dort
                                        # dann diese Summen der konst. Werte hineingespeichert. Bei ÜB und Verbindungen bei den Positionen der ÜB werden diese
                                        # Werte unten weiter in eigene Listen gespeichert, nicht in die Einschränkungseinträge.
                                        elif bond.typ == "matching_condition":
                                            for index, entry in enumerate(connection.constraints):
                                                if entry is not False:
                                                    constant_part = 0
                                                    for constant in beam.line_load:
                                                        constant_part += \
                                                            self.conditions_evaluated_MC[index +
                                                                                         (4 * j)][-1]
                                                        del self.conditions_evaluated_MC[index +
                                                                                         (4 * j)][-1]
                                                    self.added_values_MC.append(constant_part)
                                            j += 1
                                # Die obere for Schleife gilt für einen Beam mit Streckenlast und einem starren Balkenteil, das direkt bei der ÜB
                                # dabei sitzt. Das starre Balkenteil hat bei diesem Fall aber kein Lager dabei, dafür ist dann die Unterscheidung unten
                                # weiter zuständig.
                                elif position == beam.position_right:
                                    for bond in connection.position_right.bond_list:
                                        if bond.typ != "matching_condition":
                                            for index, entry in enumerate(bond.constraints):
                                                if entry is not False:
                                                    constant_part = 0
                                                    for constant in beam.line_load:
                                                        constant_part += \
                                                            self.conditions_evaluated_finished[index + (4 * i)][-1]
                                                        del self.conditions_evaluated_finished[index + (4 * i)][-1]
                                                    bond.constraints[index] -= constant_part
                                            i += 1
                                        elif bond.typ == "matching_condition":
                                            for index, entry in enumerate(connection.constraints):
                                                if entry is not False:
                                                    constant_part = 0
                                                    for constant in beam.line_load:
                                                        constant_part += \
                                                            self.conditions_evaluated_MC[index +
                                                                                         (4 * j)][-1]
                                                        del self.conditions_evaluated_MC[index +
                                                                                         (4 * j)][-1]
                                                    self.added_values_MC.append(constant_part)
                                            j += 1
                    else:
                        for bond in position.bond_list:
                            if bond.typ != "matching_condition":
                                if any(bond == bind for bind in self.bond_list):
                                    for index, entry in enumerate(bond.constraints):
                                        if entry is not False:
                                            constant_part = 0
                                            for constant in beam.line_load:
                                                constant_part += \
                                                    self.conditions_evaluated_finished[index + (4 * i)][-1]
                                                del self.conditions_evaluated_finished[index + (4 * i)][-1]
                                            bond.constraints[index] -= constant_part
                                    i += 1
                                else:
                                    for connection in position.connection_list:
                                        if isinstance(connection, RigidBeam):
                                            for index, entry in enumerate(connection.constraints):
                                                if entry is not False:
                                                    constant_part = 0
                                                    for constant in beam.line_load:
                                                        constant_part += \
                                                            self.conditions_evaluated_MC[index +
                                                                                         (4 * j)][-1]
                                                        del self.conditions_evaluated_MC[index +
                                                                                         (4 * j)][-1]
                                                    self.added_values_MC.append(constant_part)
                                            j += 1
                    # Bis hier hin erfolgt der Abzug der konstanten Werte bei den Randbedingungen und zusätzlich bei starren Balkenteilen
                    # mit und ohne Lager. Alles im "if len(position.bond_list) < 1:" wo als zusätzliche Abfrage bond.typ == "ÜB"
                    # steht, dient für starre Balkenteile ohne Lager und für Randbedingungen mit starren Balkenteilen. Im else wird einmal
                    # mit "if any(bond == bind for bind in self.bond_list):" abgefragt, ob ein Lager sich auch noch in der Bindungs-
                    # liste des Systems befindet. Ist dies der Fall, dann kann dieses Lager nur eine RB sein. Ist dies nicht der Fall, dann
                    # gehört das Lager zu einer ÜB in irgendeiner Form und das else greift. Danach wird geprüft, ob noch ein starres Beam-
                    # teil dabei ist, wenn ja, werden die Glg dementsprechend angepasst. Dabei werden die konstanten Werte zuerst
                    # aufsummiert und dann nach der Vorzeichenregel negiert, weil sie auf die andere Seite des = kommen. Diese Negierung
                    # erfolgt da, wo die addierten Werte mit den 0en aus den veränderten Einschränkungen der Lager - gerechnet werden. Bei
                    # den starren Balkenteilen, die bei einer ÜB sitzen wird nur + gerechnet, weil die Vorzeichen dann später in der Rech-
                    # nung berücksichtigt wird.
                    for bond in position.bond_list:
                        if bond.typ == "matching_condition":
                            for index, entry in enumerate(bond.constraints):
                                if entry is not False:
                                    constant_part = 0
                                    for constant in beam.line_load:
                                        constant_part += \
                                            self.conditions_evaluated_MC[index + (4 * j)][-1]
                                        del self.conditions_evaluated_MC[index + (4 * j)][-1]
                                    self.added_values_MC.append(constant_part)
                                else:
                                    self.added_values_MC.append(False)
                            j += 1
                            for vb in position.connection_list:
                                if not isinstance(vb, RigidBeam):
                                    for index, entry in enumerate(vb.constraints):  # Solange die vorhandene
                                        if entry is not False:  # Connection kein starres Balkenteil ist, wird der if
                                            constant_part = 0  # Fall ausgeführt. Also nur für ein "normales"
                                            # Verbindungselement wie zB eine LinearSpring.
                                            for constant in beam.line_load:
                                                constant_part += \
                                                    self.conditions_evaluated_connections_MC[index + (4 * k)][-1]
                                                del self.conditions_evaluated_connections_MC[index + (4 * k)][-1]
                                            self.added_values_connections.append(constant_part)
                                        else:
                                            self.added_values_connections.append(False)
                                    k += 1
                # Der obere Code dient zur Addition der konstanten Werte aus der Streckenlast und anschließenden Verschiebung in die 0
                # gesetzten Einschränkungen der jeweiligen ÜB (ganz ohne starre Beam, da die Berechnung dafür darüber passiert). Es
                # befindet sich noch eine weitere for Schleife in der for Schleife. Diese dient dazu, dass weitere eventuell angreifende
                # Verbindungselemente auch ihre konst. Werte "wegaddiert" bekommen. Es muss statt dem Minus ein Plus stehen am Ende,
                # weil die Umformung auf die andere Seite des = erst passiert. Das passiert aber nur hier bei den Übergangsbedingungen,
                # welche miteinander subtrahiert werden. Also wo 2 Gleichungen verwendet werden.
                else:
                    if len(position.bond_list) < 1:
                        for connection in position.connection_list:
                            if isinstance(connection, RigidBeam):
                                if position == beam.position_left:
                                    for bond in connection.position_left.bond_list:
                                        if bond.typ != "matching_condition":
                                            i += 1
                                        elif bond.typ == "matching_condition":
                                            for index, entry in enumerate(connection.constraints):
                                                if entry is not False:
                                                    self.added_values_MC.append(0)
                                            j += 1
                                elif position == beam.position_right:
                                    for bond in connection.position_right.bond_list:
                                        if bond.typ != "matching_condition":
                                            i += 1
                                        elif bond.typ == "matching_condition":
                                            for index, entry in enumerate(connection.constraints):
                                                if entry is not False:
                                                    self.added_values_MC.append(0)
                                            j += 1
                    else:
                        for bond in position.bond_list:
                            if bond.typ != "matching_condition":
                                if any(bond == bind for bind in self.bond_list):
                                    i += 1
                                else:
                                    for connection in position.connection_list:
                                        if isinstance(connection, RigidBeam):
                                            for index, entry in enumerate(connection.constraints):
                                                if entry is not False:
                                                    self.added_values_MC.append(0)
                                            j += 1
                    for bond in position.bond_list:
                        if bond.typ == "matching_condition":
                            for index, entry in enumerate(bond.constraints):
                                if entry is not False:
                                    self.added_values_MC.append(0)
                                else:
                                    self.added_values_MC.append(False)
                            j += 1
                            for vb in position.connection_list:
                                if not isinstance(vb, RigidBeam):
                                    for index, entry in enumerate(vb.constraints):
                                        if entry is not False:
                                            self.added_values_connections.append(0)
                                        else:
                                            self.added_values_connections.append(False)
                                    k += 1

    # Mit dem else darüber wird ein Beam überpfrüft, welcher keine Streckenlast hat und damit keine konstanten Anteile.
    # Sollte hier ein starrer Beam am jeweiligen Ende des Balkens angebracht sein und noch dazu ein Lager, wird die
    # Variable i um +1 erhöht (und damit der jeweilige Eintrag davon in conditions_evaluated_finished ausgelassen). Hat man
    # aber ein Lager an der Position im Beam, dann kommt das else darunter zum Zug und erhöht i um +1. Diese Fälle sind
    # nur wichtig, wenn mehr als 2 Beam im System vorhanden sind oder Beam 1 (der links weiter gelegene) keine
    # Streckenlast hat.
    # Weiters wird den Listen added_values_connections und added_values_MC dementsprechend wenn keine konst.
    # Werte vorhanden sind, entweder ein 0er oder ein False eingefügt (je nach Einschränkungs-Vektor). Das Führt dazu, dass
    # man dann in den Listen immer für je 2 Beam 8 Einträge bekommt, egal welche ÜB oder Connection hier sitzt. Dies
    # wiederum erleichtert den automatisierten Ablauf der Rechnung weiter unten in loese_gleichungssystem.
    # Da eine ÜB oder ein Verbindungselement an einer Position für 2 Beam jeweils vorkommen, sind auch
    # immer die Einträge dafür bei jedem Beam vorhanden. Deshalb müssen diese Einträge bei einem Beam ohne Streckenlast
    # ebenfalls beide übersprungen werden. Es muss also j und k +1 gerechnet werden.
    # Weiters dienen wie oben bereits erwähnt die weiteren Fälle, bei denen j +1 gerechnet wird für starre Beam, die an
    # der ÜB angebracht sind. Je nachdem, ob noch ein Lager dabei sitzt, kommt man in unterschiedliche Fälle. Das wurde oben
    # bereits genauer beschrieben.

    def setup_and_solve_system_of_equations(self):
        """this method sets up the coefficient matrix, solution vector and disturbance vector and solves the
        corresponding system of equations. the solution for the integration constants is printed starting from C_1"""
        intermediate_list = []
        intermediate_list_MC = []
        intermediate_list_MC_finished = []
        intermediate_list_MC_connections = []

        for element in self.conditions_evaluated_finished:  # Hier werden alle Listeneinträge einmal auf eine
            if element[0] is not False:  # gemeinsam passende Länge von 4 gebracht (pro Beam immer 4 Konstanten) und
                while len(element) < 4:  # anschließend in eine neue Liste eingefügt.
                    element.insert(0, 0)
                intermediate_list.append(element)
        for element in self.conditions_evaluated_MC:
            if element[0] is not False:
                while len(element) < 4:
                    element.insert(0, 0)
            intermediate_list_MC.append(element)
        for element in self.conditions_evaluated_connections_MC:
            if element[0] is not False:
                while len(element) < 4:
                    element.insert(0, 0)
            intermediate_list_MC_connections.append(element)

        # print('Zwischenliste der ÜB sieht so aus:\n', intermediate_list_MC, sep='')

        for element in intermediate_list:  # Hier werden die einzelnen Elemente der Zwischenliste umgedreht. Das hat den
            element.reverse()  # Sinn, damit die Lösung meiner Matrix C1-zB. C8 zu lesen ist und nicht C8-C1
        for element in intermediate_list_MC:
            element.reverse()
        for element in intermediate_list_MC_connections:
            element.reverse()
        # print('Zwischenliste der ÜB sieht so aus:\n', intermediate_list_MC, sep='')
        # print("addierte werte aus ue", self.added_values_MC)
        # print("intermediate_list_MC_connections:", intermediate_list_MC_connections)
        # print("added_values_connections:", self.added_values_connections)

        zero_list = [0, 0, 0, 0]  # Einfache Liste, mit deren Hilfe manche Glg. schnell und einfach an die Matrix an-
        # gepasst werden können.
        # Berechnung für vorhandene starre Balkenteile, die bei einer ÜB dabei sind:
        zaehler_glg_starre_balken = 0  # Zähler dient dazu, dass die jeweiligen 8er Blöcke an Glg in den Listen dement-
        # sprechend nach einer Berechnung ausgelassen werden.
        for position in self.position_list:
            for bond in position.bond_list:
                if bond.typ == "matching_condition":
                    for connection in position.connection_list:
                        if isinstance(connection, RigidBeam):
                            if len(connection.position_left.beam_list) > 0 and \
                                    len(connection.position_left.bond_list) < 1:
                                for index, entry in enumerate(intermediate_list_MC[1]):
                                    intermediate_list_MC[3 + (8 * zaehler_glg_starre_balken)][index] -= \
                                        connection.length * \
                                        intermediate_list_MC[2 + (8 * zaehler_glg_starre_balken)][index]
                                    intermediate_list_MC[1 + (8 * zaehler_glg_starre_balken)][index] += \
                                        connection.length * \
                                        intermediate_list_MC[0 + (8 * zaehler_glg_starre_balken)][index]
                                self.added_values_MC[3 + (8 * zaehler_glg_starre_balken)] -= \
                                    connection.length * self.added_values_MC[2 + (8 * zaehler_glg_starre_balken)]
                                self.added_values_MC[1 + (8 * zaehler_glg_starre_balken)] += \
                                    connection.length * self.added_values_MC[0 + (8 * zaehler_glg_starre_balken)]
                            elif len(connection.position_right.beam_list) > 0 and \
                                    len(connection.position_right.bond_list) < 1:
                                for index, entry in enumerate(intermediate_list_MC[1]):
                                    intermediate_list_MC[7 + (8 * zaehler_glg_starre_balken)][index] += \
                                        connection.length * \
                                        intermediate_list_MC[6 + (8 * zaehler_glg_starre_balken)][index]
                                    intermediate_list_MC[5 + (8 * zaehler_glg_starre_balken)][index] -= \
                                        connection.length * \
                                        intermediate_list_MC[4 + (8 * zaehler_glg_starre_balken)][index]
                                self.added_values_MC[7 + (8 * zaehler_glg_starre_balken)] += \
                                    connection.length * self.added_values_MC[6 + (8 * zaehler_glg_starre_balken)]
                                self.added_values_MC[5 + (8 * zaehler_glg_starre_balken)] -= \
                                    connection.length * self.added_values_MC[4 + (8 * zaehler_glg_starre_balken)]
                    zaehler_glg_starre_balken += 1
        # Vorsicht, diese Berechnung darf auf keinen Fall in den unteren for Schleifen irgendwie angehängt werden. Es müssen
        # nämlich zuerst diverse Einträge aufgrund der starren Balkenteile erweitert werden, bevor dann gerechnet wird. Dazu
        # zählen auch manche Einträge der Verbindungselemente wie zB Federn. Deshalb steht dieser Rechenblock über dem Block
        # für bei ÜB angreifenden Verbindungselementen.

        # Berechnung für Verbindungselemente, welche bei einer ÜB angreifen:
        counter_MC = 0  # Dient dazu, dass die Listeneinträge der ÜB welche keine Verbindungselemente haben bzw. wenn
        for position in self.position_list:  # Einträge von ÜB bereits berechnet wurden, übersprungen werden.
            for bond in position.bond_list:
                if bond.typ == "matching_condition":
                    if bond.name == "linear_spring_MC":
                        if len(position.connection_list) > 0 and len(position.beam_list) == 2:
                            for vb in position.connection_list:
                                if vb.name == "linear_spring":
                                    for beam in vb.beam_list:
                                        if vb.z_coordinate == beam.z_coordinate \
                                                and vb.position.x_coordinate == beam.position_right.x_coordinate:
                                            for index, entry in enumerate(
                                                    intermediate_list_MC_connections[3]):
                                                intermediate_list_MC[0 + 8 * counter_MC][index] += \
                                                    vb.spring_constant * \
                                                    intermediate_list_MC_connections[3][index]
                                            self.added_values_MC[0 + 8 * counter_MC] += \
                                                self.added_values_connections[3] * vb.spring_constant
                                            del intermediate_list_MC_connections[:8]
                                            del self.added_values_connections[:8]
                                            counter_MC += 1
                                        elif vb.z_coordinate == beam.z_coordinate \
                                                and vb.position.x_coordinate == beam.position_left.x_coordinate:
                                            for index, entry in enumerate(
                                                    intermediate_list_MC_connections[3]):
                                                intermediate_list_MC[4 + 8 * counter_MC][index] -= \
                                                    vb.spring_constant * \
                                                    intermediate_list_MC_connections[7][index]
                                            self.added_values_MC[4 + 8 * counter_MC] -= \
                                                self.added_values_connections[7] * vb.spring_constant
                                            del intermediate_list_MC_connections[:8]
                                            del self.added_values_connections[:8]
                                            counter_MC += 1
                                elif isinstance(vb, RigidBeam):
                                    pass  # Absichtliches pass, damit bei einem starren Balkenteil nicht die Fehler-
                                # meldung darunter getriggert wird.
                                else:
                                    print("this connection in combination with a linear spring as matching condition "
                                          "was not implemented yet. Please check function "
                                          "setup_and_solve_system_of_equations")
                        elif len(position.connection_list) > 0 and len(position.beam_list) != 2:
                            pass
                        # genau hier rein gehört programmiert, wo bei einem starren Balkenteil ohne Lager ein Verbindungselement (Feder) an-
                        # greift. Es wird dabei nur das w(x) jeweils je nach Fall um a*phi(x) erweitert. Dazu kann im Grunde der darüberstehende
                        # Code übernommen werden, da die hierbei ausgeführte Rechnung im Grunde nur dann nach der Unterscheidung wo das
                        # Verbindungselement sitzt den jeweiligen Listeneintrag erweitert (um das zusätzliche genannte a*phi(x)).

                        else:
                            counter_MC += 1  # Immer nachdem eine Rechnung für ein zusätzliches Verbindungselement an
                    # der Stelle einer ÜB fertig behandelt wurde, wird der Zähler um +1 erhöht. Damit wird dann der jeweilige fertig
                    # behandelte 8er Block von den Gleichungen der Übergangsbedingungen übersprungen. Weiters muss der Zähler auch um +1
                    # erhöht werden, wenn eine ÜB keine zusätzlichen Verbindungselemente angreifen hat, damit nicht der falsche 8er Block
                    # gerechnet wird (das macht hier das else darüber).
                    else:
                        if len(position.connection_list) > 0 and len(position.beam_list) == 2:
                            for vb in position.connection_list:
                                if vb.name == "linear_spring":
                                    for index, entry in enumerate(intermediate_list_MC_connections[3]):
                                        intermediate_list_MC[0 + 8 * counter_MC][index] += \
                                            vb.spring_constant * \
                                            intermediate_list_MC_connections[3][index]
                                    self.added_values_MC[0 + 8 * counter_MC] += \
                                        self.added_values_connections[3] * vb.spring_constant
                                    del intermediate_list_MC_connections[:8]
                                    del self.added_values_connections[:8]
                                    counter_MC += 1
                                elif isinstance(vb, RigidBeam):
                                    pass  # Absichtliches pass, damit bei einem starren Balkenteil nicht die Fehler-
                                # meldung darunter getriggert wird.
                                else:
                                    print("this connection in combination with a linear spring as matching condition "
                                          "was not implemented yet. Please check function "
                                          "setup_and_solve_system_of_equations")
                        elif len(position.connection_list) > 0 and len(position.beam_list) != 2:
                            pass
                        # genau hier rein gehört programmiert, wo bei einem starren Balkenteil ohne Lager ein Verbindungselement (Feder) an-
                        # greift. Es wird dabei nur das w(x) jeweils je nach Fall um a*phi(x) erweitert. Dazu kann im Grunde der darüberstehende
                        # Code übernommen werden, da die hierbei ausgeführte Rechnung im Grunde nur dann nach der Unterscheidung wo das
                        # Verbindungselement sitzt den jeweiligen Listeneintrag erweitert (um das zusätzliche genannte a*phi(x)).

                        else:
                            counter_MC += 1  # Mit dem else wird der Zähler wieder erhöht, wenn die jeweilige ÜB keine
                            # zusätzlich angreifenden Verbindungen aufweist.
        # Vorsicht, diese obere for Schleife darf nicht in die Berechnung darunter eingefügt werden. Das garantiert, dass die
        # Berechnung des Verbindungselementes vor der Berechnung, wo die Schnittreaktionen von 2 Beam dann gerechnet werden,
        # durchgeführt wird (weil hier ja vom jeweiligen Beam zuerst die Einträge in intermediate_list_MC
        # modifiziert werden müssen.

        # WICHTIG: Eventuell hier rein könnte man die Berechnung für starre Balkenteile mit Lagern bei einer ÜB dabei einbauen.
        # Die Systemeingabe funktioniert bis hier runter (also Glg. werden ausgegeben und angepasst), es fehlt nur noch die
        # Berechnung selbst. Hierbei sind 3 Fälle zu unterscheiden: Ob beide Beam bei der ÜB dabei ein starres Balkenteil
        # mit Lager besitzen oder nur der linke Beam oder nur der rechte Beam. Diese Unterscheidung ist in dem Programm noch
        # nicht vorhanden, muss aber gemacht werden, da dies die Glg. beeinflusst, die zur Berechnung des Systems verwendet
        # werden müssen. Wenn man eine clevere Methode zur Unterscheidung gefunden hat, könnte dies sogar eventuell im Code
        # darunter eingebaut werden und die Länge des benötigten Codes verkürzen (da hier ja prinzipiell schon alle ÜB abgedeckt
        # sind).

        for position in self.position_list:
            for bond in position.bond_list:
                # Berechnungen für ein Joint:
                if bond.name == "joint" or bond.name == "rigid_connection":
                    for index, entry in enumerate(intermediate_list_MC[4]):
                        intermediate_list_MC[4][index] *= (-1)
                        intermediate_list_MC[7][index] *= (-1)
                    intermediate_list_MC[0] += intermediate_list_MC[4]
                    intermediate_list_MC[3] += intermediate_list_MC[7]
                    intermediate_list_MC[1] += zero_list
                    intermediate_list_MC[5] = zero_list + intermediate_list_MC[5]
                    intermediate_list_MC_finished.extend([intermediate_list_MC[0],
                                                          intermediate_list_MC[3],
                                                          intermediate_list_MC[1],
                                                          intermediate_list_MC[5]])
                    del intermediate_list_MC[:8]
                # Mit dieser Schleife werden die Q(x2) und w(x2) also der jeweils rechts gelegenen Beam negiert und anschließend wird
                # Q(x1)-Q(x2) und w(x1)-w(x2) für die Bedingung gerechnet und sogleich die fertigen Glg. in eine neue Liste gespeichert.
                # Es wird auch noch M(x1)=0 und M(x2)=0 berücksichtigt. Hierzu werden auch schon jeweils 4 Nullen eingefügt, weil bei
                # den beiden Glg immer nur jeweils ein Beam beteiligt ist. Die Glg davor werden schon im Gegensatz eine Länge von 8
                # aufweisen (da 2 Beam daran beteiligt sind). Das macht dann im Nachhinein die Anpassung der Glg an die Matrix
                # leichter. In der if Abfrage oben sieht man, dass diese Schleife jeweils für ein Joint oder auch eine starre
                # Connection gelten, weil hier die gleichen Rechnungen ausgeführt werden.

                # Berechnung für eine LinearSpring, die 2 Beam als ÜB verbindet:
                elif bond.name == "linear_spring_MC":
                    for index, entry in enumerate(intermediate_list_MC[7]):
                        intermediate_list_MC[3][index] *= bond.spring_constant
                        intermediate_list_MC[7][index] *= (-1) * bond.spring_constant
                        intermediate_list_MC[0][index] += intermediate_list_MC[3][index]
                        intermediate_list_MC[4][index] += intermediate_list_MC[7][index]
                    intermediate_list_MC[0] += intermediate_list_MC[7]  # Glg 5
                    intermediate_list_MC[3] += intermediate_list_MC[4]  # Glg 6
                    intermediate_list_MC[1] += zero_list  # Glg 7
                    intermediate_list_MC[5] = zero_list + intermediate_list_MC[5]
                    # Glg 8
                    intermediate_list_MC_finished.extend([intermediate_list_MC[0],
                                                          intermediate_list_MC[3],
                                                          intermediate_list_MC[1],
                                                          intermediate_list_MC[5]])
                    del intermediate_list_MC[:8]
                # Hier werden zuerst (Q(x1)+Federsteifigkeit*w(x1))-Federsteifigkeit*w(x2) und (Q(x2)-Federsteifigkeit*w(x2))
                # +Federsteifigkeit*w(x1) gerechnet, damit das Ganze in Matrixschreibweise angegeben werden kann (wobei x1 immer für den
                # links gelegenen Beam steht und x2 für den rechts gelegenen). Dazu werden zuerst die Gleichungen von w(x) in der for
                # Schleife mit der Federkonstante der Bedingung multipliziert und w(x2) zusätzlich *-1 gerechnet, da dies lauf Vor-
                # zeichenrechnung aus der Bedingung heraus erforderlich ist. Danach werden diese Werte dementsprechend pro Glg mit
                # Q(x1) oder Q(x2) wie es oben steht addiert. Bei den Momenten werden für die Erstellung der Matrix entsprechend 0en
                # eingefügt, damit diese dann einfach an das Gesamtsystem angepasst werden. Somit erhält man dann die 4 Glg. der ÜB.

                # Berechnung für ein FixedBearing oder FloatingBearing als ÜB:
                elif bond.name == "fixed_bearing_MC" or bond.name == "floating_bearing_MC":
                    for index, entry in enumerate(intermediate_list_MC[5]):
                        intermediate_list_MC[5][index] *= (-1)
                        intermediate_list_MC[6][index] *= (-1)
                    intermediate_list_MC[1] += intermediate_list_MC[5]
                    intermediate_list_MC[2] += intermediate_list_MC[6]
                    intermediate_list_MC[3] += zero_list
                    intermediate_list_MC[7] = zero_list + intermediate_list_MC[7]
                    intermediate_list_MC_finished.extend([intermediate_list_MC[1],
                                                          intermediate_list_MC[2],
                                                          intermediate_list_MC[3],
                                                          intermediate_list_MC[7]])
                    del intermediate_list_MC[:8]
        # Hier wird im Grunde für das jeweilige Lager als ÜB M(x1)=M(x2), phi(x1)=phi(x2), w(x1)=0 und w(x2)=0 aufgestellt.
        # Dafür werden zuerst die Werte von M(x2) und phi(x2) negiert, weil diese ja auf die andere Seite vom = gerechnet werden
        # müssen. Bei den M´s werden wieder dementsprechend 0en eingefügt, um diese leichter an die Matrix anzupassen.

        # print("intermediate_list_MC:", intermediate_list_MC_finished)
        # print('intermediate_list_MC_finished sieht nach zusammenführen der Glg so aus:\n',
        #       intermediate_list_MC_finished, sep='')
        # print('Zwischenliste sieht so aus:\n', intermediate_list, sep='')

        j = 0  # Hier werden in der Zwischenliste dementsprechend 0en eingefügt, damit man die
        k0 = 1  # Matrix mit einem passenden Störvektor anschreiben kann.
        # Die Variable k0 dient dazu, um die Glg aus den Randbedingungen in Matrixform zu bringen. Es ist also nur ein Faktor
        # der entscheidet, wie oft vor und nach der jeweiligen Gleichung die zero_list eingefügt wird. Die Variable j dient
        # dabei dazu, um den jeweiligen Listenplatz in der Zwischenliste zu bearbeiten. Deshalb wird j nach jeder angepassten
        # Glg +1 gerechnet. Und weil die Liste in der die Glg stehen auch die Glg aus anderen Beam enthält, darf die
        # Information nicht verloren gehen wo man gerade in der Liste war. Deshalb wird j als eigene Variable geführt. Wenn dann
        # also auf eine weiteren Beam bei den RB wechselt muss dementsprechend dann bei diesen Glg vorne zB schon jeweils
        # einmal ein 4er Block 0en eigefügt werden, damit die Gleichung überhaupt in die Matrix passt (Beam 2 geht ja dann
        # von C5-C8 und C1-C4 aus Beam 1 sind darin nicht vorhanden). Deshalb wird immer dann k0 um +1 gerechnet.
        for beam in self.beam_list:
            for position in beam.position_list:
                if len(position.bond_list) < 1:
                    for connection in position.connection_list:
                        if isinstance(connection, RigidBeam):
                            if position == beam.position_left:
                                for bond in connection.position_left.bond_list:
                                    if bond.typ != "matching_condition":
                                        if any(bond == bind for bind in self.bond_list):
                                            for einschraenkung in bond.constraints:
                                                if einschraenkung is not False:
                                                    intermediate_list[j] = (k0 - 1) * zero_list + intermediate_list[j] + \
                                                                           (len(self.beam_list) - k0) * zero_list
                                                    j += 1
                            elif position == beam.position_right:
                                for bond in connection.position_right.bond_list:
                                    if bond.typ != "matching_condition":
                                        if any(bond == bind for bind in self.bond_list):
                                            for einschraenkung in bond.constraints:
                                                if einschraenkung is not False:
                                                    intermediate_list[j] = (k0 - 1) * zero_list + intermediate_list[j] + \
                                                                           (len(self.beam_list) - k0) * zero_list
                                                    j += 1
                else:
                    for bond in position.bond_list:
                        if bond.typ != "matching_condition":
                            if any(bond == bind for bind in self.bond_list):
                                for entry in bond.constraints:
                                    if entry is not False:
                                        intermediate_list[j] = (k0 - 1) * zero_list + intermediate_list[j] + \
                                                               (len(self.beam_list) - k0) * zero_list
                                        j += 1
            k0 += 1
        # Die Gleichungen der Lager wurden an die Matrix angepasst, mit dementsprechend 0en an den jeweiligen Stellen, wo es
        # notwendig ist.

        # Was bei den Randbedingungen k0 erledigt, erfüllt bei den Glg der Übergangsbedingungen x1. Immer wenn man mehr als 1
        # Beam im System hat, heißt das, dass Beam 1 mit Beam 2 automatisch verknüpft sein muss über eine ÜB. Für jeden
        # weiteren Beam gelten diese Bedingungen auch, nur dass sich einfach die Balkennummern um 1 erhöhen. Diese Tatsache
        # wird hier genutzt. Bei der 1.ÜB muss Balken1 u. 2 dabei sein. Also habe ich hier Glg mit C1-C8. Vorne benötigt man
        # deshalb keine 0en für die Matrix aber ev. hinten an den Glg. wenn man zB einen Beam 3 noch hat. Und genau das macht
        # dann x1. Wenn dann die Übergangsbedingung angepasst ist, geht das Programm zur nächsten und x1 wird +1 gerechnet.
        x1 = 0  # Mit dieser Schleife werden die Listen der ÜB der Beam durchgegangen. Wann immer die jeweilige ÜB
        for position in self.position_list:  # vorhanden ist, werden die 0en eingefügt, wie es die jeweilige Art der
            for bond in position.bond_list:  # ÜB nun mal erfodert.
                if bond.name == "joint" or bond.name == "rigid_connection" or \
                        bond.name == "linear_spring_MC" or bond.name == "fixed_bearing_MC" \
                        or bond.name == "floating_bearing_MC":
                    for index, element in enumerate(intermediate_list_MC_finished[:4]):
                        x1 * zero_list + element + zero_list * (len(self.beam_list) - (2 + x1))
                        if len(intermediate_list) < (len(self.beam_list) * 4):
                            intermediate_list.append(intermediate_list_MC_finished[index])
                    del intermediate_list_MC_finished[:4]
            x1 += 1

        # print('Zwischenliste sieht nach Anpassung so aus:\n', intermediate_list, sep='')

        matrix = sp.Matrix(intermediate_list)  # Matrix wird nun als Sympy Matrix erzeugt.

        solution_vector = []  # Der Lösungsvektor wird so erstellt, dass ein Abgleich stattfindet, wie viele Indexe die
        for index, entry in enumerate(
                intermediate_list[0]):  # erste Gleichung in der Zwischenliste besitzt (da alle Glg. zu
            solution_vector.append(sp.symbols("C" + str(index + 1)))  # dem Zeitpunkt schon gleich lange sind).
        # print(solution_vector)  # Anschließend werden genau so viele C1-C... Konstanten in die Liste des Lösungsvektors
        # hinzugefügt. Hier liegt absichtlich kein Vektor vor, damit der linsolve Befehl unten funktioniert.

        disturbance_vector_ansatz = []
        for position in self.position_list:
            for bond in position.bond_list:
                if bond.typ != "matching_condition":
                    if any(bond == bind for bind in self.bond_list):
                        for entry in bond.constraints:
                            if entry is not False:
                                disturbance_vector_ansatz.append(entry)
        # Hier werden dem Störvektor die konstanten Werte der Lager, welche zuvor auf die andere Seite vom = gebracht wurden
        # hinzugefügt.

        # print("Einschränkungen added_values_MC:", self.added_values_MC)
        disturbance_vector_joint = []
        disturbance_vector_linear_spring_MC = []
        disturbance_vector_bearing_MC = []
        for position in self.position_list:
            for bond in position.bond_list:
                if bond.typ == "matching_condition":
                    # Berechnungen für den Störvektor eines Gelenks oder einer Starren Connection:
                    if bond.name == "joint" or bond.name == "rigid_connection":
                        disturbance_vector_joint. \
                            append((-1) * self.added_values_MC[0] + self.added_values_MC[4])
                        disturbance_vector_joint. \
                            append((-1) * self.added_values_MC[3] + self.added_values_MC[7])
                        disturbance_vector_joint.append((-1) * self.added_values_MC[1])
                        disturbance_vector_joint.append((-1) * self.added_values_MC[5])
                        del self.added_values_MC[:8]
                    # Mit dem oberen Befehl werden die konstanten Werte von Q(x1), w(x1), M(x1) und M(x2) *(-1) gerechnet, da diese auf die
                    # andere Seite des = gebracht wurden, und es die Vorzeichenrechnung so erfordert. Danach werden die Werte mit den
                    # bereits negierten Werten von Q(x2) und w(x2), also des jeweils rechten Balkens, addiert. Für die beiden Glg der
                    # Momente wirde nichts mehr addiert, weil hier auch nur laut bedingung ein Beam jeweils an der Rechnung beteiligt ist.
                    # Das ergibt dann wie zuvor bei den Glg. 4 Werte für den Störvektor. Wie oben bei der Bildung der Glg gilt auch hier
                    # beim Störvektor, dass die Berechnung für ein Joint und eine RigidConnection gleich abläuft. Deshalb stehen die
                    # beiden auch in der if-Abfrage.

                    # Berechnung für den Störvektor einer LinearSpring als ÜB (verbindet 2 Beam):
                    elif bond.name == "linear_spring_MC":
                        disturbance_vector_linear_spring_MC. \
                            append((-1) * (self.added_values_MC[0] + bond.spring_constant * self.added_values_MC[3]) +
                                   bond.spring_constant * self.added_values_MC[7])
                        disturbance_vector_linear_spring_MC. \
                            append((-1) * (self.added_values_MC[4]) + bond.spring_constant * self.added_values_MC[7] -
                                   bond.spring_constant * self.added_values_MC[3])
                        disturbance_vector_linear_spring_MC.append((-1) * self.added_values_MC[1])
                        disturbance_vector_linear_spring_MC.append((-1) * self.added_values_MC[5])
                        del self.added_values_MC[:8]
                    # Es werden die addierten konstanten Werte der Balkenfunktionen einmal -Q(x1)-Federsteifigkeit*w(x1)+Federsteifigkeit*
                    # w(x2) und einmal -Q(x2)-Federsteifigkeit*w(x1)+Federsteifigkeit*w(x2) gerechnet. Die konst. Werte aus den beiden Mom.
                    # werden auch *-1 gerechnet, da diese auf die andere Seite vom = müssen. Das ergibt zu den 4 Glg. die 4 Werte im Stör-
                    # vektor.

                    # Berechnung für den Störvektor eines Festlagers oder eines Loslagers als ÜB:
                    elif bond.name == "fixed_bearing_MC" or bond.name == "floating_bearing_MC":
                        disturbance_vector_bearing_MC. \
                            append((-1) * self.added_values_MC[1] + self.added_values_MC[5])
                        disturbance_vector_bearing_MC. \
                            append((-1) * self.added_values_MC[2] + self.added_values_MC[6])
                        disturbance_vector_bearing_MC.append((-1) * self.added_values_MC[3])
                        disturbance_vector_bearing_MC.append((-1) * self.added_values_MC[7])
                        del self.added_values_MC[:8]
        # Hier werden die konst. Werte von den M(x) und den phi(x) nach der Vorzeichenregel dementsprechend addiert. Weiters
        # werden die Werte der w´s nur negiert, weil sie auf die andere Seite des = kommen.

        # print("disturbance_vector_linear_spring_MC=", disturbance_vector_linear_spring_MC)
        # print("self.added_values_MC=", self.added_values_MC)

        for position in self.position_list:
            for bond in position.bond_list:
                if bond.name == "joint" or bond.name == "rigid_connection":
                    for element in disturbance_vector_joint[:4]:
                        if len(disturbance_vector_ansatz) < (len(self.beam_list) * 4):
                            disturbance_vector_ansatz.append(element)
                    del disturbance_vector_joint[:4]
                elif bond.name == "linear_spring_MC":
                    for element in disturbance_vector_linear_spring_MC[:4]:
                        if len(disturbance_vector_ansatz) < (len(self.beam_list) * 4):
                            disturbance_vector_ansatz.append(element)
                    del disturbance_vector_linear_spring_MC[:4]
                elif bond.name == "fixed_bearing_MC" or bond.name == "floating_bearing_MC":
                    for element in disturbance_vector_bearing_MC[:4]:
                        if len(disturbance_vector_ansatz) < (len(self.beam_list) * 4):
                            disturbance_vector_ansatz.append(element)
                    del disturbance_vector_bearing_MC[:4]
        # Mit Hilfe dieses Blocks werden die vorhandenen fertigen Werte auf der rechten Seite des = der Übergangsbedingungen
        # wenn noch notwendig dem Störvektor hinzugefügt.

        disturbance_vector = sp.Matrix(
            [disturbance_vector_ansatz])  # Fertig aufgefüllter Störvektor wird als Sympy Matrix erstellt.

        print(matrix, '*', solution_vector, '=', disturbance_vector)
        loesung = list(
            sp.linsolve((matrix, disturbance_vector), solution_vector))  # Hier sei gesagt, dass die erzeugte Liste auf-
        # print(loesung)    # grund des FiniteSet, welches von linsolve ausgegeben wird, immer nur ein Element hat, aber
        # print(loesung[0][7])  # dafür in diesesm Element dann die jeweiligen Lösungen ansprechbar sind als
        # loesung[0][0], loesung[0][1] usw.

        # set the solution vector to the solution attribute of the system
        for i in range(len(loesung[0])):
            self.solution.append(str(loesung[0][i]))

        for index, konstante in enumerate(loesung[0]):
            print(solution_vector[index], "=", konstante)
        # hier werden die fertigen Ergebnisse von C1-... sauber ausgegeben.


class Truss:
    """base class for beams and rigid beams"""

    def __init__(self, position_list):
        self.position_list = position_list
        self.bond_list = []
        self.connection_list = []

    def add_connection(self, new_connection):
        """adds a connection to the connection list"""
        if self.connection_list:
            if not (any(new_connection == c for c in self.connection_list)):
                self.connection_list.append(new_connection)
        else:
            self.connection_list.append(new_connection)

    def add_bond(self, new_bond):
        """adds a bond to the bond list"""
        if self.bond_list:
            if not any(new_bond == b for b in self.bond_list):
                self.bond_list.append(new_bond)
        else:
            self.bond_list.append(new_bond)


class Beam(Truss):
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
        """calculates and sets the length of the beam"""
        return sp.nsimplify(abs(positions[0].x_coordinate - positions[1].x_coordinate),
                            constants=[sp.sqrt(2), sp.sqrt(3)]) * self.symbolic_length
    
    def determine_correct_symbolic_line_load(self, line_load_string):
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
        x_i = sp.symbols(f"x_{self.beam_index}")
        self.line_load = self.determine_correct_symbolic_line_load(line_load)
        self.shear_force = sp.integrate(self.line_load, x_i)
        self.moment = sp.integrate(self.shear_force, x_i)
        self.angle_phi = sp.integrate(self.moment, x_i)
        self.deflection = sp.integrate(self.angle_phi, x_i)
        
    # i simplified the calculation for the front end - for the calculations one needs to consider the signs and "EI"
    # def set_shear_force_of_x(self):
    #     return sp.integrate(self.line_load, sp.symbols("x"))

    # def set_moment_of_x(self):
    #     return sp.integrate(self.shear_force, sp.symbols("x"))

    # def set_angle_phi_of_x(self):
    #     return sp.integrate(self.moment, sp.symbols("x"))

    # def set_deflection_of_x(self):
    #     return sp.integrate(self.angle_phi, sp.symbols("x"))
    # def set_shear_force_of_x(self):
    #     """this method calculates the shear force of x by integration of the line load"""
    #     shear_force = []
    #     # the if else is not necessary for the calculation but for aesthetics of the results
    #     if len(self.line_load) == 1 and self.line_load[0] == 0:
    #         shear_force = [-sp.Rational(1, 1)]
    #     else:
    #         for index, element in enumerate(self.line_load):
    #             shear_force.append((-1) * element * sp.Rational(1, index + 1))
    #         shear_force.insert(0, -sp.Rational(1, 1))
    #     return shear_force
    #
    # def set_moment_of_x(self):
    #     """this method calculates the moment of x by integration of the shear force"""
    #     moment = []
    #     for index, element in enumerate(self.shear_force):
    #         moment.append(element * sp.Rational(1, index + 1))
    #     moment.insert(0, -sp.Rational(1, 1))
    #     return moment
    #
    # def set_angle_phi_of_x(self):
    #     """this method calculates the angle phi of x by integration of the moment"""
    #     angle_phi = []
    #     for index, element in enumerate(self.moment):
    #         angle_phi.append(element * sp.Rational(1, index + 1))
    #     angle_phi.insert(0, -sp.Rational(1, 1))
    #     for index, zahl in enumerate(angle_phi):
    #         angle_phi[index] = angle_phi[index] * 1 / (sp.symbols("E") * sp.symbols("I"))
    #     return angle_phi
    #
    # def set_deflection_of_x(self):
    #     """this method calculates the deflection of x by integration of the angle phi"""
    #     deflection = []
    #     for index, element in enumerate(self.angle_phi):
    #         deflection.append((-1) * element * sp.Rational(1, index + 1))
    #     deflection.insert(0, 1 / (sp.symbols("E") * sp.symbols("I")))
    #     return deflection

    # def get_ansatz_of_ode(self, bearing_constraint, index):
    #     """this method returns the correct equation of the ansatz of the ode dependent on the constraint of the
    #     bearing"""
    #     if bearing_constraint and index == 0:
    #         ansatz_of_ode = self.shear_force
    #     elif bearing_constraint and index == 1:
    #         ansatz_of_ode = self.moment
    #     elif bearing_constraint and index == 2:
    #         ansatz_of_ode = self.angle_phi
    #     elif bearing_constraint and index == 3:
    #         ansatz_of_ode = self.deflection
    #     else:
    #         ansatz_of_ode = False
    #     return ansatz_of_ode


class RigidBeam(Truss):
    symbolic_length = sp.symbols("a")
    type = "rigid_beam"
    constraints = [True, True, True, True]  # don't know if this is correct, is needed for the calculation

    def __init__(self, position_list):
        super().__init__(position_list)
        self.length = self.set_length(position_list)
        self.bond = False
        self.beam_list = []
        self.in_condition_considered = False

    @staticmethod
    def set_length(positions):
        """calculates and sets the length of the beam"""
        return sp.nsimplify(abs(positions[0].x_coordinate - positions[1].x_coordinate),
                            constants=[sp.sqrt(2), sp.sqrt(3)]) * sp.symbols("a")*sp.Rational(3,2) # multiply by 3/2 so that the default length is "a"

    def add_beam(self, new_beam):
        """adds a beam to the beam list"""
        if self.beam_list:
            if not any(new_beam == b for b in self.beam_list):
                self.beam_list.append(new_beam)
        else:
            self.beam_list.append(new_beam)


class Connection:
    """base class of connections. it consists of all 'Übergangselemente' (=RigidConnection, Joint) and
    'Verbindungselemente' (=LinearSpring, TorsionalSpring)"""
    bond = False
    type = None

    def __init__(self, position_list):
        self.position_list = position_list
        self.beam_list = []
        self.in_condition_considered = False

    def add_beam(self, new_beam):
        """fügt den Beam der Balkenliste hinzu"""
        if self.beam_list:
            if not any(new_beam == b for b in self.beam_list):
                self.beam_list.append(new_beam)
        else:
            self.beam_list.append(new_beam)


class BoundaryConditionSymbol(Connection):
    """base class of boundary condition elements"""
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
    type = "fixed_bearing"

    def __init__(self, position_list):
        super().__init__(position_list)


class FloatingBearing(BoundaryConditionSymbol):
    constraints = [False, True, False, True]
    type = "floating_bearing"

    def __init__(self, position_list):
        super().__init__(position_list)


class RigidSupport(BoundaryConditionSymbol):
    """this class is for rigid supports (='feste Einspannung')"""
    constraints = [False, False, True, True]
    type = "rigid_support"

    def __init__(self, position_list):
        super().__init__(position_list)


class GuidedSupportVertical(BoundaryConditionSymbol):
    """this class is for guided supports (vertical) (='Parallelfuehrung')"""
    constraints = [True, False, True, False]
    type = "guided_support_vertical"

    def __init__(self, position_list):
        super().__init__(position_list)


class FreeEnd(BoundaryConditionSymbol):
    """this class is for free ends (='freies Ende')"""
    constraints = [True, True, False, False]
    type = "free_end"

    def __init__(self, position_list):
        super().__init__(position_list)


class TorsionalSpring(Connection):
    """this class is for torsional springs (='Drehfeder')"""
    constraints = [False, False, True, False]
    spring_constant = sp.symbols("k_\\varphi")
    type = "torsional_spring"

    def __init__(self, position_list):
        super().__init__(position_list)


class LinearSpring(Connection):
    """this class is for linear springs (='Wegfeder')"""
    constraints = [False, False, True, True]
    spring_constant = sp.symbols("k_w")
    type = "linear_spring"

    def __init__(self, position_list):
        super().__init__(position_list)


class SingleMoment(Connection):
    """this class is for single moments (='Einzelmoment')"""
    constraints = [False, False, False,
                   False]  # I'm not sure if this is correct, the variable is needed for the calculation of the solution (disabled)
    type = "single_moment"
    symbol = sp.symbols("M")
    def __init__(self, position_list, positive):
        super().__init__(position_list)
        self.positive = positive  # True = counter-clockwise, False = clockwise


class SingleForce(Connection):
    """this class is for single forces (='Einzelkraefte')"""
    constraints = [False, False, False,
                   False]  # I'm not sure if this is correct, the variable is needed for the calculation of the solution (disabled)
    type = "single_force"
    symbol = sp.symbols("F")

    def __init__(self, position_list, positive):
        super().__init__(position_list)
        self.positive = positive  # True = in positive z-direction ('down'), False = against z

class BearingConnection(Connection):
    """this class is for bearing connections"""
    type = "bearing_connection"

    def __init__(self, position_list, forces):
        super().__init__(position_list)
        self.forces = forces  # for calculation of degree of indeterminacy, 1 for floating, 2 for fixed

class MatchingConditionSymbol(Connection):
    """base class of matching condition elements"""
    bond = True
    constraints = [True, True, True, True]
    type = None

    def __init__(self, position_list):
        super().__init__(position_list)
        # self.mc_position_minus = {"position": "", "index": ""}
        # self.mc_minus_is_negative_cross_section = True

        # self.mc_position_plus = {"position": ""}
        # self.mc_plus_is_positive_cross_section = True
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
        self.mc_cons = [[{"condition": "Q", "value": []},
                         {"condition": "M", "value": []},
                         {"condition": "\\varphi", "value": []},
                         {"condition": "w", "value": []}],
                        [{"condition": "Q", "value": []},
                         {"condition": "M", "value": []},
                         {"condition": "\\varphi", "value": []},
                         {"condition": "w", "value": []}]]
        self.with_bearing = [False, False]
        self.beam_direction = [None, None] # is needed inter alia for displacement conditions
        self.rigid_lever = "" # needed for the matching conditions of bearing connections


class Joint(MatchingConditionSymbol):
    """this class is for joints (='Gelenk')"""
    constraints_frontend = [True, True, False, True]
    type = "joint"

    def __init__(self, position_list):
        super().__init__(position_list)


class RigidConnection(MatchingConditionSymbol):
    """this class is for rigid connections (='starre Verbindung')"""
    constraints_frontend = [True, True, False, True]
    type = "rigid_connection"

    def __init__(self, position_list):
        super().__init__(position_list)


class LinearSpringMC(MatchingConditionSymbol):
    """this class is for linear springs placed as matching condition (=Übergangsbedingung')"""
    spring_constant = sp.symbols("k_w")
    constraints_frontend = [True, True, False, False]  # for frontend
    type = "linear_spring_MC"

    def __init__(self, position_list):
        super().__init__(position_list)


class FixedBearingMC(MatchingConditionSymbol):
    """this class is for fixed bearings placed as matching condition (=Übergangsbedingung')"""
    constraints_frontend = [False, True, False, True]  # for frontend
    type = "bearing_MC"

    def __init__(self, position_list):
        super().__init__(position_list)


class FloatingBearingMC(MatchingConditionSymbol):
    """this class is for flaoting bearings placed as matching condition (=Übergangsbedingung')"""
    constraints_frontend = [False, True, False, True]  # for frontend
    type = "bearing_MC"

    def __init__(self, position_list):
        super().__init__(position_list)


class RigidBeamMC(MatchingConditionSymbol):
    """this class is for rigid beams placed as matching condition (=Übergangsbedingung)"""
    constraints_frontend = [True, True, True, True]
    type = "rigid_beam_MC"

    def __init__(self, position_list, rigid_right):
        super().__init__(position_list)
        self.rigid_right = rigid_right
        self.length = self.set_length(position_list)
        
    @staticmethod
    def set_length(positions):
        """calculates and sets the length of the beam"""
        return sp.nsimplify(abs(positions[0].x_coordinate - positions[1].x_coordinate),
                            constants=[sp.sqrt(2), sp.sqrt(3)]) * sp.symbols("a")*sp.Rational(3,2) # multiply by 3/2 so that the default length is "a"


class Position:
    """die Positionenklasse definiert mir die Stellen, an denen Teile zusammenstoßen - diese sind essentiell für die
    Rand- und Übergangsbedingungen. Im Endeffekt entsprechen sie den Koordinaten, die aus dem frontend kommen"""

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
        i = 0
    else:
        i = 1

    if position == beam.position_list[i]:
        x_position = 0
        sign_cross_section = True  # positive cross section; default "sign" is positive = True
    else:
        x_position = beam.length
        sign_cross_section = False  # negative cross section; default "sign" is negative = False
    
    return x_position, sign_cross_section, position, i, rigid, rigid_beam
    
    
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
                                        bond.bc_cons[1] += f"{sign_string(not sign_cross_section)}{con.spring_constant}\\,\\varphi{bond.eva_pt}{{{connection.length}}}^2"
                                elif isinstance(con, SingleForce):
                                    if position != pos:
                                        if all([con.positive, sign_cross_section]) or all([con.positive, not sign_cross_section]):
                                            sign_force = True
                                        else:
                                            sign_force = False
                                        if not beam.coordinate_system_orientation:  # the sign needs to be changed, when the orientation of the z-axis is upwards
                                            sign_force = not sign_force 
                                        bond.bc_cons[1] += f"{sign_string(sign_force)}{con.symbol}\\,{connection.length}"
                                        
                                else:
                                    extend_condition(bond, con, beam, sign_cross_section)
                else:  # rigid beam is "inside"
                    bond.bc_cons[1] += f"{sign_string((not sign_cross_section))}Q{bond.eva_pt}\\,{connection.length}"
                    bond.bc_cons[3] += f"{sign_string((sign_cross_section))}{connection.length}\\,\\varphi{bond.eva_pt}"
                    for pos in connection.position_list:
                        for con in pos.connection_list:
                            if not con.in_condition_considered:
                                con.in_condition_considered = True
                                if isinstance(con, LinearSpring):
                                    if position == pos:
                                        bond.bc_cons[1] += f"{sign_string(True)}{con.spring_constant}\\,w{bond.eva_pt}\\,{connection.length}"
                                elif isinstance(con, SingleForce):
                                    if position == pos:
                                        if all([con.positive, sign_cross_section]) or all([con.positive, not sign_cross_section]):
                                            sign_force = False
                                        else:
                                            sign_force = True
                                        if not beam.coordinate_system_orientation:  # the sign needs to be changed, when the orientation of the z-axis is upwards
                                            sign_force = not sign_force 
                                        bond.bc_cons[1] += f"{sign_string(sign_force)}{con.symbol}\\,{connection.length}"
                                else:
                                    extend_condition(bond, con, beam, sign_cross_section)
            else:
                extend_condition(bond, connection, beam, sign_cross_section)


def extend_condition(bond, connection, beam, sign_cross_section):
    if isinstance(connection, TorsionalSpring):
        bond.bc_cons[1] += f"{sign_string((not sign_cross_section))}{connection.spring_constant}\\,\\varphi{bond.eva_pt}"
    elif connection.type == "linear_spring":
        bond.bc_cons[0] += f"{sign_string((not sign_cross_section))}{connection.spring_constant}\\,w{bond.eva_pt}"
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
        bond.bc_cons[1] += f"{sign_string(sign_moment)}{connection.symbol}"
    elif isinstance(connection, SingleForce):
        if not sign_cross_section:  # the single force is subtracted at the negative cross section
            sign_force = False
        else:
            sign_force = True
        if not connection.positive:  # the sign needs to be changed, when the force is negative
            sign_force = not sign_force
        if not beam.coordinate_system_orientation:  # the sign needs to be changed, when the orientation of the z-axis is upwards
            sign_force = not sign_force 
        bond.bc_cons[0] += f"{sign_string(sign_force)}{connection.symbol}"


def determine_matching_conditions(beam, bond):
    """this function determines the matching conditions of the committed bond at the committed beam"""
        
    cross_section_is_default = True
    x_position, sign_cross_section, position, i, rigid, rigid_beam = determine_position(beam, bond)

    if len(bond.position_list)>1 and not bond.type == "rigid_beam_MC":
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
    if bond.type == "rigid_beam_MC":
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
    

    for index, entry in enumerate(bond.constraints_frontend):
        if entry:
            bond.matching_conditions[id_mc][index]["value"].append(str(0))
            if len(bond.mc_cons[id_mc][index]["condition"])<2: # due to bearing connection
                bond.mc_cons[id_mc][index]["condition"] += f"{bond.eva_pt[id_mc]}"
            bond.mc_cons[id_mc][index]["value"] = "&="
    print(bond.beam_direction)
    if isinstance(bond, LinearSpringMC): # in order to define the spring force, the deflection is set with the evaluation point and the sign of the beam direction
        bond.mc_cons[id_mc][3]["condition"] = f"{translate_boolean(bond.beam_direction[id_mc])}w{bond.eva_pt[id_mc]}"
        
    if bond.type == "rigid_beam_MC": # this is a special matching condition
        if position == bond.position_list[1]: # one needs to account for the change of the shear force and the displacement, which is incorporated on the "right side" of the rigid beam
            bond.matching_conditions[id_mc][1]["value"].append([not sign_cross_section, "rigid_beam"])
            # append the moment due to the shear force on the "positive cross section" to the moment condition (of the positive cross section)
            bond.mc_cons[1][1]["condition"] += f"{sign_string((not sign_cross_section))}Q{bond.eva_pt[1]}\\,{bond.length}"
            for pos in bond.position_list:
                if pos.beam_list:
                    if pos.beam_list[0] != beam:
                        other_beam = pos.beam_list[0]
            if other_beam.coordinate_system_orientation:
                bond.matching_conditions[id_mc][3]["value"].append([True, "rigid_beam"])        
            else:
                bond.matching_conditions[id_mc][3]["value"].append([False, "rigid_beam"])
            bond.mc_cons[1][3]["condition"] += f"{sign_string(other_beam.coordinate_system_orientation)}{bond.length}\\varphi{bond.eva_pt[1]}"

    for connection in position.connection_list:
        if not connection.in_condition_considered:
            connection.in_condition_considered = True
            if connection.type == "linear_spring":                     
                if not id_mc: # negative cross section, position_list[0] in bond
                    sign = True # the spring force is always showing "up" (against default z)
                else:
                    sign = False
                if not beam.coordinate_system_orientation:
                    sign = not sign # the sign needs to be changed, when the orientation is flipped
                bond.matching_conditions[id_mc][0]["value"].append([sign, connection.type])
                bond.mc_cons[id_mc][0]["condition"] += f"{sign_string((sign))}{connection.spring_constant}\\,w{bond.eva_pt[id_mc]}"
                
                # if the bond is a rigid beam as matching condition, a linear spring is also (and only on the right side of the rigid beam) accounted for the moment condition
                if bond.type == "rigid_beam_MC" and position == bond.position_list[1]: # the appearing spring force is accounted a the shear force and must not be incorporated for the moment condition - the reference point is the "left" side of the rigid beam
                    bond.matching_conditions[id_mc][1]["value"].append([not sign, connection.type])
                    bond.mc_cons[id_mc][1]["condition"] += f"{sign_string((not sign))}{connection.spring_constant}\\,w{bond.eva_pt[id_mc]}\\,{bond.length}"

            elif connection.type == "torsional_spring":
                # i think the following is not necessary anymore because one cannot assign properly the torsional spring to one of the two neighbouring beams at a bearing as matching condition (there is an error raise in system.py)
                # if bond.type == "bearing_MC":
                #     if cross_section:
                #         bond.matching_conditions[id_mc][1]["value"].append([False, connection.type])
                #     else:
                #         bond.matching_conditions[id_mc][1]["value"].append([True, connection.type])
                # else:
                if not id_mc:
                    sign = True # the default for the negative cross section is a positive moment
                else:
                    sign = False # the default for the positive cross section is a negative moment
                if not cross_section_is_default:
                    sign = not sign
                if not beam.coordinate_system_orientation:
                    sign = not sign # the sign needs to be changed, when the orientation is flipped (due to cross_section_default)
                bond.matching_conditions[id_mc][1]["value"].append([sign, connection.type])
                bond.mc_cons[id_mc][1]["condition"] += f"{sign_string((sign))}{connection.spring_constant}\\,\\varphi{bond.eva_pt[id_mc]}"

            elif connection.type == "single_moment":
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
                bond.matching_conditions[id_mc][1]["value"].append([sign, connection.type])
                bond.mc_cons[id_mc][1]["condition"] += f"{sign_string(sign)}{connection.symbol}"

            elif connection.type == "single_force":
                if not id_mc:
                    sign = False
                else:
                    sign = True
                if not connection.positive:
                    sign = not sign
                bond.matching_conditions[id_mc][0]["value"].append([sign, connection.type])
                bond.mc_cons[id_mc][0]["condition"] += f"{sign_string(sign)}{connection.symbol}"
                # if the bond is a rigid beam as matching condition, a linear spring is also (and only on the right side of the rigid beam) accounted for the moment condition
                if bond.type == "rigid_beam_MC" and position == bond.position_list[1]: # the appearing spring force is accounted a the shear force and must not be incorporated for the moment condition - the reference point is the "left" side of the rigid beam
                    bond.matching_conditions[id_mc][1]["value"].append([not sign, connection.type])
                    bond.mc_cons[id_mc][1]["condition"] += f"{sign_string((not sign))}{connection.symbol}\\,{bond.length}"

            elif connection.type == "rigid_beam":
                if rigid:
                    if bond.type == "bearing_MC": # the conditions of bearing MC change if there is a rigid beam
                        bond.matching_conditions[0][2]["value"].append(str(0))
                        bond.matching_conditions[1][2]["value"].append(str(0))
                    if bond.type == "linear_spring_MC":  # due to the implementation in the frontend, this is necessary for the linear spring MC
                        bond.matching_conditions[id_mc][3]["value"].append(str(0))
                    
                    if beam.position_list[i] == rigid_beam.position_list[(not i)]:
                        sign_rigid = False
                    else:
                        sign_rigid = True

                    bond.matching_conditions[id_mc][1]["value"].append([sign_rigid, connection.type])
                    # append the moment due to the shear force to the moment condition
                    bond.mc_cons[id_mc][1]["condition"] += f"{sign_string((sign_rigid))}Q{bond.eva_pt[id_mc]}\\,{connection.length}"
                    
                    if not beam.coordinate_system_orientation: # this is necessary since the orientation of the angle is changing
                        sign_rigid = not sign_rigid
                    
                    bond.matching_conditions[id_mc][3]["value"].append([not sign_rigid, connection.type])
                    # append the deflection change due to the rigid beam to the deflection condition
                    bond.mc_cons[id_mc][3]["condition"] += f"{sign_string((not sign_rigid))}{connection.length}\\,\\varphi{bond.eva_pt[id_mc]}"
                    
                    for pos in connection.position_list:
                        for con in pos.connection_list:
                            if not con.in_condition_considered:
                                con.in_condition_considered = True
                                
                                if con.type == "linear_spring":
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
                                        bond.matching_conditions[id_mc][1]["value"].append([True, con.type])
                                        # append the shear force due to the linear spring to the shear force condition
                                        bond.mc_cons[id_mc][0]["condition"] += f"{sign_string(sign_linear_spring)}{con.spring_constant}\\,w{bond.eva_pt[id_mc]}"
                                        # append the moment due to the linear spring to the moment condition
                                        bond.mc_cons[id_mc][1]["condition"] += f"{sign_string(True)}{con.spring_constant}\\,w{bond.eva_pt[id_mc]}\\,{connection.length}"
                                    else: # the linear spring is directly at the bond
                                        addition_for_shear_force = "_rigid" 

                                        sign_linear_spring = sign_rigid
                                        if not beam.coordinate_system_orientation:  # the change of the sign with the following two ifs was trial and error
                                            sign_linear_spring = not sign_linear_spring
                                        if not beam.coordinate_system_position:
                                            sign_linear_spring = not sign_linear_spring
                                        # append the shear force due to the linear spring to the shear force condition
                                        bond.mc_cons[id_mc][0]["condition"] += f"{sign_string(sign_linear_spring)}{con.spring_constant}\\,\\left[{sign_string((bond.beam_direction[id_mc]))}{bond.mc_cons[id_mc][3]['condition']}\\right]"

                                    bond.matching_conditions[id_mc][0]["value"].append([sign_linear_spring, con.type+addition_for_shear_force])
                                    
                                elif con.type == "single_force":
                                    if not id_mc:
                                        sign_force = False
                                    else:
                                        sign_force = True
                                    if not con.positive:
                                        sign_force = not sign_force
                                    bond.matching_conditions[id_mc][0]["value"].append([sign_force, con.type])
                                    bond.mc_cons[id_mc][0]["condition"] += f"{sign_string(sign_force)}{con.symbol}"

                                    sign_moment = not con.positive
                                    if not beam.coordinate_system_orientation:
                                        sign_moment = not sign_moment
                                    if pos == position:
                                        bond.matching_conditions[id_mc][1]["value"].append([sign_moment, con.type])
                                        bond.mc_cons[id_mc][1]["condition"] += f"{sign_string(sign_moment)}{con.symbol}\\,{connection.length}"
                                elif con.type == "torsional_spring":
                                    sign_torsional_spring = sign_rigid
                                    if not beam.coordinate_system_orientation:  # is necessary due to the change of the sign above (with not beam.coordinate_system_orientation)
                                        sign_torsional_spring = not sign_torsional_spring
                                    bond.matching_conditions[id_mc][1]["value"].append([sign_torsional_spring, con.type])
                                    bond.mc_cons[id_mc][1]["condition"] += f"{sign_string((sign_torsional_spring))}{con.spring_constant}\\,\\varphi{bond.eva_pt[id_mc]}"
                                elif con.type == "single_moment":
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

                                    bond.matching_conditions[id_mc][1]["value"].append([sign_moment, con.type])
                                    bond.mc_cons[id_mc][1]["condition"] += f"{sign_string(sign_moment)}{con.symbol}"

                                elif con.type == "bearing_connection":
                                    # determine sign based on coordinate system position of "other" beam
                                    bond.with_bearing[id_mc] = True
                                    # reset moment and deflection condition as they are formed anew
                                    # bond.mc_cons[id_mc][1]["condition"] = f"M{bond.eva_pt[id_mc]}"
                                    bond.mc_cons[id_mc][3]["condition"] = f"{sign_string(bond.beam_direction[id_mc])}w{bond.eva_pt[id_mc]}"
                                    for pos in bond.position_list:
                                        if pos.beam_list:
                                            if pos.beam_list[0] != beam:
                                                other_beam = pos.beam_list[0]
                                        else:
                                            for conne in pos.connection_list:
                                                if isinstance(conne, RigidBeam):
                                                    if conne.beam_list[0] != beam:
                                                        other_beam = conne.beam_list[0]
                                    if bond.type == "linear_spring_MC":
                                        if beam.coordinate_system_position:
                                            sign_moment = not sign_rigid
                                        else:
                                            sign_moment = sign_rigid
                                        bond.matching_conditions[id_mc][1]["value"].append([sign_moment, con.type])
                                        # bond.matching_conditions[id_mc][1]["value"].remove([sign_rigid, connection.type])
                                    else:
                                        if beam.coordinate_system_orientation:
                                            sign_moment = other_beam.coordinate_system_position
                                        else:
                                            sign_moment = not other_beam.coordinate_system_position
                                        if not other_beam.coordinate_system_orientation:
                                            sign_moment = not sign_moment
                                        if not id_mc:
                                            bond.matching_conditions[id_mc][1]["value"].append([sign_moment, con.type])
                                            bond.mc_cons[id_mc][1]["condition"] += f"{sign_string(sign_moment)}Q{get_eva_pt_for_other_beam(bond, other_beam)}\\,{connection.length}"
                                        else:
                                            bond.matching_conditions[id_mc][1]["value"].append([not sign_moment, con.type])
                                            bond.mc_cons[id_mc][1]["condition"] += f"{sign_string((not sign_moment))}Q{bond.eva_pt[not id_mc]}\\,{connection.length}"
                                    if beam.coordinate_system_orientation:
                                        bond.matching_conditions[id_mc][1]["value"].remove([sign_rigid, connection.type])  # the moment condition is different, therefore it is removed
                                    else:
                                        bond.matching_conditions[id_mc][1]["value"].remove([not sign_rigid, connection.type])  # the moment condition is different, therefore it is removed
                                    
                                    # i did not have another look on the determination of the sign for the displacement - it looked ok
                                    if bond.type == "linear_spring_MC":
                                        bond.rigid_lever = f"{connection.length}"
                                        bond.matching_conditions[id_mc][3]["value"].append([not sign_rigid, con.type])
                                        # if not id_mc:
                                        #     bond.mc_cons[id_mc][3]["condition"] = f"{sign_string((not sign_rigid))}{connection.length}\\varphi{bond.eva_pt[id_mc]}"
                                        # else:
                                        bond.mc_cons[id_mc][3]["condition"] = f"{translate_boolean((not sign_rigid))}{connection.length}\\varphi{bond.eva_pt[id_mc]}"
                                    else:
                                        bond.matching_conditions[id_mc][3]["value"].append([sign_rigid, con.type])
                                        if id_mc:
                                            bond.mc_cons[not id_mc][3]["condition"] += f"{sign_string((sign_rigid))}{connection.length}\\,\\varphi{bond.eva_pt[id_mc]}"
                                        else:
                                            print(bond.mc_cons[not id_mc][3]["condition"])
                                            bond.mc_cons[not id_mc][3]["condition"] += f"{get_eva_pt_for_other_beam(bond, other_beam)}{sign_string((sign_rigid))}{connection.length}\\,\\varphi{bond.eva_pt[id_mc]}"
                                    bond.matching_conditions[id_mc][3]["value"].remove([not sign_rigid, connection.type])  # the deflection condition is different, therefore it is removed

                                    
                                elif con.type == "rigid_beam": # i think this is just necessary for the joint
                                    con.in_condition_considered = False 
                else:
                    connection.in_condition_considered = False 
                    
                    
def sign_string(boolean):
    if boolean:
        return "+"
    else:
        return "-"
def translate_boolean(boolean):
    if boolean:
        return ""
    else:
        return "-"


def get_eva_pt_for_other_beam(bond, beam):
        position = None
        position_intersection = [pos for pos in beam.position_list if pos in bond.position_list]
        if not position_intersection:  # there is a rigid beam between the bond and the beam
            for posi in bond.position_list:
                for con in posi.connection_list:
                    if isinstance(con, RigidBeam):
                        other_pos = [po for po in con.position_list if po not in bond.position_list][0]
                        if any(other_pos == p for p in beam.position_list):
                            rigid_beam = con
                            position_int = [rpos for rpos in beam.position_list if rpos in rigid_beam.position_list]
                            if position_int:
                                position = position_int[0]
                            break
        else:
            position = position_intersection[0]

        if beam.coordinate_system_position:
            i = 0
        else:
            i = 1
        
        if position == beam.position_list[i]:
            x_position = 0
        else:
            x_position = beam.length
            
        return f"(x_{beam.beam_index}={x_position})"
