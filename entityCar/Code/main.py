# encoding: utf-8
import numpy as np
import cv2
from driver import driver
import undistortionLib
import time


def findLine(img, grayFlag=False):
    if grayFlag:
        # 大津法二值化
        ret, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    else:
        binary = img
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
                        if len(trace[trace_k]) < 10:
                            trace.pop()
                            trace.append([])
                        else:
                            trace_k = trace_k + 1
                            trace.append([])
                        break

    return trace


class Car:
    def __init__(self):
        self.car = driver()

    def setSpeed(self, x, y):
        self.car.set_speed(x, y)

    def readBattery(self):
        return self.car.read_battery()


# PID class
class PID:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.last_error = 0
        self.integral = 0

    def update(self, error, dt):
        self.integral += error * dt
        derivative = (error - self.last_error) / dt
        self.last_error = error
        return self.kp * error + self.ki * self.integral + self.kd * derivative

    def reset(self):
        self.last_error = 0
        self.integral = 0


def main():
    car = Car()
    cap = cv2.VideoCapture(0)
    lastTime = time.time()
    while True:
        _, frame = cap.read()
        # 转换为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        caliber_gray = undistortionLib.grayUndistort(gray)
        # 大津法二值化
        ret, binary = cv2.threshold(caliber_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # 二值化闭运算
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        # canny边缘检测
        canny = cv2.Canny(binary, 50, 150)
        # 提取图像局部
        canny_cut = canny[140:480, 220:420]
        color_gray = cv2.cvtColor(canny_cut, cv2.COLOR_GRAY2BGR)
        length, width = canny_cut.shape
        interestPointSet = []
        for y in range(0, length, 10):
            pointXSet = np.transpose(np.nonzero(canny_cut[y, :]))
            if len(pointXSet) > 0:
                interestPoint = np.sum(pointXSet, axis=0) / len(pointXSet)
                interestPointSet.append((int(interestPoint), y))
        # print(interestPointSet)

        # # Hough直线检测
        # lines = cv2.HoughLinesP(canny, 1, np.pi / 180, 100, minLineLength=40, maxLineGap=20)
        # # 绘制直线
        # if lines is not None:
        #     for line in lines:
        #         x1, y1, x2, y2 = line[0]
        #         cv2.line(color_gray, (x1, y1), (x2, y2), (0, 0, 255), 2)

        for point in interestPointSet:
            cv2.circle(color_gray, point, 1, (0, 0, 255), 2)

        cv2.imshow("image", color_gray)
        # cv2.imshow("image1", canny)
        cv2.waitKey(3)

        tmpTime = time.time()
        print(1 / (tmpTime - lastTime))
        lastTime = tmpTime

        car.setSpeed(0, 0)


if __name__ == "__main__":
    main()
