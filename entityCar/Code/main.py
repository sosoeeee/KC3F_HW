# encoding: utf-8
import numpy as np
import cv2
from driver import driver
import undistortionLib
import time


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


class Path:
    def __init__(self):
        self.filter = False
        self.path = [[], [], []]
        self.filtedPath = [[], [], []]
        # 低通IIR滤波器参数
        self.b = [0.5, 0.3, 0.2]
        self.a = [0.5, 0.3, 0.2]

    def recPath(self, edgeImg, filter=False):
        self.filter = filter
        self.path[2] = self.path[1]
        self.path[1] = self.path[0]
        self.path[0] = []

        edgeImg_cut = edgeImg[140:480, 220:420]
        length, width = edgeImg_cut.shape
        # 提取轨迹点
        for y in range(0, length, 10):
            pointXSet = np.transpose(np.nonzero(edgeImg_cut[y, :]))
            if len(pointXSet) > 0:
                interestPoint = np.sum(pointXSet, axis=0) / len(pointXSet)
                self.path[0].append([int(interestPoint), y])

        if self.filter:
            self.filtedPath[2] = self.filtedPath[1]
            self.filtedPath[1] = self.filtedPath[0]
            self.filtedPath[0] = []

            if len(self.path[1]) > 0 and len(self.path[1]) > 0:
                self.filtedPath[0] = (self.b[0] * np.array(self.path[0])
                                      + self.b[1] * np.array(self.path[1])
                                      + self.b[2] * np.array(self.path[2])
                                      - self.a[1] * np.array(self.filtedPath[1])
                                      - self.a[2] * np.array(self.filtedPath[2])) / self.a[0]
                self.filtedPath[0] = self.filtedPath[0].tolist()
            else:
                self.filtedPath[0] = self.path[0]

    def filterPath(self):
        return self.filtedPath[0]

    def rawPath(self):
        return self.path[0]

    def drawPath(self, img):
        if self.filter:
            for point in self.filtedPath[0]:
                cv2.circle(img, (point[0], point[1]), 1, (0, 255, 0), 2)
        for point in self.path[0]:
            cv2.circle(img, (point[0], point[1]), 1, (0, 0, 255), 2)
        return img


def main():
    car = Car()
    cap = cv2.VideoCapture(0)
    lastTime = time.time()
    pathObserver = Path()
    while True:
        _, frame = cap.read()
        # 转换为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 相机畸变矫正
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
        length, width = canny_cut.shape
        # 轨迹提取
        pathObserver.recPath(canny_cut, filter=True)
        # path = pathObserver.filterPath()
        # path = pathObserver.rawPath()
        # 轨迹绘制
        color_gray = cv2.cvtColor(canny_cut, cv2.COLOR_GRAY2BGR)
        color_gray = pathObserver.drawPath(color_gray)

        cv2.imshow("image", color_gray)
        # cv2.imshow("image1", canny)
        cv2.waitKey(3)

        tmpTime = time.time()
        print(1 / (tmpTime - lastTime))
        lastTime = tmpTime

        car.setSpeed(0, 0)


if __name__ == "__main__":
    main()
