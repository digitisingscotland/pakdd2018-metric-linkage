#!/usr/bin/env python3

import matplotlib
matplotlib.use("cairo")
import matplotlib.pyplot as plt

import csv, sys

def loadCSV(filepath, delimiter=",", verbose=0):
    """
    Load a table from a given CSV/TSV file.

    Input
        filepath   : String
        delimiter  : String
        verbose    : Int{0..2}

    Returns
        fieldNames : [String]                   -- headings
        values     : [Dict String String]       -- values, each entry is a dictionary with fieldNames as the keys
    """
    with open(filepath, newline="\n", encoding="latin-1") as f:
        reader = csv.reader(f, delimiter=delimiter)
        try:
            fieldNames = [ x.strip() for x in next(reader) ]
        except:
            exit("Cannot read line from: %s" % filepath)
        lenFieldNames = len(fieldNames)
        rawValues = list()
        for row in reader:
            lenValues = len(row)
            if lenFieldNames != lenValues:
                exit("Mismatch in the number of fields, %d vs %d\nfilepath: %s" % (lenFieldNames, lenValues, filepath))
            row2 = {}
            allNone = True
            for i in range(0, lenFieldNames):
                col = row[i].strip()
                if col == "n/e" or col == "":
                    row2[fieldNames[i]] = None
                else:
                    row2[fieldNames[i]] = col
                    allNone = False
            # do not insert into the flatTable if all entries are None
            if not allNone:
                rawValues.append(row2)
        if verbose >= 1:
            print("Loaded data from %s, %d fields, %s entries." % (filepath, len(fieldNames), len(rawValues)))
        if verbose >= 2:
            print("Following are the fields.")
            for fieldName in fieldNames:
                print(" - %s" % fieldName)
        return (fieldNames, rawValues)


(fields, stats) = loadCSV("stats.tsv", delimiter="\t")

for f in fields:
    print("Field: " + f)


################################################################################
# Plotting Linkage Quality
################################################################################

def plotLQ(title, predicate):
    plt.clf()

    w,h = plt.figaspect(0.5)
    plt.figure(figsize=(w,h))

    font = {"family":"sans-serif", "weight":"normal", "size":24}
    plt.rc("font", **font)
    plt.rcParams["text.usetex"] = True

    plt.title("Linkage Quality w.r.t. Threshold", fontsize=22)
    plt.suptitle(title, y = 1.02, fontsize=28)

    plt.xlabel("Threshold")
    plt.ylabel("Linkage Quality")

    plt.xlim(0, 100)
    plt.ylim(-0.05, 1.05)
    plt.grid()

    data = [ line for line in stats if predicate(line) ]

    plt.plot( [ line["Distance Threshold"]  for line in data ]
            , [ line["Precision"]           for line in data ]
            , color="blue"
            , marker="o"
            , label="Precision"
            )

    plt.plot( [ line["Distance Threshold"]  for line in data ]
            , [ line["Recall"]              for line in data ]
            , color="green"
            , marker="o"
            , label="Recall"
            )

    plt.plot( [ line["Distance Threshold"]  for line in data ]
            , [ line["F1 Measure"]          for line in data ]
            , color="red"
            , marker="o"
            , label="F1 Measure"
            )

    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    plt.savefig("plotLQ -- %s.png" % title, bbox_inches="tight")
    plt.close()
    print("plotLC -- %s.png" % title)


dataset = "Cora"


linker = "Brute Force"
title = " - ".join([dataset, linker])
predicate = lambda line: line["Data Set (Source)"] == dataset and line["Linker"] == linker
plotLQ(title, predicate)


linker = "TradBlocking"
predicate = lambda line: line["Data Set (Source)"] == dataset and line["Linker"] == linker
blockingMethods = set([ line["Blocking Method"] for line in stats if predicate(line) ])
for blockingMethod in blockingMethods:
    title = " - ".join([dataset, linker, blockingMethod])
    predicate = lambda line: line["Data Set (Source)"] == dataset and line["Linker"] == linker and line["Blocking Method"] == blockingMethod
    plotLQ(title, predicate)


linker = "MTree"
title = " - ".join([dataset, linker])
predicate = lambda line: line["Data Set (Source)"] == dataset and line["Linker"] == linker
plotLQ(title, predicate)


linker = "LSH"
predicate = lambda line: line["Data Set (Source)"] == dataset and line["Linker"] == linker
shingleSizes = set([ line["Shingle size"] for line in stats if predicate(line) ])
nbBandss = set([ line["Number of bands"] for line in stats if predicate(line) ])
bandSizes = set([ line["Band size"] for line in stats if predicate(line) ])
for shingleSize in shingleSizes:
    for nbBands in nbBandss:
        for bandSize in bandSizes:
            title = " - ".join([dataset, linker, shingleSize, nbBands, bandSize])
            predicate = lambda line: line["Data Set (Source)"] == dataset and line["Linker"] == linker and line["Shingle size"] == shingleSize and line["Number of bands"] == nbBands and line["Band size"] == bandSize
            plotLQ(title, predicate)






################################################################################
# Plotting Blocking Completeness
################################################################################

def plotPQC(title, predicate):
    plt.clf()

    w,h = plt.figaspect(0.5)
    plt.figure(figsize=(w,h))

    font = {"family":"sans-serif", "weight":"normal", "size":24}
    plt.rc("font", **font)
    plt.rcParams["text.usetex"] = True

    plt.title("Linkage Quality w.r.t. Threshold", fontsize=22)
    plt.suptitle(title, y = 1.02, fontsize=28)

    plt.xlabel("Threshold")
    plt.ylabel("Blocking Quality \& Completeness")

    plt.xlim(0, 100)
    plt.ylim(-0.05, 1.05)
    plt.grid()

    data = [ line for line in stats if predicate(line) ]

    plt.plot( [ line["Distance Threshold"]          for line in data ]
            , [ line["Average pairs quality"]       for line in data ]
            , color="green"
            , marker="o"
            , label="Pairs Quality"
            )

    plt.plot( [ line["Distance Threshold"]          for line in data ]
            , [ line["Average pairs completeness"]  for line in data ]
            , color="red"
            , marker="o"
            , label="Pairs Completeness"
            )

    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    plt.savefig("plotPQC -- %s.png" % title, bbox_inches="tight")
    plt.close()
    print("plotPQC -- %s.png" % title)



dataset = "Cora"


linker = "Brute Force"
title = " - ".join([dataset, linker])
predicate = lambda line: line["Data Set (Source)"] == dataset and line["Linker"] == linker
plotPQC(title, predicate)


linker = "TradBlocking"
predicate = lambda line: line["Data Set (Source)"] == dataset and line["Linker"] == linker
blockingMethods = set([ line["Blocking Method"] for line in stats if predicate(line) ])
for blockingMethod in blockingMethods:
    title = " - ".join([dataset, linker, blockingMethod])
    predicate = lambda line: line["Data Set (Source)"] == dataset and line["Linker"] == linker and line["Blocking Method"] == blockingMethod
    plotPQC(title, predicate)


linker = "MTree"
title = " - ".join([dataset, linker])
predicate = lambda line: line["Data Set (Source)"] == dataset and line["Linker"] == linker
plotPQC(title, predicate)


linker = "LSH"
predicate = lambda line: line["Data Set (Source)"] == dataset and line["Linker"] == linker
shingleSizes = set([ line["Shingle size"] for line in stats if predicate(line) ])
nbBandss = set([ line["Number of bands"] for line in stats if predicate(line) ])
bandSizes = set([ line["Band size"] for line in stats if predicate(line) ])
for shingleSize in shingleSizes:
    for nbBands in nbBandss:
        for bandSize in bandSizes:
            title = " - ".join([dataset, linker, shingleSize, nbBands, bandSize])
            predicate = lambda line: line["Data Set (Source)"] == dataset and line["Linker"] == linker and line["Shingle size"] == shingleSize and line["Number of bands"] == nbBands and line["Band size"] == bandSize
            plotPQC(title, predicate)

