# -*- coding: utf-8 -*-
__author__ = 'CL'
__date__ = '2019/2/15 1:09 AM'
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
    excel_reader(file_name,sheet_num)

