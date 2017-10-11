#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/10/11 0011 下午 13:53
# @Author  : 李雪洋
# @File    : 05.py
# @Software: PyCharm

from urllib import request
import threading
import bs4
import re
import operator

url = 'http://www.jikexueyuan.com/course/'
urls = 'http://www.jikexueyuan.com/course/?pageNum='
courseDict = {}
totalPage = 0

class workThread(threading.Thread):
    def __init__(self, threadID, st, end):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.st = st
        self.end = end
    def getid(self):
        return str(self.threadID)
    def run(self):
        print("开启线程： %d" % self.threadID)
        for k in range(self.st, self.end):
            soup = bs4.BeautifulSoup(exechttp(urls + str(k), 'utf-8'), 'html.parser')

            ul = soup.select('ul.cf')

            array = ul[0].select('li')

            for li in array:
                courseNum = li.get('id')
                box = li.select('.lessonimg-box')

                a_href = re.findall("<a href=\"//(.*?)\"", str(box[0]))
                img_alt = re.findall("<img alt=\"(.*?)\"", str(box[0]))

                # 获取锁，用于线程同步
                threadLock.acquire()
                courseDict[int(courseNum)] = img_alt[0] + '    ' + a_href[0]
                # 释放锁，开启下一个线程
                threadLock.release()

class displayThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    @staticmethod
    def getid():
        return 'display'
    def run(self):
        temp = 0
        n = 0
        while n != totalPage:
            n = len(courseDict)
            num = int(n / totalPage * 100)
            if temp != num:
                temp = num
                print("已完成" + str(num) + "%")

def exechttp(url, code):
    try:
        res = request.urlopen(url)
        recvbody = res.read().decode(code)
        return recvbody
    except Exception:
        raise Exception


try:

    threadLock = threading.Lock()
    threads = []

    data = exechttp(url, 'utf-8')

    page = re.findall("require\(\"common:widget/pager/PagerDemo.js\"\).init\(1,(\d+),24\)", data)

    totalPage = int(page[0])

    displatTT = displayThread()
    displatTT.start()
    threads.append(displatTT)

    pos = 1
    i = 1
    while pos < totalPage:
        tmp = pos + 5
        if tmp >= totalPage:
            tmp = totalPage + 1
        tt = workThread(i, pos, tmp)
        i += 1
        tt.start()
        threads.append(tt)
        pos = tmp

    for t in threads:
        t.join()
        print("线程" + t.getid() + ": 退出")

    sorted_courseDict = sorted(courseDict.items(), key=operator.itemgetter(0))

    courseStr = ''
    for course in sorted_courseDict:
        courseStr += str(course[0]) + "  " + course[1] + "\n"

    fo = open("text2.txt", "w", encoding='utf-8')
    fo.write(courseStr)
    fo.close()
except Exception as e:
    print(e)
finally:
    print('结束')