#coding=utf8

import cv2
import numpy as np
import sys

filename = 'dataset/3.jpg'
img = cv2.imread(filename,0)

goodFeatures = cv2.goodFeaturesToTrack(img,100,0.01,5)

print goodFeatures[0][0]


