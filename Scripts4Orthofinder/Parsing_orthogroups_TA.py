#!/usr/bin/python3
# A program for finding fasta files that contain single-copy orthologs from at least 85% of the species in question
# USAGE: ./Parsing_orthogroups_TA.py
# Author: Taruna Aggarwal
# Affiliation: University of New Hampshire, Durham, NH, USA
# Date: 11/22/2015
# Purpose is parse through fasta files to find 85% or more completed orthogroups

import os
import shutil
import sys

good_files = []

# CREATE YOUR OWN SPECIES LOOKUP LIST USING THE FILE NAMES OR THE SpeciesIDs.txt by Orthofinder
lookup_species = ['Acre_chry',  'Ceph_frag',  'Fusa_gram',  'Neur_cras',  'Stan_gris',
'Agar_hyph',  'Cera_plat',  'Fusa_sola',  'Pucc_gram',  'Tala_acul',
'Alte_bras',  'Chae_glob',  'geos_flav',  'Pyro_conf',  'Tric_rees',
'Aspe_flav',  'Coch_sati',  'geos_morb',  'Rasa_byss',  'Tric_vire',
'Baud_comp',  'Cord_mili',  'geos_putt', 'Usti_mayd', 'Botr_cine',  
'Cucu_berb',  'Gros_clav',  'Rhiz_eric',  'Usti_vire', 'Byss_circ',  
'Eutl_lata',  'Myro_inun',  'Sacc_cere',  'Zymo_trit']

# CHANGE THIS PATH TO YOUR ALIGNMENTS PATH
for root, dirs, files in os.walk("/fungi/taruna/shared/genomes4orthofinder4PAML/expanded_pep/Results_Feb11/Alignments/"):
    # orig_file_num = len(files)
    for currentFile in files:
        keep_file = True # assume file is good at the start
        species_list = []
# CHANGE THIS PATH TO YOUR ALIGNMENTS PATH
        working_file = open("/fungi/taruna/shared/genomes4orthofinder4PAML/expanded_pep/Results_Feb11/Alignments/" + currentFile, "r")
        for currentLine in working_file:
            currentLine = currentLine.rstrip()
            if currentLine.startswith(">"):
                for species in lookup_species:
                    if species in currentLine:
                        if species in species_list:
                            keep_file = False # the file bad
                        else:
                            species_list.append(species)
# CHANGE TO YOUR DESIRED THRESHOLD 
        if len(species_list) < 34:
            keep_file = False # the file bad
        if keep_file:
            good_files.append(currentFile)

# CHANGE THIS PATH TO YOUR OUTPUT DIRECTORY PATH. DO NOT MAKE THE OUTPUT DIR IN THE "Alignments" DIR
Good_file_dir = "/fungi/taruna/shared/genomes4orthofinder4PAML/expanded_pep/Results_Feb11/parsed_orthogroups_len16/"
# CHANGE THIS PATH TO YOUR ALIGNMENTS PATH
Orig_file_dir = "/fungi/taruna/shared/genomes4orthofinder4PAML/expanded_pep/Results_Feb11/Alignments/"

try:
    os.makedirs(Good_file_dir)
except FileExistsError as e:
    print(e)

for file in good_files:
    shutil.copyfile(Orig_file_dir+file, Good_file_dir+file)
