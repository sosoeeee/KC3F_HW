import cv2
import numpy as np


# 图像读入
img = cv2.imread("template/right.png")
# 灰度
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 改变大小
img = cv2.resize(img, (0, 0), fx=5, fy=5)

# 高斯滤波
img = cv2.GaussianBlur(img, (21, 21), 0)
img = cv2.GaussianBlur(img, (15, 15), 0)
# canny边缘检测
edg = cv2.Canny(img, 5, 11)
edg = cv2.GaussianBlur(edg, (5, 5), 0)

# # 截取图像
# edg = edg[150:290, 175:255]

# 显示图像
cv2.imshow("edg", edg)
cv2.waitKey(0)

# 储存图像
# cv2.imwrite("template/right_template.jpg", edg)
