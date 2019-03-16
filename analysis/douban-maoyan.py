# -*- coding: utf-8 -*-
__author__ = 'CL'
__date__ = '2019/2/15 3:22 PM'
from pyecharts import Bar
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


    douban_list = []
    maoyan_list = []

    for item in data.items():
        pass
        data_1 = {}
        data_2 = {}

        data_1['name'] = item[1]['name']
        data_2['name'] = item[1]['name']
        # print(data_1['name'])

        douban_score = item[1]['douban_score']
        maoyan_score = item[1]['maoyan_score']


        data_1["sum_score"] = douban_score
        douban_list.append(data_1)

        data_2["sum_score"] = float(maoyan_score)
        maoyan_list.append(data_2)
    douban_list = sorted(douban_list, key=lambda item:item["sum_score"] ,reverse=True)
    maoyan_list = sorted(maoyan_list, key=lambda item: item["sum_score"], reverse=True)

    i = 0
    douban_list1 = []
    maoyan_list1 = []
    while i < len(douban_list):
        dd1 = {}
        dd2 = {}
        dm1 = {}
        dm2 = {}

        dd2.update(douban_list[i])
        dm2.update(maoyan_list[i])
        rank_d ,rank_m= 0,0
        if i != 0:
            if douban_list[i-1]["sum_score"] == douban_list[i]["sum_score"]:
                rank_d = douban_list1[i-1]["rank"]
            else:
                rank_d = douban_list1[i-1]["rank"]+1

            if maoyan_list[i - 1]["sum_score"] == maoyan_list[i]["sum_score"]:
                rank_m = maoyan_list1[i - 1]["rank"]
            else:
                rank_m = maoyan_list1[i - 1]["rank"] + 1

        i = i +1
        dd1["rank"] = rank_d

        dd2.update(dd1)
        douban_list1.append(dd2)

        dm1["rank"] = rank_m
        dm2.update(dm1)
        maoyan_list1.append(dm2)


    gap_list = []
    for item_d in douban_list1:
        gap = {}
        name_d = item_d['name']
        if name_d == "水滴":
            continue
        gap['name'] = name_d
        for item_m in maoyan_list1:
            if item_m['name'] ==item_d['name']:
                gap['gap'] = abs(item_m["rank"] - item_d["rank"])

        gap_list.append(gap)

        gap_list = sorted(gap_list, key=lambda item: item["gap"], reverse=True)



        pass








    list1 = []
    list2 = []
    for item in gap_list:


        s = item['name']

        import re



        list1.append(s)
        list2.append(item['gap'])

    attr = np.array(list1[0:25])
    v1 = np.array(list2[0:25])

    bar = Bar("2011-2018年科幻电影豆瓣猫眼排名差TOP25", title_pos='center', title_top='18', width=1400, height=800)
    bar.add("", attr, v1, is_convert=True, xaxis_min=10, xaxis_max=35, yaxis_label_textsize=25,
            is_yaxis_boundarygap=True, yaxis_interval=0, is_label_show=True, is_legend_show=False, label_pos='right',
            is_yaxis_inverse=True, is_splitline_show=False)

    bar.render("2011-2018年科幻电影豆瓣猫眼排名差TOP25.html")

    pass