#coding:utf-8

import os
from baidumap import BaiduMap, DataBase

AK = os.environ["BaiduAK"]
SK = os.environ["BaiduSK"]

# CREATE DATABASE baiduapi CHARACTER SET UTF8;

def test_BaiduMap():
    db = DataBase(scheme="mysql+pymysql://root:shikanon@127.0.0.1:13036/baiduapi")
    db.reset()
    bmap = BaiduMap(AK, SK)
    bmap.load_data("40.056878,116.30815","31.222965,121.505821")
    result = [i for i in bmap.get_bus_data()]
    db.insert_transit(result)
