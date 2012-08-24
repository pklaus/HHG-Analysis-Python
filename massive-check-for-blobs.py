#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Command line tool to read measurement folders and check if overflows (blobs) can be found in the images. """

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
        # run "check_for_blobs.py $folder" here

if __name__ == '__main__':
    main()
