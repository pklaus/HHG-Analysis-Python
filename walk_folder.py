#!/usr/bin/env python

from dataformat import Measurement

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print "Give a folder!"
        sys.exit(1)
    m = Measurement(sys.argv[1])
    for mp in m.measurementPoints:
        mp.display_image()
