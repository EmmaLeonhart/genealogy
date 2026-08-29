# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Anna Erevik"
LAST	Len	"Anna Erevik"
#   set the mul label to "Anna Erevik"
LAST	Lmul	"Anna Erevik"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000011623184503 Anna Erevik
LAST	P2600	"6000000011623184503"
#   P40 child = Q141200094 Siri Rasmusdtr. Erevik
LAST	P40	Q141200094	S2600	"6000000011623184503"
#   Q141200094 Siri Rasmusdtr. Erevik: P25 mother = the item just created
Q141200094	P25	LAST	S2600	"6000000011623184503"

# create a new item
CREATE
#   the item just created: set the en label to "Anna Jonesdatter Tøtland"
LAST	Len	"Anna Jonesdatter Tøtland"
#   set the mul label to "Anna Jonesdatter Tøtland"
LAST	Lmul	"Anna Jonesdatter Tøtland"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000001169317582 Anna Jonesdatter Tøtland
LAST	P2600	"6000000001169317582"
#   P569 date of birth = +1565-00-00T00:00:00Z/9
LAST	P569	+1565-00-00T00:00:00Z/9	S2600	"6000000001169317582"
#   P570 date of death = +1620-00-00T00:00:00Z/9
LAST	P570	+1620-00-00T00:00:00Z/9	S2600	"6000000001169317582"
#   P40 child = Q141205899 Bergitte Ivarsdatter Tjentland
LAST	P40	Q141205899	S2600	"6000000001169317582"
#   Q141205899 Bergitte Ivarsdatter Tjentland: P25 mother = the item just created
Q141205899	P25	LAST	S2600	"6000000001169317582"
#   the item just created: P1449 nickname = en:"Jonesdatter"
LAST	P1449	en:"Jonesdatter"
#   add a mul alias "Jonesdatter Tøtland"
LAST	Amul	"Jonesdatter Tøtland"

# create a new item
CREATE
#   set the en label to "Asbjørn Helgesen Bø"
LAST	Len	"Asbjørn Helgesen Bø"
#   set the mul label to "Asbjørn Helgesen Bø"
LAST	Lmul	"Asbjørn Helgesen Bø"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000222520395904 Asbjørn Helgesen Bø
LAST	P2600	"6000000222520395904"
#   P569 date of birth = +1789-00-00T00:00:00Z/9
LAST	P569	+1789-00-00T00:00:00Z/9	S2600	"6000000222520395904"
#   P570 date of death = +1789-08-26T00:00:00Z/11
LAST	P570	+1789-08-26T00:00:00Z/11	S2600	"6000000222520395904"
#   P25 mother = Q141205919 Malena Hansdatter Risa
LAST	P25	Q141205919	S2600	"6000000222520395904"
#   Q141205919 Malena Hansdatter Risa: P40 child = the item just created
Q141205919	P40	LAST	S2600	"6000000222520395904"
#   the item just created: P735 given name = Q721398 Asbjørn
LAST	P735	Q721398

# create a new item
CREATE
#   set the en label to "Astrid Larsdatter Mele"
LAST	Len	"Astrid Larsdatter Mele"
#   set the mul label to "Astrid Larsdatter Mele"
LAST	Lmul	"Astrid Larsdatter Mele"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005609418546 Astrid Larsdatter Mele
LAST	P2600	"6000000005609418546"
#   P569 date of birth = +1721-00-00T00:00:00Z/9
LAST	P569	+1721-00-00T00:00:00Z/9	S2600	"6000000005609418546"
#   P570 date of death = +1767-00-00T00:00:00Z/9
LAST	P570	+1767-00-00T00:00:00Z/9	S2600	"6000000005609418546"
#   P22 father = Q141189079 Lars Tormodsen Mele
LAST	P22	Q141189079	S2600	"6000000005609418546"
#   P25 mother = Q141189071 Joren Jonsdatter Espedal
LAST	P25	Q141189071	S2600	"6000000005609418546"
#   Q141189079 Lars Tormodsen Mele: P40 child = the item just created
Q141189079	P40	LAST	S2600	"6000000005609418546"
#   Q141189071 Joren Jonsdatter Espedal: P40 child = the item just created
Q141189071	P40	LAST	S2600	"6000000005609418546"
#   the item just created: P735 given name = Q167755 Astrid
LAST	P735	Q167755
#   add a mul alias "Astrid Mele"
LAST	Amul	"Astrid Mele"

# create a new item
CREATE
#   set the en label to "Berte Tørresdotter Austrått"
LAST	Len	"Berte Tørresdotter Austrått"
#   set the mul label to "Berte Tørresdotter Austrått"
LAST	Lmul	"Berte Tørresdotter Austrått"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000055365310131 Berte Tørresdotter Austrått
LAST	P2600	"6000000055365310131"
#   P569 date of birth = +1778-00-00T00:00:00Z/9
LAST	P569	+1778-00-00T00:00:00Z/9	S2600	"6000000055365310131"
#   P570 date of death = +1850-00-00T00:00:00Z/9
LAST	P570	+1850-00-00T00:00:00Z/9	S2600	"6000000055365310131"
#   P40 child = Q141200054 Rakel Jonsdatter Jonsdotter Vatne
LAST	P40	Q141200054	S2600	"6000000055365310131"
#   P40 child = Q141205921 Maria Jonsdatter Vatne
LAST	P40	Q141205921	S2600	"6000000055365310131"
#   Q141200054 Rakel Jonsdatter Jonsdotter Vatne: P25 mother = the item just created
Q141200054	P25	LAST	S2600	"6000000055365310131"
#   Q141205921 Maria Jonsdatter Vatne: P25 mother = the item just created
Q141205921	P25	LAST	S2600	"6000000055365310131"
#   the item just created: P735 given name = Q11960827 Berte
LAST	P735	Q11960827
#   add a mul alias "Berte Austrått"
LAST	Amul	"Berte Austrått"

# create a new item
CREATE
#   set the en label to "Cecilie Olsdatter Håland"
LAST	Len	"Cecilie Olsdatter Håland"
#   set the mul label to "Cecilie Olsdatter Håland"
LAST	Lmul	"Cecilie Olsdatter Håland"
#   add a mul alias "Cecilie Olsdatter Skiftun"
LAST	Amul	"Cecilie Olsdatter Skiftun"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000002482165558 Cecilie Olsdatter Skiftun
LAST	P2600	"6000000002482165558"
#   P569 date of birth = +1587-00-00T00:00:00Z/9
LAST	P569	+1587-00-00T00:00:00Z/9	S2600	"6000000002482165558"
#   P570 date of death = +1672-00-00T00:00:00Z/9
LAST	P570	+1672-00-00T00:00:00Z/9	S2600	"6000000002482165558"
#   P22 father = Q141205930 Olav Knutson Randa Randa
LAST	P22	Q141205930	S2600	"6000000002482165558"
#   P25 mother = Q141205909 Gudrun Sæbjørnsdatter Nord-Talgje
LAST	P25	Q141205909	S2600	"6000000002482165558"
#   Q141205930 Olav Knutson Randa Randa: P40 child = the item just created
Q141205930	P40	LAST	S2600	"6000000002482165558"
#   Q141205909 Gudrun Sæbjørnsdatter Nord-Talgje: P40 child = the item just created
Q141205909	P40	LAST	S2600	"6000000002482165558"
#   the item just created: P735 given name = Q16275183 Cecilie
LAST	P735	Q16275183
#   P5056 patronym or matronym = Q51885688 Olsdatter, qualified based on Q141205930 Olav Knutson Randa Randa
LAST	P5056	Q51885688	P144	Q141205930
#   add a mul alias "Cecilie Håland"
LAST	Amul	"Cecilie Håland"

# create a new item
CREATE
#   set the en label to "Dorothy Remmie"
LAST	Len	"Dorothy Remmie"
#   set the mul label to "Dorothy Remmie"
LAST	Lmul	"Dorothy Remmie"
#   add a mul alias "Dorothy Webb"
LAST	Amul	"Dorothy Webb"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000035698577979 Dorothy Webb
LAST	P2600	"6000000035698577979"
#   P26 spouse = Q141199868 Ingvold (Pinkie) Remmie
LAST	P26	Q141199868	S2600	"6000000035698577979"
#   Q141199868 Ingvold (Pinkie) Remmie: P26 spouse = the item just created
Q141199868	P26	LAST	S2600	"6000000035698577979"
#   the item just created: P735 given name = Q2647244 Dorothy
LAST	P735	Q2647244
#   P734 family name = Q2553367 Webb, qualified object of statement has role Q2507958 birth name
LAST	P734	Q2553367	P3831	Q2507958

# create a new item
CREATE
#   set the en label to "Dorthy (Rose Ann) Thelma Remmie"
LAST	Len	"Dorthy (Rose Ann) Thelma Remmie"
#   set the mul label to "Dorthy (Rose Ann) Thelma Remmie"
LAST	Lmul	"Dorthy (Rose Ann) Thelma Remmie"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000035698227660 Dorthy (Rose Ann) Thelma Remmie
LAST	P2600	"6000000035698227660"
#   P569 date of birth = +1923-12-14T00:00:00Z/11
LAST	P569	+1923-12-14T00:00:00Z/11	S2600	"6000000035698227660"
#   P570 date of death = +1997-03-19T00:00:00Z/11
LAST	P570	+1997-03-19T00:00:00Z/11	S2600	"6000000035698227660"
#   P22 father = Q141199868 Ingvold (Pinkie) Remmie
LAST	P22	Q141199868	S2600	"6000000035698227660"
#   Q141199868 Ingvold (Pinkie) Remmie: P40 child = the item just created
Q141199868	P40	LAST	S2600	"6000000035698227660"
#   the item just created: P735 given name = Q3523520 Thelma, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q3523520	P1545	"2"	P3831	Q245025
#   P1449 nickname = en:"Rose Ann"
LAST	P1449	en:"Rose Ann"
#   add a mul alias "Rose Ann Remmie"
LAST	Amul	"Rose Ann Remmie"

# create a new item
CREATE
#   set the en label to "Gard Toresson Talgje"
LAST	Len	"Gard Toresson Talgje"
#   set the mul label to "Gard Toresson Talgje"
LAST	Lmul	"Gard Toresson Talgje"
#   add a mul alias "Gard Toresson Garaa"
LAST	Amul	"Gard Toresson Garaa"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000002572728015 Gard Toresson Garaa
LAST	P2600	"6000000002572728015"
#   P569 date of birth = +1373-00-00T00:00:00Z/9
LAST	P569	+1373-00-00T00:00:00Z/9	S2600	"6000000002572728015"
#   P570 date of death = +1427-00-00T00:00:00Z/9
LAST	P570	+1427-00-00T00:00:00Z/9	S2600	"6000000002572728015"
#   P40 child = Q141205942 Tore Gardson Gardsson
LAST	P40	Q141205942	S2600	"6000000002572728015"
#   Q141205942 Tore Gardson Gardsson: P22 father = the item just created
Q141205942	P22	LAST	S2600	"6000000002572728015"
#   the item just created: P735 given name = Q12717105 Gard
LAST	P735	Q12717105
#   P1449 nickname = en:"Toresson"
LAST	P1449	en:"Toresson"
#   add a mul alias "Toresson Talgje"
LAST	Amul	"Toresson Talgje"
#   add a mul alias "Gard Talgje"
LAST	Amul	"Gard Talgje"

# create a new item
CREATE
#   set the en label to "Helge Asbjørnsen Bø"
LAST	Len	"Helge Asbjørnsen Bø"
#   set the mul label to "Helge Asbjørnsen Bø"
LAST	Lmul	"Helge Asbjørnsen Bø"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000008309908854 Helge Asbjørnsen Bø
LAST	P2600	"6000000008309908854"
#   P569 date of birth = +1755-00-00T00:00:00Z/9
LAST	P569	+1755-00-00T00:00:00Z/9	S2600	"6000000008309908854"
#   P570 date of death = +1823-06-07T00:00:00Z/11
LAST	P570	+1823-06-07T00:00:00Z/11	S2600	"6000000008309908854"
#   P26 spouse = Q141205919 Malena Hansdatter Risa
LAST	P26	Q141205919	S2600	"6000000008309908854"
#   P40 child = Q141199809 Ane Marie Helgesdatter Bø
LAST	P40	Q141199809	S2600	"6000000008309908854"
#   Q141205919 Malena Hansdatter Risa: P26 spouse = the item just created
Q141205919	P26	LAST	S2600	"6000000008309908854"
#   Q141199809 Ane Marie Helgesdatter Bø: P22 father = the item just created
Q141199809	P22	LAST	S2600	"6000000008309908854"
#   the item just created: P735 given name = Q1602361 Helge
LAST	P735	Q1602361

# create a new item
CREATE
#   set the en label to "Ingeborg Eriksdatter Time"
LAST	Len	"Ingeborg Eriksdatter Time"
#   set the mul label to "Ingeborg Eriksdatter Time"
LAST	Lmul	"Ingeborg Eriksdatter Time"
#   add a mul alias "Ingeborg Eriksdatter Netland"
LAST	Amul	"Ingeborg Eriksdatter Netland"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005607411844 Ingeborg Eriksdatter Netland
LAST	P2600	"6000000005607411844"
#   P569 date of birth = +1765-00-00T00:00:00Z/9
LAST	P569	+1765-00-00T00:00:00Z/9	S2600	"6000000005607411844"
#   P26 spouse = Q141205904 Erik Tollefson Fotland
LAST	P26	Q141205904	S2600	"6000000005607411844"
#   P40 child = Q141198393 Erik Erikson Time
LAST	P40	Q141198393	S2600	"6000000005607411844"
#   Q141205904 Erik Tollefson Fotland: P26 spouse = the item just created
Q141205904	P26	LAST	S2600	"6000000005607411844"
#   Q141198393 Erik Erikson Time: P25 mother = the item just created
Q141198393	P25	LAST	S2600	"6000000005607411844"
#   the item just created: P735 given name = Q656590 Ingeborg
LAST	P735	Q656590
#   add a mul alias "Ingeborg Time"
LAST	Amul	"Ingeborg Time"

# create a new item
CREATE
#   set the en label to "Ivar Toreson Tjentland"
LAST	Len	"Ivar Toreson Tjentland"
#   set the mul label to "Ivar Toreson Tjentland"
LAST	Lmul	"Ivar Toreson Tjentland"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000001169232790 Ivar Toreson Tjentland
LAST	P2600	"6000000001169232790"
#   P569 date of birth = +1560-00-00T00:00:00Z/9
LAST	P569	+1560-00-00T00:00:00Z/9	S2600	"6000000001169232790"
#   P570 date of death = +1640-00-00T00:00:00Z/9
LAST	P570	+1640-00-00T00:00:00Z/9	S2600	"6000000001169232790"
#   P40 child = Q141205899 Bergitte Ivarsdatter Tjentland
LAST	P40	Q141205899	S2600	"6000000001169232790"
#   Q141205899 Bergitte Ivarsdatter Tjentland: P22 father = the item just created
Q141205899	P22	LAST	S2600	"6000000001169232790"
#   the item just created: P735 given name = Q127069 Ivar
LAST	P735	Q127069

# create a new item
CREATE
#   set the en label to "Jon Hansson St. Vatne"
LAST	Len	"Jon Hansson St. Vatne"
#   set the mul label to "Jon Hansson St. Vatne"
LAST	Lmul	"Jon Hansson St. Vatne"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005608892743 Jon Hansson St. Vatne
LAST	P2600	"6000000005608892743"
#   P569 date of birth = +1773-00-00T00:00:00Z/9
LAST	P569	+1773-00-00T00:00:00Z/9	S2600	"6000000005608892743"
#   P570 date of death = +1828-00-00T00:00:00Z/9
LAST	P570	+1828-00-00T00:00:00Z/9	S2600	"6000000005608892743"
#   P40 child = Q141200054 Rakel Jonsdatter Jonsdotter Vatne
LAST	P40	Q141200054	S2600	"6000000005608892743"
#   P40 child = Q141205921 Maria Jonsdatter Vatne
LAST	P40	Q141205921	S2600	"6000000005608892743"
#   Q141200054 Rakel Jonsdatter Jonsdotter Vatne: P22 father = the item just created
Q141200054	P22	LAST	S2600	"6000000005608892743"
#   Q141205921 Maria Jonsdatter Vatne: P22 father = the item just created
Q141205921	P22	LAST	S2600	"6000000005608892743"
#   the item just created: P735 given name = Q13501137 Jon
LAST	P735	Q13501137
#   P734 family name = Q30134985 Vatne
LAST	P734	Q30134985
#   add a mul alias "Jon St. Vatne"
LAST	Amul	"Jon St. Vatne"

# create a new item
CREATE
#   set the en label to "Jon Jonsson"
LAST	Len	"Jon Jonsson"
#   set the mul label to "Jon Jonsson"
LAST	Lmul	"Jon Jonsson"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000013354249769 Jon Jonsson
LAST	P2600	"6000000013354249769"
#   P569 date of birth = +1580-00-00T00:00:00Z/9
LAST	P569	+1580-00-00T00:00:00Z/9	S2600	"6000000013354249769"
#   P570 date of death = +1636-00-00T00:00:00Z/9
LAST	P570	+1636-00-00T00:00:00Z/9	S2600	"6000000013354249769"
#   P40 child = Q141205928 NN Jonsdotter
LAST	P40	Q141205928	S2600	"6000000013354249769"
#   Q141205928 NN Jonsdotter: P22 father = the item just created
Q141205928	P22	LAST	S2600	"6000000013354249769"
#   the item just created: P735 given name = Q13501137 Jon
LAST	P735	Q13501137
#   P734 family name = Q21509276 Jonsson
LAST	P734	Q21509276

# create a new item
CREATE
#   set the en label to "Knut Johanson Håland"
LAST	Len	"Knut Johanson Håland"
#   set the mul label to "Knut Johanson Håland"
LAST	Lmul	"Knut Johanson Håland"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003376453205 Knut Johanson Håland
LAST	P2600	"6000000003376453205"
#   P569 date of birth = +1500-00-00T00:00:00Z/9
LAST	P569	+1500-00-00T00:00:00Z/9	S2600	"6000000003376453205"
#   P570 date of death = +1546-00-00T00:00:00Z/9
LAST	P570	+1546-00-00T00:00:00Z/9	S2600	"6000000003376453205"
#   P40 child = Q141205930 Olav Knutson Randa Randa
LAST	P40	Q141205930	S2600	"6000000003376453205"
#   Q141205930 Olav Knutson Randa Randa: P22 father = the item just created
Q141205930	P22	LAST	S2600	"6000000003376453205"
#   the item just created: P735 given name = Q943881 Knut
LAST	P735	Q943881

# create a new item
CREATE
#   set the en label to "Margareta Burea"
LAST	Len	"Margareta Burea"
#   set the mul label to "Margareta Burea"
LAST	Lmul	"Margareta Burea"
#   add a mul alias "Margareta Johansdotter Burea"
LAST	Amul	"Margareta Johansdotter Burea"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000025579779586 Margareta Johansdotter Burea
LAST	P2600	"6000000025579779586"
#   P569 date of birth = +1637-07-11T00:00:00Z/11
LAST	P569	+1637-07-11T00:00:00Z/11	S2600	"6000000025579779586"
#   P22 father = Q633094 Johannes Tomasson
LAST	P22	Q633094	S2600	"6000000025579779586"
#   P25 mother = Q141180406 Ingeborg Gyntesdotter
LAST	P25	Q141180406	S2600	"6000000025579779586"
#   Q633094 Johannes Tomasson: P40 child = the item just created
Q633094	P40	LAST	S2600	"6000000025579779586"
#   Q141180406 Ingeborg Gyntesdotter: P40 child = the item just created
Q141180406	P40	LAST	S2600	"6000000025579779586"
#   the item just created: P735 given name = Q8274988 Margareta
LAST	P735	Q8274988

# create a new item
CREATE
#   set the en label to "Margareta Nilsdotter"
LAST	Len	"Margareta Nilsdotter"
#   set the mul label to "Margareta Nilsdotter"
LAST	Lmul	"Margareta Nilsdotter"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000017799612472 Margareta Nilsdotter
LAST	P2600	"6000000017799612472"
#   P569 date of birth = +1585-00-00T00:00:00Z/9
LAST	P569	+1585-00-00T00:00:00Z/9	S2600	"6000000017799612472"
#   P40 child = Q141205928 NN Jonsdotter
LAST	P40	Q141205928	S2600	"6000000017799612472"
#   Q141205928 NN Jonsdotter: P25 mother = the item just created
Q141205928	P25	LAST	S2600	"6000000017799612472"
#   the item just created: P735 given name = Q8274988 Margareta
LAST	P735	Q8274988

# create a new item
CREATE
#   set the en label to "Maria No name"
LAST	Len	"Maria No name"
#   set the mul label to "Maria No name"
LAST	Lmul	"Maria No name"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000027470028034 Maria No name
LAST	P2600	"6000000027470028034"
#   P40 child = Q141205917 Kerstin Månsdotter
LAST	P40	Q141205917	S2600	"6000000027470028034"
#   Q141205917 Kerstin Månsdotter: P25 mother = the item just created
Q141205917	P25	LAST	S2600	"6000000027470028034"

# create a new item
CREATE
#   the item just created: set the en label to "Mariet Danielsdotter"
LAST	Len	"Mariet Danielsdotter"
#   set the mul label to "Mariet Danielsdotter"
LAST	Lmul	"Mariet Danielsdotter"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000017535961052 Mariet Danielsdotter
LAST	P2600	"6000000017535961052"
#   P569 date of birth = +1640-00-00T00:00:00Z/9
LAST	P569	+1640-00-00T00:00:00Z/9	S2600	"6000000017535961052"
#   P570 date of death = +1684-00-00T00:00:00Z/9
LAST	P570	+1684-00-00T00:00:00Z/9	S2600	"6000000017535961052"
#   P22 father = Q141205902 Daniel Olofsson
LAST	P22	Q141205902	S2600	"6000000017535961052"
#   P25 mother = Q141205928 NN Jonsdotter
LAST	P25	Q141205928	S2600	"6000000017535961052"
#   Q141205902 Daniel Olofsson: P40 child = the item just created
Q141205902	P40	LAST	S2600	"6000000017535961052"
#   Q141205928 NN Jonsdotter: P40 child = the item just created
Q141205928	P40	LAST	S2600	"6000000017535961052"

# create a new item
CREATE
#   the item just created: set the en label to "Måns Moge"
LAST	Len	"Måns Moge"
#   set the mul label to "Måns Moge"
LAST	Lmul	"Måns Moge"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000027469942604 Måns Moge
LAST	P2600	"6000000027469942604"
#   P40 child = Q141205917 Kerstin Månsdotter
LAST	P40	Q141205917	S2600	"6000000027469942604"
#   Q141205917 Kerstin Månsdotter: P22 father = the item just created
Q141205917	P22	LAST	S2600	"6000000027469942604"
#   the item just created: P735 given name = Q19799975 Måns
LAST	P735	Q19799975

# create a new item
CREATE
#   set the mul label to "NN N.N. Jacobsdtr. Koll"
LAST	Lmul	"NN N.N. Jacobsdtr. Koll"
#   set the ca label to "mare de Olav Knutson Randa Randa"
LAST	Lca	"mare de Olav Knutson Randa Randa"
#   set the da label to "mor til Olav Knutson Randa Randa"
LAST	Lda	"mor til Olav Knutson Randa Randa"
#   set the de label to "Mutter von Olav Knutson Randa Randa"
LAST	Lde	"Mutter von Olav Knutson Randa Randa"
#   set the en label to "mother of Olav Knutson Randa Randa"
LAST	Len	"mother of Olav Knutson Randa Randa"
#   set the es label to "madre de Olav Knutson Randa Randa"
LAST	Les	"madre de Olav Knutson Randa Randa"
#   set the it label to "madre di Olav Knutson Randa Randa"
LAST	Lit	"madre di Olav Knutson Randa Randa"
#   set the nb label to "mor til Olav Knutson Randa Randa"
LAST	Lnb	"mor til Olav Knutson Randa Randa"
#   set the nl label to "moeder van Olav Knutson Randa Randa"
LAST	Lnl	"moeder van Olav Knutson Randa Randa"
#   set the pt label to "mãe de Olav Knutson Randa Randa"
LAST	Lpt	"mãe de Olav Knutson Randa Randa"
#   set the sv label to "mor till Olav Knutson Randa Randa"
LAST	Lsv	"mor till Olav Knutson Randa Randa"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000030876120040 N.N. Jacobsdtr. Koll
LAST	P2600	"6000000030876120040"
#   P569 date of birth = +1502-00-00T00:00:00Z/9
LAST	P569	+1502-00-00T00:00:00Z/9	S2600	"6000000030876120040"
#   P570 date of death = +1562-00-00T00:00:00Z/9
LAST	P570	+1562-00-00T00:00:00Z/9	S2600	"6000000030876120040"
#   P40 child = Q141205930 Olav Knutson Randa Randa
LAST	P40	Q141205930	S2600	"6000000030876120040"
#   Q141205930 Olav Knutson Randa Randa: P25 mother = the item just created
Q141205930	P25	LAST	S2600	"6000000030876120040"

# create a new item
CREATE
#   the item just created: set the en label to "Ola Person Persson Heigre"
LAST	Len	"Ola Person Persson Heigre"
#   set the mul label to "Ola Person Persson Heigre"
LAST	Lmul	"Ola Person Persson Heigre"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003491947917 Ola Person Persson Heigre
LAST	P2600	"6000000003491947917"
#   P569 date of birth = +1760-00-00T00:00:00Z/9
LAST	P569	+1760-00-00T00:00:00Z/9	S2600	"6000000003491947917"
#   P570 date of death = +1840-05-31T00:00:00Z/11
LAST	P570	+1840-05-31T00:00:00Z/11	S2600	"6000000003491947917"
#   P40 child = Q141199892 Jon Olsen Heigre
LAST	P40	Q141199892	S2600	"6000000003491947917"
#   Q141199892 Jon Olsen Heigre: P22 father = the item just created
Q141199892	P22	LAST	S2600	"6000000003491947917"
#   the item just created: P735 given name = Q96675523 Ola
LAST	P735	Q96675523

# create a new item
CREATE
#   set the en label to "Ola Ådneson Re"
LAST	Len	"Ola Ådneson Re"
#   set the mul label to "Ola Ådneson Re"
LAST	Lmul	"Ola Ådneson Re"
#   add a mul alias "Ola Ådneson Garborg"
LAST	Amul	"Ola Ådneson Garborg"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003492005186 Ola Ådneson Garborg
LAST	P2600	"6000000003492005186"
#   P569 date of birth = +1824-05-04T00:00:00Z/11
LAST	P569	+1824-05-04T00:00:00Z/11	S2600	"6000000003492005186"
#   P22 father = Q141169072 Ådne Olsen Grøtheim
LAST	P22	Q141169072	S2600	"6000000003492005186"
#   P25 mother = Q141178202 Stine Persdatter Øksnevad
LAST	P25	Q141178202	S2600	"6000000003492005186"
#   Q141169072 Ådne Olsen Grøtheim: P40 child = the item just created
Q141169072	P40	LAST	S2600	"6000000003492005186"
#   Q141178202 Stine Persdatter Øksnevad: P40 child = the item just created
Q141178202	P40	LAST	S2600	"6000000003492005186"
#   the item just created: P735 given name = Q96675523 Ola
LAST	P735	Q96675523
#   P734 family name = Q30250555 Garborg, qualified object of statement has role Q2507958 birth name
LAST	P734	Q30250555	P3831	Q2507958
#   P734 family name = Q20148490 Re
LAST	P734	Q20148490
#   add a mul alias "Ola Re"
LAST	Amul	"Ola Re"

# create a new item
CREATE
#   set the en label to "Olaug Jonsdatter Heigre"
LAST	Len	"Olaug Jonsdatter Heigre"
#   set the mul label to "Olaug Jonsdatter Heigre"
LAST	Lmul	"Olaug Jonsdatter Heigre"
#   add a mul alias "Olaug Jonsdatter Røyneberg"
LAST	Amul	"Olaug Jonsdatter Røyneberg"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003491933401 Olaug Jonsdatter Røyneberg
LAST	P2600	"6000000003491933401"
#   P569 date of birth = +1765-00-00T00:00:00Z/9
LAST	P569	+1765-00-00T00:00:00Z/9	S2600	"6000000003491933401"
#   P570 date of death = +1818-02-18T00:00:00Z/11
LAST	P570	+1818-02-18T00:00:00Z/11	S2600	"6000000003491933401"
#   P40 child = Q141199892 Jon Olsen Heigre
LAST	P40	Q141199892	S2600	"6000000003491933401"
#   Q141199892 Jon Olsen Heigre: P25 mother = the item just created
Q141199892	P25	LAST	S2600	"6000000003491933401"
#   the item just created: P735 given name = Q11993398 Olaug
LAST	P735	Q11993398
#   add a mul alias "Olaug Heigre"
LAST	Amul	"Olaug Heigre"

# create a new item
CREATE
#   set the en label to "Olof Nilsson"
LAST	Len	"Olof Nilsson"
#   set the mul label to "Olof Nilsson"
LAST	Lmul	"Olof Nilsson"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 375729629520007230 Olof Nilsson
LAST	P2600	"375729629520007230"
#   P569 date of birth = +1539-00-00T00:00:00Z/9
LAST	P569	+1539-00-00T00:00:00Z/9	S2600	"375729629520007230"
#   P570 date of death = +1627-00-00T00:00:00Z/9
LAST	P570	+1627-00-00T00:00:00Z/9	S2600	"375729629520007230"
#   P40 child = Q141205931 Olof Olofsson
LAST	P40	Q141205931	S2600	"375729629520007230"
#   Q141205931 Olof Olofsson: P22 father = the item just created
Q141205931	P22	LAST	S2600	"375729629520007230"
#   the item just created: P735 given name = Q18089653 Olof
LAST	P735	Q18089653
#   P5056 patronym or matronym = Q130233015 Nilsson
LAST	P5056	Q130233015

# create a new item
CREATE
#   set the en label to "Ramborg Knutsdotter Lejon"
LAST	Len	"Ramborg Knutsdotter Lejon"
#   set the mul label to "Ramborg Knutsdotter Lejon"
LAST	Lmul	"Ramborg Knutsdotter Lejon"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000004870648136 Ramborg Knutsdotter Lejon
LAST	P2600	"6000000004870648136"
#   P569 date of birth = +1360-00-00T00:00:00Z/9
LAST	P569	+1360-00-00T00:00:00Z/9	S2600	"6000000004870648136"
#   P570 date of death = +1408-00-00T00:00:00Z/9
LAST	P570	+1408-00-00T00:00:00Z/9	S2600	"6000000004870648136"
#   P22 father = Q5915800 Knut Algotsson
LAST	P22	Q5915800	S2600	"6000000004870648136"
#   P40 child = Q141205942 Tore Gardson Gardsson
LAST	P40	Q141205942	S2600	"6000000004870648136"
#   Q5915800 Knut Algotsson: P40 child = the item just created
Q5915800	P40	LAST	S2600	"6000000004870648136"
#   Q141205942 Tore Gardson Gardsson: P25 mother = the item just created
Q141205942	P25	LAST	S2600	"6000000004870648136"
#   the item just created: add a mul alias "Ramborg Lejon"
LAST	Amul	"Ramborg Lejon"

# create a new item
CREATE
#   set the en label to "Rasmus Halvarson Erevik"
LAST	Len	"Rasmus Halvarson Erevik"
#   set the mul label to "Rasmus Halvarson Erevik"
LAST	Lmul	"Rasmus Halvarson Erevik"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003095172413 Rasmus Halvarson Erevik
LAST	P2600	"6000000003095172413"
#   P569 date of birth = +1636-00-00T00:00:00Z/9
LAST	P569	+1636-00-00T00:00:00Z/9	S2600	"6000000003095172413"
#   P40 child = Q141200094 Siri Rasmusdtr. Erevik
LAST	P40	Q141200094	S2600	"6000000003095172413"
#   Q141200094 Siri Rasmusdtr. Erevik: P22 father = the item just created
Q141200094	P22	LAST	S2600	"6000000003095172413"
#   the item just created: P735 given name = Q1785744 Rasmus
LAST	P735	Q1785744

# create a new item
CREATE
#   set the en label to "Rasmus Rasmusson Stangeland"
LAST	Len	"Rasmus Rasmusson Stangeland"
#   set the mul label to "Rasmus Rasmusson Stangeland"
LAST	Lmul	"Rasmus Rasmusson Stangeland"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000019668849058 Rasmus Rasmusson Stangeland
LAST	P2600	"6000000019668849058"
#   P26 spouse = Q141198441 Kirsten Olsdatter Grøtheim
LAST	P26	Q141198441	S2600	"6000000019668849058"
#   Q141198441 Kirsten Olsdatter Grøtheim: P26 spouse = the item just created
Q141198441	P26	LAST	S2600	"6000000019668849058"
#   the item just created: P735 given name = Q1785744 Rasmus
LAST	P735	Q1785744
#   P734 family name = Q21452049 Stangeland
LAST	P734	Q21452049

# create a new item
CREATE
#   set the en label to "Russel Paul Paul Romans"
LAST	Len	"Russel Paul Paul Romans"
#   set the mul label to "Russel Paul Paul Romans"
LAST	Lmul	"Russel Paul Paul Romans"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000180037145839 Russel Paul Paul Romans
LAST	P2600	"6000000180037145839"
#   P569 date of birth = +1929-11-06T00:00:00Z/11
LAST	P569	+1929-11-06T00:00:00Z/11	S2600	"6000000180037145839"
#   P570 date of death = +1996-01-07T00:00:00Z/11
LAST	P570	+1996-01-07T00:00:00Z/11	S2600	"6000000180037145839"
#   P26 spouse = Q141205907 Geneva Bell Tunheim
LAST	P26	Q141205907	S2600	"6000000180037145839"
#   Q141205907 Geneva Bell Tunheim: P26 spouse = the item just created
Q141205907	P26	LAST	S2600	"6000000180037145839"
#   the item just created: P735 given name = Q4925623 Paul, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q4925623	P1545	"2"	P3831	Q245025
#   P735 given name = Q4925623 Paul, qualified series ordinal 3, object of statement has role Q245025 middle name
LAST	P735	Q4925623	P1545	"3"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Siri Ingebretsdatter Voster"
LAST	Len	"Siri Ingebretsdatter Voster"
#   set the mul label to "Siri Ingebretsdatter Voster"
LAST	Lmul	"Siri Ingebretsdatter Voster"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000007980728976 Siri Ingebretsdatter Voster
LAST	P2600	"6000000007980728976"
#   P569 date of birth = +1630-00-00T00:00:00Z/9
LAST	P569	+1630-00-00T00:00:00Z/9	S2600	"6000000007980728976"
#   P570 date of death = +1713-00-00T00:00:00Z/9
LAST	P570	+1713-00-00T00:00:00Z/9	S2600	"6000000007980728976"
#   P22 father = Q141205913 Ingebret Pederson Voster
LAST	P22	Q141205913	S2600	"6000000007980728976"
#   P25 mother = Q141205899 Bergitte Ivarsdatter Tjentland
LAST	P25	Q141205899	S2600	"6000000007980728976"
#   Q141205913 Ingebret Pederson Voster: P40 child = the item just created
Q141205913	P40	LAST	S2600	"6000000007980728976"
#   Q141205899 Bergitte Ivarsdatter Tjentland: P40 child = the item just created
Q141205899	P40	LAST	S2600	"6000000007980728976"
#   the item just created: P735 given name = Q1772342 Siri
LAST	P735	Q1772342

# create a new item
CREATE
#   set the en label to "Sven Hansen Risa I"
LAST	Len	"Sven Hansen Risa I"
#   set the mul label to "Sven Hansen Risa I"
LAST	Lmul	"Sven Hansen Risa I"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003491951368 Sven Hansen Risa I
LAST	P2600	"6000000003491951368"
#   P569 date of birth = +1711-00-00T00:00:00Z/9
LAST	P569	+1711-00-00T00:00:00Z/9	S2600	"6000000003491951368"
#   P570 date of death = +1775-00-00T00:00:00Z/9
LAST	P570	+1775-00-00T00:00:00Z/9	S2600	"6000000003491951368"
#   P22 father = Q141205911 Hans Svensen Risa I
LAST	P22	Q141205911	S2600	"6000000003491951368"
#   P25 mother = Q141205914 Inger (Ingrid) Osmundsdatter Tunheim
LAST	P25	Q141205914	S2600	"6000000003491951368"
#   Q141205911 Hans Svensen Risa I: P40 child = the item just created
Q141205911	P40	LAST	S2600	"6000000003491951368"
#   Q141205914 Inger (Ingrid) Osmundsdatter Tunheim: P40 child = the item just created
Q141205914	P40	LAST	S2600	"6000000003491951368"
#   the item just created: P735 given name = Q2370957 Sven
LAST	P735	Q2370957
#   P1449 nickname = en:"Hanson"
LAST	P1449	en:"Hanson"
#   add a mul alias "Hanson Risa"
LAST	Amul	"Hanson Risa"

# create a new item
CREATE
#   set the en label to "Tollak Jonsson Aukland III"
LAST	Len	"Tollak Jonsson Aukland III"
#   set the mul label to "Tollak Jonsson Aukland III"
LAST	Lmul	"Tollak Jonsson Aukland III"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000002390972936 Tollak Jonsson Aukland III
LAST	P2600	"6000000002390972936"
#   P569 date of birth = +1450-00-00T00:00:00Z/9
LAST	P569	+1450-00-00T00:00:00Z/9	S2600	"6000000002390972936"
#   P570 date of death = +1522-00-00T00:00:00Z/9
LAST	P570	+1522-00-00T00:00:00Z/9	S2600	"6000000002390972936"
#   P40 child = Q141199899 Jon Tollakson Aukland IV
LAST	P40	Q141199899	S2600	"6000000002390972936"
#   Q141199899 Jon Tollakson Aukland IV: P22 father = the item just created
Q141199899	P22	LAST	S2600	"6000000002390972936"
#   the item just created: P734 family name = Q4821650 Aukland
LAST	P734	Q4821650

# create a new item
CREATE
#   set the en label to "Torkel Torbjørnson Høyland"
LAST	Len	"Torkel Torbjørnson Høyland"
#   set the mul label to "Torkel Torbjørnson Høyland"
LAST	Lmul	"Torkel Torbjørnson Høyland"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003492072756 Torkel Torbjørnson Høyland
LAST	P2600	"6000000003492072756"
#   P569 date of birth = +1731-00-00T00:00:00Z/9
LAST	P569	+1731-00-00T00:00:00Z/9	S2600	"6000000003492072756"
#   P570 date of death = +1791-00-00T00:00:00Z/9
LAST	P570	+1791-00-00T00:00:00Z/9	S2600	"6000000003492072756"
#   P26 spouse = Q141205916 Kari Olsdatter
LAST	P26	Q141205916	S2600	"6000000003492072756"
#   P40 child = Q141198375 Astri Torchelsdatter Øvre Time
LAST	P40	Q141198375	S2600	"6000000003492072756"
#   Q141205916 Kari Olsdatter: P26 spouse = the item just created
Q141205916	P26	LAST	S2600	"6000000003492072756"
#   Q141198375 Astri Torchelsdatter Øvre Time: P22 father = the item just created
Q141198375	P22	LAST	S2600	"6000000003492072756"
#   the item just created: P735 given name = Q12719075 Torkel
LAST	P735	Q12719075
#   add a mul alias "Torkel Høyland"
LAST	Amul	"Torkel Høyland"

# create a new item
CREATE
#   set the mul label to "NN ektefelle Tollak Jonsson III Aukland"
LAST	Lmul	"NN ektefelle Tollak Jonsson III Aukland"
#   set the ca label to "mare de Jon Tollakson Aukland IV"
LAST	Lca	"mare de Jon Tollakson Aukland IV"
#   set the da label to "mor til Jon Tollakson Aukland IV"
LAST	Lda	"mor til Jon Tollakson Aukland IV"
#   set the de label to "Mutter von Jon Tollakson Aukland IV"
LAST	Lde	"Mutter von Jon Tollakson Aukland IV"
#   set the en label to "mother of Jon Tollakson Aukland IV"
LAST	Len	"mother of Jon Tollakson Aukland IV"
#   set the es label to "madre de Jon Tollakson Aukland IV"
LAST	Les	"madre de Jon Tollakson Aukland IV"
#   set the it label to "madre di Jon Tollakson Aukland IV"
LAST	Lit	"madre di Jon Tollakson Aukland IV"
#   set the nb label to "mor til Jon Tollakson Aukland IV"
LAST	Lnb	"mor til Jon Tollakson Aukland IV"
#   set the nl label to "moeder van Jon Tollakson Aukland IV"
LAST	Lnl	"moeder van Jon Tollakson Aukland IV"
#   set the pt label to "mãe de Jon Tollakson Aukland IV"
LAST	Lpt	"mãe de Jon Tollakson Aukland IV"
#   set the sv label to "mor till Jon Tollakson Aukland IV"
LAST	Lsv	"mor till Jon Tollakson Aukland IV"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000221742699868 nn ektefelle Tollak Jonsson III Aukland
LAST	P2600	"6000000221742699868"
#   P40 child = Q141199899 Jon Tollakson Aukland IV
LAST	P40	Q141199899	S2600	"6000000221742699868"
#   Q141199899 Jon Tollakson Aukland IV: P25 mother = the item just created
Q141199899	P25	LAST	S2600	"6000000221742699868"

# RELATIONSHIPS between items that already exist -- the links yesterday's
#    creations made possible, and the properties never emitted. Every subject
#    and every value already has a QID, so this section depends on nothing above
#    it. It is emitted LAST, per her order: individuals, names, relationships.

#   Q116150300 Cecilie Ebbesdatter Hvide: set the ja label to "セシリエ・エッベスダッテル・ヴィーデ"
Q116150300	Lja	"セシリエ・エッベスダッテル・ヴィーデ"
#   set the zh label to "塞西莉厄·埃贝斯达特·维德"
Q116150300	Lzh	"塞西莉厄·埃贝斯达特·维德"
#   Q5915800 Knut Algotsson: set the ja label to "クヌート・アルゴットソン"
Q5915800	Lja	"クヌート・アルゴットソン"
#   set the zh label to "克努特·阿尔戈特松"
Q5915800	Lzh	"克努特·阿尔戈特松"
#   Q141189104 Siri Kristine Ivarsdatter Sandsmark: set the ja label to "シーリ・クリスティーネ・イーヴァシュダッテル・サンスマルク"
Q141189104	Lja	"シーリ・クリスティーネ・イーヴァシュダッテル・サンスマルク"
#   set the zh label to "西丽·克丽丝汀·伊瓦斯达特·桑斯马克"
Q141189104	Lzh	"西丽·克丽丝汀·伊瓦斯达特·桑斯马克"
#   Q141200019 Ola Olsen Grøtheim: set the ja label to "オーラ・オルセン・グレートヘイム"
Q141200019	Lja	"オーラ・オルセン・グレートヘイム"
#   set the zh label to "乌拉·奥尔森·格勒特海姆"
Q141200019	Lzh	"乌拉·奥尔森·格勒特海姆"
#   Q141189055 Astri Torkelsdatter Gilja: set the ja label to "アストリ・トルケルスダッテル・ギリヤ"
Q141189055	Lja	"アストリ・トルケルスダッテル・ギリヤ"
#   set the zh label to "阿斯特丽·托克尔斯达特·吉利亚"
Q141189055	Lzh	"阿斯特丽·托克尔斯达特·吉利亚"
#   Q141199819 Anna Andersdotter: set the ja label to "アンナ・アンデシュドッテル"
Q141199819	Lja	"アンナ・アンデシュドッテル"
#   set the zh label to "安娜·安德斯多特"
Q141199819	Lzh	"安娜·安德斯多特"
#   Q141199892 Jon Olsen Heigre: set the ja label to "ヨン・オルセン・ヘイグレ"
Q141199892	Lja	"ヨン・オルセン・ヘイグレ"
#   set the zh label to "永·奥尔森·海格勒"
Q141199892	Lzh	"永·奥尔森·海格勒"
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
#   Q141199808 Andreas Olofsson: P22 father = Q141205932 Olof Timmerman
Q141199808	P22	Q141205932	S2600	"6000000004334566448"
#   P25 mother = Q141205926 NN
Q141199808	P25	Q141205926	S2600	"6000000004334566448"
#   P40 child = Q141200016 Nils Andersson
Q141199808	P40	Q141200016	S2600	"6000000004334566448"
#   P26 spouse = Q141199819 Anna Andersdotter
Q141199808	P26	Q141199819	S2600	"6000000004334566448"
#   Q633094 Johannes Tomasson: set the zh label to "约翰内斯·托马松"
Q633094	Lzh	"约翰内斯·托马松"
#   Q141180413 Thomas Mattsson: set the ja label to "トーマス・マットソン"
Q141180413	Lja	"トーマス・マットソン"
#   set the zh label to "托马斯·马特松"
Q141180413	Lzh	"托马斯·马特松"
#   Q141178149 Anna Fartegnsdatter Seim: set the ja label to "アンナ・ファルテグンスダッテル・セイム"
Q141178149	Lja	"アンナ・ファルテグンスダッテル・セイム"
#   set the zh label to "安娜·法尔特格恩斯达特·塞姆"
Q141178149	Lzh	"安娜·法尔特格恩斯达特·塞姆"
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
#   Q141205913 Ingebret Pederson Voster: P26 spouse = Q141205899 Bergitte Ivarsdatter Tjentland
Q141205913	P26	Q141205899	S2600	"6000000007980389582"
#   Q141205899 Bergitte Ivarsdatter Tjentland: P26 spouse = Q141205913 Ingebret Pederson Voster
Q141205899	P26	Q141205913	S2600	"6000000007980617734"
#   Q141189069 Ingeborg Ådnesdatter Grøtheim: set the ja label to "インゲボルグ・オードネスダッテル・グレートヘイム"
Q141189069	Lja	"インゲボルグ・オードネスダッテル・グレートヘイム"
#   set the zh label to "英厄堡·奥德内斯达特·格勒特海姆"
Q141189069	Lzh	"英厄堡·奥德内斯达特·格勒特海姆"
#   Q141189108 Tillie Betsy Tunheim: set the ja label to "ティリー・ベッツィ・トゥンヘイム"
Q141189108	Lja	"ティリー・ベッツィ・トゥンヘイム"
#   set the zh label to "蒂莉·贝齐·通海姆"
Q141189108	Lzh	"蒂莉·贝齐·通海姆"
#   Q141205937 Ragnhild Eyvindsdotter Byre: P26 spouse = Q141205942 Tore Gardson Gardsson
Q141205937	P26	Q141205942	S2600	"6000000008686109792"
#   Q141178201 Marie Petrine Simensdatter Bergersen: set the ja label to "マリー・ペトリーネ・シメンスダッテル・ベルゲルセン"
Q141178201	Lja	"マリー・ペトリーネ・シメンスダッテル・ベルゲルセン"
#   set the zh label to "玛丽·佩特里内·西门斯达特·贝格尔森"
Q141178201	Lzh	"玛丽·佩特里内·西门斯达特·贝格尔森"
#   Q141168797 Christian Frederik Bergersen: set the ja label to "クリスチャン・フレデリク・ベルゲルセン"
Q141168797	Lja	"クリスチャン・フレデリク・ベルゲルセン"
#   set the zh label to "克里斯蒂安·弗雷德里克·贝格尔森"
Q141168797	Lzh	"克里斯蒂安·弗雷德里克·贝格尔森"
#   Q101247444 Ingegerd Svantepolksdotter: set the ja label to "インゲゲルド・スヴァンテポルクスドッテル"
Q101247444	Lja	"インゲゲルド・スヴァンテポルクスドッテル"
#   set the zh label to "英格格德·斯万特波尔克斯多特"
Q101247444	Lzh	"英格格德·斯万特波尔克斯多特"
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
#   Q141205895 Andreas Christiansen: P40 child = Q141205923 Mathilde Fredrikke Christiansen
Q141205895	P40	Q141205923	S2600	"6000000016278848605"
#   Q141205940 Simen Olsen: set the ja label to "シーメン・オルセン"
Q141205940	Lja	"シーメン・オルセン"
#   set the zh label to "西门·奥尔森"
Q141205940	Lzh	"西门·奥尔森"
#   Q141178199 Gunder Bergersen: set the ja label to "グンデル・ベルゲルセン"
Q141178199	Lja	"グンデル・ベルゲルセン"
#   set the zh label to "贡德尔·贝格尔森"
Q141178199	Lzh	"贡德尔·贝格尔森"
#   Q141205928 NN Jonsdotter: P26 spouse = Q141205902 Daniel Olofsson
Q141205928	P26	Q141205902	S2600	"6000000017093875188"
#   Q141205896 Ane Marie Konstanse Amanda Kristine Christiansdatter: P40 child = Q141205900 Bertrand Olav Olsen Vigdel
Q141205896	P40	Q141205900	S2600	"6000000018935780138"
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
#   Q141178197 Elisabeth Johannesen: set the ja label to "エリーサベト・ヨハンネセン"
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
#   Q141205917 Kerstin Månsdotter: P26 spouse = Q141205915 Jöns Jakobsson guldsmed
Q141205917	P26	Q141205915	S2600	"6000000027469679490"
#   Q141189076 Kristian Larsen Nord-Varhaug: set the ja label to "クリスティアン・ラーシェン・ノール・ヴァールハウグ"
Q141189076	Lja	"クリスティアン・ラーシェン・ノール・ヴァールハウグ"
#   set the zh label to "克里斯蒂安·拉尔森·诺尔·瓦尔豪格"
Q141189076	Lzh	"克里斯蒂安·拉尔森·诺尔·瓦尔豪格"
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
#   Q4953376 Helena Guttormsdatter: set the ja label to "ヘレナ・グットルムスダッテル"
Q4953376	Lja	"ヘレナ・グットルムスダッテル"
#   set the zh label to "海伦娜·古托尔姆斯达特"
Q4953376	Lzh	"海伦娜·古托尔姆斯达特"
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
#   Q141205908 Gotfred Olai Ekman: P40 child = Q141205941 Thelma Geraldine Ekman
Q141205908	P40	Q141205941	S2600	"6000000039507605374"
#   Q141189101 Samuel Tunheim: set the ja label to "サムエル・トゥンヘイム"
Q141189101	Lja	"サムエル・トゥンヘイム"
#   set the zh label to "萨穆埃尔·通海姆"
Q141189101	Lzh	"萨穆埃尔·通海姆"
#   Q141205894 Agnes Bakke: P40 child = Q141205907 Geneva Bell Tunheim
Q141205894	P40	Q141205907	S2600	"6000000039512807134"
#   Q141205929 Ola Toreson Talgje: P26 spouse = Q141205909 Gudrun Sæbjørnsdatter Nord-Talgje
Q141205929	P26	Q141205909	S2600	"6000000100130208752"
#   Q141205941 Thelma Geraldine Ekman: P22 father = Q141205908 Gotfred Olai Ekman
Q141205941	P22	Q141205908	S2600	"6000000179983874822"
#   Q141205907 Geneva Bell Tunheim: P25 mother = Q141205894 Agnes Bakke
Q141205907	P25	Q141205894	S2600	"6000000180033404926"
#   Q141189062 Cecilie Jonsdatter: set the ja label to "セシリエ・ヨンスダッテル"
Q141189062	Lja	"セシリエ・ヨンスダッテル"
#   set the zh label to "塞西莉厄·永斯达特"
Q141189062	Lzh	"塞西莉厄·永斯达特"
#   Q141189080 Lave: set the ja label to "ラーヴェ"
Q141189080	Lja	"ラーヴェ"
#   set the zh label to "拉弗"
Q141189080	Lzh	"拉弗"
#   Q141205912 Herborg Johannesdatter Obrestad: P40 child = Q141205936 NN Private
Q141205912	P40	Q141205936	S2600	"6000000221449607942"
#   Q141205936 NN Private: P25 mother = Q141205912 Herborg Johannesdatter Obrestad
Q141205936	P25	Q141205912	S2600	"6000000224702291876"
#   Q141189078 Lars Kristiansen Sør-Reime: set the ja label to "ラーシュ・クリスティアンセン・セール・レイメ"
Q141189078	Lja	"ラーシュ・クリスティアンセン・セール・レイメ"
#   set the zh label to "拉尔斯·克里斯蒂安森·瑟尔·雷梅"
Q141189078	Lzh	"拉尔斯·克里斯蒂安森·瑟尔·雷梅"


# ---------------------------------------------------------------------------
# MANUAL ZIPPER MERGES -- hard-coded, appended to every batch, on purpose.
#
# Each line asserts that an existing Wikidata item IS a particular Geni person.
#
# Eight are on the Arne -> Charlemagne chain. Their items exist and are
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
#
#   Q10411463 Andreas Olai: P2600 Geni.com profile ID.  Emma, 2026-08-28:
#   "we add this qid geni id add thing to the quickstatements block that
#   always gets added in".  Identified during the mass export campaign by
#   STRUCTURE, never by name: the Geni profile reads "Son of Olof, Brother of
#   Kerstin Olofsdotter and Benedictus Olai", and the item carries P3373
#   sibling -> Q4355463 Benedictus Olai.  Its About text gives 1521-1560,
#   matching the item's P569 date of birth and P570 date of death exactly.
#   The structured Birth field is the trap -- it says "estimated between 1450
#   and 1570", which is why the pairing looked unmakeable.  Emma put P1889
#   different from on the item to separate him from the better-known
#   Andreas Olai, so the name alone could never have settled this.
Q10411463	P2600	"6000000040951562251"


# -------------------------------------------------------------------------
# CJK CLAN LABELS -- hard-coded, appended to every batch, on purpose.
#
# Geni records these people as a marker, a place and a clan:
#   GIVN 某 (unknown-name marker) / SURN 隴西狄道 (a PLACE) / _MARNM 李 (the clan).
# 348 of 354 records have that shape and every _MARNM is one character, so the
# married-name field holds the real surname and the surname field holds a place.
#
# Emma, 2026-08-28: "this formulation should be 'woman of the Li clan, from Longxi
# Didao' as the English label and all languages have a similar thing but NN is the
# right mul". Sex comes from the data -- 169 of these 177 are men.
#
# ONLY EMPTY LABEL SLOTS ARE WRITTEN. A label REPLACES, and her other ruling is that
# Wikidata wins where it already knows a name: `en` is occupied on all 177 (Q10864996
# reads "Wanshou") and `nl` on all 177, so neither is touched here. mul is empty on
# all 177; es on 84 of them.
#
# ja and zh are absent on purpose -- the idiomatic Chinese form is a question about
# Chinese rather than about this data.
#
# Repeats every run: setting a label to what it already says is a no-op. Delete when
# the 177 are done.
# -------------------------------------------------------------------------
#   Q10864996 (李 of 隴西狄道): mul label = NN
Q10864996	Lmul	"NN"
#   Q10864996: set the nb label
Q10864996	Lnb	"kvinne av Li-slekten, fra Longxi Didao"
#   Q10864996: set the da label
Q10864996	Lda	"kvinde af Li-slægten, fra Longxi Didao"
#   Q10864996: set the sv label
Q10864996	Lsv	"kvinna av Li-ätten, från Longxi Didao"
#   Q10864996: set the de label
Q10864996	Lde	"Frau des Klans Li, aus Longxi Didao"
#   Q10864996: set the it label
Q10864996	Lit	"donna del clan Li, da Longxi Didao"
#   Q10864996: set the pt label
Q10864996	Lpt	"mulher do clã Li, de Longxi Didao"
#   Q10864996: set the ca label
Q10864996	Lca	"dona del clan Li, de Longxi Didao"
#   Q10881168 (李 of 隴西狄道): mul label = NN
Q10881168	Lmul	"NN"
#   Q10881168: set the nb label
Q10881168	Lnb	"kvinne av Li-slekten, fra Longxi Didao"
#   Q10881168: set the da label
Q10881168	Lda	"kvinde af Li-slægten, fra Longxi Didao"
#   Q10881168: set the sv label
Q10881168	Lsv	"kvinna av Li-ätten, från Longxi Didao"
#   Q10881168: set the de label
Q10881168	Lde	"Frau des Klans Li, aus Longxi Didao"
#   Q10881168: set the it label
Q10881168	Lit	"donna del clan Li, da Longxi Didao"
#   Q10881168: set the pt label
Q10881168	Lpt	"mulher do clã Li, de Longxi Didao"
#   Q10881168: set the ca label
Q10881168	Lca	"dona del clan Li, de Longxi Didao"
#   Q11064679 (李 of 隴西狄道): mul label = NN
Q11064679	Lmul	"NN"
#   Q11064679: set the nb label
Q11064679	Lnb	"kvinne av Li-slekten, fra Longxi Didao"
#   Q11064679: set the da label
Q11064679	Lda	"kvinde af Li-slægten, fra Longxi Didao"
#   Q11064679: set the sv label
Q11064679	Lsv	"kvinna av Li-ätten, från Longxi Didao"
#   Q11064679: set the de label
Q11064679	Lde	"Frau des Klans Li, aus Longxi Didao"
#   Q11064679: set the it label
Q11064679	Lit	"donna del clan Li, da Longxi Didao"
#   Q11064679: set the pt label
Q11064679	Lpt	"mulher do clã Li, de Longxi Didao"
#   Q11064679: set the ca label
Q11064679	Lca	"dona del clan Li, de Longxi Didao"
#   Q11098137 (李 of 河南府): mul label = NN
Q11098137	Lmul	"NN"
#   Q11098137: set the nb label
Q11098137	Lnb	"mann av Li-slekten, fra Henan Prefecture"
#   Q11098137: set the da label
Q11098137	Lda	"mand af Li-slægten, fra Henan Prefecture"
#   Q11098137: set the sv label
Q11098137	Lsv	"man av Li-ätten, från Henan Prefecture"
#   Q11098137: set the de label
Q11098137	Lde	"Mann des Klans Li, aus Henan Prefecture"
#   Q11098137: set the es label
Q11098137	Les	"hombre del clan Li, de Henan Prefecture"
#   Q11098137: set the it label
Q11098137	Lit	"uomo del clan Li, da Henan Prefecture"
#   Q11098137: set the pt label
Q11098137	Lpt	"homem do clã Li, de Henan Prefecture"
#   Q11098137: set the ca label
Q11098137	Lca	"home del clan Li, de Henan Prefecture"
#   Q11110062 (柳 of 河東解縣): mul label = NN
Q11110062	Lmul	"NN"
#   Q11110062: set the nb label
Q11110062	Lnb	"mann av Liu-slekten, fra Hedong Jiexian"
#   Q11110062: set the da label
Q11110062	Lda	"mand af Liu-slægten, fra Hedong Jiexian"
#   Q11110062: set the sv label
Q11110062	Lsv	"man av Liu-ätten, från Hedong Jiexian"
#   Q11110062: set the de label
Q11110062	Lde	"Mann des Klans Liu, aus Hedong Jiexian"
#   Q11110062: set the it label
Q11110062	Lit	"uomo del clan Liu, da Hedong Jiexian"
#   Q11110062: set the pt label
Q11110062	Lpt	"homem do clã Liu, de Hedong Jiexian"
#   Q11110062: set the ca label
Q11110062	Lca	"home del clan Liu, de Hedong Jiexian"
#   Q11180129 (李 of 隴西狄道): mul label = NN
Q11180129	Lmul	"NN"
#   Q11180129: set the nb label
Q11180129	Lnb	"kvinne av Li-slekten, fra Longxi Didao"
#   Q11180129: set the da label
Q11180129	Lda	"kvinde af Li-slægten, fra Longxi Didao"
#   Q11180129: set the sv label
Q11180129	Lsv	"kvinna av Li-ätten, från Longxi Didao"
#   Q11180129: set the de label
Q11180129	Lde	"Frau des Klans Li, aus Longxi Didao"
#   Q11180129: set the es label
Q11180129	Les	"mujer del clan Li, de Longxi Didao"
#   Q11180129: set the it label
Q11180129	Lit	"donna del clan Li, da Longxi Didao"
#   Q11180129: set the pt label
Q11180129	Lpt	"mulher do clã Li, de Longxi Didao"
#   Q11180129: set the ca label
Q11180129	Lca	"dona del clan Li, de Longxi Didao"
#   Q15954845 (李 of ): mul label = NN
Q15954845	Lmul	"NN"
#   Q15954845: set the nb label
Q15954845	Lnb	"kvinne av Li-slekten"
#   Q15954845: set the da label
Q15954845	Lda	"kvinde af Li-slægten"
#   Q15954845: set the sv label
Q15954845	Lsv	"kvinna av Li-ätten"
#   Q15954845: set the de label
Q15954845	Lde	"Frau des Klans Li"
#   Q15954845: set the es label
Q15954845	Les	"mujer del clan Li"
#   Q15954845: set the it label
Q15954845	Lit	"donna del clan Li"
#   Q15954845: set the pt label
Q15954845	Lpt	"mulher do clã Li"
#   Q15954845: set the ca label
Q15954845	Lca	"dona del clan Li"
#   Q16603665 (李 of 隴西狄道): mul label = NN
Q16603665	Lmul	"NN"
#   Q16603665: set the nb label
Q16603665	Lnb	"kvinne av Li-slekten, fra Longxi Didao"
#   Q16603665: set the da label
Q16603665	Lda	"kvinde af Li-slægten, fra Longxi Didao"
#   Q16603665: set the sv label
Q16603665	Lsv	"kvinna av Li-ätten, från Longxi Didao"
#   Q16603665: set the de label
Q16603665	Lde	"Frau des Klans Li, aus Longxi Didao"
#   Q16603665: set the es label
Q16603665	Les	"mujer del clan Li, de Longxi Didao"
#   Q16603665: set the it label
Q16603665	Lit	"donna del clan Li, da Longxi Didao"
#   Q16603665: set the pt label
Q16603665	Lpt	"mulher do clã Li, de Longxi Didao"
#   Q16603665: set the ca label
Q16603665	Lca	"dona del clan Li, de Longxi Didao"
#   Q18908886 (韋 of 京兆杜陵): mul label = NN
Q18908886	Lmul	"NN"
#   Q18908886: set the nb label
Q18908886	Lnb	"mann av Wei-slekten, fra Jingzhao Duling"
#   Q18908886: set the da label
Q18908886	Lda	"mand af Wei-slægten, fra Jingzhao Duling"
#   Q18908886: set the sv label
Q18908886	Lsv	"man av Wei-ätten, från Jingzhao Duling"
#   Q18908886: set the de label
Q18908886	Lde	"Mann des Klans Wei, aus Jingzhao Duling"
#   Q18908886: set the it label
Q18908886	Lit	"uomo del clan Wei, da Jingzhao Duling"
#   Q18908886: set the pt label
Q18908886	Lpt	"homem do clã Wei, de Jingzhao Duling"
#   Q18908886: set the ca label
Q18908886	Lca	"home del clan Wei, de Jingzhao Duling"
#   Q45420125 (權 of 秦州清水): mul label = NN
Q45420125	Lmul	"NN"
#   Q45420125: set the nb label
Q45420125	Lnb	"mann av Quan-slekten, fra Qinzhou Qingshui"
#   Q45420125: set the da label
Q45420125	Lda	"mand af Quan-slægten, fra Qinzhou Qingshui"
#   Q45420125: set the sv label
Q45420125	Lsv	"man av Quan-ätten, från Qinzhou Qingshui"
#   Q45420125: set the de label
Q45420125	Lde	"Mann des Klans Quan, aus Qinzhou Qingshui"
#   Q45420125: set the it label
Q45420125	Lit	"uomo del clan Quan, da Qinzhou Qingshui"
#   Q45420125: set the pt label
Q45420125	Lpt	"homem do clã Quan, de Qinzhou Qingshui"
#   Q45420125: set the ca label
Q45420125	Lca	"home del clan Quan, de Qinzhou Qingshui"
#   Q45421489 (崔 of 深州安平): mul label = NN
Q45421489	Lmul	"NN"
#   Q45421489: set the nb label
Q45421489	Lnb	"mann av Cui-slekten, fra Shenzhou Anping"
#   Q45421489: set the da label
Q45421489	Lda	"mand af Cui-slægten, fra Shenzhou Anping"
#   Q45421489: set the sv label
Q45421489	Lsv	"man av Cui-ätten, från Shenzhou Anping"
#   Q45421489: set the de label
Q45421489	Lde	"Mann des Klans Cui, aus Shenzhou Anping"
#   Q45421489: set the it label
Q45421489	Lit	"uomo del clan Cui, da Shenzhou Anping"
#   Q45421489: set the pt label
Q45421489	Lpt	"homem do clã Cui, de Shenzhou Anping"
#   Q45421489: set the ca label
Q45421489	Lca	"home del clan Cui, de Shenzhou Anping"
#   Q45422231 (柳 of 河東解縣): mul label = NN
Q45422231	Lmul	"NN"
#   Q45422231: set the nb label
Q45422231	Lnb	"mann av Liu-slekten, fra Hedong Jiexian"
#   Q45422231: set the da label
Q45422231	Lda	"mand af Liu-slægten, fra Hedong Jiexian"
#   Q45422231: set the sv label
Q45422231	Lsv	"man av Liu-ätten, från Hedong Jiexian"
#   Q45422231: set the de label
Q45422231	Lde	"Mann des Klans Liu, aus Hedong Jiexian"
#   Q45422231: set the it label
Q45422231	Lit	"uomo del clan Liu, da Hedong Jiexian"
#   Q45422231: set the pt label
Q45422231	Lpt	"homem do clã Liu, de Hedong Jiexian"
#   Q45422231: set the ca label
Q45422231	Lca	"home del clan Liu, de Hedong Jiexian"
#   Q45429773 (韋 of 襄州穀城): mul label = NN
Q45429773	Lmul	"NN"
#   Q45429773: set the nb label
Q45429773	Lnb	"mann av Wei-slekten, fra Xiangzhou Gucheng"
#   Q45429773: set the da label
Q45429773	Lda	"mand af Wei-slægten, fra Xiangzhou Gucheng"
#   Q45429773: set the sv label
Q45429773	Lsv	"man av Wei-ätten, från Xiangzhou Gucheng"
#   Q45429773: set the de label
Q45429773	Lde	"Mann des Klans Wei, aus Xiangzhou Gucheng"
#   Q45429773: set the it label
Q45429773	Lit	"uomo del clan Wei, da Xiangzhou Gucheng"
#   Q45429773: set the pt label
Q45429773	Lpt	"homem do clã Wei, de Xiangzhou Gucheng"
#   Q45429773: set the ca label
Q45429773	Lca	"home del clan Wei, de Xiangzhou Gucheng"
#   Q45448943 (蕭 of 蘭陵): mul label = NN
Q45448943	Lmul	"NN"
#   Q45448943: set the nb label
Q45448943	Lnb	"mann av Xiao-slekten, fra Lanling"
#   Q45448943: set the da label
Q45448943	Lda	"mand af Xiao-slægten, fra Lanling"
#   Q45448943: set the sv label
Q45448943	Lsv	"man av Xiao-ätten, från Lanling"
#   Q45448943: set the de label
Q45448943	Lde	"Mann des Klans Xiao, aus Lanling"
#   Q45448943: set the it label
Q45448943	Lit	"uomo del clan Xiao, da Lanling"
#   Q45448943: set the pt label
Q45448943	Lpt	"homem do clã Xiao, de Lanling"
#   Q45448943: set the ca label
Q45448943	Lca	"home del clan Xiao, de Lanling"
#   Q45449130 (蕭 of 蘭陵): mul label = NN
Q45449130	Lmul	"NN"
#   Q45449130: set the nb label
Q45449130	Lnb	"mann av Xiao-slekten, fra Lanling"
#   Q45449130: set the da label
Q45449130	Lda	"mand af Xiao-slægten, fra Lanling"
#   Q45449130: set the sv label
Q45449130	Lsv	"man av Xiao-ätten, från Lanling"
#   Q45449130: set the de label
Q45449130	Lde	"Mann des Klans Xiao, aus Lanling"
#   Q45449130: set the it label
Q45449130	Lit	"uomo del clan Xiao, da Lanling"
#   Q45449130: set the pt label
Q45449130	Lpt	"homem do clã Xiao, de Lanling"
#   Q45449130: set the ca label
Q45449130	Lca	"home del clan Xiao, de Lanling"
#   Q45450462 (韋 of 京兆萬年): mul label = NN
Q45450462	Lmul	"NN"
#   Q45450462: set the nb label
Q45450462	Lnb	"mann av Wei-slekten, fra Jingzhao Wannian"
#   Q45450462: set the da label
Q45450462	Lda	"mand af Wei-slægten, fra Jingzhao Wannian"
#   Q45450462: set the sv label
Q45450462	Lsv	"man av Wei-ätten, från Jingzhao Wannian"
#   Q45450462: set the de label
Q45450462	Lde	"Mann des Klans Wei, aus Jingzhao Wannian"
#   Q45450462: set the it label
Q45450462	Lit	"uomo del clan Wei, da Jingzhao Wannian"
#   Q45450462: set the pt label
Q45450462	Lpt	"homem do clã Wei, de Jingzhao Wannian"
#   Q45450462: set the ca label
Q45450462	Lca	"home del clan Wei, de Jingzhao Wannian"
#   Q45450834 (蕭 of 蘭陵): mul label = NN
Q45450834	Lmul	"NN"
#   Q45450834: set the nb label
Q45450834	Lnb	"mann av Xiao-slekten, fra Lanling"
#   Q45450834: set the da label
Q45450834	Lda	"mand af Xiao-slægten, fra Lanling"
#   Q45450834: set the sv label
Q45450834	Lsv	"man av Xiao-ätten, från Lanling"
#   Q45450834: set the de label
Q45450834	Lde	"Mann des Klans Xiao, aus Lanling"
#   Q45450834: set the it label
Q45450834	Lit	"uomo del clan Xiao, da Lanling"
#   Q45450834: set the pt label
Q45450834	Lpt	"homem do clã Xiao, de Lanling"
#   Q45450834: set the ca label
Q45450834	Lca	"home del clan Xiao, de Lanling"
#   Q45453968 (韋 of 京兆杜陵): mul label = NN
Q45453968	Lmul	"NN"
#   Q45453968: set the nb label
Q45453968	Lnb	"mann av Wei-slekten, fra Jingzhao Duling"
#   Q45453968: set the da label
Q45453968	Lda	"mand af Wei-slægten, fra Jingzhao Duling"
#   Q45453968: set the sv label
Q45453968	Lsv	"man av Wei-ätten, från Jingzhao Duling"
#   Q45453968: set the de label
Q45453968	Lde	"Mann des Klans Wei, aus Jingzhao Duling"
#   Q45453968: set the it label
Q45453968	Lit	"uomo del clan Wei, da Jingzhao Duling"
#   Q45453968: set the pt label
Q45453968	Lpt	"homem do clã Wei, de Jingzhao Duling"
#   Q45453968: set the ca label
Q45453968	Lca	"home del clan Wei, de Jingzhao Duling"
#   Q45461450 (崔 of 清河東武城): mul label = NN
Q45461450	Lmul	"NN"
#   Q45461450: set the nb label
Q45461450	Lnb	"mann av Cui-slekten, fra Qinghe Dongwucheng"
#   Q45461450: set the da label
Q45461450	Lda	"mand af Cui-slægten, fra Qinghe Dongwucheng"
#   Q45461450: set the sv label
Q45461450	Lsv	"man av Cui-ätten, från Qinghe Dongwucheng"
#   Q45461450: set the de label
Q45461450	Lde	"Mann des Klans Cui, aus Qinghe Dongwucheng"
#   Q45461450: set the it label
Q45461450	Lit	"uomo del clan Cui, da Qinghe Dongwucheng"
#   Q45461450: set the pt label
Q45461450	Lpt	"homem do clã Cui, de Qinghe Dongwucheng"
#   Q45461450: set the ca label
Q45461450	Lca	"home del clan Cui, de Qinghe Dongwucheng"
#   Q45469083 (李 of 隴西狄道): mul label = NN
Q45469083	Lmul	"NN"
#   Q45469083: set the nb label
Q45469083	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45469083: set the da label
Q45469083	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45469083: set the sv label
Q45469083	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45469083: set the de label
Q45469083	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45469083: set the it label
Q45469083	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45469083: set the pt label
Q45469083	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45469083: set the ca label
Q45469083	Lca	"home del clan Li, de Longxi Didao"
#   Q45471981 (李 of 隴西狄道): mul label = NN
Q45471981	Lmul	"NN"
#   Q45471981: set the nb label
Q45471981	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45471981: set the da label
Q45471981	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45471981: set the sv label
Q45471981	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45471981: set the de label
Q45471981	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45471981: set the es label
Q45471981	Les	"hombre del clan Li, de Longxi Didao"
#   Q45471981: set the it label
Q45471981	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45471981: set the pt label
Q45471981	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45471981: set the ca label
Q45471981	Lca	"home del clan Li, de Longxi Didao"
#   Q45472107 (李 of 隴西狄道): mul label = NN
Q45472107	Lmul	"NN"
#   Q45472107: set the nb label
Q45472107	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45472107: set the da label
Q45472107	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45472107: set the sv label
Q45472107	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45472107: set the de label
Q45472107	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45472107: set the es label
Q45472107	Les	"hombre del clan Li, de Longxi Didao"
#   Q45472107: set the it label
Q45472107	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45472107: set the pt label
Q45472107	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45472107: set the ca label
Q45472107	Lca	"home del clan Li, de Longxi Didao"
#   Q45473385 (李 of 隴西狄道): mul label = NN
Q45473385	Lmul	"NN"
#   Q45473385: set the nb label
Q45473385	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45473385: set the da label
Q45473385	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45473385: set the sv label
Q45473385	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45473385: set the de label
Q45473385	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45473385: set the es label
Q45473385	Les	"hombre del clan Li, de Longxi Didao"
#   Q45473385: set the it label
Q45473385	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45473385: set the pt label
Q45473385	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45473385: set the ca label
Q45473385	Lca	"home del clan Li, de Longxi Didao"
#   Q45474359 (李 of 隴西狄道): mul label = NN
Q45474359	Lmul	"NN"
#   Q45474359: set the nb label
Q45474359	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45474359: set the da label
Q45474359	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45474359: set the sv label
Q45474359	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45474359: set the de label
Q45474359	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45474359: set the es label
Q45474359	Les	"hombre del clan Li, de Longxi Didao"
#   Q45474359: set the it label
Q45474359	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45474359: set the pt label
Q45474359	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45474359: set the ca label
Q45474359	Lca	"home del clan Li, de Longxi Didao"
#   Q45481279 (李 of 隴西狄道): mul label = NN
Q45481279	Lmul	"NN"
#   Q45481279: set the nb label
Q45481279	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45481279: set the da label
Q45481279	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45481279: set the sv label
Q45481279	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45481279: set the de label
Q45481279	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45481279: set the es label
Q45481279	Les	"hombre del clan Li, de Longxi Didao"
#   Q45481279: set the it label
Q45481279	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45481279: set the pt label
Q45481279	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45481279: set the ca label
Q45481279	Lca	"home del clan Li, de Longxi Didao"
#   Q45484623 (崔 of 河南): mul label = NN
Q45484623	Lmul	"NN"
#   Q45484623: set the nb label
Q45484623	Lnb	"mann av Cui-slekten, fra Henan"
#   Q45484623: set the da label
Q45484623	Lda	"mand af Cui-slægten, fra Henan"
#   Q45484623: set the sv label
Q45484623	Lsv	"man av Cui-ätten, från Henan"
#   Q45484623: set the de label
Q45484623	Lde	"Mann des Klans Cui, aus Henan"
#   Q45484623: set the it label
Q45484623	Lit	"uomo del clan Cui, da Henan"
#   Q45484623: set the pt label
Q45484623	Lpt	"homem do clã Cui, de Henan"
#   Q45484623: set the ca label
Q45484623	Lca	"home del clan Cui, de Henan"
#   Q45484673 (陳 of 吳興長城): mul label = NN
Q45484673	Lmul	"NN"
#   Q45484673: set the nb label
Q45484673	Lnb	"mann av Chen-slekten, fra Wuxing Changcheng"
#   Q45484673: set the da label
Q45484673	Lda	"mand af Chen-slægten, fra Wuxing Changcheng"
#   Q45484673: set the sv label
Q45484673	Lsv	"man av Chen-ätten, från Wuxing Changcheng"
#   Q45484673: set the de label
Q45484673	Lde	"Mann des Klans Chen, aus Wuxing Changcheng"
#   Q45484673: set the it label
Q45484673	Lit	"uomo del clan Chen, da Wuxing Changcheng"
#   Q45484673: set the pt label
Q45484673	Lpt	"homem do clã Chen, de Wuxing Changcheng"
#   Q45484673: set the ca label
Q45484673	Lca	"home del clan Chen, de Wuxing Changcheng"
#   Q45484869 (陳 of 昇州江寧): mul label = NN
Q45484869	Lmul	"NN"
#   Q45484869: set the nb label
Q45484869	Lnb	"mann av Chen-slekten, fra Shengzhou Jiangning"
#   Q45484869: set the da label
Q45484869	Lda	"mand af Chen-slægten, fra Shengzhou Jiangning"
#   Q45484869: set the sv label
Q45484869	Lsv	"man av Chen-ätten, från Shengzhou Jiangning"
#   Q45484869: set the de label
Q45484869	Lde	"Mann des Klans Chen, aus Shengzhou Jiangning"
#   Q45484869: set the it label
Q45484869	Lit	"uomo del clan Chen, da Shengzhou Jiangning"
#   Q45484869: set the pt label
Q45484869	Lpt	"homem do clã Chen, de Shengzhou Jiangning"
#   Q45484869: set the ca label
Q45484869	Lca	"home del clan Chen, de Shengzhou Jiangning"
#   Q45484932 (陳 of 昇州江寧): mul label = NN
Q45484932	Lmul	"NN"
#   Q45484932: set the nb label
Q45484932	Lnb	"mann av Chen-slekten, fra Shengzhou Jiangning"
#   Q45484932: set the da label
Q45484932	Lda	"mand af Chen-slægten, fra Shengzhou Jiangning"
#   Q45484932: set the sv label
Q45484932	Lsv	"man av Chen-ätten, från Shengzhou Jiangning"
#   Q45484932: set the de label
Q45484932	Lde	"Mann des Klans Chen, aus Shengzhou Jiangning"
#   Q45484932: set the it label
Q45484932	Lit	"uomo del clan Chen, da Shengzhou Jiangning"
#   Q45484932: set the pt label
Q45484932	Lpt	"homem do clã Chen, de Shengzhou Jiangning"
#   Q45484932: set the ca label
Q45484932	Lca	"home del clan Chen, de Shengzhou Jiangning"
#   Q45484995 (陳 of 昇州江寧): mul label = NN
Q45484995	Lmul	"NN"
#   Q45484995: set the nb label
Q45484995	Lnb	"mann av Chen-slekten, fra Shengzhou Jiangning"
#   Q45484995: set the da label
Q45484995	Lda	"mand af Chen-slægten, fra Shengzhou Jiangning"
#   Q45484995: set the sv label
Q45484995	Lsv	"man av Chen-ätten, från Shengzhou Jiangning"
#   Q45484995: set the de label
Q45484995	Lde	"Mann des Klans Chen, aus Shengzhou Jiangning"
#   Q45484995: set the it label
Q45484995	Lit	"uomo del clan Chen, da Shengzhou Jiangning"
#   Q45484995: set the pt label
Q45484995	Lpt	"homem do clã Chen, de Shengzhou Jiangning"
#   Q45484995: set the ca label
Q45484995	Lca	"home del clan Chen, de Shengzhou Jiangning"
#   Q45485126 (陳 of 京兆長安): mul label = NN
Q45485126	Lmul	"NN"
#   Q45485126: set the nb label
Q45485126	Lnb	"mann av Chen-slekten, fra Jingzhao Chang'an"
#   Q45485126: set the da label
Q45485126	Lda	"mand af Chen-slægten, fra Jingzhao Chang'an"
#   Q45485126: set the sv label
Q45485126	Lsv	"man av Chen-ätten, från Jingzhao Chang'an"
#   Q45485126: set the de label
Q45485126	Lde	"Mann des Klans Chen, aus Jingzhao Chang'an"
#   Q45485126: set the it label
Q45485126	Lit	"uomo del clan Chen, da Jingzhao Chang'an"
#   Q45485126: set the pt label
Q45485126	Lpt	"homem do clã Chen, de Jingzhao Chang'an"
#   Q45485126: set the ca label
Q45485126	Lca	"home del clan Chen, de Jingzhao Chang'an"
#   Q45485317 (陳 of 京兆長安): mul label = NN
Q45485317	Lmul	"NN"
#   Q45485317: set the nb label
Q45485317	Lnb	"mann av Chen-slekten, fra Jingzhao Chang'an"
#   Q45485317: set the da label
Q45485317	Lda	"mand af Chen-slægten, fra Jingzhao Chang'an"
#   Q45485317: set the sv label
Q45485317	Lsv	"man av Chen-ätten, från Jingzhao Chang'an"
#   Q45485317: set the de label
Q45485317	Lde	"Mann des Klans Chen, aus Jingzhao Chang'an"
#   Q45485317: set the it label
Q45485317	Lit	"uomo del clan Chen, da Jingzhao Chang'an"
#   Q45485317: set the pt label
Q45485317	Lpt	"homem do clã Chen, de Jingzhao Chang'an"
#   Q45485317: set the ca label
Q45485317	Lca	"home del clan Chen, de Jingzhao Chang'an"
#   Q45485382 (陳 of 京兆長安): mul label = NN
Q45485382	Lmul	"NN"
#   Q45485382: set the nb label
Q45485382	Lnb	"mann av Chen-slekten, fra Jingzhao Chang'an"
#   Q45485382: set the da label
Q45485382	Lda	"mand af Chen-slægten, fra Jingzhao Chang'an"
#   Q45485382: set the sv label
Q45485382	Lsv	"man av Chen-ätten, från Jingzhao Chang'an"
#   Q45485382: set the de label
Q45485382	Lde	"Mann des Klans Chen, aus Jingzhao Chang'an"
#   Q45485382: set the it label
Q45485382	Lit	"uomo del clan Chen, da Jingzhao Chang'an"
#   Q45485382: set the pt label
Q45485382	Lpt	"homem do clã Chen, de Jingzhao Chang'an"
#   Q45485382: set the ca label
Q45485382	Lca	"home del clan Chen, de Jingzhao Chang'an"
#   Q45485462 (李 of 隴西狄道): mul label = NN
Q45485462	Lmul	"NN"
#   Q45485462: set the nb label
Q45485462	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45485462: set the da label
Q45485462	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45485462: set the sv label
Q45485462	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45485462: set the de label
Q45485462	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45485462: set the es label
Q45485462	Les	"hombre del clan Li, de Longxi Didao"
#   Q45485462: set the it label
Q45485462	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45485462: set the pt label
Q45485462	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45485462: set the ca label
Q45485462	Lca	"home del clan Li, de Longxi Didao"
#   Q45485716 (裴 of 河東聞喜): mul label = NN
Q45485716	Lmul	"NN"
#   Q45485716: set the nb label
Q45485716	Lnb	"mann av Pei-slekten, fra Hedong Wenxi"
#   Q45485716: set the da label
Q45485716	Lda	"mand af Pei-slægten, fra Hedong Wenxi"
#   Q45485716: set the sv label
Q45485716	Lsv	"man av Pei-ätten, från Hedong Wenxi"
#   Q45485716: set the de label
Q45485716	Lde	"Mann des Klans Pei, aus Hedong Wenxi"
#   Q45485716: set the it label
Q45485716	Lit	"uomo del clan Pei, da Hedong Wenxi"
#   Q45485716: set the pt label
Q45485716	Lpt	"homem do clã Pei, de Hedong Wenxi"
#   Q45485716: set the ca label
Q45485716	Lca	"home del clan Pei, de Hedong Wenxi"
#   Q45486474 (蕭 of ): mul label = NN
Q45486474	Lmul	"NN"
#   Q45486474: set the nb label
Q45486474	Lnb	"mann av Xiao-slekten"
#   Q45486474: set the da label
Q45486474	Lda	"mand af Xiao-slægten"
#   Q45486474: set the sv label
Q45486474	Lsv	"man av Xiao-ätten"
#   Q45486474: set the de label
Q45486474	Lde	"Mann des Klans Xiao"
#   Q45486474: set the it label
Q45486474	Lit	"uomo del clan Xiao"
#   Q45486474: set the pt label
Q45486474	Lpt	"homem do clã Xiao"
#   Q45486474: set the ca label
Q45486474	Lca	"home del clan Xiao"
#   Q45486525 (陳 of 湖州長城): mul label = NN
Q45486525	Lmul	"NN"
#   Q45486525: set the nb label
Q45486525	Lnb	"mann av Chen-slekten, fra Huzhou Changcheng"
#   Q45486525: set the da label
Q45486525	Lda	"mand af Chen-slægten, fra Huzhou Changcheng"
#   Q45486525: set the sv label
Q45486525	Lsv	"man av Chen-ätten, från Huzhou Changcheng"
#   Q45486525: set the de label
Q45486525	Lde	"Mann des Klans Chen, aus Huzhou Changcheng"
#   Q45486525: set the it label
Q45486525	Lit	"uomo del clan Chen, da Huzhou Changcheng"
#   Q45486525: set the pt label
Q45486525	Lpt	"homem do clã Chen, de Huzhou Changcheng"
#   Q45486525: set the ca label
Q45486525	Lca	"home del clan Chen, de Huzhou Changcheng"
#   Q45486588 (陳 of 湖州長城): mul label = NN
Q45486588	Lmul	"NN"
#   Q45486588: set the nb label
Q45486588	Lnb	"mann av Chen-slekten, fra Huzhou Changcheng"
#   Q45486588: set the da label
Q45486588	Lda	"mand af Chen-slægten, fra Huzhou Changcheng"
#   Q45486588: set the sv label
Q45486588	Lsv	"man av Chen-ätten, från Huzhou Changcheng"
#   Q45486588: set the de label
Q45486588	Lde	"Mann des Klans Chen, aus Huzhou Changcheng"
#   Q45486588: set the it label
Q45486588	Lit	"uomo del clan Chen, da Huzhou Changcheng"
#   Q45486588: set the pt label
Q45486588	Lpt	"homem do clã Chen, de Huzhou Changcheng"
#   Q45486588: set the ca label
Q45486588	Lca	"home del clan Chen, de Huzhou Changcheng"
#   Q45486909 (陳 of 湖州長城): mul label = NN
Q45486909	Lmul	"NN"
#   Q45486909: set the nb label
Q45486909	Lnb	"mann av Chen-slekten, fra Huzhou Changcheng"
#   Q45486909: set the da label
Q45486909	Lda	"mand af Chen-slægten, fra Huzhou Changcheng"
#   Q45486909: set the sv label
Q45486909	Lsv	"man av Chen-ätten, från Huzhou Changcheng"
#   Q45486909: set the de label
Q45486909	Lde	"Mann des Klans Chen, aus Huzhou Changcheng"
#   Q45486909: set the it label
Q45486909	Lit	"uomo del clan Chen, da Huzhou Changcheng"
#   Q45486909: set the pt label
Q45486909	Lpt	"homem do clã Chen, de Huzhou Changcheng"
#   Q45486909: set the ca label
Q45486909	Lca	"home del clan Chen, de Huzhou Changcheng"
#   Q45497731 (盧 of 潤州丹陽): mul label = NN
Q45497731	Lmul	"NN"
#   Q45497731: set the nb label
Q45497731	Lnb	"mann av Lu-slekten, fra Runzhou Danyang"
#   Q45497731: set the da label
Q45497731	Lda	"mand af Lu-slægten, fra Runzhou Danyang"
#   Q45497731: set the sv label
Q45497731	Lsv	"man av Lu-ätten, från Runzhou Danyang"
#   Q45497731: set the de label
Q45497731	Lde	"Mann des Klans Lu, aus Runzhou Danyang"
#   Q45497731: set the es label
Q45497731	Les	"hombre del clan Lu, de Runzhou Danyang"
#   Q45497731: set the it label
Q45497731	Lit	"uomo del clan Lu, da Runzhou Danyang"
#   Q45497731: set the pt label
Q45497731	Lpt	"homem do clã Lu, de Runzhou Danyang"
#   Q45497731: set the ca label
Q45497731	Lca	"home del clan Lu, de Runzhou Danyang"
#   Q45501359 (楊 of 弘農華陰): mul label = NN
Q45501359	Lmul	"NN"
#   Q45501359: set the nb label
Q45501359	Lnb	"mann av Yang-slekten, fra Hongnong Huayin"
#   Q45501359: set the da label
Q45501359	Lda	"mand af Yang-slægten, fra Hongnong Huayin"
#   Q45501359: set the sv label
Q45501359	Lsv	"man av Yang-ätten, från Hongnong Huayin"
#   Q45501359: set the de label
Q45501359	Lde	"Mann des Klans Yang, aus Hongnong Huayin"
#   Q45501359: set the it label
Q45501359	Lit	"uomo del clan Yang, da Hongnong Huayin"
#   Q45501359: set the pt label
Q45501359	Lpt	"homem do clã Yang, de Hongnong Huayin"
#   Q45501359: set the ca label
Q45501359	Lca	"home del clan Yang, de Hongnong Huayin"
#   Q45501424 (楊 of 弘農華陰): mul label = NN
Q45501424	Lmul	"NN"
#   Q45501424: set the nb label
Q45501424	Lnb	"mann av Yang-slekten, fra Hongnong Huayin"
#   Q45501424: set the da label
Q45501424	Lda	"mand af Yang-slægten, fra Hongnong Huayin"
#   Q45501424: set the sv label
Q45501424	Lsv	"man av Yang-ätten, från Hongnong Huayin"
#   Q45501424: set the de label
Q45501424	Lde	"Mann des Klans Yang, aus Hongnong Huayin"
#   Q45501424: set the it label
Q45501424	Lit	"uomo del clan Yang, da Hongnong Huayin"
#   Q45501424: set the pt label
Q45501424	Lpt	"homem do clã Yang, de Hongnong Huayin"
#   Q45501424: set the ca label
Q45501424	Lca	"home del clan Yang, de Hongnong Huayin"
#   Q45502571 (李 of 隴西狄道): mul label = NN
Q45502571	Lmul	"NN"
#   Q45502571: set the nb label
Q45502571	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45502571: set the da label
Q45502571	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45502571: set the sv label
Q45502571	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45502571: set the de label
Q45502571	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45502571: set the es label
Q45502571	Les	"hombre del clan Li, de Longxi Didao"
#   Q45502571: set the it label
Q45502571	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45502571: set the pt label
Q45502571	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45502571: set the ca label
Q45502571	Lca	"home del clan Li, de Longxi Didao"
#   Q45502705 (楊 of 弘農華陰): mul label = NN
Q45502705	Lmul	"NN"
#   Q45502705: set the nb label
Q45502705	Lnb	"mann av Yang-slekten, fra Hongnong Huayin"
#   Q45502705: set the da label
Q45502705	Lda	"mand af Yang-slægten, fra Hongnong Huayin"
#   Q45502705: set the sv label
Q45502705	Lsv	"man av Yang-ätten, från Hongnong Huayin"
#   Q45502705: set the de label
Q45502705	Lde	"Mann des Klans Yang, aus Hongnong Huayin"
#   Q45502705: set the it label
Q45502705	Lit	"uomo del clan Yang, da Hongnong Huayin"
#   Q45502705: set the pt label
Q45502705	Lpt	"homem do clã Yang, de Hongnong Huayin"
#   Q45502705: set the ca label
Q45502705	Lca	"home del clan Yang, de Hongnong Huayin"
#   Q45503478 (楊 of 弘農華陰): mul label = NN
Q45503478	Lmul	"NN"
#   Q45503478: set the nb label
Q45503478	Lnb	"mann av Yang-slekten, fra Hongnong Huayin"
#   Q45503478: set the da label
Q45503478	Lda	"mand af Yang-slægten, fra Hongnong Huayin"
#   Q45503478: set the sv label
Q45503478	Lsv	"man av Yang-ätten, från Hongnong Huayin"
#   Q45503478: set the de label
Q45503478	Lde	"Mann des Klans Yang, aus Hongnong Huayin"
#   Q45503478: set the it label
Q45503478	Lit	"uomo del clan Yang, da Hongnong Huayin"
#   Q45503478: set the pt label
Q45503478	Lpt	"homem do clã Yang, de Hongnong Huayin"
#   Q45503478: set the ca label
Q45503478	Lca	"home del clan Yang, de Hongnong Huayin"
#   Q45503541 (楊 of 弘農華陰): mul label = NN
Q45503541	Lmul	"NN"
#   Q45503541: set the nb label
Q45503541	Lnb	"mann av Yang-slekten, fra Hongnong Huayin"
#   Q45503541: set the da label
Q45503541	Lda	"mand af Yang-slægten, fra Hongnong Huayin"
#   Q45503541: set the sv label
Q45503541	Lsv	"man av Yang-ätten, från Hongnong Huayin"
#   Q45503541: set the de label
Q45503541	Lde	"Mann des Klans Yang, aus Hongnong Huayin"
#   Q45503541: set the it label
Q45503541	Lit	"uomo del clan Yang, da Hongnong Huayin"
#   Q45503541: set the pt label
Q45503541	Lpt	"homem do clã Yang, de Hongnong Huayin"
#   Q45503541: set the ca label
Q45503541	Lca	"home del clan Yang, de Hongnong Huayin"
#   Q45507781 (柳 of 河東解縣): mul label = NN
Q45507781	Lmul	"NN"
#   Q45507781: set the nb label
Q45507781	Lnb	"mann av Liu-slekten, fra Hedong Jiexian"
#   Q45507781: set the da label
Q45507781	Lda	"mand af Liu-slægten, fra Hedong Jiexian"
#   Q45507781: set the sv label
Q45507781	Lsv	"man av Liu-ätten, från Hedong Jiexian"
#   Q45507781: set the de label
Q45507781	Lde	"Mann des Klans Liu, aus Hedong Jiexian"
#   Q45507781: set the it label
Q45507781	Lit	"uomo del clan Liu, da Hedong Jiexian"
#   Q45507781: set the pt label
Q45507781	Lpt	"homem do clã Liu, de Hedong Jiexian"
#   Q45507781: set the ca label
Q45507781	Lca	"home del clan Liu, de Hedong Jiexian"
#   Q45508685 (楊 of 弘農華陰): mul label = NN
Q45508685	Lmul	"NN"
#   Q45508685: set the nb label
Q45508685	Lnb	"mann av Yang-slekten, fra Hongnong Huayin"
#   Q45508685: set the da label
Q45508685	Lda	"mand af Yang-slægten, fra Hongnong Huayin"
#   Q45508685: set the sv label
Q45508685	Lsv	"man av Yang-ätten, från Hongnong Huayin"
#   Q45508685: set the de label
Q45508685	Lde	"Mann des Klans Yang, aus Hongnong Huayin"
#   Q45508685: set the it label
Q45508685	Lit	"uomo del clan Yang, da Hongnong Huayin"
#   Q45508685: set the pt label
Q45508685	Lpt	"homem do clã Yang, de Hongnong Huayin"
#   Q45508685: set the ca label
Q45508685	Lca	"home del clan Yang, de Hongnong Huayin"
#   Q45508942 (楊 of 弘農華陰): mul label = NN
Q45508942	Lmul	"NN"
#   Q45508942: set the nb label
Q45508942	Lnb	"mann av Yang-slekten, fra Hongnong Huayin"
#   Q45508942: set the da label
Q45508942	Lda	"mand af Yang-slægten, fra Hongnong Huayin"
#   Q45508942: set the sv label
Q45508942	Lsv	"man av Yang-ätten, från Hongnong Huayin"
#   Q45508942: set the de label
Q45508942	Lde	"Mann des Klans Yang, aus Hongnong Huayin"
#   Q45508942: set the it label
Q45508942	Lit	"uomo del clan Yang, da Hongnong Huayin"
#   Q45508942: set the pt label
Q45508942	Lpt	"homem do clã Yang, de Hongnong Huayin"
#   Q45508942: set the ca label
Q45508942	Lca	"home del clan Yang, de Hongnong Huayin"
#   Q45509891 (楊 of 弘農華陰): mul label = NN
Q45509891	Lmul	"NN"
#   Q45509891: set the nb label
Q45509891	Lnb	"mann av Yang-slekten, fra Hongnong Huayin"
#   Q45509891: set the da label
Q45509891	Lda	"mand af Yang-slægten, fra Hongnong Huayin"
#   Q45509891: set the sv label
Q45509891	Lsv	"man av Yang-ätten, från Hongnong Huayin"
#   Q45509891: set the de label
Q45509891	Lde	"Mann des Klans Yang, aus Hongnong Huayin"
#   Q45509891: set the it label
Q45509891	Lit	"uomo del clan Yang, da Hongnong Huayin"
#   Q45509891: set the pt label
Q45509891	Lpt	"homem do clã Yang, de Hongnong Huayin"
#   Q45509891: set the ca label
Q45509891	Lca	"home del clan Yang, de Hongnong Huayin"
#   Q45510761 (柳 of 河東解縣): mul label = NN
Q45510761	Lmul	"NN"
#   Q45510761: set the nb label
Q45510761	Lnb	"mann av Liu-slekten, fra Hedong Jiexian"
#   Q45510761: set the da label
Q45510761	Lda	"mand af Liu-slægten, fra Hedong Jiexian"
#   Q45510761: set the sv label
Q45510761	Lsv	"man av Liu-ätten, från Hedong Jiexian"
#   Q45510761: set the de label
Q45510761	Lde	"Mann des Klans Liu, aus Hedong Jiexian"
#   Q45510761: set the it label
Q45510761	Lit	"uomo del clan Liu, da Hedong Jiexian"
#   Q45510761: set the pt label
Q45510761	Lpt	"homem do clã Liu, de Hedong Jiexian"
#   Q45510761: set the ca label
Q45510761	Lca	"home del clan Liu, de Hedong Jiexian"
#   Q45510826 (柳 of 河東解縣): mul label = NN
Q45510826	Lmul	"NN"
#   Q45510826: set the nb label
Q45510826	Lnb	"mann av Liu-slekten, fra Hedong Jiexian"
#   Q45510826: set the da label
Q45510826	Lda	"mand af Liu-slægten, fra Hedong Jiexian"
#   Q45510826: set the sv label
Q45510826	Lsv	"man av Liu-ätten, från Hedong Jiexian"
#   Q45510826: set the de label
Q45510826	Lde	"Mann des Klans Liu, aus Hedong Jiexian"
#   Q45510826: set the it label
Q45510826	Lit	"uomo del clan Liu, da Hedong Jiexian"
#   Q45510826: set the pt label
Q45510826	Lpt	"homem do clã Liu, de Hedong Jiexian"
#   Q45510826: set the ca label
Q45510826	Lca	"home del clan Liu, de Hedong Jiexian"
#   Q45510888 (柳 of 河東解縣): mul label = NN
Q45510888	Lmul	"NN"
#   Q45510888: set the nb label
Q45510888	Lnb	"mann av Liu-slekten, fra Hedong Jiexian"
#   Q45510888: set the da label
Q45510888	Lda	"mand af Liu-slægten, fra Hedong Jiexian"
#   Q45510888: set the sv label
Q45510888	Lsv	"man av Liu-ätten, från Hedong Jiexian"
#   Q45510888: set the de label
Q45510888	Lde	"Mann des Klans Liu, aus Hedong Jiexian"
#   Q45510888: set the it label
Q45510888	Lit	"uomo del clan Liu, da Hedong Jiexian"
#   Q45510888: set the pt label
Q45510888	Lpt	"homem do clã Liu, de Hedong Jiexian"
#   Q45510888: set the ca label
Q45510888	Lca	"home del clan Liu, de Hedong Jiexian"
#   Q45511272 (柳 of 河東解縣): mul label = NN
Q45511272	Lmul	"NN"
#   Q45511272: set the nb label
Q45511272	Lnb	"mann av Liu-slekten, fra Hedong Jiexian"
#   Q45511272: set the da label
Q45511272	Lda	"mand af Liu-slægten, fra Hedong Jiexian"
#   Q45511272: set the sv label
Q45511272	Lsv	"man av Liu-ätten, från Hedong Jiexian"
#   Q45511272: set the de label
Q45511272	Lde	"Mann des Klans Liu, aus Hedong Jiexian"
#   Q45511272: set the it label
Q45511272	Lit	"uomo del clan Liu, da Hedong Jiexian"
#   Q45511272: set the pt label
Q45511272	Lpt	"homem do clã Liu, de Hedong Jiexian"
#   Q45511272: set the ca label
Q45511272	Lca	"home del clan Liu, de Hedong Jiexian"
#   Q45511461 (柳 of 河東解縣): mul label = NN
Q45511461	Lmul	"NN"
#   Q45511461: set the nb label
Q45511461	Lnb	"mann av Liu-slekten, fra Hedong Jiexian"
#   Q45511461: set the da label
Q45511461	Lda	"mand af Liu-slægten, fra Hedong Jiexian"
#   Q45511461: set the sv label
Q45511461	Lsv	"man av Liu-ätten, från Hedong Jiexian"
#   Q45511461: set the de label
Q45511461	Lde	"Mann des Klans Liu, aus Hedong Jiexian"
#   Q45511461: set the it label
Q45511461	Lit	"uomo del clan Liu, da Hedong Jiexian"
#   Q45511461: set the pt label
Q45511461	Lpt	"homem do clã Liu, de Hedong Jiexian"
#   Q45511461: set the ca label
Q45511461	Lca	"home del clan Liu, de Hedong Jiexian"
#   Q45511905 (柳 of 河東解縣): mul label = NN
Q45511905	Lmul	"NN"
#   Q45511905: set the nb label
Q45511905	Lnb	"mann av Liu-slekten, fra Hedong Jiexian"
#   Q45511905: set the da label
Q45511905	Lda	"mand af Liu-slægten, fra Hedong Jiexian"
#   Q45511905: set the sv label
Q45511905	Lsv	"man av Liu-ätten, från Hedong Jiexian"
#   Q45511905: set the de label
Q45511905	Lde	"Mann des Klans Liu, aus Hedong Jiexian"
#   Q45511905: set the it label
Q45511905	Lit	"uomo del clan Liu, da Hedong Jiexian"
#   Q45511905: set the pt label
Q45511905	Lpt	"homem do clã Liu, de Hedong Jiexian"
#   Q45511905: set the ca label
Q45511905	Lca	"home del clan Liu, de Hedong Jiexian"
#   Q45512915 (柳 of 河東解縣): mul label = NN
Q45512915	Lmul	"NN"
#   Q45512915: set the nb label
Q45512915	Lnb	"mann av Liu-slekten, fra Hedong Jiexian"
#   Q45512915: set the da label
Q45512915	Lda	"mand af Liu-slægten, fra Hedong Jiexian"
#   Q45512915: set the sv label
Q45512915	Lsv	"man av Liu-ätten, från Hedong Jiexian"
#   Q45512915: set the de label
Q45512915	Lde	"Mann des Klans Liu, aus Hedong Jiexian"
#   Q45512915: set the it label
Q45512915	Lit	"uomo del clan Liu, da Hedong Jiexian"
#   Q45512915: set the pt label
Q45512915	Lpt	"homem do clã Liu, de Hedong Jiexian"
#   Q45512915: set the ca label
Q45512915	Lca	"home del clan Liu, de Hedong Jiexian"
#   Q45513489 (柳 of 河東解縣): mul label = NN
Q45513489	Lmul	"NN"
#   Q45513489: set the nb label
Q45513489	Lnb	"mann av Liu-slekten, fra Hedong Jiexian"
#   Q45513489: set the da label
Q45513489	Lda	"mand af Liu-slægten, fra Hedong Jiexian"
#   Q45513489: set the sv label
Q45513489	Lsv	"man av Liu-ätten, från Hedong Jiexian"
#   Q45513489: set the de label
Q45513489	Lde	"Mann des Klans Liu, aus Hedong Jiexian"
#   Q45513489: set the it label
Q45513489	Lit	"uomo del clan Liu, da Hedong Jiexian"
#   Q45513489: set the pt label
Q45513489	Lpt	"homem do clã Liu, de Hedong Jiexian"
#   Q45513489: set the ca label
Q45513489	Lca	"home del clan Liu, de Hedong Jiexian"
#   Q45513552 (柳 of 河東解縣): mul label = NN
Q45513552	Lmul	"NN"
#   Q45513552: set the nb label
Q45513552	Lnb	"mann av Liu-slekten, fra Hedong Jiexian"
#   Q45513552: set the da label
Q45513552	Lda	"mand af Liu-slægten, fra Hedong Jiexian"
#   Q45513552: set the sv label
Q45513552	Lsv	"man av Liu-ätten, från Hedong Jiexian"
#   Q45513552: set the de label
Q45513552	Lde	"Mann des Klans Liu, aus Hedong Jiexian"
#   Q45513552: set the it label
Q45513552	Lit	"uomo del clan Liu, da Hedong Jiexian"
#   Q45513552: set the pt label
Q45513552	Lpt	"homem do clã Liu, de Hedong Jiexian"
#   Q45513552: set the ca label
Q45513552	Lca	"home del clan Liu, de Hedong Jiexian"
#   Q45517450 (房 of 齊州臨淄): mul label = NN
Q45517450	Lmul	"NN"
#   Q45517450: set the nb label
Q45517450	Lnb	"mann av Fang-slekten, fra Qizhou Linzi"
#   Q45517450: set the da label
Q45517450	Lda	"mand af Fang-slægten, fra Qizhou Linzi"
#   Q45517450: set the sv label
Q45517450	Lsv	"man av Fang-ätten, från Qizhou Linzi"
#   Q45517450: set the de label
Q45517450	Lde	"Mann des Klans Fang, aus Qizhou Linzi"
#   Q45517450: set the it label
Q45517450	Lit	"uomo del clan Fang, da Qizhou Linzi"
#   Q45517450: set the pt label
Q45517450	Lpt	"homem do clã Fang, de Qizhou Linzi"
#   Q45517450: set the ca label
Q45517450	Lca	"home del clan Fang, de Qizhou Linzi"
#   Q45517515 (房 of 齊州臨淄): mul label = NN
Q45517515	Lmul	"NN"
#   Q45517515: set the nb label
Q45517515	Lnb	"mann av Fang-slekten, fra Qizhou Linzi"
#   Q45517515: set the da label
Q45517515	Lda	"mand af Fang-slægten, fra Qizhou Linzi"
#   Q45517515: set the sv label
Q45517515	Lsv	"man av Fang-ätten, från Qizhou Linzi"
#   Q45517515: set the de label
Q45517515	Lde	"Mann des Klans Fang, aus Qizhou Linzi"
#   Q45517515: set the it label
Q45517515	Lit	"uomo del clan Fang, da Qizhou Linzi"
#   Q45517515: set the pt label
Q45517515	Lpt	"homem do clã Fang, de Qizhou Linzi"
#   Q45517515: set the ca label
Q45517515	Lca	"home del clan Fang, de Qizhou Linzi"
#   Q45517579 (房 of 齊州臨淄): mul label = NN
Q45517579	Lmul	"NN"
#   Q45517579: set the nb label
Q45517579	Lnb	"mann av Fang-slekten, fra Qizhou Linzi"
#   Q45517579: set the da label
Q45517579	Lda	"mand af Fang-slægten, fra Qizhou Linzi"
#   Q45517579: set the sv label
Q45517579	Lsv	"man av Fang-ätten, från Qizhou Linzi"
#   Q45517579: set the de label
Q45517579	Lde	"Mann des Klans Fang, aus Qizhou Linzi"
#   Q45517579: set the it label
Q45517579	Lit	"uomo del clan Fang, da Qizhou Linzi"
#   Q45517579: set the pt label
Q45517579	Lpt	"homem do clã Fang, de Qizhou Linzi"
#   Q45517579: set the ca label
Q45517579	Lca	"home del clan Fang, de Qizhou Linzi"
#   Q45517644 (房 of 齊州臨淄): mul label = NN
Q45517644	Lmul	"NN"
#   Q45517644: set the nb label
Q45517644	Lnb	"mann av Fang-slekten, fra Qizhou Linzi"
#   Q45517644: set the da label
Q45517644	Lda	"mand af Fang-slægten, fra Qizhou Linzi"
#   Q45517644: set the sv label
Q45517644	Lsv	"man av Fang-ätten, från Qizhou Linzi"
#   Q45517644: set the de label
Q45517644	Lde	"Mann des Klans Fang, aus Qizhou Linzi"
#   Q45517644: set the it label
Q45517644	Lit	"uomo del clan Fang, da Qizhou Linzi"
#   Q45517644: set the pt label
Q45517644	Lpt	"homem do clã Fang, de Qizhou Linzi"
#   Q45517644: set the ca label
Q45517644	Lca	"home del clan Fang, de Qizhou Linzi"
#   Q45517670 (李 of 隴西狄道): mul label = NN
Q45517670	Lmul	"NN"
#   Q45517670: set the nb label
Q45517670	Lnb	"kvinne av Li-slekten, fra Longxi Didao"
#   Q45517670: set the da label
Q45517670	Lda	"kvinde af Li-slægten, fra Longxi Didao"
#   Q45517670: set the sv label
Q45517670	Lsv	"kvinna av Li-ätten, från Longxi Didao"
#   Q45517670: set the de label
Q45517670	Lde	"Frau des Klans Li, aus Longxi Didao"
#   Q45517670: set the es label
Q45517670	Les	"mujer del clan Li, de Longxi Didao"
#   Q45517670: set the it label
Q45517670	Lit	"donna del clan Li, da Longxi Didao"
#   Q45517670: set the pt label
Q45517670	Lpt	"mulher do clã Li, de Longxi Didao"
#   Q45517670: set the ca label
Q45517670	Lca	"dona del clan Li, de Longxi Didao"
#   Q45518351 (房 of 齊州臨淄): mul label = NN
Q45518351	Lmul	"NN"
#   Q45518351: set the nb label
Q45518351	Lnb	"mann av Fang-slekten, fra Qizhou Linzi"
#   Q45518351: set the da label
Q45518351	Lda	"mand af Fang-slægten, fra Qizhou Linzi"
#   Q45518351: set the sv label
Q45518351	Lsv	"man av Fang-ätten, från Qizhou Linzi"
#   Q45518351: set the de label
Q45518351	Lde	"Mann des Klans Fang, aus Qizhou Linzi"
#   Q45518351: set the it label
Q45518351	Lit	"uomo del clan Fang, da Qizhou Linzi"
#   Q45518351: set the pt label
Q45518351	Lpt	"homem do clã Fang, de Qizhou Linzi"
#   Q45518351: set the ca label
Q45518351	Lca	"home del clan Fang, de Qizhou Linzi"
#   Q45518415 (房 of 齊州臨淄): mul label = NN
Q45518415	Lmul	"NN"
#   Q45518415: set the nb label
Q45518415	Lnb	"mann av Fang-slekten, fra Qizhou Linzi"
#   Q45518415: set the da label
Q45518415	Lda	"mand af Fang-slægten, fra Qizhou Linzi"
#   Q45518415: set the sv label
Q45518415	Lsv	"man av Fang-ätten, från Qizhou Linzi"
#   Q45518415: set the de label
Q45518415	Lde	"Mann des Klans Fang, aus Qizhou Linzi"
#   Q45518415: set the it label
Q45518415	Lit	"uomo del clan Fang, da Qizhou Linzi"
#   Q45518415: set the pt label
Q45518415	Lpt	"homem do clã Fang, de Qizhou Linzi"
#   Q45518415: set the ca label
Q45518415	Lca	"home del clan Fang, de Qizhou Linzi"
#   Q45521650 (李 of 隴西狄道): mul label = NN
Q45521650	Lmul	"NN"
#   Q45521650: set the nb label
Q45521650	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45521650: set the da label
Q45521650	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45521650: set the sv label
Q45521650	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45521650: set the de label
Q45521650	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45521650: set the es label
Q45521650	Les	"hombre del clan Li, de Longxi Didao"
#   Q45521650: set the it label
Q45521650	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45521650: set the pt label
Q45521650	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45521650: set the ca label
Q45521650	Lca	"home del clan Li, de Longxi Didao"
#   Q45534434 (李 of 隴西狄道): mul label = NN
Q45534434	Lmul	"NN"
#   Q45534434: set the nb label
Q45534434	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45534434: set the da label
Q45534434	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45534434: set the sv label
Q45534434	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45534434: set the de label
Q45534434	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45534434: set the es label
Q45534434	Les	"hombre del clan Li, de Longxi Didao"
#   Q45534434: set the it label
Q45534434	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45534434: set the pt label
Q45534434	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45534434: set the ca label
Q45534434	Lca	"home del clan Li, de Longxi Didao"
#   Q45534750 (鄭 of 鄭州榮澤): mul label = NN
Q45534750	Lmul	"NN"
#   Q45534750: set the nb label
Q45534750	Lnb	"mann av Zheng-slekten, fra Zhengzhou Rongze"
#   Q45534750: set the da label
Q45534750	Lda	"mand af Zheng-slægten, fra Zhengzhou Rongze"
#   Q45534750: set the sv label
Q45534750	Lsv	"man av Zheng-ätten, från Zhengzhou Rongze"
#   Q45534750: set the de label
Q45534750	Lde	"Mann des Klans Zheng, aus Zhengzhou Rongze"
#   Q45534750: set the it label
Q45534750	Lit	"uomo del clan Zheng, da Zhengzhou Rongze"
#   Q45534750: set the pt label
Q45534750	Lpt	"homem do clã Zheng, de Zhengzhou Rongze"
#   Q45534750: set the ca label
Q45534750	Lca	"home del clan Zheng, de Zhengzhou Rongze"
#   Q45536767 (杜 of 京兆杜陵): mul label = NN
Q45536767	Lmul	"NN"
#   Q45536767: set the nb label
Q45536767	Lnb	"mann av Du-slekten, fra Jingzhao Duling"
#   Q45536767: set the da label
Q45536767	Lda	"mand af Du-slægten, fra Jingzhao Duling"
#   Q45536767: set the sv label
Q45536767	Lsv	"man av Du-ätten, från Jingzhao Duling"
#   Q45536767: set the de label
Q45536767	Lde	"Mann des Klans Du, aus Jingzhao Duling"
#   Q45536767: set the es label
Q45536767	Les	"hombre del clan Du, de Jingzhao Duling"
#   Q45536767: set the it label
Q45536767	Lit	"uomo del clan Du, da Jingzhao Duling"
#   Q45536767: set the pt label
Q45536767	Lpt	"homem do clã Du, de Jingzhao Duling"
#   Q45536767: set the ca label
Q45536767	Lca	"home del clan Du, de Jingzhao Duling"
#   Q45536832 (杜 of 京兆杜陵): mul label = NN
Q45536832	Lmul	"NN"
#   Q45536832: set the nb label
Q45536832	Lnb	"mann av Du-slekten, fra Jingzhao Duling"
#   Q45536832: set the da label
Q45536832	Lda	"mand af Du-slægten, fra Jingzhao Duling"
#   Q45536832: set the sv label
Q45536832	Lsv	"man av Du-ätten, från Jingzhao Duling"
#   Q45536832: set the de label
Q45536832	Lde	"Mann des Klans Du, aus Jingzhao Duling"
#   Q45536832: set the es label
Q45536832	Les	"hombre del clan Du, de Jingzhao Duling"
#   Q45536832: set the it label
Q45536832	Lit	"uomo del clan Du, da Jingzhao Duling"
#   Q45536832: set the pt label
Q45536832	Lpt	"homem do clã Du, de Jingzhao Duling"
#   Q45536832: set the ca label
Q45536832	Lca	"home del clan Du, de Jingzhao Duling"
#   Q45541151 (李 of 隴西狄道): mul label = NN
Q45541151	Lmul	"NN"
#   Q45541151: set the nb label
Q45541151	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45541151: set the da label
Q45541151	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45541151: set the sv label
Q45541151	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45541151: set the de label
Q45541151	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45541151: set the es label
Q45541151	Les	"hombre del clan Li, de Longxi Didao"
#   Q45541151: set the it label
Q45541151	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45541151: set the pt label
Q45541151	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45541151: set the ca label
Q45541151	Lca	"home del clan Li, de Longxi Didao"
#   Q45542682 (李 of 隴西狄道): mul label = NN
Q45542682	Lmul	"NN"
#   Q45542682: set the nb label
Q45542682	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45542682: set the da label
Q45542682	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45542682: set the sv label
Q45542682	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45542682: set the de label
Q45542682	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45542682: set the es label
Q45542682	Les	"hombre del clan Li, de Longxi Didao"
#   Q45542682: set the it label
Q45542682	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45542682: set the pt label
Q45542682	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45542682: set the ca label
Q45542682	Lca	"home del clan Li, de Longxi Didao"
#   Q45544329 (李 of 隴西狄道): mul label = NN
Q45544329	Lmul	"NN"
#   Q45544329: set the nb label
Q45544329	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45544329: set the da label
Q45544329	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45544329: set the sv label
Q45544329	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45544329: set the de label
Q45544329	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45544329: set the es label
Q45544329	Les	"hombre del clan Li, de Longxi Didao"
#   Q45544329: set the it label
Q45544329	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45544329: set the pt label
Q45544329	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45544329: set the ca label
Q45544329	Lca	"home del clan Li, de Longxi Didao"
#   Q45553927 (李 of 京兆長安): mul label = NN
Q45553927	Lmul	"NN"
#   Q45553927: set the nb label
Q45553927	Lnb	"mann av Li-slekten, fra Jingzhao Chang'an"
#   Q45553927: set the da label
Q45553927	Lda	"mand af Li-slægten, fra Jingzhao Chang'an"
#   Q45553927: set the sv label
Q45553927	Lsv	"man av Li-ätten, från Jingzhao Chang'an"
#   Q45553927: set the de label
Q45553927	Lde	"Mann des Klans Li, aus Jingzhao Chang'an"
#   Q45553927: set the es label
Q45553927	Les	"hombre del clan Li, de Jingzhao Chang'an"
#   Q45553927: set the it label
Q45553927	Lit	"uomo del clan Li, da Jingzhao Chang'an"
#   Q45553927: set the pt label
Q45553927	Lpt	"homem do clã Li, de Jingzhao Chang'an"
#   Q45553927: set the ca label
Q45553927	Lca	"home del clan Li, de Jingzhao Chang'an"
#   Q45556055 (李 of 河南洛陽): mul label = NN
Q45556055	Lmul	"NN"
#   Q45556055: set the nb label
Q45556055	Lnb	"mann av Li-slekten, fra Henan Luoyang"
#   Q45556055: set the da label
Q45556055	Lda	"mand af Li-slægten, fra Henan Luoyang"
#   Q45556055: set the sv label
Q45556055	Lsv	"man av Li-ätten, från Henan Luoyang"
#   Q45556055: set the de label
Q45556055	Lde	"Mann des Klans Li, aus Henan Luoyang"
#   Q45556055: set the es label
Q45556055	Les	"hombre del clan Li, de Henan Luoyang"
#   Q45556055: set the it label
Q45556055	Lit	"uomo del clan Li, da Henan Luoyang"
#   Q45556055: set the pt label
Q45556055	Lpt	"homem do clã Li, de Henan Luoyang"
#   Q45556055: set the ca label
Q45556055	Lca	"home del clan Li, de Henan Luoyang"
#   Q45557842 (崔 of 貝州清河): mul label = NN
Q45557842	Lmul	"NN"
#   Q45557842: set the nb label
Q45557842	Lnb	"mann av Cui-slekten, fra Beizhou Qinghe"
#   Q45557842: set the da label
Q45557842	Lda	"mand af Cui-slægten, fra Beizhou Qinghe"
#   Q45557842: set the sv label
Q45557842	Lsv	"man av Cui-ätten, från Beizhou Qinghe"
#   Q45557842: set the de label
Q45557842	Lde	"Mann des Klans Cui, aus Beizhou Qinghe"
#   Q45557842: set the it label
Q45557842	Lit	"uomo del clan Cui, da Beizhou Qinghe"
#   Q45557842: set the pt label
Q45557842	Lpt	"homem do clã Cui, de Beizhou Qinghe"
#   Q45557842: set the ca label
Q45557842	Lca	"home del clan Cui, de Beizhou Qinghe"
#   Q45562647 (裴 of 京兆萬年): mul label = NN
Q45562647	Lmul	"NN"
#   Q45562647: set the nb label
Q45562647	Lnb	"mann av Pei-slekten, fra Jingzhao Wannian"
#   Q45562647: set the da label
Q45562647	Lda	"mand af Pei-slægten, fra Jingzhao Wannian"
#   Q45562647: set the sv label
Q45562647	Lsv	"man av Pei-ätten, från Jingzhao Wannian"
#   Q45562647: set the de label
Q45562647	Lde	"Mann des Klans Pei, aus Jingzhao Wannian"
#   Q45562647: set the it label
Q45562647	Lit	"uomo del clan Pei, da Jingzhao Wannian"
#   Q45562647: set the pt label
Q45562647	Lpt	"homem do clã Pei, de Jingzhao Wannian"
#   Q45562647: set the ca label
Q45562647	Lca	"home del clan Pei, de Jingzhao Wannian"
#   Q45562711 (裴 of 河東聞喜): mul label = NN
Q45562711	Lmul	"NN"
#   Q45562711: set the nb label
Q45562711	Lnb	"mann av Pei-slekten, fra Hedong Wenxi"
#   Q45562711: set the da label
Q45562711	Lda	"mand af Pei-slægten, fra Hedong Wenxi"
#   Q45562711: set the sv label
Q45562711	Lsv	"man av Pei-ätten, från Hedong Wenxi"
#   Q45562711: set the de label
Q45562711	Lde	"Mann des Klans Pei, aus Hedong Wenxi"
#   Q45562711: set the it label
Q45562711	Lit	"uomo del clan Pei, da Hedong Wenxi"
#   Q45562711: set the pt label
Q45562711	Lpt	"homem do clã Pei, de Hedong Wenxi"
#   Q45562711: set the ca label
Q45562711	Lca	"home del clan Pei, de Hedong Wenxi"
#   Q45562775 (裴 of 河東聞喜): mul label = NN
Q45562775	Lmul	"NN"
#   Q45562775: set the nb label
Q45562775	Lnb	"mann av Pei-slekten, fra Hedong Wenxi"
#   Q45562775: set the da label
Q45562775	Lda	"mand af Pei-slægten, fra Hedong Wenxi"
#   Q45562775: set the sv label
Q45562775	Lsv	"man av Pei-ätten, från Hedong Wenxi"
#   Q45562775: set the de label
Q45562775	Lde	"Mann des Klans Pei, aus Hedong Wenxi"
#   Q45562775: set the it label
Q45562775	Lit	"uomo del clan Pei, da Hedong Wenxi"
#   Q45562775: set the pt label
Q45562775	Lpt	"homem do clã Pei, de Hedong Wenxi"
#   Q45562775: set the ca label
Q45562775	Lca	"home del clan Pei, de Hedong Wenxi"
#   Q45570419 (李 of 京兆萬年): mul label = NN
Q45570419	Lmul	"NN"
#   Q45570419: set the nb label
Q45570419	Lnb	"mann av Li-slekten, fra Jingzhao Wannian"
#   Q45570419: set the da label
Q45570419	Lda	"mand af Li-slægten, fra Jingzhao Wannian"
#   Q45570419: set the sv label
Q45570419	Lsv	"man av Li-ätten, från Jingzhao Wannian"
#   Q45570419: set the de label
Q45570419	Lde	"Mann des Klans Li, aus Jingzhao Wannian"
#   Q45570419: set the es label
Q45570419	Les	"hombre del clan Li, de Jingzhao Wannian"
#   Q45570419: set the it label
Q45570419	Lit	"uomo del clan Li, da Jingzhao Wannian"
#   Q45570419: set the pt label
Q45570419	Lpt	"homem do clã Li, de Jingzhao Wannian"
#   Q45570419: set the ca label
Q45570419	Lca	"home del clan Li, de Jingzhao Wannian"
#   Q45570482 (李 of 京兆萬年): mul label = NN
Q45570482	Lmul	"NN"
#   Q45570482: set the nb label
Q45570482	Lnb	"mann av Li-slekten, fra Jingzhao Wannian"
#   Q45570482: set the da label
Q45570482	Lda	"mand af Li-slægten, fra Jingzhao Wannian"
#   Q45570482: set the sv label
Q45570482	Lsv	"man av Li-ätten, från Jingzhao Wannian"
#   Q45570482: set the de label
Q45570482	Lde	"Mann des Klans Li, aus Jingzhao Wannian"
#   Q45570482: set the es label
Q45570482	Les	"hombre del clan Li, de Jingzhao Wannian"
#   Q45570482: set the it label
Q45570482	Lit	"uomo del clan Li, da Jingzhao Wannian"
#   Q45570482: set the pt label
Q45570482	Lpt	"homem do clã Li, de Jingzhao Wannian"
#   Q45570482: set the ca label
Q45570482	Lca	"home del clan Li, de Jingzhao Wannian"
#   Q45574741 (李 of 趙州贊皇): mul label = NN
Q45574741	Lmul	"NN"
#   Q45574741: set the nb label
Q45574741	Lnb	"mann av Li-slekten, fra Zhaozhou Zanhuang"
#   Q45574741: set the da label
Q45574741	Lda	"mand af Li-slægten, fra Zhaozhou Zanhuang"
#   Q45574741: set the sv label
Q45574741	Lsv	"man av Li-ätten, från Zhaozhou Zanhuang"
#   Q45574741: set the de label
Q45574741	Lde	"Mann des Klans Li, aus Zhaozhou Zanhuang"
#   Q45574741: set the es label
Q45574741	Les	"hombre del clan Li, de Zhaozhou Zanhuang"
#   Q45574741: set the it label
Q45574741	Lit	"uomo del clan Li, da Zhaozhou Zanhuang"
#   Q45574741: set the pt label
Q45574741	Lpt	"homem do clã Li, de Zhaozhou Zanhuang"
#   Q45574741: set the ca label
Q45574741	Lca	"home del clan Li, de Zhaozhou Zanhuang"
#   Q45574802 (李 of 趙州贊皇): mul label = NN
Q45574802	Lmul	"NN"
#   Q45574802: set the nb label
Q45574802	Lnb	"mann av Li-slekten, fra Zhaozhou Zanhuang"
#   Q45574802: set the da label
Q45574802	Lda	"mand af Li-slægten, fra Zhaozhou Zanhuang"
#   Q45574802: set the sv label
Q45574802	Lsv	"man av Li-ätten, från Zhaozhou Zanhuang"
#   Q45574802: set the de label
Q45574802	Lde	"Mann des Klans Li, aus Zhaozhou Zanhuang"
#   Q45574802: set the es label
Q45574802	Les	"hombre del clan Li, de Zhaozhou Zanhuang"
#   Q45574802: set the it label
Q45574802	Lit	"uomo del clan Li, da Zhaozhou Zanhuang"
#   Q45574802: set the pt label
Q45574802	Lpt	"homem do clã Li, de Zhaozhou Zanhuang"
#   Q45574802: set the ca label
Q45574802	Lca	"home del clan Li, de Zhaozhou Zanhuang"
#   Q45583513 (鄭 of 滎陽開封): mul label = NN
Q45583513	Lmul	"NN"
#   Q45583513: set the nb label
Q45583513	Lnb	"mann av Zheng-slekten, fra Xingyang Kaifeng"
#   Q45583513: set the da label
Q45583513	Lda	"mand af Zheng-slægten, fra Xingyang Kaifeng"
#   Q45583513: set the sv label
Q45583513	Lsv	"man av Zheng-ätten, från Xingyang Kaifeng"
#   Q45583513: set the de label
Q45583513	Lde	"Mann des Klans Zheng, aus Xingyang Kaifeng"
#   Q45583513: set the it label
Q45583513	Lit	"uomo del clan Zheng, da Xingyang Kaifeng"
#   Q45583513: set the pt label
Q45583513	Lpt	"homem do clã Zheng, de Xingyang Kaifeng"
#   Q45583513: set the ca label
Q45583513	Lca	"home del clan Zheng, de Xingyang Kaifeng"
#   Q45600896 (陸 of 吳郡吳縣): mul label = NN
Q45600896	Lmul	"NN"
#   Q45600896: set the nb label
Q45600896	Lnb	"mann av Lu-slekten, fra Wujun Wuxian"
#   Q45600896: set the da label
Q45600896	Lda	"mand af Lu-slægten, fra Wujun Wuxian"
#   Q45600896: set the sv label
Q45600896	Lsv	"man av Lu-ätten, från Wujun Wuxian"
#   Q45600896: set the de label
Q45600896	Lde	"Mann des Klans Lu, aus Wujun Wuxian"
#   Q45600896: set the es label
Q45600896	Les	"hombre del clan Lu, de Wujun Wuxian"
#   Q45600896: set the it label
Q45600896	Lit	"uomo del clan Lu, da Wujun Wuxian"
#   Q45600896: set the pt label
Q45600896	Lpt	"homem do clã Lu, de Wujun Wuxian"
#   Q45600896: set the ca label
Q45600896	Lca	"home del clan Lu, de Wujun Wuxian"
#   Q45602475 (李 of 京兆長安): mul label = NN
Q45602475	Lmul	"NN"
#   Q45602475: set the nb label
Q45602475	Lnb	"mann av Li-slekten, fra Jingzhao Chang'an"
#   Q45602475: set the da label
Q45602475	Lda	"mand af Li-slægten, fra Jingzhao Chang'an"
#   Q45602475: set the sv label
Q45602475	Lsv	"man av Li-ätten, från Jingzhao Chang'an"
#   Q45602475: set the de label
Q45602475	Lde	"Mann des Klans Li, aus Jingzhao Chang'an"
#   Q45602475: set the es label
Q45602475	Les	"hombre del clan Li, de Jingzhao Chang'an"
#   Q45602475: set the it label
Q45602475	Lit	"uomo del clan Li, da Jingzhao Chang'an"
#   Q45602475: set the pt label
Q45602475	Lpt	"homem do clã Li, de Jingzhao Chang'an"
#   Q45602475: set the ca label
Q45602475	Lca	"home del clan Li, de Jingzhao Chang'an"
#   Q45611337 (鄭 of 鄭州榮澤): mul label = NN
Q45611337	Lmul	"NN"
#   Q45611337: set the nb label
Q45611337	Lnb	"mann av Zheng-slekten, fra Zhengzhou Rongze"
#   Q45611337: set the da label
Q45611337	Lda	"mand af Zheng-slægten, fra Zhengzhou Rongze"
#   Q45611337: set the sv label
Q45611337	Lsv	"man av Zheng-ätten, från Zhengzhou Rongze"
#   Q45611337: set the de label
Q45611337	Lde	"Mann des Klans Zheng, aus Zhengzhou Rongze"
#   Q45611337: set the it label
Q45611337	Lit	"uomo del clan Zheng, da Zhengzhou Rongze"
#   Q45611337: set the pt label
Q45611337	Lpt	"homem do clã Zheng, de Zhengzhou Rongze"
#   Q45611337: set the ca label
Q45611337	Lca	"home del clan Zheng, de Zhengzhou Rongze"
#   Q45620545 (楊 of ): mul label = NN
Q45620545	Lmul	"NN"
#   Q45620545: set the nb label
Q45620545	Lnb	"mann av Yang-slekten"
#   Q45620545: set the da label
Q45620545	Lda	"mand af Yang-slægten"
#   Q45620545: set the sv label
Q45620545	Lsv	"man av Yang-ätten"
#   Q45620545: set the de label
Q45620545	Lde	"Mann des Klans Yang"
#   Q45620545: set the it label
Q45620545	Lit	"uomo del clan Yang"
#   Q45620545: set the pt label
Q45620545	Lpt	"homem do clã Yang"
#   Q45620545: set the ca label
Q45620545	Lca	"home del clan Yang"
#   Q45621550 (李 of 趙州贊皇): mul label = NN
Q45621550	Lmul	"NN"
#   Q45621550: set the nb label
Q45621550	Lnb	"mann av Li-slekten, fra Zhaozhou Zanhuang"
#   Q45621550: set the da label
Q45621550	Lda	"mand af Li-slægten, fra Zhaozhou Zanhuang"
#   Q45621550: set the sv label
Q45621550	Lsv	"man av Li-ätten, från Zhaozhou Zanhuang"
#   Q45621550: set the de label
Q45621550	Lde	"Mann des Klans Li, aus Zhaozhou Zanhuang"
#   Q45621550: set the es label
Q45621550	Les	"hombre del clan Li, de Zhaozhou Zanhuang"
#   Q45621550: set the it label
Q45621550	Lit	"uomo del clan Li, da Zhaozhou Zanhuang"
#   Q45621550: set the pt label
Q45621550	Lpt	"homem do clã Li, de Zhaozhou Zanhuang"
#   Q45621550: set the ca label
Q45621550	Lca	"home del clan Li, de Zhaozhou Zanhuang"
#   Q45621738 (李 of 趙州贊皇): mul label = NN
Q45621738	Lmul	"NN"
#   Q45621738: set the nb label
Q45621738	Lnb	"mann av Li-slekten, fra Zhaozhou Zanhuang"
#   Q45621738: set the da label
Q45621738	Lda	"mand af Li-slægten, fra Zhaozhou Zanhuang"
#   Q45621738: set the sv label
Q45621738	Lsv	"man av Li-ätten, från Zhaozhou Zanhuang"
#   Q45621738: set the de label
Q45621738	Lde	"Mann des Klans Li, aus Zhaozhou Zanhuang"
#   Q45621738: set the es label
Q45621738	Les	"hombre del clan Li, de Zhaozhou Zanhuang"
#   Q45621738: set the it label
Q45621738	Lit	"uomo del clan Li, da Zhaozhou Zanhuang"
#   Q45621738: set the pt label
Q45621738	Lpt	"homem do clã Li, de Zhaozhou Zanhuang"
#   Q45621738: set the ca label
Q45621738	Lca	"home del clan Li, de Zhaozhou Zanhuang"
#   Q45622685 (唐 of 晉昌冥安): mul label = NN
Q45622685	Lmul	"NN"
#   Q45622685: set the nb label
Q45622685	Lnb	"mann av Tang-slekten, fra Jinchang Ming'an"
#   Q45622685: set the da label
Q45622685	Lda	"mand af Tang-slægten, fra Jinchang Ming'an"
#   Q45622685: set the sv label
Q45622685	Lsv	"man av Tang-ätten, från Jinchang Ming'an"
#   Q45622685: set the de label
Q45622685	Lde	"Mann des Klans Tang, aus Jinchang Ming'an"
#   Q45622685: set the it label
Q45622685	Lit	"uomo del clan Tang, da Jinchang Ming'an"
#   Q45622685: set the pt label
Q45622685	Lpt	"homem do clã Tang, de Jinchang Ming'an"
#   Q45622685: set the ca label
Q45622685	Lca	"home del clan Tang, de Jinchang Ming'an"
#   Q45628948 (薛 of 蒲州寶鼎): mul label = NN
Q45628948	Lmul	"NN"
#   Q45628948: set the nb label
Q45628948	Lnb	"mann av Xue-slekten, fra Puzhou Baoding"
#   Q45628948: set the da label
Q45628948	Lda	"mand af Xue-slægten, fra Puzhou Baoding"
#   Q45628948: set the sv label
Q45628948	Lsv	"man av Xue-ätten, från Puzhou Baoding"
#   Q45628948: set the de label
Q45628948	Lde	"Mann des Klans Xue, aus Puzhou Baoding"
#   Q45628948: set the it label
Q45628948	Lit	"uomo del clan Xue, da Puzhou Baoding"
#   Q45628948: set the pt label
Q45628948	Lpt	"homem do clã Xue, de Puzhou Baoding"
#   Q45628948: set the ca label
Q45628948	Lca	"home del clan Xue, de Puzhou Baoding"
#   Q45632756 (裴 of 河東聞喜): mul label = NN
Q45632756	Lmul	"NN"
#   Q45632756: set the nb label
Q45632756	Lnb	"mann av Pei-slekten, fra Hedong Wenxi"
#   Q45632756: set the da label
Q45632756	Lda	"mand af Pei-slægten, fra Hedong Wenxi"
#   Q45632756: set the sv label
Q45632756	Lsv	"man av Pei-ätten, från Hedong Wenxi"
#   Q45632756: set the de label
Q45632756	Lde	"Mann des Klans Pei, aus Hedong Wenxi"
#   Q45632756: set the it label
Q45632756	Lit	"uomo del clan Pei, da Hedong Wenxi"
#   Q45632756: set the pt label
Q45632756	Lpt	"homem do clã Pei, de Hedong Wenxi"
#   Q45632756: set the ca label
Q45632756	Lca	"home del clan Pei, de Hedong Wenxi"
#   Q45635644 (蕭 of 蘭陵): mul label = NN
Q45635644	Lmul	"NN"
#   Q45635644: set the nb label
Q45635644	Lnb	"mann av Xiao-slekten, fra Lanling"
#   Q45635644: set the da label
Q45635644	Lda	"mand af Xiao-slægten, fra Lanling"
#   Q45635644: set the sv label
Q45635644	Lsv	"man av Xiao-ätten, från Lanling"
#   Q45635644: set the de label
Q45635644	Lde	"Mann des Klans Xiao, aus Lanling"
#   Q45635644: set the it label
Q45635644	Lit	"uomo del clan Xiao, da Lanling"
#   Q45635644: set the pt label
Q45635644	Lpt	"homem do clã Xiao, de Lanling"
#   Q45635644: set the ca label
Q45635644	Lca	"home del clan Xiao, de Lanling"
#   Q45639455 (薛 of 蒲州寶鼎): mul label = NN
Q45639455	Lmul	"NN"
#   Q45639455: set the nb label
Q45639455	Lnb	"mann av Xue-slekten, fra Puzhou Baoding"
#   Q45639455: set the da label
Q45639455	Lda	"mand af Xue-slægten, fra Puzhou Baoding"
#   Q45639455: set the sv label
Q45639455	Lsv	"man av Xue-ätten, från Puzhou Baoding"
#   Q45639455: set the de label
Q45639455	Lde	"Mann des Klans Xue, aus Puzhou Baoding"
#   Q45639455: set the it label
Q45639455	Lit	"uomo del clan Xue, da Puzhou Baoding"
#   Q45639455: set the pt label
Q45639455	Lpt	"homem do clã Xue, de Puzhou Baoding"
#   Q45639455: set the ca label
Q45639455	Lca	"home del clan Xue, de Puzhou Baoding"
#   Q45642399 (裴 of 河東聞喜): mul label = NN
Q45642399	Lmul	"NN"
#   Q45642399: set the nb label
Q45642399	Lnb	"mann av Pei-slekten, fra Hedong Wenxi"
#   Q45642399: set the da label
Q45642399	Lda	"mand af Pei-slægten, fra Hedong Wenxi"
#   Q45642399: set the sv label
Q45642399	Lsv	"man av Pei-ätten, från Hedong Wenxi"
#   Q45642399: set the de label
Q45642399	Lde	"Mann des Klans Pei, aus Hedong Wenxi"
#   Q45642399: set the it label
Q45642399	Lit	"uomo del clan Pei, da Hedong Wenxi"
#   Q45642399: set the pt label
Q45642399	Lpt	"homem do clã Pei, de Hedong Wenxi"
#   Q45642399: set the ca label
Q45642399	Lca	"home del clan Pei, de Hedong Wenxi"
#   Q45642460 (裴 of 河東聞喜): mul label = NN
Q45642460	Lmul	"NN"
#   Q45642460: set the nb label
Q45642460	Lnb	"mann av Pei-slekten, fra Hedong Wenxi"
#   Q45642460: set the da label
Q45642460	Lda	"mand af Pei-slægten, fra Hedong Wenxi"
#   Q45642460: set the sv label
Q45642460	Lsv	"man av Pei-ätten, från Hedong Wenxi"
#   Q45642460: set the de label
Q45642460	Lde	"Mann des Klans Pei, aus Hedong Wenxi"
#   Q45642460: set the it label
Q45642460	Lit	"uomo del clan Pei, da Hedong Wenxi"
#   Q45642460: set the pt label
Q45642460	Lpt	"homem do clã Pei, de Hedong Wenxi"
#   Q45642460: set the ca label
Q45642460	Lca	"home del clan Pei, de Hedong Wenxi"
#   Q45642520 (裴 of 河東聞喜): mul label = NN
Q45642520	Lmul	"NN"
#   Q45642520: set the nb label
Q45642520	Lnb	"mann av Pei-slekten, fra Hedong Wenxi"
#   Q45642520: set the da label
Q45642520	Lda	"mand af Pei-slægten, fra Hedong Wenxi"
#   Q45642520: set the sv label
Q45642520	Lsv	"man av Pei-ätten, från Hedong Wenxi"
#   Q45642520: set the de label
Q45642520	Lde	"Mann des Klans Pei, aus Hedong Wenxi"
#   Q45642520: set the it label
Q45642520	Lit	"uomo del clan Pei, da Hedong Wenxi"
#   Q45642520: set the pt label
Q45642520	Lpt	"homem do clã Pei, de Hedong Wenxi"
#   Q45642520: set the ca label
Q45642520	Lca	"home del clan Pei, de Hedong Wenxi"
#   Q45642643 (裴 of 河東聞喜): mul label = NN
Q45642643	Lmul	"NN"
#   Q45642643: set the nb label
Q45642643	Lnb	"mann av Pei-slekten, fra Hedong Wenxi"
#   Q45642643: set the da label
Q45642643	Lda	"mand af Pei-slægten, fra Hedong Wenxi"
#   Q45642643: set the sv label
Q45642643	Lsv	"man av Pei-ätten, från Hedong Wenxi"
#   Q45642643: set the de label
Q45642643	Lde	"Mann des Klans Pei, aus Hedong Wenxi"
#   Q45642643: set the it label
Q45642643	Lit	"uomo del clan Pei, da Hedong Wenxi"
#   Q45642643: set the pt label
Q45642643	Lpt	"homem do clã Pei, de Hedong Wenxi"
#   Q45642643: set the ca label
Q45642643	Lca	"home del clan Pei, de Hedong Wenxi"
#   Q45642829 (裴 of 河東聞喜): mul label = NN
Q45642829	Lmul	"NN"
#   Q45642829: set the nb label
Q45642829	Lnb	"mann av Pei-slekten, fra Hedong Wenxi"
#   Q45642829: set the da label
Q45642829	Lda	"mand af Pei-slægten, fra Hedong Wenxi"
#   Q45642829: set the sv label
Q45642829	Lsv	"man av Pei-ätten, från Hedong Wenxi"
#   Q45642829: set the de label
Q45642829	Lde	"Mann des Klans Pei, aus Hedong Wenxi"
#   Q45642829: set the it label
Q45642829	Lit	"uomo del clan Pei, da Hedong Wenxi"
#   Q45642829: set the pt label
Q45642829	Lpt	"homem do clã Pei, de Hedong Wenxi"
#   Q45642829: set the ca label
Q45642829	Lca	"home del clan Pei, de Hedong Wenxi"
#   Q45644430 (李 of 趙州平棘): mul label = NN
Q45644430	Lmul	"NN"
#   Q45644430: set the nb label
Q45644430	Lnb	"mann av Li-slekten, fra Zhaozhou Pingji"
#   Q45644430: set the da label
Q45644430	Lda	"mand af Li-slægten, fra Zhaozhou Pingji"
#   Q45644430: set the sv label
Q45644430	Lsv	"man av Li-ätten, från Zhaozhou Pingji"
#   Q45644430: set the de label
Q45644430	Lde	"Mann des Klans Li, aus Zhaozhou Pingji"
#   Q45644430: set the es label
Q45644430	Les	"hombre del clan Li, de Zhaozhou Pingji"
#   Q45644430: set the it label
Q45644430	Lit	"uomo del clan Li, da Zhaozhou Pingji"
#   Q45644430: set the pt label
Q45644430	Lpt	"homem do clã Li, de Zhaozhou Pingji"
#   Q45644430: set the ca label
Q45644430	Lca	"home del clan Li, de Zhaozhou Pingji"
#   Q45644491 (李 of 趙州平棘): mul label = NN
Q45644491	Lmul	"NN"
#   Q45644491: set the nb label
Q45644491	Lnb	"mann av Li-slekten, fra Zhaozhou Pingji"
#   Q45644491: set the da label
Q45644491	Lda	"mand af Li-slægten, fra Zhaozhou Pingji"
#   Q45644491: set the sv label
Q45644491	Lsv	"man av Li-ätten, från Zhaozhou Pingji"
#   Q45644491: set the de label
Q45644491	Lde	"Mann des Klans Li, aus Zhaozhou Pingji"
#   Q45644491: set the es label
Q45644491	Les	"hombre del clan Li, de Zhaozhou Pingji"
#   Q45644491: set the it label
Q45644491	Lit	"uomo del clan Li, da Zhaozhou Pingji"
#   Q45644491: set the pt label
Q45644491	Lpt	"homem do clã Li, de Zhaozhou Pingji"
#   Q45644491: set the ca label
Q45644491	Lca	"home del clan Li, de Zhaozhou Pingji"
#   Q45644550 (李 of 趙州平棘): mul label = NN
Q45644550	Lmul	"NN"
#   Q45644550: set the nb label
Q45644550	Lnb	"mann av Li-slekten, fra Zhaozhou Pingji"
#   Q45644550: set the da label
Q45644550	Lda	"mand af Li-slægten, fra Zhaozhou Pingji"
#   Q45644550: set the sv label
Q45644550	Lsv	"man av Li-ätten, från Zhaozhou Pingji"
#   Q45644550: set the de label
Q45644550	Lde	"Mann des Klans Li, aus Zhaozhou Pingji"
#   Q45644550: set the es label
Q45644550	Les	"hombre del clan Li, de Zhaozhou Pingji"
#   Q45644550: set the it label
Q45644550	Lit	"uomo del clan Li, da Zhaozhou Pingji"
#   Q45644550: set the pt label
Q45644550	Lpt	"homem do clã Li, de Zhaozhou Pingji"
#   Q45644550: set the ca label
Q45644550	Lca	"home del clan Li, de Zhaozhou Pingji"
#   Q45645832 (李 of 河南): mul label = NN
Q45645832	Lmul	"NN"
#   Q45645832: set the nb label
Q45645832	Lnb	"mann av Li-slekten, fra Henan"
#   Q45645832: set the da label
Q45645832	Lda	"mand af Li-slægten, fra Henan"
#   Q45645832: set the sv label
Q45645832	Lsv	"man av Li-ätten, från Henan"
#   Q45645832: set the de label
Q45645832	Lde	"Mann des Klans Li, aus Henan"
#   Q45645832: set the es label
Q45645832	Les	"hombre del clan Li, de Henan"
#   Q45645832: set the it label
Q45645832	Lit	"uomo del clan Li, da Henan"
#   Q45645832: set the pt label
Q45645832	Lpt	"homem do clã Li, de Henan"
#   Q45645832: set the ca label
Q45645832	Lca	"home del clan Li, de Henan"
#   Q45645892 (李 of 河南): mul label = NN
Q45645892	Lmul	"NN"
#   Q45645892: set the nb label
Q45645892	Lnb	"mann av Li-slekten, fra Henan"
#   Q45645892: set the da label
Q45645892	Lda	"mand af Li-slægten, fra Henan"
#   Q45645892: set the sv label
Q45645892	Lsv	"man av Li-ätten, från Henan"
#   Q45645892: set the de label
Q45645892	Lde	"Mann des Klans Li, aus Henan"
#   Q45645892: set the es label
Q45645892	Les	"hombre del clan Li, de Henan"
#   Q45645892: set the it label
Q45645892	Lit	"uomo del clan Li, da Henan"
#   Q45645892: set the pt label
Q45645892	Lpt	"homem do clã Li, de Henan"
#   Q45645892: set the ca label
Q45645892	Lca	"home del clan Li, de Henan"
#   Q45645904 (裴 of 河東聞喜): mul label = NN
Q45645904	Lmul	"NN"
#   Q45645904: set the nb label
Q45645904	Lnb	"mann av Pei-slekten, fra Hedong Wenxi"
#   Q45645904: set the da label
Q45645904	Lda	"mand af Pei-slægten, fra Hedong Wenxi"
#   Q45645904: set the sv label
Q45645904	Lsv	"man av Pei-ätten, från Hedong Wenxi"
#   Q45645904: set the de label
Q45645904	Lde	"Mann des Klans Pei, aus Hedong Wenxi"
#   Q45645904: set the it label
Q45645904	Lit	"uomo del clan Pei, da Hedong Wenxi"
#   Q45645904: set the pt label
Q45645904	Lpt	"homem do clã Pei, de Hedong Wenxi"
#   Q45645904: set the ca label
Q45645904	Lca	"home del clan Pei, de Hedong Wenxi"
#   Q45645953 (李 of 河南): mul label = NN
Q45645953	Lmul	"NN"
#   Q45645953: set the nb label
Q45645953	Lnb	"mann av Li-slekten, fra Henan"
#   Q45645953: set the da label
Q45645953	Lda	"mand af Li-slægten, fra Henan"
#   Q45645953: set the sv label
Q45645953	Lsv	"man av Li-ätten, från Henan"
#   Q45645953: set the de label
Q45645953	Lde	"Mann des Klans Li, aus Henan"
#   Q45645953: set the es label
Q45645953	Les	"hombre del clan Li, de Henan"
#   Q45645953: set the it label
Q45645953	Lit	"uomo del clan Li, da Henan"
#   Q45645953: set the pt label
Q45645953	Lpt	"homem do clã Li, de Henan"
#   Q45645953: set the ca label
Q45645953	Lca	"home del clan Li, de Henan"
#   Q45646012 (李 of 河南): mul label = NN
Q45646012	Lmul	"NN"
#   Q45646012: set the nb label
Q45646012	Lnb	"mann av Li-slekten, fra Henan"
#   Q45646012: set the da label
Q45646012	Lda	"mand af Li-slægten, fra Henan"
#   Q45646012: set the sv label
Q45646012	Lsv	"man av Li-ätten, från Henan"
#   Q45646012: set the de label
Q45646012	Lde	"Mann des Klans Li, aus Henan"
#   Q45646012: set the es label
Q45646012	Les	"hombre del clan Li, de Henan"
#   Q45646012: set the it label
Q45646012	Lit	"uomo del clan Li, da Henan"
#   Q45646012: set the pt label
Q45646012	Lpt	"homem do clã Li, de Henan"
#   Q45646012: set the ca label
Q45646012	Lca	"home del clan Li, de Henan"
#   Q45646435 (李 of 趙州平棘): mul label = NN
Q45646435	Lmul	"NN"
#   Q45646435: set the nb label
Q45646435	Lnb	"mann av Li-slekten, fra Zhaozhou Pingji"
#   Q45646435: set the da label
Q45646435	Lda	"mand af Li-slægten, fra Zhaozhou Pingji"
#   Q45646435: set the sv label
Q45646435	Lsv	"man av Li-ätten, från Zhaozhou Pingji"
#   Q45646435: set the de label
Q45646435	Lde	"Mann des Klans Li, aus Zhaozhou Pingji"
#   Q45646435: set the es label
Q45646435	Les	"hombre del clan Li, de Zhaozhou Pingji"
#   Q45646435: set the it label
Q45646435	Lit	"uomo del clan Li, da Zhaozhou Pingji"
#   Q45646435: set the pt label
Q45646435	Lpt	"homem do clã Li, de Zhaozhou Pingji"
#   Q45646435: set the ca label
Q45646435	Lca	"home del clan Li, de Zhaozhou Pingji"
#   Q45646493 (李 of 趙州平棘): mul label = NN
Q45646493	Lmul	"NN"
#   Q45646493: set the nb label
Q45646493	Lnb	"mann av Li-slekten, fra Zhaozhou Pingji"
#   Q45646493: set the da label
Q45646493	Lda	"mand af Li-slægten, fra Zhaozhou Pingji"
#   Q45646493: set the sv label
Q45646493	Lsv	"man av Li-ätten, från Zhaozhou Pingji"
#   Q45646493: set the de label
Q45646493	Lde	"Mann des Klans Li, aus Zhaozhou Pingji"
#   Q45646493: set the es label
Q45646493	Les	"hombre del clan Li, de Zhaozhou Pingji"
#   Q45646493: set the it label
Q45646493	Lit	"uomo del clan Li, da Zhaozhou Pingji"
#   Q45646493: set the pt label
Q45646493	Lpt	"homem do clã Li, de Zhaozhou Pingji"
#   Q45646493: set the ca label
Q45646493	Lca	"home del clan Li, de Zhaozhou Pingji"
#   Q45646554 (李 of 趙州平棘): mul label = NN
Q45646554	Lmul	"NN"
#   Q45646554: set the nb label
Q45646554	Lnb	"mann av Li-slekten, fra Zhaozhou Pingji"
#   Q45646554: set the da label
Q45646554	Lda	"mand af Li-slægten, fra Zhaozhou Pingji"
#   Q45646554: set the sv label
Q45646554	Lsv	"man av Li-ätten, från Zhaozhou Pingji"
#   Q45646554: set the de label
Q45646554	Lde	"Mann des Klans Li, aus Zhaozhou Pingji"
#   Q45646554: set the es label
Q45646554	Les	"hombre del clan Li, de Zhaozhou Pingji"
#   Q45646554: set the it label
Q45646554	Lit	"uomo del clan Li, da Zhaozhou Pingji"
#   Q45646554: set the pt label
Q45646554	Lpt	"homem do clã Li, de Zhaozhou Pingji"
#   Q45646554: set the ca label
Q45646554	Lca	"home del clan Li, de Zhaozhou Pingji"
#   Q45646854 (李 of 滑州匡城): mul label = NN
Q45646854	Lmul	"NN"
#   Q45646854: set the nb label
Q45646854	Lnb	"mann av Li-slekten, fra Huazhou Kuangcheng"
#   Q45646854: set the da label
Q45646854	Lda	"mand af Li-slægten, fra Huazhou Kuangcheng"
#   Q45646854: set the sv label
Q45646854	Lsv	"man av Li-ätten, från Huazhou Kuangcheng"
#   Q45646854: set the de label
Q45646854	Lde	"Mann des Klans Li, aus Huazhou Kuangcheng"
#   Q45646854: set the es label
Q45646854	Les	"hombre del clan Li, de Huazhou Kuangcheng"
#   Q45646854: set the it label
Q45646854	Lit	"uomo del clan Li, da Huazhou Kuangcheng"
#   Q45646854: set the pt label
Q45646854	Lpt	"homem do clã Li, de Huazhou Kuangcheng"
#   Q45646854: set the ca label
Q45646854	Lca	"home del clan Li, de Huazhou Kuangcheng"
#   Q45646912 (李 of 滑州匡城): mul label = NN
Q45646912	Lmul	"NN"
#   Q45646912: set the nb label
Q45646912	Lnb	"mann av Li-slekten, fra Huazhou Kuangcheng"
#   Q45646912: set the da label
Q45646912	Lda	"mand af Li-slægten, fra Huazhou Kuangcheng"
#   Q45646912: set the sv label
Q45646912	Lsv	"man av Li-ätten, från Huazhou Kuangcheng"
#   Q45646912: set the de label
Q45646912	Lde	"Mann des Klans Li, aus Huazhou Kuangcheng"
#   Q45646912: set the es label
Q45646912	Les	"hombre del clan Li, de Huazhou Kuangcheng"
#   Q45646912: set the it label
Q45646912	Lit	"uomo del clan Li, da Huazhou Kuangcheng"
#   Q45646912: set the pt label
Q45646912	Lpt	"homem do clã Li, de Huazhou Kuangcheng"
#   Q45646912: set the ca label
Q45646912	Lca	"home del clan Li, de Huazhou Kuangcheng"
#   Q45646972 (李 of 滑州匡城): mul label = NN
Q45646972	Lmul	"NN"
#   Q45646972: set the nb label
Q45646972	Lnb	"mann av Li-slekten, fra Huazhou Kuangcheng"
#   Q45646972: set the da label
Q45646972	Lda	"mand af Li-slægten, fra Huazhou Kuangcheng"
#   Q45646972: set the sv label
Q45646972	Lsv	"man av Li-ätten, från Huazhou Kuangcheng"
#   Q45646972: set the de label
Q45646972	Lde	"Mann des Klans Li, aus Huazhou Kuangcheng"
#   Q45646972: set the es label
Q45646972	Les	"hombre del clan Li, de Huazhou Kuangcheng"
#   Q45646972: set the it label
Q45646972	Lit	"uomo del clan Li, da Huazhou Kuangcheng"
#   Q45646972: set the pt label
Q45646972	Lpt	"homem do clã Li, de Huazhou Kuangcheng"
#   Q45646972: set the ca label
Q45646972	Lca	"home del clan Li, de Huazhou Kuangcheng"
#   Q45647031 (李 of 滑州匡城): mul label = NN
Q45647031	Lmul	"NN"
#   Q45647031: set the nb label
Q45647031	Lnb	"mann av Li-slekten, fra Huazhou Kuangcheng"
#   Q45647031: set the da label
Q45647031	Lda	"mand af Li-slægten, fra Huazhou Kuangcheng"
#   Q45647031: set the sv label
Q45647031	Lsv	"man av Li-ätten, från Huazhou Kuangcheng"
#   Q45647031: set the de label
Q45647031	Lde	"Mann des Klans Li, aus Huazhou Kuangcheng"
#   Q45647031: set the es label
Q45647031	Les	"hombre del clan Li, de Huazhou Kuangcheng"
#   Q45647031: set the it label
Q45647031	Lit	"uomo del clan Li, da Huazhou Kuangcheng"
#   Q45647031: set the pt label
Q45647031	Lpt	"homem do clã Li, de Huazhou Kuangcheng"
#   Q45647031: set the ca label
Q45647031	Lca	"home del clan Li, de Huazhou Kuangcheng"
#   Q45647089 (李 of 滑州匡城): mul label = NN
Q45647089	Lmul	"NN"
#   Q45647089: set the nb label
Q45647089	Lnb	"mann av Li-slekten, fra Huazhou Kuangcheng"
#   Q45647089: set the da label
Q45647089	Lda	"mand af Li-slægten, fra Huazhou Kuangcheng"
#   Q45647089: set the sv label
Q45647089	Lsv	"man av Li-ätten, från Huazhou Kuangcheng"
#   Q45647089: set the de label
Q45647089	Lde	"Mann des Klans Li, aus Huazhou Kuangcheng"
#   Q45647089: set the es label
Q45647089	Les	"hombre del clan Li, de Huazhou Kuangcheng"
#   Q45647089: set the it label
Q45647089	Lit	"uomo del clan Li, da Huazhou Kuangcheng"
#   Q45647089: set the pt label
Q45647089	Lpt	"homem do clã Li, de Huazhou Kuangcheng"
#   Q45647089: set the ca label
Q45647089	Lca	"home del clan Li, de Huazhou Kuangcheng"
#   Q45647334 (李 of 滑州匡城): mul label = NN
Q45647334	Lmul	"NN"
#   Q45647334: set the nb label
Q45647334	Lnb	"mann av Li-slekten, fra Huazhou Kuangcheng"
#   Q45647334: set the da label
Q45647334	Lda	"mand af Li-slægten, fra Huazhou Kuangcheng"
#   Q45647334: set the sv label
Q45647334	Lsv	"man av Li-ätten, från Huazhou Kuangcheng"
#   Q45647334: set the de label
Q45647334	Lde	"Mann des Klans Li, aus Huazhou Kuangcheng"
#   Q45647334: set the es label
Q45647334	Les	"hombre del clan Li, de Huazhou Kuangcheng"
#   Q45647334: set the it label
Q45647334	Lit	"uomo del clan Li, da Huazhou Kuangcheng"
#   Q45647334: set the pt label
Q45647334	Lpt	"homem do clã Li, de Huazhou Kuangcheng"
#   Q45647334: set the ca label
Q45647334	Lca	"home del clan Li, de Huazhou Kuangcheng"
#   Q45647512 (李 of 滑州匡城): mul label = NN
Q45647512	Lmul	"NN"
#   Q45647512: set the nb label
Q45647512	Lnb	"mann av Li-slekten, fra Huazhou Kuangcheng"
#   Q45647512: set the da label
Q45647512	Lda	"mand af Li-slægten, fra Huazhou Kuangcheng"
#   Q45647512: set the sv label
Q45647512	Lsv	"man av Li-ätten, från Huazhou Kuangcheng"
#   Q45647512: set the de label
Q45647512	Lde	"Mann des Klans Li, aus Huazhou Kuangcheng"
#   Q45647512: set the es label
Q45647512	Les	"hombre del clan Li, de Huazhou Kuangcheng"
#   Q45647512: set the it label
Q45647512	Lit	"uomo del clan Li, da Huazhou Kuangcheng"
#   Q45647512: set the pt label
Q45647512	Lpt	"homem do clã Li, de Huazhou Kuangcheng"
#   Q45647512: set the ca label
Q45647512	Lca	"home del clan Li, de Huazhou Kuangcheng"
#   Q45647926 (李 of 河南): mul label = NN
Q45647926	Lmul	"NN"
#   Q45647926: set the nb label
Q45647926	Lnb	"mann av Li-slekten, fra Henan"
#   Q45647926: set the da label
Q45647926	Lda	"mand af Li-slægten, fra Henan"
#   Q45647926: set the sv label
Q45647926	Lsv	"man av Li-ätten, från Henan"
#   Q45647926: set the de label
Q45647926	Lde	"Mann des Klans Li, aus Henan"
#   Q45647926: set the es label
Q45647926	Les	"hombre del clan Li, de Henan"
#   Q45647926: set the it label
Q45647926	Lit	"uomo del clan Li, da Henan"
#   Q45647926: set the pt label
Q45647926	Lpt	"homem do clã Li, de Henan"
#   Q45647926: set the ca label
Q45647926	Lca	"home del clan Li, de Henan"
#   Q45648222 (李 of 河南洛陽): mul label = NN
Q45648222	Lmul	"NN"
#   Q45648222: set the nb label
Q45648222	Lnb	"mann av Li-slekten, fra Henan Luoyang"
#   Q45648222: set the da label
Q45648222	Lda	"mand af Li-slægten, fra Henan Luoyang"
#   Q45648222: set the sv label
Q45648222	Lsv	"man av Li-ätten, från Henan Luoyang"
#   Q45648222: set the de label
Q45648222	Lde	"Mann des Klans Li, aus Henan Luoyang"
#   Q45648222: set the es label
Q45648222	Les	"hombre del clan Li, de Henan Luoyang"
#   Q45648222: set the it label
Q45648222	Lit	"uomo del clan Li, da Henan Luoyang"
#   Q45648222: set the pt label
Q45648222	Lpt	"homem do clã Li, de Henan Luoyang"
#   Q45648222: set the ca label
Q45648222	Lca	"home del clan Li, de Henan Luoyang"
#   Q45648878 (薛 of 蒲州寶鼎): mul label = NN
Q45648878	Lmul	"NN"
#   Q45648878: set the nb label
Q45648878	Lnb	"mann av Xue-slekten, fra Puzhou Baoding"
#   Q45648878: set the da label
Q45648878	Lda	"mand af Xue-slægten, fra Puzhou Baoding"
#   Q45648878: set the sv label
Q45648878	Lsv	"man av Xue-ätten, från Puzhou Baoding"
#   Q45648878: set the de label
Q45648878	Lde	"Mann des Klans Xue, aus Puzhou Baoding"
#   Q45648878: set the it label
Q45648878	Lit	"uomo del clan Xue, da Puzhou Baoding"
#   Q45648878: set the pt label
Q45648878	Lpt	"homem do clã Xue, de Puzhou Baoding"
#   Q45648878: set the ca label
Q45648878	Lca	"home del clan Xue, de Puzhou Baoding"
#   Q45648938 (薛 of 蒲州寶鼎): mul label = NN
Q45648938	Lmul	"NN"
#   Q45648938: set the nb label
Q45648938	Lnb	"mann av Xue-slekten, fra Puzhou Baoding"
#   Q45648938: set the da label
Q45648938	Lda	"mand af Xue-slægten, fra Puzhou Baoding"
#   Q45648938: set the sv label
Q45648938	Lsv	"man av Xue-ätten, från Puzhou Baoding"
#   Q45648938: set the de label
Q45648938	Lde	"Mann des Klans Xue, aus Puzhou Baoding"
#   Q45648938: set the it label
Q45648938	Lit	"uomo del clan Xue, da Puzhou Baoding"
#   Q45648938: set the pt label
Q45648938	Lpt	"homem do clã Xue, de Puzhou Baoding"
#   Q45648938: set the ca label
Q45648938	Lca	"home del clan Xue, de Puzhou Baoding"
#   Q45649066 (李 of 河南): mul label = NN
Q45649066	Lmul	"NN"
#   Q45649066: set the nb label
Q45649066	Lnb	"mann av Li-slekten, fra Henan"
#   Q45649066: set the da label
Q45649066	Lda	"mand af Li-slægten, fra Henan"
#   Q45649066: set the sv label
Q45649066	Lsv	"man av Li-ätten, från Henan"
#   Q45649066: set the de label
Q45649066	Lde	"Mann des Klans Li, aus Henan"
#   Q45649066: set the es label
Q45649066	Les	"hombre del clan Li, de Henan"
#   Q45649066: set the it label
Q45649066	Lit	"uomo del clan Li, da Henan"
#   Q45649066: set the pt label
Q45649066	Lpt	"homem do clã Li, de Henan"
#   Q45649066: set the ca label
Q45649066	Lca	"home del clan Li, de Henan"
#   Q45649184 (李 of 趙州平棘): mul label = NN
Q45649184	Lmul	"NN"
#   Q45649184: set the nb label
Q45649184	Lnb	"mann av Li-slekten, fra Zhaozhou Pingji"
#   Q45649184: set the da label
Q45649184	Lda	"mand af Li-slægten, fra Zhaozhou Pingji"
#   Q45649184: set the sv label
Q45649184	Lsv	"man av Li-ätten, från Zhaozhou Pingji"
#   Q45649184: set the de label
Q45649184	Lde	"Mann des Klans Li, aus Zhaozhou Pingji"
#   Q45649184: set the es label
Q45649184	Les	"hombre del clan Li, de Zhaozhou Pingji"
#   Q45649184: set the it label
Q45649184	Lit	"uomo del clan Li, da Zhaozhou Pingji"
#   Q45649184: set the pt label
Q45649184	Lpt	"homem do clã Li, de Zhaozhou Pingji"
#   Q45649184: set the ca label
Q45649184	Lca	"home del clan Li, de Zhaozhou Pingji"
#   Q45650019 (李 of 趙州平棘): mul label = NN
Q45650019	Lmul	"NN"
#   Q45650019: set the nb label
Q45650019	Lnb	"mann av Li-slekten, fra Zhaozhou Pingji"
#   Q45650019: set the da label
Q45650019	Lda	"mand af Li-slægten, fra Zhaozhou Pingji"
#   Q45650019: set the sv label
Q45650019	Lsv	"man av Li-ätten, från Zhaozhou Pingji"
#   Q45650019: set the de label
Q45650019	Lde	"Mann des Klans Li, aus Zhaozhou Pingji"
#   Q45650019: set the es label
Q45650019	Les	"hombre del clan Li, de Zhaozhou Pingji"
#   Q45650019: set the it label
Q45650019	Lit	"uomo del clan Li, da Zhaozhou Pingji"
#   Q45650019: set the pt label
Q45650019	Lpt	"homem do clã Li, de Zhaozhou Pingji"
#   Q45650019: set the ca label
Q45650019	Lca	"home del clan Li, de Zhaozhou Pingji"
#   Q45651316 (薛 of 河南洛陽): mul label = NN
Q45651316	Lmul	"NN"
#   Q45651316: set the nb label
Q45651316	Lnb	"mann av Xue-slekten, fra Henan Luoyang"
#   Q45651316: set the da label
Q45651316	Lda	"mand af Xue-slægten, fra Henan Luoyang"
#   Q45651316: set the sv label
Q45651316	Lsv	"man av Xue-ätten, från Henan Luoyang"
#   Q45651316: set the de label
Q45651316	Lde	"Mann des Klans Xue, aus Henan Luoyang"
#   Q45651316: set the it label
Q45651316	Lit	"uomo del clan Xue, da Henan Luoyang"
#   Q45651316: set the pt label
Q45651316	Lpt	"homem do clã Xue, de Henan Luoyang"
#   Q45651316: set the ca label
Q45651316	Lca	"home del clan Xue, de Henan Luoyang"
#   Q45651377 (薛 of 河南洛陽): mul label = NN
Q45651377	Lmul	"NN"
#   Q45651377: set the nb label
Q45651377	Lnb	"mann av Xue-slekten, fra Henan Luoyang"
#   Q45651377: set the da label
Q45651377	Lda	"mand af Xue-slægten, fra Henan Luoyang"
#   Q45651377: set the sv label
Q45651377	Lsv	"man av Xue-ätten, från Henan Luoyang"
#   Q45651377: set the de label
Q45651377	Lde	"Mann des Klans Xue, aus Henan Luoyang"
#   Q45651377: set the it label
Q45651377	Lit	"uomo del clan Xue, da Henan Luoyang"
#   Q45651377: set the pt label
Q45651377	Lpt	"homem do clã Xue, de Henan Luoyang"
#   Q45651377: set the ca label
Q45651377	Lca	"home del clan Xue, de Henan Luoyang"
#   Q45655203 (鄭 of 河南府): mul label = NN
Q45655203	Lmul	"NN"
#   Q45655203: set the nb label
Q45655203	Lnb	"mann av Zheng-slekten, fra Henan Prefecture"
#   Q45655203: set the da label
Q45655203	Lda	"mand af Zheng-slægten, fra Henan Prefecture"
#   Q45655203: set the sv label
Q45655203	Lsv	"man av Zheng-ätten, från Henan Prefecture"
#   Q45655203: set the de label
Q45655203	Lde	"Mann des Klans Zheng, aus Henan Prefecture"
#   Q45655203: set the it label
Q45655203	Lit	"uomo del clan Zheng, da Henan Prefecture"
#   Q45655203: set the pt label
Q45655203	Lpt	"homem do clã Zheng, de Henan Prefecture"
#   Q45655203: set the ca label
Q45655203	Lca	"home del clan Zheng, de Henan Prefecture"
#   Q45655848 (李 of 京兆府): mul label = NN
Q45655848	Lmul	"NN"
#   Q45655848: set the nb label
Q45655848	Lnb	"mann av Li-slekten, fra Jingzhao Prefecture"
#   Q45655848: set the da label
Q45655848	Lda	"mand af Li-slægten, fra Jingzhao Prefecture"
#   Q45655848: set the sv label
Q45655848	Lsv	"man av Li-ätten, från Jingzhao Prefecture"
#   Q45655848: set the de label
Q45655848	Lde	"Mann des Klans Li, aus Jingzhao Prefecture"
#   Q45655848: set the es label
Q45655848	Les	"hombre del clan Li, de Jingzhao Prefecture"
#   Q45655848: set the it label
Q45655848	Lit	"uomo del clan Li, da Jingzhao Prefecture"
#   Q45655848: set the pt label
Q45655848	Lpt	"homem do clã Li, de Jingzhao Prefecture"
#   Q45655848: set the ca label
Q45655848	Lca	"home del clan Li, de Jingzhao Prefecture"
#   Q45657616 (韋 of 京兆杜陵): mul label = NN
Q45657616	Lmul	"NN"
#   Q45657616: set the nb label
Q45657616	Lnb	"mann av Wei-slekten, fra Jingzhao Duling"
#   Q45657616: set the da label
Q45657616	Lda	"mand af Wei-slægten, fra Jingzhao Duling"
#   Q45657616: set the sv label
Q45657616	Lsv	"man av Wei-ätten, från Jingzhao Duling"
#   Q45657616: set the de label
Q45657616	Lde	"Mann des Klans Wei, aus Jingzhao Duling"
#   Q45657616: set the it label
Q45657616	Lit	"uomo del clan Wei, da Jingzhao Duling"
#   Q45657616: set the pt label
Q45657616	Lpt	"homem do clã Wei, de Jingzhao Duling"
#   Q45657616: set the ca label
Q45657616	Lca	"home del clan Wei, de Jingzhao Duling"
#   Q45657676 (韋 of 京兆杜陵): mul label = NN
Q45657676	Lmul	"NN"
#   Q45657676: set the nb label
Q45657676	Lnb	"mann av Wei-slekten, fra Jingzhao Duling"
#   Q45657676: set the da label
Q45657676	Lda	"mand af Wei-slægten, fra Jingzhao Duling"
#   Q45657676: set the sv label
Q45657676	Lsv	"man av Wei-ätten, från Jingzhao Duling"
#   Q45657676: set the de label
Q45657676	Lde	"Mann des Klans Wei, aus Jingzhao Duling"
#   Q45657676: set the it label
Q45657676	Lit	"uomo del clan Wei, da Jingzhao Duling"
#   Q45657676: set the pt label
Q45657676	Lpt	"homem do clã Wei, de Jingzhao Duling"
#   Q45657676: set the ca label
Q45657676	Lca	"home del clan Wei, de Jingzhao Duling"
#   Q45659526 (韋 of 京兆杜陵): mul label = NN
Q45659526	Lmul	"NN"
#   Q45659526: set the nb label
Q45659526	Lnb	"mann av Wei-slekten, fra Jingzhao Duling"
#   Q45659526: set the da label
Q45659526	Lda	"mand af Wei-slægten, fra Jingzhao Duling"
#   Q45659526: set the sv label
Q45659526	Lsv	"man av Wei-ätten, från Jingzhao Duling"
#   Q45659526: set the de label
Q45659526	Lde	"Mann des Klans Wei, aus Jingzhao Duling"
#   Q45659526: set the it label
Q45659526	Lit	"uomo del clan Wei, da Jingzhao Duling"
#   Q45659526: set the pt label
Q45659526	Lpt	"homem do clã Wei, de Jingzhao Duling"
#   Q45659526: set the ca label
Q45659526	Lca	"home del clan Wei, de Jingzhao Duling"
#   Q45659585 (韋 of 京兆杜陵): mul label = NN
Q45659585	Lmul	"NN"
#   Q45659585: set the nb label
Q45659585	Lnb	"mann av Wei-slekten, fra Jingzhao Duling"
#   Q45659585: set the da label
Q45659585	Lda	"mand af Wei-slægten, fra Jingzhao Duling"
#   Q45659585: set the sv label
Q45659585	Lsv	"man av Wei-ätten, från Jingzhao Duling"
#   Q45659585: set the de label
Q45659585	Lde	"Mann des Klans Wei, aus Jingzhao Duling"
#   Q45659585: set the it label
Q45659585	Lit	"uomo del clan Wei, da Jingzhao Duling"
#   Q45659585: set the pt label
Q45659585	Lpt	"homem do clã Wei, de Jingzhao Duling"
#   Q45659585: set the ca label
Q45659585	Lca	"home del clan Wei, de Jingzhao Duling"
#   Q45659766 (韋 of 京兆杜陵): mul label = NN
Q45659766	Lmul	"NN"
#   Q45659766: set the nb label
Q45659766	Lnb	"mann av Wei-slekten, fra Jingzhao Duling"
#   Q45659766: set the da label
Q45659766	Lda	"mand af Wei-slægten, fra Jingzhao Duling"
#   Q45659766: set the sv label
Q45659766	Lsv	"man av Wei-ätten, från Jingzhao Duling"
#   Q45659766: set the de label
Q45659766	Lde	"Mann des Klans Wei, aus Jingzhao Duling"
#   Q45659766: set the it label
Q45659766	Lit	"uomo del clan Wei, da Jingzhao Duling"
#   Q45659766: set the pt label
Q45659766	Lpt	"homem do clã Wei, de Jingzhao Duling"
#   Q45659766: set the ca label
Q45659766	Lca	"home del clan Wei, de Jingzhao Duling"
#   Q45660005 (韋 of 京兆杜陵): mul label = NN
Q45660005	Lmul	"NN"
#   Q45660005: set the nb label
Q45660005	Lnb	"mann av Wei-slekten, fra Jingzhao Duling"
#   Q45660005: set the da label
Q45660005	Lda	"mand af Wei-slægten, fra Jingzhao Duling"
#   Q45660005: set the sv label
Q45660005	Lsv	"man av Wei-ätten, från Jingzhao Duling"
#   Q45660005: set the de label
Q45660005	Lde	"Mann des Klans Wei, aus Jingzhao Duling"
#   Q45660005: set the it label
Q45660005	Lit	"uomo del clan Wei, da Jingzhao Duling"
#   Q45660005: set the pt label
Q45660005	Lpt	"homem do clã Wei, de Jingzhao Duling"
#   Q45660005: set the ca label
Q45660005	Lca	"home del clan Wei, de Jingzhao Duling"
#   Q45660063 (韋 of 京兆杜陵): mul label = NN
Q45660063	Lmul	"NN"
#   Q45660063: set the nb label
Q45660063	Lnb	"mann av Wei-slekten, fra Jingzhao Duling"
#   Q45660063: set the da label
Q45660063	Lda	"mand af Wei-slægten, fra Jingzhao Duling"
#   Q45660063: set the sv label
Q45660063	Lsv	"man av Wei-ätten, från Jingzhao Duling"
#   Q45660063: set the de label
Q45660063	Lde	"Mann des Klans Wei, aus Jingzhao Duling"
#   Q45660063: set the it label
Q45660063	Lit	"uomo del clan Wei, da Jingzhao Duling"
#   Q45660063: set the pt label
Q45660063	Lpt	"homem do clã Wei, de Jingzhao Duling"
#   Q45660063: set the ca label
Q45660063	Lca	"home del clan Wei, de Jingzhao Duling"
#   Q45660721 (韋 of 京兆杜陵): mul label = NN
Q45660721	Lmul	"NN"
#   Q45660721: set the nb label
Q45660721	Lnb	"mann av Wei-slekten, fra Jingzhao Duling"
#   Q45660721: set the da label
Q45660721	Lda	"mand af Wei-slægten, fra Jingzhao Duling"
#   Q45660721: set the sv label
Q45660721	Lsv	"man av Wei-ätten, från Jingzhao Duling"
#   Q45660721: set the de label
Q45660721	Lde	"Mann des Klans Wei, aus Jingzhao Duling"
#   Q45660721: set the it label
Q45660721	Lit	"uomo del clan Wei, da Jingzhao Duling"
#   Q45660721: set the pt label
Q45660721	Lpt	"homem do clã Wei, de Jingzhao Duling"
#   Q45660721: set the ca label
Q45660721	Lca	"home del clan Wei, de Jingzhao Duling"
#   Q45660780 (韋 of 京兆杜陵): mul label = NN
Q45660780	Lmul	"NN"
#   Q45660780: set the nb label
Q45660780	Lnb	"mann av Wei-slekten, fra Jingzhao Duling"
#   Q45660780: set the da label
Q45660780	Lda	"mand af Wei-slægten, fra Jingzhao Duling"
#   Q45660780: set the sv label
Q45660780	Lsv	"man av Wei-ätten, från Jingzhao Duling"
#   Q45660780: set the de label
Q45660780	Lde	"Mann des Klans Wei, aus Jingzhao Duling"
#   Q45660780: set the it label
Q45660780	Lit	"uomo del clan Wei, da Jingzhao Duling"
#   Q45660780: set the pt label
Q45660780	Lpt	"homem do clã Wei, de Jingzhao Duling"
#   Q45660780: set the ca label
Q45660780	Lca	"home del clan Wei, de Jingzhao Duling"
#   Q45660841 (韋 of 京兆杜陵): mul label = NN
Q45660841	Lmul	"NN"
#   Q45660841: set the nb label
Q45660841	Lnb	"mann av Wei-slekten, fra Jingzhao Duling"
#   Q45660841: set the da label
Q45660841	Lda	"mand af Wei-slægten, fra Jingzhao Duling"
#   Q45660841: set the sv label
Q45660841	Lsv	"man av Wei-ätten, från Jingzhao Duling"
#   Q45660841: set the de label
Q45660841	Lde	"Mann des Klans Wei, aus Jingzhao Duling"
#   Q45660841: set the it label
Q45660841	Lit	"uomo del clan Wei, da Jingzhao Duling"
#   Q45660841: set the pt label
Q45660841	Lpt	"homem do clã Wei, de Jingzhao Duling"
#   Q45660841: set the ca label
Q45660841	Lca	"home del clan Wei, de Jingzhao Duling"
#   Q45664697 (韋 of 京兆杜陵): mul label = NN
Q45664697	Lmul	"NN"
#   Q45664697: set the nb label
Q45664697	Lnb	"mann av Wei-slekten, fra Jingzhao Duling"
#   Q45664697: set the da label
Q45664697	Lda	"mand af Wei-slægten, fra Jingzhao Duling"
#   Q45664697: set the sv label
Q45664697	Lsv	"man av Wei-ätten, från Jingzhao Duling"
#   Q45664697: set the de label
Q45664697	Lde	"Mann des Klans Wei, aus Jingzhao Duling"
#   Q45664697: set the it label
Q45664697	Lit	"uomo del clan Wei, da Jingzhao Duling"
#   Q45664697: set the pt label
Q45664697	Lpt	"homem do clã Wei, de Jingzhao Duling"
#   Q45664697: set the ca label
Q45664697	Lca	"home del clan Wei, de Jingzhao Duling"
#   Q45664752 (韋 of 京兆杜陵): mul label = NN
Q45664752	Lmul	"NN"
#   Q45664752: set the nb label
Q45664752	Lnb	"mann av Wei-slekten, fra Jingzhao Duling"
#   Q45664752: set the da label
Q45664752	Lda	"mand af Wei-slægten, fra Jingzhao Duling"
#   Q45664752: set the sv label
Q45664752	Lsv	"man av Wei-ätten, från Jingzhao Duling"
#   Q45664752: set the de label
Q45664752	Lde	"Mann des Klans Wei, aus Jingzhao Duling"
#   Q45664752: set the it label
Q45664752	Lit	"uomo del clan Wei, da Jingzhao Duling"
#   Q45664752: set the pt label
Q45664752	Lpt	"homem do clã Wei, de Jingzhao Duling"
#   Q45664752: set the ca label
Q45664752	Lca	"home del clan Wei, de Jingzhao Duling"
#   Q45678944 (郭 of 太原): mul label = NN
Q45678944	Lmul	"NN"
#   Q45678944: set the nb label
Q45678944	Lnb	"mann av Guo-slekten, fra Taiyuan"
#   Q45678944: set the da label
Q45678944	Lda	"mand af Guo-slægten, fra Taiyuan"
#   Q45678944: set the sv label
Q45678944	Lsv	"man av Guo-ätten, från Taiyuan"
#   Q45678944: set the de label
Q45678944	Lde	"Mann des Klans Guo, aus Taiyuan"
#   Q45678944: set the it label
Q45678944	Lit	"uomo del clan Guo, da Taiyuan"
#   Q45678944: set the pt label
Q45678944	Lpt	"homem do clã Guo, de Taiyuan"
#   Q45678944: set the ca label
Q45678944	Lca	"home del clan Guo, de Taiyuan"
#   Q45682618 (武 of 太原文水): mul label = NN
Q45682618	Lmul	"NN"
#   Q45682618: set the nb label
Q45682618	Lnb	"mann av Wu-slekten, fra Taiyuan Wenshui"
#   Q45682618: set the da label
Q45682618	Lda	"mand af Wu-slægten, fra Taiyuan Wenshui"
#   Q45682618: set the sv label
Q45682618	Lsv	"man av Wu-ätten, från Taiyuan Wenshui"
#   Q45682618: set the de label
Q45682618	Lde	"Mann des Klans Wu, aus Taiyuan Wenshui"
#   Q45682618: set the it label
Q45682618	Lit	"uomo del clan Wu, da Taiyuan Wenshui"
#   Q45682618: set the pt label
Q45682618	Lpt	"homem do clã Wu, de Taiyuan Wenshui"
#   Q45682618: set the ca label
Q45682618	Lca	"home del clan Wu, de Taiyuan Wenshui"
#   Q45684235 (蘇 of 京兆萬年): mul label = NN
Q45684235	Lmul	"NN"
#   Q45684235: set the nb label
Q45684235	Lnb	"mann av Su-slekten, fra Jingzhao Wannian"
#   Q45684235: set the da label
Q45684235	Lda	"mand af Su-slægten, fra Jingzhao Wannian"
#   Q45684235: set the sv label
Q45684235	Lsv	"man av Su-ätten, från Jingzhao Wannian"
#   Q45684235: set the de label
Q45684235	Lde	"Mann des Klans Su, aus Jingzhao Wannian"
#   Q45684235: set the es label
Q45684235	Les	"hombre del clan Su, de Jingzhao Wannian"
#   Q45684235: set the it label
Q45684235	Lit	"uomo del clan Su, da Jingzhao Wannian"
#   Q45684235: set the pt label
Q45684235	Lpt	"homem do clã Su, de Jingzhao Wannian"
#   Q45684235: set the ca label
Q45684235	Lca	"home del clan Su, de Jingzhao Wannian"
#   Q45685725 (張 of 襄州襄陽): mul label = NN
Q45685725	Lmul	"NN"
#   Q45685725: set the nb label
Q45685725	Lnb	"mann av Zhang-slekten, fra Xiangzhou Xiangyang"
#   Q45685725: set the da label
Q45685725	Lda	"mand af Zhang-slægten, fra Xiangzhou Xiangyang"
#   Q45685725: set the sv label
Q45685725	Lsv	"man av Zhang-ätten, från Xiangzhou Xiangyang"
#   Q45685725: set the de label
Q45685725	Lde	"Mann des Klans Zhang, aus Xiangzhou Xiangyang"
#   Q45685725: set the it label
Q45685725	Lit	"uomo del clan Zhang, da Xiangzhou Xiangyang"
#   Q45685725: set the pt label
Q45685725	Lpt	"homem do clã Zhang, de Xiangzhou Xiangyang"
#   Q45685725: set the ca label
Q45685725	Lca	"home del clan Zhang, de Xiangzhou Xiangyang"
#   Q45685758 (張 of 襄州襄陽): mul label = NN
Q45685758	Lmul	"NN"
#   Q45685758: set the nb label
Q45685758	Lnb	"mann av Zhang-slekten, fra Xiangzhou Xiangyang"
#   Q45685758: set the da label
Q45685758	Lda	"mand af Zhang-slægten, fra Xiangzhou Xiangyang"
#   Q45685758: set the sv label
Q45685758	Lsv	"man av Zhang-ätten, från Xiangzhou Xiangyang"
#   Q45685758: set the de label
Q45685758	Lde	"Mann des Klans Zhang, aus Xiangzhou Xiangyang"
#   Q45685758: set the it label
Q45685758	Lit	"uomo del clan Zhang, da Xiangzhou Xiangyang"
#   Q45685758: set the pt label
Q45685758	Lpt	"homem do clã Zhang, de Xiangzhou Xiangyang"
#   Q45685758: set the ca label
Q45685758	Lca	"home del clan Zhang, de Xiangzhou Xiangyang"
#   Q45686328 (李 of 隴西狄道): mul label = NN
Q45686328	Lmul	"NN"
#   Q45686328: set the nb label
Q45686328	Lnb	"kvinne av Li-slekten, fra Longxi Didao"
#   Q45686328: set the da label
Q45686328	Lda	"kvinde af Li-slægten, fra Longxi Didao"
#   Q45686328: set the sv label
Q45686328	Lsv	"kvinna av Li-ätten, från Longxi Didao"
#   Q45686328: set the de label
Q45686328	Lde	"Frau des Klans Li, aus Longxi Didao"
#   Q45686328: set the es label
Q45686328	Les	"mujer del clan Li, de Longxi Didao"
#   Q45686328: set the it label
Q45686328	Lit	"donna del clan Li, da Longxi Didao"
#   Q45686328: set the pt label
Q45686328	Lpt	"mulher do clã Li, de Longxi Didao"
#   Q45686328: set the ca label
Q45686328	Lca	"dona del clan Li, de Longxi Didao"
#   Q45691897 (李 of 隴西狄道): mul label = NN
Q45691897	Lmul	"NN"
#   Q45691897: set the nb label
Q45691897	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45691897: set the da label
Q45691897	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45691897: set the sv label
Q45691897	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45691897: set the de label
Q45691897	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45691897: set the es label
Q45691897	Les	"hombre del clan Li, de Longxi Didao"
#   Q45691897: set the it label
Q45691897	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45691897: set the pt label
Q45691897	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45691897: set the ca label
Q45691897	Lca	"home del clan Li, de Longxi Didao"
#   Q45692090 (李 of 隴西狄道): mul label = NN
Q45692090	Lmul	"NN"
#   Q45692090: set the nb label
Q45692090	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45692090: set the da label
Q45692090	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45692090: set the sv label
Q45692090	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45692090: set the de label
Q45692090	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45692090: set the es label
Q45692090	Les	"hombre del clan Li, de Longxi Didao"
#   Q45692090: set the it label
Q45692090	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45692090: set the pt label
Q45692090	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45692090: set the ca label
Q45692090	Lca	"home del clan Li, de Longxi Didao"
#   Q45692318 (李 of 隴西狄道): mul label = NN
Q45692318	Lmul	"NN"
#   Q45692318: set the nb label
Q45692318	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45692318: set the da label
Q45692318	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45692318: set the sv label
Q45692318	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45692318: set the de label
Q45692318	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45692318: set the es label
Q45692318	Les	"hombre del clan Li, de Longxi Didao"
#   Q45692318: set the it label
Q45692318	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45692318: set the pt label
Q45692318	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45692318: set the ca label
Q45692318	Lca	"home del clan Li, de Longxi Didao"
#   Q45692515 (李 of 隴西狄道): mul label = NN
Q45692515	Lmul	"NN"
#   Q45692515: set the nb label
Q45692515	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45692515: set the da label
Q45692515	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45692515: set the sv label
Q45692515	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45692515: set the de label
Q45692515	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45692515: set the es label
Q45692515	Les	"hombre del clan Li, de Longxi Didao"
#   Q45692515: set the it label
Q45692515	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45692515: set the pt label
Q45692515	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45692515: set the ca label
Q45692515	Lca	"home del clan Li, de Longxi Didao"
#   Q45692573 (李 of 隴西狄道): mul label = NN
Q45692573	Lmul	"NN"
#   Q45692573: set the nb label
Q45692573	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45692573: set the da label
Q45692573	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45692573: set the sv label
Q45692573	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45692573: set the de label
Q45692573	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45692573: set the es label
Q45692573	Les	"hombre del clan Li, de Longxi Didao"
#   Q45692573: set the it label
Q45692573	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45692573: set the pt label
Q45692573	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45692573: set the ca label
Q45692573	Lca	"home del clan Li, de Longxi Didao"
#   Q45692881 (李 of 隴西狄道): mul label = NN
Q45692881	Lmul	"NN"
#   Q45692881: set the nb label
Q45692881	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45692881: set the da label
Q45692881	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45692881: set the sv label
Q45692881	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45692881: set the de label
Q45692881	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45692881: set the es label
Q45692881	Les	"hombre del clan Li, de Longxi Didao"
#   Q45692881: set the it label
Q45692881	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45692881: set the pt label
Q45692881	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45692881: set the ca label
Q45692881	Lca	"home del clan Li, de Longxi Didao"
#   Q45692909 (李 of 隴西狄道): mul label = NN
Q45692909	Lmul	"NN"
#   Q45692909: set the nb label
Q45692909	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45692909: set the da label
Q45692909	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45692909: set the sv label
Q45692909	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45692909: set the de label
Q45692909	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45692909: set the es label
Q45692909	Les	"hombre del clan Li, de Longxi Didao"
#   Q45692909: set the it label
Q45692909	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45692909: set the pt label
Q45692909	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45692909: set the ca label
Q45692909	Lca	"home del clan Li, de Longxi Didao"
#   Q45692937 (李 of 秦州成紀): mul label = NN
Q45692937	Lmul	"NN"
#   Q45692937: set the nb label
Q45692937	Lnb	"mann av Li-slekten, fra Qinzhou Chengji"
#   Q45692937: set the da label
Q45692937	Lda	"mand af Li-slægten, fra Qinzhou Chengji"
#   Q45692937: set the sv label
Q45692937	Lsv	"man av Li-ätten, från Qinzhou Chengji"
#   Q45692937: set the de label
Q45692937	Lde	"Mann des Klans Li, aus Qinzhou Chengji"
#   Q45692937: set the es label
Q45692937	Les	"hombre del clan Li, de Qinzhou Chengji"
#   Q45692937: set the it label
Q45692937	Lit	"uomo del clan Li, da Qinzhou Chengji"
#   Q45692937: set the pt label
Q45692937	Lpt	"homem do clã Li, de Qinzhou Chengji"
#   Q45692937: set the ca label
Q45692937	Lca	"home del clan Li, de Qinzhou Chengji"
#   Q45692964 (李 of 揚州): mul label = NN
Q45692964	Lmul	"NN"
#   Q45692964: set the nb label
Q45692964	Lnb	"mann av Li-slekten, fra Yangzhou"
#   Q45692964: set the da label
Q45692964	Lda	"mand af Li-slægten, fra Yangzhou"
#   Q45692964: set the sv label
Q45692964	Lsv	"man av Li-ätten, från Yangzhou"
#   Q45692964: set the de label
Q45692964	Lde	"Mann des Klans Li, aus Yangzhou"
#   Q45692964: set the es label
Q45692964	Les	"hombre del clan Li, de Yangzhou"
#   Q45692964: set the it label
Q45692964	Lit	"uomo del clan Li, da Yangzhou"
#   Q45692964: set the pt label
Q45692964	Lpt	"homem do clã Li, de Yangzhou"
#   Q45692964: set the ca label
Q45692964	Lca	"home del clan Li, de Yangzhou"
#   Q45692991 (李 of 隴西狄道): mul label = NN
Q45692991	Lmul	"NN"
#   Q45692991: set the nb label
Q45692991	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45692991: set the da label
Q45692991	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45692991: set the sv label
Q45692991	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45692991: set the de label
Q45692991	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45692991: set the es label
Q45692991	Les	"hombre del clan Li, de Longxi Didao"
#   Q45692991: set the it label
Q45692991	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45692991: set the pt label
Q45692991	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45692991: set the ca label
Q45692991	Lca	"home del clan Li, de Longxi Didao"
#   Q45693019 (李 of 隴西狄道): mul label = NN
Q45693019	Lmul	"NN"
#   Q45693019: set the nb label
Q45693019	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45693019: set the da label
Q45693019	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45693019: set the sv label
Q45693019	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45693019: set the de label
Q45693019	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45693019: set the es label
Q45693019	Les	"hombre del clan Li, de Longxi Didao"
#   Q45693019: set the it label
Q45693019	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45693019: set the pt label
Q45693019	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45693019: set the ca label
Q45693019	Lca	"home del clan Li, de Longxi Didao"
#   Q45693047 (李 of 隴西狄道): mul label = NN
Q45693047	Lmul	"NN"
#   Q45693047: set the nb label
Q45693047	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45693047: set the da label
Q45693047	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45693047: set the sv label
Q45693047	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45693047: set the de label
Q45693047	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45693047: set the es label
Q45693047	Les	"hombre del clan Li, de Longxi Didao"
#   Q45693047: set the it label
Q45693047	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45693047: set the pt label
Q45693047	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45693047: set the ca label
Q45693047	Lca	"home del clan Li, de Longxi Didao"
#   Q45697303 (李 of 隴西狄道): mul label = NN
Q45697303	Lmul	"NN"
#   Q45697303: set the nb label
Q45697303	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45697303: set the da label
Q45697303	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45697303: set the sv label
Q45697303	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45697303: set the de label
Q45697303	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45697303: set the es label
Q45697303	Les	"hombre del clan Li, de Longxi Didao"
#   Q45697303: set the it label
Q45697303	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45697303: set the pt label
Q45697303	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45697303: set the ca label
Q45697303	Lca	"home del clan Li, de Longxi Didao"
#   Q45698977 (李 of 隴西狄道): mul label = NN
Q45698977	Lmul	"NN"
#   Q45698977: set the nb label
Q45698977	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45698977: set the da label
Q45698977	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45698977: set the sv label
Q45698977	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45698977: set the de label
Q45698977	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45698977: set the es label
Q45698977	Les	"hombre del clan Li, de Longxi Didao"
#   Q45698977: set the it label
Q45698977	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45698977: set the pt label
Q45698977	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45698977: set the ca label
Q45698977	Lca	"home del clan Li, de Longxi Didao"
#   Q45699052 (李 of 隴西狄道): mul label = NN
Q45699052	Lmul	"NN"
#   Q45699052: set the nb label
Q45699052	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45699052: set the da label
Q45699052	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45699052: set the sv label
Q45699052	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45699052: set the de label
Q45699052	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45699052: set the es label
Q45699052	Les	"hombre del clan Li, de Longxi Didao"
#   Q45699052: set the it label
Q45699052	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45699052: set the pt label
Q45699052	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45699052: set the ca label
Q45699052	Lca	"home del clan Li, de Longxi Didao"
#   Q45699104 (李 of 隴西狄道): mul label = NN
Q45699104	Lmul	"NN"
#   Q45699104: set the nb label
Q45699104	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45699104: set the da label
Q45699104	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45699104: set the sv label
Q45699104	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45699104: set the de label
Q45699104	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45699104: set the es label
Q45699104	Les	"hombre del clan Li, de Longxi Didao"
#   Q45699104: set the it label
Q45699104	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45699104: set the pt label
Q45699104	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45699104: set the ca label
Q45699104	Lca	"home del clan Li, de Longxi Didao"
#   Q45699589 (李 of 潤州): mul label = NN
Q45699589	Lmul	"NN"
#   Q45699589: set the nb label
Q45699589	Lnb	"mann av Li-slekten, fra Runzhou"
#   Q45699589: set the da label
Q45699589	Lda	"mand af Li-slægten, fra Runzhou"
#   Q45699589: set the sv label
Q45699589	Lsv	"man av Li-ätten, från Runzhou"
#   Q45699589: set the de label
Q45699589	Lde	"Mann des Klans Li, aus Runzhou"
#   Q45699589: set the es label
Q45699589	Les	"hombre del clan Li, de Runzhou"
#   Q45699589: set the it label
Q45699589	Lit	"uomo del clan Li, da Runzhou"
#   Q45699589: set the pt label
Q45699589	Lpt	"homem do clã Li, de Runzhou"
#   Q45699589: set the ca label
Q45699589	Lca	"home del clan Li, de Runzhou"
#   Q45699613 (李 of 潤州): mul label = NN
Q45699613	Lmul	"NN"
#   Q45699613: set the nb label
Q45699613	Lnb	"mann av Li-slekten, fra Runzhou"
#   Q45699613: set the da label
Q45699613	Lda	"mand af Li-slægten, fra Runzhou"
#   Q45699613: set the sv label
Q45699613	Lsv	"man av Li-ätten, från Runzhou"
#   Q45699613: set the de label
Q45699613	Lde	"Mann des Klans Li, aus Runzhou"
#   Q45699613: set the es label
Q45699613	Les	"hombre del clan Li, de Runzhou"
#   Q45699613: set the it label
Q45699613	Lit	"uomo del clan Li, da Runzhou"
#   Q45699613: set the pt label
Q45699613	Lpt	"homem do clã Li, de Runzhou"
#   Q45699613: set the ca label
Q45699613	Lca	"home del clan Li, de Runzhou"
#   Q45699639 (李 of 潤州): mul label = NN
Q45699639	Lmul	"NN"
#   Q45699639: set the nb label
Q45699639	Lnb	"mann av Li-slekten, fra Runzhou"
#   Q45699639: set the da label
Q45699639	Lda	"mand af Li-slægten, fra Runzhou"
#   Q45699639: set the sv label
Q45699639	Lsv	"man av Li-ätten, från Runzhou"
#   Q45699639: set the de label
Q45699639	Lde	"Mann des Klans Li, aus Runzhou"
#   Q45699639: set the es label
Q45699639	Les	"hombre del clan Li, de Runzhou"
#   Q45699639: set the it label
Q45699639	Lit	"uomo del clan Li, da Runzhou"
#   Q45699639: set the pt label
Q45699639	Lpt	"homem do clã Li, de Runzhou"
#   Q45699639: set the ca label
Q45699639	Lca	"home del clan Li, de Runzhou"
#   Q45699665 (李 of 潤州): mul label = NN
Q45699665	Lmul	"NN"
#   Q45699665: set the nb label
Q45699665	Lnb	"mann av Li-slekten, fra Runzhou"
#   Q45699665: set the da label
Q45699665	Lda	"mand af Li-slægten, fra Runzhou"
#   Q45699665: set the sv label
Q45699665	Lsv	"man av Li-ätten, från Runzhou"
#   Q45699665: set the de label
Q45699665	Lde	"Mann des Klans Li, aus Runzhou"
#   Q45699665: set the es label
Q45699665	Les	"hombre del clan Li, de Runzhou"
#   Q45699665: set the it label
Q45699665	Lit	"uomo del clan Li, da Runzhou"
#   Q45699665: set the pt label
Q45699665	Lpt	"homem do clã Li, de Runzhou"
#   Q45699665: set the ca label
Q45699665	Lca	"home del clan Li, de Runzhou"
#   Q45699690 (李 of 潤州): mul label = NN
Q45699690	Lmul	"NN"
#   Q45699690: set the nb label
Q45699690	Lnb	"mann av Li-slekten, fra Runzhou"
#   Q45699690: set the da label
Q45699690	Lda	"mand af Li-slægten, fra Runzhou"
#   Q45699690: set the sv label
Q45699690	Lsv	"man av Li-ätten, från Runzhou"
#   Q45699690: set the de label
Q45699690	Lde	"Mann des Klans Li, aus Runzhou"
#   Q45699690: set the es label
Q45699690	Les	"hombre del clan Li, de Runzhou"
#   Q45699690: set the it label
Q45699690	Lit	"uomo del clan Li, da Runzhou"
#   Q45699690: set the pt label
Q45699690	Lpt	"homem do clã Li, de Runzhou"
#   Q45699690: set the ca label
Q45699690	Lca	"home del clan Li, de Runzhou"
#   Q45699766 (李 of 隴西狄道): mul label = NN
Q45699766	Lmul	"NN"
#   Q45699766: set the nb label
Q45699766	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45699766: set the da label
Q45699766	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45699766: set the sv label
Q45699766	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45699766: set the de label
Q45699766	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45699766: set the es label
Q45699766	Les	"hombre del clan Li, de Longxi Didao"
#   Q45699766: set the it label
Q45699766	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45699766: set the pt label
Q45699766	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45699766: set the ca label
Q45699766	Lca	"home del clan Li, de Longxi Didao"
#   Q45699789 (李 of 隴西狄道): mul label = NN
Q45699789	Lmul	"NN"
#   Q45699789: set the nb label
Q45699789	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45699789: set the da label
Q45699789	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45699789: set the sv label
Q45699789	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45699789: set the de label
Q45699789	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45699789: set the es label
Q45699789	Les	"hombre del clan Li, de Longxi Didao"
#   Q45699789: set the it label
Q45699789	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45699789: set the pt label
Q45699789	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45699789: set the ca label
Q45699789	Lca	"home del clan Li, de Longxi Didao"
#   Q45699816 (李 of 隴西狄道): mul label = NN
Q45699816	Lmul	"NN"
#   Q45699816: set the nb label
Q45699816	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45699816: set the da label
Q45699816	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45699816: set the sv label
Q45699816	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45699816: set the de label
Q45699816	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45699816: set the es label
Q45699816	Les	"hombre del clan Li, de Longxi Didao"
#   Q45699816: set the it label
Q45699816	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45699816: set the pt label
Q45699816	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45699816: set the ca label
Q45699816	Lca	"home del clan Li, de Longxi Didao"
#   Q45699868 (李 of 隴西狄道): mul label = NN
Q45699868	Lmul	"NN"
#   Q45699868: set the nb label
Q45699868	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45699868: set the da label
Q45699868	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45699868: set the sv label
Q45699868	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45699868: set the de label
Q45699868	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45699868: set the es label
Q45699868	Les	"hombre del clan Li, de Longxi Didao"
#   Q45699868: set the it label
Q45699868	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45699868: set the pt label
Q45699868	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45699868: set the ca label
Q45699868	Lca	"home del clan Li, de Longxi Didao"
#   Q45700460 (李 of 秦州成紀): mul label = NN
Q45700460	Lmul	"NN"
#   Q45700460: set the nb label
Q45700460	Lnb	"mann av Li-slekten, fra Qinzhou Chengji"
#   Q45700460: set the da label
Q45700460	Lda	"mand af Li-slægten, fra Qinzhou Chengji"
#   Q45700460: set the sv label
Q45700460	Lsv	"man av Li-ätten, från Qinzhou Chengji"
#   Q45700460: set the de label
Q45700460	Lde	"Mann des Klans Li, aus Qinzhou Chengji"
#   Q45700460: set the es label
Q45700460	Les	"hombre del clan Li, de Qinzhou Chengji"
#   Q45700460: set the it label
Q45700460	Lit	"uomo del clan Li, da Qinzhou Chengji"
#   Q45700460: set the pt label
Q45700460	Lpt	"homem do clã Li, de Qinzhou Chengji"
#   Q45700460: set the ca label
Q45700460	Lca	"home del clan Li, de Qinzhou Chengji"
#   Q45700483 (李 of 秦州成紀): mul label = NN
Q45700483	Lmul	"NN"
#   Q45700483: set the nb label
Q45700483	Lnb	"mann av Li-slekten, fra Qinzhou Chengji"
#   Q45700483: set the da label
Q45700483	Lda	"mand af Li-slægten, fra Qinzhou Chengji"
#   Q45700483: set the sv label
Q45700483	Lsv	"man av Li-ätten, från Qinzhou Chengji"
#   Q45700483: set the de label
Q45700483	Lde	"Mann des Klans Li, aus Qinzhou Chengji"
#   Q45700483: set the es label
Q45700483	Les	"hombre del clan Li, de Qinzhou Chengji"
#   Q45700483: set the it label
Q45700483	Lit	"uomo del clan Li, da Qinzhou Chengji"
#   Q45700483: set the pt label
Q45700483	Lpt	"homem do clã Li, de Qinzhou Chengji"
#   Q45700483: set the ca label
Q45700483	Lca	"home del clan Li, de Qinzhou Chengji"
#   Q45700509 (李 of 秦州成紀): mul label = NN
Q45700509	Lmul	"NN"
#   Q45700509: set the nb label
Q45700509	Lnb	"mann av Li-slekten, fra Qinzhou Chengji"
#   Q45700509: set the da label
Q45700509	Lda	"mand af Li-slægten, fra Qinzhou Chengji"
#   Q45700509: set the sv label
Q45700509	Lsv	"man av Li-ätten, från Qinzhou Chengji"
#   Q45700509: set the de label
Q45700509	Lde	"Mann des Klans Li, aus Qinzhou Chengji"
#   Q45700509: set the es label
Q45700509	Les	"hombre del clan Li, de Qinzhou Chengji"
#   Q45700509: set the it label
Q45700509	Lit	"uomo del clan Li, da Qinzhou Chengji"
#   Q45700509: set the pt label
Q45700509	Lpt	"homem do clã Li, de Qinzhou Chengji"
#   Q45700509: set the ca label
Q45700509	Lca	"home del clan Li, de Qinzhou Chengji"
#   Q45700685 (李 of 秦州成紀): mul label = NN
Q45700685	Lmul	"NN"
#   Q45700685: set the nb label
Q45700685	Lnb	"mann av Li-slekten, fra Qinzhou Chengji"
#   Q45700685: set the da label
Q45700685	Lda	"mand af Li-slægten, fra Qinzhou Chengji"
#   Q45700685: set the sv label
Q45700685	Lsv	"man av Li-ätten, från Qinzhou Chengji"
#   Q45700685: set the de label
Q45700685	Lde	"Mann des Klans Li, aus Qinzhou Chengji"
#   Q45700685: set the es label
Q45700685	Les	"hombre del clan Li, de Qinzhou Chengji"
#   Q45700685: set the it label
Q45700685	Lit	"uomo del clan Li, da Qinzhou Chengji"
#   Q45700685: set the pt label
Q45700685	Lpt	"homem do clã Li, de Qinzhou Chengji"
#   Q45700685: set the ca label
Q45700685	Lca	"home del clan Li, de Qinzhou Chengji"

