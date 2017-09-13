#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
将一个列表的数据复制到另一个列表中
"""

a = [1,2,3,4]
b = []

# for i in range(len(a)):
#     b.append(a[i])
b = a[:]

print(b)