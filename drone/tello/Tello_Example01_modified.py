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

def sendMessage(cmd):
    msg = cmd.encode(encoding='utf-8')
    sent = sock.sendto(msg, tello_address)
    time.sleep(5)

recvThread = threading.Thread(target=recv)
recvThread.start()

cmds = [
            "command",
            "takeoff",
            "up 150",
            "left 30",
            "right 60",
            "left 30",
            "forward 30",
            "back 60",
            "forward 30",
            "flip l",
            "flip r",
            "flip r",
            "flip l",
            "cw 360",
            "battery?",
            "land"
       ]

try:

    # send the commands
    for cmd in cmds:
        sendMessage(cmd)

    # close the socket
    sock.close()

except KeyboardInterrupt:
    print('\n . . .\n')
    sock.close()