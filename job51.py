#!/usr/bin/python

import requests
import random
import time
import socket
import http.client
from pymongo import MongoClient
from bs4 import BeautifulSoup
import logging
# from log import init_logging
client = MongoClient('127.0.0.1', 27017)
client.spider.authenticate('baiyang', 'baiyang')
db = client.spider
collection = db.job51


def get_content(url, data = None):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116'
    }
    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(url, headers=header, timeout=timeout)
            rep.encoding = 'gbk'
            break
        except socket.timeout as e:
            print('3:', e)
            time.sleep(random.choice(range(8, 15)))
        except socket.error as e:
            print('4:', e)
            time.sleep(random.choice(range(20, 60)))

        except http.client.BadStatusLine as e:
            print('5:', e)
            time.sleep(random.choice(range(30, 80)))

        except http.client.IncompleteRead as e:
            print('6:', e)
            time.sleep(random.choice(range(5, 15)))
    return rep.text


def get_data(html_text):
    final = []
    bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象
    content = bs.find(class_='tCompany_center')
    li = content.find(id='tHeader_mk')
    if str(li) == 'None':
        print('none')
    else:
        bid_sh = {}
        li = content.find(class_='tHeader_mk')
        bid_sh['company'] = str(li)
        bid_sh['link'] = url
        collection.insert(bid_sh)
        print(bid_sh['link'])
    return final


if __name__ == '__main__':
    for i in range(1, 10000000):
        url = 'http://jobs.51job.com/all/co'+str(i)+'.html'
        html = get_content(url)
        result = get_data(html)
