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



url3 = "http://api.letv.com/mms/out/video/playJson?id=1744455&platid=1&splatid=101&format=1&tkey=610081946&domain=www.letv.com"
def query_info3(url):
    headers = {
               "Accept-Encoding": "gzip, deflate, sdch",
               "Host": "api.letv.com",
               "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
               'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36",
               "X-Forwarded-For": "220.181.111.129",
               "Client-IP": "220.181.111.129",
               "Accept": "*/*",
               "Cache-Control": "max-age=0",
               "X-Requested-With": "ShockwaveFlash/16.0.0.257",
               "Referer": "http://www.letv.com/ptv/vplay/1744455.html",
               "Cookie": "tj_uuid=14229267983480465227; tj_lc=6fe003d1e4353eb4604fce17ca0dfb2c; newVideo=%7B%221%22%3A30%2C%222%22%3A138%2C%223%22%3A791%2C%224%22%3A773%2C%225%22%3A35%2C%228%22%3A14%2C%229%22%3A36%2C%2211%22%3A80%2C%2214%22%3A5%2C%2216%22%3A0%2C%2217%22%3A0%2C%2219%22%3A0%2C%2220%22%3A7%2C%2222%22%3A205%2C%2223%22%3A2%2C%2230%22%3A7774%2C%2232%22%3A0%2C%2233%22%3A1%2C%2234%22%3A114%2C%2235%22%3A0%2C%2236%22%3A0%2C%2238%22%3A0%7D; tj_v2c=-1744455_1; tj_env=1; vjuids=6832aee99.14b4d0c9421.0.b030cfe; vjlast=1422926845.1422926845.30; statCookie=1", 
              }
    req = urllib.request.Request(url, None, headers)
    #opn = urllib.request.build_opener(urllib.request.ProxyHandler({'http': 'proxy.uku.im:8888'}))
    opn = urllib.request.build_opener(urllib.request.ProxyHandler({'http': '220.181.111.129:3128'}))
    #opn = urllib.request.build_opener()
    return opn.open(req).read().decode('utf8')

print(query_info3(url3))
