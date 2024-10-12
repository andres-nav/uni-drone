from ultralytics import YOLO
import cv2

# define some constants
CONFIDENCE_THRESHOLD = 0.8
GREEN = (0, 255, 0)

cap = cv2.VideoCapture(
    "thetauvcsrc mode=4K ! queue! h264parse! nvv4l2decoder ! queue ! nvvidconv ! video/x-raw,format=BGRx ! queue ! videoconvert ! video/x-raw,format=BGR ! queue ! appsink"
)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")


model = YOLO("yolov8n.pt")


while True:
    ret, frame = cap.read()

    # Check if frame is successfully read
    if not ret:
        print("Failed to grab frame")
        break

    frame = cv2.resize(frame, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)

    # run the YOLO model on the frame
    detections = model(frame)[0]

    for data in detections.boxes.data.tolist():
        # extract the confidence (i.e., probability) associated with the detection
        confidence = data[4]

        # filter out weak detections by ensuring the
        # confidence is greater than the minimum confidence
        if float(confidence) < CONFIDENCE_THRESHOLD:
            continue

        # if the confidence is greater than the minimum confidence,
        # draw the bounding box on the frame
        xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), GREEN, 2)

    cv2.imshow("Input", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
