# ------------------------------------------------------------------------
# SPINE COMPLETION -- the two people whose absence is the ONLY break left in
#   the Charlemagne line. Goes at the BEGINNING of the next daily batch.
#
# Emma, 2026-08-29: "just do quickstatements to fully complete the chain next
#   session as a custom block at the beginning of the batch."
#
# paths/charlemagne-to-arne-garborg.tsv is 34 steps, Arne Garborg up to
# Charlemagne. 32 of the 34 already have a Wikidata item -- 23 in the ledger,
# 9 long-standing items verified in out/wikidata/p2600-all.tsv (Q3044
# Charlemagne, Q43974 Louis the Pious, Q273181 Judith of Flanders, Q378177
# Baldwin IV, Q314521 Berengar II, Q3769073 Gisela of Friuli, Q19061035
# Guttorm Asulfsson, Q75291928 Asulv Skulesson, Q6180419 Skule Torstigson).
#
# And the bonds hold. scripts/check-spine-bonds.py fetched all 35 items in one
# batched wbgetentities request: of the 33 consecutive pairs, 29 are joined by
# a P22/P25/P40/P26 statement TODAY, and the only 4 breaks are the pairs
# touching these two people. reports/spine-bonds.tsv is the row-by-row record.
#
#   step 14  Tore II Gardson Gard         Q141205942
#   step 15  Ramborg Knutsdotter Lejon    <- created here
#   step 16  Knut Algotsson               Q5915800
#
#   step 21  Helena Guttormsdatter        Q4953376
#   step 22  Ingrid Guttormsdotter        <- created here
#   step 23  Guttorm Asulfsson a Rein     Q19061035
#
# Each has an item directly above and directly below, so each is created AND
# linked to both in this batch -- the "two items minted in one batch cannot
# point at each other" limit does not bite, because neither neighbour is new.
# The two are 7 steps apart and never refer to one another.
#
# WHAT IS DELIBERATELY NOT HERE: P735 given name and P734 family name. Emma,
#   2026-08-29, on name items being merged away by other editors: "having a
#   strong preference for creating new name objects versus using the existing
#   ones is a very wrong move here." Ramborg, Knutsdotter, Lejon and
#   Guttormsdotter would each need a name item resolved or minted, and that
#   question is its own queue item. The person, the dates and the links do not
#   wait on it.
#
# Dates carry no ABT/AFT qualifier because the daily pipeline emits none --
#   matching it rather than diverging in a hand-written block. Ramborg's death
#   is recorded on Geni as AFT 1408 and Ingrid's birth as ABT 1135; both go in
#   at year precision, which is what /9 says.
# ------------------------------------------------------------------------

# create a new item -- step 15, Ramborg Knutsdotter Lejon
CREATE
#   the item just created: set the mul label to "Ramborg Knutsdotter Lejon"
LAST	Lmul	"Ramborg Knutsdotter Lejon"
#   set the en label to "Ramborg Knutsdotter Lejon"
LAST	Len	"Ramborg Knutsdotter Lejon"
#   set the ja label
LAST	Lja	"ラムボルグ・クヌトスドッテル・レヨン"
#   set the zh label
LAST	Lzh	"拉姆博尔格·克努特斯多特·莱永恩"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000004870648136 Ramborg Knutsdotter Lejon
LAST	P2600	"6000000004870648136"
#   P569 date of birth = 1360
LAST	P569	+1360-00-00T00:00:00Z/9	S2600	"6000000004870648136"
#   P570 date of death = after 1408, recorded at year precision
LAST	P570	+1408-00-00T00:00:00Z/9	S2600	"6000000004870648136"
#   P22 father = Q5915800 Knut Algotsson -- step 16
LAST	P22	Q5915800	S2600	"6000000004870648136"
#   Q5915800 Knut Algotsson: P40 child = the item just created
Q5915800	P40	LAST	S2600	"6000000004870648136"
#   P40 child = Q141205942 Tore II Gardson Gard -- step 14
LAST	P40	Q141205942	S2600	"6000000004870648136"
#   Q141205942 Tore II Gardson Gard: P25 mother = the item just created
Q141205942	P25	LAST	S2600	"6000000004870648136"

# create a new item -- step 22, Ingrid Guttormsdotter
CREATE
#   the item just created: set the mul label to "Ingrid Guttormsdotter"
LAST	Lmul	"Ingrid Guttormsdotter"
#   set the en label to "Ingrid Guttormsdotter"
LAST	Len	"Ingrid Guttormsdotter"
#   set the ja label
LAST	Lja	"イングリド・グトルムスドッテル"
#   set the zh label
LAST	Lzh	"伊恩格里德·古托尔姆斯多特"
#   an alias, from a second NAME record on the Geni profile
LAST	Amul	"Ingrid Guttormsdatter af Rein"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000000771986019 Ingrid Guttormsdotter
LAST	P2600	"6000000000771986019"
#   P569 date of birth = about 1135, recorded at year precision
LAST	P569	+1135-00-00T00:00:00Z/9	S2600	"6000000000771986019"
#   P22 father = Q19061035 Guttorm Asulfsson a Rein -- step 23
LAST	P22	Q19061035	S2600	"6000000000771986019"
#   Q19061035 Guttorm Asulfsson a Rein: P40 child = the item just created
Q19061035	P40	LAST	S2600	"6000000000771986019"
#   P40 child = Q4953376 Helena Guttormsdatter -- step 21
LAST	P40	Q4953376	S2600	"6000000000771986019"
#   Q4953376 Helena Guttormsdatter: P25 mother = the item just created
Q4953376	P25	LAST	S2600	"6000000000771986019"
