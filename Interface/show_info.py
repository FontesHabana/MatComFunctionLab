import customtkinter as ctk
import tkinter as tk
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy import symbols, sympify

class ResultWindow(ctk.CTkToplevel):
    def __init__(self, parent, function_str):
        super().__init__(parent.app)
        self.parent = parent
        self.function_str = function_str

        # Configuración de ventana
        self.title("Resultados del Análisis")
        self.geometry("1200x800")
        self.configure(bg="#87CEEB")

        # Hacer ventana modal
        self.grab_set()
        self.transient(parent.app)

        # Variables
        self.x = symbols('x')
        self.parameters = {}

        try:
            self.function = sympify(function_str)
            self.setup_ui()
            self.plot_function()
        except Exception as e:
            self.show_error(f"Error:\n{str(e)}")

    def setup_ui(self):
        # Configuración de grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)  # Más espacio para gráfico
        self.grid_rowconfigure(0, weight=1)

        # Frame izquierdo (análisis)
        left_frame = ctk.CTkFrame(self, fg_color="#f0f0f0")
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Frame derecho (gráfico)
        right_frame = ctk.CTkFrame(self)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Botón de regreso (texto grande)
        back_btn = ctk.CTkButton(
            left_frame,
            text="← VOLVER",
            command=self.destroy,
            font=("Arial", 18),
            width=120,
            height=40,
            fg_color="#032B44"
        )
        back_btn.pack(pady=20)

        # Panel de parámetros
        self.setup_parameters_panel(left_frame)

        # Panel de análisis
        self.setup_analysis_panel(left_frame)

        # Configurar gráfico
        self.setup_graph_panel(right_frame)

    def setup_parameters_panel(self, parent):
        """Panel de parámetros organizado verticalmente"""
        param_frame = ctk.CTkFrame(parent, fg_color="#e0e0e0")
        param_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Título
        ctk.CTkLabel(
            param_frame,
            text="PARÁMETROS AJUSTABLES:",
            font=("Arial", 20, "bold")
        ).pack(pady=(5, 15))

        # Frame para scroll vertical
        scroll_frame = ctk.CTkScrollableFrame(param_frame)
        scroll_frame.pack(fill="both", expand=True)

        # Obtener variables (excluyendo x)
        variables = [str(s) for s in self.function.free_symbols if str(s) != 'x']

        if not variables:
            ctk.CTkLabel(
                scroll_frame,
                text="No hay parámetros ajustables",
                font=("Arial", 16)
            ).pack(pady=10)
            return

        for var in variables:
            # Frame para cada parámetro
            param_row = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            param_row.pack(fill="x", pady=5, padx=5)

            # Etiqueta del parámetro (30% de ancho)
            ctk.CTkLabel(
                param_row,
                text=f"{var}:",
                font=("Arial", 18),
                width=10,
                anchor="w"
            ).pack(side="left", padx=(10, 5))

            # Slider (50% de ancho)
            slider = ctk.CTkSlider(
                param_row,
                from_=-5,
                to=5,
                number_of_steps=100,
                width=200,
                command=lambda val, v=var: self.update_parameter(v, float(val))
            )
            slider.pack(side="left", padx=5, expand=True)
            slider.set(1.0)

            # Entry (20% de ancho)
            entry = ctk.CTkEntry(
                param_row,
                width=80,
                font=("Arial", 18),
                justify="center"
            )
            entry.pack(side="left", padx=(5, 10))
            entry.insert(0, "1.0")

            # Configurar eventos
            entry.bind("<Return>",
                    lambda event, v=var, s=slider, e=entry: self.update_from_entry(v, s, e))

            # Guardar referencia
            self.parameters[var] = {
                'slider': slider,
                'entry': entry,
                'value': 1.0
            }

    def update_parameter(self, param_name, value):
        """Actualiza desde el slider"""
        try:
            # Actualizar valor
            self.parameters[param_name]['value'] = value

            # Actualizar entry correspondiente
            self.parameters[param_name]['entry'].delete(0, tk.END)
            self.parameters[param_name]['entry'].insert(0, f"{value:.2f}")

            # Regraficar
            self.plot_function()
        except Exception as e:
            print(f"Error actualizando parámetro {param_name}: {str(e)}")

    def update_from_entry(self, param_name, slider, entry):
        """Actualiza desde el campo de texto"""
        try:
            value = float(entry.get())
            # Validar rango
            value = max(-5, min(5, value))

            # Actualizar valor
            self.parameters[param_name]['value'] = value

            # Actualizar slider correspondiente
            slider.set(value)

            # Actualizar entry (por si hubo ajuste de rango)
            entry.delete(0, tk.END)
            entry.insert(0, f"{value:.2f}")

            # Regraficar
            self.plot_function()
        except ValueError:
            # Si el valor no es numérico, restaurar el anterior
            entry.delete(0, tk.END)
            entry.insert(0, f"{self.parameters[param_name]['value']:.2f}")

    def setup_analysis_panel(self, parent):
        """Panel de resultados de análisis"""
        analysis_frame = ctk.CTkScrollableFrame(parent, height=400)
        analysis_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Título (texto grande)
        ctk.CTkLabel(
            analysis_frame,
            text="Análisis:",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        # Lista de análisis (texto grande)
        analyses = [
            ("Dominio:", "empty"),
            ("Interceptos:", "empty"),
            ("Simetría:", "empty"),
            ("Asíntotas:", "empty"),
            ("Derivada:", "empty"),
            ("Monotonía:", "empty"),
            ("Extremos:", "empty"),
            ("Concavidad:", "empty")
        ]

        for title, value in analyses:
            frame = ctk.CTkFrame(analysis_frame, fg_color="#ffffff")
            frame.pack(fill="x", pady=5)

            ctk.CTkLabel(
                frame,
                text=title,
                font=("Arial", 18, "bold"),
                width=150,
                anchor="w"
            ).pack(side="left", padx=10)

            ctk.CTkLabel(
                frame,
                text=value,
                font=("Arial", 18)
            ).pack(side="left", padx=10)

    def setup_graph_panel(self, parent):
        """Configura el panel del gráfico"""
        self.figure, self.ax = plt.subplots(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Configuración inicial
        self.ax.set_facecolor('#f0f0f0')
        self.ax.grid(True, linestyle='--', alpha=0.7)

    def plot_function(self):
        """Dibuja la función actual"""
        try:
            self.ax.clear()

            # Aplicar parámetros
            current_func = self.function
            for param, data in self.parameters.items():
                current_func = current_func.subs(param, data['value'])

            # Verificar si la función es 0
            if current_func == 0:
                self.canvas.draw()
                return

            # Encontrar asíntotas verticales
            vertical_asymptotes = sp.solve(sp.denom(current_func), self.x)
            vertical_asymptotes = [float(a) for a in vertical_asymptotes if a.is_real]

            # Encontrar asíntotas horizontales
            horizontal_asymptote = sp.limit(current_func, self.x, sp.oo)

            # Convertir a numérico
            f = sp.lambdify(self.x, current_func, 'numpy')
            x_vals = np.linspace(-10, 10, 10000)
            y_vals = f(x_vals)

            # Dibujar función
            self.ax.plot(x_vals, y_vals, label=f"f(x) = {sp.pretty(current_func)}", linewidth=2)

            # Dibujar asíntotas verticales
            for va in vertical_asymptotes:
                self.ax.axvline(va, color='red', linestyle='--', linewidth=1)

            # Dibujar asíntota horizontal
            if horizontal_asymptote.is_real:
                self.ax.axhline(float(horizontal_asymptote), color='red', linestyle='--', linewidth=1)

            # Configuración de ejes
            self.ax.axhline(0, color='black', linewidth=0.5)
            self.ax.axvline(0, color='black', linewidth=0.5)
            self.ax.legend(fontsize=14, loc='upper right', frameon=True, fancybox=True, framealpha=0.7, borderpad=1)


            # Ajustar límites de los ejes para centrar la gráfica
            self.ax.set_xlim([-10, 10])
            self.ax.set_ylim([min(y_vals) - 1, max(y_vals) + 1])

            self.canvas.draw()
        except Exception as e:
            print(f"Error al graficar: {str(e)}")

    def show_error(self, message):
        """Muestra mensaje de error"""
        error_label = ctk.CTkLabel(
            self,
            text=message,
            text_color="red",
            font=("Arial", 18)
        )
        error_label.grid(row=0, column=0, padx=20, pady=20)