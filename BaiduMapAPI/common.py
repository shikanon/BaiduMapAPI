# -*- coding: utf-8 -*- 

def convertCoord(coord):
    if (isinstance(coord, tuple) or isinstance(coord, list)) and len(coord) == 2:
        return str(coord[0]) + "," + str(coord[1])
    elif isinstance(coord, str):
        if len(coord.split(",")) == 2:
            return coord
    raise ValueError("坐标值错误:%s"%str(coord))


def convertBatchCoord(coords, sep=";"):
    if isinstance(coords, tuple) or isinstance(coords, list):
        coord = ""
        for c in coords:
            coord = coord + sep + convertCoord(c)
        return coord
    elif isinstance(coords, str):
        return coords
    raise ValueError("坐标值错误:%s"%str(coords))


def expandUp(value, key):
    '''
    使用递归遍历 dict or list, 一直展开使得其值不在存在为dict类型，
    参数：
    value: 值;
    key: 主键;
    for exmaple:
    test_dict = {"a" : "A", "b":{"bB": [{"Ba": 2}, "Bb", "Bc"], "bc": {"bcd":{"bcd": 4}}}}
    expandUp(test_dict, "test")
    ## {'test_a': 'A', 'test_b_bB_0_Ba': 2, 'test_b_bB_1': 'Bb', 'test_b_bB_2': 'Bc', 'test_b_bc_bcd_bcd': 4}
    '''
    res = dict()
    if isinstance(value, dict):
        for k in value:
            if isinstance(value[k], dict) or isinstance(value[k], list): # 如果是dict or list,则继续展开
                child = expandUp(value[k], key+"_"+k)
                res.update(child)
            else:
                res[key+"_"+k] = value[k]
    elif isinstance(value, list):
        for i in range(len(value)):
            if isinstance(value[i], dict) or isinstance(value[i], list): # 如果是dict or list,则继续展开
                child = expandUp(value[i], key+"_"+str(i))
                res.update(child)
            else:
                res[key+"_"+str(i)] = value[i]
    return res