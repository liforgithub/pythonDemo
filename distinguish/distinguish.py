#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/10/12 0012 下午 12:59
# @Author  : 李雪洋
# @File    : distinguish.py
# @Software: PyCharm

class distinguish:
    def __init__(self, img, threshold):
        self.img = img
        self.threshold = threshold
    def setImg(self, img):
        self.img = img
    def get_bin_table(self):
        """
        获取灰度转二值的映射table
        :param threshold:
        :return:
        """
        table = []
        for i in range(256):
            if i < self.threshold:
                table.append(0)
            else:
                table.append(1)

        return table
    def sum_9_region(self, x, y):
        """
        9邻域框,以当前点为中心的田字框,黑点个数
        :param x:
        :param y:
        :return:
        """
        # todo 判断图片的长宽度下限
        cur_pixel = self.img.getpixel((x, y))  # 当前像素点的值
        width = self.img.width
        height = self.img.height

        if cur_pixel == 1:  # 如果当前点为白色区域,则不统计邻域值
            return 0

        if y == 0:  # 第一行
            if x == 0:  # 左上顶点,4邻域
                # 中心点旁边3个点
                sum = cur_pixel \
                      + self.img.getpixel((x, y + 1)) \
                      + self.img.getpixel((x + 1, y)) \
                      + self.img.getpixel((x + 1, y + 1))
                return 4 - sum
            elif x == width - 1:  # 右上顶点
                sum = cur_pixel \
                      + self.img.getpixel((x, y + 1)) \
                      + self.img.getpixel((x - 1, y)) \
                      + self.img.getpixel((x - 1, y + 1))

                return 4 - sum
            else:  # 最上非顶点,6邻域
                sum = self.img.getpixel((x - 1, y)) \
                      + self.img.getpixel((x - 1, y + 1)) \
                      + cur_pixel \
                      + self.img.getpixel((x, y + 1)) \
                      + self.img.getpixel((x + 1, y)) \
                      + self.img.getpixel((x + 1, y + 1))
                return 6 - sum
        elif y == height - 1:  # 最下面一行
            if x == 0:  # 左下顶点
                # 中心点旁边3个点
                sum = cur_pixel \
                      + self.img.getpixel((x + 1, y)) \
                      + self.img.getpixel((x + 1, y - 1)) \
                      + self.img.getpixel((x, y - 1))
                return 4 - sum
            elif x == width - 1:  # 右下顶点
                sum = cur_pixel \
                      + self.img.getpixel((x, y - 1)) \
                      + self.img.getpixel((x - 1, y)) \
                      + self.img.getpixel((x - 1, y - 1))

                return 4 - sum
            else:  # 最下非顶点,6邻域
                sum = cur_pixel \
                      + self.img.getpixel((x - 1, y)) \
                      + self.img.getpixel((x + 1, y)) \
                      + self.img.getpixel((x, y - 1)) \
                      + self.img.getpixel((x - 1, y - 1)) \
                      + self.img.getpixel((x + 1, y - 1))
                return 6 - sum
        else:  # y不在边界
            if x == 0:  # 左边非顶点
                sum = self.img.getpixel((x, y - 1)) \
                      + cur_pixel \
                      + self.img.getpixel((x, y + 1)) \
                      + self.img.getpixel((x + 1, y - 1)) \
                      + self.img.getpixel((x + 1, y)) \
                      + self.img.getpixel((x + 1, y + 1))

                return 6 - sum
            elif x == width - 1:  # 右边非顶点
                # print('%s,%s' % (x, y))
                sum = self.img.getpixel((x, y - 1)) \
                      + cur_pixel \
                      + self.img.getpixel((x, y + 1)) \
                      + self.img.getpixel((x - 1, y - 1)) \
                      + self.img.getpixel((x - 1, y)) \
                      + self.img.getpixel((x - 1, y + 1))

                return 6 - sum
            else:  # 具备9领域条件的
                sum = self.img.getpixel((x - 1, y - 1)) \
                      + self.img.getpixel((x - 1, y)) \
                      + self.img.getpixel((x - 1, y + 1)) \
                      + self.img.getpixel((x, y - 1)) \
                      + cur_pixel \
                      + self.img.getpixel((x, y + 1)) \
                      + self.img.getpixel((x + 1, y - 1)) \
                      + self.img.getpixel((x + 1, y)) \
                      + self.img.getpixel((x + 1, y + 1))
                return 9 - sum
    def get_crop_imgs(self, splitNum, offset):
        """
        按照图片的特点,进行切割,这个要根据具体的验证码来进行工作. # 见原理图
        :param splitNum, offset:
                splitNum 分割数字个数
                offset['s1'] 第一个数字离左边距离
                offset['s2'] 数字离顶部的距离
                offset['s3'] 数字宽度
                offset['s4'] 两个数字之间的距离
                offset['s5'] 数字高度
        :return:
        """
        child_img_list = []
        # 15 第一个数字到边缘长度
        # 11 数字长度
        # 10 两个数字之间的长度
        for i in range(splitNum):
            x = offset['s1'] + i * (offset['s3'] + offset['s4'])
            y = offset['s2']
            child_img = self.img.crop((x, y, x + offset['s3'], y + offset['s5']))
            child_img_list.append(child_img)

        return child_img_list