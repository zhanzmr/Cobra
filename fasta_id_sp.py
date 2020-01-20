import sys
import pandas as pd
import os
import pysam

print("File of list of species name is %s" % (sys.argv[1]))
print("Bam file is %s" % (sys.argv[2]))
print("Directory of speics abundance table is  %s" % (sys.argv[3]))
print("Output dir is %s" % (sys.argv[4]))

def bam_to_df(bam_path):
    '''
    loop through bam and output dataframe
    '''
    bam = pysam.AlignmentFile(bam_path, "rb")
    rname = []
    qname = []
    pos = []
    for read in bam:
        rname.append(read.reference_name)
        qname.append(read.qname)
        pos.append(read.pos)
    return pd.DataFrame({'rname': rname, 'qname': qname, 'pos': pos})

bamfile = sys.argv[2]
abundance_all = sys.argv[3]
output_path = sys.argv[4]
sp = sys.argv[1]
os.makedirs(output_path)

with open(sp, 'r') as f:
    sp = f.read().splitlines()


print("Finding fasta header for each strain...")
abundance = pd.read_csv(abundance_all, header=0)
bam_data = bam_to_df(bamfile)

print("Getting fasta ID reading for next analysis...")
# subset fasta file
for name in sp:
    s__name = [''.join(["s__" + name])]
    temp_specie = abundance[abundance['Species'].isin(s__name)]['rname'].tolist()
    fasta_id = bam_data[bam_data['rname'].isin(temp_specie)]['qname'].tolist()
    file_name = ''.join([output_path + "/" + name.replace(" ","_") + ".txt"])
    with open(file_name, 'w') as f:
        for item in fasta_id:
            f.write("%s\n" % item)


#with open(sys.argv[1], 'r') as f:
#    sp = f.read().splitlines()


#for x in range(0, 11):
#    abundance_table = pd.read_csv(abundance[x], header=0)
#    bam_data = bam_to_df(bams[x])
#    
#    with open(file_name, 'w') as f:
#        for item in fasta_id:
#            f.write("%s\n" % item)

#for x in range(2, 6):
#bams = []
#for r, d, f in os.walk(bamfile):
#    for file in f:
#        if '.bam' in file:
#                bams.append(os.path.join(r, file))

#abundance = []
#for r, d, f in os.walk(abundance_all):
#    for file in f:
#        if '.csv' in file:
#                abundance.append(os.path.join(r, file))