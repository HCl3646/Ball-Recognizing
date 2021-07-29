import cv2
import numpy as np
import sys
import math
import Definitions as df


def FindCircle(contours, radius1, radius2, src=None):
    circle = []
    circles = []
    for cnt in contours:

        (x, y), r = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        radius = int(r)

        if radius1 < radius < radius2:
            if src is None:
                circle.append([center, radius])
            else:
                if src[int(y)][int(x)] == 0:
                    continue
                else:
                    circle.append([center, radius])

    return circle


def FindEllipses(contours, src=None):
    ellipses = []
    for cnt in contours:

        if len(cnt) <= 4:
            continue

        ellipse = cv2.fitEllipse(cnt)

        if 4 * math.pi * cv2.contourArea(cnt, False) / (cv2.arcLength(cnt, True) ** 2) > 0.8:
            ellipses.append(ellipse)

            if src is None:
                continue
            else:
                cv2.ellipse(src, ellipse, (0, 0, 255), 1)

    return ellipses


def FindEllipse(contours, area1, area2, src=None):
    ellipses = []
    for cnt in contours:

        if len(cnt) <= 4:
            continue
        ellipse = cv2.fitEllipse(cnt)
        (x, y), (MA, ma), angle = ellipse

        if area1 < cv2.contourArea(cnt) < area2 and 1.1 > ma / MA > 0.9:
            ellipses.append(ellipse)

            if src is None:
                continue
            else:
                cv2.ellipse(src, ellipse, (0, 0, 255), 1)

    return ellipses
