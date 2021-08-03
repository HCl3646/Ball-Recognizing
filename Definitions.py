import cv2
import numpy as np
import math


def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)


def getDelay(video):
    fps = video.get(cv2.CAP_PROP_FPS)
    delay = round(1000 / fps)

    return delay


def getBack(video):
    _, back = video.read()
    background = cv2.cvtColor(back, cv2.COLOR_BGR2GRAY)
    background = cv2.GaussianBlur(background, (0, 0), 1.0)
    flback = background.astype(np.float32)

    return flback


def on_trackbar(pos):
    rmin = cv2.getTrackbarPos('minRadius', 'img')
    rmax = cv2.getTrackbarPos('maxRadius', 'img')
    th = cv2.getTrackbarPos('threshold', 'img')

    circles = cv2.HoughCircles(blr, cv2.HOUGH_GRADIENT, 1, 50, param1=120, param2=th, minRadius=rmin, maxRadius=rmax)

    dst = src.copy()
    if circles is not None:
        for i in range(circles.shape[1]):
            cx, cy, radius = circles[0][i]
            cv2.circle(dst, (int(cx), int(cy)), int(radius), (0, 0, 255), 2, cv2.LINE_AA)

    cv2.imshow('img', dst)


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def gradient(x1, y1, x2, y2):
    if abs((x1 - x2) / (y1 - y2)) >= 1:
        result = (x1 - x2) / (y1 - y2)
    else:
        result = (y1 - y2) / (x1 - x2)
    return result
