#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/10/20 0020 下午 15:03
# @Author  : 李雪洋
# @File    : test.py
# @Software: PyCharm

import tensorflow as tf

output = crack_captcha_cnn()
saver = tf.train.Saver()
sess = tf.Session()
saver.restore(sess, tf.train.latest_checkpoint('.'))

while (1):

    text, image = gen_captcha_text_and_image()
    image = convert2gray(image)
    image = image.flatten() / 255

    predict = tf.argmax(tf.reshape(output, [-1, MAX_CAPTCHA, CHAR_SET_LEN]), 2)
    text_list = sess.run(predict, feed_dict={X: [image], keep_prob: 1})
    predict_text = text_list[0].tolist()

    vector = np.zeros(MAX_CAPTCHA * CHAR_SET_LEN)
    i = 0
    for t in predict_text:
        vector[i * 63 + t] = 1
        i += 1
        # break

    print("正确: {}  预测: {}".format(text, vec2text(vector)))