#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/14 0014 下午 14:10
# @Author  : 李雪洋
# @File    : 44.py
# @Software: PyCharm

"""
两个 3 行 3 列的矩阵，实现其对应位置的数据相加，并返回一个新矩阵：
"""

import numpy as np

v1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
v2 = [[11, 21, 31], [41, 51, 61], [71, 81, 91]]

v3 = np.zeros(shape=(len(v1), len(v1[0])))

for i in range(0, 3):
    for j in range(0, 3):
       v3[i][j] = v1[i][j] + v2[i][j]

print(v3)