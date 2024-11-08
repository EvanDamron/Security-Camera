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
import cv2
import face_recognition
import os

# Open the RTSP stream (replace with your RTSP URL)
rtsp_url = 'rtsp://ewdamron:Banana123@192.168.5.224:554/stream1'
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("Error: Unable to open the camera stream")
else:
    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            if not ret:
                print("Error: Unable to retrieve frame from stream")
                break

            # Resize frame to reduce memory usage
            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

            # Convert the frame from BGR (OpenCV format) to RGB (face_recognition format)
            rgb_frame = small_frame[:, :, ::-1]

            # Find all face locations in the current frame
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            print(f"Detected {len(face_locations)} face(s) in the frame.")

            # Draw a box around each face
            for face_location in face_locations:
                (top, right, bottom, left) = face_location
                # Scale back up the face location since the frame was resized
                top *= 2
                right *= 2
                bottom *= 2
                left *= 2
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Display the resulting frame
            cv2.imshow('Face Detection', frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print(f"An error occurred: {e}")

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
