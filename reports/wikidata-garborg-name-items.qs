# Name items the Garborg batches need, AND the statements that use them.
#
# Each CREATE is followed by `Qperson  Pprop  LAST` for every bearer who
# ALREADY holds a QID -- LAST is exactly how you point at what was just
# created. A person this run is also CREATING cannot be linked here, because
# LAST would then name the person; they wait for the next run.
#
# A patronymic is its own item even where the spelling exists as a given
# name: CLAUDE.md, one name item per USAGE. Emma's Q141152710 Aadnesson is
# the pattern -- labels, P31, nothing else.

# Frondin -- family, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Frondin"
LAST	Len	"Frondin"
#   set the mul label to "Frondin"
LAST	Lmul	"Frondin"
#   set the en description to "family name"
LAST	Den	"family name"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q141223420 Gunilla Margareta Frondin: P734 family name = the item just created, qualified P3831 object of statement has role Q28418670 married name
Q141223420	P734	LAST	P3831	Q28418670	S2600	"6000000011759927315"
#   Q5745634 Elias Frondin: P734 family name = the item just created
Q5745634	P734	LAST	S2600	"6000000018625238474"
#   Q5745627 Berge / Birger Frondin: P734 family name = the item just created
Q5745627	P734	LAST	S2600	"6000000020128505901"

# Nedre -- family, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Nedre"
LAST	Len	"Nedre"
#   set the mul label to "Nedre"
LAST	Lmul	"Nedre"
#   set the en description to "family name"
LAST	Den	"family name"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q141216644 Rasmus Asbjørnson Nedre Rossavik: P734 family name = the item just created
Q141216644	P734	LAST	S2600	"6000000003192698959"
#   Q141224008 Gjøa Gunnbjørnsdatter Nedre Rossavik: P734 family name = the item just created, qualified P3831 object of statement has role Q28418670 married name
Q141224008	P734	LAST	P3831	Q28418670	S2600	"6000000005609443674"
#   Q141216599 Anna Rasmusdatter Nedre Rossavik: P734 family name = the item just created
Q141216599	P734	LAST	S2600	"6000000008916446714"

# Olofsdotter -- patronymic, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Olofsdotter"
LAST	Len	"Olofsdotter"
#   set the mul label to "Olofsdotter"
LAST	Lmul	"Olofsdotter"
#   set the en description to "patronymic"
LAST	Den	"patronymic"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141216618 Karin Olofsdotter: P5056 patronym or matronym = the item just created, qualified P144 based on Q141216403 Olof Nilsson
Q141216618	P5056	LAST	P144	Q141216403	S2600	"348968026630001429"
#   Q141224093 Beata Magdalena Olofsdotter Mellberg: P5056 patronym or matronym = the item just created
Q141224093	P5056	LAST	S2600	"6000000001865185124"
#   Q141249729 Kristina Olofsdotter Spaak: P5056 patronym or matronym = the item just created
Q141249729	P5056	LAST	S2600	"6000000006897337018"
#   Q141244092 Christina Olofsdotter Hammar: P5056 patronym or matronym = the item just created
Q141244092	P5056	LAST	S2600	"6000000009492573975"

# 305 more name items are needed and wait for a later
# run -- 3 a day is her cap, not a limit of the data:
#   Pedersdatter (patronymic), 4 bearer(s)
#   Tollefson (patronymic), 4 bearer(s)
#   Bjørnson (patronymic), 3 bearer(s)
#   Garfve (family), 3 bearer(s)
#   Hansson (patronymic), 3 bearer(s)
#   Helgesen (patronymic), 3 bearer(s)
#   Høle (family), 3 bearer(s)
#   Ingebretsdatter (patronymic), 3 bearer(s)
#   Kristiansen (patronymic), 3 bearer(s)
#   Larsdatter (patronymic), 3 bearer(s)
#   Larsson (patronymic), 3 bearer(s)
#   Låge-Håland (family), 3 bearer(s)
#   ... and 293 more

