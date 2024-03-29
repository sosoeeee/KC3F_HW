# encoding: utf-8
import numpy as np
import cv2
from driver import driver
import undistortionLib
import time
from letterRec import *
from circleRec import *


class Car:
    def __init__(self):
        self.car = driver()

    def setSpeed(self, x, y):
        self.car.set_speed(x, y)

    def readBattery(self):
        return self.car.read_battery()


car = Car()


# PID class
class PID:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.lastError = 0
        self.sumError = 0

    def update(self, error):
        self.sumError += error
        deltaError = error - self.lastError
        self.lastError = error
        return self.kp * error + self.ki * self.sumError + self.kd * deltaError


def GetWheelSpeed(dots, centre, para, controller):
    dots[:, 0] = dots[:, 0] - centre
    # print(para)
    # controlVariable = np.dot(dots[:, 0], para) * 0.15  # 误差为正需要右转，左轮加速
    error = np.dot(dots[:, 0], para)
    controlVariable = controller.update(error)
    # print(controlVariable)
    lSpeed = 15 - controlVariable
    rSpeed = 15 + controlVariable

    if lSpeed > 25:
        lSpeed = 25
    if rSpeed > 25:
        rSpeed = 25

    return [lSpeed, rSpeed]
    # return [0, 0]


class Path:
    def __init__(self):
        self.filter = False
        self.path = [[], [], []]
        self.filtedPath = [[], [], []]
        # 低通IIR滤波器参数
        self.b = [0.3913, 0.7827, 0.3913]
        self.a = [1, 0.3695, 0.1958]

    def recPath(self, edgeImg, filter=False):
        self.filter = filter
        self.path[2] = self.path[1]
        self.path[1] = self.path[0]
        self.path[0] = []

        length, width = edgeImg.shape
        for y in range(0, length, 10):
            pointXSet = np.transpose(np.nonzero(edgeImg[y, :]))
            if len(pointXSet) > 0:
                interestPoint = np.sum(pointXSet, axis=0) / len(pointXSet)
                self.path[0].append([int(interestPoint), y])

        if self.filter:
            self.filtedPath[2] = self.filtedPath[1]
            self.filtedPath[1] = self.filtedPath[0]
            self.filtedPath[0] = []

            if len(self.path[1]) == len(self.path[0]) and len(self.path[2]) == len(self.path[0]):
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
                cv2.circle(img, (int(point[0]), int(point[1])), 1, (0, 255, 0), 2)
        for point in self.path[0]:
            cv2.circle(img, (point[0], point[1]), 1, (0, 0, 255), 2)
        return img


def timerTurn(speed, direct, t):
    startTime = time.time()
    if direct:
        speed = speed
    else:
        speed = -speed
    while (time.time() - startTime) < t:
        car.setSpeed(speed, -speed)


def timerStraight(speed, t):
    startTime = time.time()
    while (time.time() - startTime) < t:
        car.setSpeed(speed, speed)


def crossRec(binaryImg):
    # 检测十字路口
    crossFlag = False
    # Harris角点检测
    dst = cv2.cornerHarris(binaryImg, 10, 3, 0.18)

    # # 绘图
    # color_gray = cv2.cvtColor(binaryImg, cv2.COLOR_GRAY2BGR)
    # color_gray[dst > 0.4 * dst.max()] = [0, 0, 255]
    # cv2.imshow('dst', color_gray)
    # cv2.waitKey(1)

    boolMar = dst > 0.4 * dst.max()
    loc = np.transpose(np.nonzero(boolMar))
    loc_filter = []
    if len(loc) > 0:
        loc_filter = [loc[0]]
        for i in range(len(loc) - 1):
            nearPoint = False
            for point in loc_filter:
                if abs(loc[i + 1][0] - point[0]) < 10 and abs(loc[i + 1][1] - point[1]) < 10:
                    nearPoint = True
                    break
            if not nearPoint:
                loc_filter.append(loc[i + 1])

    # print(len(loc_filter))

    if len(loc_filter) == 4:
        avrPoint = np.sum(loc_filter, axis=0) / 4
        if avrPoint[0] > 100:
            crossFlag = True

    return crossFlag


def main():
    global car
    cap = cv2.VideoCapture(0)
    lastTime = time.time()
    pathObserver = Path()
    controller = PID(0.07, 0, 1)

    # STATE = {'normal', 'wall', 'cross'}
    state = 'normal'

    left_template = cv2.imread("template/left_template.jpg")
    left_template = cv2.cvtColor(left_template, cv2.COLOR_BGR2GRAY)
    right_template = cv2.imread("template/right_template.jpg")
    right_template = cv2.cvtColor(right_template, cv2.COLOR_BGR2GRAY)

    wallRecTimer = time.time()

    while True:
        currentTime = time.time()
        # 图像采集
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
        binary_ROI = binary[140:480, 220:420]

        # 图像显示
        canny = cv2.Canny(binary_ROI, 50, 150)
        color_gray = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)

        if state == 'normal':
            # 巡线轨迹提取
            # canny边缘检测
            canny = cv2.Canny(binary_ROI, 50, 150)
            # 提取图像局部
            length, width = canny.shape
            # 轨迹提取
            pathObserver.recPath(canny, filter=True)
            # path = pathObserver.filterPath()
            path = pathObserver.rawPath()

            # 轨迹绘制来显示图像
            color_gray = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)
            color_gray = pathObserver.drawPath(color_gray)

            # 检测十字路口
            crossFlag = crossRec(binary_ROI[100:339, :])

            # 检测墙面
            if currentTime - wallRecTimer > 4:
                wallROI = caliber_gray[:, 220:420]
                wallFlag, frame = wallRec(wallROI)
            else:
                wallFlag = False

            # 轨迹控制
            if len(path) > 0:
                # 计算轨迹中心
                path = np.array(path)
                centre = int(width / 2)
                # 计算轨迹方向
                weight = float(1.0 / len(path))
                para = np.ones(len(path)) * weight
                # 计算轮速
                wheelSpeed = GetWheelSpeed(path, centre, para, controller)
                # 控制小车
                car.setSpeed(wheelSpeed[0], wheelSpeed[1])

            if crossFlag:
                print('cross')
                state = 'cross'
                car.setSpeed(0, 0)

            if wallFlag:
                state = 'wall'
                car.setSpeed(0, 0)

        elif state == 'cross':
            # Hough圆检测
            flag, frame = circleRec(caliber_gray)

            if flag:
                if getLetterRec(frame, left_template, right_template) == '左':
                    print('left')
                    timerStraight(25, 2)
                    timerTurn(25, 1, 1.4)
                    state = 'normal'
                else:
                    print('right')
                    timerStraight(25, 2)
                    timerTurn(25, 0, 1.4)
                    state = 'normal'
            else:
                state = 'normal'

        elif state == 'wall':
            timerTurn(25, 0, 1.4)
            timerStraight(25, 2)
            timerTurn(25, 1, 1.4)
            timerStraight(25, 4)
            timerTurn(25, 1, 1.4)
            timerStraight(25, 2)
            timerTurn(25, 0, 1.2)
            print('finish')
            cv2.destroyAllWindows()
            wallRecTimer = time.time()
            state = 'normal'

        # cv2.imshow("image", color_gray)
        # 显示图像
        cv2.imshow("image1", caliber_gray[:, 220:420])
        cv2.waitKey(1)

        # tmpTime = time.time()
        # print(1 / (tmpTime - lastTime))
        # lastTime = tmpTime


if __name__ == "__main__":
    main()
