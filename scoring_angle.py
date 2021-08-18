import math
import sys
import cv2
import numpy as np
import Definitions as df
from openpyxl import Workbook

mod = sys.modules[__name__]

video = cv2.VideoCapture("tasks/Golf_Test_2-1.mp4")

if not video.isOpened():
    sys.exit()

delay = df.getDelay(video)

while True:
    ret, img = video.read()

    if not ret:
        break

    boxes = list()
    lines = list()
    cimg = img.copy()

    img = cv2.GaussianBlur(img, (0, 0), 1.5)
    rimg = img.copy()
    pimg = img.copy()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # masks
    mask_white = cv2.inRange(img, np.array(
        [90, 90, 90]), np.array([255, 255, 255]))
    mask_red_r = cv2.inRange(hsv, np.array(
        [-10, 160, 0]), np.array([10, 255, 255]))
    mask_gray_r = cv2.inRange(gray, 0, 150)
    mask_white_p = cv2.inRange(img, np.array(
        [180, 180, 180]), np.array([255, 255, 255]))
    mask_green_p = cv2.inRange(hsv, np.array(
        [30, 0, 0]), np.array([60, 255, 255]))

    # red line to get angle
    rimg[mask_red_r == 0] = [0, 0, 0]
    rimg[mask_gray_r == 0] = [0, 0, 0]
    rimg = cv2.cvtColor(rimg, cv2.COLOR_BGR2GRAY)
    _, rdst = cv2.threshold(rimg, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    rcontours, _ = cv2.findContours(
        rdst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in rcontours:
        rect = cv2.minAreaRect(cnt)
        ((x, y), (w, h), angle) = rect
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        if h != 0:
            if w/h > 10 or w/h < 0.1:
                cv2.drawContours(cimg, [box], -1, (0, 255, 0), 1)
                lines.append(rect)
        if 5000 < w * h < 100000 and 0.2 < w/h < 5 and w*h > 100:
            continue

    if len(lines) >= 1:
        lines = sorted(lines, key=lambda rct: rct[2] * rct[2])
        rectangle = lines[-1]
        ((x, y), (w, h), angle) = rectangle
        box = cv2.boxPoints(rectangle)
        box = np.int0(box)
        cv2.drawContours(cimg, [box], -1, (0, 255, 255), 5)

    # to get putter angle
    pimg[cv2.inRange(gray, 230, 255) == 0] = [0, 0, 0]
    pimg = cv2.cvtColor(pimg, cv2.COLOR_BGR2GRAY)
    _, pdst = cv2.threshold(pimg, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    pcontours, _ = cv2.findContours(
        pdst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    pimg = cv2.cvtColor(pdst, cv2.COLOR_GRAY2BGR)
    for cnt in pcontours:
        rect = cv2.minAreaRect(cnt)
        ((x, y), (w, h), angle) = rect
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        if h != 0:
            if 30 > w/h > 2 or 1/30 < w/h < 1/2 and w*h < 100:
                cv2.drawContours(pimg, [box], -1, (0, 255, 0), 1)
                boxes.append(rect)

    if len(boxes) >= 1:
        boxes = sorted(boxes, key=lambda rct: rct[1][0] * rct[1][1])
        rectangle = boxes[-1]
        ((x, y), (w, h), angle) = rectangle
        box = cv2.boxPoints(rectangle)
        box = np.int0(box)
        # cv2.drawContours(pimg, [box], -1, (255, 0, 255), 5)

    cv2.imshow("dst", pimg)

    if cv2.waitKey(delay) == 27:

        break

video.release()
cv2.destroyAllWindows()