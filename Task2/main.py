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
              'yellow2': {'Lower': np.array([25, 100, 230]), 'Upper': np.array([45, 180, 255])},
              'white': {'Lower': np.array([0, 0, 200]), 'Upper': np.array([180, 30, 255])}}


# 使用前视角识别红块左转
def isLeftTurning(view1):
    # 路口识别
    # 出口标志牌
    # ori2=cv2.imread("./View218.jpg")
    flag1 = flag2 = 0
    # 可以设置上下限
    thres1 = 420
    thres2 = 100 * 0.56
    ori2 = view1
    size2 = ori2.shape
    roi2 = ori2[int(0 / 575 * size2[0]):int(300 / 575 * size2[0]),
           int(750 / 1023 * size2[1]):int(850 / 1023 * size2[1])]
    blur2 = cv2.GaussianBlur(roi2, (5, 5), 0)
    hsv_img2 = cv2.cvtColor(blur2, cv2.COLOR_BGR2HSV)
    kernel = np.ones((3, 3), dtype=np.uint8)
    erode_hsv2 = cv2.erode(hsv_img2, kernel, iterations=1)
    kernel = np.ones((3, 3), dtype=np.uint8)
    dilate_hsv2 = cv2.dilate(erode_hsv2, kernel, iterations=2)
    inRange_hsv2 = cv2.inRange(hsv_img2, color_dist['red']['Lower'], color_dist['red']['Upper'])
    sum_of_red = len((inRange_hsv2[inRange_hsv2 == 255]))
    if sum_of_red != 0:  print('sum_of_red', sum_of_red)
    if sum_of_red >= thres1:
        flag1 = 1
    # cv2.imshow("roi2", roi2)
    cv2.imshow("hsv2", inRange_hsv2)
    cv2.waitKey(1000)

    if flag1 == 1:
        return 1
    return 0


def isCrossing(view1):
    # 路口识别
    # 出口标志牌
    flag1 = 0
    # 可以设置上下限
    ori2 = view1
    size2 = ori2.shape
    roi2 = ori2[int(70 / 100 * size2[0]):int(80 / 100 * size2[0]), :]
    blur2 = cv2.GaussianBlur(roi2, (5, 5), 0)
    hsv_img2 = cv2.cvtColor(blur2, cv2.COLOR_BGR2HSV)
    inRange_hsv2 = cv2.inRange(hsv_img2, color_dist['white']['Lower'], color_dist['white']['Upper'])

    kernel = np.ones((5, 5), dtype=np.uint8)
    dilate_hsv2 = cv2.dilate(inRange_hsv2, kernel, iterations=3)
    kernel = np.ones((5, 5), dtype=np.uint8)
    erode_hsv2 = cv2.erode(dilate_hsv2, kernel, iterations=3)

    edgePicture = cv2.Canny(erode_hsv2, 50, 180)

    up_line = edgePicture[2, :]
    mid_line = edgePicture[int(len(edgePicture[:, 0]) / 2), :]
    bot_lien = edgePicture[len(edgePicture[:, 0]) - 2, :]

    up_white = len((up_line[up_line == 255]))
    mid_white = len((mid_line[mid_line == 255]))
    bot_white = len((bot_lien[bot_lien == 255]))
    print('sum_of_white', up_white, mid_white, bot_white)
    # cv2.imshow("hsv2", edgePicture)
    # cv2.waitKey(1000)

    if up_white > 8 and mid_white > 8 and bot_white > 8 and up_white + mid_white + bot_white < 48:
        print('find!')
        return 1
    else:
        print('NOT find!')
        return 0
    # if sum_of_white >= thres1:
    #     flag1 = 1
    # cv2.imshow("roi2", roi2)


# view2为左视角
def isRightTurning(viewback):
    # 可以设置上下限
    ori2 = viewback
    size2 = ori2.shape
    roi2 = ori2[int(75 / 100 * size2[0]):int(85 / 100 * size2[0]), :]
    blur2 = cv2.GaussianBlur(roi2, (5, 5), 0)
    hsv_img2 = cv2.cvtColor(blur2, cv2.COLOR_BGR2HSV)
    inRange_hsv2 = cv2.inRange(hsv_img2, color_dist['white']['Lower'], color_dist['white']['Upper'])

    kernel = np.ones((5, 5), dtype=np.uint8)
    dilate_hsv2 = cv2.dilate(inRange_hsv2, kernel, iterations=3)
    kernel = np.ones((5, 5), dtype=np.uint8)
    erode_hsv2 = cv2.erode(dilate_hsv2, kernel, iterations=3)

    edgePicture = cv2.Canny(erode_hsv2, 32, 180)

    up_line = edgePicture[2, :]
    mid_line = edgePicture[int(len(edgePicture[:, 0]) / 2), :]
    bot_lien = edgePicture[len(edgePicture[:, 0]) - 2, :]

    up_white = len((up_line[up_line == 255]))
    mid_white = len((mid_line[mid_line == 255]))
    bot_white = len((bot_lien[bot_lien == 255]))
    print('sum_of_white', up_white, mid_white, bot_white)
    # cv2.imshow("hsv2", edgePicture)
    # cv2.waitKey(1000)

    if up_white < 3 and mid_white < 3 and bot_white < 3:
        print('find!')
        return 1
    else:
        print('NOT find!')
        return 0


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
    viewFront = cv2.imdecode(view1, cv2.IMREAD_ANYCOLOR)
    viewBack = cv2.imdecode(view2, cv2.IMREAD_ANYCOLOR)
    viewLeft = cv2.imdecode(view3, cv2.IMREAD_ANYCOLOR)
    viewRight = cv2.imdecode(view4, cv2.IMREAD_ANYCOLOR)
    left_speed = 0
    right_speed = 0

    # create counter
    counter1 = counter(1)

    curState = state.get()
    # state machine
    if curState == 0:
        # 初始化状态1所需的计数器
        left_speed = 0
        right_speed = 0

        # 状态转移
        state.set(1)

    # 高速直行
    elif curState == 1:
        left_speed = 2
        right_speed = 2

        # 状态转移
        if isCrossing(viewFront):
            counter1.setCounter(25)
            state.set(2)

    # 低速直行
    elif curState == 2:
        left_speed = 1
        right_speed = 1

        # 状态转移
        if not counter1.isZero():
            counter1.updateCounter()
        else:
            if isRightTurning(viewBack):
                counter1.setCounter(15)
                state.set(4)

        # # 状态转移
        # if isLeftTurning(viewFront):
        #     counter1.setCounter(10)
        #     state.set(5)

    # 停车
    elif curState == 3:
        left_speed = 0
        right_speed = 0

        # # 状态转移
        # if isRightTurning(view1):
        #     state.set(3)

    # 右转
    elif curState == 4:
        counter1.updateCounter()
        left_speed = 1.7
        right_speed = 1.5

        if counter1.isZero():
            state.set(1)

    # 左转
    elif curState == 5:
        counter1.updateCounter()
        left_speed = 1
        right_speed = 1.1

        if counter1.isZero():
            state.set(1)

    print('cur state is', curState)
    # print('cur counter is', counter1.getVal())

    return left_speed, right_speed, 0, 0
