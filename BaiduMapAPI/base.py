# -*- coding: utf-8 -*- 
import pandas as pd
import json

from collections import defaultdict

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

class RouteObject(object):
    '''
    route object, a route object can have many line object.
    '''
    def __init__(self):
        self.distance = 0 # 总距离
        self.time = 0 # 总时间
        self.price = 0 # 总价格
        self.main_vehicle = "步行" # 交通方式 
        self.vehicle_name = []
        self.line_desc = "" # 描述
        self.lines = [] # 线路
    

    def parse(self, data):
        '''
        parse the route data to object.
        '''
        if "steps" not in data:
            return None
        if "distance" in data:
            self.distance = data["distance"]
        if "duration" in data:
            self.time = data["duration"]
        if "price" in data:
            self.price = data["price"]
        
        main_vehicle = dict()
        for steps in data["steps"]:
            for step in steps:
                line = LineObject()
                line.parse(step)

                if line.main_vehicle in main_vehicle:
                    main_vehicle[line.main_vehicle] += line.distance
                else:
                    main_vehicle[line.main_vehicle] = line.time
                if self.line_desc:
                    self.line_desc = self.line_desc + "; " + line.line_desc
                else:
                    self.line_desc = line.line_desc
                self.lines.append(line)

                if line.vehicle_name != "":
                    self.vehicle_name.append(line.vehicle_name)
        # Calculate the main modes of transportation, 
        # and take the longest distance as the main mode of transportation.
        sorted_vehicles = sorted(main_vehicle.items(),key=lambda x:x[1],reverse=True)
        # print(sorted_vehicles)
        self.main_vehicle = sorted_vehicles[0][0]
    

    def to_dict(self):
        result = {
            "distance":     self.distance,
            "duration":     self.time,
            "price":        self.price,
            "vehicle":      self.main_vehicle,
            "description":  self.line_desc
        }
        return result
        


class LineObject(object):
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
    
    def parse(self, data):
        '''
        parse the line/setp data to object.
        '''
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
        self.total_line = 0
        self.routes = []

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

    def parse(self, content):
        '''
        load the data and parse it.
        '''
        data = self._check_data(content)
        self.total_line = data["total"]
        if "routes" not in data:
            return None
        for r in data["routes"]:
            route = RouteObject()
            route.parse(r)
            self.routes.append(route)
        # 出发地
        self.origin_city_id = data["origin"]["city_id"]
        self.origin_city_name = data["origin"]["city_name"]
        self.origin_location = (data["origin"]["location"]["lng"], data["origin"]["location"]["lat"])
        # 目的地
        self.destination_city_id = data["destination"]["city_id"]
        self.destination_city_name = data["destination"]["city_name"]
        self.destination_location = (data["destination"]["location"]["lng"], data["origin"]["location"]["lat"])
    
    def to_dataframe(self):
        '''
        将TransitObject转换成一个pandas.DataFrame类型
        '''
        data = defaultdict(list)
        n = 1
        for r in self.routes:
            data["id"].append(n)
            data["origin_city_id"].append(self.origin_city_id)
            data["origin_city_name"].append(self.origin_city_name)
            data["origin_location"].append(self.origin_location)
            data["destination_city_id"].append(self.destination_city_id)
            data["destination_city_name"].append(self.destination_city_name)
            data["destination_location"].append(self.destination_location)
            data["distance"].append(r.distance)
            data["duration"].append(r.time)
            data["price"].append(r.price)
            data["main_vehicle"].append(r.main_vehicle)
            data["vehicle_name"].append(r.vehicle_name)
            data["description"].append(r.line_desc)
        return pd.DataFrame(data)


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
    
    def get_location(self):
        return self.lat,self.lng
        