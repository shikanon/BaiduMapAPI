# -*- coding: utf-8 -*- 

'''
这是一个计算origins到targets的自驾行车OD矩阵的exmaple，同时这里会将解析出来的数据存在本地
'''

import pandas as pd
import json
import os

from BaiduMapAPI.api import SearchPlace, MapDirection
from BaiduMapAPI.base import TransitObject


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

fw = open("transit_train_result.csv", "w", encoding="utf-8")
fw.write("origin\t target\t distance\t duration\t toll \n")

for i in origins_data.index:
    obj = TransitObject()
    coords = (origins_data["lat"][i],origins_data["lng"][i])
    # 火车
    content = dirction.transit(loc, coords, tactics_incity=4, trans_type_intercity=0)
    content = json.loads(content)
    obj.parse(content)
    origin = origins_data["详细地址"][i]
    target = targets_name[name]
    route = obj.routes[0]
    route = route.to_dict()
    result = "\t".join(str(r) for r in route.values()) + "\n"
    fw.write(result)


fw.close()