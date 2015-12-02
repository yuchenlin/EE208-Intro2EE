import cv2
import numpy as np
import math
import codecs
import time

def init_and_graylize(filename):
	img = cv2.imread(filename, 0)
	return img

def gauss_filter(img):
	return cv2.GaussianBlur(img, (3,3), 0)

def my_canny(img, thrLow, thrHigh):
	imgShape = img.shape
	st = time.clock()
	P = cv2.convertScaleAbs( cv2.Sobel(img, cv2.CV_16S, 1, 0) )
	Q = cv2.convertScaleAbs( cv2.Sobel(img, cv2.CV_16S, 0, 1) )
	M = cv2.addWeighted(P, 0.5, Q, 0.5, 0)
	ed = time.clock()
	print 'CALC PQM: ', ed-st
	st = time.clock()
	Theta = np.zeros(imgShape)
	for h in range(0, imgShape[0]):
		for w in range(0, imgShape[1]):
			Theta[h][w] = math.atan2(Q[h][w], P[h][w]) / math.pi * 180
	ed = time.clock()
	print 'CALC THETA: ', ed-st

	R = np.zeros(imgShape)
	st = time.clock()
	for h in range(1, imgShape[0]-1):
		for w in range(1, imgShape[1]-1):
			dTmp1 = 0
			dTmp2 = 0
			if M[h][w] == 0:
				R[h][w] = 0
			else:
				th = Theta[h][w]
				if (th >= 90 and th < 135
					or th >= 270 and th < 315):
					g1 = M[h-1][w-1]
					g2 = M[h-1][w]
					g3 = M[h+1][w]
					g4 = M[h+1][w+1]
					dW = 1 / math.tan(th / 180 * math.pi)
					dTmp1 = g1 * dW + g2 * (1 - dW)
					dTmp2 = g4 * dW + g3 * (1 - dW)

				elif ( (th >= 135) and (th < 180) 
					or (th >= 315) and (th < 360)):
					g1 = M[h-1][w-1]
					g2 = M[h][w-1]
					g3 = M[h][w+1]
					g4 = M[h+1][w+1]
					dW = math.tan(th / 180 * math.pi)
					dTmp1 = g2 * dW + g1 * (1 - dW)
					dTmp2 = g4 * dW + g3 * (1 - dW)

				elif ( (th >= 45) and (th < 90) 
					or (th >= 225) and (th < 270)):
					g1 = M[h-1][w]
					g2 = M[h-1][w+1]
					g3 = M[h+1][w]
					g4 = M[h+1][w-1]
					dW = 1 / math.tan(th / 180 * math.pi)
					dTmp1 = g2 * dW + g1 * (1 - dW)
					dTmp2 = g3 * dW + g4 * (1 - dW)

				elif ( (th >= 0) and (th < 45)
						or (th >= 180) and (th < 225)):
					g1 = M[h-1][w+1]
					g2 = M[h][w+1]
					g3 = M[h+1][w-1]
					g4 = M[h][w-1]
					dW = math.tan(th / 180 * math.pi)
					dTmp1 = g1 * dW + g2 * (1 - dW)
					dTmp2 = g3 * dW + g4 * (1 - dW)
			if ( M[h][w] >= dTmp1 and M[h][w] >= dTmp2):
				R[h][w] = 128
			else:
				R[h][w] = 0
	ed = time.clock()
	print 'MAXR: ', ed-st
	#255 must 1 might 0 cannot 
	st = time.clock()
	stack = []
	for h in range(0, imgShape[0]):
		for w in range(0, imgShape[1]):
			if ( R[h][w] == 128 and M[h][w] >= thrHigh):
				R[h][w] = 255
				stack.append((h,w))
			elif (R[h][w] == 128 and M[h][w] >= thrLow):
				R[h][w] = 1
			else:
				R[h][w] = 0

	dirW = [1,1,0,-1,-1,-1,0,1]
	dirH = [0,1,1,1,0,-1,-1,-1]
	isVisited = np.zeros(imgShape)
	while (len(stack)>0):
		h,w = stack.pop()
		for k in range(8):
			hh = h + dirH[k]
			ww = w + dirW[k]
			if (isVisited[hh][ww] == 0) and (R[hh][ww] == 1):
				stack.append((hh,ww))
				R[hh][ww] = 255
				isVisited[hh][ww] = 1
	ed = time.clock()
	print 'LINK: ', ed-st
	# for h in range(0, imgShape[0]):
	# 	for w in range(0, img.shape[1]):
	# 		if (R[h][w] == 0):
	# 			R[h,w] = 255
	# 		else:
	# 			R[h,w] = 0
	return R
start = time.clock()
img = init_and_graylize('dataset/2.jpg')
img = gauss_filter(img)
img = my_canny(img, 50, 100)
end = time.clock()
print end-start
cv2.imshow('image', img)
cv2.waitKey(0)