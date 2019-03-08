# -*- coding: utf-8 -*- 

'''
这是一个计算origins到targets的OD矩阵的exmaple，同时这里会将解析出来的数据存在本地
'''

from BaiduMapAPI import dataset

ch_street_data_2017 = dataset.getAllChStreetCoord(2017)
gd_data_2017 = ch_street_data_2017[ch_street_data_2017["省"]=="广东省"]
