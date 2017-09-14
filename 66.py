#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/14 0014 下午 15:50
# @Author  : 李雪洋
# @File    : 66.py
# @Software: PyCharm

"""
输入3个数a,b,c，按大小顺序输出。　
"""

x = int(input("请输入x: "))
y = int(input("请输入y: "))
z = int(input("请输入z: "))

if x > y:
    x, y = y, x
if x > z:
    x, z = z, x
if y > z:
    z, y = y, z

print("%d %d %d" % (x, y, z))