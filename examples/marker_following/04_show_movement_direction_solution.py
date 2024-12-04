import cv2
import numpy as np
import argparse

def my_estimatePoseSingleMarkers(corners, marker_size, mtx, distortion=None):
    '''
    Estimate the rotation and translation vectors for each detected marker.

    Parameters:
    - corners: List of detected corners for each marker.
    - marker_size: Size of the marker in the same unit as used for calibration (e.g., meters).
    - mtx: Camera matrix (intrinsic parameters).
    - distortion: Distortion coefficients.

    Returns:
    - rvecs: List of rotation vectors.
    - tvecs: List of translation vectors.
    '''
    # Define the 3D coordinates of the marker corners in the marker's coordinate system
    marker_points = np.array([
        [-marker_size / 2, marker_size / 2, 0],
        [marker_size / 2, marker_size / 2, 0],
        [marker_size / 2, -marker_size / 2, 0],
        [-marker_size / 2, -marker_size / 2, 0]
    ], dtype=np.float32)

    rvecs = []
    tvecs = []

    for c in corners:
        # Estimate pose of the marker
        success, rvec, tvec = cv2.solvePnP(marker_points, c, mtx, distortion)
        if success:
            rvecs.append(rvec)
            tvecs.append(tvec)

    return rvecs, tvecs


def command_robot(tvec):
    """
    Uses the tvec to command the robot

    Parameters:
    - tvec: 3d vector in m from the marker center to the camera center
    """
    #TODO: implement
    print("Send command to Robot")
    pass


def parse_arguments():
    parser = argparse.ArgumentParser(description="ArUco Marker Pose Estimation")
    parser.add_argument("--marker_size", type=float, required=False, default=0.05,
                        help="Size of the marker in meters.")
    parser.add_argument("--horizontal_fov", type=float, required=False, default=60,
                        help="Horizontal field of view of the camera in degrees.")
    parser.add_argument("--marker_id", type=int, required=False, 
                        help="Maker id that should be tracked")
    return parser.parse_args()

# Parse command-line arguments
args = parse_arguments()
marker_size = args.marker_size
horizontal_fov = args.horizontal_fov
marker_id = args.marker_id


# Initialize the webcam
cap = cv2.VideoCapture(0)

#TODO: Replace with robot frame

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Capture a frame to get the image size
ret, frame = cap.read()
if not ret:
    print("Error: Failed to capture image.")
    cap.release()
    exit()

# Get image dimensions
height, width = frame.shape[:2]

# Compute focal lengths in pixels
fx = fy = (width / 2) / np.tan(np.radians(horizontal_fov) / 2)

# Assume the principal point is at the center of the image
cx = width / 2
cy = height / 2

# Construct the camera intrinsic matrix
camera_matrix = np.array([[fx, 0, cx],
                          [0, fy, cy],
                          [0, 0, 1]], dtype=np.float32)

# No lens distortion
distortion_coeffs = np.zeros(5)

# Image center
image_center = (int(cx), int(cy))

# Define the ArUco dictionary and detector parameters
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters()

# Create the ArUco detector
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image.")
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect the markers
    corners, ids, rejected = detector.detectMarkers(gray)

    if ids is not None:
        # Draw detected markers
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)



        # Estimate pose of each marker
        rvecs, tvecs = my_estimatePoseSingleMarkers(corners, marker_size, camera_matrix, distortion_coeffs)

        # Draw axis and vectors for each marker
        for i, (rvec, tvec) in enumerate(zip(rvecs, tvecs)):
    

            # Draw axis
            cv2.drawFrameAxes(frame, camera_matrix, distortion_coeffs, rvec, tvec, marker_size / 2)

            # Calculate marker center in image coordinates
            marker_center = np.mean(corners[i][0], axis=0).astype(int)
            marker_center = tuple(marker_center)

            # Draw arrowed line from marker center to image center
            cv2.arrowedLine(frame, marker_center, image_center, (0, 255, 0), 2, tipLength=0.05)

            # Calculate vector components
            vector_x = image_center[0] - marker_center[0]
            vector_y = image_center[1] - marker_center[1]
            vector_z = tvec[2][0]  # Distance from camera to marker in meters

            # Prepare text to display
            text = f"id: {ids[i]} - dx: {vector_x}px, dy: {vector_y}px, dx:{tvec[0][0]:.3f}m, dy:{tvec[1][0]:.3f}m, dz: {vector_z:.2f}m"

            # Get text size
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1.0
            thickness = 1
            text_size, baseline = cv2.getTextSize(text, font, font_scale, thickness)
            text_width, text_height = text_size

            # Calculate box coordinates
            box_coords = (
                (marker_center[0], marker_center[1] - text_height - baseline),
                (marker_center[0] + text_width, marker_center[1])
            )

            # Draw rectangle (background box)
            cv2.rectangle(frame, box_coords[0], box_coords[1], (255, 255, 255), cv2.FILLED)

            # Put text over the rectangle
            cv2.putText(frame, text, (marker_center[0], marker_center[1] - baseline), font, font_scale, (0, 0, 0), thickness, cv2.LINE_AA)

            if marker_id and marker_id == ids[i]:
                command_robot(tvec=tvec)

    # Display the resulting frame
    cv2.imshow('Detected Markers and Poses', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()