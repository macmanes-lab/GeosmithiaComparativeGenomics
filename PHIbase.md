### Blastp against PHI-base db (v4.0)

#### Make database of PHIbase
```
/usr/bin/makeblastdb -in PHI_accessions -dbtype 'prot' -out PHI_database
```
#### Run blastp for *G.morbida*

```
blastp -num_threads 32 -max_target_seqs 1 -evalue 0.000001 -db phibase4.0_database \
-query g.morbida.proteins.fasta \
-out gm5.phibase.e1E-6 -outfmt 6
```
#### Run blastp for *G. flava*
```
blastp -num_threads 32 -max_target_seqs 1 -evalue 0.000001 -db phibase4.0_database \
-query gfl1_proteins_final.fasta \
-out gfl1.phibase4.e1E-6 -outfmt 6
```
#### Run blastp for *G. putterillii*
```
blastp -num_threads 32 -max_target_seqs 1 -evalue 0.000001 -db phibase4.0_database \
-query gp2_proteins_final.fasta \
-out gp4.phibase4.e1E-6 -outfmt 6
```

