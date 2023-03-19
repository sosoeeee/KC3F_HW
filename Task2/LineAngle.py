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


class GlobalVariable:
    def __init__(self, name):
        self.name = name

    def SetVariable(self, value):
        info = open('variable' + name + '.txt', 'w')
        info.write(str(value))
        info.close()

    def GetVariable(self):
        info = open('variable' + name + '.txt', 'r')
        return float(info.read())

def VThin(image, array):
    rows, cols = image.shape
    NEXT = 1
    for i in range(rows):
        for j in range(cols):
            if NEXT == 0:
                NEXT = 1
            else:
                M = int(image[i, j - 1]) + int(image[i, j]) + int(image[i, j + 1]) if 0 < j < cols - 1 else 1
                if image[i, j] == 0 and M != 0:
                    a = [0] * 9
                    for k in range(3):
                        for l in range(3):
                            if -1 < (i - 1 + k) < rows and -1 < (j - 1 + l) < cols and image[
                                i - 1 + k, j - 1 + l] == 255:
                                a[k * 3 + l] = 1
                    sum = a[0] * 1 + a[1] * 2 + a[2] * 4 + a[3] * 8 + a[5] * 16 + a[6] * 32 + a[7] * 64 + a[8] * 128
                    image[i, j] = array[sum] * 255
                    if array[sum] == 1:
                        NEXT = 0
    return image


def HThin(image, array):
    rows, cols = image.shape
    NEXT = 1
    for j in range(cols):
        for i in range(rows):
            if NEXT == 0:
                NEXT = 1
            else:
                M = int(image[i - 1, j]) + int(image[i, j]) + int(image[i + 1, j]) if 0 < i < rows - 1 else 1
                if image[i, j] == 0 and M != 0:
                    a = [0] * 9
                    for k in range(3):
                        for l in range(3):
                            if -1 < (i - 1 + k) < rows and -1 < (j - 1 + l) < cols and image[
                                i - 1 + k, j - 1 + l] == 255:
                                a[k * 3 + l] = 1
                    sum = a[0] * 1 + a[1] * 2 + a[2] * 4 + a[3] * 8 + a[5] * 16 + a[6] * 32 + a[7] * 64 + a[8] * 128
                    image[i, j] = array[sum] * 255
                    if array[sum] == 1:
                        NEXT = 0
    return image


array = [0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1,
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1,
         0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1,
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1,
         1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1,
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1,
         0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1,
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
         1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
         1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0,
         1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0]


def GetAngle(img):
    ori2 = img
    size2 = ori2.shape
    roi2 = ori2[int(55 / 100 * size2[0]):int(99 / 100 * size2[0]), int(5 / 100 * size2[1]):int(50 / 100 * size2[1])]

    roi2 = cv2.resize(roi2, None, fx=0.5, fy=0.5)
    # cv2.imshow("hsv2", roi2)
    # cv2.waitKey(0)

    blur2 = cv2.GaussianBlur(roi2, (5, 5), 0)  # 高斯模糊
    hsv_img2 = cv2.cvtColor(blur2, cv2.COLOR_BGR2HSV)

    # # 闭运算填坑
    kernel = np.ones((3, 3), dtype=np.uint8)
    dilate_hsv2 = cv2.dilate(hsv_img2, kernel, iterations=5)
    kernel = np.ones((3, 3), dtype=np.uint8)
    erode_hsv2 = cv2.erode(dilate_hsv2, kernel, iterations=5)

    edge = cv2.Canny(erode_hsv2, 120, 180)

    inRange_hsv2 = cv2.inRange(erode_hsv2, color_dist['white']['Lower'], color_dist['white']['Upper'])
    sum_of_white = len((inRange_hsv2[inRange_hsv2 == 255]))
    cv2.bitwise_not(inRange_hsv2, inRange_hsv2)
    # if sum_of_white != 0:  print('sum_of_white', sum_of_white)
    # if sum_of_red >= thres1:
    #     flag1 = 1
    # cv2.imshow("roi2", roi2)
    for i in range(9):
        HThin(inRange_hsv2, array)
        VThin(inRange_hsv2, array)
    cv2.bitwise_not(inRange_hsv2, inRange_hsv2)
    lines = cv2.HoughLinesP(inRange_hsv2, 1, np.pi / 180, 60, None, 20, 5)
    # print(lines)

    angles = []

    displayImg = cv2.cvtColor(inRange_hsv2, cv2.COLOR_GRAY2BGR)
    if lines is None:
        return -1

    for idx in range(len(lines)):
        currentLine = lines[idx][0]
        # print(currentLine)
        cv2.line(displayImg, (currentLine[0], currentLine[1]), (currentLine[2], currentLine[3]), (0, 0, 255), 1)
        if currentLine[3] == currentLine[1]:
            angle = 90
        else:
            angle = np.arctan2(currentLine[1] - currentLine[3], currentLine[2] - currentLine[0]) * 180 / np.pi
        # print("angle:", angle)
        angles.append(angle)

    i = 0
    angSum = 0
    for ang in angles:
        angSum += ang
        i += 1
    outputAngle = angSum / i

    print(outputAngle)

    cv2.imshow("hsv2", displayImg)
    cv2.waitKey(0)
    return outputAngle


def GetAngleByVanishingPoint(img):
    lastErrorVariable = GlobalVariable("last_Error")
    lastError = lastErrorVariable.GetVariable()

    ori2 = img
    size2 = ori2.shape
    roi2 = ori2[int(1 / 100 * size2[0]):int(99 / 100 * size2[0]), int(1 / 100 * size2[1]):int(99 / 100 * size2[1])]

    # roi2 = cv2.resize(roi2, None, fx=0.5, fy=0.5)
    # cv2.imshow("hsv2", roi2)
    # cv2.waitKey(0)

    hsv_img2 = cv2.cvtColor(roi2, cv2.COLOR_BGR2GRAY)
    blur2 = cv2.GaussianBlur(hsv_img2, (5, 5), 0)  # 高斯模糊
    # cv2.imshow("img1", roi2)
    # cv2.imshow("img2", hsv_img2)

    # 闭运算填坑
    # kernel = np.ones((3, 3), dtype=np.uint8)
    # dilate_hsv2 = cv2.dilate(blur2, kernel, iterations=5)
    # kernel = np.ones((3, 3), dtype=np.uint8)
    # erode_hsv2 = cv2.erode(dilate_hsv2, kernel, iterations=5)

    edge = cv2.Canny(blur2, 30, 80)

    Lines = cv2.HoughLinesP(edge, 1, np.pi / 180, 50, 10, 15)
    if Lines is None:
        print("No line in roi")
        return 0

    #### displaying
    # displayImg = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)
    # for idx in range(len(Lines)):
    #     currentLine = Lines[idx][0]
    #     # print(currentLine)
    #     cv2.line(displayImg, (currentLine[0], currentLine[1]), (currentLine[2], currentLine[3]), (0, 0, 255), 1)
    # cv2.imshow("img", displayImg)
    # cv2.waitKey(0)

    REJECT_DEGREE_TH = 4.0
    FilteredLines = []  # Filtered lines will be stored here
    for Line in Lines:  # Iterating over each line
        [[x1, y1, x2, y2]] = Line  # Getting the coordinates of the line
        # Calculating equation of the line: y = mx + c
        # if x1 != x2, slope can be found using regular equation
        if x1 != x2:
            m = (y2 - y1) / (x2 - x1)
            # if x1 = x2, slope is infinity, thus a large value
        else:
            m = 10000
        c = y2 - m * x2  # c = y - mx from the equation of line
        # theta will contain values between -90 -> +90.
        theta = math.degrees(math.atan(m))
        # Storing lines of slope not near to 0 degree or +-90 degree
        if REJECT_DEGREE_TH <= abs(theta) <= (90 - REJECT_DEGREE_TH):
            # length of the line
            l = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
            FilteredLines.append([x1, y1, x2, y2, m, c, l])

    if len(FilteredLines) > 15:  # if more than 15 lines are there
        # Sorting lines wrt their length in decreasing order
        FilteredLines = sorted(FilteredLines, key=lambda x: x[-1], reverse=True)
        # Taking only the longest 15 lines
        FilteredLines = FilteredLines[:15]

    Lines = FilteredLines
    # Initializing variables
    VanishingPoint = None  # Coordinates of the vanishing point
    MinError = 100000000000  # Minimum error found (initially large value)

    for i in range(len(Lines)):  # Iterating over lines and taking 2 at once
        for j in range(i + 1, len(Lines)):
            # Reading m and c values of the line
            m1, c1 = Lines[i][4], Lines[i][5]
            # Reading m and c values of the line
            m2, c2 = Lines[j][4], Lines[j][5]
            # If lines are not parallel
            if m1 != m2:
                # Finding (x0, y0)
                x0 = (c1 - c2) / (m2 - m1)
                y0 = m1 * x0 + c1
                err = 0  # Error of this point
                # Iterating over all lines for error calculation
                for k in range(len(Lines)):
                    # Reading m and c value of the line L
                    m, c = Lines[k][4], Lines[k][5]
                    # Calculation m and c of L_
                    m_ = (-1 / m)
                    c_ = y0 - m_ * x0
                    # Calculating (x_, y_) - point of intersection of L and L_
                    x_ = (c - c_) / (m_ - m)
                    y_ = m_ * x_ + c_
                    # Calculation distance between (x0, y0) and (x_, y_)
                    l = math.sqrt((y_ - y0) ** 2 + (x_ - x0) ** 2)
                    err += l ** 2  # Adding to error value
                err = math.sqrt(err)  # Finally taking sq root of error
                # Comparing with minimum error value till now
                # If present error value is lesser, updating minimum error value
                # and vanishing point coordinates.
                if MinError > err:
                    MinError = err
                VanishingPoint = [x0, y0]

    print(VanishingPoint)
    print(edge.shape)

    ### displaying
    displayImg = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)
    # cv2.circle(displayImg, (int(VanishingPoint[0]), int(VanishingPoint[1])), 1, (0, 0, 255), -1)
    # cv2.imshow("img", displayImg)
    # cv2.waitKey(0)
    if VanishingPoint is None:
        angleError = 0
    else:
        angle = math.atan2(VanishingPoint[1], VanishingPoint[0] - edge.shape[1] / 2)
        angleError = math.pi/2 - angle
    print(angleError)

    if abs(lastError - angleError) > 0.4:
        angleError = lastError

    lastErrorVariable.SetVariable(angleError)
    return angleError


if __name__ == '__main__':
    image = cv2.imread(r"C:\Users\wzj\Desktop\View1.jpg")
    GetAngleByVanishingPoint(image)
