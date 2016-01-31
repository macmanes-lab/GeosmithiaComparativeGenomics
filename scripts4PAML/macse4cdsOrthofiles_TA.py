#!/usr/bin/python3
"""A program for aligning CDSs of a orthogroup.

USAGE: ./macse4cdsOrthofiles_TA.py
Author: Taruna Aggarwal
Affiliation: University of New Hampshire, Durham, NH, USA
Date: 01/27/2016
Purpose is
"""

import sys
import os
import subprocess
import argparse
from multiprocessing import pool


def runMACSE(input_file, NT_output_file, AA_output_file):
    MACSE_command = "java -jar /fungi/taruna/shared/bin/MACSE/macse_v1.01b.jar "
    MACSE_command += "-prog alignSequences "
    MACSE_command += "-seq {0} -out_NT {1} -out_AA {2}".format(input_file,
            NT_output_file, AA_output_file)
    # print(MACSE_command)
    subprocess.call(MACSE_command, shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This script runs aligns "
            "coding sequences in files in a given directory.")
    parser.add_argument('--root', default="/fungi/taruna/shared/testing_macse/",
            help="PATH to the directory containing CDS orthogroup files.")
    parser.add_argument('--align_NT_dir',
            default="/fungi/taruna/shared/testing_macse/NT_aligned/",
            help="PATH to the directory for NT aligned CDS orthogroup files.")
    parser.add_argument('--align_AA_dir',
            default="/fungi/taruna/shared/testing_macse/AA_aligned/",
            help="PATH to the directory for AA aligned CDS orthogroup files.")
    args = parser.parse_args()

    Orig_file_dir = args.root
    NT_align_file_dir = args.align_NT_dir
    AA_align_file_dir = args.align_AA_dir

    try:
        os.makedirs(NT_align_file_dir)
        os.makedirs(AA_align_file_dir)
    except FileExistsError as e:
        print(e)

    # Create a list of files to apply the runMACSE function to
    flist = [fname for fname in os.listdir(args.root) if fname.endswith(".fa")]


            # runMACSE(args.root + currentFile, args.align_NT_dir \
            # + currentFile[:-3]+"_NT_aligned.fa", args.align_AA_dir \
            # + currentFile[:-3]+"_AA_aligned.fa")

    with Pool(10) as p:
        # this is where I get lost. I don't even know if this is correct.
