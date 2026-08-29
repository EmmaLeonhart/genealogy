# ------------------------------------------------------------------------
# THE LAST BOND. After this, Arne Garborg is continuously linked to Charlemagne.
#
# Emma, 2026-08-29, having just run the daily batch: "generate the quickstatements
#   so I am able to get charlemagne properly connected".
#
# MEASURED, NOT ASSUMED. scripts/check-spine-bonds.py over
#   paths/charlemagne-to-arne-garborg.tsv, one batched wbgetentities request for
#   all 34 items, run after her batch landed:
#
#       32 of 33 consecutive pairs bonded
#       the one break: steps 22-23, Q141216349 and Q19061035 state nothing
#       about each other
#
# Her batch created the two people the line was missing and closed three of the
#   four breaks by itself:
#       step 15  Ramborg Knutsdotter Lejon  -> Q141216350   (closed 14-15, 15-16)
#       step 22  Ingrid Guttormsdotter      -> Q141216349   (closed 21-22)
#
# WHY THIS ONE COULD NOT BE IN THAT BATCH, and it is not a sequencing problem.
#   `LAST P22 Q19061035` would have worked inside it -- Guttorm has existed for
#   years. The builder only emits a link when the far end is in `have`, and
#   `have` is her ledger; Guttorm is on Wikidata carrying P2600
#   6000000001200156499 but is not in the ledger, so the pipeline never knew it
#   was allowed to point at him.
#
# Ingrid is step 22, Guttorm is step 23, and the path's relation column reads
#   "her father" -- so it is P22 downward and P40 back.
# ------------------------------------------------------------------------
#   Q141216349 Ingrid Guttormsdotter: P22 father = Q19061035 Guttorm Àsulfsson à Rein
Q141216349	P22	Q19061035	S2600	"6000000000771986019"
#   Q19061035 Guttorm Àsulfsson à Rein: P40 child = Q141216349 Ingrid Guttormsdotter
Q19061035	P40	Q141216349	S2600	"6000000000771986019"
