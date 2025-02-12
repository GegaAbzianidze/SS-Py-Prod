import tkinter as tk
from tkinter import ttk

class FinishPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Title Label
        label = ttk.Label(self, text="Finish Page", font=("Helvetica", 18))
        label.pack(pady=10, padx=10)

        # Navigation buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20)

        admin_button = ttk.Button(
            button_frame,
            text="Back to Admin",
            command=lambda: controller.show_frame("AdminPanel")
        )
        admin_button.pack(pady=5)

        upload_button = ttk.Button(
            button_frame,
            text="Back to Upload",
            command=lambda: controller.show_frame("UploadPage")
        )
        upload_button.pack(pady=5)
