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


    year_dic = {}
    for i in range(2011, 2019):
        year_dic[str(i)] = 0

    for item in data.items():
        year = item[1]['year']
        if year == "2019":
            continue
        year_dic[year] = year_dic[year]+1
        pass

    # year_dic = sorted(year_dic , key=lambda item:item["year"] ,reverse=True)
    pass


    list1 = list(year_dic.keys())
    list2 = list(year_dic.values())



    attr = np.array(list1)
    v1 = np.array(list2)

    bar = Bar("2011-2018年每年科幻电影上映数量", title_pos='center', title_top='18', width=800, height=400)
    bar.add("", attr, v1, is_stack=True, yaxis_max=40, is_label_show=True)

    bar.render("2011-2018年每年科幻电影上映数量.html")

    pass