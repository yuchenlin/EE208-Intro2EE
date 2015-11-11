
#coding=utf8
import sys
import time
import jieba
from MyBloomFilter import *
reload(sys)
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup




import codecs

f = open('url2file_index_jditem.txt','r')
urlDict = {}
for line in f.xreadlines():
	ls = line.split()
	if('rss' in ls[1]):
		continue
	urlDict[ls[0]] = ls[1].strip()
f.close()
count = 0
mbf = MyBloomFilter.MyBloomFilter(32000,3)

def getImgInfo(item):
	global count
	FOLDER_NAME = 'html/'
	path = FOLDER_NAME + item
	f = codecs.open(path,'r')
	html = f.read()
	f.close()
	bs = BeautifulSoup(html,'html.parser')
	if(bs.title==None):
		return
	title = bs.title.text.strip()
	for img in bs.find_all('img'):
		src = img.get('src','')
		if(src=='' or not (src.endswith('jpg') or src.endswith('png'))):
			continue
		src = 'http:' + src
		if(mbf.lookup(src)): #BloomFilter
			continue
		mbf.add(src)
		alt = img.get('alt','')
		if(alt==''):
			continue
		alt = ' '.join(jieba.cut(alt.strip()))
		url = urlDict[item]	
		tosave = url+'seg^*'+title+'seg^*'+src+'seg^*'+alt
		count+=1
		print count,'*'
		index = codecs.open('picIndex.txt','a')	
		index.write(tosave.encode('utf-8','ignore')+'\n')
		index.close() 

def MultiProcessing():
	global urlDict
	# from multiprocessing import Pool
	# from multiprocessing.dummy import Pool as TPool
	start = time.time()
	# p = TPool(10)#设置线程池
	# p.map(getImgInfo,urlDict)
	# p.close()
	# p.join()
	for item in urlDict:
		getImgInfo(item)
	print time.time()-start
MultiProcessing()
