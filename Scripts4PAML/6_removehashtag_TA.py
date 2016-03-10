#!/usr/bin/python3
# A program for adding hashtags to the "foreground" species. 
# USAGE: ./6_removehashtag_TA.py --input path_to_input_directory
# Author: Taruna Aggarwal
# Contact: ta2007@wildcats.unh.edu
# Affiliation: University of New Hampshire, Durham, NH, USA
# Date: 1/27/2016
# Purpose is to remove '#1' from the species header that is considered the foreground branch 
# for the branch-site model in codeml of PAML

# The script will generate new files in the same directory as itself.
# The new files will be appended with '.fixed.clean'

import argparse
import os

parser = argparse.ArgumentParser(description="This script renames files and their headers in a directory.")
parser.add_argument('--input', help="PATH to the directory with input files.", required=True)
args = parser.parse_args()

for file in os.listdir(args.input):
    if file.endswith(".clean"):
        working_file = open(args.input + '/' + file, "r")
        new_file = open(file[:-6] + ".fixed.clean", "w")
        for currentLine in working_file:
            currentLine = currentLine.rstrip()
            if currentLine.startswith(">geos_morb"):
                new_file.write("{0}{1}\n".format(currentLine[:-2]))
            #elif currentLine[0]==">":
            #    new_file.write("{0}\n".format(currentLine[0:10]))
            else:
                new_file.write("{0}\n".format(currentLine))
working_file.close()
new_file.close()


