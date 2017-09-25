#!/usr/bin/env python3

# given a number of "documents", bundle them together into groups
# each groups contains all documents which share a given hash
# given a query document, we are albe to retrieve all similar documents efficiently

import zlib
import fileinput

def smallHash(t):
    # return hash(t) % 100
    # return zlib.adler32(t.encode('utf-8')) % 100
    # return zlib.adler32(t.encode('utf-8')) % 100000
    return zlib.adler32(t.encode('utf-8'))

def getShingles(q, document):
    shingles = []
    for i in range(len(document) - q + 1):
        shingle = ""
        for j in range(i,i+q):
            shingle += document[j]
        shingles.append(shingle)
    return shingles

def computeHashes(q, hashIDs, document, verbose=0):
    hashes = []
    shingles = getShingles(q, document)
    for hashID in hashIDs:
        if verbose >= 2:
            for shingle in shingles:
                h = smallHash(str(hashID) + shingle)
                print("   hash(%-2d, %-20s) = %d" % (hashID, shingle, h))
        minHash = min([ smallHash(str(hashID) + shingle)
                        for shingle in shingles ])
        if verbose >= 1:
            print("minHash(%-2d, %-20s) = %d" % (hashID, document, minHash))
        if verbose >= 2:
            print()
        hashes.append(minHash)
    return hashes

def computeSignature(q, hashIDs, document):
    hashes = computeHashes(q, range(nbBands * bandSize), document)
    bands = [ hashes[x : x+bandSize]
              for x in range(0, len(hashes), bandSize)]

    signature = []
    for (bandID, band) in enumerate(bands):
        h = smallHash(str(bandID) + str(band))
        signature.append(h)
    return signature


def addToStore(q, nbBands, bandSize, documentStore, document):
    try:
        signature = computeSignature(q, range(nbBands * bandSize), document)
        # print("addToStore", document, signature)
        for sig in signature:
            if not sig in documentStore.keys():
                documentStore[sig] = set()
            documentStore[sig].add(document)
    except:
        pass

def lookup(q, nbBands, bandSize, documentStore, document):
    signature = computeSignature(q, range(nbBands * bandSize), document)
    # print("lookup", document, signature)
    results = set()
    for sig in signature:
        if sig in documentStore:
            for doc in documentStore[sig]:
                results.add(doc)
    return results


documentStore = {}
q = 5
nbBands = 3
bandSize = 10

def add(doc):
    addToStore(q, nbBands, bandSize, documentStore, doc)

def lu(doc):
    return lookup(q, nbBands, bandSize, documentStore, doc)

# add("ozgur")
# add("akgun")
# add("ozgun")
# print(lookup(q, nbBands, bandSize, documentStore, "ozgut"))


import common

query = "will not confess he owes the malady"

i = 0
for line in fileinput.input(["t8.shakespeare.txt"]):
    line = line.lower().strip()
    i += 1
    if i < 10000:
        add(line)
        if i % 1000 == 0:
            common.tick("Line %d, Store %d" % (i, len(documentStore)))
            print("lookup:", len(lookup(q, nbBands, bandSize, documentStore, query)))
            for result in list(lookup(q, nbBands, bandSize, documentStore, query))[:10]:
                print("\t" + result)



