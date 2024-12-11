import numpy as np
from djitellopy import tello
import cv2
import matplotlib.pyplot as plt

plt.ion()
fig, ax = plt.subplots()
img_plot = ax.imshow(np.zeros((240, 360, 3), dtype=np.uint8))
me = tello.Tello()
me.connect()
print(me.get_battery())
me.streamon()
while True:
    img = me.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_plot.set_data(img)
    plt.pause(0.01)

plt.ioff()
plt.show()

