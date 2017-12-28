#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/12/28 0028 下午 15:07
# @Author  : 李雪洋
# @File    : makePickle.py
# @Software: PyCharm
import pickle
import face_recognition
import cv2

def findFace(image):
    face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model='cnn')
    # face_locations = face_recognition.face_locations(image)
    top, right, bottom, left = face_locations[0]
    return image[top:bottom, left:right]


jobs_image = face_recognition.load_image_file('.\\src\\jobs.jpg')
lixueyang_image = face_recognition.load_image_file('.\\src\\lixueyang.jpg')
obama_image = face_recognition.load_image_file('.\\src\\obama.jpg')
peifeng_image = face_recognition.load_image_file('.\\src\\peifeng.jpg')

# pkllist = {}
#
# pkllist['jobs'] = findFace(jobs_image)
# pkllist['lixueyang'] = findFace(lixueyang_image)
# pkllist['obama'] = findFace(obama_image)
# pkllist['peifeng'] = findFace(peifeng_image)

jobs_image = findFace(jobs_image)
lixueyang_image = findFace(lixueyang_image)
obama_image = findFace(obama_image)
peifeng_image = findFace(peifeng_image)

pkllist = [('jobs', jobs_image, face_recognition.face_encodings(jobs_image)[0]),
           ('lixueyang', lixueyang_image, face_recognition.face_encodings(lixueyang_image)[0]),
           ('obama', obama_image, face_recognition.face_encodings(obama_image)[0]),
           ('peifeng', peifeng_image, face_recognition.face_encodings(peifeng_image)[0])]

# data = pickle.load(open('./data.pkl', 'rb'))
pickle.dump(pkllist, open('./data.pkl', 'wb'))
print('done')

# pickle.dump(pkllist, open('./data.pkl', 'wb'))

# data = pickle.load(open('./data.pkl', 'rb'))
# print(data['jobs'])