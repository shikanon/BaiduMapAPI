# -*- coding: utf-8 -*- 

'''
这是一个计算origins到targets的自驾行车OD矩阵的exmaple，同时这里会将解析出来的数据存在本地
'''

import pandas as pd
import json
import os

from BaiduMapAPI.api import SearchPlace, MapDirection


AK = os.environ["BaiduAK"]
SK = os.environ["BaiduSK"]

origins_data = pd.read_csv("data/exmaple_citydata_coords.csv", encoding="utf-8")
targets_name = {
    "香港":"香港国际机场", "广州": "广州白云国际机场", "深圳":"深圳宝安国际机场", 
    "珠海":"珠海金湾国际机场", "澳门":"澳门国际机场", "佛山":"佛山沙堤机场", 
    "惠州":"惠州平潭机场"
}

place = SearchPlace(AK, SK)

for name in targets_name:
    pois = place.search(targets_name[name], region=name)
    poi = pois[0]

dirction = MapDirection(AK, SK)

loc = poi.get_location()

fw = open("driving_result.csv", "w", encoding="utf-8")
fw.write("origin, target, distance, duration, toll \n")

for i in origins_data.index:
    coords = (origins_data["lat"][i],origins_data["lng"][i])
    content = dirction.driving(loc, coords)
    content = json.loads(content)
    origin = origins_data["详细地址"][i]
    target = targets_name[name]
    # 常规路线的距离和时间
    driving_distance = content["result"]['routes'][0]["distance"]
    driving_duration = content["result"]['routes'][0]["duration"]
    toll = content["result"]['routes'][0]["toll"]
    fw.write("%s, %s, %s, %s, %s \n"%(origin, target, driving_distance, driving_duration, toll))


fw.close()