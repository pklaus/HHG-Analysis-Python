#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Command line tool to read measurement folders and navigate through their measurement points. """

from dataformat import Measurement
import keycode
import sys

# A dictionary that defines how many measurement points the tool should jump on keystrokes.
jump_by = {
        keycode.KEY_RIGHT: 1,
        keycode.KEY_DOWN: 10,
        keycode.KEY_SPACE: 1,
        keycode.KEY_LEFT: -1,
        keycode.KEY_UP: -10,
        }

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
        if key == keycode.KEY_ESCAPE: # 27
            break
        if key in jump_by.keys():
            i += jump_by[key]
    print("Last image displayed, exiting.")

if __name__ == '__main__':
    main()
