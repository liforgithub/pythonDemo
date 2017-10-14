#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/10/13 0013 下午 15:20
# @Author  : 李雪洋
# @File    : idcard.py
# @Software: PyCharm

import cv2
import numpy as np

def preprocess(gray):
    # # 直方图均衡化
    # equ = cv2.equalizeHist(gray)
    # 高斯平滑
    gaussian = cv2.GaussianBlur(gray, (3, 3), 0, 0, cv2.BORDER_DEFAULT)
    # cv2.imshow('gaussian', gaussian)
    # cv2.waitKey(0)
    # 中值滤波
    median = cv2.medianBlur(gaussian, 5)
    # cv2.imshow('median', median)
    # cv2.waitKey(0)
    # Sobel算子，X方向求梯度
    sobel = cv2.Sobel(median, cv2.CV_8U, 1, 0, ksize=3)
    # cv2.imshow('sobel', sobel)
    # cv2.waitKey(0)
    # 二值化
    ret, binary = cv2.threshold(sobel, 50, 255, cv2.THRESH_BINARY)
    # cv2.imshow('binary', binary)
    # cv2.waitKey(0)
    # 膨胀和腐蚀操作的核函数
    element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 7))
    # 膨胀一次，让轮廓突出
    dilation = cv2.dilate(binary, element2, iterations=1)
    cv2.imshow('dilation', dilation)
    # cv2.waitKey(0)

    return dilation


def findPlateNumberRegion(img):
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

        # 计算高和宽
        height = abs(box[0][1] - box[2][1])
        width = abs(box[0][0] - box[2][0])
        # 身份证号码正常情况下长高比在6.8-7.8之间
        ratio = float(width) / float(height)
        print("ratio:" + str(ratio))
        if ratio > 8 or ratio < 6:
            continue
        region.append(box)

    return region

def detect(img):

    # 转化成灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('gray', gray)
    # cv2.waitKey(0)

    ret, thresh2 = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY_INV)
    # thresh2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # cv2.imshow('thresh2', thresh2)
    # cv2.waitKey(0)

    # 形态学变换的预处理
    dilation = preprocess(thresh2)

    # 查找车牌区域
    region = findPlateNumberRegion(dilation)

    # 用绿线画出这些找到的轮廓
    for box in region:
        pass
        # cv2.drawContours(img, [box], 0, (0, 255, 0), 2)
    ys = [box[0, 1], box[1, 1], box[2, 1], box[3, 1]]
    xs = [box[0, 0], box[1, 0], box[2, 0], box[3, 0]]
    ys_sorted_index = np.argsort(ys)
    xs_sorted_index = np.argsort(xs)

    x1 = box[xs_sorted_index[0], 0]
    x2 = box[xs_sorted_index[3], 0]

    y1 = box[ys_sorted_index[0], 1]
    y2 = box[ys_sorted_index[3], 1]

    img_org2 = img.copy()
    # cv2.imshow('img_org2', img_org2)
    # cv2.waitKey(0)
    img_plate = img_org2[y1:y2, x1:x2]
    cv2.imshow('number plate', img_plate)
    cv2.imwrite('number_plate.jpg', img_plate)

    # 带轮廓的图片
    # cv2.imwrite('contours.png', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    imagePath = './2.bmp'
    img = cv2.imread(imagePath)
    height, width = img.shape[:2]
    img = cv2.resize(img, (int(width / 10), int(height / 10)), interpolation=cv2.INTER_CUBIC)
    cv2.imshow('img', img)
    detect(img)