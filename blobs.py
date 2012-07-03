#!/usr/bin/env python

# http://code.opencv.org/svn/opencv/trunk/opencv/samples/python2/contours.py
# http://code.opencv.org/svn/opencv/trunk/opencv/samples/python2/squares.py

import numpy as np
import cv2
import cv2.cv as cv

from tiff import TIFF16bit

def find_blobs(img):
    blobs = []
    temp = img.copy()
    temp = temp/2.**8
    temp = img.astype(np.uint8)
    retval, temp = cv2.threshold(temp, 140, 255, cv2.THRESH_BINARY)
    cv2.imshow('8bit',temp)
    contours, hierarchy = cv2.findContours(temp, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE, )
    ## select only second level contours:
    toplevel_indices, secondlevel_contours = [],[]
    if hierarchy == None:
        return []
    h = hierarchy[0]
    for i in range(len(h)):
        if h[i][3] == -1:
            toplevel_indices.append(i)
    for i in range(len(h)):
        if h[i][3] in toplevel_indices:
            print contours[i][0]
            secondlevel_contours.append(contours[i])
    ## sort contours by largest first (if there are more than one)
    blobs = sorted(secondlevel_contours, key=lambda contour:cv2.contourArea(contour), reverse=True)
    return blobs

if __name__ == '__main__':
    from glob import glob
    for fn in glob('HHG*.png'):
        img = TIFF16bit(fn)
        cv2.imshow('orig', img.img)
        h,w = img.dimensions
        blobs = find_blobs(img.img)

        vis = np.zeros((h, w, 3), np.uint8)
        cv2.drawContours( vis, blobs, -1, (128,255,255), 1, cv2.CV_AA)
        cv2.imshow('contours', vis)

        img = cv2.cvtColor( img.img, cv.CV_GRAY2BGR )
        cv2.drawContours( img, blobs, -1, (128,255,255), 1, cv2.CV_AA)

        cv2.imshow('blobs', img)
        ch = 0xFF & cv2.waitKey()
        if ch == 27:
            break
    cv2.destroyAllWindows()

