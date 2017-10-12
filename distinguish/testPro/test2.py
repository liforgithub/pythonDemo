#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/10/12 0012 下午 16:01
# @Author  : 李雪洋
# @File    : test2.py
# @Software: PyCharm

from PIL import Image
import os
import sys
import time
sys.path.append("..")
from distinguish import distinguish

img_open_path = 'E:\\pythonDemo\\distinguish\\img\\1.bmp'
img_save_path = 'E:\\pythonDemo\\distinguish\\train\\'

def get_feature(img):
    """
    获取指定图片的特征值,
    1. 按照每排的像素点,高度为15,则有15个维度,然后为11列,总共26个维度
    :param img_path:
    :return:一个维度为15（高度）的列表
    """

    width, height = img.size

    pixel_cnt_list = []
    for y in range(height):
        pix_cnt_x = 0
        for x in range(width):
            if img.getpixel((x, y)) == 0:  # 黑色点
                pix_cnt_x += 1

        pixel_cnt_list.append(pix_cnt_x)

    for x in range(width):
        pix_cnt_y = 0
        for y in range(height):
            if img.getpixel((x, y)) == 0:  # 黑色点
                pix_cnt_y += 1

        pixel_cnt_list.append(pix_cnt_y)

    return pixel_cnt_list

start = time.time()

for ii in range(1, 101):
    # 二值化
    image = Image.open('E:\\pythonDemo\\distinguish\\img\\' + str(ii) + '.bmp')
    imgry = image.convert('L')  # 转化为灰度图

    dgh = distinguish(imgry, 140)

    table = dgh.get_bin_table()
    img_gray = imgry.point(table, '1')
    dgh.setImg(img_gray)
    print('二值化完成')

    # 去噪
    width = img_gray.width
    height = img_gray.height
    for i in range(0, width):
        for j in range(0, height):
            # 筛选出个数为 1或者2 的点的坐标即为 孤立点 ，去除
            num = dgh.sum_9_region(i, j)
            if num == 1 or num == 2:
                img_gray[i, j] = 0
    print('去除噪点完成')

    # 分割数字个数
    splitNum = 4
    # s1 第一个数字离左边距离
    # s2 数字离顶部的距离
    # s3 数字宽度
    # s4 两个数字之间的距离
    # s5 数字高度
    offset = {'s1': 16, 's2': 9, 's3': 11, 's4': 9, 's5': 15}
    img_list = dgh.get_crop_imgs(splitNum, offset)
    print('图片字符切割完成')

    result = []
    for i in img_list:
        # i.show()
        # pathNum = input('输入：')
        # l = os.listdir(img_save_path + pathNum)
        # size = len(l)
        # size += 1
        # i.save(img_save_path + pathNum + '\\' + str(size) + '.bmp')

        # 生成模型集
        pixel_list = get_feature(i)

        isFind = False
        for fileNum in range(0, 10):
            wrongCount = 0
            filename = img_save_path + str(fileNum) + '\\last_train_pix_xy.txt'
            if not os.path.exists(filename):
                continue
            fo = open(filename, "r")
            trainModel = fo.readline()
            trainList = trainModel.split(' ')
            trainList = trainList[0: len(trainList) - 1]
            for trainPos in range(0, len(trainList)):
                if pixel_list[trainPos] != int(trainList[trainPos]):
                    wrongCount += 1
            if int(wrongCount / len(trainList) * 100) < 10:
                result.append(str(fileNum))
                isFind = True
                break
        if not isFind:
            result.append('$')

    end = time.time()

    image.save('E:\\pythonDemo\\distinguish\\tmp\\' + ''.join(result) + '.bmp')
    print(ii)
    print(end - start)