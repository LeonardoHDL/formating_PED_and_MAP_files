#!/usr/bin/env bash


#this script does the recoding from a gene annotation file, a lof matrix file and an external FAM file
#to create a PED file and a MAP file to further use in PLINK

#it should be run as follows:
#./Master_script_to_recode.sh -i /path/to/input/file -o /path/to/output/file -m /path/to/output/map/file

while getopts i:x:g:m:a:h:n:r:o:p flag
do
    case "${flag}" in
		i) input_file=${OPTARG}
        export input_file ;; #input file, lof matrix file, include whole path
		o) outfile=${OPTARG}
        export outfile;; #name of the output file which will be the PED file
        m) mapfile=${OPTARG}
        export mapfile;; #name of the output file which will be the MAP file

    esac
done


tmpfile=$(mktemp temporary_file.XXXXXXXXXX) #this is a temporary file that will be deleted at the end of the script
#the next command will create a temporary file with the first column of the input file
cut -d$'\t' -f1 $input_file > $tmpfile

#the next command will create a temporary file were the first column of the input file is pasted to the input file
tmpfile2=$(mktemp temporary_file.XXXXXXXXXX1)
paste $tmpfile $input_file > $tmpfile2

#this command will get the first row of the input file and paste it to the output file
tmpfile3=$(mktemp temporary_file.XXXXXXXXXX2)
head -n 1 $tmpfile2 | cat - $tmpfile2 > $tmpfile3

#define the directory to the gene annotation file and the external FAM file
gene_annotation_file="./UCONN_F2GenesInfo.csv"
external_FAM_file="./fid_and_iid.txt"

#define the path to the python script
python_script="./recoding_from_a_modified_matrix.py"

#this is the last tmp file that will be used to recode the lof matrix file, is the output file
tmpfile4=$(mktemp temporary_file.XXXXXXXXXX3)

#the specific order to run the python script is important
#after we call python, we first insert the python script, then the gene annotation file, then the lof matrix file, 
#then the external FAM file, then the output path to PED file and then the output path to MAP file


#module load python38/3.8.3
python3 $python_script $gene_annotation_file $tmpfile3 $external_FAM_file $tmpfile4 $mapfile
#module unload python38/3.8.3

#now that we have completed the recoding of the lof matrix file, we need to recode the ped file
#in order to do that we will exchange every "0" for "0 0", every "1" for "0 1" and every "2" for "1 1"
#awk 'BEGIN{FS=OFS=" "} {if(NR>1){for(i=7;i<=NF;i++){if($i==0) $i="0 0"; else if($i==1) $i="0 1"; else if($i==2) $i="1 1"}} print}' $tmpfile4 > $outfile
awk 'BEGIN{FS=OFS=" "} {for(i=7;i<=NF;i++){if($i==0) $i="1 1"; else if($i==1) $i="1 2"; else if($i==2) $i="2 2"} print}' $tmpfile4 > $outfile

#this command will delete the temporary files
rm $tmpfile
rm $tmpfile2
rm $tmpfile3
rm $tmpfile4