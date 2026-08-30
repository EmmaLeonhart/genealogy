# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   1124 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   set the zh label to "约翰·约纳森·赫格雷"
Q141189070	Lzh	"约翰·约纳森·赫格雷"
#   Q141189098 Rakel Jonasdatter Heigre: set the ja label to "ラケル・ヨナスダッテル・ヘイグレ"
Q141189098	Lja	"ラケル・ヨナスダッテル・ヘイグレ"
#   set the zh label to "拉凯尔·约纳斯达特·海格勒"
Q141189098	Lzh	"拉凯尔·约纳斯达特·海格勒"
#   Q141216635 Martha Eivindsdatter Heigre: add a mul alias "Martha Eivindsdatter Sveinsvoll"
Q141216635	Amul	"Martha Eivindsdatter Sveinsvoll"
#   set the ja label to "マーサ・エイヴィンスダッテル・ヘイグレ"
Q141216635	Lja	"マーサ・エイヴィンスダッテル・ヘイグレ"
#   set the zh label to "玛莎·埃温斯达特·海格勒"
Q141216635	Lzh	"玛莎·埃温斯达特·海格勒"
#   Q141216622 Kristine Jonsdatter Malmeim: set the ja label to "クリスティン・ヨンスダッテル・マルメイム"
Q141216622	Lja	"クリスティン・ヨンスダッテル・マルメイム"
#   Q141169046 Samuel Jonson: set the ja label to "サミュエル・ヨンソン"
Q141169046	Lja	"サミュエル・ヨンソン"
#   set the zh label to "塞缪尔·永松"
Q141169046	Lzh	"塞缪尔·永松"
#   Q141178381 Marta Jonsdatter Li: set the ja label to "マルタ・ヨンスダッテル・リー"
Q141178381	Lja	"マルタ・ヨンスダッテル・リー"
#   Q141178380 Samuel Jonson Raustad: set the ja label to "サミュエル・ヨンソン・ラウスタード"
Q141178380	Lja	"サミュエル・ヨンソン・ラウスタード"
#   set the zh label to "塞缪尔·永松·劳斯塔"
Q141178380	Lzh	"塞缪尔·永松·劳斯塔"
#   Q141206082 Jon Olson Raustad: set the ja label to "ジョン・オルソン・ラウスタード"
Q141206082	Lja	"ジョン・オルソン・ラウスタード"
#   set the zh label to "乔恩·奥尔森·劳斯塔"
Q141206082	Lzh	"乔恩·奥尔森·劳斯塔"
#   Q141216390 Kirsten Gabrielsdatter Austråt: set the ja label to "キルステン・ガブリエルスダッテル・アウストロート"
Q141216390	Lja	"キルステン・ガブリエルスダッテル・アウストロート"

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Adolf Adelswärd"
LAST	Len	"Adolf Adelswärd"
#   set the mul label to "Adolf Adelswärd"
LAST	Lmul	"Adolf Adelswärd"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000205630579893 Adolf Adelswärd, qualified P1810 subject named as Adolf Adelswärd
LAST	P2600	"6000000205630579893"	P1810	"Adolf Adelswärd"
#   P569 date of birth = +1752-00-00T00:00:00Z/9
LAST	P569	+1752-00-00T00:00:00Z/9	S2600	"6000000205630579893"
#   P570 date of death = +1755-00-00T00:00:00Z/9
LAST	P570	+1755-00-00T00:00:00Z/9	S2600	"6000000205630579893"
#   P22 father = Q5542622 Johan Adelswärd
LAST	P22	Q5542622	S2600	"6000000205630579893"
#   Q5542622 Johan Adelswärd: P40 child = the item just created
Q5542622	P40	LAST	S2600	"6000000205630579893"
#   the item just created: P735 given name = Q18145837 Adolf
LAST	P735	Q18145837

# create a new item
CREATE
#   set the en label to "Christina Burea"
LAST	Len	"Christina Burea"
#   set the mul label to "Christina Burea"
LAST	Lmul	"Christina Burea"
#   set the ja label to "クリスティーナ・ブレア"
LAST	Lja	"クリスティーナ・ブレア"
#   set the zh label to "克里斯蒂娜·布雷阿"
LAST	Lzh	"克里斯蒂娜·布雷阿"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000025579156578 Christina Burea, qualified P1810 subject named as Christina Burea
LAST	P2600	"6000000025579156578"	P1810	"Christina Burea"
#   P569 date of birth = +1598-00-00T00:00:00Z/9
LAST	P569	+1598-00-00T00:00:00Z/9	S2600	"6000000025579156578"
#   P22 father = Q633094 Johannes Thomæ Agrivillensis Bureus
LAST	P22	Q633094	S2600	"6000000025579156578"
#   P25 mother = Q141180410 Margareta Mårtensdotter Bång
LAST	P25	Q141180410	S2600	"6000000025579156578"
#   Q633094 Johannes Thomæ Agrivillensis Bureus: P40 child = the item just created
Q633094	P40	LAST	S2600	"6000000025579156578"
#   Q141180410 Margareta Mårtensdotter Bång: P40 child = the item just created
Q141180410	P40	LAST	S2600	"6000000025579156578"
#   the item just created: P735 given name = Q1083457 Christina
LAST	P735	Q1083457

# create a new item
CREATE
#   set the en label to "Elen Margrethe Stangeland"
LAST	Len	"Elen Margrethe Stangeland"
#   set the mul label to "Elen Margrethe Stangeland"
LAST	Lmul	"Elen Margrethe Stangeland"
#   set the ja label to "エレン・マルグレーテ・スタンゲラン"
LAST	Lja	"エレン・マルグレーテ・スタンゲラン"
#   set the zh label to "埃伦·马尔格雷特·斯坦格兰"
LAST	Lzh	"埃伦·马尔格雷特·斯坦格兰"
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
#   Q141198393 Erik Erikson Stangeland: P40 child = the item just created
Q141198393	P40	LAST	S2600	"6000000011039570406"

# create a new item
CREATE
#   the item just created: set the en label to "Eli Helgesdatter Auestad"
LAST	Len	"Eli Helgesdatter Auestad"
#   set the mul label to "Eli Helgesdatter Auestad"
LAST	Lmul	"Eli Helgesdatter Auestad"
#   set the ja label to "イーライ・ヘルゲスダッテル・アウエスタド"
LAST	Lja	"イーライ・ヘルゲスダッテル・アウエスタド"
#   set the zh label to "伊莱·赫尔盖斯达特·奥埃斯塔德"
LAST	Lzh	"伊莱·赫尔盖斯达特·奥埃斯塔德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003094971035 Eli Helgesdatter Auestad, qualified P1810 subject named as Eli Helgesdatter Auestad
LAST	P2600	"6000000003094971035"	P1810	"Eli Helgesdatter Auestad"
#   P569 date of birth = +1733-00-00T00:00:00Z/9
LAST	P569	+1733-00-00T00:00:00Z/9	S2600	"6000000003094971035"
#   P570 date of death = +1811-00-00T00:00:00Z/9
LAST	P570	+1811-00-00T00:00:00Z/9	S2600	"6000000003094971035"
#   P40 child = Q141223735 Helge Olsen Ytre Lima
LAST	P40	Q141223735	S2600	"6000000003094971035"
#   Q141223735 Helge Olsen Ytre Lima: P25 mother = the item just created
Q141223735	P25	LAST	S2600	"6000000003094971035"

# create a new item
CREATE
#   the item just created: set the en label to "Elly Olivia Frisk"
LAST	Len	"Elly Olivia Frisk"
#   set the mul label to "Elly Olivia Frisk"
LAST	Lmul	"Elly Olivia Frisk"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000178275437038 Elly Olivia Frisk, qualified P1810 subject named as Elly Olivia Frisk
LAST	P2600	"6000000178275437038"	P1810	"Elly Olivia Frisk"
#   P569 date of birth = +1931-00-00T00:00:00Z/9
LAST	P569	+1931-00-00T00:00:00Z/9	S2600	"6000000178275437038"
#   P570 date of death = +1993-00-00T00:00:00Z/9
LAST	P570	+1993-00-00T00:00:00Z/9	S2600	"6000000178275437038"
#   P26 spouse = Q141223733 Hans Bertil Frisk
LAST	P26	Q141223733	S2600	"6000000178275437038"
#   Q141223733 Hans Bertil Frisk: P26 spouse = the item just created
Q141223733	P26	LAST	S2600	"6000000178275437038"

# create a new item
CREATE
#   the item just created: set the en label to "Evelyn Opal Lanska"
LAST	Len	"Evelyn Opal Lanska"
#   set the mul label to "Evelyn Opal Lanska"
LAST	Lmul	"Evelyn Opal Lanska"
#   add a mul alias "Evelyn Opal Tunheim"
LAST	Amul	"Evelyn Opal Tunheim"
#   set the ja label to "エヴリン・オーパル・ランスカ"
LAST	Lja	"エヴリン・オーパル・ランスカ"
#   set the zh label to "伊芙琳·奥帕尔·兰斯卡"
LAST	Lzh	"伊芙琳·奥帕尔·兰斯卡"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000180029283821 Evelyn Opal Lanska, qualified P1810 subject named as Evelyn Opal Tunheim
LAST	P2600	"6000000180029283821"	P1810	"Evelyn Opal Tunheim"
#   P569 date of birth = +1916-07-31T00:00:00Z/11
LAST	P569	+1916-07-31T00:00:00Z/11	S2600	"6000000180029283821"
#   P570 date of death = +1999-04-24T00:00:00Z/11
LAST	P570	+1999-04-24T00:00:00Z/11	S2600	"6000000180029283821"
#   P22 father = Q141168809 Edward Tunheim
LAST	P22	Q141168809	S2600	"6000000180029283821"
#   P25 mother = Q141205894 Agnes Tunheim
LAST	P25	Q141205894	S2600	"6000000180029283821"
#   Q141168809 Edward Tunheim: P40 child = the item just created
Q141168809	P40	LAST	S2600	"6000000180029283821"
#   Q141205894 Agnes Tunheim: P40 child = the item just created
Q141205894	P40	LAST	S2600	"6000000180029283821"
#   the item just created: P735 given name = Q1381706 Evelyn, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q1381706	P1545	"1"	P7452	Q3409033
#   P735 given name = Q7095539 Opal, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q7095539	P1545	"2"	P3831	Q245025
#   P734 family name = Q36927172, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q36927172	P3831	Q2507958

# create a new item
CREATE
#   set the en label to "Hedvig Vendela Maria af Sandeberg"
LAST	Len	"Hedvig Vendela Maria af Sandeberg"
#   set the mul label to "Hedvig Vendela Maria af Sandeberg"
LAST	Lmul	"Hedvig Vendela Maria af Sandeberg"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000021547254896 Hedvig Vendela Maria af Sandeberg, qualified P1810 subject named as Hedvig Vendela Maria af Sandeberg
LAST	P2600	"6000000021547254896"	P1810	"Hedvig Vendela Maria af Sandeberg"
#   P569 date of birth = +1832-08-08T00:00:00Z/11
LAST	P569	+1832-08-08T00:00:00Z/11	S2600	"6000000021547254896"
#   P570 date of death = +1907-01-06T00:00:00Z/11
LAST	P570	+1907-01-06T00:00:00Z/11	S2600	"6000000021547254896"
#   P25 mother = Q141219155 Christina Maria Adelheim
LAST	P25	Q141219155	S2600	"6000000021547254896"
#   Q141219155 Christina Maria Adelheim: P40 child = the item just created
Q141219155	P40	LAST	S2600	"6000000021547254896"
#   the item just created: P735 given name = Q13648620 Hedvig, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q13648620	P1545	"1"	P7452	Q3409033
#   P735 given name = Q325872 Maria, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
LAST	P735	Q325872	P1545	"3"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Helen Frisk"
LAST	Len	"Helen Frisk"
#   set the mul label to "Helen Frisk"
LAST	Lmul	"Helen Frisk"
#   set the ja label to "ヘレン・フリスク"
LAST	Lja	"ヘレン・フリスク"
#   set the zh label to "海伦·弗里斯克"
LAST	Lzh	"海伦·弗里斯克"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000177921459052 Helen Frisk, qualified P1810 subject named as Helen Frisk
LAST	P2600	"6000000177921459052"	P1810	"Helen Frisk"
#   P22 father = Q141223733 Hans Bertil Frisk
LAST	P22	Q141223733	S2600	"6000000177921459052"
#   Q141223733 Hans Bertil Frisk: P40 child = the item just created
Q141223733	P40	LAST	S2600	"6000000177921459052"

# create a new item
CREATE
#   the item just created: set the en label to "Henrik Harmens"
LAST	Len	"Henrik Harmens"
#   set the mul label to "Henrik Harmens"
LAST	Lmul	"Henrik Harmens"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000008831004376 Henrik Harmens, qualified P1810 subject named as Henrik Harmens
LAST	P2600	"6000000008831004376"	P1810	"Henrik Harmens"
#   P569 date of birth = +1656-00-00T00:00:00Z/9
LAST	P569	+1656-00-00T00:00:00Z/9	S2600	"6000000008831004376"
#   P570 date of death = +1737-00-00T00:00:00Z/9
LAST	P570	+1737-00-00T00:00:00Z/9	S2600	"6000000008831004376"
#   P40 child = Q5790728 Gustaf Harmens
LAST	P40	Q5790728	S2600	"6000000008831004376"
#   Q5790728 Gustaf Harmens: P22 father = the item just created
Q5790728	P22	LAST	S2600	"6000000008831004376"
#   the item just created: P735 given name = Q594279 Henrik
LAST	P735	Q594279

# create a new item
CREATE
#   set the en label to "Magdalena Törne"
LAST	Len	"Magdalena Törne"
#   set the mul label to "Magdalena Törne"
LAST	Lmul	"Magdalena Törne"
#   set the ja label to "マグダレーナ・トルネ"
LAST	Lja	"マグダレーナ・トルネ"
#   set the zh label to "马格达莱纳·托尔内"
LAST	Lzh	"马格达莱纳·托尔内"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000008829706074 Magdalena Törne, qualified P1810 subject named as Magdalena Törne
LAST	P2600	"6000000008829706074"	P1810	"Magdalena Törne"
#   P569 date of birth = +1667-00-00T00:00:00Z/9
LAST	P569	+1667-00-00T00:00:00Z/9	S2600	"6000000008829706074"
#   P570 date of death = +1704-00-00T00:00:00Z/9
LAST	P570	+1704-00-00T00:00:00Z/9	S2600	"6000000008829706074"
#   P40 child = Q5790728 Gustaf Harmens
LAST	P40	Q5790728	S2600	"6000000008829706074"
#   Q5790728 Gustaf Harmens: P25 mother = the item just created
Q5790728	P25	LAST	S2600	"6000000008829706074"
#   the item just created: P735 given name = Q842544 Magdalena
LAST	P735	Q842544
#   P734 family name = Q65202241 Törne, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q65202241	P3831	Q28418670

# create a new item
CREATE
#   set the en label to "Ola Svenson Ytre Lima"
LAST	Len	"Ola Svenson Ytre Lima"
#   set the mul label to "Ola Svenson Ytre Lima"
LAST	Lmul	"Ola Svenson Ytre Lima"
#   set the ja label to "オーラ・スヴェンソン・イトレ・リマ"
LAST	Lja	"オーラ・スヴェンソン・イトレ・リマ"
#   set the zh label to "奥拉·斯文松·伊特雷·利马"
LAST	Lzh	"奥拉·斯文松·伊特雷·利马"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005607599800 Ola Svenson Ytre Lima, qualified P1810 subject named as Ola Svenson Ytre Lima
LAST	P2600	"6000000005607599800"	P1810	"Ola Svenson Ytre Lima"
#   P569 date of birth = +1717-00-00T00:00:00Z/9
LAST	P569	+1717-00-00T00:00:00Z/9	S2600	"6000000005607599800"
#   P570 date of death = +1791-00-00T00:00:00Z/9
LAST	P570	+1791-00-00T00:00:00Z/9	S2600	"6000000005607599800"
#   P40 child = Q141223735 Helge Olsen Ytre Lima
LAST	P40	Q141223735	S2600	"6000000005607599800"
#   Q141223735 Helge Olsen Ytre Lima: P22 father = the item just created
Q141223735	P22	LAST	S2600	"6000000005607599800"

# create a new item
CREATE
#   the item just created: set the en label to "Pehr Olsson"
LAST	Len	"Pehr Olsson"
#   set the mul label to "Pehr Olsson"
LAST	Lmul	"Pehr Olsson"
#   set the ja label to "ペール・オルソン"
LAST	Lja	"ペール・オルソン"
#   set the zh label to "佩尔·奥尔松"
LAST	Lzh	"佩尔·奥尔松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000004334845842 Pehr Olsson, qualified P1810 subject named as Pehr Olsson
LAST	P2600	"6000000004334845842"	P1810	"Pehr Olsson"
#   P569 date of birth = +1516-00-00T00:00:00Z/9
LAST	P569	+1516-00-00T00:00:00Z/9	S2600	"6000000004334845842"
#   P570 date of death = +1549-00-00T00:00:00Z/9
LAST	P570	+1549-00-00T00:00:00Z/9	S2600	"6000000004334845842"
#   P22 father = Q141205932 Olof Timmerman
LAST	P22	Q141205932	S2600	"6000000004334845842"
#   P25 mother = Q141205926 NN
LAST	P25	Q141205926	S2600	"6000000004334845842"
#   Q141205932 Olof Timmerman: P40 child = the item just created
Q141205932	P40	LAST	S2600	"6000000004334845842"
#   Q141205926 NN: P40 child = the item just created
Q141205926	P40	LAST	S2600	"6000000004334845842"
#   the item just created: P735 given name = Q18606368 Pehr
LAST	P735	Q18606368

# create a new item
CREATE
#   set the en label to "Rasmus (Paulson) Borsheim"
LAST	Len	"Rasmus (Paulson) Borsheim"
#   set the mul label to "Rasmus (Paulson) Borsheim"
LAST	Lmul	"Rasmus (Paulson) Borsheim"
#   set the ja label to "ラスムス・ポールソン・ボルスハイム"
LAST	Lja	"ラスムス・ポールソン・ボルスハイム"
#   set the zh label to "拉斯穆斯·帕乌尔松·博尔斯海姆"
LAST	Lzh	"拉斯穆斯·帕乌尔松·博尔斯海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000020344842981 Rasmus (Paulson) Borsheim, qualified P1810 subject named as Rasmus (Paulson) Borsheim
LAST	P2600	"6000000020344842981"	P1810	"Rasmus (Paulson) Borsheim"
#   P569 date of birth = +1857-07-19T00:00:00Z/11
LAST	P569	+1857-07-19T00:00:00Z/11	S2600	"6000000020344842981"
#   P570 date of death = +1938-04-02T00:00:00Z/11
LAST	P570	+1938-04-02T00:00:00Z/11	S2600	"6000000020344842981"
#   P26 spouse = Q141223853 Rakel Rasmusdottir Borsheim
LAST	P26	Q141223853	S2600	"6000000020344842981"
#   Q141223853 Rakel Rasmusdottir Borsheim: P26 spouse = the item just created
Q141223853	P26	LAST	S2600	"6000000020344842981"

# create a new item
CREATE
#   the item just created: set the en label to "Sissel Tomine Pedersdatter Nyvold"
LAST	Len	"Sissel Tomine Pedersdatter Nyvold"
#   set the mul label to "Sissel Tomine Pedersdatter Nyvold"
LAST	Lmul	"Sissel Tomine Pedersdatter Nyvold"
#   add a mul alias "Sissel Tomine Pedersdatter Holmesland"
LAST	Amul	"Sissel Tomine Pedersdatter Holmesland"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000021198413026 Sissel Tomine Pedersdatter Nyvold, qualified P1810 subject named as Sissel Tomine Pedersdatter Holmesland
LAST	P2600	"6000000021198413026"	P1810	"Sissel Tomine Pedersdatter Holmesland"
#   P569 date of birth = +1829-05-24T00:00:00Z/11
LAST	P569	+1829-05-24T00:00:00Z/11	S2600	"6000000021198413026"
#   P570 date of death = +1884-09-16T00:00:00Z/11
LAST	P570	+1884-09-16T00:00:00Z/11	S2600	"6000000021198413026"
#   P40 child = Q138474188 Hans Syvertsen Nyvold
LAST	P40	Q138474188	S2600	"6000000021198413026"
#   Q138474188 Hans Syvertsen Nyvold: P25 mother = the item just created
Q138474188	P25	LAST	S2600	"6000000021198413026"
#   the item just created: P735 given name = Q4571101 Sissel, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q4571101	P1545	"1"	P7452	Q3409033
#   P735 given name = Q19414233 Tomine, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q19414233	P1545	"2"	P3831	Q245025
#   add a mul alias "Cecilie Tomine Pedersdatter Holmesland Nyvold"
LAST	Amul	"Cecilie Tomine Pedersdatter Holmesland Nyvold"
#   add a mul alias "Sissel Tomine Nyvold"
LAST	Amul	"Sissel Tomine Nyvold"

# create a new item
CREATE
#   set the en label to "Syvert Kristian Hansen Nyvold"
LAST	Len	"Syvert Kristian Hansen Nyvold"
#   set the mul label to "Syvert Kristian Hansen Nyvold"
LAST	Lmul	"Syvert Kristian Hansen Nyvold"
#   add a mul alias "Syvert Kristian Hansen Stusvig"
LAST	Amul	"Syvert Kristian Hansen Stusvig"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000021198171670 Syvert Kristian Hansen Nyvold, qualified P1810 subject named as Syvert Kristian Hansen Stusvig
LAST	P2600	"6000000021198171670"	P1810	"Syvert Kristian Hansen Stusvig"
#   P569 date of birth = +1829-05-24T00:00:00Z/11
LAST	P569	+1829-05-24T00:00:00Z/11	S2600	"6000000021198171670"
#   P570 date of death = +1899-12-15T00:00:00Z/11
LAST	P570	+1899-12-15T00:00:00Z/11	S2600	"6000000021198171670"
#   P40 child = Q138474188 Hans Syvertsen Nyvold
LAST	P40	Q138474188	S2600	"6000000021198171670"
#   Q138474188 Hans Syvertsen Nyvold: P22 father = the item just created
Q138474188	P22	LAST	S2600	"6000000021198171670"
#   the item just created: P735 given name = Q30643295 Syvert, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q30643295	P1545	"1"	P7452	Q3409033
#   P735 given name = Q12794332 Kristian, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q12794332	P1545	"2"	P3831	Q245025
#   add a mul alias "Syvert Christian Hansen Nyvold"
LAST	Amul	"Syvert Christian Hansen Nyvold"
#   add a mul alias "Syvert Kristian Nyvold"
LAST	Amul	"Syvert Kristian Nyvold"

# create a new item
CREATE
#   set the en label to "Villum Jonsen Gautun"
LAST	Len	"Villum Jonsen Gautun"
#   set the mul label to "Villum Jonsen Gautun"
LAST	Lmul	"Villum Jonsen Gautun"
#   set the ja label to "ヴィルム・ヨンセン・ガウトン"
LAST	Lja	"ヴィルム・ヨンセン・ガウトン"
#   set the zh label to "维卢姆·永森·加乌通"
LAST	Lzh	"维卢姆·永森·加乌通"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003315775479 Villum Jonsen Gautun, qualified P1810 subject named as Villum Jonsen Gautun
LAST	P2600	"6000000003315775479"	P1810	"Villum Jonsen Gautun"
#   P569 date of birth = +1562-00-00T00:00:00Z/9
LAST	P569	+1562-00-00T00:00:00Z/9	S2600	"6000000003315775479"
#   P570 date of death = +1643-00-00T00:00:00Z/9
LAST	P570	+1643-00-00T00:00:00Z/9	S2600	"6000000003315775479"
#   P26 spouse = Q141223851 Ragnhild Østensd Stokka
LAST	P26	Q141223851	S2600	"6000000003315775479"
#   P40 child = Q141216611 Jon Villumson Raunes
LAST	P40	Q141216611	S2600	"6000000003315775479"
#   Q141223851 Ragnhild Østensd Stokka: P26 spouse = the item just created
Q141223851	P26	LAST	S2600	"6000000003315775479"
#   Q141216611 Jon Villumson Raunes: P22 father = the item just created
Q141216611	P22	LAST	S2600	"6000000003315775479"
#   the item just created: P735 given name = Q22703948 Villum
LAST	P735	Q22703948
#   add a mul alias "Villum Gautun"
LAST	Amul	"Villum Gautun"

# create a new item
CREATE
#   set the en label to "Ådne Olsson Lima Kyllingstad. Lima"
LAST	Len	"Ådne Olsson Lima Kyllingstad. Lima"
#   set the mul label to "Ådne Olsson Lima Kyllingstad. Lima"
LAST	Lmul	"Ådne Olsson Lima Kyllingstad. Lima"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000182737012832 Ådne Olsson Lima Kyllingstad. Lima, qualified P1810 subject named as Ådne Olsson Lima Kyllingstad. Lima
LAST	P2600	"6000000182737012832"	P1810	"Ådne Olsson Lima Kyllingstad. Lima"
#   P569 date of birth = +1829-01-29T00:00:00Z/11
LAST	P569	+1829-01-29T00:00:00Z/11	S2600	"6000000182737012832"
#   P22 father = Q141223849 Ola Helgeson Lima
LAST	P22	Q141223849	S2600	"6000000182737012832"
#   Q141223849 Ola Helgeson Lima: P40 child = the item just created
Q141223849	P40	LAST	S2600	"6000000182737012832"
#   Q141223837 Gustav Petersson Lejon: P26 spouse = Q141223838 Hafrid Sigtryggsdotter Boberg
Q141223837	P26	Q141223838	S2600	"6000000003414711727"
#   P735 given name = Q746076
Q141223837	P735	Q746076
#   Q141223834 Erik Monsen Bjorland: P26 spouse = Q141223846 Marit Bjørnsdatter Bjorland
Q141223834	P26	Q141223846	S2600	"6000000003491998017"
#   Q141223838 Hafrid Sigtryggsdotter Boberg: P26 spouse = Q141223837 Gustav Petersson Lejon
Q141223838	P26	Q141223837	S2600	"6000000003559734445"
#   P734 family name = Q27132293 Boberg
Q141223838	P734	Q27132293
#   Q141223846 Marit Bjørnsdatter Bjorland: P26 spouse = Q141223834 Erik Monsen Bjorland
Q141223846	P26	Q141223834	S2600	"6000000005609529475"
#   Q141223503 Anne Berta Osmundsdatter Nese: P40 child = Q141223853 Rakel Rasmusdottir Borsheim
Q141223503	P40	Q141223853	S2600	"6000000005609547544"
#   Q141223845 Maria Louisa Silfverstolpe: P40 child = Q141223830 Charlotta Eleonora Falkenberg
Q141223845	P40	Q141223830	S2600	"6000000006127758500"
#   Q141223836 Eva Augusta Löwen: P40 child = Q141223839 Jeannette Constance Tigerstedt
Q141223836	P40	Q141223839	S2600	"6000000012839208314"
#   Q141223830 Charlotta Eleonora Falkenberg: P25 mother = Q141223845 Maria Louisa Silfverstolpe
Q141223830	P25	Q141223845	S2600	"6000000019325206143"
#   Q141223853 Rakel Rasmusdottir Borsheim: P735 given name = Q16424094 Rakel, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141223853	P735	Q16424094	P1545	"1"	P7452	Q3409033
#   P734 family name = Q37328187
Q141223853	P734	Q37328187
#   Q141223839 Jeannette Constance Tigerstedt: P25 mother = Q141223836 Eva Augusta Löwen
Q141223839	P25	Q141223836	S2600	"6000000026930814601"
#   Q141219250 Inger Sørensdatter Lima: P40 child = Q141223849 Ola Helgeson Lima
Q141219250	P40	Q141223849	S2600	"6000000065991527068"
#   Q141223849 Ola Helgeson Lima: P735 given name = Q96675523 Ola
Q141223849	P735	Q96675523
#   P734 family name = Q11255517 Lima
Q141223849	P734	Q11255517

