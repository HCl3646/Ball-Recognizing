import cv2
import numpy as np
import sys
import Definitions as df
import math

cap1 = cv2.imread("tasks/sample_img-1.jpg")
cv2.imshow("dst1", cap1)
cap1 = cap1[50*2:250*2, 150*2:600*2]
cap1 = cv2.GaussianBlur(cap1, (0, 0), 1.0)
dst1 = cv2.Canny(cap1, 150, 200)
contours, _ = cv2.findContours(dst1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
triangles1 = list()
segments1 = list()

for cnt in contours:
    if cv2.contourArea(cnt) < 20:
        continue
    epsilon = cv2.arcLength(cnt, True) * 0.0845
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    vtx = len(approx)
    if vtx == 3:
        triangles1.append(approx[0][0])
        triangles1.append(approx[1][0])
        triangles1.append(approx[2][0])
        triangles1 = sorted(triangles1, key=lambda pts: pts[0])
        segments1.append(df.distance(
            triangles1[0][0], triangles1[0][1], triangles1[1][0], triangles1[1][1]))
        segments1.append(df.distance(
            triangles1[2][0], triangles1[2][1], triangles1[1][0], triangles1[1][1]))
        segments1.append(df.distance(
            triangles1[0][0], triangles1[0][1], triangles1[2][0], triangles1[2][1]))
        break
segments1.sort()
param = 3/segments1[0]

cap2 = cv2.imread("tasks/sample_img-2.jpg")
cv2.imshow("dst2", cap2)
cap2 = cap2[50*2:250*2, 150*2:600*2]
cap2 = cv2.GaussianBlur(cap2, (0, 0), 1.0)
dst2 = cv2.Canny(cap2, 150, 200)
contours, _ = cv2.findContours(dst2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
segments2 = list()
triangles2 = list()
for cnt in contours:
    if cv2.contourArea(cnt) < 50:
        continue
    epsilon = cv2.arcLength(cnt, True) * 0.0845
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    vtx = len(approx)
    if vtx == 3:
        triangles2.append(approx[0][0])
        triangles2.append(approx[1][0])
        triangles2.append(approx[2][0])
        triangles2 = sorted(triangles2, key=lambda pts: pts[0])
        segments2.append(df.distance(
            triangles2[0][0], triangles2[0][1], triangles2[1][0], triangles2[1][1]))
        segments2.append(df.distance(
            triangles2[2][0], triangles2[2][1], triangles2[1][0], triangles2[1][1]))
        segments2.append(df.distance(
            triangles2[0][0], triangles2[0][1], triangles2[2][0], triangles2[2][1]))
        break

if len(segments1) == len(segments2) == 3:
    avg_ = list()
    matching = list()
    # checking elements needed to be included
    for i in range(3):
        idx = 0
        for j in range(3):
            if 0.9 <= segments1[i] / segments2[j] <= 1.1:
                avg_.append(segments1[i]/segments2[i])
                matching.append((i,j))
            else:
                idx += 1
        if idx == 3:
            sys.exit()
        

    param_ = 1/np.average(avg_)
    param__ = param * param_

    
    print(matching)
    print((triangles2[matching[0][1]][0] - triangles1[matching[0][0]][0])*param__,
          (triangles2[matching[0][1]][1] - triangles1[matching[0][0]][1])*param__)

if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()
