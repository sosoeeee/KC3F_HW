import math
import cv2
import numpy as np
import LineAngle

kp = 0.03
ki = 0
kd = 0
setpoint = 2


def isStraight(imageFront):
    angle_now = 0
    angle_set = 20
    delta = 0
    delta_sum = 0

    # ori = cv2.read("./pic.jpg")

    # ori = view1
    # size = ori.shape
    # roi2 = ori[int(0 / 575 * size[0]):int(300 / 575 * size[0]),
    #        int(750 / 1023 * size[1]):int(850 / 1023 * size[1])]
    # blur2 = cv2.GaussianBlur(roi2, (5, 5), 0)
    # hsv_img2 = cv2.cvtColor(blur2, cv2.COLOR_BGR2HSV)
    # kernel = np.ones((3, 3), dtype=np.uint8)
    # erode_hsv2 = cv2.erode(hsv_img2, kernel, iterations=1)
    # kernel = np.ones((3, 3), dtype=np.uint8)
    # dilate_hsv2 = cv2.dilate(erode_hsv2, kernel, iterations=2)

    #  cv2.imshow("roi2", roi2)

    # 补识别angle_now的代码
    # **********
    # angle_now = LineAngle.GetAngle(image1)
    # delta_before = angle_set - angle_now

    # 识别现在的delta
    # **********
    angle_now = LineAngle.GetAngle(imageFront)

    if angle_now is -1:
        return setpoint, setpoint
    else:
        delta = angle_set - angle_now
        # **********

        delta_sum += delta
        speedDiff = kp * delta + ki * delta_sum
        if speedDiff > 0.5:
            speedDiff = 0.5
        elif speedDiff < -0.5:
            speedDiff = -0.5
        angle_left = setpoint - speedDiff
        angle_right = setpoint + speedDiff
        delta_before = delta

        return angle_left, angle_right
