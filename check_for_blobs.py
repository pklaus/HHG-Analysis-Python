#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Command line tool to read measurement folders and check if overflows (blobs) can be found in the images. """

from dataformat import Measurement
import sys
import os

def main():
    """ The main code, instantiating the class :class:`dataformat.Measurement` for every subfolder of the folder given as first argument. """
    if len(sys.argv) < 2:
        print(__doc__)
        print("usage: %s [folder]" % sys.argv[0])
        sys.exit(1)
    base_folder = sys.argv[1]
    folders = []
    for day_folder in os.listdir(base_folder):
        day_folder = os.path.join(base_folder,day_folder)
        print day_folder
        if not os.path.isdir(day_folder): continue
        for m_folder in os.listdir(day_folder):
            m_folder = os.path.join(day_folder,m_folder)
            print m_folder
            if not os.path.isdir(m_folder): continue
            folders.append(m_folder)
    if len(folders) == 0:
        print("No Subfolders found. Exiting")
        sys.exit(2)
    blob_measurements = []
    for folder in folders:
        print("Looking into folder %s." % folder)
        try:
            m = Measurement(folder)
        except Exception, e:
            print(e)
            print("Could not read in the folder %s. Continuing." % folder)
            continue
        if m.blobs_found:
            print("Found blobs")
            counts = 0
            for mp in m.measurementPoints:
                if len(mp.blobs) > 0:
                    counts += 1
            blob_measurements.append((counts, folder))
    print blob_measurements

if __name__ == '__main__':
    main()
