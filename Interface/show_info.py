"""
Show information interface module for displaying function analysis results.

This module provides the ShowInfoFrame class that creates a comprehensive
display window for mathematical function analysis results using CustomTkinter.
"""

import customtkinter as ctk
from typing import Dict, Any, List, Union
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sympy as sp
import io
from PIL import Image, ImageTk
import numpy as np


class ShowInfoFrame(ctk.CTkToplevel):
    """
    A CustomTkinter window for displaying comprehensive function analysis results.
    
    This class creates a detailed, organized display of mathematical function
    analysis including derivatives, domain, intercepts, asymptotes, and behavior analysis.
    """
    
    def __init__(self, master, analysis_results: Dict[str, Any]):
        """
        Initialize the ShowInfoFrame window.
        
        Args:
            master: Parent widget
            analysis_results: Dictionary containing function analysis results
        """
        super().__init__(master)
        
        self.analysis_results = analysis_results
        self.title("Análisis Detallado de la Función")
        self.geometry("900x1000")
        self.resizable(True, True)
        
        # Configure grid weights for responsiveness
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create main scrollable frame
        self.main_frame = ctk.CTkScrollableFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Setup the interface
        self._setup_interface()
        
        # Focus on this window
        self.focus()
        self.lift()
    
    def _create_latex_image(self, latex_string: str, font_size: int = 14) -> ImageTk.PhotoImage:
        """
        Create an image from a LaTeX string using matplotlib.
        
        Args:
            latex_string: The LaTeX string to render
            font_size: Font size for the rendered text
            
        Returns:
            ImageTk.PhotoImage object for display in tkinter
        """
        try:
            # Set matplotlib to use dark theme colors
            plt.style.use('dark_background')
            
            # Create a figure with appropriate size
            fig, ax = plt.subplots(figsize=(10, 1.2), dpi=120)
            fig.patch.set_facecolor('#2b2b2b')  # Dark background
            ax.set_facecolor('#2b2b2b')
            
            # Render the LaTeX text
            ax.text(0.02, 0.5, f'${latex_string}$', 
                   fontsize=font_size, 
                   transform=ax.transAxes, 
                   verticalalignment='center',
                   horizontalalignment='left',
                   color='white',
                   family='serif')
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            
            # Save to bytes buffer with tight bounding box
            buf = io.BytesIO()
            fig.savefig(buf, format='png', bbox_inches='tight', 
                       facecolor='#2b2b2b', edgecolor='none', 
                       dpi=120, pad_inches=0.1)
            buf.seek(0)
            
            # Convert to PIL Image and then to PhotoImage
            pil_image = Image.open(buf)
            
            # Resize if too large
            max_width = 800
            if pil_image.width > max_width:
                ratio = max_width / pil_image.width
                new_height = int(pil_image.height * ratio)
                pil_image = pil_image.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(pil_image)
            
            plt.close(fig)
            buf.close()
            
            return photo
            
        except Exception as e:
            print(f"Error creating LaTeX image: {e}")
            return None
    
    def _sympy_to_latex(self, expr_str: str) -> str:
        """
        Convert a SymPy expression string to LaTeX format.
        
        Args:
            expr_str: String representation of a SymPy expression
            
        Returns:
            LaTeX formatted string
        """
        try:
            if isinstance(expr_str, dict) and 'error' in expr_str:
                return r"\text{Error: " + str(expr_str['error']).replace('_', r'\_') + "}"
            
            if expr_str == 'No disponible' or expr_str is None:
                return r"\text{No disponible}"
            
            # Convert string to proper format for SymPy
            expr_str_clean = str(expr_str)
            
            # Handle common mathematical functions
            replacements = {
                'sqrt': 'sqrt',
                'log': 'log',
                'ln': 'log',
                'sin': 'sin',
                'cos': 'cos',
                'tan': 'tan',
                'exp': 'exp',
                'pi': 'pi',
                'e': 'E'
            }
            
            # Parse with SymPy and convert to LaTeX
            expr = sp.sympify(expr_str_clean)
            latex_str = sp.latex(expr)
            
            # Clean up LaTeX formatting
            latex_str = latex_str.replace('\\log', '\\ln')  # Use ln instead of log for natural log
            
            return latex_str
            
        except Exception as e:
            print(f"Error converting to LaTeX: {e}")
            # Return a safe LaTeX string
            safe_str = str(expr_str).replace('_', r'\_').replace('^', r'\hat{}').replace('*', r' \cdot ')
            return r"\text{" + safe_str + "}"
    
    def _add_latex_display(self, parent_frame, latex_string: str, row: int, 
                          label_text: str = "", font_size: int = 14) -> int:
        """
        Add a LaTeX rendered mathematical expression to the frame.
        
        Args:
            parent_frame: Parent frame to add the display to
            latex_string: LaTeX string to render
            row: Current row number
            label_text: Optional label text
            font_size: Font size for rendering
            
        Returns:
            Next row number
        """
        try:
            if label_text:
                label = ctk.CTkLabel(
                    parent_frame,
                    text=label_text,
                    font=ctk.CTkFont(size=14, weight="bold"),
                    justify="left"
                )
                label.grid(row=row, column=0, sticky="w", padx=40, pady=(5, 2))
                row += 1
            
            # Create LaTeX image
            latex_image = self._create_latex_image(latex_string, font_size)
            
            if latex_image:
                # Create a frame to hold the LaTeX image with dark background
                latex_frame = ctk.CTkFrame(parent_frame, fg_color="#2b2b2b", corner_radius=5)
                latex_frame.grid(row=row, column=0, sticky="ew", padx=60, pady=5)
                latex_frame.grid_columnconfigure(0, weight=1)
                
                # Create label to display the image with matching background
                image_label = tk.Label(latex_frame, image=latex_image, 
                                     bg="#2b2b2b", bd=0, highlightthickness=0)
                image_label.image = latex_image  # Keep a reference
                image_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
                
            else:
                # Fallback to regular text if LaTeX rendering fails
                fallback_label = ctk.CTkLabel(
                    parent_frame,
                    text=latex_string,
                    font=ctk.CTkFont(size=12, family="Courier"),
                    wraplength=600,
                    justify="left"
                )
                fallback_label.grid(row=row, column=0, sticky="w", padx=60, pady=2)
            
            return row + 1
            
        except Exception as e:
            print(f"Error adding LaTeX display: {e}")
            # Fallback to regular text
            fallback_label = ctk.CTkLabel(
                parent_frame,
                text=f"{label_text}: {latex_string}",
                font=ctk.CTkFont(size=12),
                wraplength=600,
                justify="left"
            )
            fallback_label.grid(row=row, column=0, sticky="w", padx=40, pady=2)
            return row + 1
    
    def _setup_interface(self):
        """Setup the complete interface with all analysis sections."""
        current_row = 0
        
        # Title
        current_row = self._add_title(current_row)
        
        # Function Information
        current_row = self._add_function_info(current_row)
        
        # Derivatives Section
        current_row = self._add_derivatives_section(current_row)
        
        # Domain Section
        current_row = self._add_domain_section(current_row)
        
        # Intercepts Section
        current_row = self._add_intercepts_section(current_row)
        
        # Symmetry Section
        current_row = self._add_symmetry_section(current_row)
        
        # Asymptotes Section
        current_row = self._add_asymptotes_section(current_row)
        
        # Critical Points Section
        current_row = self._add_critical_points_section(current_row)
        
        # Inflection Points Section
        current_row = self._add_inflection_points_section(current_row)
        
        # Monotonicity Section
        current_row = self._add_monotonicity_section(current_row)
        
        # Concavity Section
        current_row = self._add_concavity_section(current_row)
        
        # Close button
        self._add_close_button(current_row)
    
    def _add_title(self, row: int) -> int:
        """Add the main title."""
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="ANÁLISIS COMPLETO DE LA FUNCIÓN",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("gray10", "gray90")
        )
        title_label.grid(row=row, column=0, sticky="ew", padx=20, pady=(10, 20))
        return row + 1
    
    def _add_function_info(self, row: int) -> int:
        """Add function information section."""
        # Section title
        section_title = ctk.CTkLabel(
            self.main_frame,
            text="INFORMACIÓN DE LA FUNCIÓN",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("blue", "lightblue")
        )
        section_title.grid(row=row, column=0, sticky="w", padx=20, pady=(10, 5))
        row += 1
        
        # Function string (original input)
        func_str = self.analysis_results.get('function_string', 'No disponible')
        func_label = ctk.CTkLabel(
            self.main_frame,
            text=f"Función ingresada: {func_str}",
            font=ctk.CTkFont(size=14),
            wraplength=700,
            justify="left"
        )
        func_label.grid(row=row, column=0, sticky="w", padx=40, pady=2)
        row += 1
        
        # Parsed function in LaTeX
        parsed_func = self.analysis_results.get('parsed_function', 'No disponible')
        if parsed_func and parsed_func != 'No disponible':
            try:
                latex_func = self._sympy_to_latex(parsed_func)
                row = self._add_latex_display(
                    self.main_frame, 
                    f"f(x) = {latex_func}", 
                    row, 
                    "Función matemática:",
                    font_size=16
                )
            except Exception as e:
                print(f"Error rendering function LaTeX: {e}")
                parsed_label = ctk.CTkLabel(
                    self.main_frame,
                    text=f"Función procesada: {parsed_func}",
                    font=ctk.CTkFont(size=14),
                    wraplength=700,
                    justify="left"
                )
                parsed_label.grid(row=row, column=0, sticky="w", padx=40, pady=2)
                row += 1
        else:
            parsed_label = ctk.CTkLabel(
                self.main_frame,
                text=f"Función procesada: {parsed_func}",
                font=ctk.CTkFont(size=14),
                wraplength=700,
                justify="left"
            )
            parsed_label.grid(row=row, column=0, sticky="w", padx=40, pady=2)
            row += 1
        
        # Parameters
        parameters = self.analysis_results.get('parameters', {})
        if parameters:
            params_text = ", ".join([f"{k}={v}" for k, v in parameters.items()])
            params_label = ctk.CTkLabel(
                self.main_frame,
                text=f"Parámetros: {params_text}",
                font=ctk.CTkFont(size=14),
                wraplength=700,
                justify="left"
            )
            params_label.grid(row=row, column=0, sticky="w", padx=40, pady=2)
            row += 1
        
        return row + 1
    
    def _add_derivatives_section(self, row: int) -> int:
        """Add derivatives section."""
        section_title = ctk.CTkLabel(
            self.main_frame,
            text="DERIVADAS",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("blue", "lightblue")
        )
        section_title.grid(row=row, column=0, sticky="w", padx=20, pady=(10, 5))
        row += 1
        
        # First derivative
        first_deriv = self.analysis_results.get('first_derivative', 'No disponible')
        first_deriv_formatted = self._format_result(first_deriv)
        
        if first_deriv_formatted and first_deriv_formatted != 'No disponible':
            try:
                latex_first = self._sympy_to_latex(first_deriv_formatted)
                row = self._add_latex_display(
                    self.main_frame,
                    f"f'(x) = {latex_first}",
                    row,
                    "Primera derivada:",
                    font_size=14
                )
            except Exception as e:
                print(f"Error rendering first derivative LaTeX: {e}")
                first_label = ctk.CTkLabel(
                    self.main_frame,
                    text=f"Primera derivada: f'(x) = {first_deriv_formatted}",
                    font=ctk.CTkFont(size=14),
                    wraplength=700,
                    justify="left"
                )
                first_label.grid(row=row, column=0, sticky="w", padx=40, pady=2)
                row += 1
        else:
            first_label = ctk.CTkLabel(
                self.main_frame,
                text=f"Primera derivada: f'(x) = {first_deriv_formatted}",
                font=ctk.CTkFont(size=14),
                wraplength=700,
                justify="left"
            )
            first_label.grid(row=row, column=0, sticky="w", padx=40, pady=2)
            row += 1
        
        # Second derivative
        second_deriv = self.analysis_results.get('second_derivative', 'No disponible')
        second_deriv_formatted = self._format_result(second_deriv)
        
        if second_deriv_formatted and second_deriv_formatted != 'No disponible':
            try:
                latex_second = self._sympy_to_latex(second_deriv_formatted)
                row = self._add_latex_display(
                    self.main_frame,
                    f"f''(x) = {latex_second}",
                    row,
                    "Segunda derivada:",
                    font_size=14
                )
            except Exception as e:
                print(f"Error rendering second derivative LaTeX: {e}")
                second_label = ctk.CTkLabel(
                    self.main_frame,
                    text=f"Segunda derivada: f''(x) = {second_deriv_formatted}",
                    font=ctk.CTkFont(size=14),
                    wraplength=700,
                    justify="left"
                )
                second_label.grid(row=row, column=0, sticky="w", padx=40, pady=2)
                row += 1
        else:
            second_label = ctk.CTkLabel(
                self.main_frame,
                text=f"Segunda derivada: f''(x) = {second_deriv_formatted}",
                font=ctk.CTkFont(size=14),
                wraplength=700,
                justify="left"
            )
            second_label.grid(row=row, column=0, sticky="w", padx=40, pady=2)
            row += 1
        
        return row + 1
    
    def _add_domain_section(self, row: int) -> int:
        """Add domain section."""
        section_title = ctk.CTkLabel(
            self.main_frame,
            text="DOMINIO",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("blue", "lightblue")
        )
        section_title.grid(row=row, column=0, sticky="w", padx=20, pady=(10, 5))
        row += 1
        
        domain = self.analysis_results.get('domain', 'No disponible')
        domain = self._format_result(domain)
        domain_label = ctk.CTkLabel(
            self.main_frame,
            text=f"Dominio: {domain}",
            font=ctk.CTkFont(size=14),
            wraplength=700,
            justify="left"
        )
        domain_label.grid(row=row, column=0, sticky="w", padx=40, pady=2)
        row += 1
        
        return row + 1
    
    def _add_intercepts_section(self, row: int) -> int:
        """Add intercepts section."""
        section_title = ctk.CTkLabel(
            self.main_frame,
            text="INTERCEPTOS",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("blue", "lightblue")
        )
        section_title.grid(row=row, column=0, sticky="w", padx=20, pady=(10, 5))
        row += 1
        
        intercepts = self.analysis_results.get('intercepts', {})
        
        # Y-intercept
        y_intercept = intercepts.get('y_intercept')
        if y_intercept is not None:
            y_text = f"Intercepto Y: (0, {y_intercept})"
        else:
            y_text = "Intercepto Y: No existe"
        
        y_label = ctk.CTkLabel(
            self.main_frame,
            text=y_text,
            font=ctk.CTkFont(size=14),
            wraplength=700,
            justify="left"
        )
        y_label.grid(row=row, column=0, sticky="w", padx=40, pady=2)
        row += 1
        
        # X-intercepts
        x_intercepts = intercepts.get('x_intercepts', [])
        if x_intercepts:
            x_points = ", ".join([f"({x}, 0)" for x in x_intercepts])
            x_text = f"Interceptos X: {x_points}"
        else:
            x_text = "Interceptos X: No existen"
        
        x_label = ctk.CTkLabel(
            self.main_frame,
            text=x_text,
            font=ctk.CTkFont(size=14),
            wraplength=700,
            justify="left"
        )
        x_label.grid(row=row, column=0, sticky="w", padx=40, pady=2)
        row += 1
        
        return row + 1
    
    def _add_symmetry_section(self, row: int) -> int:
        """Add symmetry section."""
        section_title = ctk.CTkLabel(
            self.main_frame,
            text="SIMETRÍA",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("blue", "lightblue")
        )
        section_title.grid(row=row, column=0, sticky="w", padx=20, pady=(10, 5))
        row += 1
        
        symmetry = self.analysis_results.get('symmetry', 'No determinada')
        symmetry_map = {
            'even': 'Par (simétrica respecto al eje Y)',
            'odd': 'Impar (simétrica respecto al origen)',
            'neither': 'Ni par ni impar'
        }
        symmetry_text = symmetry_map.get(symmetry, symmetry)
        
        symmetry_label = ctk.CTkLabel(
            self.main_frame,
            text=f"Tipo de simetría: {symmetry_text}",
            font=ctk.CTkFont(size=14),
            wraplength=700,
            justify="left"
        )
        symmetry_label.grid(row=row, column=0, sticky="w", padx=40, pady=2)
        row += 1
        
        return row + 1
    
    def _add_asymptotes_section(self, row: int) -> int:
        """Add asymptotes section."""
        section_title = ctk.CTkLabel(
            self.main_frame,
            text="ASÍNTOTAS",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("blue", "lightblue")
        )
        section_title.grid(row=row, column=0, sticky="w", padx=20, pady=(10, 5))
        row += 1
        
        asymptotes = self.analysis_results.get('asymptotes', {})
        
        # Vertical asymptotes
        vertical = asymptotes.get('vertical', [])
        if vertical:
            v_text = f"Asíntotas verticales: x = {', x = '.join(map(str, vertical))}"
        else:
            v_text = "Asíntotas verticales: No existen"
        
        v_label = ctk.CTkLabel(
            self.main_frame,
            text=v_text,
            font=ctk.CTkFont(size=14),
            wraplength=700,
            justify="left"
        )
        v_label.grid(row=row, column=0, sticky="w", padx=40, pady=2)
        row += 1
        
        # Horizontal asymptotes
        horizontal = asymptotes.get('horizontal', [])
        if horizontal:
            h_text = f"Asíntotas horizontales: y = {', y = '.join(map(str, horizontal))}"
        else:
            h_text = "Asíntotas horizontales: No existen"
        
        h_label = ctk.CTkLabel(
            self.main_frame,
            text=h_text,
            font=ctk.CTkFont(size=14),
            wraplength=700,
            justify="left"
        )
        h_label.grid(row=row, column=0, sticky="w", padx=40, pady=2)
        row += 1
        
        # Oblique asymptotes
        oblique = asymptotes.get('oblique', [])
        if oblique:
            o_text = f"Asíntotas oblicuas: {', '.join(oblique)}"
        else:
            o_text = "Asíntotas oblicuas: No existen"
        
        o_label = ctk.CTkLabel(
            self.main_frame,
            text=o_text,
            font=ctk.CTkFont(size=14),
            wraplength=700,
            justify="left"
        )
        o_label.grid(row=row, column=0, sticky="w", padx=40, pady=2)
        row += 1
        
        return row + 1
    
    def _add_critical_points_section(self, row: int) -> int:
        """Add critical points section."""
        section_title = ctk.CTkLabel(
            self.main_frame,
            text="PUNTOS CRÍTICOS",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("blue", "lightblue")
        )
        section_title.grid(row=row, column=0, sticky="w", padx=20, pady=(10, 5))
        row += 1
        
        critical_points = self.analysis_results.get('critical_points', [])
        if critical_points:
            points_text = ", ".join([f"x = {point}" for point in critical_points])
            cp_text = f"Puntos críticos: {points_text}"
            
            # Add function values if available
            critical_values = self.analysis_results.get('critical_points_values', {})
            if critical_values:
                values_text = []
                for point in critical_points:
                    value = critical_values.get(str(point))
                    if value is not None:
                        values_text.append(f"f({point}) = {value}")
                if values_text:
                    cp_text += f"\nValores: {', '.join(values_text)}"
        else:
            cp_text = "Puntos críticos: No existen"
        
        cp_label = ctk.CTkLabel(
            self.main_frame,
            text=cp_text,
            font=ctk.CTkFont(size=14),
            wraplength=700,
            justify="left"
        )
        cp_label.grid(row=row, column=0, sticky="w", padx=40, pady=2)
        row += 1
        
        return row + 1
    
    def _add_inflection_points_section(self, row: int) -> int:
        """Add inflection points section."""
        section_title = ctk.CTkLabel(
            self.main_frame,
            text="PUNTOS DE INFLEXIÓN",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("blue", "lightblue")
        )
        section_title.grid(row=row, column=0, sticky="w", padx=20, pady=(10, 5))
        row += 1
        
        inflection_points = self.analysis_results.get('inflection_points', [])
        if inflection_points:
            points_text = ", ".join([f"x = {point}" for point in inflection_points])
            ip_text = f"Puntos de inflexión: {points_text}"
            
            # Add function values if available
            inflection_values = self.analysis_results.get('inflection_points_values', {})
            if inflection_values:
                values_text = []
                for point in inflection_points:
                    value = inflection_values.get(str(point))
                    if value is not None:
                        values_text.append(f"f({point}) = {value}")
                if values_text:
                    ip_text += f"\nValores: {', '.join(values_text)}"
        else:
            ip_text = "Puntos de inflexión: No existen"
        
        ip_label = ctk.CTkLabel(
            self.main_frame,
            text=ip_text,
            font=ctk.CTkFont(size=14),
            wraplength=700,
            justify="left"
        )
        ip_label.grid(row=row, column=0, sticky="w", padx=40, pady=2)
        row += 1
        
        return row + 1
    
    def _add_monotonicity_section(self, row: int) -> int:
        """Add monotonicity section."""
        section_title = ctk.CTkLabel(
            self.main_frame,
            text="MONOTONÍA",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("blue", "lightblue")
        )
        section_title.grid(row=row, column=0, sticky="w", padx=20, pady=(10, 5))
        row += 1
        
        monotonicity = self.analysis_results.get('monotonicity', {})
        
        # Increasing intervals
        increasing = monotonicity.get('increasing', [])
        if increasing:
            inc_intervals = self._format_intervals(increasing)
            inc_text = f"Intervalos crecientes: {inc_intervals}"
        else:
            inc_text = "Intervalos crecientes: No existen"
        
        inc_label = ctk.CTkLabel(
            self.main_frame,
            text=inc_text,
            font=ctk.CTkFont(size=14),
            wraplength=700,
            justify="left"
        )
        inc_label.grid(row=row, column=0, sticky="w", padx=40, pady=2)
        row += 1
        
        # Decreasing intervals
        decreasing = monotonicity.get('decreasing', [])
        if decreasing:
            dec_intervals = self._format_intervals(decreasing)
            dec_text = f"Intervalos decrecientes: {dec_intervals}"
        else:
            dec_text = "Intervalos decrecientes: No existen"
        
        dec_label = ctk.CTkLabel(
            self.main_frame,
            text=dec_text,
            font=ctk.CTkFont(size=14),
            wraplength=700,
            justify="left"
        )
        dec_label.grid(row=row, column=0, sticky="w", padx=40, pady=2)
        row += 1
        
        return row + 1
    
    def _add_concavity_section(self, row: int) -> int:
        """Add concavity section."""
        section_title = ctk.CTkLabel(
            self.main_frame,
            text="CONCAVIDAD",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("blue", "lightblue")
        )
        section_title.grid(row=row, column=0, sticky="w", padx=20, pady=(10, 5))
        row += 1
        
        concavity = self.analysis_results.get('concavity', {})
        
        # Concave up intervals
        concave_up = concavity.get('concave_up', [])
        if concave_up:
            up_intervals = self._format_intervals(concave_up)
            up_text = f"Intervalos cóncavos hacia arriba: {up_intervals}"
        else:
            up_text = "Intervalos cóncavos hacia arriba: No existen"
        
        up_label = ctk.CTkLabel(
            self.main_frame,
            text=up_text,
            font=ctk.CTkFont(size=14),
            wraplength=700,
            justify="left"
        )
        up_label.grid(row=row, column=0, sticky="w", padx=40, pady=2)
        row += 1
        
        # Concave down intervals
        concave_down = concavity.get('concave_down', [])
        if concave_down:
            down_intervals = self._format_intervals(concave_down)
            down_text = f"Intervalos cóncavos hacia abajo: {down_intervals}"
        else:
            down_text = "Intervalos cóncavos hacia abajo: No existen"
        
        down_label = ctk.CTkLabel(
            self.main_frame,
            text=down_text,
            font=ctk.CTkFont(size=14),
            wraplength=700,
            justify="left"
        )
        down_label.grid(row=row, column=0, sticky="w", padx=40, pady=2)
        row += 1
        
        return row + 1
    
    def _add_close_button(self, row: int):
        """Add close button."""
        close_button = ctk.CTkButton(
            self.main_frame,
            text="Cerrar",
            command=self.destroy,
            width=200,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        close_button.grid(row=row, column=0, pady=20)
    
    def _format_result(self, result: Any) -> str:
        """Format analysis result for display."""
        if isinstance(result, dict) and 'error' in result:
            return f"Error: {result['error']}"
        elif result is None:
            return "No disponible"
        else:
            return str(result)
    
    def _format_intervals(self, intervals: List[tuple]) -> str:
        """Format interval list for display."""
        if not intervals:
            return "No existen"
        
        formatted_intervals = []
        for interval in intervals:
            if len(interval) == 2:
                start, end = interval
                # Handle infinity values
                start_str = "-∞" if start == float('-inf') else str(start)
                end_str = "+∞" if end == float('inf') else str(end)
                formatted_intervals.append(f"({start_str}, {end_str})")
        
        return ", ".join(formatted_intervals) if formatted_intervals else "No existen"


# Utility function for quick display
def show_analysis_results(master, analysis_results: Dict[str, Any]) -> ShowInfoFrame:
    """
    Utility function to quickly display analysis results.
    
    Args:
        master: Parent widget
        analysis_results: Dictionary containing function analysis results
        
    Returns:
        ShowInfoFrame instance
    """
    return ShowInfoFrame(master, analysis_results)
