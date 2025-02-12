import tkinter as tk
from tkinter import ttk

class AdminPanel(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Title Label
        label = ttk.Label(self, text="Admin Panel", font=("Helvetica", 18))
        label.pack(pady=10, padx=10)

        # Navigation buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20)

        home_button = ttk.Button(
            button_frame,
            text="Go to Home",
            command=lambda: controller.show_frame("HomePage")
        )
        home_button.pack(pady=5)

        # Add your admin panel specific widgets and functionality here 