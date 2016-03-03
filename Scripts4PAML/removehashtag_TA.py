#!/usr/bin/python3
# A program for
# Author: Taruna Aggarwal
# Contact: ta2007@wildcats.unh.edu
# Affiliation: University of New Hampshire, Durham, NH
# Date: 2/17/2016
# USAGE: ./removehashtag_TA.py inFile outFile


import sys

inFile = open(sys.argv[1], "r")
outFile = open(sys.argv[2], "w")

for line in inFile:
  line = line.rstrip()
  if line.startswith(">geos_morb"):
    outFile.write("{0}\n".format(line[:-2]))
  #elif line[0]==">":
  #  outFile.write("{0}\n".format(line))
  else:
    outFile.write("{0}\n".format(line))

inFile.close()
outFile.close()




