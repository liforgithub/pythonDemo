import urllib.request
import bs4
import re
import time
import pickle

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'AD_RS_COOKIE=20080919',
    'Host': 'www.stats.gov.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.113 Safari/537.36'
}
url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/'

req = urllib.request.Request(url, headers=headers)
res = urllib.request.urlopen(req).read()

soup = bs4.BeautifulSoup(res, 'html.parser')

list_province = soup.select(".provincetr")

# 录取省
for tr in list_province:
    a_list = tr.select('a')
    for a in a_list:
        pickle.dump({
            'children': [],
            'label': a.text,
            'href': a.get('href'),
            'value': ''
        }, open(f'./province/base/{a.text}.pkl', 'wb'))
        print(a.text)

