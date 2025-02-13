import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from datetime import datetime
import logging
from Utils.WebcamUtils import WebcamUtils  # Changed from WebcamUtils
from PIL import Image, ImageTk
import time
from Utils.CaptureUtils import CaptureUtils
import cv2
import os
from Utils.FirebaseUtils import FirebaseUtils
import shutil
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add these global variables after the imports and before the AdminPanel class
class EventConfig:
    current_event_id: Optional[str] = None
    current_event_name: Optional[str] = None
    max_images: Optional[int] = None
    current_image_count: Optional[int] = 0
    storage_type: Optional[str] = None

class AdminPanel(ttk.Frame):
    def __init__(self, parent, controller):
        logger.debug("Initializing AdminPanel")
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.webcam = None
        self.webcam_frame = None
        
        # Initialize instance variables first
        self.firebase_utils = FirebaseUtils()
        self.event_name_entry = None
        self.date_entry = None
        self.max_images_entry = None
        self.password_var = tk.BooleanVar()  # Initialize here
        self.password_entry = None
        self.password_input_frame = None  # Initialize here
        self.storage_combo = None
        
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
        
        self.event_name_entry = ttk.Entry(
            left_frame,
            font=("Helvetica", 11)
        )
        self.event_name_entry.pack(fill=X, pady=(0, 15))

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
        self.date_entry = ttk.Entry(
            date_frame,
            font=("Helvetica", 11),
            width=28
        )
        self.date_entry.pack(side=LEFT, fill=X, expand=True)
        self.date_entry.insert(0, current_datetime.strftime('%Y-%m-%d %H:%M'))
        self.date_entry.configure(state='readonly')

        ttk.Label(
            left_frame,
            text="Max Number of Images",
            font=("Helvetica", 12),
            background='#FAF7F5'
        ).pack(anchor=W, pady=(0, 5))
        
        self.max_images_entry = ttk.Entry(
            left_frame,
            font=("Helvetica", 11)
        )
        self.max_images_entry.pack(fill=X, pady=(0, 15))
        self.max_images_entry.insert(0, "50")  # Default value

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

        self.password_var = tk.BooleanVar()
        password_checkbox = ttk.Checkbutton(
            password_frame, 
            style='Custom.TCheckbutton',
            variable=self.password_var,
            command=self.toggle_password
        )
        password_checkbox.pack(side=RIGHT)

        ttk.Label(
            right_frame,
            text="Storage Location",
            font=("Helvetica", 12),
            background='#FAF7F5'
        ).pack(anchor=W, pady=(0, 5))
        
        self.storage_combo = ttk.Combobox(
            right_frame,
            values=["Local Storage", "Cloud Storage"],
            font=("Helvetica", 11)
        )
        self.storage_combo.pack(fill=X, pady=(0, 15))
        self.storage_combo.set("Cloud Storage")  # Set default to Cloud Storage

        # Create Event Button at the bottom
        create_btn = ttk.Button(
            create_event_frame,
            text="Create Event",
            style='Success.TButton',
            command=self.event_button_clicked
        )
        create_btn.pack(fill=X, pady=(20, 0))

    def event_button_clicked(self):
        if self.storage_combo.get() == "Local Storage":
            self.create_event_local()
        elif self.storage_combo.get() == "Cloud Storage":
            self.create_event()

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
            ("Test Image Processing", "🖼", self.start_media_tests),
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

        # Add media preview frame after the buttons
        self.media_preview_frame = ttk.Frame(parent, style='Custom.TFrame')
        self.media_preview_frame.pack(fill=X, pady=(0, 20))
        self.media_preview_frame.pack_forget()  # Initially hidden

    def start_media_tests(self):
        """Start the sequence of media tests"""
        logger.debug("Starting media tests")
        try:
            # Ensure webcam is running
            self.controller.start_webcam()
            webcam = self.controller.get_webcam()
            
            # Create or show media preview frame
            if not self.media_preview_frame.winfo_ismapped():
                self.media_preview_frame.pack(before=self.logs_frame, fill=X, pady=(0, 20))
            
            # Clear any existing content
            for widget in self.media_preview_frame.winfo_children():
                widget.destroy()
            
            # Create preview label
            preview_label = ttk.Label(self.media_preview_frame)
            preview_label.pack(pady=10)
            
            # Capture and display image
            frame = webcam.get_current_frame()
            if frame is not None:
                image = Image.fromarray(frame)
                photo = ImageTk.PhotoImage(image)
                preview_label.configure(image=photo)
                preview_label.image = photo  # Keep a reference
                
                # Add GIF test button
                gif_button = ttk.Button(
                    self.media_preview_frame,
                    text="Test GIF Capture",
                    style='Custom.TButton',
                    command=lambda: self.capture_gif_test(preview_label)
                )
                gif_button.pack(pady=5)
            
        except Exception as e:
            logger.error(f"Error in media tests: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())

    def capture_gif_test(self, preview_label):
        """Capture and display a test GIF"""
        logger.debug("Starting GIF capture test")
        try:
            # Hide the GIF test button if it exists
            for widget in self.media_preview_frame.winfo_children():
                if isinstance(widget, ttk.Button) and widget['text'] == "Test GIF Capture":
                    widget.pack_forget()
            
            webcam = self.controller.get_webcam()
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"Assets/test_captures/gif_test_{timestamp}.gif"
            
            # Add a progress label
            progress_label = ttk.Label(
                self.media_preview_frame,
                text="Capturing GIF (3 seconds)...",
                style='Custom.TLabel'
            )
            progress_label.pack(pady=5)
            
            def capture_and_display():
                try:
                    # Capture GIF
                    if CaptureUtils.capture_gif(webcam, duration=3, filename=filename):
                        # Remove progress label
                        progress_label.destroy()
                        
                        # Display the captured GIF
                        gif = Image.open(filename)
                        gif_frames = []
                        
                        # Load all frames
                        current_frame = 0
                        while True:
                            try:
                                gif.seek(current_frame)
                                frame = gif.copy()
                                if frame.size != (640, 360):
                                    frame = frame.resize((640, 360), Image.Resampling.LANCZOS)
                                gif_frames.append(ImageTk.PhotoImage(frame))
                                current_frame += 1
                            except EOFError:
                                break
                        
                        def update_gif(frame_index=0):
                            if preview_label.winfo_exists():
                                preview_label.configure(image=gif_frames[frame_index])
                                preview_label.image = gif_frames[frame_index]
                                next_frame = (frame_index + 1) % len(gif_frames)
                                preview_label.after(100, update_gif, next_frame)
                        
                        # Start GIF animation
                        update_gif()
                        
                        # Add video test button
                        video_button = ttk.Button(
                            self.media_preview_frame,
                            text="Test Video Capture",
                            style='Custom.TButton',
                            command=lambda: self.capture_video_test(preview_label)
                        )
                        video_button.pack(pady=5)
                
                except Exception as e:
                    logger.error(f"Error in GIF capture and display: {str(e)}")
                    if progress_label.winfo_exists():
                        progress_label.configure(text="Error capturing GIF")
                    import traceback
                    logger.error(traceback.format_exc())
            
            # Run the capture process in a separate thread
            import threading
            capture_thread = threading.Thread(target=capture_and_display, daemon=True)
            capture_thread.start()
            
        except Exception as e:
            logger.error(f"Error setting up GIF capture: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())

    def capture_video_test(self, preview_label):
        """Capture and display a test video"""
        logger.debug("Starting video capture test")
        try:
            # Hide the video test button
            for widget in self.media_preview_frame.winfo_children():
                if isinstance(widget, ttk.Button) and widget['text'] == "Test Video Capture":
                    widget.pack_forget()
            
            webcam = self.controller.get_webcam()
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"Assets/test_captures/video_test_{timestamp}.mp4"
            
            # Add a progress label
            progress_label = ttk.Label(
                self.media_preview_frame,
                text="Capturing Video (7 seconds)...",
                style='Custom.TLabel'
            )
            progress_label.pack(pady=5)
            
            def capture_and_display():
                try:
                    # Clear previous image/gif from preview label
                    preview_label.configure(image='')
                    preview_label.image = None
                    
                    # Capture video
                    if CaptureUtils.capture_video(webcam, filename, duration=7):
                        progress_label.configure(text="Video captured successfully!")
                        
                        # Create video preview using OpenCV
                        cap = cv2.VideoCapture(filename)
                        
                        def update_video_frame():
                            ret, frame = cap.read()
                            if ret:
                                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                frame = cv2.resize(frame, (640, 360))
                                image = Image.fromarray(frame)
                                photo = ImageTk.PhotoImage(image=image)
                                preview_label.configure(image=photo)
                                preview_label.image = photo
                                preview_label.after(33, update_video_frame)
                            else:
                                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                                preview_label.after(33, update_video_frame)
                        
                        # Start video playback
                        update_video_frame()
                        
                        # Add clear button
                        clear_button = ttk.Button(
                            self.media_preview_frame,
                            text="Clear Tests",
                            style='Custom.TButton',
                            command=lambda: [cap.release(), self.clear_media_tests()]
                        )
                        clear_button.pack(pady=5)
                    else:
                        progress_label.configure(text="Failed to capture video")
                
                except Exception as e:
                    logger.error(f"Error in video capture and display: {str(e)}")
                    if progress_label.winfo_exists():
                        progress_label.configure(text="Error capturing video")
                    import traceback
                    logger.error(traceback.format_exc())
            
            # Run the capture process in a separate thread
            import threading
            capture_thread = threading.Thread(target=capture_and_display, daemon=True)
            capture_thread.start()
            
        except Exception as e:
            logger.error(f"Error setting up video capture: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())

    def clear_media_tests(self):
        """Clear all media test displays and files"""
        logger.debug("Clearing media tests")
        try:
            # Clear the preview frame
            self.media_preview_frame.pack_forget()
            for widget in self.media_preview_frame.winfo_children():
                widget.destroy()
            
            # Delete all files in test_captures directory
            test_captures_dir = "Assets/test_captures"
            if os.path.exists(test_captures_dir):
                for file in os.listdir(test_captures_dir):
                    file_path = os.path.join(test_captures_dir, file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        logger.error(f"Error deleting file {file_path}: {str(e)}")
        
        except Exception as e:
            logger.error(f"Error clearing media tests: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())

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

    def toggle_password(self):
        """Toggle password entry visibility"""
        if self.password_var.get():
            self.password_input_frame.pack(fill=X, pady=(5, 0))
        else:
            self.password_input_frame.pack_forget()
            if self.password_entry:
                self.password_entry.delete(0, tk.END)

    def create_event(self):
        """Create a new event and upload starting GIF"""
        try:
            # Validate inputs
            event_name = self.event_name_entry.get().strip()
            if not event_name:
                logger.error("Event name is required")
                return

            max_images = self.max_images_entry.get().strip()
            try:
                max_images = int(max_images)
                if max_images <= 0:
                    raise ValueError("Max images must be positive")
            except ValueError as e:
                logger.error(f"Invalid max images value: {str(e)}")
                return

            # Generate random 12-character event ID
            import string
            import random
            event_id = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

            # Get password if enabled
            password = self.password_entry.get() if self.password_var.get() else "0"
            access_level = "Public" if not self.password_var.get() else "Private"

            # Create event data
            event_data = {
                "event_id": event_id,
                "name": event_name,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                "password": password,
                "access_level": access_level,
                "max_images": max_images,
                "current_image_count": 0,
                "Images": {
                    "0": {}  # Will be updated with StartingGif info
                }
            }

            # Upload StartingGif
            starting_gif_path = "Assets/Components/StartingGif.gif"
            if not os.path.exists(starting_gif_path):
                logger.error("StartingGif.gif not found")
                return

            # Upload to Firebase Storage
            remote_path = f"events/{event_id}/StartingGif.gif"
            gif_url = self.firebase_utils.upload_file(starting_gif_path, remote_path)

            if gif_url:
                # Update event data with GIF info
                event_data["Images"]["0"] = {
                    "type": "GIF",
                    "url": gif_url,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                }

                # Create event in Firebase Realtime Database
                if self.firebase_utils.create_event(event_id, event_data):
                    logger.debug(f"Event created successfully with ID: {event_id}")
                    self.clear_event_form()
                    self.show_success_message(f"Event created successfully!\nEvent ID: {event_id}")

                    # Set global variables
                    EventConfig.current_event_id = event_id
                    EventConfig.current_event_name = event_name
                    EventConfig.max_images = max_images
                    EventConfig.current_image_count = 0
                    EventConfig.storage_type = "Cloud"
                else:
                    logger.error("Failed to create event in database")
            else:
                logger.error("Failed to upload StartingGif")

        except Exception as e:
            logger.error(f"Error creating event: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())

    def clear_event_form(self):
        """Clear all form inputs"""
        self.event_name_entry.delete(0, tk.END)
        self.max_images_entry.delete(0, tk.END)
        self.max_images_entry.insert(0, "50")
        self.password_var.set(False)
        self.password_entry.delete(0, tk.END)
        self.storage_combo.set("Cloud Storage")

    def show_success_message(self, message):
        """Show a success message to the user"""
        success_window = tk.Toplevel(self)
        success_window.title("Success")
        
        # Position window in center of screen
        window_width = 300
        window_height = 100
        screen_width = success_window.winfo_screenwidth()
        screen_height = success_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        success_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        ttk.Label(
            success_window,
            text=message,
            font=("Helvetica", 12),
            wraplength=250
        ).pack(pady=20)
        
        ttk.Button(
            success_window,
            text="OK",
            command=success_window.destroy
        ).pack()

        # Auto-close after 3 seconds
        success_window.after(3000, success_window.destroy)

    def __del__(self):
        logger.debug("AdminPanel cleanup")
        # Remove the webcam cleanup from here since it's managed at the app level 

    def create_event_local(self):
        """Create a new event in local storage"""
        try:
            # Validate inputs
            event_name = self.event_name_entry.get().strip()
            if not event_name:
                logger.error("Event name is required")
                return False

            # Generate random 12-character event ID
            import string
            import random
            event_id = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

            event_data = {
                "event_id": event_id,
                "name": event_name,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                "password": self.password_entry.get() if self.password_var.get() else "0",
                "access_level": "Public" if not self.password_var.get() else "Private",
                "max_images": int(self.max_images_entry.get().strip()),
                "current_image_count": 0
            }

            # Create event directory using event ID instead of name
            local_event_dir = f"Assets/events/{event_id}"
            os.makedirs(local_event_dir, exist_ok=True)
            
            # Copy StartingGif to event directory
            starting_gif_path = "Assets/Components/StartingGif.gif"
            if os.path.exists(starting_gif_path):
                local_gif_path = f"{local_event_dir}/StartingGif.gif"
                shutil.copy2(starting_gif_path, local_gif_path)
                event_data["Images"] = {
                    "0": {
                        "type": "GIF",
                        "path": local_gif_path,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                    }
                }
            else:
                logger.error("StartingGif.gif not found")
                return False
            
            # Create event_info.json file
            info_file_path = f"{local_event_dir}/event_info.json"
            import json
            with open(info_file_path, 'w') as f:
                json.dump(event_data, f, indent=4)
            
            logger.debug(f"Created local event in: {local_event_dir}")
            self.clear_event_form()
            self.show_success_message(f"Event created successfully!\nEvent ID: {event_id}")

            # Set global variables
            EventConfig.current_event_id = event_id
            EventConfig.current_event_name = event_name
            EventConfig.max_images = int(self.max_images_entry.get().strip())
            EventConfig.current_image_count = 0
            EventConfig.storage_type = "Local"
            return True
        
        except Exception as e:
            logger.error(f"Error creating local event: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return False