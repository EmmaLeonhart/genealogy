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

# Tunheim -- family, 23 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Tunheim"
LAST	Len	"Tunheim"
#   set the mul label to "Tunheim"
LAST	Lmul	"Tunheim"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q141162046 Ane Oline "Lena" Eivindsdatter Garborg: P734 family name = the item just created, qualified object of statement has role Q28418670 married name
Q141162046	P734	LAST	P3831	Q28418670	S2600	"6000000003492005156"
#   Q141189108 Tillie Betsy Tunheim: P734 family name = the item just created, qualified object of statement has role Q2507958 birth name
Q141189108	P734	LAST	P3831	Q2507958	S2600	"6000000008542267056"
#   Q141189084 Martin Tollefson Tunheim: P734 family name = the item just created
Q141189084	P734	LAST	S2600	"6000000019384841547"
#   Q141169062 Thoralf Tunheim: P734 family name = the item just created
Q141169062	P734	LAST	S2600	"6000000033773881611"
#   Q141168801 Cora Estelle Tunheim: P734 family name = the item just created, qualified object of statement has role Q2507958 birth name
Q141168801	P734	LAST	P3831	Q2507958	S2600	"6000000033773908408"
#   Q141168809 Edward Tunheim: P734 family name = the item just created
Q141168809	P734	LAST	S2600	"6000000033773925586"
#   Q141168787 Alma Matilda Tunheim: P734 family name = the item just created, qualified object of statement has role Q2507958 birth name
Q141168787	P734	LAST	P3831	Q2507958	S2600	"6000000033774070464"
#   Q141169041 Olaf Tunheim: P734 family name = the item just created
Q141169041	P734	LAST	S2600	"6000000033774204088"
#   Q141168788 Arne Garborg Tunheim: P734 family name = the item just created
Q141168788	P734	LAST	S2600	"6000000037693739967"
#   Q141180396 Tollef Tollefson Tunheim: P734 family name = the item just created
Q141180396	P734	LAST	S2600	"6000000037737683245"
#   Q141168794 Betsy Jacobson: P734 family name = the item just created, qualified object of statement has role Q28418670 married name
Q141168794	P734	LAST	P3831	Q28418670	S2600	"6000000037737979829"
#   Q141189107 Theodore Roosevelt Tunheim: P734 family name = the item just created
Q141189107	P734	LAST	S2600	"6000000039507759313"
#   Q141189102 Sigrid "Sally" Manilva Tunheim: P734 family name = the item just created, qualified object of statement has role Q2507958 birth name
Q141189102	P734	LAST	P3831	Q2507958	S2600	"6000000039507820846"
#   Q141189056 Bella Jeanette Tunheim: P734 family name = the item just created, qualified object of statement has role Q2507958 birth name
Q141189056	P734	LAST	P3831	Q2507958	S2600	"6000000039507887815"
#   Q141189074 Joseph Tunheim: P734 family name = the item just created
Q141189074	P734	LAST	S2600	"6000000039508106907"
#   Q141189049 Alfred Tunheim: P734 family name = the item just created
Q141189049	P734	LAST	S2600	"6000000039510214027"
#   Q141189063 Elsie Pauline Tunheim: P734 family name = the item just created, qualified object of statement has role Q2507958 birth name
Q141189063	P734	LAST	P3831	Q2507958	S2600	"6000000039510338057"
#   Q141189100 Rose Tunheim: P734 family name = the item just created, qualified object of statement has role Q2507958 birth name
Q141189100	P734	LAST	P3831	Q2507958	S2600	"6000000039510583899"
#   Q141189101 Samuel Tunheim: P734 family name = the item just created
Q141189101	P734	LAST	S2600	"6000000039510735157"
#   Q141189095 Peter Tunheim: P734 family name = the item just created
Q141189095	P734	LAST	S2600	"6000000039510875837"
#   Q141189109 Tollef "Bud" Tunheim: P734 family name = the item just created
Q141189109	P734	LAST	S2600	"6000000039510907240"

# Bergersen -- patronymic, 9 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Bergersen"
LAST	Len	"Bergersen"
#   set the mul label to "Bergersen"
LAST	Lmul	"Bergersen"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q3143008 Karen Hulda Bergersen: P5056 patronym or matronym = the item just created, qualified based on Q141168797 Christian Frederik Bergersen
Q3143008	P5056	LAST	P144	Q141168797	S2600	"6000000005606976813"
#   Q141168797 Christian Frederik Bergersen: P5056 patronym or matronym = the item just created, qualified based on Q141178199 Gunder Bergersen
Q141168797	P5056	LAST	P144	Q141178199	S2600	"6000000009126453497"
#   Q141189112 Wilhelmine Sophie Bergersen: P5056 patronym or matronym = the item just created, qualified based on Q141168797 Christian Frederik Bergersen
Q141189112	P5056	LAST	P144	Q141168797	S2600	"6000000014026120692"
#   Q141189083 Martha Elida Bergersen: P5056 patronym or matronym = the item just created, qualified based on Q141168797 Christian Frederik Bergersen
Q141189083	P5056	LAST	P144	Q141168797	S2600	"6000000014026305107"
#   Q141178199 Gunder Bergersen: P5056 patronym or matronym = the item just created
Q141178199	P5056	LAST	S2600	"6000000016756402733"
#   Q141189064 Georg August Bergersen: P5056 patronym or matronym = the item just created, qualified based on Q141178199 Gunder Bergersen
Q141189064	P5056	LAST	P144	Q141178199	S2600	"6000000020220377527"
#   Q141189065 Gustav Adolf Bergersen Næsmoen: P5056 patronym or matronym = the item just created, qualified based on Q141178199 Gunder Bergersen
Q141189065	P5056	LAST	P144	Q141178199	S2600	"6000000020220981823"
#   Q141189093 Oline Mathea Bergersen: P5056 patronym or matronym = the item just created, qualified based on Q141178199 Gunder Bergersen
Q141189093	P5056	LAST	P144	Q141178199	S2600	"6000000022418305015"
#   Q141189091 Ole Nicolai Bergersen: P5056 patronym or matronym = the item just created, qualified based on Q141168797 Christian Frederik Bergersen
Q141189091	P5056	LAST	P144	Q141168797	S2600	"6000000055822412855"

# Ronneberg -- family, 7 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Ronneberg"
LAST	Len	"Ronneberg"
#   set the mul label to "Ronneberg"
LAST	Lmul	"Ronneberg"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q141162043 Inger Marie "Mary" Eivindsdatter Garborg: P734 family name = the item just created, qualified object of statement has role Q28418670 married name
Q141162043	P734	LAST	P3831	Q28418670	S2600	"6000000003492005141"
#   Q141168820 Eliza Ronneberg: P734 family name = the item just created
Q141168820	P734	LAST	S2600	"6000000035698428095"
#   Q141168789 Arnold Ronneberg: P734 family name = the item just created
Q141168789	P734	LAST	S2600	"6000000035698494074"
#   Q141168805 Edward Ronneberg: P734 family name = the item just created
Q141168805	P734	LAST	S2600	"6000000035698546990"
#   Q141168786 Alice Ronneberg: P734 family name = the item just created
Q141168786	P734	LAST	S2600	"6000000035698611873"
#   Q141168824 Ernest Anton Ronneberg: P734 family name = the item just created
Q141168824	P734	LAST	S2600	"6000000035698619913"

# Bø -- family, 5 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Bø"
LAST	Len	"Bø"
#   set the mul label to "Bø"
LAST	Lmul	"Bø"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q141168816 Elisabet Ådnesdatter Garborg: P734 family name = the item just created, qualified object of statement has role Q28418670 married name
Q141168816	P734	LAST	P3831	Q28418670	S2600	"6000000003492005176"
#   Q141189066 Helge Rasmusson Bø: P734 family name = the item just created
Q141189066	P734	LAST	S2600	"6000000003492005191"
#   Q141189099 Rasmus Helgesen Bø: P734 family name = the item just created
Q141189099	P734	LAST	S2600	"6000000021133770643"
#   Q141189054 Anna Maria Helgesdatter Bø: P734 family name = the item just created
Q141189054	P734	LAST	S2600	"6000000196542059842"
#   Q141189113 Ådne Helgesen Bø: P734 family name = the item just created
Q141189113	P734	LAST	S2600	"6000000196542455825"

# Heigre -- family, 5 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Heigre"
LAST	Len	"Heigre"
#   set the mul label to "Heigre"
LAST	Lmul	"Heigre"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q141168957 Jonas Jonson Heigre: P734 family name = the item just created
Q141168957	P734	LAST	S2600	"6000000003491986771"
#   Q141189070 John Jonassen Heigre: P734 family name = the item just created, qualified object of statement has role Q2507958 birth name
Q141189070	P734	LAST	P3831	Q2507958	S2600	"6000000003491986951"
#   Q141178198 Enevald Jonasson Heigre: P734 family name = the item just created
Q141178198	P734	LAST	S2600	"6000000003491986956"
#   Q141189098 Rakel Jonasdatter Heigre: P734 family name = the item just created
Q141189098	P734	LAST	S2600	"6000000003491986966"
#   Q141189081 Lotte Birgithe Gustava Jonasdatter Heigre: P734 family name = the item just created, qualified object of statement has role Q2507958 birth name
Q141189081	P734	LAST	P3831	Q2507958	S2600	"6000000025793394310"

# Sør-Reime -- family, 5 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Sør-Reime"
LAST	Len	"Sør-Reime"
#   set the mul label to "Sør-Reime"
LAST	Lmul	"Sør-Reime"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q141189076 Kristian Larsen Nord-Varhaug: P734 family name = the item just created
Q141189076	P734	LAST	S2600	"6000000029302543031"
#   Q141189067 Helmik Kristiansen Sør-Reime: P734 family name = the item just created
Q141189067	P734	LAST	S2600	"6000000221449620901"
#   Q141189078 Lars Kristiansen Sør-Reime: P734 family name = the item just created
Q141189078	P734	LAST	S2600	"6000000224702528843"
#   Q141189077 Lars Bernhard Kristiansen Sør-Reime: P734 family name = the item just created
Q141189077	P734	LAST	S2600	"6000000224702710821"

# Grøtheim -- family, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Grøtheim"
LAST	Len	"Grøtheim"
#   set the mul label to "Grøtheim"
LAST	Lmul	"Grøtheim"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q141169072 Ådne Olsen Grøtheim: P734 family name = the item just created, qualified object of statement has role Q2507958 birth name
Q141169072	P734	LAST	P3831	Q2507958	S2600	"6000000003492005161"
#   Q141189088 Ola Knutsen Garborg: P734 family name = the item just created
Q141189088	P734	LAST	S2600	"6000000007744588495"
#   Q141189069 Ingeborg Ådnesdatter Grøtheim: P734 family name = the item just created
Q141189069	P734	LAST	S2600	"6000000008176802346"

# Jonsdatter -- patronymic, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Jonsdatter"
LAST	Len	"Jonsdatter"
#   set the mul label to "Jonsdatter"
LAST	Lmul	"Jonsdatter"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141152523 Ane Oline Jonsdatter Raugstad: P5056 patronym or matronym = the item just created, qualified based on Q141168955 Jon Samuelsen Raustad
Q141152523	P5056	LAST	P144	Q141168955	S2600	"6000000003491986946"
#   Q141178381 Marta Jonsdatter Li: P5056 patronym or matronym = the item just created, qualified based on Q141180408 Jon Larsson Li
Q141178381	P5056	LAST	P144	Q141180408	S2600	"6000000003491988826"
#   Q141189071 Joren Jonsdatter Espedal: P5056 patronym or matronym = the item just created
Q141189071	P5056	LAST	S2600	"6000000005609425388"
#   Q141189062 Cecilie Jonsdatter: P5056 patronym or matronym = the item just created
Q141189062	P5056	LAST	S2600	"6000000180296055830"

# Nyvold -- family, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Nyvold"
LAST	Len	"Nyvold"
#   set the mul label to "Nyvold"
LAST	Lmul	"Nyvold"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q138474188 Hans Syvertsen Nyvold: P734 family name = the item just created
Q138474188	P734	LAST	S2600	"6000000021197598122"
#   Q141168785 Aagot Nyvold: P734 family name = the item just created, qualified object of statement has role Q2507958 birth name
Q141168785	P734	LAST	P3831	Q2507958	S2600	"6000000021197722738"
#   Q141168803 Dagny Nyvold: P734 family name = the item just created, qualified object of statement has role Q2507958 birth name
Q141168803	P734	LAST	P3831	Q2507958	S2600	"6000000021197841042"
#   Q141178197 Elisabeth Johannesen: P734 family name = the item just created, qualified object of statement has role Q28418670 married name
Q141178197	P734	LAST	P3831	Q28418670	S2600	"6000000021198042859"

# Eivindsdatter -- patronymic, 3 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Eivindsdatter"
LAST	Len	"Eivindsdatter"
#   set the mul label to "Eivindsdatter"
LAST	Lmul	"Eivindsdatter"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141152600 Stine "Stena" Eivindsdatter Garborg: P5056 patronym or matronym = the item just created, qualified based on Q141152512 Eivind Aadnesson Garborg
Q141152600	P5056	LAST	P144	Q141152512	S2600	"6000000003492005121"
#   Q141162043 Inger Marie "Mary" Eivindsdatter Garborg: P5056 patronym or matronym = the item just created, qualified based on Q141152512 Eivind Aadnesson Garborg
Q141162043	P5056	LAST	P144	Q141152512	S2600	"6000000003492005141"
#   Q141162046 Ane Oline "Lena" Eivindsdatter Garborg: P5056 patronym or matronym = the item just created, qualified based on Q141152512 Eivind Aadnesson Garborg
Q141162046	P5056	LAST	P144	Q141152512	S2600	"6000000003492005156"

# 147 more name items are needed and wait for a later
# run -- 10 a day is her cap, not a limit of the data:
#   Eivindsen (patronymic), 3 bearer(s)
#   Eivindson (patronymic), 3 bearer(s)
#   Jonson (patronymic), 3 bearer(s)
#   Kristiansen (patronymic), 3 bearer(s)
#   Pierson (family), 3 bearer(s)
#   Sandsmark (family), 3 bearer(s)
#   Ådnesdatter (patronymic), 3 bearer(s)
#   Ebbesdatter (patronymic), 2 bearer(s)
#   Edlund (family), 2 bearer(s)
#   Erikson (patronymic), 2 bearer(s)
#   Espedal (family), 2 bearer(s)
#   Gundersen (patronymic), 2 bearer(s)
#   ... and 135 more

# NOT created -- the plan says these already resolve to more than
# one item, and creating another is the Maria failure that would
# have made a tenth. Emma picks, the person's sex decides.
#   Anna (given), 4 bearer(s)
#   Bure (family), 1 bearer(s)
#   Christopher (given), 1 bearer(s)
#   John (given), 1 bearer(s)
#   Karen (given), 1 bearer(s)
#   LeRoy (given), 1 bearer(s)
#   Li (family), 3 bearer(s)
#   Maria (given), 1 bearer(s)
#   Olga (given), 1 bearer(s)
#   Sophia (given), 1 bearer(s)
