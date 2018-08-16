# -*- coding: utf-8 -*-
# @Time    : 2018/8/11 18:59
# @Author  : zqj
# @FileName: 招财猫工商信息.py
# @Software: PyCharm Community Edition
# @email   ：zihe@yscredit.com

import requests
from pyquery import PyQuery as pq
url = 'https://zcmlc.p2peye.com/beian/'

headers = {
    'Host': 'zcmlc.p2peye.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

r = requests.get(url,headers=headers)
print(r.status_code)
p = pq(r.text)

result_total = {}
result1 = {}
for each in p('div.kvs > *').items():
    result = each.text().split('\n',1)
    result1[result[0]] = result[1]


result_total['工商信息'] = result1

result21 = []
result2 = {}

for eachs in p('div.tbl_body#tbl_gdxx').items():
    for each in p('div.tbl_tr').items():
        a = each.text().split('\n')
        result2['股东名称'] = a[0]
        result2['持股比例'] = a[1]
        result2['认缴出资'] = a[2]
        result21.append(result2)

result_total['股东信息'] = result21


result3 = []
for each in p('div.kvs.kvs_zyry > div > div').items():
    result3.append(each.text())
result31 = {}
for i in range(0,len(result3)-1,2):
    result31[result3[i]] = result3[i+1]

result_total['主要成员'] = result31

result4 = []
result41 = {}
for each in p('div.kvs.kvs_baxx > div > *').items():
    result4.append(each.text())
for i in range(0,len(result4)-1,2):
    result41[result4[i]] = result4[i+1]

result_total['备案信息'] = result41
#print(result_total)

#变更记录是post请求

url_post = 'https://zcmlc.p2peye.com/comchanajax/?pid=2753&pn={}'

headers_post = {
    'Host': 'zcmlc.p2peye.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
result5 = []
for i in range(1,6):
    url = url_post.format(i)
    data = {
        'currPage': str(i),
        'pageSize': '5'
    }
    r = requests.post(url = url,headers =headers_post,data = data)
    print(r.status_code)
    r.encoding = r.apparent_encoding
    content = eval(r.text.replace('<em>','').replace('<\\/em>','').replace('\r\n','')).get('data','').get('data','')
    #print(type(eval(r.text)))
    result5.append(content)
result_total['变更情况'] = result5
print(result_total)
with open(r'/Users/zhaoqj/Desktop/zcm/招财猫详细信息.txt','w') as f:
    f.writelines(str(result_total))





