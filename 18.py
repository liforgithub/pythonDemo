#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
求s=a+aa+aaa+aaaa+aa...a的值，其中a是一个数字。例如2+22+222+2222+22222(此时共有5个数相加)，几个数相加由键盘控制。
"""

a = int(input("请输入要叠加的数字: "))
b = int(input("请输入要叠加的长度: "))

s = 0
t = 0
for i in range(1, b + 1):
    t = t*10 + a
    s += t
    if i == b:
        print('%d' % t, end='')
        print("")
        break
    else:
        print('%d + ' % t, end='')
print(s)