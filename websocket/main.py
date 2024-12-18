import cv2
import struct
import asyncio
import websockets

# Initialize the video capture object
cap = cv2.VideoCapture(
    "thetauvcsrc mode=4K ! queue! h264parse! nvv4l2decoder ! queue ! nvvidconv ! video/x-raw,format=BGRx ! queue ! videoconvert ! video/x-raw,format=BGR ! queue ! appsink"
)

if not cap.isOpened():
    exit("Error: Camera not accessible.")

async def video_stream(websocket, path):
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to read from camera.")
                break

            # Encode frame as JPEG
            success, buffer = cv2.imencode('.jpg', frame)
            if not success:
                print("Error: Frame encoding failed.")
                await asyncio.sleep(2)  # Wait before retrying to encode the frame
                continue

            # Prepare the message
            message = struct.pack("Q", len(buffer)) + buffer.tobytes()

            while True:  # Retry loop for sending messages
                try:
                    # Check if the WebSocket is open before sending
                    if websocket.open:
                        await websocket.send(message)
                        break  # Exit the retry loop on success
                    else:
                        print("WebSocket connection is not open. Skipping frame.")
                        break  # Exit if the connection is not open
                except Exception as e:
                    print(f"Error sending data: {e}. Retrying...")
                    await asyncio.sleep(1)  # Wait before retrying to send data

            await asyncio.sleep(0.01)  # Small delay to avoid overwhelming the client

    except Exception as e:
        print(f"An error occurred in the video stream: {e}")
    finally:
        # Release the video capture and ensure the WebSocket connection is closed
        cap.release()
        print("Released video capture and closing connection.")

# Start the WebSocket server
start_server = websockets.serve(video_stream, '0.0.0.0', 9999)

# Start the event loop
try:
    asyncio.get_event_loop().run_until_complete(start_server)
    print("WebSocket server started on ws://0.0.0.0:9999")
    asyncio.get_event_loop().run_forever()
except Exception as e:
    print(f"Error starting server: {e}")