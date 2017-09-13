#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/13 0013 下午 17:11
# @Author  : 李雪洋
# @File    : 35.py
# @Software: PyCharm

"""
文本颜色设置。
"""

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print(bcolors.WARNING + "警告的颜色字体?" + bcolors.ENDC)