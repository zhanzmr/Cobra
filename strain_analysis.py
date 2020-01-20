import sys
import numpy as np
import pandas as pd
import pysam
import os

print("Strain ref is %s" % (sys.argv[1]))
print("The output directory is %s" % (sys.argv[2]))

path = "./strain_count/"
out_path = "./strain_abundance"
sp = "sp.txt"


#path = sys.argv[1]
#out_path = sys.argv[2]

os.makedirs(out_path)
files = []
for r, d, f in os.walk(path):
    for file in f:
        if '.txt' in file:
                files.append(os.path.join(r, file))

path_ref = './database'
files_ref = []
for r, d, f in os.walk(path_ref):
    for file in f:
        if '.txt' in file:
                files_ref.append(os.path.join(r, file))

with open(sp, 'r') as f:
    sp = f.read().splitlines()


for i in range(len(files)):
    name = sp[i]
    data = pd.read_csv(files[i], header=None, delim_whitespace=True)
    data.columns = ['Counts', 'rname']
    ref = pd.read_csv(files_ref[i], header=None, sep=',')
    ref.columns = ['rname', 'Strain']
    abundance = pd.merge(ref, data, on='rname')
    abundance.to_csv(''.join([out_path + "/" + name.replace(" ","_") + "_all.csv"]), sep=',')






