# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   2112 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
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

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Eivind Ogmundsson Byre på Høyland"
LAST	Len	"Eivind Ogmundsson Byre på Høyland"
#   set the mul label to "Eivind Ogmundsson Byre på Høyland"
LAST	Lmul	"Eivind Ogmundsson Byre på Høyland"
#   set the ja label to "エイヴィン・オグムンドソン・ビレ・ポー・ホイランド"
LAST	Lja	"エイヴィン・オグムンドソン・ビレ・ポー・ホイランド"
#   set the zh label to "埃温·奥格穆恩德松·比雷·波·霍伊拉恩德"
LAST	Lzh	"埃温·奥格穆恩德松·比雷·波·霍伊拉恩德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000004870612250 Eivind Ogmundsson Byre på Høyland, qualified P1810 subject named as Eivind Ogmundsson Byre på Høyland
LAST	P2600	"6000000004870612250"	P1810	"Eivind Ogmundsson Byre på Høyland"
#   P569 date of birth = +1375-00-00T00:00:00Z/9
LAST	P569	+1375-00-00T00:00:00Z/9	S2600	"6000000004870612250"
#   P570 date of death = +1416-00-00T00:00:00Z/9
LAST	P570	+1416-00-00T00:00:00Z/9	S2600	"6000000004870612250"
#   P26 spouse = Q141216603 Brynhild Hallvardsdotter
LAST	P26	Q141216603	S2600	"6000000004870612250"
#   P40 child = Q141205937 Ragnhild Eyvindsdotter Eyvindsdotter
LAST	P40	Q141205937	S2600	"6000000004870612250"
#   Q141216603 Brynhild Hallvardsdotter: P26 spouse = the item just created
Q141216603	P26	LAST	S2600	"6000000004870612250"
#   Q141205937 Ragnhild Eyvindsdotter Eyvindsdotter: P22 father = the item just created
Q141205937	P22	LAST	S2600	"6000000004870612250"
#   the item just created: P735 given name = Q3358418 Eivind
LAST	P735	Q3358418
#   P1449 nickname = en:"Byre"
LAST	P1449	en:"Byre"
#   add a mul alias "Byre"
LAST	Amul	"Byre"
#   add a mul alias "Eivind Byre"
LAST	Amul	"Eivind Byre"

# create a new item
CREATE
#   set the en label to "Elen Margrethe Stangeland"
LAST	Len	"Elen Margrethe Stangeland"
#   set the mul label to "Elen Margrethe Stangeland"
LAST	Lmul	"Elen Margrethe Stangeland"
#   set the ja label to "エレン・マルグレテ・スタンゲラン"
LAST	Lja	"エレン・マルグレテ・スタンゲラン"
#   set the zh label to "埃莱恩·马尔格雷特·斯坦格兰"
LAST	Lzh	"埃莱恩·马尔格雷特·斯坦格兰"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000011039570406 Elen Margrethe Stangeland, qualified P1810 subject named as Elen Margrethe Stangeland
LAST	P2600	"6000000011039570406"	P1810	"Elen Margrethe Stangeland"
#   P569 date of birth = +1855-01-04T00:00:00Z/11
LAST	P569	+1855-01-04T00:00:00Z/11	S2600	"6000000011039570406"
#   P570 date of death = +1925-06-27T00:00:00Z/11
LAST	P570	+1925-06-27T00:00:00Z/11	S2600	"6000000011039570406"
#   P22 father = Q141198393 Erik Erikson Stangeland
LAST	P22	Q141198393	S2600	"6000000011039570406"
#   P25 mother = Q141217372 Berta Larsdatter Stangeland
LAST	P25	Q141217372	S2600	"6000000011039570406"
#   Q141198393 Erik Erikson Stangeland: P40 child = the item just created
Q141198393	P40	LAST	S2600	"6000000011039570406"
#   Q141217372 Berta Larsdatter Stangeland: P40 child = the item just created
Q141217372	P40	LAST	S2600	"6000000011039570406"
#   the item just created: P735 given name = Q11967041 Elen, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q11967041	P1545	"1"	P7452	Q3409033
#   P735 given name = Q17458337 Margrethe, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q17458337	P1545	"2"	P3831	Q245025
#   P734 family name = Q21452049 Stangeland
LAST	P734	Q21452049

# create a new item
CREATE
#   set the en label to "Gabriel Johansen Obrestad"
LAST	Len	"Gabriel Johansen Obrestad"
#   set the mul label to "Gabriel Johansen Obrestad"
LAST	Lmul	"Gabriel Johansen Obrestad"
#   set the ja label to "ガブリエル・ヨハンセン・オブレスタド"
LAST	Lja	"ガブリエル・ヨハンセン・オブレスタド"
#   set the zh label to "加布里埃尔·永哈恩森·奥布雷斯塔德"
LAST	Lzh	"加布里埃尔·永哈恩森·奥布雷斯塔德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005606920993 Gabriel Johansen Obrestad, qualified P1810 subject named as Gabriel Johansen Obrestad
LAST	P2600	"6000000005606920993"	P1810	"Gabriel Johansen Obrestad"
#   P569 date of birth = +1865-04-16T00:00:00Z/11
LAST	P569	+1865-04-16T00:00:00Z/11	S2600	"6000000005606920993"
#   P22 father = Q141216387 Johannes Svensen Obrestad
LAST	P22	Q141216387	S2600	"6000000005606920993"
#   P25 mother = Q141216363 Anne Govertsdtr. Bratland
LAST	P25	Q141216363	S2600	"6000000005606920993"
#   Q141216387 Johannes Svensen Obrestad: P40 child = the item just created
Q141216387	P40	LAST	S2600	"6000000005606920993"
#   Q141216363 Anne Govertsdtr. Bratland: P40 child = the item just created
Q141216363	P40	LAST	S2600	"6000000005606920993"

# create a new item
CREATE
#   the item just created: set the en label to "Guri Torkjellsdatter Foss-Eikeland"
LAST	Len	"Guri Torkjellsdatter Foss-Eikeland"
#   set the mul label to "Guri Torkjellsdatter Foss-Eikeland"
LAST	Lmul	"Guri Torkjellsdatter Foss-Eikeland"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000035769326152 Guri Torkjellsdatter Foss-Eikeland, qualified P1810 subject named as Guri Torkjellsdatter Foss-Eikeland
LAST	P2600	"6000000035769326152"	P1810	"Guri Torkjellsdatter Foss-Eikeland"
#   P569 date of birth = +1727-00-00T00:00:00Z/9
LAST	P569	+1727-00-00T00:00:00Z/9	S2600	"6000000035769326152"
#   P570 date of death = +1773-00-00T00:00:00Z/9
LAST	P570	+1773-00-00T00:00:00Z/9	S2600	"6000000035769326152"
#   P26 spouse = Q141217404 Osmund Larsen Raunes
LAST	P26	Q141217404	S2600	"6000000035769326152"
#   Q141217404 Osmund Larsen Raunes: P26 spouse = the item just created
Q141217404	P26	LAST	S2600	"6000000035769326152"
#   the item just created: P735 given name = Q11973376 Guri
LAST	P735	Q11973376

# create a new item
CREATE
#   set the en label to "Kornelius Person Øksnevad"
LAST	Len	"Kornelius Person Øksnevad"
#   set the mul label to "Kornelius Person Øksnevad"
LAST	Lmul	"Kornelius Person Øksnevad"
#   set the ja label to "コルネリウス・ペルソン・エクスネヴァード"
LAST	Lja	"コルネリウス・ペルソン・エクスネヴァード"
#   set the zh label to "科尔内利乌斯·佩尔松·厄克斯内瓦"
LAST	Lzh	"科尔内利乌斯·佩尔松·厄克斯内瓦"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005607155254 Kornelius Person Øksnevad, qualified P1810 subject named as Kornelius Person Øksnevad
LAST	P2600	"6000000005607155254"	P1810	"Kornelius Person Øksnevad"
#   P569 date of birth = +1793-00-00T00:00:00Z/9
LAST	P569	+1793-00-00T00:00:00Z/9	S2600	"6000000005607155254"
#   P22 father = Q141200028 Per Jonson Øksnevad
LAST	P22	Q141200028	S2600	"6000000005607155254"
#   P25 mother = Q141199937 Maren Halvorsdatter Øksnevad
LAST	P25	Q141199937	S2600	"6000000005607155254"
#   Q141200028 Per Jonson Øksnevad: P40 child = the item just created
Q141200028	P40	LAST	S2600	"6000000005607155254"
#   Q141199937 Maren Halvorsdatter Øksnevad: P40 child = the item just created
Q141199937	P40	LAST	S2600	"6000000005607155254"
#   the item just created: P735 given name = Q17518394 Kornelius
LAST	P735	Q17518394
#   P734 family name = Q30583490 Øksnevad
LAST	P734	Q30583490

# create a new item
CREATE
#   set the en label to "Lars Osmundsen Nese"
LAST	Len	"Lars Osmundsen Nese"
#   set the mul label to "Lars Osmundsen Nese"
LAST	Lmul	"Lars Osmundsen Nese"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000069466362236 Lars Osmundsen Nese, qualified P1810 subject named as Lars Osmundsen Foss-Eikeland d. y.
LAST	P2600	"6000000069466362236"	P1810	"Lars Osmundsen Foss-Eikeland d. y."
#   P569 date of birth = +1759-00-00T00:00:00Z/9
LAST	P569	+1759-00-00T00:00:00Z/9	S2600	"6000000069466362236"
#   P570 date of death = +1840-09-16T00:00:00Z/11
LAST	P570	+1840-09-16T00:00:00Z/11	S2600	"6000000069466362236"
#   P22 father = Q141217404 Osmund Larsen Raunes
LAST	P22	Q141217404	S2600	"6000000069466362236"
#   Q141217404 Osmund Larsen Raunes: P40 child = the item just created
Q141217404	P40	LAST	S2600	"6000000069466362236"
#   the item just created: P735 given name = Q15635262 Lars
LAST	P735	Q15635262

# create a new item
CREATE
#   set the en label to "Marta Torbjørnsdotter Gjesdal"
LAST	Len	"Marta Torbjørnsdotter Gjesdal"
#   set the mul label to "Marta Torbjørnsdotter Gjesdal"
LAST	Lmul	"Marta Torbjørnsdotter Gjesdal"
#   set the ja label to "マルタ・トルブヨルンスドッテル・イェスダール"
LAST	Lja	"マルタ・トルブヨルンスドッテル・イェスダール"
#   set the zh label to "玛尔塔·托尔布永尔恩斯多特·耶斯达尔"
LAST	Lzh	"玛尔塔·托尔布永尔恩斯多特·耶斯达尔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005607335640 Marta Torbjørnsdotter Gjesdal, qualified P1810 subject named as Marta Torbjørnsdotter Gjesdal
LAST	P2600	"6000000005607335640"	P1810	"Marta Torbjørnsdotter Gjesdal"
#   P569 date of birth = +1745-00-00T00:00:00Z/9
LAST	P569	+1745-00-00T00:00:00Z/9	S2600	"6000000005607335640"
#   P570 date of death = +1801-00-00T00:00:00Z/9
LAST	P570	+1801-00-00T00:00:00Z/9	S2600	"6000000005607335640"
#   P40 child = Q141217391 Kristine Sørensdatter Gjesdal
LAST	P40	Q141217391	S2600	"6000000005607335640"
#   Q141217391 Kristine Sørensdatter Gjesdal: P25 mother = the item just created
Q141217391	P25	LAST	S2600	"6000000005607335640"
#   the item just created: P735 given name = Q846741 Marta
LAST	P735	Q846741
#   P734 family name = Q27888954 Gjesdal
LAST	P734	Q27888954
#   P1449 nickname = en:"Martha Torbiørnsdatter Giestdahl"
LAST	P1449	en:"Martha Torbiørnsdatter Giestdahl"
#   add a mul alias "Martha Torbiørnsdatter Giestdahl Gjesdal"
LAST	Amul	"Martha Torbiørnsdatter Giestdahl Gjesdal"

# create a new item
CREATE
#   set the mul label to "NN"
LAST	Lmul	"NN"
#   set the ca label to "fill de Aagot Garborg Koloboff"
LAST	Lca	"fill de Aagot Garborg Koloboff"
#   set the da label to "søn af Aagot Garborg Koloboff"
LAST	Lda	"søn af Aagot Garborg Koloboff"
#   set the de label to "Sohn von Aagot Garborg Koloboff"
LAST	Lde	"Sohn von Aagot Garborg Koloboff"
#   set the en label to "son of Aagot Garborg Koloboff"
LAST	Len	"son of Aagot Garborg Koloboff"
#   set the es label to "hijo de Aagot Garborg Koloboff"
LAST	Les	"hijo de Aagot Garborg Koloboff"
#   set the it label to "figlio di Aagot Garborg Koloboff"
LAST	Lit	"figlio di Aagot Garborg Koloboff"
#   set the ja label to "オーゴット・ガルボルグ・コロボフの息子"
LAST	Lja	"オーゴット・ガルボルグ・コロボフの息子"
#   set the nb label to "sønn av Aagot Garborg Koloboff"
LAST	Lnb	"sønn av Aagot Garborg Koloboff"
#   set the nl label to "zoon van Aagot Garborg Koloboff"
LAST	Lnl	"zoon van Aagot Garborg Koloboff"
#   set the pt label to "filho de Aagot Garborg Koloboff"
LAST	Lpt	"filho de Aagot Garborg Koloboff"
#   set the sv label to "son till Aagot Garborg Koloboff"
LAST	Lsv	"son till Aagot Garborg Koloboff"
#   set the zh label to "奥高特·加尔博格·科洛博夫之子"
LAST	Lzh	"奥高特·加尔博格·科洛博夫之子"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000117764720856 NN, qualified P1810 subject named as NN
LAST	P2600	"6000000117764720856"	P1810	"NN"
#   P569 date of birth = +1929-00-00T00:00:00Z/9
LAST	P569	+1929-00-00T00:00:00Z/9	S2600	"6000000117764720856"
#   P570 date of death = +1929-00-00T00:00:00Z/9
LAST	P570	+1929-00-00T00:00:00Z/9	S2600	"6000000117764720856"
#   P25 mother = Q141216453 Aagot Garborg Koloboff
LAST	P25	Q141216453	S2600	"6000000117764720856"
#   Q141216453 Aagot Garborg Koloboff: P40 child = the item just created
Q141216453	P40	LAST	S2600	"6000000117764720856"

# create a new item
CREATE
#   the item just created: set the en label to "Olof Jonsson"
LAST	Len	"Olof Jonsson"
#   set the mul label to "Olof Jonsson"
LAST	Lmul	"Olof Jonsson"
#   set the ja label to "オロフ・ヨンソン"
LAST	Lja	"オロフ・ヨンソン"
#   set the zh label to "奥洛夫·永松"
LAST	Lzh	"奥洛夫·永松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000015844614533 Olof Jonsson, qualified P1810 subject named as Olof Jonsson
LAST	P2600	"6000000015844614533"	P1810	"Olof Jonsson"
#   P569 date of birth = +1490-00-00T00:00:00Z/9
LAST	P569	+1490-00-00T00:00:00Z/9	S2600	"6000000015844614533"
#   P570 date of death = +1559-00-00T00:00:00Z/9
LAST	P570	+1559-00-00T00:00:00Z/9	S2600	"6000000015844614533"
#   P40 child = Q141216398 Malin Olofsdotter
LAST	P40	Q141216398	S2600	"6000000015844614533"
#   Q141216398 Malin Olofsdotter: P22 father = the item just created
Q141216398	P22	LAST	S2600	"6000000015844614533"
#   the item just created: P735 given name = Q18089653 Olof
LAST	P735	Q18089653

# create a new item
CREATE
#   set the mul label to "NN"
LAST	Lmul	"NN"
#   set the ca label to "marit de Aagot Garborg Koloboff"
LAST	Lca	"marit de Aagot Garborg Koloboff"
#   set the da label to "ægtemand til Aagot Garborg Koloboff"
LAST	Lda	"ægtemand til Aagot Garborg Koloboff"
#   set the de label to "Ehemann von Aagot Garborg Koloboff"
LAST	Lde	"Ehemann von Aagot Garborg Koloboff"
#   set the en label to "husband of Aagot Garborg Koloboff"
LAST	Len	"husband of Aagot Garborg Koloboff"
#   set the es label to "esposo de Aagot Garborg Koloboff"
LAST	Les	"esposo de Aagot Garborg Koloboff"
#   set the it label to "marito di Aagot Garborg Koloboff"
LAST	Lit	"marito di Aagot Garborg Koloboff"
#   set the ja label to "オーゴット・ガルボルグ・コロボフの夫"
LAST	Lja	"オーゴット・ガルボルグ・コロボフの夫"
#   set the nb label to "ektemann til Aagot Garborg Koloboff"
LAST	Lnb	"ektemann til Aagot Garborg Koloboff"
#   set the nl label to "echtgenoot van Aagot Garborg Koloboff"
LAST	Lnl	"echtgenoot van Aagot Garborg Koloboff"
#   set the pt label to "marido de Aagot Garborg Koloboff"
LAST	Lpt	"marido de Aagot Garborg Koloboff"
#   set the sv label to "make till Aagot Garborg Koloboff"
LAST	Lsv	"make till Aagot Garborg Koloboff"
#   set the zh label to "奥高特·加尔博格·科洛博夫之夫"
LAST	Lzh	"奥高特·加尔博格·科洛博夫之夫"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000116933848184 NN Private, qualified P1810 subject named as Private
LAST	P2600	"6000000116933848184"	P1810	"Private"
#   P26 spouse = Q141216453 Aagot Garborg Koloboff
LAST	P26	Q141216453	S2600	"6000000116933848184"
#   Q141216453 Aagot Garborg Koloboff: P26 spouse = the item just created
Q141216453	P26	LAST	S2600	"6000000116933848184"

# create a new item
CREATE
#   the item just created: set the mul label to "Segrid"
LAST	Lmul	"Segrid"
#   set the ca label to "mare de Malin Olofsdotter"
LAST	Lca	"mare de Malin Olofsdotter"
#   set the da label to "mor til Malin Olofsdotter"
LAST	Lda	"mor til Malin Olofsdotter"
#   set the de label to "Mutter von Malin Olofsdotter"
LAST	Lde	"Mutter von Malin Olofsdotter"
#   set the en label to "mother of Malin Olofsdotter"
LAST	Len	"mother of Malin Olofsdotter"
#   set the es label to "madre de Malin Olofsdotter"
LAST	Les	"madre de Malin Olofsdotter"
#   set the it label to "madre di Malin Olofsdotter"
LAST	Lit	"madre di Malin Olofsdotter"
#   set the ja label to "マリン・オロフスドッテルの母"
LAST	Lja	"マリン・オロフスドッテルの母"
#   set the nb label to "mor til Malin Olofsdotter"
LAST	Lnb	"mor til Malin Olofsdotter"
#   set the nl label to "moeder van Malin Olofsdotter"
LAST	Lnl	"moeder van Malin Olofsdotter"
#   set the pt label to "mãe de Malin Olofsdotter"
LAST	Lpt	"mãe de Malin Olofsdotter"
#   set the sv label to "mor till Malin Olofsdotter"
LAST	Lsv	"mor till Malin Olofsdotter"
#   set the zh label to "马利恩·奥洛夫斯多特之母"
LAST	Lzh	"马利恩·奥洛夫斯多特之母"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 4982922006040030712 Segrid NN, qualified P1810 subject named as Segrid NN
LAST	P2600	"4982922006040030712"	P1810	"Segrid NN"
#   P569 date of birth = +1505-00-00T00:00:00Z/9
LAST	P569	+1505-00-00T00:00:00Z/9	S2600	"4982922006040030712"
#   P570 date of death = +1569-00-00T00:00:00Z/9
LAST	P570	+1569-00-00T00:00:00Z/9	S2600	"4982922006040030712"
#   P40 child = Q141216398 Malin Olofsdotter
LAST	P40	Q141216398	S2600	"4982922006040030712"
#   Q141216398 Malin Olofsdotter: P25 mother = the item just created
Q141216398	P25	LAST	S2600	"4982922006040030712"

# create a new item
CREATE
#   the item just created: set the en label to "Søren Sørenson Gjesdal"
LAST	Len	"Søren Sørenson Gjesdal"
#   set the mul label to "Søren Sørenson Gjesdal"
LAST	Lmul	"Søren Sørenson Gjesdal"
#   add a mul alias "Søren Sørenson Helland"
LAST	Amul	"Søren Sørenson Helland"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003095047808 Søren Sørenson Gjesdal, qualified P1810 subject named as Søren Sørenson Helland
LAST	P2600	"6000000003095047808"	P1810	"Søren Sørenson Helland"
#   P569 date of birth = +1739-00-00T00:00:00Z/9
LAST	P569	+1739-00-00T00:00:00Z/9	S2600	"6000000003095047808"
#   P570 date of death = +1806-00-00T00:00:00Z/9
LAST	P570	+1806-00-00T00:00:00Z/9	S2600	"6000000003095047808"
#   P40 child = Q141217391 Kristine Sørensdatter Gjesdal
LAST	P40	Q141217391	S2600	"6000000003095047808"
#   Q141217391 Kristine Sørensdatter Gjesdal: P22 father = the item just created
Q141217391	P22	LAST	S2600	"6000000003095047808"
#   the item just created: P735 given name = Q7174941 Søren
LAST	P735	Q7174941
#   P734 family name = Q30085478 Helland, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q30085478	P3831	Q2507958
#   P734 family name = Q27888954 Gjesdal
LAST	P734	Q27888954
#   add a mul alias "Søren Gjesdal"
LAST	Amul	"Søren Gjesdal"

# create a new item
CREATE
#   set the en label to "Tore Sebjørnsson Talgje d.y"
LAST	Len	"Tore Sebjørnsson Talgje d.y"
#   set the mul label to "Tore Sebjørnsson Talgje d.y"
LAST	Lmul	"Tore Sebjørnsson Talgje d.y"
#   set the ja label to "トレ・セブヨルンソン・タルイェ・ドイ"
LAST	Lja	"トレ・セブヨルンソン・タルイェ・ドイ"
#   set the zh label to "托雷·塞布永尔恩松·塔尔耶·德伊"
LAST	Lzh	"托雷·塞布永尔恩松·塔尔耶·德伊"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003043756033 Tore Sebjørnsson Talgje d.y, qualified P1810 subject named as Tore Sebjørnsson Talgje d.y
LAST	P2600	"6000000003043756033"	P1810	"Tore Sebjørnsson Talgje d.y"
#   P569 date of birth = +1535-00-00T00:00:00Z/9
LAST	P569	+1535-00-00T00:00:00Z/9	S2600	"6000000003043756033"
#   P570 date of death = +1595-00-00T00:00:00Z/9
LAST	P570	+1595-00-00T00:00:00Z/9	S2600	"6000000003043756033"
#   P22 father = Q141200111 Sæbjørn Toresson Talgje
LAST	P22	Q141200111	S2600	"6000000003043756033"
#   P25 mother = Q141200101 Sissel Jonsdatter Talje
LAST	P25	Q141200101	S2600	"6000000003043756033"
#   Q141200111 Sæbjørn Toresson Talgje: P40 child = the item just created
Q141200111	P40	LAST	S2600	"6000000003043756033"
#   Q141200101 Sissel Jonsdatter Talje: P40 child = the item just created
Q141200101	P40	LAST	S2600	"6000000003043756033"
#   the item just created: P735 given name = Q1548096 Tore
LAST	P735	Q1548096
#   P1449 nickname = en:"Tore Sebjornson"
LAST	P1449	en:"Tore Sebjornson"
#   add a mul alias "Tore Sebjornson Talgje"
LAST	Amul	"Tore Sebjornson Talgje"
#   add a mul alias "Tore Talgje"
LAST	Amul	"Tore Talgje"

# create a new item
CREATE
#   set the en label to "Ulrika Persdotter"
LAST	Len	"Ulrika Persdotter"
#   set the mul label to "Ulrika Persdotter"
LAST	Lmul	"Ulrika Persdotter"
#   set the ja label to "ウルリカ・ペルスドッテル"
LAST	Lja	"ウルリカ・ペルスドッテル"
#   set the zh label to "乌尔里卡·佩尔斯多特"
LAST	Lzh	"乌尔里卡·佩尔斯多特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000177920129831 Ulrika Persdotter, qualified P1810 subject named as Ulrika Persdotter
LAST	P2600	"6000000177920129831"	P1810	"Ulrika Persdotter"
#   P569 date of birth = +1811-07-16T00:00:00Z/11
LAST	P569	+1811-07-16T00:00:00Z/11	S2600	"6000000177920129831"
#   P570 date of death = +1894-02-05T00:00:00Z/11
LAST	P570	+1894-02-05T00:00:00Z/11	S2600	"6000000177920129831"
#   P22 father = Q141217433 Per Persson Hagman
LAST	P22	Q141217433	S2600	"6000000177920129831"
#   Q141217433 Per Persson Hagman: P40 child = the item just created
Q141217433	P40	LAST	S2600	"6000000177920129831"
#   the item just created: P735 given name = Q18924998 Ulrika
LAST	P735	Q18924998
#   Q141216618 Karin Olofsdotter: P3373 sibling = Q141205931 Olof Olofsson
Q141216618	P3373	Q141205931	S2600	"348968026630001429"
#   Q141216403 Olof Nilsson: P22 father = Q141217400 Nils Albrektsson
Q141216403	P22	Q141217400	S2600	"375729629520007230"
#   Q141217400 Nils Albrektsson: P40 child = Q141216403 Olof Nilsson
Q141217400	P40	Q141216403	S2600	"375732740000012611"
#   P26 spouse = Q141216605 Gunilla Jonsdotter
Q141217400	P26	Q141216605	S2600	"375732740000012611"
#   P2600 Geni.com profile ID = 375732740000012611 Nils Albrektsson, qualified P1810 subject named as Nils Albrektsson
Q141217400	P2600	"375732740000012611"	P1810	"Nils Albrektsson"	S2600	"375732740000012611"
#   P735 given name = Q16423038 Nils
Q141217400	P735	Q16423038
#   Q141216611 Jon Villumson Raunes: P26 spouse = Q141216632 Magdalena Lauritsd Hogganvik
Q141216611	P26	Q141216632	S2600	"6000000001169146145"
#   Q141217384 David Tjølson Edland: P40 child = Q141216602 Berta Guria Davidsdatter Stokka
Q141217384	P40	Q141216602	S2600	"6000000002690086678"
#   P26 spouse = Q141217391 Kristine Sørensdatter Gjesdal
Q141217384	P26	Q141217391	S2600	"6000000002690086678"
#   P2600 Geni.com profile ID = 6000000002690086678 David Tjølson Edland, qualified P1810 subject named as David Tjølson Edland
Q141217384	P2600	"6000000002690086678"	P1810	"David Tjølson Edland"	S2600	"6000000002690086678"
#   P735 given name = Q29937870 David
Q141217384	P735	Q29937870
#   Q141216602 Berta Guria Davidsdatter Stokka: P22 father = Q141217384 David Tjølson Edland
Q141216602	P22	Q141217384	S2600	"6000000002726900648"
#   P25 mother = Q141217391 Kristine Sørensdatter Gjesdal
Q141216602	P25	Q141217391	S2600	"6000000002726900648"
#   P26 spouse = Q141216653 Torger Torgerson Stokka
Q141216602	P26	Q141216653	S2600	"6000000002726900648"
#   Q141216653 Torger Torgerson Stokka: P26 spouse = Q141216602 Berta Guria Davidsdatter Stokka
Q141216653	P26	Q141216602	S2600	"6000000002726968193"
#   Q943803 Uno von Troil: P25 mother = Q141217359 Anna Elisabet Angerstein
Q943803	P25	Q141217359	S2600	"6000000002811012188"
#   Q141200101 Sissel Jonsdatter Talje: P40 child = Q141217434 Sissel Sæbjørnsdatter Talgje
Q141200101	P40	Q141217434	S2600	"6000000003043806217"
#   Q141199819 Anna Andersdotter: P40 child = Q141199734 Nils Andersson
Q141199819	P40	Q141199734	S2600	"6000000003125438035"
#   Q141216644 Rasmus Asbjørnson Nedre Rossavik: P40 child = Q141216599 Anna Rasmusdatter Nedre Rossavik
Q141216644	P40	Q141216599	S2600	"6000000003192698959"
#   Q141216638 Olaug Jonsdatter Heigre: P26 spouse = Q141216637 Ola Person Persson Heigre
Q141216638	P26	Q141216637	S2600	"6000000003491933401"
#   Q141216637 Ola Person Persson Heigre: P26 spouse = Q141216638 Olaug Jonsdatter Heigre
Q141216637	P26	Q141216638	S2600	"6000000003491947917"
#   Q141216387 Johannes Svensen Obrestad: P40 child = Q141217390 Johan Johannessen Obrestad
Q141216387	P40	Q141217390	S2600	"6000000003491978246"
#   Q141216635 Martha Eivindsdatter Heigre: P40 child = Q141216643 Ragna Enevaldsdatter Heigre
Q141216635	P40	Q141216643	S2600	"6000000003491988061"
#   Q141216643 Ragna Enevaldsdatter Heigre: P25 mother = Q141216635 Martha Eivindsdatter Heigre
Q141216643	P25	Q141216635	S2600	"6000000003491988081"
#   Q6082455 Thure Gustaf Rudbeck: P26 spouse = Q141217393 Magdalena von Mentzer
Q6082455	P26	Q141217393	S2600	"6000000003580303855"
#   Q141216598 Anna Ivarsd Stokka: P22 father = Q141217387 Ivar Stokka
Q141216598	P22	Q141217387	S2600	"6000000003830468150"
#   Q141200111 Sæbjørn Toresson Talgje: P40 child = Q141217434 Sissel Sæbjørnsdatter Talgje
Q141200111	P40	Q141217434	S2600	"6000000004213963966"
#   Q141217434 Sissel Sæbjørnsdatter Talgje: P22 father = Q141200111 Sæbjørn Toresson Talgje
Q141217434	P22	Q141200111	S2600	"6000000004214055821"
#   P25 mother = Q141200101 Sissel Jonsdatter Talje
Q141217434	P25	Q141200101	S2600	"6000000004214055821"
#   P2600 Geni.com profile ID = 6000000004214055821 Sissel Sæbjørnsdatter Talgje, qualified P1810 subject named as Sissel Sæbjørnsdatter Talgje
Q141217434	P2600	"6000000004214055821"	P1810	"Sissel Sæbjørnsdatter Talgje"	S2600	"6000000004214055821"
#   P735 given name = Q4571101 Sissel
Q141217434	P735	Q4571101
#   Q141200028 Per Jonson Øksnevad: P40 child = Q141217385 Guri Persdatter Øksnevad
Q141200028	P40	Q141217385	S2600	"6000000005606907249"
#   Q141199937 Maren Halvorsdatter Øksnevad: P40 child = Q141217385 Guri Persdatter Øksnevad
Q141199937	P40	Q141217385	S2600	"6000000005607155237"
#   Q141217385 Guri Persdatter Øksnevad: P22 father = Q141200028 Per Jonson Øksnevad
Q141217385	P22	Q141200028	S2600	"6000000005607155246"
#   P25 mother = Q141199937 Maren Halvorsdatter Øksnevad
Q141217385	P25	Q141199937	S2600	"6000000005607155246"
#   P2600 Geni.com profile ID = 6000000005607155246 Guri Persdatter Øksnevad, qualified P1810 subject named as Guri Persdatter Øksnevad
Q141217385	P2600	"6000000005607155246"	P1810	"Guri Persdatter Øksnevad"	S2600	"6000000005607155246"
#   P735 given name = Q11973376 Guri
Q141217385	P735	Q11973376
#   P734 family name = Q30583490 Øksnevad
Q141217385	P734	Q30583490
#   Q141216632 Magdalena Lauritsd Hogganvik: P26 spouse = Q141216611 Jon Villumson Raunes
Q141216632	P26	Q141216611	S2600	"6000000005607268671"
#   Q141217391 Kristine Sørensdatter Gjesdal: P40 child = Q141216602 Berta Guria Davidsdatter Stokka
Q141217391	P40	Q141216602	S2600	"6000000005607335630"
#   P26 spouse = Q141217384 David Tjølson Edland
Q141217391	P26	Q141217384	S2600	"6000000005607335630"
#   P2600 Geni.com profile ID = 6000000005607335630 Kristine Sørensdatter Gjesdal, qualified P1810 subject named as Kristine Sørensdatter Gjesdal
Q141217391	P2600	"6000000005607335630"	P1810	"Kristine Sørensdatter Gjesdal"	S2600	"6000000005607335630"
#   P735 given name = Q16859157 Kristine
Q141217391	P735	Q16859157
#   P734 family name = Q27888954 Gjesdal
Q141217391	P734	Q27888954
#   Q141216613 Karen Henriksdotter Raunes Våga: P40 child = Q141216627 Lars Nilsen Raunes
Q141216613	P40	Q141216627	S2600	"6000000005607377021"
#   Q141216627 Lars Nilsen Raunes: P25 mother = Q141216613 Karen Henriksdotter Raunes Våga
Q141216627	P25	Q141216613	S2600	"6000000005609304829"
#   P40 child = Q141217404 Osmund Larsen Raunes
Q141216627	P40	Q141217404	S2600	"6000000005609304829"
#   P26 spouse = Q141217369 Anna Osmundsd Stokka
Q141216627	P26	Q141217369	S2600	"6000000005609304829"
#   Q141217369 Anna Osmundsd Stokka: P40 child = Q141217404 Osmund Larsen Raunes
Q141217369	P40	Q141217404	S2600	"6000000005609304839"
#   P26 spouse = Q141216627 Lars Nilsen Raunes
Q141217369	P26	Q141216627	S2600	"6000000005609304839"
#   P2600 Geni.com profile ID = 6000000005609304839 Anna Osmundsd Stokka, qualified P1810 subject named as Anna Osmundsd Stokka
Q141217369	P2600	"6000000005609304839"	P1810	"Anna Osmundsd Stokka"	S2600	"6000000005609304839"
#   Q141216645 Reiar Reiersen Kydland: P26 spouse = Q141216609 Inger Kristoffersdatter Skårland
Q141216645	P26	Q141216609	S2600	"6000000005609534659"
#   Q141216609 Inger Kristoffersdatter Skårland: P26 spouse = Q141216645 Reiar Reiersen Kydland
Q141216609	P26	Q141216645	S2600	"6000000005609534669"
#   Q1340357 Jakob Benzelius: P26 spouse = Q141217381 Catharina Edenberg
Q1340357	P26	Q141217381	S2600	"6000000006645210002"
#   Q5562579 Magnus Petri Aurivillius: P26 spouse = Q141217394 Margareta Christina von Numers
Q5562579	P26	Q141217394	S2600	"6000000007025966290"
#   Q141216605 Gunilla Jonsdotter: P26 spouse = Q141217400 Nils Albrektsson
Q141216605	P26	Q141217400	S2600	"6000000007117021938"
#   Q5562598 Samuel Aurivillius: P25 mother = Q141217394 Margareta Christina von Numers
Q5562598	P25	Q141217394	S2600	"6000000007318765242"
#   Q1168365 Samuel Olofsson Troilius: P26 spouse = Q141217359 Anna Elisabet Angerstein
Q1168365	P26	Q141217359	S2600	"6000000007442688545"
#   Q141217387 Ivar Stokka: P40 child = Q141216598 Anna Ivarsd Stokka
Q141217387	P40	Q141216598	S2600	"6000000007980728818"
#   P2600 Geni.com profile ID = 6000000007980728818 Ivar Stokka, qualified P1810 subject named as Ivar Stokka
Q141217387	P2600	"6000000007980728818"	P1810	"Ivar Stokka"	S2600	"6000000007980728818"
#   P735 given name = Q127069 Ivar
Q141217387	P735	Q127069
#   Q1527696 Carl Aurivillius: P25 mother = Q141217394 Margareta Christina von Numers
Q1527696	P25	Q141217394	S2600	"6000000008390619113"
#   Q141217394 Margareta Christina von Numers: P40 child = Q5562598 Samuel Aurivillius
Q141217394	P40	Q5562598	S2600	"6000000008391104730"
#   P40 child = Q1527696 Carl Aurivillius
Q141217394	P40	Q1527696	S2600	"6000000008391104730"
#   P26 spouse = Q5562579 Magnus Petri Aurivillius
Q141217394	P26	Q5562579	S2600	"6000000008391104730"
#   P2600 Geni.com profile ID = 6000000008391104730 Margareta Christina von Numers, qualified P1810 subject named as Margareta Christina von Numers
Q141217394	P2600	"6000000008391104730"	P1810	"Margareta Christina von Numers"	S2600	"6000000008391104730"
#   P735 given name = Q8274988 Margareta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141217394	P735	Q8274988	P1545	"1"	P7452	Q3409033
#   Q141216599 Anna Rasmusdatter Nedre Rossavik: P22 father = Q141216644 Rasmus Asbjørnson Nedre Rossavik
Q141216599	P22	Q141216644	S2600	"6000000008916446714"
#   Q141217433 Per Persson Hagman: P22 father = Q141217431 Per Andersson Storskytt
Q141217433	P22	Q141217431	S2600	"6000000011078726908"
#   P25 mother = Q141216595 Anna Danielsdotter
Q141217433	P25	Q141216595	S2600	"6000000011078726908"
#   P2600 Geni.com profile ID = 6000000011078726908 Per Persson Hagman, qualified P1810 subject named as Per Persson
Q141217433	P2600	"6000000011078726908"	P1810	"Per Persson"	S2600	"6000000011078726908"
#   P735 given name = Q13582800 Per
Q141217433	P735	Q13582800
#   Q141216633 Malin Jacobsdotter: P40 child = Q141216595 Anna Danielsdotter
Q141216633	P40	Q141216595	S2600	"6000000011078760054"
#   Q141217431 Per Andersson Storskytt: P40 child = Q141217433 Per Persson Hagman
Q141217431	P40	Q141217433	S2600	"6000000011078829655"
#   P26 spouse = Q141216595 Anna Danielsdotter
Q141217431	P26	Q141216595	S2600	"6000000011078829655"
#   P2600 Geni.com profile ID = 6000000011078829655 Per Andersson Storskytt, qualified P1810 subject named as Per Andersson
Q141217431	P2600	"6000000011078829655"	P1810	"Per Andersson"	S2600	"6000000011078829655"
#   P735 given name = Q13582800 Per
Q141217431	P735	Q13582800
#   Q141216595 Anna Danielsdotter: P25 mother = Q141216633 Malin Jacobsdotter
Q141216595	P25	Q141216633	S2600	"6000000011078918407"
#   P40 child = Q141217433 Per Persson Hagman
Q141216595	P40	Q141217433	S2600	"6000000011078918407"
#   P26 spouse = Q141217431 Per Andersson Storskytt
Q141216595	P26	Q141217431	S2600	"6000000011078918407"
#   P5056 patronym or matronym = Q140226461, qualified P144 based on Q141216461 Daniel Andersson
Q141216595	P5056	Q140226461	P144	Q141216461
#   Q719983 Johan Ihre: P26 spouse = Q141217383 Charlotta Johanna Gerner
Q719983	P26	Q141217383	S2600	"6000000011116437821"
#   Q141198393 Erik Erikson Stangeland: P40 child = Q141217392 Larine Eriksdatter Heigre
Q141198393	P40	Q141217392	S2600	"6000000011198194484"
#   P26 spouse = Q141217372 Berta Larsdatter Stangeland
Q141198393	P26	Q141217372	S2600	"6000000011198194484"
#   Q141217404 Osmund Larsen Raunes: P22 father = Q141216627 Lars Nilsen Raunes
Q141217404	P22	Q141216627	S2600	"6000000012587690898"
#   P25 mother = Q141217369 Anna Osmundsd Stokka
Q141217404	P25	Q141217369	S2600	"6000000012587690898"
#   P2600 Geni.com profile ID = 6000000012587690898 Osmund Larsen Raunes, qualified P1810 subject named as Osmund Larsen Raunes
Q141217404	P2600	"6000000012587690898"	P1810	"Osmund Larsen Raunes"	S2600	"6000000012587690898"
#   P735 given name = Q7107242 Osmund
Q141217404	P735	Q7107242
#   Q141217393 Magdalena von Mentzer: P26 spouse = Q6082455 Thure Gustaf Rudbeck
Q141217393	P26	Q6082455	S2600	"6000000012617083513"
#   P2600 Geni.com profile ID = 6000000012617083513 Magdalena von Mentzer, qualified P1810 subject named as Magdalena von Mentzer
Q141217393	P2600	"6000000012617083513"	P1810	"Magdalena von Mentzer"	S2600	"6000000012617083513"
#   P735 given name = Q842544 Magdalena, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141217393	P735	Q842544	P1545	"1"	P7452	Q3409033
#   Q141217381 Catharina Edenberg: P26 spouse = Q1340357 Jakob Benzelius
Q141217381	P26	Q1340357	S2600	"6000000012640936007"
#   P2600 Geni.com profile ID = 6000000012640936007 Catharina Edenberg, qualified P1810 subject named as Catharina Edenberg nr 617
Q141217381	P2600	"6000000012640936007"	P1810	"Catharina Edenberg nr 617"	S2600	"6000000012640936007"
#   P735 given name = Q17317997 Catharina
Q141217381	P735	Q17317997
#   Q141217383 Charlotta Johanna Gerner: P40 child = Q5822415 Albrecht Ihre
Q141217383	P40	Q5822415	S2600	"6000000013081666315"
#   P26 spouse = Q719983 Johan Ihre
Q141217383	P26	Q719983	S2600	"6000000013081666315"
#   P2600 Geni.com profile ID = 6000000013081666315 Charlotta Johanna Gerner, qualified P1810 subject named as Charlotta Johanna Gerner
Q141217383	P2600	"6000000013081666315"	P1810	"Charlotta Johanna Gerner"	S2600	"6000000013081666315"
#   P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141217383	P735	Q1067071	P1545	"1"	P7452	Q3409033
#   P735 given name = Q4120836 Johanna, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141217383	P735	Q4120836	P1545	"2"	P3831	Q245025
#   Q141217359 Anna Elisabet Angerstein: P40 child = Q943803 Uno von Troil
Q141217359	P40	Q943803	S2600	"6000000013252126990"
#   P26 spouse = Q1168365 Samuel Olofsson Troilius
Q141217359	P26	Q1168365	S2600	"6000000013252126990"
#   P2600 Geni.com profile ID = 6000000013252126990 Anna Elisabet Angerstein, qualified P1810 subject named as Anna Elisabet Angerstein
Q141217359	P2600	"6000000013252126990"	P1810	"Anna Elisabet Angerstein"	S2600	"6000000013252126990"
#   P735 given name = Q16423275 Elisabet, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141217359	P735	Q16423275	P1545	"2"	P3831	Q245025
#   Q141217415 Ottiliana Vilhelmina Conradsdotter Transchiöld: P40 child = Q5951795 Johan Wilhelm Johansson Liljencrantz
Q141217415	P40	Q5951795	S2600	"6000000013400386736"
#   P26 spouse = Q5951779 Johan Liljencrantz
Q141217415	P26	Q5951779	S2600	"6000000013400386736"
#   P2600 Geni.com profile ID = 6000000013400386736 Ottiliana Vilhelmina Conradsdotter Transchiöld, qualified P1810 subject named as Ottiliana Vilhelmina Conradsdotter Transchiöld
Q141217415	P2600	"6000000013400386736"	P1810	"Ottiliana Vilhelmina Conradsdotter Transchiöld"	S2600	"6000000013400386736"
#   P735 given name = Q15711317 Vilhelmina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141217415	P735	Q15711317	P1545	"2"	P3831	Q245025
#   Q5951795 Johan Wilhelm Johansson Liljencrantz: P25 mother = Q141217415 Ottiliana Vilhelmina Conradsdotter Transchiöld
Q5951795	P25	Q141217415	S2600	"6000000013400741602"
#   Q5951779 Johan Liljencrantz: P26 spouse = Q141217415 Ottiliana Vilhelmina Conradsdotter Transchiöld
Q5951779	P26	Q141217415	S2600	"6000000013400899375"
#   Q141216639 Olufine Bergithe Ekman: P26 spouse = Q141216640 Per Gustaf Ekman
Q141216639	P26	Q141216640	S2600	"6000000014196479728"
#   Q141217372 Berta Larsdatter Stangeland: P40 child = Q141217392 Larine Eriksdatter Heigre
Q141217372	P40	Q141217392	S2600	"6000000023500402302"
#   P26 spouse = Q141198393 Erik Erikson Stangeland
Q141217372	P26	Q141198393	S2600	"6000000023500402302"
#   P2600 Geni.com profile ID = 6000000023500402302 Berta Larsdatter Stangeland, qualified P1810 subject named as Berta Larsdatter Øksnevad
Q141217372	P2600	"6000000023500402302"	P1810	"Berta Larsdatter Øksnevad"	S2600	"6000000023500402302"
#   P735 given name = Q4092653 Berta
Q141217372	P735	Q4092653
#   P734 family name = Q21452049 Stangeland
Q141217372	P734	Q21452049
#   Q5822415 Albrecht Ihre: P25 mother = Q141217383 Charlotta Johanna Gerner
Q5822415	P25	Q141217383	S2600	"6000000024166897841"
#   Q141205917 Kerstin Månsdotter: P22 father = Q141217398 Måns Moge
Q141205917	P22	Q141217398	S2600	"6000000027469679490"
#   P25 mother = Q141217396 Maria No name
Q141205917	P25	Q141217396	S2600	"6000000027469679490"
#   Q141217398 Måns Moge: P40 child = Q141205917 Kerstin Månsdotter
Q141217398	P40	Q141205917	S2600	"6000000027469942604"
#   P26 spouse = Q141217396 Maria No name
Q141217398	P26	Q141217396	S2600	"6000000027469942604"
#   P2600 Geni.com profile ID = 6000000027469942604 Måns Moge, qualified P1810 subject named as Måns Moge
Q141217398	P2600	"6000000027469942604"	P1810	"Måns Moge"	S2600	"6000000027469942604"
#   P735 given name = Q19799975 Måns
Q141217398	P735	Q19799975
#   Q141217396 Maria No name: P40 child = Q141205917 Kerstin Månsdotter
Q141217396	P40	Q141205917	S2600	"6000000027470028034"
#   P26 spouse = Q141217398 Måns Moge
Q141217396	P26	Q141217398	S2600	"6000000027470028034"
#   P2600 Geni.com profile ID = 6000000027470028034 Maria No name, qualified P1810 subject named as Maria No name
Q141217396	P2600	"6000000027470028034"	P1810	"Maria No name"	S2600	"6000000027470028034"
#   Q141216640 Per Gustaf Ekman: P26 spouse = Q141216639 Olufine Bergithe Ekman
Q141216640	P26	Q141216639	S2600	"6000000032811550619"
#   Q141200083 Sara NN: P26 spouse = Q141199734 Nils Andersson
Q141200083	P26	Q141199734	S2600	"6000000059888596942"
#   Q141216363 Anne Govertsdtr. Bratland: P40 child = Q141217390 Johan Johannessen Obrestad
Q141216363	P40	Q141217390	S2600	"6000000169074443823"
#   Q141217392 Larine Eriksdatter Heigre: P22 father = Q141198393 Erik Erikson Stangeland
Q141217392	P22	Q141198393	S2600	"6000000201256773828"
#   P25 mother = Q141217372 Berta Larsdatter Stangeland
Q141217392	P25	Q141217372	S2600	"6000000201256773828"
#   P2600 Geni.com profile ID = 6000000201256773828 Larine Eriksdatter Heigre, qualified P1810 subject named as Larine Eriksdatter Stangeland
Q141217392	P2600	"6000000201256773828"	P1810	"Larine Eriksdatter Stangeland"	S2600	"6000000201256773828"
#   Q141217390 Johan Johannessen Obrestad: P22 father = Q141216387 Johannes Svensen Obrestad
Q141217390	P22	Q141216387	S2600	"6000000206974233871"
#   P25 mother = Q141216363 Anne Govertsdtr. Bratland
Q141217390	P25	Q141216363	S2600	"6000000206974233871"
#   P2600 Geni.com profile ID = 6000000206974233871 Johan Johannessen Obrestad, qualified P1810 subject named as Johan Johannessen Obrestad
Q141217390	P2600	"6000000206974233871"	P1810	"Johan Johannessen Obrestad"	S2600	"6000000206974233871"
#   P735 given name = Q10989273 Johan
Q141217390	P735	Q10989273

