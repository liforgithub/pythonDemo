#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/11/10 0010 下午 15:26
# @Author  : 李雪洋
# @File    : dispose.py
# @Software: PyCharm

import cv2
import numpy as np

base_path = 'E:\\pythonDemo\\opencv\\test\\img\\'

src = cv2.imread(base_path + '5.bmp')
h, w, _ = src.shape
# src = cv2.resize(src, (w*2, h*2), interpolation=cv2.INTER_CUBIC)
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
srcImg = cv2.equalizeHist(gray)

srcImg = cv2.GaussianBlur(srcImg, (5, 5), 0)
cv2.imshow('srcImg3', srcImg)
cv2.waitKey(0)

ret1, th1 = cv2.threshold(srcImg, 90, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('gray', th1)
cv2.waitKey(0)

(_, contours, _) = cv2.findContours(th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for i in range(len(contours)):
    cnt = contours[i]
    # 计算该轮廓的面积
    area = cv2.contourArea(cnt)
    # #
    # # 面积小的都筛选掉
    if area < 80:
        continue

    # 找到最小的矩形，该矩形可能有方向
    rect = cv2.minAreaRect(cnt)

    # box是四个点的坐标
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    # 计算高和宽
    height = abs(box[0][1] - box[2][1])
    width = abs(box[0][0] - box[2][0])
    # 身份证号码正常情况下长高比在8-12之间
    ratio = float(width) / float(height)
    # print("box:" + str(box))
    # print("rect is: " + str(rect))
    # print("ratio:" + str(ratio))
    # if ratio < 8 or ratio > 12:
    #     continue
    effectBox = box
    angel = rect[2]
    cv2.drawContours(src, [box], 0, (0, 255, 0), 1)

cv2.imshow('src', src)
cv2.waitKey(0)
# kernel = np.ones((7, 7), np.uint8)
# dilation = cv2.dilate(th1, kernel, iterations=1)
# cv2.imshow('dilation', dilation)
# cv2.waitKey(0)