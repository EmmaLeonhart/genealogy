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

# Gunnarson -- patronymic, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Gunnarson"
LAST	Len	"Gunnarson"
#   set the mul label to "Gunnarson"
LAST	Lmul	"Gunnarson"
#   set the en description to "patronymic"
LAST	Den	"patronymic"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141250216 Bjørn Gunnarson Mele: P5056 patronym or matronym = the item just created
Q141250216	P5056	LAST	S2600	"4462693"
#   Q141244234 Torstein Gunnarson Frafjord: P5056 patronym or matronym = the item just created
Q141244234	P5056	LAST	S2600	"6000000005607365222"
#   Q141216458 Asbjørn Gunnarson Bø: P5056 patronym or matronym = the item just created
Q141216458	P5056	LAST	S2600	"6000000042211257078"

# Låge-Håland -- family, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Låge-Håland"
LAST	Len	"Låge-Håland"
#   set the mul label to "Låge-Håland"
LAST	Lmul	"Låge-Håland"
#   set the en description to "family name"
LAST	Den	"family name"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q141216634 Marit Hansdatter Stavnheim: P734 family name = the item just created, qualified P3831 object of statement has role Q2507958 birth name
Q141216634	P734	LAST	P3831	Q2507958	S2600	"6000000009127909254"
#   Q141216381 Hans Rasmussen Låge-Håland: P734 family name = the item just created
Q141216381	P734	LAST	S2600	"6000000009127934231"
#   Q141250244 Rasmus Hansen Nord-Varhaug: P734 family name = the item just created, qualified P3831 object of statement has role Q2507958 birth name
Q141250244	P734	LAST	P3831	Q2507958	S2600	"6000000087451690855"
#   Q141199918 Kirsten Hansdatter Grøtheim: P734 family name = the item just created, qualified P3831 object of statement has role Q2507958 birth name
Q141199918	P734	LAST	P3831	Q2507958	S2600	"6000000087451897836"

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

# 327 more name items are needed and wait for a later
# run -- 3 a day is her cap, not a limit of the data:
#   Garfve (family), 3 bearer(s)
#   Hakunge (family), 3 bearer(s)
#   Hansen (patronymic), 3 bearer(s)
#   Hansson (patronymic), 3 bearer(s)
#   Helgesen (patronymic), 3 bearer(s)
#   Høle (family), 3 bearer(s)
#   Ingebretsdatter (patronymic), 3 bearer(s)
#   Johansdotter (patronymic), 3 bearer(s)
#   Knutsdatter (patronymic), 3 bearer(s)
#   Kristiansen (patronymic), 3 bearer(s)
#   Magnusson (patronymic), 3 bearer(s)
#   Olson (patronymic), 3 bearer(s)
#   ... and 315 more

