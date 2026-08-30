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

# Bergersen -- patronymic, 7 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Bergersen"
LAST	Len	"Bergersen"
#   set the mul label to "Bergersen"
LAST	Lmul	"Bergersen"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141168797 Christian Frederik Bergersen: P5056 patronym or matronym = the item just created, qualified P144 based on Q141178199 Gunder Bergersen
Q141168797	P5056	LAST	P144	Q141178199	S2600	"6000000009126453497"
#   Q141189083 Martha Elida Frenning: P5056 patronym or matronym = the item just created, qualified P144 based on Q141168797 Christian Frederik Bergersen
Q141189083	P5056	LAST	P144	Q141168797	S2600	"6000000014026305107"
#   Q141178199 Gunder Bergersen: P5056 patronym or matronym = the item just created
Q141178199	P5056	LAST	S2600	"6000000016756402733"
#   Q141189064 Georg August Bergersen: P5056 patronym or matronym = the item just created, qualified P144 based on Q141178199 Gunder Bergersen
Q141189064	P5056	LAST	P144	Q141178199	S2600	"6000000020220377527"
#   Q141189065 Gustav Adolf Gundersen: P5056 patronym or matronym = the item just created, qualified P144 based on Q141178199 Gunder Bergersen
Q141189065	P5056	LAST	P144	Q141178199	S2600	"6000000020220981823"
#   Q141189093 Oline Mathea Olsen: P5056 patronym or matronym = the item just created, qualified P144 based on Q141178199 Gunder Bergersen
Q141189093	P5056	LAST	P144	Q141178199	S2600	"6000000022418305015"
#   Q141189091 Ole Nicolai Bergersen: P5056 patronym or matronym = the item just created, qualified P144 based on Q141168797 Christian Frederik Bergersen
Q141189091	P5056	LAST	P144	Q141168797	S2600	"6000000055822412855"

# Jonsdatter -- patronymic, 6 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Jonsdatter"
LAST	Len	"Jonsdatter"
#   set the mul label to "Jonsdatter"
LAST	Lmul	"Jonsdatter"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141216638 Olaug Jonsdatter Heigre: P5056 patronym or matronym = the item just created
Q141216638	P5056	LAST	S2600	"6000000003491933401"
#   Q141200054 Rakel Jonsdatter Jonsdotter Vatne: P5056 patronym or matronym = the item just created, qualified P144 based on Q141216388 Jon Hansson St. Vatne
Q141200054	P5056	LAST	P144	Q141216388	S2600	"6000000003491986761"
#   Q141205921 Maria Jonsdatter Lura: P5056 patronym or matronym = the item just created, qualified P144 based on Q141216388 Jon Hansson St. Vatne
Q141205921	P5056	LAST	P144	Q141216388	S2600	"6000000003491995109"
#   Q141189071 Joren Jonsdatter Espedal: P5056 patronym or matronym = the item just created, qualified P144 based on Q141198435 Jon Nilsson Espedal
Q141189071	P5056	LAST	P144	Q141198435	S2600	"6000000005609425388"
#   Q141189062 Cecilie Jonsdatter: P5056 patronym or matronym = the item just created, qualified P144 based on Q116150299 Jon Reinmodsen
Q141189062	P5056	LAST	P144	Q116150299	S2600	"6000000180296055830"

# Olsen -- patronymic, 6 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Olsen"
LAST	Len	"Olsen"
#   set the mul label to "Olsen"
LAST	Lmul	"Olsen"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141200019 Ola Olsen Vaule: P5056 patronym or matronym = the item just created, qualified P144 based on Q141189088 Ola Knutsen Grøtheim
Q141200019	P5056	LAST	P144	Q141189088	S2600	"6000000002989071216"
#   Q141169072 Ådne Olsen Garborg: P5056 patronym or matronym = the item just created, qualified P144 based on Q141189088 Ola Knutsen Grøtheim
Q141169072	P5056	LAST	P144	Q141189088	S2600	"6000000003492005161"
#   Q141205900 Bertrand Olav Olsen Vigdel: P5056 patronym or matronym = the item just created, qualified P144 based on Q141189070 John Jonassen Hegre
Q141205900	P5056	LAST	P144	Q141189070	S2600	"6000000006146870818"
#   Q141200074 Rasmus Olsen Bø: P5056 patronym or matronym = the item just created, qualified P144 based on Q141189088 Ola Knutsen Grøtheim
Q141200074	P5056	LAST	P144	Q141189088	S2600	"6000000007744183945"
#   Q141216380 Hans Olsen Grøtheim: P5056 patronym or matronym = the item just created, qualified P144 based on Q141189088 Ola Knutsen Grøtheim
Q141216380	P5056	LAST	P144	Q141189088	S2600	"6000000008176954243"
#   Q141199930 Knut Olsen Gudmestad: P5056 patronym or matronym = the item just created, qualified P144 based on Q141189088 Ola Knutsen Grøtheim
Q141199930	P5056	LAST	P144	Q141189088	S2600	"6000000019668338861"

# Rasmusdatter -- patronymic, 6 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Rasmusdatter"
LAST	Len	"Rasmusdatter"
#   set the mul label to "Rasmusdatter"
LAST	Lmul	"Rasmusdatter"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141180412 Marta Rasmusdatter Li: P5056 patronym or matronym = the item just created, qualified P144 based on Q141200067 Rasmus Kjetilson Høle
Q141180412	P5056	LAST	P144	Q141200067	S2600	"6000000005609534550"
#   Q141216483 Karen Malena Rasmusdatter Tjelta: P5056 patronym or matronym = the item just created
Q141216483	P5056	LAST	S2600	"6000000008173986703"
#   Q141199830 Anna Rasmusdatter Grøtheim: P5056 patronym or matronym = the item just created
Q141199830	P5056	LAST	S2600	"6000000008176804564"
#   Q141216599 Anna Rasmusdatter Nedre Rossavik: P5056 patronym or matronym = the item just created, qualified P144 based on Q141216644 Rasmus Asbjørnson Nedre Rossavik
Q141216599	P5056	LAST	P144	Q141216644	S2600	"6000000008916446714"
#   Q141198484 Rangdi Rasmusdatter Sollienseie: P5056 patronym or matronym = the item just created
Q141198484	P5056	LAST	S2600	"6000000021122137597"
#   Q141219058 Elisabet Rasmusdatter Moen: P5056 patronym or matronym = the item just created, qualified P144 based on Q141189099 Rasmus Helgesen Bø
Q141219058	P5056	LAST	P144	Q141189099	S2600	"6000000225376733918"

# Sør-Reime -- family, 6 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Sør-Reime"
LAST	Len	"Sør-Reime"
#   set the mul label to "Sør-Reime"
LAST	Lmul	"Sør-Reime"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q141189076 Kristian Larsen Sør-Reime: P734 family name = the item just created
Q141189076	P734	LAST	S2600	"6000000029302543031"
#   Q141205912 Herborg Johannesdatter Sør-Reime: P734 family name = the item just created, qualified P3831 object of statement has role Q28418670 married name
Q141205912	P734	LAST	P3831	Q28418670	S2600	"6000000221449607942"
#   Q141189067 Helmik Kristiansen Sør-Reime: P734 family name = the item just created
Q141189067	P734	LAST	S2600	"6000000221449620901"
#   Q141198390 Elisabet Marie Osmundsdatter Sør-Reime: P734 family name = the item just created, qualified P3831 object of statement has role Q28418670 married name
Q141198390	P734	LAST	P3831	Q28418670	S2600	"6000000224702448856"
#   Q141189078 Lars Kristiansen Sør-Reime: P734 family name = the item just created
Q141189078	P734	LAST	S2600	"6000000224702528843"
#   Q141189077 Lars Bernhard Kristiansen Sør-Reime: P734 family name = the item just created
Q141189077	P734	LAST	S2600	"6000000224702710821"

# Hansdatter -- patronymic, 5 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Hansdatter"
LAST	Len	"Hansdatter"
#   set the mul label to "Hansdatter"
LAST	Lmul	"Hansdatter"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141219291 Maria Hansdatter Austrått: P5056 patronym or matronym = the item just created
Q141219291	P5056	LAST	S2600	"6000000005607475201"
#   Q141205919 Malena Hansdatter Bø: P5056 patronym or matronym = the item just created
Q141205919	P5056	LAST	S2600	"6000000005608880208"
#   Q141199856 Guri Hansdatter Garborg: P5056 patronym or matronym = the item just created, qualified P144 based on Q141205911 Hans Svensen Risa I
Q141199856	P5056	LAST	P144	Q141205911	S2600	"6000000007896387570"
#   Q141216634 Marit Hansdatter Stavnheim: P5056 patronym or matronym = the item just created, qualified P144 based on Q141216381 Hans Rasmussen Låge-Håland
Q141216634	P5056	LAST	P144	Q141216381	S2600	"6000000009127909254"
#   Q141199918 Kirsten Hansdatter Grøtheim: P5056 patronym or matronym = the item just created, qualified P144 based on Q141216381 Hans Rasmussen Låge-Håland
Q141199918	P5056	LAST	P144	Q141216381	S2600	"6000000087451897836"

# Morlanda -- family, 5 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Morlanda"
LAST	Len	"Morlanda"
#   set the mul label to "Morlanda"
LAST	Lmul	"Morlanda"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q6001555 Carl Claes Mörner af Morlanda: P734 family name = the item just created
Q6001555	P734	LAST	S2600	"6000000006127542348"
#   Q6001608 Hampus Elof Mörner af Morlanda: P734 family name = the item just created
Q6001608	P734	LAST	S2600	"6000000006127550611"
#   Q19828095 Carl Mörner af Morlanda: P734 family name = the item just created
Q19828095	P734	LAST	S2600	"6000000006127570365"
#   Q6001589 Carl Stellan Mörner af Morlanda: P734 family name = the item just created
Q6001589	P734	LAST	S2600	"6000000011399399424"
#   Q792307 Axel Otto Mörner af Morlanda: P734 family name = the item just created
Q792307	P734	LAST	S2600	"6000000017999766001"

# Eriksdatter -- patronymic, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Eriksdatter"
LAST	Len	"Eriksdatter"
#   set the mul label to "Eriksdatter"
LAST	Lmul	"Eriksdatter"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141178196 Elisabet Kirstine Eriksdatter Stangeland: P5056 patronym or matronym = the item just created, qualified P144 based on Q141198393 Erik Erikson Stangeland
Q141178196	P5056	LAST	P144	Q141198393	S2600	"6000000003491986941"
#   Q141216492 Marta Eriksdatter Fotland: P5056 patronym or matronym = the item just created
Q141216492	P5056	LAST	S2600	"6000000007974940020"
#   Q141216383 Ingeborg Eriksdatter Bjorland: P5056 patronym or matronym = the item just created
Q141216383	P5056	LAST	S2600	"6000000014100949863"
#   Q141217392 Larine Eriksdatter Heigre: P5056 patronym or matronym = the item just created, qualified P144 based on Q141198393 Erik Erikson Stangeland
Q141217392	P5056	LAST	P144	Q141198393	S2600	"6000000201256773828"

# Fersen -- patronymic, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Fersen"
LAST	Len	"Fersen"
#   set the mul label to "Fersen"
LAST	Lmul	"Fersen"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q469962 Eva Sophia Sofia von Fersen: P5056 patronym or matronym = the item just created
Q469962	P5056	LAST	S2600	"1551393"
#   Q455071 Hans Axel "Den Yngre" von Fersen: P5056 patronym or matronym = the item just created
Q455071	P5056	LAST	S2600	"6000000001515418125"
#   Q3129338 Hedvig Eleonora von Fersen: P5056 patronym or matronym = the item just created
Q3129338	P5056	LAST	S2600	"6000000008778922864"
#   Q19312912 Fabian Reinhold von Fersen: P5056 patronym or matronym = the item just created
Q19312912	P5056	LAST	S2600	"6000000008778928032"

# Gennäs -- family, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Gennäs"
LAST	Len	"Gennäs"
#   set the mul label to "Gennäs"
LAST	Lmul	"Gennäs"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q5580888 Erik Gustaf Boije af Gennäs: P734 family name = the item just created
Q5580888	P734	LAST	S2600	"6000000006127120913"
#   Q5580881 Carl Gustaf Boije af Gennäs: P734 family name = the item just created
Q5580881	P734	LAST	S2600	"6000000011536457635"
#   Q141219062 Hedvig Ulrika Boije af Gennäs: P734 family name = the item just created, qualified P3831 object of statement has role Q28418670 married name
Q141219062	P734	LAST	P3831	Q28418670	S2600	"6000000012888307497"
#   Q5580892 Fredrik Carl Boije af Gennäs: P734 family name = the item just created
Q5580892	P734	LAST	S2600	"6000000020865415341"

# 223 more name items are needed and wait for a later
# run -- 10 a day is her cap, not a limit of the data:
#   Andersson (patronymic), 3 bearer(s)
#   Erikson (patronymic), 3 bearer(s)
#   Hansson (patronymic), 3 bearer(s)
#   Helgesen (patronymic), 3 bearer(s)
#   Høle (family), 3 bearer(s)
#   Jonson (patronymic), 3 bearer(s)
#   Jonsson (patronymic), 3 bearer(s)
#   Kristiansen (patronymic), 3 bearer(s)
#   Låge-Håland (family), 3 bearer(s)
#   Osmundsdatter (patronymic), 3 bearer(s)
#   Voster (family), 3 bearer(s)
#   Ådnesdatter (patronymic), 3 bearer(s)
#   ... and 211 more

