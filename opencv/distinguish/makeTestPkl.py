#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/11/10 0010 上午 8:53
# @Author  : 李雪洋
# @File    : makeTestPkl.py
# @Software: PyCharm

import pickle
from decimal import Decimal
import cv2
import numpy as np
import os

dir_name = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

base_path = 'E:\\pythonDemo\\opencv\\cbss\\testData\\'

pkllist = []
n = 0
for dirName in dir_name:
    rootdir = base_path + dirName
    fileList = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件

    for i in range(0, len(fileList)):
        path = os.path.join(rootdir, fileList[i])
        if os.path.isfile(path):
            #print(path)
            img = cv2.imread(path, 0)
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
            pkllist.append((ary, n))
    n += 1

data = pickle.load(open('./data.pkl', 'rb'))

pickle.dump((data, pkllist), open('./data.pkl', 'wb'))