import cv2
import os
from datetime import datetime

class Save:
    def __init__(self, save_dir="captures"):
        self.save_directory = save_dir
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)

    def generate_filename(self, media_type, extension):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{media_type}_{timestamp}_{extension}"
        return os.path.join(self.save_directory, filename)

    def save_image(self, image):
        path = self.generate_filename(media_type="image", extension="jpg")
        cv2.imwrite(path, image)
        print(f"Image saved to {path}")

    def save_video(self, frames, fps=30):
        if not frames:
            raise ValueError("No Frames")

        path = self.generate_filename(media_type="video", extension="mp4")
        height, width, _ = frames[0].shape
        out = cv2.VideoWriter(path, 0, fps, (width, height))

        for frame in frames:
            out.write(frame)

        out.release()
        print(f"Video save in {path}")
