#!/usr/bin/env python3

import common
import statistics
import argparse


def sim_editdistance_mean(l1, l2):
    similarities = [ common.mkStringComparison("editdistance", a, b)
                     for (a,b) in zip(l1, l2)
                   ]
    mean = statistics.mean(similarities)
    return mean

def sim_editdistance_mean_except_missing(l1, l2):
    similarities = [ common.mkStringComparison("editdistance", a, b)
                     for (a,b) in zip(l1, l2)
                     if len(a) > 0 and len(b) > 0
                   ]
    mean = statistics.mean(similarities)
    return mean


################################################################################
# Parsing command line arguments
################################################################################

parser = argparse.ArgumentParser(description='An experiment on learning optimal similarity methods.')
parser.add_argument( '--dataset'
                   , type=str
                   , default="CORA"
                   , help='Which data set to use. Possible values: CORA.' )
parser.add_argument( '-q'
                   , type=int
                   , default=2
                   , help='Shingle width. Default 2.' )
parser.add_argument( '--nb-bands'
                   , type=int
                   , default="5"
                   , help='Number of bands for LSH. Default 5.' )
parser.add_argument( '--band-size'
                   , type=int
                   , default="3"
                   , help='Band size for LSH. Default 3.' )
cmdArgs = parser.parse_args()
print(cmdArgs)


################################################################################
# load data
################################################################################

(_, _, cora_lines_raw) = common.loadCSV("data/cora.csv")

# drop the first column, it is useless
# drop the second column, it contains the ground truth
cora_lines = []
for (i,line) in enumerate(cora_lines_raw):
    cora_lines.append(line[2:])

# if for record numbers i and j,
# cora_truth[i] == cora_truth[j] implies i and j are true-matches.
cora_truth = []
for line in cora_lines_raw:
    cora_truth.append(line[1])


################################################################################
# LSH
################################################################################

import LSH

cora_documentStore = {}
q = cmdArgs.q
nbBands = cmdArgs.nb_bands
bandSize = cmdArgs.band_size

for (i, line) in enumerate(cora_lines):
    LSH.addToStore(q, nbBands, bandSize, cora_documentStore, line)
    if i % 100 == 0 or i+1 == len(cora_lines):
        common.tick("LSH store %6.2f%%" % (100 * (i+1) / len(cora_lines)))

mins = []
maxs = []
means = []
block_sizes = []

for (i, line) in enumerate(cora_lines):
    print("==> %s" % str(line))
    block = LSH.lookup(q, nbBands, bandSize, cora_documentStore, line)
    if block:
        allDistances = [ sim_editdistance_mean_except_missing(line, candidate)
                         for candidate in block
                       ]
        for candidate in block:
            print("*** %s" % str(candidate))
        minD = min(allDistances)
        maxD = max(allDistances)
        meanD = statistics.mean(allDistances)
    else:
        minD = 0
        maxD = 0
        meanD = 0
        print("*** Empty block")

    mins.append(minD)
    maxs.append(maxD)
    means.append(meanD)
    block_sizes.append(len(block))
    common.tick("%4d %4d %8.2f %8.2f %8.2f" % (i, len(block), minD, maxD, meanD))
    print()
    # input()

print("Min  min  value: %8.2f" % min(mins))
print("Min  max  value: %8.2f" % min(maxs))
print("Min  mean value: %8.2f" % min(means))
print("Min  block size: %8.2f" % min(block_sizes))
print()
print("Max  min  value: %8.2f" % max(mins))
print("Max  max  value: %8.2f" % max(maxs))
print("Max  mean value: %8.2f" % max(means))
print("Max  block size: %8.2f" % max(block_sizes))
print()
print("Mean min  value: %8.2f" % statistics.mean(mins))
print("Mean max  value: %8.2f" % statistics.mean(maxs))
print("Mean mean value: %8.2f" % statistics.mean(means))
print("Mean block size: %8.2f" % statistics.mean(block_sizes))
print()



# for (i,l1) in enumerate(cora_lines):
#     for (j,l2) in enumerate(cora_lines):
#         if i < j and l1[0] == l2[0]:
#             print(l1)
#             print(l2)
#             print(sim_editdistance_mean(l1, l2))
#             print(sim_editdistance_mean_except_missing(l1, l2))
#             print()
#             input()
#             # similarities = [ common.mkStringComparison("editdistance", a, b)
#             #                  for (a,b) in zip(l1, l2)
#             #                ]
#             # mean = statistics.mean(similarities)
#             # similarities_nonzero = list(filter(lambda x: x > 0, similarities))
#             # mean_nonzero = statistics.mean(similarities_nonzero)
#             # if mean_nonzero >= 0.5:
#             #     print(i,j)
#             #     print(l1)
#             #     print(l2)
#             #     print(mean, similarities)
#             #     print(mean_nonzero, similarities_nonzero)
#             #     common.tick("")
#             #     print()

common.tick("Done!")

