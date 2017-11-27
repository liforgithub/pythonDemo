#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/11/10 0010 下午 15:53
# @Author  : 李雪洋
# @File    : ocr-1.py
# @Software: PyCharm

import pytesseract
from PIL import Image

# 二值化
threshold = 140
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'

im = Image.open('./../1.bmp')

# 转化到灰度图
imgry = im.convert('L')
# 二值化，采用阈值分割法，threshold为分割点
out = imgry.point(table, '1')
out.show()

code = pytesseract.image_to_string(out, config=tessdata_dir_config)

print(code)