# -*- coding: utf-8 -*-
__author__ = 'CL'
__date__ = '2019/2/14 6:55 PM'

import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import datetime

def yearly_box(year):
    date = datetime.datetime.strptime("{}-01-01".format(str(year)),"%Y-%m-%d")
    end_date = datetime.datetime.strptime("{}-12-31".format(str(year)),"%Y-%m-%d")
    total = 0

    while date <= end_date:
        url = "https://piaofang.maoyan.com/dashboard?date={}".format(date.strftime("%Y-%m-%d"))
        result = requests.get(url)
        html = result.text
        soup = BeautifulSoup(html, 'html.parser')
        data_1 = soup.find_all('span', {'class': 'cal-box-num'})
        date = date+datetime.timedelta(days=1)
        print(url)


    pass

if __name__ == '__main__':
    yearly_box(2011)
    pass