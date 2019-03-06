from BaiduMapAPI.common import convertCoord, expandUp
import pytest

def test_convertCoord():
    coord = convertCoord("12.32323,56.23422")
    assert coord == "12.32323,56.23422"
    coord = convertCoord((12.32323,56.23422))
    assert coord == "12.32323,56.23422"

def test_expandUp():
    test_dict = {"a" : "A", "b":{"bB": [{"Ba": 2}, "Bb", "Bc"], "bc": {"bcd":{"bcd": 4}}}}
    testValue = expandUp(test_dict, "test")
    assert testValue == {'test_a': 'A', 'test_b_bB_0_Ba': 2, 'test_b_bB_1': 'Bb', 
                        'test_b_bB_2': 'Bc', 'test_b_bc_bcd_bcd': 4}