# -*- coding: utf-8 -*-
__author__ = 'Lin'


import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import  urllib2,urllib,cookielib
from BeautifulSoup import BeautifulSoup
def bbsSet(id, pwd , text):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    postdata = urllib.urlencode({'id':id,'pw':pwd,'submit':'login'})
    req = urllib2.Request(url="https://bbs.sjtu.edu.cn/bbslogin",data=postdata)#this is a post request
    response = urllib2.urlopen(req) #login

    toUpdate = urllib.urlencode({'type':'update','text':text.encode('gb2312')})
    #encode
    req = urllib2.Request(url='https://bbs.sjtu.edu.cn/bbsplan',data=toUpdate)
    response = urllib2.urlopen(req)
    content = urllib2.urlopen('https://bbs.sjtu.edu.cn/bbsplan').read()
    bs = BeautifulSoup(content)
    print bs.find('textarea').string.strip().decode('utf-8')

id = "yuchenlin"
pwd = "wobuzhidao"
text = u"I am a gasdood....<<< >>> **(*&.. "
bbsSet(id,pwd,text)


