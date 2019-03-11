# -*- coding: utf-8 -*- 

import json
import pytest

from BaiduMapAPI.base import TransitObject

def test_TransitObject():
    with open("transit.json", "r") as fr:
        test_data = json.load(fr)
    trans = TransitObject()
    trans.parse(test_data)
    assert trans.total_line == 99
    df = trans.to_dataframe()
    assert len(df) == 10
    df.to_csv("test.csv",encoding="utf-8")
    