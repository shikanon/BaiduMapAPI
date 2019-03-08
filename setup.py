# -*- coding: utf-8 -*- 
import os
import sys
from shutil import rmtree

from setuptools import Command, find_packages, setup


__lib_name__ = "BaiduMapAPI"
__lib_version__ = "0.1.2"
__description__ = "The Package of Baidu Map, with unofficial"
__url__ = "https://github.com/shikanon/BaiduMapAPI"
__author__ = "shikanon"
__author_email__ = "account@shikanon.com"
__license__ = "MIT"

__keywords__ = ["Baidu", "map"]

__requires__ = [
    "requests",
]


with open("README.rst", "r", encoding="utf-8") as f:
    __long_description__ = f.read()


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
    data_files = [("BaiduMapAPI/data", ["BaiduMapAPI/data/BaiduMap_cityCode_1102.txt"])],
    long_description = __long_description__
)