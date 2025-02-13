import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from datetime import datetime
import logging
from Utils.WebcamUtils import WebcamUtils  # Changed from WebcamUtils

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AdminPanel(ttk.Frame):
    def __init__(self, parent, controller):
        logger.debug("Initializing AdminPanel")
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.webcam = None
        self.webcam_frame = None
        
        # Configure style
        style = ttk.Style()
        style.configure('Custom.TFrame', background='#FAF7F5')
        style.configure('Custom.TButton', 
                       background='#6B4D3C',
                       foreground='white',
                       padding=10)
        style.configure('Success.TButton',
                       background='#8FB3A3',
                       foreground='white',
                       padding=10)
        
        # Main container
        main_container = ttk.Frame(self, style='Custom.TFrame', padding=20)
        main_container.pack(fill=BOTH, expand=YES)
        
        # Header with background
        header_frame = ttk.Frame(main_container, style='Custom.TFrame')
        header_frame.pack(fill=X, pady=(0, 20))
        
        title = ttk.Label(
            header_frame, 
            text="Admin Dashboard",
            font=("Helvetica", 32, "bold"),
            foreground='#6B4D3C',
            background='#FAF7F5'
        )
        title.pack(side=LEFT)
        
        settings_btn = ttk.Button(
            header_frame,
            text="⚙ Settings",
            style='Custom.TButton',
            width=15
        )
        settings_btn.pack(side=RIGHT)

        # Content Frame
        content_frame = ttk.Frame(main_container, style='Custom.TFrame')
        content_frame.pack(fill=BOTH, expand=YES)

        # Tab Control
        self.tab_control = ttk.Notebook(content_frame)
        self.tab_control.pack(fill=BOTH, expand=YES)

        # Events Tab with padding
        events_tab = ttk.Frame(self.tab_control, padding=20, style='Custom.TFrame')
        self.tab_control.add(events_tab, text=" 📅 Events ")
        self.setup_events_tab(events_tab)

        # Test & Logs Tab with padding
        test_logs_tab = ttk.Frame(self.tab_control, padding=20, style='Custom.TFrame')
        self.tab_control.add(test_logs_tab, text=" 🔧 Test & Logs ")
        self.setup_test_logs_tab(test_logs_tab)

    def setup_events_tab(self, parent):
        # Create Event Section with proper spacing
        create_event_frame = ttk.Frame(parent, style='Custom.TFrame')
        create_event_frame.pack(fill=BOTH, expand=YES)

        # Header with background
        header_frame = ttk.Frame(create_event_frame, style='Custom.TFrame')
        header_frame.pack(fill=X, pady=(0, 20))

        ttk.Label(
            header_frame,
            text="Create Event",
            font=("Helvetica", 24, "bold"),
            foreground='#6B4D3C',
            background='#FAF7F5'
        ).pack(side=LEFT)

        new_event_btn = ttk.Label(
            header_frame,
            text="+ New Event",
            style='Success.TButton',
        )
        new_event_btn.pack(side=RIGHT)

        # Form container with proper spacing
        form_frame = ttk.Frame(create_event_frame, style='Custom.TFrame')
        form_frame.pack(fill=BOTH, expand=YES, pady=(0, 20))
        
        # Configure grid
        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=1)
        
        # Left Column
        left_frame = ttk.Frame(form_frame, style='Custom.TFrame')
        left_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))

        ttk.Label(
            left_frame,
            text="Event Name",
            font=("Helvetica", 12),
            background='#FAF7F5'
        ).pack(anchor=W, pady=(0, 5))
        
        ttk.Entry(
            left_frame,
            font=("Helvetica", 11)
        ).pack(fill=X, pady=(0, 15))

        ttk.Label(
            left_frame,
            text="Event Date",
            font=("Helvetica", 12),
            background='#FAF7F5'
        ).pack(anchor=W, pady=(0, 5))
        
        # Date and Time Frame
        date_frame = ttk.Frame(left_frame, style='Custom.TFrame')
        date_frame.pack(fill=X, pady=(0, 15))
        
        # Current date and time
        current_datetime = datetime.now()
        date_entry = ttk.Entry(
            date_frame,
            font=("Helvetica", 11),
            width=28
        )
        date_entry.pack(side=LEFT, fill=X, expand=True)
        date_entry.insert(0, current_datetime.strftime('%Y-%m-%d %H:%M'))
        date_entry.configure(state='readonly')  # Make it read-only

        ttk.Label(
            left_frame,
            text="Max Number of Images",
            font=("Helvetica", 12),
            background='#FAF7F5'
        ).pack(anchor=W, pady=(0, 5))
        
        ttk.Entry(
            left_frame,
            font=("Helvetica", 11)
        ).pack(fill=X, pady=(0, 15))

        # Right Column
        right_frame = ttk.Frame(form_frame, style='Custom.TFrame')
        right_frame.grid(row=0, column=1, sticky='nsew', padx=(10, 0))

        # Password Protection Section
        password_section = ttk.Frame(right_frame, style='Custom.TFrame')
        password_section.pack(fill=X, pady=(0, 15))
        
        # Password Protection Toggle Frame
        password_frame = ttk.Frame(password_section, style='Custom.TFrame')
        password_frame.pack(fill=X)
        
        ttk.Label(
            password_frame,
            text="Password Protected",
            font=("Helvetica", 12),
            background='#FAF7F5'
        ).pack(side=LEFT)
        
        # Password input frame (initially hidden)
        self.password_input_frame = ttk.Frame(password_section, style='Custom.TFrame')
        
        
        
        self.password_entry = ttk.Entry(
            self.password_input_frame,
            font=("Helvetica", 11),
            show="●"  # Show dots instead of actual characters
        )
        self.password_entry.pack(fill=X)

        def toggle_password():
            if password_var.get():  # If checkbox is checked
                self.password_input_frame.pack(fill=X, pady=(5, 0))
            else:
                self.password_input_frame.pack_forget()
                self.password_entry.delete(0, tk.END)  # Clear password when unchecked

        password_var = tk.BooleanVar()
        password_checkbox = ttk.Checkbutton(
            password_frame, 
            style='Custom.TCheckbutton',
            variable=password_var,
            command=toggle_password
        )
        password_checkbox.pack(side=RIGHT)

        ttk.Label(
            right_frame,
            text="Storage Location",
            font=("Helvetica", 12),
            background='#FAF7F5'
        ).pack(anchor=W, pady=(0, 5))
        
        storage_combo = ttk.Combobox(
            right_frame,
            values=["Local Storage", "Cloud Storage"],
            font=("Helvetica", 11)
        )
        storage_combo.pack(fill=X, pady=(0, 15))
        storage_combo.set("Select storage location")

        # Create Event Button at the bottom
        create_btn = ttk.Button(
            create_event_frame,
            text="Create Event",
            style='Success.TButton'
        )
        create_btn.pack(fill=X, pady=(20, 0))

    def setup_test_logs_tab(self, parent):
        logger.debug("Setting up test logs tab")
        # System Tests Section
        tests_frame = ttk.Frame(parent)
        tests_frame.pack(fill=X, pady=(0, 30))

        ttk.Label(
            tests_frame,
            text="System Tests",
            font=("Helvetica", 24),
            foreground='#6B4D3C'
        ).pack(anchor=W)

        # Test Buttons Grid
        buttons_frame = ttk.Frame(tests_frame)
        buttons_frame.pack(fill=X, pady=20)

        # Create Camera Test Button separately for better control
        camera_frame = ttk.Frame(buttons_frame)
        camera_frame.pack(fill=X, pady=5)
        
        camera_btn = ttk.Button(
            camera_frame,
            text="📷 Test Camera Connection",
            style='Custom.TButton',
            command=lambda: self.toggle_webcam_preview()  # Use lambda to ensure proper binding
        )
        camera_btn.pack(side=LEFT, expand=YES, fill=X, padx=5)
        logger.debug("Camera test button created and bound to toggle_webcam_preview")

        # Other test buttons
        other_buttons = [
            ("Test Upload Speed", "⬆", lambda: logger.debug("Upload speed test clicked")),
            ("Test Image Processing", "🖼", lambda: logger.debug("Image processing test clicked")),
            ("Run Diagnostics", "🔍", lambda: logger.debug("Diagnostics clicked"))
        ]

        current_frame = camera_frame
        for i, (text, icon, command) in enumerate(other_buttons):
            if i % 2 == 0:
                current_frame = ttk.Frame(buttons_frame)
                current_frame.pack(fill=X, pady=5)

            btn = ttk.Button(
                current_frame,
                text=f"{icon} {text}",
                style='Custom.TButton',
                command=command
            )
            btn.pack(side=RIGHT if i % 2 == 0 else LEFT, expand=YES, fill=X, padx=5)

        # System Logs Section
        self.logs_frame = ttk.Frame(parent)
        self.logs_frame.pack(fill=BOTH, expand=YES)
        logger.debug("Test logs tab setup completed")

    def setup_webcam_preview(self, parent):
        logger.debug("Setting up webcam preview frame")
        try:
            self.webcam_frame = ttk.Frame(self, style='Custom.TFrame')
            logger.debug("Created webcam frame")
            
            # Create header with close button
            header_frame = ttk.Frame(self.webcam_frame, style='Custom.TFrame')
            header_frame.pack(fill=X, pady=(0, 10))
            
            ttk.Label(
                header_frame,
                text="Camera Preview",
                font=("Helvetica", 16, "bold"),
                foreground='#6B4D3C',
                background='#FAF7F5'
            ).pack(side=LEFT)
            
            close_btn = ttk.Button(
                header_frame,
                text="✕",
                style='Custom.TButton',
                width=3,
                command=self.hide_webcam_preview
            )
            close_btn.pack(side=RIGHT)
            
            # Create preview label
            self.preview_label = ttk.Label(self.webcam_frame)
            self.preview_label.pack(pady=10)
            logger.debug("Webcam preview frame setup completed")
        except Exception as e:
            logger.error(f"Error setting up webcam preview frame: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())

    def toggle_webcam_preview(self):
        logger.debug("Toggle webcam preview called")
        # Check if webcam_frame exists and is not None before checking if it's mapped
        if hasattr(self, 'webcam_frame') and self.webcam_frame is not None and self.webcam_frame.winfo_ismapped():
            logger.debug("Webcam frame is visible, hiding preview")
            self.hide_webcam_preview()
        else:
            logger.debug("Webcam frame is hidden or doesn't exist, showing preview")
            self.show_webcam_preview()

    def show_webcam_preview(self):
        logger.debug("Attempting to show webcam preview")
        try:
            # Get the application-level webcam instance
            self.controller.start_webcam()
            webcam = self.controller.get_webcam()
            
            if not hasattr(self, 'webcam_frame') or self.webcam_frame is None:
                logger.debug("Setting up webcam frame")
                self.setup_webcam_preview(self)
            
            logger.debug("Packing webcam frame")
            self.webcam_frame.pack(before=self.logs_frame, fill=X, pady=(0, 20))
            
            logger.debug("Starting webcam preview")
            webcam.start_preview(self.preview_label)
            
        except Exception as e:
            logger.error(f"Error showing webcam preview: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())

    def hide_webcam_preview(self):
        logger.debug("Attempting to hide webcam preview")
        try:
            if hasattr(self, 'webcam_frame') and self.webcam_frame:
                logger.debug("Hiding webcam frame")
                self.webcam_frame.pack_forget()
                logger.debug("Webcam frame hidden")
        except Exception as e:
            logger.error(f"Error hiding webcam preview: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())

    def __del__(self):
        logger.debug("AdminPanel cleanup")
        # Remove the webcam cleanup from here since it's managed at the app level 