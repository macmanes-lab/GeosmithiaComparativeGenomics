#!/usr/bin/env python
# A program for aligning CDSs of a orthogroup using multiprocess.
# USAGE: ./macse4cdsOrthofiles_TA.py
# Author(s): Taruna Aggarwal and Brian Moore
# Affiliation: University of New Hampshire, Durham, NH, USA
# Date: 01/27/2016
# Purpose is

import sys
import os
import subprocess
import argparse
from multiprocessing import Pool, cpu_count

# Each thread will run this once
def runMACSE(files): #input_file, NT_output_file, AA_output_file):
    input_file = files[0]
    NT_output_file = files[1]
    AA_output_file = files[2]
    MACSE_command = "java -jar /macse_v1.01b.jar "
    MACSE_command += "-prog alignSequences "
    MACSE_command += "-seq {0} -out_NT {1} -out_AA {2}".format(input_file, NT_output_file, AA_output_file)
    #print(MACSE_command)
    subprocess.call(MACSE_command, shell=True)

# Each thread will get one intput file and its output names
def iterate_files(args):
    for currentFile in os.listdir(args.root):
        if currentFile.endswith(".fa"):
            # The pool callback can only take on argument, so we yield a list of filenames
            yield [
                args.root + currentFile,
                args.align_NT_dir + currentFile[:-3]+"_NT_aligned.fa",
                args.align_AA_dir + currentFile[:-3]+"_AA_aligned.fa"
            ]

# This is only run by the parent process.
if __name__ == '__main__':
    # Get your arguments from the parser
    parser = argparse.ArgumentParser(description="This script runs aligns coding sequences in files in a given directory.")
    parser.add_argument('--root', default="/macse/cds_files/", help="PATH to the directory containing CDS orthogroup files.")
    parser.add_argument('--align_NT_dir', default="/macse/NT_aligned/", help="PATH to the directory for NT aligned CDS orthogroup files.")
    parser.add_argument('--align_AA_dir', default="/macse/AA_aligned/", help="PATH to the directory for AA aligned CDS orthogroup files.")
    args = parser.parse_args()

    # Try to make output directories
    try:
        os.makedirs(args.align_NT_dir)
        os.makedirs(args.align_AA_dir)
    except FileExistsError as e:
        print(e)

    # We set up how many threads we're going to use
    threads = 16
    try:
        threads = cpu_count()
    except:
        pass

    # We setup the pool, and map the iteration to the thread callback
    pool = Pool(processes=threads)
    pool.map(runMACSE, iterate_files(args))

    print('Finished')