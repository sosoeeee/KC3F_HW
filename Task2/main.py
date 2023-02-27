# make sure other custom functions and libs can be imported under given path
import cv2
import numpy as np
import base64
import math

log = []
slow = 5

color_dist = {'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([6, 255, 255])},
              'blue': {'Lower': np.array([80, 100, 120]), 'Upper': np.array([130, 220, 180])},
              'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
              'yellow': {'Lower': np.array([25, 160, 230]), 'Upper': np.array([45, 250, 255])},
              'yellow2': {'Lower': np.array([25, 100, 230]), 'Upper': np.array([45, 180, 255])}}


def Stall_detection(view3):
    # 车位识别
    thres = 1200
    ori1 = view3
    size1 = ori1.shape
    roi1 = ori1[int(150 / 575 * size1[0]):int(500 / 575 * size1[0]), int(800 / 1023 * size1[1]):]
    blur1 = cv2.GaussianBlur(roi1, (5, 5), 0)
    hsv_img1 = cv2.cvtColor(blur1, cv2.COLOR_BGR2HSV)
    kernel = np.ones((3, 3), dtype=np.uint8)
    erode_hsv1 = cv2.erode(hsv_img1, kernel, iterations=1)
    inRange_hsv1 = cv2.inRange(erode_hsv1, color_dist['yellow']['Lower'], color_dist['yellow']['Upper'])
    sum_of_yellow = len((inRange_hsv1[inRange_hsv1 == 255]))
    # cv2.imshow("roi1", roi1)
    # cv2.imshow("hsv1", inRange_hsv1)
    # cv2.waitKey(1000)
    print('sum_of_yellow', sum_of_yellow)
    # if sum_of_yellow > 0: print('sum_of_yellow',sum_of_yellow)
    if sum_of_yellow > thres:
        return 1
    return 0


def Crossing_detection(view2):
    # 路口识别
    # 出口标志牌
    # ori2=cv2.imread("./View218.jpg")
    flag1 = flag2 = 0
    thres1 = 420
    thres2 = 100 * 0.56
    ori2 = view2
    size2 = ori2.shape
    roi2 = ori2[int(0 / 575 * size2[0]):int(300 / 575 * size2[0]),
           int(750 / 1023 * size2[1]):int(850 / 1023 * size2[1])]
    blur2 = cv2.GaussianBlur(roi2, (5, 5), 0)
    hsv_img2 = cv2.cvtColor(blur2, cv2.COLOR_BGR2HSV)
    kernel = np.ones((3, 3), dtype=np.uint8)
    erode_hsv2 = cv2.erode(hsv_img2, kernel, iterations=1)
    kernel = np.ones((3, 3), dtype=np.uint8)
    dilate_hsv2 = cv2.dilate(erode_hsv2, kernel, iterations=2)
    inRange_hsv2 = cv2.inRange(dilate_hsv2, color_dist['blue']['Lower'], color_dist['blue']['Upper'])
    sum_of_blue = len((inRange_hsv2[inRange_hsv2 == 255]))
    if sum_of_blue != 0:  print('sum_of_blue', sum_of_blue)
    if sum_of_blue >= thres1:
        flag1 = 1
    # cv2.imshow("roi2", roi2)
    # cv2.imshow("hsv2", inRange_hsv2)
    # cv2.waitKey(1000)

    # 地面黄线
    roi3 = ori2[int(300 / 575 * size2[0]):int(500 / 575 * size2[0]),
           int(700 / 1023 * size2[1]):int(1000 / 1023 * size2[1])]
    blur3 = cv2.GaussianBlur(roi3, (5, 5), 0)
    hsv_img3 = cv2.cvtColor(blur3, cv2.COLOR_BGR2HSV)
    kernel = np.ones((3, 3), dtype=np.uint8)
    erode_hsv3 = cv2.erode(hsv_img3, kernel, iterations=2)
    kernel = np.ones((3, 3), dtype=np.uint8)
    dilate_hsv3 = cv2.dilate(erode_hsv3, kernel, iterations=1)
    inRange_hsv3 = cv2.inRange(dilate_hsv3, color_dist['yellow2']['Lower'], color_dist['yellow2']['Upper'])
    sum_of_white = len((inRange_hsv3[inRange_hsv3 == 255]))
    print(sum_of_white)
    if sum_of_white >= thres2:
        flag2 = 1
    # cv2.imshow("roi3", roi3)
    # cv2.imshow("hsv3", inRange_hsv3)

    if flag1 == 1:
        return 1
    return 0


def Crossing_detection2(view1):
    # 路口识别
    # 出口标志牌
    ori4 = view1
    thres = 340
    size4 = ori4.shape
    # print(size2)
    roi4 = ori4[int(0 / 575 * size4[0]):int(250 / 575 * size4[0]),
           int(200 / 1023 * size4[1]):int(500 / 1023 * size4[1])]
    blur4 = cv2.GaussianBlur(roi4, (5, 5), 0)
    hsv_img4 = cv2.cvtColor(blur4, cv2.COLOR_BGR2HSV)
    inRange_hsv4 = cv2.inRange(hsv_img4, color_dist['blue']['Lower'], color_dist['blue']['Upper'])
    kernel = np.ones((3, 3), dtype=np.uint8)
    erode_hsv4 = cv2.erode(inRange_hsv4, kernel, iterations=1)
    kernel = np.ones((3, 3), dtype=np.uint8)
    inRange_hsv4 = cv2.dilate(erode_hsv4, kernel, iterations=3)
    sum_of_white = len((inRange_hsv4[inRange_hsv4 == 255]))
    print('--', sum_of_white, '--')
    if sum_of_white >= thres:
        return 1
    return 0
    # cv2.imshow("ori4", ori4)
    # cv2.imshow("roi4", roi4)
    # cv2.imshow("hsv4", inRange_hsv4)


class counter:
    def __init__(self, index):
        self.index = index

    def setCounter(self, num):
        info = open('c' + str(self.index) + '.txt', 'w')
        info.write(str(num))
        info.close()

    def updateCounter(self):
        info = open('c' + str(self.index) + '.txt', 'r')
        curNum = int(info.read())
        info.close()
        info = open('c' + str(self.index) + '.txt', 'w')
        info.write(str(curNum - 1))
        info.close()

    def getVal(self):
        info = open('c' + str(self.index) + '.txt', 'r')
        return int(info.read())

    def isZero(self):
        info = open('c' + str(self.index) + '.txt', 'r')
        curNum = int(info.read())
        if curNum == 0:
            return True
        else:
            return False


def image_to_speed(view1, view2, view3, view4, state):
    view1 = cv2.imdecode(view1, cv2.IMREAD_ANYCOLOR)
    view2 = cv2.imdecode(view2, cv2.IMREAD_ANYCOLOR)
    view3 = cv2.imdecode(view3, cv2.IMREAD_ANYCOLOR)
    left_speed = 0
    right_speed = 0

    # create counter
    counter1 = counter(1)

    curState = state.get()
    # state machine
    if curState == 0:
        # 初始化状态1所需的计数器
        counter1.setCounter(18)
        left_speed = 0
        right_speed = 0

        # 状态转移
        state.set(curState + 1)

    # 直行
    elif curState == 1:
        counter1.updateCounter()
        left_speed = 2
        right_speed = 2

        # 状态转移
        if counter1.isZero():
            state.set(curState + 1)
            counter1.setCounter(9)

    # 右转
    elif curState == 2:
        counter1.updateCounter()
        left_speed = 1.789
        right_speed = 1.5

        if counter1.isZero():
            state.set(curState + 1)
            counter1.setCounter(120)

    elif curState == 3:
        counter1.updateCounter()
        left_speed = 3.0
        right_speed = 3.0

        if counter1.isZero():
            state.set(curState + 1)
            counter1.setCounter(9)

    elif curState == 4:
        counter1.updateCounter()
        left_speed = 1.5
        right_speed = 1.789

        if counter1.isZero():
            state.set(curState + 1)
            counter1.setCounter(20)

    elif curState == 5:
        counter1.updateCounter()
        left_speed = 3.0
        right_speed = 3.0

        if counter1.isZero():
            state.set(curState + 1)
            counter1.setCounter(10)

    elif curState == 6:
        # counter1.updateCounter()
        left_speed = 0
        right_speed = 0

        if counter1.isZero():
            state.set(curState + 1)
            counter1.setCounter(10)

    print('cur state is', curState)
    print('cur counter is', counter1.getVal())

    return left_speed, right_speed, 1, 1
