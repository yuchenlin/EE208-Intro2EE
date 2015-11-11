# -*- coding: utf-8 -*-
__author__ = 'Lin'


import sys
reload(sys)
sys.setdefaultencoding("utf-8")


from BeautifulSoup import BeautifulSoup
import urllib2
import re
import urlparse
import os
import urllib


def valid_filename(s):
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    #  -_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
    s = ''.join(c for c in s if c in valid_chars)
    return s

def get_page(page,enableTimeout=False):
    #try-catch
    try:
        print page
        if(enableTimeout):
            html = urllib2.urlopen(page,timeout=2).read()
        else:
            html = urllib2.urlopen(page).read()
    except Exception,err:
        print err
        return None
    content = BeautifulSoup(html)
    return content

def get_all_links(content, page):
    import re
    urls = content.findAll('a',{'href':re.compile('^http|^/')})
    urlset = set() #to ensure uniqueness
    for u_item in urls:
        u = str(u_item.get('href'))

        if(not re.match('^http',u)):
            u = urlparse.urljoin(page,u)
        urlset.add(u)
    links = list(urlset)
    return links
        
def union_dfs(a,b):
    for e in b:
        if e not in a:
            a.append(e)
            
def union_bfs(a,b):
    for e in b:
        if e not in a:
            a.insert(0,e)
       
def add_page_to_folder(page, content): #将网页存到文件夹里，将网址和对应的文件名写入index.txt中
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
    
def crawl(seed, method, max_page):
    tocrawl = [seed]
    crawled = []
    graph = {}
    count = 0
    
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            #print page
            if(count==0):
                content = get_page(page)
            else:
                content = get_page(page,enableTimeout=True)
            if(content==None):
                continue
            count += 1
            add_page_to_folder(page, content)
            outlinks = get_all_links(content, page)
            graph[page] = outlinks
            globals()['union_%s' % method](tocrawl, outlinks)
            crawled.append(page)
            #pass
            if(count >= max_page):
                break
    return graph, crawled


#graph, crawled = crawl('http://www.sjtu.edu.cn', 'dfs', 10)
graph, crawled = crawl('http://www.sjtu.edu.cn/', 'bfs', 20)
print graph

