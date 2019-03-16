# -*- coding: utf-8 -*-
__author__ = 'CL'
__date__ = '2019/2/12 3:43 PM'

import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import json,xlwt
from fake_useragent import UserAgent

ua = UserAgent()

def get_url_douban():


    start = 0
    spider_count = 0

    jsonList = []
    while start <=1220:

        douban_url = "https://movie.douban.com/tag/%E7%A7%91%E5%B9%BB?start={}&type=R".format(str(start))
        douban_result = requests.get(douban_url,headers = {'User-Agent': ua.random})
        html = douban_result.text
        soup = BeautifulSoup(html, 'html.parser')
        data_1 = soup.find_all('div', {'class': 'pl2'})
        for item in data_1:
            data = {}
            url = item.select('a')[0]
            url1 = url.attrs['href']
            name_pattern = " ([\s\S]*?)\n"
            name = re.findall(name_pattern,url.contents[0])[0].strip()

            print("正在爬取《{}》:".format(name))

            star = item.select('div')[0]
            if len(star.contents) == 5:
                print('《{}》'.format(name)+"还未上映\n")
                continue

            score = star.contents[3].contents[0]

            date = item.select('p')[0].contents[0]
            if "(中国大陆)" not in date:
                print('《{}》'.format(name)+"大陆未引进\n")
                continue
            date_pattern = "(.*?)\(中国大陆"
            date1 = re.findall(date_pattern,date)[0].strip()
            date1 = date1[-10:]

            import datetime

            time1 = datetime.datetime.strptime(date1,"%Y-%m-%d")


            if time1 > datetime.datetime.today():
                print('《{}》'.format(name)+"中国大陆还未上映\n")
                continue

                pass



            id_pattern = "t/(\d*?)/"
            id = re.findall(id_pattern,url1)[0]



            data["name"] = name
            data["douban_id"] = id
            data["date"] = date1
            data["year"] = date1[0:4]
            data["douban_score"] =score

            # if spider_count == 9:
            #     spider_count = 0
            #     print("\n休息一下，防止ip被封\n")
            #     time.sleep(60)


            d_dou = douban_detail(id)
            if "False" in d_dou:
                print('《{}》是电视剧\n'.format(name))
                continue

            d_mao = maoyan(name,date1)

            d3 = {}
            d3.update(data)
            d3.update(d_dou)
            d3.update(d_mao)
            jsonList.append(d3)
            print(d3)
            print("\n")

            spider_count = spider_count + 1

        start = start+20
    return jsonList


def douban_detail(id):
    # api_url = "https://api.douban.com/v2/movie/subject/{}".format(id)
    # data = {}
    #
    #
    # result = requests.get(api_url)
    # result_json = json.loads(result.text.encode("utf-8"))
    #
    #
    # if result_json['episodes_count'] is not None:
    #     data['False'] = 'False'
    #     return data
    #
    # year = result_json['year']
    # countries = result_json['countries']

    data = {}

    url1 = "https://movie.douban.com/subject/{}".format(id)
    douban_result = requests.get(url1,headers = {'User-Agent': ua.random})
    html = douban_result.text
    soup = BeautifulSoup(html, 'html.parser')
    info = soup.find_all('div',{'id':'info'})[0]
    if "集数" in info.text:
        data['False'] = 'False'
        print()
        return data
        pass


    runtime = soup.find_all('span', {'property': 'v:runtime'})[0].attrs['content']
    countries_pattern = "地区:(.*?)\n"
    countries = re.findall(countries_pattern,info.text)[0]



    data['countries'] = countries
    data['runtime'] = runtime

    return data




    pass




def list2json(jL,fileName):

    with open("./movie.json", 'w', encoding='utf-8') as json_file:
        json.dump(jL, json_file, ensure_ascii=False)

   #


    # book =xlwt.Workbook()
    # sheet = book.add_sheet('sheet')
    # title = ['name','double_url','date','douban_score','maoyan_url','total_box','trailer_play_num','maoyan_score']
    # for col in range (len (title)):
    #     sheet.write(0,col,title[col])
    #
    # row = 1
    # for k in j:



def maoyan(name,douban_date):
    id = 0
    url = "https://piaofang.maoyan.com/search?key="+quote(name)
    maoyan_result = requests.get(url,headers = {'User-Agent': ua.random})
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
    # d1['maoyan_url'] = url
    d1['maoyan_id'] = id
    d2 = maoyan_detail(id)
    d3 = {}
    d3.update(d1)
    d3.update(d2)
    return d3

def maoyan_detail(id):
    data = {}
    url_box = "https://piaofang.maoyan.com/movie/{}".format(id)
    # url_trailers = "https://piaofang.maoyan.com/movie/{}/promotion/trailers".format(id)

    maoyan_box = requests.get(url_box,headers = {'User-Agent': ua.random})
    html = maoyan_box.text
    soup = BeautifulSoup(html, 'html.parser')
    data_1 = soup.find_all('span', {'class': 'rating-num'})
    if len(data_1) == 0:
        score = "0"
    else:
        score = data_1[0].string

    modul_box = soup.find_all('span', {'class': 'detail-num'})
    if len(modul_box) == 0:
        total_box = "0"
    else:

        num = modul_box[0].text
        unit = soup.find_all('span', {'class': 'detail-unit'})[0].text
        total_box = num + unit

    data["total_china_box"] = total_box
    data["maoyan_score"] = score



    if len(soup.find_all('div' , {'class':'NAmerican-show'})) != 0:
        num = soup.find_all('div', {'class': 'item'})[1].contents[3].text
        data["total_NA_box"] = num
    else:
        data["total_NA_box"] = "美国没上映"


    #预告片
    # maoyan_trailers = requests.get(url_trailers)
    # html = maoyan_trailers.text
    # soup = BeautifulSoup(html, 'html.parser')
    # if len(soup.find_all('div', {'class': 'nodata-content'})) != 0:
    #     data["trailer_play_num"] = "没有相关数据"
    #
    # else:
    #     trailer_play_num = soup.find_all('div', {'class': 'play-number'})[0].contents[1].text
    #
    #     data["trailer_play_num"] = trailer_play_num

    return data



def json2excel(fileName):
    jsonfile = json.load(open("movie" + ".json", "r", encoding="utf-8"))

    print (jsonfile)
    workbook = xlwt.Workbook()
    sheet1 = workbook.add_sheet('movie')
    ll = list(jsonfile[0].keys())
    for i in range(0,len(ll)):
        sheet1.write(0,i,ll[i])
    for j in range(0,len(jsonfile)):
        m = 0
        ls = list(jsonfile[j].values())
        for k in ls:
            sheet1.write(j+1,m,k)
            m += 1
    workbook.save('movie.xls')

if __name__ == '__main__':

    jL = get_url_douban()
    fileName = "sci-movie"
    #list2json(jL,fileName)
    json2excel(fileName)
    pass
