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

# Kristiansen -- patronymic, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Kristiansen"
LAST	Len	"Kristiansen"
#   set the mul label to "Kristiansen"
LAST	Lmul	"Kristiansen"
#   set the en description to "patronymic"
LAST	Den	"patronymic"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141189067 Helmik Kristiansen Sør-Reime: P5056 patronym or matronym = the item just created, qualified P144 based on Q141189076 Kristian Larsen Sør-Reime
Q141189067	P5056	LAST	P144	Q141189076	S2600	"6000000221449620901"
#   Q141189078 Lars Kristiansen Sør-Reime: P5056 patronym or matronym = the item just created, qualified P144 based on Q141189076 Kristian Larsen Sør-Reime
Q141189078	P5056	LAST	P144	Q141189076	S2600	"6000000224702528843"
#   Q141189077 Lars Bernhard Kristiansen Sør-Reime: P5056 patronym or matronym = the item just created, qualified P144 based on Q141189076 Kristian Larsen Sør-Reime
Q141189077	P5056	LAST	P144	Q141189076	S2600	"6000000224702710821"

# Tormodsdatter -- patronymic, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Tormodsdatter"
LAST	Len	"Tormodsdatter"
#   set the mul label to "Tormodsdatter"
LAST	Lmul	"Tormodsdatter"
#   set the en description to "patronymic"
LAST	Den	"patronymic"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141224345 Signy Tormodsdatter Rossavik: P5056 patronym or matronym = the item just created
Q141224345	P5056	LAST	S2600	"6000000003095080099"
#   Q141205898 Anna Tormodsdatter Mele: P5056 patronym or matronym = the item just created, qualified P144 based on Q141198507 Tormod Bjørnson Mele
Q141205898	P5056	LAST	P144	Q141198507	S2600	"6000000005609232777"

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

# 338 more name items are needed and wait for a later
# run -- 3 a day is her cap, not a limit of the data:
#   Hakunge (family), 3 bearer(s)
#   Hansen (patronymic), 3 bearer(s)
#   Hansson (patronymic), 3 bearer(s)
#   Helgesen (patronymic), 3 bearer(s)
#   Høle (family), 3 bearer(s)
#   Ingebretsdatter (patronymic), 3 bearer(s)
#   Johansdotter (patronymic), 3 bearer(s)
#   Knutsdatter (patronymic), 3 bearer(s)
#   Magnusson (patronymic), 3 bearer(s)
#   Nord-Varhaug (family), 3 bearer(s)
#   Røyneberg (family), 3 bearer(s)
#   Söfdeborg (family), 3 bearer(s)
#   ... and 326 more

# ========================================================================
# THE DAY'S PEOPLE
# ========================================================================

# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   2633 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   set the ko label to "투레 비엘케"
Q5597349	Lko	"투레 비엘케"
#   set the ko label to "마리아 카로리나 에리사베트 사흐린"
Q141244110	Lko	"마리아 카로리나 에리사베트 사흐린"
#   set the ko label to "오라 올센 바우레"
Q141200019	Lko	"오라 올센 바우레"
#   Q141224827 Margareta Olausdotter Plantin: set the ko label to "마르가레타 오라우스도테르 프란틴"
Q141224827	Lko	"마르가레타 오라우스도테르 프란틴"
#   Q141244103 Kristofer Sahlin: set the ko label to "크리스토페르 사흐린"
Q141244103	Lko	"크리스토페르 사흐린"
#   Q141242499 Gunnar Sahlin: set the ko label to "군나르 사흐린"
Q141242499	Lko	"군나르 사흐린"
#   set the ko label to "에르링 줼 웨느드트"
Q141198396	Lko	"에르링 줼 웨느드트"
#   set the ko label to "락느힐드 소피에 사흐린"
Q141223742	Lko	"락느힐드 소피에 사흐린"
#   set the ko label to "토레 셉죄르느손 탈게 디"
Q141219336	Lko	"토레 셉죄르느손 탈게 디"
#   set the ko label to "시셀 존스다테르 타레"
Q141200101	Lko	"시셀 존스다테르 타레"
#   set the ja label to "カヌテ・デューク・オフ・エストニア"
Q3743799	Lja	"カヌテ・デューク・オフ・エストニア"
#   set the zh label to "卡努特·杜克·奥夫·埃斯托尼阿"
Q3743799	Lzh	"卡努特·杜克·奥夫·埃斯托尼阿"
#   set the ko label to "카누테 두케 오프 에스토니아"
Q3743799	Lko	"카누테 두케 오프 에스토니아"
#   Q94938559 Friedrich Frommhold von Knorring: set the ja label to "フリードリヒ・フロムホルド・ヴォン・クノリング"
Q94938559	Lja	"フリードリヒ・フロムホルド・ヴォン・クノリング"
#   set the zh label to "弗里德里希·夫罗姆霍尔德·翁·克诺林"
Q94938559	Lzh	"弗里德里希·夫罗姆霍尔德·翁·克诺林"

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Anna Clo"
LAST	Len	"Anna Clo"
#   set the mul label to "Anna Clo"
LAST	Lmul	"Anna Clo"
#   add a mul alias "Anna Lenaea"
LAST	Amul	"Anna Lenaea"
#   set the ja label to "アンナ・クロ"
LAST	Lja	"アンナ・クロ"
#   set the zh label to "安娜·克洛"
LAST	Lzh	"安娜·克洛"
#   set the ko label to "안나 크로"
LAST	Lko	"안나 크로"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000008394484862 Anna Clo, qualified P1810 subject named as Anna Lenaea
LAST	P2600	"6000000008394484862"	P1810	"Anna Lenaea"
#   P569 date of birth = +1617-10-28T00:00:00Z/11
LAST	P569	+1617-10-28T00:00:00Z/11	S2600	"6000000008394484862"
#   P570 date of death = +1693-09-15T00:00:00Z/11
LAST	P570	+1693-09-15T00:00:00Z/11	S2600	"6000000008394484862"
#   P26 spouse = Q5960165 Carolus Nicolai Lithman
LAST	P26	Q5960165	S2600	"6000000008394484862"
#   Q5960165 Carolus Nicolai Lithman: P26 spouse = the item just created
Q5960165	P26	LAST	S2600	"6000000008394484862"
#   the item just created: P735 given name = Q666578 Anna
LAST	P735	Q666578
#   add a mul alias "Lenæus Clo"
LAST	Amul	"Lenæus Clo"

# create a new item
CREATE
#   set the en label to "Beata Elisabeth Rålamb"
LAST	Len	"Beata Elisabeth Rålamb"
#   set the mul label to "Beata Elisabeth Rålamb"
LAST	Lmul	"Beata Elisabeth Rålamb"
#   set the ja label to "ベアタ・エリーザベト・ローラムブ"
LAST	Lja	"ベアタ・エリーザベト・ローラムブ"
#   set the zh label to "贝阿塔·伊丽莎白·罗拉姆布"
LAST	Lzh	"贝阿塔·伊丽莎白·罗拉姆布"
#   set the ko label to "베아타 에리사베트 로람브"
LAST	Lko	"베아타 에리사베트 로람브"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000020181983483 Beata Elisabeth Rålamb, qualified P1810 subject named as Beata Elisabeth Rålamb
LAST	P2600	"6000000020181983483"	P1810	"Beata Elisabeth Rålamb"
#   P569 date of birth = +1677-08-18T00:00:00Z/11
LAST	P569	+1677-08-18T00:00:00Z/11	S2600	"6000000020181983483"
#   P570 date of death = +1716-06-05T00:00:00Z/11
LAST	P570	+1716-06-05T00:00:00Z/11	S2600	"6000000020181983483"
#   P40 child = Q141244115 Märta Elisabeth Bure
LAST	P40	Q141244115	S2600	"6000000020181983483"
#   Q141244115 Märta Elisabeth Bure: P25 mother = the item just created
Q141244115	P25	LAST	S2600	"6000000020181983483"
#   the item just created: P735 given name = Q338015 Beata, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q338015	P1545	"1"	P7452	Q3409033
#   P735 given name = Q63611044 Elisabeth, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q63611044	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Berit Eriksdatter Laland"
LAST	Len	"Berit Eriksdatter Laland"
#   set the mul label to "Berit Eriksdatter Laland"
LAST	Lmul	"Berit Eriksdatter Laland"
#   set the ja label to "ベリット・エリクスダッテル・ラランド"
LAST	Lja	"ベリット・エリクスダッテル・ラランド"
#   set the zh label to "贝里特·埃里克斯达特·拉兰德"
LAST	Lzh	"贝里特·埃里克斯达特·拉兰德"
#   set the ko label to "베리트 에리크스다테르 라란드"
LAST	Lko	"베리트 에리크스다테르 라란드"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005607217157 Berit Eriksdatter Laland, qualified P1810 subject named as Berit Eriksdatter Laland
LAST	P2600	"6000000005607217157"	P1810	"Berit Eriksdatter Laland"
#   P569 date of birth = +1711-00-00T00:00:00Z/9
LAST	P569	+1711-00-00T00:00:00Z/9	S2600	"6000000005607217157"
#   P570 date of death = +1742-00-00T00:00:00Z/9
LAST	P570	+1742-00-00T00:00:00Z/9	S2600	"6000000005607217157"
#   P40 child = Q141219349 Tørres Jonson Grannes
LAST	P40	Q141219349	S2600	"6000000005607217157"
#   P40 child = Q141244120 Ragnhild Jonsdatter Grannes
LAST	P40	Q141244120	S2600	"6000000005607217157"
#   Q141219349 Tørres Jonson Grannes: P25 mother = the item just created
Q141219349	P25	LAST	S2600	"6000000005607217157"
#   Q141244120 Ragnhild Jonsdatter Grannes: P25 mother = the item just created
Q141244120	P25	LAST	S2600	"6000000005607217157"
#   the item just created: P735 given name = Q820698 Berit
LAST	P735	Q820698
#   P5056 patronym or matronym = Q141223487
LAST	P5056	Q141223487
#   P734 family name = Q40469219
LAST	P734	Q40469219

# create a new item
CREATE
#   set the en label to "Gabriel Johansen Obrestad"
LAST	Len	"Gabriel Johansen Obrestad"
#   set the mul label to "Gabriel Johansen Obrestad"
LAST	Lmul	"Gabriel Johansen Obrestad"
#   set the ja label to "ガブリエル・ヨハンセン・オブレスタド"
LAST	Lja	"ガブリエル・ヨハンセン・オブレスタド"
#   set the zh label to "加布里埃尔·约翰森·奥布雷斯塔德"
LAST	Lzh	"加布里埃尔·约翰森·奥布雷斯塔德"
#   set the ko label to "가브리엘 조한센 옵레스타드"
LAST	Lko	"가브리엘 조한센 옵레스타드"
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
#   the item just created: P735 given name = Q4925914 Gabriel
LAST	P735	Q4925914
#   P734 family name = Q40353802
LAST	P734	Q40353802

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
#   set the ko label to "구리 노르드비"
LAST	Lko	"구리 노르드비"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000189963920888 Guri Nordby, qualified P1810 subject named as Guri ( Julia) Knutson
LAST	P2600	"6000000189963920888"	P1810	"Guri ( Julia) Knutson"
#   P569 date of birth = +1871-08-18T00:00:00Z/11
LAST	P569	+1871-08-18T00:00:00Z/11	S2600	"6000000189963920888"
#   P570 date of death = +1944-00-00T00:00:00Z/9
LAST	P570	+1944-00-00T00:00:00Z/9	S2600	"6000000189963920888"
#   P26 spouse = Q141257221 John Otterson Dokken
LAST	P26	Q141257221	S2600	"6000000189963920888"
#   P40 child = Q141219064 Lloyd Obert Dokken
LAST	P40	Q141219064	S2600	"6000000189963920888"
#   Q141257221 John Otterson Dokken: P26 spouse = the item just created
Q141257221	P26	LAST	S2600	"6000000189963920888"
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
#   set the en label to "Gustaf Jonasson Bure"
LAST	Len	"Gustaf Jonasson Bure"
#   set the mul label to "Gustaf Jonasson Bure"
LAST	Lmul	"Gustaf Jonasson Bure"
#   set the ja label to "グスタフ・ヨナソン・ブレ"
LAST	Lja	"グスタフ・ヨナソン・ブレ"
#   set the zh label to "古斯塔夫·约纳松·布雷"
LAST	Lzh	"古斯塔夫·约纳松·布雷"
#   set the ko label to "구스타프 조나손 부레"
LAST	Lko	"구스타프 조나손 부레"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000006127550579 Gustaf Jonasson Bure, qualified P1810 subject named as Gustaf Jonasson Bure
LAST	P2600	"6000000006127550579"	P1810	"Gustaf Jonasson Bure"
#   P569 date of birth = +1651-00-00T00:00:00Z/9
LAST	P569	+1651-00-00T00:00:00Z/9	S2600	"6000000006127550579"
#   P570 date of death = +1728-10-22T00:00:00Z/11
LAST	P570	+1728-10-22T00:00:00Z/11	S2600	"6000000006127550579"
#   P40 child = Q141244115 Märta Elisabeth Bure
LAST	P40	Q141244115	S2600	"6000000006127550579"
#   Q141244115 Märta Elisabeth Bure: P22 father = the item just created
Q141244115	P22	LAST	S2600	"6000000006127550579"
#   the item just created: P735 given name = Q15646212 Gustaf
LAST	P735	Q15646212
#   P734 family name = Q1703054 Jonasson
LAST	P734	Q1703054
#   P734 family name = Q11335012 Bure
LAST	P734	Q11335012

# create a new item
CREATE
#   set the en label to "Hans Jonsen Rønneberg"
LAST	Len	"Hans Jonsen Rønneberg"
#   set the mul label to "Hans Jonsen Rønneberg"
LAST	Lmul	"Hans Jonsen Rønneberg"
#   set the ja label to "ハンス・ヨンセン・レンネベルグ"
LAST	Lja	"ハンス・ヨンセン・レンネベルグ"
#   set the zh label to "汉斯·永森·伦内贝格"
LAST	Lzh	"汉斯·永森·伦内贝格"
#   set the ko label to "한스 존센 뢴네베르그"
LAST	Lko	"한스 존센 뢴네베르그"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003491933406 Hans Jonsen Rønneberg, qualified P1810 subject named as Hans Jonsen Rønneberg
LAST	P2600	"6000000003491933406"	P1810	"Hans Jonsen Rønneberg"
#   P569 date of birth = +1767-00-00T00:00:00Z/9
LAST	P569	+1767-00-00T00:00:00Z/9	S2600	"6000000003491933406"
#   P570 date of death = +1831-03-10T00:00:00Z/11
LAST	P570	+1831-03-10T00:00:00Z/11	S2600	"6000000003491933406"
#   P22 father = Q141244102 Jon Torson Røyneberg
LAST	P22	Q141244102	S2600	"6000000003491933406"
#   P25 mother = Q141244209 Berta Asbjørnsdotter Røyneberg
LAST	P25	Q141244209	S2600	"6000000003491933406"
#   Q141244102 Jon Torson Røyneberg: P40 child = the item just created
Q141244102	P40	LAST	S2600	"6000000003491933406"
#   Q141244209 Berta Asbjørnsdotter Røyneberg: P40 child = the item just created
Q141244209	P40	LAST	S2600	"6000000003491933406"
#   the item just created: P735 given name = Q632842
LAST	P735	Q632842
#   P734 family name = Q7386722 Rønneberg
LAST	P734	Q7386722

# create a new item
CREATE
#   set the en label to "Henrika von Köhler"
LAST	Len	"Henrika von Köhler"
#   set the mul label to "Henrika von Köhler"
LAST	Lmul	"Henrika von Köhler"
#   set the ja label to "ヘンリカ・ヴォン・ケーラー"
LAST	Lja	"ヘンリカ・ヴォン・ケーラー"
#   set the zh label to "亨里卡·翁·科莱尔"
LAST	Lzh	"亨里卡·翁·科莱尔"
#   set the ko label to "헨리카 본 쾨흐레르"
LAST	Lko	"헨리카 본 쾨흐레르"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000019568453073 Henrika von Köhler, qualified P1810 subject named as Henrika von Köhler
LAST	P2600	"6000000019568453073"	P1810	"Henrika von Köhler"
#   P569 date of birth = +1788-07-08T00:00:00Z/11
LAST	P569	+1788-07-08T00:00:00Z/11	S2600	"6000000019568453073"
#   P570 date of death = +1859-08-26T00:00:00Z/11
LAST	P570	+1859-08-26T00:00:00Z/11	S2600	"6000000019568453073"
#   P22 father = Q19721217 Salomon Christoffer von Köhler
LAST	P22	Q19721217	S2600	"6000000019568453073"
#   P25 mother = Q141250230 Henrika Birgitta Wachtmeister af Johannishus
LAST	P25	Q141250230	S2600	"6000000019568453073"
#   Q19721217 Salomon Christoffer von Köhler: P40 child = the item just created
Q19721217	P40	LAST	S2600	"6000000019568453073"
#   Q141250230 Henrika Birgitta Wachtmeister af Johannishus: P40 child = the item just created
Q141250230	P40	LAST	S2600	"6000000019568453073"

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
#   set the ko label to "조한 존손 하란드"
LAST	Lko	"조한 존손 하란드"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000063300979653 Johan Jonson Haland, qualified P1810 subject named as Johan Jonson Haland
LAST	P2600	"6000000063300979653"	P1810	"Johan Jonson Haland"
#   P569 date of birth = +1478-00-00T00:00:00Z/9, qualified P1319 earliest date +1478-00-00T00:00:00Z/9, P1326 latest date +1480-00-00T00:00:00Z/9
LAST	P569	+1478-00-00T00:00:00Z/9	P1319	+1478-00-00T00:00:00Z/9	P1326	+1480-00-00T00:00:00Z/9	S2600	"6000000063300979653"
#   P570 date of death = +1540-00-00T00:00:00Z/9, qualified P1319 earliest date +1540-00-00T00:00:00Z/9
LAST	P570	+1540-00-00T00:00:00Z/9	P1319	+1540-00-00T00:00:00Z/9	S2600	"6000000063300979653"
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
#   set the en label to "Johan Stecksenius"
LAST	Len	"Johan Stecksenius"
#   set the mul label to "Johan Stecksenius"
LAST	Lmul	"Johan Stecksenius"
#   set the ja label to "ヨハン・ステクセニウス"
LAST	Lja	"ヨハン・ステクセニウス"
#   set the zh label to "约翰·斯特克塞尼乌斯"
LAST	Lzh	"约翰·斯特克塞尼乌斯"
#   set the ko label to "조한 스테크세뉴스"
LAST	Lko	"조한 스테크세뉴스"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000011012541325 Johan Stecksenius, qualified P1810 subject named as Johan Stecksenius
LAST	P2600	"6000000011012541325"	P1810	"Johan Stecksenius"
#   P569 date of birth = +1679-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P569	+1679-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"6000000011012541325"
#   P570 date of death = +1743-07-22T00:00:00Z/11
LAST	P570	+1743-07-22T00:00:00Z/11	S2600	"6000000011012541325"
#   P40 child = Q141244108 Margareta Stecksenia
LAST	P40	Q141244108	S2600	"6000000011012541325"
#   Q141244108 Margareta Stecksenia: P22 father = the item just created
Q141244108	P22	LAST	S2600	"6000000011012541325"
#   the item just created: P735 given name = Q10989273 Johan
LAST	P735	Q10989273

# create a new item
CREATE
#   set the en label to "Jon Tørresson Grannes"
LAST	Len	"Jon Tørresson Grannes"
#   set the mul label to "Jon Tørresson Grannes"
LAST	Lmul	"Jon Tørresson Grannes"
#   add a mul alias "Jon Tørresson Tørresson Grannes"
LAST	Amul	"Jon Tørresson Tørresson Grannes"
#   set the ja label to "ジョン・トレソン・グラネス"
LAST	Lja	"ジョン・トレソン・グラネス"
#   set the zh label to "乔恩·托雷松·格拉内斯"
LAST	Lzh	"乔恩·托雷松·格拉内斯"
#   set the ko label to "존 퇴르레손 그란네스"
LAST	Lko	"존 퇴르레손 그란네스"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005607475221 Jon Tørresson Grannes den ygste jon, qualified P1810 subject named as Jon Tørresson Tørresson Grannes den ygste jon
LAST	P2600	"6000000005607475221"	P1810	"Jon Tørresson Tørresson Grannes den ygste jon"
#   P569 date of birth = +1711-00-00T00:00:00Z/9
LAST	P569	+1711-00-00T00:00:00Z/9	S2600	"6000000005607475221"
#   P570 date of death = +1794-00-00T00:00:00Z/9
LAST	P570	+1794-00-00T00:00:00Z/9	S2600	"6000000005607475221"
#   P40 child = Q141219349 Tørres Jonson Grannes
LAST	P40	Q141219349	S2600	"6000000005607475221"
#   P40 child = Q141244120 Ragnhild Jonsdatter Grannes
LAST	P40	Q141244120	S2600	"6000000005607475221"
#   Q141219349 Tørres Jonson Grannes: P22 father = the item just created
Q141219349	P22	LAST	S2600	"6000000005607475221"
#   Q141244120 Ragnhild Jonsdatter Grannes: P22 father = the item just created
Q141244120	P22	LAST	S2600	"6000000005607475221"
#   the item just created: P735 given name = Q13501137 Jon
LAST	P735	Q13501137
#   P734 family name = Q37442010 Grannes, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q37442010	P3831	Q2507958
#   P734 family name = Q37442010 Grannes
LAST	P734	Q37442010
#   add a mul alias "Jon Tørresen Grannes"
LAST	Amul	"Jon Tørresen Grannes"
#   add a mul alias "Jon Grannes"
LAST	Amul	"Jon Grannes"

# create a new item
CREATE
#   set the en label to "Malena Rasmusdatter Fosse"
LAST	Len	"Malena Rasmusdatter Fosse"
#   set the mul label to "Malena Rasmusdatter Fosse"
LAST	Lmul	"Malena Rasmusdatter Fosse"
#   add a mul alias "Malena Rasmusdatter Ree"
LAST	Amul	"Malena Rasmusdatter Ree"
#   set the ja label to "マレーナ・ラスムスダッテル・フォッシー"
LAST	Lja	"マレーナ・ラスムスダッテル・フォッシー"
#   set the zh label to "马莱纳·拉斯穆斯达特·福塞"
LAST	Lzh	"马莱纳·拉斯穆斯达特·福塞"
#   set the ko label to "마레나 라스무스다테르 포세"
LAST	Lko	"마레나 라스무스다테르 포세"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000009447665156 Malena Rasmusdatter Fosse, qualified P1810 subject named as Malena Rasmusdatter Ree
LAST	P2600	"6000000009447665156"	P1810	"Malena Rasmusdatter Ree"
#   P569 date of birth = +1643-00-00T00:00:00Z/9
LAST	P569	+1643-00-00T00:00:00Z/9	S2600	"6000000009447665156"
#   P570 date of death = +1675-00-00T00:00:00Z/9
LAST	P570	+1675-00-00T00:00:00Z/9	S2600	"6000000009447665156"
#   P40 child = Q141219189 Eivind Svenson Sveinsen Garborg
LAST	P40	Q141219189	S2600	"6000000009447665156"
#   Q141219189 Eivind Svenson Sveinsen Garborg: P25 mother = the item just created
Q141219189	P25	LAST	S2600	"6000000009447665156"
#   the item just created: P735 given name = Q5990536 Malena
LAST	P735	Q5990536
#   P5056 patronym or matronym = Q141223475
LAST	P5056	Q141223475
#   P734 family name = Q30087759 Ree, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q30087759	P3831	Q2507958
#   P734 family name = Q26884133 Fosse, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q26884133	P3831	Q28418670
#   add a mul alias "Malli Fosse"
LAST	Amul	"Malli Fosse"
#   add a mul alias "Malena Fosse"
LAST	Amul	"Malena Fosse"

# create a new item
CREATE
#   set the en label to "Maren Wangelsten Abrahamsdatter Felthuus"
LAST	Len	"Maren Wangelsten Abrahamsdatter Felthuus"
#   set the mul label to "Maren Wangelsten Abrahamsdatter Felthuus"
LAST	Lmul	"Maren Wangelsten Abrahamsdatter Felthuus"
#   set the ja label to "マレン・ヴァンゲルステン・アブラハムスダッテル・フェルトウス"
LAST	Lja	"マレン・ヴァンゲルステン・アブラハムスダッテル・フェルトウス"
#   set the zh label to "马伦·万盖尔斯滕·阿布拉哈姆斯达特·费尔图乌斯"
LAST	Lzh	"马伦·万盖尔斯滕·阿布拉哈姆斯达特·费尔图乌斯"
#   set the ko label to "마렌 와엘스텐 압라함스다테르 펠투우스"
LAST	Lko	"마렌 와엘스텐 압라함스다테르 펠투우스"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000013476826763 Maren Wangelsten Abrahamsdatter Felthuus, qualified P1810 subject named as Maren Wangelsten Abrahamsdatter Felthuus
LAST	P2600	"6000000013476826763"	P1810	"Maren Wangelsten Abrahamsdatter Felthuus"
#   P569 date of birth = +1754-00-00T00:00:00Z/9
LAST	P569	+1754-00-00T00:00:00Z/9	S2600	"6000000013476826763"
#   P570 date of death = +1821-04-10T00:00:00Z/11
LAST	P570	+1821-04-10T00:00:00Z/11	S2600	"6000000013476826763"
#   P26 spouse = Q141244094 Gunder Asbjørnsen Bøe
LAST	P26	Q141244094	S2600	"6000000013476826763"
#   P40 child = Q141257159 Abraham Felthuus Bøe
LAST	P40	Q141257159	S2600	"6000000013476826763"
#   Q141244094 Gunder Asbjørnsen Bøe: P26 spouse = the item just created
Q141244094	P26	LAST	S2600	"6000000013476826763"
#   Q141257159 Abraham Felthuus Bøe: P25 mother = the item just created
Q141257159	P25	LAST	S2600	"6000000013476826763"
#   the item just created: P735 given name = Q1666203 Maren, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q1666203	P1545	"1"	P7452	Q3409033
#   add a mul alias "Abrahamsdatter Felthuus"
LAST	Amul	"Abrahamsdatter Felthuus"

# create a new item
CREATE
#   set the en label to "Margareta Lithman"
LAST	Len	"Margareta Lithman"
#   set the mul label to "Margareta Lithman"
LAST	Lmul	"Margareta Lithman"
#   set the ja label to "マルガレータ・リトマン"
LAST	Lja	"マルガレータ・リトマン"
#   set the zh label to "瑪格麗塔·利特曼"
LAST	Lzh	"瑪格麗塔·利特曼"
#   set the ko label to "마르가레타 리트만"
LAST	Lko	"마르가레타 리트만"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000008394390957 Margareta Lithman, qualified P1810 subject named as Margareta Lithman
LAST	P2600	"6000000008394390957"	P1810	"Margareta Lithman"
#   P22 father = Q5960165 Carolus Nicolai Lithman
LAST	P22	Q5960165	S2600	"6000000008394390957"
#   Q5960165 Carolus Nicolai Lithman: P40 child = the item just created
Q5960165	P40	LAST	S2600	"6000000008394390957"
#   the item just created: P735 given name = Q8274988 Margareta
LAST	P735	Q8274988
#   P734 family name = Q47468803 Lithman
LAST	P734	Q47468803

# create a new item
CREATE
#   set the en label to "Nils Carlsson Posse af Säby"
LAST	Len	"Nils Carlsson Posse af Säby"
#   set the mul label to "Nils Carlsson Posse af Säby"
LAST	Lmul	"Nils Carlsson Posse af Säby"
#   set the ja label to "ニルス・カールソン・ポッセ・アフ・セビ"
LAST	Lja	"ニルス・カールソン・ポッセ・アフ・セビ"
#   set the zh label to "尼尔斯·卡尔尔松·波塞·阿夫·塞比"
LAST	Lzh	"尼尔斯·卡尔尔松·波塞·阿夫·塞比"
#   set the ko label to "닐스 카르르손 포세 아프 세비"
LAST	Lko	"닐스 카르르손 포세 아프 세비"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000009119902271 Nils Carlsson Posse af Säby, qualified P1810 subject named as Nils Carlsson Posse af Säby
LAST	P2600	"6000000009119902271"	P1810	"Nils Carlsson Posse af Säby"
#   P569 date of birth = +1733-00-00T00:00:00Z/9
LAST	P569	+1733-00-00T00:00:00Z/9	S2600	"6000000009119902271"
#   P570 date of death = +1786-00-00T00:00:00Z/9
LAST	P570	+1786-00-00T00:00:00Z/9	S2600	"6000000009119902271"
#   P22 father = Q99460476 Carl Henrik Posse af Säby
LAST	P22	Q99460476	S2600	"6000000009119902271"
#   P25 mother = Q141250228 Helena Åkesdotter Soop
LAST	P25	Q141250228	S2600	"6000000009119902271"
#   Q99460476 Carl Henrik Posse af Säby: P40 child = the item just created
Q99460476	P40	LAST	S2600	"6000000009119902271"
#   Q141250228 Helena Åkesdotter Soop: P40 child = the item just created
Q141250228	P40	LAST	S2600	"6000000009119902271"

# create a new item
CREATE
#   the item just created: set the en label to "Ole Kristiansen Sør-Reime"
LAST	Len	"Ole Kristiansen Sør-Reime"
#   set the mul label to "Ole Kristiansen Sør-Reime"
LAST	Lmul	"Ole Kristiansen Sør-Reime"
#   set the ja label to "オーレ・クリスチャンセン・セール・レイメ"
LAST	Lja	"オーレ・クリスチャンセン・セール・レイメ"
#   set the zh label to "奥勒·克里斯蒂安森·瑟尔·雷梅"
LAST	Lzh	"奥勒·克里斯蒂安森·瑟尔·雷梅"
#   set the ko label to "오레 크리스티안센 쇠르레이메"
LAST	Lko	"오레 크리스티안센 쇠르레이메"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000224702600859 Ole Kristiansen Sør-Reime, qualified P1810 subject named as Ole Kristiansen Sør-Reime
LAST	P2600	"6000000224702600859"	P1810	"Ole Kristiansen Sør-Reime"
#   P569 date of birth = +1884-03-23T00:00:00Z/11
LAST	P569	+1884-03-23T00:00:00Z/11	S2600	"6000000224702600859"
#   P22 father = Q141189076 Kristian Larsen Sør-Reime
LAST	P22	Q141189076	S2600	"6000000224702600859"
#   the item just created: P735 given name = Q2097883 Ole
LAST	P735	Q2097883
#   P734 family name = Q141189041
LAST	P734	Q141189041

# create a new item
CREATE
#   set the en label to "Olof Reftelius"
LAST	Len	"Olof Reftelius"
#   set the mul label to "Olof Reftelius"
LAST	Lmul	"Olof Reftelius"
#   set the ja label to "オロフ・レフテリウス"
LAST	Lja	"オロフ・レフテリウス"
#   set the zh label to "奥洛夫·雷夫特利乌斯"
LAST	Lzh	"奥洛夫·雷夫特利乌斯"
#   set the ko label to "오로프 레프테류스"
LAST	Lko	"오로프 레프테류스"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000026434671579 Olof Reftelius, qualified P1810 subject named as Olof Reftelius
LAST	P2600	"6000000026434671579"	P1810	"Olof Reftelius"
#   P22 father = Q6066136 Johannes Petri Reftelius Ostrogothus
LAST	P22	Q6066136	S2600	"6000000026434671579"
#   P26 spouse = Q141257176 Elisabeth Westius
LAST	P26	Q141257176	S2600	"6000000026434671579"
#   P40 child = Q6066129 Johan Martin Reftelius
LAST	P40	Q6066129	S2600	"6000000026434671579"
#   Q6066136 Johannes Petri Reftelius Ostrogothus: P40 child = the item just created
Q6066136	P40	LAST	S2600	"6000000026434671579"
#   Q141257176 Elisabeth Westius: P26 spouse = the item just created
Q141257176	P26	LAST	S2600	"6000000026434671579"
#   Q6066129 Johan Martin Reftelius: P22 father = the item just created
Q6066129	P22	LAST	S2600	"6000000026434671579"
#   the item just created: P735 given name = Q18089653 Olof
LAST	P735	Q18089653

# create a new item
CREATE
#   set the en label to "Rakel Jorina Olsdatter Nord-Varhaug"
LAST	Len	"Rakel Jorina Olsdatter Nord-Varhaug"
#   set the mul label to "Rakel Jorina Olsdatter Nord-Varhaug"
LAST	Lmul	"Rakel Jorina Olsdatter Nord-Varhaug"
#   add a mul alias "Rakel Jorina Olsdatter Torland"
LAST	Amul	"Rakel Jorina Olsdatter Torland"
#   set the ja label to "ラケル・ヨリナ・オルスダッテル・ノール・ヴァールハウグ"
LAST	Lja	"ラケル・ヨリナ・オルスダッテル・ノール・ヴァールハウグ"
#   set the zh label to "拉凯尔·约里纳·奥尔斯达特·诺尔·瓦尔豪格"
LAST	Lzh	"拉凯尔·约里纳·奥尔斯达特·诺尔·瓦尔豪格"
#   set the ko label to "라켈 조리나 올스다테르 노르드바르하욱"
LAST	Lko	"라켈 조리나 올스다테르 노르드바르하욱"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000029302515541 Rakel Jorina Olsdatter Nord-Varhaug, qualified P1810 subject named as Rakel Jorina Olsdatter Torland
LAST	P2600	"6000000029302515541"	P1810	"Rakel Jorina Olsdatter Torland"
#   P569 date of birth = +1850-03-01T00:00:00Z/11
LAST	P569	+1850-03-01T00:00:00Z/11	S2600	"6000000029302515541"
#   P570 date of death = +1897-07-18T00:00:00Z/11
LAST	P570	+1897-07-18T00:00:00Z/11	S2600	"6000000029302515541"
#   P26 spouse = Q141189076 Kristian Larsen Sør-Reime
LAST	P26	Q141189076	S2600	"6000000029302515541"
#   the item just created: P735 given name = Q16424094 Rakel, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q16424094	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1703982, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1703982	P1545	"2"	P3831	Q245025
#   P5056 patronym or matronym = Q51885688 Olsdatter
LAST	P5056	Q51885688
#   P734 family name = Q40017769, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q40017769	P3831	Q2507958
#   add a mul alias "Rakel Jorina Nord-Varhaug"
LAST	Amul	"Rakel Jorina Nord-Varhaug"

# create a new item
CREATE
#   set the en label to "Rasmus Viby Andersson Øystre Bore"
LAST	Len	"Rasmus Viby Andersson Øystre Bore"
#   set the mul label to "Rasmus Viby Andersson Øystre Bore"
LAST	Lmul	"Rasmus Viby Andersson Øystre Bore"
#   set the ja label to "ラスムス・ヴィービー・アンデション・オイストレ・ボレ"
LAST	Lja	"ラスムス・ヴィービー・アンデション・オイストレ・ボレ"
#   set the zh label to "拉斯穆斯·维比·安德松·奥伊斯特雷·博雷"
LAST	Lzh	"拉斯穆斯·维比·安德松·奥伊斯特雷·博雷"
#   set the ko label to "라스무스 비비 안데르손 외이스트레 보레"
LAST	Lko	"라스무스 비비 안데르손 외이스트레 보레"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000002866078652 Rasmus Viby Andersson Øystre Bore, qualified P1810 subject named as Rasmus Viby Andersson Øystre Bore
LAST	P2600	"6000000002866078652"	P1810	"Rasmus Viby Andersson Øystre Bore"
#   P569 date of birth = +1758-00-00T00:00:00Z/9
LAST	P569	+1758-00-00T00:00:00Z/9	S2600	"6000000002866078652"
#   P570 date of death = +1814-03-13T00:00:00Z/11
LAST	P570	+1814-03-13T00:00:00Z/11	S2600	"6000000002866078652"
#   P40 child = Q141225676 Anders Rasmusson Lea
LAST	P40	Q141225676	S2600	"6000000002866078652"
#   Q141225676 Anders Rasmusson Lea: P22 father = the item just created
Q141225676	P22	LAST	S2600	"6000000002866078652"

# create a new item
CREATE
#   the item just created: set the en label to "Reiar Jakobsen Bratt-Hetland"
LAST	Len	"Reiar Jakobsen Bratt-Hetland"
#   set the mul label to "Reiar Jakobsen Bratt-Hetland"
LAST	Lmul	"Reiar Jakobsen Bratt-Hetland"
#   set the ja label to "レイアル・ヤコブセン・ブラトヘトランド"
LAST	Lja	"レイアル・ヤコブセン・ブラトヘトランド"
#   set the zh label to "雷伊阿尔·雅科布森·布拉特赫特兰德"
LAST	Lzh	"雷伊阿尔·雅科布森·布拉特赫特兰德"
#   set the ko label to "레이아르 자콥센 브라테트란드"
LAST	Lko	"레이아르 자콥센 브라테트란드"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000010673340669 Reiar Jakobsen Bratt-Hetland, qualified P1810 subject named as Reiar Jakobsen Bratt-Hetland
LAST	P2600	"6000000010673340669"	P1810	"Reiar Jakobsen Bratt-Hetland"
#   P569 date of birth = +1641-00-00T00:00:00Z/9
LAST	P569	+1641-00-00T00:00:00Z/9	S2600	"6000000010673340669"
#   P570 date of death = +1720-00-00T00:00:00Z/9
LAST	P570	+1720-00-00T00:00:00Z/9	S2600	"6000000010673340669"
#   P25 mother = Q141257274 NN Pedersdatter Foss
LAST	P25	Q141257274	S2600	"6000000010673340669"
#   Q141257274 NN Pedersdatter Foss: P40 child = the item just created
Q141257274	P40	LAST	S2600	"6000000010673340669"
#   the item just created: add a mul alias "Reiar Bratt-Hetland"
LAST	Amul	"Reiar Bratt-Hetland"

# create a new item
CREATE
#   set the en label to "Sofia Arendtsdotter Renmark"
LAST	Len	"Sofia Arendtsdotter Renmark"
#   set the mul label to "Sofia Arendtsdotter Renmark"
LAST	Lmul	"Sofia Arendtsdotter Renmark"
#   set the ja label to "ソフィア・アレンドトスドッテル・レンマルク"
LAST	Lja	"ソフィア・アレンドトスドッテル・レンマルク"
#   set the zh label to "索菲娅·阿伦德特斯多特·伦马尔克"
LAST	Lzh	"索菲娅·阿伦德特斯多特·伦马尔克"
#   set the ko label to "소피아 아렌드츠도테르 렌마르크"
LAST	Lko	"소피아 아렌드츠도테르 렌마르크"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000026814652600 Sofia Arendtsdotter Renmark, qualified P1810 subject named as Sofia Arendtsdotter Renmark
LAST	P2600	"6000000026814652600"	P1810	"Sofia Arendtsdotter Renmark"
#   P40 child = Q141244108 Margareta Stecksenia
LAST	P40	Q141244108	S2600	"6000000026814652600"
#   Q141244108 Margareta Stecksenia: P25 mother = the item just created
Q141244108	P25	LAST	S2600	"6000000026814652600"

# create a new item
CREATE
#   the item just created: set the en label to "Stine Olsdatter Bore"
LAST	Len	"Stine Olsdatter Bore"
#   set the mul label to "Stine Olsdatter Bore"
LAST	Lmul	"Stine Olsdatter Bore"
#   set the ja label to "スティーネ・オルスダッテル・ボレ"
LAST	Lja	"スティーネ・オルスダッテル・ボレ"
#   set the zh label to "斯蒂内·奥尔斯达特·博雷"
LAST	Lzh	"斯蒂内·奥尔斯达特·博雷"
#   set the ko label to "스티네 올스다테르 보레"
LAST	Lko	"스티네 올스다테르 보레"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000002866077692 Stine Olsdatter Bore, qualified P1810 subject named as Stine Olsdatter Bore
LAST	P2600	"6000000002866077692"	P1810	"Stine Olsdatter Bore"
#   P569 date of birth = +1765-00-00T00:00:00Z/9
LAST	P569	+1765-00-00T00:00:00Z/9	S2600	"6000000002866077692"
#   P570 date of death = +1846-11-26T00:00:00Z/11
LAST	P570	+1846-11-26T00:00:00Z/11	S2600	"6000000002866077692"
#   P40 child = Q141225676 Anders Rasmusson Lea
LAST	P40	Q141225676	S2600	"6000000002866077692"
#   Q141225676 Anders Rasmusson Lea: P25 mother = the item just created
Q141225676	P25	LAST	S2600	"6000000002866077692"

# create a new item
CREATE
#   the item just created: set the en label to "Udbjørg Tormodsdatter Foss"
LAST	Len	"Udbjørg Tormodsdatter Foss"
#   set the mul label to "Udbjørg Tormodsdatter Foss"
LAST	Lmul	"Udbjørg Tormodsdatter Foss"
#   add a mul alias "Udbjørg Tormodsdatter Tormodsdatter Foss"
LAST	Amul	"Udbjørg Tormodsdatter Tormodsdatter Foss"
#   set the ja label to "ウドブヨルグ・トルモドスダッテル・フォス"
LAST	Lja	"ウドブヨルグ・トルモドスダッテル・フォス"
#   set the zh label to "乌德布约尔格·托尔莫德斯达特·福斯"
LAST	Lzh	"乌德布约尔格·托尔莫德斯达特·福斯"
#   set the ko label to "우드브죄르그 토르모드스다테르 포스"
LAST	Lko	"우드브죄르그 토르모드스다테르 포스"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000007980729070 Udbjørg Tormodsdatter Foss, qualified P1810 subject named as Udbjørg Tormodsdatter Tormodsdatter Foss
LAST	P2600	"6000000007980729070"	P1810	"Udbjørg Tormodsdatter Tormodsdatter Foss"
#   P569 date of birth = +1555-00-00T00:00:00Z/9
LAST	P569	+1555-00-00T00:00:00Z/9	S2600	"6000000007980729070"
#   P570 date of death = +1645-00-00T00:00:00Z/9
LAST	P570	+1645-00-00T00:00:00Z/9	S2600	"6000000007980729070"
#   P26 spouse = Q141244226 Knut Bjørnson Bjørheim
LAST	P26	Q141244226	S2600	"6000000007980729070"
#   P40 child = Q141250249 Sissel Knutsdatter Bjørheim
LAST	P40	Q141250249	S2600	"6000000007980729070"
#   Q141244226 Knut Bjørnson Bjørheim: P26 spouse = the item just created
Q141244226	P26	LAST	S2600	"6000000007980729070"
#   Q141250249 Sissel Knutsdatter Bjørheim: P25 mother = the item just created
Q141250249	P25	LAST	S2600	"6000000007980729070"
#   the item just created: P734 family name = Q16870001 Foss, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q16870001	P3831	Q2507958
#   P734 family name = Q16870001 Foss, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q16870001	P3831	Q28418670
#   add a mul alias "Udbjørg Foss"
LAST	Amul	"Udbjørg Foss"
#   Q105796231 Margareta Gödiksdotter Fincke till Kanckas: P735 given name = Q8274988 Margareta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q105796231	P735	Q8274988	P1545	"1"	P7452	Q3409033
#   Q110386205 Lars Bengtsson Hierta till Kålsholmen: P735 given name = Q15635262 Lars, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110386205	P735	Q15635262	P1545	"1"	P7452	Q3409033
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
#   Q141257174 Elisabet Zachariasdotter Plantin: P40 child = Q141257162 Catharina Abrahamsdotter Burman
Q141257174	P40	Q141257162	S2600	"6000000000159955623"
#   Q104383015 Evert Wilhelm Bruncrona: P735 given name = Q13580919 Evert, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q104383015	P735	Q13580919	P1545	"1"	P7452	Q3409033
#   P735 given name = Q11027623, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q104383015	P735	Q11027623	P1545	"2"	P3831	Q245025
#   Q136376387 Ebba Kristina Carlsdotter: P735 given name = Q2242896 Ebba, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q136376387	P735	Q2242896	P1545	"1"	P7452	Q3409033
#   P735 given name = Q19798802 Kristina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q136376387	P735	Q19798802	P1545	"2"	P3831	Q245025
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
#   Q110378177 Adelheid von Plain: P735 given name = Q4057477 Adelheid, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110378177	P735	Q4057477	P1545	"1"	P7452	Q3409033
#   Q116007123 Costanza di Niccolò Cavalcanti: P735 given name = Q19816831 Costanza, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q116007123	P735	Q19816831	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1984713 Niccolò, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q116007123	P735	Q1984713	P1545	"3"	P3831	Q245025
#   P734 family name = Q21450357 Cavalcanti
Q116007123	P734	Q21450357
#   Q141257162 Catharina Abrahamsdotter Burman: P25 mother = Q141257174 Elisabet Zachariasdotter Plantin
Q141257162	P25	Q141257174	S2600	"6000000003966326458"
#   P26 spouse = Q141257291 Nils Sundius
Q141257162	P26	Q141257291	S2600	"6000000003966326458"
#   Q141257291 Nils Sundius: P26 spouse = Q141257162 Catharina Abrahamsdotter Burman
Q141257291	P26	Q141257162	S2600	"6000000003966366446"
#   Q110548816 Lovisa Thott: P735 given name = Q10570000 Lovisa
Q110548816	P735	Q10570000
#   P734 family name = Q47528688 Thott
Q110548816	P734	Q47528688
#   Q139997218 Albrecht Jonsson Behm: P40 child = Q140192133 Sara Albrektsdotter Swedberg
Q139997218	P40	Q140192133	S2600	"6000000004577963540"
#   P2600 Geni.com profile ID = 6000000004577963540 Albrecht Jonsson Behm, qualified P1810 subject named as Albrecht Jonsson Behm
Q139997218	P2600	"6000000004577963540"	P1810	"Albrecht Jonsson Behm"
#   Q141257266 Mattias Tollefsen Vatnamot: P26 spouse = Q141257173 Elen Pedersdatter Vatnamot
Q141257266	P26	Q141257173	S2600	"6000000005607089279"
#   Q141257173 Elen Pedersdatter Vatnamot: P26 spouse = Q141257266 Mattias Tollefsen Vatnamot
Q141257173	P26	Q141257266	S2600	"6000000005607089288"
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
#   Q141257299 Rasmus Lydikson Amdal: P40 child = Q141257264 Lydik Rasmussen Amdal
Q141257299	P40	Q141257264	S2600	"6000000007980728992"
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
#   Q141257264 Lydik Rasmussen Amdal: P22 father = Q141257299 Rasmus Lydikson Amdal
Q141257264	P22	Q141257299	S2600	"6000000023605569477"
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
#   Q141257237 Julie Wilkens Engebretsen: P26 spouse = Q141257311 Waldemar Leopold Engebretsen
Q141257237	P26	Q141257311	S2600	"6000000036729993087"
#   Q141257311 Waldemar Leopold Engebretsen: P26 spouse = Q141257237 Julie Wilkens Engebretsen
Q141257311	P26	Q141257237	S2600	"6000000036747100847"
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

