# Path census

Measured over **443 exports** holding **1,246,329** distinct Geni profile IDs.

## Paths overall --- 690 files

```
fully covered     175   (25%)
still incomplete  515   (75%)
```

## Incomplete paths

**Every figure here is over the incomplete paths only.** Averaging over all of them mixes the completed paths in as zeros and answers a question nobody asked.

```
average full length     37.9 steps   (median 34)
average missing          8.2         (median 7)
average already held    29.8
-> the average incomplete path is 78% complete
longest path              99 steps   shortest 12
most missing              21         fewest 1
```

## Missing-count distribution

```
  1 missing :   25 paths   <= 3 -> save pages
  2 missing :   32 paths   <= 3 -> save pages
  3 missing :   44 paths   <= 3 -> save pages
  4 missing :   52 paths
  5 missing :   30 paths
  6 missing :   42 paths
  7 missing :   37 paths
  8 missing :   32 paths
  9 missing :   31 paths
 10 missing :   24 paths
 11 missing :   32 paths
 12 missing :   20 paths
 13 missing :   30 paths
 14 missing :   21 paths
 15 missing :   16 paths
 16 missing :   18 paths
 17 missing :   11 paths
 18 missing :    4 paths
 19 missing :    5 paths
 20 missing :    5 paths
 21 missing :    4 paths
```

## Histogram of path lengths

Length is fixed by the saved page --- an export never changes it. Only the missing-count distribution above moves.

```
   1-9 steps :    0 paths  
 10-19 steps :   62 paths  ############
 20-29 steps :  200 paths  ########################################
 30-39 steps :   94 paths  ###################
 40-49 steps :  111 paths  ######################
 50-59 steps :   84 paths  #################
 60-69 steps :   51 paths  ##########
 70-79 steps :   46 paths  #########
   80+ steps :   42 paths  ########
```

## Wikidata isolates

663 paths run to a Wikidata isolate; **441** of those destinations are still absent from the corpus.
