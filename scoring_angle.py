import math
import sys
import cv2
import numpy as np
import Definitions as df
from openpyxl import Workbook
import functools

mod = sys.modules[__name__]

video = cv2.VideoCapture("tasks/Golf_Test_2-1.mp4")

if not video.isOpened():
    sys.exit()

delay = df.getDelay(video)
bool = True
idx = 0
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

    # to get line angle
    rimg[mask_red_r == 0] = [0, 0, 0]
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
                lines.append(rect)
    if len(lines) >= 1:
        lines = sorted(lines, key=lambda rct: rct[1][0] * rct[1][1])
        rectangle = lines[-1]
        ((x, y), (w, h), angle) = rectangle
        box = cv2.boxPoints(rectangle)
        box = np.int0(box)
        cv2.drawContours(cimg, [box], -1, (255, 255, 255), 5)
        x0, y0, angle_line = x, y, angle
    else:
        pass   
    # to get putter angle
    pimg[cv2.inRange(gray, 200, 255) == 0] = [0, 0, 0]
    pimg[rimg > 0 ] = [0,0,0]
    mask_white = cv2.inRange(pimg, np.array(
        [90, 90, 90]), np.array([255, 255, 255]))
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
            if 1/20 < w/h < 1/1.8 and w*h > 500:
                cv2.drawContours(pimg, [box], -1, (0, 255, 0), 1)
                boxes.append(rect)
    if len(boxes) >= 1:
        angles = list()
        for i in boxes:
            angles.append(i[2])
        average = sum(angles) / len(boxes)
        boxes = sorted(boxes, key=lambda rct: abs(average - rct[2]))
        rectanglep = boxes[0]
        ((x, y), (w, h), angle_putter) = rectanglep
        angel_putter = rectanglep[2]

    #checking angle
    theta = angle_line - angle_putter
    if abs(theta) > 45:
        theta = 90 - abs(theta)
        line_theta = math.radians(90 - angle_putter)
    else:
        theta = abs(theta)
        line_theta = math.radians(angle_putter)

    if  bool == True and theta > 3:
        print("fix angle!", theta)
        bool = False
    elif bool == False and theta <= 3:
        print("right angle!", theta)
        bool = True
    else:
        pass

    if bool == True:
        idx += 1
        cv2.line(cimg, (int(x0-500/math.tan(line_theta)),int(y0-500)), (int(x0+500/math.tan(line_theta)),int(y0+500)), (255, 0, 0), 5)
    elif bool == False:
        idx -= 1
        cv2.line(cimg, (int(x0-500/math.tan(line_theta)),int(y0-500)), (int(x0+500/math.tan(line_theta)),int(y0+500)), (0, 0, 255), 5)

    cv2.imshow("dst", cv2.resize(cimg,(0,0),None,fx=0.5, fy=0.5, interpolation=None))

    if cv2.waitKey(delay) == 27:
        break

video.release()
cv2.destroyAllWindows()
print("Your score is", int(idx/delay))