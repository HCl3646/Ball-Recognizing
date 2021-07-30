import cv2
import numpy as np
import sys
import math
import finding_circle as fc
import erasing_background as eb


param = [20, 100, 1000, 10000]

img1 = cv2.imread('../ball3_2.jpg', cv2.IMREAD_GRAYSCALE)
src = img1.copy()

alpha = 0.8
img = np.clip((1 + alpha) * img1 - 128 * alpha, 0, 255).astype(np.uint8)

img = cv2.GaussianBlur(img, (0, 0), 1.0)

dst = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 5)
se = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
dst = cv2.dilate(dst, se)
dst = cv2.erode(dst, se)

contours, hierarchy = cv2.findContours(~dst, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
circle = fc.FindCircle(contours, param[0], param[1])

dst = eb.afterFindCircle(dst, circle)

contours, hierarchy = cv2.findContours(dst, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

ellipses = fc.FindEllipse(contours, src)

print(ellipses)

cv2.imshow('dst', dst)
cv2.imshow('~dst', src)

cv2.waitKey(0)
cv2.destroyAllWindows()

