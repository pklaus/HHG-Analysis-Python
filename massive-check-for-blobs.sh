#!/bin/bash
""" Tool to read measurement folders and check if overflows (blobs) can be found in the images. """

WHERE="/media/BACHELORDAT/DATA"

for PARFOLDER in $(ls $WHERE); do
  for CHILDFOLDER in $(ls $WHERE/$PARFOLDER); do
    ./check_for_blobs.py $WHERE/$PARFOLDER/$CHILDFOLDER
  done
done
