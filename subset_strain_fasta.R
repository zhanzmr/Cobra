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

file.id <- sort(list.dirs(path = file_dir, full.names = TRUE, recursive = F))
for (n in 1:length(file.id)){
  file2.id <- sort(list.files(file.id[n], full.names = T))
  file2 <- sort(list.files(file.id[n], full.names = F))
  file <- sub("_id.txt", "", file2, fixed = TRUE)
  for (xx in 1:length(file2.id)){
    temp <- read.table(file2.id[xx], quote="\"", comment.char="", stringsAsFactors=FALSE)
    sub <- fastafile[names(fastafile) %in% temp$V1]
    write.fasta(sequences = sub, names = names(sub), nbchar = 2000, file.out = paste0(file.id[n],"/",file[xx],".fasta"))
    print(xx)
  }
  print(n)
}
