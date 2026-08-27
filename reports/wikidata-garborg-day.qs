# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Alfred Tunheim"
LAST	Len	"Alfred Tunheim"
#   set the mul label to "Alfred Tunheim"
LAST	Lmul	"Alfred Tunheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000039510214027 Alfred Tunheim
LAST	P2600	"6000000039510214027"
#   P569 date of birth = +1908-09-13T00:00:00Z/11
LAST	P569	+1908-09-13T00:00:00Z/11	S2600	"6000000039510214027"
#   P570 date of death = +1958-04-04T00:00:00Z/11
LAST	P570	+1958-04-04T00:00:00Z/11	S2600	"6000000039510214027"
#   P22 father = Q141180396 Tollef Tollefson Tunheim
LAST	P22	Q141180396	S2600	"6000000039510214027"
#   P25 mother = Q141168794 Betsy Jacobson
LAST	P25	Q141168794	S2600	"6000000039510214027"
#   Q141180396 Tollef Tollefson Tunheim: P40 child = the item just created
Q141180396	P40	LAST	S2600	"6000000039510214027"
#   Q141168794 Betsy Jacobson: P40 child = the item just created
Q141168794	P40	LAST	S2600	"6000000039510214027"
#   the item just created: P735 given name = Q3480335 Alfred
LAST	P735	Q3480335

# create a new item
CREATE
#   set the en label to "Algot Bryniolfsson"
LAST	Len	"Algot Bryniolfsson"
#   set the mul label to "Algot Bryniolfsson"
LAST	Lmul	"Algot Bryniolfsson"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005795638082 Algot Bryniolfsson
LAST	P2600	"6000000005795638082"
#   P569 date of birth = +1285-00-00T00:00:00Z/9
LAST	P569	+1285-00-00T00:00:00Z/9	S2600	"6000000005795638082"
#   P570 date of death = +1332-00-00T00:00:00Z/9
LAST	P570	+1332-00-00T00:00:00Z/9	S2600	"6000000005795638082"
#   P25 mother = Q101247444 Ingegerd Svantepolksdotter
LAST	P25	Q101247444	S2600	"6000000005795638082"
#   P40 child = Q5915800 Knut Algotsson
LAST	P40	Q5915800	S2600	"6000000005795638082"
#   Q101247444 Ingegerd Svantepolksdotter: P40 child = the item just created
Q101247444	P40	LAST	S2600	"6000000005795638082"
#   Q5915800 Knut Algotsson: P22 father = the item just created
Q5915800	P22	LAST	S2600	"6000000005795638082"
#   the item just created: P735 given name = Q10405157 Algot
LAST	P735	Q10405157
#   P1449 nickname = en:"Algot Brynolfsson
LAST	P1449	en:"Algot Brynolfsson"
#   add a mul alias "Algot Brynolfsson"
LAST	Amul	"Algot Brynolfsson"

# create a new item
CREATE
#   set the en label to "Anna Carine Gundersen"
LAST	Len	"Anna Carine Gundersen"
#   set the mul label to "Anna Carine Gundersen"
LAST	Lmul	"Anna Carine Gundersen"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000030924460935 Anna Carine Gundersen
LAST	P2600	"6000000030924460935"
#   P569 date of birth = +1811-02-29T00:00:00Z/11
LAST	P569	+1811-02-29T00:00:00Z/11	S2600	"6000000030924460935"
#   P22 father = Q141178199 Gunder Bergersen
LAST	P22	Q141178199	S2600	"6000000030924460935"
#   P25 mother = Q141180395 Maren Gulbrandsdatter Ommestad
LAST	P25	Q141180395	S2600	"6000000030924460935"
#   Q141178199 Gunder Bergersen: P40 child = the item just created
Q141178199	P40	LAST	S2600	"6000000030924460935"
#   Q141180395 Maren Gulbrandsdatter Ommestad: P40 child = the item just created
Q141180395	P40	LAST	S2600	"6000000030924460935"

# create a new item
CREATE
#   the item just created: set the en label to "Anna Maria Helgesdatter Bø"
LAST	Len	"Anna Maria Helgesdatter Bø"
#   set the mul label to "Anna Maria Helgesdatter Bø"
LAST	Lmul	"Anna Maria Helgesdatter Bø"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000196542059842 Anna Maria Helgesdatter Bø
LAST	P2600	"6000000196542059842"
#   P569 date of birth = +1849-02-04T00:00:00Z/11
LAST	P569	+1849-02-04T00:00:00Z/11	S2600	"6000000196542059842"
#   P570 date of death = +1849-04-16T00:00:00Z/11
LAST	P570	+1849-04-16T00:00:00Z/11	S2600	"6000000196542059842"
#   P25 mother = Q141168816 Elisabet Ådnesdatter Garborg
LAST	P25	Q141168816	S2600	"6000000196542059842"
#   Q141168816 Elisabet Ådnesdatter Garborg: P40 child = the item just created
Q141168816	P40	LAST	S2600	"6000000196542059842"

# create a new item
CREATE
#   the item just created: set the en label to "Astri Torkelsdatter Gilja"
LAST	Len	"Astri Torkelsdatter Gilja"
#   set the mul label to "Astri Torkelsdatter Gilja"
LAST	Lmul	"Astri Torkelsdatter Gilja"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003095034747 Astri Torkelsdatter Gilja
LAST	P2600	"6000000003095034747"
#   P570 date of death = +1716-00-00T00:00:00Z/9
LAST	P570	+1716-00-00T00:00:00Z/9	S2600	"6000000003095034747"
#   P735 given name = Q30132931 Astri
LAST	P735	Q30132931
#   add a mul alias "Astri Gilja"
LAST	Amul	"Astri Gilja"

# create a new item
CREATE
#   set the en label to "Bella Jeanette Garfve"
LAST	Len	"Bella Jeanette Garfve"
#   set the mul label to "Bella Jeanette Garfve"
LAST	Lmul	"Bella Jeanette Garfve"
#   add a mul alias "Bella Jeanette Tunheim"
LAST	Amul	"Bella Jeanette Tunheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000039507887815 Bella Jeanette Tunheim
LAST	P2600	"6000000039507887815"
#   P569 date of birth = +1905-06-04T00:00:00Z/11
LAST	P569	+1905-06-04T00:00:00Z/11	S2600	"6000000039507887815"
#   P570 date of death = +1974-12-06T00:00:00Z/11
LAST	P570	+1974-12-06T00:00:00Z/11	S2600	"6000000039507887815"
#   P22 father = Q141180396 Tollef Tollefson Tunheim
LAST	P22	Q141180396	S2600	"6000000039507887815"
#   P25 mother = Q141168794 Betsy Jacobson
LAST	P25	Q141168794	S2600	"6000000039507887815"
#   Q141180396 Tollef Tollefson Tunheim: P40 child = the item just created
Q141180396	P40	LAST	S2600	"6000000039507887815"
#   Q141168794 Betsy Jacobson: P40 child = the item just created
Q141168794	P40	LAST	S2600	"6000000039507887815"
#   the item just created: P735 given name = Q792453 Bella, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q792453	P1545	"1"	P7452	Q3409033
#   P735 given name = Q2300098 Jeanette, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q2300098	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Brita Thomasdotter"
LAST	Len	"Brita Thomasdotter"
#   set the mul label to "Brita Thomasdotter"
LAST	Lmul	"Brita Thomasdotter"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000027488859090 Brita Thomasdotter
LAST	P2600	"6000000027488859090"
#   P569 date of birth = +1559-05-14T00:00:00Z/11
LAST	P569	+1559-05-14T00:00:00Z/11	S2600	"6000000027488859090"
#   P570 date of death = +1588-00-00T00:00:00Z/9
LAST	P570	+1588-00-00T00:00:00Z/9	S2600	"6000000027488859090"
#   P22 father = Q141180413 Thomas Mattsson
LAST	P22	Q141180413	S2600	"6000000027488859090"
#   P25 mother = Q141180409 Magdalena Andersdotter Bure
LAST	P25	Q141180409	S2600	"6000000027488859090"
#   Q141180413 Thomas Mattsson: P40 child = the item just created
Q141180413	P40	LAST	S2600	"6000000027488859090"
#   Q141180409 Magdalena Andersdotter Bure: P40 child = the item just created
Q141180409	P40	LAST	S2600	"6000000027488859090"

# create a new item
CREATE
#   the item just created: set the en label to "Bryniolf Bengtsson (Hafridssons ätt)"
LAST	Len	"Bryniolf Bengtsson (Hafridssons ätt)"
#   set the mul label to "Bryniolf Bengtsson (Hafridssons ätt)"
LAST	Lmul	"Bryniolf Bengtsson (Hafridssons ätt)"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000011239545575 Bryniolf Bengtsson (Hafridssons ätt)
LAST	P2600	"6000000011239545575"
#   P569 date of birth = +1276-00-00T00:00:00Z/9
LAST	P569	+1276-00-00T00:00:00Z/9	S2600	"6000000011239545575"
#   P570 date of death = +1313-00-00T00:00:00Z/9
LAST	P570	+1313-00-00T00:00:00Z/9	S2600	"6000000011239545575"
#   P26 spouse = Q101247444 Ingegerd Svantepolksdotter
LAST	P26	Q101247444	S2600	"6000000011239545575"
#   Q101247444 Ingegerd Svantepolksdotter: P26 spouse = the item just created
Q101247444	P26	LAST	S2600	"6000000011239545575"

# create a new item
CREATE
#   the item just created: set the en label to "Carl Bergersen"
LAST	Len	"Carl Bergersen"
#   set the mul label to "Carl Bergersen"
LAST	Lmul	"Carl Bergersen"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000031155498923 Carl Bergersen
LAST	P2600	"6000000031155498923"
#   P569 date of birth = +1816-03-28T00:00:00Z/11
LAST	P569	+1816-03-28T00:00:00Z/11	S2600	"6000000031155498923"
#   P22 father = Q141178199 Gunder Bergersen
LAST	P22	Q141178199	S2600	"6000000031155498923"
#   P25 mother = Q141180395 Maren Gulbrandsdatter Ommestad
LAST	P25	Q141180395	S2600	"6000000031155498923"
#   Q141178199 Gunder Bergersen: P40 child = the item just created
Q141178199	P40	LAST	S2600	"6000000031155498923"
#   Q141180395 Maren Gulbrandsdatter Ommestad: P40 child = the item just created
Q141180395	P40	LAST	S2600	"6000000031155498923"
#   the item just created: P735 given name = Q2529610 Carl
LAST	P735	Q2529610
#   P734 family name = Q27824335 Bergersen
LAST	P734	Q27824335

# create a new item
CREATE
#   set the en label to "Cecilie Jonsdatter"
LAST	Len	"Cecilie Jonsdatter"
#   set the mul label to "Cecilie Jonsdatter"
LAST	Lmul	"Cecilie Jonsdatter"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000180296055830 Cecilie Jonsdatter
LAST	P2600	"6000000180296055830"
#   P570 date of death = +1275-00-00T00:00:00Z/9
LAST	P570	+1275-00-00T00:00:00Z/9	S2600	"6000000180296055830"
#   P735 given name = Q16275183 Cecilie
LAST	P735	Q16275183

# create a new item
CREATE
#   set the en label to "Elsie Pauline Berggren"
LAST	Len	"Elsie Pauline Berggren"
#   set the mul label to "Elsie Pauline Berggren"
LAST	Lmul	"Elsie Pauline Berggren"
#   add a mul alias "Elsie Pauline Tunheim"
LAST	Amul	"Elsie Pauline Tunheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000039510338057 Elsie Pauline Tunheim
LAST	P2600	"6000000039510338057"
#   P569 date of birth = +1910-01-13T00:00:00Z/11
LAST	P569	+1910-01-13T00:00:00Z/11	S2600	"6000000039510338057"
#   P570 date of death = +1997-01-05T00:00:00Z/11
LAST	P570	+1997-01-05T00:00:00Z/11	S2600	"6000000039510338057"
#   P22 father = Q141180396 Tollef Tollefson Tunheim
LAST	P22	Q141180396	S2600	"6000000039510338057"
#   P25 mother = Q141168794 Betsy Jacobson
LAST	P25	Q141168794	S2600	"6000000039510338057"
#   Q141180396 Tollef Tollefson Tunheim: P40 child = the item just created
Q141180396	P40	LAST	S2600	"6000000039510338057"
#   Q141168794 Betsy Jacobson: P40 child = the item just created
Q141168794	P40	LAST	S2600	"6000000039510338057"
#   the item just created: P735 given name = Q16423214 Elsie, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q16423214	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18009833 Pauline, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q18009833	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Georg August Bergersen"
LAST	Len	"Georg August Bergersen"
#   set the mul label to "Georg August Bergersen"
LAST	Lmul	"Georg August Bergersen"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000020220377527 Georg August Bergersen
LAST	P2600	"6000000020220377527"
#   P569 date of birth = +1820-06-25T00:00:00Z/11
LAST	P569	+1820-06-25T00:00:00Z/11	S2600	"6000000020220377527"
#   P570 date of death = +1897-10-29T00:00:00Z/11
LAST	P570	+1897-10-29T00:00:00Z/11	S2600	"6000000020220377527"
#   P22 father = Q141178199 Gunder Bergersen
LAST	P22	Q141178199	S2600	"6000000020220377527"
#   P25 mother = Q141180395 Maren Gulbrandsdatter Ommestad
LAST	P25	Q141180395	S2600	"6000000020220377527"
#   Q141178199 Gunder Bergersen: P40 child = the item just created
Q141178199	P40	LAST	S2600	"6000000020220377527"
#   Q141180395 Maren Gulbrandsdatter Ommestad: P40 child = the item just created
Q141180395	P40	LAST	S2600	"6000000020220377527"
#   the item just created: P735 given name = Q1985538 Georg, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q1985538	P1545	"1"	P7452	Q3409033
#   P735 given name = Q370731 August, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q370731	P1545	"2"	P3831	Q245025
#   P1449 nickname = en:"Jørgen
LAST	P1449	en:"Jørgen"
#   add a mul alias "Jørgen"
LAST	Amul	"Jørgen"

# create a new item
CREATE
#   set the en label to "Gustav Adolf Gundersen"
LAST	Len	"Gustav Adolf Gundersen"
#   set the mul label to "Gustav Adolf Gundersen"
LAST	Lmul	"Gustav Adolf Gundersen"
#   add a mul alias "Gustav Adolf Bergersen Næsmoen"
LAST	Amul	"Gustav Adolf Bergersen Næsmoen"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000020220981823 Gustav Adolf Bergersen Næsmoen
LAST	P2600	"6000000020220981823"
#   P569 date of birth = +1824-12-29T00:00:00Z/11
LAST	P569	+1824-12-29T00:00:00Z/11	S2600	"6000000020220981823"
#   P570 date of death = +1896-02-01T00:00:00Z/11
LAST	P570	+1896-02-01T00:00:00Z/11	S2600	"6000000020220981823"
#   P22 father = Q141178199 Gunder Bergersen
LAST	P22	Q141178199	S2600	"6000000020220981823"
#   P25 mother = Q141180395 Maren Gulbrandsdatter Ommestad
LAST	P25	Q141180395	S2600	"6000000020220981823"
#   Q141178199 Gunder Bergersen: P40 child = the item just created
Q141178199	P40	LAST	S2600	"6000000020220981823"
#   Q141180395 Maren Gulbrandsdatter Ommestad: P40 child = the item just created
Q141180395	P40	LAST	S2600	"6000000020220981823"
#   the item just created: P735 given name = Q18145837 Adolf, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q18145837	P1545	"2"	P3831	Q245025
#   P734 family name = Q656767 Gundersen
LAST	P734	Q656767
#   P1449 nickname = en:"Bergersen
LAST	P1449	en:"Bergersen"
#   add a mul alias "Bergersen"
LAST	Amul	"Bergersen"

# create a new item
CREATE
#   set the en label to "Helge Rasmusson Bø"
LAST	Len	"Helge Rasmusson Bø"
#   set the mul label to "Helge Rasmusson Bø"
LAST	Lmul	"Helge Rasmusson Bø"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003492005191 Helge Rasmusson Bø
LAST	P2600	"6000000003492005191"
#   P569 date of birth = +1813-08-02T00:00:00Z/11
LAST	P569	+1813-08-02T00:00:00Z/11	S2600	"6000000003492005191"
#   P570 date of death = +1853-07-27T00:00:00Z/11
LAST	P570	+1853-07-27T00:00:00Z/11	S2600	"6000000003492005191"
#   P26 spouse = Q141168816 Elisabet Ådnesdatter Garborg
LAST	P26	Q141168816	S2600	"6000000003492005191"
#   Q141168816 Elisabet Ådnesdatter Garborg: P26 spouse = the item just created
Q141168816	P26	LAST	S2600	"6000000003492005191"
#   the item just created: P735 given name = Q1602361 Helge
LAST	P735	Q1602361

# create a new item
CREATE
#   set the en label to "Helmik Kristiansen Sør-Reime"
LAST	Len	"Helmik Kristiansen Sør-Reime"
#   set the mul label to "Helmik Kristiansen Sør-Reime"
LAST	Lmul	"Helmik Kristiansen Sør-Reime"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000221449620901 Helmik Kristiansen Sør-Reime
LAST	P2600	"6000000221449620901"
#   P569 date of birth = +1858-05-15T00:00:00Z/11
LAST	P569	+1858-05-15T00:00:00Z/11	S2600	"6000000221449620901"
#   P25 mother = Q141168816 Elisabet Ådnesdatter Garborg
LAST	P25	Q141168816	S2600	"6000000221449620901"
#   Q141168816 Elisabet Ådnesdatter Garborg: P40 child = the item just created
Q141168816	P40	LAST	S2600	"6000000221449620901"

# create a new item
CREATE
#   the item just created: set the en label to "Hilde Constance Marie Bergersen"
LAST	Len	"Hilde Constance Marie Bergersen"
#   set the mul label to "Hilde Constance Marie Bergersen"
LAST	Lmul	"Hilde Constance Marie Bergersen"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000055822446833 Hilde Constance Marie Bergersen
LAST	P2600	"6000000055822446833"
#   P569 date of birth = +1865-01-01T00:00:00Z/11
LAST	P569	+1865-01-01T00:00:00Z/11	S2600	"6000000055822446833"
#   P22 father = Q141168797 Christian Frederik Bergersen
LAST	P22	Q141168797	S2600	"6000000055822446833"
#   Q141168797 Christian Frederik Bergersen: P40 child = the item just created
Q141168797	P40	LAST	S2600	"6000000055822446833"
#   the item just created: P735 given name = Q2639538 Hilde, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q2639538	P1545	"1"	P7452	Q3409033
#   P735 given name = Q679755 Constance, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q679755	P1545	"2"	P3831	Q245025
#   P735 given name = Q106674406 Marie, qualified series ordinal 3, object of statement has role Q245025 middle name
LAST	P735	Q106674406	P1545	"3"	P3831	Q245025
#   P734 family name = Q27824335 Bergersen, qualified object of statement has role Q28418670 married name
LAST	P734	Q27824335	P3831	Q28418670

# create a new item
CREATE
#   set the en label to "Ingeborg Ådnesdatter Grøtheim"
LAST	Len	"Ingeborg Ådnesdatter Grøtheim"
#   set the mul label to "Ingeborg Ådnesdatter Grøtheim"
LAST	Lmul	"Ingeborg Ådnesdatter Grøtheim"
#   set the ja label to "インゲボルグ・オードネスダッテル・グレートヘイム"
LAST	Lja	"インゲボルグ・オードネスダッテル・グレートヘイム"
#   set the zh label to "英厄堡·奥德内斯达特·格勒特海姆"
LAST	Lzh	"英厄堡·奥德内斯达特·格勒特海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000008176802346 Ingeborg Ådnesdatter Grøtheim
LAST	P2600	"6000000008176802346"
#   P569 date of birth = +1743-00-00T00:00:00Z/9
LAST	P569	+1743-00-00T00:00:00Z/9	S2600	"6000000008176802346"
#   P570 date of death = +1779-00-00T00:00:00Z/9
LAST	P570	+1779-00-00T00:00:00Z/9	S2600	"6000000008176802346"
#   P40 child = Q141169072 Ådne Olsen Grøtheim
LAST	P40	Q141169072	S2600	"6000000008176802346"
#   Q141169072 Ådne Olsen Grøtheim: P25 mother = the item just created
Q141169072	P25	LAST	S2600	"6000000008176802346"
#   the item just created: P735 given name = Q656590 Ingeborg
LAST	P735	Q656590

# create a new item
CREATE
#   set the en label to "John Jonassen Hegre"
LAST	Len	"John Jonassen Hegre"
#   set the mul label to "John Jonassen Hegre"
LAST	Lmul	"John Jonassen Hegre"
#   add a mul alias "John Jonassen Heigre"
LAST	Amul	"John Jonassen Heigre"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003491986951 John Jonassen Heigre
LAST	P2600	"6000000003491986951"
#   P569 date of birth = +1866-05-04T00:00:00Z/11
LAST	P569	+1866-05-04T00:00:00Z/11	S2600	"6000000003491986951"
#   P570 date of death = +1947-06-05T00:00:00Z/11
LAST	P570	+1947-06-05T00:00:00Z/11	S2600	"6000000003491986951"
#   P22 father = Q141168957 Jonas Jonson Heigre
LAST	P22	Q141168957	S2600	"6000000003491986951"
#   P25 mother = Q141178196 Elisabet Kirstine Eriksdatter Stangeland
LAST	P25	Q141178196	S2600	"6000000003491986951"
#   Q141168957 Jonas Jonson Heigre: P40 child = the item just created
Q141168957	P40	LAST	S2600	"6000000003491986951"
#   Q141178196 Elisabet Kirstine Eriksdatter Stangeland: P40 child = the item just created
Q141178196	P40	LAST	S2600	"6000000003491986951"
#   the item just created: add a mul alias "John Hegre"
LAST	Amul	"John Hegre"

# create a new item
CREATE
#   set the en label to "Joren Jonsdatter Espedal"
LAST	Len	"Joren Jonsdatter Espedal"
#   set the mul label to "Joren Jonsdatter Espedal"
LAST	Lmul	"Joren Jonsdatter Espedal"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005609425388 Joren Jonsdatter Espedal
LAST	P2600	"6000000005609425388"
#   P570 date of death = +1757-00-00T00:00:00Z/9
LAST	P570	+1757-00-00T00:00:00Z/9	S2600	"6000000005609425388"
#   P40 child = Q141180408 Jon Larsson Li
LAST	P40	Q141180408	S2600	"6000000005609425388"
#   Q141180408 Jon Larsson Li: P25 mother = the item just created
Q141180408	P25	LAST	S2600	"6000000005609425388"
#   the item just created: P1449 nickname = en:"Joren J Mæle
LAST	P1449	en:"Joren J Mæle"
#   add a mul alias "Joren J Mæle"
LAST	Amul	"Joren J Mæle"
#   add a mul alias "Joren Espedal"
LAST	Amul	"Joren Espedal"

# create a new item
CREATE
#   set the en label to "Joseph Tunheim"
LAST	Len	"Joseph Tunheim"
#   set the mul label to "Joseph Tunheim"
LAST	Lmul	"Joseph Tunheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000039508106907 Joseph Tunheim
LAST	P2600	"6000000039508106907"
#   P569 date of birth = +1902-12-29T00:00:00Z/11
LAST	P569	+1902-12-29T00:00:00Z/11	S2600	"6000000039508106907"
#   P570 date of death = +1975-02-02T00:00:00Z/11
LAST	P570	+1975-02-02T00:00:00Z/11	S2600	"6000000039508106907"
#   P22 father = Q141180396 Tollef Tollefson Tunheim
LAST	P22	Q141180396	S2600	"6000000039508106907"
#   P25 mother = Q141168794 Betsy Jacobson
LAST	P25	Q141168794	S2600	"6000000039508106907"
#   Q141180396 Tollef Tollefson Tunheim: P40 child = the item just created
Q141180396	P40	LAST	S2600	"6000000039508106907"
#   Q141168794 Betsy Jacobson: P40 child = the item just created
Q141168794	P40	LAST	S2600	"6000000039508106907"
#   the item just created: P735 given name = Q15297160 Joseph
LAST	P735	Q15297160

# create a new item
CREATE
#   set the en label to "Kristian Larsen Sør-Reime"
LAST	Len	"Kristian Larsen Sør-Reime"
#   set the mul label to "Kristian Larsen Sør-Reime"
LAST	Lmul	"Kristian Larsen Sør-Reime"
#   add a mul alias "Kristian Larsen Nord-Varhaug"
LAST	Amul	"Kristian Larsen Nord-Varhaug"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000029302543031 Kristian Larsen Nord-Varhaug
LAST	P2600	"6000000029302543031"
#   P569 date of birth = +1829-02-15T00:00:00Z/11
LAST	P569	+1829-02-15T00:00:00Z/11	S2600	"6000000029302543031"
#   P570 date of death = +1917-02-09T00:00:00Z/11
LAST	P570	+1917-02-09T00:00:00Z/11	S2600	"6000000029302543031"
#   P26 spouse = Q141168816 Elisabet Ådnesdatter Garborg
LAST	P26	Q141168816	S2600	"6000000029302543031"
#   Q141168816 Elisabet Ådnesdatter Garborg: P26 spouse = the item just created
Q141168816	P26	LAST	S2600	"6000000029302543031"
#   the item just created: P735 given name = Q12794332 Kristian
LAST	P735	Q12794332
#   add a mul alias "Kristian Sør-Reime"
LAST	Amul	"Kristian Sør-Reime"

# create a new item
CREATE
#   set the en label to "Lars Bernhard Kristiansen Sør-Reime"
LAST	Len	"Lars Bernhard Kristiansen Sør-Reime"
#   set the mul label to "Lars Bernhard Kristiansen Sør-Reime"
LAST	Lmul	"Lars Bernhard Kristiansen Sør-Reime"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000224702710821 Lars Bernhard Kristiansen Sør-Reime
LAST	P2600	"6000000224702710821"
#   P569 date of birth = +1866-04-29T00:00:00Z/11
LAST	P569	+1866-04-29T00:00:00Z/11	S2600	"6000000224702710821"
#   P25 mother = Q141168816 Elisabet Ådnesdatter Garborg
LAST	P25	Q141168816	S2600	"6000000224702710821"
#   Q141168816 Elisabet Ådnesdatter Garborg: P40 child = the item just created
Q141168816	P40	LAST	S2600	"6000000224702710821"
#   the item just created: P735 given name = Q15635262 Lars, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q15635262	P1545	"1"	P7452	Q3409033
#   P735 given name = Q221978 Bernhard, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q221978	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Lars Kristiansen Sør-Reime"
LAST	Len	"Lars Kristiansen Sør-Reime"
#   set the mul label to "Lars Kristiansen Sør-Reime"
LAST	Lmul	"Lars Kristiansen Sør-Reime"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000224702528843 Lars Kristiansen Sør-Reime
LAST	P2600	"6000000224702528843"
#   P569 date of birth = +1861-05-21T00:00:00Z/11
LAST	P569	+1861-05-21T00:00:00Z/11	S2600	"6000000224702528843"
#   P570 date of death = +1866-02-25T00:00:00Z/11
LAST	P570	+1866-02-25T00:00:00Z/11	S2600	"6000000224702528843"
#   P25 mother = Q141168816 Elisabet Ådnesdatter Garborg
LAST	P25	Q141168816	S2600	"6000000224702528843"
#   Q141168816 Elisabet Ådnesdatter Garborg: P40 child = the item just created
Q141168816	P40	LAST	S2600	"6000000224702528843"
#   the item just created: P735 given name = Q15635262 Lars
LAST	P735	Q15635262

# create a new item
CREATE
#   set the en label to "Lars Tormodsen Mele"
LAST	Len	"Lars Tormodsen Mele"
#   set the mul label to "Lars Tormodsen Mele"
LAST	Lmul	"Lars Tormodsen Mele"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005609425379 Lars Tormodsen Mele
LAST	P2600	"6000000005609425379"
#   P569 date of birth = +1664-00-00T00:00:00Z/9
LAST	P569	+1664-00-00T00:00:00Z/9	S2600	"6000000005609425379"
#   P570 date of death = +1744-00-00T00:00:00Z/9
LAST	P570	+1744-00-00T00:00:00Z/9	S2600	"6000000005609425379"
#   P40 child = Q141180408 Jon Larsson Li
LAST	P40	Q141180408	S2600	"6000000005609425379"
#   Q141180408 Jon Larsson Li: P22 father = the item just created
Q141180408	P22	LAST	S2600	"6000000005609425379"
#   the item just created: P735 given name = Q15635262 Lars
LAST	P735	Q15635262
#   P1449 nickname = en:"Mæle
LAST	P1449	en:"Mæle"
#   add a mul alias "Mæle"
LAST	Amul	"Mæle"
#   add a mul alias "Lars Mele"
LAST	Amul	"Lars Mele"

# create a new item
CREATE
#   set the en label to "Lave"
LAST	Len	"Lave"
#   set the mul label to "Lave"
LAST	Lmul	"Lave"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000181444356836 Lave
LAST	P2600	"6000000181444356836"
#   P735 given name = Q134450528 Lave
LAST	P735	Q134450528

# create a new item
CREATE
#   set the en label to "Lotte Birgithe Gustava Jonasdatter Lea"
LAST	Len	"Lotte Birgithe Gustava Jonasdatter Lea"
#   set the mul label to "Lotte Birgithe Gustava Jonasdatter Lea"
LAST	Lmul	"Lotte Birgithe Gustava Jonasdatter Lea"
#   add a mul alias "Lotte Birgithe Gustava Jonasdatter Heigre"
LAST	Amul	"Lotte Birgithe Gustava Jonasdatter Heigre"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000025793394310 Lotte Birgithe Gustava Jonasdatter Heigre
LAST	P2600	"6000000025793394310"
#   P569 date of birth = +1876-07-07T00:00:00Z/11
LAST	P569	+1876-07-07T00:00:00Z/11	S2600	"6000000025793394310"
#   P570 date of death = +1943-02-17T00:00:00Z/11
LAST	P570	+1943-02-17T00:00:00Z/11	S2600	"6000000025793394310"
#   P22 father = Q141168957 Jonas Jonson Heigre
LAST	P22	Q141168957	S2600	"6000000025793394310"
#   P25 mother = Q141178196 Elisabet Kirstine Eriksdatter Stangeland
LAST	P25	Q141178196	S2600	"6000000025793394310"
#   Q141168957 Jonas Jonson Heigre: P40 child = the item just created
Q141168957	P40	LAST	S2600	"6000000025793394310"
#   Q141178196 Elisabet Kirstine Eriksdatter Stangeland: P40 child = the item just created
Q141178196	P40	LAST	S2600	"6000000025793394310"
#   the item just created: P735 given name = Q2352826 Lotte, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q2352826	P1545	"1"	P7452	Q3409033
#   P735 given name = Q117322332 Birgithe, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q117322332	P1545	"2"	P3831	Q245025
#   P735 given name = Q21144392 Gustava, qualified series ordinal 3, object of statement has role Q245025 middle name
LAST	P735	Q21144392	P1545	"3"	P3831	Q245025
#   P734 family name = Q6508166 Lea, qualified object of statement has role Q28418670 married name
LAST	P734	Q6508166	P3831	Q28418670
#   add a mul alias "Lotte Birgithe Gustava Lea"
LAST	Amul	"Lotte Birgithe Gustava Lea"

# create a new item
CREATE
#   set the en label to "Martha Elida Frenning"
LAST	Len	"Martha Elida Frenning"
#   set the mul label to "Martha Elida Frenning"
LAST	Lmul	"Martha Elida Frenning"
#   add a mul alias "Martha Elida Bergersen"
LAST	Amul	"Martha Elida Bergersen"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000014026305107 Martha Elida Bergersen
LAST	P2600	"6000000014026305107"
#   P569 date of birth = +1856-08-14T00:00:00Z/11
LAST	P569	+1856-08-14T00:00:00Z/11	S2600	"6000000014026305107"
#   P570 date of death = +1888-01-20T00:00:00Z/11
LAST	P570	+1888-01-20T00:00:00Z/11	S2600	"6000000014026305107"
#   P22 father = Q141168797 Christian Frederik Bergersen
LAST	P22	Q141168797	S2600	"6000000014026305107"
#   P25 mother = Q141178201 Marie Petrine Simensdatter Bergersen
LAST	P25	Q141178201	S2600	"6000000014026305107"
#   Q141168797 Christian Frederik Bergersen: P40 child = the item just created
Q141168797	P40	LAST	S2600	"6000000014026305107"
#   Q141178201 Marie Petrine Simensdatter Bergersen: P40 child = the item just created
Q141178201	P40	LAST	S2600	"6000000014026305107"
#   the item just created: P735 given name = Q11967092 Elida, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q11967092	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Martin Tollefson Tunheim"
LAST	Len	"Martin Tollefson Tunheim"
#   set the mul label to "Martin Tollefson Tunheim"
LAST	Lmul	"Martin Tollefson Tunheim"
#   set the ja label to "マルティン・トレフソン・トゥンヘイム"
LAST	Lja	"マルティン・トレフソン・トゥンヘイム"
#   set the zh label to "马丁·托勒夫松·通海姆"
LAST	Lzh	"马丁·托勒夫松·通海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000019384841547 Martin Tollefson Tunheim
LAST	P2600	"6000000019384841547"
#   P569 date of birth = +1867-12-03T00:00:00Z/11
LAST	P569	+1867-12-03T00:00:00Z/11	S2600	"6000000019384841547"
#   P570 date of death = +1937-04-14T00:00:00Z/11
LAST	P570	+1937-04-14T00:00:00Z/11	S2600	"6000000019384841547"
#   P26 spouse = Q141162046 Ane Oline Lena Eivindsdatter Garborg
LAST	P26	Q141162046	S2600	"6000000019384841547"
#   P40 child = Q141169062 Thoralf Tunheim
LAST	P40	Q141169062	S2600	"6000000019384841547"
#   P40 child = Q141168801 Cora Estelle Tunheim
LAST	P40	Q141168801	S2600	"6000000019384841547"
#   P40 child = Q141168809 Edward Tunheim
LAST	P40	Q141168809	S2600	"6000000019384841547"
#   P40 child = Q141168787 Alma Matilda Tunheim
LAST	P40	Q141168787	S2600	"6000000019384841547"
#   P40 child = Q141169041 Olaf Tunheim
LAST	P40	Q141169041	S2600	"6000000019384841547"
#   P40 child = Q141168788 Arne Garborg Tunheim
LAST	P40	Q141168788	S2600	"6000000019384841547"
#   Q141162046 Ane Oline Lena Eivindsdatter Garborg: P26 spouse = the item just created
Q141162046	P26	LAST	S2600	"6000000019384841547"
#   Q141169062 Thoralf Tunheim: P22 father = the item just created
Q141169062	P22	LAST	S2600	"6000000019384841547"
#   Q141168801 Cora Estelle Tunheim: P22 father = the item just created
Q141168801	P22	LAST	S2600	"6000000019384841547"
#   Q141168809 Edward Tunheim: P22 father = the item just created
Q141168809	P22	LAST	S2600	"6000000019384841547"
#   Q141168787 Alma Matilda Tunheim: P22 father = the item just created
Q141168787	P22	LAST	S2600	"6000000019384841547"
#   Q141169041 Olaf Tunheim: P22 father = the item just created
Q141169041	P22	LAST	S2600	"6000000019384841547"
#   Q141168788 Arne Garborg Tunheim: P22 father = the item just created
Q141168788	P22	LAST	S2600	"6000000019384841547"
#   the item just created: P735 given name = Q18002399 Martin
LAST	P735	Q18002399

# create a new item
CREATE
#   set the en label to "Mats Törnesson (hjorthorn)"
LAST	Len	"Mats Törnesson (hjorthorn)"
#   set the mul label to "Mats Törnesson (hjorthorn)"
LAST	Lmul	"Mats Törnesson (hjorthorn)"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000011239496910 Mats Törnesson (hjorthorn)
LAST	P2600	"6000000011239496910"
#   P570 date of death = +1317-00-00T00:00:00Z/9
LAST	P570	+1317-00-00T00:00:00Z/9	S2600	"6000000011239496910"
#   P26 spouse = Q101247444 Ingegerd Svantepolksdotter
LAST	P26	Q101247444	S2600	"6000000011239496910"
#   Q101247444 Ingegerd Svantepolksdotter: P26 spouse = the item just created
Q101247444	P26	LAST	S2600	"6000000011239496910"
#   the item just created: P735 given name = Q12370008 Mats
LAST	P735	Q12370008

# create a new item
CREATE
#   set the en label to "Ola Knutsen Grøtheim"
LAST	Len	"Ola Knutsen Grøtheim"
#   set the mul label to "Ola Knutsen Grøtheim"
LAST	Lmul	"Ola Knutsen Grøtheim"
#   add a mul alias "Ola Knutsen Garborg"
LAST	Amul	"Ola Knutsen Garborg"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000007744588495 Ola Knutsen Garborg
LAST	P2600	"6000000007744588495"
#   P569 date of birth = +1739-00-00T00:00:00Z/9
LAST	P569	+1739-00-00T00:00:00Z/9	S2600	"6000000007744588495"
#   P570 date of death = +1801-08-16T00:00:00Z/11
LAST	P570	+1801-08-16T00:00:00Z/11	S2600	"6000000007744588495"
#   P40 child = Q141169072 Ådne Olsen Grøtheim
LAST	P40	Q141169072	S2600	"6000000007744588495"
#   Q141169072 Ådne Olsen Grøtheim: P22 father = the item just created
Q141169072	P22	LAST	S2600	"6000000007744588495"
#   the item just created: P735 given name = Q96675523 Ola
LAST	P735	Q96675523
#   P734 family name = Q30250555 Garborg, qualified object of statement has role Q2507958 birth name
LAST	P734	Q30250555	P3831	Q2507958
#   add a mul alias "Ola Grøtheim"
LAST	Amul	"Ola Grøtheim"

# create a new item
CREATE
#   set the en label to "Ole Christopher Christiansen"
LAST	Len	"Ole Christopher Christiansen"
#   set the mul label to "Ole Christopher Christiansen"
LAST	Lmul	"Ole Christopher Christiansen"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000021122102578 Ole Christopher Christiansen
LAST	P2600	"6000000021122102578"
#   P569 date of birth = +1865-02-24T00:00:00Z/11
LAST	P569	+1865-02-24T00:00:00Z/11	S2600	"6000000021122102578"
#   P22 father = Q141168797 Christian Frederik Bergersen
LAST	P22	Q141168797	S2600	"6000000021122102578"
#   Q141168797 Christian Frederik Bergersen: P40 child = the item just created
Q141168797	P40	LAST	S2600	"6000000021122102578"
#   the item just created: P735 given name = Q2097883 Ole, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q2097883	P1545	"1"	P7452	Q3409033
#   P734 family name = Q11963736 Christiansen
LAST	P734	Q11963736
#   P1449 nickname = en:"Ole Christoffer Bergersen
LAST	P1449	en:"Ole Christoffer Bergersen"
#   add a mul alias "Ole Christoffer Bergersen"
LAST	Amul	"Ole Christoffer Bergersen"

# create a new item
CREATE
#   set the en label to "Ole Nicolai Bergersen"
LAST	Len	"Ole Nicolai Bergersen"
#   set the mul label to "Ole Nicolai Bergersen"
LAST	Lmul	"Ole Nicolai Bergersen"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000055822412855 Ole Nicolai Bergersen
LAST	P2600	"6000000055822412855"
#   P569 date of birth = +1866-02-16T00:00:00Z/11
LAST	P569	+1866-02-16T00:00:00Z/11	S2600	"6000000055822412855"
#   P22 father = Q141168797 Christian Frederik Bergersen
LAST	P22	Q141168797	S2600	"6000000055822412855"
#   Q141168797 Christian Frederik Bergersen: P40 child = the item just created
Q141168797	P40	LAST	S2600	"6000000055822412855"
#   the item just created: P735 given name = Q2097883 Ole, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q2097883	P1545	"1"	P7452	Q3409033
#   P735 given name = Q19830590 Nicolai, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q19830590	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Oline Mathea Olsen"
LAST	Len	"Oline Mathea Olsen"
#   set the mul label to "Oline Mathea Olsen"
LAST	Lmul	"Oline Mathea Olsen"
#   add a mul alias "Oline Mathea Bergersen"
LAST	Amul	"Oline Mathea Bergersen"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000022418305015 Oline Mathea Bergersen
LAST	P2600	"6000000022418305015"
#   P569 date of birth = +1822-11-01T00:00:00Z/11
LAST	P569	+1822-11-01T00:00:00Z/11	S2600	"6000000022418305015"
#   P22 father = Q141178199 Gunder Bergersen
LAST	P22	Q141178199	S2600	"6000000022418305015"
#   P25 mother = Q141180395 Maren Gulbrandsdatter Ommestad
LAST	P25	Q141180395	S2600	"6000000022418305015"
#   Q141178199 Gunder Bergersen: P40 child = the item just created
Q141178199	P40	LAST	S2600	"6000000022418305015"
#   Q141180395 Maren Gulbrandsdatter Ommestad: P40 child = the item just created
Q141180395	P40	LAST	S2600	"6000000022418305015"
#   the item just created: P735 given name = Q11993741 Oline, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q11993741	P1545	"1"	P7452	Q3409033
#   P735 given name = Q19810278 Mathea, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q19810278	P1545	"2"	P3831	Q245025
#   P734 family name = Q12042571 Olsen, qualified object of statement has role Q28418670 married name
LAST	P734	Q12042571	P3831	Q28418670
#   P1449 nickname = en:"Gundersdatter
LAST	P1449	en:"Gundersdatter"
#   add a mul alias "Gundersdatter"
LAST	Amul	"Gundersdatter"

# create a new item
CREATE
#   set the en label to "Oskar Haug"
LAST	Len	"Oskar Haug"
#   set the mul label to "Oskar Haug"
LAST	Lmul	"Oskar Haug"
#   add a mul alias "Oskar Edlund"
LAST	Amul	"Oskar Edlund"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000010256424421 Oskar Edlund
LAST	P2600	"6000000010256424421"
#   P569 date of birth = +1874-12-31T00:00:00Z/11
LAST	P569	+1874-12-31T00:00:00Z/11	S2600	"6000000010256424421"
#   P25 mother = Q141178201 Marie Petrine Simensdatter Bergersen
LAST	P25	Q141178201	S2600	"6000000010256424421"
#   Q141178201 Marie Petrine Simensdatter Bergersen: P40 child = the item just created
Q141178201	P40	LAST	S2600	"6000000010256424421"
#   the item just created: P735 given name = Q18145769 Oskar
LAST	P735	Q18145769
#   P734 family name = Q16777571 Haug
LAST	P734	Q16777571

# create a new item
CREATE
#   set the en label to "Peter Tunheim"
LAST	Len	"Peter Tunheim"
#   set the mul label to "Peter Tunheim"
LAST	Lmul	"Peter Tunheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000039510875837 Peter Tunheim
LAST	P2600	"6000000039510875837"
#   P569 date of birth = +1916-06-18T00:00:00Z/11
LAST	P569	+1916-06-18T00:00:00Z/11	S2600	"6000000039510875837"
#   P570 date of death = +1983-07-09T00:00:00Z/11
LAST	P570	+1983-07-09T00:00:00Z/11	S2600	"6000000039510875837"
#   P22 father = Q141180396 Tollef Tollefson Tunheim
LAST	P22	Q141180396	S2600	"6000000039510875837"
#   P25 mother = Q141168794 Betsy Jacobson
LAST	P25	Q141168794	S2600	"6000000039510875837"
#   Q141180396 Tollef Tollefson Tunheim: P40 child = the item just created
Q141180396	P40	LAST	S2600	"6000000039510875837"
#   Q141168794 Betsy Jacobson: P40 child = the item just created
Q141168794	P40	LAST	S2600	"6000000039510875837"
#   the item just created: P735 given name = Q2793400 Peter
LAST	P735	Q2793400

# create a new item
CREATE
#   set the en label to "Ragnhild Toresdatter Håland i Gjesdal"
LAST	Len	"Ragnhild Toresdatter Håland i Gjesdal"
#   set the mul label to "Ragnhild Toresdatter Håland i Gjesdal"
LAST	Lmul	"Ragnhild Toresdatter Håland i Gjesdal"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005609425396 Ragnhild Toresdatter Håland i Gjesdal
LAST	P2600	"6000000005609425396"
#   P569 date of birth = +1661-00-00T00:00:00Z/9
LAST	P569	+1661-00-00T00:00:00Z/9	S2600	"6000000005609425396"
#   P570 date of death = +1709-00-00T00:00:00Z/9
LAST	P570	+1709-00-00T00:00:00Z/9	S2600	"6000000005609425396"
#   P735 given name = Q1390292 Ragnhild
LAST	P735	Q1390292
#   P734 family name = Q27888954 Gjesdal
LAST	P734	Q27888954

# create a new item
CREATE
#   set the en label to "Rakel Jonasdatter Heigre"
LAST	Len	"Rakel Jonasdatter Heigre"
#   set the mul label to "Rakel Jonasdatter Heigre"
LAST	Lmul	"Rakel Jonasdatter Heigre"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003491986966 Rakel Jonasdatter Heigre
LAST	P2600	"6000000003491986966"
#   P569 date of birth = +1874-02-26T00:00:00Z/11
LAST	P569	+1874-02-26T00:00:00Z/11	S2600	"6000000003491986966"
#   P570 date of death = +1882-01-09T00:00:00Z/11
LAST	P570	+1882-01-09T00:00:00Z/11	S2600	"6000000003491986966"
#   P22 father = Q141168957 Jonas Jonson Heigre
LAST	P22	Q141168957	S2600	"6000000003491986966"
#   P25 mother = Q141178196 Elisabet Kirstine Eriksdatter Stangeland
LAST	P25	Q141178196	S2600	"6000000003491986966"
#   Q141168957 Jonas Jonson Heigre: P40 child = the item just created
Q141168957	P40	LAST	S2600	"6000000003491986966"
#   Q141178196 Elisabet Kirstine Eriksdatter Stangeland: P40 child = the item just created
Q141178196	P40	LAST	S2600	"6000000003491986966"
#   the item just created: P735 given name = Q16424094 Rakel
LAST	P735	Q16424094

# create a new item
CREATE
#   set the en label to "Rasmus Helgesen Bø"
LAST	Len	"Rasmus Helgesen Bø"
#   set the mul label to "Rasmus Helgesen Bø"
LAST	Lmul	"Rasmus Helgesen Bø"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000021133770643 Rasmus Helgesen Bø
LAST	P2600	"6000000021133770643"
#   P569 date of birth = +1850-02-25T00:00:00Z/11
LAST	P569	+1850-02-25T00:00:00Z/11	S2600	"6000000021133770643"
#   P570 date of death = +1887-07-11T00:00:00Z/11
LAST	P570	+1887-07-11T00:00:00Z/11	S2600	"6000000021133770643"
#   P25 mother = Q141168816 Elisabet Ådnesdatter Garborg
LAST	P25	Q141168816	S2600	"6000000021133770643"
#   Q141168816 Elisabet Ådnesdatter Garborg: P40 child = the item just created
Q141168816	P40	LAST	S2600	"6000000021133770643"
#   the item just created: P735 given name = Q1785744 Rasmus
LAST	P735	Q1785744

# create a new item
CREATE
#   set the en label to "Rose Lindstrom"
LAST	Len	"Rose Lindstrom"
#   set the mul label to "Rose Lindstrom"
LAST	Lmul	"Rose Lindstrom"
#   add a mul alias "Rose Tunheim"
LAST	Amul	"Rose Tunheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000039510583899 Rose Tunheim
LAST	P2600	"6000000039510583899"
#   P569 date of birth = +1912-05-03T00:00:00Z/11
LAST	P569	+1912-05-03T00:00:00Z/11	S2600	"6000000039510583899"
#   P570 date of death = +1972-03-10T00:00:00Z/11
LAST	P570	+1972-03-10T00:00:00Z/11	S2600	"6000000039510583899"
#   P22 father = Q141180396 Tollef Tollefson Tunheim
LAST	P22	Q141180396	S2600	"6000000039510583899"
#   P25 mother = Q141168794 Betsy Jacobson
LAST	P25	Q141168794	S2600	"6000000039510583899"
#   Q141180396 Tollef Tollefson Tunheim: P40 child = the item just created
Q141180396	P40	LAST	S2600	"6000000039510583899"
#   Q141168794 Betsy Jacobson: P40 child = the item just created
Q141168794	P40	LAST	S2600	"6000000039510583899"
#   the item just created: P735 given name = Q3585338 Rose
LAST	P735	Q3585338

# create a new item
CREATE
#   set the en label to "Samuel Tunheim"
LAST	Len	"Samuel Tunheim"
#   set the mul label to "Samuel Tunheim"
LAST	Lmul	"Samuel Tunheim"
#   set the ja label to "サムエル・トゥンヘイム"
LAST	Lja	"サムエル・トゥンヘイム"
#   set the zh label to "萨穆埃尔·通海姆"
LAST	Lzh	"萨穆埃尔·通海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000039510735157 Samuel Tunheim
LAST	P2600	"6000000039510735157"
#   P569 date of birth = +1918-07-20T00:00:00Z/11
LAST	P569	+1918-07-20T00:00:00Z/11	S2600	"6000000039510735157"
#   P570 date of death = +1975-07-10T00:00:00Z/11
LAST	P570	+1975-07-10T00:00:00Z/11	S2600	"6000000039510735157"
#   P22 father = Q141180396 Tollef Tollefson Tunheim
LAST	P22	Q141180396	S2600	"6000000039510735157"
#   P25 mother = Q141168794 Betsy Jacobson
LAST	P25	Q141168794	S2600	"6000000039510735157"
#   Q141180396 Tollef Tollefson Tunheim: P40 child = the item just created
Q141180396	P40	LAST	S2600	"6000000039510735157"
#   Q141168794 Betsy Jacobson: P40 child = the item just created
Q141168794	P40	LAST	S2600	"6000000039510735157"
#   the item just created: P735 given name = Q629347 Samuel
LAST	P735	Q629347

# create a new item
CREATE
#   set the en label to "Sigrid Manilva Ekman"
LAST	Len	"Sigrid Manilva Ekman"
#   set the mul label to "Sigrid Manilva Ekman"
LAST	Lmul	"Sigrid Manilva Ekman"
#   add a mul alias "Sigrid Manilva Tunheim"
LAST	Amul	"Sigrid Manilva Tunheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000039507820846 Sigrid Sally Manilva Tunheim
LAST	P2600	"6000000039507820846"
#   P569 date of birth = +1898-08-22T00:00:00Z/11
LAST	P569	+1898-08-22T00:00:00Z/11	S2600	"6000000039507820846"
#   P570 date of death = +1947-09-21T00:00:00Z/11
LAST	P570	+1947-09-21T00:00:00Z/11	S2600	"6000000039507820846"
#   P22 father = Q141180396 Tollef Tollefson Tunheim
LAST	P22	Q141180396	S2600	"6000000039507820846"
#   P25 mother = Q141168794 Betsy Jacobson
LAST	P25	Q141168794	S2600	"6000000039507820846"
#   Q141180396 Tollef Tollefson Tunheim: P40 child = the item just created
Q141180396	P40	LAST	S2600	"6000000039507820846"
#   Q141168794 Betsy Jacobson: P40 child = the item just created
Q141168794	P40	LAST	S2600	"6000000039507820846"
#   the item just created: P735 given name = Q634916 Sigrid, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q634916	P1545	"1"	P7452	Q3409033
#   P1449 nickname = en:"Sally
LAST	P1449	en:"Sally"
#   add a mul alias "Sally"
LAST	Amul	"Sally"

# create a new item
CREATE
#   set the en label to "Siri Kristine Ivarsdatter Garborg"
LAST	Len	"Siri Kristine Ivarsdatter Garborg"
#   set the mul label to "Siri Kristine Ivarsdatter Garborg"
LAST	Lmul	"Siri Kristine Ivarsdatter Garborg"
#   add a mul alias "Siri Kristine Ivarsdatter Sandsmark"
LAST	Amul	"Siri Kristine Ivarsdatter Sandsmark"
#   set the ja label to "シーリ・クリスティーネ・イーヴァシュダッテル・ガルボルグ"
LAST	Lja	"シーリ・クリスティーネ・イーヴァシュダッテル・ガルボルグ"
#   set the zh label to "西丽·克丽丝汀·伊瓦斯达特·加尔博格"
LAST	Lzh	"西丽·克丽丝汀·伊瓦斯达特·加尔博格"
#   add a ja alias "シーリ・クリスティーネ・イーヴァシュダッテル・サンスマルク"
LAST	Aja	"シーリ・クリスティーネ・イーヴァシュダッテル・サンスマルク"
#   add a zh alias "西丽·克丽丝汀·伊瓦斯达特·桑斯马克"
LAST	Azh	"西丽·克丽丝汀·伊瓦斯达特·桑斯马克"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000002954315535 Siri Kristine Ivarsdatter Sandsmark
LAST	P2600	"6000000002954315535"
#   P569 date of birth = +1863-01-19T00:00:00Z/11
LAST	P569	+1863-01-19T00:00:00Z/11	S2600	"6000000002954315535"
#   P570 date of death = +1939-10-19T00:00:00Z/11
LAST	P570	+1939-10-19T00:00:00Z/11	S2600	"6000000002954315535"
#   P26 spouse = Q141152614 Jon Eivindson Garborg
LAST	P26	Q141152614	S2600	"6000000002954315535"
#   P40 child = Q141168811 Eivind Garborg
LAST	P40	Q141168811	S2600	"6000000002954315535"
#   P40 child = Q141168792 Astrid Garborg
LAST	P40	Q141168792	S2600	"6000000002954315535"
#   P40 child = Q141168837 Ingebret Garborg
LAST	P40	Q141168837	S2600	"6000000002954315535"
#   P40 child = Q141168830 Ingeborg Garborg
LAST	P40	Q141168830	S2600	"6000000002954315535"
#   P40 child = Q141168954 Jon Garborg
LAST	P40	Q141168954	S2600	"6000000002954315535"
#   P40 child = Q141168784 Aagot Garborg
LAST	P40	Q141168784	S2600	"6000000002954315535"
#   Q141152614 Jon Eivindson Garborg: P26 spouse = the item just created
Q141152614	P26	LAST	S2600	"6000000002954315535"
#   Q141168811 Eivind Garborg: P25 mother = the item just created
Q141168811	P25	LAST	S2600	"6000000002954315535"
#   Q141168792 Astrid Garborg: P25 mother = the item just created
Q141168792	P25	LAST	S2600	"6000000002954315535"
#   Q141168837 Ingebret Garborg: P25 mother = the item just created
Q141168837	P25	LAST	S2600	"6000000002954315535"
#   Q141168830 Ingeborg Garborg: P25 mother = the item just created
Q141168830	P25	LAST	S2600	"6000000002954315535"
#   Q141168954 Jon Garborg: P25 mother = the item just created
Q141168954	P25	LAST	S2600	"6000000002954315535"
#   Q141168784 Aagot Garborg: P25 mother = the item just created
Q141168784	P25	LAST	S2600	"6000000002954315535"
#   the item just created: P735 given name = Q1772342 Siri, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q1772342	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16859157 Kristine, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q16859157	P1545	"2"	P3831	Q245025
#   P734 family name = Q30250555 Garborg, qualified object of statement has role Q28418670 married name
LAST	P734	Q30250555	P3831	Q28418670
#   add a mul alias "Siri Kristine Garborg"
LAST	Amul	"Siri Kristine Garborg"

# create a new item
CREATE
#   set the en label to "Sophia Birgitta Gundersen"
LAST	Len	"Sophia Birgitta Gundersen"
#   set the mul label to "Sophia Birgitta Gundersen"
LAST	Lmul	"Sophia Birgitta Gundersen"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000030924365079 Sophia Birgitta Gundersen
LAST	P2600	"6000000030924365079"
#   P569 date of birth = +1813-12-05T00:00:00Z/11
LAST	P569	+1813-12-05T00:00:00Z/11	S2600	"6000000030924365079"
#   P22 father = Q141178199 Gunder Bergersen
LAST	P22	Q141178199	S2600	"6000000030924365079"
#   P25 mother = Q141180395 Maren Gulbrandsdatter Ommestad
LAST	P25	Q141180395	S2600	"6000000030924365079"
#   Q141178199 Gunder Bergersen: P40 child = the item just created
Q141178199	P40	LAST	S2600	"6000000030924365079"
#   Q141180395 Maren Gulbrandsdatter Ommestad: P40 child = the item just created
Q141180395	P40	LAST	S2600	"6000000030924365079"
#   the item just created: P735 given name = Q19816187 Birgitta, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q19816187	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Theodore Roosevelt Tunheim"
LAST	Len	"Theodore Roosevelt Tunheim"
#   set the mul label to "Theodore Roosevelt Tunheim"
LAST	Lmul	"Theodore Roosevelt Tunheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000039507759313 Theodore Roosevelt Tunheim
LAST	P2600	"6000000039507759313"
#   P569 date of birth = +1900-07-13T00:00:00Z/11
LAST	P569	+1900-07-13T00:00:00Z/11	S2600	"6000000039507759313"
#   P570 date of death = +1958-10-05T00:00:00Z/11
LAST	P570	+1958-10-05T00:00:00Z/11	S2600	"6000000039507759313"
#   P22 father = Q141180396 Tollef Tollefson Tunheim
LAST	P22	Q141180396	S2600	"6000000039507759313"
#   P25 mother = Q141168794 Betsy Jacobson
LAST	P25	Q141168794	S2600	"6000000039507759313"
#   Q141180396 Tollef Tollefson Tunheim: P40 child = the item just created
Q141180396	P40	LAST	S2600	"6000000039507759313"
#   Q141168794 Betsy Jacobson: P40 child = the item just created
Q141168794	P40	LAST	S2600	"6000000039507759313"
#   the item just created: P735 given name = Q15875484 Theodore, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q15875484	P1545	"1"	P7452	Q3409033
#   P1449 nickname = en:"Ted Tunheim
LAST	P1449	en:"Ted Tunheim"
#   add a mul alias "Ted Tunheim"
LAST	Amul	"Ted Tunheim"

# create a new item
CREATE
#   set the en label to "Tillie Betsy Amundson"
LAST	Len	"Tillie Betsy Amundson"
#   set the mul label to "Tillie Betsy Amundson"
LAST	Lmul	"Tillie Betsy Amundson"
#   add a mul alias "Tillie Betsy Tunheim"
LAST	Amul	"Tillie Betsy Tunheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000008542267056 Tillie Betsy Tunheim
LAST	P2600	"6000000008542267056"
#   P569 date of birth = +1914-03-14T00:00:00Z/11
LAST	P569	+1914-03-14T00:00:00Z/11	S2600	"6000000008542267056"
#   P570 date of death = +1997-03-07T00:00:00Z/11
LAST	P570	+1997-03-07T00:00:00Z/11	S2600	"6000000008542267056"
#   P22 father = Q141180396 Tollef Tollefson Tunheim
LAST	P22	Q141180396	S2600	"6000000008542267056"
#   P25 mother = Q141168794 Betsy Jacobson
LAST	P25	Q141168794	S2600	"6000000008542267056"
#   Q141180396 Tollef Tollefson Tunheim: P40 child = the item just created
Q141180396	P40	LAST	S2600	"6000000008542267056"
#   Q141168794 Betsy Jacobson: P40 child = the item just created
Q141168794	P40	LAST	S2600	"6000000008542267056"
#   the item just created: P735 given name = Q27700115 Tillie, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q27700115	P1545	"1"	P7452	Q3409033
#   P735 given name = Q832242 Betsy, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q832242	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Tollef Bud Tunheim"
LAST	Len	"Tollef Bud Tunheim"
#   set the mul label to "Tollef Bud Tunheim"
LAST	Lmul	"Tollef Bud Tunheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000039510907240 Tollef Bud Tunheim
LAST	P2600	"6000000039510907240"
#   P569 date of birth = +1920-07-13T00:00:00Z/11
LAST	P569	+1920-07-13T00:00:00Z/11	S2600	"6000000039510907240"
#   P570 date of death = +1992-09-24T00:00:00Z/11
LAST	P570	+1992-09-24T00:00:00Z/11	S2600	"6000000039510907240"
#   P22 father = Q141180396 Tollef Tollefson Tunheim
LAST	P22	Q141180396	S2600	"6000000039510907240"
#   P25 mother = Q141168794 Betsy Jacobson
LAST	P25	Q141168794	S2600	"6000000039510907240"
#   Q141180396 Tollef Tollefson Tunheim: P40 child = the item just created
Q141180396	P40	LAST	S2600	"6000000039510907240"
#   Q141168794 Betsy Jacobson: P40 child = the item just created
Q141168794	P40	LAST	S2600	"6000000039510907240"
#   the item just created: P735 given name = Q12006598 Tollef
LAST	P735	Q12006598
#   P1449 nickname = en:"Bud
LAST	P1449	en:"Bud"
#   add a mul alias "Bud"
LAST	Amul	"Bud"
#   add a mul alias "Tollef Tunheim"
LAST	Amul	"Tollef Tunheim"

# create a new item
CREATE
#   set the en label to "Tøre Jonsen"
LAST	Len	"Tøre Jonsen"
#   set the mul label to "Tøre Jonsen"
LAST	Lmul	"Tøre Jonsen"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000180307857930 Tøre Jonsen
LAST	P2600	"6000000180307857930"
#   P570 date of death = +1305-00-00T00:00:00Z/9
LAST	P570	+1305-00-00T00:00:00Z/9	S2600	"6000000180307857930"

# create a new item
CREATE
#   set the en label to "Tørres Jonasson Hegre"
LAST	Len	"Tørres Jonasson Hegre"
#   set the mul label to "Tørres Jonasson Hegre"
LAST	Lmul	"Tørres Jonasson Hegre"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000025755145944 Tørres Jonasson Hegre
LAST	P2600	"6000000025755145944"
#   P569 date of birth = +1878-02-26T00:00:00Z/11
LAST	P569	+1878-02-26T00:00:00Z/11	S2600	"6000000025755145944"
#   P570 date of death = +1961-11-11T00:00:00Z/11
LAST	P570	+1961-11-11T00:00:00Z/11	S2600	"6000000025755145944"
#   P22 father = Q141168957 Jonas Jonson Heigre
LAST	P22	Q141168957	S2600	"6000000025755145944"
#   P25 mother = Q141178196 Elisabet Kirstine Eriksdatter Stangeland
LAST	P25	Q141178196	S2600	"6000000025755145944"
#   Q141168957 Jonas Jonson Heigre: P40 child = the item just created
Q141168957	P40	LAST	S2600	"6000000025755145944"
#   Q141178196 Elisabet Kirstine Eriksdatter Stangeland: P40 child = the item just created
Q141178196	P40	LAST	S2600	"6000000025755145944"

# create a new item
CREATE
#   the item just created: set the en label to "Wilhelmine Sophie Christiansen"
LAST	Len	"Wilhelmine Sophie Christiansen"
#   set the mul label to "Wilhelmine Sophie Christiansen"
LAST	Lmul	"Wilhelmine Sophie Christiansen"
#   add a mul alias "Wilhelmine Sophie Bergersen"
LAST	Amul	"Wilhelmine Sophie Bergersen"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000014026120692 Wilhelmine Sophie Bergersen
LAST	P2600	"6000000014026120692"
#   P569 date of birth = +1858-07-06T00:00:00Z/11
LAST	P569	+1858-07-06T00:00:00Z/11	S2600	"6000000014026120692"
#   P570 date of death = +1924-00-00T00:00:00Z/9
LAST	P570	+1924-00-00T00:00:00Z/9	S2600	"6000000014026120692"
#   P22 father = Q141168797 Christian Frederik Bergersen
LAST	P22	Q141168797	S2600	"6000000014026120692"
#   P25 mother = Q141178201 Marie Petrine Simensdatter Bergersen
LAST	P25	Q141178201	S2600	"6000000014026120692"
#   Q141168797 Christian Frederik Bergersen: P40 child = the item just created
Q141168797	P40	LAST	S2600	"6000000014026120692"
#   Q141178201 Marie Petrine Simensdatter Bergersen: P40 child = the item just created
Q141178201	P40	LAST	S2600	"6000000014026120692"
#   the item just created: P735 given name = Q15728223 Wilhelmine, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q15728223	P1545	"1"	P7452	Q3409033
#   P735 given name = Q14942517 Sophie, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q14942517	P1545	"2"	P3831	Q245025
#   P734 family name = Q11963736 Christiansen, qualified object of statement has role Q28418670 married name
LAST	P734	Q11963736	P3831	Q28418670

# create a new item
CREATE
#   set the en label to "Ådne Helgesen Bø"
LAST	Len	"Ådne Helgesen Bø"
#   set the mul label to "Ådne Helgesen Bø"
LAST	Lmul	"Ådne Helgesen Bø"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000196542455825 Ådne Helgesen Bø
LAST	P2600	"6000000196542455825"
#   P569 date of birth = +1852-08-28T00:00:00Z/11
LAST	P569	+1852-08-28T00:00:00Z/11	S2600	"6000000196542455825"
#   P570 date of death = +1881-02-14T00:00:00Z/11
LAST	P570	+1881-02-14T00:00:00Z/11	S2600	"6000000196542455825"
#   P25 mother = Q141168816 Elisabet Ådnesdatter Garborg
LAST	P25	Q141168816	S2600	"6000000196542455825"
#   Q141168816 Elisabet Ådnesdatter Garborg: P40 child = the item just created
Q141168816	P40	LAST	S2600	"6000000196542455825"

# RELATIONSHIPS between items that already exist -- the links yesterday's
#    creations made possible, and the properties never emitted. Every subject
#    and every value already has a QID, so this section depends on nothing above
#    it. It is emitted LAST, per her order: individuals, names, relationships.

#   Q116150300 Cecilie Ebbesdatter Hvide: P3373 sibling = Q2183430 Bengta Ebbesdotter Ebbesdatter Galen Queen of Sweden
Q116150300	P3373	Q2183430	S2600	"305332989800002467"
#   P735 given name = Q16275183 Cecilie
Q116150300	P735	Q16275183
#   P734 family name = Q55222347 Hvide
Q116150300	P734	Q55222347
#   Q2183430 Bengta Ebbesdotter Ebbesdatter Galen Queen of Sweden: P3373 sibling = Q116150300 Cecilie Ebbesdatter Hvide
Q2183430	P3373	Q116150300	S2600	"4947248545210089938"
#   Q284400 Giséle de Cysoing: P40 child = Q274606 Berengar I margrave of Friuli, king of Italy
Q284400	P40	Q274606	S2600	"6000000000424624719"
#   Q3743799 Knut Valdemarsson Duke of Estland, Blekinge and Lolland: P40 child = Q6197518 Svantepolk Knutsson Viby Skarsholmsätten
Q3743799	P40	Q6197518	S2600	"6000000003076221220"
#   Q6197518 Svantepolk Knutsson Viby Skarsholmsätten: P40 child = Q101247444 Ingegerd Svantepolksdotter
Q6197518	P40	Q101247444	S2600	"6000000003418900347"
#   Q141168957 Jonas Jonson Heigre: P40 child = Q141178198 Enevald Jonasson Heigre
Q141168957	P40	Q141178198	S2600	"6000000003491986771"
#   P26 spouse = Q141178196 Elisabet Kirstine Eriksdatter Stangeland
Q141168957	P26	Q141178196	S2600	"6000000003491986771"
#   P26 spouse = Q141152523 Ane Oline Jonsdatter Raugstad
Q141168957	P26	Q141152523	S2600	"6000000003491986771"
#   P735 given name = Q16646115 Jonas
Q141168957	P735	Q16646115
#   set the ja label to "ヨナス・ヨンソン・ヘイグレ"
Q141168957	Lja	"ヨナス・ヨンソン・ヘイグレ"
#   set the zh label to "约纳斯·永松·海格勒"
Q141168957	Lzh	"约纳斯·永松·海格勒"
#   Q141178196 Elisabet Kirstine Eriksdatter Stangeland: P40 child = Q141178198 Enevald Jonasson Heigre
Q141178196	P40	Q141178198	S2600	"6000000003491986941"
#   P26 spouse = Q141168957 Jonas Jonson Heigre
Q141178196	P26	Q141168957	S2600	"6000000003491986941"
#   P735 given name = Q16423275 Elisabet, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141178196	P735	Q16423275	P1545	"1"	P7452	Q3409033
#   P735 given name = Q11980788 Kirstine, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141178196	P735	Q11980788	P1545	"2"	P3831	Q245025
#   P734 family name = Q21452049 Stangeland
Q141178196	P734	Q21452049
#   Q141152523 Ane Oline Jonsdatter Raugstad: P22 father = Q141168955 Jon Samuelsen Raustad
Q141152523	P22	Q141168955	S2600	"6000000003491986946"
#   P25 mother = Q141178200 Inger Kristoffersdatter
Q141152523	P25	Q141178200	S2600	"6000000003491986946"
#   P40 child = Q467497 Aadne Eivindson Garborg
Q141152523	P40	Q467497	S2600	"6000000003491986946"
#   P40 child = Q141152600 Stine Stena Eivindsdatter Garborg
Q141152523	P40	Q141152600	S2600	"6000000003491986946"
#   P40 child = Q141152614 Jon Eivindson Garborg
Q141152523	P40	Q141152614	S2600	"6000000003491986946"
#   P40 child = Q141162040 Samuel Eivindsen Garborg
Q141152523	P40	Q141162040	S2600	"6000000003491986946"
#   P40 child = Q141162041 Even Eivindson Garborg
Q141152523	P40	Q141162041	S2600	"6000000003491986946"
#   P40 child = Q141162043 Inger Marie Mary Eivindsdatter Garborg
Q141152523	P40	Q141162043	S2600	"6000000003491986946"
#   P40 child = Q141162044 Abel Eivindsen Garborg
Q141152523	P40	Q141162044	S2600	"6000000003491986946"
#   P40 child = Q141162045 Ole Eivindsen Garborg
Q141152523	P40	Q141162045	S2600	"6000000003491986946"
#   P40 child = Q141162046 Ane Oline Lena Eivindsdatter Garborg
Q141152523	P40	Q141162046	S2600	"6000000003491986946"
#   P3373 sibling = Q141169046 Samuel Jonson
Q141152523	P3373	Q141169046	S2600	"6000000003491986946"
#   P26 spouse = Q141168957 Jonas Jonson Heigre
Q141152523	P26	Q141168957	S2600	"6000000003491986946"
#   P26 spouse = Q141152512 Eivind Aadnesson Garborg
Q141152523	P26	Q141152512	S2600	"6000000003491986946"
#   P735 given name = Q11958077 Ane, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141152523	P735	Q11958077	P1545	"1"	P7452	Q3409033
#   P735 given name = Q11993741 Oline, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141152523	P735	Q11993741	P1545	"2"	P3831	Q245025
#   set the ja label to "アーネ・オリーネ・ヨンスダッテル・ラウグスタード"
Q141152523	Lja	"アーネ・オリーネ・ヨンスダッテル・ラウグスタード"
#   set the zh label to "安内·奥利内·永斯达特·劳格斯塔"
Q141152523	Lzh	"安内·奥利内·永斯达特·劳格斯塔"
#   Q141178198 Enevald Jonasson Heigre: P22 father = Q141168957 Jonas Jonson Heigre
Q141178198	P22	Q141168957	S2600	"6000000003491986956"
#   P25 mother = Q141178196 Elisabet Kirstine Eriksdatter Stangeland
Q141178198	P25	Q141178196	S2600	"6000000003491986956"
#   P735 given name = Q111085860 Enevald
Q141178198	P735	Q111085860
#   Q141169046 Samuel Jonson: P22 father = Q141168955 Jon Samuelsen Raustad
Q141169046	P22	Q141168955	S2600	"6000000003491988821"
#   P25 mother = Q141178200 Inger Kristoffersdatter
Q141169046	P25	Q141178200	S2600	"6000000003491988821"
#   P3373 sibling = Q141152523 Ane Oline Jonsdatter Raugstad
Q141169046	P3373	Q141152523	S2600	"6000000003491988821"
#   P735 given name = Q629347 Samuel
Q141169046	P735	Q629347
#   set the ja label to "サムエル・ヨンソン"
Q141169046	Lja	"サムエル・ヨンソン"
#   set the zh label to "萨穆埃尔·永松"
Q141169046	Lzh	"萨穆埃尔·永松"
#   Q141178381 Marta Jonsdatter Li: P22 father = Q141180408 Jon Larsson Li
Q141178381	P22	Q141180408	S2600	"6000000003491988826"
#   P25 mother = Q141180412 Marta Rasmusdatter Høle
Q141178381	P25	Q141180412	S2600	"6000000003491988826"
#   P40 child = Q141168955 Jon Samuelsen Raustad
Q141178381	P40	Q141168955	S2600	"6000000003491988826"
#   P26 spouse = Q141178380 Samuel Jonson Raustad
Q141178381	P26	Q141178380	S2600	"6000000003491988826"
#   P735 given name = Q846741 Marta
Q141178381	P735	Q846741
#   Q141178380 Samuel Jonson Raustad: P40 child = Q141168955 Jon Samuelsen Raustad
Q141178380	P40	Q141168955	S2600	"6000000003491988831"
#   P26 spouse = Q141178381 Marta Jonsdatter Li
Q141178380	P26	Q141178381	S2600	"6000000003491988831"
#   P735 given name = Q629347 Samuel
Q141178380	P735	Q629347
#   set the ja label to "サムエル・ヨンソン・ラウスタード"
Q141178380	Lja	"サムエル・ヨンソン・ラウスタード"
#   set the zh label to "萨穆埃尔·永松·劳斯塔"
Q141178380	Lzh	"萨穆埃尔·永松·劳斯塔"
#   Q141152512 Eivind Aadnesson Garborg: P22 father = Q141169072 Ådne Olsen Grøtheim
Q141152512	P22	Q141169072	S2600	"6000000003492005111"
#   P25 mother = Q141178202 Stine Persdatter Øksnevad
Q141152512	P25	Q141178202	S2600	"6000000003492005111"
#   P40 child = Q467497 Aadne Eivindson Garborg
Q141152512	P40	Q467497	S2600	"6000000003492005111"
#   P40 child = Q141152600 Stine Stena Eivindsdatter Garborg
Q141152512	P40	Q141152600	S2600	"6000000003492005111"
#   P40 child = Q141152614 Jon Eivindson Garborg
Q141152512	P40	Q141152614	S2600	"6000000003492005111"
#   P40 child = Q141162040 Samuel Eivindsen Garborg
Q141152512	P40	Q141162040	S2600	"6000000003492005111"
#   P40 child = Q141162041 Even Eivindson Garborg
Q141152512	P40	Q141162041	S2600	"6000000003492005111"
#   P40 child = Q141162043 Inger Marie Mary Eivindsdatter Garborg
Q141152512	P40	Q141162043	S2600	"6000000003492005111"
#   P40 child = Q141162044 Abel Eivindsen Garborg
Q141152512	P40	Q141162044	S2600	"6000000003492005111"
#   P40 child = Q141162045 Ole Eivindsen Garborg
Q141152512	P40	Q141162045	S2600	"6000000003492005111"
#   P40 child = Q141162046 Ane Oline Lena Eivindsdatter Garborg
Q141152512	P40	Q141162046	S2600	"6000000003492005111"
#   P3373 sibling = Q141168833 Ingeborg Gurie Ådnesdatter Garborg
Q141152512	P3373	Q141168833	S2600	"6000000003492005111"
#   P3373 sibling = Q141168816 Elisabet Ådnesdatter Garborg
Q141152512	P3373	Q141168816	S2600	"6000000003492005111"
#   P26 spouse = Q141152523 Ane Oline Jonsdatter Raugstad
Q141152512	P26	Q141152523	S2600	"6000000003492005111"
#   set the ja label to "エイヴィン・オードネソン・ガルボルグ"
Q141152512	Lja	"エイヴィン・オードネソン・ガルボルグ"
#   set the zh label to "埃温·奥德内松·加尔博格"
Q141152512	Lzh	"埃温·奥德内松·加尔博格"
#   Q467497 Aadne Eivindson Garborg: P40 child = Q11959067 Arne Olaus Fjørtoft Garborg
Q467497	P40	Q11959067	S2600	"6000000003492005116"
#   P3373 sibling = Q141152600 Stine Stena Eivindsdatter Garborg
Q467497	P3373	Q141152600	S2600	"6000000003492005116"
#   P3373 sibling = Q141152614 Jon Eivindson Garborg
Q467497	P3373	Q141152614	S2600	"6000000003492005116"
#   P3373 sibling = Q141162040 Samuel Eivindsen Garborg
Q467497	P3373	Q141162040	S2600	"6000000003492005116"
#   P3373 sibling = Q141162041 Even Eivindson Garborg
Q467497	P3373	Q141162041	S2600	"6000000003492005116"
#   P26 spouse = Q3143008 Karen Hulda Bergersen
Q467497	P26	Q3143008	S2600	"6000000003492005116"
#   Q141152600 Stine Stena Eivindsdatter Garborg: P40 child = Q141168794 Betsy Jacobson
Q141152600	P40	Q141168794	S2600	"6000000003492005121"
#   P735 given name = Q20022872 Stine, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141152600	P735	Q20022872	P1545	"1"	P7452	Q3409033
#   P734 family name = Q30250555 Garborg
Q141152600	P734	Q30250555
#   set the ja label to "スティーネ・ステーナ・エイヴィンスダッテル・ガルボルグ"
Q141152600	Lja	"スティーネ・ステーナ・エイヴィンスダッテル・ガルボルグ"
#   set the zh label to "斯蒂内·斯泰娜·埃温斯达特·加尔博格"
Q141152600	Lzh	"斯蒂内·斯泰娜·埃温斯达特·加尔博格"
#   Q141152614 Jon Eivindson Garborg: P40 child = Q141168811 Eivind Garborg
Q141152614	P40	Q141168811	S2600	"6000000003492005126"
#   P40 child = Q141168792 Astrid Garborg
Q141152614	P40	Q141168792	S2600	"6000000003492005126"
#   P40 child = Q141168837 Ingebret Garborg
Q141152614	P40	Q141168837	S2600	"6000000003492005126"
#   P40 child = Q141168830 Ingeborg Garborg
Q141152614	P40	Q141168830	S2600	"6000000003492005126"
#   P40 child = Q141168954 Jon Garborg
Q141152614	P40	Q141168954	S2600	"6000000003492005126"
#   P40 child = Q141168784 Aagot Garborg
Q141152614	P40	Q141168784	S2600	"6000000003492005126"
#   P735 given name = Q13501137 Jon
Q141152614	P735	Q13501137
#   P734 family name = Q30250555 Garborg
Q141152614	P734	Q30250555
#   set the ja label to "ヨン・エイヴィンソン・ガルボルグ"
Q141152614	Lja	"ヨン・エイヴィンソン・ガルボルグ"
#   set the zh label to "永·埃温松·加尔博格"
Q141152614	Lzh	"永·埃温松·加尔博格"
#   Q141162040 Samuel Eivindsen Garborg: P735 given name = Q629347 Samuel
Q141162040	P735	Q629347
#   P734 family name = Q30250555 Garborg
Q141162040	P734	Q30250555
#   set the ja label to "サムエル・エイヴィンセン・ガルボルグ"
Q141162040	Lja	"サムエル・エイヴィンセン・ガルボルグ"
#   set the zh label to "萨穆埃尔·埃温森·加尔博格"
Q141162040	Lzh	"萨穆埃尔·埃温森·加尔博格"
#   Q141162041 Even Eivindson Garborg: P735 given name = Q4567129 Even
Q141162041	P735	Q4567129
#   P734 family name = Q30250555 Garborg
Q141162041	P734	Q30250555
#   set the ja label to "エーヴェン・エイヴィンソン・ガルボルグ"
Q141162041	Lja	"エーヴェン・エイヴィンソン・ガルボルグ"
#   set the zh label to "埃文·埃温松·加尔博格"
Q141162041	Lzh	"埃文·埃温松·加尔博格"
#   Q141162043 Inger Marie Mary Eivindsdatter Garborg: P40 child = Q141168820 Eliza Ronneberg
Q141162043	P40	Q141168820	S2600	"6000000003492005141"
#   P40 child = Q141168789 Arnold Ronneberg
Q141162043	P40	Q141168789	S2600	"6000000003492005141"
#   P40 child = Q141168805 Edward Ronneberg
Q141162043	P40	Q141168805	S2600	"6000000003492005141"
#   P40 child = Q141168786 Alice Ronneberg
Q141162043	P40	Q141168786	S2600	"6000000003492005141"
#   P40 child = Q141168824 Ernest Anton Ronneberg
Q141162043	P40	Q141168824	S2600	"6000000003492005141"
#   P735 given name = Q3358452 Inger, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141162043	P735	Q3358452	P1545	"1"	P7452	Q3409033
#   P735 given name = Q106674406 Marie, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141162043	P735	Q106674406	P1545	"2"	P3831	Q245025
#   P734 family name = Q30250555 Garborg
Q141162043	P734	Q30250555
#   set the ja label to "インゲル・マリー・メアリー・エイヴィンスダッテル・ガルボルグ"
Q141162043	Lja	"インゲル・マリー・メアリー・エイヴィンスダッテル・ガルボルグ"
#   set the zh label to "英厄尔·玛丽·玛丽·埃温斯达特·加尔博格"
Q141162043	Lzh	"英厄尔·玛丽·玛丽·埃温斯达特·加尔博格"
#   Q141162044 Abel Eivindsen Garborg: P735 given name = Q318375 Abel
Q141162044	P735	Q318375
#   P734 family name = Q30250555 Garborg
Q141162044	P734	Q30250555
#   set the ja label to "アーベル・エイヴィンセン・ガルボルグ"
Q141162044	Lja	"アーベル・エイヴィンセン・ガルボルグ"
#   set the zh label to "阿贝尔·埃温森·加尔博格"
Q141162044	Lzh	"阿贝尔·埃温森·加尔博格"
#   Q141162045 Ole Eivindsen Garborg: P735 given name = Q2097883 Ole
Q141162045	P735	Q2097883
#   P734 family name = Q30250555 Garborg
Q141162045	P734	Q30250555
#   set the ja label to "オーレ・エイヴィンセン・ガルボルグ"
Q141162045	Lja	"オーレ・エイヴィンセン・ガルボルグ"
#   set the zh label to "奥勒·埃温森·加尔博格"
Q141162045	Lzh	"奥勒·埃温森·加尔博格"
#   Q141162046 Ane Oline Lena Eivindsdatter Garborg: P40 child = Q141169062 Thoralf Tunheim
Q141162046	P40	Q141169062	S2600	"6000000003492005156"
#   P40 child = Q141168801 Cora Estelle Tunheim
Q141162046	P40	Q141168801	S2600	"6000000003492005156"
#   P40 child = Q141168809 Edward Tunheim
Q141162046	P40	Q141168809	S2600	"6000000003492005156"
#   P40 child = Q141168787 Alma Matilda Tunheim
Q141162046	P40	Q141168787	S2600	"6000000003492005156"
#   P40 child = Q141169041 Olaf Tunheim
Q141162046	P40	Q141169041	S2600	"6000000003492005156"
#   P40 child = Q141168788 Arne Garborg Tunheim
Q141162046	P40	Q141168788	S2600	"6000000003492005156"
#   P735 given name = Q11958077 Ane, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141162046	P735	Q11958077	P1545	"1"	P7452	Q3409033
#   P735 given name = Q11993741 Oline, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141162046	P735	Q11993741	P1545	"2"	P3831	Q245025
#   P734 family name = Q30250555 Garborg
Q141162046	P734	Q30250555
#   set the ja label to "アーネ・オリーネ・レーナ・エイヴィンスダッテル・ガルボルグ"
Q141162046	Lja	"アーネ・オリーネ・レーナ・エイヴィンスダッテル・ガルボルグ"
#   set the zh label to "安内·奥利内·莱娜·埃温斯达特·加尔博格"
Q141162046	Lzh	"安内·奥利内·莱娜·埃温斯达特·加尔博格"
#   Q141169072 Ådne Olsen Grøtheim: P40 child = Q141152512 Eivind Aadnesson Garborg
Q141169072	P40	Q141152512	S2600	"6000000003492005161"
#   P40 child = Q141168833 Ingeborg Gurie Ådnesdatter Garborg
Q141169072	P40	Q141168833	S2600	"6000000003492005161"
#   P40 child = Q141168816 Elisabet Ådnesdatter Garborg
Q141169072	P40	Q141168816	S2600	"6000000003492005161"
#   P26 spouse = Q141178202 Stine Persdatter Øksnevad
Q141169072	P26	Q141178202	S2600	"6000000003492005161"
#   set the ja label to "オードネ・オルセン・グレートヘイム"
Q141169072	Lja	"オードネ・オルセン・グレートヘイム"
#   set the zh label to "奥德内·奥尔森·格勒特海姆"
Q141169072	Lzh	"奥德内·奥尔森·格勒特海姆"
#   Q141178202 Stine Persdatter Øksnevad: P40 child = Q141152512 Eivind Aadnesson Garborg
Q141178202	P40	Q141152512	S2600	"6000000003492005166"
#   P40 child = Q141168833 Ingeborg Gurie Ådnesdatter Garborg
Q141178202	P40	Q141168833	S2600	"6000000003492005166"
#   P40 child = Q141168816 Elisabet Ådnesdatter Garborg
Q141178202	P40	Q141168816	S2600	"6000000003492005166"
#   P26 spouse = Q141169072 Ådne Olsen Grøtheim
Q141178202	P26	Q141169072	S2600	"6000000003492005166"
#   P735 given name = Q20022872 Stine
Q141178202	P735	Q20022872
#   P734 family name = Q30583490 Øksnevad
Q141178202	P734	Q30583490
#   set the ja label to "スティーネ・ペシュダッテル・エクスネヴァード"
Q141178202	Lja	"スティーネ・ペシュダッテル・エクスネヴァード"
#   set the zh label to "斯蒂内·佩斯达特·厄克斯内瓦"
Q141178202	Lzh	"斯蒂内·佩斯达特·厄克斯内瓦"
#   Q141168833 Ingeborg Gurie Ådnesdatter Garborg: P22 father = Q141169072 Ådne Olsen Grøtheim
Q141168833	P22	Q141169072	S2600	"6000000003492005171"
#   P25 mother = Q141178202 Stine Persdatter Øksnevad
Q141168833	P25	Q141178202	S2600	"6000000003492005171"
#   P735 given name = Q656590 Ingeborg, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141168833	P735	Q656590	P1545	"1"	P7452	Q3409033
#   P734 family name = Q30250555 Garborg
Q141168833	P734	Q30250555
#   set the ja label to "インゲボルグ・グーリエ・オードネスダッテル・ガルボルグ"
Q141168833	Lja	"インゲボルグ・グーリエ・オードネスダッテル・ガルボルグ"
#   set the zh label to "英厄堡·古里·奥德内斯达特·加尔博格"
Q141168833	Lzh	"英厄堡·古里·奥德内斯达特·加尔博格"
#   Q141168816 Elisabet Ådnesdatter Garborg: P22 father = Q141169072 Ådne Olsen Grøtheim
Q141168816	P22	Q141169072	S2600	"6000000003492005176"
#   P25 mother = Q141178202 Stine Persdatter Øksnevad
Q141168816	P25	Q141178202	S2600	"6000000003492005176"
#   P735 given name = Q16423275 Elisabet
Q141168816	P735	Q16423275
#   P734 family name = Q30250555 Garborg
Q141168816	P734	Q30250555
#   set the ja label to "エリサベート・オードネスダッテル・ガルボルグ"
Q141168816	Lja	"エリサベート・オードネスダッテル・ガルボルグ"
#   set the zh label to "伊丽莎白·奥德内斯达特·加尔博格"
Q141168816	Lzh	"伊丽莎白·奥德内斯达特·加尔博格"
#   Q141168955 Jon Samuelsen Raustad: P22 father = Q141178380 Samuel Jonson Raustad
Q141168955	P22	Q141178380	S2600	"6000000003732742137"
#   P25 mother = Q141178381 Marta Jonsdatter Li
Q141168955	P25	Q141178381	S2600	"6000000003732742137"
#   P40 child = Q141152523 Ane Oline Jonsdatter Raugstad
Q141168955	P40	Q141152523	S2600	"6000000003732742137"
#   P40 child = Q141169046 Samuel Jonson
Q141168955	P40	Q141169046	S2600	"6000000003732742137"
#   P26 spouse = Q141178200 Inger Kristoffersdatter
Q141168955	P26	Q141178200	S2600	"6000000003732742137"
#   P735 given name = Q13501137 Jon
Q141168955	P735	Q13501137
#   set the ja label to "ヨン・サムエルセン・ラウスタード"
Q141168955	Lja	"ヨン・サムエルセン・ラウスタード"
#   set the zh label to "永·萨穆埃尔森·劳斯塔"
Q141168955	Lzh	"永·萨穆埃尔森·劳斯塔"
#   Q633094 Johannes Tomasson: P22 father = Q141180413 Thomas Mattsson
Q633094	P22	Q141180413	S2600	"6000000004334763223"
#   P25 mother = Q141180409 Magdalena Andersdotter Bure
Q633094	P25	Q141180409	S2600	"6000000004334763223"
#   P26 spouse = Q141180410 Margareta Mårtensdotter Bång
Q633094	P26	Q141180410	S2600	"6000000004334763223"
#   P26 spouse = Q141180406 Ingeborg Gyntesdotter
Q633094	P26	Q141180406	S2600	"6000000004334763223"
#   Q141180413 Thomas Mattsson: P40 child = Q633094 Johannes Tomasson
Q141180413	P40	Q633094	S2600	"6000000004334768506"
#   P26 spouse = Q141180409 Magdalena Andersdotter Bure
Q141180413	P26	Q141180409	S2600	"6000000004334768506"
#   Q141178149 Anna Fartegnsdatter Seim: P734 family name = Q30088373 Seim
Q141178149	P734	Q30088373
#   Q3143008 Karen Hulda Bergersen: P22 father = Q141168797 Christian Frederik Bergersen
Q3143008	P22	Q141168797	S2600	"6000000005606976813"
#   P25 mother = Q141178201 Marie Petrine Simensdatter Bergersen
Q3143008	P25	Q141178201	S2600	"6000000005606976813"
#   P40 child = Q11959067 Arne Olaus Fjørtoft Garborg
Q3143008	P40	Q11959067	S2600	"6000000005606976813"
#   P26 spouse = Q467497 Aadne Eivindson Garborg
Q3143008	P26	Q467497	S2600	"6000000005606976813"
#   Q11959067 Arne Olaus Fjørtoft Garborg: P40 child = Q141168827 Hans Eivind Garborg
Q11959067	P40	Q141168827	S2600	"6000000005607426327"
#   P26 spouse = Q141168785 Aagot Nyvold
Q11959067	P26	Q141168785	S2600	"6000000005607426327"
#   P26 spouse = Q141168803 Dagny Nyvold
Q11959067	P26	Q141168803	S2600	"6000000005607426327"
#   set the ja label to "アルネ・オーラウス・フョルトフト・ガルボルグ"
Q11959067	Lja	"アルネ・オーラウス・フョルトフト・ガルボルグ"
#   set the zh label to "阿尔内·奥劳斯·夫约托夫特·加尔博格"
Q11959067	Lzh	"阿尔内·奥劳斯·夫约托夫特·加尔博格"
#   Q141168827 Hans Eivind Garborg: P22 father = Q11959067 Arne Olaus Fjørtoft Garborg
Q141168827	P22	Q11959067	S2600	"6000000005607426344"
#   P25 mother = Q141168785 Aagot Nyvold
Q141168827	P25	Q141168785	S2600	"6000000005607426344"
#   P735 given name = Q3358418 Eivind, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141168827	P735	Q3358418	P1545	"2"	P3831	Q245025
#   P734 family name = Q30250555 Garborg
Q141168827	P734	Q30250555
#   set the ja label to "ハンス・エイヴィン・ガルボルグ"
Q141168827	Lja	"ハンス・エイヴィン・ガルボルグ"
#   set the zh label to "汉斯·埃温·加尔博格"
Q141168827	Lzh	"汉斯·埃温·加尔博格"
#   Q141178200 Inger Kristoffersdatter: P40 child = Q141152523 Ane Oline Jonsdatter Raugstad
Q141178200	P40	Q141152523	S2600	"6000000005609534511"
#   P40 child = Q141169046 Samuel Jonson
Q141178200	P40	Q141169046	S2600	"6000000005609534511"
#   P26 spouse = Q141168955 Jon Samuelsen Raustad
Q141178200	P26	Q141168955	S2600	"6000000005609534511"
#   P735 given name = Q3358452 Inger
Q141178200	P735	Q3358452
#   set the ja label to "インゲル・クリストッフェシュダッテル"
Q141178200	Lja	"インゲル・クリストッフェシュダッテル"
#   set the zh label to "英厄尔·克里斯托弗斯达特"
Q141178200	Lzh	"英厄尔·克里斯托弗斯达特"
#   Q141180408 Jon Larsson Li: P40 child = Q141178381 Marta Jonsdatter Li
Q141180408	P40	Q141178381	S2600	"6000000005609534542"
#   P26 spouse = Q141180412 Marta Rasmusdatter Høle
Q141180408	P26	Q141180412	S2600	"6000000005609534542"
#   P735 given name = Q13501137 Jon
Q141180408	P735	Q13501137
#   Q141180412 Marta Rasmusdatter Høle: P40 child = Q141178381 Marta Jonsdatter Li
Q141180412	P40	Q141178381	S2600	"6000000005609534550"
#   P26 spouse = Q141180408 Jon Larsson Li
Q141180412	P26	Q141180408	S2600	"6000000005609534550"
#   P735 given name = Q846741 Marta
Q141180412	P735	Q846741
#   Q141180409 Magdalena Andersdotter Bure: P40 child = Q633094 Johannes Tomasson
Q141180409	P40	Q633094	S2600	"6000000006127859575"
#   P26 spouse = Q141180413 Thomas Mattsson
Q141180409	P26	Q141180413	S2600	"6000000006127859575"
#   P735 given name = Q842544 Magdalena, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141180409	P735	Q842544	P1545	"1"	P7452	Q3409033
#   Q141168811 Eivind Garborg: P22 father = Q141152614 Jon Eivindson Garborg
Q141168811	P22	Q141152614	S2600	"6000000006570861816"
#   P735 given name = Q3358418 Eivind
Q141168811	P735	Q3358418
#   P734 family name = Q30250555 Garborg
Q141168811	P734	Q30250555
#   set the ja label to "エイヴィン・ガルボルグ"
Q141168811	Lja	"エイヴィン・ガルボルグ"
#   set the zh label to "埃温·加尔博格"
Q141168811	Lzh	"埃温·加尔博格"
#   Q141168792 Astrid Garborg: P22 father = Q141152614 Jon Eivindson Garborg
Q141168792	P22	Q141152614	S2600	"6000000006572523374"
#   P735 given name = Q167755 Astrid
Q141168792	P735	Q167755
#   P734 family name = Q30250555 Garborg
Q141168792	P734	Q30250555
#   set the ja label to "アストリッド・ガルボルグ"
Q141168792	Lja	"アストリッド・ガルボルグ"
#   set the zh label to "阿斯特丽德·加尔博格"
Q141168792	Lzh	"阿斯特丽德·加尔博格"
#   Q141168837 Ingebret Garborg: P22 father = Q141152614 Jon Eivindson Garborg
Q141168837	P22	Q141152614	S2600	"6000000006572799149"
#   P735 given name = Q30229695 Ingebret
Q141168837	P735	Q30229695
#   P734 family name = Q30250555 Garborg
Q141168837	P734	Q30250555
#   set the ja label to "インゲブレート・ガルボルグ"
Q141168837	Lja	"インゲブレート・ガルボルグ"
#   set the zh label to "英厄布雷特·加尔博格"
Q141168837	Lzh	"英厄布雷特·加尔博格"
#   Q141168830 Ingeborg Garborg: P22 father = Q141152614 Jon Eivindson Garborg
Q141168830	P22	Q141152614	S2600	"6000000006573130134"
#   P735 given name = Q656590 Ingeborg
Q141168830	P735	Q656590
#   P734 family name = Q30250555 Garborg
Q141168830	P734	Q30250555
#   set the ja label to "インゲボルグ・ガルボルグ"
Q141168830	Lja	"インゲボルグ・ガルボルグ"
#   set the zh label to "英厄堡·加尔博格"
Q141168830	Lzh	"英厄堡·加尔博格"
#   Q141168954 Jon Garborg: P22 father = Q141152614 Jon Eivindson Garborg
Q141168954	P22	Q141152614	S2600	"6000000006573294012"
#   P735 given name = Q13501137 Jon
Q141168954	P735	Q13501137
#   P734 family name = Q30250555 Garborg
Q141168954	P734	Q30250555
#   set the ja label to "ヨン・ガルボルグ"
Q141168954	Lja	"ヨン・ガルボルグ"
#   set the zh label to "永·加尔博格"
Q141168954	Lzh	"永·加尔博格"
#   Q141178201 Marie Petrine Simensdatter Bergersen: P40 child = Q3143008 Karen Hulda Bergersen
Q141178201	P40	Q3143008	S2600	"6000000009126235990"
#   P26 spouse = Q141168797 Christian Frederik Bergersen
Q141178201	P26	Q141168797	S2600	"6000000009126235990"
#   P735 given name = Q106674406 Marie, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141178201	P735	Q106674406	P1545	"1"	P7452	Q3409033
#   P735 given name = Q107227465 Petrine, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141178201	P735	Q107227465	P1545	"2"	P3831	Q245025
#   set the ja label to "マリー・ペトリーネ・シメンスダッテル・ベルゲルセン"
Q141178201	Lja	"マリー・ペトリーネ・シメンスダッテル・ベルゲルセン"
#   set the zh label to "玛丽·佩特里内·西门斯达特·贝格尔森"
Q141178201	Lzh	"玛丽·佩特里内·西门斯达特·贝格尔森"
#   Q141168797 Christian Frederik Bergersen: P22 father = Q141178199 Gunder Bergersen
Q141168797	P22	Q141178199	S2600	"6000000009126453497"
#   P25 mother = Q141180395 Maren Gulbrandsdatter Ommestad
Q141168797	P25	Q141180395	S2600	"6000000009126453497"
#   P40 child = Q3143008 Karen Hulda Bergersen
Q141168797	P40	Q3143008	S2600	"6000000009126453497"
#   P26 spouse = Q141178201 Marie Petrine Simensdatter Bergersen
Q141168797	P26	Q141178201	S2600	"6000000009126453497"
#   P735 given name = Q18001597 Christian, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141168797	P735	Q18001597	P1545	"1"	P7452	Q3409033
#   P735 given name = Q17539077 Frederik, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141168797	P735	Q17539077	P1545	"2"	P3831	Q245025
#   set the ja label to "クリスチャン・フレデリク・ベルゲルセン"
Q141168797	Lja	"クリスチャン・フレデリク・ベルゲルセン"
#   set the zh label to "克里斯蒂安·弗雷德里克·贝格尔森"
Q141168797	Lzh	"克里斯蒂安·弗雷德里克·贝格尔森"
#   Q141180410 Margareta Mårtensdotter Bång: P26 spouse = Q633094 Johannes Tomasson
Q141180410	P26	Q633094	S2600	"6000000012566410426"
#   P735 given name = Q8274988 Margareta, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141180410	P735	Q8274988	P1545	"1"	P7452	Q3409033
#   Q141178199 Gunder Bergersen: P40 child = Q141168797 Christian Frederik Bergersen
Q141178199	P40	Q141168797	S2600	"6000000016756402733"
#   P26 spouse = Q141180395 Maren Gulbrandsdatter Ommestad
Q141178199	P26	Q141180395	S2600	"6000000016756402733"
#   P735 given name = Q989832 Gunder
Q141178199	P735	Q989832
#   Q141180395 Maren Gulbrandsdatter Ommestad: P40 child = Q141168797 Christian Frederik Bergersen
Q141180395	P40	Q141168797	S2600	"6000000020221673906"
#   P26 spouse = Q141178199 Gunder Bergersen
Q141180395	P26	Q141178199	S2600	"6000000020221673906"
#   P735 given name = Q1666203 Maren
Q141180395	P735	Q1666203
#   Q141168784 Aagot Garborg: P22 father = Q141152614 Jon Eivindson Garborg
Q141168784	P22	Q141152614	S2600	"6000000021079935250"
#   P735 given name = Q3482557 Aagot
Q141168784	P735	Q3482557
#   P734 family name = Q30250555 Garborg
Q141168784	P734	Q30250555
#   set the ja label to "オーゴット・ガルボルグ"
Q141168784	Lja	"オーゴット・ガルボルグ"
#   set the zh label to "奥高特·加尔博格"
Q141168784	Lzh	"奥高特·加尔博格"
#   Q138474188 Hans Syvertsen Nyvold: P40 child = Q141168785 Aagot Nyvold
Q138474188	P40	Q141168785	S2600	"6000000021197598122"
#   P40 child = Q141168803 Dagny Nyvold
Q138474188	P40	Q141168803	S2600	"6000000021197598122"
#   P26 spouse = Q141178197 Elisabeth Johannesen
Q138474188	P26	Q141178197	S2600	"6000000021197598122"
#   Q141168785 Aagot Nyvold: P22 father = Q138474188 Hans Syvertsen Nyvold
Q141168785	P22	Q138474188	S2600	"6000000021197722738"
#   P25 mother = Q141178197 Elisabeth Johannesen
Q141168785	P25	Q141178197	S2600	"6000000021197722738"
#   P40 child = Q141168827 Hans Eivind Garborg
Q141168785	P40	Q141168827	S2600	"6000000021197722738"
#   P26 spouse = Q11959067 Arne Olaus Fjørtoft Garborg
Q141168785	P26	Q11959067	S2600	"6000000021197722738"
#   P735 given name = Q3482557 Aagot
Q141168785	P735	Q3482557
#   set the ja label to "オーゴット・ニーヴォル"
Q141168785	Lja	"オーゴット・ニーヴォル"
#   set the zh label to "奥高特·尼沃尔"
Q141168785	Lzh	"奥高特·尼沃尔"
#   Q141168803 Dagny Nyvold: P22 father = Q138474188 Hans Syvertsen Nyvold
Q141168803	P22	Q138474188	S2600	"6000000021197841042"
#   P25 mother = Q141178197 Elisabeth Johannesen
Q141168803	P25	Q141178197	S2600	"6000000021197841042"
#   P26 spouse = Q11959067 Arne Olaus Fjørtoft Garborg
Q141168803	P26	Q11959067	S2600	"6000000021197841042"
#   P735 given name = Q1157346 Dagny
Q141168803	P735	Q1157346
#   set the ja label to "ダグニー・ニーヴォル"
Q141168803	Lja	"ダグニー・ニーヴォル"
#   set the zh label to "达格妮·尼沃尔"
Q141168803	Lzh	"达格妮·尼沃尔"
#   Q141178197 Elisabeth Johannesen: P40 child = Q141168785 Aagot Nyvold
Q141178197	P40	Q141168785	S2600	"6000000021198042859"
#   P40 child = Q141168803 Dagny Nyvold
Q141178197	P40	Q141168803	S2600	"6000000021198042859"
#   P26 spouse = Q138474188 Hans Syvertsen Nyvold
Q141178197	P26	Q138474188	S2600	"6000000021198042859"
#   P735 given name = Q63611044 Elisabeth
Q141178197	P735	Q63611044
#   Q141180406 Ingeborg Gyntesdotter: P26 spouse = Q633094 Johannes Tomasson
Q141180406	P26	Q633094	S2600	"6000000027324391291"
#   P735 given name = Q656590 Ingeborg
Q141180406	P735	Q656590
#   Q141169062 Thoralf Tunheim: P25 mother = Q141162046 Ane Oline Lena Eivindsdatter Garborg
Q141169062	P25	Q141162046	S2600	"6000000033773881611"
#   set the ja label to "トーラルフ・トゥンヘイム"
Q141169062	Lja	"トーラルフ・トゥンヘイム"
#   set the zh label to "托拉尔夫·通海姆"
Q141169062	Lzh	"托拉尔夫·通海姆"
#   Q141168801 Cora Estelle Tunheim: P25 mother = Q141162046 Ane Oline Lena Eivindsdatter Garborg
Q141168801	P25	Q141162046	S2600	"6000000033773908408"
#   P735 given name = Q714938 Cora, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141168801	P735	Q714938	P1545	"1"	P7452	Q3409033
#   P735 given name = Q744012 Estelle, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141168801	P735	Q744012	P1545	"2"	P3831	Q245025
#   set the ja label to "コーラ・エステル・トゥンヘイム"
Q141168801	Lja	"コーラ・エステル・トゥンヘイム"
#   set the zh label to "科拉·埃斯特尔·通海姆"
Q141168801	Lzh	"科拉·埃斯特尔·通海姆"
#   Q141168809 Edward Tunheim: P25 mother = Q141162046 Ane Oline Lena Eivindsdatter Garborg
Q141168809	P25	Q141162046	S2600	"6000000033773925586"
#   P735 given name = Q278835 Edward
Q141168809	P735	Q278835
#   set the ja label to "エドワード・トゥンヘイム"
Q141168809	Lja	"エドワード・トゥンヘイム"
#   set the zh label to "爱德华·通海姆"
Q141168809	Lzh	"爱德华·通海姆"
#   Q141168787 Alma Matilda Tunheim: P25 mother = Q141162046 Ane Oline Lena Eivindsdatter Garborg
Q141168787	P25	Q141162046	S2600	"6000000033774070464"
#   P735 given name = Q656870 Alma, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141168787	P735	Q656870	P1545	"1"	P7452	Q3409033
#   P735 given name = Q2054021 Matilda, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141168787	P735	Q2054021	P1545	"2"	P3831	Q245025
#   set the ja label to "アルマ・マチルダ・トゥンヘイム"
Q141168787	Lja	"アルマ・マチルダ・トゥンヘイム"
#   set the zh label to "阿尔玛·玛蒂尔达·通海姆"
Q141168787	Lzh	"阿尔玛·玛蒂尔达·通海姆"
#   Q141169041 Olaf Tunheim: P25 mother = Q141162046 Ane Oline Lena Eivindsdatter Garborg
Q141169041	P25	Q141162046	S2600	"6000000033774204088"
#   P735 given name = Q3881452 Olaf
Q141169041	P735	Q3881452
#   set the ja label to "オーラフ・トゥンヘイム"
Q141169041	Lja	"オーラフ・トゥンヘイム"
#   set the zh label to "奥拉夫·通海姆"
Q141169041	Lzh	"奥拉夫·通海姆"
#   Q4953376 Helena Guttormsdatter: P40 child = Q3743799 Knut Valdemarsson Duke of Estland, Blekinge and Lolland
Q4953376	P40	Q3743799	S2600	"6000000034013672054"
#   Q141168820 Eliza Ronneberg: P735 given name = Q858305 Eliza
Q141168820	P735	Q858305
#   set the ja label to "エリザ・ロンネベルグ"
Q141168820	Lja	"エリザ・ロンネベルグ"
#   set the zh label to "伊莱扎·龙内贝格"
Q141168820	Lzh	"伊莱扎·龙内贝格"
#   Q141168789 Arnold Ronneberg: P735 given name = Q3623461 Arnold
Q141168789	P735	Q3623461
#   set the ja label to "アルノルド・ロンネベルグ"
Q141168789	Lja	"アルノルド・ロンネベルグ"
#   set the zh label to "阿诺德·龙内贝格"
Q141168789	Lzh	"阿诺德·龙内贝格"
#   Q141168805 Edward Ronneberg: P735 given name = Q278835 Edward
Q141168805	P735	Q278835
#   set the ja label to "エドワード・ロンネベルグ"
Q141168805	Lja	"エドワード・ロンネベルグ"
#   set the zh label to "爱德华·龙内贝格"
Q141168805	Lzh	"爱德华·龙内贝格"
#   Q141168786 Alice Ronneberg: P735 given name = Q650689 Alice
Q141168786	P735	Q650689
#   set the ja label to "アリス・ロンネベルグ"
Q141168786	Lja	"アリス・ロンネベルグ"
#   set the zh label to "艾丽丝·龙内贝格"
Q141168786	Lzh	"艾丽丝·龙内贝格"
#   Q141168824 Ernest Anton Ronneberg: P735 given name = Q5401576 Anton, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141168824	P735	Q5401576	P1545	"2"	P3831	Q245025
#   set the ja label to "アーネスト・アントン・ロンネベルグ"
Q141168824	Lja	"アーネスト・アントン・ロンネベルグ"
#   set the zh label to "欧内斯特·安东·龙内贝格"
Q141168824	Lzh	"欧内斯特·安东·龙内贝格"
#   Q141168788 Arne Garborg Tunheim: P25 mother = Q141162046 Ane Oline Lena Eivindsdatter Garborg
Q141168788	P25	Q141162046	S2600	"6000000037693739967"
#   P735 given name = Q645757 Arne, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141168788	P735	Q645757	P1545	"1"	P7452	Q3409033
#   set the ja label to "アルネ・ガルボルグ・トゥンヘイム"
Q141168788	Lja	"アルネ・ガルボルグ・トゥンヘイム"
#   set the zh label to "阿尔内·加尔博格·通海姆"
Q141168788	Lzh	"阿尔内·加尔博格·通海姆"
#   Q141180396 Tollef Tollefson Tunheim: P26 spouse = Q141168794 Betsy Jacobson
Q141180396	P26	Q141168794	S2600	"6000000037737683245"
#   P735 given name = Q12006598 Tollef
Q141180396	P735	Q12006598
#   Q141168794 Betsy Jacobson: P26 spouse = Q141180396 Tollef Tollefson Tunheim
Q141168794	P26	Q141180396	S2600	"6000000037737979829"
#   P735 given name = Q832242 Betsy
Q141168794	P735	Q832242
#   set the ja label to "ベッツィ・ヤコブソン"
Q141168794	Lja	"ベッツィ・ヤコブソン"
#   set the zh label to "贝齐·雅各布松"
Q141168794	Lzh	"贝齐·雅各布松"

