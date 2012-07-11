#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module can find overflow areas in images (“blobs”).
It makes heavy use of OpenCV.
"""

# http://code.opencv.org/svn/opencv/trunk/opencv/samples/python2/contours.py
# http://code.opencv.org/svn/opencv/trunk/opencv/samples/python2/squares.py

import numpy as np
import cv2
import cv2.cv as cv

from tiff import TIFF

def find_blobs(img_data, verbose=False, min_area=None):
    """ Find second level contours in 16bit images

    Here is an example to illustrate the contours of the blob this function can find:

    .. image:: _static/blobs-contours.png"""
    blobs = []
    copy_data = img_data.copy()
    if img_data.dtype == 'uint16':
        if verbose: print("16 bit image found. Scaling down to 8bit.")
        copy_data = (copy_data/2.**8).astype(np.uint8)
    retval, copy_data = cv2.threshold(copy_data, 140, 255, cv2.THRESH_BINARY)
    #cv2.imshow('threshold applied',copy_data)
    contours, hierarchy = cv2.findContours(copy_data, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE, )
    ## select only second level contours:
    toplevel_indices, secondlevel_contours = [],[]
    if hierarchy == None:
        if verbose: print("Finished finding no second level contours.")
        return []
    h = hierarchy[0]
    for i in range(len(h)):
        if h[i][3] == -1:
            toplevel_indices.append(i)
    for i in range(len(h)):
        if h[i][3] in toplevel_indices:
            if verbose: print("Found a second level contour. Starting at: %s." % contours[i][0])
            if min_area != None:
                if cv2.contourArea(contours[i]) >= min_area:
                    secondlevel_contours.append(contours[i])
            else:
                secondlevel_contours.append(contours[i])
    if verbose: print("Finished finding second level contours.")
    ## sort contours by largest first (if there are more than one)
    blobs = sorted(secondlevel_contours, key=lambda contour:cv2.contourArea(contour), reverse=True)
    return blobs

def fix_image(img, blobs):
    """
    This function can fix images where blobs have been found using :py:func:`find_blobs`.

    Here is an example of what this does:

    .. image:: _static/blob-fix.png"""
    ## blobs_img holds 0 for good pixels and 1 for pixels where an overflow occured
    blobs_img = np.zeros(img.dimensions, img.data.dtype)
    cv2.drawContours( blobs_img, blobs, -1, 1, -1) # fill contour
    cv2.drawContours( blobs_img, blobs, -1, 0, 1) # exclude line
    ## cropped_blobs cuts the pixels where an overflow occured out of the original image
    cropped_blobs = blobs_img * img.data
    ## return an image with values rescaled to half its original value and the blob areas lifted up by 2^(depth-1)
    return ((img.data-cropped_blobs)*.5 + blobs_img*img.data*.5+blobs_img*2**(img.depth-1)).astype(img.data.dtype)


def main():
    """ This function is a demonstration of how this module is being used.
    It is implemented as a command line tool. Run this module file to see how it works.

    It can serve for unit tests too.
    """
    import sys
    if len(sys.argv) > 1:
        img_files = sys.argv[1:]
    else:
        print('This tool shows how to find overflows in measurement files.')
        print('USAGE: %s [image filename] [another image filename...]\n' % sys.argv[0])
        sys.exit(1)

    for img_file in img_files:
        print('Loading %s ...' % img_file)
        img = TIFF(img_file)

        #if img.data.dtype == 'uint16' and img.data.flatten().max() < 2.**8-1:
        #    print("Found 16 bit image with values < 2^8-1\nStrange... Interpreting as 8bit image.")
        #    img.data = img.data.astype(np.uint8)

        cv2.imshow('Original Image', img.data)

        blobs = find_blobs(img.data, verbose=True, min_area=3)

        # Draw a coloured line where contours have been found:
        #h,w = img.dimensions
        #vis = np.zeros((h, w, 3), np.uint8)
        #cv2.drawContours( vis, blobs, -1, (128,255,255), 1, cv2.CV_AA)
        #cv2.imshow('contours', vis)

        cv2.imshow('Fixed Image', fix_image(img, blobs))

        ## Convert to color image
        #img.data = cv2.cvtColor( img.data, cv.CV_GRAY2BGR )
        #cv2.drawContours( img.data, blobs, -1, (255,0,0), 1)
        #cv2.imshow('blobs', img.data)

        ch = 0xFF & cv2.waitKey()
        if ch == 27:
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
