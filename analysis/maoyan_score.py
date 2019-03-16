# -*- coding: utf-8 -*-
__author__ = 'CL'
__date__ = '2019/2/15 3:05 PM'

# -*- coding: utf-8 -*-
__author__ = 'CL'
__date__ = '2019/2/15 2:49 PM'

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


    data_list = []

    for item in data.items():
        pass
        data_1 = {}

        data_1['name'] = item[1]['name']
        # print(data_1['name'])

        maoyan_score = item[1]['maoyan_score']


        data_1["sum_score"] = float(maoyan_score)
        data_list.append(data_1)
    data_list = sorted(data_list , key=lambda item:item["sum_score"] ,reverse=True)


    list1 = []
    list2 = []

    for item in data_list:


        s = item['name']

        import re



        list1.append(s)
        list2.append(item['sum_score'])

    attr = np.array(list1[0:10])
    v1 = np.array(list2[0:10])

    bar = Bar("2011-2018年科幻电影猫眼评分TOP10", title_pos='center', title_top='18', width=1400, height=400)
    bar.add("", attr, v1, is_convert=True, xaxis_min=8, xaxis_max=9.8, yaxis_label_textsize=10,
            is_yaxis_boundarygap=True, yaxis_interval=0, is_label_show=True, is_legend_show=False, label_pos='right',
            is_yaxis_inverse=True, is_splitline_show=False)

    bar.render("2011-2018年科幻电影猫眼评分TOP10.html")

    pass