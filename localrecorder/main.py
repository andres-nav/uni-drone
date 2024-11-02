import cv2

# Define the GStreamer pipeline to capture video from the camera
# Modify mode and other settings as needed
capture_pipeline = (
    "thetauvcsrc mode=4K ! queue ! h264parse ! nvv4l2decoder ! queue ! "
    "nvvidconv ! video/x-raw,format=BGRx ! queue ! videoconvert ! "
    "video/x-raw,format=BGR ! appsink"
)

# Open the video capture
video_capture = cv2.VideoCapture(capture_pipeline, cv2.CAP_GSTREAMER)
frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(video_capture.get(cv2.CAP_PROP_FPS))


# Define the GStreamer pipeline for output with H.264 hardware encoding
output_file = "output_4K_hardware_encoded.mp4"
save_pipeline = (
    f"appsrc ! videoconvert ! video/x-raw,format=I420 ! "
    f"nvv4l2h264enc bitrate=8000000 ! h264parse ! "
    f"qtmux ! filesink location={output_file}"
)

# Initialize VideoWriter with the GStreamer save pipeline
out = cv2.VideoWriter(save_pipeline, cv2.CAP_GSTREAMER, 0, fps, (frame_width, frame_height))

# Check if the video capture and writer were initialized successfully
if not video_capture.isOpened():
    print("Error: Cannot open video stream.")
    exit()
if not out.isOpened():
    print("Error: Cannot open video writer.")
    video_capture.release()
    exit()

print("Recording 4K video with hardware-accelerated encoding... Press 'q' to stop.")

# Capture and write frames to output file
while video_capture.isOpened():
    ret, frame = video_capture.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Write the frame to the output file
    out.write(frame)

    # Display the frame (optional)
    #cv2.imshow("4K Video Stream", frame)


# Release resources
video_capture.release()
out.release()
cv2.destroyAllWindows()