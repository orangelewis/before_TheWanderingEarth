# -*- coding: utf-8 -*-
__author__ = 'CL'
__date__ = '2019/2/15 2:49 PM'


from pyecharts import Bar
import pandas as pd
import numpy as np
import pymysql
import xlrd

total_sum = {}
yi = 100000000
wan = 10000
total_sum['2011'] = 131*yi
total_sum['2012'] = 171*yi
total_sum['2013'] = 218*yi
total_sum['2014'] = 296*yi
total_sum['2015'] = 441*yi
total_sum['2016'] = 454*yi
total_sum['2017'] = 558*yi
total_sum['2018'] = 606*yi
total_sum['2019'] = 115*yi

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

    year_dic = {}
    for i in range(2011, 2019):
        year_dic[str(i)] = 0.0


    for item in data.items():
        pass
        data_1 = {}
        year = item[1]['year']

        if year == "2019":
            continue


        total_box = item[1]['total_china_box']


        if isinstance(total_box,float) :
            continue

        if total_box[-1] == "万":
            year_dic[year] = year_dic[year] + float(total_box[0:-1])*wan
        if total_box[-1] == "亿":
            year_dic[year] = year_dic[year] + float(total_box[0:-1])*yi


        else:
            continue

    list1 = list(year_dic.keys())
    list2 = []
    list3 = []
    for i in year_dic.items():

        p = (i[1]/(total_sum[i[0]]))*100
        list2.append('%.2f' %(p))
        list3.append('%.2f' %(100-p))

    attr = np.array(list1)
    v1 = np.array(list2)
    v2 = np.array(list3)

    bar = Bar("2011-2018年每年科幻电影票房占比(%)", title_pos='center', title_top='18', width=800, height=400)
    bar.add("科幻片占比", attr, v1, is_stack=True, yaxis_max=100,yaxis_min=0,mark_line=["average"], mark_point=["max", "min"])
    bar.add("非科幻片占比", attr, v2, is_stack=True, yaxis_max=100, yaxis_min=0)

    bar.render("2011-2018年每年科幻电影票房占比.html")

    pass