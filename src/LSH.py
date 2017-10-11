#!/usr/bin/env python3

# given a number of "documents", bundle them together into groups
# each groups contains all documents which share a given hash
# given a query document, we are albe to retrieve all similar documents efficiently

import hashlib
import os

def smallHash(number, text):
    """
    Hash some given `text`.
    This function defines a "family" of hash functions,
    each variation is identified by the value of the `number`.
    Output value: a non-negative integer, less than a million. (For now!)
    """
    m = hashlib.md5()
    m.update(bytes(number))
    m.update(text.encode('utf-8'))
    return int(m.hexdigest(), 16) % 1000000

def computeShingles(q, document):
    """
    Produce a list of shingles for a given `document`.
    Shingle width will be `q`.
    """
    shingles = []
    for i in range(len(document) - q + 1):
        shingle = ""
        for j in range(i,i+q):
            shingle += document[j]
        shingles.append(shingle)
    return shingles

def computeHashes(q, hashIDs, document):
    hashes = []
    shingles = computeShingles(q, document)
    if shingles:
        for hashID in hashIDs:
            minHash = min([ smallHash(hashID, shingle)
                            for shingle in shingles ])
            hashes.append(minHash)
        return hashes
    else:
        return None

def computeSignature(q, nbBands, bandSize, document):
    # calculate the vector of hashes
    hashes = computeHashes(q, range(nbBands * bandSize), document)

    if hashes:
        # chop them up
        bands = [ hashes[x : x+bandSize]
                  for x in range(0, len(hashes), bandSize)]

        # return these chopped up hashes, tagged with the band number
        return list(enumerate(bands))
    else:
        return None

def addToStore(q, nbBands, bandSize, documentStore, document):
    signature = computeSignature(q, nbBands, bandSize, document)
    if signature:
        for (bandID, band) in signature:
            sig = smallHash(bandID, str(band))
            if not sig in documentStore.keys():
                documentStore[sig] = set()
            documentStore[sig].add(document)

def lookup(q, nbBands, bandSize, documentStore, document):
    signature = computeSignature(q, nbBands, bandSize, document)
    results = set()
    for (bandID, band) in signature:
        sig = smallHash(bandID, str(band))
        if sig in documentStore:
            for doc in documentStore[sig]:
                results.add(doc)
    return results


def main():
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


    query = "will not confess he owes the malady"

    import fileinput
    import common

    if not os.path.isfile("t8.shakespeare.txt"):
        import urllib.request
        urllib.request.urlretrieve("http://ocw.mit.edu/ans7870/6/6.006/s08/lecturenotes/files/t8.shakespeare.txt", "t8.shakespeare.txt")

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


if __name__ == "__main__":
    main()

