# -*- coding: utf-8 -*- 
import os
import sys
from shutil import rmtree

from setuptools import Command, find_packages, setup


__lib_name__ = "BaiduMapAPI"
__lib_version__ = "0.1"
__description__ = "The Package of Baidu Map, with unofficial"
__url__ = "http://baidumapapi.shikanon.com/"
__author__ = "shikanon"
__author_email__ = "account@shikanon.com"
__license__ = "MIT"

__keywords__ = ["Baidu", "map"]

__requires__ = [
    "requests",
]


setup(
    name = __lib_name__,
    version = __lib_version__,
    description = __description__,
    url = __url__,
    author = __author__,
    author_email = __author_email__,
    license = __license__,
    packages = find_packages(exclude=("tests", "exmaple")),
    install_requires = __requires__,
    zip_safe = False,
    include_package_data = True,
    data_files = [("BaiduMapAPI", ["BaiduMapAPI/data/BaiduMap_cityCode_1102.txt"])]
)