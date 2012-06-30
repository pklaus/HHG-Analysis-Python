#!/usr/bin/env python
''' browse.py - Sample shows how to implement a simple hi resolution image navigation '''

import numpy as np
import cv2
import sys

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
        box.dim.x = size
        box.dim.y = size
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
    else:
        print 'This sample shows how to implement a simple hi resolution image navigation.'
        print 'USAGE: browse.py [image filename]\n'

        sz = 4096
        print 'generating %dx%d procedural image ...' % (sz, sz)
        img = np.zeros((sz, sz), np.uint16)
        track = np.cumsum(np.random.rand(500000, 2)-0.5, axis=0)
        track = np.int32(track*10 + (sz/2, sz/2))
        cv2.polylines(img, [track], 0, 255, 1, cv2.CV_AA)

    min_v, max_v = minmax(img)
    print("Minimum and maximum pixel values in the image: Min: %d Max: %d" % (min_v, max_v))
    img = (img-min_v)*(2**16/(max_v - min_v -1 ))

    small = img
    for i in range(1):
        small = cv2.pyrDown(small)

    def onmouse(event, x, y, flags, param):
        h, w = img.shape[:2]
        hs, ws = small.shape[:2]
        x, y = int(1.0*x*h/hs), int(1.0*y*h/hs)
        #zoom = cv2.getRectSubPix(img, (800, 600), (x+0.5, y+0.5))
        #cv2.GetSubRect(img, (60, 70, 32, 32))
        img_box = rectangle()
        img_box.pos = coordinates(0,0)
        img_box.dim = coordinates(w,h)
        box = img_box.get_rectangle_inside(200, coordinates(x,y))
        f, t = box.corners()
        zoom = img[f.y:t.y, f.x:t.x]
        #zoom = cv2.getRectSubPix(img, (200, 200), (x, y))
        cv2.imshow('zoom', zoom)

    cv2.imshow('preview', small)
    cv2.setMouseCallback('preview', onmouse)
    cv2.waitKey()
