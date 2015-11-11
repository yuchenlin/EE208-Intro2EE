# -*- coding: utf-8 -*-
__author__ = 'Lin'

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from BeautifulSoup import BeautifulSoup
import urllib2
import time
import re
import urlparse
import os
import urllib
import Queue
import threading
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import MyBloomFilter


def valid_filename(s):
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    #  -_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
    s = ''.join(c for c in s if c in valid_chars)
    return s

def get_page(page):
    #try-catch
    try:
        # print page 
        html = urllib2.urlopen(page,timeout=3).read() 
    except Exception,e:
        #print e,'---------',page 
        return None
    content = html
    return content

#with bs
def get_all_links_(content, page):
    if(content == None): 
        return []
    import re
    content = BeautifulSoup(content)
    urls = content.findAll('a',{'href':re.compile('^http|^/')})
    urlset = set() #to ensure uniqueness
    for u_item in urls:
        u = str(u_item.get('href'))
        if(not re.match('^http',u)):
            u = urlparse.urljoin(page,u)
        if(len(u) > 5 and u!=page and u not in crawled):# very important 否则进程结束不了
            urlset.add(u)
    links = list(urlset)
    return links

#without bs
def get_all_links(content, page):
    if content == None:
        return []
    import re
    urlset = set() 
    urls = re.findall(r"<a.*?href=.*?<\/a>",content,re.I)
    for i in urls:
        u=""
        href = re.findall(r'href=".*?"',i,re.I)
        if(len(href)==1):
            url = href[0].split('"')[1] 
            if(len(url)<5): continue #某些太短的无意义代码
            if('javascript' in url or url[0]=='#'): #js和锚标记
                continue
            elif(url[0:4]=='http'):#绝对地址
                u = url
            else:#相对地址
                u = urlparse.urljoin(page,url)
        if(u!=""):
            urlset.add(u)
    links = list(urlset)
    return links 



def add_page_to_folder(page, content): #将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    if content==None:
        return
    try:
        index_filename = 'index.txt'    #index.txt中每行是'网址 对应的文件名'
        folder = 'html'                 #存放网页的文件夹
        filename = valid_filename(page) #将网址变成合法的文件名
        index = open(index_filename, 'a')
        index.write(page.encode('ascii', 'ignore') + '\t' + filename + '\n')
        index.close()
        if not os.path.exists(folder):  #如果文件夹不存在则新建
            os.mkdir(folder)
        f = open(os.path.join(folder, filename), 'w')
        f.write(str(content))                #write the page into a file
        f.close()
    except Exception,e:
        print e
def working():
    global count,crawled,max_page,q
    while count <= max_page:
        if (count==0 or q.qsize>0):
            page = q.get()
        else:
            break
        if not mbf.lookup(page):
            content = get_page(page)
            if(content!=None):
                
                if(count <= max_page):
                    print count,page
                    add_page_to_folder(page,content)
                    outlinks = get_all_links(content,page)
                    for link in outlinks:
                        if(q.qsize() + count > max_page):
                            break
                        q.put(link)
                    if varLock.acquire():
                        count += 1
                        graph[page] = outlinks
                        mbf.add(page)
                        varLock.release()
            if q.unfinished_tasks: 
                q.task_done()
    while q.unfinished_tasks:
        if varLock.acquire():
            q.task_done()
            varLock.release()
crawled = []
graph = {}
count = 0
threadNUM = 30
max_page = 500
varLock = threading.Lock()
mbf = MyBloomFilter.MyBloomFilter(32000,3)


begin = time.time()
q = Queue.Queue()
q.put('http://www.sjtu.edu.cn')
for i in range(threadNUM):
    t = threading.Thread(target = working)
    t.setDaemon(True)
    t.start()
q.join()
print time.time() - begin
