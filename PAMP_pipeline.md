# PAML 4.8
## PAML should be called PAINL! 

### A. Preparing files for PAML
#### 1. Obtain single-copy orthologous coding DNA sequences (CDS) using OrthoFinder or OrthoMCL

#### 2. Align the CDS files if using a program of your choice. I used MACSE v1.01b. Run the following command for each CDS file.

```
java -jar /fungi/taruna/shared/bin/MACSE/macse_v1.01b.jar -prog alignSequences -seq CDS_OG0007645.fa
```
