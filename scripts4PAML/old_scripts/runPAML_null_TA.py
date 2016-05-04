#!/usr/bin/python3
# A program for running PAML's codeml.
# USAGE: ./runPAML_null_TA.py
# Author: Taruna Aggarwal
# Affiliation: University of New Hampshire, Durham, NH, USA
# Date: 01/27/2016
# Purpose is

import sys
import os
import subprocess
import argparse

parser = argparse.ArgumentParser(description="This script parses single copy orthoglogs among with alignment files produced by Orthofinder.")
parser.add_argument('--cds', help="PATH to cds files", required=True)
parser.add_argument('--trees', help="PATH to tree files", required=True)
args = parser.parse_args()


def runPAMLnull(cdsfile, treefile):
    runPAMLnull_cmd = "python null_autoPAML.py {0} {1} {2}".format(cdsfile, treefile, cdsfile[:-6] + ".null.out")
    subprocess.call(runPAMLnull_cmd, shell=True)

for file in os.listdir(args.cds):
  if file.endswith(".clean"):
    output = runPAMLnull(args.cds + "/" + file, args.trees + "/" + "RAxML_bestTree." + file[:-6])

