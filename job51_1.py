#!/usr/bin/python

import requests
import random
import time
import socket
import http.client
from pymongo import MongoClient
from bs4 import BeautifulSoup

client = MongoClient('127.0.0.1', 27017)
# client.spider.authenticate('baiyang', 'baiyang')
db = client.spider
collection = db.job51_1


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
        print('none', url)
    else:
        bid_sh = {}
        pass
        name = content.find('h1').string
        detail = content.find(class_='ltype')
        summary = content.find(class_='con_msg')
        position = content.find(class_='table_list')
        bid_sh['name'] = name
        # print(bid_sh['name'])
        bid_sh['link'] = url
        # bid_sh['detail'] = str(detail)
        # bid_sh['summary'] = str(summary)
        if str(position) == 'None':
            print('no position', url)
        else:
            list_ul = position.find(id='joblistdata')
            list_item = list_ul.find_all(class_='el')
            position_arr = []
            for item in list_item:
                position_detail = {}
                pass
                position_detail['position_name'] = item.find('a').string
                position_detail['position_need'] = item.find(class_='t2').string
                position_detail['position_addr'] = item.find(class_='t3').string
                position_detail['position_money'] = item.find(class_='t4').string
                position_detail['position_time'] = item.find(class_='t5').string
                position_arr.append(position_detail)
            bid_sh['position'] = str(position_arr)
        collection.insert(bid_sh)
    return final


if __name__ == '__main__':
    for i in range(1000001, 2000000):
        url = 'http://jobs.51job.com/all/co'+str(i)+'.html'
        html = get_content(url)
        result = get_data(html)
