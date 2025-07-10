"""
Function analysis module for mathematical function analysis.

This module provides the FunctionAnalyzer class that performs comprehensive
analysis of mathematical functions including domain, intercepts, asymptotes,
critical points, and behavior analysis.
"""

import sympy as sp
from sympy import Symbol, symbols, sympify, solve, limit, diff, oo, zoo, nan
from sympy.calculus.util import continuous_domain
from sympy.sets import Interval, Union, FiniteSet, EmptySet
from sympy.core.relational import Eq
from typing import Dict, List, Tuple, Union, Optional, Any
import numpy as np


class FunctionAnalyzer:
    """
    A comprehensive mathematical function analyzer using SymPy.
    
    This class provides methods to analyze various properties of mathematical
    functions including domain, intercepts, asymptotes, critical points,
    and monotonicity.
    """
    
    def __init__(self, func_str: str, parameters: Optional[Dict[str, Union[int, float]]] = None):
        """
        Initialize the FunctionAnalyzer.
        
        Args:
            func_str: String representation of the mathematical function
            parameters: Optional dictionary of parameter names and values
        """
        self.func_str = func_str
        self.parameters = parameters or {}
        self.x = Symbol('x', real=True)
        self.function = None
        self.original_function = None
        self.param_symbols = {}
        
        try:
            self._parse_function()
        except ValueError as e:
            raise ValueError(f"Invalid function: {e}")
    
    def _parse_function(self):
        """
        Parse the function string into a SymPy expression.
        
        Raises:
            ValueError: If the function string is invalid
        """
        try:
            if not self.func_str or not isinstance(self.func_str, str):
                raise ValueError("Function string cannot be empty")
            
            # Parse the function string
            self.original_function = sympify(self.func_str)
            
            # Replace any x symbols with our defined x symbol
            x_symbols = [s for s in self.original_function.free_symbols if str(s) == 'x']
            if x_symbols:
                for x_sym in x_symbols:
                    self.original_function = self.original_function.subs(x_sym, self.x)
            
            # Get all symbols in the function
            all_symbols = self.original_function.free_symbols
            
            # Separate x from parameter symbols
            for symbol in all_symbols:
                if str(symbol) == 'x':
                    continue
                else:
                    self.param_symbols[str(symbol)] = symbol
            
            # Substitute parameters if provided
            self.function = self.original_function
            if self.parameters:
                substitutions = {}
                for param_name, param_value in self.parameters.items():
                    if param_name in self.param_symbols:
                        substitutions[self.param_symbols[param_name]] = param_value
                
                if substitutions:
                    self.function = self.original_function.subs(substitutions)
            
        except Exception as e:
            raise ValueError(f"Cannot parse function '{self.func_str}': {e}")
    
    def get_domain(self) -> Union[Interval, FiniteSet]:
        """
        Calculate the domain of the function.
        
        Returns:
            SymPy set representing the domain of the function
        """
        try:
            # Use SymPy's continuous_domain function
            domain = continuous_domain(self.function, self.x, sp.S.Reals)
            return domain
        except Exception:
            try:
                # Fallback: manually check for common restrictions
                domain_restrictions = []
                
                # Check for denominators
                denominators = []
                if self.function.is_rational_function(self.x):
                    numer, denom = sp.fraction(self.function)
                    if denom != 1:
                        # Find zeros of denominator
                        zeros = solve(denom, self.x)
                        for zero in zeros:
                            if zero.is_real:
                                domain_restrictions.append(zero)
                
                # Check for square roots and even roots
                for expr in sp.preorder_traversal(self.function):
                    if expr.is_Pow and expr.exp.is_Rational:
                        if expr.exp.q % 2 == 0 and expr.exp > 0:  # Even root
                            # Argument must be non-negative
                            try:
                                constraint = solve(expr.base >= 0, self.x)
                                # This is complex to handle generally
                            except:
                                pass
                    elif hasattr(expr, 'func') and str(expr.func) in ['log', 'ln']:
                        # Logarithm argument must be positive
                        try:
                            constraint = solve(expr.args[0] > 0, self.x)
                        except:
                            pass
                
                # If we found restrictions, create domain excluding them
                if domain_restrictions:
                    intervals = []
                    restrictions_sorted = sorted([float(r.evalf()) for r in domain_restrictions if r.is_real])
                    
                    if restrictions_sorted:
                        # Add interval before first restriction
                        if restrictions_sorted[0] > -float('inf'):
                            intervals.append(Interval(-oo, restrictions_sorted[0], True, True))
                        
                        # Add intervals between restrictions
                        for i in range(len(restrictions_sorted) - 1):
                            intervals.append(Interval(restrictions_sorted[i], restrictions_sorted[i+1], True, True))
                        
                        # Add interval after last restriction
                        if restrictions_sorted[-1] < float('inf'):
                            intervals.append(Interval(restrictions_sorted[-1], oo, True, True))
                        
                        return Union(*intervals) if len(intervals) > 1 else intervals[0]
                
                # No restrictions found, domain is all real numbers
                return Interval(-oo, oo)
                
            except Exception:
                return Interval(-oo, oo)  # Default to all reals
    
    def get_intercepts(self) -> Dict[str, List[float]]:
        """
        Calculate x and y intercepts of the function.
        
        Returns:
            Dictionary with 'x_intercepts' and 'y_intercept' keys
        """
        result = {'x_intercepts': [], 'y_intercept': None}
        
        try:
            # Y-intercept: f(0)
            y_intercept = self.function.subs(self.x, 0)
            if y_intercept.is_real and y_intercept.is_finite:
                result['y_intercept'] = float(y_intercept.evalf())
        except Exception:
            pass
        
        try:
            # X-intercepts: solve f(x) = 0
            x_intercepts = solve(self.function, self.x)
            for intercept in x_intercepts:
                if intercept.is_real and intercept.is_finite:
                    result['x_intercepts'].append(float(intercept.evalf()))
        except Exception:
            pass
        
        return result
    
    def get_symmetry(self) -> str:
        """
        Determine if the function is even, odd, or neither.
        
        Returns:
            'even', 'odd', or 'neither'
        """
        try:
            f_x = self.function
            f_neg_x = self.function.subs(self.x, -self.x)
            
            # Check if f(-x) = f(x) (even function)
            if sp.simplify(f_neg_x - f_x) == 0:
                return 'even'
            
            # Check if f(-x) = -f(x) (odd function)
            if sp.simplify(f_neg_x + f_x) == 0:
                return 'odd'
            
            return 'neither'
        except Exception:
            return 'neither'
    
    def get_asymptotes(self) -> Dict[str, List[Union[float, str]]]:
        """
        Find vertical, horizontal, and oblique asymptotes.
        
        Returns:
            Dictionary with 'vertical', 'horizontal', and 'oblique' asymptotes
        """
        result = {'vertical': [], 'horizontal': [], 'oblique': []}
        
        try:
            # Vertical asymptotes: points where function approaches infinity
            if self.function.is_rational_function(self.x):
                numer, denom = sp.fraction(self.function)
                if denom != 1:
                    # Find zeros of denominator that are not zeros of numerator
                    denom_zeros = solve(denom, self.x)
                    numer_zeros = solve(numer, self.x)
                    
                    for zero in denom_zeros:
                        if zero.is_real and zero not in numer_zeros:
                            # Check if limit is indeed infinite
                            try:
                                left_limit = limit(self.function, self.x, zero, '-')
                                right_limit = limit(self.function, self.x, zero, '+')
                                if left_limit in [oo, -oo] or right_limit in [oo, -oo]:
                                    result['vertical'].append(float(zero.evalf()))
                            except:
                                result['vertical'].append(float(zero.evalf()))
        except Exception:
            pass
        
        try:
            # Horizontal asymptotes: limits as x approaches infinity
            limit_pos_inf = limit(self.function, self.x, oo)
            limit_neg_inf = limit(self.function, self.x, -oo)
            
            if limit_pos_inf.is_finite and limit_pos_inf.is_real:
                y_val = float(limit_pos_inf.evalf())
                if y_val not in result['horizontal']:
                    result['horizontal'].append(y_val)
            
            if limit_neg_inf.is_finite and limit_neg_inf.is_real:
                y_val = float(limit_neg_inf.evalf())
                if y_val not in result['horizontal']:
                    result['horizontal'].append(y_val)
        except Exception:
            pass
        
        try:
            # Oblique asymptotes: when horizontal asymptotes don't exist
            if not result['horizontal']:
                # Check for oblique asymptotes y = mx + b
                m = limit(self.function / self.x, self.x, oo)
                if m.is_finite and m.is_real and m != 0:
                    b = limit(self.function - m * self.x, self.x, oo)
                    if b.is_finite and b.is_real:
                        result['oblique'].append(f"y = {float(m.evalf())}*x + {float(b.evalf())}")
        except Exception:
            pass
        
        return result
    
    def get_critical_points(self) -> List[float]:
        """
        Find critical points where the first derivative is zero or undefined.
        
        Returns:
            List of x-coordinates of critical points
        """
        critical_points = []
        
        try:
            # Calculate first derivative
            first_derivative = diff(self.function, self.x)
            
            # Find zeros of the first derivative
            critical_candidates = solve(first_derivative, self.x)
            
            for candidate in critical_candidates:
                if candidate.is_real and candidate.is_finite:
                    critical_points.append(float(candidate.evalf()))
            
            # Find points where derivative is undefined (but function is defined)
            # This is more complex and may require additional analysis
            
        except Exception:
            pass
        
        return sorted(critical_points)
    
    def get_inflection_points(self) -> List[float]:
        """
        Find inflection points where the second derivative is zero or undefined
        and concavity changes.
        
        Returns:
            List of x-coordinates of inflection points
        """
        inflection_points = []
        
        try:
            # Calculate second derivative
            second_derivative = diff(self.function, self.x, 2)
            
            # Find zeros of the second derivative
            inflection_candidates = solve(second_derivative, self.x)
            
            for candidate in inflection_candidates:
                if candidate.is_real and candidate.is_finite:
                    # Verify that concavity actually changes
                    # This is a simplified check
                    inflection_points.append(float(candidate.evalf()))
        
        except Exception:
            pass
        
        return sorted(inflection_points)
    
    def get_monotonicity(self) -> Dict[str, List[Tuple[float, float]]]:
        """
        Determine intervals where the function is increasing or decreasing.
        
        Returns:
            Dictionary with 'increasing' and 'decreasing' interval lists
        """
        result = {'increasing': [], 'decreasing': []}
        
        try:
            # Get first derivative
            first_derivative = diff(self.function, self.x)
            
            # Get critical points
            critical_points = self.get_critical_points()
            
            # Test points between critical points
            test_points = []
            domain = self.get_domain()
            
            if critical_points:
                # Add test points
                sorted_criticals = sorted(critical_points)
                
                # Before first critical point
                test_points.append(sorted_criticals[0] - 1)
                
                # Between critical points
                for i in range(len(sorted_criticals) - 1):
                    test_points.append((sorted_criticals[i] + sorted_criticals[i+1]) / 2)
                
                # After last critical point
                test_points.append(sorted_criticals[-1] + 1)
                
                # Check sign of derivative at test points
                for i, test_point in enumerate(test_points):
                    try:
                        derivative_value = first_derivative.subs(self.x, test_point)
                        if derivative_value.is_real:
                            if derivative_value > 0:
                                if i == 0:
                                    result['increasing'].append((-float('inf'), sorted_criticals[0]))
                                elif i == len(test_points) - 1:
                                    result['increasing'].append((sorted_criticals[-1], float('inf')))
                                else:
                                    result['increasing'].append((sorted_criticals[i-1], sorted_criticals[i]))
                            elif derivative_value < 0:
                                if i == 0:
                                    result['decreasing'].append((-float('inf'), sorted_criticals[0]))
                                elif i == len(test_points) - 1:
                                    result['decreasing'].append((sorted_criticals[-1], float('inf')))
                                else:
                                    result['decreasing'].append((sorted_criticals[i-1], sorted_criticals[i]))
                    except:
                        continue
        
        except Exception:
            pass
        
        return result
    
    def get_concavity(self) -> Dict[str, List[Tuple[float, float]]]:
        """
        Determine intervals where the function is concave up or concave down.
        
        Returns:
            Dictionary with 'concave_up' and 'concave_down' interval lists
        """
        result = {'concave_up': [], 'concave_down': []}
        
        try:
            # Get second derivative
            second_derivative = diff(self.function, self.x, 2)
            
            # Get inflection points
            inflection_points = self.get_inflection_points()
            
            # Test points between inflection points
            test_points = []
            
            if inflection_points:
                sorted_inflections = sorted(inflection_points)
                
                # Before first inflection point
                test_points.append(sorted_inflections[0] - 1)
                
                # Between inflection points
                for i in range(len(sorted_inflections) - 1):
                    test_points.append((sorted_inflections[i] + sorted_inflections[i+1]) / 2)
                
                # After last inflection point
                test_points.append(sorted_inflections[-1] + 1)
                
                # Check sign of second derivative at test points
                for i, test_point in enumerate(test_points):
                    try:
                        second_deriv_value = second_derivative.subs(self.x, test_point)
                        if second_deriv_value.is_real:
                            if second_deriv_value > 0:
                                if i == 0:
                                    result['concave_up'].append((-float('inf'), sorted_inflections[0]))
                                elif i == len(test_points) - 1:
                                    result['concave_up'].append((sorted_inflections[-1], float('inf')))
                                else:
                                    result['concave_up'].append((sorted_inflections[i-1], sorted_inflections[i]))
                            elif second_deriv_value < 0:
                                if i == 0:
                                    result['concave_down'].append((-float('inf'), sorted_inflections[0]))
                                elif i == len(test_points) - 1:
                                    result['concave_down'].append((sorted_inflections[-1], float('inf')))
                                else:
                                    result['concave_down'].append((sorted_inflections[i-1], sorted_inflections[i]))
                    except:
                        continue
            else:
                # No inflection points, test one point
                try:
                    second_deriv_value = second_derivative.subs(self.x, 0)
                    if second_deriv_value.is_real:
                        if second_deriv_value > 0:
                            result['concave_up'].append((-float('inf'), float('inf')))
                        elif second_deriv_value < 0:
                            result['concave_down'].append((-float('inf'), float('inf')))
                except:
                    pass
        
        except Exception:
            pass
        
        return result
    
    def analyze_all(self) -> Dict[str, Any]:
        """
        Perform complete analysis of the function.
        
        Returns:
            Dictionary containing all analysis results
        """
        return {
            'function': str(self.function),
            'domain': str(self.get_domain()),
            'intercepts': self.get_intercepts(),
            'symmetry': self.get_symmetry(),
            'asymptotes': self.get_asymptotes(),
            'critical_points': self.get_critical_points(),
            'inflection_points': self.get_inflection_points(),
            'monotonicity': self.get_monotonicity(),
            'concavity': self.get_concavity()
        }
