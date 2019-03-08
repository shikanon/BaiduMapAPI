# -*- coding: utf-8 -*- 
import pandas as pd

def getAllChStreet(year=2018):
    '''
    get the all street in China, the return is a DataFrame type.
    '''
    if year not in [2016, 2017, 2018]:
        return ValueError("We haven't this year dataset, you can use data file to get data")
    return pd.read_csv("http://baidumapapi.shikanon.com/data/ChUnit%d.csv"%year, encoding="utf-8")

def getAllChStreetCoord(year=2018):
    '''
    get the all street and its coords in China, the return is a DataFrame type.
    '''
    if year not in [2017]:
        return ValueError("We haven't this year dataset, you can use data file to get data")
    return pd.read_csv("http://baidumapapi.shikanon.com/data/ChUnitWithCoords%d.csv"%year, encoding="utf-8")