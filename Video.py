import sys
import numpy as np
import cv2
import time
import math
import finding_circle as fc
import erasing_background as eb
import Definitions as df

video = cv2.VideoCapture("tasks/Putting - 1.mp4")

if not video.isOpened():
    sys.exit()

delay = df.getDelay(video)

idx = 0
while True:
    ret, img2 = video.read()

    if not ret:
        break

    param = [5, 20]

    if idx % 10 == 0:
        src = img2.copy()
        src = cv2.resize(src, dsize=(0, 0), fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
        img1 = eb.BackGroundHSV(img2, [42, 0, 0], [80, 240, 240])
        img1 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
        img1 = cv2.resize(img1, dsize=(0, 0), fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)

        alpha = 1.0
        img = np.clip((1 + alpha) * img1 - 128 * alpha, 0, 255).astype(np.uint8)

        img = cv2.GaussianBlur(img, (0, 0), 1.0)

        dst = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 5)
        se = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        dst = cv2.dilate(dst, se)
        dst = cv2.erode(dst, se)

        contours, hierarchy = cv2.findContours(~dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        circle = fc.FindCircle(contours, param[0], param[1], src=dst)

        dst = eb.afterFindCircle(dst, circle)

        contours, hierarchy = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        ellipses = fc.FindEllipses(contours, src=src)

        if idx % 40 == 0:
            for cnt in ellipses:
                string = 'Center({1},{0}), Radius({3},{2})'.format(cnt[0][0], cnt[0][1], cnt[1][0], cnt[1][1])
                print(ellipses.index(cnt) + 1, string)
            print("\n")

    cv2.imshow('~dst', cv2.resize(src, dsize=(0, 0), fx=4.0, fy=4.0, interpolation=cv2.INTER_LINEAR))

    idx += 1

    if cv2.waitKey(delay) == 27:
        break

video.release()
cv2.destroyAllWindows()
