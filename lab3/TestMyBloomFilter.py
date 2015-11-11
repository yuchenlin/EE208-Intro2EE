# -*- coding: utf8 -*-



#mbf = MyBloomFilter(32000,8)

f = open('gre.txt','r')
words = set()
minl = 3
maxl = 17
for line in f.xreadlines(): words.add(line.strip())
f.close()

# print len(words) #7513
# print minl #3
# print maxl #17 


# 开始测试


import random
import string


from MyBloomFilter import MyBloomFilter


n = len(words)
m = 32000
k = 3
mbf = MyBloomFilter(m,k) # k: (m/n)ln(2)   

for w in words: mbf.add(w)

falseCount = 0
amount = 100000

# for i in range(amount):
#     ranLen = random.randint(minl,maxl+1)
#     strr = string.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], ranLen)).replace(' ','')
#     if((strr not in words) and (mbf.lookup(strr))):
#         falseCount += 1



import time
from multiprocessing import Pool
from multiprocessing.dummy import Pool as TPool

def work(i):
    global mbf
    ranLen = random.randint(minl,maxl+1)
    strr = string.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], ranLen)).replace(' ','')
    return (strr not in words) and (mbf.lookup(strr))

start = time.time()

p = TPool(13)#设置线程池
res = p.map(work,range(1,amount))
p.close()
p.join()

falseCount = sum(res)
print 'falseCount = ',falseCount
print 'amount = ',amount
print 'The Rate is',falseCount/(amount+0.0)
print 'using ',time.time() -  start ,'s'
