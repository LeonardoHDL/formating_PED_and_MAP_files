#!/usr/bin/env python

#this script is part of an automatization proccess to recode a matrix of genotypes
# and a FAM file into a PED file

#import necessary libraries
import pandas as pd
import numpy as np
import sys
import warnings
warnings.filterwarnings("ignore")

#define the gene anottation file
gene_anottation_file_directory= sys.argv[1]
gene_anottation_file= pd.read_csv(gene_anottation_file_directory)
print(f'gene_anottation_file.shape: {gene_anottation_file.shape}')

#define the gene_lof_matrix
gene_lof_matrix_directory= sys.argv[2]
gene_lof_matrix=pd.read_table(gene_lof_matrix_directory)
print(f'gene_lof_matrix.shape: {gene_lof_matrix.shape}')
#use a copy of the gene_lof_matrix to avoid any changes in the original file
sample_gene_matrix=gene_lof_matrix
print(f'sample_gene_matrix.shape: {sample_gene_matrix.shape}')

#since we want the gene names to be the column names, we will transpose the matrix
transposed_sample_gene_matrix=sample_gene_matrix.transpose()
print(f'transposed_sample_gene_matrix.shape: {transposed_sample_gene_matrix.shape}')
#we will reset the index to be able to work with the data
transposed_sample_gene_matrix.reset_index(inplace=True)
#due to duplicate columns because of the preprocessing of the data, we will remove the first column
transposed_sample_gene_matrix=transposed_sample_gene_matrix.iloc[:,1:]

#we will rename the columns with the first row of the matrix
first_row=transposed_sample_gene_matrix.iloc[0,:].tolist()
first_row[0]='Gene(ensxxx)'
transposed_sample_gene_matrix.columns=first_row

#we will remove the first 2 rows of the matrix, again due to the preprocessing of the data
semifianl_transposed_sample_gene_matrix=transposed_sample_gene_matrix.iloc[2:,:]

#we will split the Gene(ensxxx) column into 2 columns, one with the gene name and the other with the gene ID
semifianl_transposed_sample_gene_matrix[['GeneName','GeneID']]=semifianl_transposed_sample_gene_matrix['Gene(ensxxx)'].str.split('(',n=1,expand=True)
print(f'semifianl_transposed_sample_gene_matrix.shape: {semifianl_transposed_sample_gene_matrix.shape}')

#we will filter the gene anottation file to only have the gene name and the gene ID
filetr_of_genes_anno_file=pd.DataFrame(gene_anottation_file[['GeneName','GeneId']])
filetr_of_genes_anno_file.columns=['GeneName','GeneID']
print(f'filetr_of_genes_anno_file.shape: {filetr_of_genes_anno_file.shape}')

#we will remove the parenthesis from the gene ID column
semifianl_transposed_sample_gene_matrix['GeneID']=semifianl_transposed_sample_gene_matrix['GeneID'].str.replace(')','')
print(f'semifianl_transposed_sample_gene_matrix.shape: {semifianl_transposed_sample_gene_matrix.shape}')

#we will merge the semifinal matrix with the filtered gene anottation file so that only 
#matching genes are kept
merged_semifinal_w_anottation=pd.merge(semifianl_transposed_sample_gene_matrix,filetr_of_genes_anno_file,on='GeneID',how='inner')
print(f'merged_semifinal_w_anottation.shape: {merged_semifinal_w_anottation.shape}')

#so that columns of the matrix are in the same order as the gene anottation file, we will sort the columns
merged_semifinal_w_anottation=merged_semifinal_w_anottation.sort_values(by=['Gene(ensxxx)'])

#since we only did the transpose to get a column of the gene names, we will transpose the matrix again
re_transposed_final_matrix=merged_semifinal_w_anottation.transpose()
print(f're_transposed_final_matrix.shape: {re_transposed_final_matrix.shape}')

#we will reset the index to be able to work with the data
re_transposed_final_matrix=re_transposed_final_matrix.reset_index()
print(f're_transposed_final_matrix.shape: {re_transposed_final_matrix.shape}')

#we will rename the columns with the first row of the matrix
new_col_names=re_transposed_final_matrix.iloc[0,:].tolist()
new_col_names[0]='IID'
re_transposed_final_matrix.columns=new_col_names

#we will remove the first row of the matrix because it is the same as the column names
re_transposed_final_matrix=re_transposed_final_matrix.iloc[1:,:]
print(f're_transposed_final_matrix.shape: {re_transposed_final_matrix.shape}')

#we will remove the last 3 rows of the matrix because they are not samples, theyre the added columns from str_split
re_transposed_final_matrix=re_transposed_final_matrix.iloc[:-3,:]
print(f're_transposed_final_matrix.shape: {re_transposed_final_matrix.shape}')

#define the directory of the FAM file
external_fam=sys.argv[3]
fid_and_iid = pd.read_table(external_fam,sep=' ',names=['FID','IID','motherID', 'FatherID', 'SEX', 'PHENO'])
print(f'fid_and_iid.shape: {fid_and_iid.shape}')

#we will merge the re_transposed_final_matrix with the FAM file to get the FID and IID columns
geno_and_fam=pd.merge(re_transposed_final_matrix,fid_and_iid,how='inner',on=['IID'])
print(f'geno_and_fam.shape: {geno_and_fam.shape}')

#as the PED requieres a specific order of the columns, we will reorder the columns
geno_and_fam_col_names=geno_and_fam.columns.tolist()
new_col_order = ['FID','IID','FatherID','motherID','SEX', 'PHENO']+geno_and_fam_col_names[:-5]
geno_and_fam_new_order = geno_and_fam[new_col_order]
print(f'geno_and_fam_new_order.shape: {geno_and_fam_new_order.shape}')

#we have a duplicate column that we will remove
column_position = 6  # Index of the column to be deleted (0-based index)
geno_and_fam_final = geno_and_fam_new_order.iloc[:, [i for i in range(len(geno_and_fam_new_order.columns)) if i != column_position]]

##now we will save the file
print(f'geno_and_fam_final.shape: {geno_and_fam_final.shape}')
output_file=sys.argv[4]
geno_and_fam_final.to_csv(output_file,sep=' ',index=False, header=False)

#now from the gene anottation file we will create the MAP file
print('the gene anottation file will be used to create the MAP file')
print(f'gene_anottation_file.shape: {gene_anottation_file.shape}')

#first we obtain the columns that we need from the gene anottation file
gene_anottation_file_for_MAP=gene_anottation_file[['GeneName','GeneId','CHR','MinPos','MaxPos']]

#now we get the genes that are in the matrix
genes_to_be_kept=merged_semifinal_w_anottation[['Gene(ensxxx)','GeneName_x','GeneID']]
print(f'genes to be kept.shape: {genes_to_be_kept.shape}')

#we will rename the column GeneName_x to GeneName
genes_to_be_kept.rename(columns={'GeneName_x':'GeneName'},inplace=True)

#now we proceed to merge the gene anottation file with the genes to be kept
#so that genes that are not in the matrix are removed
merged_gene_anottation_file_for_MAP=pd.merge(gene_anottation_file_for_MAP,genes_to_be_kept,on=['GeneName'],how='inner')
print('merged_gene_anottation_file_for_MAP.shape: ',merged_gene_anottation_file_for_MAP.shape)


#now add a column of 0s called CM
merged_gene_anottation_file_for_MAP['CM']=0

#now we will select the columns that we want to keep and in a specific order
MAP_file=merged_gene_anottation_file_for_MAP[['CHR','Gene(ensxxx)','CM','MinPos','MaxPos']]
print(f'MAP_file.shape: {MAP_file.shape}')

#concatenate two columns with specific character separator
separator = ':'
MAP_file['Concatenated_Columns'] = [f"{a}{separator}{b}" for a, b in zip(MAP_file['MinPos'], MAP_file['MaxPos'])]
print(f'MAP_file.shape: {MAP_file.shape}')

#now we will rename the the new column as BPposition
MAP_file.rename(columns={'Concatenated_Columns':'BPposition'},inplace=True)

#at last, we will select the columns that we want to keep and in a specific order
seminfinal_MAP_file=MAP_file[['CHR','Gene(ensxxx)','CM','BPposition']]
print(f'seminfinal_MAP_file.shape: {seminfinal_MAP_file.shape}')

#now we will sort the MAP file by the gene name, so that it is in the same order as the PED file
sorted_final_MAP_file=seminfinal_MAP_file.sort_values(by=['Gene(ensxxx)'])
print(f'sorted_seminfinal_MAP_file.shape: {sorted_final_MAP_file.shape}')

#now we proceed to save the MAP file
output_file_for_MAP=sys.argv[5]
sorted_final_MAP_file.to_csv(output_file_for_MAP,sep=' ',index=False, header=False)
