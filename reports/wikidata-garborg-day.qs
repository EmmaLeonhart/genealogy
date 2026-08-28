# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Andreas Olai"
LAST	Len	"Andreas Olai"
#   set the mul label to "Andreas Olai"
LAST	Lmul	"Andreas Olai"
#   add a mul alias "Andreas Olofsson"
LAST	Amul	"Andreas Olofsson"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000004334566448 Andreas Olofsson
LAST	P2600	"6000000004334566448"
#   P569 date of birth = +1512-03-03T00:00:00Z/11
LAST	P569	+1512-03-03T00:00:00Z/11	S2600	"6000000004334566448"
#   P570 date of death = +1569-03-03T00:00:00Z/11
LAST	P570	+1569-03-03T00:00:00Z/11	S2600	"6000000004334566448"
#   P40 child = Q141180409 Magdalena Andersdotter Bure
LAST	P40	Q141180409	S2600	"6000000004334566448"
#   Q141180409 Magdalena Andersdotter Bure: P22 father = the item just created
Q141180409	P22	LAST	S2600	"6000000004334566448"
#   the item just created: P1449 nickname = en:"Anders Olofsson"
LAST	P1449	en:"Anders Olofsson"
#   add a mul alias "Anders Olofsson Olai"
LAST	Amul	"Anders Olofsson Olai"

# create a new item
CREATE
#   set the en label to "Ane Marie Helgesdatter Bø"
LAST	Len	"Ane Marie Helgesdatter Bø"
#   set the mul label to "Ane Marie Helgesdatter Bø"
LAST	Lmul	"Ane Marie Helgesdatter Bø"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000007896103690 Ane Marie Helgesdatter Bø
LAST	P2600	"6000000007896103690"
#   P569 date of birth = +1787-06-03T00:00:00Z/11
LAST	P569	+1787-06-03T00:00:00Z/11	S2600	"6000000007896103690"
#   P570 date of death = +1859-06-01T00:00:00Z/11
LAST	P570	+1859-06-01T00:00:00Z/11	S2600	"6000000007896103690"
#   P40 child = Q141189066 Helge Rasmusson Bø
LAST	P40	Q141189066	S2600	"6000000007896103690"
#   Q141189066 Helge Rasmusson Bø: P25 mother = the item just created
Q141189066	P25	LAST	S2600	"6000000007896103690"
#   the item just created: P735 given name = Q11958077 Ane, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q11958077	P1545	"1"	P7452	Q3409033
#   P735 given name = Q106674406 Marie, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q106674406	P1545	"2"	P3831	Q245025
#   P1449 nickname = en:"Anna Maria"
LAST	P1449	en:"Anna Maria"
#   add a mul alias "Anna Maria Bø"
LAST	Amul	"Anna Maria Bø"

# create a new item
CREATE
#   set the en label to "Anna Andersdotter"
LAST	Len	"Anna Andersdotter"
#   set the mul label to "Anna Andersdotter"
LAST	Lmul	"Anna Andersdotter"
#   set the ja label to "アンナ・アンデシュドッテル"
LAST	Lja	"アンナ・アンデシュドッテル"
#   set the zh label to "安娜·安德斯多特"
LAST	Lzh	"安娜·安德斯多特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003125438035 Anna Andersdotter
LAST	P2600	"6000000003125438035"
#   P569 date of birth = +1515-00-00T00:00:00Z/9
LAST	P569	+1515-00-00T00:00:00Z/9	S2600	"6000000003125438035"
#   P570 date of death = +1583-04-30T00:00:00Z/11
LAST	P570	+1583-04-30T00:00:00Z/11	S2600	"6000000003125438035"
#   P40 child = Q141180409 Magdalena Andersdotter Bure
LAST	P40	Q141180409	S2600	"6000000003125438035"
#   Q141180409 Magdalena Andersdotter Bure: P25 mother = the item just created
Q141180409	P25	LAST	S2600	"6000000003125438035"

# create a new item
CREATE
#   the item just created: set the en label to "Anna Jönsdotter"
LAST	Len	"Anna Jönsdotter"
#   set the mul label to "Anna Jönsdotter"
LAST	Lmul	"Anna Jönsdotter"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000027470336201 Anna Jönsdotter
LAST	P2600	"6000000027470336201"
#   P570 date of death = +1602-08-20T00:00:00Z/11
LAST	P570	+1602-08-20T00:00:00Z/11	S2600	"6000000027470336201"
#   P40 child = Q141180410 Margareta Mårtensdotter Bång
LAST	P40	Q141180410	S2600	"6000000027470336201"
#   Q141180410 Margareta Mårtensdotter Bång: P25 mother = the item just created
Q141180410	P25	LAST	S2600	"6000000027470336201"

# create a new item
CREATE
#   the item just created: set the en label to "Anna Maria Samuelsdtr. Tunheim"
LAST	Len	"Anna Maria Samuelsdtr. Tunheim"
#   set the mul label to "Anna Maria Samuelsdtr. Tunheim"
LAST	Lmul	"Anna Maria Samuelsdtr. Tunheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000029983034410 Anna Maria Samuelsdtr. Tunheim
LAST	P2600	"6000000029983034410"
#   P569 date of birth = +1826-04-14T00:00:00Z/11
LAST	P569	+1826-04-14T00:00:00Z/11	S2600	"6000000029983034410"
#   P570 date of death = +1897-04-19T00:00:00Z/11
LAST	P570	+1897-04-19T00:00:00Z/11	S2600	"6000000029983034410"
#   P40 child = Q141189084 Martin Tollefson Tunheim
LAST	P40	Q141189084	S2600	"6000000029983034410"
#   P40 child = Q141180396 Tollef Tollefson Tunheim
LAST	P40	Q141180396	S2600	"6000000029983034410"
#   Q141189084 Martin Tollefson Tunheim: P25 mother = the item just created
Q141189084	P25	LAST	S2600	"6000000029983034410"
#   Q141180396 Tollef Tollefson Tunheim: P25 mother = the item just created
Q141180396	P25	LAST	S2600	"6000000029983034410"

# create a new item
CREATE
#   the item just created: set the en label to "Anna Rasmusdatter Grøtheim"
LAST	Len	"Anna Rasmusdatter Grøtheim"
#   set the mul label to "Anna Rasmusdatter Grøtheim"
LAST	Lmul	"Anna Rasmusdatter Grøtheim"
#   add a mul alias "Anna Rasmusdatter Årsland"
LAST	Amul	"Anna Rasmusdatter Årsland"
#   set the ja label to "アンナ・ラスムスダッテル・グレートヘイム"
LAST	Lja	"アンナ・ラスムスダッテル・グレートヘイム"
#   set the zh label to "安娜·拉斯穆斯达特·格勒特海姆"
LAST	Lzh	"安娜·拉斯穆斯达特·格勒特海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000008176804564 Anna Rasmusdatter Årsland
LAST	P2600	"6000000008176804564"
#   P569 date of birth = +1745-00-00T00:00:00Z/9
LAST	P569	+1745-00-00T00:00:00Z/9	S2600	"6000000008176804564"
#   P570 date of death = +1791-00-00T00:00:00Z/9
LAST	P570	+1791-00-00T00:00:00Z/9	S2600	"6000000008176804564"
#   P26 spouse = Q141189088 Ola Knutsen Garborg
LAST	P26	Q141189088	S2600	"6000000008176804564"
#   Q141189088 Ola Knutsen Garborg: P26 spouse = the item just created
Q141189088	P26	LAST	S2600	"6000000008176804564"
#   the item just created: add a mul alias "Anna Grøtheim"
LAST	Amul	"Anna Grøtheim"

# create a new item
CREATE
#   set the en label to "Bertha Ingeborg Tunheim"
LAST	Len	"Bertha Ingeborg Tunheim"
#   set the mul label to "Bertha Ingeborg Tunheim"
LAST	Lmul	"Bertha Ingeborg Tunheim"
#   add a mul alias "Bertha Ingeborg Moen"
LAST	Amul	"Bertha Ingeborg Moen"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000039507595739 Bertha Ingeborg Moen
LAST	P2600	"6000000039507595739"
#   P569 date of birth = +1915-03-17T00:00:00Z/11
LAST	P569	+1915-03-17T00:00:00Z/11	S2600	"6000000039507595739"
#   P570 date of death = +2014-10-21T00:00:00Z/11
LAST	P570	+2014-10-21T00:00:00Z/11	S2600	"6000000039507595739"
#   P26 spouse = Q141189074 Joseph Tunheim
LAST	P26	Q141189074	S2600	"6000000039507595739"
#   Q141189074 Joseph Tunheim: P26 spouse = the item just created
Q141189074	P26	LAST	S2600	"6000000039507595739"
#   the item just created: P735 given name = Q16420820 Bertha, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q16420820	P1545	"1"	P7452	Q3409033
#   P735 given name = Q656590 Ingeborg, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q656590	P1545	"2"	P3831	Q245025
#   P734 family name = Q16934183 Moen, qualified object of statement has role Q2507958 birth name
LAST	P734	Q16934183	P3831	Q2507958

# create a new item
CREATE
#   set the en label to "Florence June Tunheim Cosman"
LAST	Len	"Florence June Tunheim Cosman"
#   set the mul label to "Florence June Tunheim Cosman"
LAST	Lmul	"Florence June Tunheim Cosman"
#   add a mul alias "Florence June Williams"
LAST	Amul	"Florence June Williams"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000039511001067 Florence June Williams
LAST	P2600	"6000000039511001067"
#   P569 date of birth = +1916-07-19T00:00:00Z/11
LAST	P569	+1916-07-19T00:00:00Z/11	S2600	"6000000039511001067"
#   P570 date of death = +1997-01-03T00:00:00Z/11
LAST	P570	+1997-01-03T00:00:00Z/11	S2600	"6000000039511001067"
#   P26 spouse = Q141189109 Tollef Bud Tunheim
LAST	P26	Q141189109	S2600	"6000000039511001067"
#   Q141189109 Tollef Bud Tunheim: P26 spouse = the item just created
Q141189109	P26	LAST	S2600	"6000000039511001067"
#   the item just created: P735 given name = Q950780 Florence, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q950780	P1545	"1"	P7452	Q3409033
#   P734 family name = Q1688722 Williams, qualified object of statement has role Q2507958 birth name
LAST	P734	Q1688722	P3831	Q2507958
#   P1449 nickname = en:"Anderson"
LAST	P1449	en:"Anderson"
#   add a mul alias "Anderson Tunheim Cosman"
LAST	Amul	"Anderson Tunheim Cosman"

# create a new item
CREATE
#   set the en label to "Garborg"
LAST	Len	"Garborg"
#   set the mul label to "Garborg"
LAST	Lmul	"Garborg"
#   set the ja label to "ガルボルグ"
LAST	Lja	"ガルボルグ"
#   set the zh label to "加尔博格"
LAST	Lzh	"加尔博格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000021223635839 Garborg
LAST	P2600	"6000000021223635839"
#   P22 father = Q11959067 Arne Olaus Fjørtoft Garborg
LAST	P22	Q11959067	S2600	"6000000021223635839"
#   P25 mother = Q141168785 Aagot Nyvold
LAST	P25	Q141168785	S2600	"6000000021223635839"
#   Q11959067 Arne Olaus Fjørtoft Garborg: P40 child = the item just created
Q11959067	P40	LAST	S2600	"6000000021223635839"
#   Q141168785 Aagot Nyvold: P40 child = the item just created
Q141168785	P40	LAST	S2600	"6000000021223635839"

# create a new item
CREATE
#   the item just created: set the en label to "Gunnbjørn Toresson Tengs"
LAST	Len	"Gunnbjørn Toresson Tengs"
#   set the mul label to "Gunnbjørn Toresson Tengs"
LAST	Lmul	"Gunnbjørn Toresson Tengs"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000002463510938 Gunnbjørn Toresson Tengs
LAST	P2600	"6000000002463510938"
#   P569 date of birth = +1420-00-00T00:00:00Z/9
LAST	P569	+1420-00-00T00:00:00Z/9	S2600	"6000000002463510938"
#   P570 date of death = +1486-00-00T00:00:00Z/9
LAST	P570	+1486-00-00T00:00:00Z/9	S2600	"6000000002463510938"
#   P40 child = Q141198835 Bergitte Gunnbjørnsdatter Tengs
LAST	P40	Q141198835	S2600	"6000000002463510938"
#   Q141198835 Bergitte Gunnbjørnsdatter Tengs: P22 father = the item just created
Q141198835	P22	LAST	S2600	"6000000002463510938"
#   the item just created: P1449 nickname = en:"Tordsen"
LAST	P1449	en:"Tordsen"
#   add a mul alias "Tordsen Tengs"
LAST	Amul	"Tordsen Tengs"
#   add a mul alias "Gunnbjørn Tengs"
LAST	Amul	"Gunnbjørn Tengs"

# create a new item
CREATE
#   set the en label to "Guri Hansdatter Garborg"
LAST	Len	"Guri Hansdatter Garborg"
#   set the mul label to "Guri Hansdatter Garborg"
LAST	Lmul	"Guri Hansdatter Garborg"
#   add a mul alias "Guri Hansdatter Risa"
LAST	Amul	"Guri Hansdatter Risa"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000007896387570 Guri Hansdatter Risa
LAST	P2600	"6000000007896387570"
#   P569 date of birth = +1703-00-00T00:00:00Z/9
LAST	P569	+1703-00-00T00:00:00Z/9	S2600	"6000000007896387570"
#   P570 date of death = +1758-00-00T00:00:00Z/9
LAST	P570	+1758-00-00T00:00:00Z/9	S2600	"6000000007896387570"
#   P40 child = Q141189088 Ola Knutsen Garborg
LAST	P40	Q141189088	S2600	"6000000007896387570"
#   Q141189088 Ola Knutsen Garborg: P25 mother = the item just created
Q141189088	P25	LAST	S2600	"6000000007896387570"
#   the item just created: P735 given name = Q11973376 Guri
LAST	P735	Q11973376
#   P734 family name = Q30250555 Garborg, qualified object of statement has role Q28418670 married name
LAST	P734	Q30250555	P3831	Q28418670
#   add a mul alias "Guri Garborg"
LAST	Amul	"Guri Garborg"

# create a new item
CREATE
#   set the en label to "Helga Bjørnsdatter Tengs"
LAST	Len	"Helga Bjørnsdatter Tengs"
#   set the mul label to "Helga Bjørnsdatter Tengs"
LAST	Lmul	"Helga Bjørnsdatter Tengs"
#   add a mul alias "Helga Bjørnsdatter Bjørnsdatter"
LAST	Amul	"Helga Bjørnsdatter Bjørnsdatter"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000004697849241 Helga Bjørnsdatter Bjørnsdatter
LAST	P2600	"6000000004697849241"
#   P569 date of birth = +1420-00-00T00:00:00Z/9
LAST	P569	+1420-00-00T00:00:00Z/9	S2600	"6000000004697849241"
#   P570 date of death = +1500-00-00T00:00:00Z/9
LAST	P570	+1500-00-00T00:00:00Z/9	S2600	"6000000004697849241"
#   P40 child = Q141198835 Bergitte Gunnbjørnsdatter Tengs
LAST	P40	Q141198835	S2600	"6000000004697849241"
#   Q141198835 Bergitte Gunnbjørnsdatter Tengs: P25 mother = the item just created
Q141198835	P25	LAST	S2600	"6000000004697849241"
#   the item just created: P735 given name = Q1035107 Helga
LAST	P735	Q1035107
#   add a mul alias "Helga Tengs"
LAST	Amul	"Helga Tengs"

# create a new item
CREATE
#   set the en label to "Ingvold (Pinkie) Remmie"
LAST	Len	"Ingvold (Pinkie) Remmie"
#   set the mul label to "Ingvold (Pinkie) Remmie"
LAST	Lmul	"Ingvold (Pinkie) Remmie"
#   set the ja label to "イングヴォル・ピンキー・レミー"
LAST	Lja	"イングヴォル・ピンキー・レミー"
#   set the zh label to "英瓦尔·平基·雷米"
LAST	Lzh	"英瓦尔·平基·雷米"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000035698131765 Ingvold (Pinkie) Remmie
LAST	P2600	"6000000035698131765"
#   P569 date of birth = +1910-03-03T00:00:00Z/11
LAST	P569	+1910-03-03T00:00:00Z/11	S2600	"6000000035698131765"
#   P570 date of death = +1985-01-21T00:00:00Z/11
LAST	P570	+1985-01-21T00:00:00Z/11	S2600	"6000000035698131765"
#   P22 father = Q141198510 Tønnes Emil Enokson Rønneberg
LAST	P22	Q141198510	S2600	"6000000035698131765"
#   P25 mother = Q141162043 Inger Marie Mary Eivindsdatter Garborg
LAST	P25	Q141162043	S2600	"6000000035698131765"
#   Q141198510 Tønnes Emil Enokson Rønneberg: P40 child = the item just created
Q141198510	P40	LAST	S2600	"6000000035698131765"
#   Q141162043 Inger Marie Mary Eivindsdatter Garborg: P40 child = the item just created
Q141162043	P40	LAST	S2600	"6000000035698131765"
#   the item just created: P1449 nickname = en:"Pinkie"
LAST	P1449	en:"Pinkie"
#   add a mul alias "Pinkie Remmie"
LAST	Amul	"Pinkie Remmie"
#   add a mul alias "Ingvold Remmie"
LAST	Amul	"Ingvold Remmie"

# create a new item
CREATE
#   set the en label to "Ivar Sandsmark Garborg"
LAST	Len	"Ivar Sandsmark Garborg"
#   set the mul label to "Ivar Sandsmark Garborg"
LAST	Lmul	"Ivar Sandsmark Garborg"
#   add a mul alias "Ivar Garborg"
LAST	Amul	"Ivar Garborg"
#   set the ja label to "イーヴァル・サンスマルク・ガルボルグ"
LAST	Lja	"イーヴァル・サンスマルク・ガルボルグ"
#   set the zh label to "伊瓦尔·桑斯马克·加尔博格"
LAST	Lzh	"伊瓦尔·桑斯马克·加尔博格"
#   add a ja alias "イーヴァル・ガルボルグ"
LAST	Aja	"イーヴァル・ガルボルグ"
#   add a zh alias "伊瓦尔·加尔博格"
LAST	Azh	"伊瓦尔·加尔博格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000006571784497 Ivar Garborg
LAST	P2600	"6000000006571784497"
#   P569 date of birth = +1884-12-05T00:00:00Z/11
LAST	P569	+1884-12-05T00:00:00Z/11	S2600	"6000000006571784497"
#   P570 date of death = +1937-12-06T00:00:00Z/11
LAST	P570	+1937-12-06T00:00:00Z/11	S2600	"6000000006571784497"
#   P22 father = Q141152614 Jon Eivindson Garborg
LAST	P22	Q141152614	S2600	"6000000006571784497"
#   P25 mother = Q141189104 Siri Kristine Ivarsdatter Sandsmark
LAST	P25	Q141189104	S2600	"6000000006571784497"
#   Q141152614 Jon Eivindson Garborg: P40 child = the item just created
Q141152614	P40	LAST	S2600	"6000000006571784497"
#   Q141189104 Siri Kristine Ivarsdatter Sandsmark: P40 child = the item just created
Q141189104	P40	LAST	S2600	"6000000006571784497"
#   the item just created: P735 given name = Q127069 Ivar
LAST	P735	Q127069
#   P734 family name = Q30250555 Garborg, qualified object of statement has role Q2507958 birth name
LAST	P734	Q30250555	P3831	Q2507958
#   P734 family name = Q30250555 Garborg
LAST	P734	Q30250555

# create a new item
CREATE
#   set the en label to "Ivar Valheim"
LAST	Len	"Ivar Valheim"
#   set the mul label to "Ivar Valheim"
LAST	Lmul	"Ivar Valheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000002452595429 Ivar Valheim
LAST	P2600	"6000000002452595429"
#   P735 given name = Q127069 Ivar
LAST	P735	Q127069

# create a new item
CREATE
#   set the en label to "Jon Olsen Heigre"
LAST	Len	"Jon Olsen Heigre"
#   set the mul label to "Jon Olsen Heigre"
LAST	Lmul	"Jon Olsen Heigre"
#   set the ja label to "ヨン・オルセン・ヘイグレ"
LAST	Lja	"ヨン・オルセン・ヘイグレ"
#   set the zh label to "永·奥尔森·海格勒"
LAST	Lzh	"永·奥尔森·海格勒"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003491986736 Jon Olsen Heigre
LAST	P2600	"6000000003491986736"
#   P569 date of birth = +1804-00-00T00:00:00Z/9
LAST	P569	+1804-00-00T00:00:00Z/9	S2600	"6000000003491986736"
#   P570 date of death = +1850-02-14T00:00:00Z/11
LAST	P570	+1850-02-14T00:00:00Z/11	S2600	"6000000003491986736"
#   P40 child = Q141168957 Jonas Jonson Heigre
LAST	P40	Q141168957	S2600	"6000000003491986736"
#   Q141168957 Jonas Jonson Heigre: P22 father = the item just created
Q141168957	P22	LAST	S2600	"6000000003491986736"
#   the item just created: P735 given name = Q13501137 Jon
LAST	P735	Q13501137

# create a new item
CREATE
#   set the en label to "Jon Tollakson Aukland IV"
LAST	Len	"Jon Tollakson Aukland IV"
#   set the mul label to "Jon Tollakson Aukland IV"
LAST	Lmul	"Jon Tollakson Aukland IV"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000002391120029 Jon Tollakson Aukland IV
LAST	P2600	"6000000002391120029"
#   P569 date of birth = +1486-00-00T00:00:00Z/9
LAST	P569	+1486-00-00T00:00:00Z/9	S2600	"6000000002391120029"
#   P570 date of death = +1565-00-00T00:00:00Z/9
LAST	P570	+1565-00-00T00:00:00Z/9	S2600	"6000000002391120029"
#   P26 spouse = Q141198835 Bergitte Gunnbjørnsdatter Tengs
LAST	P26	Q141198835	S2600	"6000000002391120029"
#   P40 child = Q141198834 Gunnbjørn Jonson Aukland
LAST	P40	Q141198834	S2600	"6000000002391120029"
#   Q141198835 Bergitte Gunnbjørnsdatter Tengs: P26 spouse = the item just created
Q141198835	P26	LAST	S2600	"6000000002391120029"
#   Q141198834 Gunnbjørn Jonson Aukland: P22 father = the item just created
Q141198834	P22	LAST	S2600	"6000000002391120029"
#   the item just created: P735 given name = Q13501137 Jon
LAST	P735	Q13501137
#   P734 family name = Q4821650 Aukland
LAST	P734	Q4821650

# create a new item
CREATE
#   set the en label to "Karen Sophie Pedersdatter"
LAST	Len	"Karen Sophie Pedersdatter"
#   set the mul label to "Karen Sophie Pedersdatter"
LAST	Lmul	"Karen Sophie Pedersdatter"
#   set the ja label to "カーレン・ソフィー・ペーデシュダッテル"
LAST	Lja	"カーレン・ソフィー・ペーデシュダッテル"
#   set the zh label to "卡伦·索菲·佩德斯达特"
LAST	Lzh	"卡伦·索菲·佩德斯达特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000021137401277 Karen Sophie Pedersdatter
LAST	P2600	"6000000021137401277"
#   P40 child = Q141178201 Marie Petrine Simensdatter Bergersen
LAST	P40	Q141178201	S2600	"6000000021137401277"
#   Q141178201 Marie Petrine Simensdatter Bergersen: P25 mother = the item just created
Q141178201	P25	LAST	S2600	"6000000021137401277"
#   the item just created: P735 given name = Q14942517 Sophie, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q14942517	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Kirsten Hansdatter Grøtheim"
LAST	Len	"Kirsten Hansdatter Grøtheim"
#   set the mul label to "Kirsten Hansdatter Grøtheim"
LAST	Lmul	"Kirsten Hansdatter Grøtheim"
#   add a mul alias "Kirsten Hansdatter Låge-Håland"
LAST	Amul	"Kirsten Hansdatter Låge-Håland"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000087451897836 Kirsten Hansdatter Låge-Håland
LAST	P2600	"6000000087451897836"
#   P569 date of birth = +1699-00-00T00:00:00Z/9
LAST	P569	+1699-00-00T00:00:00Z/9	S2600	"6000000087451897836"
#   P570 date of death = +1750-10-12T00:00:00Z/11
LAST	P570	+1750-10-12T00:00:00Z/11	S2600	"6000000087451897836"
#   P40 child = Q141189069 Ingeborg Ådnesdatter Grøtheim
LAST	P40	Q141189069	S2600	"6000000087451897836"
#   Q141189069 Ingeborg Ådnesdatter Grøtheim: P25 mother = the item just created
Q141189069	P25	LAST	S2600	"6000000087451897836"
#   the item just created: P735 given name = Q256744 Kirsten
LAST	P735	Q256744
#   add a mul alias "Kirsten Grøtheim"
LAST	Amul	"Kirsten Grøtheim"

# create a new item
CREATE
#   set the en label to "Knut Elvindson Garborg"
LAST	Len	"Knut Elvindson Garborg"
#   set the mul label to "Knut Elvindson Garborg"
LAST	Lmul	"Knut Elvindson Garborg"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000007896295466 Knut Elvindson Garborg
LAST	P2600	"6000000007896295466"
#   P569 date of birth = +1693-00-00T00:00:00Z/9
LAST	P569	+1693-00-00T00:00:00Z/9	S2600	"6000000007896295466"
#   P570 date of death = +1749-00-00T00:00:00Z/9
LAST	P570	+1749-00-00T00:00:00Z/9	S2600	"6000000007896295466"
#   P40 child = Q141189088 Ola Knutsen Garborg
LAST	P40	Q141189088	S2600	"6000000007896295466"
#   Q141189088 Ola Knutsen Garborg: P22 father = the item just created
Q141189088	P22	LAST	S2600	"6000000007896295466"
#   the item just created: P735 given name = Q943881 Knut
LAST	P735	Q943881
#   P734 family name = Q30250555 Garborg
LAST	P734	Q30250555

# create a new item
CREATE
#   set the en label to "Knut Olsen Gudmestad"
LAST	Len	"Knut Olsen Gudmestad"
#   set the mul label to "Knut Olsen Gudmestad"
LAST	Lmul	"Knut Olsen Gudmestad"
#   add a mul alias "Knut Olsen Grøtheim"
LAST	Amul	"Knut Olsen Grøtheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000019668338861 Knut Olsen Grøtheim
LAST	P2600	"6000000019668338861"
#   P569 date of birth = +1774-00-00T00:00:00Z/9
LAST	P569	+1774-00-00T00:00:00Z/9	S2600	"6000000019668338861"
#   P570 date of death = +1850-05-02T00:00:00Z/11
LAST	P570	+1850-05-02T00:00:00Z/11	S2600	"6000000019668338861"
#   P22 father = Q141189088 Ola Knutsen Garborg
LAST	P22	Q141189088	S2600	"6000000019668338861"
#   P25 mother = Q141189069 Ingeborg Ådnesdatter Grøtheim
LAST	P25	Q141189069	S2600	"6000000019668338861"
#   Q141189088 Ola Knutsen Garborg: P40 child = the item just created
Q141189088	P40	LAST	S2600	"6000000019668338861"
#   Q141189069 Ingeborg Ådnesdatter Grøtheim: P40 child = the item just created
Q141189069	P40	LAST	S2600	"6000000019668338861"
#   the item just created: P735 given name = Q943881 Knut
LAST	P735	Q943881
#   add a mul alias "Knut Gudmestad"
LAST	Amul	"Knut Gudmestad"

# create a new item
CREATE
#   set the en label to "Maren Halvorsdatter Øksnevad"
LAST	Len	"Maren Halvorsdatter Øksnevad"
#   set the mul label to "Maren Halvorsdatter Øksnevad"
LAST	Lmul	"Maren Halvorsdatter Øksnevad"
#   add a mul alias "Maren Halvorsdatter Storhaug"
LAST	Amul	"Maren Halvorsdatter Storhaug"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005607155237 Maren Halvorsdatter Storhaug
LAST	P2600	"6000000005607155237"
#   P569 date of birth = +1766-00-00T00:00:00Z/9
LAST	P569	+1766-00-00T00:00:00Z/9	S2600	"6000000005607155237"
#   P570 date of death = +1843-06-08T00:00:00Z/11
LAST	P570	+1843-06-08T00:00:00Z/11	S2600	"6000000005607155237"
#   P40 child = Q141178202 Stine Persdatter Øksnevad
LAST	P40	Q141178202	S2600	"6000000005607155237"
#   Q141178202 Stine Persdatter Øksnevad: P25 mother = the item just created
Q141178202	P25	LAST	S2600	"6000000005607155237"
#   the item just created: P735 given name = Q1666203 Maren
LAST	P735	Q1666203
#   P734 family name = Q27892826 Storhaug, qualified object of statement has role Q2507958 birth name
LAST	P734	Q27892826	P3831	Q2507958
#   P734 family name = Q30583490 Øksnevad, qualified object of statement has role Q28418670 married name
LAST	P734	Q30583490	P3831	Q28418670
#   P1449 nickname = en:"Mari Halvorsdatter Øksnevad"
LAST	P1449	en:"Mari Halvorsdatter Øksnevad"
#   add a mul alias "Mari Halvorsdatter Øksnevad Øksnevad"
LAST	Amul	"Mari Halvorsdatter Øksnevad Øksnevad"
#   add a mul alias "Maren Øksnevad"
LAST	Amul	"Maren Øksnevad"

# create a new item
CREATE
#   set the en label to "Marie Garborg"
LAST	Len	"Marie Garborg"
#   set the mul label to "Marie Garborg"
LAST	Lmul	"Marie Garborg"
#   add a mul alias "Marie Tverdahl"
LAST	Amul	"Marie Tverdahl"
#   set the ja label to "マリー・ガルボルグ"
LAST	Lja	"マリー・ガルボルグ"
#   set the zh label to "玛丽·加尔博格"
LAST	Lzh	"玛丽·加尔博格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000177204223824 Marie Tverdahl
LAST	P2600	"6000000177204223824"
#   P569 date of birth = +1925-01-07T00:00:00Z/11
LAST	P569	+1925-01-07T00:00:00Z/11	S2600	"6000000177204223824"
#   P570 date of death = +2013-11-28T00:00:00Z/11
LAST	P570	+2013-11-28T00:00:00Z/11	S2600	"6000000177204223824"
#   P26 spouse = Q141168827 Hans Eivind Garborg
LAST	P26	Q141168827	S2600	"6000000177204223824"
#   Q141168827 Hans Eivind Garborg: P26 spouse = the item just created
Q141168827	P26	LAST	S2600	"6000000177204223824"
#   the item just created: P735 given name = Q106674406 Marie
LAST	P735	Q106674406
#   P734 family name = Q30250555 Garborg, qualified object of statement has role Q28418670 married name
LAST	P734	Q30250555	P3831	Q28418670
#   P1449 nickname = en:"lill"
LAST	P1449	en:"lill"
#   add a mul alias "lill Garborg"
LAST	Amul	"lill Garborg"

# create a new item
CREATE
#   set the en label to "Martinus Johannis"
LAST	Len	"Martinus Johannis"
#   set the mul label to "Martinus Johannis"
LAST	Lmul	"Martinus Johannis"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000006828782200 Martinus Johannis
LAST	P2600	"6000000006828782200"
#   P570 date of death = +1603-01-15T00:00:00Z/11
LAST	P570	+1603-01-15T00:00:00Z/11	S2600	"6000000006828782200"
#   P40 child = Q141180410 Margareta Mårtensdotter Bång
LAST	P40	Q141180410	S2600	"6000000006828782200"
#   Q141180410 Margareta Mårtensdotter Bång: P22 father = the item just created
Q141180410	P22	LAST	S2600	"6000000006828782200"
#   the item just created: P735 given name = Q17520926 Martinus
LAST	P735	Q17520926
#   P1449 nickname = en:"Martinus Johannis"
LAST	P1449	en:"Martinus Johannis"
#   add a mul alias "Martinus Johannis Johannis"
LAST	Amul	"Martinus Johannis Johannis"

# create a new item
CREATE
#   set the en label to "Mildred Lorraine Schantzen"
LAST	Len	"Mildred Lorraine Schantzen"
#   set the mul label to "Mildred Lorraine Schantzen"
LAST	Lmul	"Mildred Lorraine Schantzen"
#   add a mul alias "Mildred Lorraine Tunheim"
LAST	Amul	"Mildred Lorraine Tunheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000180009386839 Mildred Lorraine Tunheim
LAST	P2600	"6000000180009386839"
#   P569 date of birth = +1931-04-05T00:00:00Z/11
LAST	P569	+1931-04-05T00:00:00Z/11	S2600	"6000000180009386839"
#   P570 date of death = +1984-03-17T00:00:00Z/11
LAST	P570	+1984-03-17T00:00:00Z/11	S2600	"6000000180009386839"
#   P22 father = Q141189049 Alfred Tunheim
LAST	P22	Q141189049	S2600	"6000000180009386839"
#   Q141189049 Alfred Tunheim: P40 child = the item just created
Q141189049	P40	LAST	S2600	"6000000180009386839"
#   the item just created: P735 given name = Q11287301 Mildred, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q11287301	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1158295 Lorraine, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q1158295	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Mona Beth Carney Castro"
LAST	Len	"Mona Beth Carney Castro"
#   set the mul label to "Mona Beth Carney Castro"
LAST	Lmul	"Mona Beth Carney Castro"
#   add a mul alias "Mona Beth Tunheim"
LAST	Amul	"Mona Beth Tunheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000162536870947 Mona Beth Tunheim
LAST	P2600	"6000000162536870947"
#   P569 date of birth = +1946-07-07T00:00:00Z/11
LAST	P569	+1946-07-07T00:00:00Z/11	S2600	"6000000162536870947"
#   P570 date of death = +1977-03-23T00:00:00Z/11
LAST	P570	+1977-03-23T00:00:00Z/11	S2600	"6000000162536870947"
#   P22 father = Q141189074 Joseph Tunheim
LAST	P22	Q141189074	S2600	"6000000162536870947"
#   Q141189074 Joseph Tunheim: P40 child = the item just created
Q141189074	P40	LAST	S2600	"6000000162536870947"
#   the item just created: P735 given name = Q2419834 Mona, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q2419834	P1545	"1"	P7452	Q3409033
#   P735 given name = Q14639649 Beth, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q14639649	P1545	"2"	P3831	Q245025
#   P734 family name = Q1049855 Castro, qualified object of statement has role Q28418670 married name
LAST	P734	Q1049855	P3831	Q28418670

# create a new item
CREATE
#   set the en label to "Myrtle Lenora Tunheim"
LAST	Len	"Myrtle Lenora Tunheim"
#   set the mul label to "Myrtle Lenora Tunheim"
LAST	Lmul	"Myrtle Lenora Tunheim"
#   set the ja label to "マートル・レノーラ・トゥンヘイム"
LAST	Lja	"マートル・レノーラ・トゥンヘイム"
#   set the zh label to "默特尔·莱诺拉·通海姆"
LAST	Lzh	"默特尔·莱诺拉·通海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000037693663051 Myrtle Lenora Tunheim
LAST	P2600	"6000000037693663051"
#   P569 date of birth = +1908-07-08T00:00:00Z/11
LAST	P569	+1908-07-08T00:00:00Z/11	S2600	"6000000037693663051"
#   P570 date of death = +1921-09-28T00:00:00Z/11
LAST	P570	+1921-09-28T00:00:00Z/11	S2600	"6000000037693663051"
#   P22 father = Q141189084 Martin Tollefson Tunheim
LAST	P22	Q141189084	S2600	"6000000037693663051"
#   P25 mother = Q141162046 Ane Oline Lena Eivindsdatter Garborg
LAST	P25	Q141162046	S2600	"6000000037693663051"
#   Q141189084 Martin Tollefson Tunheim: P40 child = the item just created
Q141189084	P40	LAST	S2600	"6000000037693663051"
#   Q141162046 Ane Oline Lena Eivindsdatter Garborg: P40 child = the item just created
Q141162046	P40	LAST	S2600	"6000000037693663051"
#   the item just created: P735 given name = Q3858942 Myrtle, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q3858942	P1545	"1"	P7452	Q3409033
#   P735 given name = Q26944868 Lenora, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q26944868	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Nils Andersson"
LAST	Len	"Nils Andersson"
#   set the mul label to "Nils Andersson"
LAST	Lmul	"Nils Andersson"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000006127859612 Nils Andersson
LAST	P2600	"6000000006127859612"
#   P569 date of birth = +1557-03-05T00:00:00Z/11
LAST	P569	+1557-03-05T00:00:00Z/11	S2600	"6000000006127859612"
#   P570 date of death = +1598-00-00T00:00:00Z/9
LAST	P570	+1598-00-00T00:00:00Z/9	S2600	"6000000006127859612"
#   P735 given name = Q16423038 Nils
LAST	P735	Q16423038

# create a new item
CREATE
#   set the en label to "Ola Olsen Vaule"
LAST	Len	"Ola Olsen Vaule"
#   set the mul label to "Ola Olsen Vaule"
LAST	Lmul	"Ola Olsen Vaule"
#   add a mul alias "Ola Olsen Grøtheim"
LAST	Amul	"Ola Olsen Grøtheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000002989071216 Ola Olsen Grøtheim
LAST	P2600	"6000000002989071216"
#   P569 date of birth = +1786-00-00T00:00:00Z/9
LAST	P569	+1786-00-00T00:00:00Z/9	S2600	"6000000002989071216"
#   P570 date of death = +1864-03-28T00:00:00Z/11
LAST	P570	+1864-03-28T00:00:00Z/11	S2600	"6000000002989071216"
#   P22 father = Q141189088 Ola Knutsen Garborg
LAST	P22	Q141189088	S2600	"6000000002989071216"
#   Q141189088 Ola Knutsen Garborg: P40 child = the item just created
Q141189088	P40	LAST	S2600	"6000000002989071216"
#   the item just created: P735 given name = Q96675523 Ola
LAST	P735	Q96675523
#   add a mul alias "Ola Vaule"
LAST	Amul	"Ola Vaule"

# create a new item
CREATE
#   set the en label to "Per Jonson Øksnevad"
LAST	Len	"Per Jonson Øksnevad"
#   set the mul label to "Per Jonson Øksnevad"
LAST	Lmul	"Per Jonson Øksnevad"
#   add a mul alias "Per Jonson Grude"
LAST	Amul	"Per Jonson Grude"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005606907249 Per Jonson Grude
LAST	P2600	"6000000005606907249"
#   P569 date of birth = +1726-00-00T00:00:00Z/9
LAST	P569	+1726-00-00T00:00:00Z/9	S2600	"6000000005606907249"
#   P570 date of death = +1806-07-20T00:00:00Z/11
LAST	P570	+1806-07-20T00:00:00Z/11	S2600	"6000000005606907249"
#   P40 child = Q141178202 Stine Persdatter Øksnevad
LAST	P40	Q141178202	S2600	"6000000005606907249"
#   Q141178202 Stine Persdatter Øksnevad: P22 father = the item just created
Q141178202	P22	LAST	S2600	"6000000005606907249"
#   the item just created: P735 given name = Q13582800 Per
LAST	P735	Q13582800
#   P734 family name = Q30229687 Grude, qualified object of statement has role Q2507958 birth name
LAST	P734	Q30229687	P3831	Q2507958
#   P734 family name = Q30583490 Øksnevad
LAST	P734	Q30583490
#   add a mul alias "Per Øksnevad"
LAST	Amul	"Per Øksnevad"

# create a new item
CREATE
#   set the mul label to "NN"
LAST	Lmul	"NN"
#   set the ca label to "filla de Tollef Bud Tunheim"
LAST	Lca	"filla de Tollef Bud Tunheim"
#   set the da label to "datter af Tollef Bud Tunheim"
LAST	Lda	"datter af Tollef Bud Tunheim"
#   set the de label to "Tochter von Tollef Bud Tunheim"
LAST	Lde	"Tochter von Tollef Bud Tunheim"
#   set the en label to "daughter of Tollef Bud Tunheim"
LAST	Len	"daughter of Tollef Bud Tunheim"
#   set the es label to "hija de Tollef Bud Tunheim"
LAST	Les	"hija de Tollef Bud Tunheim"
#   set the it label to "figlia di Tollef Bud Tunheim"
LAST	Lit	"figlia di Tollef Bud Tunheim"
#   set the nb label to "datter av Tollef Bud Tunheim"
LAST	Lnb	"datter av Tollef Bud Tunheim"
#   set the nl label to "dochter van Tollef Bud Tunheim"
LAST	Lnl	"dochter van Tollef Bud Tunheim"
#   set the pt label to "filha de Tollef Bud Tunheim"
LAST	Lpt	"filha de Tollef Bud Tunheim"
#   set the sv label to "dotter till Tollef Bud Tunheim"
LAST	Lsv	"dotter till Tollef Bud Tunheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000180039903952 NN Private
LAST	P2600	"6000000180039903952"
#   P22 father = Q141189109 Tollef Bud Tunheim
LAST	P22	Q141189109	S2600	"6000000180039903952"
#   Q141189109 Tollef Bud Tunheim: P40 child = the item just created
Q141189109	P40	LAST	S2600	"6000000180039903952"

# create a new item
CREATE
#   the item just created: set the en label to "Rakel Jonsdatter Jonsdotter Vatne"
LAST	Len	"Rakel Jonsdatter Jonsdotter Vatne"
#   set the mul label to "Rakel Jonsdatter Jonsdotter Vatne"
LAST	Lmul	"Rakel Jonsdatter Jonsdotter Vatne"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003491986761 Rakel Jonsdatter Jonsdotter Vatne
LAST	P2600	"6000000003491986761"
#   P569 date of birth = +1810-00-00T00:00:00Z/9
LAST	P569	+1810-00-00T00:00:00Z/9	S2600	"6000000003491986761"
#   P570 date of death = +1871-01-29T00:00:00Z/11
LAST	P570	+1871-01-29T00:00:00Z/11	S2600	"6000000003491986761"
#   P40 child = Q141168957 Jonas Jonson Heigre
LAST	P40	Q141168957	S2600	"6000000003491986761"
#   Q141168957 Jonas Jonson Heigre: P25 mother = the item just created
Q141168957	P25	LAST	S2600	"6000000003491986761"
#   the item just created: P735 given name = Q16424094 Rakel
LAST	P735	Q16424094
#   P734 family name = Q30134985 Vatne, qualified object of statement has role Q28418670 married name
LAST	P734	Q30134985	P3831	Q28418670
#   add a mul alias "Rakel Vatne"
LAST	Amul	"Rakel Vatne"

# create a new item
CREATE
#   set the en label to "Rasmus Kjetilson Høle"
LAST	Len	"Rasmus Kjetilson Høle"
#   set the mul label to "Rasmus Kjetilson Høle"
LAST	Lmul	"Rasmus Kjetilson Høle"
#   add a mul alias "Rasmus Kjetilson Kjetilsen Høle"
LAST	Amul	"Rasmus Kjetilson Kjetilsen Høle"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003095034915 Rasmus Kjetilson Kjetilsen Høle
LAST	P2600	"6000000003095034915"
#   P569 date of birth = +1679-00-00T00:00:00Z/9
LAST	P569	+1679-00-00T00:00:00Z/9	S2600	"6000000003095034915"
#   P570 date of death = +1743-00-00T00:00:00Z/9
LAST	P570	+1743-00-00T00:00:00Z/9	S2600	"6000000003095034915"
#   P40 child = Q141180412 Marta Rasmusdatter Høle
LAST	P40	Q141180412	S2600	"6000000003095034915"
#   Q141180412 Marta Rasmusdatter Høle: P22 father = the item just created
Q141180412	P22	LAST	S2600	"6000000003095034915"
#   the item just created: P735 given name = Q1785744 Rasmus
LAST	P735	Q1785744
#   add a mul alias "Rasmus Høle"
LAST	Amul	"Rasmus Høle"

# create a new item
CREATE
#   set the en label to "Rasmus Olsen Bø"
LAST	Len	"Rasmus Olsen Bø"
#   set the mul label to "Rasmus Olsen Bø"
LAST	Lmul	"Rasmus Olsen Bø"
#   add a mul alias "Rasmus Olsen Grøtheim"
LAST	Amul	"Rasmus Olsen Grøtheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000007744183945 Rasmus Olsen Grøtheim
LAST	P2600	"6000000007744183945"
#   P569 date of birth = +1780-00-00T00:00:00Z/9
LAST	P569	+1780-00-00T00:00:00Z/9	S2600	"6000000007744183945"
#   P570 date of death = +1849-04-26T00:00:00Z/11
LAST	P570	+1849-04-26T00:00:00Z/11	S2600	"6000000007744183945"
#   P22 father = Q141189088 Ola Knutsen Garborg
LAST	P22	Q141189088	S2600	"6000000007744183945"
#   P40 child = Q141189066 Helge Rasmusson Bø
LAST	P40	Q141189066	S2600	"6000000007744183945"
#   Q141189088 Ola Knutsen Garborg: P40 child = the item just created
Q141189088	P40	LAST	S2600	"6000000007744183945"
#   Q141189066 Helge Rasmusson Bø: P22 father = the item just created
Q141189066	P22	LAST	S2600	"6000000007744183945"
#   the item just created: P735 given name = Q1785744 Rasmus
LAST	P735	Q1785744
#   add a mul alias "Rasmus Bø"
LAST	Amul	"Rasmus Bø"

# create a new item
CREATE
#   set the en label to "Sara"
LAST	Len	"Sara"
#   set the mul label to "Sara"
LAST	Lmul	"Sara"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000059888596942 Sara
LAST	P2600	"6000000059888596942"
#   P735 given name = Q833345 Sara
LAST	P735	Q833345
#   add a mul alias "Sara NN"
LAST	Amul	"Sara NN"

# create a new item
CREATE
#   set the en label to "Selma Johanna Tunheim"
LAST	Len	"Selma Johanna Tunheim"
#   set the mul label to "Selma Johanna Tunheim"
LAST	Lmul	"Selma Johanna Tunheim"
#   add a mul alias "Selma Johanna Horton"
LAST	Amul	"Selma Johanna Horton"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000039510366865 Selma Johanna Horton
LAST	P2600	"6000000039510366865"
#   P569 date of birth = +1910-02-11T00:00:00Z/11
LAST	P569	+1910-02-11T00:00:00Z/11	S2600	"6000000039510366865"
#   P570 date of death = +1969-05-29T00:00:00Z/11
LAST	P570	+1969-05-29T00:00:00Z/11	S2600	"6000000039510366865"
#   P26 spouse = Q141189049 Alfred Tunheim
LAST	P26	Q141189049	S2600	"6000000039510366865"
#   Q141189049 Alfred Tunheim: P26 spouse = the item just created
Q141189049	P26	LAST	S2600	"6000000039510366865"
#   the item just created: P735 given name = Q713759 Selma, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q713759	P1545	"1"	P7452	Q3409033
#   P735 given name = Q4120836 Johanna, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q4120836	P1545	"2"	P3831	Q245025
#   P734 family name = Q16870893 Horton, qualified object of statement has role Q2507958 birth name
LAST	P734	Q16870893	P3831	Q2507958

# create a new item
CREATE
#   set the en label to "Siri Rasmusdtr. Erevik"
LAST	Len	"Siri Rasmusdtr. Erevik"
#   set the mul label to "Siri Rasmusdtr. Erevik"
LAST	Lmul	"Siri Rasmusdtr. Erevik"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003095172404 Siri Rasmusdtr. Erevik
LAST	P2600	"6000000003095172404"
#   P569 date of birth = +1688-00-00T00:00:00Z/9
LAST	P569	+1688-00-00T00:00:00Z/9	S2600	"6000000003095172404"
#   P570 date of death = +1744-00-00T00:00:00Z/9
LAST	P570	+1744-00-00T00:00:00Z/9	S2600	"6000000003095172404"
#   P40 child = Q141180412 Marta Rasmusdatter Høle
LAST	P40	Q141180412	S2600	"6000000003095172404"
#   Q141180412 Marta Rasmusdatter Høle: P25 mother = the item just created
Q141180412	P25	LAST	S2600	"6000000003095172404"
#   the item just created: P735 given name = Q1772342 Siri, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q1772342	P1545	"1"	P7452	Q3409033

# create a new item
CREATE
#   set the en label to "Sissel Jonsdatter Talje"
LAST	Len	"Sissel Jonsdatter Talje"
#   set the mul label to "Sissel Jonsdatter Talje"
LAST	Lmul	"Sissel Jonsdatter Talje"
#   add a mul alias "Sissel Jonsdatter Aukland"
LAST	Amul	"Sissel Jonsdatter Aukland"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003043806217 Sissel Jonsdatter Aukland
LAST	P2600	"6000000003043806217"
#   P569 date of birth = +1510-00-00T00:00:00Z/9
LAST	P569	+1510-00-00T00:00:00Z/9	S2600	"6000000003043806217"
#   P570 date of death = +1560-00-00T00:00:00Z/9
LAST	P570	+1560-00-00T00:00:00Z/9	S2600	"6000000003043806217"
#   P25 mother = Q141198835 Bergitte Gunnbjørnsdatter Tengs
LAST	P25	Q141198835	S2600	"6000000003043806217"
#   Q141198835 Bergitte Gunnbjørnsdatter Tengs: P40 child = the item just created
Q141198835	P40	LAST	S2600	"6000000003043806217"
#   the item just created: P735 given name = Q4571101 Sissel
LAST	P735	Q4571101
#   P734 family name = Q4821650 Aukland, qualified object of statement has role Q2507958 birth name
LAST	P734	Q4821650	P3831	Q2507958
#   P1449 nickname = en:"Sissela Jondtr Aukland."
LAST	P1449	en:"Sissela Jondtr Aukland."
#   add a mul alias "Sissela Jondtr Aukland. Talje"
LAST	Amul	"Sissela Jondtr Aukland. Talje"
#   add a mul alias "Sissel Talje"
LAST	Amul	"Sissel Talje"

# create a new item
CREATE
#   set the en label to "Sæbjørn Toresson Talgje"
LAST	Len	"Sæbjørn Toresson Talgje"
#   set the mul label to "Sæbjørn Toresson Talgje"
LAST	Lmul	"Sæbjørn Toresson Talgje"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000004213963966 Sæbjørn Toresson Talgje
LAST	P2600	"6000000004213963966"
#   P569 date of birth = +1510-00-00T00:00:00Z/9
LAST	P569	+1510-00-00T00:00:00Z/9	S2600	"6000000004213963966"
#   P570 date of death = +1578-00-00T00:00:00Z/9
LAST	P570	+1578-00-00T00:00:00Z/9	S2600	"6000000004213963966"
#   P735 given name = Q125281009 Sæbjørn
LAST	P735	Q125281009

# create a new item
CREATE
#   set the en label to "Tollef Pederson Tunheim"
LAST	Len	"Tollef Pederson Tunheim"
#   set the mul label to "Tollef Pederson Tunheim"
LAST	Lmul	"Tollef Pederson Tunheim"
#   add a mul alias "Tollef Pederson Hetland"
LAST	Amul	"Tollef Pederson Hetland"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000029983078557 Tollef Pederson Hetland
LAST	P2600	"6000000029983078557"
#   P569 date of birth = +1815-06-25T00:00:00Z/11
LAST	P569	+1815-06-25T00:00:00Z/11	S2600	"6000000029983078557"
#   P570 date of death = +1892-05-30T00:00:00Z/11
LAST	P570	+1892-05-30T00:00:00Z/11	S2600	"6000000029983078557"
#   P40 child = Q141189084 Martin Tollefson Tunheim
LAST	P40	Q141189084	S2600	"6000000029983078557"
#   P40 child = Q141180396 Tollef Tollefson Tunheim
LAST	P40	Q141180396	S2600	"6000000029983078557"
#   Q141189084 Martin Tollefson Tunheim: P22 father = the item just created
Q141189084	P22	LAST	S2600	"6000000029983078557"
#   Q141180396 Tollef Tollefson Tunheim: P22 father = the item just created
Q141180396	P22	LAST	S2600	"6000000029983078557"
#   the item just created: P735 given name = Q12006598 Tollef
LAST	P735	Q12006598
#   P734 family name = Q16870758 Hetland, qualified object of statement has role Q2507958 birth name
LAST	P734	Q16870758	P3831	Q2507958
#   add a mul alias "Tollef Tunheim"
LAST	Amul	"Tollef Tunheim"

# create a new item
CREATE
#   set the en label to "Ådne Hansen Grøtheim"
LAST	Len	"Ådne Hansen Grøtheim"
#   set the mul label to "Ådne Hansen Grøtheim"
LAST	Lmul	"Ådne Hansen Grøtheim"
#   add a mul alias "Ådne Hansen Store Oma"
LAST	Amul	"Ådne Hansen Store Oma"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000225229617898 Ådne Hansen Store Oma
LAST	P2600	"6000000225229617898"
#   P569 date of birth = +1710-00-00T00:00:00Z/9
LAST	P569	+1710-00-00T00:00:00Z/9	S2600	"6000000225229617898"
#   P570 date of death = +1770-00-00T00:00:00Z/9
LAST	P570	+1770-00-00T00:00:00Z/9	S2600	"6000000225229617898"
#   P40 child = Q141189069 Ingeborg Ådnesdatter Grøtheim
LAST	P40	Q141189069	S2600	"6000000225229617898"
#   Q141189069 Ingeborg Ådnesdatter Grøtheim: P22 father = the item just created
Q141189069	P22	LAST	S2600	"6000000225229617898"
#   the item just created: add a mul alias "Ådne Grøtheim"
LAST	Amul	"Ådne Grøtheim"

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
#   Q141198835 Bergitte Gunnbjørnsdatter Tengs: P40 child = Q141198834 Gunnbjørn Jonson Aukland
Q141198835	P40	Q141198834	S2600	"6000000002481819312"
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
#   P40 child = Q141198489 Sigrid Garborg
Q141189104	P40	Q141198489	S2600	"6000000002954315535"
#   set the ja label to "シーリ・クリスティーネ・イーヴァシュダッテル・サンスマルク"
Q141189104	Lja	"シーリ・クリスティーネ・イーヴァシュダッテル・サンスマルク"
#   set the zh label to "西丽·克丽丝汀·伊瓦斯达特·桑斯马克"
Q141189104	Lzh	"西丽·克丽丝汀·伊瓦斯达特·桑斯马克"
#   Q141198396 Erling Juel Wendt: P40 child = Q141198482 NN Private
Q141198396	P40	Q141198482	S2600	"6000000003002459585"
#   P26 spouse = Q141168784 Aagot Garborg
Q141198396	P26	Q141168784	S2600	"6000000003002459585"
#   P735 given name = Q472066 Erling, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141198396	P735	Q472066	P1545	"1"	P7452	Q3409033
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
#   P26 spouse = Q141198538 Gunnarsdatter Frafjord
Q141198503	P26	Q141198538	S2600	"6000000003095166856"
#   P735 given name = Q1548096 Tore
Q141198503	P735	Q1548096
#   Q141198401 Hedvig Svantepolks de Gdańsk of Danzig: P40 child = Q6197518 Svantepolk Knutsson Viby Skarsholmsätten
Q141198401	P40	Q6197518	S2600	"6000000003358192683"
#   P26 spouse = Q3743799 Knut Valdemarsson Duke of Estland, Blekinge and Lolland
Q141198401	P26	Q3743799	S2600	"6000000003358192683"
#   P735 given name = Q13648620 Hedvig, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141198401	P735	Q13648620	P1545	"1"	P7452	Q3409033
#   Q6197518 Svantepolk Knutsson Viby Skarsholmsätten: P26 spouse = Q141198377 Benedicta Sunesdotter Folkungaätten
Q6197518	P26	Q141198377	S2600	"6000000003418900347"
#   Q141168957 Jonas Jonson Heigre: set the ja label to "ヨナス・ヨンソン・ヘイグレ"
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
#   P3373 sibling = Q141189098 Rakel Jonasdatter Heigre
Q141178198	P3373	Q141189098	S2600	"6000000003491986956"
#   P3373 sibling = Q141189111 Tørres Jonasson Hegre
Q141178198	P3373	Q141189111	S2600	"6000000003491986956"
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
#   Q141198510 Tønnes Emil Enokson Rønneberg: P40 child = Q141168820 Eliza Ronneberg
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
#   Q141162043 Inger Marie Mary Eivindsdatter Garborg: P26 spouse = Q141198510 Tønnes Emil Enokson Rønneberg
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
#   set the ja label to "アーネ・オリーネ・レーナ・エイヴィンスダッテル・ガルボルグ"
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
#   Q141189066 Helge Rasmusson Bø: P40 child = Q141189099 Rasmus Helgesen Bø
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
#   Q141198370 Skårland: P40 child = Q141178200 Inger Kristoffersdatter
Q141198370	P40	Q141178200	S2600	"6000000003686206816"
#   P26 spouse = Q141198375 Astri Torchelsdatter Øvre Time
Q141198370	P26	Q141198375	S2600	"6000000003686206816"
#   Q141198375 Astri Torchelsdatter Øvre Time: P40 child = Q141178200 Inger Kristoffersdatter
Q141198375	P40	Q141178200	S2600	"6000000003731596731"
#   P26 spouse = Q141198370 Skårland
Q141198375	P26	Q141198370	S2600	"6000000003731596731"
#   P735 given name = Q30132931 Astri, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141198375	P735	Q30132931	P1545	"1"	P7452	Q3409033
#   Q141168955 Jon Samuelsen Raustad: P26 spouse = Q141178200 Inger Kristoffersdatter
Q141168955	P26	Q141178200	S2600	"6000000003732742137"
#   set the ja label to "ヨン・サムエルセン・ラウスタード"
Q141168955	Lja	"ヨン・サムエルセン・ラウスタード"
#   set the zh label to "永·萨穆埃尔森·劳斯塔"
Q141168955	Lzh	"永·萨穆埃尔森·劳斯塔"
#   Q633094 Johannes Tomasson: P26 spouse = Q141180410 Margareta Mårtensdotter Bång
Q633094	P26	Q141180410	S2600	"6000000004334763223"
#   set the zh label to "约翰内斯·托马松"
Q633094	Lzh	"约翰内斯·托马松"
#   Q141180413 Thomas Mattsson: set the ja label to "トーマス・マットソン"
Q141180413	Lja	"トーマス・マットソン"
#   set the zh label to "托马斯·马特松"
Q141180413	Lzh	"托马斯·马特松"
#   Q141178149 Anna Fartegnsdatter Seim: set the ja label to "アンナ・ファルテグンスダッテル・セイム"
Q141178149	Lja	"アンナ・ファルテグンスダッテル・セイム"
#   set the zh label to "安娜·法尔特格恩斯达特·塞姆"
Q141178149	Lzh	"安娜·法尔特格恩斯达特·塞姆"
#   Q3143008 Karen Hulda Bergersen: P25 mother = Q141178201 Marie Petrine Simensdatter Bergersen
Q3143008	P25	Q141178201	S2600	"6000000005606976813"
#   Q141198834 Gunnbjørn Jonson Aukland: P25 mother = Q141198835 Bergitte Gunnbjørnsdatter Tengs
Q141198834	P25	Q141198835	S2600	"6000000005607359959"
#   P40 child = Q141198832 Lars Gunnbjørnsen Mjølhus
Q141198834	P40	Q141198832	S2600	"6000000005607359959"
#   P734 family name = Q4821650 Aukland
Q141198834	P734	Q4821650
#   Q11959067 Arne Olaus Fjørtoft Garborg: set the ja label to "アルネ・オーラウス・フョルトフト・ガルボルグ"
Q11959067	Lja	"アルネ・オーラウス・フョルトフト・ガルボルグ"
#   set the zh label to "阿尔内·奥劳斯·夫约托夫特·加尔博格"
Q11959067	Lzh	"阿尔内·奥劳斯·夫约托夫特·加尔博格"
#   Q141168827 Hans Eivind Garborg: set the ja label to "ハンス・エイヴィン・ガルボルグ"
Q141168827	Lja	"ハンス・エイヴィン・ガルボルグ"
#   set the zh label to "汉斯·埃温·加尔博格"
Q141168827	Lzh	"汉斯·埃温·加尔博格"
#   Q141198832 Lars Gunnbjørnsen Mjølhus: P22 father = Q141198834 Gunnbjørn Jonson Aukland
Q141198832	P22	Q141198834	S2600	"6000000005608959093"
#   P40 child = Q141198831 Peder Larsen Mjølhus
Q141198832	P40	Q141198831	S2600	"6000000005608959093"
#   P735 given name = Q15635262 Lars
Q141198832	P735	Q15635262
#   Q141198538 Gunnarsdatter Frafjord: P40 child = Q141189097 Ragnhild Toresdatter Håland i Gjesdal
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
#   P25 mother = Q141198538 Gunnarsdatter Frafjord
Q141189097	P25	Q141198538	S2600	"6000000005609425396"
#   P26 spouse = Q141189079 Lars Tormodsen Mele
Q141189097	P26	Q141189079	S2600	"6000000005609425396"
#   Q141178200 Inger Kristoffersdatter: P22 father = Q141198370 Skårland
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
#   Q141180412 Marta Rasmusdatter Høle: P26 spouse = Q141180408 Jon Larsson Li
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
#   Q141180409 Magdalena Andersdotter Bure: set the ja label to "マグダレーナ・アンデシュドッテル・ブーレ"
Q141180409	Lja	"マグダレーナ・アンデシュドッテル・ブーレ"
#   set the zh label to "玛格达莱娜·安德斯多特·布雷"
Q141180409	Lzh	"玛格达莱娜·安德斯多特·布雷"
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
#   Q141189088 Ola Knutsen Garborg: P40 child = Q141198441 Kirsten Olsdatter Grøtheim
Q141189088	P40	Q141198441	S2600	"6000000007744588495"
#   P26 spouse = Q141189069 Ingeborg Ådnesdatter Grøtheim
Q141189088	P26	Q141189069	S2600	"6000000007744588495"
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
#   Q141189069 Ingeborg Ådnesdatter Grøtheim: P40 child = Q141198441 Kirsten Olsdatter Grøtheim
Q141189069	P40	Q141198441	S2600	"6000000008176802346"
#   P26 spouse = Q141189088 Ola Knutsen Garborg
Q141189069	P26	Q141189088	S2600	"6000000008176802346"
#   set the ja label to "インゲボルグ・オードネスダッテル・グレートヘイム"
Q141189069	Lja	"インゲボルグ・オードネスダッテル・グレートヘイム"
#   set the zh label to "英厄堡·奥德内斯达特·格勒特海姆"
Q141189069	Lzh	"英厄堡·奥德内斯达特·格勒特海姆"
#   Q141189108 Tillie Betsy Tunheim: set the ja label to "ティリー・ベッツィ・トゥンヘイム"
Q141189108	Lja	"ティリー・ベッツィ・トゥンヘイム"
#   set the zh label to "蒂莉·贝齐·通海姆"
Q141189108	Lzh	"蒂莉·贝齐·通海姆"
#   Q141178201 Marie Petrine Simensdatter Bergersen: P26 spouse = Q141198384 Carl Johan Edlund
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
#   Q141180410 Margareta Mårtensdotter Bång: P40 child = Q109266155 Magdalena Johansdotter Bure
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
#   Q141189084 Martin Tollefson Tunheim: P40 child = Q141198472 Olga E. Tunheim
Q141189084	P40	Q141198472	S2600	"6000000019384841547"
#   set the ja label to "マルティン・トレフソン・トゥンヘイム"
Q141189084	Lja	"マルティン・トレフソン・トゥンヘイム"
#   set the zh label to "马丁·托勒夫松·通海姆"
Q141189084	Lzh	"马丁·托勒夫松·通海姆"
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
#   Q138474188 Hans Syvertsen Nyvold: P26 spouse = Q141178197 Elisabeth Johannesen
Q138474188	P26	Q141178197	S2600	"6000000021197598122"
#   set the ja label to "ハンス・シーヴェシェン・ニーヴォル"
Q138474188	Lja	"ハンス・シーヴェシェン・ニーヴォル"
#   set the zh label to "汉斯·西韦特森·尼沃尔"
Q138474188	Lzh	"汉斯·西韦特森·尼沃尔"
#   Q141168785 Aagot Nyvold: P25 mother = Q141178197 Elisabeth Johannesen
Q141168785	P25	Q141178197	S2600	"6000000021197722738"
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
#   Q141189081 Lotte Birgithe Gustava Jonasdatter Heigre: set the ja label to "ロッテ・ビルギーテ・グスタヴァ・ヨナスダッテル・ヘイグレ"
Q141189081	Lja	"ロッテ・ビルギーテ・グスタヴァ・ヨナスダッテル・ヘイグレ"
#   set the zh label to "洛特·比尔吉特·古斯塔娃·约纳斯达特·海格勒"
Q141189081	Lzh	"洛特·比尔吉特·古斯塔娃·约纳斯达特·海格勒"
#   Q141180406 Ingeborg Gyntesdotter: set the ja label to "インゲボルグ・ギュンテスドッテル"
Q141180406	Lja	"インゲボルグ・ギュンテスドッテル"
#   set the zh label to "英厄堡·金特斯多特"
Q141180406	Lzh	"英厄堡·金特斯多特"
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
#   Q141168788 Arne Garborg Tunheim: set the ja label to "アルネ・ガルボルグ・トゥンヘイム"
Q141168788	Lja	"アルネ・ガルボルグ・トゥンヘイム"
#   set the zh label to "阿尔内·加尔博格·通海姆"
Q141168788	Lzh	"阿尔内·加尔博格·通海姆"
#   Q141180396 Tollef Tollefson Tunheim: set the ja label to "トッレヴ・トレフソン・トゥンヘイム"
Q141180396	Lja	"トッレヴ・トレフソン・トゥンヘイム"
#   set the zh label to "托勒夫·托勒夫松·通海姆"
Q141180396	Lzh	"托勒夫·托勒夫松·通海姆"
#   Q141168794 Betsy Jacobson: P22 father = Q141198428 Jacob Johannessen Aabø
Q141168794	P22	Q141198428	S2600	"6000000037737979829"
#   set the ja label to "ベッツィ・ヤコブソン"
Q141168794	Lja	"ベッツィ・ヤコブソン"
#   set the zh label to "贝齐·雅各布松"
Q141168794	Lzh	"贝齐·雅各布松"
#   Q141189101 Samuel Tunheim: set the ja label to "サムエル・トゥンヘイム"
Q141189101	Lja	"サムエル・トゥンヘイム"
#   set the zh label to "萨穆埃尔·通海姆"
Q141189101	Lzh	"萨穆埃尔·通海姆"
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
#   Q141198399 Eugene LeRoy Tunheim: P22 father = Q141168809 Edward Tunheim
Q141198399	P22	Q141168809	S2600	"6000000180028300872"
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

