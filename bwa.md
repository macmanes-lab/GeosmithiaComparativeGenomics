## BWA 

### A. Index the *G. putterillii* genome assembly

```
bwa index gp2-K55P4K91-scaffolds.fa 

```

### B. Map paired-end reads to the indexed genome

```
bwa mem gp2-K55P4K91-scaffolds.fa \
gp2_R1.fastq gp2_R1.fastq > gp2.sam 
```

### C. Sort PE sam file

```
samtools sort gp2.sam gp2.sorted
```

### D. Find mapping metrics
```
samtools flagstat gp2.sorted.bam
```
### E. Repeat A-D for *G. flava*