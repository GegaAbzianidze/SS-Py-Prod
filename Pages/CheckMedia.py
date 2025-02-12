import tkinter as tk
from tkinter import ttk

class CheckMedia(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Title Label
        label = ttk.Label(self, text="Check Media Page", font=("Helvetica", 18))
        label.pack(pady=10, padx=10)

        # Navigation buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20)

        upload_button = ttk.Button(
            button_frame,
            text="Go to Upload",
            command=lambda: controller.show_frame("UploadPage")
        )
        upload_button.pack(pady=5)

        capture_button = ttk.Button(
            button_frame,
            text="Back to Capture",
            command=lambda: controller.show_frame("CapturePage")
        )
        capture_button.pack(pady=5)
