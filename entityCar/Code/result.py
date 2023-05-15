# coding=utf-8
import glob
import cv2
import os
import numpy as np


def NCC(img, template):
    thresh = 95  # 设定阈值
    max_val = 255  # 设定最大像素值

    # 灰度
    #img = cv2.imread(imgPath)
    #template = cv2.imread(templatePath)

    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    # 改变大小
    img = cv2.resize(img, (0, 0), fx=5, fy=5)
    # 高斯滤波
    img = cv2.GaussianBlur(img, (21, 21), 0)
    img = cv2.GaussianBlur(img, (15, 15), 0)
    # canny边缘检测
    edg = cv2.Canny(img, 5, 11)
    # 闭运算
    img = cv2.GaussianBlur(edg, (5, 5), 0)

    #cv2.imshow('Original Image', img)

    #cv2.imshow('Original template', template)
    #cv2.waitKey(1000)
    #cv2.destroyAllWindows()

    similarity = cv2.matchTemplate(img, template, cv2.TM_CCORR_NORMED)
    max_similarity = np.max(similarity)

    print(max_similarity)
    return max_similarity


def rec(img, template_left, template_right):
    if NCC(img, template_left) >= NCC(img, template_right):
        return "左"
    else:
        return "右"


def main(img,template_left,template_right):
    #left = "template/left_template.jpg"
    #right = "template/right_template.jpg"
    # print(NCC(img, left))
    # print(NCC(img, right))
    return rec(img, template_left, template_right)


# for i in range(1, 50):
#     print(main("Graphs/" + str(i) + ".png"))

