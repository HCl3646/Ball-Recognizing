import cv2
import numpy as np
import sys
import math
import Definitions as df
import erasing_background as eb

mod = sys.modules[__name__]
video = cv2.VideoCapture("Golf_Test_1.mp4")

if not video.isOpened():
    sys.exit()

delay = df.getDelay(video)
idx = 0
count = 0
ball = []
while True:
    ret, img = video.read()

    if not ret:
        break
    img = cv2.GaussianBlur(img, (0, 0), 1.0)
    dst = cv2.inRange(img, np.array([90, 90, 90]), np.array([255, 255, 255]))

    src = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    _, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
    pts = []
    for i in range(len(stats)):
        x, y, w, h, area = stats[i]
        mx, my = centroids[i]
        if (h, w) < dst.shape and 400 * 4 < w * h < 3000 * 4 and 2 / 3 < w / h < 4 / 3 and 0.8 < area / (0.25 * math.pi * w * h) < 1.2:
            cv2.rectangle(src, (x, y, w, h), (0, 0, 255), 1)
            cv2.line(src, (int(mx), int(my)), (int(mx), int(my)), (0, 0, 255), 3)
            point = (int(mx), int(my), idx)
            pts.append(point)
            cv2.putText(src, str(pts.index(point)), (int(mx) + 1, int(my) - 1), 0, 1, (0, 255, 0), 1, cv2.LINE_AA, False)
    for p in pts:
        cnt = 0
        for j in ball:
            length = df.distance(j[len(j) - 1][0], j[len(j) - 1][1], p[0], p[1])
            if length > 100:
                cnt += 1
            elif length < 4:
                break
            else:
                j.append((p[0],p[1]))
                break
        if cnt == len(ball):
            ball.append([p])
            count += 1


    cv2.imshow('dst', src)
    idx += 1

    if cv2.waitKey(delay) == 27:
        break

video.release()
cv2.destroyAllWindows()
for i in ball:
    print(i)
