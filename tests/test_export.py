import json
import pytest

from BaiduMapAPI.api import MapDirection
from BaiduMapAPI.export import BaiduResultExport
from .constant import AK, SK

def test_BaiduResultExport():
    direction = MapDirection(AK, SK)
    origin = "23.137903,113.34348"
    destination = "22.638172,113.821705"
    content = direction.transit(origin, destination)
    BaiduResultExport(content)
