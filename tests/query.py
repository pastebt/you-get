#! /usr/bin/python3

import urllib.request


USER_AGENT="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36"

def query_info2(url):
    headers = {'User-Agent': USER_AGENT,

               #"X-Forwarded-For": "220.181.111.171",
               #"Client-IP": "220.181.111.171",
               #"Referer": "http://www.bilibili.com/video/av1251587/",
               #"X-Requested-With": "ShockwaveFlash/16.0.0.296",

               #'Referer': 'http://ccf.pptv.com/0',
              }
    req = urllib.request.Request(url, None, headers)
    #opn = urllib.request.build_opener(urllib.request.ProxyHandler({'http': 'proxy.uku.im:8888'}))
    opn = urllib.request.build_opener()
    return opn.open(req).read().decode('utf8')

url = "http://interface.bilibili.com/playurl?accel=1&cid=1905810&player=1&ts=1422843177&sign=aa690f529ef94ac33e7de956d64aea91"
url2 = "http://interface.bilibili.com/playurl?appkey=85eb6835b0a1034e&cid=1905810&sign=509a4cad95e466e91261b5e0838718b1"

def query_info3(url):
    headers = {
               "Accept-Encoding": "gzip, deflate, sdch",
               "Host": "api.letv.com",
               "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
               'User-Agent': USER_AGENT,
               "X-Forwarded-For": "220.181.111.129",
               "Client-IP": "220.181.111.129",
               "Accept": "*/*",
               "Cache-Control": "max-age=0",

               "X-Requested-With": "ShockwaveFlash/16.0.0.257",
               "Referer": "http://www.letv.com/ptv/vplay/1744455.html",

              }
    req = urllib.request.Request(url, None, headers)
    #opn = urllib.request.build_opener(urllib.request.ProxyHandler({'http': 'proxy.uku.im:8888'}))
    opn = urllib.request.build_opener()
    return opn.open(req).read().decode('utf8')

url3 = "http://api.letv.com/mms/out/video/playJson?id=1744455&platid=1&splatid=101&format=1&tkey=610081946&domain=www.letv.com"
print(query_info3(url3))
