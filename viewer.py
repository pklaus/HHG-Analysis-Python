#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This command line tool can display 16bit TIFF images.
Their contrast is streched and the viewer includes a zoom window.

It is similar to OpenCV's example file browse.py_ .

.. _browse.py: http://code.opencv.org/projects/opencv/repository/entry/trunk/opencv/samples/python2/browse.py
"""

import numpy as np
import cv2
import sys
import Tkinter # for Tkinter.Tk().winfo_screenwidth()
from geometry import coordinates, rectangle
from tiff import TIFF

def main():
    """ Displayes the image file given as first parameter on the command line. """
    if len(sys.argv) > 1:
        fn = sys.argv[1]
        print 'loading %s ...' % fn
        img = TIFF(fn)
        bit = img.depth
    else:
        print __doc__
        print 'USAGE: %s [image filename]\n' % sys.argv[0]
        sys.exit(1)

    print("Minimum and maximum pixel values in the image: Min: %d Max: %d" % img.minmax)
    print("Rescaling to fill full 16bit space.")

    img.data = img.rescale()

    # determine screen size (see http://stackoverflow.com/a/3949983/183995 )
    root = Tkinter.Tk()
    screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
    small = img
    while small.dimensions[0] > screen_height or small.dimensions[1] > screen_width:
        small.scale_down_to_half()

    def onmouse(event, x, y, flags, param):
        h, w = img.dimensions
        hs, ws = small.dimensions
        x, y = int(1.0*x*h/hs), int(1.0*y*h/hs)
        show_zoom(x,y)

    zoom_window_size = 466
    zoom_factor = 3
    zoom = np.zeros((zoom_window_size, zoom_window_size),img.data.dtype)
    def show_zoom(x,y):
        h, w = img.dimensions
        img_box = rectangle()
        img_box.pos = coordinates(0,0)
        img_box.dim = coordinates(w,h)
        box = img_box.get_rectangle_inside(zoom_window_size/zoom_factor, coordinates(x,y))
        f, t = box.corners()
        #zoom = cv2.getRectSubPix(img, (800, 600), (x+0.5, y+0.5))
        #cv2.GetSubRect(img, (60, 70, 32, 32))
        #zoom = cv2.getRectSubPix(img, (200, 200), (x, y))
        #zoom = img[f.y:t.y, f.x:t.x]
        ## http://docs.opencv.org/modules/imgproc/doc/geometric_transformations.html#resize
        cv2.resize(img.data[f.y:t.y, f.x:t.x], dsize=(zoom_window_size,zoom_window_size), dst=zoom, interpolation=cv2.INTER_NEAREST)
        cv2.imshow('Detail', zoom)
    cv2.namedWindow("Detail")
    cv2.moveWindow("Detail", 5, 50+small.dimensions[0])
    cv2.imshow('Overview', small.data)
    cv2.moveWindow("Overview", 5, 20)
    show_zoom(0,0)
    cv2.setMouseCallback('Overview', onmouse)
    cv2.waitKey()

if __name__ == '__main__':
    main()
