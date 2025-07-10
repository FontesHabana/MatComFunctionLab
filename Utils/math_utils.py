"""
Mathematical utility functions for function analysis.

This module provides helper functions for mathematical operations,
expression evaluation, and number validation.
"""

import sympy as sp
import numpy as np
from typing import Union, Dict, Any, Optional


def is_real_number(value: Any) -> bool:
    """
    Check if a given value is a real number (integer or float).
    
    Args:
        value: The value to check
        
    Returns:
        bool: True if the value is a real number, False otherwise
    """
    try:
        # Check if it's already a number
        if isinstance(value, (int, float)):
            # Check for NaN and infinity
            if isinstance(value, float):
                return not (np.isnan(value) or np.isinf(value))
            return True
        
        # Try to convert string to float
        if isinstance(value, str):
            float_val = float(value)
            return not (np.isnan(float_val) or np.isinf(float_val))
        
        # Check if it's a sympy number
        if hasattr(value, 'is_real') and hasattr(value, 'is_finite'):
            return bool(value.is_real and value.is_finite)
        
        return False
    except (ValueError, TypeError, AttributeError):
        return False


def evaluate_expression(expression: str, x_value: Union[int, float], params: Optional[Dict[str, Union[int, float]]] = None) -> Optional[float]:
    """
    Evaluate a mathematical expression at a given x value with optional parameters.
    
    Args:
        expression: String representation of a mathematical function
        x_value: The value at which to evaluate the expression
        params: Optional dictionary of parameter names and values to substitute
        
    Returns:
        float: The evaluated result, or None if evaluation fails
    """
    try:
        # Validate inputs
        if not isinstance(expression, str) or not expression.strip():
            return None
        
        if not is_real_number(x_value):
            return None
        
        # Create sympy symbol for x
        x = sp.Symbol('x')
        
        # Parse the expression
        try:
            expr = sp.sympify(expression)
        except (sp.SympifyError, ValueError, TypeError):
            return None
        
        # Substitute parameters if provided
        if params:
            try:
                # Validate parameters
                validated_params = {}
                for param_name, param_value in params.items():
                    if not isinstance(param_name, str):
                        continue
                    if not is_real_number(param_value):
                        continue
                    validated_params[sp.Symbol(param_name)] = float(param_value)
                
                if validated_params:
                    expr = expr.subs(validated_params)
            except (TypeError, ValueError, AttributeError):
                # Continue without parameter substitution if it fails
                pass
        
        # Substitute x value
        result = expr.subs(x, float(x_value))
        
        # Convert to float
        try:
            # Handle complex results
            if result.is_real is False or (hasattr(result, 'im') and result.im != 0):
                return None
            
            float_result = float(result.evalf())
            
            # Check for invalid results
            if np.isnan(float_result) or np.isinf(float_result):
                return None
            
            return float_result
            
        except (ValueError, TypeError, AttributeError):
            return None
    
    except Exception:
        # Catch any unexpected errors
        return None


# Additional utility functions for common mathematical operations

def safe_log(value: Union[int, float], base: Union[int, float] = np.e) -> Optional[float]:
    """
    Safely compute logarithm, returning None for invalid inputs.
    
    Args:
        value: The value to compute log of
        base: The logarithm base (default: natural log)
        
    Returns:
        float: The logarithm result, or None if invalid
    """
    try:
        if not is_real_number(value) or not is_real_number(base):
            return None
        
        if value <= 0 or base <= 0 or base == 1:
            return None
        
        if base == np.e:
            result = np.log(value)
        else:
            result = np.log(value) / np.log(base)
        
        return result if not (np.isnan(result) or np.isinf(result)) else None
    
    except Exception:
        return None


def safe_sqrt(value: Union[int, float]) -> Optional[float]:
    """
    Safely compute square root, returning None for negative values.
    
    Args:
        value: The value to compute square root of
        
    Returns:
        float: The square root result, or None if invalid
    """
    try:
        if not is_real_number(value):
            return None
        
        if value < 0:
            return None
        
        result = np.sqrt(value)
        return result if not (np.isnan(result) or np.isinf(result)) else None
    
    except Exception:
        return None


def safe_power(base: Union[int, float], exponent: Union[int, float]) -> Optional[float]:
    """
    Safely compute power operation, handling edge cases.
    
    Args:
        base: The base value
        exponent: The exponent value
        
    Returns:
        float: The power result, or None if invalid
    """
    try:
        if not is_real_number(base) or not is_real_number(exponent):
            return None
        
        # Handle special cases
        if base == 0 and exponent < 0:
            return None  # Division by zero
        
        if base < 0 and not isinstance(exponent, int) and exponent != int(exponent):
            return None  # Complex result
        
        result = np.power(base, exponent)
        return result if not (np.isnan(result) or np.isinf(result)) else None
    
    except Exception:
        return None
