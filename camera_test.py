import cv2

rtsp_url = 'rtsp://ewdamron:Banana123@192.168.5.224:554/stream1'
cap = cv2.VideoCapture(rtsp_url)
if not cap.isOpened():
    print("Error: Could not open video.")
else:
    print("Success: Opened video.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        cv2.imshow('RTSP stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
