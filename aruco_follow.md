# ArUco Follow Project

## Overview
The ArUco Follow project is designed to enable the Unitree Go2 to autonomously track an ArUco marker or be controlled manually via a keyboard. The robot switches between these modes based on user input and adapts its behavior accordingly.

## Dog Class
The `Dog` class encapsulates all functionalities related to controlling the robotic dog. It is implemented in `dog.py` and includes the following attributes and methods:

### Attributes
- **`ip_address`** (`str`): The IP address of the robotic dog.
- **`vx`** (`float`): Target velocity in the x-direction (robot frame).
- **`vy`** (`float`): Target velocity in the y-direction (robot frame).
- **`vz`** (`float`): Rotational velocity (robot frame).
- **`vmax`** (`float`): Maximum linear velocity.
- **`wmax`** (`float`): Maximum angular velocity.
- **`conn`** (`Go2WebRTCConnection`): Contains the Go2WebRTCConnection object.
- **`mode`** (`ControlMode`): Defines the current control mode of the robot (manual or autonomous).
- **`marker_detected`** (`bool`): Indicates if an ArUco marker is detected.
- **`search_active`** (`bool`): Indicates if the robot is actively searching for an ArUco marker.
- **`last_detection_timestamp`** (`float`): Timestamp of the last ArUco marker detection.
- **`camera_matrix`** (`numpy.ndarray`): Projection matrix for world-coordinates <-> image-coordinates transformations.
- **`dist_coeffs`** (`numpy.ndarray`): Distortion coefficients for the camera lens.

### Methods
- **`balance_stand(self)`**: Sets the robot to the balance stand state.
- **`paw_wave(self)`**: Lets the robot wave with it's right paw 
- **`move_xyz(self)`**: Moves the robot based on the current velocity attributes (`vx`, `vy`, `vz`).
- **`sit(self)`**: Lets the robot sit down.
- **`stand_down(self)`**: Sets in a resting state.
- **`stand_up(self)`**: Lets the robot perform the stand-up movement.
- **`set_vui(self, color: VUI_COLOR)`**: Sets the color of the robots front LED.

## Control Mode Class
The `ControlMode` class is an enumeration that defines the operational modes of the robot:

- **`MODE_AUTO`**: Autonomous mode, where the robot searches for and tracks the ArUco marker.
- **`MODE_MANUAL`**: Manual mode, allowing user control (e.g., via keyboard).

## ArUco Follow Script (`aruco_follow.py`)
The `aruco_follow.py` script is the main entry point of the project. It manages the interaction between the user and the Unitree Go2 and handles the toggling of control modes. The script includes the following functionalities:

### Features

1. **Mode Switching**:
   - Users can toggle between `MODE_MANUAL` and `MODE_AUTO` using keyboard's TAB-key.
   - In `MODE_MANUAL`, the robot responds to user's keyboard inputs to control the robot directly.
   - In `MODE_AUTO`, the robot searches for an ArUco marker and maintains a predefined distance once detected.

2. **ArUco Marker Detection**:
   - The script processes the video feed from the robot's camera to detect ArUco markers.
   - Upon detecting a marker, the robot calculates its position relative to the marker and adjusts its velocity to maintain the desired distance.

3. **Search Behavior**:
   - When no marker is detected, the robot enters a search mode where it rotates and scans its surroundings.
   - The search continues until the marker is found or the mode is toggled.

4. **Keyboard Control**:
   - Users can control the robot's linear and angular velocities using specific keys.
   - Commands include forward/backward movement, lateral movement, rotation and some predefined movements.

5. **LED Indicator**:
   - LED turns green if an ArUco marker is found in the image
   - LED turns blue if no ArUco marker is found in the image

6. **Safety Mechanisms**:
  - TODO

### Functions

- **`toggle_mode()`**:
  Toggles between manual and autonomous modes based on user input.

- **`process_marker_detection(marker_data)`**:
  Processes the detected marker's data to calculate relative position and update the robot's velocities.

- **`keyboard_control()`**:
  Captures and processes keyboard inputs to control the robot in manual mode.

- **`search_for_marker()`**:
  Implements the search behavior by rotating the robot when no marker is detected.

- **`main()`**:
  The main loop of the script, managing mode switching, marker detection, and robot control.

### Key Bindings (Manual Mode)
- **`TAB`**: Toggle between manual and autonomous modes
- **`W`**: Move forward
- **`S`**: Move backward
- **`A`**: Rotate counterclockwise
- **`D`**: Rotate clockwise
- **`Q`**: Sidestep left
- **`E`**: Sidestep right
- **`1`**: Paw wave
- **`2`**: Sit
- **`3`**: Stand down
- **`4`**: Stand up + balance stand

## Camera Calibration
A key component of this program is the pose estimation of the ArUco marker.
For this purpose the file `ost.yaml` file is a mandatory component for the project, as it provides the camera parameters required for accurate ArUco marker detection and pose estimation. These parameters are critical for transforming 2D image coordinates into 3D world coordinates.
The file has been generated and obtained via the ROS camera calibrator (separate workspace).

### Contents of `ost.yaml`
The `ost.yaml` file contains:
- **Camera Matrix (`camera_matrix`)**: A 3x3 matrix describing the intrinsic parameters of the camera, including focal lengths and the optical center.
- **Distortion Coefficients (`dist_coeffs`)**: A list of coefficients describing the distortion caused by the camera lens.

## Usage Instructions
1. Ensure the robotic dog is powered on and connected to the network.
2. Ensure that `IP_ADDRESS` in `aruco_follow.py` is set to the robots IP address.
2. Run the `aruco_follow.py` script.
3. Use the keyboard to control the robot in manual mode or switch to autonomous mode to let it track an ArUco marker.
4. Observe the robot's behavior and ensure a clear view of the marker for optimal tracking.

## TODO:
1. Encapsulate keyboard control and ArUco functionality each in a separate python module. The dog class should have an attribute for each as a class placeholder that can be set, if this functionality is needed. The modules will be implemented by the students as lab exercises.
2. Safety mechanisms - Robot should stop, when:  
   - connection is lost  
   - no ArUco marker is found for a specific period of time  
   - Lidar or depth camera detects an obstacle
3. Restrict ArUco tracking to follow only a specific marker ID (e.g., 0).
4. Private attributes + getters and setters (`@property`) for more robustness and better error handling
5. Find a solution to eliminate the requirement for the OpenCV image window to be active in order to capture keyboard input.
