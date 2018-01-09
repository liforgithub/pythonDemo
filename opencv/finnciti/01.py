#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/11/8 0008 下午 19:18
# @Author  : 李雪洋
# @File    : download.py
# @Software: PyCharm
import cv2
import numpy as np
import os

img_save_path = 'E:\\pythonDemo\\opencv\\cbss\\spit\\'


# 按照指定图像大小调整尺寸
def resize_image(image, height, width):
    top, bottom, left, right = (0, 0, 0, 0)

    # 获取图像尺寸
    h, w = image.shape

    # 对于长宽不相等的图片，找到最长的一边
    longest_edge = max(h, w)

    # 计算短边需要增加多上像素宽度使其与长边等长
    if h < longest_edge:
        dh = longest_edge - h
        top = dh // 2
        bottom = dh - top
    elif w < longest_edge:
        dw = longest_edge - w
        left = dw // 2
        right = dw - left
    else:
        pass

    # RGB颜色
    BLACK = [0, 0, 0]

    # 给图像增加边界，是图片长、宽等长，cv2.BORDER_CONSTANT指定边界颜色由value指定
    constant = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=BLACK)

    # 调整图像大小并返回
    return cv2.resize(constant, (height, width))


def saveSpitImg(boxList, dst):
    for box in boxList:
        img_org2 = dst.copy()
        img_plate = img_org2[box[2]:box[3], box[0]:box[1]]
        # img_plate = cv2.resize(img_plate, (30, 30), interpolation=cv2.INTER_CUBIC)
        img_plate = resize_image(img_plate, 30, 30)
        l = os.listdir(img_save_path)
        size = len(l)
        size += 1
        cv2.imwrite(img_save_path + str(size) + '.bmp', img_plate)


# for i in range(1, 5001):
#     print(i)
#     srcImg = cv2.imread(f"E:\\pythonDemo\\opencv\\cbss\\img\\{i}.bmp")
#     h, w, _ = srcImg.shape
#     dstImg = cv2.resize(srcImg, (w * 10, h * 10), interpolation=cv2.INTER_CUBIC)
#     # cv2.imshow('dstImg', dstImg)
#     # cv2.waitKey(0)
#
#     gray = cv2.cvtColor(dstImg, cv2.COLOR_BGR2GRAY)
#
#     ret1, th1 = cv2.threshold(gray, 82, 255, cv2.THRESH_BINARY_INV)
#     # cv2.imshow('th1', th1)
#     # cv2.waitKey(0)
#
#     kernel = np.ones((11, 11), np.uint8)
#     dilation = cv2.dilate(th1, kernel, iterations=1)
#
#     # cv2.imshow('dilation', dilation)
#     # cv2.waitKey(0)
#
#     kernel = np.ones((11, 11), np.uint8)
#     dilation2 = cv2.dilate(dilation, kernel, iterations=1)
#
#     # cv2.imshow('dilation2', dilation2)
#     # cv2.waitKey(0)
#
#     (_, contours, _) = cv2.findContours(dilation2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#
#     boxList = []
#     for j in contours:
#         # 计算该轮廓的面积
#         area = cv2.contourArea(j)
#         #
#         # 面积小的都筛选掉
#         if area < 1300:
#             continue
#
#         x, y, width, height = cv2.boundingRect(j)
#         box = [x, y, width, height]
#         box = [box[0], box[0] + box[2], box[1], box[1] + box[3]]
#         boxList.append(box)
#         # cv2.rectangle(dstImg, (box[0], box[2]), (box[1], box[3]), (0, 255, 0), 1)
#     saveSpitImg(boxList, th1)

i = 77
src = cv2.imread(f"E:\\pythonDemo\\opencv\\finnciti\\img\\{i}.bmp", 0)
cv2.imshow('src', src)
cv2.waitKey(0)

ret1, th1 = cv2.threshold(src, 82, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('th1', th1)
cv2.waitKey(0)
