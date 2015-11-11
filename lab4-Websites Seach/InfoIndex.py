
#coding=utf8
import sys
import time
reload(sys)
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup

import codecs

f = open('url2file_index_sjtu.txt','r')
urlDict = {}
for line in f.xreadlines():
	ls = line.split()
	if('rss' in ls[1]):
		continue
	urlDict[ls[0]] = ls[1].strip()
f.close()

#对一个文件进行处理
def processTheInfo():
	global urlDict
	FOLDER_NAME = 'html/'
	for item in urlDict:
		#item = '7d48a36713e5da9a5541b097c131fda8.html'
		path = FOLDER_NAME + item
		f = codecs.open(path,'r')
		html = f.read()
		f.close()
		title_begin = html.find('<title>')+7
		title = ''
		if(title_begin==6):
			title_begin = html.find('<TITLE>')+7
			title_end = html.find('</TITLE>')
		else:
			title_end = html.find('</title>')
		if(title_end==-1):
			continue
		title = html[title_begin:title_end].strip()
		tosave = item+' '+urlDict[item]+' '+title
		print title,urlDict[item]
		if(title=='知乎 - 与世界分享你的知识、经验和见解'):
			continue
		index = codecs.open('infoIndex.txt','a')	
		index.write(tosave.encode('utf-8','ignore')+'\n')
		index.close()

def SolveCodingProblem():
	global urlDict
	from chardet.universaldetector import UniversalDetector
	FOLDER_NAME = 'html/'
	detector = UniversalDetector()
	for item in urlDict:
		filename = FOLDER_NAME + item
		f = open(filename,'r')
		html = f.read()
		f.close()
		code = 'utf-8'
		if('GB' in html or 'gb' in html):
			code = 'gbk'
		if(code=='gbk'):
			html = html.decode('gbk','ignore').encode('utf-8')
		else:
			html = html.decode('utf-8','ignore').encode('utf-8')
		f = codecs.open(filename,'w',encoding='utf-8')
		f.write(html)
		f.close()
count = 0
def CleanSegAndSave(filepath):
	#filepath = 'd21a8b47718c9f0eb76e18b1ca028845.html'
	import os
	if(os.path.exists('txt/'+filepath+'.txt')):
		return
	global count
	f = open('html/'+filepath,'r')
	html = f.read()
	f.close()
	#print nltk.clean_html(html)
	bs = BeautifulSoup(html,"html.parser")
	start = time.time()
	text = clean(html) #0.013
	#print bs.get_text() #0.003
	#print ''.join(bs.findAll(text=True))	#0.020
	import jieba
	l = jieba.cut(text,HMM=True)
	final = []
	stopwords='你们我们他们是这个那个的地得和']
	for i in l:
		if(i in stopwords):
			continue
		else:
			final.append(i)
	txt = " ".join(final)
	
	f = codecs.open('txt/'+filepath+'.txt','w',encoding='utf-8')
	f.write(txt)
	f.close()
	count+=1
	print count
	#print time.time() - start

#SolveCodingProblem()

#processTheInfo()

#去除html标签和标点符号等
def clean(html):
	import re,string
	text = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())		
	text = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", text)	
	text = re.sub(r"(?s)<.*?>", "", text)		
	text = re.sub(r"&.*?;", "", text)
	todelete = ['\n','\r','\t','，','。','？','、','！','：','“ ','” ',' ','；','-','.','"','”','“',':','?','（','）','(',')']

	for i in todelete:
		text = text.replace(i,'')
	return text

def MultiProcessingCleanAndSave():
	f = codecs.open('infoIndex.txt','r',encoding='utf-8')
	files = []
	for line in f.xreadlines():
		files.append(line.split()[0])
	f.close()
	from multiprocessing import Pool
	from multiprocessing.dummy import Pool as TPool
	start = time.time()
	p = TPool(10)#设置线程池
	p.map(CleanSegAndSave,files)
	p.close()
	p.join()
	print time.time()-start
MultiProcessingCleanAndSave()
#processTheInfo()
#CleanSegAndSave('')
