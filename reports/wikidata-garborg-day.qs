# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   2248 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
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

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Anders Persson Hägg"
LAST	Len	"Anders Persson Hägg"
#   set the mul label to "Anders Persson Hägg"
LAST	Lmul	"Anders Persson Hägg"
#   add a mul alias "Anders Persson"
LAST	Amul	"Anders Persson"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000039229563859 Anders Persson Hägg, qualified P1810 subject named as Anders Persson
LAST	P2600	"6000000039229563859"	P1810	"Anders Persson"
#   P569 date of birth = +1759-02-22T00:00:00Z/11
LAST	P569	+1759-02-22T00:00:00Z/11	S2600	"6000000039229563859"
#   P570 date of death = +1834-01-01T00:00:00Z/11
LAST	P570	+1834-01-01T00:00:00Z/11	S2600	"6000000039229563859"
#   P25 mother = Q141216595 Anna Danielsdotter
LAST	P25	Q141216595	S2600	"6000000039229563859"
#   Q141216595 Anna Danielsdotter: P40 child = the item just created
Q141216595	P40	LAST	S2600	"6000000039229563859"
#   the item just created: P735 given name = Q8843357 Anders
LAST	P735	Q8843357
#   P734 family name = Q27876648 Persson
LAST	P734	Q27876648

# create a new item
CREATE
#   set the en label to "Anna Ormsd Byre"
LAST	Len	"Anna Ormsd Byre"
#   set the mul label to "Anna Ormsd Byre"
LAST	Lmul	"Anna Ormsd Byre"
#   set the ja label to "アンナ・オルムスド・ビレ"
LAST	Lja	"アンナ・オルムスド・ビレ"
#   set the zh label to "安娜·奥尔姆斯德·比雷"
LAST	Lzh	"安娜·奥尔姆斯德·比雷"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000002376475916 Anna Ormsd Byre, qualified P1810 subject named as Anna Ormsd Byre
LAST	P2600	"6000000002376475916"	P1810	"Anna Ormsd Byre"
#   P569 date of birth = +1538-00-00T00:00:00Z/9
LAST	P569	+1538-00-00T00:00:00Z/9	S2600	"6000000002376475916"
#   P570 date of death = +1599-00-00T00:00:00Z/9
LAST	P570	+1599-00-00T00:00:00Z/9	S2600	"6000000002376475916"
#   P22 father = Q141216499 Orm Ånonsen
LAST	P22	Q141216499	S2600	"6000000002376475916"
#   P25 mother = Q141216598 Anna Ivarsd Stokka
LAST	P25	Q141216598	S2600	"6000000002376475916"
#   P40 child = Q141206080 Peder Tormodson Foss
LAST	P40	Q141206080	S2600	"6000000002376475916"
#   Q141216499 Orm Ånonsen: P40 child = the item just created
Q141216499	P40	LAST	S2600	"6000000002376475916"
#   Q141216598 Anna Ivarsd Stokka: P40 child = the item just created
Q141216598	P40	LAST	S2600	"6000000002376475916"
#   Q141206080 Peder Tormodson Foss: P25 mother = the item just created
Q141206080	P25	LAST	S2600	"6000000002376475916"
#   the item just created: P1449 nickname = en:"Anna Ormsd Stokka"
LAST	P1449	en:"Anna Ormsd Stokka"
#   add a mul alias "Anna Ormsd Stokka Byre"
LAST	Amul	"Anna Ormsd Stokka Byre"

# create a new item
CREATE
#   set the en label to "Anna Osmundsd Stokka"
LAST	Len	"Anna Osmundsd Stokka"
#   set the mul label to "Anna Osmundsd Stokka"
LAST	Lmul	"Anna Osmundsd Stokka"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005609304839 Anna Osmundsd Stokka, qualified P1810 subject named as Anna Osmundsd Stokka
LAST	P2600	"6000000005609304839"	P1810	"Anna Osmundsd Stokka"
#   P569 date of birth = +1700-00-00T00:00:00Z/9
LAST	P569	+1700-00-00T00:00:00Z/9	S2600	"6000000005609304839"
#   P570 date of death = +1766-06-02T00:00:00Z/11
LAST	P570	+1766-06-02T00:00:00Z/11	S2600	"6000000005609304839"
#   P26 spouse = Q141216627 Lars Nilsen Raunes
LAST	P26	Q141216627	S2600	"6000000005609304839"
#   Q141216627 Lars Nilsen Raunes: P26 spouse = the item just created
Q141216627	P26	LAST	S2600	"6000000005609304839"

# create a new item
CREATE
#   the item just created: set the en label to "Anna Torgersdatter Høle"
LAST	Len	"Anna Torgersdatter Høle"
#   set the mul label to "Anna Torgersdatter Høle"
LAST	Lmul	"Anna Torgersdatter Høle"
#   add a mul alias "Anna Torgersdatter I"
LAST	Amul	"Anna Torgersdatter I"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 5379950964420081030 Anna Torgersdtr. Høle, qualified P1810 subject named as Anna Torgersdtr. I
LAST	P2600	"5379950964420081030"	P1810	"Anna Torgersdtr. I"
#   P40 child = Q141200067 Rasmus Kjetilson Høle
LAST	P40	Q141200067	S2600	"5379950964420081030"
#   Q141200067 Rasmus Kjetilson Høle: P25 mother = the item just created
Q141200067	P25	LAST	S2600	"5379950964420081030"
#   the item just created: add a mul alias "Anna Torgersdtr. Høle"
LAST	Amul	"Anna Torgersdtr. Høle"

# create a new item
CREATE
#   set the en label to "Asbjørn Rasmusson Frafjord"
LAST	Len	"Asbjørn Rasmusson Frafjord"
#   set the mul label to "Asbjørn Rasmusson Frafjord"
LAST	Lmul	"Asbjørn Rasmusson Frafjord"
#   set the ja label to "アスブヨルン・ラスムソン・フラフヨルド"
LAST	Lja	"アスブヨルン・ラスムソン・フラフヨルド"
#   set the zh label to "阿斯布永尔恩·拉斯穆松·夫拉夫永尔德"
LAST	Lzh	"阿斯布永尔恩·拉斯穆松·夫拉夫永尔德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003095034712 Asbjørn Rasmusson Frafjord, qualified P1810 subject named as Asbjørn Rasmusson Frafjord
LAST	P2600	"6000000003095034712"	P1810	"Asbjørn Rasmusson Frafjord"
#   P569 date of birth = +1642-00-00T00:00:00Z/9
LAST	P569	+1642-00-00T00:00:00Z/9	S2600	"6000000003095034712"
#   P570 date of death = +1695-00-00T00:00:00Z/9
LAST	P570	+1695-00-00T00:00:00Z/9	S2600	"6000000003095034712"
#   P40 child = Q141216644 Rasmus Asbjørnson Nedre Rossavik
LAST	P40	Q141216644	S2600	"6000000003095034712"
#   Q141216644 Rasmus Asbjørnson Nedre Rossavik: P22 father = the item just created
Q141216644	P22	LAST	S2600	"6000000003095034712"
#   the item just created: P735 given name = Q721398 Asbjørn
LAST	P735	Q721398
#   P734 family name = Q38902733 Frafjord
LAST	P734	Q38902733

# create a new item
CREATE
#   set the en label to "Ånon i Byre"
LAST	Len	"Ånon i Byre"
#   set the mul label to "Ånon i Byre"
LAST	Lmul	"Ånon i Byre"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000007980728811 Ånon i Byre, qualified P1810 subject named as Ånon i Byre
LAST	P2600	"6000000007980728811"	P1810	"Ånon i Byre"
#   P569 date of birth = +1483-00-00T00:00:00Z/9
LAST	P569	+1483-00-00T00:00:00Z/9	S2600	"6000000007980728811"
#   P40 child = Q141216499 Orm Ånonsen
LAST	P40	Q141216499	S2600	"6000000007980728811"
#   Q141216499 Orm Ånonsen: P22 father = the item just created
Q141216499	P22	LAST	S2600	"6000000007980728811"
#   the item just created: P1449 nickname = en:"Amund"
LAST	P1449	en:"Amund"
#   add a mul alias "Amund Byre"
LAST	Amul	"Amund Byre"

# create a new item
CREATE
#   set the en label to "Berta Larsdatter Kvam"
LAST	Len	"Berta Larsdatter Kvam"
#   set the mul label to "Berta Larsdatter Kvam"
LAST	Lmul	"Berta Larsdatter Kvam"
#   add a mul alias "Berta Larsdatter Nedre Rossavik"
LAST	Amul	"Berta Larsdatter Nedre Rossavik"
#   set the ja label to "ベルタ・ラーシュダッテル・クヴァム"
LAST	Lja	"ベルタ・ラーシュダッテル・クヴァム"
#   set the zh label to "贝尔塔·拉尔斯达特·克瓦姆"
LAST	Lzh	"贝尔塔·拉尔斯达特·克瓦姆"
#   add a ja alias "ベルタ・ラーシュダッテル・ネドレ・ロサヴィク"
LAST	Aja	"ベルタ・ラーシュダッテル・ネドレ・ロサヴィク"
#   add a zh alias "贝尔塔·拉尔斯达特·内德雷·罗萨维克"
LAST	Azh	"贝尔塔·拉尔斯达特·内德雷·罗萨维克"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005607599048 Berta Larsdatter Kvam, qualified P1810 subject named as Berta Larsdatter Nedre Rossavik
LAST	P2600	"6000000005607599048"	P1810	"Berta Larsdatter Nedre Rossavik"
#   P569 date of birth = +1636-00-00T00:00:00Z/9
LAST	P569	+1636-00-00T00:00:00Z/9	S2600	"6000000005607599048"
#   P570 date of death = +1708-00-00T00:00:00Z/9
LAST	P570	+1708-00-00T00:00:00Z/9	S2600	"6000000005607599048"
#   P22 father = Q141198751 Lars Person Nedre Rossavik
LAST	P22	Q141198751	S2600	"6000000005607599048"
#   P25 mother = Q141198755 Anna Ingebretsdatter Voster
LAST	P25	Q141198755	S2600	"6000000005607599048"
#   Q141198751 Lars Person Nedre Rossavik: P40 child = the item just created
Q141198751	P40	LAST	S2600	"6000000005607599048"
#   Q141198755 Anna Ingebretsdatter Voster: P40 child = the item just created
Q141198755	P40	LAST	S2600	"6000000005607599048"
#   the item just created: P735 given name = Q4092653 Berta
LAST	P735	Q4092653
#   P734 family name = Q30086760 Kvam, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q30086760	P3831	Q28418670
#   P1449 nickname = en:"Berete"
LAST	P1449	en:"Berete"
#   add a mul alias "Berete Kvam"
LAST	Amul	"Berete Kvam"
#   add a mul alias "Berta Kvam"
LAST	Amul	"Berta Kvam"

# create a new item
CREATE
#   set the en label to "David Tjølson Edland"
LAST	Len	"David Tjølson Edland"
#   set the mul label to "David Tjølson Edland"
LAST	Lmul	"David Tjølson Edland"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000002690086678 David Tjølson Edland, qualified P1810 subject named as David Tjølson Edland
LAST	P2600	"6000000002690086678"	P1810	"David Tjølson Edland"
#   P569 date of birth = +1772-00-00T00:00:00Z/9
LAST	P569	+1772-00-00T00:00:00Z/9	S2600	"6000000002690086678"
#   P570 date of death = +1854-00-00T00:00:00Z/9
LAST	P570	+1854-00-00T00:00:00Z/9	S2600	"6000000002690086678"
#   P40 child = Q141216602 Berta Guria Davidsdatter Stokka
LAST	P40	Q141216602	S2600	"6000000002690086678"
#   Q141216602 Berta Guria Davidsdatter Stokka: P22 father = the item just created
Q141216602	P22	LAST	S2600	"6000000002690086678"
#   the item just created: P735 given name = Q29937870 David
LAST	P735	Q29937870
#   add a mul alias "David Edland"
LAST	Amul	"David Edland"

# create a new item
CREATE
#   set the en label to "Eivind Knutson Garborg"
LAST	Len	"Eivind Knutson Garborg"
#   set the mul label to "Eivind Knutson Garborg"
LAST	Lmul	"Eivind Knutson Garborg"
#   set the ja label to "エイヴィン・クヌートソン・ガルボルグ"
LAST	Lja	"エイヴィン・クヌートソン・ガルボルグ"
#   set the zh label to "埃温·克努特松·加尔博格"
LAST	Lzh	"埃温·克努特松·加尔博格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003491971237 Eivind Knutson Garborg, qualified P1810 subject named as Eivind Knutson Garborg
LAST	P2600	"6000000003491971237"	P1810	"Eivind Knutson Garborg"
#   P569 date of birth = +1728-00-00T00:00:00Z/9
LAST	P569	+1728-00-00T00:00:00Z/9	S2600	"6000000003491971237"
#   P570 date of death = +1810-00-00T00:00:00Z/9
LAST	P570	+1810-00-00T00:00:00Z/9	S2600	"6000000003491971237"
#   P22 father = Q141199925 Knut Elvindson Garborg
LAST	P22	Q141199925	S2600	"6000000003491971237"
#   P25 mother = Q141199856 Guri Hansdatter Garborg
LAST	P25	Q141199856	S2600	"6000000003491971237"
#   Q141199925 Knut Elvindson Garborg: P40 child = the item just created
Q141199925	P40	LAST	S2600	"6000000003491971237"
#   Q141199856 Guri Hansdatter Garborg: P40 child = the item just created
Q141199856	P40	LAST	S2600	"6000000003491971237"
#   the item just created: P735 given name = Q3358418 Eivind
LAST	P735	Q3358418
#   P734 family name = Q30250555 Garborg
LAST	P734	Q30250555

# create a new item
CREATE
#   set the en label to "Eivind Ogmundsson Byre på Høyland"
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
#   set the en label to "Helga Pedersdtter Pedersdatter"
LAST	Len	"Helga Pedersdtter Pedersdatter"
#   set the mul label to "Helga Pedersdtter Pedersdatter"
LAST	Lmul	"Helga Pedersdtter Pedersdatter"
#   set the ja label to "ヘルガ・ペデルスドテル・ペーデシュダッテル"
LAST	Lja	"ヘルガ・ペデルスドテル・ペーデシュダッテル"
#   set the zh label to "赫尔加·佩德尔斯德特尔·佩德斯达特"
LAST	Lzh	"赫尔加·佩德尔斯德特尔·佩德斯达特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003491988871 Helga Pedersdtter Pedersdtr, qualified P1810 subject named as Helga Pedersdtter Pedersdtr
LAST	P2600	"6000000003491988871"	P1810	"Helga Pedersdtter Pedersdtr"
#   P40 child = Q141206082 Jon Olson Raustad
LAST	P40	Q141206082	S2600	"6000000003491988871"
#   Q141206082 Jon Olson Raustad: P25 mother = the item just created
Q141206082	P25	LAST	S2600	"6000000003491988871"
#   the item just created: P735 given name = Q1035107 Helga, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q1035107	P1545	"1"	P7452	Q3409033

# create a new item
CREATE
#   set the en label to "Kari Tollaksdatter Kartevoll"
LAST	Len	"Kari Tollaksdatter Kartevoll"
#   set the mul label to "Kari Tollaksdatter Kartevoll"
LAST	Lmul	"Kari Tollaksdatter Kartevoll"
#   set the ja label to "カリ・トラクスダッテル・カルテヴォル"
LAST	Lja	"カリ・トラクスダッテル・カルテヴォル"
#   set the zh label to "卡里·托拉克斯达特·卡尔特沃尔"
LAST	Lzh	"卡里·托拉克斯达特·卡尔特沃尔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005606851268 Kari Tollaksdatter Kartevoll, qualified P1810 subject named as Kari Tollaksdatter Kartevoll
LAST	P2600	"6000000005606851268"	P1810	"Kari Tollaksdatter Kartevoll"
#   P569 date of birth = +1687-00-00T00:00:00Z/9
LAST	P569	+1687-00-00T00:00:00Z/9	S2600	"6000000005606851268"
#   P570 date of death = +1765-10-18T00:00:00Z/11
LAST	P570	+1765-10-18T00:00:00Z/11	S2600	"6000000005606851268"
#   P40 child = Q141216645 Reiar Reiersen Kydland
LAST	P40	Q141216645	S2600	"6000000005606851268"
#   Q141216645 Reiar Reiersen Kydland: P25 mother = the item just created
Q141216645	P25	LAST	S2600	"6000000005606851268"
#   the item just created: P735 given name = Q1333594 Kari
LAST	P735	Q1333594

# create a new item
CREATE
#   set the en label to "Kristine Sørensdatter Gjesdal"
LAST	Len	"Kristine Sørensdatter Gjesdal"
#   set the mul label to "Kristine Sørensdatter Gjesdal"
LAST	Lmul	"Kristine Sørensdatter Gjesdal"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005607335630 Kristine Sørensdatter Gjesdal, qualified P1810 subject named as Kristine Sørensdatter Gjesdal
LAST	P2600	"6000000005607335630"	P1810	"Kristine Sørensdatter Gjesdal"
#   P569 date of birth = +1782-00-00T00:00:00Z/9
LAST	P569	+1782-00-00T00:00:00Z/9	S2600	"6000000005607335630"
#   P570 date of death = +1867-00-00T00:00:00Z/9
LAST	P570	+1867-00-00T00:00:00Z/9	S2600	"6000000005607335630"
#   P40 child = Q141216602 Berta Guria Davidsdatter Stokka
LAST	P40	Q141216602	S2600	"6000000005607335630"
#   Q141216602 Berta Guria Davidsdatter Stokka: P25 mother = the item just created
Q141216602	P25	LAST	S2600	"6000000005607335630"
#   the item just created: P735 given name = Q16859157 Kristine
LAST	P735	Q16859157
#   P734 family name = Q27888954 Gjesdal
LAST	P734	Q27888954

# create a new item
CREATE
#   set the en label to "Lars Olofsson"
LAST	Len	"Lars Olofsson"
#   set the mul label to "Lars Olofsson"
LAST	Lmul	"Lars Olofsson"
#   set the ja label to "ラーシュ・オロフソン"
LAST	Lja	"ラーシュ・オロフソン"
#   set the zh label to "拉尔斯·奥洛夫松"
LAST	Lzh	"拉尔斯·奥洛夫松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000001520371624 Lars Olofsson, qualified P1810 subject named as Lars Olofsson
LAST	P2600	"6000000001520371624"	P1810	"Lars Olofsson"
#   P569 date of birth = +1565-00-00T00:00:00Z/9
LAST	P569	+1565-00-00T00:00:00Z/9	S2600	"6000000001520371624"
#   P570 date of death = +1656-00-00T00:00:00Z/9
LAST	P570	+1656-00-00T00:00:00Z/9	S2600	"6000000001520371624"
#   P22 father = Q141216403 Olof Nilsson
LAST	P22	Q141216403	S2600	"6000000001520371624"
#   P25 mother = Q141216398 Malin Olofsdotter
LAST	P25	Q141216398	S2600	"6000000001520371624"
#   Q141216403 Olof Nilsson: P40 child = the item just created
Q141216403	P40	LAST	S2600	"6000000001520371624"
#   Q141216398 Malin Olofsdotter: P40 child = the item just created
Q141216398	P40	LAST	S2600	"6000000001520371624"
#   the item just created: P735 given name = Q15635262 Lars
LAST	P735	Q15635262

# create a new item
CREATE
#   set the en label to "Marta Fanuelsdotter Madland"
LAST	Len	"Marta Fanuelsdotter Madland"
#   set the mul label to "Marta Fanuelsdotter Madland"
LAST	Lmul	"Marta Fanuelsdotter Madland"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000002055318933 Marta Fanuelsdotter Madland, qualified P1810 subject named as Marta Fanuelsdotter Madland
LAST	P2600	"6000000002055318933"	P1810	"Marta Fanuelsdotter Madland"
#   P569 date of birth = +1766-00-00T00:00:00Z/9
LAST	P569	+1766-00-00T00:00:00Z/9	S2600	"6000000002055318933"
#   P570 date of death = +1835-00-00T00:00:00Z/9
LAST	P570	+1835-00-00T00:00:00Z/9	S2600	"6000000002055318933"
#   P40 child = Q141216653 Torger Torgerson Stokka
LAST	P40	Q141216653	S2600	"6000000002055318933"
#   Q141216653 Torger Torgerson Stokka: P25 mother = the item just created
Q141216653	P25	LAST	S2600	"6000000002055318933"
#   the item just created: P735 given name = Q846741 Marta
LAST	P735	Q846741

# create a new item
CREATE
#   set the en label to "Morten"
LAST	Len	"Morten"
#   set the mul label to "Morten"
LAST	Lmul	"Morten"
#   set the ja label to "モルテン"
LAST	Lja	"モルテン"
#   set the zh label to "莫尔特恩"
LAST	Lzh	"莫尔特恩"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000201845176860 Morten, qualified P1810 subject named as Morten
LAST	P2600	"6000000201845176860"	P1810	"Morten"
#   P40 child = Q141206060 Cecilie Mortensdatter
LAST	P40	Q141206060	S2600	"6000000201845176860"
#   Q141206060 Cecilie Mortensdatter: P22 father = the item just created
Q141206060	P22	LAST	S2600	"6000000201845176860"
#   the item just created: P735 given name = Q1586063 Morten
LAST	P735	Q1586063

# create a new item
CREATE
#   set the mul label to "NN"
LAST	Lmul	"NN"
#   set the ca label to "mare de Orm Ånonsen"
LAST	Lca	"mare de Orm Ånonsen"
#   set the da label to "mor til Orm Ånonsen"
LAST	Lda	"mor til Orm Ånonsen"
#   set the de label to "Mutter von Orm Ånonsen"
LAST	Lde	"Mutter von Orm Ånonsen"
#   set the en label to "mother of Orm Ånonsen"
LAST	Len	"mother of Orm Ånonsen"
#   set the es label to "madre de Orm Ånonsen"
LAST	Les	"madre de Orm Ånonsen"
#   set the it label to "madre di Orm Ånonsen"
LAST	Lit	"madre di Orm Ånonsen"
#   set the ja label to "オルム・オーノンセンの母"
LAST	Lja	"オルム・オーノンセンの母"
#   set the nb label to "mor til Orm Ånonsen"
LAST	Lnb	"mor til Orm Ånonsen"
#   set the nl label to "moeder van Orm Ånonsen"
LAST	Lnl	"moeder van Orm Ånonsen"
#   set the pt label to "mãe de Orm Ånonsen"
LAST	Lpt	"mãe de Orm Ånonsen"
#   set the sv label to "mor till Orm Ånonsen"
LAST	Lsv	"mor till Orm Ånonsen"
#   set the zh label to "奥尔姆·奥诺恩森之母"
LAST	Lzh	"奥尔姆·奥诺恩森之母"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000001770277407 NN, qualified P1810 subject named as NN
LAST	P2600	"6000000001770277407"	P1810	"NN"
#   P569 date of birth = +1487-00-00T00:00:00Z/9
LAST	P569	+1487-00-00T00:00:00Z/9	S2600	"6000000001770277407"
#   P40 child = Q141216499 Orm Ånonsen
LAST	P40	Q141216499	S2600	"6000000001770277407"
#   Q141216499 Orm Ånonsen: P25 mother = the item just created
Q141216499	P25	LAST	S2600	"6000000001770277407"

# create a new item
CREATE
#   the item just created: set the en label to "Nils Albrektsson"
LAST	Len	"Nils Albrektsson"
#   set the mul label to "Nils Albrektsson"
LAST	Lmul	"Nils Albrektsson"
#   set the ja label to "ニルス・アルブレクトソン"
LAST	Lja	"ニルス・アルブレクトソン"
#   set the zh label to "尼尔斯·阿尔布雷克特松"
LAST	Lzh	"尼尔斯·阿尔布雷克特松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 375732740000012611 Nils Albrektsson, qualified P1810 subject named as Nils Albrektsson
LAST	P2600	"375732740000012611"	P1810	"Nils Albrektsson"
#   P569 date of birth = +1505-00-00T00:00:00Z/9
LAST	P569	+1505-00-00T00:00:00Z/9	S2600	"375732740000012611"
#   P570 date of death = +1573-00-00T00:00:00Z/9
LAST	P570	+1573-00-00T00:00:00Z/9	S2600	"375732740000012611"
#   P26 spouse = Q141216605 Gunilla Jonsdotter
LAST	P26	Q141216605	S2600	"375732740000012611"
#   P40 child = Q141216403 Olof Nilsson
LAST	P40	Q141216403	S2600	"375732740000012611"
#   Q141216605 Gunilla Jonsdotter: P26 spouse = the item just created
Q141216605	P26	LAST	S2600	"375732740000012611"
#   Q141216403 Olof Nilsson: P22 father = the item just created
Q141216403	P22	LAST	S2600	"375732740000012611"
#   the item just created: P735 given name = Q16423038 Nils
LAST	P735	Q16423038

# create a new item
CREATE
#   set the en label to "Ola Jonson Hetland"
LAST	Len	"Ola Jonson Hetland"
#   set the mul label to "Ola Jonson Hetland"
LAST	Lmul	"Ola Jonson Hetland"
#   set the ja label to "オーラ・ヨンソン・ヘトランド"
LAST	Lja	"オーラ・ヨンソン・ヘトランド"
#   set the zh label to "乌拉·永松·赫特拉恩德"
LAST	Lzh	"乌拉·永松·赫特拉恩德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003491988866 Ola Jonson Hetland, qualified P1810 subject named as Ola Jonson Hetland
LAST	P2600	"6000000003491988866"	P1810	"Ola Jonson Hetland"
#   P570 date of death = +1733-00-00T00:00:00Z/9
LAST	P570	+1733-00-00T00:00:00Z/9	S2600	"6000000003491988866"
#   P40 child = Q141206082 Jon Olson Raustad
LAST	P40	Q141206082	S2600	"6000000003491988866"
#   Q141206082 Jon Olson Raustad: P22 father = the item just created
Q141206082	P22	LAST	S2600	"6000000003491988866"
#   the item just created: P735 given name = Q96675523 Ola
LAST	P735	Q96675523
#   P734 family name = Q16870758 Hetland
LAST	P734	Q16870758

# create a new item
CREATE
#   set the en label to "Ola Jonson Li"
LAST	Len	"Ola Jonson Li"
#   set the mul label to "Ola Jonson Li"
LAST	Lmul	"Ola Jonson Li"
#   set the ja label to "オーラ・ヨンソン・リ"
LAST	Lja	"オーラ・ヨンソン・リ"
#   set the zh label to "乌拉·永松·李"
LAST	Lzh	"乌拉·永松·李"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003095034832 Ola Jonson Li, qualified P1810 subject named as Ola Jonson Li
LAST	P2600	"6000000003095034832"	P1810	"Ola Jonson Li"
#   P22 father = Q141180408 Jon Larsson Mæle
LAST	P22	Q141180408	S2600	"6000000003095034832"
#   P25 mother = Q141180412 Marta Rasmusdatter Li
LAST	P25	Q141180412	S2600	"6000000003095034832"
#   Q141180408 Jon Larsson Mæle: P40 child = the item just created
Q141180408	P40	LAST	S2600	"6000000003095034832"
#   Q141180412 Marta Rasmusdatter Li: P40 child = the item just created
Q141180412	P40	LAST	S2600	"6000000003095034832"
#   the item just created: P735 given name = Q96675523 Ola
LAST	P735	Q96675523

# create a new item
CREATE
#   set the en label to "Osmund Larsen Raunes"
LAST	Len	"Osmund Larsen Raunes"
#   set the mul label to "Osmund Larsen Raunes"
LAST	Lmul	"Osmund Larsen Raunes"
#   set the ja label to "オスムンド・ラーシェン・ラウネス"
LAST	Lja	"オスムンド・ラーシェン・ラウネス"
#   set the zh label to "奥斯穆恩德·拉尔森·拉乌内斯"
LAST	Lzh	"奥斯穆恩德·拉尔森·拉乌内斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000012587690898 Osmund Larsen Raunes, qualified P1810 subject named as Osmund Larsen Raunes
LAST	P2600	"6000000012587690898"	P1810	"Osmund Larsen Raunes"
#   P569 date of birth = +1730-00-00T00:00:00Z/9
LAST	P569	+1730-00-00T00:00:00Z/9	S2600	"6000000012587690898"
#   P570 date of death = +1766-00-00T00:00:00Z/9
LAST	P570	+1766-00-00T00:00:00Z/9	S2600	"6000000012587690898"
#   P22 father = Q141216627 Lars Nilsen Raunes
LAST	P22	Q141216627	S2600	"6000000012587690898"
#   Q141216627 Lars Nilsen Raunes: P40 child = the item just created
Q141216627	P40	LAST	S2600	"6000000012587690898"
#   the item just created: P735 given name = Q7107242 Osmund
LAST	P735	Q7107242
#   P1449 nickname = en:"Lars Foss-Eikeland"
LAST	P1449	en:"Lars Foss-Eikeland"
#   add a mul alias "Lars Foss-Eikeland Raunes"
LAST	Amul	"Lars Foss-Eikeland Raunes"

# create a new item
CREATE
#   set the en label to "Per Andersson Storskytt"
LAST	Len	"Per Andersson Storskytt"
#   set the mul label to "Per Andersson Storskytt"
LAST	Lmul	"Per Andersson Storskytt"
#   add a mul alias "Per Andersson"
LAST	Amul	"Per Andersson"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000011078829655 Per Andersson Storskytt, qualified P1810 subject named as Per Andersson
LAST	P2600	"6000000011078829655"	P1810	"Per Andersson"
#   P569 date of birth = +1720-00-00T00:00:00Z/9
LAST	P569	+1720-00-00T00:00:00Z/9	S2600	"6000000011078829655"
#   P570 date of death = +1802-05-24T00:00:00Z/11
LAST	P570	+1802-05-24T00:00:00Z/11	S2600	"6000000011078829655"
#   P26 spouse = Q141216595 Anna Danielsdotter
LAST	P26	Q141216595	S2600	"6000000011078829655"
#   Q141216595 Anna Danielsdotter: P26 spouse = the item just created
Q141216595	P26	LAST	S2600	"6000000011078829655"
#   the item just created: P735 given name = Q13582800 Per
LAST	P735	Q13582800
#   P734 family name = Q2817217 Andersson
LAST	P734	Q2817217

# create a new item
CREATE
#   set the en label to "Per Persson Hagman"
LAST	Len	"Per Persson Hagman"
#   set the mul label to "Per Persson Hagman"
LAST	Lmul	"Per Persson Hagman"
#   add a mul alias "Per Persson"
LAST	Amul	"Per Persson"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000011078726908 Per Persson Hagman, qualified P1810 subject named as Per Persson
LAST	P2600	"6000000011078726908"	P1810	"Per Persson"
#   P569 date of birth = +1754-09-24T00:00:00Z/11
LAST	P569	+1754-09-24T00:00:00Z/11	S2600	"6000000011078726908"
#   P570 date of death = +1840-08-18T00:00:00Z/11
LAST	P570	+1840-08-18T00:00:00Z/11	S2600	"6000000011078726908"
#   P25 mother = Q141216595 Anna Danielsdotter
LAST	P25	Q141216595	S2600	"6000000011078726908"
#   Q141216595 Anna Danielsdotter: P40 child = the item just created
Q141216595	P40	LAST	S2600	"6000000011078726908"
#   the item just created: P735 given name = Q13582800 Per
LAST	P735	Q13582800
#   P734 family name = Q27876648 Persson
LAST	P734	Q27876648

# create a new item
CREATE
#   set the en label to "Rasmus Hansen Nord-Varhaug"
LAST	Len	"Rasmus Hansen Nord-Varhaug"
#   set the mul label to "Rasmus Hansen Nord-Varhaug"
LAST	Lmul	"Rasmus Hansen Nord-Varhaug"
#   add a mul alias "Rasmus Hansen Låge-Håland"
LAST	Amul	"Rasmus Hansen Låge-Håland"
#   set the ja label to "ラスムス・ハンセン・ノール・ヴァールハウグ"
LAST	Lja	"ラスムス・ハンセン・ノール・ヴァールハウグ"
#   set the zh label to "拉斯穆斯·哈恩森·诺尔·瓦尔豪格"
LAST	Lzh	"拉斯穆斯·哈恩森·诺尔·瓦尔豪格"
#   add a ja alias "ラスムス・ハンセン・ローゲホーランド"
LAST	Aja	"ラスムス・ハンセン・ローゲホーランド"
#   add a zh alias "拉斯穆斯·哈恩森·洛盖霍拉恩德"
LAST	Azh	"拉斯穆斯·哈恩森·洛盖霍拉恩德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000087451690855 Rasmus Hansen Nord-Varhaug, qualified P1810 subject named as Rasmus Hansen Låge-Håland
LAST	P2600	"6000000087451690855"	P1810	"Rasmus Hansen Låge-Håland"
#   P569 date of birth = +1710-00-00T00:00:00Z/9
LAST	P569	+1710-00-00T00:00:00Z/9	S2600	"6000000087451690855"
#   P570 date of death = +1774-06-18T00:00:00Z/11
LAST	P570	+1774-06-18T00:00:00Z/11	S2600	"6000000087451690855"
#   P22 father = Q141216381 Hans Rasmussen Låge-Håland
LAST	P22	Q141216381	S2600	"6000000087451690855"
#   P25 mother = Q141216383 Ingeborg Eriksdatter Bjorland
LAST	P25	Q141216383	S2600	"6000000087451690855"
#   Q141216381 Hans Rasmussen Låge-Håland: P40 child = the item just created
Q141216381	P40	LAST	S2600	"6000000087451690855"
#   Q141216383 Ingeborg Eriksdatter Bjorland: P40 child = the item just created
Q141216383	P40	LAST	S2600	"6000000087451690855"
#   the item just created: P735 given name = Q1785744 Rasmus
LAST	P735	Q1785744
#   add a mul alias "Rasmus Nord-Varhaug"
LAST	Amul	"Rasmus Nord-Varhaug"

# create a new item
CREATE
#   set the en label to "Reiar Einarsen Kydland"
LAST	Len	"Reiar Einarsen Kydland"
#   set the mul label to "Reiar Einarsen Kydland"
LAST	Lmul	"Reiar Einarsen Kydland"
#   set the ja label to "レイアル・エイナルセン・キドランド"
LAST	Lja	"レイアル・エイナルセン・キドランド"
#   set the zh label to "雷伊阿尔·艾纳尔森·基德拉恩德"
LAST	Lzh	"雷伊阿尔·艾纳尔森·基德拉恩德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000000496970049 Reiar Einarsen Kydland, qualified P1810 subject named as Reiar Einarsen Kydland
LAST	P2600	"6000000000496970049"	P1810	"Reiar Einarsen Kydland"
#   P569 date of birth = +1667-00-00T00:00:00Z/9
LAST	P569	+1667-00-00T00:00:00Z/9	S2600	"6000000000496970049"
#   P570 date of death = +1734-00-00T00:00:00Z/9
LAST	P570	+1734-00-00T00:00:00Z/9	S2600	"6000000000496970049"
#   P40 child = Q141216645 Reiar Reiersen Kydland
LAST	P40	Q141216645	S2600	"6000000000496970049"
#   Q141216645 Reiar Reiersen Kydland: P22 father = the item just created
Q141216645	P22	LAST	S2600	"6000000000496970049"

# create a new item
CREATE
#   the item just created: set the en label to "Sara Asbjørnsdatter Bø"
LAST	Len	"Sara Asbjørnsdatter Bø"
#   set the mul label to "Sara Asbjørnsdatter Bø"
LAST	Lmul	"Sara Asbjørnsdatter Bø"
#   set the ja label to "サラ・アスブヨルンスダッテル・ベー"
LAST	Lja	"サラ・アスブヨルンスダッテル・ベー"
#   set the zh label to "萨拉·阿斯布永尔恩斯达特·贝"
LAST	Lzh	"萨拉·阿斯布永尔恩斯达特·贝"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000222520233004 Sara Asbjørnsdatter Bø, qualified P1810 subject named as Sara Asbjørnsdatter Bø
LAST	P2600	"6000000222520233004"	P1810	"Sara Asbjørnsdatter Bø"
#   P569 date of birth = +1762-00-00T00:00:00Z/9
LAST	P569	+1762-00-00T00:00:00Z/9	S2600	"6000000222520233004"
#   P22 father = Q141216458 Asbjørn Gunnarson Bø
LAST	P22	Q141216458	S2600	"6000000222520233004"
#   P25 mother = Q141216456 Anna Helgesdotter Opstad
LAST	P25	Q141216456	S2600	"6000000222520233004"
#   Q141216458 Asbjørn Gunnarson Bø: P40 child = the item just created
Q141216458	P40	LAST	S2600	"6000000222520233004"
#   Q141216456 Anna Helgesdotter Opstad: P40 child = the item just created
Q141216456	P40	LAST	S2600	"6000000222520233004"
#   the item just created: P735 given name = Q833345 Sara
LAST	P735	Q833345

# create a new item
CREATE
#   set the en label to "Sune Folkesson Folkunga"
LAST	Len	"Sune Folkesson Folkunga"
#   set the mul label to "Sune Folkesson Folkunga"
LAST	Lmul	"Sune Folkesson Folkunga"
#   set the ja label to "スネ・フォルケソン・フォルクンガ"
LAST	Lja	"スネ・フォルケソン・フォルクンガ"
#   set the zh label to "苏内·福尔凯松·福尔库恩加"
LAST	Lzh	"苏内·福尔凯松·福尔库恩加"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 4293217 Sune Folkesson Folkunga, qualified P1810 subject named as Sune Folkesson Folkunga
LAST	P2600	"4293217"	P1810	"Sune Folkesson Folkunga"
#   P569 date of birth = +1195-00-00T00:00:00Z/9
LAST	P569	+1195-00-00T00:00:00Z/9	S2600	"4293217"
#   P570 date of death = +1247-00-00T00:00:00Z/9
LAST	P570	+1247-00-00T00:00:00Z/9	S2600	"4293217"
#   P40 child = Q4981287 Benedicta Sunesdotter Folkungaätten
LAST	P40	Q4981287	S2600	"4293217"
#   Q4981287 Benedicta Sunesdotter Folkungaätten: P22 father = the item just created
Q4981287	P22	LAST	S2600	"4293217"
#   the item just created: P735 given name = Q920329 Sune
LAST	P735	Q920329
#   P1449 nickname = en:"Bjälbo"
LAST	P1449	en:"Bjälbo"
#   add a mul alias "Bjälbo Folkunga"
LAST	Amul	"Bjälbo Folkunga"

# create a new item
CREATE
#   set the en label to "Tollak Jonsson Aukland III"
LAST	Len	"Tollak Jonsson Aukland III"
#   set the mul label to "Tollak Jonsson Aukland III"
LAST	Lmul	"Tollak Jonsson Aukland III"
#   set the ja label to "トラク・ヨンソン・アウクランド・イイイ"
LAST	Lja	"トラク・ヨンソン・アウクランド・イイイ"
#   set the zh label to "托拉克·永松·奥克拉恩德·伊伊伊"
LAST	Lzh	"托拉克·永松·奥克拉恩德·伊伊伊"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000002390972936 Tollak Jonsson Aukland III, qualified P1810 subject named as Tollak Jonsson Aukland III
LAST	P2600	"6000000002390972936"	P1810	"Tollak Jonsson Aukland III"
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
#   set the en label to "Torger Olson Skorve"
LAST	Len	"Torger Olson Skorve"
#   set the mul label to "Torger Olson Skorve"
LAST	Lmul	"Torger Olson Skorve"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 3960809 Torger Olson Skorve, qualified P1810 subject named as Torger Olson Skorve
LAST	P2600	"3960809"	P1810	"Torger Olson Skorve"
#   P569 date of birth = +1753-07-02T00:00:00Z/11
LAST	P569	+1753-07-02T00:00:00Z/11	S2600	"3960809"
#   P570 date of death = +1826-12-28T00:00:00Z/11
LAST	P570	+1826-12-28T00:00:00Z/11	S2600	"3960809"
#   P40 child = Q141216653 Torger Torgerson Stokka
LAST	P40	Q141216653	S2600	"3960809"
#   Q141216653 Torger Torgerson Stokka: P22 father = the item just created
Q141216653	P22	LAST	S2600	"3960809"
#   the item just created: P735 given name = Q2444019 Torger
LAST	P735	Q2444019

# create a new item
CREATE
#   set the en label to "Tormod Olavsen Foss"
LAST	Len	"Tormod Olavsen Foss"
#   set the mul label to "Tormod Olavsen Foss"
LAST	Lmul	"Tormod Olavsen Foss"
#   set the ja label to "トルモド・オラヴセン・フォス"
LAST	Lja	"トルモド・オラヴセン・フォス"
#   set the zh label to "托尔莫德·奥拉夫森·福斯"
LAST	Lzh	"托尔莫德·奥拉夫森·福斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000002376687013 Tormod Olavsen Foss, qualified P1810 subject named as Tormod Olavsen Foss
LAST	P2600	"6000000002376687013"	P1810	"Tormod Olavsen Foss"
#   P569 date of birth = +1535-00-00T00:00:00Z/9
LAST	P569	+1535-00-00T00:00:00Z/9	S2600	"6000000002376687013"
#   P570 date of death = +1614-00-00T00:00:00Z/9
LAST	P570	+1614-00-00T00:00:00Z/9	S2600	"6000000002376687013"
#   P40 child = Q141206080 Peder Tormodson Foss
LAST	P40	Q141206080	S2600	"6000000002376687013"
#   Q141206080 Peder Tormodson Foss: P22 father = the item just created
Q141206080	P22	LAST	S2600	"6000000002376687013"
#   the item just created: P735 given name = Q7825922 Tormod
LAST	P735	Q7825922
#   P734 family name = Q16870001 Foss
LAST	P734	Q16870001

# create a new item
CREATE
#   set the mul label to "nn ektefelle Tollak Jonsson III Aukland"
LAST	Lmul	"nn ektefelle Tollak Jonsson III Aukland"
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
#   set the ja label to "ヨン・トラクソン・アウクランド・イヴの母"
LAST	Lja	"ヨン・トラクソン・アウクランド・イヴの母"
#   set the nb label to "mor til Jon Tollakson Aukland IV"
LAST	Lnb	"mor til Jon Tollakson Aukland IV"
#   set the nl label to "moeder van Jon Tollakson Aukland IV"
LAST	Lnl	"moeder van Jon Tollakson Aukland IV"
#   set the pt label to "mãe de Jon Tollakson Aukland IV"
LAST	Lpt	"mãe de Jon Tollakson Aukland IV"
#   set the sv label to "mor till Jon Tollakson Aukland IV"
LAST	Lsv	"mor till Jon Tollakson Aukland IV"
#   set the zh label to "永·托拉克松·奥克拉恩德·伊夫之母"
LAST	Lzh	"永·托拉克松·奥克拉恩德·伊夫之母"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000221742699868 nn ektefelle Tollak Jonsson III Aukland, qualified P1810 subject named as nn ektefelle Tollak Jonsson III Aukland
LAST	P2600	"6000000221742699868"	P1810	"nn ektefelle Tollak Jonsson III Aukland"
#   P40 child = Q141199899 Jon Tollakson Aukland IV
LAST	P40	Q141199899	S2600	"6000000221742699868"
#   Q141199899 Jon Tollakson Aukland IV: P25 mother = the item just created
Q141199899	P25	LAST	S2600	"6000000221742699868"
#   Q141216618 Karin Olofsdotter: P3373 sibling = Q141205931 Olof Olofsson
Q141216618	P3373	Q141205931	S2600	"348968026630001429"
#   Q141216611 Jon Villumson Raunes: P26 spouse = Q141216632 Magdalena Lauritsd Hogganvik
Q141216611	P26	Q141216632	S2600	"6000000001169146145"
#   Q141216602 Berta Guria Davidsdatter Stokka: P26 spouse = Q141216653 Torger Torgerson Stokka
Q141216602	P26	Q141216653	S2600	"6000000002726900648"
#   Q141216653 Torger Torgerson Stokka: P26 spouse = Q141216602 Berta Guria Davidsdatter Stokka
Q141216653	P26	Q141216602	S2600	"6000000002726968193"
#   Q141199819 Anna Andersdotter: P40 child = Q141199734 Nils Andersson
Q141199819	P40	Q141199734	S2600	"6000000003125438035"
#   Q141216644 Rasmus Asbjørnson Nedre Rossavik: P40 child = Q141216599 Anna Rasmusdatter Nedre Rossavik
Q141216644	P40	Q141216599	S2600	"6000000003192698959"
#   Q141216638 Olaug Jonsdatter Heigre: P26 spouse = Q141216637 Ola Person Persson Heigre
Q141216638	P26	Q141216637	S2600	"6000000003491933401"
#   Q141216637 Ola Person Persson Heigre: P26 spouse = Q141216638 Olaug Jonsdatter Heigre
Q141216637	P26	Q141216638	S2600	"6000000003491947917"
#   Q141216635 Martha Eivindsdatter Heigre: P40 child = Q141216643 Ragna Enevaldsdatter Heigre
Q141216635	P40	Q141216643	S2600	"6000000003491988061"
#   Q141216643 Ragna Enevaldsdatter Heigre: P25 mother = Q141216635 Martha Eivindsdatter Heigre
Q141216643	P25	Q141216635	S2600	"6000000003491988081"
#   Q141216632 Magdalena Lauritsd Hogganvik: P26 spouse = Q141216611 Jon Villumson Raunes
Q141216632	P26	Q141216611	S2600	"6000000005607268671"
#   Q141216613 Karen Henriksdotter Raunes Våga: P40 child = Q141216627 Lars Nilsen Raunes
Q141216613	P40	Q141216627	S2600	"6000000005607377021"
#   Q141216627 Lars Nilsen Raunes: P25 mother = Q141216613 Karen Henriksdotter Raunes Våga
Q141216627	P25	Q141216613	S2600	"6000000005609304829"
#   Q141216645 Reiar Reiersen Kydland: P26 spouse = Q141216609 Inger Kristoffersdatter Skårland
Q141216645	P26	Q141216609	S2600	"6000000005609534659"
#   Q141216609 Inger Kristoffersdatter Skårland: P26 spouse = Q141216645 Reiar Reiersen Kydland
Q141216609	P26	Q141216645	S2600	"6000000005609534669"
#   Q141216599 Anna Rasmusdatter Nedre Rossavik: P22 father = Q141216644 Rasmus Asbjørnson Nedre Rossavik
Q141216599	P22	Q141216644	S2600	"6000000008916446714"
#   Q141216633 Malin Jacobsdotter: P40 child = Q141216595 Anna Danielsdotter
Q141216633	P40	Q141216595	S2600	"6000000011078760054"
#   Q141216595 Anna Danielsdotter: P25 mother = Q141216633 Malin Jacobsdotter
Q141216595	P25	Q141216633	S2600	"6000000011078918407"
#   P5056 patronym or matronym = Q140226461, qualified P144 based on Q141216461 Daniel Andersson
Q141216595	P5056	Q140226461	P144	Q141216461
#   Q141216639 Olufine Bergithe Ekman: P26 spouse = Q141216640 Per Gustaf Ekman
Q141216639	P26	Q141216640	S2600	"6000000014196479728"
#   Q141216640 Per Gustaf Ekman: P26 spouse = Q141216639 Olufine Bergithe Ekman
Q141216640	P26	Q141216639	S2600	"6000000032811550619"
#   Q141200083 Sara NN: P26 spouse = Q141199734 Nils Andersson
Q141200083	P26	Q141199734	S2600	"6000000059888596942"

