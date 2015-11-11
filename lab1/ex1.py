__author__ = 'Lin'

import urllib2
from BeautifulSoup import BeautifulSoup
urlText = 'http://www.cnblogs.com/yuchenlin/'
#urlText = 'http://www.baidu.com/'
content = urllib2.urlopen(urlText).read()

bs = BeautifulSoup(content)

#print bs.head.title.string
def getAllUrl(ctnt):
    urlset = set() 
    for i in ctnt.findAll('a'):
        str = i.get('href')
        if(str!=None):
            if(str[-1]=='/' and len(str)>2):
                str = str[:-1]
            if(str[:2]=='//'):
                urlset.add('http:'+str)
            elif(str[:2]=='ja' or str[:2]=='/'):
                continue
            else:
                urlset.add(str)
    return  urlset

urlset =  getAllUrl(bs)

f = file("res1.txt","w")
strText = ""
for i in urlset:
    strText += (i + "\r\n")
f.write(strText)
f.close()