# -*- coding: utf-8 -*- 
import BaiduMapAPI
import requests
import time
import os

from BaiduMapAPI import checkAK
from BaiduMapAPI import common
from BaiduMapAPI.globals import HOST


class APIBase:
    '''
    The base of all the api, it provide Key Encryption Service and initialize.
    '''
    def __init__(self, ak, sk=None):
        self.ak = ak
        self.sk = sk
        if sk:
            self.encry = checkAK.URLEncryption(self.ak, self.sk)



class MapDirection(APIBase):
    '''
    Direction API, include transit, riding and driving. It only support Areas of China. If you want
    to watch other places, you can use the class of OverseasDirection.
    '''

    def _getPayload(self, origin, destination, **kwargs):
        orig = common.convertCoord(origin)
        dest = common.convertCoord(destination)
        payload = {"origin": orig, "destination": dest, 
            "ak": self.ak, "timestamp": int(time.time())}
        if kwargs:
            payload.update(kwargs)
        return payload


    def transit(self, origin, destination, **kwargs):
        '''
        origin : string, include "latitude,longitude", 
        for exmaple: guangzhou coordinate value is "23.137903,113.34348",
        destination : string, include "latitude,longitude", 
        for exmaple: guangzhou coordinate value is "23.137903,113.34348",
        site: http://lbsyun.baidu.com/index.php?title=webapi/direction-api-v2
        '''
        urlPath = "/direction/v2/transit"
        payload = self._getPayload(origin, destination, **kwargs)
        content = self.encry.get(HOST, urlPath, payload)
        print("Direction transit URL: ", self.encry.url)
        return content


    def riding(self, origin, destination, **kwargs):
        '''
        origin : string, include "latitude,longitude", 
        for exmaple: guangzhou coordinate value is "23.137903,113.34348",
        destination : string, include "latitude,longitude", 
        for exmaple: guangzhou coordinate value is "23.137903,113.34348",
        site: http://lbsyun.baidu.com/index.php?title=webapi/direction-api-v2
        '''
        urlPath = "/direction/v2/riding"
        payload = self._getPayload(origin, destination, **kwargs)
        content = self.encry.get(HOST, urlPath, payload)
        print("Direction riding URL: ", self.encry.url)
        return content
    
    
    def driving(self, origin, destination, **kwargs):
        '''
        origin : string, include "latitude,longitude", 
        for exmaple: guangzhou coordinate value is "23.137903,113.34348",
        destination : string, include "latitude,longitude", 
        for exmaple: guangzhou coordinate value is "23.137903,113.34348",
        site: http://lbsyun.baidu.com/index.php?title=webapi/direction-api-v2
        '''
        urlPath = "/direction/v2/driving"
        payload = self._getPayload(origin, destination, **kwargs)
        content = self.encry.get(HOST, urlPath, payload)
        print("Direction driving URL: ", self.encry.url)
        return content



class OverseasDirection(APIBase):
    '''
    Overseas Route Planning Services to Support the Capacity of Travel Route Planning Services in Hong Kong, 
    Macao, Taiwan and Overseas Countries/Areas of China
    '''

    def _getPayload(self, origin, destination, **kwargs):
        orig = common.convertCoord(origin)
        dest = common.convertCoord(destination)
        payload = {"origin": orig, "destination": dest, 
            "ak": self.ak, "timestamp": int(time.time())}
        if kwargs:
            payload.update(kwargs)
        return payload


    def driving(self, origin, destination, **kwargs):
        '''
        origin : string, include "latitude,longitude", 
        for exmaple: guangzhou coordinate value is "23.137903,113.34348",
        destination : string, include "latitude,longitude", 
        for exmaple: guangzhou coordinate value is "23.137903,113.34348",
        site: http://lbsyun.baidu.com/index.php?title=webapi/direction-api-abroad
        '''
        urlPath = "/direction_abroad/v1/driving"
        payload = self._getPayload(origin, destination, **kwargs)
        content = self.encry.get(HOST, urlPath, payload)
        print("OverseasDirection driving URL: ", self.encry.url)
        return content
    

    def walking(self, origin, destination, **kwargs):
        '''
        origin : string, include "latitude,longitude", 
        for exmaple: guangzhou coordinate value is "23.137903,113.34348",
        destination : string, include "latitude,longitude", 
        for exmaple: guangzhou coordinate value is "23.137903,113.34348",
        site: http://lbsyun.baidu.com/index.php?title=webapi/direction-api-abroad
        '''
        urlPath = "/direction_abroad/v1/walking"
        payload = self._getPayload(origin, destination, **kwargs)
        content = self.encry.get(HOST, urlPath, payload)
        print("OverseasDirection walking URL: ", self.encry.url)
        return content
    

    def transit(self, origin, destination, **kwargs):
        '''
        origin : string, include "latitude,longitude", 
        for exmaple: guangzhou coordinate value is "23.137903,113.34348",
        destination : string, include "latitude,longitude", 
        for exmaple: guangzhou coordinate value is "23.137903,113.34348",
        site: http://lbsyun.baidu.com/index.php?title=webapi/direction-api-abroad
        '''
        urlPath = "/direction_abroad/v1/transit"
        payload = self._getPayload(origin, destination, **kwargs)
        content = self.encry.get(HOST, urlPath, payload)
        print("OverseasDirection transit URL: ", self.encry.url)
        return content



class RouteMatrix(APIBase):
    '''
    This Class mostly provide batch processing methods. When your resources are insufficient, you can use it.
    But the result is simpler than the MapDirection API.
    The class not support access of SN encryption.
    '''

    def __init__(self, white_ak):
        self.ak = white_ak


    def _getPayload(self, origins, destinations, **kwargs):
        orig = common.convertBatchCoord(origins, sep="|")
        dest = common.convertBatchCoord(destinations, sep="|")
        payload = {"origins": orig, "destinations": dest, "ak": self.ak}
        if kwargs:
            payload.update(kwargs)
        return payload
    

    def driving(self, origins, destinations, **kwargs):
        '''
        origin : string, include "latitude,longitude|latitude,longitude|latitude,longitude", 
        for exmaple: guangzhou coordinate value is "23.137903,113.34348|40.063597,116.364973",
        destination : string, include "latitude,longitude|latitude,longitude|latitude,longitude", 
        for exmaple: guangzhou coordinate value is "23.137903,113.34348|40.063597,116.364973",
        site: http://lbsyun.baidu.com/index.php?title=webapi/route-matrix-api-v2
        '''
        urlPath = "/routematrix/v2/driving"
        payload = self._getPayload(origins, destinations, **kwargs)
        r = requests.get(HOST + urlPath, params=payload)
        print("routematrix driving URL: ", r.url)
        return r.content


    def riding(self, origins, destinations, **kwargs):
        '''
        origin : string, include "latitude,longitude|latitude,longitude|latitude,longitude", 
        for exmaple: guangzhou coordinate value is "23.137903,113.34348|40.063597,116.364973",
        destination : string, include "latitude,longitude|latitude,longitude|latitude,longitude", 
        for exmaple: guangzhou coordinate value is "23.137903,113.34348|40.063597,116.364973",
        site: http://lbsyun.baidu.com/index.php?title=webapi/route-matrix-api-v2
        '''
        urlPath = "/routematrix/v2/riding"
        payload = self._getPayload(origins, destinations, **kwargs)
        r = requests.get(HOST + urlPath, params=payload)
        print("routematrix riding URL: ", r.url)
        return r.content


    def walking(self, origins, destinations, **kwargs):
        '''
        origin : string, include "latitude,longitude|latitude,longitude|latitude,longitude", 
        for exmaple: guangzhou coordinate value is "23.137903,113.34348|40.063597,116.364973",
        destination : string, include "latitude,longitude|latitude,longitude|latitude,longitude", 
        for exmaple: guangzhou coordinate value is "23.137903,113.34348|40.063597,116.364973",
        site: http://lbsyun.baidu.com/index.php?title=webapi/route-matrix-api-v2
        '''
        urlPath = "/routematrix/v2/walking"
        payload = self._getPayload(origins, destinations, **kwargs)
        r = requests.get(HOST + urlPath, params=payload)
        print("routematrix walking URL: ", r.url)
        return r.content



class SearchPlace(APIBase):
    '''
    This Class mostly provide the search of POI, include city search, circular area search, 
    rectangular area search. The result contains detailed geographic information.
    '''

    def __init__(self, ak, sk):
        # get the module path, and can easy find the data  directory
        datapath = os.path.split(BaiduMapAPI.__file__)[0] + "/data/BaiduMap_cityCode_1102.txt"
        with open(datapath, "r", encoding="utf-8") as fr:
            self._allregion = fr.read()
        APIBase.__init__(self, ak, sk)


    def _getPayload(self, query, **kwargs):
        payload = {"query": query, "ak": self.ak, "timestamp": int(time.time())}
        if kwargs:
            payload.update(kwargs)
        return payload
    
    def listAllRegion(self):
        return self._allregion


    def searchRegion(self, query, region, **kwargs):
        '''
        query : string, for exmaple: "银行",
        region : string, is city name or city code. If you want to know the
        all places, you can use listAllRegion to list them. 
        site: http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-placeapi
        '''
        urlPath = "/place/v2/search"
        if "$" in  query:
            raise ValueError("Search Region API cann't support multi key query!")
        payload = self._getPayload(query, **kwargs)
        if region not in self._allregion:
            print("region 输入有误不对%s"%region)
        payload["region"] = region
        content = self.encry.get(HOST, urlPath, payload)
        print("search region URL: ", self.encry.url)
        return content
    

    def fuzzySearchRegion(self, query, region, city_limit="true", **kwargs):
        '''
        query : string, for exmaple: "银行",
        region : string, is city name or city code. If you want to know the
        all places, you can use listAllRegion to list them. 
        site: http://lbsyun.baidu.com/index.php?title=webapi/place-suggestion-api
        '''
        urlPath = "/place/v2/suggestion"
        if "$" in  query:
            raise ValueError("Search Region API cann't support multi key query!")
        payload = self._getPayload(query, **kwargs)
        if region not in self._allregion:
            raise ValueError("region 输入不对")
        payload["region"] = region
        payload["city_limit"] = city_limit
        content = self.encry.get(HOST, urlPath, payload)
        print("fuzzy search region URL: ", self.encry.url)
        return content
    

    def searchCircularArea(self, query, location, **kwargs):
        '''
        query : string, separate with `$` , for exmaple: "银行$酒店",
        location : string, include "latitude,longitude", 
        for exmaple: guangzhou coordinate value is "23.137903,113.34348",
        site: http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-placeapi
        '''
        urlPath = "/place/v2/search"
        payload = self._getPayload(query, **kwargs)
        location = common.convertCoord(location)
        payload["location"] = location
        content = self.encry.get(HOST, urlPath, payload)
        print("search circular area URL: ", self.encry.url)
        return content


    def searchRectangularArea(self, query, bounds, **kwargs):
        '''
        query : string, separate with `$` , for exmaple: "银行$酒店",
        bounds : string, include "min(latitude),min(longitude),max(latitude),max(longitude)", 
        for exmaple: "23.137903,113.34348,40.063597,116.364973",
        site: http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-placeapi
        '''
        urlPath = "/place/v2/search"
        payload = self._getPayload(query, **kwargs)
        payload["bounds"] = bounds
        content = self.encry.get(HOST, urlPath, payload)
        print("search rectangular area URL: ", self.encry.url)
        return content



class Geocoder(APIBase):
    '''
    This API Provides geocoding and geocoding. You can use it to find the geographic 
    coordinates of POIs, or to check which POIs are located at this location by 
    geographic coordinates.
    '''

    def geoEncode(self, address, latest_admin_data=1, **kwargs):
        '''
        address : string, for exmaple: "北京市海淀区上地十街10号",
        latest_admin : int, Whether this parameter can access the latest data, 1 means use lastest 
        administrative area data, 0 will not.
        site: http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding
        '''
        urlPath = "/geocoder/v2/"
        payload = {"address": address, "latest_admin": latest_admin_data, 
                    "ak": self.ak, "timestamp": int(time.time())}
        if kwargs:
            payload.update(kwargs)
        content = self.encry.get(HOST, urlPath, payload)
        print("geo-encode URL: ", self.encry.url)
        return content

    def geoDecode(self, location, latest_admin_data=1, **kwargs):
        '''
        location : string or tuple, for exmaple: "38.76623,116.43213",
        latest_admin : int, Whether this parameter can access the latest data, 1 means use lastest 
        administrative area data, 0 will not.
        site: http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding
        '''
        urlPath = "/geocoder/v2/"
        location = common.convertCoord(location)
        payload = {"location": location, "latest_admin": latest_admin_data,
                    "ak": self.ak, "timestamp": int(time.time())}
        if kwargs:
            payload.update(kwargs)
        content = self.encry.get(HOST, urlPath, payload)
        print("geo-decode URL: ", self.encry.url)
        return content



class CoordTrans(APIBase):
    '''
    Direction API, include transit, riding and driving. It only support Areas of China. If you want
    to watch other places, you can use the class of OverseasDirection.
    '''

    def _getPayload(self, coords, **kwargs):
        coords = common.convertBatchCoord(coords, sep=";")
        payload = {"coords": coords, "ak": self.ak, "timestamp": int(time.time())}
        if kwargs:
            payload.update(kwargs)
        return payload
    
    def transform(self, coords, origin, target, **kwargs):
        '''
        coords : string, include "latitude,longitude;latitude,longitude;latitude,longitude", 
        for exmaple:  "23.137903,113.34348;40.063597,116.364973",
        origin : int, include 1: WGS84; 2: sougou map; 3: google map; 4: metric coordinates of google map;
        5: baidu map; 6: metric coordinates of baidu map; 7: mapbar; 8: 51 map , 
        target : int, include 3: GCJ02; 4:  metric coordinates of GCJ02; 5: bd09ll; 6: bd09mc
        site: http://lbsyun.baidu.com/index.php?title=webapi/guide/changeposition
        '''
        urlPath = "/geoconv/v1/"
        payload = self._getPayload(coords, **kwargs)
        payload["from"] = origin
        payload["to"] = target
        content = self.encry.get(HOST, urlPath, payload)
        print("coordinate transform URL: ", self.encry.url)
        return content



class TrafficQuery(APIBase):
    '''
    It provides real-time traffic query.
    '''

    def query(self, road_name, city, nolog=False):
        '''
        query the road condition with read-time.
        road_name: string, for example "北五环", "信息路"
        '''
        urlPath = "/traffic/v1/road"
        payload = {"road_name": road_name, "city": city, "ak": self.ak, "timestamp": int(time.time())}
        content = self.encry.get(HOST, urlPath, payload)
        if not nolog:
            print("coordinate transform URL: ", self.encry.url)
        return content
