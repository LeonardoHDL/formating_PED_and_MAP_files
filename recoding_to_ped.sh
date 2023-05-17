#!/usr/bin/env bash


#this script is meant to recode the ped file from a lof matrix file
#which contain genotypes in the form of 0, 1, 2
#the ped file requires genotypes in the form of 0 0, 0 1, 1 1
#it also deletes the header line of the lof matrix file

while getopts i:x:g:m:a:h:n:r:o:p flag
do
    case "${flag}" in
		i) input_file=${OPTARG}
        export input_file ;; #input file, lof matrix file, include whole path
        x) extrafiles=${OPTARG}
        export extrafiles;; #external file containing FID and IID for all individuals include whole path
		o) outfile=${OPTARG}
        export outdirectory;; #name of the output file which will be the PED file

    esac
done

path_to_python_script="/mnt/Guanina/cvan/data/Keloids_F2/Analysis/leo_analysis/20230508_burden_analysis/m1_1_trial/merging_fam_and_genotype_info_to_create_ped_file.py"

awk '{ for (i = 2; i <= NF; i++) { if ($i == 0) $i = "0 0"; else if ($i == 1) $i = "0 1"; else if ($i == 2) $i = "1 1"; } print }' $input_file > $outfile
tmpfile=$(mktemp temporary_file.XXXXXXXXXX)
mv $outfile $tmpfile
tail -n +2 $tmpfile > $outfile
rm $tmpfile

module load python38/3.8.3
python3 merging_fam_and_genotype_info_to_create_ped_file.py fid_and_iid.txt $outfile