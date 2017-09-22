#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/15 0015 上午 9:01
# @Author  : 李雪洋
# @File    : 80.py
# @Software: PyCharm

"""
海滩上有一堆桃子，五只猴子来分。
第一只猴子把这堆桃子平均分为五份，多了一个，这只猴子把多的一个扔入海中，拿走了一份。
第二只猴子把剩下的桃子又平均分成五份，又多了一个，它同样把多的一个扔入海中，拿走了一份，
第三、第四、第五只猴子都是这样做的，问海滩上原来最少有多少个桃子？
"""

def fn(n):
    for j in range(5):
        if (n % 5 == 1) and n > 5:
            n -= (n - 1) / 5 + 1
        else:
            return False

    return True

for i in range(1, 10000):
    if fn(i):
        print(i)
        break