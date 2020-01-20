#! /usr/bin/Rscript

args = commandArgs(trailingOnly=TRUE)
## program...
if (!require("seqinr")) install.packages("seqinr")
library(seqinr)

fasta_file = args[1]
file_dir <- args[2]
print("Reading the fasta sample file.....")
fastafile<- read.fasta(file = fasta_file, 
                       seqtype = "AA",as.string = TRUE, set.attributes = FALSE)

file.id <- sort(list.files(file_dir, full.names = T))
file <- sort(list.files(file_dir, full.names = F))
file <- sub(".txt", "", file, fixed = TRUE)
print("Subsetting the fasta file....")
for (n in 1:length(file)){
  temp <- read.table(file.id[n], quote="\"", comment.char="", stringsAsFactors=FALSE)
  sub <- fastafile[names(fastafile) %in% temp$V1]
  write.fasta(sequences = sub, names = names(sub), nbchar = 2000, file.out = paste0(file_dir,"/",file[n],".fasta"))
}
