import urllib.request
import bs4

res = urllib.request.urlopen('http://news.sina.com.cn/china/').read()

data = res.decode('utf-8')

soup = bs4.BeautifulSoup(data, 'html.parser')

list_a = soup.select('.newsItem')

for a in list_a:
    print(a.text)