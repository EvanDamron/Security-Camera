import cv2
from flask import Flask, Response

app = Flask(__name__)


def generate_frames(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Encode the frame as a JPEG image
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        # Convert the buffer to bytes and use it to form a response
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(rtsp_url='rtsp://ewdamron:Banana123@192.168.5.224:554/stream1'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
