#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
输入一行字符，分别统计出其中英文字母、空格、数字和其它字符的个数。
"""

import re

s = input("请输入字符串: ")

# a = b = c = d = 0
# for i in s:
#     if i.isalpha():
#         a += 1
#     elif i.isspace():
#         b += 1
#     elif i.isdigit():
#         c += 1
#     else:
#         d += 1

a = re.findall(r'[a-zA-Z]', s)
b = re.findall(r'[0-9]', s)
c = re.findall(r' ', s)
d = len(s) - len(a) - len(b) - len(c)


print("英文字母 %d、空格 %d、数字 %d 其它字符 %d" % (len(a), len(b), len(c), d))