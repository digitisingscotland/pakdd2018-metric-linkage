#!/usr/bin/env python3

import common
import statistics

(_, _, cora_lines) = common.loadCSV("data/cora.csv")

for (i,l1) in enumerate(cora_lines):
    for (j,l2) in enumerate(cora_lines):
        if i != j:
            similarities = [ common.mkStringComparison("editdistance", a, b)
                             for (a,b) in zip(l1, l2)
                           ]
            mean = statistics.mean(similarities)
            similarities_nonzero = list(filter(lambda x: x > 0, similarities))
            mean_nonzero = statistics.mean(similarities_nonzero)
            if mean_nonzero >= 0.5:
                print(i,j)
                print(l1)
                print(l2)
                print(mean, similarities)
                print(mean_nonzero, similarities_nonzero)
                common.tick("")
                print()

common.tick("Done!")
