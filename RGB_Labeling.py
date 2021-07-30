import cv2
import numpy as np
import sys
import math
import Definitions as df
import erasing_background as eb

mod = sys.modules[__name__]
video = cv2.VideoCapture("Putting - 1.mp4")

if not video.isOpened():
    sys.exit()

delay = df.getDelay(video)
idx = 0
count = 0
while True:
    ret, img = video.read()

    if not ret:
        break
    img = cv2.GaussianBlur(img, (0, 0), 1.0)
    dst = cv2.inRange(img, np.array([90, 90, 90]), np.array([255, 255, 255]))

    src = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    _, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

    for x, y, w, h, area in stats:
        if (h, w) < dst.shape and 100 * 4 < w * h < 3000 * 4 and 2 / 3 < w / h < 4 / 3 and 0.8 < area / (
                0.25 * math.pi * w * h) < 1.2:
            cv2.rectangle(src, (x, y, w, h), (0, 0, 255), 1)



    cv2.imshow('dst', src)

    if cv2.waitKey(delay) == 27:
        break

video.release()
cv2.destroyAllWindows()
