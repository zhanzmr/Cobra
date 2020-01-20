import sys
import numpy as np
import pandas as pd
import pysam
import pandas as pd

print("The bam_path is %s" % (sys.argv[1]))
print("The Taxonomy Reference is %s" % (sys.argv[2]))
print("Get top %s species for down stream analysis" % (sys.argv[3]))
print("The output directory is %s" % (sys.argv[4]))

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


def get_abundence(bam_file, tax_file, top_n):
    counts = bam_file['rname'].value_counts()
    counts = counts.reset_index()
    counts.columns = ['rname', 'Counts']
    tax_file.columns =['rname', 'taxonomy']
    tax_file[['Class','Order','Family','Genus','Species']] = tax_file["taxonomy"].str.split(";", n = 10, expand = True).drop(columns=[0, 1])
    tax_file = tax_file.drop('taxonomy', axis=1)
    abundance_all = pd.merge(counts, tax_file, on='rname')
    abundance_top = abundance_all.sort_values(by=['Counts'], ascending=False)[0:int(top_n)-1]
    sp_name = abundance_top['Species'].tolist()
    sp = []
    for name in sp_name:
        name = name.replace("s__", "")
        sp.append(name)
    sp = np.unique(sp).tolist()
    return abundance_all, abundance_top, sp


file_path = sys.argv[1]
top_n = sys.argv[3]
bam_data = bam_to_df(file_path)
output_path = sys.argv[4]
tax = pd.read_csv(sys.argv[2], sep="	", header=None, engine='python')
print("Getting abundance for the sample....")
abundance_all, abundance_top, sp = get_abundence(bam_data, tax, top_n)

abundance_all.to_csv(''.join([output_path + "/abundance_all.csv"]), sep=',')
abundance_top.to_csv(''.join([output_path + "/abundance_top.csv"]), sep=',')
with open(''.join([output_path + "/sp.txt"]), 'w') as f:
    for item in sp:
        f.write("%s\n" % item)


