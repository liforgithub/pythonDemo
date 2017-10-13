#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/10/13 0013 下午 14:31
# @Author  : 李雪洋
# @File    : 01.py
# @Software: PyCharm

import numpy as np
import argparse
from PIL import Image
import cv2

img_open_path = './2.bmp'

image = cv2.imread(img_open_path)

height, width = image.shape[:2]

res = cv2.resize(image, (int(width/10), int(height/10)), interpolation=cv2.INTER_CUBIC)
cv2.imshow('iker', res)
#cv2.imshow('image', image)
cv2.waitKey(0)
cv2.destoryAllWindows()

