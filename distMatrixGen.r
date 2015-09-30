#!/usr/bin/env Rscript
#
# distMatrixGen.r
# Author: Philip Braunstein
# Copyright (c) 2015 BioSeq
#
# Creates a distance matrix and clustered tree based on the microbes in each
# sample.
#

# Command Line args
args <- commandArgs(TRUE)

# CONSTANTS
INPUT <-  args[1]
UUID <- args[2]
OUTPUT_1 <- paste("output/distMatrix-Genus-", UUID, ".txt", sep="")
OUTPUT_2 <- paste("output/clustered-Genus-", UUID, ".pdf", sep="")

mydata <- read.table(INPUT, header=TRUE, sep="\t")

row.names(mydata)<-mydata$SAMPLE  # Relabel rows

mydata <- mydata[-1]  # Delete first column (labels)

# Create the distance object and matrix from this object
distObj <- dist(mydata)
euclidean <- as.matrix(distObj)
row.names(euclidean) <- row.names(mydata)

size <- dim(euclidean)[1]

# Add size to the distance matrix to write out
fileConn <- file(OUTPUT_1)
writeLines(c(paste(size)), fileConn)
close(fileConn)

write.table(euclidean, file=OUTPUT_1, append=TRUE, sep="\t", quote=F, col.names=F)

clustered <- hclust(distObj, method="complete", members=NULL)


pdf(OUTPUT_2, width=15, height=5)
plot(clustered, main = "Cluster by Genus")
print(as.name(paste(OUTPUT_1, OUTPUT_2)))

