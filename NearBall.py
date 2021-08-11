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

lo = 80
real_prop = 42.7/1000
# uneasy to detect balls due to shadow, but it is not needed to detect perfectly for deciding collision

img = cv2.imread(imgList[0])
imgc = img.copy()
alpha = 1.0
img = np.clip((1 + alpha) * img - 128 * alpha, 0, 255).astype(np.uint16)
img = cv2.GaussianBlur(img, (0, 0), 1.5)
dst = cv2.inRange(img, np.array([lo, lo, lo]), np.array([255, 255, 255]))
dst = cv2.medianBlur(dst, 3)
src = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
temp_pic = imgc
_, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
contours, hierarchy = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
pts = list()
k1 = 3/2
k2 = 9/8


for i in range(len(stats)):
    x, y, w, h, area = stats[i]
    mx, my = centroids[i]
    if (h, w) < dst.shape and 0.9 < area / (0.25 * math.pi * w * h) and 81 * 4 < w * h < 3600 * 4:
        if k1 > w/h >= 1:
            cv2.rectangle(temp_pic, (x, y, w, w), (0, 0, 255), 3)
            cv2.line(temp_pic, (int(mx), int(my-h/2+w/2)),
                     (int(mx), int(my-h/2+w/2)), (0, 0, 255), 11)
            point = [x, y, w, w, area, mx, my-h/2+w/2, w/2]
            pts.append(point)
        elif k1 > h/w > 1:
            cv2.rectangle(temp_pic, (x, y, h, h), (0, 0, 255), 3)
            cv2.line(temp_pic, (int(mx-w/2+h/2), int(my)),
                     (int(mx-w/2+h/2), int(my)), (0, 0, 255), 11)
            point = [x, y, h, h, area, mx-w/2+h/2, my, h/2]
            pts.append(point)

for j in range(len(pts)):
    for cnt in contours:
        if len(cnt)>=5:
            ellipse = cv2.fitEllipse(cnt)
            (x1, y1), (MA, ma), angle = ellipse
            if (0,0) < (int(y1), int(x1)) < dst.shape:
                for k in range(len(stats)):
                    if labels[int(y1)][int(x1)] == k+1:
                        cv2.ellipse(temp_pic, ellipse,(255,255,5),5)

sorted_pts = sorted(pts, key=lambda points: points[2]+point[3])
i1 = sorted_pts[-1]
i2 = sorted_pts[-2]
i3 = sorted_pts[-3]
triangle = [(i1[5], i1[6], i1[7]), (i2[5], i2[6], i2[7]), (i3[5], i3[6], i3[7]), df.distance(
    i1[5], i1[6], i2[5], i2[6]), df.distance(i3[5], i3[6], i2[5], i2[6]), df.distance(i3[5], i3[6], i1[5], i1[6])]
print(triangle)
cv2.imshow("img", cv2.resize(temp_pic, (0, 0), None,
           fx=0.25, fy=0.25, interpolation=None))
cv2.imwrite('images/NearBall.jpg', temp_pic)
cv2.waitKey()