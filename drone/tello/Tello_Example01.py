##################################
# Tello EDU Sample Program 01 
#
# MIT NEET-AM Autonomous Machines
#
# 11/18/2024
##################################


import threading # used to create separate flows of excecution
import socket # used to create a UDP client via WiFi
import time # used to add delays between commands


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

recvThread = threading.Thread(target=recv)
recvThread.start()

try:
    msg = "command"
    # Send data
    msg = msg.encode(encoding="utf-8")
    sent = sock.sendto(msg, tello_address)

    msg = "takeoff"
    # Send data
    msg = msg.encode(encoding="utf-8")
    sent = sock.sendto(msg, tello_address)
    time.sleep(5)

    msg = "up 150"
    # Send data
    msg = msg.encode(encoding="utf-8")
    sent = sock.sendto(msg, tello_address)
    time.sleep(5)

    msg = "left 30"
    # Send data
    msg = msg.encode(encoding="utf-8")
    sent = sock.sendto(msg, tello_address)
    time.sleep(5)

    msg = "right 60"
    # Send data
    msg = msg.encode(encoding="utf-8")
    sent = sock.sendto(msg, tello_address)
    time.sleep(5)

    msg = "left 30"
    # Send data
    msg = msg.encode(encoding="utf-8")
    sent = sock.sendto(msg, tello_address)
    time.sleep(5)

    msg = "forward 30"
    # Send data
    msg = msg.encode(encoding="utf-8")
    sent = sock.sendto(msg, tello_address)
    time.sleep(5)

    msg = "back 60"
    # Send data
    msg = msg.encode(encoding="utf-8")
    sent = sock.sendto(msg, tello_address)
    time.sleep(5)
    
    msg = "forward 30"
    # Send data
    msg = msg.encode(encoding="utf-8")
    sent = sock.sendto(msg, tello_address)
    time.sleep(5)

    msg = "flip l"
    # Send data
    msg = msg.encode(encoding="utf-8")
    sent = sock.sendto(msg, tello_address)
    time.sleep(5)

    msg = "flip r"
    # Send data
    msg = msg.encode(encoding="utf-8")
    sent = sock.sendto(msg, tello_address)
    time.sleep(5)

    msg = "flip r"
    # Send data
    msg = msg.encode(encoding="utf-8")
    sent = sock.sendto(msg, tello_address)
    time.sleep(5)

    msg = "flip l"
    # Send data
    msg = msg.encode(encoding="utf-8")
    sent = sock.sendto(msg, tello_address)
    time.sleep(5)

    msg = "cw 360"
    # Send data
    msg = msg.encode(encoding="utf-8")
    sent = sock.sendto(msg, tello_address)
    time.sleep(5)

    msgbat = "battery?"
    # Send data
    msgbat = msgbat.encode(encoding="utf-8")
    sent = sock.sendto(msgbat, tello_address)
    time.sleep(5)


    msg = "land"
    # Send data
    msg = msg.encode(encoding="utf-8")
    sent = sock.sendto(msg, tello_address)

    # close the socket
    sock.close()

except KeyboardInterrupt:
    print('\n . . .\n')
    sock.close()