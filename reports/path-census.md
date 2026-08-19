# Path census

Measured over **393 exports** holding **1,050,854** distinct Geni profile IDs.

## Paths overall --- 690 files

```
fully covered     148   (21%)
still incomplete  542   (79%)
```

## Incomplete paths

**Every figure here is over the incomplete paths only.** Averaging over all of them mixes the completed paths in as zeros and answers a question nobody asked.

```
average full length     39.0 steps   (median 36)
average missing          9.0         (median 8)
average already held    30.0
-> the average incomplete path is 77% complete
longest path              99 steps   shortest 12
most missing              35         fewest 1
```

## Missing-count distribution

```
  1 missing :   18 paths   <= 3 -> save pages
  2 missing :   29 paths   <= 3 -> save pages
  3 missing :   43 paths   <= 3 -> save pages
  4 missing :   52 paths
  5 missing :   28 paths
  6 missing :   40 paths
  7 missing :   37 paths
  8 missing :   34 paths
  9 missing :   33 paths
 10 missing :   26 paths
 11 missing :   32 paths
 12 missing :   24 paths
 13 missing :   35 paths
 14 missing :   25 paths
 15 missing :   17 paths
 16 missing :   19 paths
 17 missing :   17 paths
 18 missing :    5 paths
 19 missing :    8 paths
 20 missing :    7 paths
 21 missing :    5 paths
 22 missing :    5 paths
 24 missing :    2 paths
 35 missing :    1 paths
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

663 paths run to a Wikidata isolate; **478** of those destinations are still absent from the corpus.
