# -*- coding: utf8 -*-


#处理gre_e_c.txt 把中文都撤去

f = open('gre_e_c.txt','r')
isEnglish = True
f_wr = open('gre.txt','w')
for line in f.xreadlines():
    if(isEnglish):
        f_wr.write(line)
    isEnglish = not isEnglish

f.close()
f_wr.close()