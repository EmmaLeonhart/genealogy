# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   2203 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
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

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Ane Maria Olsdatter Vestre Stangaland"
LAST	Len	"Ane Maria Olsdatter Vestre Stangaland"
#   set the mul label to "Ane Maria Olsdatter Vestre Stangaland"
LAST	Lmul	"Ane Maria Olsdatter Vestre Stangaland"
#   add a mul alias "Ane Maria Olsdatter Grannes"
LAST	Amul	"Ane Maria Olsdatter Grannes"
#   set the ja label to "アーネ・マリア・オルスダッテル・ヴェストレ・スタンガランド"
LAST	Lja	"アーネ・マリア・オルスダッテル・ヴェストレ・スタンガランド"
#   set the zh label to "安内·马里阿·奥尔斯达特·韦斯特雷·斯塔恩加拉恩德"
LAST	Lzh	"安内·马里阿·奥尔斯达特·韦斯特雷·斯塔恩加拉恩德"
#   add a ja alias "アーネ・マリア・オルスダッテル・グラネス"
LAST	Aja	"アーネ・マリア・オルスダッテル・グラネス"
#   add a zh alias "安内·马里阿·奥尔斯达特·格拉内斯"
LAST	Azh	"安内·马里阿·奥尔斯达特·格拉内斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003491995729 Ane Maria Olsdatter Vestre Stangaland, qualified P1810 subject named as Ane Maria Olsdatter Grannes
LAST	P2600	"6000000003491995729"	P1810	"Ane Maria Olsdatter Grannes"
#   P569 date of birth = +1853-12-18T00:00:00Z/11
LAST	P569	+1853-12-18T00:00:00Z/11	S2600	"6000000003491995729"
#   P570 date of death = +1875-07-21T00:00:00Z/11
LAST	P570	+1875-07-21T00:00:00Z/11	S2600	"6000000003491995729"
#   P26 spouse = Q141216393 Kristian Monsen Stangeland
LAST	P26	Q141216393	S2600	"6000000003491995729"
#   P40 child = Q141205896 Ane Marie Konstanse Amanda Kristine Hegre
LAST	P40	Q141205896	S2600	"6000000003491995729"
#   Q141216393 Kristian Monsen Stangeland: P26 spouse = the item just created
Q141216393	P26	LAST	S2600	"6000000003491995729"
#   Q141205896 Ane Marie Konstanse Amanda Kristine Hegre: P25 mother = the item just created
Q141205896	P25	LAST	S2600	"6000000003491995729"
#   the item just created: P735 given name = Q11958077 Ane, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q11958077	P1545	"1"	P7452	Q3409033
#   P5056 patronym or matronym = Q51885688 Olsdatter
LAST	P5056	Q51885688
#   P734 family name = Q37442010 Grannes, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q37442010	P3831	Q2507958
#   add a mul alias "Ane Maria Vestre Stangaland"
LAST	Amul	"Ane Maria Vestre Stangaland"

# create a new item
CREATE
#   set the en label to "Anna Danielsdotter"
LAST	Len	"Anna Danielsdotter"
#   set the mul label to "Anna Danielsdotter"
LAST	Lmul	"Anna Danielsdotter"
#   set the ja label to "アンナ・ダニエルスドッテル"
LAST	Lja	"アンナ・ダニエルスドッテル"
#   set the zh label to "安娜·达尼埃尔斯多特"
LAST	Lzh	"安娜·达尼埃尔斯多特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000011078918407 Anna Danielsdotter, qualified P1810 subject named as Anna Danielsdotter
LAST	P2600	"6000000011078918407"	P1810	"Anna Danielsdotter"
#   P569 date of birth = +1718-00-00T00:00:00Z/9
LAST	P569	+1718-00-00T00:00:00Z/9	S2600	"6000000011078918407"
#   P570 date of death = +1802-00-00T00:00:00Z/9
LAST	P570	+1802-00-00T00:00:00Z/9	S2600	"6000000011078918407"
#   P22 father = Q141216461 Daniel Andersson
LAST	P22	Q141216461	S2600	"6000000011078918407"
#   Q141216461 Daniel Andersson: P40 child = the item just created
Q141216461	P40	LAST	S2600	"6000000011078918407"

# create a new item
CREATE
#   the item just created: set the en label to "Anna Ivarsd Stokka"
LAST	Len	"Anna Ivarsd Stokka"
#   set the mul label to "Anna Ivarsd Stokka"
LAST	Lmul	"Anna Ivarsd Stokka"
#   set the ja label to "アンナ・イヴァルスド・ストカ"
LAST	Lja	"アンナ・イヴァルスド・ストカ"
#   set the zh label to "安娜·伊瓦尔斯德·斯托卡"
LAST	Lzh	"安娜·伊瓦尔斯德·斯托卡"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003830468150 Anna Ivarsd Stokka, qualified P1810 subject named as Anna Ivarsd Stokka
LAST	P2600	"6000000003830468150"	P1810	"Anna Ivarsd Stokka"
#   P569 date of birth = +1514-00-00T00:00:00Z/9
LAST	P569	+1514-00-00T00:00:00Z/9	S2600	"6000000003830468150"
#   P26 spouse = Q141216499 Orm Ånonsen
LAST	P26	Q141216499	S2600	"6000000003830468150"
#   P40 child = Q141205922 Marit Ormsd Byre
LAST	P40	Q141205922	S2600	"6000000003830468150"
#   Q141216499 Orm Ånonsen: P26 spouse = the item just created
Q141216499	P26	LAST	S2600	"6000000003830468150"
#   Q141205922 Marit Ormsd Byre: P25 mother = the item just created
Q141205922	P25	LAST	S2600	"6000000003830468150"

# create a new item
CREATE
#   the item just created: set the en label to "Anna Rasmusdatter Nedre Rossavik"
LAST	Len	"Anna Rasmusdatter Nedre Rossavik"
#   set the mul label to "Anna Rasmusdatter Nedre Rossavik"
LAST	Lmul	"Anna Rasmusdatter Nedre Rossavik"
#   set the ja label to "アンナ・ラスムスダッテル・ネドレ・ロサヴィク"
LAST	Lja	"アンナ・ラスムスダッテル・ネドレ・ロサヴィク"
#   set the zh label to "安娜·拉斯穆斯达特·内德雷·罗萨维克"
LAST	Lzh	"安娜·拉斯穆斯达特·内德雷·罗萨维克"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000008916446714 Anna Rasmusdatter Nedre Rossavik, qualified P1810 subject named as Anna Rasmusdatter Nedre Rossavik
LAST	P2600	"6000000008916446714"	P1810	"Anna Rasmusdatter Nedre Rossavik"
#   P569 date of birth = +1697-00-00T00:00:00Z/9
LAST	P569	+1697-00-00T00:00:00Z/9	S2600	"6000000008916446714"
#   P570 date of death = +1730-09-10T00:00:00Z/11
LAST	P570	+1730-09-10T00:00:00Z/11	S2600	"6000000008916446714"
#   P25 mother = Q141205898 Anna Tormodsdatter Mele
LAST	P25	Q141205898	S2600	"6000000008916446714"
#   Q141205898 Anna Tormodsdatter Mele: P40 child = the item just created
Q141205898	P40	LAST	S2600	"6000000008916446714"

# create a new item
CREATE
#   the item just created: set the en label to "Astrid Omundsdatter Grøtheim"
LAST	Len	"Astrid Omundsdatter Grøtheim"
#   set the mul label to "Astrid Omundsdatter Grøtheim"
LAST	Lmul	"Astrid Omundsdatter Grøtheim"
#   add a mul alias "Astrid Omundsdatter Opstad"
LAST	Amul	"Astrid Omundsdatter Opstad"
#   set the ja label to "アストリッド・オムンドスダッテル・グレートヘイム"
LAST	Lja	"アストリッド・オムンドスダッテル・グレートヘイム"
#   set the zh label to "阿斯特丽德·奥穆恩德斯达特·格勒特海姆"
LAST	Lzh	"阿斯特丽德·奥穆恩德斯达特·格勒特海姆"
#   add a ja alias "アストリッド・オムンドスダッテル・オプスタド"
LAST	Aja	"アストリッド・オムンドスダッテル・オプスタド"
#   add a zh alias "阿斯特丽德·奥穆恩德斯达特·奥普斯塔德"
LAST	Azh	"阿斯特丽德·奥穆恩德斯达特·奥普斯塔德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000008176887325 Astrid Omundsdatter Grøtheim, qualified P1810 subject named as Astrid Omundsdatter Opstad
LAST	P2600	"6000000008176887325"	P1810	"Astrid Omundsdatter Opstad"
#   P569 date of birth = +1742-00-00T00:00:00Z/9
LAST	P569	+1742-00-00T00:00:00Z/9	S2600	"6000000008176887325"
#   P570 date of death = +1804-11-18T00:00:00Z/11
LAST	P570	+1804-11-18T00:00:00Z/11	S2600	"6000000008176887325"
#   P26 spouse = Q141189088 Ola Knutsen Grøtheim
LAST	P26	Q141189088	S2600	"6000000008176887325"
#   Q141189088 Ola Knutsen Grøtheim: P26 spouse = the item just created
Q141189088	P26	LAST	S2600	"6000000008176887325"
#   the item just created: P735 given name = Q167755 Astrid
LAST	P735	Q167755
#   P734 family name = Q37268235 Opstad, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q37268235	P3831	Q2507958
#   add a mul alias "Astrid Grøtheim"
LAST	Amul	"Astrid Grøtheim"

# create a new item
CREATE
#   set the en label to "Austman Gustavson Gudfastarsson"
LAST	Len	"Austman Gustavson Gudfastarsson"
#   set the mul label to "Austman Gustavson Gudfastarsson"
LAST	Lmul	"Austman Gustavson Gudfastarsson"
#   set the ja label to "アウストマン・グスタヴソン・グドファスタルソン"
LAST	Lja	"アウストマン・グスタヴソン・グドファスタルソン"
#   set the zh label to "奥斯特马恩·古斯塔夫松·古德法斯塔尔松"
LAST	Lzh	"奥斯特马恩·古斯塔夫松·古德法斯塔尔松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000221197647828 Austman Gustavson Gudfastarsson, qualified P1810 subject named as Austman Gustavson Gudfastarsson
LAST	P2600	"6000000221197647828"	P1810	"Austman Gustavson Gudfastarsson"
#   P569 date of birth = +1080-00-00T00:00:00Z/9
LAST	P569	+1080-00-00T00:00:00Z/9	S2600	"6000000221197647828"
#   P570 date of death = +1140-00-00T00:00:00Z/9
LAST	P570	+1140-00-00T00:00:00Z/9	S2600	"6000000221197647828"
#   P40 child = Q10511224 Guttorm Ostmannson of Jämtland & Svealand
LAST	P40	Q10511224	S2600	"6000000221197647828"
#   Q10511224 Guttorm Ostmannson of Jämtland & Svealand: P22 father = the item just created
Q10511224	P22	LAST	S2600	"6000000221197647828"

# create a new item
CREATE
#   the item just created: set the en label to "Berta Guria Davidsdatter Stokka"
LAST	Len	"Berta Guria Davidsdatter Stokka"
#   set the mul label to "Berta Guria Davidsdatter Stokka"
LAST	Lmul	"Berta Guria Davidsdatter Stokka"
#   add a mul alias "Berta Guria Davidsdatter Edland"
LAST	Amul	"Berta Guria Davidsdatter Edland"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000002726900648 Berta Guria Davidsdatter Stokka, qualified P1810 subject named as Berta Guria Davidsdatter Edland
LAST	P2600	"6000000002726900648"	P1810	"Berta Guria Davidsdatter Edland"
#   P569 date of birth = +1806-00-00T00:00:00Z/9
LAST	P569	+1806-00-00T00:00:00Z/9	S2600	"6000000002726900648"
#   P570 date of death = +1870-03-29T00:00:00Z/11
LAST	P570	+1870-03-29T00:00:00Z/11	S2600	"6000000002726900648"
#   P40 child = Q141216510 Torger Torgerson Stokka
LAST	P40	Q141216510	S2600	"6000000002726900648"
#   Q141216510 Torger Torgerson Stokka: P25 mother = the item just created
Q141216510	P25	LAST	S2600	"6000000002726900648"
#   the item just created: P735 given name = Q4092653 Berta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q4092653	P1545	"1"	P7452	Q3409033
#   add a mul alias "Berta Guria Stokka"
LAST	Amul	"Berta Guria Stokka"

# create a new item
CREATE
#   set the en label to "Brynhild Hallvardsdotter"
LAST	Len	"Brynhild Hallvardsdotter"
#   set the mul label to "Brynhild Hallvardsdotter"
LAST	Lmul	"Brynhild Hallvardsdotter"
#   set the ja label to "ブリンヒルド・ハルヴァルドスドッテル"
LAST	Lja	"ブリンヒルド・ハルヴァルドスドッテル"
#   set the zh label to "布里恩希尔德·哈尔瓦尔德斯多特"
LAST	Lzh	"布里恩希尔德·哈尔瓦尔德斯多特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000004870702053 Brynhild Hallvardsdotter, qualified P1810 subject named as Brynhild Hallvardsdotter
LAST	P2600	"6000000004870702053"	P1810	"Brynhild Hallvardsdotter"
#   P569 date of birth = +1375-00-00T00:00:00Z/9
LAST	P569	+1375-00-00T00:00:00Z/9	S2600	"6000000004870702053"
#   P570 date of death = +1417-00-00T00:00:00Z/9
LAST	P570	+1417-00-00T00:00:00Z/9	S2600	"6000000004870702053"
#   P40 child = Q141205937 Ragnhild Eyvindsdotter Eyvindsdotter
LAST	P40	Q141205937	S2600	"6000000004870702053"
#   Q141205937 Ragnhild Eyvindsdotter Eyvindsdotter: P25 mother = the item just created
Q141205937	P25	LAST	S2600	"6000000004870702053"
#   the item just created: P735 given name = Q521264 Brynhild
LAST	P735	Q521264
#   P1449 nickname = en:"Hallvardsdatter"
LAST	P1449	en:"Hallvardsdatter"
#   add a mul alias "Hallvardsdatter Hallvardsdotter"
LAST	Amul	"Hallvardsdatter Hallvardsdotter"

# create a new item
CREATE
#   set the en label to "Gladys Signe Nash Stoeckmann"
LAST	Len	"Gladys Signe Nash Stoeckmann"
#   set the mul label to "Gladys Signe Nash Stoeckmann"
LAST	Lmul	"Gladys Signe Nash Stoeckmann"
#   add a mul alias "Gladys Signe Ekman"
LAST	Amul	"Gladys Signe Ekman"
#   set the ja label to "グラディス・シグネ・ナス・ストエククマン"
LAST	Lja	"グラディス・シグネ・ナス・ストエククマン"
#   set the zh label to "格拉迪斯·西格内·纳斯·斯托埃克克马恩"
LAST	Lzh	"格拉迪斯·西格内·纳斯·斯托埃克克马恩"
#   add a ja alias "グラディス・シグネ・エクマン"
LAST	Aja	"グラディス・シグネ・エクマン"
#   add a zh alias "格拉迪斯·西格内·埃克马恩"
LAST	Azh	"格拉迪斯·西格内·埃克马恩"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000179959474850 Gladys Signe Nash Stoeckmann, qualified P1810 subject named as Gladys Signe Ekman
LAST	P2600	"6000000179959474850"	P1810	"Gladys Signe Ekman"
#   P569 date of birth = +1917-09-16T00:00:00Z/11
LAST	P569	+1917-09-16T00:00:00Z/11	S2600	"6000000179959474850"
#   P570 date of death = +1976-11-25T00:00:00Z/11
LAST	P570	+1976-11-25T00:00:00Z/11	S2600	"6000000179959474850"
#   P22 father = Q141205908 Gotfred Olai Ekman
LAST	P22	Q141205908	S2600	"6000000179959474850"
#   P25 mother = Q141189102 Sigrid Sally Manilva Ekman
LAST	P25	Q141189102	S2600	"6000000179959474850"
#   Q141205908 Gotfred Olai Ekman: P40 child = the item just created
Q141205908	P40	LAST	S2600	"6000000179959474850"
#   Q141189102 Sigrid Sally Manilva Ekman: P40 child = the item just created
Q141189102	P40	LAST	S2600	"6000000179959474850"
#   the item just created: P735 given name = Q13422277 Gladys, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q13422277	P1545	"1"	P7452	Q3409033
#   P735 given name = Q2096893 Signe, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q2096893	P1545	"2"	P3831	Q245025
#   P734 family name = Q1965666 Nash, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q1965666	P3831	Q28418670

# create a new item
CREATE
#   set the en label to "Gunilla Jonsdotter"
LAST	Len	"Gunilla Jonsdotter"
#   set the mul label to "Gunilla Jonsdotter"
LAST	Lmul	"Gunilla Jonsdotter"
#   set the ja label to "グニラ・ヨンスドッテル"
LAST	Lja	"グニラ・ヨンスドッテル"
#   set the zh label to "古尼拉·永恩斯多特"
LAST	Lzh	"古尼拉·永恩斯多特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000007117021938 Gunilla Jonsdotter, qualified P1810 subject named as Gunilla Jonsdotter
LAST	P2600	"6000000007117021938"	P1810	"Gunilla Jonsdotter"
#   P569 date of birth = +1501-00-00T00:00:00Z/9
LAST	P569	+1501-00-00T00:00:00Z/9	S2600	"6000000007117021938"
#   P570 date of death = +1552-00-00T00:00:00Z/9
LAST	P570	+1552-00-00T00:00:00Z/9	S2600	"6000000007117021938"
#   P40 child = Q141216403 Olof Nilsson
LAST	P40	Q141216403	S2600	"6000000007117021938"
#   Q141216403 Olof Nilsson: P25 mother = the item just created
Q141216403	P25	LAST	S2600	"6000000007117021938"
#   the item just created: P735 given name = Q3909969 Gunilla
LAST	P735	Q3909969

# create a new item
CREATE
#   set the en label to "Hans Erikson Øvre Håland"
LAST	Len	"Hans Erikson Øvre Håland"
#   set the mul label to "Hans Erikson Øvre Håland"
LAST	Lmul	"Hans Erikson Øvre Håland"
#   add a mul alias "Hans Erikson Erikson"
LAST	Amul	"Hans Erikson Erikson"
#   set the ja label to "ハンス・エリクソン・オヴレ・ホーランド"
LAST	Lja	"ハンス・エリクソン・オヴレ・ホーランド"
#   set the zh label to "汉斯·埃里克松·奥夫雷·霍兰"
LAST	Lzh	"汉斯·埃里克松·奥夫雷·霍兰"
#   add a ja alias "ハンス・エリクソン・エリクソン"
LAST	Aja	"ハンス・エリクソン・エリクソン"
#   add a zh alias "汉斯·埃里克松·埃里克松"
LAST	Azh	"汉斯·埃里克松·埃里克松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000009152082622 Hans Erikson Øvre Håland, qualified P1810 subject named as Hans Erikson Erikson
LAST	P2600	"6000000009152082622"	P1810	"Hans Erikson Erikson"
#   P569 date of birth = +1681-00-00T00:00:00Z/9
LAST	P569	+1681-00-00T00:00:00Z/9	S2600	"6000000009152082622"
#   P570 date of death = +1733-00-00T00:00:00Z/9
LAST	P570	+1733-00-00T00:00:00Z/9	S2600	"6000000009152082622"
#   P26 spouse = Q141216507 Torborg Toresdatter Norheim
LAST	P26	Q141216507	S2600	"6000000009152082622"
#   P40 child = Q141200127 Ådne Hansen Grøtheim
LAST	P40	Q141200127	S2600	"6000000009152082622"
#   Q141216507 Torborg Toresdatter Norheim: P26 spouse = the item just created
Q141216507	P26	LAST	S2600	"6000000009152082622"
#   Q141200127 Ådne Hansen Grøtheim: P22 father = the item just created
Q141200127	P22	LAST	S2600	"6000000009152082622"
#   the item just created: add a mul alias "Hans Øvre Håland"
LAST	Amul	"Hans Øvre Håland"

# create a new item
CREATE
#   set the en label to "Hans Ådnesen Grøtheim"
LAST	Len	"Hans Ådnesen Grøtheim"
#   set the mul label to "Hans Ådnesen Grøtheim"
LAST	Lmul	"Hans Ådnesen Grøtheim"
#   set the ja label to "ハンス・オードネセン・グレートヘイム"
LAST	Lja	"ハンス・オードネセン・グレートヘイム"
#   set the zh label to "汉斯·奥德内森·格勒特海姆"
LAST	Lzh	"汉斯·奥德内森·格勒特海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000226485101824 Hans Ådnesen Grøtheim, qualified P1810 subject named as Hans Ådnesen Grøtheim
LAST	P2600	"6000000226485101824"	P1810	"Hans Ådnesen Grøtheim"
#   P569 date of birth = +1741-00-00T00:00:00Z/9
LAST	P569	+1741-00-00T00:00:00Z/9	S2600	"6000000226485101824"
#   P22 father = Q141200127 Ådne Hansen Grøtheim
LAST	P22	Q141200127	S2600	"6000000226485101824"
#   P25 mother = Q141199918 Kirsten Hansdatter Grøtheim
LAST	P25	Q141199918	S2600	"6000000226485101824"
#   Q141200127 Ådne Hansen Grøtheim: P40 child = the item just created
Q141200127	P40	LAST	S2600	"6000000226485101824"
#   Q141199918 Kirsten Hansdatter Grøtheim: P40 child = the item just created
Q141199918	P40	LAST	S2600	"6000000226485101824"

# create a new item
CREATE
#   the item just created: set the en label to "Inger Kristoffersdatter Skårland"
LAST	Len	"Inger Kristoffersdatter Skårland"
#   set the mul label to "Inger Kristoffersdatter Skårland"
LAST	Lmul	"Inger Kristoffersdatter Skårland"
#   set the ja label to "インゲル・クリストッフェシュダッテル・スコールランド"
LAST	Lja	"インゲル・クリストッフェシュダッテル・スコールランド"
#   set the zh label to "英厄尔·克里斯托弗斯达特·斯科尔拉恩德"
LAST	Lzh	"英厄尔·克里斯托弗斯达特·斯科尔拉恩德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005609534669 Inger Kristoffersdatter Skårland, qualified P1810 subject named as Inger Kristoffersdatter Skårland
LAST	P2600	"6000000005609534669"	P1810	"Inger Kristoffersdatter Skårland"
#   P569 date of birth = +1727-00-00T00:00:00Z/9
LAST	P569	+1727-00-00T00:00:00Z/9	S2600	"6000000005609534669"
#   P570 date of death = +1820-12-11T00:00:00Z/11
LAST	P570	+1820-12-11T00:00:00Z/11	S2600	"6000000005609534669"
#   P40 child = Q141198370 NN Skårland
LAST	P40	Q141198370	S2600	"6000000005609534669"
#   Q141198370 NN Skårland: P25 mother = the item just created
Q141198370	P25	LAST	S2600	"6000000005609534669"
#   the item just created: P735 given name = Q3358452 Inger
LAST	P735	Q3358452

# create a new item
CREATE
#   set the en label to "Jon Villumson Raunes"
LAST	Len	"Jon Villumson Raunes"
#   set the mul label to "Jon Villumson Raunes"
LAST	Lmul	"Jon Villumson Raunes"
#   add a mul alias "Jon Villumson Gautun"
LAST	Amul	"Jon Villumson Gautun"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000001169146145 Jon Villumson Raunes, qualified P1810 subject named as Jon Villumson Gautun
LAST	P2600	"6000000001169146145"	P1810	"Jon Villumson Gautun"
#   P569 date of birth = +1590-00-00T00:00:00Z/9
LAST	P569	+1590-00-00T00:00:00Z/9	S2600	"6000000001169146145"
#   P570 date of death = +1662-00-00T00:00:00Z/9
LAST	P570	+1662-00-00T00:00:00Z/9	S2600	"6000000001169146145"
#   P40 child = Q141216488 Lars Jonsen Landsnes
LAST	P40	Q141216488	S2600	"6000000001169146145"
#   Q141216488 Lars Jonsen Landsnes: P22 father = the item just created
Q141216488	P22	LAST	S2600	"6000000001169146145"
#   the item just created: P735 given name = Q13501137 Jon
LAST	P735	Q13501137
#   P1449 nickname = en:"Jon Raunes"
LAST	P1449	en:"Jon Raunes"
#   add a mul alias "Jon Raunes"
LAST	Amul	"Jon Raunes"

# create a new item
CREATE
#   set the en label to "Karen Henriksdotter Raunes Våga"
LAST	Len	"Karen Henriksdotter Raunes Våga"
#   set the mul label to "Karen Henriksdotter Raunes Våga"
LAST	Lmul	"Karen Henriksdotter Raunes Våga"
#   add a mul alias "Karen Henriksdotter Ringja"
LAST	Amul	"Karen Henriksdotter Ringja"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005607377021 Karen Henriksdotter Raunes Våga, qualified P1810 subject named as Karen Henriksdotter Ringja
LAST	P2600	"6000000005607377021"	P1810	"Karen Henriksdotter Ringja"
#   P569 date of birth = +1675-00-00T00:00:00Z/9
LAST	P569	+1675-00-00T00:00:00Z/9	S2600	"6000000005607377021"
#   P570 date of death = +1729-00-00T00:00:00Z/9
LAST	P570	+1729-00-00T00:00:00Z/9	S2600	"6000000005607377021"
#   P26 spouse = Q141216496 Nils Larsen Raunes
LAST	P26	Q141216496	S2600	"6000000005607377021"
#   Q141216496 Nils Larsen Raunes: P26 spouse = the item just created
Q141216496	P26	LAST	S2600	"6000000005607377021"
#   the item just created: P1449 nickname = en:"Kari"
LAST	P1449	en:"Kari"
#   add a mul alias "Kari Raunes Våga"
LAST	Amul	"Kari Raunes Våga"
#   add a mul alias "Karen Raunes Våga"
LAST	Amul	"Karen Raunes Våga"

# create a new item
CREATE
#   set the en label to "Karin Olofsdotter"
LAST	Len	"Karin Olofsdotter"
#   set the mul label to "Karin Olofsdotter"
LAST	Lmul	"Karin Olofsdotter"
#   set the ja label to "カリン・オロフスドッテル"
LAST	Lja	"カリン・オロフスドッテル"
#   set the zh label to "卡里恩·奥洛夫斯多特"
LAST	Lzh	"卡里恩·奥洛夫斯多特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 348968026630001429 Karin Olofsdotter, qualified P1810 subject named as Karin Olofsdotter
LAST	P2600	"348968026630001429"	P1810	"Karin Olofsdotter"
#   P22 father = Q141216403 Olof Nilsson
LAST	P22	Q141216403	S2600	"348968026630001429"
#   P25 mother = Q141216398 Malin Olofsdotter
LAST	P25	Q141216398	S2600	"348968026630001429"
#   Q141216403 Olof Nilsson: P40 child = the item just created
Q141216403	P40	LAST	S2600	"348968026630001429"
#   Q141216398 Malin Olofsdotter: P40 child = the item just created
Q141216398	P40	LAST	S2600	"348968026630001429"
#   the item just created: P735 given name = Q1814118 Karin
LAST	P735	Q1814118

# create a new item
CREATE
#   set the en label to "Kristine Jonsdatter Malmeim"
LAST	Len	"Kristine Jonsdatter Malmeim"
#   set the mul label to "Kristine Jonsdatter Malmeim"
LAST	Lmul	"Kristine Jonsdatter Malmeim"
#   add a mul alias "Kristine Jonsdatter Raustad"
LAST	Amul	"Kristine Jonsdatter Raustad"
#   set the ja label to "クリスティーネ・ヨンスダッテル・マルメイム"
LAST	Lja	"クリスティーネ・ヨンスダッテル・マルメイム"
#   set the zh label to "克丽丝汀·永斯达特·马尔梅伊姆"
LAST	Lzh	"克丽丝汀·永斯达特·马尔梅伊姆"
#   add a ja alias "クリスティーネ・ヨンスダッテル・ラウスタード"
LAST	Aja	"クリスティーネ・ヨンスダッテル・ラウスタード"
#   add a zh alias "克丽丝汀·永斯达特·劳斯塔"
LAST	Azh	"克丽丝汀·永斯达特·劳斯塔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003491988269 Kristine Jonsdatter Malmeim, qualified P1810 subject named as Kristine Jonsdatter Raustad
LAST	P2600	"6000000003491988269"	P1810	"Kristine Jonsdatter Raustad"
#   P569 date of birth = +1826-12-28T00:00:00Z/11
LAST	P569	+1826-12-28T00:00:00Z/11	S2600	"6000000003491988269"
#   P570 date of death = +1902-04-14T00:00:00Z/11
LAST	P570	+1902-04-14T00:00:00Z/11	S2600	"6000000003491988269"
#   P22 father = Q141168955 Jon Samuelsen Raustad
LAST	P22	Q141168955	S2600	"6000000003491988269"
#   P25 mother = Q141178200 Inger Kristoffersdatter
LAST	P25	Q141178200	S2600	"6000000003491988269"
#   Q141168955 Jon Samuelsen Raustad: P40 child = the item just created
Q141168955	P40	LAST	S2600	"6000000003491988269"
#   Q141178200 Inger Kristoffersdatter: P40 child = the item just created
Q141178200	P40	LAST	S2600	"6000000003491988269"
#   the item just created: P735 given name = Q16859157 Kristine
LAST	P735	Q16859157
#   add a mul alias "Kristine Malmeim"
LAST	Amul	"Kristine Malmeim"

# create a new item
CREATE
#   set the en label to "Lars Nilsen Raunes"
LAST	Len	"Lars Nilsen Raunes"
#   set the mul label to "Lars Nilsen Raunes"
LAST	Lmul	"Lars Nilsen Raunes"
#   set the ja label to "ラーシュ・ニルセン・ラウネス"
LAST	Lja	"ラーシュ・ニルセン・ラウネス"
#   set the zh label to "拉尔斯·尼尔森·拉乌内斯"
LAST	Lzh	"拉尔斯·尼尔森·拉乌内斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005609304829 Lars Nilsen Raunes, qualified P1810 subject named as Lars Nilsen Raunes
LAST	P2600	"6000000005609304829"	P1810	"Lars Nilsen Raunes"
#   P569 date of birth = +1697-00-00T00:00:00Z/9
LAST	P569	+1697-00-00T00:00:00Z/9	S2600	"6000000005609304829"
#   P570 date of death = +1775-00-00T00:00:00Z/9
LAST	P570	+1775-00-00T00:00:00Z/9	S2600	"6000000005609304829"
#   P22 father = Q141216496 Nils Larsen Raunes
LAST	P22	Q141216496	S2600	"6000000005609304829"
#   Q141216496 Nils Larsen Raunes: P40 child = the item just created
Q141216496	P40	LAST	S2600	"6000000005609304829"
#   the item just created: P735 given name = Q15635262 Lars
LAST	P735	Q15635262
#   P1449 nickname = en:"Stråtveit"
LAST	P1449	en:"Stråtveit"
#   add a mul alias "Stråtveit Raunes"
LAST	Amul	"Stråtveit Raunes"

# create a new item
CREATE
#   set the en label to "Magdalena Lauritsd Hogganvik"
LAST	Len	"Magdalena Lauritsd Hogganvik"
#   set the mul label to "Magdalena Lauritsd Hogganvik"
LAST	Lmul	"Magdalena Lauritsd Hogganvik"
#   set the ja label to "マグダレーナ・ラウリトスド・ホガンヴィク"
LAST	Lja	"マグダレーナ・ラウリトスド・ホガンヴィク"
#   set the zh label to "玛格达莱娜·拉乌里特斯德·霍加恩维克"
LAST	Lzh	"玛格达莱娜·拉乌里特斯德·霍加恩维克"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005607268671 Magdalena Lauritsd Hogganvik, qualified P1810 subject named as Magdalena Lauritsd Hogganvik
LAST	P2600	"6000000005607268671"	P1810	"Magdalena Lauritsd Hogganvik"
#   P569 date of birth = +1600-00-00T00:00:00Z/9
LAST	P569	+1600-00-00T00:00:00Z/9	S2600	"6000000005607268671"
#   P570 date of death = +1673-00-00T00:00:00Z/9
LAST	P570	+1673-00-00T00:00:00Z/9	S2600	"6000000005607268671"
#   P40 child = Q141216488 Lars Jonsen Landsnes
LAST	P40	Q141216488	S2600	"6000000005607268671"
#   Q141216488 Lars Jonsen Landsnes: P25 mother = the item just created
Q141216488	P25	LAST	S2600	"6000000005607268671"
#   the item just created: P735 given name = Q842544 Magdalena, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q842544	P1545	"1"	P7452	Q3409033

# create a new item
CREATE
#   set the en label to "Malin Jacobsdotter"
LAST	Len	"Malin Jacobsdotter"
#   set the mul label to "Malin Jacobsdotter"
LAST	Lmul	"Malin Jacobsdotter"
#   set the ja label to "マリン・ヤコブスドッテル"
LAST	Lja	"マリン・ヤコブスドッテル"
#   set the zh label to "马利恩·雅科布斯多特"
LAST	Lzh	"马利恩·雅科布斯多特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000011078760054 Malin Jacobsdotter, qualified P1810 subject named as Malin Jacobsdotter
LAST	P2600	"6000000011078760054"	P1810	"Malin Jacobsdotter"
#   P569 date of birth = +1696-00-00T00:00:00Z/9
LAST	P569	+1696-00-00T00:00:00Z/9	S2600	"6000000011078760054"
#   P570 date of death = +1776-00-00T00:00:00Z/9
LAST	P570	+1776-00-00T00:00:00Z/9	S2600	"6000000011078760054"
#   P26 spouse = Q141216461 Daniel Andersson
LAST	P26	Q141216461	S2600	"6000000011078760054"
#   Q141216461 Daniel Andersson: P26 spouse = the item just created
Q141216461	P26	LAST	S2600	"6000000011078760054"
#   the item just created: P735 given name = Q18369928 Malin
LAST	P735	Q18369928

# create a new item
CREATE
#   set the en label to "Marit Hansdatter Stavnheim"
LAST	Len	"Marit Hansdatter Stavnheim"
#   set the mul label to "Marit Hansdatter Stavnheim"
LAST	Lmul	"Marit Hansdatter Stavnheim"
#   add a mul alias "Marit Hansdatter Låge-Håland"
LAST	Amul	"Marit Hansdatter Låge-Håland"
#   set the ja label to "マリト・ハンスダッテル・スタヴンヘイム"
LAST	Lja	"マリト・ハンスダッテル・スタヴンヘイム"
#   set the zh label to "马里特·汉斯达特·斯塔夫恩赫伊姆"
LAST	Lzh	"马里特·汉斯达特·斯塔夫恩赫伊姆"
#   add a ja alias "マリト・ハンスダッテル・ローゲホーランド"
LAST	Aja	"マリト・ハンスダッテル・ローゲホーランド"
#   add a zh alias "马里特·汉斯达特·洛盖霍拉恩德"
LAST	Azh	"马里特·汉斯达特·洛盖霍拉恩德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000009127909254 Marit Hansdatter Stavnheim, qualified P1810 subject named as Marit Hansdatter Låge-Håland
LAST	P2600	"6000000009127909254"	P1810	"Marit Hansdatter Låge-Håland"
#   P569 date of birth = +1701-00-00T00:00:00Z/9
LAST	P569	+1701-00-00T00:00:00Z/9	S2600	"6000000009127909254"
#   P22 father = Q141216381 Hans Rasmussen Låge-Håland
LAST	P22	Q141216381	S2600	"6000000009127909254"
#   P25 mother = Q141216383 Ingeborg Eriksdatter Bjorland
LAST	P25	Q141216383	S2600	"6000000009127909254"
#   Q141216381 Hans Rasmussen Låge-Håland: P40 child = the item just created
Q141216381	P40	LAST	S2600	"6000000009127909254"
#   Q141216383 Ingeborg Eriksdatter Bjorland: P40 child = the item just created
Q141216383	P40	LAST	S2600	"6000000009127909254"
#   the item just created: P735 given name = Q1566153 Marit
LAST	P735	Q1566153
#   add a mul alias "Marit Stavnheim"
LAST	Amul	"Marit Stavnheim"

# create a new item
CREATE
#   set the en label to "Martha Eivindsdatter Heigre"
LAST	Len	"Martha Eivindsdatter Heigre"
#   set the mul label to "Martha Eivindsdatter Heigre"
LAST	Lmul	"Martha Eivindsdatter Heigre"
#   add a mul alias "Martha Eivindsdatter Sveinsvoll"
LAST	Amul	"Martha Eivindsdatter Sveinsvoll"
#   set the ja label to "マルタ・エイヴィンスダッテル・ヘイグレ"
LAST	Lja	"マルタ・エイヴィンスダッテル・ヘイグレ"
#   set the zh label to "玛尔塔·埃温斯达特·海格勒"
LAST	Lzh	"玛尔塔·埃温斯达特·海格勒"
#   add a ja alias "マルタ・エイヴィンスダッテル・スヴェインスヴォル"
LAST	Aja	"マルタ・エイヴィンスダッテル・スヴェインスヴォル"
#   add a zh alias "玛尔塔·埃温斯达特·斯韦伊恩斯沃尔"
LAST	Azh	"玛尔塔·埃温斯达特·斯韦伊恩斯沃尔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003491988061 Martha Eivindsdatter Heigre, qualified P1810 subject named as Martha Eivindsdatter Sveinsvoll
LAST	P2600	"6000000003491988061"	P1810	"Martha Eivindsdatter Sveinsvoll"
#   P569 date of birth = +1874-03-23T00:00:00Z/11
LAST	P569	+1874-03-23T00:00:00Z/11	S2600	"6000000003491988061"
#   P26 spouse = Q141178198 Enevald Jonasson Heigre
LAST	P26	Q141178198	S2600	"6000000003491988061"
#   Q141178198 Enevald Jonasson Heigre: P26 spouse = the item just created
Q141178198	P26	LAST	S2600	"6000000003491988061"
#   the item just created: add a mul alias "Martha Heigre"
LAST	Amul	"Martha Heigre"

# create a new item
CREATE
#   set the en label to "Marthe Gurie Osmundsdatter Ueland"
LAST	Len	"Marthe Gurie Osmundsdatter Ueland"
#   set the mul label to "Marthe Gurie Osmundsdatter Ueland"
LAST	Lmul	"Marthe Gurie Osmundsdatter Ueland"
#   set the ja label to "マルテ・グーリエ・オスムンドスダッテル・ウエランド"
LAST	Lja	"マルテ・グーリエ・オスムンドスダッテル・ウエランド"
#   set the zh label to "马尔特·古里·奥斯穆恩德斯达特·乌埃拉恩德"
LAST	Lzh	"马尔特·古里·奥斯穆恩德斯达特·乌埃拉恩德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000002954116461 Marthe Gurie Osmundsdatter Ueland, qualified P1810 subject named as Marthe Gurie Osmundsdatter Ueland
LAST	P2600	"6000000002954116461"	P1810	"Marthe Gurie Osmundsdatter Ueland"
#   P569 date of birth = +1805-06-09T00:00:00Z/11
LAST	P569	+1805-06-09T00:00:00Z/11	S2600	"6000000002954116461"
#   P570 date of death = +1847-12-16T00:00:00Z/11
LAST	P570	+1847-12-16T00:00:00Z/11	S2600	"6000000002954116461"
#   P40 child = Q141198414 Ingeborg Olsdatter Sandsmark
LAST	P40	Q141198414	S2600	"6000000002954116461"
#   Q141198414 Ingeborg Olsdatter Sandsmark: P25 mother = the item just created
Q141198414	P25	LAST	S2600	"6000000002954116461"
#   the item just created: P735 given name = Q1483687 Marthe, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q1483687	P1545	"1"	P7452	Q3409033
#   P734 family name = Q27889293 Ueland
LAST	P734	Q27889293

# create a new item
CREATE
#   set the en label to "Ola Person Persson Heigre"
LAST	Len	"Ola Person Persson Heigre"
#   set the mul label to "Ola Person Persson Heigre"
LAST	Lmul	"Ola Person Persson Heigre"
#   set the ja label to "オーラ・ペルソン・ペルソン・ヘイグレ"
LAST	Lja	"オーラ・ペルソン・ペルソン・ヘイグレ"
#   set the zh label to "乌拉·佩尔松·佩尔松·海格勒"
LAST	Lzh	"乌拉·佩尔松·佩尔松·海格勒"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003491947917 Ola Person Persson Heigre, qualified P1810 subject named as Ola Person Persson Heigre
LAST	P2600	"6000000003491947917"	P1810	"Ola Person Persson Heigre"
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
#   set the en label to "Olaug Jonsdatter Heigre"
LAST	Len	"Olaug Jonsdatter Heigre"
#   set the mul label to "Olaug Jonsdatter Heigre"
LAST	Lmul	"Olaug Jonsdatter Heigre"
#   add a mul alias "Olaug Jonsdatter Røyneberg"
LAST	Amul	"Olaug Jonsdatter Røyneberg"
#   set the ja label to "オラウグ・ヨンスダッテル・ヘイグレ"
LAST	Lja	"オラウグ・ヨンスダッテル・ヘイグレ"
#   set the zh label to "奥拉乌格·永斯达特·海格勒"
LAST	Lzh	"奥拉乌格·永斯达特·海格勒"
#   add a ja alias "オラウグ・ヨンスダッテル・ロイネベルグ"
LAST	Aja	"オラウグ・ヨンスダッテル・ロイネベルグ"
#   add a zh alias "奥拉乌格·永斯达特·罗伊内贝尔格"
LAST	Azh	"奥拉乌格·永斯达特·罗伊内贝尔格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003491933401 Olaug Jonsdatter Heigre, qualified P1810 subject named as Olaug Jonsdatter Røyneberg
LAST	P2600	"6000000003491933401"	P1810	"Olaug Jonsdatter Røyneberg"
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
#   set the en label to "Olufine Bergithe Ekman"
LAST	Len	"Olufine Bergithe Ekman"
#   set the mul label to "Olufine Bergithe Ekman"
LAST	Lmul	"Olufine Bergithe Ekman"
#   add a mul alias "Olufine Bergithe Jenssen"
LAST	Amul	"Olufine Bergithe Jenssen"
#   set the ja label to "オルフィネ・ベルギテ・エクマン"
LAST	Lja	"オルフィネ・ベルギテ・エクマン"
#   set the zh label to "奥卢菲内·贝尔吉特·埃克马恩"
LAST	Lzh	"奥卢菲内·贝尔吉特·埃克马恩"
#   add a ja alias "オルフィネ・ベルギテ・イェンセン"
LAST	Aja	"オルフィネ・ベルギテ・イェンセン"
#   add a zh alias "奥卢菲内·贝尔吉特·耶恩森"
LAST	Azh	"奥卢菲内·贝尔吉特·耶恩森"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000014196479728 Olufine Bergithe Ekman, qualified P1810 subject named as Olufine Bergithe Jenssen
LAST	P2600	"6000000014196479728"	P1810	"Olufine Bergithe Jenssen"
#   P569 date of birth = +1873-01-26T00:00:00Z/11
LAST	P569	+1873-01-26T00:00:00Z/11	S2600	"6000000014196479728"
#   P570 date of death = +1943-01-28T00:00:00Z/11
LAST	P570	+1943-01-28T00:00:00Z/11	S2600	"6000000014196479728"
#   P40 child = Q141205908 Gotfred Olai Ekman
LAST	P40	Q141205908	S2600	"6000000014196479728"
#   Q141205908 Gotfred Olai Ekman: P25 mother = the item just created
Q141205908	P25	LAST	S2600	"6000000014196479728"

# create a new item
CREATE
#   the item just created: set the en label to "Per Gustaf Ekman"
LAST	Len	"Per Gustaf Ekman"
#   set the mul label to "Per Gustaf Ekman"
LAST	Lmul	"Per Gustaf Ekman"
#   set the ja label to "ペル・グスタフ・エクマン"
LAST	Lja	"ペル・グスタフ・エクマン"
#   set the zh label to "佩尔·古斯塔夫·埃克马恩"
LAST	Lzh	"佩尔·古斯塔夫·埃克马恩"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000032811550619 Per Gustaf Ekman, qualified P1810 subject named as Per Gustaf Ekman
LAST	P2600	"6000000032811550619"	P1810	"Per Gustaf Ekman"
#   P569 date of birth = +1861-02-26T00:00:00Z/11
LAST	P569	+1861-02-26T00:00:00Z/11	S2600	"6000000032811550619"
#   P570 date of death = +1936-12-11T00:00:00Z/11
LAST	P570	+1936-12-11T00:00:00Z/11	S2600	"6000000032811550619"
#   P40 child = Q141205908 Gotfred Olai Ekman
LAST	P40	Q141205908	S2600	"6000000032811550619"
#   Q141205908 Gotfred Olai Ekman: P22 father = the item just created
Q141205908	P22	LAST	S2600	"6000000032811550619"
#   the item just created: P735 given name = Q13582800 Per, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q13582800	P1545	"1"	P7452	Q3409033
#   P735 given name = Q15646212 Gustaf, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q15646212	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the mul label to "NN"
LAST	Lmul	"NN"
#   set the ca label to "fill de Sigurd Sverre Ravn Talle"
LAST	Lca	"fill de Sigurd Sverre Ravn Talle"
#   set the da label to "søn af Sigurd Sverre Ravn Talle"
LAST	Lda	"søn af Sigurd Sverre Ravn Talle"
#   set the de label to "Sohn von Sigurd Sverre Ravn Talle"
LAST	Lde	"Sohn von Sigurd Sverre Ravn Talle"
#   set the en label to "son of Sigurd Sverre Ravn Talle"
LAST	Len	"son of Sigurd Sverre Ravn Talle"
#   set the es label to "hijo de Sigurd Sverre Ravn Talle"
LAST	Les	"hijo de Sigurd Sverre Ravn Talle"
#   set the it label to "figlio di Sigurd Sverre Ravn Talle"
LAST	Lit	"figlio di Sigurd Sverre Ravn Talle"
#   set the ja label to "シグルド・スヴェレ・ラヴン・タッレの息子"
LAST	Lja	"シグルド・スヴェレ・ラヴン・タッレの息子"
#   set the nb label to "sønn av Sigurd Sverre Ravn Talle"
LAST	Lnb	"sønn av Sigurd Sverre Ravn Talle"
#   set the nl label to "zoon van Sigurd Sverre Ravn Talle"
LAST	Lnl	"zoon van Sigurd Sverre Ravn Talle"
#   set the pt label to "filho de Sigurd Sverre Ravn Talle"
LAST	Lpt	"filho de Sigurd Sverre Ravn Talle"
#   set the sv label to "son till Sigurd Sverre Ravn Talle"
LAST	Lsv	"son till Sigurd Sverre Ravn Talle"
#   set the zh label to "西古尔德·斯韦雷·拉夫恩·塔勒之子"
LAST	Lzh	"西古尔德·斯韦雷·拉夫恩·塔勒之子"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000177688399821 NN Private, qualified P1810 subject named as Private
LAST	P2600	"6000000177688399821"	P1810	"Private"
#   P22 father = Q141216404 Sigurd Sverre Ravn Talle
LAST	P22	Q141216404	S2600	"6000000177688399821"
#   P25 mother = Q141168830 Ingeborg Talle
LAST	P25	Q141168830	S2600	"6000000177688399821"
#   Q141216404 Sigurd Sverre Ravn Talle: P40 child = the item just created
Q141216404	P40	LAST	S2600	"6000000177688399821"
#   Q141168830 Ingeborg Talle: P40 child = the item just created
Q141168830	P40	LAST	S2600	"6000000177688399821"

# create a new item
CREATE
#   the item just created: set the en label to "Ragna Enevaldsdatter Heigre"
LAST	Len	"Ragna Enevaldsdatter Heigre"
#   set the mul label to "Ragna Enevaldsdatter Heigre"
LAST	Lmul	"Ragna Enevaldsdatter Heigre"
#   set the ja label to "ラグナ・エネヴァルドスダッテル・ヘイグレ"
LAST	Lja	"ラグナ・エネヴァルドスダッテル・ヘイグレ"
#   set the zh label to "拉格纳·埃内瓦尔德斯达特·海格勒"
LAST	Lzh	"拉格纳·埃内瓦尔德斯达特·海格勒"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003491988081 Ragna Enevaldsdatter Heigre, qualified P1810 subject named as Ragna Enevaldsdatter Heigre
LAST	P2600	"6000000003491988081"	P1810	"Ragna Enevaldsdatter Heigre"
#   P569 date of birth = +1907-01-30T00:00:00Z/11
LAST	P569	+1907-01-30T00:00:00Z/11	S2600	"6000000003491988081"
#   P570 date of death = +1991-10-26T00:00:00Z/11
LAST	P570	+1991-10-26T00:00:00Z/11	S2600	"6000000003491988081"
#   P22 father = Q141178198 Enevald Jonasson Heigre
LAST	P22	Q141178198	S2600	"6000000003491988081"
#   Q141178198 Enevald Jonasson Heigre: P40 child = the item just created
Q141178198	P40	LAST	S2600	"6000000003491988081"
#   the item just created: P735 given name = Q578453 Ragna
LAST	P735	Q578453

# create a new item
CREATE
#   set the en label to "Rasmus Asbjørnson Nedre Rossavik"
LAST	Len	"Rasmus Asbjørnson Nedre Rossavik"
#   set the mul label to "Rasmus Asbjørnson Nedre Rossavik"
LAST	Lmul	"Rasmus Asbjørnson Nedre Rossavik"
#   add a mul alias "Rasmus Asbjørnson Frafjord"
LAST	Amul	"Rasmus Asbjørnson Frafjord"
#   set the ja label to "ラスムス・アスブヨルンソン・ネドレ・ロサヴィク"
LAST	Lja	"ラスムス・アスブヨルンソン・ネドレ・ロサヴィク"
#   set the zh label to "拉斯穆斯·阿斯布永尔恩松·内德雷·罗萨维克"
LAST	Lzh	"拉斯穆斯·阿斯布永尔恩松·内德雷·罗萨维克"
#   add a ja alias "ラスムス・アスブヨルンソン・フラフヨルド"
LAST	Aja	"ラスムス・アスブヨルンソン・フラフヨルド"
#   add a zh alias "拉斯穆斯·阿斯布永尔恩松·夫拉夫永尔德"
LAST	Azh	"拉斯穆斯·阿斯布永尔恩松·夫拉夫永尔德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003192698959 Rasmus Asbjørnson Nedre Rossavik, qualified P1810 subject named as Rasmus Asbjørnson Frafjord
LAST	P2600	"6000000003192698959"	P1810	"Rasmus Asbjørnson Frafjord"
#   P569 date of birth = +1671-00-00T00:00:00Z/9
LAST	P569	+1671-00-00T00:00:00Z/9	S2600	"6000000003192698959"
#   P570 date of death = +1732-08-31T00:00:00Z/11
LAST	P570	+1732-08-31T00:00:00Z/11	S2600	"6000000003192698959"
#   P26 spouse = Q141205898 Anna Tormodsdatter Mele
LAST	P26	Q141205898	S2600	"6000000003192698959"
#   Q141205898 Anna Tormodsdatter Mele: P26 spouse = the item just created
Q141205898	P26	LAST	S2600	"6000000003192698959"
#   the item just created: P735 given name = Q1785744 Rasmus
LAST	P735	Q1785744
#   P734 family name = Q38902733 Frafjord, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q38902733	P3831	Q2507958
#   add a mul alias "Rasmus Nedre Rossavik"
LAST	Amul	"Rasmus Nedre Rossavik"

# create a new item
CREATE
#   set the en label to "Reiar Reiersen Kydland"
LAST	Len	"Reiar Reiersen Kydland"
#   set the mul label to "Reiar Reiersen Kydland"
LAST	Lmul	"Reiar Reiersen Kydland"
#   set the ja label to "レイアル・レイエルセン・キドランド"
LAST	Lja	"レイアル・レイエルセン・キドランド"
#   set the zh label to "雷伊阿尔·雷伊埃尔森·基德拉恩德"
LAST	Lzh	"雷伊阿尔·雷伊埃尔森·基德拉恩德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005609534659 Reiar Reiersen Kydland, qualified P1810 subject named as Reiar Reiersen Kydland
LAST	P2600	"6000000005609534659"	P1810	"Reiar Reiersen Kydland"
#   P569 date of birth = +1726-00-00T00:00:00Z/9
LAST	P569	+1726-00-00T00:00:00Z/9	S2600	"6000000005609534659"
#   P570 date of death = +1792-00-00T00:00:00Z/9
LAST	P570	+1792-00-00T00:00:00Z/9	S2600	"6000000005609534659"
#   P40 child = Q141198370 NN Skårland
LAST	P40	Q141198370	S2600	"6000000005609534659"
#   Q141198370 NN Skårland: P22 father = the item just created
Q141198370	P22	LAST	S2600	"6000000005609534659"

# create a new item
CREATE
#   the item just created: set the en label to "Tollef Mattiasson Fotland"
LAST	Len	"Tollef Mattiasson Fotland"
#   set the mul label to "Tollef Mattiasson Fotland"
LAST	Lmul	"Tollef Mattiasson Fotland"
#   set the ja label to "トッレヴ・マティアソン・フォトランド"
LAST	Lja	"トッレヴ・マティアソン・フォトランド"
#   set the zh label to "托勒夫·马蒂阿松·福特拉恩德"
LAST	Lzh	"托勒夫·马蒂阿松·福特拉恩德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000007974939920 Tollef Mattiasson Fotland, qualified P1810 subject named as Tollef Mattiasson Fotland
LAST	P2600	"6000000007974939920"	P1810	"Tollef Mattiasson Fotland"
#   P569 date of birth = +1728-00-00T00:00:00Z/9
LAST	P569	+1728-00-00T00:00:00Z/9	S2600	"6000000007974939920"
#   P570 date of death = +1797-06-01T00:00:00Z/11
LAST	P570	+1797-06-01T00:00:00Z/11	S2600	"6000000007974939920"
#   P26 spouse = Q141216492 Marta Eriksdatter Fotland
LAST	P26	Q141216492	S2600	"6000000007974939920"
#   P40 child = Q141205904 Erik Tollefson Foss-Eikeland
LAST	P40	Q141205904	S2600	"6000000007974939920"
#   Q141216492 Marta Eriksdatter Fotland: P26 spouse = the item just created
Q141216492	P26	LAST	S2600	"6000000007974939920"
#   Q141205904 Erik Tollefson Foss-Eikeland: P22 father = the item just created
Q141205904	P22	LAST	S2600	"6000000007974939920"
#   the item just created: P735 given name = Q12006598 Tollef
LAST	P735	Q12006598
#   P734 family name = Q29726874 Fotland
LAST	P734	Q29726874

# create a new item
CREATE
#   set the en label to "Tore Toresson Talgje"
LAST	Len	"Tore Toresson Talgje"
#   set the mul label to "Tore Toresson Talgje"
LAST	Lmul	"Tore Toresson Talgje"
#   set the ja label to "トレ・トレソン・タルイェ"
LAST	Lja	"トレ・トレソン・タルイェ"
#   set the zh label to "托雷·托雷松·塔尔耶"
LAST	Lzh	"托雷·托雷松·塔尔耶"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000002452584590 Tore Toresson Talgje, qualified P1810 subject named as Tore Toresson Talgje
LAST	P2600	"6000000002452584590"	P1810	"Tore Toresson Talgje"
#   P569 date of birth = +1515-00-00T00:00:00Z/9
LAST	P569	+1515-00-00T00:00:00Z/9	S2600	"6000000002452584590"
#   P570 date of death = +1578-00-00T00:00:00Z/9
LAST	P570	+1578-00-00T00:00:00Z/9	S2600	"6000000002452584590"
#   P25 mother = Q141206060 Cecilie Mortensdatter
LAST	P25	Q141206060	S2600	"6000000002452584590"
#   P40 child = Q141205929 Ola Toreson Randa
LAST	P40	Q141205929	S2600	"6000000002452584590"
#   Q141206060 Cecilie Mortensdatter: P40 child = the item just created
Q141206060	P40	LAST	S2600	"6000000002452584590"
#   Q141205929 Ola Toreson Randa: P22 father = the item just created
Q141205929	P22	LAST	S2600	"6000000002452584590"
#   the item just created: P735 given name = Q1548096 Tore
LAST	P735	Q1548096
#   add a mul alias "Tore Talgje"
LAST	Amul	"Tore Talgje"

# create a new item
CREATE
#   set the en label to "Torger Torgerson Stokka"
LAST	Len	"Torger Torgerson Stokka"
#   set the mul label to "Torger Torgerson Stokka"
LAST	Lmul	"Torger Torgerson Stokka"
#   add a mul alias "Torger Torgerson Skorve"
LAST	Amul	"Torger Torgerson Skorve"
#   set the ja label to "トルゲル・トルゲルソン・ストカ"
LAST	Lja	"トルゲル・トルゲルソン・ストカ"
#   set the zh label to "托尔盖尔·托尔盖尔松·斯托卡"
LAST	Lzh	"托尔盖尔·托尔盖尔松·斯托卡"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000002726968193 Torger Torgerson Stokka, qualified P1810 subject named as Torger Torgerson Skorve
LAST	P2600	"6000000002726968193"	P1810	"Torger Torgerson Skorve"
#   P569 date of birth = +1801-00-00T00:00:00Z/9
LAST	P569	+1801-00-00T00:00:00Z/9	S2600	"6000000002726968193"
#   P570 date of death = +1880-11-18T00:00:00Z/11
LAST	P570	+1880-11-18T00:00:00Z/11	S2600	"6000000002726968193"
#   P40 child = Q141216510 Torger Torgerson Stokka
LAST	P40	Q141216510	S2600	"6000000002726968193"
#   Q141216510 Torger Torgerson Stokka: P22 father = the item just created
Q141216510	P22	LAST	S2600	"6000000002726968193"
#   the item just created: P735 given name = Q2444019 Torger
LAST	P735	Q2444019
#   add a mul alias "Torger Stokka"
LAST	Amul	"Torger Stokka"
#   Q141216455 Anders Persson: P40 child = Q141216461 Daniel Andersson
Q141216455	P40	Q141216461	S2600	"375734886370012680"
#   Q141216349 Ingrid Guttormsdotter: P26 spouse = Q10511224 Guttorm Ostmannson of Jämtland & Svealand
Q141216349	P26	Q10511224	S2600	"6000000000771986019"
#   Q141216496 Nils Larsen Raunes: P22 father = Q141216488 Lars Jonsen Landsnes
Q141216496	P22	Q141216488	S2600	"6000000001770188397"
#   Q141216487 Knut Johanson Håland: P26 spouse = Q141216494 N.N. Jacobsdtr. Koll
Q141216487	P26	Q141216494	S2600	"6000000003376453205"
#   Q141216489 Laurits Leivson Bjørheim: P26 spouse = Q141216460 Bjørnsdatter Tau
Q141216489	P26	Q141216460	S2600	"6000000003422289517"
#   Q141216488 Lars Jonsen Landsnes: P40 child = Q141216496 Nils Larsen Raunes
Q141216488	P40	Q141216496	S2600	"6000000005607123730"
#   Q141216460 Bjørnsdatter Tau: P26 spouse = Q141216489 Laurits Leivson Bjørheim
Q141216460	P26	Q141216489	S2600	"6000000005607353362"
#   Q141216483 Karen Malena Rasmusdatter Tjelta: P26 spouse = Q141216470 Govert Jonson Årsvoll
Q141216483	P26	Q141216470	S2600	"6000000008173986703"
#   Q141216470 Govert Jonson Årsvoll: P26 spouse = Q141216483 Karen Malena Rasmusdatter Tjelta
Q141216470	P26	Q141216483	S2600	"6000000008174080446"
#   Q141216498 Norman Charles Tunheim: P25 mother = Q141216454 Alice Lillian Tunheim Nelson
Q141216498	P25	Q141216454	S2600	"6000000009736181790"
#   Q141216490 Malli Svensdatter Lura: P26 spouse = Q141216481 Jon Tørresson Soma
Q141216490	P26	Q141216481	S2600	"6000000014277480039"
#   Q141216481 Jon Tørresson Soma: P26 spouse = Q141216490 Malli Svensdatter Lura
Q141216481	P26	Q141216490	S2600	"6000000014277496029"
#   Q141216461 Daniel Andersson: P22 father = Q141216455 Anders Persson
Q141216461	P22	Q141216455	S2600	"6000000018528235866"
#   Q141216494 N.N. Jacobsdtr. Koll: P26 spouse = Q141216487 Knut Johanson Håland
Q141216494	P26	Q141216487	S2600	"6000000030876120040"
#   Q141216454 Alice Lillian Tunheim Nelson: P40 child = Q141216498 Norman Charles Tunheim
Q141216454	P40	Q141216498	S2600	"6000000039510815149"
#   Q141216458 Asbjørn Gunnarson Bø: P26 spouse = Q141216456 Anna Helgesdotter Opstad
Q141216458	P26	Q141216456	S2600	"6000000042211257078"
#   Q141216456 Anna Helgesdotter Opstad: P26 spouse = Q141216458 Asbjørn Gunnarson Bø
Q141216456	P26	Q141216458	S2600	"6000000042211257124"
#   Q141216500 NN Private: P25 mother = Q141216493 Minnie Ronneberg
Q141216500	P25	Q141216493	S2600	"6000000117728698004"
#   Q141216493 Minnie Ronneberg: P40 child = Q141216500 NN Private
Q141216493	P40	Q141216500	S2600	"6000000117729569834"

