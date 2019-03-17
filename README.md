# BaiduMapAPI

Language: [English](https://github.com/shikanon/BaiduMapAPI/blob/master/README.md) | [中文](https://github.com/shikanon/BaiduMapAPI/blob/master/README_ZH.md)

A Simple Python Baidu Map API Library, make easy for you when you want to use map data.

It is Python Baidu Map API Library. We encapsulate it, and make it more easy for you.

This is [document](http://baidumapapi.shikanon.com/doc/)

## Installation

You can install it via pip
```
$ pip install BaiduMapAPI
```
or clone it and install it
```
$ git clone https://github.com/shikanon/BaiduMapAPI.git
$ cd BaiduMapAPI
$ pip install -r requirements.txt
$ python setup.py install
```

## Exmaple

Query the transit info

```
direction = MapDirection(AK, SK)
origin = "23.137903,113.34348"
destination = "22.544383,114.062203"
coord_type = "wgs84"
content = direction.transit(origin, destination, coord_type=coord_type)
result = json.loads(content)
print(result)
```


This exmaple of getting all street of china.

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