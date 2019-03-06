import json
import pytest

from .constant import AK, SK
from BaiduMapAPI.checkAK import URLEncryption
from BaiduMapAPI.globals import HOST

def test_URLEncryption():
    encry = URLEncryption(AK, SK)
    urlPath = "/geocoder/v2/"
    payload = {"address": "百度大厦", "output": "json", "ak": AK}
    content = encry.get(HOST, urlPath, payload)
    print(content)
    result = json.loads(content)
    assert result["status"] == 0