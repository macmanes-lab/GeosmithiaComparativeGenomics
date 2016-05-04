#!/usr/bin/python3
# A program for aligning CDSs of a orthogroup.
# USAGE: ./pal2nal_TA.py
# Author: Taruna Aggarwal
# Affiliation: University of New Hampshire, Durham, NH, USA
# Date: 01/27/2016
# Purpose is

import sys
import os
import subprocess
import argparse

parser = argparse.ArgumentParser(description="This script parses single copy orthoglogs among with alignment files produced by Orthofinder.")
parser.add_argument('--AAinput', help="PATH to AA files", required=True)
parser.add_argument('--NTinput', help="PATH to NT files", required=True)
args = parser.parse_args()


def runpal2nal(AAfile, NTfile):
    runpal2nal_command = "perl /home/mcclintock/ta2007/bin/pal2nal.v14/pal2nal.pl {0} {1} -output fasta -nogap -nomismatch > {2}".format(AAfile, NTfile, AAfile[:-14] + ".clean")
    subprocess.call(runpal2nal_command, shell=True)

for file in os.listdir(args.AAinput):
  if file.endswith(".fa"):
    output = runpal2nal(args.AAinput + "/" + file, args.NTinput + "/" + file[0:13] + "_NT_aligned.fa")

