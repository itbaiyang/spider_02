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
collection = db.chinabidding


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
    data = bs.find(id='list')
    li = data.find_all(class_='yj_nei')
    for day in li:
        bid_sh = {}
        td_1 = day.find(class_='td_1')
        a_link = td_1.find('a')
        bid_sh['link'] = a_link.get('href')
        bid_sh['title'] = a_link.get('title')
        td_2 = day.find_all(class_='td_2')
        bid_sh['hangye'] = td_2[0].string
        bid_sh['diqu'] = td_2[1].string
        bid_sh['time'] = td_2[2].string
        print(bid_sh['time'])
        bid_html = get_content_detail('https://www.chinabidding.cn'+bid_sh['link'])
        soup = BeautifulSoup(bid_html, "html.parser")
        tr = soup.find(id="main_dom")
        bid_sh["bid_company_list"] = str(tr)
        collection.insert(bid_sh)
    return final


if __name__ == '__main__':
    # init_logging()
    for i in range(1, 313):
        url = 'https://www.chinabidding.cn/zbxx/zhongbgg/'+str(i)+'.html'
        html = get_content_detail(url)
        result = get_data(html)

