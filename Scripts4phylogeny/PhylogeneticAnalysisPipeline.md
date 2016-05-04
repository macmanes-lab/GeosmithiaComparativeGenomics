### Phylogenetic Analysis

##### The steps for construction of the phylogenetic tree is outlined below. 

Step 1: Generate and align protein orthogroups using OrthoFinder (v0.3.0).

Step 2: Parse single-copy orthogroups (`Parsing_orthogroups_TA.py` from `Scripts4Orthofinder` folder). 

Step 3: Trim sites in each orthogroup using `-gappyout` option in trimAl (trimAl v1.4.rev15) (`trimal4Orthofiles_TA.py`).

Step 4: Rename all the headers in each orthogroups so they are uniform across all files (`renaming_trimalFiles_TA.py`). 

Step 5: Concatenate all the trimmed and renamed orthogroup files using `seqCat.pl` by Olaf R.P. Bininda-Emonds. This perl script requires a text file containing names of sequences files that need to be concatenated (check `help` command by running `./seqCat.pl -h`). There is no space after `-d` argument.

```
seqCat.pl -dfiles_names.txt -if
```


Step 6. Convert the nexus file to fasta using `SeqConverter.pl`

Step 6. Trim sites further using MARE (Matrix Reduction) version 0.1.2-rc at an alpha value of 3 (option `-d`).

```
MARE the fungal_phylogeny_seqs.fasta -d 3 -m
```

Step 7. Run PartitionFinder v1.1.1

Step 7a. For RAxML version 8.1.20, find best-fit models for each orthogroup. Many orthogroups might have same models.


``` 
raxmlHPC-PTHREADS -T 10 -f a -x 12345 -# 200 -s ../PartitionFinder/geo_seqs.phylip -q partition_models.txt -p12345 -n geosmithia_pf_rax_bootstrap -m PROTGAMMALG
```

Step 7b. Run MrBayes using the MARE output.

Step 7C. Run PhyloBayes using the MARE output.

```
pb -d phylip_file run1_name
```
```
pb -d phylip_file run2_name
```
```
bpcomp -x 1000 2 run1_name run2_name
```



 