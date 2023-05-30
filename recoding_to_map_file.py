
import pandas as pd
import numpy as np
import sys
lof_matrix=sys.argv[1]
lof_matrix_file = pd.read_table('UCHC_Freeze_Two.M1.1.lofMatrix.txt',sep='\t', header=0)
genes=lof_matrix_file.columns.tolist() #this is the list of genes that are present in the PED file
genes=genes[1:] #first column is sample names, thats why we are removing it
genes=pd.DataFrame(genes,columns=['gene(ensxxx)']) #we added the column name
#since gene names are in the format of gene(ensxxx), we need to extract the gene name and the ensembl id separately
#Extracting text within parentheses into new column 'Code'
genes['uniqueID'] = genes['gene(ensxxx)'].str.extract(r'\((.*?)\)')
# Removing text inside parentheses from 'Gene' column
genes['GENE'] = genes['gene(ensxxx)'].str.replace(r'\(.*?\)', '')
#we remove duplicates because we want to have only one row per gene
genes_no_duplicates=genes.drop_duplicates(subset=['GENE'])
#now we proceed to read the variants matrix which contains CHROM, POS, REF, ALT, GENE
variants_matrix=sys.argv[2]
variants=pd.read_table(variants_matrix,sep='\t', header=0)
#we subset the variants matrix to only have CHROM and GENE, it will be used in further steps
varaiants_with_chr=variants[['CHR','GENE']]
#we then subset only info of interest from the variants matrix
variants=variants[['GENE','POS']]
#we proceed to merge the variants matrix with the genes matrix
merged_variants_and_genes=pd.merge(genes,variants,how='left',on=['GENE'])
#since the merge function does permutations with repeated values, we need to remove duplicates
variants_and_genes_no_duplicates=merged_variants_and_genes.drop_duplicates(subset=['GENE'],keep='first')
#now we merge the variants matrix with the genes matrix, but this time we use the varaiants_with_chr matrix
variants_and_genes_no_duplicates_w_CHR=pd.merge(variants_and_genes_no_duplicates,varaiants_with_chr,how='right',on=['GENE'])
#we again remove duplicates
variants_and_genes_no_duplicates_w_CHR=variants_and_genes_no_duplicates_w_CHR.drop_duplicates(subset=['GENE'],keep='first')