# encoding: utf-8
import cv2
import numpy as np
import time

f = open("newMap.txt")
tmpList = f.readlines()
print("file1 read")

tmpArray1 = []
tmpArray2 = []
arrayDiff = 640 * 480
idx = 0
for i in range(480):
    tta1 = []
    tta2 = []
    for j in range(640):
        tta1.append(int(tmpList[idx].strip('\n')))
        tta2.append(int(tmpList[idx + arrayDiff].strip('\n')))
        idx = idx + 1
    tmpArray1.append(tta1)
    tmpArray2.append(tta2)
Map = [np.array(tmpArray1), np.array(tmpArray2)]

f.close()
print("list1 initialized")

f = open("edge_test.txt")
tmpList = f.readlines()
print("file2 read")
f.close()

EdgeMap = np.zeros((480, 640, 2), np.uint16)
idx = 0
for i in range(480):
    for j in range(640):
        EdgeMap[i][j][0] = int(tmpList[idx].strip('\n'))
        EdgeMap[i][j][1] = int(tmpList[idx + 1].strip('\n'))
        idx = idx + 2
print("list2 initialized")


def grayUndistort(gray):
    undis = np.zeros((480, 640), np.uint8)
    gray2 = np.array(gray)
    undis = gray2[tuple(Map)]
    return undis


def edgeUndistort(gray, para1=200, para2=230):
    edges = cv2.Canny(gray, para1, para2)
    # 除去用不到的边框部分
    usedEdge = edges[43: 422, 101: 549]
    nzIndex = list(np.nonzero(usedEdge))
    # print(type(nzIndex))
    nzIndex[0] = nzIndex[0] + 43
    nzIndex[1] = nzIndex[1] + 101

    undistortedEdge = np.zeros((480, 640), np.uint8)
    middleIndex = EdgeMap[tuple(nzIndex)]

    transIndex = middleIndex[:, 0], middleIndex[:, 1]

    undistortedEdge[transIndex] = 255

    return undistortedEdge
