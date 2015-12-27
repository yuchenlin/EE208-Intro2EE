#coding=utf8
import cv2
import numpy as np

#计算img的RGB能量比例
def CalcRGB(img):
	b,g,r = cv2.split(img)	#分散三种颜色，注意顺序
	#分别计算三种颜色的能量
	energy_b = np.sum(b) 
	energy_g = np.sum(g)
	energy_r = np.sum(r)
	energy_all  = energy_b + energy_g + energy_r #计算总能量
	#输出三个能量的比例
	res = [0.0,0.0,0.0]
	res[0] = (energy_b+0.0) / energy_all
	res[1] = (energy_g+0.0) / energy_all
	res[2] = (energy_r+0.0) / energy_all
	return res

#计算一个图片的特征向量
def CalcP(imgurl):
	P = []
	img = cv2.imread(imgurl,1)  #读入图像
	h = img.shape[0]
	w = img.shape[1]  
	P += CalcRGB(img[0:h/2,0:w/2])
	P += CalcRGB(img[h/2:h,0:w/2])
	P += CalcRGB(img[0:h/2,w/2:w])
	P += CalcRGB(img[h/2:h,w/2:w])

	#为了使 0 1 2 分布均匀测试得到的比例
	low = 0.32
	high = 0.35

	for i,p in enumerate(P):
		P[i] = 0
		if(p>low and p<high):
			P[i] = 1
		elif(p>=high):
			P[i] = 2
	return P

#p 是一个特征向量 
#Sub 是一个需要映射的位置的集合 比如 [1,7,10,15,20]
def CalcLSH(p,Sub):
	#制备12个空集合的集合
	I = [[] for i in range(12)]

	for i in Sub:	#对每个元素进行分类
		I[(i-1)/2].append(i)

	lsh = []
	
	#I[ind] 即是 PPT 中的 I|ind 这个集合
	for ind in range(12):
		if(len(I[ind])==0):
			continue
		for i in I[ind]:
			lsh.append(0+(i-2*ind<=p[ind]))

	return lsh

#Sub 是固定选取的子集
def PreProcessing(Sub):
	#files 是图片库
	#allHash 所有图片库里图片的 lsh 值组成的集合
	#allHashFileID[ind] 存储了所有的以 allHash[ind]为 lsh 值的图片的坐标
	#allP 是所有图片的特征向量集合
	import os
	files = os.listdir('Dataset')
	allHash = []
	allHashFileID = []
	allP = []

	for i in range(len(files)):
		imgurl = 'Dataset/' + files[i]
		p = CalcP(imgurl)
		allP.append(p)
		lsh = CalcLSH(p,Sub)

		if(lsh in allHash):
			allHashFileID[allHash.index(lsh)].append(i)
		else:
			allHash.append(lsh)
			allHashFileID.append([i])

	return files,allHash,allHashFileID,allP

#归一化
def Normalize(vec):
	res = [0.0]*12
	s = 0
	for i in vec:
		s += i**2
	s = s**0.5
	if(s>0):
		for i in range(12):
			res[i] = float(vec[i]) / s
	return res

#计算两个向量的余弦相似度 余弦值越大 夹角越小 相似度越大
def CalcSimilarity(A,B):
	A = Normalize(A)
	B = Normalize(B)
	res = 0.0
	for i in range(12):
		res += A[i]*B[i]
	return res

#利用 LSH 来进行搜索
#imgurl 是要查询的图片的链接
#files 是图片库
#allHash 所有图片库里图片的 lsh 值组成的集合
#allHashFileID[ind] 存储了所有的以 allHash[ind]为 lsh 值的图片的坐标
#allP 是所有图片的特征向量集合
#Sub 是固定选取的子集
def Search_LSH(imgurl,files,allHash,allHashFileID,allP,Sub):
	res = []
	p = CalcP(imgurl)
	lsh = CalcLSH(p,Sub)
	if lsh not in allHash:
		return res #如果不存在可能的图片就直接返回空集
	ind = allHash.index(lsh)#返回第一次出现lsh的坐标

	for i in allHashFileID[ind]:#所有的可能的图片
		res.append((files[i], CalcSimilarity(p,allP[i])))
	res.sort(lambda x,y:cmp(x[1],y[1]),reverse=True)
	return res

#暴力搜索
def Search_NN(imgurl,Sub,allP):
	res = []
	p = CalcP(imgurl)
	import os
	files = os.listdir('Dataset')
	for i in range(len(files)):
		imgurl = 'Dataset/' + files[i]
		res.append((files[i],CalcSimilarity(p,allP[i])))
	res.sort(lambda x,y:cmp(x[1],y[1]),reverse=True)
	return res

#print MyCalcP('target.jpg')
# for i in range(1,31):
# 	#print str(i)+'.jpg:\t',
# 	print MyCalcP('Dataset/%d.jpg'%i)

def main():
	imgurl = 'target.jpg'
	Sub = [2,4,9,11,13,21]
	import time 
	
	
	
	files,allHash,allHashFileID,allP = PreProcessing(Sub)

	print 'Search_LSH Result:'
	start = time.time()
	res = Search_LSH(imgurl, files, allHash, allHashFileID, allP, Sub)
	for i in res[0:min(5,len(res))]:
		print i
	print 'time cost: ' , time.time()-start
	
	print 

	print 'Search_NN Result:'
	start = time.time()
	res = Search_NN(imgurl,Sub,allP)
	for i in res[0:min(10,len(res))]:
		print i
	print 'time cost: ' , time.time()-start


main()



