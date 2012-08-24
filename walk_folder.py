#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Command line tool to read measurement folders and navigate through their measurement points. """

from dataformat import Measurement
import keycode
import sys

def main():
    """ The main code, instantiating the class :class:`dataformat.Measurement` with the folder of the first argument given. """
    if len(sys.argv) < 2:
        print "Give a folder!"
        sys.exit(1)
    try:
        m = Measurement(sys.argv[1])
    except Exception, e:
        print e
        sys.exit(2)
    if m.blobs_found:
        print("Attention, at least one image appears to have an overflow! Please correct that first.")
    print "Measurement read in."
    i = 0
    print("Use the left / right keys to navigate.")
    while i in range(len(m.measurementPoints)):
        print("Showing image %d of %d." % (i+1, len(m.measurementPoints)) )
        key = m.measurementPoints[i].display_image(rescale=True,rescale_to_percentile_and_max=True)
        # how many measurement points should the tool jump on keystrokes
        if key in keycode.KEY_ESCAPE or key in keycode.KEY_CLOSE_WINDOW:
            break
        if key in keycode.KEY_RIGHT or key in keycode.KEY_SPACE:
            i += 1
        elif key in keycode.KEY_LEFT:
            i += -1
        elif key in keycode.KEY_DOWN:
            i += 10
        elif key in keycode.KEY_UP:
            i += -10
    print("Last image displayed, exiting.")

if __name__ == '__main__':
    main()
