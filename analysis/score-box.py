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

if __name__ == '__main__':
    from excel_reader import excel_reader

    file_name = "movie.xls"
    sheet_num = 1
    data = excel_reader(file_name,sheet_num)


    douban_list = []
    maoyan_list = []
    box_list = []

    for item in data.items():
        pass
        data_1 = {}
        data_2 = {}
        data_3 = {}

        data_1['name'] = item[1]['name']
        data_2['name'] = item[1]['name']
        data_3['name'] = item[1]['name']
        # print(data_1['name'])

        douban_score = item[1]['douban_score']
        maoyan_score = item[1]['maoyan_score']



        data_1["sum_score"] = douban_score
        douban_list.append(data_1)

        data_2["sum_score"] = float(maoyan_score)
        maoyan_list.append(data_2)

        # box
        total_box = item[1]['total_china_box']

        if isinstance(total_box, float):
            data_3['sum_score'] = 0.0
            continue

        if total_box[-1] == "万":
            data_3['sum_score'] = (float(item[1]['total_china_box'][0:-1]) * wan) / (total_sum[item[1]['year']])
        if total_box[-1] == "亿":
            year_total = total_sum[item[1]['year']]
            data_3['sum_score'] = (float(item[1]['total_china_box'][0:-1]) * yi) / year_total
        else:
            data_3['sum_score'] = 0.0
        box_list.append(data_3)


    douban_list = sorted(douban_list, key=lambda item:item["sum_score"] ,reverse=True)
    maoyan_list = sorted(maoyan_list, key=lambda item: item["sum_score"], reverse=True)
    box_list = sorted(box_list, key=lambda item: item["sum_score"], reverse=True)

    i = 0
    douban_list1 = []
    maoyan_list1 = []
    box_list1 = []
    while i < len(douban_list):
        dd1 = {}
        dd2 = {}
        dm1 = {}
        dm2 = {}

        db1 = {}
        db2 = {}

        dd2.update(douban_list[i])
        dm2.update(maoyan_list[i])
        db2.update(box_list[i])
        rank_d ,rank_m,rank_b= 0,0,0
        if i != 0:
            if douban_list[i-1]["sum_score"] == douban_list[i]["sum_score"]:
                rank_d = douban_list1[i-1]["rank"]
            else:
                rank_d = douban_list1[i-1]["rank"]+1

            if maoyan_list[i - 1]["sum_score"] == maoyan_list[i]["sum_score"]:
                rank_m = maoyan_list1[i - 1]["rank"]
            else:
                rank_m = maoyan_list1[i - 1]["rank"] + 1

            if box_list[i - 1]["sum_score"] == box_list[i]["sum_score"]:
                rank_b = box_list1[i - 1]["rank"]
            else:
                rank_b = box_list1[i - 1]["rank"] + 1

        i = i +1
        dd1["rank"] = rank_d
        dd2.update(dd1)
        douban_list1.append(dd2)

        dm1["rank"] = rank_m
        dm2.update(dm1)
        maoyan_list1.append(dm2)

        db1["rank"] = rank_b
        db2.update(db1)
        box_list1.append(db2)

        print(box_list[i])


    gap_list_dou = []
    for item_b in box_list1:
        gap = {}
        name_b = item_b['name']
        if name_b == "水滴":
            continue
        gap['name'] = name_b
        gap['rb'] = item_b["rank"]
        for item_d in douban_list1:
            if item_d['name'] ==item_b['name']:
                gap['sum'] = item_d["rank"] + item_b["rank"]
                gap['gap'] = abs(item_d["rank"] - item_b["rank"])
                gap['rm'] = item_d["rank"]

        gap_list_dou.append(gap)

        gap_list_dou_sum = sorted(gap_list_dou, key=lambda item: item["sum"])
        gap_list_dou_gap = sorted(gap_list_dou, key=lambda item: item["gap"])







        pass

    gap_list_mao = []
    for item_b in box_list1:
        gap = {}
        name_b = item_b['name']
        if name_b == "水滴":
            continue
        gap['name'] = name_b
        gap['rb'] = item_b["rank"]
        for item_m in douban_list1:
            if item_m['name'] ==item_b['name']:
                gap['sum'] = item_m["rank"] + item_b["rank"]
                gap['gap'] = abs(item_m["rank"] - item_b["rank"])
                gap['rm'] = item_m["rank"]

        gap_list_mao.append(gap)

        gap_list_mao_sum = sorted(gap_list_mao, key=lambda item: item["sum"])
        gap_list_mao_gap = sorted(gap_list_mao, key=lambda item: item["gap"])








    list1 = []
    list2 = []
    list_m = []
    list_d = []
    for item in gap_list_dou_gap:


        s = item['name']

        import re



        list1.append(s)
        list2.append(item['gap'])
        list_d.append(item['rd'])
        list_m.append(item['rb'])

    attr = np.array(list1[0:25])
    v1 = np.array(list2[0:25])
    v2 = np.array(list_d[0:25])
    v3 = np.array(list_m[0:25])


    bar = Bar("2011-2018年科幻叫做不叫好（豆瓣）TOP25", title_pos='center', title_top='18', width=1400, height=800)

    bar.add("综合", attr, v1, is_convert=True, xaxis_min=0, xaxis_max=35, yaxis_label_textsize=25,
            is_yaxis_boundarygap=True, yaxis_interval=0, is_label_show=True, label_pos='right',
            is_yaxis_inverse=True, is_splitline_show=False)

    bar.add("豆瓣", attr, v2, is_convert=True, xaxis_min=0, xaxis_max=35, yaxis_label_textsize=25,
            is_yaxis_boundarygap=True, yaxis_interval=0, is_label_show=True, label_pos='right',
            is_yaxis_inverse=True, is_splitline_show=False,is_stack=True)
    bar.add("票房", attr, v3, is_convert=True, xaxis_min=0, xaxis_max=35, yaxis_label_textsize=25,
            is_yaxis_boundarygap=True, yaxis_interval=0, is_label_show=True,  label_pos='right',
            is_yaxis_inverse=True, is_splitline_show=False, is_stack=True)

    bar.render("2011-2018年科幻叫做不叫好（豆瓣）TOP25.html")

    pass