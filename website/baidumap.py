#coding:utf-8
import json
import records
from BaiduMapAPI.api import SearchPlace, MapDirection
from BaiduMapAPI.base import TransitObject

class DataBase:
    def __init__(self, scheme):
        self.record_db = records.Database(scheme, encoding='utf-8', echo=True)
    
    def create_table(self):
        '''
        创建数据库
        '''
        create_transit_sql = '''CREATE TABLE IF NOT EXISTS transit(
            id int(4) NOT NULL AUTO_INCREMENT,
            transit_type varchar(255) NOT NULL,
            fid int(4) NOT NULL,
            origin_city_id int,
            origin_city_name varchar(255),
            origin_location_lat float,
            origin_location_lng float,
            destination_city_id int,
            destination_city_name varchar(255),
            destination_location_lat float,
            destination_location_lng float,
            distance float,
            duration float,
            price float,
            main_vehicle varchar(255),
            vehicle_list varchar(255),
            description TEXT,
            PRIMARY KEY ( `id` )
        )DEFAULT CHARSET=utf8 ;
        '''
        self.record_db.query(create_transit_sql)
    
    def reset(self):
        delete_table = '''DROP TABLE IF EXISTS transit'''
        self.record_db.query(delete_table)
        self.create_table()

    def insert_transit(self, records):
        insert_sql = '''
        insert into transit (
            transit_type, fid, origin_city_id, origin_city_name, origin_location_lat,
            origin_location_lng, destination_city_id, destination_city_name, 
            destination_location_lat, destination_location_lng, distance,
            duration, price, main_vehicle, vehicle_list, description
        )
        values (
            :transit_type, :fid, :origin_city_id, :origin_city_name, :origin_location_lat,
            :origin_location_lng, :destination_city_id, :destination_city_name, 
            :destination_location_lat, :destination_location_lng, :distance,
            :duration, :price, :main_vehicle, :vehicle_list, :description
        )
        '''
        self.record_db.bulk_query(insert_sql, *records)

class BaiduMap:
    def __init__(self, ak, sk):
        self.origin = list()
        self.destination = list()
        self.place = SearchPlace(ak, sk)
        self.dirction = MapDirection(ak, sk)
        
    
    def load_data(self, origin, destination):
        self.origin.append(origin)
        self.destination.append(destination)

    def get_train_data(self):
        # 火车优先
        for o_loc in self.origin:
            for d_loc in self.destination:
                data = self.dirction.transit(o_loc, d_loc, tactics_intercity=0, trans_type_intercity=0)
                data = data.to_dict()
                result = list()
                for d in data:
                    d["transit_type"] = "火车"
                    d["origin_location_lat"] = d["origin_location"][0]
                    d["origin_location_lng"] = d["origin_location"][1]
                    d["destination_location_lat"] =d["destination_location"][0]
                    d["destination_location_lng"] = d["origin_location"][1]
                    result.append(d)
                yield result

    def get_plane_data(self):
        # 飞机优先
        for o_loc in self.origin:
            for d_loc in self.destination:
                data = self.dirction.transit(o_loc, d_loc, tactics_intercity=0, trans_type_intercity=1)
                data = data.to_dict()
                result = list()
                for d in data:
                    d["transit_type"] = "飞机"
                    d["origin_location_lat"] = d["origin_location"][0]
                    d["origin_location_lng"] = d["origin_location"][1]
                    d["destination_location_lat"] =d["destination_location"][0]
                    d["destination_location_lng"] = d["origin_location"][1]
                    result.append(d)
                yield result

    def get_bus_data(self, departure=None):
        # 巴士
        for o_loc in self.origin:
            for d_loc in self.destination:
                data = self.dirction.transit(o_loc, d_loc, tactics_intercity=0, trans_type_intercity=2)
                data = data.to_dict()
                result = list()
                for d in data:
                    d["transit_type"] = "大巴"
                    d["origin_location_lat"] = d["origin_location"][0]
                    d["origin_location_lng"] = d["origin_location"][1]
                    d["destination_location_lat"] =d["destination_location"][0]
                    d["destination_location_lng"] = d["origin_location"][1]
                    result.append(d)
                yield result
