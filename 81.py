#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/16 0016 上午 11:00
# @Author  : 李雪洋
# @File    : 81.py
# @Software: PyCharm

"""
809*??=800*??+9*?? 其中??代表的两位数, 809*??为四位数，8*??的结果为两位数，9*??的结果为3位数。求??代表的两位数，及809*??后的结果。
"""

for i in range(10, 100):
    if (int(809 * i / 1000) >= 1) and \
            (int(809 * i / 1000) < 10) and \
            (int(8 * i / 10) >= 1) and \
            (int(8 * i / 10) < 10) and \
            (int(9 * i / 100) >= 1) and \
            (int(9 * i / 100) < 10):
        print("?? =======> %d" % i)
        print("809*?? ===> %d" % (809 * i))