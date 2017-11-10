#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/11/9 0009 下午 15:15
# @Author  : 李雪洋
# @File    : makeTrainPkl.py
# @Software: PyCharm

import pickle
from decimal import Decimal
import cv2
import numpy as np
import os

dir_name = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

base_path = 'E:\\pythonDemo\\opencv\\cbss\\trainDemo\\'

pkllist = []
for dirName in dir_name:
    rootdir = base_path + dirName
    fileList = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件

    realNp = np.zeros((len(dir_name), 1))
    for n in range(len(dir_name)):
        if dir_name[n] == dirName:
            realNp[n] = 1
        else:
            realNp[n] = 0

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
            pkllist.append((ary, realNp))

fw = open('./data.pkl', 'wb+')
pickle.dump(pkllist, fw)
