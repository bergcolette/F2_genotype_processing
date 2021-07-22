## here are the steps I walk through to filter in an F2 mapping population.
## I recommend running these code chunks in a jupyter notebook. 

## First, let's filter based on positive controls.
## In an F2 mapping population where individuals are aligned to a 
## reference genome that matches one of the parents and parent A, parent B, 
## and F1's are included in the dataset, sites can be filtered based on 
## the positive controls


import numpy as np
import pandas as pd

from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype

#read in data (this should be an 012 matrix of SNPs where columns are SNPs and rows are individual names)
df = pd.read_csv("~/path/to/SNP/matrix.csv")

#transpose the matrix
tdf = df.set_index('ind').T.reset_index()

#filter based on parent B -- for parent B, every SNP should be the alt (2)
mtdf = tdf[tdf["ParentB"] != 0]
mtdf = mtdf[mtdf["ParentB"] != 1]

#filter based on parent A -- for parent B, every SNP should be the ref (0)
mtdf = tdf[tdf["ParentA"] != 1]
mtdf = mtdf[mtdf["ParentA"] != 2]

#filter based on F1's -- every SNP should be the het (1)
mtdf = tdf[tdf["F1"] != 0]
mtdf = mtdf[mtdf["F1"] != 2]

# write the filtered SNPs to a csv
mtdf.to_csv("filtered_genotypes.csv", index = False)


## here's how you filter based on other criteria (ie, the transmission ratios)
## F2 mapping populations, generally, should be in HWE (1:2:1 ref:het:alt).
## BUT, there's all kinds of biologically possible reasons for your SNPs to be out of HWE (see Fishman & McIntosh 2019)
## therefore, this takes visualization. There aren't strict cutoffs that work in every case. 
## you may have done some prior filtering in vcftools based on HWE -- 
## personally I like to filter in vcftools based on coverage / phred quality and do the rest of the filtering this way. 


# read in data (this should be an 012 matrix of SNPs where columns are SNPs and rows are individual names)
df = pd.read_csv("filtered_genotypes.csv")
df1 = df.set_index('index').T.reset_index()

# make a list of all the sites (these are the same as column names)
siteList = list(df)

refCount = []
hetCount = []
altCount = []

# make a dataframe containing chr numbers and site numbers
tmpDF = pd.DataFrame(columns=['genome','chr','site'])
tmpDF[['genome','chr','site']] = df['index'].str.split('_', expand=True)

# loop through and count all the ref, het, and alt genotypes at each site
for i in siteList:
    countRef = (df1[i]==0).sum()
    refCount.append(countRef)

for i in siteList:
    countHet = (df1[i]==1).sum()
    hetCount.append(countHet)

for i in siteList:
    countAlt = (df1[i]==2).sum()
    altCount.append(countAlt)
    
# remove first column
altCount = altCount[1::]
hetCount = hetCount[1::]
refCount= refCount[1::]

# convert from int to numeric
altCount = pd.to_numeric(altCount)
hetCount = pd.to_numeric(hetCount)
refCount = pd.to_numeric(refCount)

# calculate the sum
total = altCount + hetCount + refCount

refRatio = np.divide(refCount, total)
hetRatio = np.divide(hetCount, total)
altRatio = np.divide(altCount, total)

# now add your ratios back to the genotype matrix

df['refRatio'] = refRatio
df['hetRatio'] = hetRatio
df['altRatio'] = altRatio

# add in the chr and site names from the tmp dataframe you made before
t_df['chr'] = tmpDF['chr']
t_df['site'] = tmpDF['site']


# here I recommend visualizing the transmission ratios by plotting the het, alt, and ref ratios. you can do this with a package called bokeh. 

from bokeh.io import output_file, show
from bokeh.layouts import row
from bokeh.layouts import column
from bokeh.plotting import figure

# I do one plot for each chromosome but I'll just do one for the first chromosome here
df_c1 = df[df["chr"] == 1]

# prepare some data
t_1x = df_c1['site']
t_1y = df_c1['refRatio']
t_1y1 = df_c1['hetRatio']
t_1y2 = df_c1['altRatio']

t_1x = pd.to_numeric(t1_x)

# output to static HTML file
output_file("genotype_ratios.html", title="Genotype Ratios")

# create a new plot with a title and axis labels
t_1 = figure(title="chr1", x_axis_label='site', y_axis_label='Ratio')

# add a line renderer with legend and line thickness
t_1.circle(t_1x, t_1y, legend="refRatio", line_width=2, color="blue")
t_1.circle(t_1x, t_1y1, legend="hetRatio", line_width=2, color="purple")
t_1.circle(t_1x, t_1y2, legend="altRatio", line_width=2, color="red")

# plot the figure!
show(t_1)

# you then may choose to filter based on a cutoff of extremely distorted ratios. 
# Here it's good to fiddle around with it -- try different cutoffs and then visualize again. 

refRatioCutoff = x
hetRatioCutoff = y
altRatioCutoff = z
 
# again, this is about fiddling around. You'll probably want to set an upper and lower limit for some of these.

t_df_filt = t_df[t_df["refRatio"]] > x
t_df_filt = t_df_filt[t_df_filt["hetRatio"]] > y
t_df_filt = t_df[t_df["altRatio"]] > z

# visualize it again to see if it looks cleaner, or if it looks like the filtering was too extreme / biased. 
# do a few cycles of filter -> vis -> filter
# once you feel good about it, you are ready for downstream analyses!

