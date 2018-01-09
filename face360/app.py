#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/12/22 0022 下午 13:55
# @Author  : 李雪洋
# @File    : app.py
# @Software: PyCharm

from flask import *
import face_recognition
import os
import base64
import cv2

app = Flask(__name__)

imageTypeList = ['image/jpg', 'image/jpeg', 'image/png']

SRC_IMG_PATH = 'E:\\pythonDemo\\face360\\src\\'
TMP_IMG_PATH = 'E:\\pythonDemo\\face360\\tmp\\'


def getSuccessRes(data):
    return jsonify({
        'data': data,
        'rescode': 200,
        'result': 'success'
    }), 200


def getFailRes(data):
    return jsonify({
        'data': data,
        'rescode': 200,
        'result': 'fail'
    }), 200


def saveImg(bob, fileBasePath):
    fileName = bob.filename
    fileType = bob.mimetype
    print(f"----------------接受图片上传------------------")
    print(f"文件名：{fileName}")
    print(f"文件类型：{fileType}")

    if fileType not in imageTypeList:
        raise Exception("需上传image/jpg, image/jpeg, image/png类型的图片")

    if os.path.exists(f'{fileBasePath}{fileName}'):
        raise Exception("该文件名已存在，请修改文件名重新上传")

    with open(f'{fileBasePath}{fileName}', 'wb') as f:
        f.write(bob.read())
        f.flush()
        f.close()

    if not os.path.exists(f'{fileBasePath}{fileName}'):
        raise Exception('文件上传失败')


def compareFaces(filePath):
    name = ''
    try:
        fileList = os.listdir(SRC_IMG_PATH)
        labels = []
        encodingList = []
        for file in fileList:
            img = face_recognition.load_image_file(f'{SRC_IMG_PATH}{file}')
            fileName = os.path.basename(file)
            if fileName.find('.'):
                name = fileName[0:fileName.find('.')]
            labels.append(name)
            encodingList.append(face_recognition.face_encodings(img)[0])

        img = face_recognition.load_image_file(filePath)
        unknown_encoding = face_recognition.face_encodings(img)[0]
        results = face_recognition.compare_faces(encodingList, unknown_encoding)

        for i in range(0, len(results)):
            if results[i]:
                name = labels[i]
                print('The person is:' + labels[i])

    except Exception as err:
        msg = err
        if err == 'list index out of range':
            msg = '未提取到头像信息'
        name = msg
    finally:
        return name


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/recognition', methods=['POST'])
def recognition():
    bob = request.files['file']
    try:
        if os.path.exists(f'{TMP_IMG_PATH}{bob.filename}'):
            os.remove(f'{TMP_IMG_PATH}{bob.filename}')
        saveImg(bob, TMP_IMG_PATH)
        print(f"----------------文件上传成功------------------")
    except Exception as err:
        print(err)
        print(f"----------------文件上传失败------------------")
        return getFailRes(str(err))

    print(f"----------------比对文件开始------------------")
    name = compareFaces(f'{TMP_IMG_PATH}{bob.filename}')
    print(f'srcName={bob.filename}')
    print(f'checkName={name}')
    print(f"----------------比对文件结束------------------")
    if os.path.exists(f'{TMP_IMG_PATH}{bob.filename}'):
        os.remove(f'{TMP_IMG_PATH}{bob.filename}')
    return getSuccessRes(name)


@app.route('/upload', methods=['POST'])
def uploadImg():
    bob = request.files['file']
    try:
        saveImg(bob, SRC_IMG_PATH)
        print(f"----------------文件上传成功------------------")
        return getSuccessRes('文件上传成功')
    except Exception as err:
        print(err)
        print(f"----------------文件上传失败------------------")
        return getFailRes(str(err))


def findFace(image):
    face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model='cnn')
    top, right, bottom, left = face_locations[0]
    return image[top:bottom, left:right]


@app.route('/compareFace', methods=['POST'])
def compareFace():
    if os.path.exists(f'{TMP_IMG_PATH}1.jpg'):
        os.remove(f'{TMP_IMG_PATH}1.jpg')
    if os.path.exists(f'{TMP_IMG_PATH}2.jpg'):
        os.remove(f'{TMP_IMG_PATH}2.jpg')
    print('-------------删除图片-------------------')

    uploadImgUrl = request.json['uploadImgUrl']
    imgUrl = request.json['imgUrl']

    uploadImgUrl = uploadImgUrl[uploadImgUrl.find(',') + 1:]
    imgUrl = imgUrl[imgUrl.find(',') + 1:]

    uploadImgUrl = uploadImgUrl.replace(' ', '+', 10000)
    imgUrl = imgUrl.replace(' ', '+', 10000)

    uploadImgUrl_base64 = base64.b64decode(uploadImgUrl)
    imgUrl_base64 = base64.b64decode(imgUrl)

    file_uploadImgUrl = open(f'{TMP_IMG_PATH}1.jpg', 'wb')
    file_imgUrl = open(f'{TMP_IMG_PATH}2.jpg', 'wb')
    file_uploadImgUrl.write(uploadImgUrl_base64)
    file_imgUrl.write(imgUrl_base64)
    file_uploadImgUrl.flush()
    file_imgUrl.flush()
    file_uploadImgUrl.close()
    file_imgUrl.close()

    try:
        img_1 = face_recognition.load_image_file(f'{TMP_IMG_PATH}1.jpg')
        img_2 = face_recognition.load_image_file(f'{TMP_IMG_PATH}2.jpg')
        img1_face = findFace(img_1)
        img2_face = findFace(img_2)
        cv2.imwrite(f'{TMP_IMG_PATH}1_face.jpg', img1_face)
        cv2.imwrite(f'{TMP_IMG_PATH}2_face.jpg', img2_face)
        img_1_encoding = face_recognition.face_encodings(img1_face)[0]
        img_2_encoding = face_recognition.face_encodings(img2_face)[0]
        name = face_recognition.compare_faces([img_1_encoding], img_2_encoding)
        if name[0]:
            name = '匹配'
        else:
            name = '不匹配'
        return getSuccessRes(name)
    except Exception as err:
        msg = str(err)
        if str(err) == 'list index out of range':
            msg = '未提取到头像信息'
        return getFailRes(msg)


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=80)
