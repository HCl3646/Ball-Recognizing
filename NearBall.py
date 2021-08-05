import math
import sys
import cv2
import numpy as np
import Definitions as df
import erasing_background as eb
from openpyxl import Workbook

imgList = list()
for i in range(6):
    imgList.append("tasks/NearBall_{}.jpg".format(i+1))

lo = 70
# uneasy to detect balls due to shadow, but it is not needed to detect perfectly for deciding collision

img = cv2.imread(imgList[5])
imgc = img.copy()
alpha = 1.0
img = np.clip((1 + alpha) * img - 128 * alpha, 0, 255).astype(np.uint16)
img = cv2.GaussianBlur(img, (0, 0), 1.5)
dst = cv2.inRange(img, np.array([lo, lo, lo]), np.array([255, 255, 255]))
dst = cv2.medianBlur(dst, 3)
src = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
_, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
pts = list()
k = 3/4

for i in range(len(stats)):
    x, y, w, h, area = stats[i]
    mx, my = centroids[i]
    if (h, w) < dst.shape and k < w / h < 1/k and 0.8 < area / (0.25 * math.pi * w * h) < 1.2 and 81 * 4 < w * h < 3600 * 4:
        if w > h :
            cv2.rectangle(imgc, (x, y, w, w), (0, 0, 255), 3)
            cv2.line(imgc, (int(mx), int(my-h/2+w/2)),
                        (int(mx), int(my-h/2+w/2)), (0, 0, 255), 11)
            point = [x, y, w, w, area, mx, my-h/2+w/2]
            pts.append(point)
        if w <= h:
            cv2.rectangle(imgc, (x, y, h, h), (0, 0, 255), 3)
            cv2.line(imgc, (int(mx-w/2+h/2), int(my)),
                        (int(mx-w/2+h/2), int(my)), (0, 0, 255), 11)
            point = [x, y, h, h, area, mx-w/2+h/2, my]
            pts.append(point)

temp = np.zeros(6)
for p in pts:
    if (p[2]+p[3]) >= (temp[2]+temp[3]):
        temp = p
cv2.line(src, (int(temp[5]), int(temp[6])),
         (int(temp[5]), int(temp[6])), (255, 0, 0), 30)

cv2.imshow("img", cv2.resize(imgc, (0, 0), None,
           fx=0.25, fy=0.25, interpolation=None))
cv2.waitKey()
