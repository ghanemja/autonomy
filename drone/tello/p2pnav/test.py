##################################
# Tello EDU Sample Program 01 
#
# MIT NEET-AM Autonomous Machines
#
# 11/18/2024
##################################

from djitellopy import Tello
import threading # used to create separate flows of excecution
import socket # used to create a UDP client via WiFi
import time # used to add delays between commands
import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np

host = ''
port = 9000
locaddr = (host, port)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ('192.168.10.1', 8889)
sock.bind(locaddr)

# function for receiving messages from the tello
# prints "ok" if successfull or "error" if not successful
def recv():
    count = 0
    while True:
        try:
            data, server = sock.recvfrom(1518)
            print(data.decode(encoding="utf-8"))
        except Exception:
            print('\nExit . . .\n')
            break

def sendMessage(cmd):
    msg = cmd.encode(encoding='utf-8')
    sent = sock.sendto(msg, tello_address)
    time.sleep(5)

def get_centroid(frame_reader):
    # cv method centroiding
    img = cv.imread(frame_reader.frame)
    edges = cv.Canny(img, 100, 200)

    plt.subplot(121),plt.imshow(img,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    
    plt.show()

    # if img is not None:
    # use cv for edge detection
    

recvThread = threading.Thread(target=recv)
recvThread.start()

tello = Tello()
frame_reader = tello.get_frame_read()

stop = False
while not stop:

    height = tello.get_height
    yaw = tello.get_yaw
    pitch = tello.get_pitch
    roll = tello.get_roll




