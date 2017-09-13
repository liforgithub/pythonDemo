#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
输入三个整数x,y,z，请把这三个数由小到大输出
"""

x = input("请输入x：")
y = input("请输入y：")
z = input("请输入z：")

if x > y:
    x, y = y, x
if y > z:
    y, z = z, y
if x > y:
    x, y = y, x

print(x, y, z)