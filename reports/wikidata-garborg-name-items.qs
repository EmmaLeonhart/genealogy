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

# Jonson -- patronymic, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Jonson"
LAST	Len	"Jonson"
#   set the mul label to "Jonson"
LAST	Lmul	"Jonson"
#   set the en description to "patronymic"
LAST	Den	"patronymic"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141205903 Enok Jonson Rønneberg: P5056 patronym or matronym = the item just created, qualified P144 based on Q141216481 Jon Tørresson Soma
Q141205903	P5056	LAST	P144	Q141216481	S2600	"6000000001656464422"
#   Q141249595 Asbjørn Jonson Rønneberg: P5056 patronym or matronym = the item just created, qualified P144 based on Q141244102 Jon Torson Røyneberg
Q141249595	P5056	LAST	P144	Q141244102	S2600	"6000000003491988141"
#   Q141219349 Tørres Jonson Grannes: P5056 patronym or matronym = the item just created
Q141219349	P5056	LAST	S2600	"6000000005608892520"
#   Q141216470 Govert Jonson Årsvoll: P5056 patronym or matronym = the item just created
Q141216470	P5056	LAST	S2600	"6000000008174080446"

# Rasmussen -- patronymic, 4 bearer(s) in the batches
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
#   Q141223738 Ola Rasmussen Bø: P5056 patronym or matronym = the item just created, qualified P144 based on Q141200074 Rasmus Olsen Bø
Q141223738	P5056	LAST	P144	Q141200074	S2600	"6000000196541254827"
#   Q141242406 Hans Rasmussen Bø: P5056 patronym or matronym = the item just created, qualified P144 based on Q141189099 Rasmus Helgesen Bø
Q141242406	P5056	LAST	P144	Q141189099	S2600	"6000000225376735889"
#   Q141242555 Ola Rasmussen Bø: P5056 patronym or matronym = the item just created, qualified P144 based on Q141189099 Rasmus Helgesen Bø
Q141242555	P5056	LAST	P144	Q141189099	S2600	"6000000225376871825"

# Asbjørnsdatter -- patronymic, 3 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Asbjørnsdatter"
LAST	Len	"Asbjørnsdatter"
#   set the mul label to "Asbjørnsdatter"
LAST	Lmul	"Asbjørnsdatter"
#   set the en description to "patronymic"
LAST	Den	"patronymic"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141224263 Karen Asbjørnsdatter Opstad: P5056 patronym or matronym = the item just created, qualified P144 based on Q141216458 Asbjørn Gunnarson Bø
Q141224263	P5056	LAST	P144	Q141216458	S2600	"6000000011046282612"
#   Q141242419 Sara Asbjørnsdatter Bø: P5056 patronym or matronym = the item just created, qualified P144 based on Q141216458 Asbjørn Gunnarson Bø
Q141242419	P5056	LAST	P144	Q141216458	S2600	"6000000222520233004"
#   Q141242459 Anna Asbjørnsdatter Bø: P5056 patronym or matronym = the item just created, qualified P144 based on Q141216458 Asbjørn Gunnarson Bø
Q141242459	P5056	LAST	P144	Q141216458	S2600	"6000000222520767827"

# 294 more name items are needed and wait for a later
# run -- 3 a day is her cap, not a limit of the data:
#   Frondin (family), 3 bearer(s)
#   Garfve (family), 3 bearer(s)
#   Hansson (patronymic), 3 bearer(s)
#   Helgesen (patronymic), 3 bearer(s)
#   Høle (family), 3 bearer(s)
#   Ingebretsdatter (patronymic), 3 bearer(s)
#   Kristiansen (patronymic), 3 bearer(s)
#   Låge-Håland (family), 3 bearer(s)
#   Magnusson (patronymic), 3 bearer(s)
#   Nedre (family), 3 bearer(s)
#   Olofsdotter (patronymic), 3 bearer(s)
#   Pedersdatter (patronymic), 3 bearer(s)
#   ... and 282 more

