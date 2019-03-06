# -*- coding: utf-8 -*- 
import json
from BaiduMapAPI.common import expandUp

def JsonExpand(originValue):
    if isinstance(originValue, str):
        jsonDict = json.loads(json.loads(originValue))
    elif isinstance(originValue, dict):
        jsonDict = originValue
    else:
        raise ValueError("传入参数值必须为 string 或者 dict, 不能为%s"%str(originValue))
    return expandUp(jsonDict, "DATA")

def BaiduResultExport(content):
    res = json.loads(content)
    if "result" not in res:
        raise ValueError("传入内容没有结果，无法解析")
    res = res["result"]
    expandRes = JsonExpand(res)
    print(expandRes)
