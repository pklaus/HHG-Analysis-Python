#!/usr/bin/env python

import cv2
import numpy as np
from mathtools import scoreatpercentile

class TIFF16bit():
    depth_map = {'uint8': 8, 'uint16': 16, 'uint32': 32, 'uint64': 64}
    def __init__(self, filename=None):
        if filename:
            self.read(filename)
    def read(self,filename):
        self.img = cv2.imread(filename,-1)
        self.filename = filename
        self.update()
    def set(self,img):
        self.img = img
        self.filename = None
        self.update()
    def update(self):
        self.dimensions = self.img.shape[:2]
        self.depth = self.depth_map[str(self.img.dtype)]
    def percentiles(self, percentages):
        percentiles = dict()
        values = self.img.flatten()
        values.sort()
        for percentage in percentages:
            percentiles[percentage] = scoreatpercentile(values, percentage)
        return percentiles
    def minmax(self):
        return self.img.min(), self.img.max()
    def rescale(self, minmax=None):
        np.seterr(under='print')
        if minmax:
            min_v, max_v = minmax
        else:
            min_v, max_v = self.minmax()
        min_v, max_v = int(min_v), int(max_v)
        subtract = np.choose(np.greater(self.img, min_v), (self.img, min_v))
        return (self.img-subtract)*int((2**16-1.)/(max_v - min_v))
        return (self.img-min_v)*int((2**16-1.)/(max_v - min_v))
    def scale_down_to_half(self):
        self.img = cv2.pyrDown(self.img)
        self.update()

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print "Give a 16bit TIFF!"
        sys.exit(1)
    i = TIFF16bit(sys.argv[1])
    print("Image of %dx%d pixels." % (i.dimensions))
    print("Depth: %d bit" % i.depth)
    img = i.rescale()
    cv2.imshow('test',img)
    print("Press key in OpenCV window to continue / exit.")
    cv2.waitKey()
