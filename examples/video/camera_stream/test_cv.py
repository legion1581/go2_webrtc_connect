import cv2
import numpy as np

def test_cv2_imshow():
    # Create a dummy frame (a simple black image)
    height, width = 480, 640  # You can adjust the size
    dummy_frame = np.zeros((height, width, 3), dtype=np.uint8)

    # Draw a red rectangle in the center (just to see something on the image)
    start_point = (int(width / 4), int(height / 4))
    end_point = (int(3 * width / 4), int(3 * height / 4))
    color = (0, 0, 255)  # Red color in BGR
    thickness = 2
    cv2.rectangle(dummy_frame, start_point, end_point, color, thickness)

    # Test the imshow function
    cv2.imshow("Received Video", dummy_frame)

    # Wait for a key press for 3 seconds (3000 milliseconds)
    cv2.waitKey(3000)

    # Close all windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_cv2_imshow()
