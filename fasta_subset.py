import pyfaidx as pyf
import os

os.chdir("/mnt/c/Users/mengr/Documents/ONT_doc/BC01_analysis")
genes = pyf.Fasta('BC01.fasta')
fna = "Bacillus_halotolerans.txt"

with open(fna, 'r') as f:
    sp = f.read().splitlines()



