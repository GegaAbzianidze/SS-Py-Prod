import tkinter as tk
from tkinter import ttk

class CapturePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Title Label
        label = ttk.Label(self, text="Capture Page", font=("Helvetica", 18))
        label.pack(pady=10, padx=10)

        # Navigation buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20)

        check_media_button = ttk.Button(
            button_frame,
            text="Go to Check Media",
            command=lambda: controller.show_frame("CheckMedia")
        )   
        check_media_button.pack(pady=5)

        home_button = ttk.Button(
            button_frame,
            text="Back to Home",
            command=lambda: controller.show_frame("HomePage")
        )
        home_button.pack(pady=5)
