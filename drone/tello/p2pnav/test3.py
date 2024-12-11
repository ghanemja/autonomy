from djitellopy import Tello
import cv2 as cv
import numpy as np
import threading
import time

# Initialize Tello drone
tello = Tello()
tello.connect(wait_for_state=False)
tello.streamon()
tello.takeoff()
time.sleep(3)
tello.move_up(20)

# Function to detect orange hoops and find their centroids
def detect_orange_hoop(frame):
    # Convert frame to HSV color space for better color segmentation
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    # Define HSV range for orange color (adjust values if needed)
    lower_orange = np.array([10, 100, 100])
    upper_orange = np.array([25, 255, 255])
    
    # Create a mask for orange color
    mask = cv.inRange(hsv, lower_orange, upper_orange)
    
    # Perform edge detection using Canny
    edges = cv.Canny(mask, 100, 100)
    
    # Find contours in the edge-detected image
    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    if contours:
        print("Contours")
        # Sort contours by area and keep the largest one (assuming it's the closest hoop)
        largest_contour = max(contours, key=cv.contourArea)
        
        # Calculate the centroid of the largest contour
        M = cv.moments(largest_contour)
        if M["m00"] > 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            print("HOOP FOUND")
            return (cx, cy), True  # Return centroid and detection status
    return None, False

def navigate_to_hoop2(centroid, frame_width, frame_height):
    cx, cy = centroid
    frame_center_x = frame_width // 2
    frame_center_y = frame_height // 2
    
    # Calculate offsets from the center of the frame
    x_offset = cx - frame_center_x
    y_offset = cy - frame_center_y
    
    # Calculate speed based on offset (max speed of 50)
    max_speed = 50
    x_speed = int(np.clip((x_offset / frame_width) * max_speed * 2, -max_speed, max_speed))
    y_speed = int(np.clip((y_offset / frame_height) * max_speed * 2, -max_speed, max_speed))
    
    # Adjust drone movement based on calculated speeds
    if abs(x_speed) > 5:  # Small threshold to avoid minute movements
        tello.send_rc_control(x_speed, 0, 0, 0)  # Move left/right
    
    if abs(y_speed) > 5:  # Small threshold to avoid minute movements
        tello.send_rc_control(0, 0, -y_speed, 0)  # Move up/down (inverted for y-axis)
    
    print(f"Adjusting position: x_speed={x_speed}, y_speed={y_speed}")
    time.sleep(0.5)  # Reduced wait time for more responsive control

# Function to navigate towards a detected hoop
def navigate_to_hoop(centroid, frame_width, frame_height):
    cx, cy = centroid
    
    # Calculate the center of the frame programmatically
    frame_center_x = frame_width // 2
    frame_center_y = frame_height // 2
    
    # Calculate offsets from the center of the frame
    x_offset = cx - frame_center_x
    y_offset = cy - frame_center_y
    
    # Adjust drone movement based on offsets (values can be fine-tuned)
    if abs(x_offset) > 10:  # Horizontal adjustment
        if x_offset > 0:
            tello.move_right(10)  # Move right
        else:
            tello.move_left(10)  # Move left
    
    if abs(y_offset) > 10:  # Vertical adjustment
        if y_offset > 0:
            tello.move_down(10)  # Move down
        else:
            tello.move_up(10)   # Move up
    
    time.sleep(1)  # Allow time for movement adjustment
    tello.move_forward(70)

# Main loop to process frames and control drone navigation
try:
    while True:
        frame = tello.get_frame_read().frame
        
        # Get frame dimensions programmatically
        frame_height, frame_width = frame.shape[:2]

        # tello.move_up(50)
        
        # Detect orange hoop in the current frame
        centroid, found = detect_orange_hoop(frame)
        
        if found:
            print(f"Hoop detected at {centroid}")
            navigate_to_hoop(centroid, frame_width, frame_height)
        else:
            print("No hoop detected. Searching...")
            tello.rotate_clockwise(30)  # Rotate to search for the next hoop
            
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Landing...")
    tello.land()
