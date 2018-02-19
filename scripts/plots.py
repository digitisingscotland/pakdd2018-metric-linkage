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


def toFloat(s):
    if s == "NA":
        return 0
    else:
        return float(s)


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
    # plt.rcParams["text.usetex"] = True

    # plt.title("Linkage Quality w.r.t. Threshold", fontsize=22)
    # plt.suptitle(title, y = 1.02, fontsize=28)

    plt.xlabel("Distance Threshold")
    plt.ylabel("Linkage Quality")

    data = [ line for line in stats if predicate(line) ]

    plt.xlim( min([ toFloat(line["Distance Threshold"]) for line in data ])
            , max([ toFloat(line["Distance Threshold"]) for line in data ])
            )
    plt.ylim(-0.05, 1.05)
    plt.grid()

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
            , label="F-measure"
            )

    # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.legend()

    plt.savefig("plotLQ -- %s.eps" % title, bbox_inches="tight")
    plt.close()
    print("plotLQ -- %s.eps" % title)


dataset = "Cora"

linker = "Brute Force"
title = " - ".join([dataset, linker])
predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and line["Linker"] == linker
plotLQ(title, predicate)


linker = "TradBlocking"
predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and line["Linker"] == linker
blockingMethods = set([ line["Blocking Method"] for line in stats if predicate(line) ])
for blockingMethod in blockingMethods:
    title = " - ".join([dataset, linker, blockingMethod])
    predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and line["Linker"] == linker and line["Blocking Method"] == blockingMethod
    plotLQ(title, predicate)


linker = "MTree"
title = " - ".join([dataset, linker])
predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and line["Linker"] == linker
plotLQ(title, predicate)


linker = "LSH"
predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and line["Linker"] == linker
shingleSizes = set([ line["Shingle size"] for line in stats if predicate(line) ])
nbBandss = set([ line["Number of bands"] for line in stats if predicate(line) ])
bandSizes = set([ line["Band size"] for line in stats if predicate(line) ])
for shingleSize in shingleSizes:
    for nbBands in nbBandss:
        for bandSize in bandSizes:
            title = " - ".join([dataset, linker, shingleSize, nbBands, bandSize])
            predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and line["Linker"] == linker and line["Shingle size"] == shingleSize and line["Number of bands"] == nbBands and line["Band size"] == bandSize
            plotLQ(title, predicate)


dataset = "Skye"

linker = "MTree"
title = " - ".join([dataset, linker])
predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and line["Linker"] == linker
plotLQ(title, predicate)


linker = "LSH"
predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and line["Linker"] == linker
shingleSizes = set([ line["Shingle size"] for line in stats if predicate(line) ])
nbBandss = set([ line["Number of bands"] for line in stats if predicate(line) ])
bandSizes = set([ line["Band size"] for line in stats if predicate(line) ])
for shingleSize in shingleSizes:
    for nbBands in nbBandss:
        for bandSize in bandSizes:
            title = " - ".join([dataset, linker, shingleSize, nbBands, bandSize])
            predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and line["Linker"] == linker and line["Shingle size"] == shingleSize and line["Number of bands"] == nbBands and line["Band size"] == bandSize
            plotLQ(title, predicate)


dataset = "Kilmarnock"

linker = "MTree"
title = " - ".join([dataset, linker])
predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and line["Linker"] == linker
plotLQ(title, predicate)


linker = "LSH"
predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and line["Linker"] == linker
shingleSizes = set([ line["Shingle size"] for line in stats if predicate(line) ])
nbBandss = set([ line["Number of bands"] for line in stats if predicate(line) ])
bandSizes = set([ line["Band size"] for line in stats if predicate(line) ])
for shingleSize in shingleSizes:
    for nbBands in nbBandss:
        for bandSize in bandSizes:
            title = " - ".join([dataset, linker, shingleSize, nbBands, bandSize])
            predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and line["Linker"] == linker and line["Shingle size"] == shingleSize and line["Number of bands"] == nbBands and line["Band size"] == bandSize
            plotLQ(title, predicate)






################################################################################
# Plotting Blocking Completeness
################################################################################

def plotBQ(title, predicate):
    plt.clf()

    w,h = plt.figaspect(0.5)
    plt.figure(figsize=(w,h))

    font = {"family":"sans-serif", "weight":"normal", "size":24}
    plt.rc("font", **font)
    # plt.rcParams["text.usetex"] = True

    plt.title("Block Quality", fontsize=22)
    plt.suptitle(title, y = 1.02, fontsize=28)

    plt.xlabel("Distance Threshold")
    plt.ylabel("Proportion")

    data = [ line for line in stats if predicate(line) ]

    plt.xlim( min([ toFloat(line["Distance Threshold"]) for line in data ])
            , max([ toFloat(line["Distance Threshold"]) for line in data ])
            )
    plt.ylim(-0.05, 1.05)
    plt.grid()

    plt.plot( [         line["Distance Threshold"]          for line in data ]
            , [ toFloat(line["Average links quality"])       for line in data ]
            , color="green"
            , marker="o"
            , label="Block Quality"
            )

    # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.legend()

    plt.savefig("plotBQ -- %s.eps" % title, bbox_inches="tight")
    plt.close()
    print("plotBQ -- %s.eps" % title)



def plotPQC(title, predicate):
    plt.clf()

    w,h = plt.figaspect(0.5)
    plt.figure(figsize=(w,h))

    font = {"family":"sans-serif", "weight":"normal", "size":24}
    plt.rc("font", **font)
    # plt.rcParams["text.usetex"] = True

    plt.title("Pairs Quality and Completeness", fontsize=22)
    plt.suptitle(title, y = 1.02, fontsize=28)

    plt.xlabel("Distance Threshold")
    plt.ylabel("Proportion")

    data = [ line for line in stats if predicate(line) ]

    plt.xlim( min([ toFloat(line["Distance Threshold"]) for line in data ])
            , max([ toFloat(line["Distance Threshold"]) for line in data ])
            )
    plt.ylim(-0.05, 1.05)
    plt.grid()

    plt.plot( [         line["Distance Threshold"]          for line in data ]
            , [ toFloat(line["Average pairs quality"])       for line in data ]
            , color="green"
            , marker="o"
            , label="Pairs Quality"
            )

    plt.plot( [         line["Distance Threshold"]          for line in data ]
            , [ toFloat(line["Average pairs completeness"])  for line in data ]
            , color="red"
            , marker="o"
            , label="Pairs Completeness"
            )

    # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.legend()

    plt.savefig("plotPQC -- %s.eps" % title, bbox_inches="tight")
    plt.close()
    print("plotPQC -- %s.eps" % title)



dataset = "Cora"


linker = "Brute Force"
title = " - ".join([dataset, linker])
predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and line["Linker"] == linker
plotBQ(title, predicate)
plotPQC(title, predicate)


linker = "TradBlocking"
predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and line["Linker"] == linker
blockingMethods = set([ line["Blocking Method"] for line in stats if predicate(line) ])
for blockingMethod in blockingMethods:
    title = " - ".join([dataset, linker, blockingMethod])
    predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and line["Linker"] == linker and line["Blocking Method"] == blockingMethod
    plotBQ(title, predicate)
    plotPQC(title, predicate)


linker = "MTree"
title = " - ".join([dataset, linker])
predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and line["Linker"] == linker
plotBQ(title, predicate)
plotPQC(title, predicate)


linker = "LSH"
predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and line["Linker"] == linker
shingleSizes = set([ line["Shingle size"] for line in stats if predicate(line) ])
nbBandss = set([ line["Number of bands"] for line in stats if predicate(line) ])
bandSizes = set([ line["Band size"] for line in stats if predicate(line) ])
for shingleSize in shingleSizes:
    for nbBands in nbBandss:
        for bandSize in bandSizes:
            title = " - ".join([dataset, linker, shingleSize, nbBands, bandSize])
            predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and line["Linker"] == linker and line["Shingle size"] == shingleSize and line["Number of bands"] == nbBands and line["Band size"] == bandSize
            plotBQ(title, predicate)
            plotPQC(title, predicate)


dataset = "Skye"


linker = "MTree"
title = " - ".join([dataset, linker])
predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and line["Linker"] == linker
plotBQ(title, predicate)
plotPQC(title, predicate)


linker = "LSH"
predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and line["Linker"] == linker
shingleSizes = set([ line["Shingle size"] for line in stats if predicate(line) ])
nbBandss = set([ line["Number of bands"] for line in stats if predicate(line) ])
bandSizes = set([ line["Band size"] for line in stats if predicate(line) ])
for shingleSize in shingleSizes:
    for nbBands in nbBandss:
        for bandSize in bandSizes:
            title = " - ".join([dataset, linker, shingleSize, nbBands, bandSize])
            predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and line["Linker"] == linker and line["Shingle size"] == shingleSize and line["Number of bands"] == nbBands and line["Band size"] == bandSize
            plotBQ(title, predicate)
            plotPQC(title, predicate)


dataset = "Kilmarnock"


linker = "MTree"
title = " - ".join([dataset, linker])
predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and line["Linker"] == linker
plotBQ(title, predicate)
plotPQC(title, predicate)


linker = "LSH"
predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and line["Linker"] == linker
shingleSizes = set([ line["Shingle size"] for line in stats if predicate(line) ])
nbBandss = set([ line["Number of bands"] for line in stats if predicate(line) ])
bandSizes = set([ line["Band size"] for line in stats if predicate(line) ])
for shingleSize in shingleSizes:
    for nbBands in nbBandss:
        for bandSize in bandSizes:
            title = " - ".join([dataset, linker, shingleSize, nbBands, bandSize])
            predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and line["Linker"] == linker and line["Shingle size"] == shingleSize and line["Number of bands"] == nbBands and line["Band size"] == bandSize
            plotBQ(title, predicate)
            plotPQC(title, predicate)





################################################################################
# Traditional Blocking at Threshold 70
################################################################################

def plotFixedThresholdTraditional1(title, blockingMethods, predicate):
    plt.clf()

    w,h = plt.figaspect(0.5)
    plt.figure(figsize=(w,h))

    font = {"family":"sans-serif", "weight":"normal", "size":24}
    plt.rc("font", **font)
    # plt.rcParams["text.usetex"] = True

    plt.title("Block Quality", fontsize=22)
    plt.suptitle(title, y = 1.02, fontsize=28)

    plt.xlabel("Blocking Strategy")
    plt.ylabel("Proportion")

    data = [ line for line in stats if predicate(line) ]

    # plt.xlim([ line["Blocking Method"]       for line in data ]            )
    # plt.xlim([ line["Blocking Method"] for line in data ])
    plt.ylim(-0.05, 1.05)
    plt.grid()


    xRange = blockingMethods
    plt.xticks(range(len(xRange)), xRange)

    # fig, axs = plt.subplots()
    plt.plot( range(len(xRange))
            , [ line["Precision"]                       for blockingMethod in blockingMethods
                                                        for line in data if line["Blocking Method"] == blockingMethod ]
            , color="blue"
            , marker="o"
            , label="Precision"
            )
    plt.plot( range(len(xRange))
            , [ line["Recall"]                          for blockingMethod in blockingMethods
                                                        for line in data if line["Blocking Method"] == blockingMethod ]
            , color="green"
            , marker="o"
            , label="Recall"
            )
    plt.plot( range(len(xRange))
            , [ line["F1 Measure"]                      for blockingMethod in blockingMethods
                                                        for line in data if line["Blocking Method"] == blockingMethod ]
            , color="red"
            , marker="o"
            , label="F-measure"
            )

    # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.legend()

    plt.savefig("plotFixedThresholdTraditional1 -- %s.eps" % title, bbox_inches="tight")
    plt.close()
    print("plotFixedThresholdTraditional1 -- %s.eps" % title)


def plotFixedThresholdTraditional2(title, blockingMethods, predicate):
    plt.clf()

    w,h = plt.figaspect(0.5)
    plt.figure(figsize=(w,h))

    font = {"family":"sans-serif", "weight":"normal", "size":24}
    plt.rc("font", **font)
    # plt.rcParams["text.usetex"] = True

    plt.title("Block Quality", fontsize=22)
    plt.suptitle(title, y = 1.02, fontsize=28)

    plt.xlabel("Blocking Strategy")
    plt.ylabel("Proportion")

    data = [ line for line in stats if predicate(line) ]

    # plt.xlim([ line["Blocking Method"]       for line in data ]            )
    # plt.xlim([ line["Blocking Method"] for line in data ])
    plt.ylim(-0.05, 1.05)
    plt.grid()


    xRange = blockingMethods
    plt.xticks(range(len(xRange)), xRange)

    plt.plot( range(len(xRange))
            , [ line["Average pairs quality"]           for blockingMethod in blockingMethods
                                                        for line in data if line["Blocking Method"] == blockingMethod ]
            , color="blue"
            , marker="o"
            , label="Pairs quality"
            )
    plt.plot( range(len(xRange))
            , [ line["Average pairs completeness"]      for blockingMethod in blockingMethods
                                                        for line in data if line["Blocking Method"] == blockingMethod ]
            , color="green"
            , marker="o"
            , label="Pairs completeness"
            )

    # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.legend()

    plt.savefig("plotFixedThresholdTraditional2 -- %s.eps" % title, bbox_inches="tight")
    plt.close()
    print("plotFixedThresholdTraditional2 -- %s.eps" % title)


def plotFixedThresholdLSH(title, predicate):
    plt.clf()

    w,h = plt.figaspect(0.5)
    plt.figure(figsize=(w,h))

    font = {"family":"sans-serif", "weight":"normal", "size":24}
    plt.rc("font", **font)
    # plt.rcParams["text.usetex"] = True

    plt.title("Block Quality", fontsize=22)
    plt.suptitle(title, y = 1.02, fontsize=28)

    plt.xlabel("Blocking Strategy")
    plt.ylabel("Proportion")

    data = [ line for line in stats if predicate(line) ]

    # plt.xlim([ line["Blocking Method"]       for line in data ]            )
    # plt.xlim([ line["Blocking Method"] for line in data ])
    plt.ylim(-0.05, 1.05)
    plt.grid()

    xRange = [ line["Number of bands"] + " " + line["Band size"]                 for line in data ]
    plt.xticks(range(len(xRange)), xRange)

    # fig, axs = plt.subplots()
    plt.plot( range(len(xRange))
            , [ line["Precision"]                       for line in data ]
            , color="blue"
            , marker="o"
            , label="Precision"
            )
    plt.plot( range(len(xRange))
            , [ line["Recall"]                          for line in data ]
            , color="green"
            , marker="o"
            , label="Recall"
            )
    plt.plot( range(len(xRange))
            , [ line["F1 Measure"]                      for line in data ]
            , color="red"
            , marker="o"
            , label="F-measure"
            )

    plt.plot( range(len(xRange))
            , [ line["Average pairs quality"]           for line in data ]
            , color="purple"
            , marker="o"
            , label="Pairs quality"
            )
    plt.plot( range(len(xRange))
            , [ line["Average pairs completeness"]      for line in data ]
            , color="pink"
            , marker="o"
            , label="Pairs completeness"
            )

    # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.legend()

    plt.savefig("plotFixedThresholdLSH -- %s.eps" % title, bbox_inches="tight")
    plt.close()
    print("plotFixedThresholdLSH -- %s.eps" % title)




dataset = "Cora"


linker = "TradBlocking"
threshold = 70
predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and line["Linker"] == linker and toFloat(line["Distance Threshold"]) == threshold
blockingMethods = ['5', '3', '7', '10', '8', '9', 'all']
print(blockingMethods)
title = " - ".join([dataset, linker, "70"])
plotFixedThresholdTraditional1(title, blockingMethods, predicate)
plotFixedThresholdTraditional2(title, blockingMethods, predicate)


linker = "LSH"
threshold = 70
predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and line["Linker"] == linker and toFloat(line["Distance Threshold"]) == threshold
title = " - ".join([dataset, linker, "70"])
plotFixedThresholdLSH(title, predicate)









################################################################################
# Plotting F-Measures against each other
################################################################################

def plotFs(title, measure, predicate):
    title = " - ".join([title, measure])
    plt.clf()

    w,h = plt.figaspect(0.5)
    plt.figure(figsize=(w,h))

    font = {"family":"sans-serif", "weight":"normal", "size":24}
    plt.rc("font", **font)
    # plt.rcParams["text.usetex"] = True

    # plt.title("Linkage Quality w.r.t. Threshold", fontsize=22)
    # plt.suptitle(title, y = 1.02, fontsize=28)

    plt.xlabel("Distance Threshold")
    plt.ylabel(measure)

    data = [ line for line in stats if predicate(line) ]

    plt.xlim( min([ toFloat(line["Distance Threshold"]) for line in data ])
            , max([ toFloat(line["Distance Threshold"]) for line in data ])
            )
    plt.ylim(-0.05, 1.05)
    plt.grid()

    shingleSizes = set([ line["Shingle size"] for line in data if predicate(line) ])
    nbBandss = set([ line["Number of bands"] for line in data if predicate(line) ])
    bandSizes = set([ line["Band size"] for line in data if predicate(line) ])
    for shingleSize in shingleSizes:
        for nbBands in nbBandss:
            for bandSize in bandSizes:

                dataLSH = [ line for line in data if line["Linker"] == "LSH" and line["Shingle size"] == shingleSize and line["Number of bands"] == nbBands and line["Band size"] == bandSize ]

                plt.plot( [ line["Distance Threshold"]  for line in dataLSH ]
                        , [ line[measure]               for line in dataLSH ]
                        , color="blue"
                        , marker="o"
                        , label="LSH"
                        )

    dataMTree = [ line for line in data if line["Linker"] == "MTree" ]

    plt.plot( [ line["Distance Threshold"]  for line in dataMTree ]
            , [ line[measure]               for line in dataMTree ]
            , color="red"
            , marker="o"
            , label="M-tree"
            )

    # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    from collections import OrderedDict

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())


    plt.savefig("plotFs -- %s.eps" % title, bbox_inches="tight")
    plt.close()
    print("plotFs -- %s.eps" % title)


dataset = "Cora"
title = " - ".join([dataset])
predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and toFloat(line["Distance Threshold"]) <= 30
plotFs(title, "Precision", predicate)
plotFs(title, "Recall", predicate)
plotFs(title, "F-measure", predicate)


dataset = "Skye"
title = " - ".join([dataset])
predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and toFloat(line["Distance Threshold"]) <= 30
plotFs(title, "Precision", predicate)
plotFs(title, "Recall", predicate)
plotFs(title, "F-measure", predicate)


dataset = "Kilmarnock"
title = " - ".join([dataset])
predicate = lambda line: line["Data Set (Source)"].startswith(dataset) and toFloat(line["Distance Threshold"]) <= 30
plotFs(title, "Precision", predicate)
plotFs(title, "Recall", predicate)
plotFs(title, "F-measure", predicate)

