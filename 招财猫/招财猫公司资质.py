# -*- coding: utf-8 -*-
# @Time    : 2018/8/11 16:39
# @Author  : zqj
# @FileName: 招财猫公司资质.py
# @Software: PyCharm Community Edition
# @email   ：zihe@yscredit.com

import requests
from pyquery import PyQuery as pq
url = 'https://zcmlc.p2peye.com/'
headers = {
'Host': 'zcmlc.p2peye.com',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

try:
    r = requests.get(url=url,headers=headers)
    #print(r.status_code)
except Exception as e:
    print(e)

p = pq(r.text)

result = {}
for each in p('span.strength-title-left').items():
    title = each.text()

result['title'] = title
content = []
for each in p('div.strength-item > span').items():
    #print(each.text())
    content.append(each.text())
#print(content)
for i in range(0,len(content)-1,2):
    result[content[i]] = content[i+1]

print(result)

with open(r'/Users/zhaoqj/Desktop/招财猫公司资质.txt','w') as f:
    f.writelines(str(result))