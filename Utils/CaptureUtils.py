import cv2
from PIL import Image
import time
import os

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

        while time.time() - start_time < duration:
            frame = webcam.get_current_frame()
            if frame is not None:
                frames.append(Image.fromarray(frame))
            time.sleep(frame_interval)

        if frames:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            frames[0].save(
                filename,
                save_all=True,
                append_images=frames[1:],
                duration=int(1000 / fps),  # Duration per frame in ms
                loop=0,
                optimize=True
            )
            return True
        return False

    @staticmethod
    def capture_video(webcam, filename, duration=7, fps=30):
        """Capture a video from the webcam"""
        frames = []
        start_time = time.time()
        frame_interval = 1.0 / fps

        while time.time() - start_time < duration:
            frame = webcam.get_current_frame()
            if frame is not None:
                frames.append(frame)
            time.sleep(frame_interval)

        if frames:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            out = cv2.VideoWriter(
                filename,
                cv2.VideoWriter_fourcc(*'mp4v'),
                fps,
                frames[0].shape[:2][::-1]
            )
            
            for frame in frames:
                out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            out.release()
            return True
        return False 