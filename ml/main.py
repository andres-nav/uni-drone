import cv2

cap = cv2.VideoCapture(
    "thetauvcsrc \
    ! nvv4l2decoder \
    ! queue \
    ! videoconvert n-threads=0 \
    ! video/x-raw,format=BGR \
    ! queue \
    ! appsink"
)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")


while True:
    ret, frame = cap.read()

    # Check if frame is successfully read
    if not ret:
        print("Failed to grab frame")
        break

    frame = cv2.resize(frame, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)

    cv2.imshow("Input", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
