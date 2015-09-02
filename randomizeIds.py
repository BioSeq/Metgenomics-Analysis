#!/usr/bin/env python

# Randomizes the IDs in the metagenomics experiment OTU table. Assumes that
# the first row has ID-HP and ID-RC format. Makes it so that the RC and HP from
# the same sample have the same randomized ID.

from sys import argv
from sys import exit
import random

INPUT = "otutable.txt"
OUTPUT = "otutablerandomized.txt"
MAP = "secretMap.txt"

def main():
    process()
    exit(0)

# Reads in file, writes it out with randomized IDs
# Use the first line it finds to make a new header with randomized ids
def process():
    filew = open(OUTPUT, 'w')
    firstLine = True
    with open(INPUT, 'r') as filer:
        for line in filer:
            if firstLine:
                filew.write(createNewHeader(line.strip()))
                firstLine = False
            else:
                filew.write(line)
    filew.close()


# Creates a new header for the file by randomizing the IDs
def createNewHeader(header):
        samples = header.split("\t")
        topLeft = samples[0]  # Get whatever was in the OTU table before
        samples = samples[1:]  # Cut out #OTU
        
        num = len(samples)
        # Make sure that there are an even number of samples
        if num %2 != 0:
            print "ERROR: Uneven Sample Number. Something Wrong"
            exit(1)

        ids = [x.split("-")[0] for x in samples]
        bodySites = [x.split("-")[1] for x in samples]

        # Make array that will have random ids
        newIds = []
        for i in range(num / 2):
            newIds.append(i)
        
        # shuffle this list so there is no correspondance between new and old
        # ids
        random.shuffle(newIds)

        idMap = {}

        currentNewIdCounter = 0
        for oldId in ids:
            if oldId in idMap:
                continue
            idMap[oldId] = str(newIds[currentNewIdCounter])

            currentNewIdCounter += 1

        # Save map for future use
        writeMap(idMap)

        newHL = [idMap[x] for x in ids]

        for i in range(len(bodySites)):
            newHL[i] = newHL[i] + "-" + bodySites[i]
        
        newHS = "\t".join(newHL)
        newHeader = topLeft + "\t" + newHS + "\n"

        return newHeader

# Saves the idMap to a file so that later scripts can remember the mapping
def writeMap(idMap):
    with open(MAP, 'w') as filew:
        for key in idMap.keys():
            filew.write(key + "\t" + idMap[key] + "\n")
        
            

if __name__ == '__main__':
    main()
