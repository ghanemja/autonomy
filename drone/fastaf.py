from tellopy import Tello
from helper import detect_tags
from time import sleep, time

import av
import cv2
import numpy as np

FLY = False
CONNECT_ATTEMPTS = 3
SKIP_FRAMES = 300
THROTTLE_FRAMES = 3
LK_PARAMS = {
    "winSize": (45, 45),
    "maxLevel": 2,
    "criteria": (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),
}
WIDTH = 960
HEIGHT = 720
CX = WIDTH // 2
CY = HEIGHT // 2

P_Z = 40        # Forward-back gain
P_X = 0.1       # Left-right gain
P_Y = 0.15      # Up-down gain
P_T = 0.0015    # Theta gain (yaw)
P_W = 0.15      # Shear gain

# State
targets = [16, 3, 18, 8]
u1 = None
gray = [None, None]
dist = float("inf")
timer = 0

drone = Tello()

# Connect to drone
drone.connect()
drone.wait_for_connection(60)
drone.set_video_mode(False)

# Start video stream
for _ in range(CONNECT_ATTEMPTS):
    try:
        container = av.open(drone.get_video_stream())
        break
    except av.AVError as e:
        print("AV Error", e)
if not container:
    raise Exception("Unable to open video stream!")

# Takeoff
if FLY:
    drone.takeoff()
    sleep(2)
    drone.up(50)
    sleep(1.5)
    drone.up(0)

# Program loop
try:
    for i, frame in enumerate(container.decode(video=0)):
        # Sync camera by throttling framerate
        if i < SKIP_FRAMES or i % THROTTLE_FRAMES != 0:
            continue

        # Image processsing
        frame = cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2BGR)
        tags = detect_tags(frame, target_point_dist=0.55, visualize=True)

        # Target point on the screen
        x, y, z = None, None, None

        print(f"Tracking: {targets[0]}; [{dist}]")

        # Tracked tag found
        if targets[0] in tags:
            print("[Mode] Tracking")

            if u1 is None:
                drone.set_yaw(0)
                drone.up(0)
                sleep(1)
            z = tags[targets[0]]['tag'].pose_t[2]
            x = tags[targets[0]]['target']['pixel_coords'][0]
            y = tags[targets[0]]['target']['pixel_coords'][1]

            # Reset for optical flow if needed at next frame
            u1 = tags[targets[0]]['target']['pixel_coords']
            gray = [None, None]
            dist = z
            timer = time()
        # Optical flow
        elif u1 is not None:
            print("[Mode] Optical Flow")

            # Last tracked tag is gone
            # if dist < 1:
            #     bias = True
            #     dist = float("inf")
            #     targets.pop(0)
            if time() - timer > dist * 2:
                print("transition")
                targets.pop(0)
                drone.forward(-10)
                drone.set_yaw(0)
                drone.right(0)
                drone.up(65)

                timer = 0
                dist = float("inf")
                u1 = None
                sleep(0.5)
                drone.forward(0)
                drone.up(0)
                continue

            gray[1] = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray[0] = gray[1] if gray[0] is None else gray[0]

            u1_i = np.reshape(np.array([u1[0], u1[1]], dtype="float32"), (1,1,2))
            u2, _, _ = cv2.calcOpticalFlowPyrLK(gray[0], gray[1], u1_i, None, **LK_PARAMS)
            p = list(u2.flatten())

            cv2.circle(frame, (int(p[0]), int(p[1])), 5, (255, 0, 255), thickness=-1)

            gray[0] = gray[1]
            u1 = p
            
            x, y = p
            z = 2
        # Look around
        elif FLY:
            print("[Mode] Looking Around")

            drone.right(0)
            drone.forward(0)
            drone.up(10)
            drone.set_yaw(0.65)
        
        # PID Controller
        if x is not None and FLY:
            dx = x - CX
            dy = y - CY
            dw = min(abs(dx) + abs(dy), 75)
            drone.right(P_X * dx)
            drone.set_yaw(P_T * dx)
            drone.down(P_Y * dy)
            drone.forward((P_Z - P_W * dw) * z)

        # GUI
        cv2.imshow("Tello", frame)
        cv2.waitKey(1)

finally:
    drone.land()
    drone.quit()
    cv2.destroyAllWindows()