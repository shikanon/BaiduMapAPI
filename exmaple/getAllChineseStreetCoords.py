# -*- coding: utf-8 -*- 
import os
import json
import pandas as pd

from BaiduMapAPI.api import SearchPlace

'''
这个例子是通过 SearchPlace API 查找全国各街道办的位置坐标
'''

# constant
AK = os.environ["BaiduAK"]
SK = os.environ["BaiduSK"]

# get street name
df = pd.read_csv("exmaple_citydata.csv", encoding="utf-8")
df["lat"] = 0.0
df["lng"] = 0.0

df["三级区县"] = df["三级区县"].fillna("")

df["详细地址"] = df["三级区县"] + df["四级镇街"]

search = SearchPlace(AK, SK)

for i in df.index:
    print(df["详细地址"][i], df["二级市"][i])
    content = search.searchRegion(query=df["详细地址"][i], region=df["二级市"][i], output="json")
    result = json.loads(content)

    assert result["status"] == 0

    if len(result["results"]) > 0:
        df["lat"][i] = result["results"][0]["location"]["lat"]
        df["lng"][i] = result["results"][0]["location"]["lng"]

df.to_csv("exmaple_citydata_coords.csv", encoding="utf-8", index=False)