#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/10/20 0020 上午 10:52
# @Author  : 李雪洋
# @File    : download.py
# @Software: PyCharm

import tensorflow as tf

b = tf.Variable(tf.zeros([100]))  #生成100维的向量 初始维0
w = tf.Variable(tf.random_uniform([784, 100], -1, 1))  #生成784x100的随机矩阵

x = tf.placeholder(tf.float32)  #输入的placeholder

relu = tf.nn.relu(tf.matmul(w, x) + b) #relu(wx + b)

c = [...]
s = tf.Session()
for step in range(10):
    ipt = tf.Variable(tf.zeros([100]))
    result = s.run(c, feed_dict={x: ipt})
    print(step, result)