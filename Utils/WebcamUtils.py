import cv2
import threading
import tkinter as tk
from PIL import Image, ImageTk
import time

class WebcamUtils:
    """
    A class to handle webcam preview functionality with improved performance and resource management.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        # Singleton pattern to prevent multiple webcam instances
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(WebcamUtils, cls).__new__(cls)
            return cls._instance

    def __init__(self, preview_size=(960, 540)):
        # Initialize only once
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.preview_size = preview_size
            self.cam = None
            self.frame = None
            self.image = None
            self.running = False
            self._frame_lock = threading.Lock()
            self._preview_thread = None

    def initialize_camera(self):
        """Initialize the camera with proper settings"""
        if self.cam is None:
            self.cam = cv2.VideoCapture(cv2.CAP_DSHOW)
            self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            self.cam.set(cv2.CAP_PROP_FPS, 30)
            
            if not self.cam.isOpened():
                raise RuntimeError("Failed to open camera")

    def start_preview(self, label):
        """Start the webcam preview"""
        if not self.running:
            try:
                self.initialize_camera()
                self.running = True
                self._preview_thread = threading.Thread(
                    target=self._update_preview,
                    args=(label,),
                    daemon=True
                )
                self._preview_thread.start()
            except Exception as e:
                self.running = False
                raise RuntimeError(f"Failed to start preview: {str(e)}")

    def _update_preview(self, label):
        """Update the preview frame"""
        while self.running:
            try:
                ret, frame = self.cam.read()
                if ret:
                    with self._frame_lock:
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        frame = cv2.resize(frame, self.preview_size)
                        self.frame = frame
                        self.image = ImageTk.PhotoImage(Image.fromarray(frame))
                        
                    label.config(image=self.image)
                    label.image = self.image
                    
                    time.sleep(0.033)  # ~30 FPS
            except Exception as e:
                print(f"Preview update error: {str(e)}")
                break

    def get_current_frame(self):
        """Get the current frame safely"""
        with self._frame_lock:
            return self.frame.copy() if self.frame is not None else None

    def stop_preview(self):
        """Stop the preview and release resources"""
        self.running = False
        if self._preview_thread:
            self._preview_thread.join(timeout=1.0)
        if self.cam:
            self.cam.release()
            self.cam = None

    def __del__(self):
        """Ensure resources are properly released"""
        self.stop_preview()

class WebcamCapture:
    def __init__(self):
        self.cap = None
        self.is_capturing = False
        self.current_frame = None
        self.capture_thread = None
        self.frame_lock = threading.Lock()

    def start_capture(self, camera_index=0):
        """Start capturing from webcam"""
        if self.cap is None:
            self.cap = cv2.VideoCapture(camera_index)
            if not self.cap.isOpened():
                raise ValueError(f"Failed to open camera {camera_index}")
            
            # Set resolution (adjust as needed)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            
        self.is_capturing = True
        self.capture_thread = threading.Thread(target=self._capture_loop)
        self.capture_thread.daemon = True
        self.capture_thread.start()

    def stop_capture(self):
        """Stop capturing from webcam"""
        self.is_capturing = False
        if self.capture_thread:
            self.capture_thread.join()
        if self.cap:
            self.cap.release()
            self.cap = None

    def _capture_loop(self):
        """Main capture loop"""
        while self.is_capturing:
            ret, frame = self.cap.read()
            if ret:
                with self.frame_lock:
                    self.current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            time.sleep(0.03)  # ~30 FPS

    def get_frame(self):
        """Get the current frame"""
        with self.frame_lock:
            if self.current_frame is not None:
                return self.current_frame.copy()
        return None

    def capture_photo(self):
        """Capture a single photo"""
        frame = self.get_frame()
        if frame is not None:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"capture_{timestamp}.jpg"
            cv2.imwrite(filename, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            return filename
        return None

class WebcamWidget(tk.Frame):
    def __init__(self, parent, size=(640, 480)):
        super().__init__(parent)
        self.size = size
        
        # Create webcam capture instance
        self.webcam = WebcamCapture()
        
        # Create canvas for displaying webcam feed
        self.canvas = tk.Canvas(self, width=size[0], height=size[1])
        self.canvas.pack()
        
        # Initialize variables
        self.update_id = None
        self.current_image = None

    def start(self):
        """Start displaying webcam feed"""
        try:
            self.webcam.start_capture()
            self._update_frame()
        except ValueError as e:
            print(f"Error starting webcam: {e}")

    def stop(self):
        """Stop displaying webcam feed"""
        if self.update_id:
            self.after_cancel(self.update_id)
            self.update_id = None
        self.webcam.stop_capture()

    def _update_frame(self):
        """Update the frame displayed in the widget"""
        frame = self.webcam.get_frame()
        if frame is not None:
            # Convert frame to PhotoImage
            image = Image.fromarray(frame)
            image = image.resize(self.size, Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image=image)
            
            # Update canvas
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            self.current_image = photo  # Keep a reference
        
        self.update_id = self.after(30, self._update_frame)  # Update every 30ms (~30 FPS)

    def capture_photo(self):
        """Capture and save a photo"""
        return self.webcam.capture_photo()

    def destroy(self):
        """Clean up resources"""
        self.stop()
        super().destroy() 