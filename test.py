#coding:utf-8
import cookielib
import urllib2

request = urllib2.Request('http://coding.imooc.com/class/chapter/92.html#Anchor')
request.add_header('user-agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36')
response= urllib2.urlopen(request)
