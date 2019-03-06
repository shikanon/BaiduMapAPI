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
df = pd.read_csv("http://baidumapapi.shikanon.com/data/ChUnit2017.csv", encoding="utf-8")
df["lat"] = 0.0
df["lng"] = 0.0

df["全称"] = df["省"] + df["城市"] + df["区镇"] + df["街道"]

search = SearchPlace(AK, SK)

for i in df.index:
    print(df["全称"][i], df["省"][i])
    if df["城市"][i] == "市辖区":
        content = search.searchRegion(query=df["全称"][i], region=df["省"][i], output="json")
    else:
        content = search.searchRegion(query=df["全称"][i], region=df["城市"][i], output="json")
    result = json.loads(content)

    assert result["status"] == 0

    if len(result["results"]) > 0:
        df["lat"][i] = result["results"][0]["location"]["lat"]
        df["lng"][i] = result["results"][0]["location"]["lng"]

df.to_csv("街道的位置坐标.csv", encoding="utf-8", index=False)