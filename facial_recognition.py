import face_recognition
import cv2
import numpy as np
import os
from send import send_email
from PIL import Image
from save import Save


# Function to load multiple images and create encodings for a person
def load_face_encodings(image_folder, resize_to=(800, 600)):
    face_encodings = []
    for image_file in os.listdir(image_folder):
        image_path = os.path.join(image_folder, image_file)
        try:
            # Open the image using PIL
            with Image.open(image_path) as img:
                # Resize the image
                # img = img.resize(resize_to)
                # Convert to a format suitable for face_recognition
                img_array = np.array(img)

            # Detect and encode the face
            encoding = face_recognition.face_encodings(img_array)[0]
            face_encodings.append(encoding)
        except IndexError:
            print(f"Face not detected in image: {image_file}")
        except Exception as e:
            print(f"Error processing image {image_file}: {e}")
    return face_encodings

def get_most_recent_file(directory, extension="jpg"):
    # List all files in the directory with the specified extension
    files = [f for f in os.listdir(directory) if f.endswith(f".{extension}")]
    if not files:
        raise FileNotFoundError(f"No files with extension '{extension}' found in {directory}")

    # Get the full paths of the files
    full_paths = [os.path.join(directory, f) for f in files]

    # Sort files by their modification time, newest first
    most_recent_file = max(full_paths, key=os.path.getmtime)
    return most_recent_file

if __name__ == "__main__":

    # image = cv2.imread("Evan/IMG_2704.JPG")
    # cv2.imshow("Loaded Image", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    saver = Save()

    # Get a reference to webcam #0 (the default one)
    rtsp_url = 'rtsp://ewdamron:Banana123@192.168.5.224:554/stream1'
    video_capture = cv2.VideoCapture(rtsp_url)

    known_face_encodings = []
    known_face_names = []

    # Load all images for Evan
    evan_encodings = load_face_encodings("Evan")
    known_face_encodings.extend(evan_encodings)
    known_face_names.extend(["Evan"] * len(evan_encodings))
    # print(known_face_encodings)
    # exit()

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    sent = False
    unknown_frames = []    # Store frames with unknown faces for video saving

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Only process every other frame of video to save time
        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            assert rgb_small_frame.dtype == np.uint8, "Image must be of type uint8"
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            if face_locations:
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            else:
                face_encodings = []

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

                # Check if the face is unknown
                if name == "Unknown":
                    # Save the current frame for video saving
                    unknown_frames.append(frame)

                    # Save an image immediately
                    saver.save_image(frame)

                    # Send an email with the most recent photo in captures folder
                    if not sent:
                        path = get_most_recent_file("captures")
                        send_email(path, "evandamron14@gmail.com")
                        sent = True

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Save the video with unknown faces
    # if unknown_frames:
    #     saver.save_video(unknown_frames)

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
