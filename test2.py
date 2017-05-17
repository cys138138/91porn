# -*- encoding: utf-8 -*-

import re
import random
import sys
import time
import datetime
import threading
from random import choice
import requests
import bs4
import html5lib

def get_ip():
    """获取代理IP"""
    url = "http://www.xicidaili.com/wt/"
    headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
                "Accept-Encoding":"gzip, deflate, sdch",
                "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
                "Referer":"http://www.xicidaili.com",
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
                }
    r = requests.get(url,headers=headers)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    data = soup.table.find_all("td")
    ip_compile= re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>')    # 匹配IP
    port_compile = re.compile(r'<td>(\d+)</td>')                # 匹配端口
    ip = re.findall(ip_compile,str(data))       # 获取所有IP
    port = re.findall(port_compile,str(data))   # 获取所有端口
    return [":".join(i) for i in zip(ip,port)]  # 组合IP+端口，如：115.112.88.23:8080

# 设置 user-agent列表，每次请求时，可在此列表中随机挑选一个user-agnet
uas = [
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0; Baiduspider-ads) Gecko/17.0 Firefox/17.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9b4) Gecko/2008030317 Firefox/3.0b4",
    "Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; BIDUBrowser 7.6)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko",
    ]

def get_url(code=0,ips=[]):
    """
        投票
        如果因为代理IP不可用造成投票失败，则会自动换一个代理IP后继续投
    """
    try:
        ip = choice(ips)
    except:
        return False
    else:
        proxies = {
            "http":ip,
        }
        headers2 = { "Accept":"text/html,application/xhtml+xml,application/xml;",
                        "Accept-Encoding":"gzip, deflate, sdch",
                        "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
                        "Referer":"",
                        "User-Agent":choice(uas),
                        }
    try:
        num = random.uniform(0,1)
        hz_url = "http://www.baidu.com/"
        hz_r = requests.get(hz_url,headers=headers2,proxies=proxies)
    except requests.exceptions.ConnectionError:
        print("ConnectionError")
        if not ips:
            print("not ip")
            sys.exit()
        # 删除不可用的代理IP
        if ip in ips:
            ips.remove(ip)
        # 重新请求URL
        get_url(code,ips)
    else:
        date = datetime.datetime.now().strftime('%H:%M:%S')
        print("第%s次 [%s] [%s]：投票%s (剩余可用代理IP数：%s)") % (code,date,ip,hz_r.text,len(ips))



ips = []
for i in range(6000):
    # 每隔1000次重新获取一次最新的代理IP，每次可获取最新的100个代理IP
    if i % 1000 == 0:
        ips.extend(get_ip())
    # 启用线程，隔1秒产生一个线程，可控制时间加快投票速度 ,time.sleep的最小单位是毫秒
    t1 = threading.Thread(target=get_url,args=(i,ips))
    t1.start()
    time.sleep(1)

