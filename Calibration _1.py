import cv2
import numpy as np
import sys
import Definitions as df
import math

cap1 = cv2.imread("tasks/sample_img-1.jpg")
cap1 = cap1[50*2:250*2,150*2:600*2]
cap1 = cv2.GaussianBlur(cap1, (0,0), 1.0)
dst1 = cv2.Canny(cap1, 150, 200)
cv2.imshow("dst1",dst1)
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
        segments1.append(df.distance(approx[0][0][0],approx[0][0][1],approx[1][0][0],approx[1][0][1]))
        segments1.append(df.distance(approx[2][0][0],approx[2][0][1],approx[1][0][0],approx[1][0][1]))
        segments1.append(df.distance(approx[0][0][0],approx[0][0][1],approx[2][0][0],approx[2][0][1]))
        break
segments1.sort()
print(segments1)
param = 3/segments1[0]

cap2 = cv2.imread("tasks/sample_img-2.jpg")
cap2 = cap2[50*2:250*2,150*2:600*2]
cap2 = cv2.GaussianBlur(cap2, (0,0), 1.0)
dst2 = cv2.Canny(cap2, 150, 200)
cv2.imshow("cap2", dst2)
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
        segments2.append(df.distance(approx[0][0][0],approx[0][0][1],approx[1][0][0],approx[1][0][1]))
        segments2.append(df.distance(approx[2][0][0],approx[2][0][1],approx[1][0][0],approx[1][0][1]))
        segments2.append(df.distance(approx[0][0][0],approx[0][0][1],approx[2][0][0],approx[2][0][1]))
        break
segments2.sort()
print(segments2)

if len(segments1) == len(segments2):
    avg_ = list()
    for i in range(len(segments1)):
        if 0.9 < segments1[i]/segments2[i] < 1.1:
            avg_.append(segments1[i]/segments2[i])
        else:
            sys.exit()
    param_ = 1/np.average(avg_)
    param__ = param * param_
    print(param__)
    
if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()