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
    esac
done

ped_file=${input_file}ped
map_file=${input_file}map
outfile=${outdirectory}Gene_burden_Analysis_M1.1
pheno_file='/mnt/Guanina/cvan/data/Keloids_F2/Analysis/leo_analysis/20230227_PCA_results_and_extrafiles/pheno.txt'
covars_file='/mnt/Guanina/cvan/data/Keloids_F2/Analysis/leo_analysis/20230508_burden_analysis/covarfile_array_0.005.txt'
module load plink/1.9
plink --ped ${ped_file} --map ${map_file}  --logistic --pheno $pheno_file --pheno-name Keloids --covar $covars_file --covar-name PC1-PC4 --hide-covar --allow-no-sex --keep-allele-order --out $outfile
module unload plink/1.9



#now that we have done the association analysis, we still havet to plot the results

results_of_assoc_just_snps=${outfile}
path_R_script='assoc_results_plotts.R'
output_for_QQ=${outdirectory}M1.1_QQplot.png
output_for_man=${outdirectory}M1.1_MAN_plot.png
output_top_ten=${outdirectory}M1.1_top_ten_genes.txt

module load r/4.2.2
Rscript --vanilla ${path_R_script} ${results_of_assoc_just_snps} ${output_for_QQ} ${output_for_man} ${output_top_ten}
module unload r/4.2.2

