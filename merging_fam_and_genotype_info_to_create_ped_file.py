import pandas as pd
import numpy as np
import sys
fid_iid_external=sys.argv[1]
fid_and_iid = pd.read_table(fid_iid_external,sep=' ',names=['FID','IID'])
fid_and_iid['fatherID']=0
fid_and_iid['motherID']=0
fid_and_iid['SEX']=0
fid_and_iid['PHENO']=0
genotype_file=sys.argv[2]
geno_file=pd.read_table(genotype_file, sep=' ',header=None)
colnames=geno_file.columns.tolist()
colnames[0]='IID'
geno_file.columns=colnames
geno_and_fam=pd.merge(geno_file,fid_and_iid,how='inner',on=['IID'])
geno_and_fam_col_names=geno_and_fam.columns.tolist()
new_col_order = ['FID','IID','fatherID','motherID','SEX', 'PHENO']+geno_and_fam_col_names[:-5]
geno_and_fam_new_order = geno_and_fam[new_col_order]
column_position = 6  # Index of the column to be deleted (0-based index)
geno_and_fam_final = geno_and_fam_new_order.iloc[:, [i for i in range(len(geno_and_fam_new_order.columns)) if i != column_position]]
##now we will save the file
name_and_location_of_where_to_save_file=sys.argv[3]
geno_and_fam_final.to_csv(f'{name_and_location_of_where_to_save_file}',sep=' ',index=False,header=False)








