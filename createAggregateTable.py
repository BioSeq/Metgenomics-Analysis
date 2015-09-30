#!/usr/bin/env python
#
# createAggregrateTable.py
# Author: Philip Braunstein
# Copyright (c) 2015 BioSeq
#
# Generates aggrgate tables where each row correspondes to one sample and each
# column corresponds to the fraction of a microbe in the given sample. This is
# needed to create the distance matrix for the clustering in a later script.
#

# CONSTANTS
# Parameters
LEVEL = "Genus"
OUTPUT_PREFIX = "output/aggregateTable_" + LEVEL + "-" 
DATA_FOLDER = "data/"
CLASSIFICATIONS = "Classification.txt"

# Indices
FILE_NAME_IND = 1
LEVEL_IND = 2
GROUP_IND = 3
PERC_IND = 5

from sys import argv
from sys import exit
import os

def main():
    if len(argv) != 3:
            usage()
    
    files = [x for x in os.listdir(DATA_FOLDER) if\
                            x.startswith("Classification")]

    samples = readInPhylogeny()

    idMap = readInMap(argv[1])

    groups = findAllGroups(samples)

    output = OUTPUT_PREFIX + argv[2] + ".txt"

    writeOut(samples, groups, idMap, output)

    print output

    exit(0)


# Reads in the map that has the same randomized sample names as were used to
# generate the OTU table. Returned as a mapping from oldIds to newIds (dict)
def readInMap(mapFile):
    toReturn = {}
    with open(mapFile, 'r') as filer:
        for line in filer:
            listL = line.strip().split("\t")
            toReturn[listL[0]] = listL[1]

    return toReturn


# Prints correct invocation of script and exits non-zero
def usage():
    print "USAGE:", argv[0], "mapFile runId"
    exit(1)


# Returns a dictionary of dictionaries. The key of the outer dictionary
# is the sample name (e.g. 9ss-HP). The key of each the inner dictionary is 
# the phylogeny, and the value is a list of number of reads and level.
# Assumes classifications file is in the data folder and called
# Classification.txt
# {5ss_RC:{Bacteria:[2342342, Kingdom], ...}
# Filters out Unclassified reads
def readInPhylogeny():
    toReturn = {}
    with open(os.path.join(DATA_FOLDER, CLASSIFICATIONS)) as filer:
        for line in filer:
            if line.startswith("SampleNumber"):  # Skip header
                continue
            
            listL = line.strip().split("\t")

            # Skip unclassified reads
            if listL[3] == 'Unclassified':
                continue

            # Skip entries not of the correct level
            if listL[LEVEL_IND] != LEVEL:
                continue

            if listL[FILE_NAME_IND] in toReturn.keys():
                toReturn[listL[FILE_NAME_IND]][listL[GROUP_IND]] =\
                                                            listL[PERC_IND]
            else:
                toReturn[listL[FILE_NAME_IND]] = \
                                    {listL[GROUP_IND]:listL[PERC_IND]}

    return toReturn



# Reads through all of the keys of all of the dictionaries in the list 
# passed in. This function returns a list of all of the keys. Each key
# is reported only once. 
def findAllGroups(samples):
    toReturn = []

    for samp in samples.keys():
        for key in samples[samp].keys():
            if key not in toReturn:
                toReturn.append(key)

    return toReturn


# Writes a new file with percentages in each group as the column for each
# sample as the row. The samples and sampleNames are parallel lists, so that
# they match up.
def writeOut(samples, groups, idMap, output):
    with open(output, 'w') as filew:
        # Make header for file
        filew.write("SAMPLE")
        for bug in groups:
            filew.write("\t" + bug)
        filew.write("\n")

        # File in table
        for samp in samples.keys():
            filew.write(mystifyName(samp, idMap))

            for bug in groups:
                # Bugs not seen marked 0%
                try:
                    filew.write("\t" + samples[samp][bug])
                except KeyError:  
                    filew.write("\t0")

            filew.write("\n")


# Splits original name on dashes, and then looks up what the new name is from
# idMap, then puts the former ending back on. If T is mapped to 19, then T-HP
# gets mapped to 19-HP
def mystifyName(origName, idMap):
    listL = origName.split("-")

    return idMap[listL[0]] + "-" + listL[1]
        

if __name__ == '__main__':
        main()
