import customtkinter as ctk
import tkinter as tk
from Interface.show_info import ResultWindow

class MatcomFunctionLabApp:
    def __init__(self):
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("dark-blue")
        
        self.app = ctk.CTk()
        self.setup_window()
        self.create_widgets()
        self.app.mainloop()

    def setup_window(self):
        width_window = self.app.winfo_screenwidth()
        height_window = self.app.winfo_screenheight()

        width_screen = int(width_window * 0.8)
        height_screen = int(height_window * 0.8)

        x_position = (width_window - width_screen) // 2
        y_position = (height_window - height_screen) // 2

        self.app.geometry(f"{width_screen}x{height_screen}+{x_position}+{y_position}")
        self.app.title("MatcomFunctionLab")
        self.app.configure(bg="#87CEEB")

    def create_widgets(self):
        self.app.grid_columnconfigure(0, weight=1)
        
        # Título
        app_title = ctk.CTkLabel(
            self.app, 
            text="MatcomFunctionLab", 
            text_color="#333333",
            font=("Arial", 50, "bold"),
            fg_color="transparent",
            bg_color="transparent"
        )
        app_title.grid(row=0, column=0, padx=20, pady=(100, 30), columnspan=2, sticky="nsew")

        # Entrada de función
        self.function_entry = ctk.CTkEntry(
            self.app,
            placeholder_text="f(x)=sin(x+4)+x^2",
            font=('Arial', 20, 'italic'),
            height=60,
            bg_color="transparent",
            border_color="#ADD8E6",
            placeholder_text_color="#999999"
        )
        self.function_entry.grid(row=1, column=0, padx=(100, 20), pady=(30, 20), sticky="ew")

        # Botón de análisis
        analyze_btn = ctk.CTkButton(
            self.app,
            text="Init",
            command=self.analyze_function,
            height=55,
            bg_color="transparent",
            fg_color="#032B44"
        )
        analyze_btn.grid(row=1, column=1, padx=(20, 100), pady=(30, 20), sticky="ew")

        # Ejemplos
        examples_label = ctk.CTkLabel(
            self.app,
            text="Ejemplos de funciones",
            text_color="#333333",
            font=("Arial", 24, "bold"),
            fg_color="transparent",
            bg_color="transparent"
        )
        examples_label.grid(row=2, column=0, padx=20, pady=(20, 20), columnspan=2, sticky="nsew")

        # Botones de ejemplo
        self.create_example_buttons()

    def create_example_buttons(self):
        examples = [
            ("F1", "sin(x) + x**a"),
            ("F2", "cos(x) - log(x+a)"),
            ("F3", "x**a - b*x")
        ]

        for i, (text, func) in enumerate(examples, start=3):
            btn = ctk.CTkButton(
                self.app,
                text=text,
                command=lambda f=func: self.set_example(f),
                height=60,
                bg_color="transparent",
                fg_color="#032B44"
            )
            btn.grid(row=i, column=0, padx=400, pady=20, columnspan=2, sticky="nsew")

    def set_example(self, example):
        self.function_entry.delete(0, tk.END)
        self.function_entry.insert(0, example)

    def analyze_function(self):
        function_str = self.function_entry.get().strip()
        if not function_str:
            tk.messagebox.showerror("Error", "Ingrese una función")
            return
        
        try:
            from sympy import symbols, sympify
            x = symbols('x')
            sympify(function_str)
            ResultWindow(self, function_str)
        except Exception as e:
            tk.messagebox.showerror("Error", f"Función inválida:\n{str(e)}")