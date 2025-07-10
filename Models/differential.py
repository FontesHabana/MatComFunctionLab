"""
Differential calculus module for computing derivatives.

This module provides the DifferentialCalculator class that computes
first and second derivatives of mathematical functions using SymPy.
"""

import sympy as sp
from sympy import diff, Symbol
from typing import Optional, Union


class DifferentialCalculator:
    """
    A calculator for computing derivatives of mathematical functions.
    
    This class provides methods to compute first and second derivatives
    of SymPy expressions with robust error handling.
    """
    
    def __init__(self, sympy_function: sp.Expr, variable: Symbol):
        """
        Initialize the DifferentialCalculator.
        
        Args:
            sympy_function: The SymPy expression to differentiate
            variable: The SymPy symbol representing the variable of differentiation
        """
        self.function = sympy_function
        self.variable = variable
        self._first_derivative = None
        self._second_derivative = None
    
    def get_first_derivative(self) -> Optional[sp.Expr]:
        """
        Calculate and return the first derivative of the function.
        
        Returns:
            SymPy expression representing the first derivative, or None if calculation fails
        """
        try:
            if self._first_derivative is None:
                self._first_derivative = diff(self.function, self.variable)
            return self._first_derivative
        except Exception as e:
            # Handle any differentiation errors
            print(f"Error calculating first derivative: {e}")
            return None
    
    def get_second_derivative(self) -> Optional[sp.Expr]:
        """
        Calculate and return the second derivative of the function.
        
        Returns:
            SymPy expression representing the second derivative, or None if calculation fails
        """
        try:
            if self._second_derivative is None:
                # Calculate second derivative directly or from first derivative
                first_deriv = self.get_first_derivative()
                if first_deriv is not None:
                    self._second_derivative = diff(first_deriv, self.variable)
                else:
                    # Try direct calculation if first derivative failed
                    self._second_derivative = diff(self.function, self.variable, 2)
            return self._second_derivative
        except Exception as e:
            # Handle any differentiation errors
            print(f"Error calculating second derivative: {e}")
            return None
    
    def get_derivative(self, order: int = 1) -> Optional[sp.Expr]:
        """
        Calculate and return the nth derivative of the function.
        
        Args:
            order: The order of the derivative (1 for first, 2 for second, etc.)
            
        Returns:
            SymPy expression representing the nth derivative, or None if calculation fails
        """
        try:
            if order <= 0:
                return self.function
            elif order == 1:
                return self.get_first_derivative()
            elif order == 2:
                return self.get_second_derivative()
            else:
                # For higher order derivatives
                return diff(self.function, self.variable, order)
        except Exception as e:
            print(f"Error calculating derivative of order {order}: {e}")
            return None
    
    def evaluate_derivative(self, order: int, x_value: Union[int, float]) -> Optional[float]:
        """
        Evaluate the nth derivative at a specific point.
        
        Args:
            order: The order of the derivative
            x_value: The value at which to evaluate the derivative
            
        Returns:
            The numerical value of the derivative at x_value, or None if evaluation fails
        """
        try:
            derivative = self.get_derivative(order)
            if derivative is None:
                return None
            
            # Substitute the value and evaluate
            result = derivative.subs(self.variable, x_value)
            
            # Convert to float if possible
            if result.is_real and result.is_finite:
                return float(result.evalf())
            else:
                return None
                
        except Exception as e:
            print(f"Error evaluating derivative of order {order} at x={x_value}: {e}")
            return None
    
    def get_derivative_info(self) -> dict:
        """
        Get comprehensive information about the derivatives.
        
        Returns:
            Dictionary containing the function and its first and second derivatives
        """
        return {
            'original_function': str(self.function),
            'variable': str(self.variable),
            'first_derivative': str(self.get_first_derivative()) if self.get_first_derivative() is not None else None,
            'second_derivative': str(self.get_second_derivative()) if self.get_second_derivative() is not None else None
        }
    
    def reset_cache(self):
        """
        Reset the cached derivative values.
        
        This method clears the cached first and second derivatives,
        forcing recalculation on the next call.
        """
        self._first_derivative = None
        self._second_derivative = None
    
    def update_function(self, new_function: sp.Expr, new_variable: Optional[Symbol] = None):
        """
        Update the function and optionally the variable.
        
        Args:
            new_function: The new SymPy expression
            new_variable: Optional new variable symbol
        """
        self.function = new_function
        if new_variable is not None:
            self.variable = new_variable
        self.reset_cache()


# Utility functions for common derivative operations

def compute_derivative(expression: str, variable_name: str = 'x', order: int = 1) -> Optional[str]:
    """
    Utility function to compute derivative from string expression.
    
    Args:
        expression: String representation of the mathematical function
        variable_name: Name of the variable (default: 'x')
        order: Order of the derivative (default: 1)
        
    Returns:
        String representation of the derivative, or None if calculation fails
    """
    try:
        # Parse the expression
        var = Symbol(variable_name)
        func = sp.sympify(expression)
        
        # Create calculator and compute derivative
        calculator = DifferentialCalculator(func, var)
        derivative = calculator.get_derivative(order)
        
        return str(derivative) if derivative is not None else None
        
    except Exception as e:
        print(f"Error computing derivative: {e}")
        return None


def find_critical_points_numeric(expression: str, variable_name: str = 'x', 
                                domain_start: float = -10, domain_end: float = 10) -> list:
    """
    Find critical points numerically by solving first derivative = 0.
    
    Args:
        expression: String representation of the mathematical function
        variable_name: Name of the variable (default: 'x')
        domain_start: Start of the domain to search (default: -10)
        domain_end: End of the domain to search (default: 10)
        
    Returns:
        List of critical points as float values
    """
    try:
        var = Symbol(variable_name)
        func = sp.sympify(expression)
        
        calculator = DifferentialCalculator(func, var)
        first_deriv = calculator.get_first_derivative()
        
        if first_deriv is None:
            return []
        
        # Solve first derivative = 0
        critical_points = sp.solve(first_deriv, var)
        
        # Filter real solutions within domain
        real_points = []
        for point in critical_points:
            if point.is_real:
                val = float(point.evalf())
                if domain_start <= val <= domain_end:
                    real_points.append(val)
        
        return sorted(real_points)
        
    except Exception as e:
        print(f"Error finding critical points: {e}")
        return []
