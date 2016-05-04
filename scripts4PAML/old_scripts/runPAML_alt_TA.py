#!/usr/bin/python3
# A program for running PAML's codeml.
# USAGE: ./runPAML_alt_TA.py
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


def runPAMLalt(cdsfile, treefile):
    runPAMLalt_cmd = "python alt_autoPAML.py {0} {1} {2}".format(cdsfile, treefile, cdsfile[:-6] + ".alt.out")
    subprocess.call(runPAMLalt_cmd, shell=True)

for file in os.listdir(args.cds):
  if file.endswith(".clean"):
    output = runPAMLalt(args.cds + "/" + file, args.trees + "/" + "RAxML_bestTree." + file[:-6])

