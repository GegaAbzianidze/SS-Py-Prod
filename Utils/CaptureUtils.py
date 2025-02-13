import cv2
from PIL import Image
import time
import os
import logging

logger = logging.getLogger(__name__)

class CaptureUtils:
    @staticmethod
    def capture_image(frame, filename):
        """Capture a single image from the provided frame"""
        if frame is not None:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            cv2.imwrite(filename, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            return True
        return False

    @staticmethod
    def capture_gif(webcam, duration, filename, fps=10):
        """Capture a GIF from the webcam"""
        frames = []
        start_time = time.time()
        frame_interval = 1.0 / fps
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Capture frames
        while time.time() - start_time < duration:
            frame = webcam.get_current_frame()
            if frame is not None:
                # Convert frame to PIL Image and resize if needed
                image = Image.fromarray(frame)
                if image.size != (640, 360):
                    image = image.resize((640, 360), Image.Resampling.LANCZOS)
                frames.append(image)
            time.sleep(frame_interval)
        
        if frames:
            try:
                # Save GIF with optimizations
                frames[0].save(
                    filename,
                    save_all=True,
                    append_images=frames[1:],
                    duration=int(1000 / fps),  # Duration per frame in ms
                    loop=0,
                    optimize=False,  # Disable optimization for better quality
                    quality=95  # Higher quality
                )
                return True
            except Exception as e:
                logger.error(f"Error saving GIF: {str(e)}")
                return False
        return False

    @staticmethod
    def capture_video(webcam, filename, duration=7, fps=30):
        """Capture a video from the webcam"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            frames = []
            start_time = time.time()
            frame_interval = 1.0 / fps
            
            # Capture frames
            while time.time() - start_time < duration:
                frame = webcam.get_current_frame()
                if frame is not None:
                    # Convert from RGB to BGR for OpenCV
                    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    frames.append(frame_bgr)
                time.sleep(frame_interval)

            if frames:
                # Get dimensions from the first frame
                height, width = frames[0].shape[:2]
                
                # Initialize video writer with proper codec
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
                
                try:
                    # Write frames
                    for frame in frames:
                        out.write(frame)
                    return True
                except Exception as e:
                    logger.error(f"Error writing video: {str(e)}")
                    return False
                finally:
                    # Always release the video writer
                    out.release()
            
            return False
            
        except Exception as e:
            logger.error(f"Error in video capture: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return False 