#!/usr/bin/python3
# A program for renaming headers in orthogroup files 
# USAGE: ./renamingtrimALfiles_TA.py
# Author: Taruna Aggarwal
# Affiliation: University of New Hampshire, Durham, NH, USA
# Date: 01/28/2016
# Purpose is to rename headers so each file contains the same corresponding headers


# This script assumes that your files have headers containing the string '.pep'
# Usage: python3 renamingtrimALfiles_TA.py path_to_dir_with_files

import sys
import os

for currentFile in os.listdir(sys.argv[1]+ "/"):
    if currentFile.endswith(".fa"):
        # CHANGE THIS LINE
        working_file = open(sys.argv[1]+ "/" + currentFile, "r")
        new_file = open(currentFile[:-11]+"_trim_rename.fa", "w")
        for currentLine in working_file:
            currentLine = currentLine.rstrip()
            if currentLine.startswith(">"):
                species_name = currentLine.split('.pep')[0]
                new_file.write("{0}\n".format(species_name))
            else:
                new_file.write("{0}\n".format(currentLine))


