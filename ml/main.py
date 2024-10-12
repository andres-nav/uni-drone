from ultralytics import YOLO
import torch
import cv2

# Define some constants
CONFIDENCE_THRESHOLD = 0.8
GREEN = (0, 255, 0)

cap = cv2.VideoCapture(
    "thetauvcsrc mode=4K ! queue! h264parse! nvv4l2decoder ! queue ! nvvidconv ! video/x-raw,format=BGRx ! queue ! videoconvert ! video/x-raw,format=BGR ! queue ! appsink"
)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# Load YOLOv8 model and move it to the GPU
model = YOLO("yolov8n.pt").to("cuda")  # Ensure the model runs on CUDA

while True:
    ret, frame = cap.read()

    # Check if frame is successfully read
    if not ret:
        print("Failed to grab frame")
        break

    # Resize the frame for faster inference
    frame = cv2.resize(frame, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)

    # Move the frame to the GPU for inference
    frame_gpu = torch.tensor(frame).to("cuda")  # Ensure the frame is on CUDA

    # Run the YOLO model on the frame (perform inference on the GPU)
    detections = model(frame_gpu)[0]

    for data in detections.boxes.data.tolist():
        # Extract the confidence associated with the detection
        confidence = data[4]

        # Filter out weak detections by ensuring the confidence is greater than the minimum
        if float(confidence) < CONFIDENCE_THRESHOLD:
            continue

        # Draw the bounding box on the frame if confidence is sufficient
        xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), GREEN, 2)

    # Display the frame with detections
    cv2.imshow("Input", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
