## This script shows how to make SNP calls from an F2 mapping population into windowed genotype calls. 
## it's useful with a super unwieldy / large datasets where there are many more called sites than there are crossover events in the F2 mapping population. 

# start by reading in an 012 dataframe where individuals are rows and SNPs are columns


df = pd.read_csv('~/path/to/SNPs.csv')
df.drop("Unnamed: 0",axis=1, inplace=True)

# transpose it
tdf = df.set_index('ind').T.reset_index()

# split into one dataframe per linkage group


lg1 = tdf[tdf.chr == 'chr1']
lg2 = tdf[tdf.chr == 'chr2']

# ... repeat for each linkage 

# reset the index
lg1 = lg1.reset_index(drop=True)
lg2 = lg2.reset_index(drop=True)

# create bins of some number of SNPs each in each linkage group
x = # number of snps in bin

bins1 = [i for i in np.arange(lg1.index.min(), lg1.index.max(), x)] + [np.inf]
bins2 = [i for i in np.arange(lg2.index.min(), lg2.index.max(), x)] + [np.inf]

ind_list = [list_of_individuals]

# create dataframes for the loop to write to. 
stats_df1  = pd.DataFrame(columns=["indv_name","count","mean","num_of_nans_chr1"])
stats_df2  = pd.DataFrame(columns=["indv_name","count","mean","num_of_nans_chr2"])

# cut each linkage group into bins of x SNPs each.
cut_bins1 = pd.cut(lg1.index,bins=bins1)
cut_bins2 = pd.cut(lg2.index,bins=bins2)

#loop through and create dataframes of the means, count, and number of nans in each window for each indv.
#these are big/long dataframes so this will take a while


for col in small_list:
    mdf = lg1[['index',col]]
    asdf = mdf.groupby(cut_bins1)[col].agg(['mean','count'])
    asdf["num_of_nans_chr1"] = 12 - asdf["count"]
    asdf["indv_name"] = col
    stats_df1  = stats_df1.append(asdf)
print("df1 done")
    
for col in small_list:
    mdf = lg2[['index',col]]
    asdf = mdf.groupby(cut_bins2)[col].agg(['mean','count'])
    asdf["num_of_nans_chr2"] = 12 - asdf["count"]
    asdf["indv_name"] = col
    stats_df2  = stats_df2.append(asdf)
print("df2 done")    


## if num of nans is > a cuttoff, this should be counted as an NA
cutoff = # cutoff number

stats_df1.loc[stats_df1['num_of_nans_chr1'] > cutoff, 'mean'] = np.nan
stats_df2.loc[stats_df2['num_of_nans_chr2'] > cutoff, 'mean'] = np.nan

#ok, now that we've replaced the problematic windows witn nans
#we want a wide table, with just the means. don't worry about the warnings, the command is deprecated.

stats_df1_narrow = stats_df1[['indv_name', 'mean']]
stats_df1_narrow['bin'] = stats_df1.index
stats_df1_wide = stats_df1_narrow.pivot_table(index='bin', columns='indv_name', values='mean', aggfunc='first', dropna=False)

stats_df2_narrow = stats_df2[['indv_name', 'mean']]
stats_df2_narrow['bin'] = stats_df2.index
stats_df2_wide = stats_df2_narrow.pivot_table(index='bin', columns='indv_name', values='mean', aggfunc='first', dropna=False)

## let's append all the linkage groups together

one_two = stats_df1_wide.append(stats_df2_wide, ignore_index=True)

## loop through & convert to genotypes. The windows are based on the distributions 
##some windows will be NAs because of amibiguity

choiceList = ['BB', 'AA', 'AB']

for i in small_list:
    condList = [(all_lgs[i] > .75), (all_lgs[i] < .25), ((all_lgs[i] < .75) & (all_lgs[i] > .25))]
    all_lgs[i] = np.select(condList, choiceList)
    
# replace 0's with NaNs

for i in small_list:
    all_lgs[i].replace('0',np.nan,inplace=True)
    print("done with all_lgs")

# write it to .csv
all_lgs.to_csv("all_lgs.csv")


