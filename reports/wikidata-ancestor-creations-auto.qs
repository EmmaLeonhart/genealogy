# ========================================================================
# ONE PARENT A RUN, UP THE ACCOUNT OWNER'S OWN ANCESTRY -- the scheduled run, 2 creation(s).
# 620 eligible: an ancestor of 6000000087535357291 who carries a QID and whose parent the tree
# knows and Wikidata does not. Chosen at random, seeded on 2026-09-18 so the pick is
# stable for the day -- the batch is recomposed several times a day and an
# unseeded choice would create a different person on each recomposition.
# ========================================================================
#   6000000196282195908: father of Q3437950 (5620645112580020100), created because the tree knows them and Wikidata does not
CREATE
LAST	Len	"Hailaga Halvdansson Halfdansson"
LAST	Lmul	"Hailaga Halvdansson Halfdansson"
LAST	P31	Q5	S2600	"6000000196282195908"
LAST	P2600	"6000000196282195908"
LAST	P21	Q6581097	S2600	"6000000196282195908"
#   Q3437950: P22 = the item just created
Q3437950	P22	LAST	S2600	"5620645112580020100"
#   6000000004839304936: mother of Q12337724 (6000000007086528162), created because the tree knows them and Wikidata does not
CREATE
LAST	Len	"Regnild"
LAST	Lmul	"Regnild"
LAST	P31	Q5	S2600	"6000000004839304936"
LAST	P2600	"6000000004839304936"
LAST	P21	Q6581072	S2600	"6000000004839304936"
#   Q12337724: P25 = the item just created
Q12337724	P25	LAST	S2600	"6000000007086528162"
