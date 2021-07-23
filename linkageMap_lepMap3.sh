## lepMap3 takes a pedigree file and a posterior file 

## start with a genotype assay matrix in this format: 

## SNP   IND1 IND2 IND3 IND4   ...
## AX-01 AA   AB   BB   NoCall ...
## AX-02 AB   AA   AA   BB     ...
## ...

# then convert it to the right posterior file using the script affx2post.awk
# that script can be downloaded from Pasi's sourceforge here: https://sourceforge.net/projects/lep-map3/files/

# conversion command: 
awk -f affx2post all_lgs_threshold10_relaxedHets_2.21.txt > PCF2_windowData_2.21.post

# I found the pedigree file super unintuitive. 
# If you know who your grandparents are / they are inbred lines, you can keep them in the pedigree file
# honestly making the pedigree was confusing as hell and I still don't understand it in staring at the one I made
# just gonna link to Pasi's instructions: https://sourceforge.net/p/lep-map3/wiki/LM3%20Home/#parentcall2

## here are the commands I use in lepMap3 to make the linkage maps. 

# ParentCall2 -- generates SNP likelihoods
java -cp bin/ ParentCall2 data=pedigree_windows_called.txt posteriorFile=PCF2_windowData_2.21.post > PCF2_windowData.call

# SeparateChromsomes2 - organizes markers into linkage groups. lodLimit and theta are adjustable
# It may take a few rounds of adjusting lod / theta until you find a number of linkage groups that makes sense for your system
java -cp bin/ SeparateChromosomes2  data=PCF2_windowData.call lodLimit=25 theta=0.3 > map=PCF2_map.2.21.txt

# I skip the Filtering2 step because I do my own filtering
# I skip JoinSingles2All bc I didn't have any singletons after OrderMarkers2

# OrderMarkers2 commands are run separately on each linkage group. Each run will have it's own likelihood score -- 
# I ran each linkage group 6 times and selected the output with the highest likelihood score in the log. 
# here's an example of one command for the first chromosome.

java -cp bin/ OrderMarkers2 map=PCF2_map.2.21.txt data=PCF2_windowData.call chromosome=1 sexAveraged=1 selfingPhase=1 useKosambi=1 > PCF2_windows_chr1.1.txt

# once you've selected the runs with the best likelihoods, you want to convert them to an understandable format
# use pasi's script map2genotypes.awk (available here: https://sourceforge.net/projects/lep-map3/files/)

# here's an example with one chromosome (you'll have a separate file for each one)
awk -vfullData=1 -f  map2genotypes.awk PCF2_windows_chr1.5 > genotypes1.txt

# now you have text files with the map location & the genotypes. 
# I do some further processing to get all the linkage groups in one file with the right individual & site names 
# (in another text file)
