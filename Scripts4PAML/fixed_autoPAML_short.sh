#! /bin/bash

usage=$(cat << EOF
   # This script runs a pipeline that takes a fasta file and BAMfiles and tests for selection:
   #
   autoPAML.sh [options]
   Options:
      -t <v> : *required* Numberof threads to use.
EOF
);

while getopts f:b:o:t: option
do
        case "${option}"
        in
		t) TC=${OPTARG};;
        esac
done

##Align
END=$(ls | wc -l | awk '{print $1}')
START=1

for inputaln in $(ls *fasta); do
    F=`basename $inputaln .fasta`;
    if [ $(ps -U aggarwal | grep 'java\|codeml\|raxmlHPC' | wc -l | awk '{print $1}') -lt $TC ] ;
    then
        echo 'I have a core to use'
        java -Xmx2000m -jar /fungi/taruna/shared/bin/MACSE/macse_v1.01b.jar -prog alignSequences -seq $inputaln -out_NT $F.aln || true &&
        perl /fungi/taruna/shared/bin/pal2nal.v14/pal2nal.pl $F'_macse_AA.fasta' $F.aln -output fasta -nogap -nomismatch > $F.clean || true &&
        raxmlHPC-PTHREADS -f a -m GTRGAMMA -p 83845 -T 1 -x 93458 -N 100 -n $F.tree -s $F.clean || true &&
        ./removehashtag_TA.py $F.clean $F.fixed.clean || true && 
        python null_autoPAML.py $F.fixed.clean RAxML_bestTree.$F.tree $F.null.out || true &&
        python alt_autoPAML.py $F.fixed.clean RAxML_bestTree.$F.tree $F.alt.out || true &&
        python results_paml.py $F.null.out $F.alt.out | tee -a geosmithia_PAML.results || true &
    else
        echo 'Dont wake me up until there is something else to do'
        sleep 25s
    fi
done