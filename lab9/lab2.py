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
    return int(math.atan2(dy,dx)*180/math.pi+180)
#判断是否越界
def isValid(im,x,y):
    return (x>=16) and (x<=(im.shape[0]-16)) and
     (y>=16) and (y<=(im.shape[1]-16))

#计算主梯度方向
def getMainDirection(im,f):
    Hist = [0]*36
    fx = int(f[0]); fy=int(f[1]);
    R = 8
    for x in range(fx-R,fx+R+1):
        for y in range(fy-R,fy+R+1):
            if not isValid(im,x,y):
                continue
            Theta = getTheta(im,x,y)
            M = getIntension(im,x,y)
            ind = Theta/10
            if(ind==36): ind = 0;
            Hist[ind] += M 

    maxTheta = 0
    for ind in range(36):
        if(Hist[ind]>maxTheta):#比当前的主方向的强度大
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

def convertX(x,y,x0,sinDir,cosDir):
    return int(x * cosDir - y*sinDir + x0)

def convertY(x,y,y0,sinDir,cosDir):
    return int(x * sinDir + y*cosDir + y0)

def getSIFTVector(im,features):
    siftVec = []
    
    #定义存储单元
    Inten=[0]*16               # 存储梯度强度
    Theta=[0]*16               # 存储梯度方向
    for i in range(16):
        Inten[i]=[0]*16
        Theta[i]=[0]*16
    final={}                    #128维sift 向量

    for f in features:
        fx = int(f[0]); fy=int(f[1]);
        if(not isValid(im,fx,fy)):
            continue
        mainDirection = getMainDirection(im,f)
        dir = mainDirection*math.pi/180.0
        sinDir = math.sin(dir)
        cosDir = math.cos(dir)
        
        #坐标变换
        for x in range(-8,9):
            for y in range(-8,9):
                rx = convertX(x,y,fx,sinDir,cosDir)
                rx1 = convertX(x-1,y,fx,sinDir,cosDir)
                rx2 = convertX(x+1,y,fx,sinDir,cosDir)

                ry = convertY(x,y,fy,sinDir,cosDir)
                ry1 = convertY(x,y-1,fy,sinDir,cosDir)
                ry2 = convertY(x,y+1,fy,sinDir,cosDir)

                Inten[x][y] = math.hypot((im[rx1,ry]-im[rx2,ry]),
                                         (im[rx,ry1]-im[rx,ry2]))
                Theta[x][y] = math.atan2(im[rx1][ry]-im[rx2][ry],
                                        im[rx][ry1]-im[rx][ry2])
                                         + math.pi + dir


                while Theta[x][y] >= math.pi * 2:
                    Theta[x][y] -= math.pi * 2
                while Theta[x][y] < 0:
                    Theta[x][y] += 2*math.pi

        #计算描述子

        Hist=[]

        for i in range(-2,2):
            for j in range(-2,2):     
                tmpHist = [0]*8
                for m in range(4):
                    for n in range(4):
                        xx = i * 4 + m
                        yy = j * 4 + n
                        tmpHist[int(Theta[xx][yy]/(math.pi/4))] 
                            += Inten[xx][yy]
                
                Hist+=tmpHist

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
    x = int(ori.shape[0]*scale)
    y = int(ori.shape[1]*scale)
    return cv2.resize(ori,(x,y))



def getSIFTbyURL(url,scale=1,mainDirection=0):
    filename = url
    img = cv2.imread(filename,0)
    if(scale!=1):
        img = getResizedImg(img,scale)

    #获得特征点
    goodFeatureTemp = cv2.goodFeaturesToTrack(img,100,0.01,5)
    goodFeatures = []
    #转换格式为 list
    for gf in goodFeatureTemp:
        goodFeatures.append((int(gf[0][0]),int(gf[0][1])))
    vector = getSIFTVector(img,goodFeatures)

    print goodFeatures
    return vector,goodFeatures

def main():
    url1 = 'target.jpg'
    url2 = 'dataset/5.jpg'

    v_tar,f_t = getSIFTbyURL(url1)
    v_i,f_i  = getSIFTbyURL(url2) 

    res_t = []
    res_i = []

    for t,vt in enumerate(v_tar): 
        for i,vi in enumerate(v_i): 
            s = 0
            for ind in range(128):
                s += vt[ind]*vi[ind]
            if(s>0.77):
                res_t.append(f_t[t])
                res_i.append(f_i[i])  

    img1 = cv2.imread(url1)
    img2 = cv2.imread(url2)
    drawMatches(img1,res_t,img2,res_i)
    print res_t
    print res_i

def drawMatches(img1, kp1, img2, kp2): 
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]
    out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')
    out[:rows1,:cols1,:] = np.dstack([img1])
    out[:rows2,cols1:cols1+cols2,:] = np.dstack([img2])

    for i in range(len(kp1)): 
        (x1,y1) = kp1[i]
        (x2,y2) = kp2[i]  
        import random
        b=random.randint(0,255)
        g=random.randint(0,255)
        r=random.randint(0,255)
        color = (b,g,r)
        cv2.circle(out, (int(x1),int(y1)), 4, color, 1)   
        cv2.circle(out, (int(x2)+cols1,int(y2)), 4, color, 1)
        cv2.line(out, (int(x1),int(y1)), 
                        (int(x2)+cols1,int(y2)), color, 1)
    cv2.imshow('Matched Features', out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

main()