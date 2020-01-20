import os
import sys
import sh
import ncbi_genome_download as ngd

print("the script has the name %s" % (sys.argv[0]))
print("sp list %s" % (sys.argv[1]))
print("the output directory is %s" % (sys.argv[2]))

with open(sys.argv[1], 'r') as f:
    sp = f.read().splitlines()
output_path = sys.argv[2]

def genome_download(name, output_path):
    path = ''.join([output_path + name.replace(" ","_")])
    os.makedirs(path)
    ngd.download(group = "bacteria", genus = name, file_format = "fasta", parallel = 10, dry_run = True)
    ngd.download(group = "bacteria", genus = name, file_format = "fasta", parallel = 10, dry_run = False, output = path)
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.gz' in file:
                files.append(os.path.join(r, file))

    for f in files:
        sh.gunzip(f)
        
    files2 = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.fna' in file:
                files2.append(os.path.join(r, file))

    out = ''.join([output_path + "/" + name.replace(" ","_") + ".fasta"])
    sh.cat(files2, _out = out)
    return path

#Download Genome Reference
for name in sp:
    path = genome_download(name, output_path)
    print(path)
    delete = ''.join([output_path + "/" + name.replace(" ","_")])
    sh.rm("-rf", delete)

