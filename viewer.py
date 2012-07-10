#!/usr/bin/env python
''' browse.py - Sample shows how to implement a simple hi resolution image navigation '''

import numpy as np
import cv2
import sys

from geometry import coordinates, rectangle
from tiff import TIFF

import Tkinter # for Tkinter.Tk().winfo_screenwidth()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fn = sys.argv[1]
        print 'loading %s ...' % fn
        img = TIFF(fn)
        bit = img.depth
    else:
        print 'This sample shows how to implement a simple hi resolution image navigation.'
        print 'USAGE: browse.py [image filename]\n'

        sz = 4096
        bit = 8
        print 'generating %dx%d procedural image ...' % (sz, sz)
        img_data = np.zeros((sz, sz), np.uint8)
        track = np.cumsum(np.random.rand(500000, 2)-0.5, axis=0)
        track = np.int32(track*10 + (sz/2, sz/2))
        cv2.polylines(img_data, [track], 0, 255, 1, cv2.CV_AA)

    print("Minimum and maximum pixel values in the image: Min: %d Max: %d" % img.minmax())
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
