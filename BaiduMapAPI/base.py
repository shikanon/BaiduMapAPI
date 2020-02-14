# -*- coding: utf-8 -*- 
import pandas as pd
import json

from collections import defaultdict
from BaiduMapAPI import common

vehicle_info = {
    1: "火车", 2: "飞机", 3: "公交",
    4: "驾车", 5: "步行", 6: "大巴"
}

pulic_vechicle_info = {
    0: "普通日行公交车",
    1: "城市轨道交通",
    2: "机场巴士",
    3: "有轨电车",
    4: "机场巴士",
    5: "旅游线路车",
    6: "普通公交车(夜班车)",
    7: "机场巴士",
    8: "轮渡",
    9: "其他",
    10: "快车",
    11: "慢车",
    12: "机场轨道交通",
    13: "机场轨道交通",
    14: "机场轨道交通",
}

road_type_info = {
    0: "高速路",
    1: "城市高速路",
    2: "国道",
    3: "省道",
    4: "县道",
    5: "乡镇村道",
    6: "其他道路",
    7: "九级路",
    8: "轮渡航线",
    9: "行人道路",
}

# 数据解析装饰器
def parse_object(Object):
    def get_data(func):
        def check_and_parse_data(*args, **kwargs):
            obj = Object()
            content = func(*args, **kwargs)
            common.check_response(content)
            obj.parse(content)
            return obj
        return check_and_parse_data
    return get_data

        


class TransitLineObject(object):
    '''
    lines object
    '''
    def __init__(self):
        self.distance = 0 # 距离
        self.time = 0 # 时间
        self.price = 0 # 价格
        self.line_desc = "" # 描述
        self.main_vehicle = "" # 交通方式 
        self.vehicle_name = "" # 名称
    
    def __str__(self):
        obj_string = "<LineObject distance: %d, time: %d, price: %d, main_vehicle: %s>"%(
            self.distance, self.time, self.price, self.main_vehicle)
    
    def parse(self, data:dict):
        '''
        parse the line/setp data to object.
        '''
        if type(data) != dict:
            raise ValueError(data)
        if "distance" in data:
            self.distance = data["distance"]
        if "duration" in data:
            self.time = data["duration"]
        if "price" in data:
            self.price = data["price"]
        if "instructions" in data:
            self.line_desc = data["instructions"]
        if "vehicle_info" in data:
            vehicle_type = data["vehicle_info"]["type"]
            if vehicle_type == 3 and "detail" in data["vehicle_info"]:
                    self.main_vehicle = pulic_vechicle_info[data["vehicle_info"]["detail"]["type"]]
            else:
                self.main_vehicle = vehicle_info[vehicle_type]
            if "detail" in data["vehicle_info"]:
                if data["vehicle_info"]["detail"] is not None:
                    self.vehicle_name = data["vehicle_info"]["detail"]["name"]



class TransitObject(object):
    '''
    Almost all modes of transportation except self-driving and cycling. 
    It include trains, planes, buses, driving, walking, buses etc.
    '''
    def __init__(self):
        self.total_line = 0 # 总共线路数
        self.routes = [] # RouteObject对象
    
    def __str__(self):
        return str(self.to_dataframe().head())

    def _check_data(self, data):
        '''
        check input parameters function. 
        校验数据
        '''
        if isinstance(data, dict):
            parsed_data = data
        elif isinstance(data, str) or isinstance(data, bytes):
            try:
                parsed_data = json.loads(data)
            except:
                raise ValueError("传入参数不对, 传入参数必须为json文本格式")
        else:
            raise ValueError("传入参数不对, 传入参数必须为json文本格式")
        if "status" in parsed_data and "result" in parsed_data:
            if parsed_data["status"] == 0:
                return parsed_data["result"]
        else:
            raise ValueError("传入数据中status 或者 result 值不对")

    def to_dict(self):
        '''将TransitObject转换成一个dict类型
        '''
        result = list()
        n = 1
        for r in self.routes:
            data = {
                "fid": n,
                "origin_city_id": self.origin_city_id,
                "origin_city_name": self.origin_city_name,
                "origin_location": self.origin_location,
                "destination_city_id": self.destination_city_id,
                "destination_city_name": self.destination_city_name,
                "destination_location": self.destination_location,
                "distance": r["distance"],
                "duration": r["duration"],
                "price": r["price"],
                "main_vehicle": r["main_vehicle"],
                "vehicle_list": r["vehicle_list"],
                "description": r["description"]
            }
            result.append(data)
        return result

    def to_dataframe(self):
        '''
        将TransitObject转换成一个pandas.DataFrame类型
        '''
        data = defaultdict(list)
        n = 1
        for r in self.routes:
            data["fid"].append(n)
            data["origin_city_id"].append(self.origin_city_id)
            data["origin_city_name"].append(self.origin_city_name)
            data["origin_location"].append(self.origin_location)
            data["destination_city_id"].append(self.destination_city_id)
            data["destination_city_name"].append(self.destination_city_name)
            data["destination_location"].append(self.destination_location)
            data["distance"].append(r["distance"])
            data["duration"].append(r["duration"])
            data["price"].append(r["price"])
            data["main_vehicle"].append(r["main_vehicle"])
            data["vehicle_list"].append(r["vehicle_list"])
            data["description"].append(r["description"])
        return pd.DataFrame(data)


    def parse(self, content):
        '''
        load the data and parse it.
        '''
        data = self._check_data(content)
        self.total_line = data["total"]
        if "routes" not in data:
            return None
        for r in data["routes"]:
            lines = self._route_parse(r)
            self.routes.append(lines)
        # 出发地
        self.origin_city_id = data["origin"]["city_id"]
        self.origin_city_name = data["origin"]["city_name"]
        self.origin_location = (data["origin"]["location"]["lng"], data["origin"]["location"]["lat"])
        # 目的地
        self.destination_city_id = data["destination"]["city_id"]
        self.destination_city_name = data["destination"]["city_name"]
        self.destination_location = (data["destination"]["location"]["lng"], data["origin"]["location"]["lat"])
    
    def _route_parse(self, data):
        if type(data) != dict:
            raise ValueError(data)
        if "steps" not in data:
            return None
        lines = [] # 线路
        result = {
            "distance":     0, # 总距离
            "duration":     0, # 总时间
            "price":        0, # 总价格
            "vehicle":      "步行", # 交通方式
            "vehicle_list": "", # 交通工具列表
            "description":  "" # 描述
        }
        result["distance"] = data["distance"]
        result["duration"] = data["duration"]
        result["price"] = data["price"]
        
        main_vehicle = dict()
        for steps in data["steps"]:
            for step in steps:
                line = TransitLineObject()
                line.parse(step)

                if line.main_vehicle in main_vehicle:
                    main_vehicle[line.main_vehicle] += line.distance
                else:
                    main_vehicle[line.main_vehicle] = line.time
                if result["description"]:
                    result["description"] = result["description"] + "; " + line.line_desc
                else:
                    result["description"] = line.line_desc
                lines.append(line)

                if line.vehicle_name != "":
                    result["vehicle_list"] = result["vehicle_list"] + "; " + line.vehicle_name
                else:
                    result["vehicle_list"] = line.vehicle_name
        # Calculate the main modes of transportation, 
        # and take the longest distance as the main mode of transportation.
        sorted_vehicles = sorted(main_vehicle.items(),key=lambda x:x[1],reverse=True)
        # print(sorted_vehicles)
        result["main_vehicle"] = sorted_vehicles[0][0]
        return result



class DriveObject(object):
    '''
    自驾出行路线对象
    '''
    def __init__(self):
            self.total_line = 0 # 总共线路数
            self.routes = [] # RouteObject对象
    
    def __str__(self):
        return str(self.to_dataframe().head())

    def _check_data(self, data):
        '''
        check input parameters function. 
        校验数据
        '''
        if isinstance(data, dict):
            parsed_data = data
        elif isinstance(data, str) or isinstance(data, bytes):
            try:
                parsed_data = json.loads(data)
            except:
                raise ValueError("传入参数不对, 传入参数必须为json文本格式")
        else:
            raise ValueError("传入参数不对, 传入参数必须为json文本格式")
        if "status" in parsed_data and "result" in parsed_data:
            if parsed_data["status"] == 0:
                return parsed_data["result"]
        else:
            raise ValueError("传入数据中status 或者 result 值不对")

    def to_dict(self):
        '''将DriveObject转换成一个dict类型
        '''
        result = list()
        n = 1
        for r in self.routes:
            data = {
                "fid": n,
                "origin_location": self.origin_location,
                "destination_location": self.destination_location,
                "distance": r["distance"],
                "duration": r["duration"],
                "price": r["price"],
                "path": r["path"],
                "description": r["description"]
            }
            result.append(data)
        return result

    def to_dataframe(self):
        '''
        将DriveObject转换成一个pandas.DataFrame类型
        '''
        data = defaultdict(list)
        n = 1
        for r in self.routes:
            data["fid"].append(n)
            data["origin_location"].append(self.origin_location)
            data["destination_location"].append(self.destination_location)
            data["distance"].append(r["distance"])
            data["duration"].append(r["duration"])
            data["price"].append(r["price"])
            data["path"].append(r["path"])
            data["description"].append(r["description"])
        return pd.DataFrame(data)

    def parse(self, content):
        '''
        load the data and parse it.
        '''
        data = self._check_data(content)
        self.total_line = data["total"]
        if "routes" not in data:
            return None
        for r in data["routes"]:
            lines = self._route_parse(r)
            self.routes.append(lines)
        # 地址
        place = data["routes"][0]
        # 出发地
        self.origin_location = (place["origin"]["lng"], place["origin"]["lat"])
        # 目的地
        self.destination_location = (place["destination"]["lng"], place["origin"]["lat"])
    
    def _route_parse(self, data):
        if type(data) != dict:
            raise ValueError(data)
        if "steps" not in data:
            return None
        lines = [] # 线路
        result = {
            "distance":     0, # 总距离
            "duration":     0, # 总时间
            "price":        0, # 总价格
            "path":      "", # 地理坐标
            "description":  "" # 路线名称描述
        }
        result["distance"] = data["distance"]
        result["duration"] = data["duration"]
        result["price"] = data["taxi_fee"] + data["toll"]
        
        main_vehicle = dict()
        for steps in data["steps"]:
            description = "%s(%s)"%(steps["road_name"],road_type_info[steps["road_type"]])
            if result["description"]:
                result["description"] = result["description"] + "; " + description
            else:
                result["description"] = description

            if result["path"]:
                result["path"] = result["path"] + ";" + steps["path"]
            else:
                result["path"] = steps["path"]
        return result



class POI(object):
    '''
    Point of Interest, it can be a house, a shop, a mailbox, a bus stop, etc.
    '''
    def __init__(self, uid, name, address, province, 
                city, area, lat, lng):
        self.uid = uid
        self.name = name
        self.address = address
        self.province = province
        self.city = city
        self.area = area
        self.lat = lat
        self.lng = lng
    
    def __str__(self):
        return "<POI uid: %s, name: %s>"%(str(self.uid), self.name)
    
    def get_location(self):
        return self.lat,self.lng
        