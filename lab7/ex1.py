import numpy as np
import cv2 
import cv
import math

img = cv2.imread('img1.png')

cv2.namedWindow('Image')
cv2.imshow('Image',img)
cv2.waitKey(0)
cv2.destoryAllWindows()