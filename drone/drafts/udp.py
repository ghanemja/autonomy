# # import socket
# # import time
# # import cv2
# # import numpy as np

# # def get_local_ip():
# #     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# #     try:
# #         s.connect(('10.255.255.255', 1))
# #         IP = s.getsockname()[0]
# #     except Exception:
# #         IP = '127.0.0.1'
# #     finally:
# #         s.close()
# #     return IP

# # tello_ip = '192.168.10.1'
# # tello_port = 8889
# # tello_address = (tello_ip, tello_port)

# # host = get_local_ip()
# # port = 9000

# # mypc_address = (host, port)

# # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# # sock.bind(mypc_address)

# # print(f"Bound to {mypc_address}")

# # sock.sendto('command'.encode('utf-8'), tello_address)
# # sock.sendto('streamon'.encode('utf-8'), tello_address)
# # print("Start streaming")

# # capture = cv2.VideoCapture('udp://0.0.0.0:11111', cv2.CAP_FFMPEG)
# # if not capture.isOpened():
# #     capture.open('udp://0.0.0.0:11111')

# # cv2.namedWindow('Tello Stream', cv2.WINDOW_NORMAL)

# # running = True
# # while running:
# #     ret, frame = capture.read()
# #     if ret:
# #         cv2.imshow('Tello Stream', frame)
    
# #     key = cv2.waitKey(1) & 0xFF
# #     if key == ord('q') or key == 27:  # 'q' key or ESC key
# #         running = False

# # capture.release()
# # cv2.destroyAllWindows()
# # sock.sendto('streamoff'.encode('utf-8'), tello_address)
# # sock.close()
# # print("Streaming stopped")
# import socket
# import cv2
# import numpy as np

# def get_local_ip():
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     try:
#         s.connect(('10.255.255.255', 1))
#         IP = s.getsockname()[0]
#     except Exception:
#         IP = '127.0.0.1'
#     finally:
#         s.close()
#     return IP

# tello_ip = '192.168.10.1'
# tello_port = 8889
# tello_address = (tello_ip, tello_port)

# host = get_local_ip()
# port = 9000

# mypc_address = (host, port)

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind(mypc_address)

# print(f"Bound to {mypc_address}")

# sock.sendto('command'.encode('utf-8'), tello_address)
# sock.sendto('streamon'.encode('utf-8'), tello_address)
# print("Start streaming")

# capture = cv2.VideoCapture('udp://0.0.0.0:11111', cv2.CAP_FFMPEG)
# if not capture.isOpened():
#     capture.open('udp://0.0.0.0:11111')

# cv2.namedWindow('Tello Stream', cv2.WINDOW_NORMAL)

# running = True
# while running:
#     ret, frame = capture.read()
#     if ret:
#         cv2.imshow('Tello Stream', frame)
       
#     # key = cv2.waitKey(1) & 0xFF
#     # if key == ord('q') or key == 27:  # 'q' key or ESC key
#     #     break

# capture.release()
# cv2.destroyAllWindows()
# sock.sendto('streamoff'.encode('utf-8'), tello_address)
# sock.close()
# print("Streaming stopped")
import socket
import cv2
import numpy as np

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

tello_ip = '192.168.10.1'
tello_port = 8889
tello_address = (tello_ip, tello_port)

host = get_local_ip()
port = 9000

mypc_address = (host, port)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(mypc_address)

print(f"Bound to {mypc_address}")

# Send commands to Tello
sock.sendto('command'.encode('utf-8'), tello_address)
sock.sendto('streamon'.encode('utf-8'), tello_address)
print("Start streaming")

# Open video capture
try:
    capture = cv2.VideoCapture('udp://@0.0.0.0:11111') # , cv2.CAP_FFMPEG)
except Exception as e:
    print("Error opening capture...")

if not capture.isOpened():
    print("Error: Unable to open video stream.")
else:
    print("Video stream opened successfully.")

cv2.namedWindow('Tello Stream', cv2.WINDOW_NORMAL)

# running = True
# while running:
#     ret, frame = capture.read()
    
#     if not ret:
#         print("Error: No frame received.")
#         continue
    
#     # Check if frame is valid
#     if frame is None or frame.size == 0:
#         print("Received an empty frame.")
#         continue
    
#     # Display the frame
#     cv2.imshow('Tello Stream', frame)
    
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('q') or key == 27:  # 'q' key or ESC key
#         running = False
while True:
    ret, frame = capture.read()
    
    if not ret:
        print("Error: No frame received.")
        break
    
    # Optional: Convert the frame to a different color space if needed
    # For example, converting to grayscale:
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the frame in a window
    cv2.imshow('Drone Camera Stream', frame)

    # Break the loop on 'q' key press or window close
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:  # 'q' key or ESC key
        break
# running = True
# while running:
#     ret, frame = capture.read()
    
#     if not ret:
#         print("Error: No frame received.")
#         continue
    
#     # Check if frame is valid
#     if frame is None or frame.size == 0:
#         print("Received an empty frame.")
#         continue
    
#     # Display the frame
#     cv2.imshow('Tello Stream', frame)
    
#     # Check if the window is closed (user clicked X button)
#     if cv2.getWindowProperty('Tello Stream', cv2.WND_PROP_VISIBLE) < 1:
#         running = False
    
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('q') or key == 27:  # 'q' key or ESC key
#         running = False

# Clean up
capture.release()
cv2.destroyAllWindows()
sock.sendto('streamoff'.encode('utf-8'), tello_address)
sock.close()
print("Streaming stopped")
# import cv2
# import numpy as np

# # Define the video stream URL or address (replace with your drone's stream address)
# video_stream_url = 'udp://@0.0.0.0:11111'  # Example for UDP stream

# # Open the video capture
# capture = cv2.VideoCapture(video_stream_url)

# if not capture.isOpened():
#     print("Error: Unable to open video stream.")
#     exit()

# cv2.namedWindow('Drone Camera Stream', cv2.WINDOW_NORMAL)

# while True:
#     ret, frame = capture.read()
    
#     if not ret:
#         print("Error: No frame received.")
#         break
    
#     # Optional: Convert the frame to a different color space if needed
#     # For example, converting to grayscale:
#     # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Display the frame in a window
#     cv2.imshow('Drone Camera Stream', frame)

#     # Break the loop on 'q' key press or window close
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('q') or key == 27:  # 'q' key or ESC key
#         break

# # Clean up
# capture.release()
# cv2.destroyAllWindows()
