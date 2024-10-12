import cv2
import subprocess


cap = cv2.VideoCapture(
    "thetauvcsrc mode=4K ! queue! h264parse! nvv4l2decoder ! queue ! nvvidconv ! video/x-raw,format=BGRx ! queue ! videoconvert ! video/x-raw,format=BGR ! queue ! appsink"
)

if not cap.isOpened():
    raise IOError("Cannot open webcam")

# GStreamer pipeline for streaming video over RTSP
gst_str = (
    'appsrc ! videoconvert ! x264enc speed-preset=ultrafast tune=zerolatency ! rtph264pay ! '
    'udpsink host=0.0.0.0 port=9999'
)

# Start GStreamer pipeline with subprocess
gst_pipe = subprocess.Popen(['gst-launch-1.0', gst_str], stdin=subprocess.PIPE)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Write the frame to the GStreamer pipeline
    gst_pipe.stdin.write(frame.tobytes())

    # Show the video stream locally (optional)
    #cv2.imshow('Video Stream', frame)



# Release resources
cap.release()
gst_pipe.terminate()
cv2.destroyAllWindows()