# -*- coding: utf-8 -*-
__author__ = 'CL'
__date__ = '2019/2/15 7:43 PM'
from pyecharts import Bar,Pie
import pandas as pd
import numpy as np
import pymysql
import xlrd

def excel_reader(file_name,sheet_num = 0):
    import xlrd

    book = xlrd.open_workbook(file_name, formatting_info=False)
    table = book.sheet_by_index(sheet_num)

    dict2 = {}

    colsNum = table.ncols
    rowsNum = table.nrows

    a = table.row_values(0)
    b = table.row_values(1)
    ab = dict(zip(a,b))

    for i in range(1 , rowsNum):
        c = table.row_values(i,0,colsNum)
        dict1 = dict(zip(ab,c))
        dict2[i] = dict1

    return dict2

if __name__ == '__main__':
    file_name = "movie.xls"
    sheet_num = 1
    data = excel_reader(file_name,sheet_num)

    list_countries = []
    location = {}
    total = 0

    for item in data.items():
        total = total+1
        places = item[1]['countries'].split('/')
        for place in places:
            place = place.strip()
            if place not in list_countries:
                list_countries.append(place)
                location[place] = 1
            else:
                location[place] = location[place]+1

    # total = sum(location.values())
    top10 = sorted(location.items(),key=lambda k:k[1], reverse=True)[0:10]
    # other = total
    # for item in top5:
    #     other = other - item[1]
    list1 = []
    list2 = []
    for i in top10:
        list1.append(i[0])
        list2.append(i[1])

    attr = list1
    v1 = list2

    bar = Bar("2011-2018年各国家电影数量TOP10", title_pos='center', title_top='18', width=800, height=400)
    bar.add("", attr, v1, is_stack=True, is_label_show=True)
    bar.render("2011-2018年各国家电影数量TOP10.html")

    other = total -top10[0][1]

    attr = ["美国","其他"]
    v1 = [top10[0][1],other]
    pie = Pie("2011-2018年各国参与制作科幻电影占比TOP5（包括合拍）", title_pos='center', width=900)
    import pyecharts


    l = 10
    for i in range(0,5):
        num = int(((top10[i][1])/total)*100)

        pie.add(
            "", [top10[i][0], ""], [num, 100-num], center=[l, 30], radius=[18, 24], legend_top="center",label_pos="center",
        is_label_show=True,label_text_color=None

        )
        l = l+20



    pie.render("2011-2018年各国参与制作科幻电影占比TOP5.html")




    pass




