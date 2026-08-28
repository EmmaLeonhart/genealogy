# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the mul label to "NN Garborg"
LAST	Lmul	"NN Garborg"
#   set the ca label to "filla de Arne Olaus Fjørtoft Garborg"
LAST	Lca	"filla de Arne Olaus Fjørtoft Garborg"
#   set the da label to "datter af Arne Olaus Fjørtoft Garborg"
LAST	Lda	"datter af Arne Olaus Fjørtoft Garborg"
#   set the de label to "Tochter von Arne Olaus Fjørtoft Garborg"
LAST	Lde	"Tochter von Arne Olaus Fjørtoft Garborg"
#   set the en label to "daughter of Arne Olaus Fjørtoft Garborg"
LAST	Len	"daughter of Arne Olaus Fjørtoft Garborg"
#   set the es label to "hija de Arne Olaus Fjørtoft Garborg"
LAST	Les	"hija de Arne Olaus Fjørtoft Garborg"
#   set the it label to "figlia di Arne Olaus Fjørtoft Garborg"
LAST	Lit	"figlia di Arne Olaus Fjørtoft Garborg"
#   set the ja label to "アルネ・オーラウス・フョルトフト・ガルボルグの娘"
LAST	Lja	"アルネ・オーラウス・フョルトフト・ガルボルグの娘"
#   set the nb label to "datter av Arne Olaus Fjørtoft Garborg"
LAST	Lnb	"datter av Arne Olaus Fjørtoft Garborg"
#   set the nl label to "dochter van Arne Olaus Fjørtoft Garborg"
LAST	Lnl	"dochter van Arne Olaus Fjørtoft Garborg"
#   set the pt label to "filha de Arne Olaus Fjørtoft Garborg"
LAST	Lpt	"filha de Arne Olaus Fjørtoft Garborg"
#   set the sv label to "dotter till Arne Olaus Fjørtoft Garborg"
LAST	Lsv	"dotter till Arne Olaus Fjørtoft Garborg"
#   set the zh label to "阿尔内·奥劳斯·夫约托夫特·加尔博格之女"
LAST	Lzh	"阿尔内·奥劳斯·夫约托夫特·加尔博格之女"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000021223364767 NN Garborg
LAST	P2600	"6000000021223364767"
#   P22 father = Q11959067 Arne Olaus Fjørtoft Garborg
LAST	P22	Q11959067	S2600	"6000000021223364767"
#   P25 mother = Q141168785 Aagot Nyvold
LAST	P25	Q141168785	S2600	"6000000021223364767"
#   Q11959067 Arne Olaus Fjørtoft Garborg: P40 child = the item just created
Q11959067	P40	LAST	S2600	"6000000021223364767"
#   Q141168785 Aagot Nyvold: P40 child = the item just created
Q141168785	P40	LAST	S2600	"6000000021223364767"

# create a new item
CREATE
#   the item just created: set the en label to "Agnes Tunheim"
LAST	Len	"Agnes Tunheim"
#   set the mul label to "Agnes Tunheim"
LAST	Lmul	"Agnes Tunheim"
#   add a mul alias "Agnes Bakke"
LAST	Amul	"Agnes Bakke"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000039512807134 Agnes Bakke
LAST	P2600	"6000000039512807134"
#   P569 date of birth = +1897-12-15T00:00:00Z/11
LAST	P569	+1897-12-15T00:00:00Z/11	S2600	"6000000039512807134"
#   P570 date of death = +1999-12-15T00:00:00Z/11
LAST	P570	+1999-12-15T00:00:00Z/11	S2600	"6000000039512807134"
#   P26 spouse = Q141168809 Edward Tunheim
LAST	P26	Q141168809	S2600	"6000000039512807134"
#   P40 child = Q141198399 Eugene LeRoy Tunheim
LAST	P40	Q141198399	S2600	"6000000039512807134"
#   Q141168809 Edward Tunheim: P26 spouse = the item just created
Q141168809	P26	LAST	S2600	"6000000039512807134"
#   Q141198399 Eugene LeRoy Tunheim: P25 mother = the item just created
Q141198399	P25	LAST	S2600	"6000000039512807134"
#   the item just created: P735 given name = Q394431 Agnes
LAST	P735	Q394431
#   P734 family name = Q27887927 Bakke, qualified object of statement has role Q2507958 birth name
LAST	P734	Q27887927	P3831	Q2507958

# create a new item
CREATE
#   set the en label to "Arne Martin Tunheim"
LAST	Len	"Arne Martin Tunheim"
#   set the mul label to "Arne Martin Tunheim"
LAST	Lmul	"Arne Martin Tunheim"
#   set the ja label to "アルネ・マルティン・トゥンヘイム"
LAST	Lja	"アルネ・マルティン・トゥンヘイム"
#   set the zh label to "阿尔内·马丁·通海姆"
LAST	Lzh	"阿尔内·马丁·通海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000033773894299 Arne Martin Tunheim
LAST	P2600	"6000000033773894299"
#   P569 date of birth = +1931-08-03T00:00:00Z/11
LAST	P569	+1931-08-03T00:00:00Z/11	S2600	"6000000033773894299"
#   P570 date of death = +2005-01-06T00:00:00Z/11
LAST	P570	+2005-01-06T00:00:00Z/11	S2600	"6000000033773894299"
#   P22 father = Q141189084 Martin Tollefson Tunheim
LAST	P22	Q141189084	S2600	"6000000033773894299"
#   Q141189084 Martin Tollefson Tunheim: P40 child = the item just created
Q141189084	P40	LAST	S2600	"6000000033773894299"
#   the item just created: P735 given name = Q645757 Arne, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q645757	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18002399 Martin, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q18002399	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Cal Verna Marie Gary"
LAST	Len	"Cal Verna Marie Gary"
#   set the mul label to "Cal Verna Marie Gary"
LAST	Lmul	"Cal Verna Marie Gary"
#   add a mul alias "Cal Verna Marie Tunheim"
LAST	Amul	"Cal Verna Marie Tunheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000180009481886 Cal Verna Marie Tunheim
LAST	P2600	"6000000180009481886"
#   P569 date of birth = +1936-03-23T00:00:00Z/11
LAST	P569	+1936-03-23T00:00:00Z/11	S2600	"6000000180009481886"
#   P570 date of death = +2007-09-11T00:00:00Z/11
LAST	P570	+2007-09-11T00:00:00Z/11	S2600	"6000000180009481886"
#   P22 father = Q141189049 Alfred Tunheim
LAST	P22	Q141189049	S2600	"6000000180009481886"
#   P25 mother = Q141200084 Selma Johanna Horton
LAST	P25	Q141200084	S2600	"6000000180009481886"
#   Q141189049 Alfred Tunheim: P40 child = the item just created
Q141189049	P40	LAST	S2600	"6000000180009481886"
#   Q141200084 Selma Johanna Horton: P40 child = the item just created
Q141200084	P40	LAST	S2600	"6000000180009481886"
#   the item just created: P735 given name = Q11900974 Verna, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q11900974	P1545	"2"	P3831	Q245025
#   P735 given name = Q106674406 Marie, qualified series ordinal 3, object of statement has role Q245025 middle name
LAST	P735	Q106674406	P1545	"3"	P3831	Q245025
#   P1449 nickname = en:"Calverna"
LAST	P1449	en:"Calverna"
#   add a mul alias "Calverna Gary"
LAST	Amul	"Calverna Gary"

# create a new item
CREATE
#   set the en label to "Daniel Olofsson"
LAST	Len	"Daniel Olofsson"
#   set the mul label to "Daniel Olofsson"
LAST	Lmul	"Daniel Olofsson"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000001139071013 Daniel Olofsson
LAST	P2600	"6000000001139071013"
#   P569 date of birth = +1609-00-00T00:00:00Z/9
LAST	P569	+1609-00-00T00:00:00Z/9	S2600	"6000000001139071013"
#   P25 mother = Q141200604 Anna Nilsdotter
LAST	P25	Q141200604	S2600	"6000000001139071013"
#   Q141200604 Anna Nilsdotter: P40 child = the item just created
Q141200604	P40	LAST	S2600	"6000000001139071013"
#   the item just created: P735 given name = Q53787734 Daniel
LAST	P735	Q53787734
#   P734 family name = Q23645132 Olofsson
LAST	P734	Q23645132

# create a new item
CREATE
#   set the en label to "Geneva Bell Gullingsrud Romans"
LAST	Len	"Geneva Bell Gullingsrud Romans"
#   set the mul label to "Geneva Bell Gullingsrud Romans"
LAST	Lmul	"Geneva Bell Gullingsrud Romans"
#   add a mul alias "Geneva Bell Tunheim"
LAST	Amul	"Geneva Bell Tunheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000180033404926 Geneva Bell Tunheim
LAST	P2600	"6000000180033404926"
#   P569 date of birth = +1923-08-25T00:00:00Z/11
LAST	P569	+1923-08-25T00:00:00Z/11	S2600	"6000000180033404926"
#   P570 date of death = +1983-04-09T00:00:00Z/11
LAST	P570	+1983-04-09T00:00:00Z/11	S2600	"6000000180033404926"
#   P22 father = Q141168809 Edward Tunheim
LAST	P22	Q141168809	S2600	"6000000180033404926"
#   Q141168809 Edward Tunheim: P40 child = the item just created
Q141168809	P40	LAST	S2600	"6000000180033404926"
#   the item just created: P735 given name = Q28707501 Geneva, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q28707501	P1545	"1"	P7452	Q3409033
#   P735 given name = Q21423096 Bell, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q21423096	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Gudrun Sæbjørnsdatter Talgje"
LAST	Len	"Gudrun Sæbjørnsdatter Talgje"
#   set the mul label to "Gudrun Sæbjørnsdatter Talgje"
LAST	Lmul	"Gudrun Sæbjørnsdatter Talgje"
#   add a mul alias "Gudrun Sæbjørnsdatter Nord-Talgje"
LAST	Amul	"Gudrun Sæbjørnsdatter Nord-Talgje"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000001169235389 Gudrun Sæbjørnsdatter Nord-Talgje
LAST	P2600	"6000000001169235389"
#   P569 date of birth = +1550-00-00T00:00:00Z/9
LAST	P569	+1550-00-00T00:00:00Z/9	S2600	"6000000001169235389"
#   P570 date of death = +1617-00-00T00:00:00Z/9
LAST	P570	+1617-00-00T00:00:00Z/9	S2600	"6000000001169235389"
#   P22 father = Q141200111 Sæbjørn Toresson Talgje
LAST	P22	Q141200111	S2600	"6000000001169235389"
#   P25 mother = Q141200101 Sissel Jonsdatter Aukland
LAST	P25	Q141200101	S2600	"6000000001169235389"
#   Q141200111 Sæbjørn Toresson Talgje: P40 child = the item just created
Q141200111	P40	LAST	S2600	"6000000001169235389"
#   Q141200101 Sissel Jonsdatter Aukland: P40 child = the item just created
Q141200101	P40	LAST	S2600	"6000000001169235389"
#   the item just created: P735 given name = Q1553074 Gudrun
LAST	P735	Q1553074
#   P1449 nickname = en:"Guri"
LAST	P1449	en:"Guri"
#   add a mul alias "Guri Talgje"
LAST	Amul	"Guri Talgje"
#   add a mul alias "Gudrun Talgje"
LAST	Amul	"Gudrun Talgje"

# create a new item
CREATE
#   set the en label to "Hallvord Randa"
LAST	Len	"Hallvord Randa"
#   set the mul label to "Hallvord Randa"
LAST	Lmul	"Hallvord Randa"
#   add a mul alias "Hallvord Hesbø"
LAST	Amul	"Hallvord Hesbø"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000001169235380 Hallvord (Knutsson Hage?) Hesbø
LAST	P2600	"6000000001169235380"
#   P569 date of birth = +1540-00-00T00:00:00Z/9
LAST	P569	+1540-00-00T00:00:00Z/9	S2600	"6000000001169235380"
#   P570 date of death = +1580-00-00T00:00:00Z/9
LAST	P570	+1580-00-00T00:00:00Z/9	S2600	"6000000001169235380"
#   P1449 nickname = en:"Knutsson Hage?"
LAST	P1449	en:"Knutsson Hage?"
#   P1449 nickname = en:"Haldor"
LAST	P1449	en:"Haldor"
#   add a mul alias "Knutsson Hage? Randa"
LAST	Amul	"Knutsson Hage? Randa"
#   add a mul alias "Haldor Randa"
LAST	Amul	"Haldor Randa"

# create a new item
CREATE
#   set the en label to "Hans Olsen Grøtheim"
LAST	Len	"Hans Olsen Grøtheim"
#   set the mul label to "Hans Olsen Grøtheim"
LAST	Lmul	"Hans Olsen Grøtheim"
#   set the ja label to "ハンス・オルセン・グレートヘイム"
LAST	Lja	"ハンス・オルセン・グレートヘイム"
#   set the zh label to "汉斯·奥尔森·格勒特海姆"
LAST	Lzh	"汉斯·奥尔森·格勒特海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000008176954243 Hans Olsen Grøtheim
LAST	P2600	"6000000008176954243"
#   P569 date of birth = +1790-02-07T00:00:00Z/11
LAST	P569	+1790-02-07T00:00:00Z/11	S2600	"6000000008176954243"
#   P570 date of death = +1801-00-00T00:00:00Z/9
LAST	P570	+1801-00-00T00:00:00Z/9	S2600	"6000000008176954243"
#   P22 father = Q141189088 Ola Knutsen Garborg
LAST	P22	Q141189088	S2600	"6000000008176954243"
#   P25 mother = Q141199830 Anna Rasmusdatter Årsland
LAST	P25	Q141199830	S2600	"6000000008176954243"
#   Q141189088 Ola Knutsen Garborg: P40 child = the item just created
Q141189088	P40	LAST	S2600	"6000000008176954243"
#   Q141199830 Anna Rasmusdatter Årsland: P40 child = the item just created
Q141199830	P40	LAST	S2600	"6000000008176954243"

# create a new item
CREATE
#   the item just created: set the en label to "Hindrik Fransson vintappare"
LAST	Len	"Hindrik Fransson vintappare"
#   set the mul label to "Hindrik Fransson vintappare"
LAST	Lmul	"Hindrik Fransson vintappare"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000027488689563 Hindrik Fransson vintappare
LAST	P2600	"6000000027488689563"
#   P26 spouse = Q141189058 Brita Thomasdotter
LAST	P26	Q141189058	S2600	"6000000027488689563"
#   Q141189058 Brita Thomasdotter: P26 spouse = the item just created
Q141189058	P26	LAST	S2600	"6000000027488689563"
#   the item just created: P1449 nickname = en:"Henrik Heinrich Frantzson"
LAST	P1449	en:"Henrik Heinrich Frantzson"
#   add a mul alias "Henrik Heinrich Frantzson Fransson vintappare"
LAST	Amul	"Henrik Heinrich Frantzson Fransson vintappare"

# create a new item
CREATE
#   set the en label to "Janna Joakimsdatter Lea"
LAST	Len	"Janna Joakimsdatter Lea"
#   set the mul label to "Janna Joakimsdatter Lea"
LAST	Lmul	"Janna Joakimsdatter Lea"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000025813347852 Janna Joakimsdatter Lea
LAST	P2600	"6000000025813347852"
#   P569 date of birth = +1907-12-19T00:00:00Z/11
LAST	P569	+1907-12-19T00:00:00Z/11	S2600	"6000000025813347852"
#   P570 date of death = +1935-08-01T00:00:00Z/11
LAST	P570	+1935-08-01T00:00:00Z/11	S2600	"6000000025813347852"
#   P25 mother = Q141189081 Lotte Birgithe Gustava Jonasdatter Heigre
LAST	P25	Q141189081	S2600	"6000000025813347852"
#   Q141189081 Lotte Birgithe Gustava Jonasdatter Heigre: P40 child = the item just created
Q141189081	P40	LAST	S2600	"6000000025813347852"
#   the item just created: P735 given name = Q20000584 Janna
LAST	P735	Q20000584
#   P734 family name = Q6508166 Lea
LAST	P734	Q6508166

# create a new item
CREATE
#   set the en label to "Joachim Johnson Lea"
LAST	Len	"Joachim Johnson Lea"
#   set the mul label to "Joachim Johnson Lea"
LAST	Lmul	"Joachim Johnson Lea"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000025793788004 Joachim Johnson Lea
LAST	P2600	"6000000025793788004"
#   P569 date of birth = +1874-10-16T00:00:00Z/11
LAST	P569	+1874-10-16T00:00:00Z/11	S2600	"6000000025793788004"
#   P570 date of death = +1960-06-29T00:00:00Z/11
LAST	P570	+1960-06-29T00:00:00Z/11	S2600	"6000000025793788004"
#   P26 spouse = Q141189081 Lotte Birgithe Gustava Jonasdatter Heigre
LAST	P26	Q141189081	S2600	"6000000025793788004"
#   Q141189081 Lotte Birgithe Gustava Jonasdatter Heigre: P26 spouse = the item just created
Q141189081	P26	LAST	S2600	"6000000025793788004"
#   the item just created: P735 given name = Q4926961 Joachim
LAST	P735	Q4926961
#   P734 family name = Q6508166 Lea
LAST	P734	Q6508166

# create a new item
CREATE
#   set the en label to "Jon Olson Raustad"
LAST	Len	"Jon Olson Raustad"
#   set the mul label to "Jon Olson Raustad"
LAST	Lmul	"Jon Olson Raustad"
#   set the ja label to "ヨン・オルソン・ラウスタード"
LAST	Lja	"ヨン・オルソン・ラウスタード"
#   set the zh label to "永·奥尔松·劳斯塔"
LAST	Lzh	"永·奥尔松·劳斯塔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003491988836 Jon Olson Raustad
LAST	P2600	"6000000003491988836"
#   P569 date of birth = +1708-09-29T00:00:00Z/11
LAST	P569	+1708-09-29T00:00:00Z/11	S2600	"6000000003491988836"
#   P570 date of death = +1769-00-00T00:00:00Z/9
LAST	P570	+1769-00-00T00:00:00Z/9	S2600	"6000000003491988836"
#   P40 child = Q141178380 Samuel Jonson Raustad
LAST	P40	Q141178380	S2600	"6000000003491988836"
#   Q141178380 Samuel Jonson Raustad: P22 father = the item just created
Q141178380	P22	LAST	S2600	"6000000003491988836"
#   the item just created: P735 given name = Q13501137 Jon
LAST	P735	Q13501137

# create a new item
CREATE
#   set the en label to "Jorunn Jonsdatter Li"
LAST	Len	"Jorunn Jonsdatter Li"
#   set the mul label to "Jorunn Jonsdatter Li"
LAST	Lmul	"Jorunn Jonsdatter Li"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000038211894304 Jorunn Jonsdatter Li
LAST	P2600	"6000000038211894304"
#   P569 date of birth = +1746-00-00T00:00:00Z/9
LAST	P569	+1746-00-00T00:00:00Z/9	S2600	"6000000038211894304"
#   P570 date of death = +1814-00-00T00:00:00Z/9
LAST	P570	+1814-00-00T00:00:00Z/9	S2600	"6000000038211894304"
#   P22 father = Q141180408 Jon Larsson Li
LAST	P22	Q141180408	S2600	"6000000038211894304"
#   P25 mother = Q141180412 Marta Rasmusdatter Høle
LAST	P25	Q141180412	S2600	"6000000038211894304"
#   Q141180408 Jon Larsson Li: P40 child = the item just created
Q141180408	P40	LAST	S2600	"6000000038211894304"
#   Q141180412 Marta Rasmusdatter Høle: P40 child = the item just created
Q141180412	P40	LAST	S2600	"6000000038211894304"
#   the item just created: P735 given name = Q1799021 Jorunn
LAST	P735	Q1799021
#   add a mul alias "Jorunn Li"
LAST	Amul	"Jorunn Li"

# create a new item
CREATE
#   set the en label to "Kirsten Gabrielsdatter Austråt"
LAST	Len	"Kirsten Gabrielsdatter Austråt"
#   set the mul label to "Kirsten Gabrielsdatter Austråt"
LAST	Lmul	"Kirsten Gabrielsdatter Austråt"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003491988841 Kirsten Gabrielsdatter Austråt
LAST	P2600	"6000000003491988841"
#   P569 date of birth = +1712-03-05T00:00:00Z/11
LAST	P569	+1712-03-05T00:00:00Z/11	S2600	"6000000003491988841"
#   P570 date of death = +1778-03-08T00:00:00Z/11
LAST	P570	+1778-03-08T00:00:00Z/11	S2600	"6000000003491988841"
#   P40 child = Q141178380 Samuel Jonson Raustad
LAST	P40	Q141178380	S2600	"6000000003491988841"
#   Q141178380 Samuel Jonson Raustad: P25 mother = the item just created
Q141178380	P25	LAST	S2600	"6000000003491988841"
#   the item just created: P735 given name = Q256744 Kirsten
LAST	P735	Q256744

# create a new item
CREATE
#   set the mul label to "NN Jonsdotter"
LAST	Lmul	"NN Jonsdotter"
#   set the ca label to "esposa de Daniel Olofsson"
LAST	Lca	"esposa de Daniel Olofsson"
#   set the da label to "hustru til Daniel Olofsson"
LAST	Lda	"hustru til Daniel Olofsson"
#   set the de label to "Ehefrau von Daniel Olofsson"
LAST	Lde	"Ehefrau von Daniel Olofsson"
#   set the en label to "wife of Daniel Olofsson"
LAST	Len	"wife of Daniel Olofsson"
#   set the es label to "esposa de Daniel Olofsson"
LAST	Les	"esposa de Daniel Olofsson"
#   set the it label to "moglie di Daniel Olofsson"
LAST	Lit	"moglie di Daniel Olofsson"
#   set the nb label to "hustru til Daniel Olofsson"
LAST	Lnb	"hustru til Daniel Olofsson"
#   set the nl label to "echtgenote van Daniel Olofsson"
LAST	Lnl	"echtgenote van Daniel Olofsson"
#   set the pt label to "esposa de Daniel Olofsson"
LAST	Lpt	"esposa de Daniel Olofsson"
#   set the sv label to "maka till Daniel Olofsson"
LAST	Lsv	"maka till Daniel Olofsson"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000017093875188 NN Jonsdotter
LAST	P2600	"6000000017093875188"
#   P569 date of birth = +1610-00-00T00:00:00Z/9
LAST	P569	+1610-00-00T00:00:00Z/9	S2600	"6000000017093875188"
#   P570 date of death = +1659-00-00T00:00:00Z/9
LAST	P570	+1659-00-00T00:00:00Z/9	S2600	"6000000017093875188"

# create a new item
CREATE
#   set the en label to "Ola Toreson Randa"
LAST	Len	"Ola Toreson Randa"
#   set the mul label to "Ola Toreson Randa"
LAST	Lmul	"Ola Toreson Randa"
#   add a mul alias "Ola Toreson Talgje"
LAST	Amul	"Ola Toreson Talgje"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000100130208752 Ola Toreson Talgje
LAST	P2600	"6000000100130208752"
#   P735 given name = Q96675523 Ola
LAST	P735	Q96675523
#   add a mul alias "Ola Randa"
LAST	Amul	"Ola Randa"

# create a new item
CREATE
#   set the en label to "Olav Knutson Randa Håland"
LAST	Len	"Olav Knutson Randa Håland"
#   set the mul label to "Olav Knutson Randa Håland"
LAST	Lmul	"Olav Knutson Randa Håland"
#   add a mul alias "Olav Knutson Randa Randa"
LAST	Amul	"Olav Knutson Randa Randa"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003376377487 Olav Knutson Randa Randa
LAST	P2600	"6000000003376377487"
#   P569 date of birth = +1530-00-00T00:00:00Z/9
LAST	P569	+1530-00-00T00:00:00Z/9	S2600	"6000000003376377487"
#   P570 date of death = +1603-00-00T00:00:00Z/9
LAST	P570	+1603-00-00T00:00:00Z/9	S2600	"6000000003376377487"
#   P735 given name = Q16511262 Olav, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q16511262	P1545	"1"	P7452	Q3409033
#   add a mul alias "Olav Randa Håland"
LAST	Amul	"Olav Randa Håland"

# create a new item
CREATE
#   set the en label to "Olof Olofsson"
LAST	Len	"Olof Olofsson"
#   set the mul label to "Olof Olofsson"
LAST	Lmul	"Olof Olofsson"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000007021340142 Olof Olofsson
LAST	P2600	"6000000007021340142"
#   P569 date of birth = +1570-00-00T00:00:00Z/9
LAST	P569	+1570-00-00T00:00:00Z/9	S2600	"6000000007021340142"
#   P570 date of death = +1623-00-00T00:00:00Z/9
LAST	P570	+1623-00-00T00:00:00Z/9	S2600	"6000000007021340142"
#   P26 spouse = Q141200604 Anna Nilsdotter
LAST	P26	Q141200604	S2600	"6000000007021340142"
#   Q141200604 Anna Nilsdotter: P26 spouse = the item just created
Q141200604	P26	LAST	S2600	"6000000007021340142"
#   the item just created: P735 given name = Q18089653 Olof
LAST	P735	Q18089653

# create a new item
CREATE
#   set the mul label to "NN"
LAST	Lmul	"NN"
#   set the ca label to "fill de Yngve Andrew Berggren"
LAST	Lca	"fill de Yngve Andrew Berggren"
#   set the da label to "søn af Yngve Andrew Berggren"
LAST	Lda	"søn af Yngve Andrew Berggren"
#   set the de label to "Sohn von Yngve Andrew Berggren"
LAST	Lde	"Sohn von Yngve Andrew Berggren"
#   set the en label to "son of Yngve Andrew Berggren"
LAST	Len	"son of Yngve Andrew Berggren"
#   set the es label to "hijo de Yngve Andrew Berggren"
LAST	Les	"hijo de Yngve Andrew Berggren"
#   set the it label to "figlio di Yngve Andrew Berggren"
LAST	Lit	"figlio di Yngve Andrew Berggren"
#   set the nb label to "sønn av Yngve Andrew Berggren"
LAST	Lnb	"sønn av Yngve Andrew Berggren"
#   set the nl label to "zoon van Yngve Andrew Berggren"
LAST	Lnl	"zoon van Yngve Andrew Berggren"
#   set the pt label to "filho de Yngve Andrew Berggren"
LAST	Lpt	"filho de Yngve Andrew Berggren"
#   set the sv label to "son till Yngve Andrew Berggren"
LAST	Lsv	"son till Yngve Andrew Berggren"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000180012363839 NN Private
LAST	P2600	"6000000180012363839"
#   P25 mother = Q141189063 Elsie Pauline Tunheim
LAST	P25	Q141189063	S2600	"6000000180012363839"
#   Q141189063 Elsie Pauline Tunheim: P40 child = the item just created
Q141189063	P40	LAST	S2600	"6000000180012363839"

# create a new item
CREATE
#   the item just created: set the en label to "Ragnhild Eyvindsdotter Eyvindsdotter"
LAST	Len	"Ragnhild Eyvindsdotter Eyvindsdotter"
#   set the mul label to "Ragnhild Eyvindsdotter Eyvindsdotter"
LAST	Lmul	"Ragnhild Eyvindsdotter Eyvindsdotter"
#   add a mul alias "Ragnhild Eyvindsdotter Byre"
LAST	Amul	"Ragnhild Eyvindsdotter Byre"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000008686109792 Ragnhild Eyvindsdotter Byre
LAST	P2600	"6000000008686109792"
#   P569 date of birth = +1405-00-00T00:00:00Z/9
LAST	P569	+1405-00-00T00:00:00Z/9	S2600	"6000000008686109792"
#   P570 date of death = +1450-00-00T00:00:00Z/9
LAST	P570	+1450-00-00T00:00:00Z/9	S2600	"6000000008686109792"
#   P40 child = Q141199851 Gunnbjørn Toresson Tengs
LAST	P40	Q141199851	S2600	"6000000008686109792"
#   Q141199851 Gunnbjørn Toresson Tengs: P25 mother = the item just created
Q141199851	P25	LAST	S2600	"6000000008686109792"
#   the item just created: P735 given name = Q1390292 Ragnhild
LAST	P735	Q1390292
#   add a mul alias "Ragnhild Eyvindsdotter"
LAST	Amul	"Ragnhild Eyvindsdotter"

# create a new item
CREATE
#   set the en label to "Rudolph Ronneberg"
LAST	Len	"Rudolph Ronneberg"
#   set the mul label to "Rudolph Ronneberg"
LAST	Lmul	"Rudolph Ronneberg"
#   set the ja label to "ルドルフ・ロンネベルグ"
LAST	Lja	"ルドルフ・ロンネベルグ"
#   set the zh label to "鲁道夫·龙内贝格"
LAST	Lzh	"鲁道夫·龙内贝格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000035698102642 Rudolph Ronneberg
LAST	P2600	"6000000035698102642"
#   P569 date of birth = +1903-10-12T00:00:00Z/11
LAST	P569	+1903-10-12T00:00:00Z/11	S2600	"6000000035698102642"
#   P570 date of death = +1985-05-06T00:00:00Z/11
LAST	P570	+1985-05-06T00:00:00Z/11	S2600	"6000000035698102642"
#   P22 father = Q141198510 Tønnes Emil Enokson Rønneberg
LAST	P22	Q141198510	S2600	"6000000035698102642"
#   P25 mother = Q141162043 Inger Marie Mary Eivindsdatter Garborg
LAST	P25	Q141162043	S2600	"6000000035698102642"
#   Q141198510 Tønnes Emil Enokson Rønneberg: P40 child = the item just created
Q141198510	P40	LAST	S2600	"6000000035698102642"
#   Q141162043 Inger Marie Mary Eivindsdatter Garborg: P40 child = the item just created
Q141162043	P40	LAST	S2600	"6000000035698102642"

# create a new item
CREATE
#   the item just created: set the en label to "Sigrid Kristoffersdatter Tunheim"
LAST	Len	"Sigrid Kristoffersdatter Tunheim"
#   set the mul label to "Sigrid Kristoffersdatter Tunheim"
LAST	Lmul	"Sigrid Kristoffersdatter Tunheim"
#   add a mul alias "Sigrid Kristoffersdatter Ronning"
LAST	Amul	"Sigrid Kristoffersdatter Ronning"
#   set the ja label to "シーグリ・クリストッフェシュダッテル・トゥンヘイム"
LAST	Lja	"シーグリ・クリストッフェシュダッテル・トゥンヘイム"
#   set the zh label to "西格丽·克里斯托弗斯达特·通海姆"
LAST	Lzh	"西格丽·克里斯托弗斯达特·通海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000014003997997 Sigrid Kristoffersdatter Ronning
LAST	P2600	"6000000014003997997"
#   P569 date of birth = +1889-02-24T00:00:00Z/11
LAST	P569	+1889-02-24T00:00:00Z/11	S2600	"6000000014003997997"
#   P570 date of death = +1964-05-11T00:00:00Z/11
LAST	P570	+1964-05-11T00:00:00Z/11	S2600	"6000000014003997997"
#   P26 spouse = Q141189084 Martin Tollefson Tunheim
LAST	P26	Q141189084	S2600	"6000000014003997997"
#   Q141189084 Martin Tollefson Tunheim: P26 spouse = the item just created
Q141189084	P26	LAST	S2600	"6000000014003997997"
#   the item just created: P735 given name = Q634916 Sigrid
LAST	P735	Q634916
#   P1449 nickname = en:"Sigrid Rønning"
LAST	P1449	en:"Sigrid Rønning"
#   add a mul alias "Sigrid Rønning Tunheim"
LAST	Amul	"Sigrid Rønning Tunheim"
#   add a mul alias "Sigrid Tunheim"
LAST	Amul	"Sigrid Tunheim"

# create a new item
CREATE
#   set the en label to "Simen Olsen"
LAST	Len	"Simen Olsen"
#   set the mul label to "Simen Olsen"
LAST	Lmul	"Simen Olsen"
#   set the ja label to "シーメン・オルセン"
LAST	Lja	"シーメン・オルセン"
#   set the zh label to "西门·奥尔森"
LAST	Lzh	"西门·奥尔森"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000016756376445 Simen Olsen
LAST	P2600	"6000000016756376445"
#   P26 spouse = Q141199909 Karen Sophie Pedersdatter
LAST	P26	Q141199909	S2600	"6000000016756376445"
#   P40 child = Q141178201 Marie Petrine Simensdatter Bergersen
LAST	P40	Q141178201	S2600	"6000000016756376445"
#   Q141199909 Karen Sophie Pedersdatter: P26 spouse = the item just created
Q141199909	P26	LAST	S2600	"6000000016756376445"
#   Q141178201 Marie Petrine Simensdatter Bergersen: P22 father = the item just created
Q141178201	P22	LAST	S2600	"6000000016756376445"
#   the item just created: P735 given name = Q2287061 Simen
LAST	P735	Q2287061
#   P734 family name = Q12042571 Olsen
LAST	P734	Q12042571

# create a new item
CREATE
#   set the en label to "Tore Gardson Gardsson"
LAST	Len	"Tore Gardson Gardsson"
#   set the mul label to "Tore Gardson Gardsson"
LAST	Lmul	"Tore Gardson Gardsson"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000002572701505 Tore Gardson Gardsson
LAST	P2600	"6000000002572701505"
#   P569 date of birth = +1400-00-00T00:00:00Z/9
LAST	P569	+1400-00-00T00:00:00Z/9	S2600	"6000000002572701505"
#   P570 date of death = +1450-00-00T00:00:00Z/9
LAST	P570	+1450-00-00T00:00:00Z/9	S2600	"6000000002572701505"
#   P40 child = Q141199851 Gunnbjørn Toresson Tengs
LAST	P40	Q141199851	S2600	"6000000002572701505"
#   Q141199851 Gunnbjørn Toresson Tengs: P22 father = the item just created
Q141199851	P22	LAST	S2600	"6000000002572701505"
#   the item just created: P735 given name = Q1548096 Tore
LAST	P735	Q1548096
#   P1449 nickname = en:"Garå"
LAST	P1449	en:"Garå"
#   add a mul alias "Garå Gardsson"
LAST	Amul	"Garå Gardsson"

# create a new item
CREATE
#   set the en label to "Yngve Andrew Berggren"
LAST	Len	"Yngve Andrew Berggren"
#   set the mul label to "Yngve Andrew Berggren"
LAST	Lmul	"Yngve Andrew Berggren"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000039510112428 Yngve Andrew Berggren
LAST	P2600	"6000000039510112428"
#   P569 date of birth = +1907-03-10T00:00:00Z/11
LAST	P569	+1907-03-10T00:00:00Z/11	S2600	"6000000039510112428"
#   P570 date of death = +1979-01-28T00:00:00Z/11
LAST	P570	+1979-01-28T00:00:00Z/11	S2600	"6000000039510112428"
#   P26 spouse = Q141189063 Elsie Pauline Tunheim
LAST	P26	Q141189063	S2600	"6000000039510112428"
#   Q141189063 Elsie Pauline Tunheim: P26 spouse = the item just created
Q141189063	P26	LAST	S2600	"6000000039510112428"
#   the item just created: P735 given name = Q1408019 Yngve, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q1408019	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18042461 Andrew, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q18042461	P1545	"2"	P3831	Q245025

# RELATIONSHIPS between items that already exist -- the links yesterday's
#    creations made possible, and the properties never emitted. Every subject
#    and every value already has a QID, so this section depends on nothing above
#    it. It is emitted LAST, per her order: individuals, names, relationships.

#   Q116150300 Cecilie Ebbesdatter Hvide: P40 child = Q141189062 Cecilie Jonsdatter
Q116150300	P40	Q141189062	S2600	"305332989800002467"
#   P40 child = Q141189110 Tøre Jonsen
Q116150300	P40	Q141189110	S2600	"305332989800002467"
#   P40 child = Q141189080 Lave
Q116150300	P40	Q141189080	S2600	"305332989800002467"
#   P26 spouse = Q116150299 Jon Reinmodsen
Q116150300	P26	Q116150299	S2600	"305332989800002467"
#   set the ja label to "セシリエ・エッベスダッテル・ヴィーデ"
Q116150300	Lja	"セシリエ・エッベスダッテル・ヴィーデ"
#   set the zh label to "塞西莉厄·埃贝斯达特·维德"
Q116150300	Lzh	"塞西莉厄·埃贝斯达特·维德"
#   Q141198447 Kristina Tolvesdotter Näs: P40 child = Q5915800 Knut Algotsson
Q141198447	P40	Q5915800	S2600	"340342479380013975"
#   P26 spouse = Q141189050 Algot Bryniolfsson
Q141198447	P26	Q141189050	S2600	"340342479380013975"
#   P735 given name = Q19798802 Kristina
Q141198447	P735	Q19798802
#   Q116150299 Jon Reinmodsen: P40 child = Q141189062 Cecilie Jonsdatter
Q116150299	P40	Q141189062	S2600	"5101295410550070399"
#   P40 child = Q141189110 Tøre Jonsen
Q116150299	P40	Q141189110	S2600	"5101295410550070399"
#   P40 child = Q141189080 Lave
Q116150299	P40	Q141189080	S2600	"5101295410550070399"
#   P26 spouse = Q116150300 Cecilie Ebbesdatter Hvide
Q116150299	P26	Q116150300	S2600	"5101295410550070399"
#   P735 given name = Q13501137 Jon
Q116150299	P735	Q13501137
#   Q284400 Giséle de Cysoing: P26 spouse = Q141198389 Eberhard margrave & duke of Friuli
Q284400	P26	Q141198389	S2600	"6000000000424624719"
#   Q141199899 Jon Tollakson Aukland IV: P40 child = Q141200101 Sissel Jonsdatter Aukland
Q141199899	P40	Q141200101	S2600	"6000000002391120029"
#   P40 child = Q141198834 Gunnbjørn Jonson Aukland
Q141199899	P40	Q141198834	S2600	"6000000002391120029"
#   P26 spouse = Q141198835 Bergitte Gunnbjørnsdatter Tengs
Q141199899	P26	Q141198835	S2600	"6000000002391120029"
#   P735 given name = Q13501137 Jon, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141199899	P735	Q13501137	P1545	"1"	P7452	Q3409033
#   Q141199891 Ivar Valheim: P26 spouse = Q141200101 Sissel Jonsdatter Aukland
Q141199891	P26	Q141200101	S2600	"6000000002452595429"
#   P735 given name = Q127069 Ivar
Q141199891	P735	Q127069
#   Q141199851 Gunnbjørn Toresson Tengs: P40 child = Q141198835 Bergitte Gunnbjørnsdatter Tengs
Q141199851	P40	Q141198835	S2600	"6000000002463510938"
#   P26 spouse = Q141199862 Helga Bjørnsdatter Bjørnsdatter
Q141199851	P26	Q141199862	S2600	"6000000002463510938"
#   Q141198835 Bergitte Gunnbjørnsdatter Tengs: P22 father = Q141199851 Gunnbjørn Toresson Tengs
Q141198835	P22	Q141199851	S2600	"6000000002481819312"
#   P25 mother = Q141199862 Helga Bjørnsdatter Bjørnsdatter
Q141198835	P25	Q141199862	S2600	"6000000002481819312"
#   P40 child = Q141200101 Sissel Jonsdatter Aukland
Q141198835	P40	Q141200101	S2600	"6000000002481819312"
#   P40 child = Q141198834 Gunnbjørn Jonson Aukland
Q141198835	P40	Q141198834	S2600	"6000000002481819312"
#   P26 spouse = Q141199899 Jon Tollakson Aukland IV
Q141198835	P26	Q141199899	S2600	"6000000002481819312"
#   Q5915800 Knut Algotsson: P25 mother = Q141198447 Kristina Tolvesdotter Näs
Q5915800	P25	Q141198447	S2600	"6000000002572699392"
#   set the ja label to "クヌート・アルゴットソン"
Q5915800	Lja	"クヌート・アルゴットソン"
#   set the zh label to "克努特·阿尔戈特松"
Q5915800	Lzh	"克努特·阿尔戈特松"
#   Q141198377 Benedicta Sunesdotter Folkungaätten: P40 child = Q101247444 Ingegerd Svantepolksdotter
Q141198377	P40	Q101247444	S2600	"6000000002601672538"
#   P26 spouse = Q6197518 Svantepolk Knutsson Viby Skarsholmsätten
Q141198377	P26	Q6197518	S2600	"6000000002601672538"
#   P735 given name = Q21147545 Benedicta
Q141198377	P735	Q21147545
#   Q141198422 Iver Pedersen Sandsmark: P40 child = Q141189104 Siri Kristine Ivarsdatter Sandsmark
Q141198422	P40	Q141189104	S2600	"6000000002954100954"
#   P26 spouse = Q141198414 Ingeborg Olsdatter Ueland
Q141198422	P26	Q141198414	S2600	"6000000002954100954"
#   P735 given name = Q11977747 Iver
Q141198422	P735	Q11977747
#   P5056 patronym or matronym = Q130233025
Q141198422	P5056	Q130233025
#   Q141198414 Ingeborg Olsdatter Ueland: P40 child = Q141189104 Siri Kristine Ivarsdatter Sandsmark
Q141198414	P40	Q141189104	S2600	"6000000002954137517"
#   P26 spouse = Q141198422 Iver Pedersen Sandsmark
Q141198414	P26	Q141198422	S2600	"6000000002954137517"
#   P735 given name = Q656590 Ingeborg
Q141198414	P735	Q656590
#   P5056 patronym or matronym = Q51885688 Olsdatter
Q141198414	P5056	Q51885688
#   P734 family name = Q27889293 Ueland
Q141198414	P734	Q27889293
#   Q141189104 Siri Kristine Ivarsdatter Sandsmark: P22 father = Q141198422 Iver Pedersen Sandsmark
Q141189104	P22	Q141198422	S2600	"6000000002954315535"
#   P25 mother = Q141198414 Ingeborg Olsdatter Ueland
Q141189104	P25	Q141198414	S2600	"6000000002954315535"
#   P40 child = Q141198499 Solveig Garborg
Q141189104	P40	Q141198499	S2600	"6000000002954315535"
#   P40 child = Q141199881 Ivar Garborg
Q141189104	P40	Q141199881	S2600	"6000000002954315535"
#   P40 child = Q141198489 Sigrid Garborg
Q141189104	P40	Q141198489	S2600	"6000000002954315535"
#   set the ja label to "シーリ・クリスティーネ・イーヴァシュダッテル・サンスマルク"
Q141189104	Lja	"シーリ・クリスティーネ・イーヴァシュダッテル・サンスマルク"
#   set the zh label to "西丽·克丽丝汀·伊瓦斯达特·桑斯马克"
Q141189104	Lzh	"西丽·克丽丝汀·伊瓦斯达特·桑斯马克"
#   Q141200019 Ola Olsen Grøtheim: P22 father = Q141189088 Ola Knutsen Garborg
Q141200019	P22	Q141189088	S2600	"6000000002989071216"
#   P25 mother = Q141199830 Anna Rasmusdatter Årsland
Q141200019	P25	Q141199830	S2600	"6000000002989071216"
#   P3373 sibling = Q141200074 Rasmus Olsen Grøtheim
Q141200019	P3373	Q141200074	S2600	"6000000002989071216"
#   P735 given name = Q96675523 Ola
Q141200019	P735	Q96675523
#   set the ja label to "オーラ・オルセン・グレートヘイム"
Q141200019	Lja	"オーラ・オルセン・グレートヘイム"
#   set the zh label to "乌拉·奥尔森·格勒特海姆"
Q141200019	Lzh	"乌拉·奥尔森·格勒特海姆"
#   Q141198396 Erling Juel Wendt: P40 child = Q141198482 NN Private
Q141198396	P40	Q141198482	S2600	"6000000003002459585"
#   P26 spouse = Q141168784 Aagot Garborg
Q141198396	P26	Q141168784	S2600	"6000000003002459585"
#   P735 given name = Q472066 Erling, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141198396	P735	Q472066	P1545	"1"	P7452	Q3409033
#   Q141200101 Sissel Jonsdatter Aukland: P22 father = Q141199899 Jon Tollakson Aukland IV
Q141200101	P22	Q141199899	S2600	"6000000003043806217"
#   P25 mother = Q141198835 Bergitte Gunnbjørnsdatter Tengs
Q141200101	P25	Q141198835	S2600	"6000000003043806217"
#   P3373 sibling = Q141198834 Gunnbjørn Jonson Aukland
Q141200101	P3373	Q141198834	S2600	"6000000003043806217"
#   P26 spouse = Q141199891 Ivar Valheim
Q141200101	P26	Q141199891	S2600	"6000000003043806217"
#   P26 spouse = Q141200111 Sæbjørn Toresson Talgje
Q141200101	P26	Q141200111	S2600	"6000000003043806217"
#   P735 given name = Q4571101 Sissel
Q141200101	P735	Q4571101
#   P734 family name = Q4821650 Aukland
Q141200101	P734	Q4821650
#   Q3743799 Knut Valdemarsson Duke of Estland, Blekinge and Lolland: P26 spouse = Q141198401 Hedvig Svantepolks de Gdańsk of Danzig
Q3743799	P26	Q141198401	S2600	"6000000003076221220"
#   Q141198382 Berita Larsdatter Nedre Rossavik: P22 father = Q141198751 Lars Person Trevland
Q141198382	P22	Q141198751	S2600	"6000000003095034654"
#   P25 mother = Q141198755 Anna Ingebretsdatter Voster
Q141198382	P25	Q141198755	S2600	"6000000003095034654"
#   P40 child = Q141189079 Lars Tormodsen Mele
Q141198382	P40	Q141189079	S2600	"6000000003095034654"
#   P26 spouse = Q141198507 Tormod Bjørnson Mele
Q141198382	P26	Q141198507	S2600	"6000000003095034654"
#   P26 spouse = Q141198453 Lars Jonsen Kvam
Q141198382	P26	Q141198453	S2600	"6000000003095034654"
#   Q141189055 Astri Torkelsdatter Gilja: P26 spouse = Q141189079 Lars Tormodsen Mele
Q141189055	P26	Q141189079	S2600	"6000000003095034747"
#   set the ja label to "アストリ・トルケルスダッテル・ギリヤ"
Q141189055	Lja	"アストリ・トルケルスダッテル・ギリヤ"
#   set the zh label to "阿斯特丽·托克尔斯达特·吉利亚"
Q141189055	Lzh	"阿斯特丽·托克尔斯达特·吉利亚"
#   Q141200067 Rasmus Kjetilson Kjetilsen Høle: P40 child = Q141180412 Marta Rasmusdatter Høle
Q141200067	P40	Q141180412	S2600	"6000000003095034915"
#   P26 spouse = Q141200094 Siri Rasmusdtr. Erevik
Q141200067	P26	Q141200094	S2600	"6000000003095034915"
#   P735 given name = Q1785744 Rasmus
Q141200067	P735	Q1785744
#   Q141198831 Peder Larsen Mjølhus: P22 father = Q141198832 Lars Gunnbjørnsen Mjølhus
Q141198831	P22	Q141198832	S2600	"6000000003095034944"
#   P40 child = Q141198751 Lars Person Trevland
Q141198831	P40	Q141198751	S2600	"6000000003095034944"
#   P735 given name = Q10622039 Peder
Q141198831	P735	Q10622039
#   Q141198435 Jon Nilsson Espedal: P40 child = Q141189071 Joren Jonsdatter Espedal
Q141198435	P40	Q141189071	S2600	"6000000003095137629"
#   P26 spouse = Q141198371 Anna Belestdatter Lauvsnes
Q141198435	P26	Q141198371	S2600	"6000000003095137629"
#   P735 given name = Q13501137 Jon
Q141198435	P735	Q13501137
#   P5056 patronym or matronym = Q130233015 Nilsson
Q141198435	P5056	Q130233015
#   Q141198503 Tore Erikson Håland: P40 child = Q141189097 Ragnhild Toresdatter Håland i Gjesdal
Q141198503	P40	Q141189097	S2600	"6000000003095166856"
#   P26 spouse = Q141198538 nn Gunnarsdatter Frafjord
Q141198503	P26	Q141198538	S2600	"6000000003095166856"
#   P735 given name = Q1548096 Tore
Q141198503	P735	Q1548096
#   Q141200094 Siri Rasmusdtr. Erevik: P40 child = Q141180412 Marta Rasmusdatter Høle
Q141200094	P40	Q141180412	S2600	"6000000003095172404"
#   P26 spouse = Q141200067 Rasmus Kjetilson Kjetilsen Høle
Q141200094	P26	Q141200067	S2600	"6000000003095172404"
#   P735 given name = Q1772342 Siri, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141200094	P735	Q1772342	P1545	"1"	P7452	Q3409033
#   Q141199819 Anna Andersdotter: P40 child = Q141180409 Magdalena Andersdotter Bure
Q141199819	P40	Q141180409	S2600	"6000000003125438035"
#   P40 child = Q141200016 Nils Andersson
Q141199819	P40	Q141200016	S2600	"6000000003125438035"
#   P26 spouse = Q141199808 Andreas Olofsson
Q141199819	P26	Q141199808	S2600	"6000000003125438035"
#   set the ja label to "アンナ・アンデシュドッテル"
Q141199819	Lja	"アンナ・アンデシュドッテル"
#   set the zh label to "安娜·安德斯多特"
Q141199819	Lzh	"安娜·安德斯多特"
#   Q141198401 Hedvig Svantepolks de Gdańsk of Danzig: P40 child = Q6197518 Svantepolk Knutsson Viby Skarsholmsätten
Q141198401	P40	Q6197518	S2600	"6000000003358192683"
#   P26 spouse = Q3743799 Knut Valdemarsson Duke of Estland, Blekinge and Lolland
Q141198401	P26	Q3743799	S2600	"6000000003358192683"
#   P735 given name = Q13648620 Hedvig, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141198401	P735	Q13648620	P1545	"1"	P7452	Q3409033
#   Q6197518 Svantepolk Knutsson Viby Skarsholmsätten: P26 spouse = Q141198377 Benedicta Sunesdotter Folkungaätten
Q6197518	P26	Q141198377	S2600	"6000000003418900347"
#   Q141199892 Jon Olsen Heigre: P40 child = Q141168957 Jonas Jonson Heigre
Q141199892	P40	Q141168957	S2600	"6000000003491986736"
#   P26 spouse = Q141200054 Rakel Jonsdatter Jonsdotter Vatne
Q141199892	P26	Q141200054	S2600	"6000000003491986736"
#   P735 given name = Q13501137 Jon
Q141199892	P735	Q13501137
#   set the ja label to "ヨン・オルセン・ヘイグレ"
Q141199892	Lja	"ヨン・オルセン・ヘイグレ"
#   set the zh label to "永·奥尔森·海格勒"
Q141199892	Lzh	"永·奥尔森·海格勒"
#   Q141200054 Rakel Jonsdatter Jonsdotter Vatne: P40 child = Q141168957 Jonas Jonson Heigre
Q141200054	P40	Q141168957	S2600	"6000000003491986761"
#   P26 spouse = Q141199892 Jon Olsen Heigre
Q141200054	P26	Q141199892	S2600	"6000000003491986761"
#   P735 given name = Q16424094 Rakel
Q141200054	P735	Q16424094
#   P734 family name = Q30134985 Vatne
Q141200054	P734	Q30134985
#   Q141168957 Jonas Jonson Heigre: P22 father = Q141199892 Jon Olsen Heigre
Q141168957	P22	Q141199892	S2600	"6000000003491986771"
#   P25 mother = Q141200054 Rakel Jonsdatter Jonsdotter Vatne
Q141168957	P25	Q141200054	S2600	"6000000003491986771"
#   set the ja label to "ヨナス・ヨンソン・ヘイグレ"
Q141168957	Lja	"ヨナス・ヨンソン・ヘイグレ"
#   set the zh label to "约纳斯·永松·海格勒"
Q141168957	Lzh	"约纳斯·永松·海格勒"
#   Q141178196 Elisabet Kirstine Eriksdatter Stangeland: P22 father = Q141198393 Erik Erikson Time
Q141178196	P22	Q141198393	S2600	"6000000003491986941"
#   P25 mother = Q141198454 Lisabeth Larsdotter Vasshus
Q141178196	P25	Q141198454	S2600	"6000000003491986941"
#   set the ja label to "エリサベート・シシュティーネ・エリクスダッテル・スタンゲラン"
Q141178196	Lja	"エリサベート・シシュティーネ・エリクスダッテル・スタンゲラン"
#   set the zh label to "伊丽莎白·谢什蒂内·埃里克斯达特·斯坦格兰"
Q141178196	Lzh	"伊丽莎白·谢什蒂内·埃里克斯达特·斯坦格兰"
#   Q141152523 Ane Oline Jonsdatter Raugstad: set the ja label to "アーネ・オリーネ・ヨンスダッテル・ラウグスタード"
Q141152523	Lja	"アーネ・オリーネ・ヨンスダッテル・ラウグスタード"
#   set the zh label to "安内·奥利内·永斯达特·劳格斯塔"
Q141152523	Lzh	"安内·奥利内·永斯达特·劳格斯塔"
#   Q141189070 John Jonassen Heigre: P3373 sibling = Q141178198 Enevald Jonasson Heigre
Q141189070	P3373	Q141178198	S2600	"6000000003491986951"
#   P3373 sibling = Q141189098 Rakel Jonasdatter Heigre
Q141189070	P3373	Q141189098	S2600	"6000000003491986951"
#   P3373 sibling = Q141189111 Tørres Jonasson Hegre
Q141189070	P3373	Q141189111	S2600	"6000000003491986951"
#   P3373 sibling = Q141189081 Lotte Birgithe Gustava Jonasdatter Heigre
Q141189070	P3373	Q141189081	S2600	"6000000003491986951"
#   Q141178198 Enevald Jonasson Heigre: P3373 sibling = Q141189070 John Jonassen Heigre
Q141178198	P3373	Q141189070	S2600	"6000000003491986956"
#   set the ja label to "エーネヴァル・ヨナソン・ヘイグレ"
Q141178198	Lja	"エーネヴァル・ヨナソン・ヘイグレ"
#   set the zh label to "埃内瓦尔德·约纳松·海格勒"
Q141178198	Lzh	"埃内瓦尔德·约纳松·海格勒"
#   Q141169046 Samuel Jonson: set the ja label to "サムエル・ヨンソン"
Q141169046	Lja	"サムエル・ヨンソン"
#   set the zh label to "萨穆埃尔·永松"
Q141169046	Lzh	"萨穆埃尔·永松"
#   Q141178381 Marta Jonsdatter Li: set the ja label to "マルタ・ヨンスダッテル・リ"
Q141178381	Lja	"マルタ・ヨンスダッテル・リ"
#   set the zh label to "玛尔塔·永斯达特·李"
Q141178381	Lzh	"玛尔塔·永斯达特·李"
#   Q141178380 Samuel Jonson Raustad: set the ja label to "サムエル・ヨンソン・ラウスタード"
Q141178380	Lja	"サムエル・ヨンソン・ラウスタード"
#   set the zh label to "萨穆埃尔·永松·劳斯塔"
Q141178380	Lzh	"萨穆埃尔·永松·劳斯塔"
#   Q141198510 Tønnes Emil Enokson Rønneberg: P40 child = Q141199868 Ingvold (Pinkie) Remmie
Q141198510	P40	Q141199868	S2600	"6000000003491995164"
#   P40 child = Q141168820 Eliza Ronneberg
Q141198510	P40	Q141168820	S2600	"6000000003491995164"
#   P40 child = Q141168789 Arnold Ronneberg
Q141198510	P40	Q141168789	S2600	"6000000003491995164"
#   P40 child = Q141168805 Edward Ronneberg
Q141198510	P40	Q141168805	S2600	"6000000003491995164"
#   P40 child = Q141168786 Alice Ronneberg
Q141198510	P40	Q141168786	S2600	"6000000003491995164"
#   P40 child = Q141168824 Ernest Anton Ronneberg
Q141198510	P40	Q141168824	S2600	"6000000003491995164"
#   P26 spouse = Q141162043 Inger Marie Mary Eivindsdatter Garborg
Q141198510	P26	Q141162043	S2600	"6000000003491995164"
#   P735 given name = Q12008141 Tønnes, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141198510	P735	Q12008141	P1545	"1"	P7452	Q3409033
#   P735 given name = Q989320 Emil, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141198510	P735	Q989320	P1545	"2"	P3831	Q245025
#   P734 family name = Q7386722 Rønneberg
Q141198510	P734	Q7386722
#   set the ja label to "テンネス・エミール・エノクソン・レンネベルグ"
Q141198510	Lja	"テンネス・エミール・エノクソン・レンネベルグ"
#   set the zh label to "滕内斯·埃米尔·埃诺克松·伦内贝格"
Q141198510	Lzh	"滕内斯·埃米尔·埃诺克松·伦内贝格"
#   Q141152512 Eivind Aadnesson Garborg: set the ja label to "エイヴィン・オードネソン・ガルボルグ"
Q141152512	Lja	"エイヴィン・オードネソン・ガルボルグ"
#   set the zh label to "埃温·奥德内松·加尔博格"
Q141152512	Lzh	"埃温·奥德内松·加尔博格"
#   Q141152600 Stine Stena Eivindsdatter Garborg: P26 spouse = Q141198428 Jacob Johannessen Aabø
Q141152600	P26	Q141198428	S2600	"6000000003492005121"
#   set the ja label to "スティーネ・ステーナ・エイヴィンスダッテル・ガルボルグ"
Q141152600	Lja	"スティーネ・ステーナ・エイヴィンスダッテル・ガルボルグ"
#   set the zh label to "斯蒂内·斯泰娜·埃温斯达特·加尔博格"
Q141152600	Lzh	"斯蒂内·斯泰娜·埃温斯达特·加尔博格"
#   Q141152614 Jon Eivindson Garborg: P40 child = Q141198499 Solveig Garborg
Q141152614	P40	Q141198499	S2600	"6000000003492005126"
#   P40 child = Q141199881 Ivar Garborg
Q141152614	P40	Q141199881	S2600	"6000000003492005126"
#   P40 child = Q141198489 Sigrid Garborg
Q141152614	P40	Q141198489	S2600	"6000000003492005126"
#   set the ja label to "ヨン・エイヴィンソン・ガルボルグ"
Q141152614	Lja	"ヨン・エイヴィンソン・ガルボルグ"
#   set the zh label to "永·埃温松·加尔博格"
Q141152614	Lzh	"永·埃温松·加尔博格"
#   Q141162040 Samuel Eivindsen Garborg: set the ja label to "サムエル・エイヴィンセン・ガルボルグ"
Q141162040	Lja	"サムエル・エイヴィンセン・ガルボルグ"
#   set the zh label to "萨穆埃尔·埃温森·加尔博格"
Q141162040	Lzh	"萨穆埃尔·埃温森·加尔博格"
#   Q141162041 Even Eivindson Garborg: set the ja label to "エーヴェン・エイヴィンソン・ガルボルグ"
Q141162041	Lja	"エーヴェン・エイヴィンソン・ガルボルグ"
#   set the zh label to "埃文·埃温松·加尔博格"
Q141162041	Lzh	"埃文·埃温松·加尔博格"
#   Q141162043 Inger Marie Mary Eivindsdatter Garborg: P40 child = Q141199868 Ingvold (Pinkie) Remmie
Q141162043	P40	Q141199868	S2600	"6000000003492005141"
#   P26 spouse = Q141198510 Tønnes Emil Enokson Rønneberg
Q141162043	P26	Q141198510	S2600	"6000000003492005141"
#   set the ja label to "インゲル・マリー・メアリー・エイヴィンスダッテル・ガルボルグ"
Q141162043	Lja	"インゲル・マリー・メアリー・エイヴィンスダッテル・ガルボルグ"
#   set the zh label to "英厄尔·玛丽·玛丽·埃温斯达特·加尔博格"
Q141162043	Lzh	"英厄尔·玛丽·玛丽·埃温斯达特·加尔博格"
#   Q141162044 Abel Eivindsen Garborg: set the ja label to "アーベル・エイヴィンセン・ガルボルグ"
Q141162044	Lja	"アーベル・エイヴィンセン・ガルボルグ"
#   set the zh label to "阿贝尔·埃温森·加尔博格"
Q141162044	Lzh	"阿贝尔·埃温森·加尔博格"
#   Q141162045 Ole Eivindsen Garborg: set the ja label to "オーレ・エイヴィンセン・ガルボルグ"
Q141162045	Lja	"オーレ・エイヴィンセン・ガルボルグ"
#   set the zh label to "奥勒·埃温森·加尔博格"
Q141162045	Lzh	"奥勒·埃温森·加尔博格"
#   Q141162046 Ane Oline Lena Eivindsdatter Garborg: P40 child = Q141198472 Olga E. Tunheim
Q141162046	P40	Q141198472	S2600	"6000000003492005156"
#   P40 child = Q141199992 Myrtle Lenora Tunheim
Q141162046	P40	Q141199992	S2600	"6000000003492005156"
#   set the ja label to "アーネ・オリーネ・レーナ・エイヴィンスダッテル・ガルボルグ"
Q141162046	Lja	"アーネ・オリーネ・レーナ・エイヴィンスダッテル・ガルボルグ"
#   set the zh label to "安内·奥利内·莱娜·埃温斯达特·加尔博格"
Q141162046	Lzh	"安内·奥利内·莱娜·埃温斯达特·加尔博格"
#   Q141169072 Ådne Olsen Grøtheim: set the ja label to "オードネ・オルセン・グレートヘイム"
Q141169072	Lja	"オードネ・オルセン・グレートヘイム"
#   set the zh label to "奥德内·奥尔森·格勒特海姆"
Q141169072	Lzh	"奥德内·奥尔森·格勒特海姆"
#   Q141178202 Stine Persdatter Øksnevad: P22 father = Q141200028 Per Jonson Grude
Q141178202	P22	Q141200028	S2600	"6000000003492005166"
#   P25 mother = Q141199937 Maren Halvorsdatter Storhaug
Q141178202	P25	Q141199937	S2600	"6000000003492005166"
#   set the ja label to "スティーネ・ペシュダッテル・エクスネヴァード"
Q141178202	Lja	"スティーネ・ペシュダッテル・エクスネヴァード"
#   set the zh label to "斯蒂内·佩斯达特·厄克斯内瓦"
Q141178202	Lzh	"斯蒂内·佩斯达特·厄克斯内瓦"
#   Q141168833 Ingeborg Gurie Ådnesdatter Garborg: set the ja label to "インゲボルグ・グーリエ・オードネスダッテル・ガルボルグ"
Q141168833	Lja	"インゲボルグ・グーリエ・オードネスダッテル・ガルボルグ"
#   set the zh label to "英厄堡·古里·奥德内斯达特·加尔博格"
Q141168833	Lzh	"英厄堡·古里·奥德内斯达特·加尔博格"
#   Q141168816 Elisabet Ådnesdatter Garborg: set the ja label to "エリサベート・オードネスダッテル・ガルボルグ"
Q141168816	Lja	"エリサベート・オードネスダッテル・ガルボルグ"
#   set the zh label to "伊丽莎白·奥德内斯达特·加尔博格"
Q141168816	Lzh	"伊丽莎白·奥德内斯达特·加尔博格"
#   Q141189066 Helge Rasmusson Bø: P22 father = Q141200074 Rasmus Olsen Grøtheim
Q141189066	P22	Q141200074	S2600	"6000000003492005191"
#   P25 mother = Q141199809 Ane Marie Helgesdatter Bø
Q141189066	P25	Q141199809	S2600	"6000000003492005191"
#   P40 child = Q141189099 Rasmus Helgesen Bø
Q141189066	P40	Q141189099	S2600	"6000000003492005191"
#   P40 child = Q141189054 Anna Maria Helgesdatter Bø
Q141189066	P40	Q141189054	S2600	"6000000003492005191"
#   P40 child = Q141189113 Ådne Helgesen Bø
Q141189066	P40	Q141189113	S2600	"6000000003492005191"
#   Q141198389 Eberhard margrave & duke of Friuli: P40 child = Q274606 Berengar I margrave of Friuli, king of Italy
Q141198389	P40	Q274606	S2600	"6000000003495348447"
#   P26 spouse = Q284400 Giséle de Cysoing
Q141198389	P26	Q284400	S2600	"6000000003495348447"
#   P735 given name = Q1278816 Eberhard, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141198389	P735	Q1278816	P1545	"1"	P7452	Q3409033
#   Q141198370 NN Skårland: P40 child = Q141178200 Inger Kristoffersdatter
Q141198370	P40	Q141178200	S2600	"6000000003686206816"
#   P26 spouse = Q141198375 Astri Torchelsdatter Øvre Time
Q141198370	P26	Q141198375	S2600	"6000000003686206816"
#   Q141198375 Astri Torchelsdatter Øvre Time: P40 child = Q141178200 Inger Kristoffersdatter
Q141198375	P40	Q141178200	S2600	"6000000003731596731"
#   P26 spouse = Q141198370 NN Skårland
Q141198375	P26	Q141198370	S2600	"6000000003731596731"
#   P735 given name = Q30132931 Astri, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141198375	P735	Q30132931	P1545	"1"	P7452	Q3409033
#   Q141168955 Jon Samuelsen Raustad: P26 spouse = Q141178200 Inger Kristoffersdatter
Q141168955	P26	Q141178200	S2600	"6000000003732742137"
#   set the ja label to "ヨン・サムエルセン・ラウスタード"
Q141168955	Lja	"ヨン・サムエルセン・ラウスタード"
#   set the zh label to "永·萨穆埃尔森·劳斯塔"
Q141168955	Lzh	"永·萨穆埃尔森·劳斯塔"
#   Q141200111 Sæbjørn Toresson Talgje: P26 spouse = Q141200101 Sissel Jonsdatter Aukland
Q141200111	P26	Q141200101	S2600	"6000000004213963966"
#   P735 given name = Q125281009 Sæbjørn
Q141200111	P735	Q125281009
#   Q141199808 Andreas Olofsson: P40 child = Q141180409 Magdalena Andersdotter Bure
Q141199808	P40	Q141180409	S2600	"6000000004334566448"
#   P40 child = Q141200016 Nils Andersson
Q141199808	P40	Q141200016	S2600	"6000000004334566448"
#   P26 spouse = Q141199819 Anna Andersdotter
Q141199808	P26	Q141199819	S2600	"6000000004334566448"
#   Q633094 Johannes Tomasson: P26 spouse = Q141180410 Margareta Mårtensdotter Bång
Q633094	P26	Q141180410	S2600	"6000000004334763223"
#   set the zh label to "约翰内斯·托马松"
Q633094	Lzh	"约翰内斯·托马松"
#   Q141180413 Thomas Mattsson: set the ja label to "トーマス・マットソン"
Q141180413	Lja	"トーマス・マットソン"
#   set the zh label to "托马斯·马特松"
Q141180413	Lzh	"托马斯·马特松"
#   Q141199862 Helga Bjørnsdatter Bjørnsdatter: P40 child = Q141198835 Bergitte Gunnbjørnsdatter Tengs
Q141199862	P40	Q141198835	S2600	"6000000004697849241"
#   P26 spouse = Q141199851 Gunnbjørn Toresson Tengs
Q141199862	P26	Q141199851	S2600	"6000000004697849241"
#   P735 given name = Q1035107 Helga
Q141199862	P735	Q1035107
#   Q141178149 Anna Fartegnsdatter Seim: set the ja label to "アンナ・ファルテグンスダッテル・セイム"
Q141178149	Lja	"アンナ・ファルテグンスダッテル・セイム"
#   set the zh label to "安娜·法尔特格恩斯达特·塞姆"
Q141178149	Lzh	"安娜·法尔特格恩斯达特·塞姆"
#   Q141200028 Per Jonson Grude: P40 child = Q141178202 Stine Persdatter Øksnevad
Q141200028	P40	Q141178202	S2600	"6000000005606907249"
#   P26 spouse = Q141199937 Maren Halvorsdatter Storhaug
Q141200028	P26	Q141199937	S2600	"6000000005606907249"
#   P735 given name = Q13582800 Per
Q141200028	P735	Q13582800
#   P734 family name = Q30229687 Grude
Q141200028	P734	Q30229687
#   Q3143008 Karen Hulda Bergersen: P25 mother = Q141178201 Marie Petrine Simensdatter Bergersen
Q3143008	P25	Q141178201	S2600	"6000000005606976813"
#   Q141199937 Maren Halvorsdatter Storhaug: P40 child = Q141178202 Stine Persdatter Øksnevad
Q141199937	P40	Q141178202	S2600	"6000000005607155237"
#   P26 spouse = Q141200028 Per Jonson Grude
Q141199937	P26	Q141200028	S2600	"6000000005607155237"
#   P735 given name = Q1666203 Maren
Q141199937	P735	Q1666203
#   P734 family name = Q27892826 Storhaug
Q141199937	P734	Q27892826
#   Q141198834 Gunnbjørn Jonson Aukland: P22 father = Q141199899 Jon Tollakson Aukland IV
Q141198834	P22	Q141199899	S2600	"6000000005607359959"
#   P25 mother = Q141198835 Bergitte Gunnbjørnsdatter Tengs
Q141198834	P25	Q141198835	S2600	"6000000005607359959"
#   P40 child = Q141198832 Lars Gunnbjørnsen Mjølhus
Q141198834	P40	Q141198832	S2600	"6000000005607359959"
#   P734 family name = Q4821650 Aukland
Q141198834	P734	Q4821650
#   Q11959067 Arne Olaus Fjørtoft Garborg: P40 child = Q141199845 NN Garborg
Q11959067	P40	Q141199845	S2600	"6000000005607426327"
#   set the ja label to "アルネ・オーラウス・フョルトフト・ガルボルグ"
Q11959067	Lja	"アルネ・オーラウス・フョルトフト・ガルボルグ"
#   set the zh label to "阿尔内·奥劳斯·夫约托夫特·加尔博格"
Q11959067	Lzh	"阿尔内·奥劳斯·夫约托夫特·加尔博格"
#   Q141168827 Hans Eivind Garborg: P26 spouse = Q141199952 Marie Tverdahl
Q141168827	P26	Q141199952	S2600	"6000000005607426344"
#   set the ja label to "ハンス・エイヴィン・ガルボルグ"
Q141168827	Lja	"ハンス・エイヴィン・ガルボルグ"
#   set the zh label to "汉斯·埃温·加尔博格"
Q141168827	Lzh	"汉斯·埃温·加尔博格"
#   Q141198832 Lars Gunnbjørnsen Mjølhus: P22 father = Q141198834 Gunnbjørn Jonson Aukland
Q141198832	P22	Q141198834	S2600	"6000000005608959093"
#   P40 child = Q141198831 Peder Larsen Mjølhus
Q141198832	P40	Q141198831	S2600	"6000000005608959093"
#   P735 given name = Q15635262 Lars
Q141198832	P735	Q15635262
#   Q141198538 nn Gunnarsdatter Frafjord: P40 child = Q141189097 Ragnhild Toresdatter Håland i Gjesdal
Q141198538	P40	Q141189097	S2600	"6000000005609418157"
#   P26 spouse = Q141198503 Tore Erikson Håland
Q141198538	P26	Q141198503	S2600	"6000000005609418157"
#   P734 family name = Q38902733 Frafjord
Q141198538	P734	Q38902733
#   Q141198371 Anna Belestdatter Lauvsnes: P40 child = Q141189071 Joren Jonsdatter Espedal
Q141198371	P40	Q141189071	S2600	"6000000005609418895"
#   P26 spouse = Q141198435 Jon Nilsson Espedal
Q141198371	P26	Q141198435	S2600	"6000000005609418895"
#   Q141189079 Lars Tormodsen Mele: P22 father = Q141198507 Tormod Bjørnson Mele
Q141189079	P22	Q141198507	S2600	"6000000005609425379"
#   P25 mother = Q141198382 Berita Larsdatter Nedre Rossavik
Q141189079	P25	Q141198382	S2600	"6000000005609425379"
#   P26 spouse = Q141189055 Astri Torkelsdatter Gilja
Q141189079	P26	Q141189055	S2600	"6000000005609425379"
#   P26 spouse = Q141189071 Joren Jonsdatter Espedal
Q141189079	P26	Q141189071	S2600	"6000000005609425379"
#   P26 spouse = Q141189097 Ragnhild Toresdatter Håland i Gjesdal
Q141189079	P26	Q141189097	S2600	"6000000005609425379"
#   set the ja label to "ラーシュ・トルモドセン・メーレ"
Q141189079	Lja	"ラーシュ・トルモドセン・メーレ"
#   set the zh label to "拉尔斯·托尔莫德森·梅勒"
Q141189079	Lzh	"拉尔斯·托尔莫德森·梅勒"
#   Q141189071 Joren Jonsdatter Espedal: P22 father = Q141198435 Jon Nilsson Espedal
Q141189071	P22	Q141198435	S2600	"6000000005609425388"
#   P25 mother = Q141198371 Anna Belestdatter Lauvsnes
Q141189071	P25	Q141198371	S2600	"6000000005609425388"
#   P26 spouse = Q141189079 Lars Tormodsen Mele
Q141189071	P26	Q141189079	S2600	"6000000005609425388"
#   set the ja label to "ヨーレン・ヨンスダッテル・エスペダール"
Q141189071	Lja	"ヨーレン・ヨンスダッテル・エスペダール"
#   set the zh label to "约伦·永斯达特·埃斯佩达尔"
Q141189071	Lzh	"约伦·永斯达特·埃斯佩达尔"
#   Q141189097 Ragnhild Toresdatter Håland i Gjesdal: P22 father = Q141198503 Tore Erikson Håland
Q141189097	P22	Q141198503	S2600	"6000000005609425396"
#   P25 mother = Q141198538 nn Gunnarsdatter Frafjord
Q141189097	P25	Q141198538	S2600	"6000000005609425396"
#   P26 spouse = Q141189079 Lars Tormodsen Mele
Q141189097	P26	Q141189079	S2600	"6000000005609425396"
#   Q141178200 Inger Kristoffersdatter: P22 father = Q141198370 NN Skårland
Q141178200	P22	Q141198370	S2600	"6000000005609534511"
#   P25 mother = Q141198375 Astri Torchelsdatter Øvre Time
Q141178200	P25	Q141198375	S2600	"6000000005609534511"
#   set the ja label to "インゲル・クリストッフェシュダッテル"
Q141178200	Lja	"インゲル・クリストッフェシュダッテル"
#   set the zh label to "英厄尔·克里斯托弗斯达特"
Q141178200	Lzh	"英厄尔·克里斯托弗斯达特"
#   Q141180408 Jon Larsson Li: P26 spouse = Q141180412 Marta Rasmusdatter Høle
Q141180408	P26	Q141180412	S2600	"6000000005609534542"
#   set the ja label to "ヨン・ラーション・リ"
Q141180408	Lja	"ヨン・ラーション・リ"
#   set the zh label to "永·拉尔松·李"
Q141180408	Lzh	"永·拉尔松·李"
#   Q141180412 Marta Rasmusdatter Høle: P22 father = Q141200067 Rasmus Kjetilson Kjetilsen Høle
Q141180412	P22	Q141200067	S2600	"6000000005609534550"
#   P25 mother = Q141200094 Siri Rasmusdtr. Erevik
Q141180412	P25	Q141200094	S2600	"6000000005609534550"
#   P26 spouse = Q141180408 Jon Larsson Li
Q141180412	P26	Q141180408	S2600	"6000000005609534550"
#   set the ja label to "マルタ・ラスムスダッテル・ヘーレ"
Q141180412	Lja	"マルタ・ラスムスダッテル・ヘーレ"
#   set the zh label to "玛尔塔·拉斯穆斯达特·赫勒"
Q141180412	Lzh	"玛尔塔·拉斯穆斯达特·赫勒"
#   Q141189050 Algot Bryniolfsson: P22 father = Q141189059 Bryniolf Bengtsson (Hafridssons ätt)
Q141189050	P22	Q141189059	S2600	"6000000005795638082"
#   P26 spouse = Q141198447 Kristina Tolvesdotter Näs
Q141189050	P26	Q141198447	S2600	"6000000005795638082"
#   set the ja label to "アルゴット・ブリニオルフソン"
Q141189050	Lja	"アルゴット・ブリニオルフソン"
#   set the zh label to "阿尔戈特·布吕尼奥尔夫松"
Q141189050	Lzh	"阿尔戈特·布吕尼奥尔夫松"
#   Q141198381 Bengt Hafridsson Lejon: P40 child = Q141189059 Bryniolf Bengtsson (Hafridssons ätt)
Q141198381	P40	Q141189059	S2600	"6000000005795638104"
#   P735 given name = Q817199 Bengt
Q141198381	P735	Q817199
#   Q141180409 Magdalena Andersdotter Bure: P22 father = Q141199808 Andreas Olofsson
Q141180409	P22	Q141199808	S2600	"6000000006127859575"
#   P25 mother = Q141199819 Anna Andersdotter
Q141180409	P25	Q141199819	S2600	"6000000006127859575"
#   set the ja label to "マグダレーナ・アンデシュドッテル・ブーレ"
Q141180409	Lja	"マグダレーナ・アンデシュドッテル・ブーレ"
#   set the zh label to "玛格达莱娜·安德斯多特·布雷"
Q141180409	Lzh	"玛格达莱娜·安德斯多特·布雷"
#   Q141200016 Nils Andersson: P22 father = Q141199808 Andreas Olofsson
Q141200016	P22	Q141199808	S2600	"6000000006127859612"
#   P25 mother = Q141199819 Anna Andersdotter
Q141200016	P25	Q141199819	S2600	"6000000006127859612"
#   P40 child = Q141200604 Anna Nilsdotter
Q141200016	P40	Q141200604	S2600	"6000000006127859612"
#   P26 spouse = Q141200083 Sara NN
Q141200016	P26	Q141200083	S2600	"6000000006127859612"
#   P735 given name = Q16423038 Nils
Q141200016	P735	Q16423038
#   Q141168811 Eivind Garborg: set the ja label to "エイヴィン・ガルボルグ"
Q141168811	Lja	"エイヴィン・ガルボルグ"
#   set the zh label to "埃温·加尔博格"
Q141168811	Lzh	"埃温·加尔博格"
#   Q141198499 Solveig Garborg: P22 father = Q141152614 Jon Eivindson Garborg
Q141198499	P22	Q141152614	S2600	"6000000006571580688"
#   P25 mother = Q141189104 Siri Kristine Ivarsdatter Sandsmark
Q141198499	P25	Q141189104	S2600	"6000000006571580688"
#   P735 given name = Q1533508 Solveig
Q141198499	P735	Q1533508
#   P734 family name = Q30250555 Garborg
Q141198499	P734	Q30250555
#   set the ja label to "ソルヴェイグ・ガルボルグ"
Q141198499	Lja	"ソルヴェイグ・ガルボルグ"
#   set the zh label to "索尔维格·加尔博格"
Q141198499	Lzh	"索尔维格·加尔博格"
#   Q141199881 Ivar Garborg: P22 father = Q141152614 Jon Eivindson Garborg
Q141199881	P22	Q141152614	S2600	"6000000006571784497"
#   P25 mother = Q141189104 Siri Kristine Ivarsdatter Sandsmark
Q141199881	P25	Q141189104	S2600	"6000000006571784497"
#   P735 given name = Q127069 Ivar
Q141199881	P735	Q127069
#   P734 family name = Q30250555 Garborg
Q141199881	P734	Q30250555
#   set the ja label to "イーヴァル・ガルボルグ"
Q141199881	Lja	"イーヴァル・ガルボルグ"
#   set the zh label to "伊瓦尔·加尔博格"
Q141199881	Lzh	"伊瓦尔·加尔博格"
#   Q141198489 Sigrid Garborg: P22 father = Q141152614 Jon Eivindson Garborg
Q141198489	P22	Q141152614	S2600	"6000000006571991649"
#   P25 mother = Q141189104 Siri Kristine Ivarsdatter Sandsmark
Q141198489	P25	Q141189104	S2600	"6000000006571991649"
#   P735 given name = Q634916 Sigrid
Q141198489	P735	Q634916
#   P734 family name = Q30250555 Garborg
Q141198489	P734	Q30250555
#   set the ja label to "シーグリ・ガルボルグ"
Q141198489	Lja	"シーグリ・ガルボルグ"
#   set the zh label to "西格丽·加尔博格"
Q141198489	Lzh	"西格丽·加尔博格"
#   Q141168792 Astrid Garborg: set the ja label to "アストリッド・ガルボルグ"
Q141168792	Lja	"アストリッド・ガルボルグ"
#   set the zh label to "阿斯特丽德·加尔博格"
Q141168792	Lzh	"阿斯特丽德·加尔博格"
#   Q141168837 Ingebret Garborg: set the ja label to "インゲブレート・ガルボルグ"
Q141168837	Lja	"インゲブレート・ガルボルグ"
#   set the zh label to "英厄布雷特·加尔博格"
Q141168837	Lzh	"英厄布雷特·加尔博格"
#   Q141168830 Ingeborg Garborg: set the ja label to "インゲボルグ・ガルボルグ"
Q141168830	Lja	"インゲボルグ・ガルボルグ"
#   set the zh label to "英厄堡·加尔博格"
Q141168830	Lzh	"英厄堡·加尔博格"
#   Q141168954 Jon Garborg: set the ja label to "ヨン・ガルボルグ"
Q141168954	Lja	"ヨン・ガルボルグ"
#   set the zh label to "永·加尔博格"
Q141168954	Lzh	"永·加尔博格"
#   Q109266155 Magdalena Johansdotter Bure: P25 mother = Q141180410 Margareta Mårtensdotter Bång
Q109266155	P25	Q141180410	S2600	"6000000006828701331"
#   Q141199959 Martinus Johannis: P40 child = Q141180410 Margareta Mårtensdotter Bång
Q141199959	P40	Q141180410	S2600	"6000000006828782200"
#   P26 spouse = Q141199822 Anna Jönsdotter
Q141199959	P26	Q141199822	S2600	"6000000006828782200"
#   P735 given name = Q17520926 Martinus
Q141199959	P735	Q17520926
#   Q141200604 Anna Nilsdotter: P22 father = Q141200016 Nils Andersson
Q141200604	P22	Q141200016	S2600	"6000000007020763500"
#   P25 mother = Q141200083 Sara NN
Q141200604	P25	Q141200083	S2600	"6000000007020763500"
#   Q141200074 Rasmus Olsen Grøtheim: P22 father = Q141189088 Ola Knutsen Garborg
Q141200074	P22	Q141189088	S2600	"6000000007744183945"
#   P25 mother = Q141199830 Anna Rasmusdatter Årsland
Q141200074	P25	Q141199830	S2600	"6000000007744183945"
#   P40 child = Q141189066 Helge Rasmusson Bø
Q141200074	P40	Q141189066	S2600	"6000000007744183945"
#   P26 spouse = Q141199809 Ane Marie Helgesdatter Bø
Q141200074	P26	Q141199809	S2600	"6000000007744183945"
#   P735 given name = Q1785744 Rasmus
Q141200074	P735	Q1785744
#   Q141189088 Ola Knutsen Garborg: P22 father = Q141199925 Knut Elvindson Garborg
Q141189088	P22	Q141199925	S2600	"6000000007744588495"
#   P25 mother = Q141199856 Guri Hansdatter Risa
Q141189088	P25	Q141199856	S2600	"6000000007744588495"
#   P40 child = Q141200019 Ola Olsen Grøtheim
Q141189088	P40	Q141200019	S2600	"6000000007744588495"
#   P40 child = Q141200074 Rasmus Olsen Grøtheim
Q141189088	P40	Q141200074	S2600	"6000000007744588495"
#   P40 child = Q141199930 Knut Olsen Grøtheim
Q141189088	P40	Q141199930	S2600	"6000000007744588495"
#   P40 child = Q141198441 Kirsten Olsdatter Grøtheim
Q141189088	P40	Q141198441	S2600	"6000000007744588495"
#   P26 spouse = Q141189069 Ingeborg Ådnesdatter Grøtheim
Q141189088	P26	Q141189069	S2600	"6000000007744588495"
#   P26 spouse = Q141199830 Anna Rasmusdatter Årsland
Q141189088	P26	Q141199830	S2600	"6000000007744588495"
#   Q141199809 Ane Marie Helgesdatter Bø: P40 child = Q141189066 Helge Rasmusson Bø
Q141199809	P40	Q141189066	S2600	"6000000007896103690"
#   P26 spouse = Q141200074 Rasmus Olsen Grøtheim
Q141199809	P26	Q141200074	S2600	"6000000007896103690"
#   P735 given name = Q11958077 Ane, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141199809	P735	Q11958077	P1545	"1"	P7452	Q3409033
#   P735 given name = Q106674406 Marie, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141199809	P735	Q106674406	P1545	"2"	P3831	Q245025
#   Q141199925 Knut Elvindson Garborg: P40 child = Q141189088 Ola Knutsen Garborg
Q141199925	P40	Q141189088	S2600	"6000000007896295466"
#   P26 spouse = Q141199856 Guri Hansdatter Risa
Q141199925	P26	Q141199856	S2600	"6000000007896295466"
#   P735 given name = Q943881 Knut
Q141199925	P735	Q943881
#   P734 family name = Q30250555 Garborg
Q141199925	P734	Q30250555
#   Q141199856 Guri Hansdatter Risa: P40 child = Q141189088 Ola Knutsen Garborg
Q141199856	P40	Q141189088	S2600	"6000000007896387570"
#   P26 spouse = Q141199925 Knut Elvindson Garborg
Q141199856	P26	Q141199925	S2600	"6000000007896387570"
#   P735 given name = Q11973376 Guri
Q141199856	P735	Q11973376
#   Q141198507 Tormod Bjørnson Mele: P40 child = Q141189079 Lars Tormodsen Mele
Q141198507	P40	Q141189079	S2600	"6000000007980617631"
#   P26 spouse = Q141198382 Berita Larsdatter Nedre Rossavik
Q141198507	P26	Q141198382	S2600	"6000000007980617631"
#   P735 given name = Q7825922 Tormod
Q141198507	P735	Q7825922
#   Q141198755 Anna Ingebretsdatter Voster: P40 child = Q141198382 Berita Larsdatter Nedre Rossavik
Q141198755	P40	Q141198382	S2600	"6000000007980728952"
#   P26 spouse = Q141198751 Lars Person Trevland
Q141198755	P26	Q141198751	S2600	"6000000007980728952"
#   Q141198751 Lars Person Trevland: P22 father = Q141198831 Peder Larsen Mjølhus
Q141198751	P22	Q141198831	S2600	"6000000007980728982"
#   P40 child = Q141198382 Berita Larsdatter Nedre Rossavik
Q141198751	P40	Q141198382	S2600	"6000000007980728982"
#   P26 spouse = Q141198755 Anna Ingebretsdatter Voster
Q141198751	P26	Q141198755	S2600	"6000000007980728982"
#   P735 given name = Q15635262 Lars
Q141198751	P735	Q15635262
#   Q141189069 Ingeborg Ådnesdatter Grøtheim: P22 father = Q141200127 Ådne Hansen Store Oma
Q141189069	P22	Q141200127	S2600	"6000000008176802346"
#   P25 mother = Q141199918 Kirsten Hansdatter Låge-Håland
Q141189069	P25	Q141199918	S2600	"6000000008176802346"
#   P40 child = Q141199930 Knut Olsen Grøtheim
Q141189069	P40	Q141199930	S2600	"6000000008176802346"
#   P40 child = Q141198441 Kirsten Olsdatter Grøtheim
Q141189069	P40	Q141198441	S2600	"6000000008176802346"
#   P26 spouse = Q141189088 Ola Knutsen Garborg
Q141189069	P26	Q141189088	S2600	"6000000008176802346"
#   set the ja label to "インゲボルグ・オードネスダッテル・グレートヘイム"
Q141189069	Lja	"インゲボルグ・オードネスダッテル・グレートヘイム"
#   set the zh label to "英厄堡·奥德内斯达特·格勒特海姆"
Q141189069	Lzh	"英厄堡·奥德内斯达特·格勒特海姆"
#   Q141199830 Anna Rasmusdatter Årsland: P40 child = Q141200019 Ola Olsen Grøtheim
Q141199830	P40	Q141200019	S2600	"6000000008176804564"
#   P40 child = Q141200074 Rasmus Olsen Grøtheim
Q141199830	P40	Q141200074	S2600	"6000000008176804564"
#   P26 spouse = Q141189088 Ola Knutsen Garborg
Q141199830	P26	Q141189088	S2600	"6000000008176804564"
#   Q141189108 Tillie Betsy Tunheim: set the ja label to "ティリー・ベッツィ・トゥンヘイム"
Q141189108	Lja	"ティリー・ベッツィ・トゥンヘイム"
#   set the zh label to "蒂莉·贝齐·通海姆"
Q141189108	Lzh	"蒂莉·贝齐·通海姆"
#   Q141178201 Marie Petrine Simensdatter Bergersen: P25 mother = Q141199909 Karen Sophie Pedersdatter
Q141178201	P25	Q141199909	S2600	"6000000009126235990"
#   P26 spouse = Q141198384 Carl Johan Edlund
Q141178201	P26	Q141198384	S2600	"6000000009126235990"
#   set the ja label to "マリー・ペトリーネ・シメンスダッテル・ベルゲルセン"
Q141178201	Lja	"マリー・ペトリーネ・シメンスダッテル・ベルゲルセン"
#   set the zh label to "玛丽·佩特里内·西门斯达特·贝格尔森"
Q141178201	Lzh	"玛丽·佩特里内·西门斯达特·贝格尔森"
#   Q141168797 Christian Frederik Bergersen: P22 father = Q141178199 Gunder Bergersen
Q141168797	P22	Q141178199	S2600	"6000000009126453497"
#   P25 mother = Q141180395 Maren Gulbrandsdatter Ommestad
Q141168797	P25	Q141180395	S2600	"6000000009126453497"
#   P26 spouse = Q141178201 Marie Petrine Simensdatter Bergersen
Q141168797	P26	Q141178201	S2600	"6000000009126453497"
#   P26 spouse = Q141198484 Rangdi Rasmusdatter Sollienseie
Q141168797	P26	Q141198484	S2600	"6000000009126453497"
#   P26 spouse = Q141198464 Maren Olsdatter
Q141168797	P26	Q141198464	S2600	"6000000009126453497"
#   set the ja label to "クリスチャン・フレデリク・ベルゲルセン"
Q141168797	Lja	"クリスチャン・フレデリク・ベルゲルセン"
#   set the zh label to "克里斯蒂安·弗雷德里克·贝格尔森"
Q141168797	Lzh	"克里斯蒂安·弗雷德里克·贝格尔森"
#   Q141189094 Oskar Edlund: P22 father = Q141198384 Carl Johan Edlund
Q141189094	P22	Q141198384	S2600	"6000000010256424421"
#   Q141198393 Erik Erikson Time: P40 child = Q141178196 Elisabet Kirstine Eriksdatter Stangeland
Q141198393	P40	Q141178196	S2600	"6000000011198194484"
#   P26 spouse = Q141198454 Lisabeth Larsdotter Vasshus
Q141198393	P26	Q141198454	S2600	"6000000011198194484"
#   P735 given name = Q750186 Erik
Q141198393	P735	Q750186
#   Q141198454 Lisabeth Larsdotter Vasshus: P40 child = Q141178196 Elisabet Kirstine Eriksdatter Stangeland
Q141198454	P40	Q141178196	S2600	"6000000011198310542"
#   P26 spouse = Q141198393 Erik Erikson Time
Q141198454	P26	Q141198393	S2600	"6000000011198310542"
#   P735 given name = Q21148195 Lisabeth
Q141198454	P735	Q21148195
#   Q101247444 Ingegerd Svantepolksdotter: set the ja label to "インゲゲルド・スヴァンテポルクスドッテル"
Q101247444	Lja	"インゲゲルド・スヴァンテポルクスドッテル"
#   set the zh label to "英格格德·斯万特波尔克斯多特"
Q101247444	Lzh	"英格格德·斯万特波尔克斯多特"
#   Q141189059 Bryniolf Bengtsson (Hafridssons ätt): P22 father = Q141198381 Bengt Hafridsson Lejon
Q141189059	P22	Q141198381	S2600	"6000000011239545575"
#   P40 child = Q141189050 Algot Bryniolfsson
Q141189059	P40	Q141189050	S2600	"6000000011239545575"
#   Q16165426 Catharina Burea: P25 mother = Q141180410 Margareta Mårtensdotter Bång
Q16165426	P25	Q141180410	S2600	"6000000012526829690"
#   Q141180410 Margareta Mårtensdotter Bång: P22 father = Q141199959 Martinus Johannis
Q141180410	P22	Q141199959	S2600	"6000000012566410426"
#   P25 mother = Q141199822 Anna Jönsdotter
Q141180410	P25	Q141199822	S2600	"6000000012566410426"
#   P40 child = Q109266155 Magdalena Johansdotter Bure
Q141180410	P40	Q109266155	S2600	"6000000012566410426"
#   P40 child = Q16165426 Catharina Burea
Q141180410	P40	Q16165426	S2600	"6000000012566410426"
#   set the ja label to "マルガレータ・モーテンスドッテル・ボング"
Q141180410	Lja	"マルガレータ・モーテンスドッテル・ボング"
#   set the zh label to "玛格丽塔·莫滕斯多特·邦格"
Q141180410	Lzh	"玛格丽塔·莫滕斯多特·邦格"
#   Q141189112 Wilhelmine Sophie Bergersen: set the ja label to "ヴィルヘルミーネ・ソフィー・ベルゲルセン"
Q141189112	Lja	"ヴィルヘルミーネ・ソフィー・ベルゲルセン"
#   set the zh label to "威廉明妮·索菲·贝格尔森"
Q141189112	Lzh	"威廉明妮·索菲·贝格尔森"
#   Q141189083 Martha Elida Bergersen: set the ja label to "マルタ・エリーダ・ベルゲルセン"
Q141189083	Lja	"マルタ・エリーダ・ベルゲルセン"
#   set the zh label to "玛尔塔·埃利达·贝格尔森"
Q141189083	Lzh	"玛尔塔·埃利达·贝格尔森"
#   Q141178199 Gunder Bergersen: P26 spouse = Q141180395 Maren Gulbrandsdatter Ommestad
Q141178199	P26	Q141180395	S2600	"6000000016756402733"
#   set the ja label to "グンデル・ベルゲルセン"
Q141178199	Lja	"グンデル・ベルゲルセン"
#   set the zh label to "贡德尔·贝格尔森"
Q141178199	Lzh	"贡德尔·贝格尔森"
#   Q141198428 Jacob Johannessen Aabø: P40 child = Q141168794 Betsy Jacobson
Q141198428	P40	Q141168794	S2600	"6000000019384694298"
#   P26 spouse = Q141152600 Stine Stena Eivindsdatter Garborg
Q141198428	P26	Q141152600	S2600	"6000000019384694298"
#   P735 given name = Q25999604 Jacob
Q141198428	P735	Q25999604
#   set the ja label to "ヤコブ・ヨハンネセン・オーベー"
Q141198428	Lja	"ヤコブ・ヨハンネセン・オーベー"
#   set the zh label to "雅各布·约翰内森·奥贝"
Q141198428	Lzh	"雅各布·约翰内森·奥贝"
#   Q141189084 Martin Tollefson Tunheim: P22 father = Q141200112 Tollef Pederson Hetland
Q141189084	P22	Q141200112	S2600	"6000000019384841547"
#   P25 mother = Q141199826 Anna Maria Samuelsdtr. Tunheim
Q141189084	P25	Q141199826	S2600	"6000000019384841547"
#   P40 child = Q141198472 Olga E. Tunheim
Q141189084	P40	Q141198472	S2600	"6000000019384841547"
#   P40 child = Q141199992 Myrtle Lenora Tunheim
Q141189084	P40	Q141199992	S2600	"6000000019384841547"
#   set the ja label to "マルティン・トレフソン・トゥンヘイム"
Q141189084	Lja	"マルティン・トレフソン・トゥンヘイム"
#   set the zh label to "马丁·托勒夫松·通海姆"
Q141189084	Lzh	"马丁·托勒夫松·通海姆"
#   Q141199930 Knut Olsen Grøtheim: P22 father = Q141189088 Ola Knutsen Garborg
Q141199930	P22	Q141189088	S2600	"6000000019668338861"
#   P25 mother = Q141189069 Ingeborg Ådnesdatter Grøtheim
Q141199930	P25	Q141189069	S2600	"6000000019668338861"
#   P735 given name = Q943881 Knut
Q141199930	P735	Q943881
#   set the ja label to "クヌート・オルセン・グレートヘイム"
Q141199930	Lja	"クヌート・オルセン・グレートヘイム"
#   set the zh label to "克努特·奥尔森·格勒特海姆"
Q141199930	Lzh	"克努特·奥尔森·格勒特海姆"
#   Q141198441 Kirsten Olsdatter Grøtheim: P22 father = Q141189088 Ola Knutsen Garborg
Q141198441	P22	Q141189088	S2600	"6000000019668822075"
#   P25 mother = Q141189069 Ingeborg Ådnesdatter Grøtheim
Q141198441	P25	Q141189069	S2600	"6000000019668822075"
#   P735 given name = Q256744 Kirsten
Q141198441	P735	Q256744
#   P5056 patronym or matronym = Q51885688 Olsdatter, qualified based on Q141189088 Ola Knutsen Garborg
Q141198441	P5056	Q51885688	P144	Q141189088
#   Q141180395 Maren Gulbrandsdatter Ommestad: P26 spouse = Q141178199 Gunder Bergersen
Q141180395	P26	Q141178199	S2600	"6000000020221673906"
#   set the ja label to "マーレン・グルブランスダッテル・オンメスタード"
Q141180395	Lja	"マーレン・グルブランスダッテル・オンメスタード"
#   set the zh label to "马伦·古尔布兰斯达特·翁梅斯塔德"
Q141180395	Lzh	"马伦·古尔布兰斯达特·翁梅斯塔德"
#   Q141168784 Aagot Garborg: P40 child = Q141198482 NN Private
Q141168784	P40	Q141198482	S2600	"6000000021079935250"
#   P26 spouse = Q141198396 Erling Juel Wendt
Q141168784	P26	Q141198396	S2600	"6000000021079935250"
#   set the ja label to "オーゴット・ガルボルグ"
Q141168784	Lja	"オーゴット・ガルボルグ"
#   set the zh label to "奥高特·加尔博格"
Q141168784	Lzh	"奥高特·加尔博格"
#   Q141198482 NN Private: P22 father = Q141198396 Erling Juel Wendt
Q141198482	P22	Q141198396	S2600	"6000000021080190248"
#   P25 mother = Q141168784 Aagot Garborg
Q141198482	P25	Q141168784	S2600	"6000000021080190248"
#   Q141189090 Ole Christopher Christiansen: P25 mother = Q141198484 Rangdi Rasmusdatter Sollienseie
Q141189090	P25	Q141198484	S2600	"6000000021122102578"
#   Q141198484 Rangdi Rasmusdatter Sollienseie: P40 child = Q141189090 Ole Christopher Christiansen
Q141198484	P40	Q141189090	S2600	"6000000021122137597"
#   P26 spouse = Q141168797 Christian Frederik Bergersen
Q141198484	P26	Q141168797	S2600	"6000000021122137597"
#   Q141189099 Rasmus Helgesen Bø: P22 father = Q141189066 Helge Rasmusson Bø
Q141189099	P22	Q141189066	S2600	"6000000021133770643"
#   Q141199909 Karen Sophie Pedersdatter: P40 child = Q141178201 Marie Petrine Simensdatter Bergersen
Q141199909	P40	Q141178201	S2600	"6000000021137401277"
#   P735 given name = Q14942517 Sophie, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141199909	P735	Q14942517	P1545	"2"	P3831	Q245025
#   set the ja label to "カーレン・ソフィー・ペーデシュダッテル"
Q141199909	Lja	"カーレン・ソフィー・ペーデシュダッテル"
#   set the zh label to "卡伦·索菲·佩德斯达特"
Q141199909	Lzh	"卡伦·索菲·佩德斯达特"
#   Q138474188 Hans Syvertsen Nyvold: P26 spouse = Q141178197 Elisabeth Johannesen
Q138474188	P26	Q141178197	S2600	"6000000021197598122"
#   set the ja label to "ハンス・シーヴェシェン・ニーヴォル"
Q138474188	Lja	"ハンス・シーヴェシェン・ニーヴォル"
#   set the zh label to "汉斯·西韦特森·尼沃尔"
Q138474188	Lzh	"汉斯·西韦特森·尼沃尔"
#   Q141168785 Aagot Nyvold: P25 mother = Q141178197 Elisabeth Johannesen
Q141168785	P25	Q141178197	S2600	"6000000021197722738"
#   P40 child = Q141199845 NN Garborg
Q141168785	P40	Q141199845	S2600	"6000000021197722738"
#   set the ja label to "オーゴット・ニーヴォル"
Q141168785	Lja	"オーゴット・ニーヴォル"
#   set the zh label to "奥高特·尼沃尔"
Q141168785	Lzh	"奥高特·尼沃尔"
#   Q141168803 Dagny Nyvold: P25 mother = Q141178197 Elisabeth Johannesen
Q141168803	P25	Q141178197	S2600	"6000000021197841042"
#   set the ja label to "ダグニー・ニーヴォル"
Q141168803	Lja	"ダグニー・ニーヴォル"
#   set the zh label to "达格妮·尼沃尔"
Q141168803	Lzh	"达格妮·尼沃尔"
#   Q141178197 Elisabeth Johannesen: P26 spouse = Q138474188 Hans Syvertsen Nyvold
Q141178197	P26	Q138474188	S2600	"6000000021198042859"
#   set the ja label to "エリーサベト・ヨハンネセン"
Q141178197	Lja	"エリーサベト・ヨハンネセン"
#   set the zh label to "伊丽莎白·约翰内森"
Q141178197	Lzh	"伊丽莎白·约翰内森"
#   Q141199845 NN Garborg: P22 father = Q11959067 Arne Olaus Fjørtoft Garborg
Q141199845	P22	Q11959067	S2600	"6000000021223635839"
#   P25 mother = Q141168785 Aagot Nyvold
Q141199845	P25	Q141168785	S2600	"6000000021223635839"
#   P734 family name = Q30250555 Garborg
Q141199845	P734	Q30250555
#   Q141189081 Lotte Birgithe Gustava Jonasdatter Heigre: set the ja label to "ロッテ・ビルギーテ・グスタヴァ・ヨナスダッテル・ヘイグレ"
Q141189081	Lja	"ロッテ・ビルギーテ・グスタヴァ・ヨナスダッテル・ヘイグレ"
#   set the zh label to "洛特·比尔吉特·古斯塔娃·约纳斯达特·海格勒"
Q141189081	Lzh	"洛特·比尔吉特·古斯塔娃·约纳斯达特·海格勒"
#   Q141180406 Ingeborg Gyntesdotter: set the ja label to "インゲボルグ・ギュンテスドッテル"
Q141180406	Lja	"インゲボルグ・ギュンテスドッテル"
#   set the zh label to "英厄堡·金特斯多特"
Q141180406	Lzh	"英厄堡·金特斯多特"
#   Q141199822 Anna Jönsdotter: P40 child = Q141180410 Margareta Mårtensdotter Bång
Q141199822	P40	Q141180410	S2600	"6000000027470336201"
#   P26 spouse = Q141199959 Martinus Johannis
Q141199822	P26	Q141199959	S2600	"6000000027470336201"
#   Q141189076 Kristian Larsen Nord-Varhaug: P40 child = Q141189067 Helmik Kristiansen Sør-Reime
Q141189076	P40	Q141189067	S2600	"6000000029302543031"
#   P40 child = Q141189078 Lars Kristiansen Sør-Reime
Q141189076	P40	Q141189078	S2600	"6000000029302543031"
#   P40 child = Q141189077 Lars Bernhard Kristiansen Sør-Reime
Q141189076	P40	Q141189077	S2600	"6000000029302543031"
#   set the ja label to "クリスティアン・ラーシェン・ノール・ヴァールハウグ"
Q141189076	Lja	"クリスティアン・ラーシェン・ノール・ヴァールハウグ"
#   set the zh label to "克里斯蒂安·拉尔森·诺尔·瓦尔豪格"
Q141189076	Lzh	"克里斯蒂安·拉尔森·诺尔·瓦尔豪格"
#   Q141199826 Anna Maria Samuelsdtr. Tunheim: P40 child = Q141189084 Martin Tollefson Tunheim
Q141199826	P40	Q141189084	S2600	"6000000029983034410"
#   P40 child = Q141180396 Tollef Tollefson Tunheim
Q141199826	P40	Q141180396	S2600	"6000000029983034410"
#   P26 spouse = Q141200112 Tollef Pederson Hetland
Q141199826	P26	Q141200112	S2600	"6000000029983034410"
#   Q141200112 Tollef Pederson Hetland: P40 child = Q141189084 Martin Tollefson Tunheim
Q141200112	P40	Q141189084	S2600	"6000000029983078557"
#   P40 child = Q141180396 Tollef Tollefson Tunheim
Q141200112	P40	Q141180396	S2600	"6000000029983078557"
#   P26 spouse = Q141199826 Anna Maria Samuelsdtr. Tunheim
Q141200112	P26	Q141199826	S2600	"6000000029983078557"
#   P735 given name = Q12006598 Tollef
Q141200112	P735	Q12006598
#   P734 family name = Q16870758 Hetland
Q141200112	P734	Q16870758
#   Q141198472 Olga E. Tunheim: P22 father = Q141189084 Martin Tollefson Tunheim
Q141198472	P22	Q141189084	S2600	"6000000033773801550"
#   P25 mother = Q141162046 Ane Oline Lena Eivindsdatter Garborg
Q141198472	P25	Q141162046	S2600	"6000000033773801550"
#   P735 given name = Q19803501 E., qualified series ordinal 2, object of statement has role Q245025 middle name
Q141198472	P735	Q19803501	P1545	"2"	P3831	Q245025
#   set the ja label to "オルガ・E.・トゥンヘイム"
Q141198472	Lja	"オルガ・E.・トゥンヘイム"
#   set the zh label to "奥尔加·E.·通海姆"
Q141198472	Lzh	"奥尔加·E.·通海姆"
#   Q141169062 Thoralf Tunheim: set the ja label to "トーラルフ・トゥンヘイム"
Q141169062	Lja	"トーラルフ・トゥンヘイム"
#   set the zh label to "托拉尔夫·通海姆"
Q141169062	Lzh	"托拉尔夫·通海姆"
#   Q141168801 Cora Estelle Tunheim: P40 child = Q141198387 Donald Herbert Pierson
Q141168801	P40	Q141198387	S2600	"6000000033773908408"
#   P26 spouse = Q141198408 Herbert August Pierson
Q141168801	P26	Q141198408	S2600	"6000000033773908408"
#   set the ja label to "コーラ・エステル・トゥンヘイム"
Q141168801	Lja	"コーラ・エステル・トゥンヘイム"
#   set the zh label to "科拉·埃斯特尔·通海姆"
Q141168801	Lzh	"科拉·埃斯特尔·通海姆"
#   Q141168809 Edward Tunheim: P40 child = Q141198399 Eugene LeRoy Tunheim
Q141168809	P40	Q141198399	S2600	"6000000033773925586"
#   set the ja label to "エドワード・トゥンヘイム"
Q141168809	Lja	"エドワード・トゥンヘイム"
#   set the zh label to "爱德华·通海姆"
Q141168809	Lzh	"爱德华·通海姆"
#   Q141168787 Alma Matilda Tunheim: set the ja label to "アルマ・マチルダ・トゥンヘイム"
Q141168787	Lja	"アルマ・マチルダ・トゥンヘイム"
#   set the zh label to "阿尔玛·玛蒂尔达·通海姆"
Q141168787	Lzh	"阿尔玛·玛蒂尔达·通海姆"
#   Q141169041 Olaf Tunheim: set the ja label to "オーラフ・トゥンヘイム"
Q141169041	Lja	"オーラフ・トゥンヘイム"
#   set the zh label to "奥拉夫·通海姆"
Q141169041	Lzh	"奥拉夫·通海姆"
#   Q4953376 Helena Guttormsdatter: set the ja label to "ヘレナ・グットルムスダッテル"
Q4953376	Lja	"ヘレナ・グットルムスダッテル"
#   set the zh label to "海伦娜·古托尔姆斯达特"
Q4953376	Lzh	"海伦娜·古托尔姆斯达特"
#   Q141199868 Ingvold (Pinkie) Remmie: P22 father = Q141198510 Tønnes Emil Enokson Rønneberg
Q141199868	P22	Q141198510	S2600	"6000000035698131765"
#   P25 mother = Q141162043 Inger Marie Mary Eivindsdatter Garborg
Q141199868	P25	Q141162043	S2600	"6000000035698131765"
#   set the ja label to "イングヴォル・ピンキー・レミー"
Q141199868	Lja	"イングヴォル・ピンキー・レミー"
#   set the zh label to "英瓦尔·平基·雷米"
Q141199868	Lzh	"英瓦尔·平基·雷米"
#   Q141168820 Eliza Ronneberg: P22 father = Q141198510 Tønnes Emil Enokson Rønneberg
Q141168820	P22	Q141198510	S2600	"6000000035698428095"
#   set the ja label to "エリザ・ロンネベルグ"
Q141168820	Lja	"エリザ・ロンネベルグ"
#   set the zh label to "伊莱扎·龙内贝格"
Q141168820	Lzh	"伊莱扎·龙内贝格"
#   Q141168789 Arnold Ronneberg: P22 father = Q141198510 Tønnes Emil Enokson Rønneberg
Q141168789	P22	Q141198510	S2600	"6000000035698494074"
#   set the ja label to "アルノルド・ロンネベルグ"
Q141168789	Lja	"アルノルド・ロンネベルグ"
#   set the zh label to "阿诺德·龙内贝格"
Q141168789	Lzh	"阿诺德·龙内贝格"
#   Q141168805 Edward Ronneberg: P22 father = Q141198510 Tønnes Emil Enokson Rønneberg
Q141168805	P22	Q141198510	S2600	"6000000035698546990"
#   set the ja label to "エドワード・ロンネベルグ"
Q141168805	Lja	"エドワード・ロンネベルグ"
#   set the zh label to "爱德华·龙内贝格"
Q141168805	Lzh	"爱德华·龙内贝格"
#   Q141168786 Alice Ronneberg: P22 father = Q141198510 Tønnes Emil Enokson Rønneberg
Q141168786	P22	Q141198510	S2600	"6000000035698611873"
#   set the ja label to "アリス・ロンネベルグ"
Q141168786	Lja	"アリス・ロンネベルグ"
#   set the zh label to "艾丽丝·龙内贝格"
Q141168786	Lzh	"艾丽丝·龙内贝格"
#   Q141168824 Ernest Anton Ronneberg: P22 father = Q141198510 Tønnes Emil Enokson Rønneberg
Q141168824	P22	Q141198510	S2600	"6000000035698619913"
#   set the ja label to "アーネスト・アントン・ロンネベルグ"
Q141168824	Lja	"アーネスト・アントン・ロンネベルグ"
#   set the zh label to "欧内斯特·安东·龙内贝格"
Q141168824	Lzh	"欧内斯特·安东·龙内贝格"
#   Q141199992 Myrtle Lenora Tunheim: P22 father = Q141189084 Martin Tollefson Tunheim
Q141199992	P22	Q141189084	S2600	"6000000037693663051"
#   P25 mother = Q141162046 Ane Oline Lena Eivindsdatter Garborg
Q141199992	P25	Q141162046	S2600	"6000000037693663051"
#   P735 given name = Q3858942 Myrtle, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141199992	P735	Q3858942	P1545	"1"	P7452	Q3409033
#   P735 given name = Q26944868 Lenora, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141199992	P735	Q26944868	P1545	"2"	P3831	Q245025
#   set the ja label to "マートル・レノーラ・トゥンヘイム"
Q141199992	Lja	"マートル・レノーラ・トゥンヘイム"
#   set the zh label to "默特尔·莱诺拉·通海姆"
Q141199992	Lzh	"默特尔·莱诺拉·通海姆"
#   Q141168788 Arne Garborg Tunheim: set the ja label to "アルネ・ガルボルグ・トゥンヘイム"
Q141168788	Lja	"アルネ・ガルボルグ・トゥンヘイム"
#   set the zh label to "阿尔内·加尔博格·通海姆"
Q141168788	Lzh	"阿尔内·加尔博格·通海姆"
#   Q141180396 Tollef Tollefson Tunheim: P22 father = Q141200112 Tollef Pederson Hetland
Q141180396	P22	Q141200112	S2600	"6000000037737683245"
#   P25 mother = Q141199826 Anna Maria Samuelsdtr. Tunheim
Q141180396	P25	Q141199826	S2600	"6000000037737683245"
#   set the ja label to "トッレヴ・トレフソン・トゥンヘイム"
Q141180396	Lja	"トッレヴ・トレフソン・トゥンヘイム"
#   set the zh label to "托勒夫·托勒夫松·通海姆"
Q141180396	Lzh	"托勒夫·托勒夫松·通海姆"
#   Q141168794 Betsy Jacobson: P22 father = Q141198428 Jacob Johannessen Aabø
Q141168794	P22	Q141198428	S2600	"6000000037737979829"
#   set the ja label to "ベッツィ・ヤコブソン"
Q141168794	Lja	"ベッツィ・ヤコブソン"
#   set the zh label to "贝齐·雅各布松"
Q141168794	Lzh	"贝齐·雅各布松"
#   Q141199833 Bertha Ingeborg Moen: P40 child = Q141199976 Mona Beth Tunheim
Q141199833	P40	Q141199976	S2600	"6000000039507595739"
#   P26 spouse = Q141189074 Joseph Tunheim
Q141199833	P26	Q141189074	S2600	"6000000039507595739"
#   P735 given name = Q16420820 Bertha, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141199833	P735	Q16420820	P1545	"1"	P7452	Q3409033
#   P735 given name = Q656590 Ingeborg, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141199833	P735	Q656590	P1545	"2"	P3831	Q245025
#   P734 family name = Q16934183 Moen
Q141199833	P734	Q16934183
#   Q141189074 Joseph Tunheim: P40 child = Q141199976 Mona Beth Tunheim
Q141189074	P40	Q141199976	S2600	"6000000039508106907"
#   P26 spouse = Q141199833 Bertha Ingeborg Moen
Q141189074	P26	Q141199833	S2600	"6000000039508106907"
#   Q141189049 Alfred Tunheim: P40 child = Q141199966 Mildred Lorraine Tunheim
Q141189049	P40	Q141199966	S2600	"6000000039510214027"
#   P26 spouse = Q141200084 Selma Johanna Horton
Q141189049	P26	Q141200084	S2600	"6000000039510214027"
#   Q141200084 Selma Johanna Horton: P40 child = Q141199966 Mildred Lorraine Tunheim
Q141200084	P40	Q141199966	S2600	"6000000039510366865"
#   P26 spouse = Q141189049 Alfred Tunheim
Q141200084	P26	Q141189049	S2600	"6000000039510366865"
#   P735 given name = Q713759 Selma, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141200084	P735	Q713759	P1545	"1"	P7452	Q3409033
#   P735 given name = Q4120836 Johanna, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141200084	P735	Q4120836	P1545	"2"	P3831	Q245025
#   P734 family name = Q16870893 Horton
Q141200084	P734	Q16870893
#   Q141189101 Samuel Tunheim: set the ja label to "サムエル・トゥンヘイム"
Q141189101	Lja	"サムエル・トゥンヘイム"
#   set the zh label to "萨穆埃尔·通海姆"
Q141189101	Lzh	"萨穆埃尔·通海姆"
#   Q141189109 Tollef Bud Tunheim: P40 child = Q141200047 NN Private
Q141189109	P40	Q141200047	S2600	"6000000039510907240"
#   P26 spouse = Q141199836 Florence June Williams
Q141189109	P26	Q141199836	S2600	"6000000039510907240"
#   Q141199836 Florence June Williams: P40 child = Q141200047 NN Private
Q141199836	P40	Q141200047	S2600	"6000000039511001067"
#   P26 spouse = Q141189109 Tollef Bud Tunheim
Q141199836	P26	Q141189109	S2600	"6000000039511001067"
#   P735 given name = Q950780 Florence, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141199836	P735	Q950780	P1545	"1"	P7452	Q3409033
#   P734 family name = Q1688722 Williams
Q141199836	P734	Q1688722
#   Q141198408 Herbert August Pierson: P40 child = Q141198387 Donald Herbert Pierson
Q141198408	P40	Q141198387	S2600	"6000000039512930731"
#   P26 spouse = Q141168801 Cora Estelle Tunheim
Q141198408	P26	Q141168801	S2600	"6000000039512930731"
#   P735 given name = Q4926833 Herbert, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141198408	P735	Q4926833	P1545	"1"	P7452	Q3409033
#   P735 given name = Q370731 August, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141198408	P735	Q370731	P1545	"2"	P3831	Q245025
#   Q141198464 Maren Olsdatter: P40 child = Q141189091 Ole Nicolai Bergersen
Q141198464	P40	Q141189091	S2600	"6000000055822300842"
#   P40 child = Q141189068 Hilde Constance Marie Bergersen
Q141198464	P40	Q141189068	S2600	"6000000055822300842"
#   P26 spouse = Q141168797 Christian Frederik Bergersen
Q141198464	P26	Q141168797	S2600	"6000000055822300842"
#   P735 given name = Q1666203 Maren
Q141198464	P735	Q1666203
#   P5056 patronym or matronym = Q51885688 Olsdatter
Q141198464	P5056	Q51885688
#   Q141189091 Ole Nicolai Bergersen: P25 mother = Q141198464 Maren Olsdatter
Q141189091	P25	Q141198464	S2600	"6000000055822412855"
#   Q141189068 Hilde Constance Marie Bergersen: P25 mother = Q141198464 Maren Olsdatter
Q141189068	P25	Q141198464	S2600	"6000000055822446833"
#   Q141198384 Carl Johan Edlund: P40 child = Q141189094 Oskar Edlund
Q141198384	P40	Q141189094	S2600	"6000000055825108079"
#   P26 spouse = Q141178201 Marie Petrine Simensdatter Bergersen
Q141198384	P26	Q141178201	S2600	"6000000055825108079"
#   P735 given name = Q2529610 Carl, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141198384	P735	Q2529610	P1545	"1"	P7452	Q3409033
#   P735 given name = Q10989273 Johan, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141198384	P735	Q10989273	P1545	"2"	P3831	Q245025
#   Q141200083 Sara NN: P40 child = Q141200604 Anna Nilsdotter
Q141200083	P40	Q141200604	S2600	"6000000059888596942"
#   P26 spouse = Q141200016 Nils Andersson
Q141200083	P26	Q141200016	S2600	"6000000059888596942"
#   P735 given name = Q833345 Sara
Q141200083	P735	Q833345
#   Q141199918 Kirsten Hansdatter Låge-Håland: P40 child = Q141189069 Ingeborg Ådnesdatter Grøtheim
Q141199918	P40	Q141189069	S2600	"6000000087451897836"
#   P26 spouse = Q141200127 Ådne Hansen Store Oma
Q141199918	P26	Q141200127	S2600	"6000000087451897836"
#   P735 given name = Q256744 Kirsten
Q141199918	P735	Q256744
#   Q141199976 Mona Beth Tunheim: P22 father = Q141189074 Joseph Tunheim
Q141199976	P22	Q141189074	S2600	"6000000162536870947"
#   P25 mother = Q141199833 Bertha Ingeborg Moen
Q141199976	P25	Q141199833	S2600	"6000000162536870947"
#   P735 given name = Q2419834 Mona, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141199976	P735	Q2419834	P1545	"1"	P7452	Q3409033
#   P735 given name = Q14639649 Beth, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141199976	P735	Q14639649	P1545	"2"	P3831	Q245025
#   Q141199952 Marie Tverdahl: P26 spouse = Q141168827 Hans Eivind Garborg
Q141199952	P26	Q141168827	S2600	"6000000177204223824"
#   P735 given name = Q106674406 Marie
Q141199952	P735	Q106674406
#   Q141199966 Mildred Lorraine Tunheim: P22 father = Q141189049 Alfred Tunheim
Q141199966	P22	Q141189049	S2600	"6000000180009386839"
#   P25 mother = Q141200084 Selma Johanna Horton
Q141199966	P25	Q141200084	S2600	"6000000180009386839"
#   P735 given name = Q11287301 Mildred, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141199966	P735	Q11287301	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1158295 Lorraine, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141199966	P735	Q1158295	P1545	"2"	P3831	Q245025
#   Q141198399 Eugene LeRoy Tunheim: P22 father = Q141168809 Edward Tunheim
Q141198399	P22	Q141168809	S2600	"6000000180028300872"
#   Q141200047 NN Private: P22 father = Q141189109 Tollef Bud Tunheim
Q141200047	P22	Q141189109	S2600	"6000000180039903952"
#   P25 mother = Q141199836 Florence June Williams
Q141200047	P25	Q141199836	S2600	"6000000180039903952"
#   Q141198387 Donald Herbert Pierson: P22 father = Q141198408 Herbert August Pierson
Q141198387	P22	Q141198408	S2600	"6000000180042586884"
#   P25 mother = Q141168801 Cora Estelle Tunheim
Q141198387	P25	Q141168801	S2600	"6000000180042586884"
#   P735 given name = Q13422248 Donald, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141198387	P735	Q13422248	P1545	"1"	P7452	Q3409033
#   P735 given name = Q4926833 Herbert, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141198387	P735	Q4926833	P1545	"2"	P3831	Q245025
#   Q141189062 Cecilie Jonsdatter: P22 father = Q116150299 Jon Reinmodsen
Q141189062	P22	Q116150299	S2600	"6000000180296055830"
#   P25 mother = Q116150300 Cecilie Ebbesdatter Hvide
Q141189062	P25	Q116150300	S2600	"6000000180296055830"
#   set the ja label to "セシリエ・ヨンスダッテル"
Q141189062	Lja	"セシリエ・ヨンスダッテル"
#   set the zh label to "塞西莉厄·永斯达特"
Q141189062	Lzh	"塞西莉厄·永斯达特"
#   Q141189110 Tøre Jonsen: P22 father = Q116150299 Jon Reinmodsen
Q141189110	P22	Q116150299	S2600	"6000000180307857930"
#   P25 mother = Q116150300 Cecilie Ebbesdatter Hvide
Q141189110	P25	Q116150300	S2600	"6000000180307857930"
#   Q141189080 Lave: P22 father = Q116150299 Jon Reinmodsen
Q141189080	P22	Q116150299	S2600	"6000000181444356836"
#   P25 mother = Q116150300 Cecilie Ebbesdatter Hvide
Q141189080	P25	Q116150300	S2600	"6000000181444356836"
#   set the ja label to "ラーヴェ"
Q141189080	Lja	"ラーヴェ"
#   set the zh label to "拉弗"
Q141189080	Lzh	"拉弗"
#   Q19657284 Buyeo Deokjang: P26 spouse = Q141198548 덕장 부여
Q19657284	P26	Q141198548	S2600	"6000000186285688253"
#   Q141198548 덕장 부여: P40 child = Q12598947 Taebi Buyeo
Q141198548	P40	Q12598947	S2600	"6000000186285688269"
#   P26 spouse = Q19657284 Buyeo Deokjang
Q141198548	P26	Q19657284	S2600	"6000000186285688269"
#   Q12598947 Taebi Buyeo: P25 mother = Q141198548 덕장 부여
Q12598947	P25	Q141198548	S2600	"6000000186285688286"
#   Q141198453 Lars Jonsen Kvam: P26 spouse = Q141198382 Berita Larsdatter Nedre Rossavik
Q141198453	P26	Q141198382	S2600	"6000000194934774831"
#   P735 given name = Q15635262 Lars
Q141198453	P735	Q15635262
#   P734 family name = Q30086760 Kvam
Q141198453	P734	Q30086760
#   Q141189054 Anna Maria Helgesdatter Bø: P22 father = Q141189066 Helge Rasmusson Bø
Q141189054	P22	Q141189066	S2600	"6000000196542059842"
#   Q141189113 Ådne Helgesen Bø: P22 father = Q141189066 Helge Rasmusson Bø
Q141189113	P22	Q141189066	S2600	"6000000196542455825"
#   Q141189067 Helmik Kristiansen Sør-Reime: P22 father = Q141189076 Kristian Larsen Nord-Varhaug
Q141189067	P22	Q141189076	S2600	"6000000221449620901"
#   Q141198390 Elisabet Marie Osmundsdatter Nygaard: P26 spouse = Q141189077 Lars Bernhard Kristiansen Sør-Reime
Q141198390	P26	Q141189077	S2600	"6000000224702448856"
#   P735 given name = Q16423275 Elisabet, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141198390	P735	Q16423275	P1545	"1"	P7452	Q3409033
#   P735 given name = Q106674406 Marie, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141198390	P735	Q106674406	P1545	"2"	P3831	Q245025
#   P734 family name = Q16880608 Nygaard
Q141198390	P734	Q16880608
#   Q141189078 Lars Kristiansen Sør-Reime: P22 father = Q141189076 Kristian Larsen Nord-Varhaug
Q141189078	P22	Q141189076	S2600	"6000000224702528843"
#   set the ja label to "ラーシュ・クリスティアンセン・セール・レイメ"
Q141189078	Lja	"ラーシュ・クリスティアンセン・セール・レイメ"
#   set the zh label to "拉尔斯·克里斯蒂安森·瑟尔·雷梅"
Q141189078	Lzh	"拉尔斯·克里斯蒂安森·瑟尔·雷梅"
#   Q141189077 Lars Bernhard Kristiansen Sør-Reime: P22 father = Q141189076 Kristian Larsen Nord-Varhaug
Q141189077	P22	Q141189076	S2600	"6000000224702710821"
#   P26 spouse = Q141198390 Elisabet Marie Osmundsdatter Nygaard
Q141189077	P26	Q141198390	S2600	"6000000224702710821"
#   Q141200127 Ådne Hansen Store Oma: P40 child = Q141189069 Ingeborg Ådnesdatter Grøtheim
Q141200127	P40	Q141189069	S2600	"6000000225229617898"
#   P26 spouse = Q141199918 Kirsten Hansdatter Låge-Håland
Q141200127	P26	Q141199918	S2600	"6000000225229617898"


# ---------------------------------------------------------------------------
# MANUAL ZIPPER MERGES -- hard-coded, appended to every batch, on purpose.
#
# Each line asserts that an existing Wikidata item IS a particular Geni person.
# These eight are on the Arne -> Charlemagne chain. Their items exist and are
# well documented, but carry no P2600 Geni.com profile ID, so nothing outside
# this repo records the correspondence and the chain cannot be followed on
# Wikidata. The daily algorithm depends on these pairings.
#
# They repeat every run by design. The first run that reaches an item adds the
# statement; every later run adds a duplicate, which QuickStatements merges away.
# That is the whole mechanism -- no state, no checking, no cleverness. When all
# eight are on Wikidata, delete this block.
#
# Evidence for each is in reports/wikidata-spine-add-p2600.qs: every one is
# anchored on a DIFFERENT relative that already carries a recorded P2600, never
# on a name match. Two were accepted by Emma on 2026-08-26.
# ---------------------------------------------------------------------------
#   Q5915800 Knut Algotsson: P2600 Geni.com profile ID
Q5915800	P2600	"6000000002572699392"
#   Q101247444 Ingegerd Svantepolksdotter: P2600 Geni.com profile ID
Q101247444	P2600	"6000000011239201122"
#   Q6197518 Svantepolk Knutsson Viby: P2600 Geni.com profile ID
Q6197518	P2600	"6000000003418900347"
#   Q3743799 Knut Valdemarsson, Duke of Estland: P2600 Geni.com profile ID
Q3743799	P2600	"6000000003076221220"
#   Q4953376 Helena Guttormsdatter: P2600 Geni.com profile ID
Q4953376	P2600	"6000000034013672054"
#   Q466257 Rozala of Italy: P2600 Geni.com profile ID
Q466257	P2600	"4258970970100070152"
#   Q274606 Berengar I, emperor of the Romans: P2600 Geni.com profile ID
Q274606	P2600	"6000000001669654269"
#   Q284400 Gisele of Cysoing: P2600 Geni.com profile ID
Q284400	P2600	"6000000000424624719"

