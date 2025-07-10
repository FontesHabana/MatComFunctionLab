"""
Test script for LaTeX rendering functionality.

This script tests if LaTeX rendering works properly with matplotlib.
"""

import matplotlib.pyplot as plt
import sympy as sp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from PIL import Image, ImageTk
import io

def test_latex_rendering():
    """Test basic LaTeX rendering functionality."""
    
    # Test basic LaTeX rendering
    try:
        # Create a simple function
        x = sp.Symbol('x')
        func = x**2 + 2*x + 1
        latex_str = sp.latex(func)
        print(f"LaTeX string: {latex_str}")
        
        # Test matplotlib LaTeX rendering
        fig, ax = plt.subplots(figsize=(6, 1), dpi=100)
        ax.text(0.1, 0.5, f'$f(x) = {latex_str}$', fontsize=14, 
               transform=ax.transAxes, verticalalignment='center')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        # Save and show
        plt.savefig('test_latex.png', bbox_inches='tight', dpi=150)
        plt.show()
        
        print("LaTeX rendering test successful!")
        return True
        
    except Exception as e:
        print(f"LaTeX rendering test failed: {e}")
        return False

def test_derivatives_latex():
    """Test LaTeX rendering for derivatives."""
    
    try:
        x = sp.Symbol('x')
        
        # Test various functions
        functions = [
            x**2 + 3*x + 2,
            sp.sin(x) + sp.cos(x),
            sp.exp(x) * x,
            (x**2 + 1) / (x - 1),
            sp.log(x) + sp.sqrt(x)
        ]
        
        for i, func in enumerate(functions):
            print(f"\nFunction {i+1}: {func}")
            
            # First derivative
            first_deriv = sp.diff(func, x)
            latex_first = sp.latex(first_deriv)
            print(f"First derivative LaTeX: f'(x) = {latex_first}")
            
            # Second derivative
            second_deriv = sp.diff(func, x, 2)
            latex_second = sp.latex(second_deriv)
            print(f"Second derivative LaTeX: f''(x) = {latex_second}")
        
        return True
        
    except Exception as e:
        print(f"Derivatives LaTeX test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing LaTeX rendering functionality...")
    
    # Test basic rendering
    if test_latex_rendering():
        print("✓ Basic LaTeX rendering works")
    else:
        print("✗ Basic LaTeX rendering failed")
    
    # Test derivatives
    if test_derivatives_latex():
        print("✓ Derivatives LaTeX rendering works")
    else:
        print("✗ Derivatives LaTeX rendering failed")
    
    print("\nTest completed!")
