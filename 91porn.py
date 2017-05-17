# -*- encoding: utf-8 -*-
from bs4 import BeautifulSoup as bs
import requests
import html5lib
import re
from ProgressBar import ProgressBar
import random
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import http
import time
from contextlib import closing

proxies = {
    "https": "https://112.193.91.55:80"
}

url = 'http://email.91dizhi.at.gmail.com.t9i.club/video.php?category=rf'
cookies = dict(language='cn_CN')


# 设置 user-agent列表，每次请求时，可在此列表中随机挑选一个user-agnet
uas = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/58.0.3029.96 Chrome/58.0.3029.96 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0; Baiduspider-ads) Gecko/17.0 Firefox/17.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9b4) Gecko/2008030317 Firefox/3.0b4",
    "Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; BIDUBrowser 7.6)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko",
    ]



def setHeader():
    randomIP = str(random.randint(0, 255)) + '.' + str(random.randint(0, 255)) + '.' + str(
        random.randint(0, 255)) + '.' + str(random.randint(0, 255))
    headers = {
        'User-Agent': random.choice(uas),
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        'X-Forwarded-For': randomIP,
    }
    return headers

def getContent(url,stream=False):
    try:
        s = requests.Session()
        retries = Retry(total= 5,
                        backoff_factor=10,
                        status_forcelist=[500,502,503,504]
                        )
        s.mount('http://',HTTPAdapter(max_retries= retries))
        return s.get(url,headers = setHeader(),stream=stream)
    except ConnectionResetError:
        print('ConnectionResetError')
        time.sleep(10)
        getContent(url,stream=False)
    except http.client.IncompleteRead:
        print('http.client.IncompleteRead')
        time.sleep(10)
        getContent(url,stream=False)

# r = requests.get(url, headers=setHeader(), cookies=cookies)
r = getContent(url)
# print(r.status_code)

soup = bs(r.text, 'html5lib')
videoPages = set()
for link in soup.find_all('a'):
    # print(link.get('href'))
    ss = link.get('href')
    if len(ss) > 8 and ss.find('view_video') != -1:
        videoPages.add(ss)

print(videoPages)

videoLinks = set()
for link in videoPages:
    # page = requests.get(link, headers=setHeader(), cookies=cookies)
    page = getContent(link)
    # print(page.text.encode(page.encoding).decode('utf-8'))
    utext = page.text.encode(page.encoding).decode('utf-8')
    soup2 = bs(utext, 'html5lib')
    # print(soup2.text)
    vurl = soup2.find('video').find('source').get('src')
    videoTitle = soup2.find(id='viewvideo-title').get_text().strip()
    fileType = re.findall('\.(.{3}?)\?',vurl)  # .mp4\.avi
    # print(soup2.find('video').find('source').get('src'))
    print(vurl)
    fileName = videoTitle + '.' + fileType[0]
    # print(fileName)
    # exit()
    # res = requests.get(vurl,stream=True)
    # res = getContent(vurl,stream=True)
    with closing(getContent(vurl,stream=True)) as res:
        chunk_size = 1024
        content_size = int(res.headers['content-length'])
        progress = ProgressBar(videoTitle, total=content_size, unit="KB", chunk_size=chunk_size, run_status="正在下载",
        fin_status="下载完成")
        file = open(fileName,'wb')
        for chunk in res.iter_content(chunk_size=512):
            if chunk:
                file.write(chunk)
                progress.refresh(count=len(chunk))
