module load SAMtools/1.9-foss-2016b

# call variants
bcftools mpileup -Ou -f Bacillus_halotolerans.fna ONT_Bacillus_halotolerans.bam | bcftools call -mv -Oz -o calls.vcf.gz
bcftools index calls.vcf.gz

# normalize indels
bcftools norm -f Bacillus_halotolerans.fna calls.vcf.gz -Ob -o calls.norm.bcf

# filter adjacent indels within 5bp
bcftools filter --IndelGap 5 calls.norm.bcf -Ob -o calls.norm.flt-indels.bcf


bcftools index calls.vcf.gz
cat Bacillus_halotolerans.fna | bcftools consensus calls.vcf.gz > consensus.fa

UNIX/LINUX

minimap2 -ax map-ont --sam-hit-only -t 10 --secondary=no  Bacillus_halotolerans.fasta Bacillus_halotolerans.fasta | samtools sort -o conses_Bacillus_halotolerans.bam

# call variants
bcftools mpileup -Ou -f Bacillus_halotolerans.fasta conses_Bacillus_halotolerans.bam | bcftools call -mv -Oz -o calls.vcf.gz
bcftools index calls.vcf.gz

# normalize indels
bcftools norm -f Bacillus_halotolerans.fasta calls.vcf.gz -Ob -o calls.norm.bcf

# filter adjacent indels within 5bp
bcftools filter --IndelGap 5 calls.norm.bcf -Ob -o calls.norm.flt-indels.bcf