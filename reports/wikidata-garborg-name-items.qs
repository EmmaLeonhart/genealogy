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

# Olofsson -- patronymic, 5 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Olofsson"
LAST	Len	"Olofsson"
#   set the mul label to "Olofsson"
LAST	Lmul	"Olofsson"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141223844 Laurentius Olai: P5056 patronym or matronym = the item just created, qualified P144 based on Q141205932 Olof Timmerman
Q141223844	P5056	LAST	P144	Q141205932	S2600	"6000000004334886671"
#   Q5613434 Börje Cronberg: P5056 patronym or matronym = the item just created
Q5613434	P5056	LAST	S2600	"6000000007026278130"
#   Q6218220 Olof Olofsson Törnflycht: P5056 patronym or matronym = the item just created
Q6218220	P5056	LAST	S2600	"6000000012056738350"
#   Q5916162 Anders Olofsson Knös: P5056 patronym or matronym = the item just created
Q5916162	P5056	LAST	S2600	"6000000020394079179"

# 302 more name items are needed and wait for a later
# run -- 3 a day is her cap, not a limit of the data:
#   Trevland (family), 5 bearer(s)
#   Ekebyholm (family), 4 bearer(s)
#   Jonsen (patronymic), 4 bearer(s)
#   Jonson (patronymic), 4 bearer(s)
#   Rasmussen (patronymic), 4 bearer(s)
#   Asbjørnsdatter (patronymic), 3 bearer(s)
#   Erikson (patronymic), 3 bearer(s)
#   Frondin (family), 3 bearer(s)
#   Garfve (family), 3 bearer(s)
#   Hansson (patronymic), 3 bearer(s)
#   Helgesen (patronymic), 3 bearer(s)
#   Høle (family), 3 bearer(s)
#   ... and 290 more

