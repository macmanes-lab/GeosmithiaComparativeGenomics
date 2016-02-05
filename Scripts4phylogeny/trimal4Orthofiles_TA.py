#!/usr/bin/python3
# A program for trimal'ing all files that contain protein sequences of single-copy orthologs.
# USAGE: ./trimal4Orthofiles_TA.py
# Author: Taruna Aggarwal
# Affiliation: University of New Hampshire, Durham, NH, USA
# Date: 01/27/2016
# Purpose is

import sys
import os
import subprocess
import argparse
import shutil

parser = argparse.ArgumentParser(description="This script runs trimal for files in a directory.")
parser.add_argument('--root', default="/home/mcclintock/ta2007/myscripts/orthogroupScripts/parsed_orthogroups_len16/", help="PATH to the directory containing orthogroup files.")
parser.add_argument('--trimal_dir', default="/home/mcclintock/ta2007/myscripts/orthogroupScripts/trimal_orthogroups_len16_gt20percent/", help="PATH to the directory for trimmed orthogroup files.")
args = parser.parse_args()


def runtrimal(input_file, output_file):
    trimal_command = "/home/mcclintock/ta2007/bin/trimal/source/trimal -in {0} -out {1} -gt 0.20".format(input_file, output_file)
    subprocess.call(trimal_command, shell=True)



Orig_file_dir = args.root
trimal_file_dir = args.trimal_dir

for currentFile in os.listdir(args.root):
    if currentFile.endswith(".fa"):
        trimmed_output = runtrimal(args.root + currentFile, args.trimal_dir + currentFile[:-3]+"_trimmed.fa")
