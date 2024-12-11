import cv2
cv2.startWindowThread()


from djitellopy import Tello

# Initialize Tello
tello = Tello()
tello.connect()
print("Battery:", tello.get_battery())

# Start video streaming
tello.streamon()

# Create a frame reader
frame_read = tello.get_frame_read()
# Main loop to display video
try:
    while True:
        img = frame_read.frame  # Get the latest frame
        if img is not None:  # Ensure the frame is valid
            cv2.namedWindow('Tello', cv2.WINDOW_AUTOSIZE)
            cv2.imshow("Tello Video Stream", img)
            cv2.waitKey(0)  # delay 0
        else:
            print("No frame received.")
        
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit on 'q' key
            break
finally:
    tello.streamoff()  # Turn off streaming
    cv2.destroyAllWindows()  # Close OpenCV windows
