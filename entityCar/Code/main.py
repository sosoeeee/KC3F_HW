# encoding: utf-8
import numpy as np
import cv2
from driver import driver


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
    while True:
        _, frame = cap.read()
        # 图像同态滤波
        frame = cv2.pyrMeanShiftFiltering(frame, 10, 100)
        # 转换为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 高斯滤波
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        # 大津法二值化
        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # canny边缘检测
        canny = cv2.Canny(binary, 50, 150)
        cv2.imshow("image", canny)
        cv2.imshow("image1", binary)
        cv2.waitKey(3)
        car.setSpeed(0, 0)


if __name__ == "__main__":
    main()
