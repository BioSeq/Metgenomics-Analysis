#!/usr/bin/env python

from sys import argv
from sys import exit
import subprocess as sp
import uuid

def main():
    runId = str(uuid.uuid4())
    print "Unique run ID is", runId
    print
    print "Generating OTU table...."
    otuTable = sp.check_output(["./aggregateOTUs.py", runId]).strip()
    print "OTU table:", otuTable
    print

    print "Randomizing IDs...."
    packing1 = sp.check_output(["./randomizeIds.py", otuTable,\
                                                runId]).strip().split()
    randomOtuTable = packing1[0]
    mapFile = packing1[1]

    print "Randomized OTU table:", randomOtuTable
    print "ID Mapping File:", mapFile
    print

    print "Generating aggregate table...."
    aggTable = sp.check_output(["./createAggregateTable.py", mapFile,
                                            runId]).strip()
    print "Aggregated OTU table:", aggTable
    print

    print "Clustering data and making tree visualization...."
    packing2 = sp.check_output(["./distMatrixGen.r", aggTable, 
                                runId]).strip().split()
    print "Distance Matrix:", packing2[0]
    print "Clustered Tree:", packing2[1]
    print
    print "Done."


if __name__ == '__main__':
    main()
