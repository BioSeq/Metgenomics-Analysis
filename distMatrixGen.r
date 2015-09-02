#!/usr/bin/env Rscript

#
# distMatrixGen.r
# Author: Philip Braunstein
# Date Created: September 3, 2014
# Last Modified: September 3, 2014
#
# Reads in a table of class by sample and creates a distance matrix for
# this data between the samples. This file is saved in the constant OUTPUT.
# This script also generates a tree from the distance matrix that is saved
# as a PDF file.
#

# CONSTANTS
INPUT <- "aggregateTable_Species.txt"
OUTPUT <- "classDistMatrixSpecies.txt"

mydata <- read.table(INPUT, header=TRUE, sep="\t")

row.names(mydata)<-mydata$SAMPLE  # Relabel rows

mydata <- mydata[-1]  # Delete first column (labels)

# Create the distance object and matrix from this object
distObj <- dist(mydata)
euclidean <- as.matrix(distObj)
row.names(euclidean) <- row.names(mydata)

size <- dim(euclidean)[1]

# Add size to the distance matrix to write out
fileConn <- file(OUTPUT)
writeLines(c(paste(size)), fileConn)
close(fileConn)

write.table(euclidean, file=OUTPUT, append=TRUE, sep="\t", quote=F, col.names=F)

clustered <- hclust(distObj, method="complete", members=NULL)


pdf("Species.pdf", width=15, height=5)
plot(clustered, main = "Cluster by Species")

