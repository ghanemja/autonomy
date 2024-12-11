import cv2
import numpy as np
import time

# Simulated Tello class
class SimulatedTello:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.yaw = 0

    def send_rc_control(self, left_right, forward_backward, up_down, yaw):
        self.x += left_right
        self.y += forward_backward
        self.z += up_down
        self.yaw += yaw
        print(f"Drone position: ({self.x}, {self.y}, {self.z}), Yaw: {self.yaw}")

    def rotate_clockwise(self, angle):
        self.yaw += angle
        print(f"Rotating clockwise by {angle} degrees. New yaw: {self.yaw}")

def create_simulated_frame(width=960, height=720, hoop_center=None):
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    if hoop_center is None:
        hoop_center = (width//2, height//2)
    cv2.circle(frame, hoop_center, 100, (0, 165, 255), thickness=10)
    return frame

def detect_orange_hoop(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_orange = np.array([10, 100, 100])
    upper_orange = np.array([25, 255, 255])
    mask = cv2.inRange(hsv, lower_orange, upper_orange)
    edges = cv2.Canny(mask, 100, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        if M["m00"] > 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            return (cx, cy), True
    return None, False

def navigate_to_hoop(tello, centroid, frame_width, frame_height):
    cx, cy = centroid
    frame_center_x = frame_width // 2
    frame_center_y = frame_height // 2
    
    x_offset = cx - frame_center_x
    y_offset = cy - frame_center_y
    
    max_speed = 50
    x_speed = int(np.clip((x_offset / frame_width) * max_speed * 2, -max_speed, max_speed))
    y_speed = int(np.clip((y_offset / frame_height) * max_speed * 2, -max_speed, max_speed))
    
    if abs(x_speed) > 5:
        tello.send_rc_control(x_speed, 0, 0, 0)
    
    if abs(y_speed) > 5:
        tello.send_rc_control(0, 0, -y_speed, 0)
    
    print(f"Adjusting position: x_speed={x_speed}, y_speed={y_speed}")
    time.sleep(0.5)

def main():
    tello = SimulatedTello()
    frame_width, frame_height = 960, 720
    hoop_center = (frame_width//2, frame_height//2)

    try:
        while True:
            frame = create_simulated_frame(frame_width, frame_height, hoop_center)
            
            centroid, found = detect_orange_hoop(frame)
            
            if found:
                print(f"Hoop detected at {centroid}")
                navigate_to_hoop(tello, centroid, frame_width, frame_height)
            else:
                print("No hoop detected. Searching...")
                tello.rotate_clockwise(30)
            
            cv2.imshow("Simulated Tello View", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            # Simulate hoop movement
            hoop_center = ((hoop_center[0] + 5) % frame_width, hoop_center[1])
            
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Simulation ended by user")
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
