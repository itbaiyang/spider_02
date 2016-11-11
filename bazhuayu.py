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
db = client.spider
collection = db.bazhuayu


def get_content(url, data = None):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116'
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


def get_content_detail(url, data = None):
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
            rep.encoding = 'utf-8'
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
    data = bs.find(id="list")
    li = data.find_all('li')

    for day in li:
        bid_sh = {}
        pass
        a_link = day.select('li > a')
        span_link = day.select('li > span')
        for i in range(0, len(a_link)):
            print(a_link[i])
            bid_sh['title'] = a_link[0].string
            bid_sh['link'] = a_link[0].get('href')
            bid_sh['time'] = span_link[0].get('href')
            print(bid_sh['link'])
            bid_html = get_content_detail('http://www.8yu.cn'+bid_sh['link'])
            soup = BeautifulSoup(bid_html, "html.parser")
            tr = soup.find(id='view_control')
            bid_sh["bid_company_list"] = str(tr)
            collection.insert(bid_sh)
    return final


if __name__ == '__main__':
    # init_logging()
    for i in range(1, 166):
        url = 'http://www.8yu.cn/list_000000_0_0_'+str(i)+'.html'
        html = get_content_detail(url)
        result = get_data(html)