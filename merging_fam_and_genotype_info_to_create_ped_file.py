import pandas as pd
import numpy as np
import sys

#this script is meant to merge the fam file with the genotype file to create a ped file
#fam file is a external  file that contains the family information
#genotype file is the file that contains the genotype information, it can be a LOF matrix
fid_iid_external=sys.argv[1]
fid_and_iid = pd.read_table(fid_iid_external,sep=' ',names=['FID','IID','motherID', 'FatherID', 'SEX', 'PHENO'])
genotype_file=sys.argv[2]
geno_file=pd.read_table(genotype_file, sep=' ',header=None)
geno_and_fam=pd.merge(geno_file,fid_and_iid,how='inner',on=['IID'])
geno_and_fam_col_names=geno_and_fam.columns.tolist()
new_col_order = ['FID','IID','FatherID','motherID','SEX', 'PHENO']+geno_and_fam_col_names[:-5]
geno_and_fam_new_order = geno_and_fam[new_col_order]
column_position = 6  # Index of the column to be deleted (0-based index)
geno_and_fam_final = geno_and_fam_new_order.iloc[:, [i for i in range(len(geno_and_fam_new_order.columns)) if i != column_position]]
##now we will save the file
directory_of_output=sys.argv[3]
geno_and_fam_final.to_csv(f'{directory_of_output}',sep=' ',index=False,header=False)








