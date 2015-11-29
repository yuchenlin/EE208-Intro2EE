# ref: http://blog.csdn.net/likezhaobin/article/details/6892629

import cv2  
import numpy as np    
  
img = cv2.imread("dataset/1.jpg", 0) 
  
img = cv2.GaussianBlur(img,(3,3),0)

canny = cv2.Canny(img, 50, 150)  
  
cv2.imshow('OpenCV\'s Canny', canny)  
cv2.waitKey(0)  
cv2.destroyAllWindows()  
