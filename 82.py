import re
import urllib.request

try:
    res = urllib.request.urlopen('http://npm.qianmi.com/package/@qianmi/bm-x-site-openapi')

    if res.getcode() != 200:
        print("页面返回失败")
    data = res.read().decode('utf-8')
    version = re.findall("<img title=\"(.*?)\"", data)
    print(version[0])

except Exception as e:
    print(e)
finally:
    print("结束")
