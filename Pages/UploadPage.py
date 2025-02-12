import tkinter as tk
from tkinter import ttk

class UploadPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Title Label
        label = ttk.Label(self, text="Upload Page", font=("Helvetica", 18))
        label.pack(pady=10, padx=10)

        # Navigation buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20)

        finish_button = ttk.Button(
            button_frame,
            text="Go to Finish",
            command=lambda: controller.show_frame("FinishPage")
        )
        finish_button.pack(pady=5)

        check_media_button = ttk.Button(
            button_frame,
            text="Back to Check Media",
            command=lambda: controller.show_frame("CheckMedia")
        )
        check_media_button.pack(pady=5)
