from flask import Flask, Response
import cv2

app = Flask(__name__)

# Initialize the camera
video_capture = cv2.VideoCapture( "thetauvcsrc mode=4K ! queue! h264parse! nvv4l2decoder ! queue ! nvvidconv ! video/x-raw,format=BGRx ! queue ! videoconvert ! video/x-raw,format=BGR ! queue ! appsink")

# Set the video resolution to 4K (3840x2160)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

# Define the codec and create VideoWriter object to save the stream
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 'mp4v' for MP4
out = cv2.VideoWriter('output_4K.mp4', fourcc, 20.0, (3840, 2160))

def generate_frames():
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        else:
            # Save the frame to the video file
            out.write(frame)

            # Encode the frame as JPEG for streaming
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame in byte format as multipart
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    # Route for video feed, which returns frames generated by generate_frames function
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    # Run the Flask app (host='0.0.0.0' makes it accessible over the network)
    app.run(host='0.0.0.0', port=9999, debug=True)

# Release resources when the app is stopped
video_capture.release()
out.release()