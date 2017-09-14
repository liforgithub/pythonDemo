#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/14 0014 下午 16:03
# @Author  : 李雪洋
# @File    : 68.py
# @Software: PyCharm

"""
有n个整数，使其前面各数顺序向后移m个位置，最后m个数变成最前面的m个数
"""

v = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

x = int(input("请输入X： "))

v1 = v[:x - 1]
v2 = v[x - 1: 2 * (x - 1)]
v3 = v[2 * (x - 1):]

v = v2 + v1 + v3

print(v1)
print(v2)
print(v3)

print(v)