import math
import sys
import cv2
import numpy as np
import Definitions as df
import erasing_background as eb
from openpyxl import Workbook


video = cv2.VideoCapture("tasks\Golf_Test_1.mp4")

if not video.isOpened():
    sys.exit()

ret, line = video.read()

line = cv2.GaussianBlur(line, (0, 0), 1.0)
cline = line.copy()
hsv = cv2.cvtColor(line, cv2.COLOR_BGR2HSV)

mask_white = cv2.inRange(line, np.array(
    [80, 80, 80]), np.array([255, 255, 255]))
line[mask_white > 0] = [0, 0, 0]

mask_green = cv2.inRange(hsv, np.array([40, 0, 0]), np.array([50, 255, 255]))
line[mask_green > 0] = [0, 0, 0]

cdline = cv2.Canny(line, 30, 255)

line = cv2.cvtColor(line, cv2.COLOR_BGR2GRAY)

_, dstline = cv2.threshold(line, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

contours, _ = cv2.findContours(cdline, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
lines = list()

for cnt in contours:
    rect = cv2.minAreaRect(cnt)
    ((x, y), (w, h), angle) = rect
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    if h != 0:
        if w/h > 10 or w/h < 0.1:
            lines.append(rect)
if len(lines) >= 1:
    lines = sorted(lines, key=lambda rct: rct[1][0] * rct[1][1])
    line = lines[-1]
    ((x0, y0), (w0, h0), angle_0) = line

delay = df.getDelay(video)
theta_0 = angle_0
while True:
    ret, img = video.read()

    if not ret:
        break

    img = cv2.GaussianBlur(img, (0, 0), 1.0)
    cimg = img.copy()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask_white = cv2.inRange(img, np.array([70, 70, 70]), np.array([255, 255, 255]))
    img[mask_white > 0] = [0,0,0]

    mask_green = cv2.inRange(hsv, np.array([40,0,0]), np.array([50, 255, 255]))
    img[mask_green > 0] = [0,0,0]

    cdimg = cv2.Canny(img, 30, 255)

    contours, _ = cv2.findContours(
        cdimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    boxes = list()
    lines = list()

    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        ((x, y), (w, h), angle) = rect
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        if 5000 < w * h < 100000 and 0.2 < w/h < 5:
            cv2.drawContours(cimg, [box], -1, (0, 255, 0), 1)
            boxes.append(rect)
        elif h != 0:
            if w/h > 10 or w/h < 0.1:
                continue

    if len(boxes) >= 1:
        boxes = sorted(boxes, key=lambda rct: rct[1][0] * rct[1][1])
        rectangle = boxes[-1]
        ((x, y), (w, h), angle) = rectangle
        box = cv2.boxPoints(rectangle)
        box = np.int0(box)
        cv2.drawContours(cimg, [box], -1, (0, 0, 255), 5)

    theta = angle_0 - angle + 90
    if abs(theta_0 - theta) > 5:
        print(angle_0 + 90 - angle)
        theta_0 = theta

    cv2.imshow("src", img)
    if cv2.waitKey(delay) == 27:
        break

video.release()
cv2.destroyAllWindows()
