#!/usr/bin/env python

from sys import argv
from sys import exit
import subprocess as sp
import uuid

def main():
    runId = str(uuid.uuid4())
    print "Unique run ID is", runId
    print "Generating OTU table...."
    otuTable = sp.check_output(["./aggregateOTUs.py", runId]).strip()
    print "OTU table:", otuTable, "created."
    print
    print "Randomizing IDs...."
    print "Generating aggregate table...."
    print "Clustering data and making tree visualization...."
    print "Cleaning up...."
    print "Done."


if __name__ == '__main__':
    main()
