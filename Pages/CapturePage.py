import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class CapturePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Configure styles first
        style = ttk.Style()
        style.configure('TFrame', background='white')
        style.configure('TLabel', background='white') # Create new style for big back button
        
        # Main container with padding
        main_container = ttk.Frame(self)
        main_container.pack(fill=BOTH, expand=True)
        
        # Top navigation bar
        nav_frame = ttk.Frame(main_container)
        nav_frame.pack(fill=X, padx=40, pady=35)
        
        # Back button with larger font and size using the new style
        back_button = tk.Label(
            nav_frame,
            text="◄Back",
            font=("Helvetica", 13),
            cursor="hand2"
        )
        back_button.pack(side=LEFT)
        back_button.bind("<Button-1>", lambda e: controller.show_frame("HomePage"))
        
        # Mode display with larger font
        self.mode_label = ttk.Label(
            nav_frame,
            text="Mode: ",
            font=("Helvetica", 13)
        )
        self.mode_label.pack(side=RIGHT)
        
        # Center frame for webcam preview
        center_frame = ttk.Frame(main_container)
        center_frame.pack(expand=True, fill=BOTH, padx=70)
        
        # Create a frame to center the preview
        preview_container = ttk.Frame(center_frame)
        preview_container.pack(expand=True, pady=(0, 0))  # Added top padding of 50 pixels
        
        # Webcam preview label
        self.preview_label = ttk.Label(
            preview_container
        )
        self.preview_label.pack(expand=True)
        
        # Bottom frame for capture button with higher z-index
        button_frame = ttk.Frame(main_container)
        button_frame.pack(side=BOTTOM, pady=(0, 50))  # Increased bottom padding
        button_frame.lift()  # Bring button frame to front
        
        # Load capture button image
        self.capture_img = tk.PhotoImage(file="Assets/Components/Capture.png")
        
        # Create capture button
        capture_btn = tk.Label(
            button_frame,
            image=self.capture_img,
            cursor="hand2",
            bg='white',
        )
        capture_btn.pack()
        capture_btn.bind("<Button-1>", self.take_picture)
        
        # Ensure button stays on top
        button_frame.lift()
        capture_btn.lift()

    def set_mode(self, mode):
        self.mode_label.config(text=f"Mode: {mode}")
        # Start webcam preview when page is shown
        self.controller.start_webcam()
        webcam = self.controller.get_webcam()
        if webcam:
            # Set larger display mode for capture page
            webcam.set_display_mode("large")
            webcam.start_preview(self.preview_label)

    def take_picture(self, event):
        # Add your capture logic here
        pass
