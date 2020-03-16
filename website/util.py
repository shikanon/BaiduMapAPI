# coding=utf-8
'''
# Author: shikanon (shikanon@tensorbytes.com)
# File Created Time: 2020-02-22 6:44:22
# 
# Project: website
# File: util.py
# Description: 
# 
'''
import os
import datetime
import logging
import json
import pandas as pd

COLORS = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,
}

def read_data(path):
    if ".csv" in path[-4:]:
        data = pd.read_csv(path)
    elif ".xls" in path[-4:] or ".xlsx" in path[:-5]:
        data = pd.read_excel(path)
    else:
        raise ValueError("file format error, you must try .xls or .csv, but input is %s"%path)
    return data


class ColorFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%'):
        logging.Formatter.__init__(self, fmt, datefmt, style)

    def format(self, record):
        levelname = record.levelname
        if levelname == "INFO":
            record.levelname = "\033[1;%dm"%COLORS["green"] + record.levelname + "\033[0m"
            record.message = "\033[1;%dm"%COLORS["green"] + record.message + "\033[0m"
        elif levelname in ["CRITICAL", "ERROR"]:
            record.levelname = "\033[1;%dm"%COLORS["red"] + record.levelname + "\033[0m"
            record.message = "\033[1;%dm"%COLORS["red"] + record.message + "\033[0m"
        return logging.Formatter.format(self, record)



class logsys:
    '''日志系统
    '''
    def __init__(self, name, level=10):
        self.logger = logging.getLogger(name)
        if level <= 10:
            loglevel = logging.DEBUG
        elif level <= 20:
            loglevel = logging.INFO
        else:
            loglevel = logging.ERROR
        self.logger.setLevel(loglevel)
        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler("log(%s-%s).log"%(name,datetime.datetime.now().strftime('%Y%m%d%H')))
        fhformatter = logging.Formatter("[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        fh.setFormatter(fhformatter)
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        chformatter = ColorFormatter("[%(asctime)s][%(levelname)s][%(name)s]:  %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        ch.setFormatter(chformatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        
    
    def getlogger(self):
        return self.logger
        

class recovsys:
    '''恢复系统
    path 目录路径
    '''
    def __init__(self, path="bak"):
        self.hasfile = False
        if not os.path.exists(path):
            os.makedirs(path)
        self.filenames = list()
        for f in os.listdir(path):
            if ".bak" == f[-4:]:
                self.filenames.append(path + "/" + f)
                self.hasfile = True
        self.filename = path + "/" + "recov_%s.bak"%(datetime.datetime.now().strftime("%Y%m%d%H%M"))
    
    def clean(self):
        for recovfile in self.filenames:
            os.remove(recovfile)
    
    def backup(self, data: dict):
        with open(self.filename, "a") as fw:
            w_data = json.dumps(data)
            fw.write(w_data)
            fw.write("\n")

    def recover(self):
        for recovfile in self.filenames:
            with open(recovfile, "r") as fr:
                for line in fr.readlines():
                    data = json.loads(line)
                    yield data 
