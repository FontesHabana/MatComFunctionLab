"""
Main application interface for MatcomFunctionLab.

This module provides the main App class that creates a comprehensive
CustomTkinter interface for mathematical function analysis and visualization.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import sympy as sp
import re
from typing import Dict, List, Optional, Any
import sys
import os

# Add the project root to the path to import local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Models.main_function import MainFunctionProcessor
from Interface.show_info import ShowInfoFrame
from Utils.math_utils import evaluate_expression, is_real_number


class App(ctk.CTk):
    """
    Main application class for MatcomFunctionLab.
    
    This class provides a comprehensive interface for mathematical function
    analysis including input, parameter adjustment, visualization, and detailed analysis.
    """
    
    def __init__(self):
        """Initialize the main application."""
        super().__init__()
        
        # Configure main window
        self.title("MatcomFunctionLab - Analizador de Funciones")
        self.geometry("1400x900")
        self.resizable(True, True)
        
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Configure grid weights
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Initialize variables
        self.current_function = ""
        self.current_parameters = {}
        self.parameter_controls = {}
        self.analysis_results = None
        self.processor = None
        
        # Create the interface
        self._create_interface()
        
        # Initialize matplotlib
        plt.style.use('dark_background')
    
    def _create_interface(self):
        """Create the main interface layout."""
        # Left panel for controls
        self._create_left_panel()
        
        # Right panel for matplotlib
        self._create_right_panel()
    
    def _create_left_panel(self):
        """Create the left control panel."""
        # Left frame
        self.left_frame = ctk.CTkFrame(self, corner_radius=0)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        self.left_frame.grid_rowconfigure(4, weight=1)  # Parameter frame expandable
        
        # Title
        title_label = ctk.CTkLabel(
            self.left_frame,
            text="MatcomFunctionLab",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        # Function input section
        func_label = ctk.CTkLabel(
            self.left_frame,
            text="Función matemática:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        func_label.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="w")
        
        self.function_entry = ctk.CTkEntry(
            self.left_frame,
            width=300,
            height=40,
            placeholder_text="Ej: x**2 - 2*x + 1, sin(x), a*x**2 + b*x + c",
            font=ctk.CTkFont(size=14)
        )
        self.function_entry.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        self.function_entry.bind("<Return>", lambda event: self.init_function())
        
        # Init button
        self.init_button = ctk.CTkButton(
            self.left_frame,
            text="Inicializar Función",
            command=self.init_function,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.init_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        # Parameters frame (scrollable)
        self.params_frame = ctk.CTkScrollableFrame(
            self.left_frame,
            label_text="Parámetros de la Función",
            height=200
        )
        self.params_frame.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")
        
        # Analysis button
        self.analysis_button = ctk.CTkButton(
            self.left_frame,
            text="Mostrar Análisis Detallado",
            command=self.show_analysis,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold"),
            state="disabled"
        )
        self.analysis_button.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.left_frame,
            text="Ingrese una función para comenzar",
            font=ctk.CTkFont(size=12),
            text_color=("gray60", "gray40")
        )
        self.status_label.grid(row=6, column=0, padx=20, pady=(5, 20), sticky="ew")
        
        # Configure column weight
        self.left_frame.grid_columnconfigure(0, weight=1)
    
    def _create_right_panel(self):
        """Create the right panel with matplotlib canvas."""
        # Right frame
        self.right_frame = ctk.CTkFrame(self, corner_radius=0)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)
        
        # Create matplotlib figure and canvas
        self.fig = Figure(figsize=(10, 8), dpi=100, facecolor='#212121')
        self.ax = self.fig.add_subplot(111, facecolor='#2b2b2b')
        
        # Configure plot appearance
        self.ax.grid(True, alpha=0.3, color='white')
        self.ax.set_xlabel('x', color='white', fontsize=12)
        self.ax.set_ylabel('f(x)', color='white', fontsize=12)
        self.ax.tick_params(colors='white')
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, self.right_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        
        # Add navigation toolbar
        self.toolbar_frame = ctk.CTkFrame(self.right_frame)
        self.toolbar_frame.grid(row=1, column=0, sticky="ew", pady=(5, 0))
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbar_frame)
        self.toolbar.config(bg='#212121')
        self.toolbar.update()
    
    def _extract_parameters(self, func_str: str) -> List[str]:
        """Extract parameter names from function string."""
        try:
            # Parse with sympy to get symbols
            expr = sp.sympify(func_str)
            symbols = expr.free_symbols
            
            # Filter out 'x' and common functions
            parameters = []
            excluded = {'x', 'e', 'pi', 'I', 'E', 'sin', 'cos', 'tan', 'log', 'ln', 'exp', 'sqrt'}
            
            for symbol in symbols:
                symbol_str = str(symbol)
                if symbol_str not in excluded and symbol_str.isalpha():
                    parameters.append(symbol_str)
            
            return sorted(parameters)
        except Exception:
            return []
    
    def _create_parameter_controls(self, parameters: List[str]):
        """Create slider and entry controls for parameters."""
        # Clear existing controls
        for widget in self.params_frame.winfo_children():
            widget.destroy()
        
        self.parameter_controls = {}
        
        if not parameters:
            no_params_label = ctk.CTkLabel(
                self.params_frame,
                text="Esta función no tiene parámetros",
                font=ctk.CTkFont(size=12),
                text_color=("gray60", "gray40")
            )
            no_params_label.grid(row=0, column=0, padx=20, pady=20)
            return
        
        for i, param in enumerate(parameters):
            # Parameter label
            param_label = ctk.CTkLabel(
                self.params_frame,
                text=f"Parámetro {param}:",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            param_label.grid(row=i*3, column=0, padx=10, pady=(10, 5), sticky="w")
            
            # Value frame
            value_frame = ctk.CTkFrame(self.params_frame)
            value_frame.grid(row=i*3+1, column=0, padx=10, pady=5, sticky="ew")
            value_frame.grid_columnconfigure(1, weight=1)
            
            # Entry for exact value
            entry = ctk.CTkEntry(
                value_frame,
                width=80,
                height=30,
                font=ctk.CTkFont(size=12)
            )
            entry.grid(row=0, column=0, padx=(5, 10), pady=5)
            entry.insert(0, "1.0")
            
            # Slider for interactive adjustment
            slider = ctk.CTkSlider(
                value_frame,
                from_=-10,
                to=10,
                number_of_steps=200,
                height=20
            )
            slider.grid(row=0, column=1, padx=(0, 5), pady=5, sticky="ew")
            slider.set(1.0)
            
            # Value display label
            value_label = ctk.CTkLabel(
                value_frame,
                text="1.00",
                width=60,
                font=ctk.CTkFont(size=12)
            )
            value_label.grid(row=0, column=2, padx=5, pady=5)
            
            # Store controls
            self.parameter_controls[param] = {
                'entry': entry,
                'slider': slider,
                'label': value_label
            }
            
            # Bind events
            slider.configure(command=lambda value, p=param: self._on_slider_change(p, value))
            entry.bind("<Return>", lambda event, p=param: self._on_entry_change(p))
            entry.bind("<FocusOut>", lambda event, p=param: self._on_entry_change(p))
            
            # Initialize parameter value
            self.current_parameters[param] = 1.0
        
        # Configure grid weights
        self.params_frame.grid_columnconfigure(0, weight=1)
    
    def _on_slider_change(self, param: str, value: float):
        """Handle slider value change."""
        # Update entry and label
        controls = self.parameter_controls[param]
        controls['entry'].delete(0, tk.END)
        controls['entry'].insert(0, f"{value:.2f}")
        controls['label'].configure(text=f"{value:.2f}")
        
        # Update parameter value
        self.current_parameters[param] = value
        
        # Redraw plot
        self._update_plot()
    
    def _on_entry_change(self, param: str):
        """Handle entry value change."""
        controls = self.parameter_controls[param]
        try:
            value = float(controls['entry'].get())
            
            # Clamp value to slider range
            value = max(-10, min(10, value))
            
            # Update slider and label
            controls['slider'].set(value)
            controls['label'].configure(text=f"{value:.2f}")
            
            # Update parameter value
            self.current_parameters[param] = value
            
            # Redraw plot
            self._update_plot()
            
        except ValueError:
            # Reset to current value
            current_value = self.current_parameters.get(param, 1.0)
            controls['entry'].delete(0, tk.END)
            controls['entry'].insert(0, f"{current_value:.2f}")
    
    def init_function(self):
        """Initialize function analysis and plotting."""
        func_str = self.function_entry.get().strip()
        
        if not func_str:
            self._show_error("Por favor, ingrese una función")
            return
        
        try:
            # Update status
            self.status_label.configure(text="Analizando función...")
            self.update()
            
            # Store current function
            self.current_function = func_str
            
            # Extract parameters
            parameters = self._extract_parameters(func_str)
            
            # Create parameter controls
            self._create_parameter_controls(parameters)
            
            # Initialize processor
            self.processor = MainFunctionProcessor(func_str, self.current_parameters)
            
            # Perform analysis
            self.analysis_results = self.processor.analyze_function()
            
            # Check for analysis errors
            if 'error' in self.analysis_results:
                self._show_error(f"Error en el análisis: {self.analysis_results['error']}")
                return
            
            # Enable analysis button
            self.analysis_button.configure(state="normal")
            
            # Plot function
            self._plot_function()
            
            # Update status
            self.status_label.configure(text="Función analizada exitosamente")
            
        except Exception as e:
            self._show_error(f"Error al procesar la función: {str(e)}")
            self.status_label.configure(text="Error en el análisis")
    
    def _update_plot(self):
        """Update plot with current parameters."""
        if not self.current_function:
            return
        
        try:
            # Update processor with new parameters
            self.processor = MainFunctionProcessor(self.current_function, self.current_parameters)
            self.analysis_results = self.processor.analyze_function()
            
            # Plot function
            self._plot_function()
            
        except Exception as e:
            print(f"Error updating plot: {e}")
    
    def _plot_function(self):
        """Plot the function with analysis results."""
        if not self.analysis_results:
            return
        
        # Clear previous plot
        self.ax.clear()
        
        # Configure plot appearance
        self.ax.grid(True, alpha=0.3, color='white')
        self.ax.set_xlabel('x', color='white', fontsize=12)
        self.ax.set_ylabel('f(x)', color='white', fontsize=12)
        self.ax.tick_params(colors='white')
        self.ax.set_facecolor('#2b2b2b')
        
        # Determine plot range
        x_range = self._get_plot_range()
        x_vals = np.linspace(x_range[0], x_range[1], 1000)
        
        # Calculate function values
        y_vals = []
        for x in x_vals:
            value = evaluate_expression(self.current_function, x, self.current_parameters)
            y_vals.append(value if value is not None else np.nan)
        
        y_vals = np.array(y_vals)
        
        # Plot main function
        valid_mask = ~np.isnan(y_vals) & np.isfinite(y_vals)
        if np.any(valid_mask):
            self.ax.plot(x_vals[valid_mask], y_vals[valid_mask], 'cyan', linewidth=2, label='f(x)')
        
        # Plot analysis markers
        self._plot_analysis_markers()
        
        # Plot asymptotes
        self._plot_asymptotes(x_range)
        
        # Set reasonable y-limits
        self._set_plot_limits(y_vals)
        
        # Add legend
        self.ax.legend(loc='upper right', facecolor='#2b2b2b', edgecolor='white', labelcolor='white')
        
        # Set title
        title = f"f(x) = {self.current_function}"
        if self.current_parameters:
            params_str = ", ".join([f"{k}={v:.2f}" for k, v in self.current_parameters.items()])
            title += f" | {params_str}"
        self.ax.set_title(title, color='white', fontsize=14, pad=20)
        
        # Refresh canvas
        self.canvas.draw()
    
    def _get_plot_range(self) -> tuple:
        """Determine appropriate plot range."""
        # Default range
        x_min, x_max = -10, 10
        
        # Adjust based on critical points and intercepts
        if self.analysis_results:
            points = []
            
            # Add critical points
            critical_points = self.analysis_results.get('critical_points', [])
            points.extend(critical_points)
            
            # Add x-intercepts
            intercepts = self.analysis_results.get('intercepts', {})
            x_intercepts = intercepts.get('x_intercepts', [])
            points.extend(x_intercepts)
            
            # Add inflection points
            inflection_points = self.analysis_results.get('inflection_points', [])
            points.extend(inflection_points)
            
            if points:
                points_array = np.array([p for p in points if is_real_number(p)])
                if len(points_array) > 0:
                    range_padding = max(2, (np.max(points_array) - np.min(points_array)) * 0.2)
                    x_min = min(x_min, np.min(points_array) - range_padding)
                    x_max = max(x_max, np.max(points_array) + range_padding)
        
        return (x_min, x_max)
    
    def _plot_analysis_markers(self):
        """Plot markers for critical points, intercepts, etc."""
        if not self.analysis_results:
            return
        
        # Critical points (need to classify as max/min)
        critical_points = self.analysis_results.get('critical_points', [])
        critical_values = self.analysis_results.get('critical_points_values', {})
        
        for cp in critical_points:
            if str(cp) in critical_values:
                y_val = critical_values[str(cp)]
                if y_val is not None:
                    # Simple classification: use second derivative test
                    # For now, use triangles (can be enhanced)
                    self.ax.plot(cp, y_val, '^', color='red', markersize=10, 
                                label='Puntos críticos' if cp == critical_points[0] else "")
        
        # Inflection points
        inflection_points = self.analysis_results.get('inflection_points', [])
        inflection_values = self.analysis_results.get('inflection_points_values', {})
        
        for ip in inflection_points:
            if str(ip) in inflection_values:
                y_val = inflection_values[str(ip)]
                if y_val is not None:
                    self.ax.plot(ip, y_val, 'o', color='orange', markersize=8,
                                label='Puntos de inflexión' if ip == inflection_points[0] else "")
        
        # X-intercepts
        intercepts = self.analysis_results.get('intercepts', {})
        x_intercepts = intercepts.get('x_intercepts', [])
        
        for xi in x_intercepts:
            self.ax.plot(xi, 0, 's', color='blue', markersize=8,
                        label='Interceptos X' if xi == x_intercepts[0] else "")
        
        # Y-intercept
        y_intercept = intercepts.get('y_intercept')
        if y_intercept is not None:
            self.ax.plot(0, y_intercept, 'D', color='purple', markersize=8, label='Intercepto Y')
    
    def _plot_asymptotes(self, x_range: tuple):
        """Plot asymptotes."""
        if not self.analysis_results:
            return
        
        asymptotes = self.analysis_results.get('asymptotes', {})
        
        # Vertical asymptotes
        vertical = asymptotes.get('vertical', [])
        for va in vertical:
            self.ax.axvline(x=va, color='red', linestyle='--', alpha=0.7, linewidth=1,
                          label='Asíntotas verticales' if va == vertical[0] else "")
        
        # Horizontal asymptotes
        horizontal = asymptotes.get('horizontal', [])
        for ha in horizontal:
            self.ax.axhline(y=ha, color='green', linestyle='--', alpha=0.7, linewidth=1,
                          label='Asíntotas horizontales' if ha == horizontal[0] else "")
        
        # Oblique asymptotes (simplified)
        oblique = asymptotes.get('oblique', [])
        for oa in oblique:
            if isinstance(oa, str) and '=' in oa:
                # Try to parse and plot oblique asymptote
                # This is a simplified implementation
                try:
                    # Extract slope and intercept from string like "y = 2*x + 1"
                    parts = oa.split('=')
                    if len(parts) == 2:
                        expr = parts[1].strip()
                        x_vals = np.linspace(x_range[0], x_range[1], 100)
                        y_vals = [evaluate_expression(expr, x, {}) for x in x_vals]
                        y_vals = [y for y in y_vals if y is not None]
                        if y_vals:
                            self.ax.plot(x_vals[:len(y_vals)], y_vals, '--', color='yellow', 
                                        alpha=0.7, linewidth=1,
                                        label='Asíntotas oblicuas' if oa == oblique[0] else "")
                except:
                    pass
    
    def _set_plot_limits(self, y_vals: np.ndarray):
        """Set appropriate plot limits."""
        # Y-limits based on function values
        valid_y = y_vals[np.isfinite(y_vals)]
        
        if len(valid_y) > 0:
            y_min, y_max = np.min(valid_y), np.max(valid_y)
            y_range = y_max - y_min
            
            if y_range > 0:
                padding = y_range * 0.1
                self.ax.set_ylim(y_min - padding, y_max + padding)
            else:
                # Constant function
                self.ax.set_ylim(y_min - 1, y_max + 1)
        else:
            # No valid points
            self.ax.set_ylim(-10, 10)
    
    def show_analysis(self):
        """Show detailed analysis window."""
        if not self.analysis_results:
            self._show_error("No hay análisis disponible. Primero inicialice una función.")
            return
        
        try:
            # Create and show analysis window
            analysis_window = ShowInfoFrame(self, self.analysis_results)
            # Bring the analysis window to the front
            analysis_window.lift()
            analysis_window.focus_force()
            analysis_window.grab_set()  # Make it modal
        except Exception as e:
            self._show_error(f"Error al mostrar el análisis: {str(e)}")
    
    def _show_error(self, message: str):
        """Show error message."""
        messagebox.showerror("Error", message)
        self.status_label.configure(text=f"Error: {message}")


def main():
    """Main function to run the application."""
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
