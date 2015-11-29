#coding=utf-8
import numpy as np
import cv2 
import cv
import math

#flag =0 Return a grayscale image.
img1_gray = cv2.imread('img1.png',0) 
img2_gray = cv2.imread('img2.png',0) 
img3_gray = cv2.imread('img3.png',0) 
img4_gray = cv2.imread('img4.png',0) 
img1_rgb = cv2.imread('img1.png',1) 
img2_rgb = cv2.imread('img2.png',1)


def calcAndDrawHist_1(hist,colorToShow):
	
	minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(hist)
	histImg = np.zeros([256,256,3], np.uint8)
	hpt = int(0.9*256)
	for h in range(256):    
	    intensity = int(hist[h]*hpt/maxVal)    
	    cv2.line(histImg,(h,256), (h,256-intensity), colorToShow) 

	cv2.imshow("histGray-img",histImg)
	cv2.waitKey(0)



def CreatHist():

	histGray_1 = cv2.calcHist([img1_gray],[0],None,[256],[0.0,255.0])
	histGray_2 = cv2.calcHist([img2_gray],[0],None,[256],[0.0,255.0])
	# calcAndDrawHist_1(histGray_1,[100,100,100])
	# calcAndDrawHist_1(histGray_2,[100,100,100])
	b1,g1,r1 = cv2.split(img1_rgb)

	histColor_1_r = cv2.calcHist([b1],[0],None,[256],[0.0,255.0])
	histColor_1_g = cv2.calcHist([g1],[0],None,[256],[0.0,255.0])
	histColor_1_b = cv2.calcHist([r1],[0],None,[256],[0.0,255.0])
	calcAndDrawHist_1(histColor_1_r,[255, 0, 0])
	calcAndDrawHist_1(histColor_1_g,[0, 255, 0])
	calcAndDrawHist_1(histColor_1_b,[0, 0, 255])

def CalcEnery():
	img1_rgb = cv2.imread('img1.png',1)  #读入图像
	b,g,r = cv2.split(img1_rgb)	#分散三种颜色，注意顺序
	#分别计算三种颜色的能量
	energy_b = np.sum(b) 
	energy_g = np.sum(g)
	energy_r = np.sum(r)
	energy_all  = energy_b + energy_g + energy_r #计算总能量
	#输出三个能量的比例
	print (energy_b+0.0) / energy_all
	print (energy_g+0.0) / energy_all
	print (energy_r+0.0) / energy_all

def CalcGray():
	#以灰度的形式读入
	img2_gray = cv2.imread('img2.png',0) 
	#生成灰度表格，注意最大值最小值的范围
	histGray_2 = cv2.calcHist([img2_gray],[0],None,[256],[0.0,256.0])
	#用list 来处理更好的输出格式
	h_list = []
	for h in histGray_2:h_list.append(h[0])
	#求出所有灰度所含像素点数目之后，当然也可以直接利用图片的长宽乘积
	h_sum = sum(h_list)
	#输出每个灰度所占的比例
	for i in h_list:
		print (i+0.0)/h_sum
def CalcGridient(): 

	#创建算子向量 ：

	#mx ： 对每个元素的左面一个乘以-1，自己乘以0，右边乘以1 然后相加
	#my ： 对每个元素的上面一个乘以-1，自己乘以0，下面乘以1 然后相加
	mx = np.array([[-1, 0, 1]]) 
	my = np.array([[-1, 0, 1]]).T #转置

	#读入灰度图片，并且将其转成一个 numpy 对象，从而可以更好的计算
	img1_gray = cv2.imread('img1.png',0) 
	im = np.array(img1_gray).astype(np.uint8)

	#分别计算x 方向， y 方向的梯度
	gx = cv2.filter2D(im, cv2.CV_32F, mx)
	gy = cv2.filter2D(im, cv2.CV_32F, my)

	#存储梯度强度
	M = [0]*360
	
	#二维遍历所有的像素点，计算他们的梯度强度
	for x in range(1,gx.shape[0]):
		for y in range(1,gx.shape[1]):
			#计数
			M[math.trunc( math.sqrt((gx[x][y]**2+gy[x][y]**2)) ) ]+=1;

	#输出所有的灰度强度分布
	s = sum(M)
	for m in M:	print (m+0.0)/s
	

	# print gx.shape
	# # print gx.dtype

	# print '-----'
	# print im
	# print '-----'
	# print gx
	# print '-----'
	# print gy
