import cv2 
import numpy as np

img1 = cv2.imread('target.jpg')
img2 = cv2.imread('tar.jpg')

rows1 = img1.shape[0]
cols1 = img1.shape[1]
rows2 = img2.shape[0]
cols2 = img2.shape[1]
out = np.zeros( (max([rows1,rows2]),cols1+cols2,3),  dtype='uint8')

# Place the first image to the left
out[:rows1,:cols1,:] = np.dstack([img1])

# Place the next image to the right of it
out[:rows2,cols1:cols1+cols2,:] = np.dstack([img2])

cv2.circle(out, (135,390 ), 1, (255, 0, 0), 1)

