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

# Bjørnson -- patronymic, 3 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Bjørnson"
LAST	Len	"Bjørnson"
#   set the mul label to "Bjørnson"
LAST	Lmul	"Bjørnson"
#   set the en description to "patronymic"
LAST	Den	"patronymic"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141244226 Knut Bjørnson Bjørheim: P5056 patronym or matronym = the item just created, qualified P144 based on Q141244210 Bjørn Lauritsen Bjørheim
Q141244226	P5056	LAST	P144	Q141244210	S2600	"6000000002277957043"
#   Q141198507 Tormod Bjørnson Mele: P5056 patronym or matronym = the item just created, qualified P144 based on Q141250216 Bjørn Gunnarson Mele
Q141198507	P5056	LAST	P144	Q141250216	S2600	"6000000007980617631"

# Hakunge -- family, 3 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Hakunge"
LAST	Len	"Hakunge"
#   set the mul label to "Hakunge"
LAST	Lmul	"Hakunge"
#   set the en description to "family name"
LAST	Den	"family name"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q141219054 Carl Emil Cronhielm af Hakunge: P734 family name = the item just created
Q141219054	P734	LAST	S2600	"6000000008178453589"
#   Q110304582 Gustava Magdalena Cronhielm af Hakunge: P734 family name = the item just created
Q110304582	P734	LAST	S2600	"6000000012959992080"
#   Q4938400 Christina Charlotta Cronhielm af Hakunge: P734 family name = the item just created
Q4938400	P734	LAST	S2600	"6000000020584191181"

# Hansen -- patronymic, 3 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Hansen"
LAST	Len	"Hansen"
#   set the mul label to "Hansen"
LAST	Lmul	"Hansen"
#   set the en description to "patronymic"
LAST	Den	"patronymic"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141223961 Syvert Kristian Hansen Nyvold: P5056 patronym or matronym = the item just created
Q141223961	P5056	LAST	S2600	"6000000021198171670"
#   Q141250244 Rasmus Hansen Nord-Varhaug: P5056 patronym or matronym = the item just created, qualified P144 based on Q141216381 Hans Rasmussen Låge-Håland
Q141250244	P5056	LAST	P144	Q141216381	S2600	"6000000087451690855"
#   Q141200127 Ådne Hansen Grøtheim: P5056 patronym or matronym = the item just created, qualified P144 based on Q141216607 Hans Erikson Øvre Håland
Q141200127	P5056	LAST	P144	Q141216607	S2600	"6000000225229617898"

# 342 more name items are needed and wait for a later
# run -- 3 a day is her cap, not a limit of the data:
#   Hansson (patronymic), 3 bearer(s)
#   Helgesen (patronymic), 3 bearer(s)
#   Høle (family), 3 bearer(s)
#   Ingebretsdatter (patronymic), 3 bearer(s)
#   Johansdotter (patronymic), 3 bearer(s)
#   Knutsdatter (patronymic), 3 bearer(s)
#   Larsson (patronymic), 3 bearer(s)
#   Magnusson (patronymic), 3 bearer(s)
#   Nord-Varhaug (family), 3 bearer(s)
#   Olson (patronymic), 3 bearer(s)
#   Rudén (family), 3 bearer(s)
#   Røyneberg (family), 3 bearer(s)
#   ... and 330 more

