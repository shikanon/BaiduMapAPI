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

dirction = MapDirection(AK, SK)

fw = open("transit_buses_result.csv", "w", encoding="utf-8")
fw.write("origin\t target\t distance\t duration\t price\t vehicle\t description \n")

for name in targets_name:
    pois = place.search(targets_name[name], region=name)
    poi = pois[0]

    loc = poi.get_location()

    for i in origins_data.index:
        obj = TransitObject()
        coords = (round(origins_data["lat"][i],5),round(origins_data["lng"][i],5))
        # 巴士
        content = dirction.transit(loc, coords, tactics_incity=0, trans_type_intercity=2)
        content = json.loads(content)
        if "status" in content and content["status"] == 0:
            obj.parse(content)
            origin = origins_data["详细地址"][i]
            target = targets_name[name]
            result = str(origin) + "\t" +str(target) 
            if len(obj.routes)==0:
                break
            route = obj.routes[0]
            route = route.to_dict()
            result = result + "\t" + "\t".join(str(r) for r in route.values()) + "\n"
            print(result)
            fw.write(result)


fw.close()