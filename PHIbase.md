### Blastp against PHI-base db (v4.0)

#### Make database of PHIbase
```
/usr/bin/makeblastdb -in PHI_accessions -dbtype 'prot' -out PHI_database
```
#### Run blastp for *G.morbida*

```
blastp -num_threads 32 -max_target_seqs 1 -evalue 0.000001 -db PHI_database \
-query g.morbida.proteins.fasta \
-out g.morbida.phibase.e1E-6 -outfmt 6
```
#### Run blastp for *G. flava*
```
blastp -num_threads 32 -max_target_seqs 1 -evalue 0.000001 -db PHI_database \
-query Fusarium_solani.v2.0.29.pep.all.fa \
-out f.solani.phibase.e1E-6 -outfmt 6
```
#### Run blastp for *G. putterillii*
```
blastp -num_threads 32 -max_target_seqs 1 -evalue 0.000001 -db PHI_database \
-query Grosmannia_clavigera_kw1407.GCA_000143105.2.29.pep.all.fa \
-out g.clavigera.phibase.e1E-6 -outfmt 6
```
