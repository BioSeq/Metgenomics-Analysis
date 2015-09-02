#!/usr/bin/env python

#
# createAggregrateTable.py
# Author: Philip Braunstein
# Date Created: September 2, 2014
# Last Modified: September 2, 2014
#
# Takes in Classification files generated from metagenomics app on Basespace and
# creates a table that the percentages of each microbe by sample.
#
# The level of phylogeny and output file name are both constants that can 
# be changed.
#
# This script DOES NOT check that the files provided on the command line
# are formatted correctly. Undefined behavior may result from use of this
# script with improperly formatted files.
#

# CONSTANTS
# Parameters
LEVEL = "Genus"
OUTPUT_FILE = "aggregateTable_" + LEVEL + ".txt"
MAP = "secretMap.txt"

# Indices
FILE_NAME_IND = 1
LEVEL_IND = 2
GROUP_IND = 3
PERC_IND = 5

from sys import argv
from sys import exit

def main():
        if len(argv) < 2:
                print "ERROR: At least one sample file required"
                usage()
        
        files = argv[1:]  # Don't include script name in files to read

        samples = readInAllFiles(files)

        idMap = readInMap()

        sampleNames = getSampleNames(files, idMap)
        
        groups = findAllGroups(samples)

        writeOut(samples, sampleNames, groups)

        exit(0)

# Reads in the map that has the same randomized sample names as were used to
# generate the OTU table. Returned as a mapping from oldIds to newIds (dict)
def readInMap():
    toReturn = {}
    with open(MAP, 'r') as filer:
        for line in filer:
            listL = line.strip().split("\t")
            toReturn[listL[0]] = listL[1]

    return toReturn


# Prints correct invocation of script and exits non-zero
def usage():
        print "USAGE:", argv[0], "SAMPLE_FILES"
        exit(1)


# Uses helper function to read in all of the files provided on
# the command line. Returns a list of dictionaries.
def readInAllFiles(files):
        samples = []

        for fileToRead in files:
                samples.append(readIn(fileToRead))

        return samples


# Reads in a sample file. Calls usage() if the file is not a valid format
# returns a dictionary of the form {FILE_NAME:{LEVEL:PERCENTAGE}}
# WARNING: This function does not check if the file is a valid file type.
def readIn(toRead):
        toReturn = {}

        with open(toRead, 'r') as filer:
               for line in filer:
                        listL = line.strip().split("\t")

                        if listL[LEVEL_IND] == LEVEL:  # Get correct level
                                toReturn[listL[GROUP_IND]] = listL[PERC_IND]

        return toReturn


# Looks at the second line in each file to get the sample name
# Returns the a list of these file names
def getSampleNames(files, idMap):
        toReturn = []
        for fileToRead in files:
                with open(fileToRead, 'r') as filer:
                        filer.readline()
                        listL = filer.readline().strip().split("\t")
                        name = listL[FILE_NAME_IND]

                        # Randomized names inserted here
                        nameList = name.split("-")
                        name = idMap[nameList[0]] + "-" + nameList[1]

                toReturn.append(name)

        return toReturn


# Reads through all of the keys of all of the dictionaries in the list 
# passed in. This function returns a list of all of the keys. Each key
# is reported only once. 
def findAllGroups(samples):
        toReturn = []

        for samp in samples:
                for key in samp.keys():
                        if key not in toReturn:
                                toReturn.append(key)

        return toReturn


# Writes a new file with percentages in each group as the column for each
# sample as the row. The samples and sampleNames are parallel lists, so that
# they match up.
def writeOut(samples, sampleNames, groups):
        with open(OUTPUT_FILE, 'w') as filew:
                # Make header for file
                filew.write("SAMPLE")
                for bug in groups:
                        filew.write("\t" + bug)
                filew.write("\n")

                # Fill in body of table
                for x in range(len(samples)):
                        filew.write(sampleNames[x])

                        for bug in groups:
                                # Bugs not seen marked 0%
                                try:
                                        filew.write("\t" + samples[x][bug])
                                except KeyError:  
                                        filew.write("\t0")

                        filew.write("\n")
        

if __name__ == '__main__':
        main()
