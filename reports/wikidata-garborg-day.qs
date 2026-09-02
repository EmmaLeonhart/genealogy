# ========================================================================
# NAME ITEMS FIRST. One file, her instruction of 2026-08-30 -- there is no
# longer a second batch to remember to run.
# ========================================================================
# Name items the Garborg batches need, AND the statements that use them.
#
# Each CREATE is followed by `Qperson  Pprop  LAST` for every bearer who
# ALREADY holds a QID -- LAST is exactly how you point at what was just
# created. A person this run is also CREATING cannot be linked here, because
# LAST would then name the person; they wait for the next run.
#
# A patronymic is its own item even where the spelling exists as a given
# name: CLAUDE.md, one name item per USAGE. Emma's Q141152710 Aadnesson is
# the pattern -- labels, P31, nothing else.

# Garfve -- family, 3 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Garfve"
LAST	Len	"Garfve"
#   set the mul label to "Garfve"
LAST	Lmul	"Garfve"
#   set the en description to "family name"
LAST	Den	"family name"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q141224010 Harlan Roger Garfve: P734 family name = the item just created
Q141224010	P734	LAST	S2600	"6000000019472886300"
#   Q141189056 Bella Jeanette Garfve: P734 family name = the item just created, qualified P3831 object of statement has role Q28418670 married name
Q141189056	P734	LAST	P3831	Q28418670	S2600	"6000000039507887815"
#   Q141224188 Hjalmer Morris Garfve: P734 family name = the item just created
Q141224188	P734	LAST	S2600	"6000000039508406904"

# Hakunge -- family, 3 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Hakunge"
LAST	Len	"Hakunge"
#   set the mul label to "Hakunge"
LAST	Lmul	"Hakunge"
#   set the en description to "family name"
LAST	Den	"family name"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q141219054 Carl Emil Cronhielm af Hakunge: P734 family name = the item just created
Q141219054	P734	LAST	S2600	"6000000008178453589"
#   Q110304582 Gustava Magdalena Cronhielm af Hakunge: P734 family name = the item just created
Q110304582	P734	LAST	S2600	"6000000012959992080"
#   Q4938400 Christina Charlotta Cronhielm af Hakunge: P734 family name = the item just created
Q4938400	P734	LAST	S2600	"6000000020584191181"

# Hansen -- patronymic, 3 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Hansen"
LAST	Len	"Hansen"
#   set the mul label to "Hansen"
LAST	Lmul	"Hansen"
#   set the en description to "patronymic"
LAST	Den	"patronymic"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141223961 Syvert Kristian Hansen Nyvold: P5056 patronym or matronym = the item just created
Q141223961	P5056	LAST	S2600	"6000000021198171670"
#   Q141250244 Rasmus Hansen Nord-Varhaug: P5056 patronym or matronym = the item just created, qualified P144 based on Q141216381 Hans Rasmussen Låge-Håland
Q141250244	P5056	LAST	P144	Q141216381	S2600	"6000000087451690855"
#   Q141200127 Ådne Hansen Grøtheim: P5056 patronym or matronym = the item just created, qualified P144 based on Q141216607 Hans Erikson Øvre Håland
Q141200127	P5056	LAST	P144	Q141216607	S2600	"6000000225229617898"

# 326 more name items are needed and wait for a later
# run -- 3 a day is her cap, not a limit of the data:
#   Hansson (patronymic), 3 bearer(s)
#   Helgesen (patronymic), 3 bearer(s)
#   Høle (family), 3 bearer(s)
#   Ingebretsdatter (patronymic), 3 bearer(s)
#   Johansdotter (patronymic), 3 bearer(s)
#   Knutsdatter (patronymic), 3 bearer(s)
#   Kristiansen (patronymic), 3 bearer(s)
#   Magnusson (patronymic), 3 bearer(s)
#   Røyneberg (family), 3 bearer(s)
#   Söfdeborg (family), 3 bearer(s)
#   Tollefson (patronymic), 3 bearer(s)
#   Ugla (family), 3 bearer(s)
#   ... and 314 more

# ========================================================================
# THE DAY'S PEOPLE
# ========================================================================

# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   2665 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   set the zh label to "伊丽莎白·翁·萨韦兰德"
Q110547994	Lzh	"伊丽莎白·翁·萨韦兰德"
#   set the ko label to "에리사베트 본 사베란드"
Q110547994	Lko	"에리사베트 본 사베란드"
#   Q6188549 Sten Bosson Natt och Dag till Ekhult: set the ja label to "ステン・ボソン・ナト・オク・ダグ"
Q6188549	Lja	"ステン・ボソン・ナト・オク・ダグ"
#   set the zh label to "斯滕·博松·纳特·奥克·达格"
Q6188549	Lzh	"斯滕·博松·纳特·奥克·达格"
#   set the ko label to "스텐 보손 나트 오츠 닥"
Q6188549	Lko	"스텐 보손 나트 오츠 닥"
#   set the ja label to "グイゲス・ガイ・デ・フォレズ・ヴィイ"
Q30879127	Lja	"グイゲス・ガイ・デ・フォレズ・ヴィイ"
#   set the zh label to "古伊盖斯·盖伊·德·福雷兹·维伊"
Q30879127	Lzh	"古伊盖斯·盖伊·德·福雷兹·维伊"
#   set the ko label to "귀게스 구이 데 포레즈 비이"
Q30879127	Lko	"귀게스 구이 데 포레즈 비이"
#   Q73763413 Margareta Johansdotter Wallensteen: add a mul alias "Margareta Johansdotter Wallensteen"
Q73763413	Amul	"Margareta Johansdotter Wallensteen"
#   set the ja label to "マルガレータ・ヴァルステニウス"
Q73763413	Lja	"マルガレータ・ヴァルステニウス"
#   set the zh label to "瑪格麗塔·瓦尔斯特尼乌斯"
Q73763413	Lzh	"瑪格麗塔·瓦尔斯特尼乌斯"
#   set the ko label to "마르가레타 와르스테뉴스"
Q73763413	Lko	"마르가레타 와르스테뉴스"
#   Q5626011 Gustaf Duwall: set the ja label to "グスタフ・ドヴァル"
Q5626011	Lja	"グスタフ・ドヴァル"
#   set the zh label to "古斯塔夫·杜瓦尔"
Q5626011	Lzh	"古斯塔夫·杜瓦尔"
#   set the ko label to "구스타프 두와르르"
Q5626011	Lko	"구스타프 두와르르"

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Abraham Felthuus Bøe"
LAST	Len	"Abraham Felthuus Bøe"
#   set the mul label to "Abraham Felthuus Bøe"
LAST	Lmul	"Abraham Felthuus Bøe"
#   set the ja label to "アブラハム・フェルトウス・ボエ"
LAST	Lja	"アブラハム・フェルトウス・ボエ"
#   set the zh label to "亚伯拉罕·费尔图乌斯·博埃"
LAST	Lzh	"亚伯拉罕·费尔图乌斯·博埃"
#   set the ko label to "압라함 펠투우스 뵈에"
LAST	Lko	"압라함 펠투우스 뵈에"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000001850030895 Abraham Felthuus Bøe, qualified P1810 subject named as Abraham Felthuus Bøe
LAST	P2600	"6000000001850030895"	P1810	"Abraham Felthuus Bøe"
#   P569 date of birth = +1788-02-06T00:00:00Z/11
LAST	P569	+1788-02-06T00:00:00Z/11	S2600	"6000000001850030895"
#   P570 date of death = +1862-12-15T00:00:00Z/11
LAST	P570	+1862-12-15T00:00:00Z/11	S2600	"6000000001850030895"
#   P22 father = Q141244094 Gunder Asbjørnsen Bøe
LAST	P22	Q141244094	S2600	"6000000001850030895"
#   Q141244094 Gunder Asbjørnsen Bøe: P40 child = the item just created
Q141244094	P40	LAST	S2600	"6000000001850030895"
#   the item just created: P735 given name = Q4055996 Abraham, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q4055996	P1545	"1"	P7452	Q3409033
#   P734 family name = Q5005210
LAST	P734	Q5005210

# create a new item
CREATE
#   set the en label to "Birgit Agnes Helena Rehn"
LAST	Len	"Birgit Agnes Helena Rehn"
#   set the mul label to "Birgit Agnes Helena Rehn"
LAST	Lmul	"Birgit Agnes Helena Rehn"
#   add a mul alias "Birgit Agnes Helena Mankell"
LAST	Amul	"Birgit Agnes Helena Mankell"
#   set the ja label to "ビルギット・アグネス・ヘレナ・レン"
LAST	Lja	"ビルギット・アグネス・ヘレナ・レン"
#   set the zh label to "比尔吉特·阿格内斯·海伦娜·雷恩"
LAST	Lzh	"比尔吉特·阿格内斯·海伦娜·雷恩"
#   set the ko label to "비르기트 악네스 헤레나 레흐느"
LAST	Lko	"비르기트 악네스 헤레나 레흐느"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000017425538435 Birgit Agnes Helena Rehn, qualified P1810 subject named as Birgit Agnes Helena Mankell
LAST	P2600	"6000000017425538435"	P1810	"Birgit Agnes Helena Mankell"
#   P569 date of birth = +1918-00-00T00:00:00Z/9
LAST	P569	+1918-00-00T00:00:00Z/9	S2600	"6000000017425538435"
#   P570 date of death = +2004-00-00T00:00:00Z/9
LAST	P570	+2004-00-00T00:00:00Z/9	S2600	"6000000017425538435"
#   P22 father = Q329253 Ivar Henning Mankell
LAST	P22	Q329253	S2600	"6000000017425538435"
#   P25 mother = Q141244080 Agnes Karolina Lindblom
LAST	P25	Q141244080	S2600	"6000000017425538435"
#   Q329253 Ivar Henning Mankell: P40 child = the item just created
Q329253	P40	LAST	S2600	"6000000017425538435"
#   Q141244080 Agnes Karolina Lindblom: P40 child = the item just created
Q141244080	P40	LAST	S2600	"6000000017425538435"
#   the item just created: P735 given name = Q865198 Birgit, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q865198	P1545	"1"	P7452	Q3409033
#   P735 given name = Q394431 Agnes, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q394431	P1545	"2"	P3831	Q245025
#   P735 given name = Q1035239 Helena, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1035239	P1545	"3"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Catharina Abrahamsdotter Burman"
LAST	Len	"Catharina Abrahamsdotter Burman"
#   set the mul label to "Catharina Abrahamsdotter Burman"
LAST	Lmul	"Catharina Abrahamsdotter Burman"
#   set the ja label to "カタリーナ・アブラハムスドッテル・ブルマン"
LAST	Lja	"カタリーナ・アブラハムスドッテル・ブルマン"
#   set the zh label to "卡塔里娜·阿布拉哈姆斯多特·布尔曼"
LAST	Lzh	"卡塔里娜·阿布拉哈姆斯多特·布尔曼"
#   set the ko label to "카타리나 압라함스도테르 부르만"
LAST	Lko	"카타리나 압라함스도테르 부르만"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003966326458 Catharina Abrahamsdotter Burman, qualified P1810 subject named as Catharina Abrahamsdotter Burman
LAST	P2600	"6000000003966326458"	P1810	"Catharina Abrahamsdotter Burman"
#   P569 date of birth = +1691-01-19T00:00:00Z/11
LAST	P569	+1691-01-19T00:00:00Z/11	S2600	"6000000003966326458"
#   P570 date of death = +1756-00-00T00:00:00Z/9
LAST	P570	+1756-00-00T00:00:00Z/9	S2600	"6000000003966326458"
#   P22 father = Q16165489 Abraham Laurentii Burman
LAST	P22	Q16165489	S2600	"6000000003966326458"
#   P40 child = Q19976400 Abraham Burensund
LAST	P40	Q19976400	S2600	"6000000003966326458"
#   Q16165489 Abraham Laurentii Burman: P40 child = the item just created
Q16165489	P40	LAST	S2600	"6000000003966326458"
#   Q19976400 Abraham Burensund: P25 mother = the item just created
Q19976400	P25	LAST	S2600	"6000000003966326458"
#   the item just created: P735 given name = Q17317997 Catharina
LAST	P735	Q17317997
#   P734 family name = Q450765 Burman, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q450765	P3831	Q28418670
#   add a mul alias "Catharina Burman"
LAST	Amul	"Catharina Burman"

# create a new item
CREATE
#   set the en label to "Ebba Gustava Charlotta Uggla"
LAST	Len	"Ebba Gustava Charlotta Uggla"
#   set the mul label to "Ebba Gustava Charlotta Uggla"
LAST	Lmul	"Ebba Gustava Charlotta Uggla"
#   set the ja label to "エバ・グスタヴァ・カルロタ・ウグラ"
LAST	Lja	"エバ・グスタヴァ・カルロタ・ウグラ"
#   set the zh label to "埃巴·古斯塔娃·卡尔洛塔·乌格拉"
LAST	Lzh	"埃巴·古斯塔娃·卡尔洛塔·乌格拉"
#   set the ko label to "에바 구스타바 차르로타 욱라"
LAST	Lko	"에바 구스타바 차르로타 욱라"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000006128061904 Ebba Gustava Charlotta Uggla, qualified P1810 subject named as Ebba Gustava Charlotta Uggla
LAST	P2600	"6000000006128061904"	P1810	"Ebba Gustava Charlotta Uggla"
#   P569 date of birth = +1785-09-26T00:00:00Z/11
LAST	P569	+1785-09-26T00:00:00Z/11	S2600	"6000000006128061904"
#   P570 date of death = +1844-07-11T00:00:00Z/11
LAST	P570	+1844-07-11T00:00:00Z/11	S2600	"6000000006128061904"
#   P26 spouse = Q5813639 Claes Fredrik Claesson Horn af Åminne
LAST	P26	Q5813639	S2600	"6000000006128061904"
#   Q5813639 Claes Fredrik Claesson Horn af Åminne: P26 spouse = the item just created
Q5813639	P26	LAST	S2600	"6000000006128061904"
#   the item just created: P735 given name = Q2242896 Ebba, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q2242896	P1545	"1"	P7452	Q3409033
#   P735 given name = Q21144392 Gustava, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q21144392	P1545	"2"	P3831	Q245025
#   P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1067071	P1545	"3"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Elen Pedersdatter Vatnamot"
LAST	Len	"Elen Pedersdatter Vatnamot"
#   set the mul label to "Elen Pedersdatter Vatnamot"
LAST	Lmul	"Elen Pedersdatter Vatnamot"
#   add a mul alias "Elen Pedersdatter Herikstad"
LAST	Amul	"Elen Pedersdatter Herikstad"
#   set the ja label to "エレン・ペーデシュダッテル・ヴァトナモト"
LAST	Lja	"エレン・ペーデシュダッテル・ヴァトナモト"
#   set the zh label to "埃伦·佩德斯达特·瓦特纳莫特"
LAST	Lzh	"埃伦·佩德斯达特·瓦特纳莫特"
#   set the ko label to "에렌 페데르스다테르 바트나모트"
LAST	Lko	"에렌 페데르스다테르 바트나모트"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005607089288 Elen Pedersdatter Vatnamot, qualified P1810 subject named as Elen Pedersdatter Herikstad
LAST	P2600	"6000000005607089288"	P1810	"Elen Pedersdatter Herikstad"
#   P569 date of birth = +1699-00-00T00:00:00Z/9
LAST	P569	+1699-00-00T00:00:00Z/9	S2600	"6000000005607089288"
#   P40 child = Q141216647 Tollef Mattiasson Fotland
LAST	P40	Q141216647	S2600	"6000000005607089288"
#   Q141216647 Tollef Mattiasson Fotland: P25 mother = the item just created
Q141216647	P25	LAST	S2600	"6000000005607089288"
#   the item just created: P735 given name = Q11967041 Elen
LAST	P735	Q11967041
#   P734 family name = Q122836741, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q122836741	P3831	Q2507958
#   add a mul alias "Elen Vatnamot"
LAST	Amul	"Elen Vatnamot"

# create a new item
CREATE
#   set the en label to "Elisabet Zachariasdotter Plantin"
LAST	Len	"Elisabet Zachariasdotter Plantin"
#   set the mul label to "Elisabet Zachariasdotter Plantin"
LAST	Lmul	"Elisabet Zachariasdotter Plantin"
#   set the ja label to "エリーザベト・ザカリアスドッテル・プランティン"
LAST	Lja	"エリーザベト・ザカリアスドッテル・プランティン"
#   set the zh label to "伊丽莎白·扎卡里阿斯多特·普兰廷"
LAST	Lzh	"伊丽莎白·扎卡里阿斯多特·普兰廷"
#   set the ko label to "에리사베트 자차리아스도테르 프란틴"
LAST	Lko	"에리사베트 자차리아스도테르 프란틴"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000000159955623 Elisabet Zachariasdotter Plantin, qualified P1810 subject named as Elisabet Zachariasdotter Plantin
LAST	P2600	"6000000000159955623"	P1810	"Elisabet Zachariasdotter Plantin"
#   P569 date of birth = +1670-09-00T00:00:00Z/10
LAST	P569	+1670-09-00T00:00:00Z/10	S2600	"6000000000159955623"
#   P570 date of death = +1740-04-04T00:00:00Z/11
LAST	P570	+1740-04-04T00:00:00Z/11	S2600	"6000000000159955623"
#   P26 spouse = Q16165489 Abraham Laurentii Burman
LAST	P26	Q16165489	S2600	"6000000000159955623"
#   Q16165489 Abraham Laurentii Burman: P26 spouse = the item just created
Q16165489	P26	LAST	S2600	"6000000000159955623"
#   the item just created: P735 given name = Q16423275 Elisabet
LAST	P735	Q16423275
#   add a mul alias "Elisabet Plantin"
LAST	Amul	"Elisabet Plantin"

# create a new item
CREATE
#   set the en label to "Elisabeth Westius"
LAST	Len	"Elisabeth Westius"
#   set the mul label to "Elisabeth Westius"
LAST	Lmul	"Elisabeth Westius"
#   set the ja label to "エリーザベト・ヴェスティウス"
LAST	Lja	"エリーザベト・ヴェスティウス"
#   set the zh label to "伊丽莎白·韦斯蒂乌斯"
LAST	Lzh	"伊丽莎白·韦斯蒂乌斯"
#   set the ko label to "에리사베트 웨스튜스"
LAST	Lko	"에리사베트 웨스튜스"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000026434774123 Elisabeth Westius, qualified P1810 subject named as Elisabeth Westius
LAST	P2600	"6000000026434774123"	P1810	"Elisabeth Westius"
#   P40 child = Q6066129 Johan Martin Reftelius
LAST	P40	Q6066129	S2600	"6000000026434774123"
#   Q6066129 Johan Martin Reftelius: P25 mother = the item just created
Q6066129	P25	LAST	S2600	"6000000026434774123"
#   the item just created: P735 given name = Q63611044 Elisabeth
LAST	P735	Q63611044
#   add a mul alias "Westin Westius"
LAST	Amul	"Westin Westius"

# create a new item
CREATE
#   set the en label to "Gunhild Øysteinsdotter Kvavik"
LAST	Len	"Gunhild Øysteinsdotter Kvavik"
#   set the mul label to "Gunhild Øysteinsdotter Kvavik"
LAST	Lmul	"Gunhild Øysteinsdotter Kvavik"
#   set the ja label to "グンヒルド・オイステインスドッテル・クヴァヴィク"
LAST	Lja	"グンヒルド・オイステインスドッテル・クヴァヴィク"
#   set the zh label to "贡希尔德·奥伊斯特因斯多特·克瓦维克"
LAST	Lzh	"贡希尔德·奥伊斯特因斯多特·克瓦维克"
#   set the ko label to "군힐드 외이스테인스도테르 크바비크"
LAST	Lko	"군힐드 외이스테인스도테르 크바비크"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000004569616464 Gunhild Øysteinsdotter Kvavik, qualified P1810 subject named as Gunhild Øysteinsdotter Skofteland
LAST	P2600	"6000000004569616464"	P1810	"Gunhild Øysteinsdotter Skofteland"
#   P569 date of birth = +1465-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P569	+1465-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"6000000004569616464"
#   P570 date of death = +1530-00-00T00:00:00Z/9, qualified P1319 earliest date +1530-00-00T00:00:00Z/9
LAST	P570	+1530-00-00T00:00:00Z/9	P1319	+1530-00-00T00:00:00Z/9	S2600	"6000000004569616464"
#   P26 spouse = Q141242383 Bjørn Gunnbjørnsson Kvåvig
LAST	P26	Q141242383	S2600	"6000000004569616464"
#   P40 child = Q141250248 Signe Bjørnsdotter Kvavik
LAST	P40	Q141250248	S2600	"6000000004569616464"
#   Q141242383 Bjørn Gunnbjørnsson Kvåvig: P26 spouse = the item just created
Q141242383	P26	LAST	S2600	"6000000004569616464"
#   Q141250248 Signe Bjørnsdotter Kvavik: P25 mother = the item just created
Q141250248	P25	LAST	S2600	"6000000004569616464"
#   the item just created: P735 given name = Q2634697 Gunhild
LAST	P735	Q2634697
#   add a mul alias "Kvaavig Skofteland"
LAST	Amul	"Kvaavig Skofteland"

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
#   set the ko label to "조한나 헨리에타 투레스도테르 리빙 아프 코베르그"
LAST	Lko	"조한나 헨리에타 투레스도테르 리빙 아프 코베르그"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000015119258311 Johanna Henrietta Turesdotter Ribbing af Koberg, qualified P1810 subject named as Johanna Henrietta Turesdotter Ribbing af Koberg
LAST	P2600	"6000000015119258311"	P1810	"Johanna Henrietta Turesdotter Ribbing af Koberg"
#   P569 date of birth = +1778-11-26T00:00:00Z/11
LAST	P569	+1778-11-26T00:00:00Z/11	S2600	"6000000015119258311"
#   P570 date of death = +1845-01-25T00:00:00Z/11, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P570	+1845-01-25T00:00:00Z/11	P1480	Q5727902	S2600	"6000000015119258311"
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
#   set the ko label to "조흐느 오테르손 도켄"
LAST	Lko	"조흐느 오테르손 도켄"
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
#   set the en label to "Julie Wilkens Engebretsen"
LAST	Len	"Julie Wilkens Engebretsen"
#   set the mul label to "Julie Wilkens Engebretsen"
LAST	Lmul	"Julie Wilkens Engebretsen"
#   add a mul alias "Julie Wilkens"
LAST	Amul	"Julie Wilkens"
#   set the ja label to "ジュリー・ヴィルケンス・エンゲブレトセン"
LAST	Lja	"ジュリー・ヴィルケンス・エンゲブレトセン"
#   set the zh label to "朱莉·维尔肯斯·恩盖布雷特森"
LAST	Lzh	"朱莉·维尔肯斯·恩盖布雷特森"
#   set the ko label to "주리에 위르켄스 에에브레첸"
LAST	Lko	"주리에 위르켄스 에에브레첸"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000036729993087 Julie Wilkens Engebretsen, qualified P1810 subject named as Julie Wilkens
LAST	P2600	"6000000036729993087"	P1810	"Julie Wilkens"
#   P569 date of birth = +1853-06-08T00:00:00Z/11
LAST	P569	+1853-06-08T00:00:00Z/11	S2600	"6000000036729993087"
#   P570 date of death = +1929-03-20T00:00:00Z/11
LAST	P570	+1929-03-20T00:00:00Z/11	S2600	"6000000036729993087"
#   P40 child = Q141216453 Aagot Garborg Koloboff
LAST	P40	Q141216453	S2600	"6000000036729993087"
#   Q141216453 Aagot Garborg Koloboff: P25 mother = the item just created
Q141216453	P25	LAST	S2600	"6000000036729993087"
#   the item just created: P735 given name = Q15725563 Julie
LAST	P735	Q15725563
#   P734 family name = Q5377462 Engebretsen, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q5377462	P3831	Q28418670

# create a new item
CREATE
#   set the en label to "Kornelius Moen"
LAST	Len	"Kornelius Moen"
#   set the mul label to "Kornelius Moen"
LAST	Lmul	"Kornelius Moen"
#   set the ja label to "コルネリウス・モーエン"
LAST	Lja	"コルネリウス・モーエン"
#   set the zh label to "科尔内利乌斯·莫恩"
LAST	Lzh	"科尔内利乌斯·莫恩"
#   set the ko label to "코르네류스 묀"
LAST	Lko	"코르네류스 묀"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000225376647971 Kornelius Moen, qualified P1810 subject named as Kornelius Moen
LAST	P2600	"6000000225376647971"	P1810	"Kornelius Moen"
#   P26 spouse = Q141219058 Elisabet Rasmusdatter Moen
LAST	P26	Q141219058	S2600	"6000000225376647971"
#   Q141219058 Elisabet Rasmusdatter Moen: P26 spouse = the item just created
Q141219058	P26	LAST	S2600	"6000000225376647971"
#   the item just created: P735 given name = Q17518394 Kornelius
LAST	P735	Q17518394
#   P734 family name = Q16934183 Moen
LAST	P734	Q16934183

# create a new item
CREATE
#   set the en label to "Lydik Rasmussen Amdal"
LAST	Len	"Lydik Rasmussen Amdal"
#   set the mul label to "Lydik Rasmussen Amdal"
LAST	Lmul	"Lydik Rasmussen Amdal"
#   set the ja label to "リディク・ラスムセン・アムダル"
LAST	Lja	"リディク・ラスムセン・アムダル"
#   set the zh label to "利迪克·拉斯穆森·阿姆达尔"
LAST	Lzh	"利迪克·拉斯穆森·阿姆达尔"
#   set the ko label to "리디크 라스무센 암달"
LAST	Lko	"리디크 라스무센 암달"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000023605569477 Lydik Rasmussen Amdal, qualified P1810 subject named as Lydik Rasmussen Amdal
LAST	P2600	"6000000023605569477"	P1810	"Lydik Rasmussen Amdal"
#   P569 date of birth = +1656-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P569	+1656-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"6000000023605569477"
#   P570 date of death = +1682-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P570	+1682-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"6000000023605569477"
#   P25 mother = Q141223551 Ragnhild Ingebretsdatter Voster
LAST	P25	Q141223551	S2600	"6000000023605569477"
#   Q141223551 Ragnhild Ingebretsdatter Voster: P40 child = the item just created
Q141223551	P40	LAST	S2600	"6000000023605569477"
#   the item just created: P734 family name = Q37478260
LAST	P734	Q37478260

# create a new item
CREATE
#   set the en label to "Mattias Tollefsen Vatnamot"
LAST	Len	"Mattias Tollefsen Vatnamot"
#   set the mul label to "Mattias Tollefsen Vatnamot"
LAST	Lmul	"Mattias Tollefsen Vatnamot"
#   set the ja label to "マティアス・トッレヴセン・ヴァトナモト"
LAST	Lja	"マティアス・トッレヴセン・ヴァトナモト"
#   set the zh label to "马蒂阿斯·托勒夫森·瓦特纳莫特"
LAST	Lzh	"马蒂阿斯·托勒夫森·瓦特纳莫特"
#   set the ko label to "마티아스 톨레프센 바트나모트"
LAST	Lko	"마티아스 톨레프센 바트나모트"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005607089279 Mattias Tollefsen Vatnamot, qualified P1810 subject named as Mattias Tollefsen Vatnamot
LAST	P2600	"6000000005607089279"	P1810	"Mattias Tollefsen Vatnamot"
#   P570 date of death = +1758-00-00T00:00:00Z/9
LAST	P570	+1758-00-00T00:00:00Z/9	S2600	"6000000005607089279"
#   P40 child = Q141216647 Tollef Mattiasson Fotland
LAST	P40	Q141216647	S2600	"6000000005607089279"
#   Q141216647 Tollef Mattiasson Fotland: P22 father = the item just created
Q141216647	P22	LAST	S2600	"6000000005607089279"
#   the item just created: P735 given name = Q16279186 Mattias
LAST	P735	Q16279186

# create a new item
CREATE
#   set the mul label to "NN Pedersdatter Foss"
LAST	Lmul	"NN Pedersdatter Foss"
#   set the ca label to "filla de Peder Tormodsen Foss"
LAST	Lca	"filla de Peder Tormodsen Foss"
#   set the da label to "datter af Peder Tormodsen Foss"
LAST	Lda	"datter af Peder Tormodsen Foss"
#   set the de label to "Tochter von Peder Tormodsen Foss"
LAST	Lde	"Tochter von Peder Tormodsen Foss"
#   set the en label to "daughter of Peder Tormodsen Foss"
LAST	Len	"daughter of Peder Tormodsen Foss"
#   set the es label to "hija de Peder Tormodsen Foss"
LAST	Les	"hija de Peder Tormodsen Foss"
#   set the fr label to "fille de Peder Tormodsen Foss"
LAST	Lfr	"fille de Peder Tormodsen Foss"
#   set the it label to "figlia di Peder Tormodsen Foss"
LAST	Lit	"figlia di Peder Tormodsen Foss"
#   set the ja label to "ペーダー・トルモドセン・フォスの娘"
LAST	Lja	"ペーダー・トルモドセン・フォスの娘"
#   set the ko label to "페데르 토르모드센 포스의 딸"
LAST	Lko	"페데르 토르모드센 포스의 딸"
#   set the nb label to "datter av Peder Tormodsen Foss"
LAST	Lnb	"datter av Peder Tormodsen Foss"
#   set the nl label to "dochter van Peder Tormodsen Foss"
LAST	Lnl	"dochter van Peder Tormodsen Foss"
#   set the pt label to "filha de Peder Tormodsen Foss"
LAST	Lpt	"filha de Peder Tormodsen Foss"
#   set the sv label to "dotter till Peder Tormodsen Foss"
LAST	Lsv	"dotter till Peder Tormodsen Foss"
#   set the zh label to "彼泽·托尔莫德森·福斯之女"
LAST	Lzh	"彼泽·托尔莫德森·福斯之女"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005608952898 NN Pedersdatter Foss
LAST	P2600	"6000000005608952898"
#   P22 father = Q141206080 Peder Tormodsen Foss
LAST	P22	Q141206080	S2600	"6000000005608952898"
#   P25 mother = Q141206061 Cecilie Olsdatter Håland
LAST	P25	Q141206061	S2600	"6000000005608952898"
#   Q141206080 Peder Tormodsen Foss: P40 child = the item just created
Q141206080	P40	LAST	S2600	"6000000005608952898"
#   Q141206061 Cecilie Olsdatter Håland: P40 child = the item just created
Q141206061	P40	LAST	S2600	"6000000005608952898"

# create a new item
CREATE
#   the item just created: set the en label to "Nils Olsson"
LAST	Len	"Nils Olsson"
#   set the mul label to "Nils Olsson"
LAST	Lmul	"Nils Olsson"
#   set the ja label to "ニルス・オルソン"
LAST	Lja	"ニルス・オルソン"
#   set the zh label to "尼尔斯·奥尔松"
LAST	Lzh	"尼尔斯·奥尔松"
#   set the ko label to "닐스 올손"
LAST	Lko	"닐스 올손"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000004335084173 Nils Olsson, qualified P1810 subject named as Nils Olsson
LAST	P2600	"6000000004335084173"	P1810	"Nils Olsson"
#   P569 date of birth = +1518-00-00T00:00:00Z/9
LAST	P569	+1518-00-00T00:00:00Z/9	S2600	"6000000004335084173"
#   P570 date of death = +1549-00-00T00:00:00Z/9
LAST	P570	+1549-00-00T00:00:00Z/9	S2600	"6000000004335084173"
#   P22 father = Q141205932 Olof Timmerman
LAST	P22	Q141205932	S2600	"6000000004335084173"
#   P25 mother = Q141205926 NN
LAST	P25	Q141205926	S2600	"6000000004335084173"
#   Q141205932 Olof Timmerman: P40 child = the item just created
Q141205932	P40	LAST	S2600	"6000000004335084173"
#   Q141205926 NN: P40 child = the item just created
Q141205926	P40	LAST	S2600	"6000000004335084173"
#   the item just created: P735 given name = Q16423038 Nils
LAST	P735	Q16423038
#   P734 family name = Q21497082 Olsson
LAST	P734	Q21497082

# create a new item
CREATE
#   set the en label to "Nils Sundius"
LAST	Len	"Nils Sundius"
#   set the mul label to "Nils Sundius"
LAST	Lmul	"Nils Sundius"
#   set the ja label to "ニルス・スンディウス"
LAST	Lja	"ニルス・スンディウス"
#   set the zh label to "尼尔斯·孙迪乌斯"
LAST	Lzh	"尼尔斯·孙迪乌斯"
#   set the ko label to "닐스 순듀스"
LAST	Lko	"닐스 순듀스"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003966366446 Nils Sundius, qualified P1810 subject named as Nils Sundius
LAST	P2600	"6000000003966366446"	P1810	"Nils Sundius"
#   P569 date of birth = +1687-09-30T00:00:00Z/11
LAST	P569	+1687-09-30T00:00:00Z/11	S2600	"6000000003966366446"
#   P570 date of death = +1761-07-24T00:00:00Z/11
LAST	P570	+1761-07-24T00:00:00Z/11	S2600	"6000000003966366446"
#   P40 child = Q19976400 Abraham Burensund
LAST	P40	Q19976400	S2600	"6000000003966366446"
#   Q19976400 Abraham Burensund: P22 father = the item just created
Q19976400	P22	LAST	S2600	"6000000003966366446"
#   the item just created: P735 given name = Q16423038 Nils
LAST	P735	Q16423038

# create a new item
CREATE
#   set the en label to "Rasmus Lydikson Amdal"
LAST	Len	"Rasmus Lydikson Amdal"
#   set the mul label to "Rasmus Lydikson Amdal"
LAST	Lmul	"Rasmus Lydikson Amdal"
#   add a mul alias "Rasmus Lydikson Kvam"
LAST	Amul	"Rasmus Lydikson Kvam"
#   set the ja label to "ラスムス・リディクソン・アムダル"
LAST	Lja	"ラスムス・リディクソン・アムダル"
#   set the zh label to "拉斯穆斯·利迪克松·阿姆达尔"
LAST	Lzh	"拉斯穆斯·利迪克松·阿姆达尔"
#   set the ko label to "라스무스 리디크손 암달"
LAST	Lko	"라스무스 리디크손 암달"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000007980728992 Rasmus Lydikson Amdal, qualified P1810 subject named as Rasmus Lydikson Kvam
LAST	P2600	"6000000007980728992"	P1810	"Rasmus Lydikson Kvam"
#   P569 date of birth = +1628-00-00T00:00:00Z/9
LAST	P569	+1628-00-00T00:00:00Z/9	S2600	"6000000007980728992"
#   P570 date of death = +1708-00-00T00:00:00Z/9
LAST	P570	+1708-00-00T00:00:00Z/9	S2600	"6000000007980728992"
#   P26 spouse = Q141223551 Ragnhild Ingebretsdatter Voster
LAST	P26	Q141223551	S2600	"6000000007980728992"
#   Q141223551 Ragnhild Ingebretsdatter Voster: P26 spouse = the item just created
Q141223551	P26	LAST	S2600	"6000000007980728992"
#   the item just created: P735 given name = Q1785744 Rasmus
LAST	P735	Q1785744
#   P734 family name = Q30086760 Kvam, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q30086760	P3831	Q2507958
#   P734 family name = Q37478260
LAST	P734	Q37478260
#   add a mul alias "Amdal"
LAST	Amul	"Amdal"
#   add a mul alias "Rasmus Amdal"
LAST	Amul	"Rasmus Amdal"

# create a new item
CREATE
#   set the en label to "Torger Olsen Ålgård"
LAST	Len	"Torger Olsen Ålgård"
#   set the mul label to "Torger Olsen Ålgård"
LAST	Lmul	"Torger Olsen Ålgård"
#   set the ja label to "トルゲル・オルセン・オールゴールド"
LAST	Lja	"トルゲル・オルセン・オールゴールド"
#   set the zh label to "托尔盖尔·奥尔森·奥尔戈尔德"
LAST	Lzh	"托尔盖尔·奥尔森·奥尔戈尔德"
#   set the ko label to "토르게르 올센 올고르드"
LAST	Lko	"토르게르 올센 올고르드"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000216588272880 Torger Olsen Ålgård, qualified P1810 subject named as Torger Olsen Ålgård
LAST	P2600	"6000000216588272880"	P1810	"Torger Olsen Ålgård"
#   P569 date of birth = +1830-03-14T00:00:00Z/11
LAST	P569	+1830-03-14T00:00:00Z/11	S2600	"6000000216588272880"
#   P570 date of death = +1888-05-19T00:00:00Z/11
LAST	P570	+1888-05-19T00:00:00Z/11	S2600	"6000000216588272880"
#   P22 father = Q141223849 Ola Helgeson Lima
LAST	P22	Q141223849	S2600	"6000000216588272880"
#   P25 mother = Q141223999 Anna Ådnesdatter Lima
LAST	P25	Q141223999	S2600	"6000000216588272880"
#   Q141223849 Ola Helgeson Lima: P40 child = the item just created
Q141223849	P40	LAST	S2600	"6000000216588272880"
#   Q141223999 Anna Ådnesdatter Lima: P40 child = the item just created
Q141223999	P40	LAST	S2600	"6000000216588272880"

# create a new item
CREATE
#   the item just created: set the en label to "Waldemar Leopold Engebretsen"
LAST	Len	"Waldemar Leopold Engebretsen"
#   set the mul label to "Waldemar Leopold Engebretsen"
LAST	Lmul	"Waldemar Leopold Engebretsen"
#   set the ja label to "ヴァルデマール・レオポルト・エンゲブレトセン"
LAST	Lja	"ヴァルデマール・レオポルト・エンゲブレトセン"
#   set the zh label to "瓦尔德马尔·利奥波德·恩盖布雷特森"
LAST	Lzh	"瓦尔德马尔·利奥波德·恩盖布雷特森"
#   set the ko label to "와르데마르 레오폴드 에에브레첸"
LAST	Lko	"와르데마르 레오폴드 에에브레첸"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000036747100847 Waldemar Leopold Engebretsen, qualified P1810 subject named as Waldemar Leopold Engebretsen
LAST	P2600	"6000000036747100847"	P1810	"Waldemar Leopold Engebretsen"
#   P569 date of birth = +1848-12-26T00:00:00Z/11
LAST	P569	+1848-12-26T00:00:00Z/11	S2600	"6000000036747100847"
#   P570 date of death = +1907-05-06T00:00:00Z/11
LAST	P570	+1907-05-06T00:00:00Z/11	S2600	"6000000036747100847"
#   P40 child = Q141216453 Aagot Garborg Koloboff
LAST	P40	Q141216453	S2600	"6000000036747100847"
#   Q141216453 Aagot Garborg Koloboff: P22 father = the item just created
Q141216453	P22	LAST	S2600	"6000000036747100847"
#   the item just created: P735 given name = Q18609914 Waldemar, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q18609914	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1076652 Leopold, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1076652	P1545	"2"	P3831	Q245025
#   Q105796231 Margareta Gödiksdotter Fincke till Kanckas: P735 given name = Q8274988 Margareta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q105796231	P735	Q8274988	P1545	"1"	P7452	Q3409033
#   Q110386205 Lars Bengtsson Hierta till Kålsholmen: P735 given name = Q15635262 Lars, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110386205	P735	Q15635262	P1545	"1"	P7452	Q3409033
#   Q141250216 Bjørn Gunnarson Mele: P26 spouse = Q141250249 Sissel Knutsdatter Bjørheim
Q141250216	P26	Q141250249	S2600	"4462693"
#   Q141250249 Sissel Knutsdatter Bjørheim: P26 spouse = Q141250216 Bjørn Gunnarson Mele
Q141250249	P26	Q141250216	S2600	"4462761"
#   Q104172926 Carl Johan Oskar von Numers: P735 given name = Q2529610 Carl, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q104172926	P735	Q2529610	P1545	"1"	P7452	Q3409033
#   P735 given name = Q10989273 Johan, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q104172926	P735	Q10989273	P1545	"2"	P3831	Q245025
#   P735 given name = Q18145769 Oskar, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q104172926	P735	Q18145769	P1545	"3"	P3831	Q245025
#   Q135441621 Carl Lagerborg: P735 given name = Q2529610 Carl
Q135441621	P735	Q2529610
#   Q110561236 Christina Fjodorovna Rosladin: P735 given name = Q1083457 Christina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110561236	P735	Q1083457	P1545	"1"	P7452	Q3409033
#   Q133861599 Beata Sofia Stierncrona: P735 given name = Q338015 Beata, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q133861599	P735	Q338015	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q133861599	P735	Q18201520	P1545	"2"	P3831	Q245025
#   Q108082048 Adolf Vilhelm Boije af Gennäs: P735 given name = Q18145837 Adolf, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q108082048	P735	Q18145837	P1545	"1"	P7452	Q3409033
#   P735 given name = Q12805716 Vilhelm, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q108082048	P735	Q12805716	P1545	"2"	P3831	Q245025
#   P734 family name = Q141223490
Q108082048	P734	Q141223490
#   Q104383015 Evert Wilhelm Bruncrona: P735 given name = Q13580919 Evert, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q104383015	P735	Q13580919	P1545	"1"	P7452	Q3409033
#   P735 given name = Q11027623, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q104383015	P735	Q11027623	P1545	"2"	P3831	Q245025
#   Q136376387 Ebba Kristina Carlsdotter: P735 given name = Q2242896 Ebba, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q136376387	P735	Q2242896	P1545	"1"	P7452	Q3409033
#   P735 given name = Q19798802 Kristina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q136376387	P735	Q19798802	P1545	"2"	P3831	Q245025
#   Q141224209 Jacob Chydenius: P40 child = Q109852817 Jakob Chydenius
Q141224209	P40	Q109852817	S2600	"6000000000583643059"
#   Q141250218 Brita Magdalena Eriksdotter Rahm: P26 spouse = Q109852817 Jakob Chydenius
Q141250218	P26	Q109852817	S2600	"6000000001186122035"
#   Q110304710 Leveke Dorothea von Levetzow: P735 given name = Q909253 Dorothea, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110304710	P735	Q909253	P1545	"2"	P3831	Q245025
#   Q130683609 Cecilia Lucia Brodersen: P735 given name = Q859234 Cecilia, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q130683609	P735	Q859234	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1160640 Lucia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q130683609	P735	Q1160640	P1545	"2"	P3831	Q245025
#   Q136376245 Fredrik Elof Gyllenkrok RSO: P735 given name = Q4926491 Fredrik, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q136376245	P735	Q4926491	P1545	"1"	P7452	Q3409033
#   P735 given name = Q3366319 Elof, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q136376245	P735	Q3366319	P1545	"2"	P3831	Q245025
#   Q110547994 Elisabeth von Saveland: P735 given name = Q63611044 Elisabeth, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110547994	P735	Q63611044	P1545	"1"	P7452	Q3409033
#   Q30879127 Guiges Guy de Forez VII: P735 given name = Q1159023 Guy, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q30879127	P735	Q1159023	P1545	"2"	P3831	Q245025
#   Q141216594 Ane Maria Olsdatter Vestre Stangaland: P26 spouse = Q138473856 Kristian Monsen Stangeland
Q141216594	P26	Q138473856	S2600	"6000000003491995729"
#   Q110378177 Adelheid von Plain: P735 given name = Q4057477 Adelheid, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110378177	P735	Q4057477	P1545	"1"	P7452	Q3409033
#   Q116007123 Costanza di Niccolò Cavalcanti: P735 given name = Q19816831 Costanza, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q116007123	P735	Q19816831	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1984713 Niccolò, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q116007123	P735	Q1984713	P1545	"3"	P3831	Q245025
#   P734 family name = Q21450357 Cavalcanti
Q116007123	P734	Q21450357
#   Q110548816 Lovisa Thott: P735 given name = Q10570000 Lovisa
Q110548816	P735	Q10570000
#   P734 family name = Q47528688 Thott
Q110548816	P734	Q47528688
#   Q130564935 Christoph Ernst von Platen: P735 given name = Q17689481 Christoph, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q130564935	P735	Q17689481	P1545	"1"	P7452	Q3409033
#   P735 given name = Q292691 Ernst, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q130564935	P735	Q292691	P1545	"2"	P3831	Q245025
#   Q110303165 Sofia Elisabeth Augusta von Buchwaldt: P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110303165	P735	Q18201520	P1545	"1"	P7452	Q3409033
#   P735 given name = Q63611044 Elisabeth, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110303165	P735	Q63611044	P1545	"2"	P3831	Q245025
#   P735 given name = Q1370330 Augusta, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q110303165	P735	Q1370330	P1545	"3"	P3831	Q245025
#   Q141250230 Henrika Birgitta Wachtmeister af Johannishus: P40 child = Q141250253 Ulrika Henrika von Köhler
Q141250230	P40	Q141250253	S2600	"6000000006127526153"
#   Q110304545 Charlotta Lovisa Gyllenkrok: P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110304545	P735	Q1067071	P1545	"1"	P7452	Q3409033
#   P735 given name = Q10570000 Lovisa, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110304545	P735	Q10570000	P1545	"2"	P3831	Q245025
#   Q76250299 Vendela Sofia von Wright: P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q76250299	P735	Q18201520	P1545	"2"	P3831	Q245025
#   P734 family name = Q2594455 Wright
Q76250299	P734	Q2594455
#   Q110548033 Marie Emilie Reuterskiöld: P735 given name = Q106674406 Marie, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110548033	P735	Q106674406	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16275679 Emilie, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110548033	P735	Q16275679	P1545	"2"	P3831	Q245025
#   Q110395728 Eugenia Karolina Desideria von Essen: P735 given name = Q962602 Eugenia, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110395728	P735	Q962602	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1734206 Karolina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110395728	P735	Q1734206	P1545	"2"	P3831	Q245025
#   P735 given name = Q682121 Desideria, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q110395728	P735	Q682121	P1545	"3"	P3831	Q245025
#   Q133861600 Catharina Elisabet Lamoni: P735 given name = Q17317997 Catharina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q133861600	P735	Q17317997	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16423275 Elisabet, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q133861600	P735	Q16423275	P1545	"2"	P3831	Q245025
#   Q99202612 Maria Eleonora von Busseck: P735 given name = Q325872 Maria, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q99202612	P735	Q325872	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18759077 Eleonora, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q99202612	P735	Q18759077	P1545	"2"	P3831	Q245025
#   Q141250247 Sara Carlberg: P26 spouse = Q141250225 Conrad von Braunjohan
Q141250247	P26	Q141250225	S2600	"6000000006435949669"
#   Q141250225 Conrad von Braunjohan: P26 spouse = Q141250247 Sara Carlberg
Q141250225	P26	Q141250247	S2600	"6000000006436219130"
#   Q136660380 Maria Andersdotter Bergia: P735 given name = Q325872 Maria
Q136660380	P735	Q325872
#   Q136376354 Agneta Sofia Löwenhielm: P735 given name = Q3354746 Agneta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q136376354	P735	Q3354746	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q136376354	P735	Q18201520	P1545	"2"	P3831	Q245025
#   Q99460476 Carl Henrik Posse af Säby: P26 spouse = Q141250228 Helena Åkesdotter Soop
Q99460476	P26	Q141250228	S2600	"6000000007182710798"
#   Q141250228 Helena Åkesdotter Soop: P26 spouse = Q99460476 Carl Henrik Posse af Säby
Q141250228	P26	Q99460476	S2600	"6000000007182716723"
#   Q109852820 Gustav Adolf Järnefelt: P735 given name = Q746076, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q109852820	P735	Q746076	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18145837 Adolf, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q109852820	P735	Q18145837	P1545	"2"	P3831	Q245025
#   Q133283834 Nils Gabriel Danckwardt-Lillieström till Gälsebo: P735 given name = Q16423038 Nils, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q133283834	P735	Q16423038	P1545	"1"	P7452	Q3409033
#   P735 given name = Q4925914 Gabriel, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q133283834	P735	Q4925914	P1545	"2"	P3831	Q245025
#   Q110548896 Ebba Lidman: P735 given name = Q2242896 Ebba
Q110548896	P735	Q2242896
#   Q135665878 Anna Christina Stålhammar: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q135665878	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1083457 Christina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q135665878	P735	Q1083457	P1545	"2"	P3831	Q245025
#   Q141224012 Hedvig Chydenius: P40 child = Q109852817 Jakob Chydenius
Q141224012	P40	Q109852817	S2600	"6000000007774748338"
#   Q110457041 Anna Sofia Stålhammar: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110457041	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110457041	P735	Q18201520	P1545	"2"	P3831	Q245025
#   Q134546510 Catharina Elisabet Brandt: P25 mother = Q141250213 Anna Maria Norn
Q134546510	P25	Q141250213	S2600	"6000000008496890939"
#   P2600 Geni.com profile ID = 6000000008496890939 Catharina Elisabet Brandt, qualified P1810 subject named as Catharina Elisabet Brandt
Q134546510	P2600	"6000000008496890939"	P1810	"Catharina Elisabet Brandt"
#   P735 given name = Q17317997 Catharina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q134546510	P735	Q17317997	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16423275 Elisabet, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q134546510	P735	Q16423275	P1545	"2"	P3831	Q245025
#   P734 family name = Q11941314 Brandt
Q134546510	P734	Q11941314
#   Q134895550 Maria Hoffman: P735 given name = Q325872 Maria
Q134895550	P735	Q325872
#   Q110304544 Sophie Magdalena Magdalena von Essen: P735 given name = Q14942517 Sophie, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110304544	P735	Q14942517	P1545	"1"	P7452	Q3409033
#   P735 given name = Q842544 Magdalena, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110304544	P735	Q842544	P1545	"2"	P3831	Q245025
#   P735 given name = Q842544 Magdalena, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q110304544	P735	Q842544	P1545	"3"	P3831	Q245025
#   Q110548812 Maria Stiernblad: P735 given name = Q325872 Maria
Q110548812	P735	Q325872
#   Q110386180 Elisabet Ramsvärd: P735 given name = Q16423275 Elisabet
Q110386180	P735	Q16423275
#   Q127270620 Johan Olofsson: P735 given name = Q10989273 Johan
Q127270620	P735	Q10989273
#   Q131740913 Hedvig Sofia Hamilton: P735 given name = Q13648620 Hedvig, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q131740913	P735	Q13648620	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q131740913	P735	Q18201520	P1545	"2"	P3831	Q245025
#   Q5916852 Lorentz Kockum: P735 given name = Q21061236 Lorentz
Q5916852	P735	Q21061236
#   Q141250214 Anna Nilsdotter: P26 spouse = Q141250215 Benjamin Mårtensson
Q141250214	P26	Q141250215	S2600	"6000000011078617825"
#   Q141250215 Benjamin Mårtensson: P26 spouse = Q141250214 Anna Nilsdotter
Q141250215	P26	Q141250214	S2600	"6000000011078886609"
#   Q109296145 Charlotta Florentina Beata Ingelotz: P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q109296145	P735	Q1067071	P1545	"1"	P7452	Q3409033
#   P735 given name = Q610489 Florentina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q109296145	P735	Q610489	P1545	"2"	P3831	Q245025
#   P735 given name = Q338015 Beata, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q109296145	P735	Q338015	P1545	"3"	P3831	Q245025
#   Q109835643 Maria Catharina Douglies: P735 given name = Q325872 Maria, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q109835643	P735	Q325872	P1545	"1"	P7452	Q3409033
#   P735 given name = Q17317997 Catharina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q109835643	P735	Q17317997	P1545	"2"	P3831	Q245025
#   Q131726979 Vilhelmina Lovisa Fredrika Ulrika Iserhielm: P735 given name = Q15711317 Vilhelmina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q131726979	P735	Q15711317	P1545	"1"	P7452	Q3409033
#   P735 given name = Q10570000 Lovisa, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q131726979	P735	Q10570000	P1545	"2"	P3831	Q245025
#   P735 given name = Q5499550 Fredrika, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q131726979	P735	Q5499550	P1545	"3"	P3831	Q245025
#   P735 given name = Q18924998 Ulrika, qualified P1545 series ordinal 4, P3831 object of statement has role Q245025 middle name
Q131726979	P735	Q18924998	P1545	"4"	P3831	Q245025
#   Q101247028 Anna Catharina Fleming af Liebelitz: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q101247028	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P735 given name = Q17317997 Catharina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q101247028	P735	Q17317997	P1545	"2"	P3831	Q245025
#   Q136536614 Ture Johansson Sandelin: P735 given name = Q2460609 Ture
Q136536614	P735	Q2460609
#   Q134626249 Gustaf Enebom: P735 given name = Q15646212 Gustaf
Q134626249	P735	Q15646212
#   Q64828819 Johanna Gustava Axelina Åberg: P735 given name = Q4120836 Johanna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q64828819	P735	Q4120836	P1545	"1"	P7452	Q3409033
#   P735 given name = Q21144392 Gustava, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q64828819	P735	Q21144392	P1545	"2"	P3831	Q245025
#   P735 given name = Q10423722 Axelina, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q64828819	P735	Q10423722	P1545	"3"	P3831	Q245025
#   Q109835201 Lovisa Löf: P735 given name = Q10570000 Lovisa
Q109835201	P735	Q10570000
#   Q110395628 Maria Lovisa Ulrika Ehrenpohl: P735 given name = Q325872 Maria, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110395628	P735	Q325872	P1545	"1"	P7452	Q3409033
#   P735 given name = Q10570000 Lovisa, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110395628	P735	Q10570000	P1545	"2"	P3831	Q245025
#   P735 given name = Q18924998 Ulrika, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q110395628	P735	Q18924998	P1545	"3"	P3831	Q245025
#   Q108743048 Augusta Maria Sophia Rålamb: P735 given name = Q1370330 Augusta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q108743048	P735	Q1370330	P1545	"1"	P7452	Q3409033
#   P735 given name = Q325872 Maria, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q108743048	P735	Q325872	P1545	"2"	P3831	Q245025
#   P735 given name = Q2302787 Sophia, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q108743048	P735	Q2302787	P1545	"3"	P3831	Q245025
#   Q64829391 Abraham Johansson Fought dä: P735 given name = Q4055996 Abraham, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q64829391	P735	Q4055996	P1545	"1"	P7452	Q3409033
#   Q111998458 Sara de Marez: P735 given name = Q833345 Sara, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q111998458	P735	Q833345	P1545	"1"	P7452	Q3409033
#   Q108654979 Petronella Ottilia Schwencken von Friesen: P735 given name = Q16423664 Petronella, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q108654979	P735	Q16423664	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1423455 Ottilia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q108654979	P735	Q1423455	P1545	"2"	P3831	Q245025
#   Q141250253 Ulrika Henrika von Köhler: P25 mother = Q141250230 Henrika Birgitta Wachtmeister af Johannishus
Q141250253	P25	Q141250230	S2600	"6000000019568439151"
#   Q141250231 Jacob Baltzar von Hartmansdorff: P26 spouse = Q141250226 Fredrika Grönhagen
Q141250231	P26	Q141250226	S2600	"6000000019659479506"
#   Q141250226 Fredrika Grönhagen: P26 spouse = Q141250231 Jacob Baltzar von Hartmansdorff
Q141250226	P26	Q141250231	S2600	"6000000019659634521"
#   Q110151674 Jakobina Gustava von Essen: P735 given name = Q21144392 Gustava, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110151674	P735	Q21144392	P1545	"2"	P3831	Q245025
#   Q110153084 Amalia Eleonora von Lepel: P735 given name = Q453020 Amalia, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110153084	P735	Q453020	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18759077 Eleonora, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110153084	P735	Q18759077	P1545	"2"	P3831	Q245025
#   Q141250233 Joachim Johnson Lea: P40 child = Q141250238 Marta Joakimsdatter Lea
Q141250233	P40	Q141250238	S2600	"6000000025793788004"
#   Q141250238 Marta Joakimsdatter Lea: P22 father = Q141250233 Joachim Johnson Lea
Q141250238	P22	Q141250233	S2600	"6000000025810442031"
#   Q110304572 Cecilia Christophers: P735 given name = Q859234 Cecilia
Q110304572	P735	Q859234
#   Q110304541 Margareta Catharina von Finecke: P735 given name = Q8274988 Margareta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110304541	P735	Q8274988	P1545	"1"	P7452	Q3409033
#   P735 given name = Q17317997 Catharina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110304541	P735	Q17317997	P1545	"2"	P3831	Q245025
#   Q138495479 Friedrich Conrad Dietrich Adrian von Kleist: P735 given name = Q14038597 Friedrich, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q138495479	P735	Q14038597	P1545	"1"	P7452	Q3409033
#   P735 given name = Q17436400 Conrad, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q138495479	P735	Q17436400	P1545	"2"	P3831	Q245025
#   P735 given name = Q18145860 Dietrich, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q138495479	P735	Q18145860	P1545	"3"	P3831	Q245025
#   P735 given name = Q372250 Adrian, qualified P1545 series ordinal 4, P3831 object of statement has role Q245025 middle name
Q138495479	P735	Q372250	P1545	"4"	P3831	Q245025
#   Q130524451 Carl Henrik von Hofsten RSO: P735 given name = Q2529610 Carl, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q130524451	P735	Q2529610	P1545	"1"	P7452	Q3409033
#   P735 given name = Q594279 Henrik, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q130524451	P735	Q594279	P1545	"2"	P3831	Q245025

