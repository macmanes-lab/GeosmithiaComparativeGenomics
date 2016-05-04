#!/usr/bin/env python
# A program for aligning CDSs of a orthogroup.
# USAGE: ./runRAxML_TA.py
# Author: Taruna Aggarwal
# Affiliation: University of New Hampshire, Durham, NH, USA
# Date: 01/27/2016
# Purpose is

import os
import subprocess
import argparse

parser = argparse.ArgumentParser(description="This script runs RAxML for files in a directory.")
parser.add_argument('--root', help="PATH to the directory containing clean files.", required=True)
args = parser.parse_args()


def runRAxML(input_file, name):
    raxmlHPC_command = "raxmlHPC-PTHREADS-AVX -f a -m GTRGAMMA -p 13487 -x 93484 -N 100 -s {0} -n {1} -T 8".format(input_file, name)
    subprocess.call(raxmlHPC_command, shell=True)

for currentFile in os.listdir(args.root):
    if currentFile.endswith(".fasta"):
        runRAxML(args.root + currentFile, currentFile[:-20])


