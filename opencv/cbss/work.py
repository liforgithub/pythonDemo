#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/11/10 0010 上午 9:59
# @Author  : 李雪洋
# @File    : work.py
# @Software: PyCharm
import numpy as np
from decimal import Decimal
import pickle
import network
import cv2

dir_name = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

img_path = 'E:\\pythonDemo\\opencv\\cbss\\spit\\5848.bmp'
w, b = pickle.load(open('./w-b.pkl', 'rb'))

img = cv2.imread(img_path, 0)
# cv2.imshow('img', img)
# cv2.waitKey(0)
array = np.array(img)  # array is a numpy array
print(array)
ary = np.zeros((900, 1))
num = 0
for x in array:
    for y in x:
        ary[num] = [float(Decimal(y / 255).quantize(Decimal('0.00000000')))]
        num += 1
net = network.Network([900, 30, 26])
net.setWB(w, b)
print(f"n = {dir_name[np.argmax(net.feedforward(ary))]}")