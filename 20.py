#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
一球从100米高度自由落下，每次落地后反跳回原高度的一半；再落下，求它在第10次落地时，共经过多少米？第10次反弹多高？

1 100
2 100 + 50 + 50
3 100 + 50 + 50 + 25 + 25
"""
hei = 100.0
for i in range(1, 11):
    if i == 1:
        sum = hei
    else:
        sum += hei*2
    hei /= 2
    if i == 10:
        print("共经过%s米" % sum)
        print("第10次跳起的高度为%s" % hei)