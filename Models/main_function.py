"""
Main function processor module for comprehensive function analysis.

This module provides the MainFunctionProcessor class that orchestrates
complete mathematical function analysis by coordinating FunctionAnalyzer
and DifferentialCalculator classes.
"""

import sympy as sp
from typing import Dict, Optional, Union, Any
import sys
import os
from datetime import datetime

# Add the project root to the path to import local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Models.function import FunctionAnalyzer
from Models.differential import DifferentialCalculator
from Utils.math_utils import is_real_number, evaluate_expression


class MainFunctionProcessor:
    """
    Main processor for comprehensive mathematical function analysis.
    
    This class orchestrates the complete analysis of mathematical functions
    by coordinating FunctionAnalyzer and DifferentialCalculator classes.
    """
    
    def __init__(self, func_str: str, parameters: Optional[Dict[str, Union[int, float]]] = None):
        """
        Initialize the MainFunctionProcessor.
        
        Args:
            func_str: String representation of the mathematical function
            parameters: Optional dictionary of parameter names and values
        """
        self.func_str = func_str
        self.parameters = parameters or {}
        self.function_analyzer = None
        self.differential_calculator = None
        self.x = sp.Symbol('x', real=True)
        
    def _initialize_analyzers(self) -> bool:
        """
        Initialize the FunctionAnalyzer and DifferentialCalculator instances.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            # Initialize FunctionAnalyzer
            self.function_analyzer = FunctionAnalyzer(self.func_str, self.parameters)
            
            # Get the parsed function from FunctionAnalyzer
            sympy_function = self.function_analyzer.function
            
            # Initialize DifferentialCalculator
            self.differential_calculator = DifferentialCalculator(sympy_function, self.x)
            
            return True
            
        except Exception as e:
            print(f"Error initializing analyzers: {e}")
            return False
    
    def _safe_analysis_call(self, method_name: str, analyzer_method) -> Any:
        """
        Safely call an analysis method with error handling.
        
        Args:
            method_name: Name of the method for error reporting
            analyzer_method: The method to call
            
        Returns:
            Result of the method call or error information
        """
        try:
            return analyzer_method()
        except Exception as e:
            error_msg = f"Error in {method_name}: {str(e)}"
            print(error_msg)
            return {"error": error_msg}
    
    def _format_derivative_result(self, derivative: Optional[sp.Expr]) -> Union[str, Dict[str, str]]:
        """
        Format derivative result for output.
        
        Args:
            derivative: SymPy expression representing the derivative
            
        Returns:
            Formatted derivative string or error information
        """
        if derivative is None:
            return {"error": "Could not calculate derivative"}
        
        try:
            return str(derivative)
        except Exception as e:
            return {"error": f"Error formatting derivative: {str(e)}"}
    
    def _get_derivative_analysis(self) -> Dict[str, Any]:
        """
        Perform derivative analysis using DifferentialCalculator.
        
        Returns:
            Dictionary containing derivative analysis results
        """
        derivatives = {}
        
        # Get first derivative
        first_deriv = self._safe_analysis_call(
            "first_derivative",
            self.differential_calculator.get_first_derivative
        )
        derivatives['first_derivative'] = self._format_derivative_result(first_deriv)
        
        # Get second derivative
        second_deriv = self._safe_analysis_call(
            "second_derivative", 
            self.differential_calculator.get_second_derivative
        )
        derivatives['second_derivative'] = self._format_derivative_result(second_deriv)
        
        # Get comprehensive derivative info
        try:
            derivatives['derivative_info'] = self.differential_calculator.get_derivative_info()
        except Exception as e:
            derivatives['derivative_info'] = {"error": f"Error getting derivative info: {str(e)}"}
        
        return derivatives
    
    def _get_function_analysis(self) -> Dict[str, Any]:
        """
        Perform function analysis using FunctionAnalyzer.
        
        Returns:
            Dictionary containing function analysis results
        """
        analysis = {}
        
        # Basic function information
        analysis['function_string'] = self.func_str
        analysis['parameters'] = self.parameters
        analysis['parsed_function'] = str(self.function_analyzer.function)
        
        # Domain analysis
        analysis['domain'] = self._safe_analysis_call(
            "domain_analysis",
            self.function_analyzer.get_domain
        )
        if not isinstance(analysis['domain'], dict) or 'error' not in analysis['domain']:
            analysis['domain'] = str(analysis['domain'])
        
        # Intercepts
        analysis['intercepts'] = self._safe_analysis_call(
            "intercepts_analysis",
            self.function_analyzer.get_intercepts
        )
        
        # Symmetry
        analysis['symmetry'] = self._safe_analysis_call(
            "symmetry_analysis",
            self.function_analyzer.get_symmetry
        )
        
        # Asymptotes
        analysis['asymptotes'] = self._safe_analysis_call(
            "asymptotes_analysis",
            self.function_analyzer.get_asymptotes
        )
        
        # Critical points
        analysis['critical_points'] = self._safe_analysis_call(
            "critical_points_analysis",
            self.function_analyzer.get_critical_points
        )
        
        # Inflection points
        analysis['inflection_points'] = self._safe_analysis_call(
            "inflection_points_analysis",
            self.function_analyzer.get_inflection_points
        )
        
        # Monotonicity
        analysis['monotonicity'] = self._safe_analysis_call(
            "monotonicity_analysis",
            self.function_analyzer.get_monotonicity
        )
        
        # Concavity
        analysis['concavity'] = self._safe_analysis_call(
            "concavity_analysis",
            self.function_analyzer.get_concavity
        )
        
        return analysis
    
    def _evaluate_function_at_points(self, points: list) -> Dict[str, float]:
        """
        Evaluate the function at specific points.
        
        Args:
            points: List of x-values to evaluate
            
        Returns:
            Dictionary mapping x-values to function values
        """
        evaluations = {}
        
        for point in points:
            if is_real_number(point):
                try:
                    value = evaluate_expression(self.func_str, point, self.parameters)
                    evaluations[str(point)] = value
                except Exception as e:
                    evaluations[str(point)] = f"Error: {str(e)}"
        
        return evaluations
    
    def _add_additional_analysis(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add additional analysis information.
        
        Args:
            analysis: Current analysis dictionary
            
        Returns:
            Enhanced analysis dictionary
        """
        # Evaluate function at critical points
        if 'critical_points' in analysis and isinstance(analysis['critical_points'], list):
            analysis['critical_points_values'] = self._evaluate_function_at_points(
                analysis['critical_points']
            )
        
        # Evaluate function at inflection points
        if 'inflection_points' in analysis and isinstance(analysis['inflection_points'], list):
            analysis['inflection_points_values'] = self._evaluate_function_at_points(
                analysis['inflection_points']
            )
        
        # Add some sample function values
        sample_points = [-2, -1, 0, 1, 2]
        analysis['sample_evaluations'] = self._evaluate_function_at_points(sample_points)
        
        return analysis
    
    def analyze_function(self) -> Dict[str, Any]:
        """
        Perform comprehensive function analysis.
        
        This method coordinates all analysis components and returns a structured
        dictionary containing complete function analysis results.
        
        Returns:
            Dictionary containing comprehensive analysis results or error information
        """
        try:
            # Initialize analyzers
            if not self._initialize_analyzers():
                return {
                    "error": "Failed to initialize analyzers",
                    "function_string": self.func_str,
                    "parameters": self.parameters
                }
            
            # Perform function analysis
            function_analysis = self._get_function_analysis()
            
            # Perform derivative analysis
            derivative_analysis = self._get_derivative_analysis()
            
            # Combine results
            complete_analysis = {
                **function_analysis,
                **derivative_analysis
            }
            
            # Add additional analysis
            complete_analysis = self._add_additional_analysis(complete_analysis)
            
            # Add metadata
            complete_analysis['analysis_status'] = 'completed'
            complete_analysis['analysis_timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            return complete_analysis
            
        except Exception as e:
            return {
                "error": f"Critical error during analysis: {str(e)}",
                "function_string": self.func_str,
                "parameters": self.parameters,
                "analysis_status": "failed"
            }
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summarized version of the function analysis.
        
        Returns:
            Dictionary containing key analysis highlights
        """
        try:
            full_analysis = self.analyze_function()
            
            if 'error' in full_analysis:
                return full_analysis
            
            # Extract key information
            summary = {
                'function': full_analysis.get('parsed_function', 'Unknown'),
                'domain': full_analysis.get('domain', 'Unknown'),
                'symmetry': full_analysis.get('symmetry', 'Unknown'),
                'critical_points_count': len(full_analysis.get('critical_points', [])),
                'inflection_points_count': len(full_analysis.get('inflection_points', [])),
                'has_vertical_asymptotes': len(full_analysis.get('asymptotes', {}).get('vertical', [])) > 0,
                'has_horizontal_asymptotes': len(full_analysis.get('asymptotes', {}).get('horizontal', [])) > 0,
                'y_intercept': full_analysis.get('intercepts', {}).get('y_intercept'),
                'first_derivative': full_analysis.get('first_derivative', 'Unknown'),
                'second_derivative': full_analysis.get('second_derivative', 'Unknown')
            }
            
            return summary
            
        except Exception as e:
            return {"error": f"Error generating summary: {str(e)}"}


# Utility function for quick analysis
def quick_analyze(func_str: str, parameters: Optional[Dict[str, Union[int, float]]] = None) -> Dict[str, Any]:
    """
    Utility function for quick function analysis.
    
    Args:
        func_str: String representation of the mathematical function
        parameters: Optional dictionary of parameter names and values
        
    Returns:
        Dictionary containing complete analysis results
    """
    processor = MainFunctionProcessor(func_str, parameters)
    return processor.analyze_function()


def quick_summary(func_str: str, parameters: Optional[Dict[str, Union[int, float]]] = None) -> Dict[str, Any]:
    """
    Utility function for quick function analysis summary.
    
    Args:
        func_str: String representation of the mathematical function
        parameters: Optional dictionary of parameter names and values
        
    Returns:
        Dictionary containing analysis summary
    """
    processor = MainFunctionProcessor(func_str, parameters)
    return processor.get_summary()
