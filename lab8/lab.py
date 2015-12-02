#coding=utf8
import cv2
import numpy as np
import math
import sys
sys.setrecursionlimit(1000000)

PI = math.pi
#C is center point, sita is the angel
def GetPoint(C,sita):
	st = abs(sita)
	i,j = C
	if(st<=PI/4):
		d = 1*math.tan(st)
		if(sita>0):
			j = j-1
			i = i-d
		else:
			j = j-1
			i = i+d
	elif(st>PI/4 and st<PI/2):
		d = 1/math.tan(st)
		if(sita>0):
			i = i-1
			j = j-d
		else:
			i = i+1
			j = j-d
	else:#st == PI/2
		if(sita>0):
			i = i-1
		else:
			i = i+1
	return (i,j)

#P is Point , M is Matrix
def isInteger(num):
	return math.trunc(num)==num
def InsertValue(P,M): 
	x,y = P
	if(isInteger(x) and isInteger(y)):
		return M[x][y]
	elif(isInteger(x) and not isInteger(y)):
		y1 = math.trunc(y)
		y2 = y1+1
		dy = y-y1
		return M[x][y1]*dy + M[x][y2]*(1-dy)
	else:
		x1 = math.trunc(x)
		x2 = x1+1
		dx = x-x1
		return M[x1][y]*dx + M[x2][y]*(1-dx)


def MyCanny(url,l1=0.79,l2=0.5):
	#read the image in gray channel
	img = cv2.imread(url,0)
	print img.shape
	#blur: why sigma = 0 ?
	img = cv2.GaussianBlur(img,(3,3),0)
	#Canny preparation
	# sx = np.array([[-1,1],[-1,1]])
	# sy = np.array([[1,1],[-1,-1]])
	# P = cv2.filter2D(img,cv2.CV_32F,sx,anchor=(0,0))/2
	# Q = cv2.filter2D(img,cv2.CV_32F,sy,anchor=(0,0))/2
	# M = np.sqrt(P*P+Q*Q)
	
	# print img
	# print P
	# print Q
	#Sobel operator 
	dx = cv2.Sobel(img,cv2.CV_16S,1,0)  
	dy = cv2.Sobel(img,cv2.CV_16S,0,1)  
	P = cv2.convertScaleAbs(dx)   # convert 2 uint8  
	Q = cv2.convertScaleAbs(dy)   
	M = cv2.addWeighted(P,0.5,Q,0.5,0)  
	


	N = np.zeros(M.shape)
	Sita = np.zeros(img.shape)
	
	for x in range(1,img.shape[0]-1):
		for y in range(1,img.shape[1]-1):
			Sita[x][y] = math.atan2(Q[x][y],P[x][y])
			# if(P[x][y] == 0):
			# 	Sita[x][y] = np.sign(Q[x][y]) * PI/2
			# else:
			# 	Sita[x][y] = math.atan(Q[x][y]/P[x][y])

	#surpress the non-extreme-value
	import time
	start = time.time()
	for x in range(1,img.shape[0]-1):
		for y in range(1,img.shape[1]-1):
			if(M[x][y]==0):
				N[x][y]=0
				continue
			dtmp1 = GetPoint((x,y),Sita[x][y])
			dtmp2 = (2*x-dtmp1[0],2*y-dtmp1[1])
			if((M[x][y] < 0.85*InsertValue(dtmp1,M)) or (M[x][y] < 0.85*InsertValue(dtmp2,M))):
				N[x][y] = 0 
			else:
				N[x][y] = 110 # (x,y) is a possible edge point
	print time.time() - start
	#calc the hist of the M
	histM = [0]*370 #because the maximum of M is 360*1.414
	for x in range(1,img.shape[0]-1):
		for y in range(1,img.shape[1]-1):
			if(N[x][y]==110):
				#histM only records the points which has not been suppressed
				histM[int(np.trunc(M[x][y]))]+=1
	# print histM
	edgeNum = sum(histM) #The number of the possible edge points
	maxM = 0
	for i in range(370):
		if(histM[i]>0):
			maxM = i
	#get the two thresold values  l1 l2

	highCount = int(l1 * edgeNum+0.5)
	highThresold = 1
	iterNum = histM[1]
	while (iterNum < highCount):
		highThresold += 1
		iterNum += histM[highThresold]

	lowThresold = int(highThresold * l2 + 0.5)

	print highThresold,lowThresold
	#highThresold=150;lowThresold=50;
	#print highThresold,lowThresold
	#detect the edges
	res = np.zeros(img.shape)

	for x in range(img.shape[0]):
		for y in range(img.shape[1]):
			if((N[x][y]==110) and (M[x][y]>=highThresold)):
				N[x][y] = 255 #white
				Trace(x,y,lowThresold,N,M)

	#clear 110
	for x in range(img.shape[0]):
		for y in range(img.shape[1]):
			if(N[x][y]!=255):
				N[x][y] = 0 #black
	print 'ok'
	cv2.imshow("MyCannyWithSobel-2",N)
	cv2.waitKey(0)

def Trace(ori_x,ori_y,lowThresold,res,MM):
	dx = [1,1,0,-1,-1,-1,0,1]
	dy = [0,1,1,1,0,-1,-1,-1]
	for i in range(8):
		x = ori_x+dx[i]
		y = ori_y+dy[i]
		if(res[x][y]==110 and MM[x][y]>=lowThresold):
			res[x][y]=255
			Trace(x,y,lowThresold,res,MM)

	
MyCanny('dataset/2.jpg',0.77,0.5)
# MyCanny('dataset/1.jpg',0.71,0.33)
# MyCanny('dataset/3.jpg',0.71,0.33)
