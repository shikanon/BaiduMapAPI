# coding=utf-8
'''
# Author: shikanon (shikanon@tensorbytes.com)
# File Created Time: 2020-02-13 8:57:41
# 
# Project: website
# File: run.py
# Description: 
# 
'''
import os

from baidumap import BaiduMap, DataBase
from util import read_data, logsys, recovsys


logger = logsys(__file__,level=10).getlogger()
recov = recovsys()
AK = os.environ["BaiduAK"]
SK = os.environ["BaiduSK"]


def initdb():
    db = DataBase(scheme="mysql+pymysql://root:shikanon@127.0.0.1:13036/baiduapi")
    db.reset()
    return db


def run():
    db = initdb()
    o = read_data("中国城市坐标D.xls")
    d = read_data("中国城市坐标D.xls")
    logger.info("成功加载文件")
    bmap = BaiduMap(AK, SK)
    # 加载数据
    if recov.hasfile:
        datas = recov.recover()
        for data in datas:
            bmap.load_data(**data)
    else:
        for i in o.index:
            for j in d.index:
                if i >= j:
                    continue
                data = {
                    "origin": "%s,%s"%(o.iloc[i].y, o.iloc[i].x),
                    "destination": "%s,%s"%(d.iloc[j].y, d.iloc[j].x)
                }
                bmap.load_data(**data)
    logger.info("完成数据加载")
    # 开始写入
    for result in bmap.get_train_data():
        try:
            db.insert_transit(result)
        except Exception:
            logger.error("写入失败")


run()