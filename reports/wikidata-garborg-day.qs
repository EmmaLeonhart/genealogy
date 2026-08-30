# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   774 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   set the zh label to "马里特·奥尔姆斯德·比雷"
Q141205922	Lzh	"马里特·奥尔姆斯德·比雷"
#   Q141216499 Orm Ånonsen: set the zh label to "奥尔姆·奥农森"
Q141216499	Lzh	"奥尔姆·奥农森"
#   Q6145888 Göran Ludvig von Köhler: set the ja label to "ゲオルク・ルズヴィ・ヴォン・ケーラー"
Q6145888	Lja	"ゲオルク・ルズヴィ・ヴォン・ケーラー"
#   set the zh label to "格奥尔格·卢德维格·翁·科莱尔"
Q6145888	Lzh	"格奥尔格·卢德维格·翁·科莱尔"
#   Q19721217 Salomon Christoffer von Köhler: set the ja label to "サロモン・ヴォン・ケーラー"
Q19721217	Lja	"サロモン・ヴォン・ケーラー"
#   set the zh label to "萨洛蒙·翁·科莱尔"
Q19721217	Lzh	"萨洛蒙·翁·科莱尔"
#   Q141199899 Jon Tollakson Aukland, IV: set the ja label to "ジョン・トラクソン・アウクランド・イヴ"
Q141199899	Lja	"ジョン・トラクソン・アウクランド・イヴ"
#   set the zh label to "乔恩·托拉克松·奥克兰德·伊夫"
Q141199899	Lzh	"乔恩·托拉克松·奥克兰德·伊夫"
#   Q141216648 Tore Toresson Talgje: set the ja label to "トーレ・トレソン・タルイェ"
Q141216648	Lja	"トーレ・トレソン・タルイェ"
#   Q141199891 Ivar Valheim: set the ja label to "イヴァル・ヴァルヘイム"
Q141199891	Lja	"イヴァル・ヴァルヘイム"
#   set the zh label to "伊瓦尔·瓦尔赫伊姆"
Q141199891	Lzh	"伊瓦尔·瓦尔赫伊姆"
#   set the ja label to "グンンブヨルン・トレソン・テングス"
Q141199851	Lja	"グンンブヨルン・トレソン・テングス"
#   set the zh label to "贡布约尔恩·托雷松·滕斯"
Q141199851	Lzh	"贡布约尔恩·托雷松·滕斯"
#   set the ja label to "セシリエ・オルスダッテル・ホーランド"
Q141206061	Lja	"セシリエ・オルスダッテル・ホーランド"
#   set the zh label to "塞西莉厄·奥尔斯达特·霍兰"
Q141206061	Lzh	"塞西莉厄·奥尔斯达特·霍兰"

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "3 barn?"
LAST	Len	"3 barn?"
#   set the mul label to "3 barn?"
LAST	Lmul	"3 barn?"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P2600 Geni.com profile ID = 6000000221895035823 3 barn?, qualified P1810 subject named as 3 barn?
LAST	P2600	"6000000221895035823"	P1810	"3 barn?"
#   P22 father = Q2478781 Adolf Fredrik Munck
LAST	P22	Q2478781	S2600	"6000000221895035823"
#   Q2478781 Adolf Fredrik Munck: P40 child = the item just created
Q2478781	P40	LAST	S2600	"6000000221895035823"

# create a new item
CREATE
#   the item just created: set the en label to "Alfhild Hulda Erfurt"
LAST	Len	"Alfhild Hulda Erfurt"
#   set the mul label to "Alfhild Hulda Erfurt"
LAST	Lmul	"Alfhild Hulda Erfurt"
#   add a mul alias "Alfhild Hulda Frenning"
LAST	Amul	"Alfhild Hulda Frenning"
#   set the ja label to "アルフヒルド・フルダ・エルフルト"
LAST	Lja	"アルフヒルド・フルダ・エルフルト"
#   set the zh label to "阿尔夫希尔德·胡尔达·埃尔富尔特"
LAST	Lzh	"阿尔夫希尔德·胡尔达·埃尔富尔特"
#   add a ja alias "アルフヒルド・フルダ・フレニング"
LAST	Aja	"アルフヒルド・フルダ・フレニング"
#   add a zh alias "阿尔夫希尔德·胡尔达·夫雷宁"
LAST	Azh	"阿尔夫希尔德·胡尔达·夫雷宁"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000021122365521 Alfhild Hulda Erfurt, qualified P1810 subject named as Alfhild Hulda Frenning
LAST	P2600	"6000000021122365521"	P1810	"Alfhild Hulda Frenning"
#   P569 date of birth = +1880-00-00T00:00:00Z/9
LAST	P569	+1880-00-00T00:00:00Z/9	S2600	"6000000021122365521"
#   P22 father = Q141219056 Christian Frenning
LAST	P22	Q141219056	S2600	"6000000021122365521"
#   P25 mother = Q141189083 Martha Elida Frenning
LAST	P25	Q141189083	S2600	"6000000021122365521"
#   Q141219056 Christian Frenning: P40 child = the item just created
Q141219056	P40	LAST	S2600	"6000000021122365521"
#   Q141189083 Martha Elida Frenning: P40 child = the item just created
Q141189083	P40	LAST	S2600	"6000000021122365521"
#   the item just created: P735 given name = Q2778125 Alfhild, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q2778125	P1545	"1"	P7452	Q3409033
#   P735 given name = Q857854 Hulda, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q857854	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Anna Charlotta Lovisa Augusta Hägerflycht"
LAST	Len	"Anna Charlotta Lovisa Augusta Hägerflycht"
#   set the mul label to "Anna Charlotta Lovisa Augusta Hägerflycht"
LAST	Lmul	"Anna Charlotta Lovisa Augusta Hägerflycht"
#   add a mul alias "Anna Charlotta Lovisa Augusta Törnbladh (Törnebladh)"
LAST	Amul	"Anna Charlotta Lovisa Augusta Törnbladh (Törnebladh)"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000006127131734 Anna Charlotta Lovisa Augusta Hägerflycht, qualified P1810 subject named as Anna Charlotta Lovisa Augusta Törnbladh (Törnebladh)
LAST	P2600	"6000000006127131734"	P1810	"Anna Charlotta Lovisa Augusta Törnbladh (Törnebladh)"
#   P569 date of birth = +1818-12-20T00:00:00Z/11
LAST	P569	+1818-12-20T00:00:00Z/11	S2600	"6000000006127131734"
#   P570 date of death = +1876-12-15T00:00:00Z/11
LAST	P570	+1876-12-15T00:00:00Z/11	S2600	"6000000006127131734"
#   P22 father = Q6218068 Carl Peter Peter Törnebladh
LAST	P22	Q6218068	S2600	"6000000006127131734"
#   Q6218068 Carl Peter Peter Törnebladh: P40 child = the item just created
Q6218068	P40	LAST	S2600	"6000000006127131734"
#   the item just created: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1067071	P1545	"2"	P3831	Q245025
#   P735 given name = Q10570000 Lovisa, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
LAST	P735	Q10570000	P1545	"3"	P3831	Q245025
#   P735 given name = Q1370330 Augusta, qualified P1545 series ordinal 4, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1370330	P1545	"4"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Anna Sofia Ramström"
LAST	Len	"Anna Sofia Ramström"
#   set the mul label to "Anna Sofia Ramström"
LAST	Lmul	"Anna Sofia Ramström"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000221894848830 Anna Sofia Ramström, qualified P1810 subject named as Anna Sofia Ramström
LAST	P2600	"6000000221894848830"	P1810	"Anna Sofia Ramström"
#   P569 date of birth = +1738-00-00T00:00:00Z/9
LAST	P569	+1738-00-00T00:00:00Z/9	S2600	"6000000221894848830"
#   P570 date of death = +1786-05-11T00:00:00Z/11
LAST	P570	+1786-05-11T00:00:00Z/11	S2600	"6000000221894848830"
#   P26 spouse = Q2478781 Adolf Fredrik Munck
LAST	P26	Q2478781	S2600	"6000000221894848830"
#   Q2478781 Adolf Fredrik Munck: P26 spouse = the item just created
Q2478781	P26	LAST	S2600	"6000000221894848830"
#   the item just created: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q18201520	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Brita Schytte"
LAST	Len	"Brita Schytte"
#   set the mul label to "Brita Schytte"
LAST	Lmul	"Brita Schytte"
#   set the ja label to "ブリッタ・シテ"
LAST	Lja	"ブリッタ・シテ"
#   set the zh label to "布里塔·西特"
LAST	Lzh	"布里塔·西特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000012901496092 Brita Schytte, qualified P1810 subject named as Brita Schytte
LAST	P2600	"6000000012901496092"	P1810	"Brita Schytte"
#   P569 date of birth = +1623-11-10T00:00:00Z/11
LAST	P569	+1623-11-10T00:00:00Z/11	S2600	"6000000012901496092"
#   P570 date of death = +1668-05-18T00:00:00Z/11
LAST	P570	+1668-05-18T00:00:00Z/11	S2600	"6000000012901496092"
#   P26 spouse = Q5568857 Daniel Jonsson Behmer
LAST	P26	Q5568857	S2600	"6000000012901496092"
#   P40 child = Q141223499 Anna Danielsdotter Behmer
LAST	P40	Q141223499	S2600	"6000000012901496092"
#   Q5568857 Daniel Jonsson Behmer: P26 spouse = the item just created
Q5568857	P26	LAST	S2600	"6000000012901496092"
#   Q141223499 Anna Danielsdotter Behmer: P25 mother = the item just created
Q141223499	P25	LAST	S2600	"6000000012901496092"
#   the item just created: P735 given name = Q918013
LAST	P735	Q918013
#   P734 family name = Q30132664 Schytte, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q30132664	P3831	Q28418670

# create a new item
CREATE
#   set the en label to "Guri Nordby"
LAST	Len	"Guri Nordby"
#   set the mul label to "Guri Nordby"
LAST	Lmul	"Guri Nordby"
#   add a mul alias "Guri Knutson"
LAST	Amul	"Guri Knutson"
#   set the ja label to "グリ・ノルドビ"
LAST	Lja	"グリ・ノルドビ"
#   set the zh label to "古里·诺尔德比"
LAST	Lzh	"古里·诺尔德比"
#   add a ja alias "グリ・クヌートソン"
LAST	Aja	"グリ・クヌートソン"
#   add a zh alias "古里·克努特松"
LAST	Azh	"古里·克努特松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000189963920888 Guri ( Julia) Nordby, qualified P1810 subject named as Guri ( Julia) Knutson
LAST	P2600	"6000000189963920888"	P1810	"Guri ( Julia) Knutson"
#   P569 date of birth = +1871-08-18T00:00:00Z/11
LAST	P569	+1871-08-18T00:00:00Z/11	S2600	"6000000189963920888"
#   P570 date of death = +1944-00-00T00:00:00Z/9
LAST	P570	+1944-00-00T00:00:00Z/9	S2600	"6000000189963920888"
#   P40 child = Q141219064 Lloyd Obert Dokken
LAST	P40	Q141219064	S2600	"6000000189963920888"
#   Q141219064 Lloyd Obert Dokken: P25 mother = the item just created
Q141219064	P25	LAST	S2600	"6000000189963920888"
#   the item just created: P735 given name = Q11973376 Guri
LAST	P735	Q11973376
#   P734 family name = Q30229827, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q30229827	P3831	Q28418670
#   add a mul alias "Julia Nordby"
LAST	Amul	"Julia Nordby"
#   add a mul alias "Julia Knutson Nordby"
LAST	Amul	"Julia Knutson Nordby"

# create a new item
CREATE
#   set the en label to "Hans Bertil Frisk"
LAST	Len	"Hans Bertil Frisk"
#   set the mul label to "Hans Bertil Frisk"
LAST	Lmul	"Hans Bertil Frisk"
#   set the ja label to "ハンス・ベルティル・フリスク"
LAST	Lja	"ハンス・ベルティル・フリスク"
#   set the zh label to "汉斯·贝蒂尔·弗里斯克"
LAST	Lzh	"汉斯·贝蒂尔·弗里斯克"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000177921459066 Hans Bertil Frisk, qualified P1810 subject named as Hans Bertil Frisk
LAST	P2600	"6000000177921459066"	P1810	"Hans Bertil Frisk"
#   P569 date of birth = +1930-08-26T00:00:00Z/11
LAST	P569	+1930-08-26T00:00:00Z/11	S2600	"6000000177921459066"
#   P570 date of death = +1991-05-00T00:00:00Z/10
LAST	P570	+1991-05-00T00:00:00Z/10	S2600	"6000000177921459066"
#   P25 mother = Q141223506 Beda Elvira Wedberg
LAST	P25	Q141223506	S2600	"6000000177921459066"
#   Q141223506 Beda Elvira Wedberg: P40 child = the item just created
Q141223506	P40	LAST	S2600	"6000000177921459066"

# create a new item
CREATE
#   the item just created: set the en label to "Helge Olsen Ytre Lima"
LAST	Len	"Helge Olsen Ytre Lima"
#   set the mul label to "Helge Olsen Ytre Lima"
LAST	Lmul	"Helge Olsen Ytre Lima"
#   set the ja label to "ヘルゲ・オルセン・イトレ・リマ"
LAST	Lja	"ヘルゲ・オルセン・イトレ・リマ"
#   set the zh label to "黑尔格·奥尔森·伊特雷·利马"
LAST	Lzh	"黑尔格·奥尔森·伊特雷·利马"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005607599821 Helge Olsen Ytre Lima, qualified P1810 subject named as Helge Olsen Ytre Lima
LAST	P2600	"6000000005607599821"	P1810	"Helge Olsen Ytre Lima"
#   P569 date of birth = +1768-00-00T00:00:00Z/9
LAST	P569	+1768-00-00T00:00:00Z/9	S2600	"6000000005607599821"
#   P570 date of death = +1852-00-00T00:00:00Z/9
LAST	P570	+1852-00-00T00:00:00Z/9	S2600	"6000000005607599821"
#   P26 spouse = Q141219250 Inger Sørensdatter Lima
LAST	P26	Q141219250	S2600	"6000000005607599821"
#   Q141219250 Inger Sørensdatter Lima: P26 spouse = the item just created
Q141219250	P26	LAST	S2600	"6000000005607599821"

# create a new item
CREATE
#   the item just created: set the en label to "Johan Jonson Haland"
LAST	Len	"Johan Jonson Haland"
#   set the mul label to "Johan Jonson Haland"
LAST	Lmul	"Johan Jonson Haland"
#   set the ja label to "ヨハン・ヨンソン・ハランド"
LAST	Lja	"ヨハン・ヨンソン・ハランド"
#   set the zh label to "约翰·永松·哈兰德"
LAST	Lzh	"约翰·永松·哈兰德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000063300979653 Johan Jonson Haland, qualified P1810 subject named as Johan Jonson Haland
LAST	P2600	"6000000063300979653"	P1810	"Johan Jonson Haland"
#   P569 date of birth = +1478-00-00T00:00:00Z/9
LAST	P569	+1478-00-00T00:00:00Z/9	S2600	"6000000063300979653"
#   P570 date of death = +1540-00-00T00:00:00Z/9
LAST	P570	+1540-00-00T00:00:00Z/9	S2600	"6000000063300979653"
#   P40 child = Q141216487 Knut Johanson Håland
LAST	P40	Q141216487	S2600	"6000000063300979653"
#   Q141216487 Knut Johanson Håland: P22 father = the item just created
Q141216487	P22	LAST	S2600	"6000000063300979653"
#   the item just created: P735 given name = Q10989273 Johan
LAST	P735	Q10989273
#   add a mul alias "Johan Haland"
LAST	Amul	"Johan Haland"

# create a new item
CREATE
#   set the en label to "Johanna Henrietta Turesdotter Ribbing af Koberg"
LAST	Len	"Johanna Henrietta Turesdotter Ribbing af Koberg"
#   set the mul label to "Johanna Henrietta Turesdotter Ribbing af Koberg"
LAST	Lmul	"Johanna Henrietta Turesdotter Ribbing af Koberg"
#   set the ja label to "ヨハンナ・ヘンリエッタ・トレスドッテル・リビング・アフ・コベルグ"
LAST	Lja	"ヨハンナ・ヘンリエッタ・トレスドッテル・リビング・アフ・コベルグ"
#   set the zh label to "约翰娜·亨里埃塔·图雷斯多特·里宾·阿夫·科贝尔格"
LAST	Lzh	"约翰娜·亨里埃塔·图雷斯多特·里宾·阿夫·科贝尔格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000015119258311 Johanna Henrietta Turesdotter Ribbing af Koberg, qualified P1810 subject named as Johanna Henrietta Turesdotter Ribbing af Koberg
LAST	P2600	"6000000015119258311"	P1810	"Johanna Henrietta Turesdotter Ribbing af Koberg"
#   P569 date of birth = +1778-11-26T00:00:00Z/11
LAST	P569	+1778-11-26T00:00:00Z/11	S2600	"6000000015119258311"
#   P570 date of death = +1845-01-25T00:00:00Z/11
LAST	P570	+1845-01-25T00:00:00Z/11	S2600	"6000000015119258311"
#   P26 spouse = Q6079124 Axel Pontus von Rosen
LAST	P26	Q6079124	S2600	"6000000015119258311"
#   Q6079124 Axel Pontus von Rosen: P26 spouse = the item just created
Q6079124	P26	LAST	S2600	"6000000015119258311"
#   the item just created: P735 given name = Q4120836 Johanna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q4120836	P1545	"1"	P7452	Q3409033
#   P735 given name = Q783677 Henrietta, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q783677	P1545	"2"	P3831	Q245025
#   P734 family name = Q37134374 Ribbing
LAST	P734	Q37134374

# create a new item
CREATE
#   set the en label to "John Otterson Dokken"
LAST	Len	"John Otterson Dokken"
#   set the mul label to "John Otterson Dokken"
LAST	Lmul	"John Otterson Dokken"
#   set the ja label to "ジョン・オテルソン・ドケン"
LAST	Lja	"ジョン・オテルソン・ドケン"
#   set the zh label to "约翰·奥特尔松·多肯"
LAST	Lzh	"约翰·奥特尔松·多肯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000189964294868 John Otterson Dokken, qualified P1810 subject named as John Otterson Dokken
LAST	P2600	"6000000189964294868"	P1810	"John Otterson Dokken"
#   P569 date of birth = +1855-04-00T00:00:00Z/10
LAST	P569	+1855-04-00T00:00:00Z/10	S2600	"6000000189964294868"
#   P570 date of death = +1917-07-10T00:00:00Z/11
LAST	P570	+1917-07-10T00:00:00Z/11	S2600	"6000000189964294868"
#   P40 child = Q141219064 Lloyd Obert Dokken
LAST	P40	Q141219064	S2600	"6000000189964294868"
#   Q141219064 Lloyd Obert Dokken: P22 father = the item just created
Q141219064	P22	LAST	S2600	"6000000189964294868"
#   the item just created: P735 given name = Q4925477 John
LAST	P735	Q4925477
#   add a mul alias "John Dokken"
LAST	Amul	"John Dokken"

# create a new item
CREATE
#   set the en label to "Karl Emil Frisk"
LAST	Len	"Karl Emil Frisk"
#   set the mul label to "Karl Emil Frisk"
LAST	Lmul	"Karl Emil Frisk"
#   set the ja label to "カール・エミール・フリスク"
LAST	Lja	"カール・エミール・フリスク"
#   set the zh label to "卡尔·埃米尔·弗里斯克"
LAST	Lzh	"卡尔·埃米尔·弗里斯克"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000177921458827 Karl Emil Frisk, qualified P1810 subject named as Karl Emil Frisk
LAST	P2600	"6000000177921458827"	P1810	"Karl Emil Frisk"
#   P569 date of birth = +1902-01-28T00:00:00Z/11
LAST	P569	+1902-01-28T00:00:00Z/11	S2600	"6000000177921458827"
#   P570 date of death = +1983-11-04T00:00:00Z/11
LAST	P570	+1983-11-04T00:00:00Z/11	S2600	"6000000177921458827"
#   P26 spouse = Q141223506 Beda Elvira Wedberg
LAST	P26	Q141223506	S2600	"6000000177921458827"
#   Q141223506 Beda Elvira Wedberg: P26 spouse = the item just created
Q141223506	P26	LAST	S2600	"6000000177921458827"

# create a new item
CREATE
#   the item just created: set the en label to "Kirsti Olsdatter Bærheim"
LAST	Len	"Kirsti Olsdatter Bærheim"
#   set the mul label to "Kirsti Olsdatter Bærheim"
LAST	Lmul	"Kirsti Olsdatter Bærheim"
#   set the ja label to "キルスティ・オルスダッテル・ベルヘイム"
LAST	Lja	"キルスティ・オルスダッテル・ベルヘイム"
#   set the zh label to "基尔斯蒂·奥尔斯达特·贝尔赫伊姆"
LAST	Lzh	"基尔斯蒂·奥尔斯达特·贝尔赫伊姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003492083933 Kirsti Olsdatter Bærheim, qualified P1810 subject named as Kirsti Olsdatter Bærheim
LAST	P2600	"6000000003492083933"	P1810	"Kirsti Olsdatter Bærheim"
#   P569 date of birth = +1684-00-00T00:00:00Z/9
LAST	P569	+1684-00-00T00:00:00Z/9	S2600	"6000000003492083933"
#   P570 date of death = +1748-00-00T00:00:00Z/9
LAST	P570	+1748-00-00T00:00:00Z/9	S2600	"6000000003492083933"
#   P40 child = Q141219052 Anna Olsdatter Heigre
LAST	P40	Q141219052	S2600	"6000000003492083933"
#   Q141219052 Anna Olsdatter Heigre: P25 mother = the item just created
Q141219052	P25	LAST	S2600	"6000000003492083933"
#   the item just created: P735 given name = Q4349920 Kirsti
LAST	P735	Q4349920
#   P5056 patronym or matronym = Q51885688 Olsdatter
LAST	P5056	Q51885688
#   P734 family name = Q40246530 Bærheim, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q40246530	P3831	Q28418670
#   add a mul alias "Kirsti Bærheim"
LAST	Amul	"Kirsti Bærheim"

# create a new item
CREATE
#   set the en label to "Malena Henriksdatter Lauvsnes"
LAST	Len	"Malena Henriksdatter Lauvsnes"
#   set the mul label to "Malena Henriksdatter Lauvsnes"
LAST	Lmul	"Malena Henriksdatter Lauvsnes"
#   add a mul alias "Malena Henriksdatter Steinnes"
LAST	Amul	"Malena Henriksdatter Steinnes"
#   set the ja label to "マレーナ・ヘンリクスダッテル・ラウヴスネス"
LAST	Lja	"マレーナ・ヘンリクスダッテル・ラウヴスネス"
#   set the zh label to "马莱纳·亨里克斯达特·拉乌夫斯内斯"
LAST	Lzh	"马莱纳·亨里克斯达特·拉乌夫斯内斯"
#   add a ja alias "マレーナ・ヘンリクスダッテル・ステイネス"
LAST	Aja	"マレーナ・ヘンリクスダッテル・ステイネス"
#   add a zh alias "马莱纳·亨里克斯达特·斯特伊内斯"
LAST	Azh	"马莱纳·亨里克斯达特·斯特伊内斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000008686123375 Malena Henriksdatter Lauvsnes, qualified P1810 subject named as Malena Henriksdatter Steinnes
LAST	P2600	"6000000008686123375"	P1810	"Malena Henriksdatter Steinnes"
#   P569 date of birth = +1645-00-00T00:00:00Z/9
LAST	P569	+1645-00-00T00:00:00Z/9	S2600	"6000000008686123375"
#   P40 child = Q141198371 Anna Belestdatter Lauvsnes
LAST	P40	Q141198371	S2600	"6000000008686123375"
#   Q141198371 Anna Belestdatter Lauvsnes: P25 mother = the item just created
Q141198371	P25	LAST	S2600	"6000000008686123375"
#   the item just created: P735 given name = Q5990536 Malena
LAST	P735	Q5990536
#   P734 family name = Q27892767 Steinnes, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q27892767	P3831	Q2507958
#   add a mul alias "Malena Lauvsnes"
LAST	Amul	"Malena Lauvsnes"

# create a new item
CREATE
#   set the en label to "Maren Ellingsdatter Tunheim"
LAST	Len	"Maren Ellingsdatter Tunheim"
#   set the mul label to "Maren Ellingsdatter Tunheim"
LAST	Lmul	"Maren Ellingsdatter Tunheim"
#   set the ja label to "マレン・エリングスダッテル・トゥンヘイム"
LAST	Lja	"マレン・エリングスダッテル・トゥンヘイム"
#   set the zh label to "马伦·埃林斯达特·通海姆"
LAST	Lzh	"马伦·埃林斯达特·通海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 340026788150007985 Maren Ellingsdatter Tunheim, qualified P1810 subject named as Maren Ellingsdatter Tunheim
LAST	P2600	"340026788150007985"	P1810	"Maren Ellingsdatter Tunheim"
#   P569 date of birth = +1653-00-00T00:00:00Z/9
LAST	P569	+1653-00-00T00:00:00Z/9	S2600	"340026788150007985"
#   P570 date of death = +1689-00-00T00:00:00Z/9
LAST	P570	+1689-00-00T00:00:00Z/9	S2600	"340026788150007985"
#   P40 child = Q141205914 Inger (Ingrid) Osmundsdatter Risa
LAST	P40	Q141205914	S2600	"340026788150007985"
#   Q141205914 Inger (Ingrid) Osmundsdatter Risa: P25 mother = the item just created
Q141205914	P25	LAST	S2600	"340026788150007985"
#   the item just created: P735 given name = Q1666203 Maren
LAST	P735	Q1666203
#   P734 family name = Q36927172
LAST	P734	Q36927172

# create a new item
CREATE
#   set the en label to "Marta Fanuelsdotter Madland"
LAST	Len	"Marta Fanuelsdotter Madland"
#   set the mul label to "Marta Fanuelsdotter Madland"
LAST	Lmul	"Marta Fanuelsdotter Madland"
#   set the ja label to "マルタ・ファヌエルスドッテル・マドランド"
LAST	Lja	"マルタ・ファヌエルスドッテル・マドランド"
#   set the zh label to "玛尔塔·法努埃尔斯多特·马德兰德"
LAST	Lzh	"玛尔塔·法努埃尔斯多特·马德兰德"
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
#   P734 family name = Q37124498
LAST	P734	Q37124498

# create a new item
CREATE
#   set the en label to "Ola Jonson Folkvår"
LAST	Len	"Ola Jonson Folkvår"
#   set the mul label to "Ola Jonson Folkvår"
LAST	Lmul	"Ola Jonson Folkvår"
#   set the ja label to "オーラ・ヨンソン・フォルクヴォール"
LAST	Lja	"オーラ・ヨンソン・フォルクヴォール"
#   set the zh label to "奥拉·永松·福尔克沃尔"
LAST	Lzh	"奥拉·永松·福尔克沃尔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003491988851 Ola Jonson Folkvår, qualified P1810 subject named as Ola Jonson Folkvår
LAST	P2600	"6000000003491988851"	P1810	"Ola Jonson Folkvår"
#   P569 date of birth = +1737-00-00T00:00:00Z/9
LAST	P569	+1737-00-00T00:00:00Z/9	S2600	"6000000003491988851"
#   P570 date of death = +1805-00-00T00:00:00Z/9
LAST	P570	+1805-00-00T00:00:00Z/9	S2600	"6000000003491988851"
#   P22 father = Q141206082 Jon Olson Raustad
LAST	P22	Q141206082	S2600	"6000000003491988851"
#   Q141206082 Jon Olson Raustad: P40 child = the item just created
Q141206082	P40	LAST	S2600	"6000000003491988851"

# create a new item
CREATE
#   the item just created: set the en label to "Osmund Andersen Tunheim"
LAST	Len	"Osmund Andersen Tunheim"
#   set the mul label to "Osmund Andersen Tunheim"
LAST	Lmul	"Osmund Andersen Tunheim"
#   set the ja label to "オスムンド・アンデルセン・トゥンヘイム"
LAST	Lja	"オスムンド・アンデルセン・トゥンヘイム"
#   set the zh label to "奥斯蒙德·安德森·通海姆"
LAST	Lzh	"奥斯蒙德·安德森·通海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000002763481707 Osmund Andersen Tunheim, qualified P1810 subject named as Osmund Andersen Tunheim
LAST	P2600	"6000000002763481707"	P1810	"Osmund Andersen Tunheim"
#   P569 date of birth = +1635-00-00T00:00:00Z/9
LAST	P569	+1635-00-00T00:00:00Z/9	S2600	"6000000002763481707"
#   P570 date of death = +1699-00-00T00:00:00Z/9
LAST	P570	+1699-00-00T00:00:00Z/9	S2600	"6000000002763481707"
#   P40 child = Q141205914 Inger (Ingrid) Osmundsdatter Risa
LAST	P40	Q141205914	S2600	"6000000002763481707"
#   Q141205914 Inger (Ingrid) Osmundsdatter Risa: P22 father = the item just created
Q141205914	P22	LAST	S2600	"6000000002763481707"
#   the item just created: P735 given name = Q7107242 Osmund
LAST	P735	Q7107242
#   P734 family name = Q36927172
LAST	P734	Q36927172

# create a new item
CREATE
#   set the en label to "Ragnhild Kristine Øystensdatter Nese"
LAST	Len	"Ragnhild Kristine Øystensdatter Nese"
#   set the mul label to "Ragnhild Kristine Øystensdatter Nese"
LAST	Lmul	"Ragnhild Kristine Øystensdatter Nese"
#   set the ja label to "ラグンヒル・クリスティン・オイステンスダッテル・ネセ"
LAST	Lja	"ラグンヒル・クリスティン・オイステンスダッテル・ネセ"
#   set the zh label to "拉格希尔德·克丽丝汀·奥伊斯滕斯达特·内塞"
LAST	Lzh	"拉格希尔德·克丽丝汀·奥伊斯滕斯达特·内塞"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000010479856178 Ragnhild Kristine Øystensdatter Nese, qualified P1810 subject named as Ragnhild Kristine Øystensdatter Nese
LAST	P2600	"6000000010479856178"	P1810	"Ragnhild Kristine Øystensdatter Nese"
#   P569 date of birth = +1786-09-05T00:00:00Z/11
LAST	P569	+1786-09-05T00:00:00Z/11	S2600	"6000000010479856178"
#   P570 date of death = +1871-02-06T00:00:00Z/11
LAST	P570	+1871-02-06T00:00:00Z/11	S2600	"6000000010479856178"
#   P26 spouse = Q141223432 Osmund Larsson Nese
LAST	P26	Q141223432	S2600	"6000000010479856178"
#   P40 child = Q141223503 Anne Berta Osmundsdatter Nese
LAST	P40	Q141223503	S2600	"6000000010479856178"
#   Q141223432 Osmund Larsson Nese: P26 spouse = the item just created
Q141223432	P26	LAST	S2600	"6000000010479856178"
#   Q141223503 Anne Berta Osmundsdatter Nese: P25 mother = the item just created
Q141223503	P25	LAST	S2600	"6000000010479856178"

# create a new item
CREATE
#   the item just created: set the en label to "Rasmus Wibye Andersson Lea"
LAST	Len	"Rasmus Wibye Andersson Lea"
#   set the mul label to "Rasmus Wibye Andersson Lea"
LAST	Lmul	"Rasmus Wibye Andersson Lea"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005609547535 Rasmus Wibye Andersson Lea, qualified P1810 subject named as Rasmus Wibye Andersson Lea
LAST	P2600	"6000000005609547535"	P1810	"Rasmus Wibye Andersson Lea"
#   P569 date of birth = +1813-00-00T00:00:00Z/9
LAST	P569	+1813-00-00T00:00:00Z/9	S2600	"6000000005609547535"
#   P570 date of death = +1880-03-27T00:00:00Z/11
LAST	P570	+1880-03-27T00:00:00Z/11	S2600	"6000000005609547535"
#   P26 spouse = Q141223503 Anne Berta Osmundsdatter Nese
LAST	P26	Q141223503	S2600	"6000000005609547535"
#   Q141223503 Anne Berta Osmundsdatter Nese: P26 spouse = the item just created
Q141223503	P26	LAST	S2600	"6000000005609547535"

# create a new item
CREATE
#   the item just created: set the en label to "Torger Olson Skorve"
LAST	Len	"Torger Olson Skorve"
#   set the mul label to "Torger Olson Skorve"
LAST	Lmul	"Torger Olson Skorve"
#   set the ja label to "トルゲル・オルソン・スコルヴェ"
LAST	Lja	"トルゲル・オルソン・スコルヴェ"
#   set the zh label to "托尔盖尔·奥尔森·斯科尔韦"
LAST	Lzh	"托尔盖尔·奥尔森·斯科尔韦"
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
#   P734 family name = Q48531176
LAST	P734	Q48531176

# create a new item
CREATE
#   set the en label to "Tormod Rasmusson Nedre Rossavik"
LAST	Len	"Tormod Rasmusson Nedre Rossavik"
#   set the mul label to "Tormod Rasmusson Nedre Rossavik"
LAST	Lmul	"Tormod Rasmusson Nedre Rossavik"
#   set the ja label to "トルモド・ラスムソン・ネドレ・ロサヴィク"
LAST	Lja	"トルモド・ラスムソン・ネドレ・ロサヴィク"
#   set the zh label to "托尔莫德·拉斯穆松·内德雷·罗萨维克"
LAST	Lzh	"托尔莫德·拉斯穆松·内德雷·罗萨维克"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005609571149 Tormod Rasmusson Nedre Rossavik, qualified P1810 subject named as Tormod Rasmusson Nedre Rossavik
LAST	P2600	"6000000005609571149"	P1810	"Tormod Rasmusson Nedre Rossavik"
#   P569 date of birth = +1719-00-00T00:00:00Z/9
LAST	P569	+1719-00-00T00:00:00Z/9	S2600	"6000000005609571149"
#   P570 date of death = +1801-00-00T00:00:00Z/9
LAST	P570	+1801-00-00T00:00:00Z/9	S2600	"6000000005609571149"
#   P22 father = Q141216644 Rasmus Asbjørnson Nedre Rossavik
LAST	P22	Q141216644	S2600	"6000000005609571149"
#   P25 mother = Q141205898 Anna Tormodsdatter Mele
LAST	P25	Q141205898	S2600	"6000000005609571149"
#   Q141216644 Rasmus Asbjørnson Nedre Rossavik: P40 child = the item just created
Q141216644	P40	LAST	S2600	"6000000005609571149"
#   Q141205898 Anna Tormodsdatter Mele: P40 child = the item just created
Q141205898	P40	LAST	S2600	"6000000005609571149"
#   the item just created: P735 given name = Q7825922 Tormod
LAST	P735	Q7825922
#   P734 family name = Q122838342
LAST	P734	Q122838342
#   add a mul alias "Tormod Nedre Rossavik"
LAST	Amul	"Tormod Nedre Rossavik"
#   Q141223423 Harlverg B. Ekman: P3373 sibling = Q141205908 Gotfred Olai Ekman
Q141223423	P3373	Q141205908	S2600	"285886949080005081"
#   Q141219059 Gustava Maria Sofia Mannerheim: P735 given name = Q325872 Maria, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141219059	P735	Q325872	P1545	"2"	P3831	Q245025
#   P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q141219059	P735	Q18201520	P1545	"3"	P3831	Q245025
#   Q141223426 Isak Reinhold Sahlberg: P26 spouse = Q141223428 Lovisa Catharina Polviander
Q141223426	P26	Q141223428	S2600	"5580425653980118255"
#   Q141223428 Lovisa Catharina Polviander: P26 spouse = Q141223426 Isak Reinhold Sahlberg
Q141223428	P26	Q141223426	S2600	"5580429510180056637"
#   Q141219324 Sofia Maria Mannerheim: P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141219324	P735	Q18201520	P1545	"1"	P7452	Q3409033
#   P735 given name = Q325872 Maria, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141219324	P735	Q325872	P1545	"2"	P3831	Q245025
#   Q141219332 Sofia Wadenstierna: P735 given name = Q18201520 Sofia
Q141219332	P735	Q18201520
#   Q141219316 Reiar Einarsen Kydland: P734 family name = Q30514142
Q141219316	P734	Q30514142
#   Q141205922 Marit Ormsd Byre: P734 family name = Q37515983
Q141205922	P734	Q37515983
#   Q141199851 Lagmann Gunnbjørn Toresson Tengs: P735 given name = Q136849653, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141199851	P735	Q136849653	P1545	"2"	P3831	Q245025
#   P734 family name = Q55233230
Q141199851	P734	Q55233230
#   Q141206061 Cecilie Olsdatter Håland: P734 family name = Q30580079
Q141206061	P734	Q30580079
#   Q141205942 Tore II Gardson Gard: P734 family name = Q37475140
Q141205942	P734	Q37475140
#   Q141217384 David Tjølson Edland: P734 family name = Q31454737
Q141217384	P734	Q31454737
#   Q141216602 Berta Guria Davidsdatter Stokka: P734 family name = Q37033285
Q141216602	P734	Q37033285
#   Q141216653 Torger Torgerson Stokka: P734 family name = Q37033285
Q141216653	P734	Q37033285
#   Q141223432 Osmund Larsson Nese: P735 given name = Q7107242 Osmund
Q141223432	P735	Q7107242
#   P734 family name = Q37543374
Q141223432	P734	Q37543374
#   Q141198422 Iver Pedersen Sandsmark: P734 family name = Q37541803
Q141198422	P734	Q37541803
#   Q141198414 Ingeborg Olsdatter Sandsmark: P734 family name = Q37541803
Q141198414	P734	Q37541803
#   Q141198396 Erling Juel Wendt: P735 given name = Q123820113, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141198396	P735	Q123820113	P1545	"2"	P3831	Q245025
#   Q141198382 Berita Larsdatter Rossavik: P734 family name = Q122838342
Q141198382	P734	Q122838342
#   Q141189055 Astri Torkelsdatter Gilja: P734 family name = Q122836259
Q141189055	P734	Q122836259
#   Q141216471 Gunnbjørn Gunnbjørnson Rossavik: P735 given name = Q136849653
Q141216471	P735	Q136849653
#   P734 family name = Q122838342
Q141216471	P734	Q122838342
#   Q141198435 Jon Nilsson Espedal: P734 family name = Q27892902
Q141198435	P734	Q27892902
#   Q141198503 Tore Erikson Håland: P734 family name = Q30580079
Q141198503	P734	Q30580079
#   Q141200094 Siri Rasmusdtr. Erevik: P734 family name = Q35855266
Q141200094	P734	Q35855266
#   Q141199819 Anna Andersdotter: P735 given name = Q666578 Anna
Q141199819	P735	Q666578
#   Q141216644 Rasmus Asbjørnson Nedre Rossavik: P734 family name = Q122838342
Q141216644	P734	Q122838342
#   Q141205930 Olav Knutson Randa Håland: P734 family name = Q30580079
Q141205930	P734	Q30580079
#   Q141216487 Knut Johanson Håland: P734 family name = Q30580079
Q141216487	P734	Q30580079
#   Q141216489 Laurits Leivson Bjørheim: P734 family name = Q30834379
Q141216489	P734	Q30834379
#   Q141216638 Olaug Jonsdatter Heigre: P734 family name = Q45305861
Q141216638	P734	Q45305861
#   Q141219299 Per Asbjørnson Stokka: P734 family name = Q37033285
Q141219299	P734	Q37033285
#   Q141216637 Ola Person Persson Heigre: P734 family name = Q45305861
Q141216637	P734	Q45305861
#   Q141205914 Inger (Ingrid) Osmundsdatter Risa: P734 family name = Q36931214
Q141205914	P734	Q36931214
#   Q141216387 Johannes Svensen Obrestad: P734 family name = Q40353802
Q141216387	P734	Q40353802
#   Q141199892 Jon Olsen Heigre: P734 family name = Q45305861
Q141199892	P734	Q45305861
#   Q141216365 Berte Karine Jonsdatter Stokka: P734 family name = Q37033285
Q141216365	P734	Q37033285
#   Q141216510 Torger Torgerson Stokka: P734 family name = Q37033285
Q141216510	P734	Q37033285
#   Q141189070 John Jonassen Hegre: P735 given name = Q4925477 John
Q141189070	P735	Q4925477
#   P734 family name = Q36955626
Q141189070	P734	Q36955626
#   Q141189098 Rakel Jonasdatter Heigre: P734 family name = Q45305861
Q141189098	P734	Q45305861
#   Q141216635 Martha Eivindsdatter Heigre: P735 given name = Q16279062
Q141216635	P735	Q16279062
#   P734 family name = Q45305861
Q141216635	P734	Q45305861
#   Q141216643 Ragna Enevaldsdatter Heigre: P734 family name = Q45305861
Q141216643	P734	Q45305861
#   Q141178381 Marta Jonsdatter Li: P734 family name = Q686223 Li
Q141178381	P734	Q686223
#   Q141205921 Maria Jonsdatter Lura: P735 given name = Q325872 Maria
Q141205921	P735	Q325872
#   P734 family name = Q37303374
Q141205921	P734	Q37303374
#   Q141216594 Ane Maria Olsdatter Vestre Stangaland: P735 given name = Q325872 Maria, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141216594	P735	Q325872	P1545	"2"	P3831	Q245025
#   Q141162043 Inger Marie Mary Eivindsdatter Ronneberg: P735 given name = Q734578 Mary, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q141162043	P735	Q734578	P1545	"3"	P3831	Q245025
#   Q141162046 Ane Oline Lena Eivindsdatter Tunheim: P735 given name = Q654581 Lena, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q141162046	P735	Q654581	P1545	"3"	P3831	Q245025
#   Q141169072 Ådne Olsen Garborg: P735 given name = Q12011446
Q141169072	P735	Q12011446
#   Q141189066 Helge Rasmusson Bø: P734 family name = Q30253098
Q141189066	P734	Q30253098
#   Q141216407 Torkel Torbjørnson Høyland: P734 family name = Q27888882
Q141216407	P734	Q27888882
#   Q141198370 NN Skårland: P734 family name = Q40480033
Q141198370	P734	Q40480033
#   Q141198375 Astri Torchelsdatter Øvre Time: P734 family name = Q37494555
Q141198375	P734	Q37494555
#   Q141216356 NN Undheim: P734 family name = Q27888846
Q141216356	P734	Q27888846
#   Q141216598 Anna Ivarsd Stokka: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141216598	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P734 family name = Q37033285
Q141216598	P734	Q37033285
#   Q141199704 Andreas Olai: P735 given name = Q4926263 Andreas
Q141199704	P735	Q4926263
#   Q141180413 Thomas Matthiæ: P735 given name = Q16428906
Q141180413	P735	Q16428906
#   Q141216495 NN (Frille): P734 family name = Q54366191
Q141216495	P734	Q54366191
#   Q141199862 Helga Bjørnsdatter Tengs: P734 family name = Q55233230
Q141199862	P734	Q55233230
#   Q141219176 Eivind Ogmundsson Byre på Høyland: P734 family name = Q27888882
Q141219176	P734	Q27888882
#   Q141216377 Hanna Sofie Wendt: P735 given name = Q1554377 Hannah, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141216377	P735	Q1554377	P1545	"1"	P7452	Q3409033
#   Q141216488 Lars Jonsen Landsnes: P734 family name = Q122837341
Q141216488	P734	Q122837341
#   Q141216632 Magdalena Lauritsd Hogganvik: P734 family name = Q55240992
Q141216632	P734	Q55240992
#   Q141216396 Lisbet Olavsdatter Håland: P734 family name = Q30580079
Q141216396	P734	Q30580079
#   Q141198834 Gunnbjørn Jonson Mjølhus: P735 given name = Q136849653
Q141198834	P735	Q136849653
#   Q141216613 Karen Henriksdotter Raunes Våga: P735 given name = Q1221747 Karen, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141216613	P735	Q1221747	P1545	"1"	P7452	Q3409033
#   P734 family name = Q40306448
Q141216613	P734	Q40306448
#   Q141216384 Ingeborg Eriksdatter Time: P734 family name = Q37494555
Q141216384	P734	Q37494555
#   Q141168827 Hans Eivind Garborg: P735 given name = Q632842, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141168827	P735	Q632842	P1545	"1"	P7452	Q3409033
#   Q141219291 Maria Hansdatter Austrått: P735 given name = Q325872 Maria
Q141219291	P735	Q325872
#   Q141223436 Tore Underberge III: P735 given name = Q1548096 Tore, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141223436	P735	Q1548096	P1545	"1"	P7452	Q3409033
#   Q141205919 Malena Hansdatter Bø: P734 family name = Q30253098
Q141205919	P734	Q30253098
#   Q141219349 Tørres Jonson Grannes: P735 given name = Q12008164
Q141219349	P735	Q12008164
#   Q141205898 Anna Tormodsdatter Mele: P735 given name = Q666578 Anna
Q141205898	P735	Q666578
#   Q141219060 Halvor Johannesson Hobberstad: P734 family name = Q40703807
Q141219060	P734	Q40703807
#   Q141217369 Anna Osmundsd Stokka: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141217369	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P734 family name = Q37033285
Q141217369	P734	Q37033285
#   Q141198371 Anna Belestdatter Lauvsnes: P735 given name = Q666578 Anna
Q141198371	P735	Q666578
#   Q141189071 Joren Jonsdatter Espedal: P735 given name = Q2554259
Q141189071	P735	Q2554259
#   P734 family name = Q27892902
Q141189071	P734	Q27892902
#   Q141180408 Jon Larsson Mæle: P734 family name = Q34190986
Q141180408	P734	Q34190986
#   Q141180412 Marta Rasmusdatter Li: P734 family name = Q686223 Li
Q141180412	P734	Q686223
#   Q141216645 Reiar Reiersen Kydland: P734 family name = Q30514142
Q141216645	P734	Q30514142
#   Q141216609 Inger Kristoffersdatter Skårland: P734 family name = Q40480033
Q141216609	P734	Q40480033
#   Q141223503 Anne Berta Osmundsdatter Nese: P735 given name = Q564684 Anne, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141223503	P735	Q564684	P1545	"1"	P7452	Q3409033
#   P735 given name = Q4092653 Berta, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141223503	P735	Q4092653	P1545	"2"	P3831	Q245025
#   P734 family name = Q37543374
Q141223503	P734	Q37543374
#   Q141219051 Anna Börjesdotter Bothniensis: P735 given name = Q666578 Anna
Q141219051	P735	Q666578
#   Q141205900 Bertrand Olav Olsen Vigdel: P735 given name = Q3637880, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141205900	P735	Q3637880	P1545	"1"	P7452	Q3409033
#   Q141205938 Ranveig Olsd Trevland: P735 given name = Q30836047, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141205938	P735	Q30836047	P1545	"1"	P7452	Q3409033
#   Q141205911 Hans Svensen Risa I: P735 given name = Q632842, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141205911	P735	Q632842	P1545	"1"	P7452	Q3409033
#   Q141200074 Rasmus Olsen Bø: P734 family name = Q30253098
Q141200074	P734	Q30253098
#   Q141189088 Ola Knutsen Grøtheim: P734 family name = Q122836435
Q141189088	P734	Q122836435
#   Q141199809 Ane Marie Helgesdatter Bø: P734 family name = Q30253098
Q141199809	P734	Q30253098
#   Q141217387 Ivar Stokka: P734 family name = Q37033285
Q141217387	P734	Q37033285
#   Q141198755 Anna Ingebretsdatter Voster: P735 given name = Q666578 Anna
Q141198755	P735	Q666578
#   Q141198751 Lars Person Nedre Rossavik: P734 family name = Q122838342
Q141198751	P734	Q122838342
#   Q141216483 Karen Malena Rasmusdatter Tjelta: P735 given name = Q1221747 Karen, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141216483	P735	Q1221747	P1545	"1"	P7452	Q3409033
#   P734 family name = Q38898383
Q141216483	P734	Q38898383
#   Q141189069 Ingeborg Ådnesdatter Grøtheim: P734 family name = Q122836435
Q141189069	P734	Q122836435
#   Q141199830 Anna Rasmusdatter Grøtheim: P735 given name = Q666578 Anna
Q141199830	P735	Q666578
#   P734 family name = Q122836435
Q141199830	P734	Q122836435
#   Q141216600 Astrid Omundsdatter Grøtheim: P734 family name = Q122836435
Q141216600	P734	Q122836435
#   Q141216380 Hans Olsen Grøtheim: P735 given name = Q632842
Q141216380	P735	Q632842
#   P734 family name = Q122836435
Q141216380	P734	Q122836435
#   Q141216382 Helge Asbjørnsen Bø: P734 family name = Q30253098
Q141216382	P734	Q30253098
#   Q141217394 Margareta Christina von Numers: P735 given name = Q1083457 Christina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141217394	P735	Q1083457	P1545	"2"	P3831	Q245025
#   Q141205937 Ragnhild Eyvindsdotter Eyvindsdotter: P40 child = Q141223436 Tore Underberge III
Q141205937	P40	Q141223436	S2600	"6000000008686109792"
#   Q141223430 Magdalena Sofia Falkenberg af Bålby: P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141223430	P735	Q18201520	P1545	"2"	P3831	Q245025
#   Q141216599 Anna Rasmusdatter Nedre Rossavik: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141216599	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P734 family name = Q122838342
Q141216599	P734	Q122838342
#   Q141216381 Hans Rasmussen Låge-Håland: P735 given name = Q632842
Q141216381	P735	Q632842
#   Q141216607 Hans Erikson Øvre Håland: P735 given name = Q632842, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141216607	P735	Q632842	P1545	"1"	P7452	Q3409033
#   P734 family name = Q30580079
Q141216607	P734	Q30580079
#   Q141216498 Norman Charles Tunheim: P734 family name = Q36927172
Q141216498	P734	Q36927172
#   Q141219284 Maria Benjaminsdotter: P735 given name = Q325872 Maria
Q141219284	P735	Q325872
#   Q141216595 Anna Danielsdotter: P735 given name = Q666578 Anna
Q141216595	P735	Q666578
#   Q141223434 Samuel Aslakson Tunheim: P26 spouse = Q141223417 Elen Malena Halvorsdtr Tunheim
Q141223434	P26	Q141223417	S2600	"6000000011971496046"
#   P734 family name = Q36927172
Q141223434	P734	Q36927172
#   Q141219202 Elen Kristoffersdotter Nese: P40 child = Q141223432 Osmund Larsson Nese
Q141219202	P40	Q141223432	S2600	"6000000012587664964"
#   P734 family name = Q37543374
Q141219202	P734	Q37543374
#   Q141217359 Anna Elisabet Angerstein: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141217359	P735	Q666578	P1545	"1"	P7452	Q3409033
#   Q141189083 Martha Elida Frenning: P735 given name = Q16279062, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141189083	P735	Q16279062	P1545	"1"	P7452	Q3409033
#   Q141216383 Ingeborg Eriksdatter Bjorland: P734 family name = Q123200450
Q141216383	P734	Q123200450
#   Q141223516 Hans Otto Kristian Jenssen: P40 child = Q141223517 Hilma Petrine Jenssen
Q141223516	P40	Q141223517	S2600	"6000000014188476819"
#   Q141223517 Hilma Petrine Jenssen: P22 father = Q141223516 Hans Otto Kristian Jenssen
Q141223517	P22	Q141223516	S2600	"6000000014196669652"
#   Q141216490 Malli Svensdatter Lura: P735 given name = Q106145589
Q141216490	P735	Q106145589
#   P734 family name = Q37303374
Q141216490	P734	Q37303374
#   Q141216481 Jon Tørresson Soma: P734 family name = Q37104818
Q141216481	P734	Q37104818
#   Q141219070 Tørres Jonsson Vatne: P735 given name = Q12008164
Q141219070	P735	Q12008164
#   Q141216400 Margreta Lauritsdatter Øvre Bjørheim: P734 family name = Q30834379
Q141216400	P734	Q30834379
#   Q141205895 Andreas Christiansen: P735 given name = Q4926263 Andreas
Q141205895	P735	Q4926263
#   Q141216401 Mariet Danielsdotter: P735 given name = Q117599926
Q141216401	P735	Q117599926
#   Q141223518 Jakob Bunge: P26 spouse = Q141223502 Anna Martens
Q141223518	P26	Q141223502	S2600	"6000000018604538988"
#   Q141223502 Anna Martens: P26 spouse = Q141223518 Jakob Bunge
Q141223502	P26	Q141223518	S2600	"6000000018604581410"
#   Q141205896 Ane Marie Konstanse Amanda Kristine Hegre: P735 given name = Q19572240, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q141205896	P735	Q19572240	P1545	"3"	P3831	Q245025
#   P734 family name = Q36955626
Q141205896	P734	Q36955626
#   Q141189084 Martin Tollefson Tunheim: P734 family name = Q36927172
Q141189084	P734	Q36927172
#   Q141219155 Christina Maria Adelheim: P735 given name = Q1083457 Christina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141219155	P735	Q1083457	P1545	"1"	P7452	Q3409033
#   P735 given name = Q325872 Maria, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141219155	P735	Q325872	P1545	"2"	P3831	Q245025
#   Q141199930 Knut Olsen Gudmestad: P734 family name = Q37015437
Q141199930	P734	Q37015437
#   Q141198441 Kirsten Olsdatter Grøtheim: P734 family name = Q122836435
Q141198441	P734	Q122836435
#   Q141189065 Gustav Adolf Gundersen: P735 given name = Q746076, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141189065	P735	Q746076	P1545	"1"	P7452	Q3409033
#   Q141216386 Jens Wilhelm Wendt: P735 given name = Q11027623, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141216386	P735	Q11027623	P1545	"2"	P3831	Q245025
#   Q141189090 Ole Christopher Christiansen: P735 given name = Q1084472 Christopher, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141189090	P735	Q1084472	P1545	"2"	P3831	Q245025
#   Q141189099 Rasmus Helgesen Bø: P734 family name = Q30253098
Q141189099	P734	Q30253098
#   Q141219050 Ane Olsdatter Bø: P734 family name = Q30253098
Q141219050	P734	Q30253098
#   Q141199909 Karen Sophie Pedersdatter: P735 given name = Q1221747 Karen, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141199909	P735	Q1221747	P1545	"1"	P7452	Q3409033
#   Q138474188 Hans Syvertsen Nyvold: P735 given name = Q632842
Q138474188	P735	Q632842
#   Q141216505 Thekla Cecilie Dybo: P735 given name = Q21147318 Thekla, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141216505	P735	Q21147318	P1545	"1"	P7452	Q3409033
#   Q141223523 Johan Fredrik Wedberg: P40 child = Q141223506 Beda Elvira Wedberg
Q141223523	P40	Q141223506	S2600	"6000000021652410546"
#   P735 given name = Q10989273 Johan, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141223523	P735	Q10989273	P1545	"1"	P7452	Q3409033
#   P735 given name = Q4926491 Fredrik, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141223523	P735	Q4926491	P1545	"2"	P3831	Q245025
#   P734 family name = Q54444784
Q141223523	P734	Q54444784
#   Q141189111 Tørres Jonasson Hegre: P735 given name = Q12008164
Q141189111	P735	Q12008164
#   P734 family name = Q36955626
Q141189111	P734	Q36955626
#   Q141223411 Anna Mårtensdotter: P735 given name = Q666578 Anna
Q141223411	P735	Q666578
#   Q141217398 Måns Moge: P734 family name = Q12796950
Q141217398	P734	Q12796950
#   Q141217396 Maria No name: P735 given name = Q325872 Maria, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141217396	P735	Q325872	P1545	"1"	P7452	Q3409033
#   P735 given name = Q21148356, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141217396	P735	Q21148356	P1545	"2"	P3831	Q245025
#   Q141199822 Anna Jönsdotter: P735 given name = Q666578 Anna
Q141199822	P735	Q666578
#   Q141189058 Brita Thomasdotter: P735 given name = Q918013
Q141189058	P735	Q918013
#   Q141199826 Anna Maria Samuelsdtr. Tunheim: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141199826	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P735 given name = Q325872 Maria, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141199826	P735	Q325872	P1545	"2"	P3831	Q245025
#   P734 family name = Q36927172
Q141199826	P734	Q36927172
#   Q141200112 Tollef Pederson Tunheim: P734 family name = Q36927172
Q141200112	P734	Q36927172
#   Q141223417 Elen Malena Halvorsdtr Tunheim: P26 spouse = Q141223434 Samuel Aslakson Tunheim
Q141223417	P26	Q141223434	S2600	"6000000029983713844"
#   P734 family name = Q36927172
Q141223417	P734	Q36927172
#   Q141216494 N.N. Jacobsdtr. Koll: P734 family name = Q21510541
Q141216494	P734	Q21510541
#   Q141189105 Sophia Birgitta Gundersen: P735 given name = Q2302787 Sophia, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141189105	P735	Q2302787	P1545	"1"	P7452	Q3409033
#   Q141189052 Anna Carine Gundersen: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141189052	P735	Q666578	P1545	"1"	P7452	Q3409033
#   Q141198472 Olga E. Garborg Oswald: P735 given name = Q20187, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141198472	P735	Q20187	P1545	"1"	P7452	Q3409033
#   Q141219052 Anna Olsdatter Heigre: P735 given name = Q666578 Anna
Q141219052	P735	Q666578
#   P734 family name = Q45305861
Q141219052	P734	Q45305861
#   Q141199992 Myrtle Lenora Tunheim: P734 family name = Q36927172
Q141199992	P734	Q36927172
#   Q141216405 Tabite Tollefsdotter Tunheim: P734 family name = Q36927172
Q141216405	P734	Q36927172
#   Q141205918 Mabel Tunheim: P734 family name = Q36927172
Q141205918	P734	Q36927172
#   Q141199833 Bertha Ingeborg Tunheim: P734 family name = Q36927172
Q141199833	P734	Q36927172
#   Q141189107 Theodore Roosevelt Tunheim: P734 family name = Q36927172
Q141189107	P734	Q36927172
#   Q141189102 Sigrid Sally Manilva Ekman: P735 given name = Q19816532 Sally, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141189102	P735	Q19816532	P1545	"2"	P3831	Q245025
#   Q141189074 Joseph Tunheim: P734 family name = Q36927172
Q141189074	P734	Q36927172
#   Q141189049 Alfred Tunheim: P734 family name = Q36927172
Q141189049	P734	Q36927172
#   Q141200084 Selma Johanna Tunheim: P734 family name = Q36927172
Q141200084	P734	Q36927172
#   Q141189101 Samuel Tunheim: P734 family name = Q36927172
Q141189101	P734	Q36927172
#   Q141189095 Peter Tunheim: P734 family name = Q36927172
Q141189095	P734	Q36927172
#   Q141189109 Tollef Bud Tunheim: P734 family name = Q36927172
Q141189109	P734	Q36927172
#   Q141223424 Harriet Lane Tunheim: P734 family name = Q36927172
Q141223424	P734	Q36927172
#   Q141199836 Florence June Tunheim Cosman: P735 given name = Q1152453 June, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141199836	P735	Q1152453	P1545	"2"	P3831	Q245025
#   Q141205894 Agnes Tunheim: P734 family name = Q36927172
Q141205894	P734	Q36927172
#   Q141216458 Asbjørn Gunnarson Bø: P734 family name = Q30253098
Q141216458	P734	Q30253098
#   Q141216456 Anna Helgesdotter Opstad: P735 given name = Q666578 Anna
Q141216456	P735	Q666578
#   Q141216468 Erik Hansson Gausland: P734 family name = Q132192515
Q141216468	P734	Q132192515
#   Q141219063 Lars Osmundsen Nese: P734 family name = Q37543374
Q141219063	P734	Q37543374
#   Q141199918 Kirsten Hansdatter Grøtheim: P734 family name = Q122836435
Q141199918	P734	Q122836435
#   Q141216363 Anne Govertsdtr. Bratland: P735 given name = Q564684 Anne, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141216363	P735	Q564684	P1545	"1"	P7452	Q3409033
#   Q141223506 Beda Elvira Wedberg: P22 father = Q141223523 Johan Fredrik Wedberg
Q141223506	P22	Q141223523	S2600	"6000000177921458833"
#   P735 given name = Q3051870 Elvira, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141223506	P735	Q3051870	P1545	"2"	P3831	Q245025
#   P734 family name = Q54444784
Q141223506	P734	Q54444784
#   Q141223427 Johanna Matilda Carlsdotter: P735 given name = Q4120836 Johanna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141223427	P735	Q4120836	P1545	"1"	P7452	Q3409033
#   P735 given name = Q2054021 Matilda, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141223427	P735	Q2054021	P1545	"2"	P3831	Q245025
#   Q141223507 Carl, Johan Ersson: P735 given name = Q10989273 Johan, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141223507	P735	Q10989273	P1545	"2"	P3831	Q245025
#   Q141219160 Christina, Sofia Carlsdotter: P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141219160	P735	Q18201520	P1545	"2"	P3831	Q245025
#   Q141198399 Eugene LeRoy Tunheim: P735 given name = Q545971, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141198399	P735	Q545971	P1545	"1"	P7452	Q3409033
#   P735 given name = Q19839067 Leroy, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141198399	P735	Q19839067	P1545	"2"	P3831	Q245025
#   P734 family name = Q36927172
Q141198399	P734	Q36927172
#   Q141219164 David Robert Tunheim: P735 given name = Q4927937 Robert, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141219164	P735	Q4927937	P1545	"2"	P3831	Q245025
#   P734 family name = Q36927172
Q141219164	P734	Q36927172
#   Q141189054 Anna Maria Helgesdatter Bø: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141189054	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P735 given name = Q325872 Maria, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141189054	P735	Q325872	P1545	"2"	P3831	Q245025
#   P734 family name = Q30253098
Q141189054	P734	Q30253098
#   Q141189113 Ådne Helgesen Bø: P735 given name = Q12011446
Q141189113	P735	Q12011446
#   P734 family name = Q30253098
Q141189113	P734	Q30253098
#   Q141217392 Larine Eriksdatter Heigre: P734 family name = Q45305861
Q141217392	P734	Q45305861
#   Q141217390 Johan Johannessen Obrestad: P734 family name = Q40353802
Q141217390	P734	Q40353802
#   Q141206056 Asbjørn Helgesen Bø: P734 family name = Q30253098
Q141206056	P734	Q30253098
#   Q141216379 Hans Halvardsen Grøtheim: P735 given name = Q632842
Q141216379	P735	Q632842
#   P734 family name = Q122836435
Q141216379	P734	Q122836435
#   Q141216374 Halvard Assersen Grøtheim: P734 family name = Q122836435
Q141216374	P734	Q122836435
#   Q141200127 Ådne Hansen Grøtheim: P735 given name = Q12011446
Q141200127	P735	Q12011446
#   P734 family name = Q122836435
Q141200127	P734	Q122836435
#   Q141216608 Hans Ådnesen Grøtheim: P735 given name = Q632842
Q141216608	P735	Q632842
#   P734 family name = Q122836435
Q141216608	P734	Q122836435

