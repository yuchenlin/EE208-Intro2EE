from bs4 import BeautifulSoup
import jieba
import codecs
from datetime import datetime
import sys
import os
reload(sys)
sys.setdefaultencoding("utf-8")


def clean_html(html):
    import re,string
    text = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())      
    text = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", text)   
    text = re.sub(r"(?s)<.*?>", "", text)       
    text = re.sub(r"&.*?;", "", text)
    return text

def exe(filename):
    if(os.path.exists('ori_txt/'+filename+'.txt')):
        print filename,'exists'
        return
    f = open('html/'+filename)
    bs = BeautifulSoup(f.read(),"html.parser")
    f.close()
    ori_text = clean_html(bs.get_text())
    ori_text = " ".join(jieba.cut(ori_text))
    f = open('ori_txt/'+filename+'.txt','w')
    f.write(ori_text)
    f.close()
    print filename,'is ok'

f = codecs.open('infoIndex.txt','r',encoding='utf-8')
filenames = []
for line in f.xreadlines():
    ls = line.split()
    filenames.append(ls[0])
f.close()
from multiprocessing import Pool
from multiprocessing.dummy import Pool as TPool
p = TPool(30)
start = datetime.now()
p.map(exe,filenames)
p.close()
p.join()
print datetime.now()-start