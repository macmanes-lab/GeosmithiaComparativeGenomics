### Phylogenetic Analysis

##### The construction of the phylogenetic tree required the use of several tools and the overall workflow is outlined below. 

Step 1: Generate protein orthogroups using OrthoFinder (v0.3.0).

Step 2: Parse single-copy orthogroups (`Parsing_orthogroups_TA.py`). 

Step 3: Trim sites in each orthogroup using `-gappyout` option in trimAl (trimAl v1.4.rev15).

Step 4: Rename all the headers in each orthogroups so they are uniform across all files. 

Step 5: Concatenate all the trimmed and renamed orthogroup files using `seqCat.pl`.

Step 6. Trim sites further using MARE (Matrix Reduction) version 0.1.2-rc at an alpha value of 5 (option `-d`).

```
MARE partition_coordinates.txt geo_phylogeny_seqs_unwrapped.fasta -d 5 -m

```

Step 7a. Run MrBayes using the MARE output.

Step 7b. For RAxML, find best-fit models for each orthogroup. Many orthogroups might have same models.

 