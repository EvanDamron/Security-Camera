# functions that can be merged once facial recognition works.

import cv2
from Save import Save  # Import the Save class

# Initialize the Save class
saver = Save()

# RTSP stream URL
rtsp_url = 'rtsp://ewdamron:Banana123@192.168.5.224:554/stream1'

def capture_and_save_video(rtsp_url, fps=30, duration=None):
    """
    Captures video from an RTSP stream and saves it as an mp4 file.

    Parameters:
    - rtsp_url: str, the RTSP URL for the video stream.
    - fps: int, frames per second for saving the video.
    - duration: int or None, duration in seconds to capture video; if None, capture indefinitely.
    """
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    print("Success: Opened video.")
    frames = []
    start_time = cv2.getTickCount() / cv2.getTickFrequency()  # Get initial time for duration

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Display the frame
        cv2.imshow('RTSP stream', frame)

        # Append frame to the video frames list
        frames.append(frame)

        # Check for 'q' key press to stop recording
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Check duration, if specified
        if duration:
            current_time = cv2.getTickCount() / cv2.getTickFrequency()
            if (current_time - start_time) >= duration:
                break

    # Save the captured video
    saver.save_video(frames, fps=fps)

    cap.release()
    cv2.destroyAllWindows()

def capture_and_save_image(rtsp_url):
    """
    Captures an image from an RTSP stream and saves it as a jpg file.

    Parameters:
    - rtsp_url: str, the RTSP URL for the video stream.
    """
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    print("Success: Opened video.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Display the frame
        cv2.imshow('RTSP stream', frame)

        # Capture and save an image when 's' is pressed
        if cv2.waitKey(1) & 0xFF == ord('s'):
            saver.save_image(frame)
            print("Image captured and saved.")

        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Example calls
# Capture and save a 10-second video
capture_and_save_video(rtsp_url, fps=30, duration=10)

# Capture and save an image
capture_and_save_image(rtsp_url)
