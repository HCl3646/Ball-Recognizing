import cv2
import numpy as np
import sys
import math


def afterFindCircle(src, circle):
    for y in range(len(src)):
        for x in range(len(src[y])):
            count = 0
            for cnt in circle:
                formula = (y - cnt[0][1]) ** 2 + (x - cnt[0][0]) ** 2
                if formula > (cnt[1])**2:
                    count += 1

            if count == len(circle):
                src[y][x] = 0
    return src


def BackGroundHSV(img, low, high):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (0, 0), 1.0)

    color_lo = np.array(low)
    color_hi = np.array(high)

    mask = cv2.inRange(hsv, color_lo, color_hi)

    img[mask > 0] = [0, 0, 0]

    return img