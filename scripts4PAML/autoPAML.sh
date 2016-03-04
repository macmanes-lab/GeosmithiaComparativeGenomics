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

for inputaln in $(ls *_NT_aligned.fa); do
    F=`basename $inputaln .fa`;
    if [ $(ps -all | grep 'codeml\|raxmlHPC' | wc -l | awk '{print $1}') -lt $TC ] ;
    then
        echo 'I have a core to use'
        ./adding_hashtag_TA.py $F.fasta
        perl pal2nal.pl $F'_AA_aligned.fa' $F'_NT_aligned.fa' -output fasta -nogap -nomismatch > $F.clean &&
        raxmlHPC-PTHREADS -f a -m GTRGAMMA -p 83845 -T 1 -x 93458 -N 100 -n $F.tree -s $F.clean &&
        Insert text change python script
        python null_autoPAML.py $F.clean RAxML_bestTree.$F.tree $F.null.out &&
        python alt_autoPAML.py $F.clean RAxML_bestTree.$F.tree $F.alt.out &&
        python autoPAMLresults.py $F.out | tee -a paml.results &
    else
        echo 'Dont wake me up until there is something else to do'
        sleep 25s
    fi
done