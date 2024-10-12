import cv2

# Initialize the camera
cap = cv2.VideoCapture(
     "thetauvcsrc mode=4K ! queue! h264parse! nvv4l2decoder ! queue ! nvvidconv ! video/x-raw,format=BGRx ! queue ! videoconvert ! video/x-raw,format=BGR ! queue ! appsink"
     )

# Set the video resolution to 4K (3840x2160)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object to save the stream
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 'mp4v' for MP4
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (width, height))

while cap.isOpened():
    ret, frame = cap.read()
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
cap.release()
out.release()
cv2.destroyAllWindows()
