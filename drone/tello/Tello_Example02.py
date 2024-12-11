##################################
# Tello EDU Sample Program 02 
#
# MIT NEET-AM Autonomous Machines
#
# 11/20/2024
##################################

from djitellopy import Tello
import time 

tello = Tello()

tello.connect()

tello.takeoff()
time.sleep(5)

tello.move_up(150)
time.sleep(5)

tello.move_left(30)
time.sleep(5)

tello.move_right(60)
time.sleep(5)

tello.move_left(30)
time.sleep(5)

tello.move_forward(30)
time.sleep(5)

tello.move_back(60)
time.sleep(5)

tello.move_forward(30)
time.sleep(5)

tello.flip_left()
time.sleep(5)

tello.flip_right()
time.sleep(5)

tello.flip_right()
time.sleep(5)

tello.flip_left()
time.sleep(5)

tello.rotate_clockwise(360)
time.sleep(5)

tello.get_battery()
time.sleep(5)

tello.land()