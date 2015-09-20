#!/usr/bin/env python
#
# Author: Philip Braunstein
# Group: BioSeq
# Date Created: October 19, 2014
# Last Modified: October 19, 2014
#
# Takes in classification files from ILLUMINA sequencing run as well as
# GreenGenes mapping file to convert all these classification files
# into a single otu table that can go directly into PICRUSt.
#
# The two features are (in the first case HP & RC) are located in the globals
# FEAT_A and FEAT_B.
#

from sys import argv
from sys import exit
import os
import uuid

# CONSTANTS
FEAT_A = "HP"
FEAT_B = "RC"
UNFOUND = "NO_BUG"
MAP = "supportingFiles/97_otu_taxonomy.txt"
DATA_FOLDER = "data/"
CLASSIFICATIONS = "Classification.txt"
OUTPUT_PREFIX = "output/otutable-"

def main():
        if len(argv) != 2:
            usage()

        map = readInMap()
        phylogeny = readInPhylogeny()
        newPhylo = switchNotes(phylogeny, map)
        otuList = getAllOTUs(newPhylo)
        output = OUTPUT_PREFIX + argv[1] + ".txt"
        writeOut(newPhylo, otuList, output)
        print output  # So that run script can know of new file location
        exit(0)

# Prints usage of script then exits non-zero
def usage():
    print "USAGE:", argv[0], "runId"
    exit(1)

# generates the OTU table
def writeOut(newPhylo, otuList, output):
        labels = []
        dicts = []
        for samp in newPhylo.keys():  # Put things lists so order preserved
                labels.append(samp)
                dicts.append(newPhylo[samp])

        with open(output, 'w') as filew:
                filew.write(prepareHeader(labels))
                for otu in otuList:
                        filew.write(otu)
                        for d in dicts:
                                try:
                                        filew.write("\t" + d[otu])
                                except KeyError:
                                        filew.write("\t" + str(0))

                        filew.write("\n")


def prepareHeader(labels):
        return "#OTU_ID" + "\t" + "\t".join(labels) + "\n"
                 


# Makes a list of all the otus seen in the experiment with no
# duplicates
def getAllOTUs(phylogeny):
        toReturn = []

        for samp in phylogeny.keys():
                dictio = phylogeny[samp]

                for otu in dictio.keys():
                        if otu not in toReturn:
                                toReturn.append(otu)

        return toReturn



# Changes out the phylogeny from the string notations to the gg ids
# New key for every dictionary is the ggID instead of the string
def switchNotes(phylogeny, mapd):
        switchLevel(phylogeny)
        toReturn = {}

        for samp in phylogeny.keys():
                newDict = {}
                oldDict = phylogeny[samp]

                for key in oldDict.keys():
                        refDict = mapd[oldDict[key][1]]  # Get right ref dict
                        try:
                                ggID = refDict[key]
                        except KeyError:  # Don't know this phylogeny toss it
                                continue

                        newDict[ggID] = oldDict[key][0]  # Get num reads

                toReturn[samp] = newDict

        return toReturn
                        
                
# Switches out the following Level mappinLevel mappingef switchLevel(phylogeny):
# Kingdom -- k
# Phylum -- p
# Class -- c
# Order -- o
# Family -- f
# Genus -- g
# Species -- s
def switchLevel(phylogeny):
        for sample in phylogeny.keys():
                dictio = phylogeny[sample]
                for key in dictio.keys():
                        dictio[key][1] = dictio[key][1][:1].lower()


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

            if listL[1] in toReturn.keys():
                toReturn[listL[1]][listL[3]] = [listL[4], listL[2]]
            else:
                toReturn[listL[1]] = {listL[3]:[listL[4], listL[2]]}

    return toReturn


# Reads in the GG mapping file into a dictionary such that each key
# is a level of phylogeny, and each value is another dictionary with
# mappings from names to that level of pyhlogeny.
# {"k":{"Bacteria:0001", ...}, "p":{"Baterioides":76372, ...}, ...}
def readInMap():
        toReturn = prepEmptyPhylo()
        with open(MAP, 'r') as filer:
                for line in filer:
                        kvp = parseLine(line)
                        # Pull out the right phylo dict, and add in
                        # the key value pair to that dictionary
                        toReturn[kvp['p']][kvp['k']] = kvp['v']                
        return toReturn


# Returns a dict from that line that has the key (name of bug), val (GG Id),
# and phylolevel (k, c, p, etc.).
# v -- value (gg id)
# p -- phylogeny level (eg. Genus)
# k -- bug name (e.g. Bateroides)
def parseLine(line):
        kvp = {}
        listL = line.strip().split("\t")
        kvp['v'] = listL[0]  # gg ID is val
        phylo = listL[1].split("; ")
        phylo.reverse()

        for level in phylo:
                levelL = level.split("__")
                if levelL[1] != "":
                        kvp['p'] = levelL[0]  # Put in phylolevel
                        kvp['k'] = levelL[1]  # Put in bug name
                        break
        return kvp


# Puts empty dicts for each level of gg phylo into dict
def prepEmptyPhylo():
        toReturn = {}
        toReturn['k'] = {}
        toReturn['p'] = {}
        toReturn['c'] = {}
        toReturn['o'] = {}
        toReturn['f'] = {}
        toReturn['g'] = {}
        toReturn['s'] = {}
        return toReturn


# Prints out the map to stdout, redirect to debug
def tPrintMap(map):
        for key in map.keys():
                print key
                dictio = map[key]
                for k in dictio.keys():
                        print "key = " + k + ", val = " + dictio[k]
                print



if __name__ == '__main__':
        main()
