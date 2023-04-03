# encoding: utf-8
import numpy as np
import cv2

img = cv2.imread('cross.jpg')
# 图像缩放
img = cv2.resize(img, (640, 480))
# 转换为HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# 定义绿色的阈值
lower_green = np.array([35, 43, 46])
upper_green = np.array([77, 255, 255])

# 二值化
binary = cv2.inRange(hsv, lower_green, upper_green)

# 角点检测
# gray = np.float32(binary)
# dst = cv2.cornerHarris(gray, 8, 3, 0.15)
#
# img[dst > 0.4 * dst.max()] = [0, 0, 255]
# boolMar = dst > 0.4 * dst.max()
# loc = np.transpose(np.nonzero(boolMar))
# loc_filter = [loc[0]]
# print(loc)
# for i in range(len(loc)-1):
#     for point in loc_filter:
#         if abs(loc[i+1][0] - point[0]) < 10 and abs(loc[i+1][1] - point[1]) < 10:
#             break

# canny边缘检测
canny = cv2.Canny(binary, 50, 150)

direction = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
length, width = binary.shape
trace = [[]]
trace_k = 0

for i in range(length - 1, -1, -1):
    for j in range(width):
        if canny[i, j] == 255:
            trace[trace_k].append([j, i])
            canny[i, j] = 0
            k = 0
            while 1:
                for cnt in range(8):
                    k = k % 8
                    x = i + direction[k][0]
                    y = j + direction[k][1]
                    if length > x >= 0 and width > y >= 0:
                        if canny[x, y] == 255:
                            trace[trace_k].append([y, x])
                            canny[x, y] = 0
                            i = x
                            j = y
                            k = k - 2
                            break
                    k = k + 1

                if cnt == 7:
                    findOne = True
                    trace_k = trace_k + 1
                    trace.append([])
                    break

m = 0

# 在二值化图像上绘制轨迹
img = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
for i in range(len(trace)):
    for point in trace[i]:

        img = cv2.circle(img, point, 1, (0, 0, 255), 1)

print(m)
cv2.imshow("image", binary)
cv2.imshow("image1", img)
cv2.waitKey(0)

