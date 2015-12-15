import cv2
import numpy as np
from matplotlib import pyplot as plt

url2 = 'dataset/1.jpg'
def drawMatches(img1, kp1, img2, kp2, matches):
    global url2
    

    # Create a new output image that concatenates the two images together
    # (a.k.a) a montage
    img1 = cv2.imread('target.jpg', 1)
    img2 = cv2.imread(url2, 1)
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    out = np.zeros((max([rows1, rows2]), cols1 + cols2, 3), dtype='uint8')

    # Place the first image to the left
    out[:rows1, :cols1, :] = np.dstack([img1])

    # Place the next image to the right of it
    out[:rows2, cols1:cols1 + cols2, :] = np.dstack([img2])

    # For each pair of points we have between both images
    # draw circles, then connect a line between them
    for mat in matches:

        # Get the matching keypoints for each of the images
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        # x - columns
        # y - rows
        (x1, y1) = kp1[img1_idx].pt
        (x2, y2) = kp2[img2_idx].pt

        # Draw a small circle at both co-ordinates
        # radius 4
        # colour blue
        # thickness = 1
        import random
        b=random.randint(0,255)
        g=random.randint(0,255)
        r=random.randint(0,255)
        color = (b,g,r)
        cv2.circle(out, (int(x1),int(y1)), 4, color, 1)   
        cv2.circle(out, (int(x2)+cols1,int(y2)), 4, color, 1)
        cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), color, 1)

        # cv2.circle(out, (int(x1), int(y1)), 4, (255, 0, 0), 1)
        # cv2.circle(out, (int(x2) + cols1, int(y2)), 4, (255, 0, 0), 1)

        # # Draw a line in between the two points
        # # thickness = 1
        # # colour blue
        # cv2.line(out, (int(x1), int(y1)), (int(x2) + cols1, int(y2)),
        #          (255, 0, 0), 1)
    # Show the image
    cv2.namedWindow('Matched Features', cv2.WINDOW_NORMAL)
    cv2.imshow('Matched Features', out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # return output



img1 = cv2.imread('target.jpg', 0)  # queryImage
img2 = cv2.imread(url2, 0)   # trainImage
print 1
# Initiate SIFT detector
orb = cv2.ORB()

print 2
# find the keypoints and descriptors with SIFT
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)
print 3
# create BFMatcher object
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
print 4
# Match descriptors.
matches = bf.match(des1, des2)
print 5
# Sort them in the order of their distance.
matches = sorted(matches, key=lambda x: x.distance)
print 6
# Draw first 10 matches.
print 7
img3 = drawMatches(img1, kp1, img2, kp2, matches[:30])
# plt.imshow(img3), plt.show()