import sys
import pandas as pd
import os
import pysam

print("Bam file is  %s" % (sys.argv[1]))
print("Directory of strain abundance table is  %s" % (sys.argv[2]))
print("Output dir is %s" % (sys.argv[3]))
print("File of list of species name is %s" % (sys.argv[4]))

#bamfile = "./alignment"
#abundance_all = "./strain_abundance"
#output_path = "./strain_id"
#sp = "sp.txt"
#os.chdir("/mnt/c/Users/mengr/Documents/ONT_doc/BC01_analysis")


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

bamfile = sys.argv[1]
abundance_all = sys.argv[2]
output_path = sys.argv[3]
sp = sys.argv[4]
os.makedirs(output_path)


bams = []
for r, d, f in os.walk(bamfile):
    for file in f:
        if '.bam' in file:
                bams.append(os.path.join(r, file))

abundance = []
for r, d, f in os.walk(abundance_all):
    for file in f:
        if '.csv' in file:
                abundance.append(os.path.join(r, file))

with open(sp, 'r') as f:
    sp = f.read().splitlines()


print("Finding fasta header for each strain...")

for x in range(0, 11):
    diree = ''.join(["./strain_id/" + sp[x].replace(" ","_")])
    os.makedirs(diree)
    abundance_table = pd.read_csv(abundance[x], header=0)
    bam_data = bam_to_df(bams[x])
    strain_name = abundance_table['rname'].tolist()
    for strain in strain_name:
#        temp_strain = abundance_table[abundance_table['rname']==strain]['rname'].tolist()
        fasta_id = bam_data[bam_data['rname']==strain]['qname'].tolist()
        file_name = ''.join(["./strain_id/" + sp[x].replace(" ","_") + "/" + strain + "_id.txt"])
        with open(file_name, 'w') as f:
            for item in fasta_id:
                f.write("%s\n" % item)


