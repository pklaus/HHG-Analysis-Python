#!/usr/bin/env python
''' browse.py - Sample shows how to implement a simple hi resolution image navigation '''

import numpy as np
import cv2
import sys

import Tkinter # for Tkinter.Tk().winfo_screenwidth()

def minmax(array):
    '''numpy.ndarray find min and max'''
    return (array.min(), array.max())

class coordinates(object):
    x = None
    y = None
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y
    def move(self, offset):
        self.x += offset.x
        self.y += offset.y
    def __add__(self, other):
        return coordinates(self.x+other.x, self.y+other.y)
class rectangle(object):
    pos = coordinates()
    dim = coordinates()
    def fully_in(self, other):
        if self.pos.x >= other.pos.x and \
           self.pos.y >= other.pos.y and \
           self.pos.x + self.dim.x <= other.pos.y + other.dim.x and \
           self.pos.y + self.dim.y <= other.pos.y + other.dim.y:
               return True
        return False
    def move(self, by):
        self.pos.move(by)
    def get_rectangle_inside(self, size, center):
        box = rectangle()
        box.pos.x = center.x - size/2
        box.pos.y = center.y - size/2
        box.dim.x, box.dim.y = size, size
        if  box.pos.x < self.pos.x:
            box.move(coordinates(self.pos.x - box.pos.x, 0))
        if  box.pos.y < self.pos.y:
            box.move(coordinates(0, self.pos.y - box.pos.y))
        if  box.pos.x + box.dim.x > self.pos.x + self.dim.x:
            box.move(coordinates(self.pos.x + self.dim.x - (box.pos.x + box.dim.x), 0))
        if  box.pos.y + box.dim.y > self.pos.y + self.dim.y:
            box.move(coordinates(0, self.pos.y + self.dim.y - (box.pos.y + box.dim.y)))
        if not box.fully_in(self):
            raise NameError("Box too big for me.")
        return box
    def corners(self):
        return (self.pos, self.pos+self.dim)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fn = sys.argv[1]
        print 'loading %s ...' % fn
        img = cv2.imread(fn,-1)
        bit = 16
    else:
        print 'This sample shows how to implement a simple hi resolution image navigation.'
        print 'USAGE: browse.py [image filename]\n'

        sz = 4096
        bit = 8
        print 'generating %dx%d procedural image ...' % (sz, sz)
        img = np.zeros((sz, sz), np.uint8)
        track = np.cumsum(np.random.rand(500000, 2)-0.5, axis=0)
        track = np.int32(track*10 + (sz/2, sz/2))
        cv2.polylines(img, [track], 0, 255, 1, cv2.CV_AA)

    min_v, max_v = minmax(img)
    print("Minimum and maximum pixel values in the image: Min: %d Max: %d" % (min_v, max_v))
    img = (img-min_v)*(2**bit/(max_v - min_v -1 ))

    # determine screen size (see http://stackoverflow.com/a/3949983/183995 )
    root = Tkinter.Tk()
    screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
    small = img
    while small.shape[0] > screen_height or small.shape[1] > screen_width:
        small = cv2.pyrDown(small)

    def onmouse(event, x, y, flags, param):
        h, w = img.shape[:2]
        hs, ws = small.shape[:2]
        x, y = int(1.0*x*h/hs), int(1.0*y*h/hs)
        show_zoom(x,y)

    zoom_size = 256
    zoom_factor = 3
    zoom = np.zeros((zoom_size*zoom_factor, zoom_size*zoom_factor),img.dtype)
    def show_zoom(x,y):
        h, w = img.shape[:2]
        img_box = rectangle()
        img_box.pos = coordinates(0,0)
        img_box.dim = coordinates(w,h)
        box = img_box.get_rectangle_inside(zoom_size, coordinates(x,y))
        f, t = box.corners()
        #zoom = cv2.getRectSubPix(img, (800, 600), (x+0.5, y+0.5))
        #cv2.GetSubRect(img, (60, 70, 32, 32))
        #zoom = cv2.getRectSubPix(img, (200, 200), (x, y))
        #zoom = img[f.y:t.y, f.x:t.x]
        ## http://docs.opencv.org/modules/imgproc/doc/geometric_transformations.html#resize
        cv2.resize(img[f.y:t.y, f.x:t.x], dsize=(zoom_size*zoom_factor,zoom_size*zoom_factor), dst=zoom, interpolation=cv2.INTER_NEAREST)
        cv2.imshow('Detail', zoom)
    cv2.namedWindow("Detail")
    cv2.moveWindow("Detail", 500, 400)
    cv2.imshow('Overview', small)
    show_zoom(0,0)
    cv2.setMouseCallback('Overview', onmouse)
    cv2.waitKey()
