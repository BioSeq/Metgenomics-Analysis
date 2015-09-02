#!/usr/bin/env Rscript

#
# distMatrixGen.r
# Author: Philip Braunstein
# Date Created: September 3, 2014
# Last Modified: September 2, 2015
#
# Reads in a table of class by sample and creates a distance matrix for
# this data between the samples. This file is saved in the constant OUTPUT.
# This script also generates a tree from the distance matrix that is saved
# as a PDF file.
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

