#!/usr/bin/python3
# A program for
# USAGE: ./renaming_trimalFiles_TA.py PATH_To_Directory_With_Orthofiles
# Author: Taruna Aggarwal
# Affiliation: University of New Hampshire, Durham, NH, USA
# Date: 01/28/2016
# Purpose is rename all the headers in orthofiles so they are same for the concatenation step.

import sys
import os


for currentFile in os.listdir(sys.argv[1]):
    if currentFile.endswith(".fa"):
        # CHANGE THIS LINE
        working_file = open(sys.argv[1] + "/" + currentFile, "r")
        new_file = open(currentFile[0:9] + "_trim_renamed.fa", "w")
        for currentLine in working_file:
            currentLine = currentLine.rstrip()
            if currentLine.startswith(">"):
                currentLine = currentLine.replace("-", "_")
                currentLine = currentLine.replace(".", "_")
                species_name = currentLine.split('_pep')[0]
                new_file.write("{0}\n".format(species_name))
            else:
                new_file.write("{0}\n".format(currentLine))

new_file.close()
working_file.close()

