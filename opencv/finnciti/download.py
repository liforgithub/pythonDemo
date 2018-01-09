#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2017/11/8 0008 下午 19:18
# @Author  : 李雪洋
# @File    : download.py
# @Software: PyCharm

# https://hq.cbss.10010.com/image?mode=validate&width=60&height=20&random=0.5718313927110062
import requests
import os, base64


def download(n):
    url = 'https://www.finnciti.com/bdcohio.php?get=image&c=captcha&t=6a632e7c838cfad8ce626eeab83afd95&d=1510538479958'
    headers = {
        'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'accept-language': 'zh-CN,zh;q = 0.8',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://www.finnciti.com/?page=market_building_material',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    cookie = dict(cookies_are='visid_incap_1334872=2NGqyDyKR5+9Ebx7NutqvQdsCVoAAAAAQUIPAAAAAAC9D7BJcEcLfwcqr82ob7+J; incap_ses_452_1334872=4T0JYz8mb0m5bqoxY9RFBgdsCVoAAAAAMsFKWIKiNjDjUAO71WfwkQ==; incap_ses_869_1334872=4AFPTAABhizKUO2r9U4PDESCCVoAAAAAyzTYhVyEljbp7JuoUrb0Jg==; __utmt=1; __utma=220632335.1924314676.1510572647.1510572647.1510572647.1; __utmb=220632335.1.10.1510572647; __utmc=220632335; __utmz=220632335.1510572647.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); PHPSESSID=4v9bc5k0cd01nm52o33478f7o2; lastlogindt=2017-11-13+09%3A55%3A56; language=1; profilepic=1')
    res = requests.get(url, headers=headers, cookies=cookie)
    with open('E:\\pythonDemo\\opencv\\finnciti\\img\\' + str(n) + '.bmp', 'wb') as f:
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
        f.close()
    print(n)


for i in range(1, 101):
    download(i)
