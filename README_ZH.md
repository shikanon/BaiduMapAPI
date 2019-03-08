# BaiduMapAPI

Language: [English](https://github.com/shikanon/BaiduMapAPI/README.md) | [中文](https://github.com/shikanon/BaiduMapAPI/README_ZH.md)

这是一个非官方的百度地图API封装库。

This is [English Document](https://github.com/shikanon/BaiduMapAPI/README.md)

## Installation

pip 安装
```
$ pip install BaiduMapAPI
```

下载编译源码
```
$ git clone https://github.com/shikanon/BaiduMapAPI.git
$ cd BaiduMapAPI
$ pip install -r requirements.txt
$ python setup.py install
```

## Exmaple

获取全国街道的数据

```
df = pd.read_csv("http://baidumapapi.shikanon.com/data/ChUnit2017.csv", encoding="utf-8")
df["lat"] = 0.0
df["lng"] = 0.0

df["详细地址"] = df["区镇"] + df["街道"]

search = SearchPlace(AK, SK)

for i in df.index:
    print(df["详细地址"][i], df["省"][i])
    if df["城市"][i] == "市辖区":
        content = search.searchRegion(query=df["详细地址"][i], region=df["省"][i], output="json")
    else:
        content = search.searchRegion(query=df["详细地址"][i], region=df["城市"][i], output="json")
    result = json.loads(content)

    assert result["status"] == 0

    if len(result["results"]) > 0:
        df["lat"][i] = result["results"][0]["location"]["lat"]
        df["lng"][i] = result["results"][0]["location"]["lng"]
```