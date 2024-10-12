import cv2
import subprocess
import threading
import time
from flask import Flask, Response

app = Flask(__name__)

# Initialize global variables for the video stream
video_capture = cv2.VideoCapture(
    "thetauvcsrc mode=4K ! queue! h264parse! nvv4l2decoder ! queue ! nvvidconv ! video/x-raw,format=BGRx ! queue ! videoconvert ! video/x-raw,format=BGR ! queue ! appsink"
)

if not video_capture.isOpened():
    raise IOError("Cannot open webcam")


frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(video_capture.get(cv2.CAP_PROP_FPS))
is_streaming = True

# FFmpeg command using CUDA NVENC for hardware-accelerated encoding
ffmpeg_cmd = [
    'ffmpeg',
    '-y',  # Overwrite output file if it exists
    '-f', 'rawvideo',
    '-pix_fmt', 'bgr24',  # Pixel format for OpenCV frames
    '-s', f'{frame_width}x{frame_height}',  # Input resolution
    '-r', str(fps),  # Input framerate
    '-i', '-',  # Input from stdin
    '-c:v', 'h264_nvenc',  # CUDA-based encoding using NVENC
    '-preset', 'fast',  # NVENC encoding preset
    '-f', 'mpegts',  # MPEG transport stream format
    '-'  # Output to stdout (pipe to Flask)
]

# Start FFmpeg process
ffmpeg_proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

# Flask route for HTTP streaming
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Frame generator function for the Flask stream
def generate_frames():
    global is_streaming

    while is_streaming:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        if not ret:
            break

        # Send the frame to the FFmpeg process via stdin
        ffmpeg_proc.stdin.write(frame.tobytes())

        # Capture the encoded frame from FFmpeg's stdout
        encoded_frame = ffmpeg_proc.stdout.read(frame_width * frame_height * 3 // 2)  # Adjust buffer size for encoded frame

        # Yield the encoded frame as HTTP multipart response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + encoded_frame + b'\r\n\r\n')

# Thread to stop the stream on keypress
def stop_stream():
    global is_streaming
    while True:
        if input("Press 'q' to stop streaming:\n").strip() == 'q':
            is_streaming = False
            break

# Start the Flask app
if __name__ == '__main__':
    threading.Thread(target=stop_stream).start()  # Start thread for stopping the stream
    app.run(host='0.0.0.0', port=5000, threaded=True)

    # Clean up resources
    video_capture.release()
    ffmpeg_proc.stdin.close()
    ffmpeg_proc.wait()