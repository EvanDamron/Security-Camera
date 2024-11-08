# import cv2
# import face_recognition
# import os
#
# # Load known faces and their encodings
# known_face_encodings = []
# known_face_names = []
#
# # Path to folder with images of known people
# known_faces_dir = 'known_faces'
#
# # Load each person's image and learn how to recognize it
# for filename in os.listdir(known_faces_dir):
#     if filename.endswith(('.jpg', '.jpeg', '.png')):
#         image = face_recognition.load_image_file(f"{known_faces_dir}/{filename}")
#         encoding = face_recognition.face_encodings(image)[0]
#         known_face_encodings.append(encoding)
#         known_face_names.append(os.path.splitext(filename)[0])  # Use filename as person's name
#
# # Open the RTSP stream (replace with your RTSP URL)
# rtsp_url = 'rtsp://ewdamron:Banana123@192.168.5.224:554/stream1'
# cap = cv2.VideoCapture(rtsp_url)
#
# if not cap.isOpened():
#     print("Error: Unable to open the camera stream")
# else:
#     while True:
#         # Capture frame-by-frame
#         ret, frame = cap.read()
#
#         if not ret:
#             print("Error: Unable to retrieve frame from stream")
#             break
#
#         # Convert the frame from BGR (OpenCV format) to RGB (face_recognition format)
#         rgb_frame = frame[:, :, ::-1]
#
#         # Find all face locations and face encodings in the current frame
#         face_locations = face_recognition.face_locations(rgb_frame)
#         face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
#
#         # Loop over each detected face
#         for face_encoding, face_location in zip(face_encodings, face_locations):
#             # See if the face matches any of the known faces
#             matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
#             name = "Unknown"
#
#             # Find the known face with the smallest distance to the new face
#             face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
#             best_match_index = face_distances.argmin()
#             if matches[best_match_index]:
#                 name = known_face_names[best_match_index]
#
#             # Draw a box around the face
#             (top, right, bottom, left) = face_location
#             cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
#
#             # Label the face with the name
#             cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
#
#         # Display the resulting frame
#         cv2.imshow('Face Recognition', frame)
#
#         # Break the loop if 'q' is pressed
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
# # Release the capture and close windows
# cap.release()
# cv2.destroyAllWindows()



#
# import cv2
# import face_recognition
# import os
#
# # Open the RTSP stream (replace with your RTSP URL)
# rtsp_url = 'rtsp://ewdamron:Banana123@192.168.5.224:554/stream1'
# cap = cv2.VideoCapture(rtsp_url)
#
# if not cap.isOpened():
#     print("Error: Unable to open the camera stream")
# else:
#     try:
#         while True:
#             # Capture frame-by-frame
#             ret, frame = cap.read()
#
#             if not ret:
#                 print("Error: Unable to retrieve frame from stream")
#                 break
#
#             # Resize frame to reduce memory usage
#             small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
#
#             # Convert the frame from BGR (OpenCV format) to RGB (face_recognition format)
#             rgb_frame = small_frame[:, :, ::-1]
#
#             # Find all face locations in the current frame
#             face_locations = face_recognition.face_locations(rgb_frame)
#             face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
#
#             print(f"Detected {len(face_locations)} face(s) in the frame.")
#
#             # Draw a box around each face
#             for face_location in face_locations:
#                 (top, right, bottom, left) = face_location
#                 # Scale back up the face location since the frame was resized
#                 top *= 2
#                 right *= 2
#                 bottom *= 2
#                 left *= 2
#                 cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
#
#             # Display the resulting frame
#             cv2.imshow('Face Detection', frame)
#
#             # Break the loop if 'q' is pressed
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#     except Exception as e:
#         print(f"An error occurred: {e}")
#
# # Release the capture and close windows
# cap.release()
# cv2.destroyAllWindows()


import face_recognition
import cv2
import numpy as np

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
rtsp_url = 'rtsp://ewdamron:Banana123@192.168.5.224:554/stream1'
cap = cv2.VideoCapture(rtsp_url)

# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding
]
known_face_names = [
    "Barack Obama",
    "Joe Biden"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Only process every other frame of video to save time
    if process_this_frame:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

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

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
