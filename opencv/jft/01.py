#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/11/27 0027 下午 20:00
# @Author  : 李雪洋
# @File    : 01.py
# @Software: PyCharm

import cv2
import numpy as np
import os

img_save_path = 'E:\\pythonDemo\\opencv\\jft\\spit\\'

srcImg = cv2.imread(f"E:\\pythonDemo\\opencv\\jft\\img\\1.bmp")
h, w, _ = srcImg.shape
dstImg = cv2.resize(srcImg, (w * 10, h * 10), interpolation=cv2.INTER_CUBIC)
cv2.imshow('dstImg', dstImg)
cv2.waitKey(0)

dstImg = cv2.GaussianBlur(dstImg, (9, 9), 0)
cv2.imshow('gau', dstImg)
cv2.waitKey(0)

gray = cv2.cvtColor(dstImg, cv2.COLOR_BGR2GRAY)
ret1, th1 = cv2.threshold(gray, 95, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('th1', th1)
cv2.waitKey(0)

kernel = np.ones((11, 11), np.uint8)
dilation = cv2.dilate(th1, kernel, iterations=1)

cv2.imshow('dilation', dilation)
cv2.waitKey(0)