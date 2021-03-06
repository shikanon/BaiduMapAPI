# -*- coding: utf-8 -*- 

import json
import pytest

from constant import AK, SK, AK_whitelist
from BaiduMapAPI.api import MapDirection, RouteMatrix, SearchPlace, Geocoder, CoordTrans
from BaiduMapAPI.base import POI

def test_MapDirection_Transit():
    direction = MapDirection(AK, SK)
    origin = "23.137903,113.34348"
    destination = "22.544383,114.062203"
    coord_type = "wgs84"
    # 测试交通工具
    content = direction._get_raw_transit(origin, destination, coord_type=coord_type)
    result = json.loads(content)
    assert result["status"] == 0
    TransitObject = direction.transit(origin, destination, coord_type=coord_type)
    print(TransitObject)
    assert len(TransitObject.to_dataframe().columns) == 13

def test_MapDirection_Driving():
    direction = MapDirection(AK, SK)
    origin = "23.137903,113.34348"
    destination = "22.544383,114.062203"
    coord_type = "wgs84"
    # 测试自驾出行
    content = direction._get_raw_driving(origin, destination, coord_type=coord_type)
    result = json.loads(content)
    assert result["status"] == 0
    DriveObject = direction.driving(origin, destination, coord_type=coord_type)
    print(DriveObject)
    assert len(DriveObject.to_dataframe().columns) == 8


def test_MapDirection_Riding():
    direction = MapDirection(AK, SK)
    origin = "23.137903,113.34348"
    destination = "23.344383,113.362203"
    coord_type = "wgs84"
    # 测试骑行
    content = direction._get_raw_riding(origin, destination, coord_type=coord_type)
    result = json.loads(content)
    assert result["status"] == 0
    TransitObject = direction.riding(origin, destination, coord_type=coord_type)
    print(TransitObject)
    assert len(TransitObject.to_dataframe().columns) == 13


def test_RouteMatrix():
    routematrix = RouteMatrix(AK_whitelist)
    origins = "23.137903,113.34348|22.937903,113.34348|23.237903,113.34348"
    destinations = "23.544383,113.062203|23.944383,113.062203|23.244383,113.262203"
    tactics = "12"
    content = routematrix.driving(origins, destinations, tactics=tactics)
    result = json.loads(content)
    assert result["status"] == 0

    content = routematrix.riding(origins, destinations, tactics=tactics)
    result = json.loads(content)
    assert result["status"] == 0

    content = routematrix.walking(origins, destinations, tactics=tactics)
    result = json.loads(content)
    assert result["status"] == 0


def test_SearchPlace():
    search = SearchPlace(AK, SK)
    allregion = search.listAllRegion()
    assert "北京" in allregion and "广州" in allregion

    query = "银行"
    region = "338" # 肇庆
    content = search.searchRegion(query=query, region=region, output="json")
    result = json.loads(content)
    assert result["status"] == 0

    content = search.fuzzySearchRegion(query="北京路", region="广州", city_limit="false",output="json")
    result = json.loads(content)
    assert result["status"] == 0
    
    poi = "银行$酒店"
    location = "23.137903,113.34348"
    content = search.searchCircularArea(query=poi, location=location, output="json")
    result = json.loads(content)
    assert result["status"] == 0

    bounds = "23.137903,113.34348,40.063597,116.364973"
    content = search.searchRectangularArea(query=poi, bounds=bounds, output="json")
    result = json.loads(content)
    assert result["status"] == 0

    # 测试批量百度坐标查询
    places = {
        "香港":"香港国际机场", "广州": "广州白云国际机场", 
        "深圳":"深圳宝安国际机场", "珠海":"珠海金湾国际机场",
        "澳门":"澳门国际机场", "佛山":"佛山沙堤机场", 
        "惠州":"惠州平潭机场"
    }
    result = search.queryBatchPlaceCoord(places)
    result = list(result)
    assert len(result) == 7
    assert len(result[0]) == 2

    # 测试 search 方法
    pois = search.search(query, region=region)
    for p in pois:
        assert isinstance(p, POI)


def test_Geocoder():
    geocoder = Geocoder(AK, SK)
    address = "广州市天河区中山大道"
    content = geocoder.geoEncode(address=address, pois=1, output="json")
    result = json.loads(content)
    assert result["status"] == 0

    location = "23.137903,113.34348"
    content = geocoder.geoDecode(location=location, output="json")
    result = json.loads(content)
    assert result["status"] == 0


def test_CoordTrans():
    trans = CoordTrans(AK, SK)
    coords = "23.137903,113.34348;40.063597,116.364973"
    origin = 1
    target = 5
    content = trans.transform(coords, origin, target)
    result = json.loads(content)
    assert result["status"] == 0