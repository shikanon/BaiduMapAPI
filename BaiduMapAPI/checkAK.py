# -*- coding: utf-8 -*- 
import urllib
import hashlib
import requests


class URLEncryption:
    
    def __init__(self, ak, sk):
        self.ak = ak
        self.sk = sk
        self.url = None

    def encryption(self, urlPath, payload):
        '''
        urlPath : string , exmaple: "/geocoder/v2/",
        payload : dict or string, exmaple: 
        {"address": "百度大厦", "output": "json", "ak": yourak} or
        address=百度大厦&output=json&ak=yourak
        '''
        if isinstance(payload, str):
            queryStr = urlPath + "?" + payload
            encodedStr = urllib.parse.quote(queryStr, safe="/:=&?#+!$@|")
        elif isinstance(payload, dict):
            encodedStr = urlPath + "?" + urllib.parse.urlencode(payload, safe="/:=&?#+!@")
        else:
            raise ValueError("payload参数值错误")
        
        # sk 加密计算
        # 在最后直接追加上sk
        rawStr = encodedStr + self.sk
        # md5计算出的sn值7de5a22212ffaa9e326444c75a58f9a0
        sn = hashlib.md5(urllib.parse.quote_plus(rawStr).encode("utf-8")).hexdigest()
        return sn

    def get(self, host, urlPath, payload, retry=2):
        '''
        host: string, example: "http://api.map.baidu.com"
        urlPath : string , exmaple: "/geocoder/v2/",
        payload : dict , exmaple: 
        {"address": "百度大厦", "output": "json", "ak": yourak}
        '''
        sn = self.encryption(urlPath, payload)
        payload["sn"] = sn
        for i in range(retry):
            try:
                r = requests.get(host + urlPath, params=payload)
                break
            except requests.exceptions.ConnectionError as e:
                print("retry %s"%(host + urlPath))
                if i == (retry - 1):
                    raise e
            except Exception as e:
                raise e
        self.url = r.url
        return r.content

