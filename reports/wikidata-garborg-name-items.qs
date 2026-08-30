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

# Jonsson -- patronymic, 6 bearer(s) in the batches
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

# Jenssen -- patronymic, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Jenssen"
LAST	Len	"Jenssen"
#   set the mul label to "Jenssen"
LAST	Lmul	"Jenssen"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141216639 Olufine Bergithe Ekman: P5056 patronym or matronym = the item just created, qualified P144 based on Q141223516 Hans Otto Kristian Jenssen
Q141216639	P5056	LAST	P144	Q141223516	S2600	"6000000014196479728"
#   Q141223517 Hilma Petrine Jenssen: P5056 patronym or matronym = the item just created, qualified P144 based on Q141223516 Hans Otto Kristian Jenssen
Q141223517	P5056	LAST	P144	Q141223516	S2600	"6000000014196669652"
#   Q141225138 Iver Emil Jenssen: P5056 patronym or matronym = the item just created, qualified P144 based on Q141223516 Hans Otto Kristian Jenssen
Q141225138	P5056	LAST	P144	Q141223516	S2600	"6000000014196751178"

# Trevland -- family, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Trevland"
LAST	Len	"Trevland"
#   set the mul label to "Trevland"
LAST	Lmul	"Trevland"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q141205938 Ranveig Olsd Trevland: P734 family name = the item just created, qualified P3831 object of statement has role Q28418670 married name
Q141205938	P734	LAST	P3831	Q28418670	S2600	"6000000006358672581"
#   Q141225186 Ola Pedersen Trevland: P734 family name = the item just created
Q141225186	P734	LAST	S2600	"6000000061945034833"
#   Q141223431 Ola Taraldsen Trevland: P734 family name = the item just created
Q141223431	P734	LAST	S2600	"6000000226904207910"
#   Q141224789 Jon Olsen Trevland: P734 family name = the item just created
Q141224789	P734	LAST	S2600	"6000000226904750852"

# Andersson -- patronymic, 3 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Andersson"
LAST	Len	"Andersson"
#   set the mul label to "Andersson"
LAST	Lmul	"Andersson"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q6057321 Olof Andersson Pryss: P5056 patronym or matronym = the item just created
Q6057321	P5056	LAST	S2600	"6000000001208426544"
#   Q16650163 Samuel Andersson Pryss: P5056 patronym or matronym = the item just created
Q16650163	P5056	LAST	S2600	"6000000001720825110"
#   Q5916189 Gustaf Andersson Knös: P5056 patronym or matronym = the item just created
Q5916189	P5056	LAST	S2600	"6000000021501491188"

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
#   P5056 patronym or matronym = the item just created
Q141216607	P5056	LAST	S2600	"6000000009152082622"

# Garfve -- family, 3 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Garfve"
LAST	Len	"Garfve"
#   set the mul label to "Garfve"
LAST	Lmul	"Garfve"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q141224010 Harlan Roger Garfve: P734 family name = the item just created
Q141224010	P734	LAST	S2600	"6000000019472886300"
#   Q141189056 Bella Jeanette Garfve: P734 family name = the item just created, qualified P3831 object of statement has role Q28418670 married name
Q141189056	P734	LAST	P3831	Q28418670	S2600	"6000000039507887815"
#   Q141224188 Hjalmer Morris Garfve: P734 family name = the item just created
Q141224188	P734	LAST	S2600	"6000000039508406904"

# Hansson -- patronymic, 3 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Hansson"
LAST	Len	"Hansson"
#   set the mul label to "Hansson"
LAST	Lmul	"Hansson"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141216388 Jon Hansson St. Vatne: P5056 patronym or matronym = the item just created
Q141216388	P5056	LAST	S2600	"6000000005608892743"
#   Q5976894 Gabriel Hansson Marklin: P5056 patronym or matronym = the item just created
Q5976894	P5056	LAST	S2600	"6000000044191693814"
#   Q141216468 Erik Hansson Gausland: P5056 patronym or matronym = the item just created, qualified P144 based on Q141216381 Hans Rasmussen Låge-Håland
Q141216468	P5056	LAST	P144	Q141216381	S2600	"6000000053561772011"

# Helgesen -- patronymic, 3 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Helgesen"
LAST	Len	"Helgesen"
#   set the mul label to "Helgesen"
LAST	Lmul	"Helgesen"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141189099 Rasmus Helgesen Bø: P5056 patronym or matronym = the item just created, qualified P144 based on Q141189066 Helge Rasmusson Bø
Q141189099	P5056	LAST	P144	Q141189066	S2600	"6000000021133770643"
#   Q141189113 Ådne Helgesen Bø: P5056 patronym or matronym = the item just created, qualified P144 based on Q141189066 Helge Rasmusson Bø
Q141189113	P5056	LAST	P144	Q141189066	S2600	"6000000196542455825"
#   Q141206056 Asbjørn Helgesen Bø: P5056 patronym or matronym = the item just created, qualified P144 based on Q141216382 Helge Asbjørnsen Bø
Q141206056	P5056	LAST	P144	Q141216382	S2600	"6000000222520395904"

# Høle -- family, 3 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Høle"
LAST	Len	"Høle"
#   set the mul label to "Høle"
LAST	Lmul	"Høle"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q141200067 Rasmus Kjetilson Høle: P734 family name = the item just created, qualified P3831 object of statement has role Q2507958 birth name
Q141200067	P734	LAST	P3831	Q2507958	S2600	"6000000003095034915"
#   P734 family name = the item just created
Q141200067	P734	LAST	S2600	"6000000003095034915"
#   Q141180412 Marta Rasmusdatter Li: P734 family name = the item just created, qualified P3831 object of statement has role Q2507958 birth name
Q141180412	P734	LAST	P3831	Q2507958	S2600	"6000000005609534550"

# Johansdotter -- patronymic, 3 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Johansdotter"
LAST	Len	"Johansdotter"
#   set the mul label to "Johansdotter"
LAST	Lmul	"Johansdotter"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q109266155 Magdalena Johansdotter Bure: P5056 patronym or matronym = the item just created, qualified P144 based on Q633094 Johannes Thomæ Agrivillensis Bureus
Q109266155	P5056	LAST	P144	Q633094	S2600	"6000000006828701331"
#   Q141206084 Margareta Burea: P5056 patronym or matronym = the item just created, qualified P144 based on Q633094 Johannes Thomæ Agrivillensis Bureus
Q141206084	P5056	LAST	P144	Q633094	S2600	"6000000025579779586"

# 263 more name items are needed and wait for a later
# run -- 10 a day is her cap, not a limit of the data:
#   Jonsen (patronymic), 3 bearer(s)
#   Jonson (patronymic), 3 bearer(s)
#   Kristiansen (patronymic), 3 bearer(s)
#   Låge-Håland (family), 3 bearer(s)
#   Magnusson (patronymic), 3 bearer(s)
#   Nedre (family), 3 bearer(s)
#   Olofsson (patronymic), 3 bearer(s)
#   Osmundsdatter (patronymic), 3 bearer(s)
#   Pedersdatter (patronymic), 3 bearer(s)
#   Rasmussen (patronymic), 3 bearer(s)
#   Voster (family), 3 bearer(s)
#   Ådnesdatter (patronymic), 3 bearer(s)
#   ... and 251 more

