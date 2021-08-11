import math
import sys
import cv2
import numpy as np
import Definitions as df
import erasing_background as eb
from openpyxl import Workbook

video = cv2.VideoCapture("tasks\Putting_Pratice.mp4")

if not video.isOpened():
    sys.exit()

delay = df.getDelay(video)

while True:
    ret, img = video.read()

    if not ret:
        break
    cimg = img.copy()
    brown_lo = np.array([100, 100, 100])
    brown_hi = np.array([255, 255, 255])

    mask = cv2.inRange(img, brown_lo, brown_hi)
    img[mask > 0] = [0, 0, 0]

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (0,0), 1.0)
    _, dst = cv2.threshold(img, 70, 255, cv2.THRESH_BINARY)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    contours, _ = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    boxes = list()
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        boxes.append(rect)

    boxes = sorted(boxes, key=lambda rct: rct[1][0] * rct[1][1])
    rectangle = boxes[-1]
    ((x, y), (w, h), angle) = rectangle
    box = cv2.boxPoints(rectangle)
    box = np.int0(box)
    cv2.drawContours(cimg, [box], -1, (0, 255, 0), 1)
    print(angle)

    cv2.imshow("src", cimg)
    if cv2.waitKey(delay) == 27:
        cv2.imwrite("putting_1.jpg", cimg)
        break

video.release()
cv2.destroyAllWindows()
