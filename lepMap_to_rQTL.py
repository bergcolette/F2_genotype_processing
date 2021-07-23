# lepMap files are kinda quirky, this is how I process them into a matrix 
# with map locations, genotypes, site names and individual names
# the resulting file can be loaded into rQTL

# import the packages you need 

import pandas as pd
import numpy as np

# read in the data for each linkage group -- here's just one file 

genotype1 = pd.read_csv("~/Desktop/012_files/genotypes1.txt", delimiter = "\t") 

# you don't need all the beginning columns

genotype_1 = genotype1.iloc[5:]
genotype_2 = genotype1.iloc[5:]

# the linkage groups won't be in the same order as those from the physical map, so you can rename them
# you may need to go back to lepMap3 to check which markers ended up in which linkage group
## you can use this command in lepMap for that: cut -f1,2 p.call > cut_pcall.txt
## that will give you a list of the physical site names & where they ended up in the lepMap linkage map

genotype_1['CHR'] = 'linkage_group_name1'
genotype_2['CHR'] = 'linkage_group_name2'

# append the linkage groups together

g_all = genotype_1.append(genotype_2)

# grab the site names from the original matrix that you loaded into lepMap3

siteDF = pd.read_csv("~/Desktop/all_lgs_threshold10_relaxedHets.csv")

# add site names to a temporary dataframe
tmpDF = pd.DataFrame(columns=('MARKER','site'))
tmpDF['site'] = siteDF['indv']

# in lepMap3, the markers are numbered but don't have the marker name from the physical map.
# you can use the marker numbers to merge the spreadsheet with the list of physical marker names.
# make a range from 1 to the number of markers & add to temporary dataframe

x = pd.Series(range(1,1001))
tmpDF['MARKER'] = x

# change the marker number to an integer in both dataframes

tmpDF['MARKER']=tmpDF['MARKER'].astype(int)
g_all['MARKER']=g_all['MARKER'].astype(int)

# merge temp with the genotype dataframe 

inner_join = pd.merge(tmpDF,  
                      g_all,  
                      on ='MARKER',  
                      how ='inner') 
                      
# sort by linkage group order

inner_join = inner_join.sort_values(by=['CHR', 'MALE_POS'], ascending=[True, True])

# filter out unnecessary columns

inner_join = inner_join.drop('FEMALE_POS', axis=1)
inner_join = inner_join.drop('MARKER', axis=1)

# ok, now change the format from AA / AB / BB to A / H / B, which is what rQTL takes

cols = list(inner_join)
cols = cols[3::]

choiceList = ['B', 'H', 'H', 'A']


for i in cols:
    condList = [(inner_join[i] == '2 2'), (inner_join[i] == '1 2'), (inner_join[i] == '2 1'), (inner_join[i] == '1 1')]
    inner_join[i] = np.select(condList, choiceList)

print("done")

# add individual names

names = ['list', 'of', 'names']

inner_join.columns = names

# write to csv! from there it's super easy to transpose in excel and load into rQTL. see avi karn's tutorial for example datasheet: https://avikarn.com/2019-04-17-Genetic-Mapping-in-Lep-MAP3/
inner_join.to_csv("linkageMap.csv")
