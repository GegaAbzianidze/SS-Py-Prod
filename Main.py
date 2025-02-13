import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from Pages.AdminPanel import AdminPanel
from Pages.HomePage import HomePage
from Pages.CapturePage import CapturePage
from Pages.CheckMedia import CheckMedia
from Pages.UploadPage import UploadPage
from Pages.FinishPage import FinishPage

class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="cosmo")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Initialize single webcam instance for the entire application
        self.webcam = None
        self.webcam_running = False
        
        # Set initial window state
        self.is_fullscreen = True
        self.attributes('-fullscreen', True)
        
        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")

        # Add keyboard bindings
        self.bind('<Escape>', lambda e: self.toggle_fullscreen())
        self.bind('<Control-x>', self.close_program)

        # Create a container frame
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # Create frames for each page
        for F in (HomePage, AdminPanel, CapturePage, CheckMedia, UploadPage, FinishPage):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("AdminPanel")  # Show AdminPanel page by default

    def show_frame(self, page_name):
        """Raise the frame/page to the top to display it"""
        frame = self.frames[page_name]
        frame.tkraise()

    def close_program(self, event=None):
        """Close the application"""
        self.quit()
        self.destroy()

    def on_closing(self):
        """Handle cleanup when closing the application"""
        self.stop_webcam()
        self.quit()
        self.destroy()

    def toggle_fullscreen(self, event=None):
        """Toggle between fullscreen and windowed mode"""
        self.is_fullscreen = not self.is_fullscreen
        self.attributes('-fullscreen', self.is_fullscreen)
        if not self.is_fullscreen:
            # Set a reasonable window size when not fullscreen
            self.geometry('800x600')

    def get_webcam(self):
        """Get or create the webcam instance"""
        if not self.webcam:
            from Utils.WebcamUtils import WebcamUtils
            self.webcam = WebcamUtils(preview_size=(640, 360))
        return self.webcam
    
    def start_webcam(self):
        """Start the webcam if it's not already running"""
        if not self.webcam_running:
            self.webcam_running = True
            self.get_webcam()
    
    def stop_webcam(self):
        """Stop the webcam completely"""
        if self.webcam:
            self.webcam.stop_preview()
            self.webcam = None
            self.webcam_running = False

if __name__ == "__main__":
    app = App()
    app.mainloop()
