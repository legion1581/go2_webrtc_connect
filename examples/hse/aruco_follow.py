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
from cv2 import aruco
import numpy as np
from numpy import atan2, pi
from dog import Dog, ControlMode

# Create an OpenCV window and display a blank image
height, width = 720, 1280  # Adjust the size as needed
img = np.zeros((height, width, 3), dtype=np.uint8)
cv2.imshow('Video', img)
cv2.waitKey(1)  # Ensure the window is created

import logging
import threading
import time
import yaml
from os import path
from queue import Queue
from go2_webrtc_driver.webrtc_driver import Go2WebRTCConnection, WebRTCConnectionMethod
from go2_webrtc_driver.constants import VUI_COLOR
from aiortc import MediaStreamTrack



# Constants 
DEG2RAD = pi/180.0
RAD2DEG = 180.0/pi

# Enable logging for debugging
logging.basicConfig(level=logging.WARN)

MARKER_ID = 0
IP_ADDRESS = "192.168.4.202"
CAMERA_CALIBRATION_DATA = "ost.yaml"
V_MAX = 1.0         # Maximum translational velocity (m/s)
V_MIN = 0.25        # Maximum translational velocity (m/s)
W_MAX = 0.5         # Maximum rotational velocity (rad/s)
DIST_MIN = 0.4      # Distance and which robots starts to back off from ArUco
DIST_FOLLOW = 1.0   # Minimum distance at which the dog starts to follow the ArUco
DIST_ACC_MAX = 3.5  # Distance to ArUco where V_MAX is reached 
PHI_MAX = 0.2618    # Max angle at which the dog starts to center the ArUco


def map(x, in_min, in_max, out_min, out_max):
    return out_min + (x - in_min)/(in_max - in_min) * (out_max - out_min)

def constrain(x, min, max):
    return min if x < min else (max if x > max else x) 

def load_camera_parameters(yaml_file):
    # Default values in case the file does not exist
    camera_matrix = np.eye(3, dtype=np.float32)
    dist_coeffs = np.ones(5, dtype=np.float32)

    try:    
        with open(yaml_file, 'r') as file:
            data = yaml.safe_load(file)
    
        # Extract camera matrix
        camera_matrix = np.array(data['camera_matrix']['data']).reshape(3, 3)
        
        # Extract distortion coefficients
        dist_coeffs = np.array(data['distortion_coefficients']['data'])
    except FileNotFoundError:
        print("ERROR - File not found: " + yaml_file)
        print("The camera matrix will be set to the unity matrix.\n \
              The distortion coefficients will be set to a vector of ones.")

    return camera_matrix, dist_coeffs

def my_estimatePoseSingleMarkers(corners, marker_size, mtx, distortion):
    '''
    This will estimate the rvec and tvec for each of the marker corners detected by:
       corners, ids, rejectedImgPoints = detector.detectMarkers(image)
    corners - is an array of detected corners for each detected marker in the image
    marker_size - is the size of the detected markers
    mtx - is the camera matrix
    distortion - is the camera distortion matrix
    RETURN list of rvecs, tvecs, and trash (so that it corresponds to the old estimatePoseSingleMarkers())
    '''
    marker_points = np.array([[-marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, -marker_size / 2, 0],
                              [-marker_size / 2, -marker_size / 2, 0]], dtype=np.float32)
    trash = []
    rvecs = []
    tvecs = []
    for c in corners:
        nada, R, t = cv2.solvePnP(marker_points, c, mtx, distortion, False, cv2.SOLVEPNP_ITERATIVE)
        rvecs.append(R)
        tvecs.append(t)
        trash.append(nada)
    return rvecs, tvecs, trash


dog = Dog(IP_ADDRESS)


def main():
    global dog
    frame_queue = Queue()

    # Read camera parameters from YAML file
    camera_matrix, dist_coeffs = load_camera_parameters(CAMERA_CALIBRATION_DATA)
    dog.set_camera_parameters(camera_matrix, dist_coeffs)

    aruco_dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    detector_parameters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(aruco_dictionary, detector_parameters)
    marker_size = 0.15 # 150 mm

    # Choose a connection method (uncomment the correct one)
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
        corners = None
        rvecs = None
        tvecs = None
        aruco_x, aruco_y, aruco_z = None, None, None
        phi, phi_deg = None, None
        while True:
            if not frame_queue.empty():
                img = frame_queue.get()
                img_greyscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                corners, ids, rejected = detector.detectMarkers(img_greyscale)
                if ids is not None:
                    aruco.drawDetectedMarkers(img, corners, ids)
                    if any(id == 0 for id in ids):
                        dog.marker_detected = True
                        dog.search_active = False
                        dog.last_detection_timestamp = time.time()
                        asyncio.run_coroutine_threadsafe(dog.set_vui(VUI_COLOR.GREEN), loop)

                        # Perform pose estimation here
                        rvecs, tvecs, trash = my_estimatePoseSingleMarkers(corners, marker_size, dog.camera_matrix, dog.dist_coeffs)
                        aruco_x = tvecs[0][0][0]
                        aruco_y = tvecs[0][1][0]
                        aruco_z = tvecs[0][2][0]

                        phi = atan2(aruco_x, aruco_z) # horizontal angle to ArUco

                    else:
                        dog.marker_detected = False
                        asyncio.run_coroutine_threadsafe(dog.set_vui(VUI_COLOR.BLUE), loop)
                    
                # Write pose data as text into the image
                text = ""
                text_phi = ""
                if dog.marker_detected and aruco_z is not None:
                    text = f"Position: ({aruco_x:.3f}, {aruco_y:.3f}, {aruco_z:.3f})"
                    phi_deg = phi * RAD2DEG # angle in degrees
                    text_phi =  f"phi: {phi_deg:.1f} deg"
                else:
                    text = "Position: unknown"
                    text_phi = "phi: unknown"
                thickness = 2
                scale = 0.85
                font = cv2.FONT_HERSHEY_SIMPLEX
                
                # Adaptive text color
                brightness = np.mean(img_greyscale[-50, :]) # 0 - 255
                c = 255 - brightness

                color = (c, c, c)

                origin = (10, img.shape[0] - 11)
                cv2.putText(img, text, origin, font, scale, color, thickness, cv2.LINE_AA)
                text = "Mode: " + dog.mode[len("MODE_"):]
                origin = (10, img.shape[0] - 51)
                cv2.putText(img, text, origin, font, scale, color, thickness, cv2.LINE_AA)
                origin = (img.shape[1] - 251, img.shape[0] - 11)
                cv2.putText(img, text_phi, origin, font, scale, color, thickness, cv2.LINE_AA)

                # Display the frame 
                cv2.imshow('Video', img)
                key_input = cv2.waitKey(1)

                if key_input == 9: # Tab-Key
                    dog.toggle_mode()

                elif dog.mode is ControlMode.MODE_MANUAL.value:
                    dog.process_key(key_input, loop)
                elif dog.mode is ControlMode.MODE_AUTO.value:
                    # ArUco false-positive filter
                    pos_invalid = True
                    if aruco_z is not None: 
                        x_valid = -5.0 < aruco_x < 5.0 
                        y_valid = -1.0 < aruco_y < 1.0
                        z_valid = 0.0 < aruco_z < 10.0
                        pos_invalid = not all([x_valid, y_valid, z_valid])
                    false_positive = pos_invalid 
                    if dog.marker_detected and not false_positive: 
                        if aruco_z > DIST_FOLLOW:
                            # Increase translational velocity gradually depending on current distance
                            # V_MAX at distance of DIST_ACC_MAX
                            vx = map(aruco_z, DIST_FOLLOW, DIST_ACC_MAX, V_MIN, V_MAX)

                            # Keep velocity within boundaries
                            vx = constrain(vx, V_MIN, V_MAX)

                            dog.vx, dog.vy, dog.vz = vx, 0.0, -aruco_x/aruco_z
                        elif aruco_z < DIST_MIN:
                            dog.vx, dog.vy, dog.vz = -V_MIN, 0.0, 0.0
                        else:
                            vz = 0.0
                            if phi > PHI_MAX:
                                vz = -W_MAX
                            elif -phi > PHI_MAX:
                                vz = W_MAX

                            dog.vx, dog.vy, dog.vz = 0.0, 0.0, vz
                        asyncio.run_coroutine_threadsafe(dog.move_xyz(), loop)

                    else:
                        dog.search_active = True
                        # In which direction did the ArUco marker disappear?
                        if aruco_x is None or aruco_x < 0:
                            asyncio.run_coroutine_threadsafe(dog.find_marker(clockwise=False), loop)
                        else:
                            asyncio.run_coroutine_threadsafe(dog.find_marker(clockwise=True), loop)


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
