import tkinter as tk
from tkinter import ttk

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Main title
        title_label = ttk.Label(self, text="SnapStation", font=("Helvetica", 62, "bold"))
        title_label.pack(pady=(150, 10))
        
        # Subtitle
        subtitle_label = ttk.Label(self, text="Choose your capture mode", font=("Helvetica", 22))
        subtitle_label.pack(pady=(0, 40))

        # Create center frame for buttons
        center_frame = ttk.Frame(self)
        center_frame.pack(expand=True, pady=(0, 100))
        
        # Load button images from Components folder
        self.take_picture_img = tk.PhotoImage(file="Assets/Components/Picture.png")
        self.create_gif_img = tk.PhotoImage(file="Assets/Components/Gif.png")
        self.create_panorama_img = tk.PhotoImage(file="Assets/Components/360.png")
        
        # Create image buttons with equal spacing
        take_picture_btn = tk.Label(
            center_frame,
            image=self.take_picture_img,
            cursor="hand2"
        )
        take_picture_btn.grid(row=0, column=0, padx=20)
        take_picture_btn.bind("<Button-1>", lambda e: self.switch_to_capture("PIC"))
        
        create_gif_btn = tk.Label(
            center_frame,
            image=self.create_gif_img,
            cursor="hand2"
        )
        create_gif_btn.grid(row=0, column=1, padx=20)
        create_gif_btn.bind("<Button-1>", lambda e: self.switch_to_capture("GIF"))

        create_panorama_btn = tk.Label(
            center_frame,
            image=self.create_panorama_img,
            cursor="hand2"
        )
        create_panorama_btn.grid(row=0, column=2, padx=20)
        create_panorama_btn.bind("<Button-1>", lambda e: self.switch_to_capture("360°"))
        
    def switch_to_capture(self, mode):
        capture_page = self.controller.frames["CapturePage"]
        capture_page.set_mode(mode)
        self.controller.show_frame("CapturePage")
        