__author__ = 'Lin'

import urllib2
from BeautifulSoup import BeautifulSoup

content = urllib2.urlopen('http://tieba.baidu.com/p/2127779138#!/l/p1').read()

bs = BeautifulSoup(content)

#print bs.head.title.string
def getAllIMG(ctnt):
    imgSet = set()
    for i in ctnt.findAll('img'):
        str = i.get('src')
        if(str!=None):
            imgSet.add(str)
    return  imgSet

imgSet =  getAllIMG(bs)

f = file("res2.txt","w")
strText = ""
for i in imgSet:
    strText += (i + "\r\n")
f.write(strText)
f.close()
#
# __author__ = 'Lin'
#
# import urllib2
# from BeautifulSoup import BeautifulSoup
#
# content = urllib2.urlopen('http://tieba.baidu.com/p/2127779138#!/l/p1').read()
#
# bs = BeautifulSoup(content)
#
# #print bs.head.title.string
# def getAllUrl(ctnt):
#     urlset = set()
#     for i in ctnt.findAll('img'):
#         str = i.get('src')
#         if(str!=None):
#             urlset.add(str)
#     return  urlset
#
# urlset =  getAllUrl(bs)
#
# f = file("res2.txt","w")
# strText = ""
# for i in urlset:
#     strText += (i + "\r\n")
# f.write(strText)
# f.close()