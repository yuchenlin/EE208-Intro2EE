# http://music.163.com/#/song?id=33367671


import urllib
import urllib2
from bs4 import BeautifulSoup

for i in range(33367671,33444444):
	html = urllib2.urlopen('http://music.163.com/song?id='+str(i)).read()
	bs = BeautifulSoup(html,'html.parser')
	print bs.title.text ,  'http://music.163.com/song?id='+str(i) 

	