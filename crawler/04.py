#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/10/11 0011 上午 10:12
# @Author  : 李雪洋
# @File    : 04.py
# @Software: PyCharm

from urllib import request
import bs4
import re

def exechttp(url, code):
    try:
        res = request.urlopen(url)
        recvbody = res.read().decode(code)
        return recvbody
    except Exception as ee:
        print(ee)

url = 'http://www.jikexueyuan.com/course/'
urls = 'http://www.jikexueyuan.com/course/?pageNum='
courseList = []

try:

    data = exechttp(url, 'utf-8')

    page = re.findall("require\(\"common:widget/pager/PagerDemo.js\"\).init\(1,(\d+),24\)", data)

    totalPage = int(page[0])

    courseStr = ''
    for i in range(1, totalPage + 1):

        soup = bs4.BeautifulSoup(exechttp(urls + str(i), 'utf-8'), 'html.parser')

        array_li = soup.select('.lessonimg-box')

        for li in array_li:
            a_href = re.findall("<a href=\"//(.*?)\"", str(li))
            img_alt = re.findall("<img alt=\"(.*?)\"", str(li))
            courseList.append(img_alt[0] + '    ' + a_href[0])
            courseStr += img_alt[0] + '    ' + a_href[0] + '\n'

        print(str(round(len(courseList)/2303, 2)) + "%")

    fo = open("text.txt", "w", encoding='utf-8')
    fo.write(courseStr)
    fo.close()

except Exception as e:
    print(e)
finally:
    print('结束')