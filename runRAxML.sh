#! /bin/bash

usage=$(cat << EOF
   # This script runs a pipeline that takes a fasta file and BAMfiles and tests for selection:
   #
   runRAxML.sh [options]
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


for inputaln in $(ls *aln); do
    F=`basename $inputaln .aln`;
    if [ $(ps -U ta2007 | grep 'raxmlHPC-PTHREADS' | wc -l | awk '{print $1}') -lt $TC ] ;
    then
        echo 'I have a core to use'
        #java -Xmx2000m -jar ~/bin/MACSE/macse_v1.01b.jar -prog alignSequences -seq $inputaln -out_NT $F.aln &&
        raxmlHPC-PTHREADS -T 1 -m GTRGAMMA -n $F.tree -s $F.aln -p 12345 &
        #python paml.py $F.aln RAxML_bestTree.$F.tree $F.out &
    else
        echo 'Dont wake me up until there is something else to do'
        sleep 25s
    fi
done