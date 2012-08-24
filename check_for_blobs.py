#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Command line tool to read measurement folders and check if overflows (blobs) can be found in the images. """

from dataformat import Measurement
import sys

def main():
    """ The main code, instantiating the class :class:`dataformat.Measurement` for every subfolder of the folder given as first argument. """
    if len(sys.argv) < 2:
        print(__doc__)
        print("usage: %s [folder]" % sys.argv[0])
        sys.exit(1)
    folder = sys.argv[1]
    print("Looking into folder %s." % folder)
    try:
        m = Measurement(folder)
    except Exception, e:
        print(e)
        print("Could not read in the folder %s. Exiting." % folder)
        sys.exit(2)
    counts = 0
    if m.blobs_found:
        print("Found blobs")
        for mp in m.measurementPoints:
            if len(mp.blobs) > 0:
                counts += 1
    print folder, counts

if __name__ == '__main__':
    main()
