#!/usr/bin/env bash

#this script performs the GWAS analysis using the gene burden test

#it should be run as follows:

while getopts i:x:g:m:a:h:n:r:o:p flag
do
    case "${flag}" in
		i) input_file=${OPTARG}
        export input_file ;; #path and prefix to the ped and map files
		o) outdirectory=${OPTARG}
        export outdirectory;; #path where the results will be saved
        m) mapfile=${OPTARG}
        export mapfile;; 

    esac
done

tmpfile=$(mktemp temporary_file.XXXXXXXXXX) #this is a temporary file that will be deleted at the end of the script
outfile=${outdirectory}Gene_burden_Analysis_M1.1
pheno_file='/mnt/Guanina/cvan/data/Keloids_F2/Analysis/leo_analysis/20230227_PCA_results_and_extrafiles/pheno.txt'
covars_file='/mnt/Guanina/cvan/data/Keloids_F2/Analysis/leo_analysis/20230508_burden_analysis/covarfile_array_0.005.txt'

module load plink/1.9
plink --file $input_file --keep-allele-order --make-bed --out $tmpfile
plink --bfile $tmpfile --logistic --pheno $pheno_file --pheno-name Keloids --covar $covars_file --covar-name PC1-PC4 --allow-no-sex --keep-allele-order --out $outfile
module unload plink/1.9

rm $tmpfile