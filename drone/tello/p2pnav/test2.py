import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('test2.jpg')
edges = cv.Canny(img, 100, 200)

print('plotting')
plt.subplot(121),plt.imshow(img)
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(121),plt.imshow(edges)
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    
contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

for contour in contours:
    M = cv.moments(contour)

    if M['m00'] != 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        cv.circle(img, (cx, cy), 5, (0,0,255), -1)

win = cv.imshow('hoop', img)
cv.resizeWindow('hoop', 200.0,200.0)
cv.waitKey(0)
# plt.imshow(img)
