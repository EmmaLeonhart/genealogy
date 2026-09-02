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

# Kristiansen -- patronymic, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Kristiansen"
LAST	Len	"Kristiansen"
#   set the mul label to "Kristiansen"
LAST	Lmul	"Kristiansen"
#   set the en description to "patronymic"
LAST	Den	"patronymic"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141189067 Helmik Kristiansen Sør-Reime: P5056 patronym or matronym = the item just created, qualified P144 based on Q141189076 Kristian Larsen Sør-Reime
Q141189067	P5056	LAST	P144	Q141189076	S2600	"6000000221449620901"
#   Q141189078 Lars Kristiansen Sør-Reime: P5056 patronym or matronym = the item just created, qualified P144 based on Q141189076 Kristian Larsen Sør-Reime
Q141189078	P5056	LAST	P144	Q141189076	S2600	"6000000224702528843"
#   Q141189077 Lars Bernhard Kristiansen Sør-Reime: P5056 patronym or matronym = the item just created, qualified P144 based on Q141189076 Kristian Larsen Sør-Reime
Q141189077	P5056	LAST	P144	Q141189076	S2600	"6000000224702710821"

# Tormodsdatter -- patronymic, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Tormodsdatter"
LAST	Len	"Tormodsdatter"
#   set the mul label to "Tormodsdatter"
LAST	Lmul	"Tormodsdatter"
#   set the en description to "patronymic"
LAST	Den	"patronymic"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141224345 Signy Tormodsdatter Rossavik: P5056 patronym or matronym = the item just created
Q141224345	P5056	LAST	S2600	"6000000003095080099"
#   Q141205898 Anna Tormodsdatter Mele: P5056 patronym or matronym = the item just created, qualified P144 based on Q141198507 Tormod Bjørnson Mele
Q141205898	P5056	LAST	P144	Q141198507	S2600	"6000000005609232777"

# Garfve -- family, 3 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Garfve"
LAST	Len	"Garfve"
#   set the mul label to "Garfve"
LAST	Lmul	"Garfve"
#   set the en description to "family name"
LAST	Den	"family name"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q141224010 Harlan Roger Garfve: P734 family name = the item just created
Q141224010	P734	LAST	S2600	"6000000019472886300"
#   Q141189056 Bella Jeanette Garfve: P734 family name = the item just created, qualified P3831 object of statement has role Q28418670 married name
Q141189056	P734	LAST	P3831	Q28418670	S2600	"6000000039507887815"
#   Q141224188 Hjalmer Morris Garfve: P734 family name = the item just created
Q141224188	P734	LAST	S2600	"6000000039508406904"

# 338 more name items are needed and wait for a later
# run -- 3 a day is her cap, not a limit of the data:
#   Hakunge (family), 3 bearer(s)
#   Hansen (patronymic), 3 bearer(s)
#   Hansson (patronymic), 3 bearer(s)
#   Helgesen (patronymic), 3 bearer(s)
#   Høle (family), 3 bearer(s)
#   Ingebretsdatter (patronymic), 3 bearer(s)
#   Johansdotter (patronymic), 3 bearer(s)
#   Knutsdatter (patronymic), 3 bearer(s)
#   Magnusson (patronymic), 3 bearer(s)
#   Nord-Varhaug (family), 3 bearer(s)
#   Røyneberg (family), 3 bearer(s)
#   Söfdeborg (family), 3 bearer(s)
#   ... and 326 more

