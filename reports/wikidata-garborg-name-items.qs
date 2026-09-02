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

# Voster -- family, 6 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Voster"
LAST	Len	"Voster"
#   set the mul label to "Voster"
LAST	Lmul	"Voster"
#   set the en description to "family name"
LAST	Den	"family name"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q141205913 Ingebret Pederson Voster: P734 family name = the item just created
Q141205913	P734	LAST	S2600	"6000000007980389582"
#   Q141242562 Peder Jonsen Voster: P734 family name = the item just created
Q141242562	P734	LAST	S2600	"6000000007980605161"
#   Q141198755 Anna Ingebretsdatter Voster: P734 family name = the item just created
Q141198755	P734	LAST	S2600	"6000000007980728952"
#   Q141223551 Ragnhild Ingebretsdatter Voster: P734 family name = the item just created
Q141223551	P734	LAST	S2600	"6000000007980728958"
#   Q141244126 Valborg Ingebretsdatter Voster: P734 family name = the item just created
Q141244126	P734	LAST	S2600	"6000000007980728964"
#   Q141244116 NN Voster: P734 family name = the item just created, qualified P3831 object of statement has role Q28418670 married name
Q141244116	P734	LAST	P3831	Q28418670	S2600	"6000000015302207141"

# Rasmussen -- patronymic, 5 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Rasmussen"
LAST	Len	"Rasmussen"
#   set the mul label to "Rasmussen"
LAST	Lmul	"Rasmussen"
#   set the en description to "patronymic"
LAST	Den	"patronymic"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141216381 Hans Rasmussen Låge-Håland: P5056 patronym or matronym = the item just created
Q141216381	P5056	LAST	S2600	"6000000009127934231"
#   Q141257264 Lydik Rasmussen Amdal: P5056 patronym or matronym = the item just created, qualified P144 based on Q141257299 Rasmus Lydikson Amdal
Q141257264	P5056	LAST	P144	Q141257299	S2600	"6000000023605569477"
#   Q141223738 Ola Rasmussen Bø: P5056 patronym or matronym = the item just created, qualified P144 based on Q141200074 Rasmus Olsen Bø
Q141223738	P5056	LAST	P144	Q141200074	S2600	"6000000196541254827"
#   Q141242406 Hans Rasmussen Bø: P5056 patronym or matronym = the item just created, qualified P144 based on Q141189099 Rasmus Helgesen Bø
Q141242406	P5056	LAST	P144	Q141189099	S2600	"6000000225376735889"
#   Q141242555 Ola Rasmussen Bø: P5056 patronym or matronym = the item just created, qualified P144 based on Q141189099 Rasmus Helgesen Bø
Q141242555	P5056	LAST	P144	Q141189099	S2600	"6000000225376871825"

# Ekebyholm -- family, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Ekebyholm"
LAST	Len	"Ekebyholm"
#   set the mul label to "Ekebyholm"
LAST	Lmul	"Ekebyholm"
#   set the en description to "family name"
LAST	Den	"family name"
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

# 344 more name items are needed and wait for a later
# run -- 3 a day is her cap, not a limit of the data:
#   Kristiansen (patronymic), 4 bearer(s)
#   Låge-Håland (family), 4 bearer(s)
#   Tormodsdatter (patronymic), 4 bearer(s)
#   Asbjørnsdatter (patronymic), 3 bearer(s)
#   Frondin (family), 3 bearer(s)
#   Garfve (family), 3 bearer(s)
#   Hakunge (family), 3 bearer(s)
#   Hansen (patronymic), 3 bearer(s)
#   Hansson (patronymic), 3 bearer(s)
#   Helgesen (patronymic), 3 bearer(s)
#   Høle (family), 3 bearer(s)
#   Ingebretsdatter (patronymic), 3 bearer(s)
#   ... and 332 more

