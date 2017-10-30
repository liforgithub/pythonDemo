#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/10/18 0018 下午 13:55
# @Author  : 李雪洋
# @File    : 07-test.py
# @Software: PyCharm

import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

"""
加载图片
"""
# SRC_IMG_PATH = './img/01.bmp'
# SRC_IMG_PATH = './img/3.bmp'
# SRC_IMG_PATH = './img/04.bmp'
SRC_IMG_PATH = './img/id_card14.bmp'
srcImg = cv2.imread(SRC_IMG_PATH)
# 可以直接以灰度图片打开，这里便于后面观察，以原图打开，下一步在进行灰度处理
# srcImg = cv2.imread(SRC_IMG_PATH, 0)
h, w, _ = srcImg.shape
if h > 600:
    yN = int(h / 600)
    srcImg = cv2.resize(srcImg, (int(w / yN), int(h / yN)), interpolation=cv2.INTER_CUBIC)

cv2.imshow('srcImg', srcImg)
cv2.waitKey(0)

"""
灰度处理图片
"""
gray = cv2.cvtColor(srcImg, cv2.COLOR_BGR2GRAY)

cv2.imshow('gray', gray)
cv2.waitKey(0)

"""
高斯模糊
"""
gbr = cv2.GaussianBlur(gray, (5, 5), 0)

edges = cv2.Canny(gbr, 100, 200)

cv2.imshow('gbr', edges)
cv2.waitKey(0)

"""
寻找身份证
"""
(_, contours, _) = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

effectBox = 0
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
    # print("rect is: " + str(rect))

    # box是四个点的坐标
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    # print("box:" + str(box))

    # 计算高和宽
    height = abs(box[0][1] - box[2][1])
    width = abs(box[0][0] - box[2][0])
    # 身份证号码正常情况下长高比在6.8-7.8之间
    ratio = float(width) / float(height)
    # print("ratio:" + str(ratio))
    if 1 < ratio < 2:
        pass
        # print(box)
        # print(rect[2])
    effectBox = box
    # cv2.drawContours(srcImg, [box], 0, (0, 255, 0), 1)

# cv2.imshow('drawEffectArea', srcImg)
# cv2.waitKey(0)

"""
去除无关图像区域并旋转有效图像到水平位置
(530, 340)大小为总结出来的合适的大小，不固定
"""
pts1 = np.float32([effectBox[1], effectBox[2], effectBox[0], effectBox[3]])
pts2 = np.float32([[0, 0], [530, 0], [0, 340], [530, 340]])

M = cv2.getPerspectiveTransform(pts1, pts2)
rightcardImg = cv2.warpPerspective(srcImg, M, (530, 340))

# cv2.imshow('rightcardImg', rightcardImg)
# cv2.waitKey(0)
gray = cv2.cvtColor(rightcardImg, cv2.COLOR_BGR2GRAY)

gbr = cv2.GaussianBlur(gray, (5, 5), 0)

bin_adaptiveThreshold = cv2.adaptiveThreshold(gbr, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 13, 9)
# cv2.imshow('equalizeHist', bin_adaptiveThreshold)
# cv2.waitKey(0)

kernel = np.ones((11, 11), np.uint8)
dilation = cv2.dilate(bin_adaptiveThreshold, kernel, iterations=1)
# cv2.imshow('dilation', dilation)
# cv2.waitKey(0)

"""
寻找身份证号位置
"""

(_, contours, _) = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

effectBox = 0
angel = 0
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
    if ratio < 8 or ratio > 12:
        continue
    effectBox = box
    angel = rect[2]
    # cv2.drawContours(rightcardImg, [box], 0, (0, 255, 0), 1)
# cv2.imshow('cardNumPos', rightcardImg)
# cv2.waitKey(0)

"""
截取出身份证号码区域
"""
height = abs(effectBox[0][1] - effectBox[2][1])
width = abs(effectBox[0][0] - effectBox[2][0])

pts1 = np.float32([effectBox[1], effectBox[2], effectBox[0], effectBox[3]])
pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

M = cv2.getPerspectiveTransform(pts1, pts2)
cardImg = cv2.warpPerspective(rightcardImg, M, (width, height))

# cv2.imshow('cardImg', cardImg)
# cv2.waitKey(0)

gray = cv2.cvtColor(cardImg, cv2.COLOR_BGR2GRAY)
gray = cv2.equalizeHist(gray)
gbr = cv2.GaussianBlur(gray, (5, 5), 0)
# bin_adaptiveThreshold = cv2.adaptiveThreshold(gbr, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 13, 9)
ret, bin_adaptiveThreshold = cv2.threshold(gbr, 50, 255, cv2.THRESH_BINARY_INV)

cv2.imshow('gray', bin_adaptiveThreshold)
cv2.waitKey(0)

kernel = np.ones((3, 3), np.uint8)
dilation = cv2.dilate(bin_adaptiveThreshold, kernel, iterations=1)
cv2.imshow('dilation', dilation)
cv2.waitKey(0)

(_, contours, _) = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

region = []
for i in range(len(contours)):
    cnt = contours[i]
    # 计算该轮廓的面积
    area = cv2.contourArea(cnt)
    #
    # 面积小的都筛选掉
    if area < 70:
        continue

    x, y, width, height = cv2.boundingRect(contours[i])

    # 身份证号码正常情况下长高比在8-12之间
    if height == 0 or width == 0:
        continue
    ratio = float(width) / float(height)
    if 0 < ratio < 1:
        region.append([x, y, width, height])
    # cv2.drawContours(cardImg, [box], 0, (0, 255, 0), 1)

region = sorted(region, key=lambda a_list: a_list[0])

imgList = []
i = 0
for box in region:
    box = [box[0], box[0] + box[2], box[1], box[1] + box[3]]
    img_org2 = cardImg.copy()
    img_plate = img_org2[box[2]:box[3], box[0]:box[1]]
    imgList.append(img_plate)

    cv2.imshow(str(i), img_plate)
    l = os.listdir('E:\\pythonDemo\\opencv\\tmp')
    size = len(l)
    size += 1
    cv2.imwrite('E:\\pythonDemo\\opencv\\tmp\\' + str(size) + '.bmp', img_plate)
    cv2.waitKey(0)
    i += 1