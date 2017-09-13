#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/13 0013 下午 17:33
# @Author  : 李雪洋
# @File    : 38.py
# @Software: PyCharm

"""
求一个3*3矩阵对角线元素之和。
44 87 99
25 59 32
14 53 54
right = v[0][0] + v[1][1] + v[2][2]
left = v[0][2] + v[1][1] + v[2][0]
"""

v = [[44, 87, 99], [25, 59, 32], [14, 53, 54]]

left = 0
right = 0
for i in range(0, 3):
    right += v[i][i]
    left += v[i][2 - i]

print("left: %d" % left)
print("right: %d" % right)
