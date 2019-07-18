# -*- coding: utf-8 -*- 

import pandas as pd
import time
import json
import os
from collections import defaultdict

from BaiduMapAPI.api import MapDirection
from BaiduMapAPI.base import TransitObject

# 加载密钥
AK = os.environ["BaiduAK"]
SK = os.environ["BaiduSK"]

# 加载数据
data_path = "data/A级景点坐标.xls"
save_file = "自行车OD矩阵结果文件.xls"
origins_df = pd.read_excel(data_path, encoding="utf-8")
target_df = pd.read_excel(data_path, encoding="utf-8")

# 数据
result = defaultdict(list)

# 只存其中的一条线路
dirction = MapDirection(AK, SK)

try:
    for i in origins_df.index:
        for j in target_df.index:
            if i > j:
                print(i, j)
                # name
                origin_name = origins_df["NAME"][i]
                target_name = target_df["NAME"][j]
                print(origin_name, target_name)
                # "23.137903,113.34348"
                origins_coords = (round(origins_df["Y"][i],5),round(origins_df["X"][i],5))
                target_coords = (round(target_df["Y"][j],5),round(target_df["X"][j],5))
                content = dirction.driving(origins_coords, target_coords)
                content = json.loads(content)
                assert content["message"] == "成功"

                if len(content["result"]["routes"]) > 0:
                    tag = content["result"]["routes"][0]["tag"]
                    distance = content["result"]["routes"][0]["distance"]
                    duration = content["result"]["routes"][0]["duration"]
                    step_path = " ;".join(str(step["path"]) for step in content["result"]["routes"][0]["steps"] if "path" in step)
                    step_distance = " ;".join(str(step["distance"]) for step in content["result"]["routes"][0]["steps"] if "distance" in step)
                    step_road_type = " ;".join(str(step["road_type"]) for step in content["result"]["routes"][0]["steps"] if "road_type" in step)
                    step_road_name = " ;".join(str(step["road_name"]) for step in content["result"]["routes"][0]["steps"] if "road_name" in step)
                # 数据结构
                result["origin_name"].append(origin_name)
                result["target_name"].append(target_name)
                result["origins_lat"].append(origins_df["Y"][i])
                result["origins_long"].append(origins_df["X"][i])
                result["target_lat"].append(target_df["Y"][i])
                result["target_long"].append(target_df["X"][i])
                result["tag"].append(tag)
                result["distance"].append(distance)
                result["duration"].append(duration)
                result["step_path"].append(step_path)
                result["step_distance"].append(step_distance)
                result["step_road_type"].append(step_road_type)
                result["step_road_name"].append(step_road_name)
                time.sleep(1)
except:
    print("程度中断退出")
    print("程序现在跑到第%d,%d个"%(i,j))
    with open("log.txt", "w") as fw:
        fw.write("%d,%d"%(i,j))

result = pd.DataFrame(result)
result.to_excel(save_file)
