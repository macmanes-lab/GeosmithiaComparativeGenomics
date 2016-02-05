#!/usr/bin/python3
# A program for trimal'ing all files that contain protein sequences of single-copy orthologs 
# generated with Orthofinder version 0.3.0
# USAGE: ./trimal4Orthofiles_TA.py
# Author: Taruna Aggarwal
# Affiliation: University of New Hampshire, Durham, NH, USA
# Date: 01/27/2016
# Purpose is trim protein sequences using trimAl v1.4.rev15 with -gappyout option

# Usage: ./trimal4Orthofiles_TA.py --root dir_with_all_orthofinder_files --trimal_dir path_to_output_dir

import os
import subprocess
import argparse


parser = argparse.ArgumentParser(description="This script runs trimal on a set of sequence files in a directory.")
parser.add_argument('--root', help="PATH to the directory containing orthogroup files.", required=True)
parser.add_argument('--trimal_dir', help="PATH to the directory for trimmed orthogroup files.", required=True)
args = parser.parse_args()


def runtrimal(input_file, output_file):
    trimal_command = "trimal -in {0} -out {1} -gappyout".format(input_file, output_file)
    subprocess.call(trimal_command, shell=True)


Orig_file_dir = args.root
trimal_file_dir = args.trimal_dir

for currentFile in os.listdir(args.root):
    if currentFile.endswith(".fa"):
        trimmed_output = runtrimal(args.root + currentFile, args.trimal_dir + currentFile[:-3]+"_trimmed.fa")
