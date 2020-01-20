#!/bin/bash
echo "sample_name is $1"
echo "fasta/fastq file is $2"
echo "reference_file is $3"
echo "top number of species is $4"
echo "Number of thread is $5"
echo "output_directory is $6"
sample="$1"
reference="$3"
ori_file="$2"


minimap2 -ax map-ont --sam-hit-only -t $5 --secondary=no $reference $ori_file | samtools sort -o $sample/$sample.bam
# Species level analysis, output abundance_all, abundance_top and sp.txt (species name)
python ./python/species_analysis.py BC01.bam Taxonomy_final.txt 15 ./
# Download reference genome for top species
python ./python/genome_download.py sp.txt ./database
# Get fasta header for each species
python ./python/fasta_id_sp.py sp.txt BC01.bam abundance_all.csv ./fasta
# Subset fasta 
Rscript --vanilla ./python/subset_fasta.R BC01.fasta fasta/
rm ./fasta/*.txt 


# Minimap the fasta with 
fasta=(./fasta/*.fasta)
gen_ref=(./database/*.fna)
echo "${#fasta[@]}"
echo "${#gen_ref[@]}"

echo "${fasta[1]}"
echo "${gen_ref[1]}"

n=${#fasta[@]}
counter=1
while [ $counter -le $n ]
do
    minimap2 -ax map-ont --sam-hit-only -t $5 --secondary=no ${gen_ref[$counter]} ${fasta[$counter]} | samtools sort -o ./alignment/$(basename "$fasta[$counter]").bam
    echo $counter
    ((counter++))
done

# Strain level process
for name in ./database/*.fna 
do
    grep "^>" $name > strain_id.txt
    sed 's/,.*//' strain_id.txt | sed 's/ /,/' | sed 's/.*>//' > id_$name.txt
    rm strain_id.txt
done

mkdir ./strain_count
for bam in ./alignment/*.bam
do
    samtools view $bam | cut -f3 | sort | uniq -c > ./strain_count/count_$(basename "$bam").txt
done

# Get strain abundance table for the top species
python ./python/strain_analysis.py ./strain_count/ ./strain_abundance sp.txt

##### Strain consistant sequence analysis ######
# Get fasta header for each species
python ./python/fasta_id_strain.py ./alignment ./strain_abundance ./strain_id sp.txt
# Subset for each strain
Rscript --vanilla ./python/subset_strain_fasta.R BC01.fasta strain_id/
# Conse sequence




# 