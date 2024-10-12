import cv2
import subprocess

# Initialize the camera
cap = cv2.VideoCapture(
     "thetauvcsrc mode=4K ! queue! h264parse! nvv4l2decoder ! queue ! nvvidconv ! video/x-raw,format=BGRx ! queue ! videoconvert ! video/x-raw,format=BGR ! queue ! appsink"
     )


if not cap.isOpened():
    raise IOError("Cannot open webcam")



# Get video properties (resolution, frame rate)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Output video file path
output_file = 'output_cuda.mp4'

# FFmpeg command for local recording with CUDA NVENC (H.264 encoding)
ffmpeg_cmd = [
    'ffmpeg',
    '-y',  # Overwrite the output file if it exists
    '-f', 'rawvideo',  # Input format (raw frames)
    '-pix_fmt', 'bgr24',  # Pixel format used by OpenCV (24-bit BGR)
    '-s', f'{frame_width}x{frame_height}',  # Input resolution
    '-r', str(fps),  # Input framerate
    '-i', '-',  # Input from stdin (piped from OpenCV)
    '-c:v', 'hevc_nvenc',  # Use NVIDIA NVENC for H.265 encoding
    '-preset', 'fast',  # Encoding preset (options: slow, medium, fast)
    '-b:v', '5M',  # Set video bitrate (adjust as needed)
    '-maxrate', '5M',  # Set max video bitrate
    '-bufsize', '10M',  # Buffer size for rate control
    output_file  # Output file
]

# Start FFmpeg process
ffmpeg_proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

# Capture and write frames to FFmpeg
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Write the frame to FFmpeg's stdin
    ffmpeg_proc.stdin.write(frame.tobytes())

    # Display the frame locally (optional)
    cv2.imshow('Video Recording with CUDA', frame)


# Release resources
cap.release()
ffmpeg_proc.stdin.close()
ffmpeg_proc.wait()
cv2.destroyAllWindows()