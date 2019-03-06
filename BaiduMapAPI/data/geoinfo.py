# -*- coding: utf-8 -*- 

import requests
import urllib
from bs4 import BeautifulSoup
import time


class GeoInfoCrawler:
    def __init__(self, year=2018):
        self.year = year
        self.first_url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/%d/index.html"%year

        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}

        self.fw = open("ChAdminUnit%d.csv"%year, "w", encoding="utf-8")
        file_header = "省,城市id,城市,区镇id,区镇,街道id,街道"
        self.fw.write(file_header+"\n")
    
    def crawl(self):
        first_sess = requests.get(self.first_url, headers=self.headers)
        first_soup = BeautifulSoup(first_sess.content, "html5lib")
        for el in first_soup.select(".provincetr a"):
            self.province_name = el.get_text()
            city_url = urllib.parse.urljoin(first_sess.url, el["href"])
            try:
                self.parse_city(city_url)
            except:
                time.sleep(5*60)
                self.parse_city(city_url)
            print(el.get_text())

    def parse_city(self, city_url):
        city_sess = requests.get(city_url, headers=self.headers)
        city_soup = BeautifulSoup(city_sess.content, "html5lib")
        n = 1
        for el_city in city_soup.select(".citytr a"):
            if n % 2 == 0:
                self.city_name = el_city.get_text()
                print(self.city_name)
                county_url = urllib.parse.urljoin(city_sess.url, el_city["href"])
                try:
                    self.parse_county(county_url)
                except:
                    time.sleep(5*6)
                    self.parse_county(county_url)
            else:
                self.city_id = el_city.get_text()
            n += 1

    def parse_county(self, county_url):
        county_sess = requests.get(county_url, headers=self.headers)
        county_soup = BeautifulSoup(county_sess.content, "html5lib")
        m = 1
        for el_county in county_soup.select(".countytr a"):
            if m % 2 == 0:
                self.county_name = el_county.get_text()
                street_url = urllib.parse.urljoin(county_sess.url, el_county["href"])
                try:
                    self.parse_street(street_url)
                except:
                    time.sleep(5)
                    self.parse_street(street_url)
            else:
                self.county_id = el_county.get_text()
            m += 1

    def parse_street(self, street_url):
        street_sess = requests.get(street_url, headers=self.headers)
        street_soup = BeautifulSoup(street_sess.content, "html5lib")
        p = 1
        for el_street in street_soup.select(".towntr a"):
            if p % 2 == 0:
                self.street_name = el_street.get_text()
                self.write()
            else:
                self.street_id = el_street.get_text()
            p += 1
    
    def write(self):
        content = self.province_name + "," + self.city_id + "," + self.city_name + \
            "," + self.county_id + "," + self.county_name + "," + self.street_id + \
            "," + self.street_name
        self.fw.write(content+"\n")


if __name__ == "__main__":
    geo = GeoInfoCrawler(2016)
    geo.crawl()
