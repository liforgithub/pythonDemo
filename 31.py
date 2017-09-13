#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/13 0013 下午 16:35
# @Author  : 李雪洋
# @File    : 31.py
# @Software: PyCharm

"""
请输入星期几的第一个字母来判断一下是星期几，如果第一个字母一样，则继续判断第二个字母
"""

import time

myD = {'Monday': '星期一',
        'Tuesday': '星期二',
        'Wednesday': '星期三',
        'Thursday': '星期四',
        'Friday': '星期五',
        'Saturday': '星期六',
        'Sunday': '星期日'}
isContinue = True

s = ''
while isContinue:
    count = 0
    prt = '请输入一个字母： ' if s == '' else '请再输入一个字母: '
    time.sleep(0.2)
    s += input(prt)
    for key, value in dict.items(myD):
        if s == key[:len(s)]:
            print('%s ---- %s' % (key, value))
            count += 1
    if count == 0:
        print('没有找到对应的事件')
        isContinue = False
    elif count == 1:
        isContinue = False
