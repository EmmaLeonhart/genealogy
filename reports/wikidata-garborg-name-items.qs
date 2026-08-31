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

# Jonsson -- patronymic, 5 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Jonsson"
LAST	Len	"Jonsson"
#   set the mul label to "Jonsson"
LAST	Lmul	"Jonsson"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q5568857 Daniel Jonsson Behmer: P5056 patronym or matronym = the item just created
Q5568857	P5056	LAST	S2600	"6000000006776755330"
#   Q141224872 Petrus Jonae Jonæ Linnerius: P5056 patronym or matronym = the item just created
Q141224872	P5056	LAST	S2600	"6000000006782697953"
#   Q141216476 Jon Jonsson Vatne: P5056 patronym or matronym = the item just created, qualified P144 based on Q141216388 Jon Hansson St. Vatne
Q141216476	P5056	LAST	P144	Q141216388	S2600	"6000000014516017872"
#   Q141219070 Tørres Jonsson Vatne: P5056 patronym or matronym = the item just created, qualified P144 based on Q141216388 Jon Hansson St. Vatne
Q141219070	P5056	LAST	P144	Q141216388	S2600	"6000000014516687339"
#   Q141225218 Olof Jonsson: P5056 patronym or matronym = the item just created
Q141225218	P5056	LAST	S2600	"6000000015844614533"

# Trevland -- family, 5 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Trevland"
LAST	Len	"Trevland"
#   set the mul label to "Trevland"
LAST	Lmul	"Trevland"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q141225750 Jon Pedersen Trevland: P734 family name = the item just created
Q141225750	P734	LAST	S2600	"6000000001770193504"
#   Q141205938 Ranveig Olsd Trevland: P734 family name = the item just created, qualified P3831 object of statement has role Q28418670 married name
Q141205938	P734	LAST	P3831	Q28418670	S2600	"6000000006358672581"
#   Q141225186 Ola Pedersen Trevland: P734 family name = the item just created
Q141225186	P734	LAST	S2600	"6000000061945034833"
#   Q141223431 Ola Taraldsen Trevland: P734 family name = the item just created
Q141223431	P734	LAST	S2600	"6000000226904207910"
#   Q141224789 Jon Olsen Trevland: P734 family name = the item just created
Q141224789	P734	LAST	S2600	"6000000226904750852"

# Erikson -- patronymic, 3 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Erikson"
LAST	Len	"Erikson"
#   set the mul label to "Erikson"
LAST	Lmul	"Erikson"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141198503 Tore Erikson Håland: P5056 patronym or matronym = the item just created
Q141198503	P5056	LAST	S2600	"6000000003095166856"
#   Q141216607 Hans Erikson Øvre Håland: P5056 patronym or matronym = the item just created
Q141216607	P5056	LAST	S2600	"6000000009152082622"

# 256 more name items are needed and wait for a later
# run -- 3 a day is her cap, not a limit of the data:
#   Garfve (family), 3 bearer(s)
#   Helgesen (patronymic), 3 bearer(s)
#   Høle (family), 3 bearer(s)
#   Jonsen (patronymic), 3 bearer(s)
#   Jonson (patronymic), 3 bearer(s)
#   Kristiansen (patronymic), 3 bearer(s)
#   Låge-Håland (family), 3 bearer(s)
#   Magnusson (patronymic), 3 bearer(s)
#   Nedre (family), 3 bearer(s)
#   Olofsson (patronymic), 3 bearer(s)
#   Osmundsdatter (patronymic), 3 bearer(s)
#   Rasmussen (patronymic), 3 bearer(s)
#   ... and 244 more

