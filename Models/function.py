import numpy as np
import sympy as sp

class Function:
    def __init__(self, function_str):
        self.function_str = function_str
        self.parameters = {}
        self.parameter_names = []
        self.x = sp.symbols('x')
        try:
            self.function_sp_original = sp.sympify(function_str, locals={'x': self.x})
            if not isinstance(self.function_sp_original, sp.Expr):
                raise TypeError("La cadena no representa una expresión matemática válida.")
            if self.function_sp_original.is_number:
                self.parameter_names = []
            else:
                self.parameter_names = self.parse_parameters()
                for name in self.parameter_names:
                    self.parameters[name] = 1.0
        except (sp.SympifyError, TypeError, SyntaxError) as e:
            print(f"Error al procesar la cadena de función '{function_str}': {e}")
            self.function_sp_original = None
            self.parameter_names = []

        self.function_sp_param = self.get_sympy_expression_with_values()

        self.domain = None
        self.intercepts_x = []
        self.intercepts_y = []
        self.crit_points = []
        self.v_assyn = []
        self.o_assyn = []
        self.symmetry = "No calculado"
        self.derivative_1 = None
        self.derivative_2 = None
        self.monotonicity = {"increasing": [], "decreasing": []}
        self.concavity = {"concave_up": [], "concave_down": []}
        self.inflection_points = []

    def parse_parameters(self):
        if self.function_sp_original is None or self.function_sp_original.is_number:
            return []
        free_symbols = self.function_sp_original.free_symbols
        parameter_symbols = [sym for sym in free_symbols if sym != self.x]
        parameter_names_str = [str(sym) for sym in parameter_symbols]
        parameter_names_str.sort()
        return parameter_names_str

    def modify_parameters(self, new_parameter_values_dict):
        for name, value in new_parameter_values_dict.items():
            if name in self.parameter_names:
                try:
                    self.parameters[name] = float(value)
                except (ValueError, TypeError):
                    print(f"Advertencia: No se pudo convertir el valor '{value}' para el parámetro '{name}' a número. Se mantendrá el valor anterior.")
            else:
                print(f"Advertencia: El parámetro '{name}' no existe en esta función.")

        self.function_sp_param = self.get_sympy_expression_with_values()
        self.calculate_all_analysis() # Recalcular análisis cuando los parámetros cambian


    def get_sympy_expression_with_values(self):
        if self.function_sp_original is None:
            return None
        substitution_dict = {}
        for name, value in self.parameters.items():
            param_symbol = sp.symbols(name)
            substitution_dict[param_symbol] = value
        return self.function_sp_original.subs(substitution_dict)

    def evaluate(self, x_value):
        if self.function_sp_param is None:
            return np.nan
        try:
            result = self.function_sp_param.subs(self.x, x_value).evalf()
            if result.is_real:
                return float(result)
            else:
                return np.nan # No evaluar puntos complejos o imaginarios
        except (TypeError, ValueError, NotImplementedError, ZeroDivisionError) as e:
            # print(f"Error al evaluar la función en x={x_value}: {e}")
            return np.nan
        except Exception as e:
            # print(f"Error inesperado al evaluar la función en x={x_value}: {e}")
            return np.nan

    def calculate_all_analysis(self):
        print("Recalculando análisis...")
        self.calculate_domain()
        self.calculate_intercepts()
        self.check_symmetry()
        self.calculate_asymptotes()
        self.calculate_derivative(order=1)
        self.calculate_derivative(order=2)
        self.analyze_monotonicity()
        self.find_extrema()
        self.analyze_concavity()
        print("Análisis completado.")
        return {
            "domain": self.domain,
            "intercepts_x": self.intercepts_x,
            "intercepts_y": self.intercepts_y,
            "symmetry": self.symmetry,
            "v_assyn": self.v_assyn,
            "o_assyn": self.o_assyn,
            "derivative_1": self.derivative_1,
            "monotonicity": self.monotonicity,
            "crit_points": self.crit_points,
            "derivative_2": self.derivative_2,
            "concavity": self.concavity,
            "inflection_points": self.inflection_points,
        }

    def calculate_domain(self):
        expr = self.function_sp_param
        if expr is None:
            self.domain = sp.EmptySet
            return
        try:
            self.domain = sp.calculus.util.continuous_domain(expr, self.x, sp.S.Reals)
            # print(f"Dominio calculado: {self.domain}")
        except Exception as e:
            print(f"Error calculando el dominio: {e}")
            self.domain = sp.S.Reals

    def calculate_intercepts(self):
        expr = self.function_sp_param
        if expr is None or self.domain is None:
            self.intercepts_y = []
            self.intercepts_x = []
            return

        y_int = []
        try:
            if self.domain.contains(0):
                y_val = expr.subs(self.x, 0).evalf()
                if y_val.is_real and y_val.is_finite:
                    y_int = [float(y_val)]
        except Exception as e:
            print(f"Error calculando intercepto Y: {e}")
        self.intercepts_y = y_int

        x_int_list = []
        try:
            solutions = sp.solveset(expr, self.x, domain=self.domain)
            if isinstance(solutions, sp.FiniteSet):
                for sol in solutions:
                    if sol.is_real:
                        try:
                            eval_sol = float(sol.evalf())
                            if abs(self.evaluate(eval_sol)) < 1e-9: # Verificar que realmente sea cercano a cero
                                x_int_list.append(eval_sol)
                        except (TypeError, ValueError):
                            pass # Ignorar soluciones no evaluables a float
            elif isinstance(solutions, (sp.Intersection, sp.Union)):
                # Intentar manejar uniones o intersecciones si es necesario
                pass

            # Filtrar duplicados numéricos muy cercanos
            unique_x_ints = []
            if x_int_list:
                sorted_x_ints = sorted(x_int_list)
                unique_x_ints.append(sorted_x_ints[0])
                for i in range(1, len(sorted_x_ints)):
                    if not np.isclose(sorted_x_ints[i], sorted_x_ints[i-1]):
                        unique_x_ints.append(sorted_x_ints[i])

            self.intercepts_x = unique_x_ints
            # print(f"Interceptos calculados: Y={self.intercepts_y}, X={self.intercepts_x}")

        except NotImplementedError:
            print(f"No se pudo resolver simbólicamente para los interceptos X con solveset.")
            self.intercepts_x = [] # Indicar que no se pudo calcular
        except Exception as e:
            print(f"Error calculando interceptos X: {e}")
            self.intercepts_x = []

    def check_symmetry(self):
        expr = self.function_sp_param
        if expr is None:
            self.symmetry = "Error"
            return

        try:
            f_neg_x = expr.subs(self.x, -self.x)

            is_even = sp.simplify(expr - f_neg_x) == 0
            is_odd = sp.simplify(expr + f_neg_x) == 0

            if is_even:
                self.symmetry = "par"
            elif is_odd:
                self.symmetry = "impar"
            else:
                self.symmetry = "ninguna"
            # print(f"Simetría calculada: {self.symmetry}")

        except Exception as e:
            print(f"Error verificando simetría: {e}")
            self.symmetry = "Error al calcular"

    def calculate_asymptotes(self):
        expr = self.function_sp_param
        if expr is None or self.domain is None:
            self.v_assyn = []
            self.o_assyn = []
            return

        vertical = []
        horizontal = []
        oblique_expr = []

        try:
            singularities = sp.singularities(expr, self.x, domain=sp.S.Reals) # Buscar en todos los reales inicialmente
            if isinstance(singularities, sp.FiniteSet):
                for s in singularities:
                    if s.is_real:
                        # Verificar si la singularidad está excluida del dominio calculado
                        # A veces el dominio calculado puede ser más restrictivo que las singularidades simples
                        # if not self.domain.contains(s): # Esto podría ser demasiado restrictivo
                        lim_left = sp.limit(expr, self.x, s, dir='-')
                        lim_right = sp.limit(expr, self.x, s, dir='+')
                        if lim_left.is_infinite or lim_right.is_infinite:
                            vertical.append(float(s))

            lim_plus_inf = sp.limit(expr, self.x, sp.oo)
            lim_minus_inf = sp.limit(expr, self.x, -sp.oo)

            has_horizontal_plus = lim_plus_inf.is_finite
            has_horizontal_minus = lim_minus_inf.is_finite

            if has_horizontal_plus:
                h_val = float(lim_plus_inf.evalf())
                if h_val not in horizontal: horizontal.append(h_val)

            if has_horizontal_minus:
                h_val = float(lim_minus_inf.evalf())
                if h_val not in horizontal: horizontal.append(h_val)


            if not has_horizontal_plus:
                m_plus = sp.limit(expr / self.x, self.x, sp.oo)
                if m_plus.is_finite and m_plus != 0:
                    b_plus = sp.limit(expr - m_plus * self.x, self.x, sp.oo)
                    if b_plus.is_finite:
                        o_expr = m_plus * self.x + b_plus
                        if o_expr not in oblique_expr: oblique_expr.append(o_expr)


            if not has_horizontal_minus:
                m_minus = sp.limit(expr / self.x, self.x, -sp.oo)
                if m_minus.is_finite and m_minus != 0:
                    b_minus = sp.limit(expr - m_minus * self.x, self.x, -sp.oo)
                    if b_minus.is_finite:
                        o_expr = m_minus * self.x + b_minus
                        if o_expr not in oblique_expr: oblique_expr.append(o_expr)

            # Formatear salida
            self.v_assyn = sorted([f"x = {v:.2f}" for v in vertical])
            self.o_assyn = sorted([f"y = {h:.2f}" for h in horizontal] + [f"y = {sp.latex(oe)}" for oe in oblique_expr])

            # print(f"Asíntotas calculadas: V={self.v_assyn}, H/O={self.o_assyn}")

        except NotImplementedError:
            print("Error: Cálculo de límites no implementado para esta función en SymPy.")
            self.v_assyn = ["Error de cálculo"]
            self.o_assyn = ["Error de cálculo"]
        except Exception as e:
            print(f"Error calculando asíntotas: {e}")
            self.v_assyn = []
            self.o_assyn = []


    def calculate_derivative(self, order=1):
        expr = self.function_sp_param
        if expr is None:
            if order == 1: self.derivative_1 = None
            if order == 2: self.derivative_2 = None
            return None

        try:
            deriv = sp.diff(expr, self.x, order)
            # Simplificar puede ser costoso y a veces contraproducente
            # deriv = sp.simplify(deriv)
            if order == 1:
                self.derivative_1 = deriv
                # print(f"Derivada 1ra calculada: {self.derivative_1}")
            elif order == 2:
                self.derivative_2 = deriv
                # print(f"Derivada 2da calculada: {self.derivative_2}")
            return deriv
        except Exception as e:
            print(f"Error calculando derivada orden {order}: {e}")
            if order == 1: self.derivative_1 = None
            if order == 2: self.derivative_2 = None
            return None

    def analyze_monotonicity(self):
        if self.derivative_1 is None or self.domain is None:
            self.monotonicity = {"increasing": [], "decreasing": []}
            return

        increasing_intervals = []
        decreasing_intervals = []
        try:
            # Usar intervalos donde la derivada es positiva/negativa
            # solveset a veces falla o es lento con desigualdades complejas
            # Alternativa: Encontrar ceros de la derivada y probar puntos intermedios

            # 1. Encontrar puntos críticos (ceros de f' y puntos donde f' no está definida pero f sí)
            critical_zeros = sp.solveset(self.derivative_1, self.x, domain=self.domain)
            f_prime_domain = sp.calculus.util.continuous_domain(self.derivative_1, self.x, sp.S.Reals)
            critical_undefined = self.domain - f_prime_domain

            potential_critical_points = set()
            if isinstance(critical_zeros, sp.FiniteSet):
                potential_critical_points.update(sol for sol in critical_zeros if sol.is_real)
            if isinstance(critical_undefined, sp.FiniteSet):
                potential_critical_points.update(sol for sol in critical_undefined if sol.is_real)
            elif isinstance(critical_undefined, sp.Union):
                for item in critical_undefined.args:
                    if isinstance(item, sp.FiniteSet):
                        potential_critical_points.update(sol for sol in item if sol.is_real)


            # 2. Incluir puntos de discontinuidad de f (bordes del dominio)
            boundary_points = set()
            if isinstance(self.domain, sp.Interval):
                if self.domain.left_open == False and self.domain.start.is_finite: boundary_points.add(self.domain.start)
                if self.domain.right_open == False and self.domain.end.is_finite: boundary_points.add(self.domain.end)
            elif isinstance(self.domain, sp.Union):
                for interval in self.domain.args:
                    if isinstance(interval, sp.Interval):
                        if interval.left_open == False and interval.start.is_finite: boundary_points.add(interval.start)
                        if interval.right_open == False and interval.end.is_finite: boundary_points.add(interval.end)


            split_points = sorted([float(p.evalf()) for p in potential_critical_points | boundary_points])

            # 3. Probar el signo de f' en los intervalos definidos por split_points
            test_intervals = self._create_test_intervals(split_points, self.domain)

            for interval in test_intervals:
                # Tomar un punto de prueba dentro del intervalo
                if interval.start == -sp.oo and interval.end == sp.oo:
                    test_point_val = 0
                elif interval.start == -sp.oo:
                    test_point_val = float(interval.end.evalf()) - 1 if interval.end.is_finite else -1
                elif interval.end == sp.oo:
                    test_point_val = float(interval.start.evalf()) + 1 if interval.start.is_finite else 1
                else:
                    test_point_val = (float(interval.start.evalf()) + float(interval.end.evalf())) / 2

                # Asegurarse que el punto está en el dominio de f y f'
                if self.domain.contains(test_point_val) and f_prime_domain.contains(test_point_val):
                    try:
                        deriv_value = self.derivative_1.subs(self.x, test_point_val).evalf()
                        if deriv_value > 1e-9: # Tolerancia > 0
                            increasing_intervals.append(interval)
                        elif deriv_value < -1e-9: # Tolerancia < 0
                            decreasing_intervals.append(interval)
                    except (TypeError, ValueError, NotImplementedError, ZeroDivisionError):
                        print(f"No se pudo evaluar f'({test_point_val}) para monotonía.")
                        pass # No se pudo evaluar, no añadir intervalo

            self.monotonicity = {
                "increasing": self._simplify_interval_list(increasing_intervals),
                "decreasing": self._simplify_interval_list(decreasing_intervals)
            }
            # print(f"Monotonía calculada: {self.monotonicity}")

        except Exception as e:
            print(f"Error analizando monotonía: {e}")
            self.monotonicity = {"increasing": ["Error"], "decreasing": ["Error"]}


    def find_extrema(self):
        if self.derivative_1 is None or self.domain is None:
            self.crit_points = []
            return

        critical_points_data = []
        try:
            # Reutilizar puntos críticos de monotonía
            f_prime_domain = sp.calculus.util.continuous_domain(self.derivative_1, self.x, sp.S.Reals)
            critical_zeros = sp.solveset(self.derivative_1, self.x, domain=self.domain)
            critical_undefined = self.domain - f_prime_domain

            potential_critical_points = set()
            if isinstance(critical_zeros, sp.FiniteSet):
                potential_critical_points.update(sol for sol in critical_zeros if sol.is_real)
            if isinstance(critical_undefined, sp.FiniteSet):
                potential_critical_points.update(sol for sol in critical_undefined if sol.is_real)
            elif isinstance(critical_undefined, sp.Union):
                for item in critical_undefined.args:
                    if isinstance(item, sp.FiniteSet):
                        potential_critical_points.update(sol for sol in item if sol.is_real)

            sorted_candidates = sorted([float(p.evalf()) for p in potential_critical_points])

            # Usar el test de la primera derivada (cambio de signo en monotonía)
            inc = self.monotonicity.get("increasing", [])
            dec = self.monotonicity.get("decreasing", [])

            for cp_val in sorted_candidates:
                # Verificar que el punto esté en el dominio de f
                if not self.domain.contains(cp_val): continue

                y_val = self.evaluate(cp_val)
                if np.isnan(y_val): continue # Ignorar si no se puede evaluar

                point_info = {'x': cp_val, 'y': y_val, 'type': 'indefinido'}

                # Buscar cambio de decreciente a creciente (mínimo)
                change_to_inc = any(i.start == cp_val for i in inc) and any(d.end == cp_val for d in dec)
                # Buscar cambio de creciente a decreciente (máximo)
                change_to_dec = any(d.start == cp_val for d in dec) and any(i.end == cp_val for i in inc)

                if change_to_inc:
                    point_info['type'] = 'min'
                    critical_points_data.append(point_info)
                elif change_to_dec:
                    point_info['type'] = 'max'
                    critical_points_data.append(point_info)
                else:
                    # Podría ser un punto de inflexión horizontal o un punto singular no extremo
                    # Se puede usar el test de la segunda derivada como backup si f'' existe y es != 0
                    if self.derivative_2 is not None:
                        try:
                            f2_val = self.derivative_2.subs(self.x, cp_val).evalf()
                            if abs(f2_val) > 1e-9: # Si f'' != 0 y f' = 0
                                if f2_val > 0: point_info['type'] = 'min'
                                else: point_info['type'] = 'max'
                                critical_points_data.append(point_info)
                            # else: f''=0, no concluyente por 2da derivada
                        except Exception:
                            pass # No se pudo evaluar f''


            self.crit_points = sorted(critical_points_data, key=lambda p: p['x'])
            # print(f"Extremos calculados: {self.crit_points}")

        except Exception as e:
            print(f"Error encontrando extremos: {e}")
            self.crit_points = []

    def analyze_concavity(self):
        if self.derivative_2 is None or self.domain is None:
            self.concavity = {"concave_up": [], "concave_down": []}
            self.inflection_points = []
            return

        up_intervals = []
        down_intervals = []
        inflection_pts = []

        try:
            # Similar a monotonía, pero con f''
            # 1. Encontrar puntos donde f''=0 o f'' no está definida (pero f sí)
            potential_inflection_zeros = sp.solveset(self.derivative_2, self.x, domain=self.domain)
            f_double_prime_domain = sp.calculus.util.continuous_domain(self.derivative_2, self.x, sp.S.Reals)
            potential_inflection_undefined = self.domain - f_double_prime_domain

            potential_points = set()
            if isinstance(potential_inflection_zeros, sp.FiniteSet):
                potential_points.update(sol for sol in potential_inflection_zeros if sol.is_real)
            if isinstance(potential_inflection_undefined, sp.FiniteSet):
                potential_points.update(sol for sol in potential_inflection_undefined if sol.is_real)
            elif isinstance(potential_inflection_undefined, sp.Union):
                for item in potential_inflection_undefined.args:
                    if isinstance(item, sp.FiniteSet):
                        potential_points.update(sol for sol in item if sol.is_real)


            # 2. Incluir puntos de discontinuidad de f
            boundary_points = set()
            if isinstance(self.domain, sp.Interval):
                if self.domain.left_open == False and self.domain.start.is_finite: boundary_points.add(self.domain.start)
                if self.domain.right_open == False and self.domain.end.is_finite: boundary_points.add(self.domain.end)
            elif isinstance(self.domain, sp.Union):
                for interval in self.domain.args:
                    if isinstance(interval, sp.Interval):
                        if interval.left_open == False and interval.start.is_finite: boundary_points.add(interval.start)
                        if interval.right_open == False and interval.end.is_finite: boundary_points.add(interval.end)

            split_points = sorted([float(p.evalf()) for p in potential_points | boundary_points])

            # 3. Probar el signo de f'' en los intervalos
            test_intervals = self._create_test_intervals(split_points, self.domain)

            for interval in test_intervals:
                if interval.start == -sp.oo and interval.end == sp.oo:
                    test_point_val = 0
                elif interval.start == -sp.oo:
                    test_point_val = float(interval.end.evalf()) - 1 if interval.end.is_finite else -1
                elif interval.end == sp.oo:
                    test_point_val = float(interval.start.evalf()) + 1 if interval.start.is_finite else 1
                else:
                    test_point_val = (float(interval.start.evalf()) + float(interval.end.evalf())) / 2

                # Asegurarse que el punto está en el dominio de f y f''
                if self.domain.contains(test_point_val) and f_double_prime_domain.contains(test_point_val):
                    try:
                        deriv2_value = self.derivative_2.subs(self.x, test_point_val).evalf()
                        if deriv2_value > 1e-9:
                            up_intervals.append(interval)
                        elif deriv2_value < -1e-9:
                            down_intervals.append(interval)
                    except (TypeError, ValueError, NotImplementedError, ZeroDivisionError):
                        print(f"No se pudo evaluar f''({test_point_val}) para concavidad.")
                        pass

            self.concavity = {
                "concave_up": self._simplify_interval_list(up_intervals),
                "concave_down": self._simplify_interval_list(down_intervals)
            }

            # 4. Identificar puntos de inflexión donde cambia la concavidad
            all_potential_inf_vals = sorted([float(p.evalf()) for p in potential_points if p.is_real and self.domain.contains(p)])

            for p_val in all_potential_inf_vals:
                is_inflection = False
                # Verificar si p_val es el límite entre un intervalo cóncavo hacia arriba y uno hacia abajo
                concavity_change = any(i.start == p_val for i in up_intervals) and any(d.end == p_val for d in down_intervals)
                concavity_change = concavity_change or (any(i.end == p_val for i in up_intervals) and any(d.start == p_val for d in down_intervals))

                if concavity_change:
                    # Asegurar que la función está definida en p_val
                    if not np.isnan(self.evaluate(p_val)):
                        inflection_pts.append(p_val)

            self.inflection_points = sorted(list(set(inflection_pts))) # Eliminar duplicados
            # print(f"Concavidad calculada: {self.concavity}")
            # print(f"Puntos de inflexión calculados: {self.inflection_points}")

        except Exception as e:
            print(f"Error analizando concavidad: {e}")
            self.concavity = {"concave_up": ["Error"], "concave_down": ["Error"]}
            self.inflection_points = []

    # --------------------------------------------------
    #  Métodos Auxiliares
    # --------------------------------------------------

    def _sympy_set_to_interval_list(self, s_set):
        intervals = []
        if isinstance(s_set, sp.Interval):
            intervals.append(s_set)
        elif isinstance(s_set, sp.Union):
            for item in s_set.args:
                if isinstance(item, sp.Interval):
                    intervals.append(item)
                elif isinstance(item, sp.FiniteSet):
                    # Podría ocurrir si la desigualdad es verdadera/falsa solo en puntos aislados
                    pass
        elif isinstance(s_set, sp.FiniteSet):
            pass
        elif isinstance(s_set, sp.ConditionSet):
            print("Advertencia: El resultado de solveset es un ConditionSet, no se puede convertir a lista de intervalos fácilmente.")

        try:
            intervals.sort(key=lambda i: i.start if hasattr(i, 'start') else -sp.oo)
        except Exception:
            pass
        return intervals

    def _create_test_intervals(self, split_points, domain_set):
        """Crea intervalos de prueba basados en puntos de división y el dominio."""
        intervals = []
        sorted_points = sorted(list(set(split_points))) # Unicos y ordenados

        # Añadir -oo y +oo como límites si el dominio no está acotado
        domain_intervals = []
        if isinstance(domain_set, sp.Interval):
            domain_intervals.append(domain_set)
        elif isinstance(domain_set, sp.Union):
            for item in domain_set.args:
                if isinstance(item, sp.Interval):
                    domain_intervals.append(item)
        elif isinstance(domain_set, sp.EmptySet):
            return []
        elif domain_set == sp.S.Reals:
            domain_intervals.append(sp.Interval(-sp.oo, sp.oo))

        if not domain_intervals: return [] # Si no hay intervalos en el dominio

        # Procesar cada intervalo del dominio
        for domain_interval in domain_intervals:
            start = domain_interval.start
            end = domain_interval.end
            relevant_points = [p for p in sorted_points if domain_interval.contains(p)]

            current_start = start
            for point in relevant_points:
                if current_start < point:
                    intervals.append(sp.Interval(current_start, point, left_open= not domain_interval.contains(current_start), right_open=True))
                current_start = point # El punto en sí no es un intervalo

            # Último intervalo hasta el final del dominio
            if current_start < end:
                intervals.append(sp.Interval(current_start, end, left_open=True, right_open= not domain_interval.contains(end)))

        # Filtrar intervalos vacíos o puntos
        valid_intervals = [i for i in intervals if i.measure > 0]
        return valid_intervals


    def _simplify_interval_list(self, interval_list):
        """Intenta unir intervalos adyacentes o superpuestos."""
        if not interval_list: return []

        # Asegurar que todos son intervalos y ordenar
        intervals = sorted([i for i in interval_list if isinstance(i, sp.Interval)],
                           key=lambda i: i.start)

        if not intervals: return []

        merged = [intervals[0]]
        for current in intervals[1:]:
            previous = merged[-1]
            # Si se superponen o son adyacentes (permitiendo puntos cerrados)
            if current.start <= previous.end:
                # Unir tomando el máximo final y ajustando aperturas
                new_end = max(previous.end, current.end)
                # La nueva unión es abierta a la derecha si AMBOS lo eran en el punto de unión, O si el final es el de current y current era abierto
                new_right_open = (previous.right_open and current.start == previous.end and current.left_open) or \
                                 (new_end == current.end and current.right_open)

                merged[-1] = sp.Interval(previous.start, new_end, previous.left_open, new_right_open)
            else:
                merged.append(current)
        return merged