#!/usr/bin/env python

import cv2
import numpy as np
from mathtools import scoreatpercentile

class TIFF(object):
    """
    A Class that helps reading TIFF image files,
    especially 16 bit grayscale images.

    It also contains frequently used operations on those images.

    The image array data can be accessed via the property TIFF.data
    """
    depth_map = {'uint8': 8, 'uint16': 16, 'uint32': 32, 'uint64': 64}
    def __init__(self, filename=None):
        if filename:
            self.read(filename)
    def read(self,filename):
        self.data = cv2.imread(filename,-1)
        self.filename = filename
    def get_data(self):
        return self.__data
    def set_data(self, data):
        self.__data = data
        #self.filename = None
        self.update()
    data = property(get_data, set_data)
    def update(self):
        self.dimensions = self.data.shape[:2]
        self.depth = self.depth_map[str(self.data.dtype)]
    def percentiles(self, percentages):
        percentiles = dict()
        values = self.data.flatten()
        values.sort()
        for percentage in percentages:
            percentiles[percentage] = scoreatpercentile(values, percentage)
        return percentiles
    def minmax(self):
        return self.data.min(), self.data.max()
    def rescale(self, minmax=None):
        np.seterr(under='print')
        if minmax:
            min_v, max_v = minmax
        else:
            min_v, max_v = self.minmax()
        min_v, max_v = int(min_v), int(max_v)
        subtract = np.choose(np.greater(self.data, min_v), (self.data, min_v))
        return (self.data-subtract)*int((2**16-1.)/(max_v - min_v))
    def scale_down_to_half(self):
        self.data = cv2.pyrDown(self.data)
        self.update()

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print "Give a 16bit TIFF!"
        sys.exit(1)
    i = TIFF(sys.argv[1])
    print("Image of %dx%d pixels." % (i.dimensions))
    print("Depth: %d bit" % i.depth)
    rdata = i.rescale()
    cv2.imshow('test',rdata)
    print("Press key in OpenCV window to continue / exit.")
    cv2.waitKey()
