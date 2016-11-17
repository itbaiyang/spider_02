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
collection = db.yingcai
collection_company = db.company_mz


def get_content(url_list, data = None):
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
            rep = requests.get(url_list, headers=header, timeout=timeout)
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
    final = {}
    position_arr = []
    bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象
    data = bs.find(id='searchList')
    position_list = data.find(class_='resultList')
    data_list = position_list.find_all(class_='jobList')
    final['link'] = url
    final['name'] = i['search_key']
    # final['name'] = i
    for day in data_list:
        bid_sh = {}
        li_data = day.find_all('li')
        bid_sh['position_name'] = li_data[0].find(class_='e1').find('a').string
        bid_sh['position_time'] = li_data[0].find(class_='e2').string
        bid_sh['position_company'] = li_data[0].find(class_='e3').find('a').string
        bid_sh['position_address'] = li_data[1].find(class_='e1').string
        bid_sh['position_money'] = li_data[1].find(class_='e2').string
        other_message = li_data[1].find(class_='e3').find_all('em')
        bid_sh['position_category'] = other_message[0].string
        bid_sh['position_class'] = other_message[1].string
        bid_sh['position_mans'] = other_message[2].string
        position_arr.append(bid_sh)
    print(url)
    final['position'] = str(position_arr)
    collection.insert(final)
    return final


if __name__ == '__main__':
    for i in collection_company.find():
        print(str(i))
        url = 'http://www.chinahr.com/sou/?city=34%2C398&keyword='+i['search_key']
        html = get_content(url)
        result = get_data(html)
    # i = '北京国联景行信息科技有限公司'
    # url = 'http://www.chinahr.com/sou/?city=34%2C398&keyword=北京国联景行信息科技有限公司'
    # html = get_content(url)
    # result = get_data(html)
