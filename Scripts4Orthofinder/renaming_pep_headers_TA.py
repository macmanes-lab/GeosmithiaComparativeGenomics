#!/usr/bin/python3
# A program for renaming fasta headers
# USAGE: ./renaming_headers_TA.py --input path_to_input_directory
# Author: Taruna Aggarwal
# Affiliation: University of New Hampshire, Durham, NH, USA
# Date: 1/27/2016
# Purpose is to replace headers with their corresponding file names
# and add consecutive numbers to the new headers

# This script assumes that your pep files are named in a specific manner:
# SpeciesInitial_genusName.pep and an example is F_solani.pep
# The script will generate new files in the same directory as itself.

import argparse
import os

parser = argparse.ArgumentParser(description="This script renames files and their headers in a directory.")
parser.add_argument('--input', help="PATH to the directory with input files.", required=True)
args = parser.parse_args()

for file in os.listdir(args.input):
    if file.endswith(".pep"):
        working_file = open(args.input + '/' + file, "r")
        new_file = open(file[:-4] + "_renamed.pep", "w")
        print("Renaming {0}".format(file))
        counter = 1
        for currentLine in working_file:
            currentLine = currentLine.rstrip()
            if currentLine.startswith(">"):
                new_file.write("{0}_{1}\n".format((file[:-4]), counter))
                counter += 1
            else:
                new_file.write("{0}\n".format(currentLine))


