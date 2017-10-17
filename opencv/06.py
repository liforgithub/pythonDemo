#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/10/17 0017 下午 14:53
# @Author  : 李雪洋
# @File    : 06.py
# @Software: PyCharm

import cv2
import numpy as np
import os

# 生成训练集
def get_feature(img):
    h, w = img.shape
    pointList = []
    for height in range(h):
        wCount = 0
        for width in range(w):
            if bin[height, width] == 255:
                wCount += 1
        pointList.append(wCount)

    for width in range(w):
        hCount = 0
        for height in range(h):
            if bin[height, width] == 255:
                hCount += 1
        pointList.append(hCount)

    return pointList

# 获取检测到的最小矩形坐标
def getRectangularCoordinate(box):
    if isinstance(box, list):
        return [box[0], box[0] + box[2], box[1], box[1] + box[3]]

    ys = [box[0, 1], box[1, 1], box[2, 1], box[3, 1]]
    xs = [box[0, 0], box[1, 0], box[2, 0], box[3, 0]]
    ys_sorted_index = np.argsort(ys)
    xs_sorted_index = np.argsort(xs)

    x1 = box[xs_sorted_index[0], 0]
    x2 = box[xs_sorted_index[3], 0]

    y1 = box[ys_sorted_index[0], 1]
    y2 = box[ys_sorted_index[3], 1]

    return [x1, x2, y1, y2]

def findPlateNumberRegion2(img):
    region = []
    # 查找轮廓
    (_, contours, _) = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 筛选面积小的
    for i in contours:
        # 计算该轮廓的面积
        area = cv2.contourArea(i)

        # 面积小的都筛选掉
        if area < 70:
            continue

        x, y, width, height = cv2.boundingRect(i)

        # 身份证号码正常情况下长高比在6.8-7.8之间
        ratio = float(width) / float(height)
        print("ratio:" + str(ratio))
        if 0 < ratio < 1:
            region.append([x, y, width, height])
    # 该列表为无序列表，要想得到正确的身份证顺序，需要对其进行排序，排序的规则就是以轮廓的左上角x坐标为准
    return sorted(region, key=lambda a_list: a_list[0])


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
        # if area < 2000:
        #     continue

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
    [ret3, th3] = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # cv2.imshow('th3', th3)

    kernel = np.ones((10, 10), np.uint8)
    erosion = cv2.erode(th3, kernel, iterations=1)
    # cv2.imshow('th3-erosion', erosion)

    kernel = np.ones((10, 10), np.uint8)
    dilation = cv2.dilate(th3, kernel, iterations=1)
    # cv2.imshow('th3-dilation', dilation)

    box, angel = findPlateNumberRegion(dilation, 2, 1)

    rows, cols, _ = srcImg.shape
    # 这里的第一个参数为旋转中心，第二个为旋转角度，第三个为旋转后的缩放因子
    # 可以通过设置旋转中心，缩放因子，以及窗口大小来防止旋转后超出边界的问题
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angel, 1)
    # 第三个参数是输出图像的尺寸中心
    srcImg = cv2.warpAffine(srcImg, M, (cols, rows))
    dilation = cv2.warpAffine(dilation, M, (cols, rows))
    img = cv2.warpAffine(img, M, (cols, rows))

    box, angel = findPlateNumberRegion(dilation, 2, 1)

    cv2.drawContours(srcImg, [box], 0, (0, 255, 0), 2)

    coordinate = getRectangularCoordinate(box)

    img_org2 = srcImg.copy()

    img_plate = img_org2[coordinate[2]:coordinate[3], coordinate[0]:coordinate[1]]
    img = img[coordinate[2]:coordinate[3], coordinate[0]:coordinate[1]]
    # cv2.imshow('number plate', img_plate)
    # cv2.waitKey(0)

    # (530, 340)为正常可辨识范围取的基本值，可浮动
    img = cv2.resize(img, (530, 340), interpolation=cv2.INTER_CUBIC)
    img_plate = cv2.resize(img_plate, (530, 340), interpolation=cv2.INTER_CUBIC)

    # cv2.imshow('img_plate', img_plate)
    # cv2.imshow('img-00', img)
    # cv2.waitKey(0)

    return img, img_plate


img = cv2.imread('./img/01.bmp')
# cv2.imshow('src-img', img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(gray, (5, 5), 0)

########################取有效区域########################
effectiveArea, srcImg = getEffectiveArea(blur, img)
########################取有效区域########################

# 阈值一定要设为 0！
ret3, th3 = cv2.threshold(effectiveArea, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
# cv2.imshow('th3', th3)

# 腐蚀操作
# 去掉部分噪点
kernel = np.ones((3, 3), np.uint8)
erosion = cv2.erode(th3, kernel, iterations=1)
# cv2.imshow('th3-erosion', erosion)

# 膨胀的核函数(9, 7)
# element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (12, 15))
# 膨胀一次，让轮廓突出
kernel = np.ones((15, 15), np.uint8)
dilation = cv2.dilate(erosion, kernel, iterations=1)
# cv2.imshow('th3-dilation', dilation)
# cv2.waitKey(0)

box, angel = findPlateNumberRegion(dilation, 10, 6)

# cv2.drawContours(srcImg, [box], 0, (0, 255, 0), 2)

coordinate = getRectangularCoordinate(box)

img_org2 = srcImg.copy()

img_plate = img_org2[coordinate[2]:coordinate[3], coordinate[0]:coordinate[1]]
# cv2.imshow('number plate', img_plate)

rows, cols, _ = img_plate.shape
# 这里的第一个参数为旋转中心，第二个为旋转角度，第三个为旋转后的缩放因子
# 可以通过设置旋转中心，缩放因子，以及窗口大小来防止旋转后超出边界的问题
M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angel, 1)
# 第三个参数是输出图像的尺寸中心
dst = cv2.warpAffine(img_plate, M, (cols, rows))

# cv2.imshow('dst', dst)
# cv2.waitKey(0)

gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(gray, (5, 5), 0)

ret3, th3 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# cv2.imshow('th3-eff', th3)
# cv2.waitKey(0)

kernel = np.ones((4, 3), np.uint8)
dilation = cv2.dilate(th3, kernel, iterations=1)

# cv2.imshow('end-dilation', dilation)
# cv2.waitKey(0)

# 分割字符
boxList = findPlateNumberRegion2(dilation)

imgList = []
for box in boxList:
    # cv2.drawContours(dst, [box], 0, (0, 255, 0), 1)
    # cv2.rectangle(dst, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), (0, 255, 0), 1)
    coordinate = getRectangularCoordinate(box)
    img_org2 = dst.copy()
    img_plate = img_org2[coordinate[2]:coordinate[3], coordinate[0]:coordinate[1]]
    imgList.append(img_plate)
    h, w, _ = img_plate.shape
    bin2 = cv2.resize(img_plate, (w * 10, h * 10), interpolation=cv2.INTER_CUBIC)
    cv2.imshow('bin', bin2)
    cv2.waitKey(0)
    gray = cv2.cvtColor(img_plate, cv2.COLOR_BGR2GRAY)
    ret3, bin = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # kernel = np.ones((1, 1), np.uint8)
    # erosion = cv2.erode(bin, kernel, iterations=1)
    bin2 = cv2.resize(bin, (w * 10, h * 10), interpolation=cv2.INTER_CUBIC)
    cv2.imshow('bin2', bin2)
    cv2.waitKey(0)

img_save_path = 'E:\\pythonDemo\\opencv\\train\\'

i = 0
result = []
for img in imgList:
    h, w, _ = img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret3, bin = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # bin2 = cv2.resize(bin, (w * 10, h * 10), interpolation=cv2.INTER_CUBIC)
    # cv2.imshow(str(i), bin2)
    # cv2.waitKey(0)

    pixel_list = get_feature(bin)

    isFind = False
    for fileNum in range(0, 10):
        filename = img_save_path + str(fileNum) + '\\last_train_pix_xy.txt'
        if not os.path.exists(filename):
            continue
        fo = open(filename, "r")
        while True:
            wrongCount = 0
            trainModel = fo.readline()
            if trainModel:
                trainList = trainModel.split(' ')
                trainList = trainList[0: len(trainList) - 1]
                if len(trainList) == len(pixel_list):
                    for trainPos in range(0, len(trainList)):
                        if pixel_list[trainPos] != int(trainList[trainPos]):
                            wrongCount += 1
                    print('#################' + str(fileNum) + '###################')
                    print(pixel_list)
                    print(str(int(wrongCount / len(trainList) * 100)))
                    print(trainList)
                    print('#################' + str(fileNum) + '###################')
                    print('\n\n')
                    if int(wrongCount / len(trainList) * 100) < 10:
                        result.append(str(fileNum))
                        isFind = True
                        break

            else:
                break
        if isFind:
            break
    if not isFind:
        result.append('$')
print(result)

# cv2.waitKey(0)

cv2.destroyAllWindows()
