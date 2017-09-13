#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/13 0013 下午 17:07
# @Author  : 李雪洋
# @File    : 33.py
# @Software: PyCharm

"""
按逗号分隔列表。
"""

v = [1, 2, 3, 4]
print(','.join(str(n) for n in v))