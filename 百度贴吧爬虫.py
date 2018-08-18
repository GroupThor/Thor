# -*- coding: utf-8 -*-
# @Time    : 2018/8/18 08:23
# @Author  : zqj
# @FileName: 百度贴吧爬虫.py
# @Software: PyCharm Community Edition
# @email   ：zihe@yscredit.com

import requests
from pyquery import PyQuery as pq
import re
import urllib.parse
import json
#得到总页数
class baidutieba():
    def __init__(self):
        self.headers = {
            'Host': 'tieba.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537'
        }

    #return pages,per_page
    def get_pages(self,keyword):
        key = urllib.parse.quote(keyword)
        #print(key)
        url = 'https://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}'.format(key,0)
        r = requests.get(url,headers = self.headers)
        if r.status_code == 200:
            data = r.text
        else:
            print('爬虫首页出错，代码{}'.format(r.status_code))
            data = ''
            return data
        p = pq(data)
        second_url = p('#frs_list_pager > a:nth-child(2)').attr['href']
        third_url = p('#frs_list_pager > a:nth-child(3)').attr['href']
        last_url = p('a.last.pagination-item').attr['href']

        if last_url:
            second_num = re.compile(r'=(\d+)$', re.S).findall(second_url)
            third_num = re.compile(r'=(\d+)$',re.S).findall(third_url)
            last_num = re.compile(r'=(\d+)$', re.S).findall(last_url)
            try:
                per_page = int(third_num[0]) - int(second_num[0])
                pages = int(last_num[0])//per_page + 1
                #print(pages)
                return pages,per_page
            except:
                print('网站形式有异')
                pages = 0
                per_page = 0
                return pages,per_page
        else:
            pages = 0
            per_page = 0
            return pages,per_page

    #return num_list
    def get_perurl(self,keyword):
        pages = self.get_pages(keyword=keyword)[0]
        per_page = self.get_pages(keyword=keyword)[1]
        num_list = []
        key = urllib.parse.quote(keyword)
        if pages != 0:
            for i in range(0,pages+1):
                url = 'https://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}'.format(key,i*per_page)
                r = requests.get(url,headers = self.headers)
                if r.status_code == 200:
                    num = re.compile('href="/p/(\d+)"', re.S).findall(r.text)
                    num_list = num + num_list
                else:
                    print('遍历第{}页时出错，代码{}'.format(i+1,r.status_code))
                    pass
            return num_list
        else:
            return num_list

    #return content_total
    def get_detail(self,keyword):
        url_num_list = self.get_perurl(keyword=keyword)
        content_total = []
        for url_num in url_num_list:
            url = 'https://tieba.baidu.com/p/' + url_num
            r = requests.get(url,headers = self.headers)
            if r.status_code == 200:
                #抓取楼层信息
                p = pq(r.text)
                for eachs in p('div.l_post.l_post_bright.j_l_post.clearfix  ').items():
                    content = {}
                    tail_info = []
                    for each in eachs('span.tail-info').items():
                        # print(each.text())
                        tail_info.append(each.text())

                    post_content = []
                    for each in eachs('div.d_post_content.j_d_post_content ').items():
                        # print(each.text())
                        post_content.append(each.text())
                        post_content.append(re.compile(r'(\d+)$', re.S).findall(each.attr['id'])[0])
                        #print(each.attr['id'])

                    # print(tail_info)
                    # print('#######')
                    # print(post_content)

                    if len(tail_info) == 2:
                        content['楼层'] = tail_info[0]
                        content['发表时间'] = tail_info[1]
                    elif len(tail_info) == 3:
                        content['楼层'] = tail_info[1]
                        content['评论时间'] = tail_info[2]
                    if post_content:
                        content['评论内容'] = post_content[0]
                        content['层主id'] = post_content[1]
                    content_total.append(content)
            else:
                print('当前url:{}爬取失败,代码{}'.format(url_num,r.status_code))
                continue

            #print(content_total)
            url_reply = 'https://tieba.baidu.com/p/totalComment?tid={}&see_lz=0'.format(url_num)
            #print(url_reply)
            reply = requests.get(url_reply, headers=self.headers).text
            reply_json = json.loads(reply)
            reply_comment = reply_json.get('data', '').get('comment_list', '')
            #print(reply_comment)
            for x in content_total:
                if reply_comment:
                    id = x['层主id']
                    if id in reply_comment.keys():
                        x['楼层回复信息'] = reply_comment[id]
                    else:
                        x['楼层回复信息'] = '当前楼层暂无回复'
                else:
                    x['楼层回复信息'] = '当前楼层暂无回复'

            #print(content_total)

        return content_total




t = baidutieba()

with open(r'/Users/zhaoqj/Desktop/zcm/百度贴吧数据.txt','w') as f :
    f.writelines(str(t.get_detail("招财猫理财")))


