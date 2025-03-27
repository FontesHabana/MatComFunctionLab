import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter as tk
import matplotlib.pyplot as plt

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
        app_title = ctk.CTkLabel(self.app, text="MatcomFunctionLab", text_color="#333333",
                                 font=("Arial", 50, "bold"),
                                 fg_color="transparent",
                                 bg_color="transparent")
        app_title.grid(row=0, column=0, padx=20, pady=(100, 30), columnspan=2, sticky="nsew")

        imput_function = ctk.CTkEntry(self.app, placeholder_text="f(x)=sin(x+4)+x^2",
                                      font=('Arial', 20, 'italic'),
                                      height=60,
                                      bg_color="transparent",
                                      border_color="#ADD8E6",
                                      placeholder_text_color="#999999")
        imput_function.grid(row=1, column=0, padx=(100, 20), pady=(30, 20), sticky="ew")

        buttom_sendFunction = ctk.CTkButton(self.app, text="Init",
                                            command=self.buttom_callback,
                                            height=55,
                                            bg_color="transparent",
                                            fg_color="#032B44")
        buttom_sendFunction.grid(row=1, column=1, padx=(20, 100), pady=(30, 20), sticky="ew")

        some_function = ctk.CTkLabel(self.app, text="Ejemplos de funciones", text_color="#333333",
                                     font=("Arial", 24, "bold"),
                                     fg_color="transparent",
                                     bg_color="transparent")
        some_function.grid(row=2, column=0, padx=20, pady=(20, 20), columnspan=2, sticky="nsew")

        buttom_sendF1 = ctk.CTkButton(self.app, text="F1", command=self.buttom_callback,
                                      height=60,
                                      bg_color="transparent",
                                      fg_color="#032B44")
        buttom_sendF1.grid(row=3, column=0, padx=400, pady=20, columnspan=2, sticky="nsew")

        buttom_sendF2 = ctk.CTkButton(self.app, text="F2",
                                      command=self.buttom_callback,
                                      height=60,
                                      bg_color="transparent",
                                      fg_color="#032B44")
        buttom_sendF2.grid(row=4, column=0, padx=400, pady=20, columnspan=2, sticky="nsew")


    def buttom_callback(self):
        self.open_result_window(self.imput_function.get())

    
        
if __name__ == "__main__":
    MatcomFunctionLabApp()