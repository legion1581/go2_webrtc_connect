"""
Robot Control Script for WebRTC and Marker Detection
Based on: https://github.com/legion1581/go2_webrtc_connect

Author: Marco Dittmann  
Date: 4.12.24  

Description:  
This script uses the Dog class to control the movement of a robotic dog and utilizes its camera feed to search for and detect ArUco markers.
The robot's behavior dynamically adapts based on marker detection, allowing it to perform various actions, such as moving, sitting, and standing.  
The script integrates OpenCV for video processing, asyncio for asynchronous communication, and WebRTC for establishing a connection with the robot.
It processes video frames in real-time to detect markers and triggers appropriate actions based on the detection state.  

Features:  
- Real-time video streaming and marker detection with OpenCV and ArUco.  
- Robot movement control (e.g., move, sit, stand) using the Dog class.  
- Asynchronous communication with the robot via WebRTC.  
- Integration with threading for smooth operation.  

Note:  
- Ensure the robot's IP address is correctly set in the IP_ADDRESS constant.  
- Install all dependencies, including OpenCV, asyncio, and aiortc.  
"""

import asyncio
import cv2
import numpy as np
import logging
import threading
import time
from queue import Queue
from dog import Dog, ControlMode
from go2_webrtc_driver.webrtc_driver import Go2WebRTCConnection, WebRTCConnectionMethod
from aiortc import MediaStreamTrack

# Create an OpenCV window and display a blank image
height, width = 720, 1280  # Adjust the size as needed
img = np.zeros((height, width, 3), dtype=np.uint8)
cv2.imshow('Video', img)
cv2.waitKey(1)  # Ensure the window is created

# Constants 
IP_ADDRESS = "192.168.4.219"

# Enable logging for debugging
logging.basicConfig(level=logging.WARN)

dog = Dog(IP_ADDRESS)

def main():
    global dog
    frame_queue = Queue()

    # Choose a connection method
    dog.conn = Go2WebRTCConnection(WebRTCConnectionMethod.LocalSTA, ip=dog.ip_address)

    # Async function to receive video frames and put them in the queue
    async def recv_camera_stream(track: MediaStreamTrack):
        while True:
            frame = await track.recv()
            # Convert the frame to a NumPy array
            img = frame.to_ndarray(format="bgr24")
            frame_queue.put(img)

    def run_asyncio_loop(loop):
        asyncio.set_event_loop(loop)
        async def setup():
            try:
                # Connect to the device
                await dog.conn.connect()

                # Switch video channel on and start receiving video frames
                dog.conn.video.switchVideoChannel(True)

                # Add callback to handle received video frames
                dog.conn.video.add_track_callback(recv_camera_stream)

                logging.info("Performing 'StandUp' movement...")
                dog.balance_stand()
            except Exception as e:
                logging.error(f"Error in WebRTC connection: {e}")

        # Run the setup coroutine and then start the event loop
        loop.run_until_complete(setup())
        loop.run_forever()

    # Create a new event loop for the asyncio code
    loop = asyncio.new_event_loop()

    # Start the asyncio event loop in a separate thread
    asyncio_thread = threading.Thread(target=run_asyncio_loop, args=(loop,))
    asyncio_thread.start()

    try:
        while True:
            if not frame_queue.empty():
                img = frame_queue.get()

                # Display the frame 
                cv2.imshow('Video', img)
                key_input = cv2.waitKey(1)

                if key_input == 9:  # Tab-Key
                    dog.toggle_mode()
                elif dog.mode is ControlMode.MODE_MANUAL.value:
                    dog.process_key(key_input, loop)

            else:
                # Sleep briefly to prevent high CPU usage
                time.sleep(0.01)
    finally:
        cv2.destroyAllWindows()
        # Stop the asyncio event loop
        loop.call_soon_threadsafe(loop.stop)
        asyncio_thread.join()

if __name__ == "__main__":
    main()

