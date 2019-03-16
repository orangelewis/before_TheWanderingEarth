# -*- coding: utf-8 -*-
__author__ = 'CL'
__date__ = '2019/2/12 8:38 PM'

import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

def maoyan():
    name = "攻壳机动队"
    douban_date = "2017-04-07"
    id = 0
    url = "https://piaofang.maoyan.com/search?key="+quote(name)
    maoyan_result = requests.get(url)
    html = maoyan_result.text
    soup = BeautifulSoup(html, 'html.parser')
    data_1 = soup.find_all('article', {'class': 'indentInner canTouch'})
    for item in data_1:
        date = item.contents[5].contents[0]
        if douban_date in date:
            id = item.attrs['data-url']
            id_pattern = "\d{1,10}"
            id = re.findall(id_pattern,id)[0]

            break
        pass
    d1 = {}
    d1['maoyan_url'] = url
    d2 = maoyan_detail(id)
    d3 = {}
    d3.update(d1)
    d3.update(d2)
    return d3

def maoyan_detail(id):
    data = {}
    url_box = "https://piaofang.maoyan.com/movie/{}".format(id)
    url_trailers = "https://piaofang.maoyan.com/movie/{}/promotion/trailers".format(id)

    maoyan_box = requests.get(url_box)
    html = maoyan_box.text
    soup = BeautifulSoup(html, 'html.parser')
    data_1 = soup.find_all('span', {'class': 'rating-num'})
    score = data_1[0].string

    date_2 = soup.find_all('div', {'class': 'info-block'})
    box = date_2[2].contents[5]
    num = soup.find_all('span', {'class': 'detail-num'})[0].text
    unit = soup.find_all('span', {'class': 'detail-unit'})[0].text
    total_box = num+unit
    data["total_box"] = total_box
    data["maoyan_score"] = score



    maoyan_trailers = requests.get(url_trailers)
    html = maoyan_trailers.text
    soup = BeautifulSoup(html, 'html.parser')
    if len(soup.find_all('div', {'class': 'nodata-content'})) != 0:
        data["trailer_play_num"] = "没有相关数据"

    else :
        trailer_play_num = soup.find_all('div', {'class': 'play-number'})[0].contents[1].text




        data["trailer_play_num"] = trailer_play_num

    print(data)
    return data




if __name__ == '__main__':
    date = maoyan()