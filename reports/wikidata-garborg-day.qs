# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

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
#   set the en label to "Andreas Christiansen"
LAST	Len	"Andreas Christiansen"
#   set the mul label to "Andreas Christiansen"
LAST	Lmul	"Andreas Christiansen"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000016278848605 Andreas Christiansen
LAST	P2600	"6000000016278848605"
#   P569 date of birth = +1855-00-00T00:00:00Z/9
LAST	P569	+1855-00-00T00:00:00Z/9	S2600	"6000000016278848605"
#   P26 spouse = Q141189112 Wilhelmine Sophie Bergersen
LAST	P26	Q141189112	S2600	"6000000016278848605"
#   Q141189112 Wilhelmine Sophie Bergersen: P26 spouse = the item just created
Q141189112	P26	LAST	S2600	"6000000016278848605"
#   the item just created: P734 family name = Q11963736 Christiansen
LAST	P734	Q11963736

# create a new item
CREATE
#   set the en label to "Ane Marie Konstanse Amanda Kristine Hegre"
LAST	Len	"Ane Marie Konstanse Amanda Kristine Hegre"
#   set the mul label to "Ane Marie Konstanse Amanda Kristine Hegre"
LAST	Lmul	"Ane Marie Konstanse Amanda Kristine Hegre"
#   add a mul alias "Ane Marie Konstanse Amanda Kristine Christiansdatter"
LAST	Amul	"Ane Marie Konstanse Amanda Kristine Christiansdatter"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000018935780138 Ane Marie Konstanse Amanda Kristine Christiansdatter
LAST	P2600	"6000000018935780138"
#   P569 date of birth = +1875-07-19T00:00:00Z/11
LAST	P569	+1875-07-19T00:00:00Z/11	S2600	"6000000018935780138"
#   P570 date of death = +1951-03-06T00:00:00Z/11
LAST	P570	+1951-03-06T00:00:00Z/11	S2600	"6000000018935780138"
#   P26 spouse = Q141189070 John Jonassen Heigre
LAST	P26	Q141189070	S2600	"6000000018935780138"
#   Q141189070 John Jonassen Heigre: P26 spouse = the item just created
Q141189070	P26	LAST	S2600	"6000000018935780138"
#   the item just created: P735 given name = Q11958077 Ane, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q11958077	P1545	"1"	P7452	Q3409033
#   P735 given name = Q106674406 Marie, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q106674406	P1545	"2"	P3831	Q245025
#   P735 given name = Q453722 Amanda, qualified series ordinal 4, object of statement has role Q245025 middle name
LAST	P735	Q453722	P1545	"4"	P3831	Q245025
#   P735 given name = Q16859157 Kristine, qualified series ordinal 5, object of statement has role Q245025 middle name
LAST	P735	Q16859157	P1545	"5"	P3831	Q245025
#   P1449 nickname = en:"Anne Marie Hegre"
LAST	P1449	en:"Anne Marie Hegre"
#   add a mul alias "Anne Marie Hegre Hegre"
LAST	Amul	"Anne Marie Hegre Hegre"

# create a new item
CREATE
#   set the en label to "Anna Tormodsdatter Mele"
LAST	Len	"Anna Tormodsdatter Mele"
#   set the mul label to "Anna Tormodsdatter Mele"
LAST	Lmul	"Anna Tormodsdatter Mele"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005609232777 Anna Tormodsdatter Mele
LAST	P2600	"6000000005609232777"
#   P569 date of birth = +1678-00-00T00:00:00Z/9
LAST	P569	+1678-00-00T00:00:00Z/9	S2600	"6000000005609232777"
#   P570 date of death = +1747-00-00T00:00:00Z/9
LAST	P570	+1747-00-00T00:00:00Z/9	S2600	"6000000005609232777"
#   P22 father = Q141198507 Tormod Bjørnson Mele
LAST	P22	Q141198507	S2600	"6000000005609232777"
#   P25 mother = Q141198382 Berita Larsdatter Nedre Rossavik
LAST	P25	Q141198382	S2600	"6000000005609232777"
#   Q141198507 Tormod Bjørnson Mele: P40 child = the item just created
Q141198507	P40	LAST	S2600	"6000000005609232777"
#   Q141198382 Berita Larsdatter Nedre Rossavik: P40 child = the item just created
Q141198382	P40	LAST	S2600	"6000000005609232777"
#   the item just created: add a mul alias "Anna Mele"
LAST	Amul	"Anna Mele"

# create a new item
CREATE
#   set the en label to "Bergitte Ivarsdatter Tjentland"
LAST	Len	"Bergitte Ivarsdatter Tjentland"
#   set the mul label to "Bergitte Ivarsdatter Tjentland"
LAST	Lmul	"Bergitte Ivarsdatter Tjentland"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000007980617734 Bergitte Ivarsdatter Tjentland
LAST	P2600	"6000000007980617734"
#   P569 date of birth = +1585-00-00T00:00:00Z/9
LAST	P569	+1585-00-00T00:00:00Z/9	S2600	"6000000007980617734"
#   P570 date of death = +1647-00-00T00:00:00Z/9
LAST	P570	+1647-00-00T00:00:00Z/9	S2600	"6000000007980617734"
#   P40 child = Q141198755 Anna Ingebretsdatter Voster
LAST	P40	Q141198755	S2600	"6000000007980617734"
#   Q141198755 Anna Ingebretsdatter Voster: P25 mother = the item just created
Q141198755	P25	LAST	S2600	"6000000007980617734"
#   the item just created: P1449 nickname = en:"Berete"
LAST	P1449	en:"Berete"
#   add a mul alias "Berete Tjentland"
LAST	Amul	"Berete Tjentland"

# create a new item
CREATE
#   set the en label to "Bertrand Olav Olsen Vigdel"
LAST	Len	"Bertrand Olav Olsen Vigdel"
#   set the mul label to "Bertrand Olav Olsen Vigdel"
LAST	Lmul	"Bertrand Olav Olsen Vigdel"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000006146870818 Bertrand Olav Olsen Vigdel
LAST	P2600	"6000000006146870818"
#   P569 date of birth = +1918-05-10T00:00:00Z/11
LAST	P569	+1918-05-10T00:00:00Z/11	S2600	"6000000006146870818"
#   P570 date of death = +1941-04-01T00:00:00Z/11
LAST	P570	+1941-04-01T00:00:00Z/11	S2600	"6000000006146870818"
#   P22 father = Q141189070 John Jonassen Heigre
LAST	P22	Q141189070	S2600	"6000000006146870818"
#   Q141189070 John Jonassen Heigre: P40 child = the item just created
Q141189070	P40	LAST	S2600	"6000000006146870818"
#   the item just created: P735 given name = Q16511262 Olav, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q16511262	P1545	"2"	P3831	Q245025

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
#   set the en label to "Enok Jonson Rønneberg"
LAST	Len	"Enok Jonson Rønneberg"
#   set the mul label to "Enok Jonson Rønneberg"
LAST	Lmul	"Enok Jonson Rønneberg"
#   add a mul alias "Enok Jonson Lura"
LAST	Amul	"Enok Jonson Lura"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000001656464422 Enok Jonson Lura
LAST	P2600	"6000000001656464422"
#   P569 date of birth = +1810-00-00T00:00:00Z/9
LAST	P569	+1810-00-00T00:00:00Z/9	S2600	"6000000001656464422"
#   P570 date of death = +1886-07-29T00:00:00Z/11
LAST	P570	+1886-07-29T00:00:00Z/11	S2600	"6000000001656464422"
#   P40 child = Q141198510 Tønnes Emil Enokson Rønneberg
LAST	P40	Q141198510	S2600	"6000000001656464422"
#   Q141198510 Tønnes Emil Enokson Rønneberg: P22 father = the item just created
Q141198510	P22	LAST	S2600	"6000000001656464422"
#   the item just created: P735 given name = Q16423369 Enok
LAST	P735	Q16423369
#   P734 family name = Q7386722 Rønneberg
LAST	P734	Q7386722
#   add a mul alias "Enok Rønneberg"
LAST	Amul	"Enok Rønneberg"

# create a new item
CREATE
#   set the en label to "Erik Tollefson Foss-Eikeland"
LAST	Len	"Erik Tollefson Foss-Eikeland"
#   set the mul label to "Erik Tollefson Foss-Eikeland"
LAST	Lmul	"Erik Tollefson Foss-Eikeland"
#   add a mul alias "Erik Tollefson Fotland"
LAST	Amul	"Erik Tollefson Fotland"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000007977884350 Erik Tollefson Fotland
LAST	P2600	"6000000007977884350"
#   P569 date of birth = +1766-00-00T00:00:00Z/9
LAST	P569	+1766-00-00T00:00:00Z/9	S2600	"6000000007977884350"
#   P570 date of death = +1840-02-21T00:00:00Z/11
LAST	P570	+1840-02-21T00:00:00Z/11	S2600	"6000000007977884350"
#   P40 child = Q141198393 Erik Erikson Time
LAST	P40	Q141198393	S2600	"6000000007977884350"
#   Q141198393 Erik Erikson Time: P22 father = the item just created
Q141198393	P22	LAST	S2600	"6000000007977884350"
#   the item just created: P735 given name = Q750186 Erik
LAST	P735	Q750186
#   P734 family name = Q29726874 Fotland, qualified object of statement has role Q2507958 birth name
LAST	P734	Q29726874	P3831	Q2507958
#   P1449 nickname = en:"Erik Time"
LAST	P1449	en:"Erik Time"
#   add a mul alias "Erik Time Foss-Eikeland"
LAST	Amul	"Erik Time Foss-Eikeland"
#   add a mul alias "Erik Foss-Eikeland"
LAST	Amul	"Erik Foss-Eikeland"

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
#   set the en label to "Gotfred Olai Ekman"
LAST	Len	"Gotfred Olai Ekman"
#   set the mul label to "Gotfred Olai Ekman"
LAST	Lmul	"Gotfred Olai Ekman"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000039507605374 Gotfred Olai Ekman
LAST	P2600	"6000000039507605374"
#   P569 date of birth = +1893-09-02T00:00:00Z/11
LAST	P569	+1893-09-02T00:00:00Z/11	S2600	"6000000039507605374"
#   P570 date of death = +1953-06-30T00:00:00Z/11
LAST	P570	+1953-06-30T00:00:00Z/11	S2600	"6000000039507605374"
#   P26 spouse = Q141189102 Sigrid Sally Manilva Tunheim
LAST	P26	Q141189102	S2600	"6000000039507605374"
#   Q141189102 Sigrid Sally Manilva Tunheim: P26 spouse = the item just created
Q141189102	P26	LAST	S2600	"6000000039507605374"
#   the item just created: P735 given name = Q23497956 Gotfred, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q23497956	P1545	"1"	P7452	Q3409033
#   P735 given name = Q19384399 Olai, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q19384399	P1545	"2"	P3831	Q245025
#   P1449 nickname = en:"Gotfred Olie"
LAST	P1449	en:"Gotfred Olie"
#   add a mul alias "Gotfred Olie Ekman"
LAST	Amul	"Gotfred Olie Ekman"

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
#   set the en label to "Hans Svensen Risa I"
LAST	Len	"Hans Svensen Risa I"
#   set the mul label to "Hans Svensen Risa I"
LAST	Lmul	"Hans Svensen Risa I"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000006922466045 Hans Svensen Risa I
LAST	P2600	"6000000006922466045"
#   P569 date of birth = +1682-00-00T00:00:00Z/9
LAST	P569	+1682-00-00T00:00:00Z/9	S2600	"6000000006922466045"
#   P570 date of death = +1733-04-29T00:00:00Z/11
LAST	P570	+1733-04-29T00:00:00Z/11	S2600	"6000000006922466045"
#   P40 child = Q141199856 Guri Hansdatter Risa
LAST	P40	Q141199856	S2600	"6000000006922466045"
#   Q141199856 Guri Hansdatter Risa: P22 father = the item just created
Q141199856	P22	LAST	S2600	"6000000006922466045"

# create a new item
CREATE
#   the item just created: set the en label to "Herborg Johannesdatter Sør-Reime"
LAST	Len	"Herborg Johannesdatter Sør-Reime"
#   set the mul label to "Herborg Johannesdatter Sør-Reime"
LAST	Lmul	"Herborg Johannesdatter Sør-Reime"
#   add a mul alias "Herborg Johannesdatter Obrestad"
LAST	Amul	"Herborg Johannesdatter Obrestad"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000221449607942 Herborg Johannesdatter Obrestad
LAST	P2600	"6000000221449607942"
#   P569 date of birth = +1861-04-27T00:00:00Z/11
LAST	P569	+1861-04-27T00:00:00Z/11	S2600	"6000000221449607942"
#   P570 date of death = +1923-10-18T00:00:00Z/11
LAST	P570	+1923-10-18T00:00:00Z/11	S2600	"6000000221449607942"
#   P26 spouse = Q141189067 Helmik Kristiansen Sør-Reime
LAST	P26	Q141189067	S2600	"6000000221449607942"
#   Q141189067 Helmik Kristiansen Sør-Reime: P26 spouse = the item just created
Q141189067	P26	LAST	S2600	"6000000221449607942"
#   the item just created: P735 given name = Q11975140 Herborg
LAST	P735	Q11975140
#   add a mul alias "Herborg Sør-Reime"
LAST	Amul	"Herborg Sør-Reime"

# create a new item
CREATE
#   set the en label to "Ingebret Pederson Voster"
LAST	Len	"Ingebret Pederson Voster"
#   set the mul label to "Ingebret Pederson Voster"
LAST	Lmul	"Ingebret Pederson Voster"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000007980389582 Ingebret Pederson Voster
LAST	P2600	"6000000007980389582"
#   P569 date of birth = +1590-00-00T00:00:00Z/9
LAST	P569	+1590-00-00T00:00:00Z/9	S2600	"6000000007980389582"
#   P570 date of death = +1646-00-00T00:00:00Z/9
LAST	P570	+1646-00-00T00:00:00Z/9	S2600	"6000000007980389582"
#   P40 child = Q141198755 Anna Ingebretsdatter Voster
LAST	P40	Q141198755	S2600	"6000000007980389582"
#   Q141198755 Anna Ingebretsdatter Voster: P22 father = the item just created
Q141198755	P22	LAST	S2600	"6000000007980389582"
#   the item just created: P735 given name = Q30229695 Ingebret
LAST	P735	Q30229695
#   add a mul alias "Ingebret Voster"
LAST	Amul	"Ingebret Voster"

# create a new item
CREATE
#   set the en label to "Inger Osmundsdatter Risa"
LAST	Len	"Inger Osmundsdatter Risa"
#   set the mul label to "Inger Osmundsdatter Risa"
LAST	Lmul	"Inger Osmundsdatter Risa"
#   add a mul alias "Inger Osmundsdatter Tunheim"
LAST	Amul	"Inger Osmundsdatter Tunheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003491951665 Inger (Ingrid) Osmundsdatter Tunheim
LAST	P2600	"6000000003491951665"
#   P569 date of birth = +1682-00-00T00:00:00Z/9
LAST	P569	+1682-00-00T00:00:00Z/9	S2600	"6000000003491951665"
#   P570 date of death = +1719-00-00T00:00:00Z/9
LAST	P570	+1719-00-00T00:00:00Z/9	S2600	"6000000003491951665"
#   P40 child = Q141199856 Guri Hansdatter Risa
LAST	P40	Q141199856	S2600	"6000000003491951665"
#   Q141199856 Guri Hansdatter Risa: P25 mother = the item just created
Q141199856	P25	LAST	S2600	"6000000003491951665"
#   the item just created: P735 given name = Q3358452 Inger
LAST	P735	Q3358452
#   P1449 nickname = en:"Ingrid"
LAST	P1449	en:"Ingrid"
#   add a mul alias "Ingrid Risa"
LAST	Amul	"Ingrid Risa"
#   add a mul alias "Inger Risa"
LAST	Amul	"Inger Risa"

# create a new item
CREATE
#   set the en label to "Jöns Jakobsson guldsmed"
LAST	Len	"Jöns Jakobsson guldsmed"
#   set the mul label to "Jöns Jakobsson guldsmed"
LAST	Lmul	"Jöns Jakobsson guldsmed"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000006595807857 Jöns Jakobsson guldsmed
LAST	P2600	"6000000006595807857"
#   P40 child = Q141199822 Anna Jönsdotter
LAST	P40	Q141199822	S2600	"6000000006595807857"
#   Q141199822 Anna Jönsdotter: P22 father = the item just created
Q141199822	P22	LAST	S2600	"6000000006595807857"
#   the item just created: P735 given name = Q47526977 Jöns
LAST	P735	Q47526977
#   P734 family name = Q731903 Jakobsson
LAST	P734	Q731903

# create a new item
CREATE
#   set the en label to "Kari Olsdatter"
LAST	Len	"Kari Olsdatter"
#   set the mul label to "Kari Olsdatter"
LAST	Lmul	"Kari Olsdatter"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005609534649 Kari Olsdatter
LAST	P2600	"6000000005609534649"
#   P569 date of birth = +1729-00-00T00:00:00Z/9
LAST	P569	+1729-00-00T00:00:00Z/9	S2600	"6000000005609534649"
#   P570 date of death = +1804-03-30T00:00:00Z/11
LAST	P570	+1804-03-30T00:00:00Z/11	S2600	"6000000005609534649"
#   P40 child = Q141198375 Astri Torchelsdatter Øvre Time
LAST	P40	Q141198375	S2600	"6000000005609534649"
#   Q141198375 Astri Torchelsdatter Øvre Time: P25 mother = the item just created
Q141198375	P25	LAST	S2600	"6000000005609534649"
#   the item just created: P735 given name = Q1333594 Kari
LAST	P735	Q1333594
#   P5056 patronym or matronym = Q51885688 Olsdatter
LAST	P5056	Q51885688

# create a new item
CREATE
#   set the en label to "Kerstin Månsdotter"
LAST	Len	"Kerstin Månsdotter"
#   set the mul label to "Kerstin Månsdotter"
LAST	Lmul	"Kerstin Månsdotter"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000027469679490 Kerstin Månsdotter
LAST	P2600	"6000000027469679490"
#   P40 child = Q141199822 Anna Jönsdotter
LAST	P40	Q141199822	S2600	"6000000027469679490"
#   Q141199822 Anna Jönsdotter: P25 mother = the item just created
Q141199822	P25	LAST	S2600	"6000000027469679490"
#   the item just created: P735 given name = Q7618688 Kerstin
LAST	P735	Q7618688
#   P5056 patronym or matronym = Q28136553 Månsdotter
LAST	P5056	Q28136553

# create a new item
CREATE
#   set the en label to "Mabel Tunheim"
LAST	Len	"Mabel Tunheim"
#   set the mul label to "Mabel Tunheim"
LAST	Lmul	"Mabel Tunheim"
#   add a mul alias "Mabel Ingalls"
LAST	Amul	"Mabel Ingalls"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000039507489796 Mabel Ingalls
LAST	P2600	"6000000039507489796"
#   P569 date of birth = +1915-07-22T00:00:00Z/11
LAST	P569	+1915-07-22T00:00:00Z/11	S2600	"6000000039507489796"
#   P570 date of death = +2010-12-22T00:00:00Z/11
LAST	P570	+2010-12-22T00:00:00Z/11	S2600	"6000000039507489796"
#   P26 spouse = Q141189107 Theodore Roosevelt Tunheim
LAST	P26	Q141189107	S2600	"6000000039507489796"
#   Q141189107 Theodore Roosevelt Tunheim: P26 spouse = the item just created
Q141189107	P26	LAST	S2600	"6000000039507489796"
#   the item just created: P735 given name = Q949355 Mabel
LAST	P735	Q949355

# create a new item
CREATE
#   set the en label to "Malena Hansdatter Bø"
LAST	Len	"Malena Hansdatter Bø"
#   set the mul label to "Malena Hansdatter Bø"
LAST	Lmul	"Malena Hansdatter Bø"
#   add a mul alias "Malena Hansdatter Risa"
LAST	Amul	"Malena Hansdatter Risa"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005608880208 Malena Hansdatter Risa
LAST	P2600	"6000000005608880208"
#   P569 date of birth = +1747-00-00T00:00:00Z/9
LAST	P569	+1747-00-00T00:00:00Z/9	S2600	"6000000005608880208"
#   P40 child = Q141199809 Ane Marie Helgesdatter Bø
LAST	P40	Q141199809	S2600	"6000000005608880208"
#   Q141199809 Ane Marie Helgesdatter Bø: P25 mother = the item just created
Q141199809	P25	LAST	S2600	"6000000005608880208"
#   the item just created: P735 given name = Q5990536 Malena
LAST	P735	Q5990536
#   add a mul alias "Malena Bø"
LAST	Amul	"Malena Bø"

# create a new item
CREATE
#   set the en label to "Maria Jonsdatter Lura"
LAST	Len	"Maria Jonsdatter Lura"
#   set the mul label to "Maria Jonsdatter Lura"
LAST	Lmul	"Maria Jonsdatter Lura"
#   add a mul alias "Maria Jonsdatter Vatne"
LAST	Amul	"Maria Jonsdatter Vatne"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003491995109 Maria Jonsdatter Vatne
LAST	P2600	"6000000003491995109"
#   P569 date of birth = +1813-00-00T00:00:00Z/9
LAST	P569	+1813-00-00T00:00:00Z/9	S2600	"6000000003491995109"
#   P570 date of death = +1883-12-25T00:00:00Z/11
LAST	P570	+1883-12-25T00:00:00Z/11	S2600	"6000000003491995109"
#   P40 child = Q141198510 Tønnes Emil Enokson Rønneberg
LAST	P40	Q141198510	S2600	"6000000003491995109"
#   Q141198510 Tønnes Emil Enokson Rønneberg: P25 mother = the item just created
Q141198510	P25	LAST	S2600	"6000000003491995109"
#   the item just created: P734 family name = Q30134985 Vatne, qualified object of statement has role Q2507958 birth name
LAST	P734	Q30134985	P3831	Q2507958
#   add a mul alias "Maria Lura"
LAST	Amul	"Maria Lura"

# create a new item
CREATE
#   set the en label to "Marit Ormsd Byre"
LAST	Len	"Marit Ormsd Byre"
#   set the mul label to "Marit Ormsd Byre"
LAST	Lmul	"Marit Ormsd Byre"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000002301351344 Marit Ormsd Byre
LAST	P2600	"6000000002301351344"
#   P569 date of birth = +1553-00-00T00:00:00Z/9
LAST	P569	+1553-00-00T00:00:00Z/9	S2600	"6000000002301351344"
#   P570 date of death = +1617-00-00T00:00:00Z/9
LAST	P570	+1617-00-00T00:00:00Z/9	S2600	"6000000002301351344"
#   P26 spouse = Q141198832 Lars Gunnbjørnsen Mjølhus
LAST	P26	Q141198832	S2600	"6000000002301351344"
#   P40 child = Q141198831 Peder Larsen Mjølhus
LAST	P40	Q141198831	S2600	"6000000002301351344"
#   Q141198832 Lars Gunnbjørnsen Mjølhus: P26 spouse = the item just created
Q141198832	P26	LAST	S2600	"6000000002301351344"
#   Q141198831 Peder Larsen Mjølhus: P25 mother = the item just created
Q141198831	P25	LAST	S2600	"6000000002301351344"
#   the item just created: P735 given name = Q1566153 Marit, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q1566153	P1545	"1"	P7452	Q3409033
#   P1449 nickname = en:"Fister"
LAST	P1449	en:"Fister"
#   add a mul alias "Fister Byre"
LAST	Amul	"Fister Byre"

# create a new item
CREATE
#   set the en label to "Mathilde Fredrikke Thams"
LAST	Len	"Mathilde Fredrikke Thams"
#   set the mul label to "Mathilde Fredrikke Thams"
LAST	Lmul	"Mathilde Fredrikke Thams"
#   add a mul alias "Mathilde Fredrikke Christiansen"
LAST	Amul	"Mathilde Fredrikke Christiansen"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005718339007 Mathilde Fredrikke Christiansen
LAST	P2600	"6000000005718339007"
#   P569 date of birth = +1883-05-05T00:00:00Z/11
LAST	P569	+1883-05-05T00:00:00Z/11	S2600	"6000000005718339007"
#   P570 date of death = +1945-09-03T00:00:00Z/11
LAST	P570	+1945-09-03T00:00:00Z/11	S2600	"6000000005718339007"
#   P25 mother = Q141189112 Wilhelmine Sophie Bergersen
LAST	P25	Q141189112	S2600	"6000000005718339007"
#   Q141189112 Wilhelmine Sophie Bergersen: P40 child = the item just created
Q141189112	P40	LAST	S2600	"6000000005718339007"
#   the item just created: P735 given name = Q12326416 Mathilde, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q12326416	P1545	"1"	P7452	Q3409033
#   P735 given name = Q11970107 Fredrikke, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q11970107	P1545	"2"	P3831	Q245025
#   P734 family name = Q11963736 Christiansen, qualified object of statement has role Q2507958 birth name
LAST	P734	Q11963736	P3831	Q2507958
#   P1449 nickname = en:"Matty"
LAST	P1449	en:"Matty"
#   add a mul alias "Matty Thams"
LAST	Amul	"Matty Thams"

# create a new item
CREATE
#   set the mul label to "NN N.N. Gjøa"
LAST	Lmul	"NN N.N. Gjøa"
#   set the ca label to "mare de Lars Gunnbjørnsen Mjølhus"
LAST	Lca	"mare de Lars Gunnbjørnsen Mjølhus"
#   set the da label to "mor til Lars Gunnbjørnsen Mjølhus"
LAST	Lda	"mor til Lars Gunnbjørnsen Mjølhus"
#   set the de label to "Mutter von Lars Gunnbjørnsen Mjølhus"
LAST	Lde	"Mutter von Lars Gunnbjørnsen Mjølhus"
#   set the en label to "mother of Lars Gunnbjørnsen Mjølhus"
LAST	Len	"mother of Lars Gunnbjørnsen Mjølhus"
#   set the es label to "madre de Lars Gunnbjørnsen Mjølhus"
LAST	Les	"madre de Lars Gunnbjørnsen Mjølhus"
#   set the it label to "madre di Lars Gunnbjørnsen Mjølhus"
LAST	Lit	"madre di Lars Gunnbjørnsen Mjølhus"
#   set the nb label to "mor til Lars Gunnbjørnsen Mjølhus"
LAST	Lnb	"mor til Lars Gunnbjørnsen Mjølhus"
#   set the nl label to "moeder van Lars Gunnbjørnsen Mjølhus"
LAST	Lnl	"moeder van Lars Gunnbjørnsen Mjølhus"
#   set the pt label to "mãe de Lars Gunnbjørnsen Mjølhus"
LAST	Lpt	"mãe de Lars Gunnbjørnsen Mjølhus"
#   set the sv label to "mor till Lars Gunnbjørnsen Mjølhus"
LAST	Lsv	"mor till Lars Gunnbjørnsen Mjølhus"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000012242894384 N.N. Gjøa
LAST	P2600	"6000000012242894384"
#   P569 date of birth = +1520-00-00T00:00:00Z/9
LAST	P569	+1520-00-00T00:00:00Z/9	S2600	"6000000012242894384"
#   P26 spouse = Q141198834 Gunnbjørn Jonson Aukland
LAST	P26	Q141198834	S2600	"6000000012242894384"
#   P40 child = Q141198832 Lars Gunnbjørnsen Mjølhus
LAST	P40	Q141198832	S2600	"6000000012242894384"
#   Q141198834 Gunnbjørn Jonson Aukland: P26 spouse = the item just created
Q141198834	P26	LAST	S2600	"6000000012242894384"
#   Q141198832 Lars Gunnbjørnsen Mjølhus: P25 mother = the item just created
Q141198832	P25	LAST	S2600	"6000000012242894384"

# create a new item
CREATE
#   the item just created: set the mul label to "NN"
LAST	Lmul	"NN"
#   set the ca label to "mare de Andreas Olofsson"
LAST	Lca	"mare de Andreas Olofsson"
#   set the da label to "mor til Andreas Olofsson"
LAST	Lda	"mor til Andreas Olofsson"
#   set the de label to "Mutter von Andreas Olofsson"
LAST	Lde	"Mutter von Andreas Olofsson"
#   set the en label to "mother of Andreas Olofsson"
LAST	Len	"mother of Andreas Olofsson"
#   set the es label to "madre de Andreas Olofsson"
LAST	Les	"madre de Andreas Olofsson"
#   set the it label to "madre di Andreas Olofsson"
LAST	Lit	"madre di Andreas Olofsson"
#   set the nb label to "mor til Andreas Olofsson"
LAST	Lnb	"mor til Andreas Olofsson"
#   set the nl label to "moeder van Andreas Olofsson"
LAST	Lnl	"moeder van Andreas Olofsson"
#   set the pt label to "mãe de Andreas Olofsson"
LAST	Lpt	"mãe de Andreas Olofsson"
#   set the sv label to "mor till Andreas Olofsson"
LAST	Lsv	"mor till Andreas Olofsson"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000006828575883 NN
LAST	P2600	"6000000006828575883"
#   P40 child = Q141199808 Andreas Olofsson
LAST	P40	Q141199808	S2600	"6000000006828575883"
#   Q141199808 Andreas Olofsson: P25 mother = the item just created
Q141199808	P25	LAST	S2600	"6000000006828575883"

# create a new item
CREATE
#   the item just created: set the mul label to "NN Jonsdotter"
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
#   set the en label to "Olof Timmerman"
LAST	Len	"Olof Timmerman"
#   set the mul label to "Olof Timmerman"
LAST	Lmul	"Olof Timmerman"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003125391522 Olof Timmerman
LAST	P2600	"6000000003125391522"
#   P569 date of birth = +1486-00-00T00:00:00Z/9
LAST	P569	+1486-00-00T00:00:00Z/9	S2600	"6000000003125391522"
#   P570 date of death = +1549-00-00T00:00:00Z/9
LAST	P570	+1549-00-00T00:00:00Z/9	S2600	"6000000003125391522"
#   P40 child = Q141199808 Andreas Olofsson
LAST	P40	Q141199808	S2600	"6000000003125391522"
#   Q141199808 Andreas Olofsson: P22 father = the item just created
Q141199808	P22	LAST	S2600	"6000000003125391522"
#   the item just created: P735 given name = Q18089653 Olof
LAST	P735	Q18089653

# create a new item
CREATE
#   set the mul label to "NN"
LAST	Lmul	"NN"
#   set the ca label to "marit de Mona Beth Tunheim"
LAST	Lca	"marit de Mona Beth Tunheim"
#   set the da label to "ægtemand til Mona Beth Tunheim"
LAST	Lda	"ægtemand til Mona Beth Tunheim"
#   set the de label to "Ehemann von Mona Beth Tunheim"
LAST	Lde	"Ehemann von Mona Beth Tunheim"
#   set the en label to "husband of Mona Beth Tunheim"
LAST	Len	"husband of Mona Beth Tunheim"
#   set the es label to "esposo de Mona Beth Tunheim"
LAST	Les	"esposo de Mona Beth Tunheim"
#   set the it label to "marito di Mona Beth Tunheim"
LAST	Lit	"marito di Mona Beth Tunheim"
#   set the nb label to "ektemann til Mona Beth Tunheim"
LAST	Lnb	"ektemann til Mona Beth Tunheim"
#   set the nl label to "echtgenoot van Mona Beth Tunheim"
LAST	Lnl	"echtgenoot van Mona Beth Tunheim"
#   set the pt label to "marido de Mona Beth Tunheim"
LAST	Lpt	"marido de Mona Beth Tunheim"
#   set the sv label to "make till Mona Beth Tunheim"
LAST	Lsv	"make till Mona Beth Tunheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000180000912822 NN Private
LAST	P2600	"6000000180000912822"
#   P26 spouse = Q141199976 Mona Beth Tunheim
LAST	P26	Q141199976	S2600	"6000000180000912822"
#   Q141199976 Mona Beth Tunheim: P26 spouse = the item just created
Q141199976	P26	LAST	S2600	"6000000180000912822"

# create a new item
CREATE
#   the item just created: set the mul label to "NN"
LAST	Lmul	"NN"
#   set the ca label to "fill de Joseph Tunheim"
LAST	Lca	"fill de Joseph Tunheim"
#   set the da label to "søn af Joseph Tunheim"
LAST	Lda	"søn af Joseph Tunheim"
#   set the de label to "Sohn von Joseph Tunheim"
LAST	Lde	"Sohn von Joseph Tunheim"
#   set the en label to "son of Joseph Tunheim"
LAST	Len	"son of Joseph Tunheim"
#   set the es label to "hijo de Joseph Tunheim"
LAST	Les	"hijo de Joseph Tunheim"
#   set the it label to "figlio di Joseph Tunheim"
LAST	Lit	"figlio di Joseph Tunheim"
#   set the nb label to "sønn av Joseph Tunheim"
LAST	Lnb	"sønn av Joseph Tunheim"
#   set the nl label to "zoon van Joseph Tunheim"
LAST	Lnl	"zoon van Joseph Tunheim"
#   set the pt label to "filho de Joseph Tunheim"
LAST	Lpt	"filho de Joseph Tunheim"
#   set the sv label to "son till Joseph Tunheim"
LAST	Lsv	"son till Joseph Tunheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000179998546896 NN Private
LAST	P2600	"6000000179998546896"
#   P22 father = Q141189074 Joseph Tunheim
LAST	P22	Q141189074	S2600	"6000000179998546896"
#   P25 mother = Q141199833 Bertha Ingeborg Moen
LAST	P25	Q141199833	S2600	"6000000179998546896"
#   Q141189074 Joseph Tunheim: P40 child = the item just created
Q141189074	P40	LAST	S2600	"6000000179998546896"
#   Q141199833 Bertha Ingeborg Moen: P40 child = the item just created
Q141199833	P40	LAST	S2600	"6000000179998546896"

# create a new item
CREATE
#   the item just created: set the mul label to "NN"
LAST	Lmul	"NN"
#   set the ca label to "filla de Helmik Kristiansen Sør-Reime"
LAST	Lca	"filla de Helmik Kristiansen Sør-Reime"
#   set the da label to "datter af Helmik Kristiansen Sør-Reime"
LAST	Lda	"datter af Helmik Kristiansen Sør-Reime"
#   set the de label to "Tochter von Helmik Kristiansen Sør-Reime"
LAST	Lde	"Tochter von Helmik Kristiansen Sør-Reime"
#   set the en label to "daughter of Helmik Kristiansen Sør-Reime"
LAST	Len	"daughter of Helmik Kristiansen Sør-Reime"
#   set the es label to "hija de Helmik Kristiansen Sør-Reime"
LAST	Les	"hija de Helmik Kristiansen Sør-Reime"
#   set the it label to "figlia di Helmik Kristiansen Sør-Reime"
LAST	Lit	"figlia di Helmik Kristiansen Sør-Reime"
#   set the nb label to "datter av Helmik Kristiansen Sør-Reime"
LAST	Lnb	"datter av Helmik Kristiansen Sør-Reime"
#   set the nl label to "dochter van Helmik Kristiansen Sør-Reime"
LAST	Lnl	"dochter van Helmik Kristiansen Sør-Reime"
#   set the pt label to "filha de Helmik Kristiansen Sør-Reime"
LAST	Lpt	"filha de Helmik Kristiansen Sør-Reime"
#   set the sv label to "dotter till Helmik Kristiansen Sør-Reime"
LAST	Lsv	"dotter till Helmik Kristiansen Sør-Reime"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000224702291876 NN Private
LAST	P2600	"6000000224702291876"
#   P22 father = Q141189067 Helmik Kristiansen Sør-Reime
LAST	P22	Q141189067	S2600	"6000000224702291876"
#   Q141189067 Helmik Kristiansen Sør-Reime: P40 child = the item just created
Q141189067	P40	LAST	S2600	"6000000224702291876"

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
#   set the en label to "Ranveig Olsd Trevland"
LAST	Len	"Ranveig Olsd Trevland"
#   set the mul label to "Ranveig Olsd Trevland"
LAST	Lmul	"Ranveig Olsd Trevland"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000006358672581 Ranveig Olsd Trevland
LAST	P2600	"6000000006358672581"
#   P570 date of death = +1646-00-00T00:00:00Z/9
LAST	P570	+1646-00-00T00:00:00Z/9	S2600	"6000000006358672581"
#   P26 spouse = Q141198831 Peder Larsen Mjølhus
LAST	P26	Q141198831	S2600	"6000000006358672581"
#   P40 child = Q141198751 Lars Person Trevland
LAST	P40	Q141198751	S2600	"6000000006358672581"
#   Q141198831 Peder Larsen Mjølhus: P26 spouse = the item just created
Q141198831	P26	LAST	S2600	"6000000006358672581"
#   Q141198751 Lars Person Trevland: P25 mother = the item just created
Q141198751	P25	LAST	S2600	"6000000006358672581"
#   the item just created: P1449 nickname = en:"Larsson"
LAST	P1449	en:"Larsson"
#   add a mul alias "Larsson Trevland"
LAST	Amul	"Larsson Trevland"

# create a new item
CREATE
#   set the en label to "Rasmus Person Øksnevad"
LAST	Len	"Rasmus Person Øksnevad"
#   set the mul label to "Rasmus Person Øksnevad"
LAST	Lmul	"Rasmus Person Øksnevad"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005607155262 Rasmus Person Øksnevad
LAST	P2600	"6000000005607155262"
#   P569 date of birth = +1794-09-28T00:00:00Z/11
LAST	P569	+1794-09-28T00:00:00Z/11	S2600	"6000000005607155262"
#   P22 father = Q141200028 Per Jonson Grude
LAST	P22	Q141200028	S2600	"6000000005607155262"
#   P25 mother = Q141199937 Maren Halvorsdatter Storhaug
LAST	P25	Q141199937	S2600	"6000000005607155262"
#   Q141200028 Per Jonson Grude: P40 child = the item just created
Q141200028	P40	LAST	S2600	"6000000005607155262"
#   Q141199937 Maren Halvorsdatter Storhaug: P40 child = the item just created
Q141199937	P40	LAST	S2600	"6000000005607155262"
#   the item just created: P735 given name = Q1785744 Rasmus
LAST	P735	Q1785744
#   P734 family name = Q30583490 Øksnevad
LAST	P734	Q30583490

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
#   set the en label to "Thelma Geraldine Bagby"
LAST	Len	"Thelma Geraldine Bagby"
#   set the mul label to "Thelma Geraldine Bagby"
LAST	Lmul	"Thelma Geraldine Bagby"
#   add a mul alias "Thelma Geraldine Ekman"
LAST	Amul	"Thelma Geraldine Ekman"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000179983874822 Thelma Geraldine Ekman
LAST	P2600	"6000000179983874822"
#   P569 date of birth = +1920-01-31T00:00:00Z/11
LAST	P569	+1920-01-31T00:00:00Z/11	S2600	"6000000179983874822"
#   P570 date of death = +1981-09-08T00:00:00Z/11
LAST	P570	+1981-09-08T00:00:00Z/11	S2600	"6000000179983874822"
#   P25 mother = Q141189102 Sigrid Sally Manilva Tunheim
LAST	P25	Q141189102	S2600	"6000000179983874822"
#   Q141189102 Sigrid Sally Manilva Tunheim: P40 child = the item just created
Q141189102	P40	LAST	S2600	"6000000179983874822"
#   the item just created: P735 given name = Q3523520 Thelma, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q3523520	P1545	"1"	P7452	Q3409033

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

# RELATIONSHIPS between items that already exist -- the links yesterday's
#    creations made possible, and the properties never emitted. Every subject
#    and every value already has a QID, so this section depends on nothing above
#    it. It is emitted LAST, per her order: individuals, names, relationships.

#   Q116150300 Cecilie Ebbesdatter Hvide: set the ja label to "セシリエ・エッベスダッテル・ヴィーデ"
Q116150300	Lja	"セシリエ・エッベスダッテル・ヴィーデ"
#   set the zh label to "塞西莉厄·埃贝斯达特·维德"
Q116150300	Lzh	"塞西莉厄·埃贝斯达特·维德"
#   Q5975022 Lars August Mannerheim: P3373 sibling = Q1814297 Carl Erik Mannerheim
Q5975022	P3373	Q1814297	S2600	"6000000000047190401"
#   Q1814297 Carl Erik Mannerheim: P3373 sibling = Q5975022 Lars August Mannerheim
Q1814297	P3373	Q5975022	S2600	"6000000000047267273"
#   Q141199899 Jon Tollakson Aukland IV: P40 child = Q141200101 Sissel Jonsdatter Aukland
Q141199899	P40	Q141200101	S2600	"6000000002391120029"
#   Q141199891 Ivar Valheim: P26 spouse = Q141200101 Sissel Jonsdatter Aukland
Q141199891	P26	Q141200101	S2600	"6000000002452595429"
#   Q141199851 Gunnbjørn Toresson Tengs: P26 spouse = Q141199862 Helga Bjørnsdatter Bjørnsdatter
Q141199851	P26	Q141199862	S2600	"6000000002463510938"
#   Q141189104 Siri Kristine Ivarsdatter Sandsmark: set the ja label to "シーリ・クリスティーネ・イーヴァシュダッテル・サンスマルク"
Q141189104	Lja	"シーリ・クリスティーネ・イーヴァシュダッテル・サンスマルク"
#   set the zh label to "西丽·克丽丝汀·伊瓦斯达特·桑斯马克"
Q141189104	Lzh	"西丽·克丽丝汀·伊瓦斯达特·桑斯马克"
#   Q141200019 Ola Olsen Grøtheim: P25 mother = Q141199830 Anna Rasmusdatter Årsland
Q141200019	P25	Q141199830	S2600	"6000000002989071216"
#   set the ja label to "オーラ・オルセン・グレートヘイム"
Q141200019	Lja	"オーラ・オルセン・グレートヘイム"
#   set the zh label to "乌拉·奥尔森·格勒特海姆"
Q141200019	Lzh	"乌拉·奥尔森·格勒特海姆"
#   Q141200101 Sissel Jonsdatter Aukland: P22 father = Q141199899 Jon Tollakson Aukland IV
Q141200101	P22	Q141199899	S2600	"6000000003043806217"
#   P26 spouse = Q141199891 Ivar Valheim
Q141200101	P26	Q141199891	S2600	"6000000003043806217"
#   P26 spouse = Q141200111 Sæbjørn Toresson Talgje
Q141200101	P26	Q141200111	S2600	"6000000003043806217"
#   Q141189055 Astri Torkelsdatter Gilja: set the ja label to "アストリ・トルケルスダッテル・ギリヤ"
Q141189055	Lja	"アストリ・トルケルスダッテル・ギリヤ"
#   set the zh label to "阿斯特丽·托克尔斯达特·吉利亚"
Q141189055	Lzh	"阿斯特丽·托克尔斯达特·吉利亚"
#   Q141200067 Rasmus Kjetilson Kjetilsen Høle: P26 spouse = Q141200094 Siri Rasmusdtr. Erevik
Q141200067	P26	Q141200094	S2600	"6000000003095034915"
#   Q141200094 Siri Rasmusdtr. Erevik: P26 spouse = Q141200067 Rasmus Kjetilson Kjetilsen Høle
Q141200094	P26	Q141200067	S2600	"6000000003095172404"
#   Q10608167 Olaus Persson: P40 child = Q16650154 Ericus Olai Plantin
Q10608167	P40	Q16650154	S2600	"6000000003110778492"
#   Q141199819 Anna Andersdotter: P40 child = Q141200016 Nils Andersson
Q141199819	P40	Q141200016	S2600	"6000000003125438035"
#   P26 spouse = Q141199808 Andreas Olofsson
Q141199819	P26	Q141199808	S2600	"6000000003125438035"
#   set the ja label to "アンナ・アンデシュドッテル"
Q141199819	Lja	"アンナ・アンデシュドッテル"
#   set the zh label to "安娜·安德斯多特"
Q141199819	Lzh	"安娜·安德斯多特"
#   Q16650154 Ericus Olai Plantin: P22 father = Q10608167 Olaus Persson
Q16650154	P22	Q10608167	S2600	"6000000003374922780"
#   Q141199892 Jon Olsen Heigre: P26 spouse = Q141200054 Rakel Jonsdatter Jonsdotter Vatne
Q141199892	P26	Q141200054	S2600	"6000000003491986736"
#   set the ja label to "ヨン・オルセン・ヘイグレ"
Q141199892	Lja	"ヨン・オルセン・ヘイグレ"
#   set the zh label to "永·奥尔森·海格勒"
Q141199892	Lzh	"永·奥尔森·海格勒"
#   Q141200054 Rakel Jonsdatter Jonsdotter Vatne: P26 spouse = Q141199892 Jon Olsen Heigre
Q141200054	P26	Q141199892	S2600	"6000000003491986761"
#   Q141168957 Jonas Jonson Heigre: set the ja label to "ヨナス・ヨンソン・ヘイグレ"
Q141168957	Lja	"ヨナス・ヨンソン・ヘイグレ"
#   set the zh label to "约纳斯·永松·海格勒"
Q141168957	Lzh	"约纳斯·永松·海格勒"
#   Q141178196 Elisabet Kirstine Eriksdatter Stangeland: set the ja label to "エリサベート・シシュティーネ・エリクスダッテル・スタンゲラン"
Q141178196	Lja	"エリサベート・シシュティーネ・エリクスダッテル・スタンゲラン"
#   set the zh label to "伊丽莎白·谢什蒂内·埃里克斯达特·斯坦格兰"
Q141178196	Lzh	"伊丽莎白·谢什蒂内·埃里克斯达特·斯坦格兰"
#   Q141152523 Ane Oline Jonsdatter Raugstad: set the ja label to "アーネ・オリーネ・ヨンスダッテル・ラウグスタード"
Q141152523	Lja	"アーネ・オリーネ・ヨンスダッテル・ラウグスタード"
#   set the zh label to "安内·奥利内·永斯达特·劳格斯塔"
Q141152523	Lzh	"安内·奥利内·永斯达特·劳格斯塔"
#   Q141178198 Enevald Jonasson Heigre: set the ja label to "エーネヴァル・ヨナソン・ヘイグレ"
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
#   Q141198510 Tønnes Emil Enokson Rønneberg: set the ja label to "テンネス・エミール・エノクソン・レンネベルグ"
Q141198510	Lja	"テンネス・エミール・エノクソン・レンネベルグ"
#   set the zh label to "滕内斯·埃米尔·埃诺克松·伦内贝格"
Q141198510	Lzh	"滕内斯·埃米尔·埃诺克松·伦内贝格"
#   Q141152512 Eivind Aadnesson Garborg: set the ja label to "エイヴィン・オードネソン・ガルボルグ"
Q141152512	Lja	"エイヴィン・オードネソン・ガルボルグ"
#   set the zh label to "埃温·奥德内松·加尔博格"
Q141152512	Lzh	"埃温·奥德内松·加尔博格"
#   Q141152600 Stine Stena Eivindsdatter Garborg: set the ja label to "スティーネ・ステーナ・エイヴィンスダッテル・ガルボルグ"
Q141152600	Lja	"スティーネ・ステーナ・エイヴィンスダッテル・ガルボルグ"
#   set the zh label to "斯蒂内·斯泰娜·埃温斯达特·加尔博格"
Q141152600	Lzh	"斯蒂内·斯泰娜·埃温斯达特·加尔博格"
#   Q141152614 Jon Eivindson Garborg: set the ja label to "ヨン・エイヴィンソン・ガルボルグ"
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
#   Q141162043 Inger Marie Mary Eivindsdatter Garborg: set the ja label to "インゲル・マリー・メアリー・エイヴィンスダッテル・ガルボルグ"
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
#   Q141162046 Ane Oline Lena Eivindsdatter Garborg: set the ja label to "アーネ・オリーネ・レーナ・エイヴィンスダッテル・ガルボルグ"
Q141162046	Lja	"アーネ・オリーネ・レーナ・エイヴィンスダッテル・ガルボルグ"
#   set the zh label to "安内·奥利内·莱娜·埃温斯达特·加尔博格"
Q141162046	Lzh	"安内·奥利内·莱娜·埃温斯达特·加尔博格"
#   Q141169072 Ådne Olsen Grøtheim: set the ja label to "オードネ・オルセン・グレートヘイム"
Q141169072	Lja	"オードネ・オルセン・グレートヘイム"
#   set the zh label to "奥德内·奥尔森·格勒特海姆"
Q141169072	Lzh	"奥德内·奥尔森·格勒特海姆"
#   Q141178202 Stine Persdatter Øksnevad: set the ja label to "スティーネ・ペシュダッテル・エクスネヴァード"
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
#   Q141168955 Jon Samuelsen Raustad: set the ja label to "ヨン・サムエルセン・ラウスタード"
Q141168955	Lja	"ヨン・サムエルセン・ラウスタード"
#   set the zh label to "永·萨穆埃尔森·劳斯塔"
Q141168955	Lzh	"永·萨穆埃尔森·劳斯塔"
#   Q141200111 Sæbjørn Toresson Talgje: P26 spouse = Q141200101 Sissel Jonsdatter Aukland
Q141200111	P26	Q141200101	S2600	"6000000004213963966"
#   Q141199808 Andreas Olofsson: P40 child = Q141200016 Nils Andersson
Q141199808	P40	Q141200016	S2600	"6000000004334566448"
#   P26 spouse = Q141199819 Anna Andersdotter
Q141199808	P26	Q141199819	S2600	"6000000004334566448"
#   Q633094 Johannes Tomasson: set the zh label to "约翰内斯·托马松"
Q633094	Lzh	"约翰内斯·托马松"
#   Q141180413 Thomas Mattsson: set the ja label to "トーマス・マットソン"
Q141180413	Lja	"トーマス・マットソン"
#   set the zh label to "托马斯·马特松"
Q141180413	Lzh	"托马斯·马特松"
#   Q141199862 Helga Bjørnsdatter Bjørnsdatter: P26 spouse = Q141199851 Gunnbjørn Toresson Tengs
Q141199862	P26	Q141199851	S2600	"6000000004697849241"
#   Q141178149 Anna Fartegnsdatter Seim: set the ja label to "アンナ・ファルテグンスダッテル・セイム"
Q141178149	Lja	"アンナ・ファルテグンスダッテル・セイム"
#   set the zh label to "安娜·法尔特格恩斯达特·塞姆"
Q141178149	Lzh	"安娜·法尔特格恩斯达特·塞姆"
#   Q141200028 Per Jonson Grude: P26 spouse = Q141199937 Maren Halvorsdatter Storhaug
Q141200028	P26	Q141199937	S2600	"6000000005606907249"
#   Q141199937 Maren Halvorsdatter Storhaug: P26 spouse = Q141200028 Per Jonson Grude
Q141199937	P26	Q141200028	S2600	"6000000005607155237"
#   Q11959067 Arne Olaus Fjørtoft Garborg: set the ja label to "アルネ・オーラウス・フョルトフト・ガルボルグ"
Q11959067	Lja	"アルネ・オーラウス・フョルトフト・ガルボルグ"
#   set the zh label to "阿尔内·奥劳斯·夫约托夫特·加尔博格"
Q11959067	Lzh	"阿尔内·奥劳斯·夫约托夫特·加尔博格"
#   Q141168827 Hans Eivind Garborg: set the ja label to "ハンス・エイヴィン・ガルボルグ"
Q141168827	Lja	"ハンス・エイヴィン・ガルボルグ"
#   set the zh label to "汉斯·埃温·加尔博格"
Q141168827	Lzh	"汉斯·埃温·加尔博格"
#   Q141189079 Lars Tormodsen Mele: set the ja label to "ラーシュ・トルモドセン・メーレ"
Q141189079	Lja	"ラーシュ・トルモドセン・メーレ"
#   set the zh label to "拉尔斯·托尔莫德森·梅勒"
Q141189079	Lzh	"拉尔斯·托尔莫德森·梅勒"
#   Q141189071 Joren Jonsdatter Espedal: set the ja label to "ヨーレン・ヨンスダッテル・エスペダール"
Q141189071	Lja	"ヨーレン・ヨンスダッテル・エスペダール"
#   set the zh label to "约伦·永斯达特·埃斯佩达尔"
Q141189071	Lzh	"约伦·永斯达特·埃斯佩达尔"
#   Q141178200 Inger Kristoffersdatter: set the ja label to "インゲル・クリストッフェシュダッテル"
Q141178200	Lja	"インゲル・クリストッフェシュダッテル"
#   set the zh label to "英厄尔·克里斯托弗斯达特"
Q141178200	Lzh	"英厄尔·克里斯托弗斯达特"
#   Q141180408 Jon Larsson Li: set the ja label to "ヨン・ラーション・リ"
Q141180408	Lja	"ヨン・ラーション・リ"
#   set the zh label to "永·拉尔松·李"
Q141180408	Lzh	"永·拉尔松·李"
#   Q141180412 Marta Rasmusdatter Høle: set the ja label to "マルタ・ラスムスダッテル・ヘーレ"
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
#   Q141180409 Magdalena Andersdotter Bure: set the ja label to "マグダレーナ・アンデシュドッテル・ブーレ"
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
#   Q141168811 Eivind Garborg: set the ja label to "エイヴィン・ガルボルグ"
Q141168811	Lja	"エイヴィン・ガルボルグ"
#   set the zh label to "埃温·加尔博格"
Q141168811	Lzh	"埃温·加尔博格"
#   Q141198499 Solveig Garborg: set the ja label to "ソルヴェイグ・ガルボルグ"
Q141198499	Lja	"ソルヴェイグ・ガルボルグ"
#   set the zh label to "索尔维格·加尔博格"
Q141198499	Lzh	"索尔维格·加尔博格"
#   Q141199881 Ivar Garborg: set the ja label to "イーヴァル・ガルボルグ"
Q141199881	Lja	"イーヴァル・ガルボルグ"
#   set the zh label to "伊瓦尔·加尔博格"
Q141199881	Lzh	"伊瓦尔·加尔博格"
#   Q141198489 Sigrid Garborg: set the ja label to "シーグリ・ガルボルグ"
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
#   Q141199959 Martinus Johannis: P26 spouse = Q141199822 Anna Jönsdotter
Q141199959	P26	Q141199822	S2600	"6000000006828782200"
#   Q141200604 Anna Nilsdotter: P22 father = Q141200016 Nils Andersson
Q141200604	P22	Q141200016	S2600	"6000000007020763500"
#   P25 mother = Q141200083 Sara NN
Q141200604	P25	Q141200083	S2600	"6000000007020763500"
#   Q141200074 Rasmus Olsen Grøtheim: P25 mother = Q141199830 Anna Rasmusdatter Årsland
Q141200074	P25	Q141199830	S2600	"6000000007744183945"
#   P26 spouse = Q141199809 Ane Marie Helgesdatter Bø
Q141200074	P26	Q141199809	S2600	"6000000007744183945"
#   Q141199809 Ane Marie Helgesdatter Bø: P26 spouse = Q141200074 Rasmus Olsen Grøtheim
Q141199809	P26	Q141200074	S2600	"6000000007896103690"
#   Q141199925 Knut Elvindson Garborg: P26 spouse = Q141199856 Guri Hansdatter Risa
Q141199925	P26	Q141199856	S2600	"6000000007896295466"
#   Q141199856 Guri Hansdatter Risa: P26 spouse = Q141199925 Knut Elvindson Garborg
Q141199856	P26	Q141199925	S2600	"6000000007896387570"
#   Q141189069 Ingeborg Ådnesdatter Grøtheim: set the ja label to "インゲボルグ・オードネスダッテル・グレートヘイム"
Q141189069	Lja	"インゲボルグ・オードネスダッテル・グレートヘイム"
#   set the zh label to "英厄堡·奥德内斯达特·格勒特海姆"
Q141189069	Lzh	"英厄堡·奥德内斯达特·格勒特海姆"
#   Q141199830 Anna Rasmusdatter Årsland: P40 child = Q141200019 Ola Olsen Grøtheim
Q141199830	P40	Q141200019	S2600	"6000000008176804564"
#   P40 child = Q141200074 Rasmus Olsen Grøtheim
Q141199830	P40	Q141200074	S2600	"6000000008176804564"
#   Q141189108 Tillie Betsy Tunheim: set the ja label to "ティリー・ベッツィ・トゥンヘイム"
Q141189108	Lja	"ティリー・ベッツィ・トゥンヘイム"
#   set the zh label to "蒂莉·贝齐·通海姆"
Q141189108	Lzh	"蒂莉·贝齐·通海姆"
#   Q141178201 Marie Petrine Simensdatter Bergersen: set the ja label to "マリー・ペトリーネ・シメンスダッテル・ベルゲルセン"
Q141178201	Lja	"マリー・ペトリーネ・シメンスダッテル・ベルゲルセン"
#   set the zh label to "玛丽·佩特里内·西门斯达特·贝格尔森"
Q141178201	Lzh	"玛丽·佩特里内·西门斯达特·贝格尔森"
#   Q141168797 Christian Frederik Bergersen: set the ja label to "クリスチャン・フレデリク・ベルゲルセン"
Q141168797	Lja	"クリスチャン・フレデリク・ベルゲルセン"
#   set the zh label to "克里斯蒂安·弗雷德里克·贝格尔森"
Q141168797	Lzh	"克里斯蒂安·弗雷德里克·贝格尔森"
#   Q141189059 Bryniolf Bengtsson (Hafridssons ätt): P22 father = Q141198381 Bengt Hafridsson Lejon
Q141189059	P22	Q141198381	S2600	"6000000011239545575"
#   P40 child = Q141189050 Algot Bryniolfsson
Q141189059	P40	Q141189050	S2600	"6000000011239545575"
#   Q141180410 Margareta Mårtensdotter Bång: set the ja label to "マルガレータ・モーテンスドッテル・ボング"
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
#   Q141178199 Gunder Bergersen: set the ja label to "グンデル・ベルゲルセン"
Q141178199	Lja	"グンデル・ベルゲルセン"
#   set the zh label to "贡德尔·贝格尔森"
Q141178199	Lzh	"贡德尔·贝格尔森"
#   Q141198428 Jacob Johannessen Aabø: set the ja label to "ヤコブ・ヨハンネセン・オーベー"
Q141198428	Lja	"ヤコブ・ヨハンネセン・オーベー"
#   set the zh label to "雅各布·约翰内森·奥贝"
Q141198428	Lzh	"雅各布·约翰内森·奥贝"
#   Q141189084 Martin Tollefson Tunheim: set the ja label to "マルティン・トレフソン・トゥンヘイム"
Q141189084	Lja	"マルティン・トレフソン・トゥンヘイム"
#   set the zh label to "马丁·托勒夫松·通海姆"
Q141189084	Lzh	"马丁·托勒夫松·通海姆"
#   Q141199930 Knut Olsen Grøtheim: set the ja label to "クヌート・オルセン・グレートヘイム"
Q141199930	Lja	"クヌート・オルセン・グレートヘイム"
#   set the zh label to "克努特·奥尔森·格勒特海姆"
Q141199930	Lzh	"克努特·奥尔森·格勒特海姆"
#   Q141180395 Maren Gulbrandsdatter Ommestad: set the ja label to "マーレン・グルブランスダッテル・オンメスタード"
Q141180395	Lja	"マーレン・グルブランスダッテル・オンメスタード"
#   set the zh label to "马伦·古尔布兰斯达特·翁梅斯塔德"
Q141180395	Lzh	"马伦·古尔布兰斯达特·翁梅斯塔德"
#   Q141168784 Aagot Garborg: set the ja label to "オーゴット・ガルボルグ"
Q141168784	Lja	"オーゴット・ガルボルグ"
#   set the zh label to "奥高特·加尔博格"
Q141168784	Lzh	"奥高特·加尔博格"
#   Q141199909 Karen Sophie Pedersdatter: set the ja label to "カーレン・ソフィー・ペーデシュダッテル"
Q141199909	Lja	"カーレン・ソフィー・ペーデシュダッテル"
#   set the zh label to "卡伦·索菲·佩德斯达特"
Q141199909	Lzh	"卡伦·索菲·佩德斯达特"
#   Q138474188 Hans Syvertsen Nyvold: set the ja label to "ハンス・シーヴェシェン・ニーヴォル"
Q138474188	Lja	"ハンス・シーヴェシェン・ニーヴォル"
#   set the zh label to "汉斯·西韦特森·尼沃尔"
Q138474188	Lzh	"汉斯·西韦特森·尼沃尔"
#   Q141168785 Aagot Nyvold: set the ja label to "オーゴット・ニーヴォル"
Q141168785	Lja	"オーゴット・ニーヴォル"
#   set the zh label to "奥高特·尼沃尔"
Q141168785	Lzh	"奥高特·尼沃尔"
#   Q141168803 Dagny Nyvold: set the ja label to "ダグニー・ニーヴォル"
Q141168803	Lja	"ダグニー・ニーヴォル"
#   set the zh label to "达格妮·尼沃尔"
Q141168803	Lzh	"达格妮·尼沃尔"
#   Q141178197 Elisabeth Johannesen: P735 given name = Q63611044 Elisabeth
Q141178197	P735	Q63611044
#   set the ja label to "エリーサベト・ヨハンネセン"
Q141178197	Lja	"エリーサベト・ヨハンネセン"
#   set the zh label to "伊丽莎白·约翰内森"
Q141178197	Lzh	"伊丽莎白·约翰内森"
#   Q141199845 NN Garborg: P734 family name = Q30250555 Garborg
Q141199845	P734	Q30250555
#   Q141189081 Lotte Birgithe Gustava Jonasdatter Heigre: set the ja label to "ロッテ・ビルギーテ・グスタヴァ・ヨナスダッテル・ヘイグレ"
Q141189081	Lja	"ロッテ・ビルギーテ・グスタヴァ・ヨナスダッテル・ヘイグレ"
#   set the zh label to "洛特·比尔吉特·古斯塔娃·约纳斯达特·海格勒"
Q141189081	Lzh	"洛特·比尔吉特·古斯塔娃·约纳斯达特·海格勒"
#   Q141180406 Ingeborg Gyntesdotter: set the ja label to "インゲボルグ・ギュンテスドッテル"
Q141180406	Lja	"インゲボルグ・ギュンテスドッテル"
#   set the zh label to "英厄堡·金特斯多特"
Q141180406	Lzh	"英厄堡·金特斯多特"
#   Q141199822 Anna Jönsdotter: P26 spouse = Q141199959 Martinus Johannis
Q141199822	P26	Q141199959	S2600	"6000000027470336201"
#   Q141189076 Kristian Larsen Nord-Varhaug: set the ja label to "クリスティアン・ラーシェン・ノール・ヴァールハウグ"
Q141189076	Lja	"クリスティアン・ラーシェン・ノール・ヴァールハウグ"
#   set the zh label to "克里斯蒂安·拉尔森·诺尔·瓦尔豪格"
Q141189076	Lzh	"克里斯蒂安·拉尔森·诺尔·瓦尔豪格"
#   Q141199826 Anna Maria Samuelsdtr. Tunheim: P26 spouse = Q141200112 Tollef Pederson Hetland
Q141199826	P26	Q141200112	S2600	"6000000029983034410"
#   Q141200112 Tollef Pederson Hetland: P26 spouse = Q141199826 Anna Maria Samuelsdtr. Tunheim
Q141200112	P26	Q141199826	S2600	"6000000029983078557"
#   Q141198472 Olga E. Tunheim: set the ja label to "オルガ・E.・トゥンヘイム"
Q141198472	Lja	"オルガ・E.・トゥンヘイム"
#   set the zh label to "奥尔加·E.·通海姆"
Q141198472	Lzh	"奥尔加·E.·通海姆"
#   Q141169062 Thoralf Tunheim: set the ja label to "トーラルフ・トゥンヘイム"
Q141169062	Lja	"トーラルフ・トゥンヘイム"
#   set the zh label to "托拉尔夫·通海姆"
Q141169062	Lzh	"托拉尔夫·通海姆"
#   Q141168801 Cora Estelle Tunheim: set the ja label to "コーラ・エステル・トゥンヘイム"
Q141168801	Lja	"コーラ・エステル・トゥンヘイム"
#   set the zh label to "科拉·埃斯特尔·通海姆"
Q141168801	Lzh	"科拉·埃斯特尔·通海姆"
#   Q141168809 Edward Tunheim: set the ja label to "エドワード・トゥンヘイム"
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
#   Q141199868 Ingvold (Pinkie) Remmie: set the ja label to "イングヴォル・ピンキー・レミー"
Q141199868	Lja	"イングヴォル・ピンキー・レミー"
#   set the zh label to "英瓦尔·平基·雷米"
Q141199868	Lzh	"英瓦尔·平基·雷米"
#   Q141168820 Eliza Ronneberg: set the ja label to "エリザ・ロンネベルグ"
Q141168820	Lja	"エリザ・ロンネベルグ"
#   set the zh label to "伊莱扎·龙内贝格"
Q141168820	Lzh	"伊莱扎·龙内贝格"
#   Q141168789 Arnold Ronneberg: set the ja label to "アルノルド・ロンネベルグ"
Q141168789	Lja	"アルノルド・ロンネベルグ"
#   set the zh label to "阿诺德·龙内贝格"
Q141168789	Lzh	"阿诺德·龙内贝格"
#   Q141168805 Edward Ronneberg: set the ja label to "エドワード・ロンネベルグ"
Q141168805	Lja	"エドワード・ロンネベルグ"
#   set the zh label to "爱德华·龙内贝格"
Q141168805	Lzh	"爱德华·龙内贝格"
#   Q141168786 Alice Ronneberg: set the ja label to "アリス・ロンネベルグ"
Q141168786	Lja	"アリス・ロンネベルグ"
#   set the zh label to "艾丽丝·龙内贝格"
Q141168786	Lzh	"艾丽丝·龙内贝格"
#   Q141168824 Ernest Anton Ronneberg: set the ja label to "アーネスト・アントン・ロンネベルグ"
Q141168824	Lja	"アーネスト・アントン・ロンネベルグ"
#   set the zh label to "欧内斯特·安东·龙内贝格"
Q141168824	Lzh	"欧内斯特·安东·龙内贝格"
#   Q141199992 Myrtle Lenora Tunheim: set the ja label to "マートル・レノーラ・トゥンヘイム"
Q141199992	Lja	"マートル・レノーラ・トゥンヘイム"
#   set the zh label to "默特尔·莱诺拉·通海姆"
Q141199992	Lzh	"默特尔·莱诺拉·通海姆"
#   Q141168788 Arne Garborg Tunheim: set the ja label to "アルネ・ガルボルグ・トゥンヘイム"
Q141168788	Lja	"アルネ・ガルボルグ・トゥンヘイム"
#   set the zh label to "阿尔内·加尔博格·通海姆"
Q141168788	Lzh	"阿尔内·加尔博格·通海姆"
#   Q141180396 Tollef Tollefson Tunheim: set the ja label to "トッレヴ・トレフソン・トゥンヘイム"
Q141180396	Lja	"トッレヴ・トレフソン・トゥンヘイム"
#   set the zh label to "托勒夫·托勒夫松·通海姆"
Q141180396	Lzh	"托勒夫·托勒夫松·通海姆"
#   Q141168794 Betsy Jacobson: set the ja label to "ベッツィ・ヤコブソン"
Q141168794	Lja	"ベッツィ・ヤコブソン"
#   set the zh label to "贝齐·雅各布松"
Q141168794	Lzh	"贝齐·雅各布松"
#   Q141199833 Bertha Ingeborg Moen: P40 child = Q141199976 Mona Beth Tunheim
Q141199833	P40	Q141199976	S2600	"6000000039507595739"
#   Q141200084 Selma Johanna Horton: P40 child = Q141199966 Mildred Lorraine Tunheim
Q141200084	P40	Q141199966	S2600	"6000000039510366865"
#   Q141189101 Samuel Tunheim: set the ja label to "サムエル・トゥンヘイム"
Q141189101	Lja	"サムエル・トゥンヘイム"
#   set the zh label to "萨穆埃尔·通海姆"
Q141189101	Lzh	"萨穆埃尔·通海姆"
#   Q141199836 Florence June Williams: P40 child = Q141200047 NN Private
Q141199836	P40	Q141200047	S2600	"6000000039511001067"
#   Q141200083 Sara NN: P40 child = Q141200604 Anna Nilsdotter
Q141200083	P40	Q141200604	S2600	"6000000059888596942"
#   P26 spouse = Q141200016 Nils Andersson
Q141200083	P26	Q141200016	S2600	"6000000059888596942"
#   Q141199918 Kirsten Hansdatter Låge-Håland: P26 spouse = Q141200127 Ådne Hansen Store Oma
Q141199918	P26	Q141200127	S2600	"6000000087451897836"
#   Q141199976 Mona Beth Tunheim: P25 mother = Q141199833 Bertha Ingeborg Moen
Q141199976	P25	Q141199833	S2600	"6000000162536870947"
#   Q141199966 Mildred Lorraine Tunheim: P25 mother = Q141200084 Selma Johanna Horton
Q141199966	P25	Q141200084	S2600	"6000000180009386839"
#   Q141200047 NN Private: P25 mother = Q141199836 Florence June Williams
Q141200047	P25	Q141199836	S2600	"6000000180039903952"
#   Q141189062 Cecilie Jonsdatter: set the ja label to "セシリエ・ヨンスダッテル"
Q141189062	Lja	"セシリエ・ヨンスダッテル"
#   set the zh label to "塞西莉厄·永斯达特"
Q141189062	Lzh	"塞西莉厄·永斯达特"
#   Q141189080 Lave: set the ja label to "ラーヴェ"
Q141189080	Lja	"ラーヴェ"
#   set the zh label to "拉弗"
Q141189080	Lzh	"拉弗"
#   Q141189078 Lars Kristiansen Sør-Reime: set the ja label to "ラーシュ・クリスティアンセン・セール・レイメ"
Q141189078	Lja	"ラーシュ・クリスティアンセン・セール・レイメ"
#   set the zh label to "拉尔斯·克里斯蒂安森·瑟尔·雷梅"
Q141189078	Lzh	"拉尔斯·克里斯蒂安森·瑟尔·雷梅"
#   Q141200127 Ådne Hansen Store Oma: P26 spouse = Q141199918 Kirsten Hansdatter Låge-Håland
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

