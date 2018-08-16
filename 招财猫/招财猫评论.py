# -*- coding: utf-8 -*-
# @Time    : 2018/8/11 16:55
# @Author  : zqj
# @FileName: comment.py
# @Software: PyCharm Community Edition
# @email   ：zihe@yscredit.com

import requests
from pyquery import PyQuery as pq

url0 = 'https://zcmlc.p2peye.com/comment/list-0-0-{}.html'

headers = {
    'Host': 'zcmlc.p2peye.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}
result_total = []
for i in range(1,14):
    url = url0.format(i)
    try:
        r = requests.get(url,headers = headers)
    except Exception as e:
        print(e)

    p = pq(r.text)

    for eachs in p('li.feed-detail.clearfix > *').items():
        result = {}
        #print(eachs)
        info = []
        for each in eachs('div.info.clearfix > *').items():
            info.append(each.text())
            print('*********')
        if len(info) == 2:
            result['用户昵称'] = info[0]
            result['用户评价'] = info[1]
        for each in eachs('div.link a').items():
            result['评价内容'] = each.text()
        for each in eachs('div.qt-gl.time').items():
            result['评价时间'] = each.text()
        for each in eachs('ul.item-list').items():
            result['相关回复'] = each.text()
        print('############当前第{}页########'.format(i))
        if result:
            result_total.append(result)

with open(r'/Users/zhaoqj/Desktop/zcm/招财猫公司资质.txt','w') as f:
    f.writelines(str(result_total))

