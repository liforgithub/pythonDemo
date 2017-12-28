#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/12/28 0028 下午 13:54
# @Author  : 李雪洋
# @File    : test.py
# @Software: PyCharm

import face_recognition
import pickle
import datetime


def findFace(image):
    # face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model='cnn')
    face_locations = face_recognition.face_locations(image)
    top, right, bottom, left = face_locations[0]
    return image[top:bottom, left:right]

begin = datetime.datetime.now()

data = pickle.load(open('./data.pkl', 'rb'))

unknown_image = face_recognition.load_image_file('.\\src\\1.jpg')

unknown_encoding = face_recognition.face_encodings(findFace(unknown_image))[0]

compareName = ''
for (name, image, encoding) in data:

    # face_encoding = face_recognition.face_encodings(image)[0]
    results = face_recognition.compare_faces([encoding], unknown_encoding, tolerance=0.5)
    if results[0]:
        compareName = name
        break

end = datetime.datetime.now()
print((end - begin).total_seconds())

print(f'name={compareName}')
