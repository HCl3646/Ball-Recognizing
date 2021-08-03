import math
import sys
import cv2
import numpy as np
import Definitions as df
import erasing_background as eb

mod = sys.modules[__name__]
video = cv2.VideoCapture("Golf_Test_1.mp4")

if not video.isOpened():
    sys.exit()

delay = df.getDelay(video)
idx, count, score, score_0 = np.zeros(4)
balls = list()
while True:
    ret, img = video.read()

    if not ret:
        break

    img = cv2.GaussianBlur(img, (0, 0), 1.0)
    dst = cv2.inRange(img, np.array([90, 90, 90]), np.array([255, 255, 255]))
    src = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    _, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
    pts = list()

    for i in range(len(stats)):
        x, y, w, h, area = stats[i]
        mx, my = centroids[i]
        if (h, w) < dst.shape and 500 * 4 < w * h < 3000 * 4 and 2 / 3 < w / h < 4 / 3 and 0.8 < area / (
                0.25 * math.pi * w * h) < 1.2:
            cv2.rectangle(src, (x, y, w, h), (0, 0, 255), 1)
            cv2.line(src, (int(mx), int(my)), (int(mx), int(my)), (0, 0, 255), 3)
            point = (mx, my, idx)
            pts.append(point)
            cv2.putText(src, str(pts.index(point)), (int(mx) + 1, int(my) - 1), 0, 1, (0, 255, 0), 1, cv2.LINE_AA,
                        False)
                        
    for p in pts:
        cnt = 0
        length_0 = 9999999999
        temp = list()
        boolean = True
        for j in balls:
            length = df.distance(j[ - 1][0], j[- 1][1], p[0], p[1])
            if length > 200:
                cnt += 1
            elif length < 10:
                boolean = False
                break
            else:
                if length <= length_0:
                    length_0 = length
                    temp = j
                else:
                    continue
        if cnt == len(balls):
            balls.append([p])
            count += 1
        elif boolean is True and cnt != len(balls):
            temp.append(p)
        else:
            continue

    # 오랜시간 가만히 있던 공이 움직이는거 체크하는 것도 나쁘지 않을수도
    for i in balls:
        if len(i) >= 2 and idx == i[-1][2]:
            if len(i) >= 3 and df.distance(i[-1][0], i[-1][1], i[-2][0], i[-2][1]) >= 12:
                g0 = df.gradient(i[- 2][0], i[- 2][1], i[- 3][0], i[- 3][1])
                g1 = df.gradient(i[- 1][0], i[- 1][1], i[- 2][0], i[- 2][1])
                if abs(math.atan(g0)-math.atan(g1)) >= math.pi/12 :
                    score += 1
                    break
                    
            elif i[-1][2] - i[-2][2] > delay * 7:
                score += 1
                break
    
    cv2.imshow('dst', src)
    idx += 1
    if score != score_0:
        print(int(score), int(idx))
        score_0 = score
        cv2.imwrite("images/img_{}.jpg".format(int(idx)),src)

    if cv2.waitKey(delay) == 27:
        break

video.release()
cv2.destroyAllWindows()