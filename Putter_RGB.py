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

delay = df.getDelay(video)

while True:
    ret, img = video.read()

    if not ret:
        break

    cimg = ~img.copy()
    hsv = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    brown_lo = np.array([0, 85, 0])
    brown_hi = np.array([255, 255, 255])
    cdimg = cv2.Canny(img, 30, 255)

    mask = cv2.inRange(img, brown_lo, brown_hi)
    img[mask > 0] = [0,0,0]
  
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # alpha = 1.0
    # img = np.clip((1 + alpha) * img - 128 * alpha, 0, 255).astype(np.uint8)
    # img = cv2.GaussianBlur(img, (0, 0), 1.0)
    # _, dst = cv2.threshold(img, 70, 255, cv2.THRESH_BINARY)
    # # dst = cv2.adaptiveThreshold(~img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 5)
    # img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    # # cimg = cv2.cvtColor(~dst, cv2.COLOR_GRAY2BGR)

    img = cv2.GaussianBlur(img, (0, 0), 1.0)
    _, dst = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # dst = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 5)
    contours, _ = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    boxes = list()
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        ((x, y), (w, h), angle) = rect
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        if 3000 < w * h<100000 and 0.2< w/h <5:
            cv2.drawContours(cimg, [box], -1, (0,255,0),1)
            boxes.append(rect)
        if h != 0:
            if w/h > 10 or w/h < 0.1:
                cv2.drawContours(cimg, [box], -1, (255,0,0),3)
                angle_0 = angle

        
    if len(boxes) >= 1:
        boxes = sorted(boxes, key=lambda rct: rct[1][0] * rct[1][1] )
        rectangle = boxes[-1]
        ((x, y), (w, h), angle) = rectangle
        box = cv2.boxPoints(rectangle)
        box = np.int0(box)
        if w <= h:
            

    # _, labels, stats, centroids = cv2.connectedComponentsWithStats(~dst)
    # dst = cv2.cvtColor(~dst, cv2.COLOR_GRAY2BGR)
    # for i in range(len(stats)):
    #     x, y, w, h, area = stats[i]
    #     mx, my = centroids[i]
    #     cv2.rectangle(dst, (x, y, w, h), (0, 0, 255), 1)
    
    cv2.imshow("src" ,cimg)
    if cv2.waitKey(delay) == 27:
        break

video.release()
cv2.destroyAllWindows()