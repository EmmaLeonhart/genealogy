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
#   Q5568857 Daniel Jonsson Behmer: P5056 patronym or matronym = the item just created, qualified P144 based on Q25451348 Jon Mickelsson Behm
Q5568857	P5056	LAST	P144	Q25451348	S2600	"6000000006776755330"
#   Q141224872 Petrus Jonae Jonæ Linnerius: P5056 patronym or matronym = the item just created
Q141224872	P5056	LAST	S2600	"6000000006782697953"
#   Q141216476 Jon Jonsson Vatne: P5056 patronym or matronym = the item just created, qualified P144 based on Q141216388 Jon Hansson St. Vatne
Q141216476	P5056	LAST	P144	Q141216388	S2600	"6000000014516017872"
#   Q141219070 Tørres Jonsson Vatne: P5056 patronym or matronym = the item just created, qualified P144 based on Q141216388 Jon Hansson St. Vatne
Q141219070	P5056	LAST	P144	Q141216388	S2600	"6000000014516687339"
#   Q141225218 Olof Jonsson: P5056 patronym or matronym = the item just created
Q141225218	P5056	LAST	S2600	"6000000015844614533"

# Ekebyholm -- family, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Ekebyholm"
LAST	Len	"Ekebyholm"
#   set the mul label to "Ekebyholm"
LAST	Lmul	"Ekebyholm"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q109296398 Fredrika Eleonora Arvidsdotter Horn af Ekebyholm: P734 family name = the item just created
Q109296398	P734	LAST	S2600	"6000000006127496847"
#   Q5813616 Adam Horn af Ekebyholm till Ekebyholm: P734 family name = the item just created
Q5813616	P734	LAST	S2600	"6000000007285499105"
#   Q19678400 Eva Horn af Ekebyholm: P734 family name = the item just created
Q19678400	P734	LAST	S2600	"6000000007286110282"
#   Q717179 Arvid Bernhard Horn af Ekebyholm: P734 family name = the item just created
Q717179	P734	LAST	S2600	"6000000011637024489"

# Jonsen -- patronymic, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Jonsen"
LAST	Len	"Jonsen"
#   set the mul label to "Jonsen"
LAST	Lmul	"Jonsen"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141223970 Villum Jonsen Gautun: P5056 patronym or matronym = the item just created
Q141223970	P5056	LAST	S2600	"6000000003315775479"
#   Q141242562 Peder Jonsen Voster: P5056 patronym or matronym = the item just created
Q141242562	P5056	LAST	S2600	"6000000007980605161"
#   Q141189110 Tøre Jonsen: P5056 patronym or matronym = the item just created, qualified P144 based on Q116150299 Jon Reinmodsen
Q141189110	P5056	LAST	P144	Q116150299	S2600	"6000000180307857930"
#   Q141198453 Lars Jonsen Kvam: P5056 patronym or matronym = the item just created
Q141198453	P5056	LAST	S2600	"6000000194934774831"

# 297 more name items are needed and wait for a later
# run -- 3 a day is her cap, not a limit of the data:
#   Jonson (patronymic), 4 bearer(s)
#   Rasmussen (patronymic), 4 bearer(s)
#   Asbjørnsdatter (patronymic), 3 bearer(s)
#   Frondin (family), 3 bearer(s)
#   Garfve (family), 3 bearer(s)
#   Hansson (patronymic), 3 bearer(s)
#   Helgesen (patronymic), 3 bearer(s)
#   Høle (family), 3 bearer(s)
#   Ingebretsdatter (patronymic), 3 bearer(s)
#   Kristiansen (patronymic), 3 bearer(s)
#   Låge-Håland (family), 3 bearer(s)
#   Magnusson (patronymic), 3 bearer(s)
#   ... and 285 more

