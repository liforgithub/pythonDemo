#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/14 0014 下午 14:09
# @Author  : 李雪洋
# @File    : 43.py
# @Software: PyCharm

"""
模仿静态变量(static)另一案例。
"""

class Num:
    nNum = 1
    def inc(self):
        self.nNum += 1
        print('nNum = %d' % self.nNum)

if __name__ == '__main__':
    nNum = 2
    inst = Num()
    for i in range(3):
        nNum += 1
        print('The num = %d' % nNum)
        inst.inc()