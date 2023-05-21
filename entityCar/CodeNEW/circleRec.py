# coding=utf-8
import numpy as np
import cv2
import undistortionLib as undistort
import os

# left = "template/left_template.jpg"
# right = "template/right_template.jpg"
# template_left = cv2.imread(left)
#
# template_right = cv2.imread(right)
#
# # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# template_left = cv2.cvtColor(template_left, cv2.COLOR_BGR2GRAY)
# template_right = cv2.cvtColor(template_right, cv2.COLOR_BGR2GRAY)
# list = []
# for i in range(2):
#     list.append(str(i))
#
# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))  # 前一个代表用4个字符表示的视频编码格式  #后一个为保存的视频格式
#
# # ret = cap.set(3, 640)  # 设置帧宽
# # ret = cap.set(4, 480)  # 设置帧高
# font = cv2.FONT_HERSHEY_SIMPLEX  # 设置字体样式
# kernel = np.ones((5, 5), np.uint8)  # 卷积核


def circleRec(image):
    # 读取图片
    # image = cv2.imread(image_path)
    # 转换为灰色通道
    flag = 0
    kernel = np.ones((5, 5), np.uint8)  # 卷积核
    font = cv2.FONT_HERSHEY_SIMPLEX
    frame = image

    #  消除噪声
    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)  # 形态学开运算
    edges = cv2.Canny(opening, 50, 100)  # 边缘识别
    # 识别圆形
    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=15, maxRadius=35)
    if circles is not None:  # 如果识别出圆
        for circle in circles[0]:
            #  获取圆的坐标与半径
            x = int(circle[0])
            y = int(circle[1])
            r = int(circle[2])

            size = frame.shape
            # if y -  r > 0 and y +  r < size[0] and x -  r > 0 and x +  r < size[1]:
            if y - 1.5 * r > 0 and y + 1.5 * r < size[0] and x - 1.5 * r > 0 and x + 1.5 * r < size[1]:
                frame = frame[int(y - 1.5 * r):int(y + 1.5 * r), int(x - 1.5 * r):int(x + 1.5 * r)]
                flag = 1
                print(frame.shape)
                cv2.imshow('frame', frame)
                cv2.waitKey(100)
    else:
        # 如果识别不出，显示圆心不存在
        # cv2.putText(frame, 'x: None y: None', (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA, 0)
        # cv2.destroyAllWindows()
        flag = 0

    return flag, frame


def wallRec(image):
    # 读取图片
    # image = cv2.imread(image_path)
    # 转换为灰色通道
    flag = 0
    kernel = np.ones((5, 5), np.uint8)  # 卷积核
    font = cv2.FONT_HERSHEY_SIMPLEX
    frame = image

    #  消除噪声
    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)  # 形态学开运算
    edges = cv2.Canny(opening, 50, 100)  # 边缘识别
    # 识别圆形
    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, 20, param1=80, param2=40, minRadius=15, maxRadius=55)
    if circles is not None:  # 如果识别出圆
        for circle in circles[0]:
            #  获取圆的坐标与半径
            x = int(circle[0])
            y = int(circle[1])
            r = int(circle[2])

            size = frame.shape
            # if y -  r > 0 and y +  r < size[0] and x -  r > 0 and x +  r < size[1]:
            if y - 1.5 * r > 0 and y + 1.5 * r < size[0] and x - 1.5 * r > 0 and x + 1.5 * r < size[1]:
                frame = frame[int(y - 1.5 * r):int(y + 1.5 * r), int(x - 1.5 * r):int(x + 1.5 * r)]
                flag = 1
                print(frame.shape)
                cv2.imshow('frame', frame)
                cv2.waitKey(100)
    else:
        # 如果识别不出，显示圆心不存在
        # cv2.putText(frame, 'x: None y: None', (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA, 0)
        # cv2.destroyAllWindows()
        flag = 0

    return flag, frame


# def process_image(image, index):
#     # 读取图片
#     # image = cv2.imread(image_path)
#     # 转换为灰色通道
#     flag = 0
#     kernel = np.ones((5, 5), np.uint8)  # 卷积核
#     font = cv2.FONT_HERSHEY_SIMPLEX
#     frame = image
#     # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 转换为灰色通道
#     # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # 转换为HSV空间
#
#     #  消除噪声
#     opening = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)  # 形态学开运算
#     bila = cv2.bilateralFilter(opening, 10, 100, 200)  # 双边滤波消除噪声
#     edges = cv2.Canny(opening, 50, 100)  # 边缘识别
#     # 识别圆形
#     circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=15, maxRadius=35)
#     if circles is not None:  # 如果识别出圆
#         for circle in circles[0]:
#             #  获取圆的坐标与半径
#             x = int(circle[0])
#             y = int(circle[1])
#             r = int(circle[2])
#             # cv2.circle(frame, (x, y), r, (0, 255, 0), 3)  # 标记圆
#             # cv2.circle(frame, (x, y), 6, (255, 255, 0), -1)  # 标记圆心
#             # text = 'x:  ' + str(x) + ' y:  ' + str(y)
#             # cv2.putText(frame, text, (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA, 0)  # 显示圆心位置
#             # 以圆心为中心，截取半径大小的图片
#             size = frame.shape
#             # if y -  r > 0 and y +  r < size[0] and x -  r > 0 and x +  r < size[1]:
#             if y - 1.5 * r > 0 and y + 1.5 * r < size[0] and x - 1.5 * r > 0 and x + 1.5 * r < size[1]:
#                 frame = frame[int(y - 1.5 * r):int(y + 1.5 * r), int(x - 1.5 * r):int(x + 1.5 * r)]
#                 flag = 1
#                 print(frame.shape)
#                 cv2.imshow('frame', frame)
#                 cv2.waitKey(100)
#                 # print("find")
#
#             # frame = frame[y - r:y + r, x - r:x + r]
#             '''flag=1
#             cv2.imshow('frame', frame)
#             cv2.waitKey(100)
#             print(flag)'''
#
#             # cv2.imwrite("Graphs2/{}.png".format(index), frame)
#             # index += 1
#     else:
#         # 如果识别不出，显示圆心不存在
#         cv2.putText(frame, 'x: None y: None', (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA, 0)
#         # cv2.imshow('frame', frame)
#
#         cv2.destroyAllWindows()
#         # cv2.imshow('edges', edges)
#         flag = 0
#         # print(flag)
#
#     return flag, frame, index
#
#
# if cap.isOpened() is True:  # 检查摄像头是否正常启动
#     index = 0
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if frame is None:
#             continue
#         image_path = "D:/huofuyuan.jpg"
#         image = cv2.imread(image_path)
#         image = np.array(image)
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         gray = undistort.grayUndistort(gray)  # 转换为灰色通道
#         # cv2.imshow('gray', gray)
#         # cv2.waitKey(100)
#
#         flag, frame, index = process_image(gray, index)
#         if flag == 1:
#             print("find")
#             print(getLetterRec(frame, template_left, template_right))
#             cv2.imshow('frame', frame)
#             cv2.waitKey(100)
#
#         # cv2.imshow('edges', edges)
#
#         k = cv2.waitKey(5) & 0xFF
#         if k == 27:
#             break
#
#     cap.release()
#     cv2.destroyAllWindows()
# else:
#     print('cap is not opened!')
