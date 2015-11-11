# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import urllib2 
req = urllib2.Request("http://www.qiushibaike.com/pic", None, {'User-agent' : 'Custom User Agent'})
content = urllib2.urlopen(req).read()
from bs4 import  BeautifulSoup
constTitle = "http://www.qiushibaike.com"
import re
def getQiushibaikePage(content):
    docs={}
    bs = BeautifulSoup(content)    
    nextPage = constTitle + bs.find('a',{'class':'next'}).get('href')
    print nextPage
    for qiu_item in bs.findAll('div',{'id':re.compile('^qiushi_tag_\d+')}):
        tag = str(qiu_item.get('id'))[11:]
        imgurl = qiu_item.find('div',{'class':'thumb'}).find('a').find('img').get('src')
        qiushi = qiu_item.find('div',{'class':'content'}).contents[0]#.decode('utf-8')
        docs[tag] ={"content" : qiushi ,"imgurl":imgurl}   
    return docs,nextPage

returnVals = getQiushibaikePage(content)
textToSave = ""
for i in returnVals[0]:
    textToSave +=  returnVals[0][i]['imgurl']+ "\t"
    textToSave +=  returnVals[0][i]['content'].decode('utf-8').strip() + "\r\n"
f = open("res3.txt","w")
f.write(textToSave)
f.close()

