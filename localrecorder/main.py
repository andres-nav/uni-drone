import cv2

# Initialize the camera
video_capture = cv2.VideoCapture( "thetauvcsrc mode=4K ! queue! h264parse! nvv4l2decoder ! queue ! nvvidconv ! video/x-raw,format=BGRx ! queue ! videoconvert ! video/x-raw,format=BGR ! queue ! appsink")

# Set the video resolution to 4K (3840x2160)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

# Define the codec and create VideoWriter object
# 'XVID' for AVI or 'mp4v' for MP4.
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' for MP4
out = cv2.VideoWriter('output_4K.mp4', fourcc, 20.0, (3840, 2160))

while video_capture.isOpened():
    ret, frame = video_capture.read()
    if ret:
        # Write the frame into the file 'output_4K.mp4'
        out.write(frame)

        # Show the video in a window (optional, be aware 4K might strain the display)
        #cv2.imshow('4K Video Stream', frame)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything once the job is finished
video_capture.release()
out.release()
cv2.destroyAllWindows()
