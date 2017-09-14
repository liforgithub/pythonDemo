#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/9/14 0014 下午 15:11
# @Author  : 李雪洋
# @File    : 56.py
# @Software: PyCharm

"""
画图，学用circle画圆形。
"""

import turtle

turtle.title("画圆")
turtle.setup(800, 600, 0, 0)
pen = turtle.Turtle()
pen.color("blue")
pen.width(5)
pen.shape("turtle")
pen.speed(1)
pen.circle(100)