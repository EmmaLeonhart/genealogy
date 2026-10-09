# Parents of Jon Samuelsen Raustad (Q141168955), geni 6000000003732742137.
# Emma, 2026-08-25: "add the parents of Jon Samuelsen Raustad".
#
# Checked before writing: neither parent's Geni id appears on any Wikidata item,
# Q141168955 names no P22/P25 yet, and Jon is their only recorded child so no
# sibling item points at an existing parent. Both are genuinely new.
#
# Run in this order. The two CREATE blocks mint the parents; the last two lines
# attach them to Jon and need his QID, which already exists, so they can run in the
# same batch.

# --- father ---------------------------------------------------------------
CREATE
LAST	Len	"Samuel Jonson Raustad"
LAST	Lmul	"Samuel Jonson Raustad"
LAST	P31	Q5
LAST	P21	Q6581097
LAST	P2600	"6000000003491988831"
LAST	P569	+1753-00-00T00:00:00Z/9	S2600	"6000000003491988831"
LAST	P570	+1840-00-00T00:00:00Z/9	S2600	"6000000003491988831"
LAST	P40	Q141168955	S2600	"6000000003491988831"

# --- mother ---------------------------------------------------------------
CREATE
LAST	Len	"Marta Jonsdatter Li"
LAST	Lmul	"Marta Jonsdatter Li"
LAST	P31	Q5
LAST	P21	Q6581072
LAST	P2600	"6000000003491988826"
LAST	P569	+1751-00-00T00:00:00Z/9	S2600	"6000000003491988826"
LAST	P40	Q141168955	S2600	"6000000003491988826"
