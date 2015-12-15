#coding=utf8

import cv2
import numpy as np
import sys
import math

#获取梯度强度
def getIntension(im,x,y):
    x = int(x); y = int(y);
    dx = int(im[x+1,y])-int(im[x-1,y])
    dy = int(im[x,y+1])-int(im[x,y-1])
    return math.hypot(dx,dy)
#获取梯度方向
def getTheta(im,x,y):
    x = int(x); y = int(y);
    dx = int(im[x+1,y])-int(im[x-1,y])
    dy = int(im[x,y+1])-int(im[x,y-1])
    return int(math.atan2(dy,dx)*180/math.pi)
#判断是否越界
def isValid(im,x,y):
    return (x>=1) and (x<=(im.shape[0]-3)) and (y>=1) and (y<=(im.shape[1]-3))

#计算主梯度方向
def getMainDirection(im,features):
    mainDirection = 0
    Hist = [0]*36
    R = 8
    for f in features:
        fx = int(f[0][0]); fy=int(f[0][1]);
        for x in range(fx-R,fx+R+1):
            for y in range(fy-R,fy+R+1):
                if not isValid(im,x,y):
                    continue
                Theta = getTheta(im,x,y)
                M = getIntension(im,x,y)
                ind = Theta/10
                if(ind==36): ind = 0;
                Hist[ind] += M 

    maxHist = maxTheta = 0
    for ind in range(36):
        if(Hist[ind]>maxHist):#比当前的主方向的强度大
            maxHist = Hist[ind]
            maxTheta = ind*10+5 #取中值代表主方向
    return maxTheta
#计算插值
def insertValue(im,x,y,dir):
    x0 = int(x); y0 = int(y);
    res =  (
           getTheta(im,x0,y0)     *(x0+1-x) *(y0+1-y) +
           getTheta(im,x0+1,y0)   *(x-x0)   *(y0+1-y) +
           getTheta(im,x0,y0+1)   *(x0+1-x) *(y-y0)   +
           getTheta(im,x0+1,y0+1) *(x-x0)   *(y-y0)  
           )
    res -= dir
    while res<0: res += 360;
    return res

#计算SIFT的向量

def getSIFTVector(im,mainDirection,features):
    siftVec = []

    return siftVec

def getSIFTVector_(im,mainDirection,features):
    siftVec = []
    dir = mainDirection/180.0*math.pi
    sinDir = math.sin(dir)
    cosDir = math.cos(dir)

    for f in features:
        fx = int(f[0][0]); fy=int(f[0][1]);
        x0 = fx + 8*sinDir
        y0 = fy - 8*cosDir

        x0 = x0 - 8*cosDir
        y0 = y0 - 8*sinDir
        #此时 x0,y0为物体坐标系的最左上角的点的坐标
        #计算描述子
        Hist = []
        #把16*16的区域 分成16个块 每个块4*4
        for i in range(4):
            x1 = x0 + 4*i*cosDir
            y1 = y0 + 4*i*sinDir
            #x1,y1为每个小块的左上角的点
            for j in range(4):
                x2 = x1 - 4*j*sinDir
                y2 = x1 + 4*j*cosDir

                tmpHist = [0]*8
                
                for m in range(4):
                    x3 = x2 + m*cosDir
                    y3 = y2 + m*sinDir

                    for k in range(4):
                        x4 = x3 - k*sinDir
                        y4 = y3 + k*cosDir

                        if(isValid(im,x4,y4)):
                            ind = int(insertValue(im,x4,y4,mainDirection)/45)
                            if ind == 8 : ind = 0

                            tmpHist[ind] += 1
                #累计
                Hist += tmpHist
        #对每个特征点

        sumValue = 0
        #128维向量描述子  

        for i in range(128):
            sumValue += Hist[i]**2
        sumValue = math.sqrt(sumValue)
        if(sumValue!=0):
            for x in range(128):
                Hist[x] /= float(sumValue)
        siftVec.append(Hist)

    return siftVec
def getResizedImg(ori,scale):
    x = int(round(ori.shape[0]*scale))
    y = int(round(ori.shape[1]*scale))
    return cv2.resize(ori,(x,y))
def getSIFTbyURL(url,scale=1):
    filename = url
    img = cv2.imread(filename,0)
    if(scale!=1):
        img = getResizedImg(img,scale)
    #获得角点       
    goodFeatures = cv2.goodFeaturesToTrack(img,100,0.01,5)
    #print goodFeatures[0][0]
    #把x,y 互换

    #求主方向
    mainDirection = getMainDirection(img,goodFeatures)
    vector = getSIFTVector(img,mainDirection,goodFeatures)

    return vector,goodFeatures

def main():
    url1 = 'target.jpg'
    url2 = 'target.jpg'
    v_tar,f_t = getSIFTbyURL(url1)
    v_i,f_i  = getSIFTbyURL(url2,1)
    k = 0
    chosen = [0]*len(v_i)
    res_t = []
    res_i = []
    for vt in v_tar:
        maxI = 0
        n = 0
        j = 0
        for vi in v_i:
            tmp = 0
            for i in range(128):
                tmp += vt[i]*vi[i]
            if tmp > maxI and chosen[j]==0:
                maxI = tmp
                n = j
            j+=1
        if(maxI>0.6):
            res_t.append(f_t[k])
            res_i.append(f_i[n])
            chosen[n]=1
        chosen[n] = 1
        k+=1
    img1 = cv2.imread(url1)
    img2 = cv2.imread(url2)
    drawMatches(img1,res_t,img2,res_i)

def drawMatches(img1, kp1, img2, kp2):
    # Create a new output image that concatenates the two images together
    # (a.k.a) a montage
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')

    # Place the first image to the left
    out[:rows1,:cols1,:] = np.dstack([img1])

    # Place the next image to the right of it
    out[:rows2,cols1:cols1+cols2,:] = np.dstack([img2])

    # For each pair of points we have between both images
    # draw circles, then connect a line between them
    for i in range(len(kp1)):

        # Get the matching keypoints for each of the images
        
        # x - columns
        # y - rows
        (x1,y1) = kp1[i][0]
        (x2,y2) = kp2[i][0]

        # Draw a small circle at both co-ordinates
        # radius 4
        # colour blue
        # thickness = 1
        print x1,y1
        print x2,y2
        print 
        cv2.circle(out, (int(x1),int(y1)), 4, (255, 0, 0), 1)   
        cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (255, 0, 0), 1)

        # Draw a line in between the two points
        # thickness = 1
        # colour blue
        cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255, 0, 0), 1)


    # Show the image
    cv2.imshow('Matched Features', out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


main()