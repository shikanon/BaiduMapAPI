#coding:utf-8
import json
import records

from util import recovsys, logsys
from BaiduMapAPI.api import SearchPlace, MapDirection
from BaiduMapAPI.base import TransitObject


logger = logsys("baidumap",level=10).getlogger()


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
            steps_distance TEXT,
            steps_duration TEXT,
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
            duration, price, main_vehicle, vehicle_list, description,
            steps_distance, steps_duration
        )
        values (
            :transit_type, :fid, :origin_city_id, :origin_city_name, :origin_location_lat,
            :origin_location_lng, :destination_city_id, :destination_city_name, 
            :destination_location_lat, :destination_location_lng, :distance,
            :duration, :price, :main_vehicle, :vehicle_list, :description,
            :steps_distance, :steps_duration
        )
        '''
        self.record_db.bulk_query(insert_sql, *records)

class BaiduMap:
    def __init__(self, ak, sk):
        self.origin = list()
        self.destination = list()
        self.place = SearchPlace(ak, sk)
        self.dirction = MapDirection(ak, sk)
        self.recov = recovsys()
        
    
    def load_data(self, origin, destination):
        self.origin.append(origin)
        self.destination.append(destination)

    def get_train_data(self):
        self.recov.clean()
        # 火车优先
        for o_loc in self.origin:
            for d_loc in self.destination:
                result = list()
                try:
                    data = self.dirction.transit(o_loc, d_loc, tactics_intercity=0, trans_type_intercity=0, coord_type="wgs84")
                    data = data.to_dict()
                    for d in data:
                        d["transit_type"] = "火车"
                        d["origin_location_lat"] = d["origin_location"][0]
                        d["origin_location_lng"] = d["origin_location"][1]
                        d["destination_location_lat"] =d["destination_location"][0]
                        d["destination_location_lng"] = d["origin_location"][1]
                        result.append(d)
                    logger.info("完成{}到{}的数据写入".format(o_loc, d_loc))
                except Exception as e:
                    back_data = {
                        "origin": o_loc,
                        "destination": d_loc
                    }
                    self.recov.backup(back_data)
                    logger.error("起始地: %s, 目的地: %s"%(o_loc, d_loc))
                yield result

    def get_plane_data(self):
        self.recov.clean()
        # 飞机优先
        for o_loc in self.origin:
            for d_loc in self.destination:
                result = list()
                try:
                    data = self.dirction.transit(o_loc, d_loc, tactics_intercity=0, trans_type_intercity=1, coord_type="wgs84")
                    data = data.to_dict()
                    for d in data:
                        d["transit_type"] = "飞机"
                        d["origin_location_lat"] = d["origin_location"][0]
                        d["origin_location_lng"] = d["origin_location"][1]
                        d["destination_location_lat"] =d["destination_location"][0]
                        d["destination_location_lng"] = d["origin_location"][1]
                        result.append(d)
                    logger.info("完成{}到{}的数据写入".format(o_loc, d_loc))
                except Exception:
                    back_data = {
                        "origin": o_loc,
                        "destination": d_loc
                    }
                    self.recov.backup(back_data)
                    logger.error("起始地: %s, 目的地: %s"%(o_loc,d_loc))
                yield result

    def get_bus_data(self, departure=None):
        self.recov.clean()
        # 巴士
        for o_loc in self.origin:
            for d_loc in self.destination:
                result = list()
                try:
                    data = self.dirction.transit(o_loc, d_loc, tactics_intercity=0, trans_type_intercity=2, coord_type="wgs84")
                    data = data.to_dict()
                    for d in data:
                        d["transit_type"] = "大巴"
                        d["origin_location_lat"] = d["origin_location"][0]
                        d["origin_location_lng"] = d["origin_location"][1]
                        d["destination_location_lat"] =d["destination_location"][0]
                        d["destination_location_lng"] = d["origin_location"][1]
                        result.append(d)
                    logger.info("完成{}到{}的数据写入".format(o_loc, d_loc))
                except Exception:
                    back_data = {
                        "origin": o_loc,
                        "destination": d_loc
                    }
                    self.recov.backup(back_data)
                    logger.error("起始地: %s, 目的地: %s"%(o_loc,d_loc))
                yield result
