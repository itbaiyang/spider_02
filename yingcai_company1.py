#!/usr/bin/python

import requests
import random
import time
import socket
import http.client
from pymongo import MongoClient
from bs4 import BeautifulSoup
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
client = MongoClient('127.0.0.1', 27017)
db = client.spider_02
collection = db.yingcai
collection_company = db.company_china_yc


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
    bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象
    data = bs.find(class_='base-company')
    if data == 'None':
        print('none data')
    else:
        try:
            company_name = data.find(class_='wrap-til').find('h1').string
            final['company_name'] = company_name
            company_tag = data.find(class_='wrap-mc').find_all('em')
            if company_tag == 'None':
                print('none tag')
            else:
                position_arr = []
                for item_add in company_tag:
                    item_em = item_add.string
                    position_arr.append(str(item_em))
                final['company_tag'] = str(position_arr)
            company_detail = data.find(class_='address-company').find_all('p')
            if company_detail == 'None':
                print('none detail')
            else:
                detail = []
                for item in company_detail:
                    p_detail = item.get_text()
                    detail.append(p_detail)
            final['detail'] = str(detail)
            collection.insert(final)
        except:
            print('none')
    return final


if __name__ == '__main__':
    for i in range(100001, 200000):
        print(str(i))
        url = 'http://www.chinahr.com/company/20-'+str(i)+'.html'
        html = get_content(url)
        result = get_data(html)

