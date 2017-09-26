
# common functionality here

import csv
import os
import resource
import socket
import statistics
import sys
import time

# febrl
sys.path.append(os.path.expanduser("~/repos/github/stacs-srg/linkage-py/tools/febrl/febrl-0.4.2"))
import stringcmp



hostname = socket.gethostname()

def getMemory():
    if hostname.startswith("manifesto"):
        # manifesto gives us kilobytes
        divisor = 1000
    else:
        # whereas my laptop gives bytes...
        divisor = 1000000
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / divisor



def getTime():
    return time.process_time()



def tick(message):
    print("%-80s %10.2f MB %10.2f secs" % (message, getMemory(), getTime()))
    sys.stdout.flush()



class Date:
    day = None
    month = None
    year = None

    def __init__(self, yearStr, monthStr, dayStr):
        try:
            self.year = int(yearStr)
        except (ValueError, TypeError):
            self.year = None

        try:
            self.month = int(monthStr)
        except (ValueError, TypeError):
            months = {
                'jan': '1',
                'feb': '2',
                'mar': '3',
                'apr': '4',
                'may': '5',
                'jun': '6',
                'jul': '7',
                'aug': '8',
                'sep': '9',
                'oct': '10',
                'nov': '11',
                'dec': '12',
            }
            if monthStr == None:
                self.month = None
            else:
                key = monthStr.lower().strip()
                if key in months.keys():
                    self.month = months[key]
                else:
                    self.month = None

        try:
            self.day = int(dayStr)
        except (ValueError, TypeError):
            self.day = None

    def __str__(self):
        return "%s-%s-%s" % (self.year, self.month, self.day)



def mkDate(yearStr, monthStr, dayStr):
    d = Date(yearStr, monthStr, dayStr)
    return d



# TODO: split date stuff
def mkDateFromYear(year):
    d = Date(year, None, None)
    return d



def mkPlace(one, two):
    if one == "n/e" or one == "": one = None
    if two == "n/e" or two == "": two = None
    if one == two: two = None

    if one == None and two == None:
        return None
    elif one == None:
        return two
    elif two == None:
        return one
    else:
        return "%s %s" % (one, two)



# split from /
# use the first bit
# sometimes the data uses "alterntives"
def mkName(nameStr):
    if nameStr == None:
        return None
    return nameStr.split("/")[0]



def mkGender(genderStr):
    if genderStr == "m":
        return "m"
    elif genderStr == "f":
        return "f"
    else:
        return None



def mkOppositeGender(genderStr):
    if genderStr == "f":
        return "m"
    elif genderStr == "m":
        return "f"
    else:
        return None



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
        valuesArray: [String]
    """
    with open(filepath, newline='\n', encoding="latin-1") as f:
        reader = csv.reader(f, delimiter=delimiter)
        fieldNames = [ x.strip() for x in next(reader) ]
        lenFieldNames = len(fieldNames)
        rawValues = list()
        rawValuesArray = list()
        for row in reader:
            lenValues = len(row)
            if lenFieldNames != lenValues:
                exit("Mismatch in the number of fields, %d vs %d" % (lenFieldNames, lenValues))
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
                rawValuesArray.append(row)
        if verbose >= 1:
            print("Loaded data from %s, %d fields, %s entries." % (filepath, len(fieldNames), len(rawValues)))
        if verbose >= 2:
            print("Following are the fields.")
            for fieldName in fieldNames:
                print(" - %s" % fieldName)
        return (fieldNames, rawValues, rawValuesArray)



# tablefmt='plain' is the simplest, the default
# tablefmt='psql' is nice
# tablefmt='fancy_grid' is also nice, but takes up too much vertical space
def dumpTable(table, selectedFields=None, howmany=None, tablefmt='plain'):
    dump = []
    if selectedFields == None or selectedFields == []:
        selectedFields = []
        # assume all are selected
        for key, value in table[0].items():
            selectedFields.append(key)
    for line in table:
        if howmany != None and len(dump) > howmany:
            break
        dumpline = []
        if selectedFields == None:
            for key, value in line.items():
                dumpline.append(value)
        else:
            for key in selectedFields:
                dumpline.append(line[key])
        dump.append(dumpline)
    print(tabulate.tabulate(dump, selectedFields, tablefmt=tablefmt))



# entity fields are the following.
# in addition, each entity has a Record field denoting the type of record it comes from
#                         and an Entity field denoting the type of entity within the record.
entityFields =  [ "ID"
                , "Location"
                , "Gender"
                , "Name"
                , "Surname"
                , "Occupation"
                , "SpouseName"
                , "SpouseSurname"
                , "SpouseOccupation"
                , "FatherName"
                , "FatherSurname"
                , "FatherOccupation"
                , "MotherName"
                , "MotherSurname"
                , "MotherOccupation"
                , "DateOfRegistry"
                , "DateOfBirth"
                , "DateOfBirth_Day"
                , "DateOfBirth_Month"
                , "DateOfBirth_Year"
                , "DateOfDeath"
                , "DateOfDeath_Day"
                , "DateOfDeath_Month"
                , "DateOfDeath_Year"
                , "DateOfMarriage"
                , "DateOfMarriage_Day"
                , "DateOfMarriage_Month"
                , "DateOfMarriage_Year"
                , "PlaceOfMarriage"
                , "DateOfParentsMarriage"
                , "DateOfParentsMarriage_Day"
                , "DateOfParentsMarriage_Month"
                , "DateOfParentsMarriage_Year"
                , "PlaceOfParentsMarriage"
                , "KnownLinks"
                ]



stringComparisonMethods = [ "exact"
                          , "jaro"
                          , "winkler"
                          , "qgram1short"
                          , "qgram1avrg"
                          , "qgram1long"
                          , "qgram2short"
                          , "qgram2avrg"
                          , "qgram2long"
                          , "qgram3short"
                          , "qgram3avrg"
                          , "qgram3long"
                          , "qgram1Pshort"
                          , "qgram1Pavrg"
                          , "qgram1Plong"
                          , "qgram2Pshort"
                          , "qgram2Pavrg"
                          , "qgram2Plong"
                          , "qgram3Pshort"
                          , "qgram3Pavrg"
                          , "qgram3Plong"
                          , "posqgram1short"
                          , "posqgram1avrg"
                          , "posqgram1long"
                          , "posqgram2short"
                          , "posqgram2avrg"
                          , "posqgram2long"
                          , "posqgram3short"
                          , "posqgram3avrg"
                          , "posqgram3long"
                          , "posqgram1Pshort"
                          , "posqgram1Pavrg"
                          , "posqgram1Plong"
                          , "posqgram2Pshort"
                          , "posqgram2Pavrg"
                          , "posqgram2Plong"
                          , "posqgram3Pshort"
                          , "posqgram3Pavrg"
                          , "posqgram3lPlong"
                          , "sgramshort"
                          , "sgramavrg"
                          , "sgramlong"
                          , "sgramPshort"
                          , "sgramPavrg"
                          , "sgramPlong"
                          , "editdist"
                          , "mod_editdist"
                          , "editex"
                          , "bagdist"
                          , "swdistshort"
                          , "swdistavrg"
                          , "swdistlong"
                          , "syllaldistshort"
                          , "syllaldistavrg"
                          , "syllaldistlong"
                          , "seqmatch"
                          , "compressZLib"
                          , "compressBZ2"
                          # , "compressArith"
                          , "lcs2short"
                          , "lcs2avrg"
                          , "lcs2long"
                          , "lcs3short"
                          , "lcs3avrg"
                          , "lcs3long"
                          , "ontolcs2short"
                          , "ontolcs2avrg"
                          , "ontolcs2long"
                          , "ontolcs3short"
                          , "ontolcs3avrg"
                          , "ontolcs3long"
                          , "permwinkler"
                          , "sortwinkler"
                          ]



allKeyFields = [ [ "Name", "Surname", "Gender"
                 , "DateOfMarriage", "PlaceOfMarriage"
                 , "FatherName", "FatherSurname"
                 , "MotherName", "MotherSurname"
                 , "DateOfParentsMarriage", "PlaceOfParentsMarriage"
                 ]
               , [ "Name", "Surname", "Gender"
                 , "FatherName", "FatherSurname"
                 , "MotherName", "MotherSurname"
                 , "DateOfParentsMarriage", "PlaceOfParentsMarriage"
                 ]
               , [ "Name", "Surname", "Gender"
                 , "FatherName"
                 , "MotherName"
                 , "DateOfParentsMarriage"
                 ]
               , [ "Name", "Surname", "Gender"
                 ]
               ]



def calculateDistance(keyFields, stringComparison, distanceCombiner, a, b):
    distances = {}
    for f in keyFields:
        if a[f] == None or b[f] == None:
            pass
        else:
            distance = stringComparison(a[f],b[f])
            if distance != None:
                distances[f] = distance
            # print("%-60s %-30s %-30s %10.2f" % (f,a[f],b[f],distance))
    combinedDistance = distanceCombiner(distances)
    # print("%-122s %10.2f" % ("combinedDistance",combinedDistance))
    return combinedDistance



def mkStringComparison(methodStr, aStr, bStr):
    aStrCopy = aStr if aStr != None else ""
    bStrCopy = bStr if bStr != None else ""
    if methodStr.startswith('compress'):
        aStrCopy = bytes(aStrCopy, "latin-1")
        bStrCopy = bytes(bStrCopy, "latin-1")
    try:
        return stringcmp.do_stringcmp(methodStr, aStrCopy, bStrCopy)[0]
    except Exception as e:
        filename = "febrl-exceptions-%s.txt" % methodStr
        with open(filename, 'a') as f:
            f.write('stringcmp.do_stringcmp("%s", "%s", "%s")\n' % (methodStr, aStrCopy, bStrCopy))
            f.write(str(e))
            f.write("\n\n")
        return None


# all string comparison methods
# each entry is a tuple: first is a description, second is the function (taking two strings and returning a float)
stringComparisons = [ ( methodStr
                      # PYTHON'S LAMBDAS SUCK
                      # https://docs.python.org/3/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-values-all-return-the-same-result
                      , lambda a, b, methodStr=methodStr:
                            mkStringComparison(methodStr, a, b)
                      )
                      for methodStr in stringComparisonMethods
                    ]



# This is a distanceCombiner
# Takes a simple mean, or 0 if the input list is empty
# "distances" is a dictionary: where the keys are field names, and the values are distances
def simpleMerge(distances):
    if distances == {}:
        return 0
    else:
        return statistics.mean(distances.values())



# all distance combiners
# a distance combiner takes a dictionary as an argument: where the keys are field names, and the values are distances
# it returns a float representing the combined distance
distanceCombiners = [ simpleMerge
                    ]


