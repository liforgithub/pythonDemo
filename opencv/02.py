#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/10/14 0014 上午 10:18
# @Author  : 李雪洋
# @File    : 02.py
# @Software: PyCharm

import cv2
import numpy as np


def findPlateNumberRegion(img, large, small):
    region = []
    # 查找轮廓
    (_, contours, _) = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 筛选面积小的
    for i in range(len(contours)):
        cnt = contours[i]
        # 计算该轮廓的面积
        area = cv2.contourArea(cnt)
        #
        # 面积小的都筛选掉
        if area < 2000:
            continue

        # 找到最小的矩形，该矩形可能有方向
        rect = cv2.minAreaRect(cnt)
        print("rect is: " + str(rect))

        # box是四个点的坐标
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        print("box:" + str(box))

        # 计算高和宽
        height = abs(box[0][1] - box[2][1])
        width = abs(box[0][0] - box[2][0])
        # 身份证号码正常情况下长高比在6.8-7.8之间
        ratio = float(width) / float(height)
        print("ratio:" + str(ratio))
        if small < ratio < large:
            return box, rect[2]


def getEffectiveArea(img, srcImg):
    ret3, th3 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imshow('th3', th3)

    kernel = np.ones((10, 10), np.uint8)
    erosion = cv2.erode(th3, kernel, iterations=1)
    # cv2.imshow('th3-erosion', erosion)

    kernel = np.ones((10, 10), np.uint8)
    dilation = cv2.dilate(th3, kernel, iterations=1)
    # cv2.imshow('th3-dilation', dilation)

    box, angel = findPlateNumberRegion(dilation, 2, 1)

    cv2.drawContours(srcImg, [box], 0, (0, 255, 0), 2)

    ys = [box[0, 1], box[1, 1], box[2, 1], box[3, 1]]
    xs = [box[0, 0], box[1, 0], box[2, 0], box[3, 0]]
    ys_sorted_index = np.argsort(ys)
    xs_sorted_index = np.argsort(xs)

    x1 = box[xs_sorted_index[0], 0]
    x2 = box[xs_sorted_index[3], 0]

    y1 = box[ys_sorted_index[0], 1]
    y2 = box[ys_sorted_index[3], 1]

    img_org2 = srcImg.copy()

    cv2.imshow('img_org2', img_org2)
    cv2.waitKey(0)

    img_plate = img_org2[y1:y2, x1:x2]
    img = img[y1:y2, x1:x2]
    cv2.imshow('number plate', img_plate)
    cv2.waitKey(0)

    #(340, 530)为正常可辨识范围取的基本值，可浮动
    img = cv2.resize(img, (530, 340), interpolation=cv2.INTER_CUBIC)
    img_plate = cv2.resize(img_plate, (530, 340), interpolation=cv2.INTER_CUBIC)

    return img, img_plate


img = cv2.imread('./img/01.bmp')
cv2.imshow('img', img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(gray, (5, 5), 0)

########################取有效区域########################
effectiveArea, srcImg = getEffectiveArea(blur, img)
########################取有效区域########################

# 阈值一定要设为 0！
ret3, th3 = cv2.threshold(effectiveArea, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
cv2.imshow('th3', th3)

# 腐蚀操作
# 去掉部分噪点
kernel = np.ones((3, 3), np.uint8)
erosion = cv2.erode(th3, kernel, iterations=1)
cv2.imshow('th3-erosion', erosion)

# 膨胀的核函数(9, 7)
# element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (12, 15))
# 膨胀一次，让轮廓突出
kernel = np.ones((15, 15), np.uint8)
dilation = cv2.dilate(erosion, kernel, iterations=1)
cv2.imshow('th3-dilation', dilation)
cv2.waitKey(0)

box, angel = findPlateNumberRegion(dilation, 9, 6)

cv2.drawContours(srcImg, [box], 0, (0, 255, 0), 2)

ys = [box[0, 1], box[1, 1], box[2, 1], box[3, 1]]
xs = [box[0, 0], box[1, 0], box[2, 0], box[3, 0]]
ys_sorted_index = np.argsort(ys)
xs_sorted_index = np.argsort(xs)

x1 = box[xs_sorted_index[0], 0]
x2 = box[xs_sorted_index[3], 0]

y1 = box[ys_sorted_index[0], 1]
y2 = box[ys_sorted_index[3], 1]

img_org2 = srcImg.copy()

cv2.imshow('img_org2', img_org2)

img_plate = img_org2[y1:y2, x1:x2]
cv2.imshow('number plate', img_plate)

rows, cols, _ = img_plate.shape
# 这里的第一个参数为旋转中心，第二个为旋转角度，第三个为旋转后的缩放因子
# 可以通过设置旋转中心，缩放因子，以及窗口大小来防止旋转后超出边界的问题
M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angel, 1)
# 第三个参数是输出图像的尺寸中心
dst = cv2.warpAffine(img_plate, M, (cols, rows))

cv2.imshow('dst', dst)

cv2.waitKey(0)

cv2.destroyAllWindows()
