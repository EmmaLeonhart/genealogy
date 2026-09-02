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
#   2662 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   set the ja label to "エングエランド・ル・バティセウル・デ・コウシ・イイイ"
Q933505	Lja	"エングエランド・ル・バティセウル・デ・コウシ・イイイ"
#   set the zh label to "恩古埃兰德·勒·巴蒂塞乌尔·德·科乌西·伊伊伊"
Q933505	Lzh	"恩古埃兰德·勒·巴蒂塞乌尔·德·科乌西·伊伊伊"
#   set the ja label to "カール・コンスタンティン・デ・カルナル"
Q5618560	Lja	"カール・コンスタンティン・デ・カルナル"
#   set the ko label to "미챌 판트"
Q5725186	Lko	"미챌 판트"
#   Q141223432 Osmund Larsson Nese: set the ko label to "오스문드 라르손 네세"
Q141223432	Lko	"오스문드 라르손 네세"
#   Q141223542 Margareta Elisabet Roos: set the ko label to "마르가레타 에리사베트 루스"
Q141223542	Lko	"마르가레타 에리사베트 루스"
#   Q141225230 Osmund Andersen Tunheim: set the ko label to "오스문드 안데르센 툰헤임"
Q141225230	Lko	"오스문드 안데르센 툰헤임"
#   set the ko label to "마티아스 스튜츄스"
Q456456	Lko	"마티아스 스튜츄스"
#   Q141249620 Ola Kristoffersen Kartevoll: add a mul alias "Ola Kristoffersen Kartevoll *"
Q141249620	Amul	"Ola Kristoffersen Kartevoll *"
#   set the ko label to "우노 본 트로일"
Q943803	Lko	"우노 본 트로일"
#   Q141223429 Magdalena Elisabet Tersmeden: set the ko label to "막다레나 에리사베트 테르스메덴"
Q141223429	Lko	"막다레나 에리사베트 테르스메덴"
#   set the ko label to "이에보르그 시몬스다테르 이트레 리마"
Q141225713	Lko	"이에보르그 시몬스다테르 이트레 리마"
#   set the ko label to "미챌 퇴르느프리츠트"
Q6218214	Lko	"미챌 퇴르느프리츠트"
#   set the ko label to "이베르 페데르센 산드스마르크"
Q141198422	Lko	"이베르 페데르센 산드스마르크"
#   set the ko label to "마르테 구리에 오스문드스다테르 웨란드"
Q141216636	Lko	"마르테 구리에 오스문드스다테르 웨란드"

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
#   Q138582215 Eva Christina Eriksdotter de Besche: P735 given name = Q64412279 Eva, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q138582215	P735	Q64412279	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1083457 Christina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q138582215	P735	Q1083457	P1545	"2"	P3831	Q245025
#   P5056 patronym or matronym = Q130232912 Eriksdotter
Q138582215	P5056	Q130232912
#   Q469962 Eva Sophia Sofia von Fersen: P735 given name = Q64412279 Eva, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q469962	P735	Q64412279	P1545	"1"	P7452	Q3409033
#   P735 given name = Q2302787 Sophia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q469962	P735	Q2302787	P1545	"2"	P3831	Q245025
#   P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q469962	P735	Q18201520	P1545	"3"	P3831	Q245025
#   Q6235986 Carl Gustaf Wennerstedt: P735 given name = Q2529610 Carl, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q6235986	P735	Q2529610	P1545	"1"	P7452	Q3409033
#   P735 given name = Q15646212 Gustaf, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q6235986	P735	Q15646212	P1545	"2"	P3831	Q245025
#   Q29246906 Eleonora Juliana Wiggman: P735 given name = Q18759077 Eleonora, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q29246906	P735	Q18759077	P1545	"1"	P7452	Q3409033
#   P735 given name = Q12900572 Juliana, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q29246906	P735	Q12900572	P1545	"2"	P3831	Q245025
#   Q4830275 Axel Gustaf Gyllenkrok: P735 given name = Q15646212 Gustaf, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q4830275	P735	Q15646212	P1545	"2"	P3831	Q245025
#   Q105796231 Margareta Gödiksdotter Fincke till Kanckas: P735 given name = Q8274988 Margareta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q105796231	P735	Q8274988	P1545	"1"	P7452	Q3409033
#   Q110386205 Lars Bengtsson Hierta till Kålsholmen: P735 given name = Q15635262 Lars, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110386205	P735	Q15635262	P1545	"1"	P7452	Q3409033
#   Q109952542 Catharina Sabina Crail von Bamberg: P735 given name = Q17317997 Catharina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q109952542	P735	Q17317997	P1545	"1"	P7452	Q3409033
#   P735 given name = Q4964490 Sabina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q109952542	P735	Q4964490	P1545	"2"	P3831	Q245025
#   Q2183430 Bengta Ebbesdotter Ebbesdatter Hvide Queen of Sweden: P735 given name = Q20899047 Queen, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q2183430	P735	Q20899047	P1545	"3"	P3831	Q245025
#   P734 family name = Q37437749
Q2183430	P734	Q37437749
#   Q6045829 Johan Teodor Petré: P735 given name = Q7701015 Teodor, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q6045829	P735	Q7701015	P1545	"2"	P3831	Q245025
#   Q6011791 Ruben Frans Isendorf Nilson: P735 given name = Q18114894 Ruben, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q6011791	P735	Q18114894	P1545	"1"	P7452	Q3409033
#   P735 given name = Q3480175 Frans, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q6011791	P735	Q3480175	P1545	"2"	P3831	Q245025
#   Q104172926 Carl Johan Oskar von Numers: P735 given name = Q2529610 Carl, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q104172926	P735	Q2529610	P1545	"1"	P7452	Q3409033
#   P735 given name = Q10989273 Johan, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q104172926	P735	Q10989273	P1545	"2"	P3831	Q245025
#   P735 given name = Q18145769 Oskar, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q104172926	P735	Q18145769	P1545	"3"	P3831	Q245025
#   Q101247544 Anna Göransdotter Snakenborg: P735 given name = Q666578 Anna
Q101247544	P735	Q666578
#   Q75917080 Catherine Constantia Pellew: P735 given name = Q2218095 Catherine, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q75917080	P735	Q2218095	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1127708 Constantia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q75917080	P735	Q1127708	P1545	"2"	P3831	Q245025
#   Q135441621 Carl Lagerborg: P735 given name = Q2529610 Carl
Q135441621	P735	Q2529610
#   Q2415388 Carl Gustaf Mannerheim: P735 given name = Q2529610 Carl, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q2415388	P735	Q2529610	P1545	"1"	P7452	Q3409033
#   P735 given name = Q15646212 Gustaf, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q2415388	P735	Q15646212	P1545	"2"	P3831	Q245025
#   Q5975022 Lars August Mannerheim: P735 given name = Q370731 August, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5975022	P735	Q370731	P1545	"2"	P3831	Q245025
#   Q56403540 Daniel Lindh: P735 given name = Q53787734 Daniel
Q56403540	P735	Q53787734
#   Q110561236 Christina Fjodorovna Rosladin: P735 given name = Q1083457 Christina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110561236	P735	Q1083457	P1545	"1"	P7452	Q3409033
#   Q6371586 Carl August Ramsay: P735 given name = Q2529610 Carl, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q6371586	P735	Q2529610	P1545	"1"	P7452	Q3409033
#   P735 given name = Q370731 August, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q6371586	P735	Q370731	P1545	"2"	P3831	Q245025
#   Q130772654 Hedvig Christina Creutz: P735 given name = Q13648620 Hedvig, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q130772654	P735	Q13648620	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1083457 Christina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q130772654	P735	Q1083457	P1545	"2"	P3831	Q245025
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
#   Q5749466 Henrik Gahn: P735 given name = Q594279 Henrik
Q5749466	P735	Q594279
#   Q104383015 Evert Wilhelm Bruncrona: P735 given name = Q13580919 Evert, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q104383015	P735	Q13580919	P1545	"1"	P7452	Q3409033
#   P735 given name = Q11027623, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q104383015	P735	Q11027623	P1545	"2"	P3831	Q245025
#   Q593706 Nils Gustaf Nordenskiöld: P735 given name = Q15646212 Gustaf, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q593706	P735	Q15646212	P1545	"2"	P3831	Q245025
#   Q136376387 Ebba Kristina Carlsdotter: P735 given name = Q2242896 Ebba, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q136376387	P735	Q2242896	P1545	"1"	P7452	Q3409033
#   P735 given name = Q19798802 Kristina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q136376387	P735	Q19798802	P1545	"2"	P3831	Q245025
#   Q110457044 Anna Magdalena Pauli: P735 given name = Q842544 Magdalena, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110457044	P735	Q842544	P1545	"2"	P3831	Q245025
#   Q72388326 Isabel de Vipont: P735 given name = Q4218918 Isabel, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q72388326	P735	Q4218918	P1545	"1"	P7452	Q3409033
#   Q6190771 Carl Emil Knut Карлов Stjernvall-Walleen: P735 given name = Q2529610 Carl, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q6190771	P735	Q2529610	P1545	"1"	P7452	Q3409033
#   P735 given name = Q943881 Knut, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q6190771	P735	Q943881	P1545	"3"	P3831	Q245025
#   Q110304710 Leveke Dorothea von Levetzow: P735 given name = Q909253 Dorothea, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110304710	P735	Q909253	P1545	"2"	P3831	Q245025
#   Q130683609 Cecilia Lucia Brodersen: P735 given name = Q859234 Cecilia, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q130683609	P735	Q859234	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1160640 Lucia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q130683609	P735	Q1160640	P1545	"2"	P3831	Q245025
#   Q94910724 Joachim Engelke von Bernstorff: P735 given name = Q4926961 Joachim, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q94910724	P735	Q4926961	P1545	"1"	P7452	Q3409033
#   Q2066886 Hedvig Catharina Charlotta De la Gardie: P735 given name = Q17317997 Catharina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q2066886	P735	Q17317997	P1545	"2"	P3831	Q245025
#   P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q2066886	P735	Q1067071	P1545	"3"	P3831	Q245025
#   Q455071 Hans Axel von Fersen: P735 given name = Q5407300 Axel, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q455071	P735	Q5407300	P1545	"2"	P3831	Q245025
#   Q933505 Enguerrand Le Bâtisseur de Coucy III: P735 given name = Q1342982 Enguerrand, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q933505	P735	Q1342982	P1545	"1"	P7452	Q3409033
#   Q136376245 Fredrik Elof Gyllenkrok RSO: P25 mother = Q2965864 Christina Charlotta Cederström
Q136376245	P25	Q2965864	S2600	"6000000001606349437"
#   P2600 Geni.com profile ID = 6000000001606349437 Fredrik Elof Gyllenkrok RSO, qualified P1810 subject named as Fredrik Elof Gyllenkrok RSO
Q136376245	P2600	"6000000001606349437"	P1810	"Fredrik Elof Gyllenkrok RSO"
#   P735 given name = Q4926491 Fredrik, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q136376245	P735	Q4926491	P1545	"1"	P7452	Q3409033
#   P735 given name = Q3366319 Elof, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q136376245	P735	Q3366319	P1545	"2"	P3831	Q245025
#   Q110547994 Elisabeth von Saveland: P735 given name = Q63611044 Elisabeth, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110547994	P735	Q63611044	P1545	"1"	P7452	Q3409033
#   Q5575607 Nils Adam Turesson Bielke: P5056 patronym or matronym = Q130232969 Turesson
Q5575607	P5056	Q130232969
#   Q5575580 Gustaf Ture Bielke: P735 given name = Q2460609 Ture, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5575580	P735	Q2460609	P1545	"2"	P3831	Q245025
#   Q19976400 Abraham Burensund: P735 given name = Q4055996 Abraham
Q19976400	P735	Q4055996
#   Q30879127 Guiges Guy de Forez VII: P735 given name = Q1159023 Guy, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q30879127	P735	Q1159023	P1545	"2"	P3831	Q245025
#   Q5626011 Gustaf Duwall: P735 given name = Q15646212 Gustaf
Q5626011	P735	Q15646212
#   Q6145888 Göran Ludvig von Köhler: P735 given name = Q1559427 Göran, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q6145888	P735	Q1559427	P1545	"1"	P7452	Q3409033
#   Q19721217 Salomon Christoffer von Köhler: P735 given name = Q1084384 Christoffer, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q19721217	P735	Q1084384	P1545	"2"	P3831	Q245025
#   Q5618560 Carl Constantin de Carnall: P735 given name = Q2529610 Carl, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q5618560	P735	Q2529610	P1545	"1"	P7452	Q3409033
#   P735 given name = Q5163687 Constantin, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5618560	P735	Q5163687	P1545	"2"	P3831	Q245025
#   Q94938559 Friedrich Frommhold von Knorring: P735 given name = Q14038597 Friedrich, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q94938559	P735	Q14038597	P1545	"1"	P7452	Q3409033
#   Q10608167 Olaus Petri Niurenius: P735 given name = Q10625184 Petri, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q10608167	P735	Q10625184	P1545	"2"	P3831	Q245025
#   Q4157020 Magnus Julius Axelsson De la Gardie till Tullgarn: P735 given name = Q1102114 Julius, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q4157020	P735	Q1102114	P1545	"2"	P3831	Q245025
#   Q99202609 Wilhelm von Ascheberg: P735 given name = Q11027623, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q99202609	P735	Q11027623	P1545	"1"	P7452	Q3409033
#   Q100995353 Gustaf Magnus Oskar Rogér Björnstjerna: P735 given name = Q15646212 Gustaf, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q100995353	P735	Q15646212	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18109457 Magnus, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q100995353	P735	Q18109457	P1545	"2"	P3831	Q245025
#   P735 given name = Q18145769 Oskar, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q100995353	P735	Q18145769	P1545	"3"	P3831	Q245025
#   Q75500962 Edward Bruce: P735 given name = Q278835 Edward
Q75500962	P735	Q278835
#   P734 family name = Q16860571 Bruce
Q75500962	P734	Q16860571
#   Q5759363 Jacob Gillberg: P735 given name = Q25999604 Jacob
Q5759363	P735	Q25999604
#   Q2478781 Adolf Fredrik Munck: P735 given name = Q4926491 Fredrik, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q2478781	P735	Q4926491	P1545	"2"	P3831	Q245025
#   Q5783620 Laurentius Jonæ Hallenius: P734 family name = Q47035866
Q5783620	P734	Q47035866
#   Q1324672 Eleonore von Fürstenberg: P735 given name = Q17190292, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q1324672	P735	Q17190292	P1545	"1"	P7452	Q3409033
#   P734 family name = Q51079363 Fürstenberg
Q1324672	P734	Q51079363
#   Q110378177 Adelheid von Plain: P735 given name = Q4057477 Adelheid, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110378177	P735	Q4057477	P1545	"1"	P7452	Q3409033
#   Q109835501 Hedvig Katarina Johansdotter Bartels: P735 given name = Q13648620 Hedvig, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q109835501	P735	Q13648620	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16277703 Katarina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q109835501	P735	Q16277703	P1545	"2"	P3831	Q245025
#   Q116007123 Costanza di Niccolò Cavalcanti: P735 given name = Q19816831 Costanza, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q116007123	P735	Q19816831	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1984713 Niccolò, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q116007123	P735	Q1984713	P1545	"3"	P3831	Q245025
#   P734 family name = Q21450357 Cavalcanti
Q116007123	P734	Q21450357
#   Q103771971 Anna Maria Törnstjerna, Törne: P735 given name = Q325872 Maria, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q103771971	P735	Q325872	P1545	"2"	P3831	Q245025
#   P734 family name = Q65202241 Törne
Q103771971	P734	Q65202241
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
#   Q900478 Vilhelm Hisinger: P735 given name = Q12805716 Vilhelm
Q900478	P735	Q12805716
#   Q95972040 William Sinclair: P735 given name = Q12344159 William
Q95972040	P735	Q12344159
#   P734 family name = Q16883357 Sinclair
Q95972040	P734	Q16883357
#   Q2471654 Eva Aurora Charlotta Karamzin: P735 given name = Q64412279 Eva, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q2471654	P735	Q64412279	P1545	"1"	P7452	Q3409033
#   Q139997218 Albrecht Jonsson Behm: P22 father = Q25451348 Jon Mickelsson Behm
Q139997218	P22	Q25451348	S2600	"6000000004577963540"
#   P40 child = Q140192133 Sara Albrektsdotter Swedberg
Q139997218	P40	Q140192133	S2600	"6000000004577963540"
#   P2600 Geni.com profile ID = 6000000004577963540 Albrecht Jonsson Behm, qualified P1810 subject named as Albrecht Jonsson Behm
Q139997218	P2600	"6000000004577963540"	P1810	"Albrecht Jonsson Behm"
#   P735 given name = Q18180401 Albrecht
Q139997218	P735	Q18180401
#   Q6003542 Henrik Johan Nauckhoff: P735 given name = Q10989273 Johan, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q6003542	P735	Q10989273	P1545	"2"	P3831	Q245025
#   Q75319653 Francis Charles Cadogan: P735 given name = Q1441346 Francis, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q75319653	P735	Q1441346	P1545	"1"	P7452	Q3409033
#   P735 given name = Q2958359 Charles, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q75319653	P735	Q2958359	P1545	"2"	P3831	Q245025
#   P734 family name = Q16865288 Cadogan
Q75319653	P734	Q16865288
#   Q141257266 Mattias Tollefsen Vatnamot: P26 spouse = Q141257173 Elen Pedersdatter Vatnamot
Q141257266	P26	Q141257173	S2600	"6000000005607089279"
#   Q141257173 Elen Pedersdatter Vatnamot: P26 spouse = Q141257266 Mattias Tollefsen Vatnamot
Q141257173	P26	Q141257266	S2600	"6000000005607089288"
#   Q5914181 Otto Reinhold Klingspor: P735 given name = Q18091397 Reinhold, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5914181	P735	Q18091397	P1545	"2"	P3831	Q245025
#   Q130564935 Christoph Ernst von Platen: P735 given name = Q17689481 Christoph, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q130564935	P735	Q17689481	P1545	"1"	P7452	Q3409033
#   P735 given name = Q292691 Ernst, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q130564935	P735	Q292691	P1545	"2"	P3831	Q245025
#   Q103772007 Anna Sofia Gyllenhaal: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q103772007	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q103772007	P735	Q18201520	P1545	"2"	P3831	Q245025
#   Q6184934 Erik Samuel Sparre af Söfdeborg: P735 given name = Q750186 Erik, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q6184934	P735	Q750186	P1545	"1"	P7452	Q3409033
#   Q130755124 Johan Gustav Boije af Gennäs: P735 given name = Q746076, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q130755124	P735	Q746076	P1545	"2"	P3831	Q245025
#   P734 family name = Q141223490
Q130755124	P734	Q141223490
#   Q5898100 Peter Petersson Kalling till Myrö: P735 given name = Q2793400 Peter, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q5898100	P735	Q2793400	P1545	"1"	P7452	Q3409033
#   Q16649829 Fredrik Adolf Löwenhielm: P735 given name = Q4926491 Fredrik, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q16649829	P735	Q4926491	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18145837 Adolf, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q16649829	P735	Q18145837	P1545	"2"	P3831	Q245025
#   Q110303165 Sofia Elisabeth Augusta von Buchwaldt: P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110303165	P735	Q18201520	P1545	"1"	P7452	Q3409033
#   P735 given name = Q63611044 Elisabeth, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110303165	P735	Q63611044	P1545	"2"	P3831	Q245025
#   P735 given name = Q1370330 Augusta, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q110303165	P735	Q1370330	P1545	"3"	P3831	Q245025
#   Q2075113 Hedvig Ulrika Armfelt: P735 given name = Q18924998 Ulrika, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q2075113	P735	Q18924998	P1545	"2"	P3831	Q245025
#   Q110304545 Charlotta Lovisa Gyllenkrok: P25 mother = Q2965864 Christina Charlotta Cederström
Q110304545	P25	Q2965864	S2600	"6000000006127529405"
#   P2600 Geni.com profile ID = 6000000006127529405 Charlotta Lovisa Gyllenkrok, qualified P1810 subject named as Charlotta Lovisa Gyllenkrok
Q110304545	P2600	"6000000006127529405"	P1810	"Charlotta Lovisa Gyllenkrok"
#   P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110304545	P735	Q1067071	P1545	"1"	P7452	Q3409033
#   P735 given name = Q10570000 Lovisa, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110304545	P735	Q10570000	P1545	"2"	P3831	Q245025
#   Q109296452 Jacquette Elizabeth Eleonora Piper: P735 given name = Q60691640 Jacquette, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q109296452	P735	Q60691640	P1545	"1"	P7452	Q3409033
#   P735 given name = Q385468 Elizabeth, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q109296452	P735	Q385468	P1545	"2"	P3831	Q245025
#   P735 given name = Q18759077 Eleonora, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q109296452	P735	Q18759077	P1545	"3"	P3831	Q245025
#   Q6215643 Nils Axel Arvid Carlsson Trolle: P735 given name = Q16423038 Nils, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q6215643	P735	Q16423038	P1545	"1"	P7452	Q3409033
#   P735 given name = Q5407300 Axel, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q6215643	P735	Q5407300	P1545	"2"	P3831	Q245025
#   P735 given name = Q717011 Arvid, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q6215643	P735	Q717011	P1545	"3"	P3831	Q245025
#   P734 family name = Q42748130 Trolle
Q6215643	P734	Q42748130
#   Q76250299 Vendela Sofia von Wright: P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q76250299	P735	Q18201520	P1545	"2"	P3831	Q245025
#   P734 family name = Q2594455 Wright
Q76250299	P734	Q2594455
#   Q130684265 Carl Philip Strömfelt: P735 given name = Q827311 Philip, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q130684265	P735	Q827311	P1545	"2"	P3831	Q245025
#   Q5813639 Claes Fredrik Claesson Horn af Åminne: P735 given name = Q4926491 Fredrik, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5813639	P735	Q4926491	P1545	"2"	P3831	Q245025
#   Q110548033 Marie Emilie Reuterskiöld: P735 given name = Q106674406 Marie, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110548033	P735	Q106674406	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16275679 Emilie, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110548033	P735	Q16275679	P1545	"2"	P3831	Q245025
#   Q109829800 Eva Helena Adelswärd: P735 given name = Q64412279 Eva, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q109829800	P735	Q64412279	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1035239 Helena, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q109829800	P735	Q1035239	P1545	"2"	P3831	Q245025
#   Q97821557 Anna Catharina Åkerhielm af Margretelund: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q97821557	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P735 given name = Q17317997 Catharina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q97821557	P735	Q17317997	P1545	"2"	P3831	Q245025
#   Q5628451 Albert Carl August Lars Ehrensvärd: P735 given name = Q577011 Albert, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q5628451	P735	Q577011	P1545	"1"	P7452	Q3409033
#   P735 given name = Q2529610 Carl, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5628451	P735	Q2529610	P1545	"2"	P3831	Q245025
#   P735 given name = Q370731 August, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q5628451	P735	Q370731	P1545	"3"	P3831	Q245025
#   P735 given name = Q15635262 Lars, qualified P1545 series ordinal 4, P3831 object of statement has role Q245025 middle name
Q5628451	P735	Q15635262	P1545	"4"	P3831	Q245025
#   Q5951786 Johan Gustafsson Liljencrantz: P735 given name = Q10989273 Johan
Q5951786	P735	Q10989273
#   Q805827 Baltzar Carl von Platen: P735 given name = Q2529610 Carl, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q805827	P735	Q2529610	P1545	"2"	P3831	Q245025
#   Q110395728 Eugenia Karolina Desideria von Essen: P22 father = Q657814 Hans Henrik von Essen
Q110395728	P22	Q657814	S2600	"6000000006127907643"
#   P25 mother = Q110395711 Charlotta Eleonora Hedvig von Krassow
Q110395728	P25	Q110395711	S2600	"6000000006127907643"
#   P2600 Geni.com profile ID = 6000000006127907643 Eugenia Karolina Desideria von Essen, qualified P1810 subject named as Eugenia Karolina Desideria von Essen
Q110395728	P2600	"6000000006127907643"	P1810	"Eugenia Karolina Desideria von Essen"
#   P735 given name = Q962602 Eugenia, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110395728	P735	Q962602	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1734206 Karolina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110395728	P735	Q1734206	P1545	"2"	P3831	Q245025
#   P735 given name = Q682121 Desideria, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q110395728	P735	Q682121	P1545	"3"	P3831	Q245025
#   Q5580703 Carl Julius Bernhard von Bohlen: P735 given name = Q1102114 Julius, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5580703	P735	Q1102114	P1545	"2"	P3831	Q245025
#   P735 given name = Q221978 Bernhard, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q5580703	P735	Q221978	P1545	"3"	P3831	Q245025
#   Q5802535 Mattias von Hermansson: P735 given name = Q16279186 Mattias, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q5802535	P735	Q16279186	P1545	"1"	P7452	Q3409033
#   Q5950139 Anders Liedbeck: P735 given name = Q8843357 Anders
Q5950139	P735	Q8843357
#   Q6215610 Erik Birger Trolle: P735 given name = Q750186 Erik, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q6215610	P735	Q750186	P1545	"1"	P7452	Q3409033
#   Q133861600 Catharina Elisabet Lamoni: P735 given name = Q17317997 Catharina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q133861600	P735	Q17317997	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16423275 Elisabet, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q133861600	P735	Q16423275	P1545	"2"	P3831	Q245025
#   Q110548098 Anna Christina Hanssen: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110548098	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1083457 Christina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110548098	P735	Q1083457	P1545	"2"	P3831	Q245025
#   Q99202612 Maria Eleonora von Busseck: P735 given name = Q325872 Maria, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q99202612	P735	Q325872	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18759077 Eleonora, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q99202612	P735	Q18759077	P1545	"2"	P3831	Q245025
#   Q364270 Carl Gustaf Patrik de Laval: P735 given name = Q2529610 Carl, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q364270	P735	Q2529610	P1545	"1"	P7452	Q3409033
#   P734 family name = Q23072571 Laval
Q364270	P734	Q23072571
#   Q141250247 Sara Carlberg: P26 spouse = Q141250225 Conrad von Braunjohan
Q141250247	P26	Q141250225	S2600	"6000000006435949669"
#   Q141250225 Conrad von Braunjohan: P26 spouse = Q141250247 Sara Carlberg
Q141250225	P26	Q141250247	S2600	"6000000006436219130"
#   Q5884303 Johan Casparson Poppelman: P735 given name = Q10989273 Johan
Q5884303	P735	Q10989273
#   Q1340404 Eric Benzelius d.y.: P735 given name = Q12788459 Eric, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q1340404	P735	Q12788459	P1545	"1"	P7452	Q3409033
#   Q1393227 Eva De la Gardie: P735 given name = Q64412279 Eva, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q1393227	P735	Q64412279	P1545	"1"	P7452	Q3409033
#   Q5568857 Daniel Jonsson Behmer: P735 given name = Q53787734 Daniel
Q5568857	P735	Q53787734
#   Q130335459 Karin Sofia af Buren: P735 given name = Q1814118 Karin, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q130335459	P735	Q1814118	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q130335459	P735	Q18201520	P1545	"2"	P3831	Q245025
#   Q2040261 Otto Reinhold Strömfelt: P735 given name = Q18091397 Reinhold, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q2040261	P735	Q18091397	P1545	"2"	P3831	Q245025
#   Q105900312 Philippus Bononius (Bondesson): P735 given name = Q19970429 Philippus, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q105900312	P735	Q19970429	P1545	"1"	P7452	Q3409033
#   Q5562579 Magnus Petri Aurivillius: P735 given name = Q10625184 Petri, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5562579	P735	Q10625184	P1545	"2"	P3831	Q245025
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
#   Q692994 Henrik Benzelius: P735 given name = Q594279 Henrik
Q692994	P735	Q594279
#   Q5769269 Hans Sebastian Grave: P735 given name = Q632842, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q5769269	P735	Q632842	P1545	"1"	P7452	Q3409033
#   P735 given name = Q4844560 Sebastian, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5769269	P735	Q4844560	P1545	"2"	P3831	Q245025
#   Q19678400 Eva Horn af Ekebyholm: P735 given name = Q64412279 Eva, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q19678400	P735	Q64412279	P1545	"1"	P7452	Q3409033
#   Q5542574 Johan Fredrik Adelheim Borgström: P735 given name = Q4926491 Fredrik, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5542574	P735	Q4926491	P1545	"2"	P3831	Q245025
#   Q109480152 Johan Wulfsson Polhammar: P735 given name = Q10989273 Johan
Q109480152	P735	Q10989273
#   Q109663400 Sofia Katarina Nordlind: P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q109663400	P735	Q18201520	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16277703 Katarina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q109663400	P735	Q16277703	P1545	"2"	P3831	Q245025
#   Q5040378 Carl Jesper Benzelius: P735 given name = Q1158511 Jesper, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5040378	P735	Q1158511	P1545	"2"	P3831	Q245025
#   Q64691009 Nikolaus Wilhelm Heinrich* Berendts: P735 given name = Q15728996 Nikolaus, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q64691009	P735	Q15728996	P1545	"1"	P7452	Q3409033
#   P735 given name = Q11027623, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q64691009	P735	Q11027623	P1545	"2"	P3831	Q245025
#   Q25451348 Jon Mickelsson Behm: P735 given name = Q13501137 Jon
Q25451348	P735	Q13501137
#   Q15069149 Eduard* Albert Christopher Ludwig Collins: P735 given name = Q577011 Albert, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q15069149	P735	Q577011	P1545	"2"	P3831	Q245025
#   P735 given name = Q1084472 Christopher, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q15069149	P735	Q1084472	P1545	"3"	P3831	Q245025
#   P735 given name = Q14159020 Ludwig, qualified P1545 series ordinal 4, P3831 object of statement has role Q245025 middle name
Q15069149	P735	Q14159020	P1545	"4"	P3831	Q245025
#   P734 family name = Q1791084 Collins
Q15069149	P734	Q1791084
#   Q103773586 Anna Sinclair: P735 given name = Q666578 Anna
Q103773586	P735	Q666578
#   P734 family name = Q16883357 Sinclair
Q103773586	P734	Q16883357
#   Q6170263 Fredrik Bogislaus von Schwerin: P734 family name = Q37225673 Schwerin
Q6170263	P734	Q37225673
#   Q10418965 Arvid Sigismund Horn af Åminne: P735 given name = Q10667549 Sigismund, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q10418965	P735	Q10667549	P1545	"2"	P3831	Q245025
#   Q109852820 Gustav Adolf Järnefelt: P735 given name = Q746076, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q109852820	P735	Q746076	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18145837 Adolf, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q109852820	P735	Q18145837	P1545	"2"	P3831	Q245025
#   Q6206425 Per Reinhold Tersmeden: P735 given name = Q18091397 Reinhold, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q6206425	P735	Q18091397	P1545	"2"	P3831	Q245025
#   Q5754056 Peter Niklas von Gedda: P735 given name = Q2793400 Peter, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q5754056	P735	Q2793400	P1545	"1"	P7452	Q3409033
#   Q5630706 Peter Ekman II: P735 given name = Q2793400 Peter, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q5630706	P735	Q2793400	P1545	"1"	P7452	Q3409033
#   Q109296034 Jacquelina Elisabet De Geer af Leufsta: P735 given name = Q16423275 Elisabet, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q109296034	P735	Q16423275	P1545	"2"	P3831	Q245025
#   Q98545742 Friherrinnan Sofia Ulrika Carolina Stedt: P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q98545742	P735	Q18201520	P1545	"2"	P3831	Q245025
#   P735 given name = Q18924998 Ulrika, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q98545742	P735	Q18924998	P1545	"3"	P3831	Q245025
#   P735 given name = Q5044762 Carolina, qualified P1545 series ordinal 4, P3831 object of statement has role Q245025 middle name
Q98545742	P735	Q5044762	P1545	"4"	P3831	Q245025
#   Q6175942 David Wilhelm Silfverstolpe: P735 given name = Q29937870 David, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q6175942	P735	Q29937870	P1545	"1"	P7452	Q3409033
#   P735 given name = Q11027623, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q6175942	P735	Q11027623	P1545	"2"	P3831	Q245025
#   Q5960165 Carolus Nicolai Lithman: P735 given name = Q1044619 Carolus, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q5960165	P735	Q1044619	P1545	"1"	P7452	Q3409033
#   P735 given name = Q19830590 Nicolai, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5960165	P735	Q19830590	P1545	"2"	P3831	Q245025
#   Q5931284 Olof Elias Lagerheim: P735 given name = Q18089653 Olof, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q5931284	P735	Q18089653	P1545	"1"	P7452	Q3409033
#   P735 given name = Q11878157 Elias, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5931284	P735	Q11878157	P1545	"2"	P3831	Q245025
#   Q16649517 Gerhard Jonæ: P735 given name = Q7996169 Gerhard
Q16649517	P735	Q7996169
#   Q5757435 Martinus Erici Gestrinius: P735 given name = Q110012183, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5757435	P735	Q110012183	P1545	"2"	P3831	Q245025
#   Q6177449 Johan Carlsson Siöblad: P735 given name = Q10989273 Johan
Q6177449	P735	Q10989273
#   Q12363134 Gustaf Adolf Strömfelt till Strömhult: P735 given name = Q15646212 Gustaf, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q12363134	P735	Q15646212	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18145837 Adolf, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q12363134	P735	Q18145837	P1545	"2"	P3831	Q245025
#   Q133283834 Nils Gabriel Danckwardt-Lillieström till Gälsebo: P735 given name = Q16423038 Nils, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q133283834	P735	Q16423038	P1545	"1"	P7452	Q3409033
#   P735 given name = Q4925914 Gabriel, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q133283834	P735	Q4925914	P1545	"2"	P3831	Q245025
#   Q102121588 Catharina Elisabet Daurer: P735 given name = Q17317997 Catharina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q102121588	P735	Q17317997	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16423275 Elisabet, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q102121588	P735	Q16423275	P1545	"2"	P3831	Q245025
#   Q5626148 Carl Wilhelm von Düben: P735 given name = Q11027623, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5626148	P735	Q11027623	P1545	"2"	P3831	Q245025
#   Q4944366 Charlotta Aurora De Geer af Finspång: P735 given name = Q1066178 Aurora, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q4944366	P735	Q1066178	P1545	"2"	P3831	Q245025
#   Q110548896 Ebba Lidman: P22 father = Q5950427 Sven Fredrik Lidman
Q110548896	P22	Q5950427	S2600	"6000000007753308375"
#   P2600 Geni.com profile ID = 6000000007753308375 Ebba Lidman, qualified P1810 subject named as Ebba Lidman
Q110548896	P2600	"6000000007753308375"	P1810	"Ebba Lidman"
#   P735 given name = Q2242896 Ebba
Q110548896	P735	Q2242896
#   Q135665878 Anna Christina Stålhammar: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q135665878	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1083457 Christina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q135665878	P735	Q1083457	P1545	"2"	P3831	Q245025
#   Q141224012 Hedvig Chydenius: P40 child = Q109852817 Jakob Chydenius
Q141224012	P40	Q109852817	S2600	"6000000007774748338"
#   Q19977201 Jakob Pedersson Törnsköld till Runstorp: P5056 patronym or matronym = Q130232998
Q19977201	P5056	Q130232998
#   Q6218068 Carl Peter Peter Törnebladh: P735 given name = Q2793400 Peter, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q6218068	P735	Q2793400	P1545	"2"	P3831	Q245025
#   P735 given name = Q2793400 Peter, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q6218068	P735	Q2793400	P1545	"3"	P3831	Q245025
#   Q110457041 Anna Sofia Stålhammar: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110457041	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110457041	P735	Q18201520	P1545	"2"	P3831	Q245025
#   Q4355686 August Gustaf Nordenskjöld: P735 given name = Q15646212 Gustaf, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q4355686	P735	Q15646212	P1545	"2"	P3831	Q245025
#   Q141257299 Rasmus Lydikson Amdal: P40 child = Q141257264 Lydik Rasmussen Amdal
Q141257299	P40	Q141257264	S2600	"6000000007980728992"
#   Q126217078 Elsa Christina Ehrenkrona: P735 given name = Q1077181 Elsa, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q126217078	P735	Q1077181	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1083457 Christina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q126217078	P735	Q1083457	P1545	"2"	P3831	Q245025
#   Q73763454 Sigfrid Porthan: P735 given name = Q329006 Sigfrid
Q73763454	P735	Q329006
#   Q5935475 Albrecht von Lantinghausen: P735 given name = Q18180401 Albrecht, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q5935475	P735	Q18180401	P1545	"1"	P7452	Q3409033
#   Q76254086 William Marsh: P735 given name = Q12344159 William
Q76254086	P735	Q12344159
#   P734 family name = Q16876476 Marsh
Q76254086	P734	Q16876476
#   Q565581 Anne Marsh-Caldwell: P735 given name = Q564684 Anne
Q565581	P735	Q564684
#   Q5823030 Carl Gustaf Indebetou: P735 given name = Q2529610 Carl, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q5823030	P735	Q2529610	P1545	"1"	P7452	Q3409033
#   P735 given name = Q15646212 Gustaf, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5823030	P735	Q15646212	P1545	"2"	P3831	Q245025
#   Q5754581 Bengt Reinhold Geijer: P735 given name = Q18091397 Reinhold, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5754581	P735	Q18091397	P1545	"2"	P3831	Q245025
#   Q16649477 Nicolaus Jacobi Bothniensis: P735 given name = Q30510238 Jacobi, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q16649477	P735	Q30510238	P1545	"2"	P3831	Q245025
#   Q362485 Sten Carl Turesson Bielke: P735 given name = Q2529610 Carl, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q362485	P735	Q2529610	P1545	"2"	P3831	Q245025
#   P5056 patronym or matronym = Q130232969 Turesson, qualified P144 based on Q5597349 Thure Stensson Bielke
Q362485	P5056	Q130232969	P144	Q5597349
#   Q134546510 Catharina Elisabet Brandt: P22 father = Q473225 Georg Brandt
Q134546510	P22	Q473225	S2600	"6000000008496890939"
#   P25 mother = Q141250213 Anna Maria Norn
Q134546510	P25	Q141250213	S2600	"6000000008496890939"
#   P2600 Geni.com profile ID = 6000000008496890939 Catharina Elisabet Brandt, qualified P1810 subject named as Catharina Elisabet Brandt
Q134546510	P2600	"6000000008496890939"	P1810	"Catharina Elisabet Brandt"
#   P735 given name = Q17317997 Catharina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q134546510	P735	Q17317997	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16423275 Elisabet, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q134546510	P735	Q16423275	P1545	"2"	P3831	Q245025
#   P734 family name = Q11941314 Brandt
Q134546510	P734	Q11941314
#   Q131726981 Renata Elisabet Blum: P735 given name = Q16423275 Elisabet, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q131726981	P735	Q16423275	P1545	"2"	P3831	Q245025
#   P734 family name = Q886147 Blum
Q131726981	P734	Q886147
#   Q127270460 Margareta Tilas: P735 given name = Q8274988 Margareta
Q127270460	P735	Q8274988
#   Q16650516 Mikael von Törne: P734 family name = Q65202241 Törne
Q16650516	P734	Q65202241
#   Q16650517 Mikael von Törne: P734 family name = Q65202241 Törne
Q16650517	P734	Q65202241
#   Q4973002 Christina Charlotta Piper: P735 given name = Q1083457 Christina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q4973002	P735	Q1083457	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q4973002	P735	Q1067071	P1545	"2"	P3831	Q245025
#   Q6185927 Jakob Vilhelm Wilhelm Sprengtporten: P735 given name = Q12805716 Vilhelm, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q6185927	P735	Q12805716	P1545	"2"	P3831	Q245025
#   Q109835490 Catharina Eleonora Temminck: P735 given name = Q18759077 Eleonora, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q109835490	P735	Q18759077	P1545	"2"	P3831	Q245025
#   Q109294802 Mattias Arkimboldus Skjöldebrand: P735 given name = Q16279186 Mattias, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q109294802	P735	Q16279186	P1545	"1"	P7452	Q3409033
#   Q5913812 Axel Leonhard Leonard Klinckowström: P735 given name = Q948418 Leonard, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q5913812	P735	Q948418	P1545	"3"	P3831	Q245025
#   Q5706932 Claes Julius Ekeblad: P735 given name = Q1102114 Julius, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5706932	P735	Q1102114	P1545	"2"	P3831	Q245025
#   Q137213784 Carl Arvid Svensson Hallenborg: P735 given name = Q2529610 Carl, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q137213784	P735	Q2529610	P1545	"1"	P7452	Q3409033
#   P735 given name = Q717011 Arvid, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q137213784	P735	Q717011	P1545	"2"	P3831	Q245025
#   Q109835397 Carl Gustaf Lagerfelt: P735 given name = Q15646212 Gustaf, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q109835397	P735	Q15646212	P1545	"2"	P3831	Q245025
#   Q5855920 Odert Reinhold von Essen d.y.: P735 given name = Q18091397 Reinhold, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5855920	P735	Q18091397	P1545	"2"	P3831	Q245025
#   Q5931099 Israel Lagerfelt: P735 given name = Q1399596 Izrail
Q5931099	P735	Q1399596
#   Q19976679 Otto Johan Lagerfelt: P735 given name = Q10989273 Johan, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q19976679	P735	Q10989273	P1545	"2"	P3831	Q245025
#   Q5931081 Gustaf Adolf Lagerfelt: P735 given name = Q18145837 Adolf, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5931081	P735	Q18145837	P1545	"2"	P3831	Q245025
#   Q1648141 Adolf Ludvig Ribbing: P735 given name = Q18145837 Adolf, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q1648141	P735	Q18145837	P1545	"1"	P7452	Q3409033
#   P735 given name = Q12233911 Ludvig, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q1648141	P735	Q12233911	P1545	"2"	P3831	Q245025
#   Q134895550 Maria Hoffman: P735 given name = Q325872 Maria
Q134895550	P735	Q325872
#   Q26239902 Abraham Falkengréen: P735 given name = Q4055996 Abraham
Q26239902	P735	Q4055996
#   Q90238048 Erik Reinhold von Nolcken: P735 given name = Q750186 Erik, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q90238048	P735	Q750186	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18091397 Reinhold, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q90238048	P735	Q18091397	P1545	"2"	P3831	Q245025
#   Q546949 Sofia Magdalena Silfverstolpe: P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q546949	P735	Q18201520	P1545	"1"	P7452	Q3409033
#   P735 given name = Q842544 Magdalena, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q546949	P735	Q842544	P1545	"2"	P3831	Q245025
#   Q108937197 Catharina Charlotta Rudbeck: P735 given name = Q17317997 Catharina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q108937197	P735	Q17317997	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q108937197	P735	Q1067071	P1545	"2"	P3831	Q245025
#   Q110304544 Sophie Magdalena Magdalena von Essen: P735 given name = Q14942517 Sophie, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110304544	P735	Q14942517	P1545	"1"	P7452	Q3409033
#   P735 given name = Q842544 Magdalena, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110304544	P735	Q842544	P1545	"2"	P3831	Q245025
#   P735 given name = Q842544 Magdalena, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q110304544	P735	Q842544	P1545	"3"	P3831	Q245025
#   Q6240337 Per Henrik Widmark RVO: P735 given name = Q13582800 Per, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q6240337	P735	Q13582800	P1545	"1"	P7452	Q3409033
#   Q110548812 Maria Stiernblad: P735 given name = Q325872 Maria
Q110548812	P735	Q325872
#   P735 given name = Q12788459 Eric, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q5542632	P735	Q12788459	P1545	"1"	P7452	Q3409033
#   Q104549962 Katarina Gerdtsdotter von Glaen: P735 given name = Q16277703 Katarina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q104549962	P735	Q16277703	P1545	"1"	P7452	Q3409033
#   Q930758 Carl Aurivillius von Rosenstein: P734 family name = Q21488358 Rosenstein
Q930758	P734	Q21488358
#   Q134761202 Anders Andersson Mennander: P735 given name = Q8843357 Anders
Q134761202	P735	Q8843357
#   Q6228008 Hans Wachtmeister af Johannishus: P735 given name = Q632842, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q6228008	P735	Q632842	P1545	"1"	P7452	Q3409033
#   Q6080164 Nils Rosén von Rosenstein: P734 family name = Q21488358 Rosenstein
Q6080164	P734	Q21488358
#   Q95243484 Jürgen Johann Johann von Maydell: P735 given name = Q11122389 Johann, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q95243484	P735	Q11122389	P1545	"2"	P3831	Q245025
#   P735 given name = Q11122389 Johann, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q95243484	P735	Q11122389	P1545	"3"	P3831	Q245025
#   Q85986394 Henrik Thomas Adlercreutz: P735 given name = Q594279 Henrik, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q85986394	P735	Q594279	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16428906, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q85986394	P735	Q16428906	P1545	"2"	P3831	Q245025
#   Q329253 Ivar Henning Mankell: P735 given name = Q127069 Ivar, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q329253	P735	Q127069	P1545	"1"	P7452	Q3409033
#   Q110386180 Elisabet Ramsvärd: P735 given name = Q16423275 Elisabet
Q110386180	P735	Q16423275
#   Q110457058 Johanna Christina Tham: P735 given name = Q4120836 Johanna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110457058	P735	Q4120836	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1083457 Christina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110457058	P735	Q1083457	P1545	"2"	P3831	Q245025
#   Q127270620 Johan Olofsson: P735 given name = Q10989273 Johan
Q127270620	P735	Q10989273
#   Q5823775 Ernst Ivar Insulander: P735 given name = Q292691 Ernst, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q5823775	P735	Q292691	P1545	"1"	P7452	Q3409033
#   P735 given name = Q127069 Ivar, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5823775	P735	Q127069	P1545	"2"	P3831	Q245025
#   Q131740913 Hedvig Sofia Hamilton: P735 given name = Q13648620 Hedvig, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q131740913	P735	Q13648620	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q131740913	P735	Q18201520	P1545	"2"	P3831	Q245025
#   Q821990 Christopher Jacob Boström: P735 given name = Q25999604 Jacob, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q821990	P735	Q25999604	P1545	"2"	P3831	Q245025
#   Q5916852 Lorentz Kockum: P735 given name = Q21061236 Lorentz
Q5916852	P735	Q21061236
#   Q98180381 Kristina Elisabeth Nordenadler: P735 given name = Q19798802 Kristina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q98180381	P735	Q19798802	P1545	"1"	P7452	Q3409033
#   P735 given name = Q63611044 Elisabeth, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q98180381	P735	Q63611044	P1545	"2"	P3831	Q245025
#   Q5997341 Sven Johan Munthe: P735 given name = Q2370957 Sven, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q5997341	P735	Q2370957	P1545	"1"	P7452	Q3409033
#   P735 given name = Q10989273 Johan, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5997341	P735	Q10989273	P1545	"2"	P3831	Q245025
#   Q141250214 Anna Nilsdotter: P26 spouse = Q141250215 Benjamin Mårtensson
Q141250214	P26	Q141250215	S2600	"6000000011078617825"
#   Q141250215 Benjamin Mårtensson: P26 spouse = Q141250214 Anna Nilsdotter
Q141250215	P26	Q141250214	S2600	"6000000011078886609"
#   Q2424918 Tomas Ihre: P735 given name = Q1546318 Tomas
Q2424918	P735	Q1546318
#   Q4989142 Eva Helena Löwen: P735 given name = Q64412279 Eva, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q4989142	P735	Q64412279	P1545	"1"	P7452	Q3409033
#   Q75418653 Nanfan Coote 2nd Earl of Bellomont: P735 given name = Q8933847 Earl, qualified P1545 series ordinal 4, P3831 object of statement has role Q245025 middle name
Q75418653	P735	Q8933847	P1545	"4"	P3831	Q245025
#   Q5616509 Jacob Danckwardt-Lillieström: P735 given name = Q25999604 Jacob
Q5616509	P735	Q25999604
#   Q109296145 Charlotta Florentina Beata Ingelotz: P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q109296145	P735	Q1067071	P1545	"1"	P7452	Q3409033
#   P735 given name = Q610489 Florentina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q109296145	P735	Q610489	P1545	"2"	P3831	Q245025
#   P735 given name = Q338015 Beata, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q109296145	P735	Q338015	P1545	"3"	P3831	Q245025
#   Q110313429 Otto Wilhelm Ramsay: P735 given name = Q18029644 Otto, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110313429	P735	Q18029644	P1545	"1"	P7452	Q3409033
#   P735 given name = Q11027623, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110313429	P735	Q11027623	P1545	"2"	P3831	Q245025
#   Q73762532 Hans Henrik Wittfooth: P735 given name = Q594279 Henrik, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q73762532	P735	Q594279	P1545	"2"	P3831	Q245025
#   Q135934120 Margareta Clason: P735 given name = Q8274988 Margareta
Q135934120	P735	Q8274988
#   Q109835643 Maria Catharina Douglies: P735 given name = Q325872 Maria, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q109835643	P735	Q325872	P1545	"1"	P7452	Q3409033
#   P735 given name = Q17317997 Catharina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q109835643	P735	Q17317997	P1545	"2"	P3831	Q245025
#   Q106072786 Johanna Andriesdr Heijmans: P735 given name = Q4120836 Johanna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q106072786	P735	Q4120836	P1545	"1"	P7452	Q3409033
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
#   Q135855612 Kjell Henrik Barnekow: P735 given name = Q1785936 Kjell, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q135855612	P735	Q1785936	P1545	"1"	P7452	Q3409033
#   P735 given name = Q594279 Henrik, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q135855612	P735	Q594279	P1545	"2"	P3831	Q245025
#   P734 family name = Q557984 Barnekow
Q135855612	P734	Q557984
#   Q16596199 Hedvig Sofia Rosen: P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q16596199	P735	Q18201520	P1545	"2"	P3831	Q245025
#   Q333651 Henrik Gabriel Porthan: P735 given name = Q4925914 Gabriel, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q333651	P735	Q4925914	P1545	"2"	P3831	Q245025
#   Q5618800 Pontus Fredrik De la Gardie: P735 given name = Q4926491 Fredrik, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5618800	P735	Q4926491	P1545	"2"	P3831	Q245025
#   Q136536614 Ture Johansson Sandelin: P735 given name = Q2460609 Ture
Q136536614	P735	Q2460609
#   Q5723363 Anton Ludvig Ludwig Fahnehielm: P735 given name = Q5401576 Anton, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q5723363	P735	Q5401576	P1545	"1"	P7452	Q3409033
#   P735 given name = Q12233911 Ludvig, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5723363	P735	Q12233911	P1545	"2"	P3831	Q245025
#   P735 given name = Q14159020 Ludwig, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q5723363	P735	Q14159020	P1545	"3"	P3831	Q245025
#   Q101424903 Per Bring, adlad Lagerbring: P735 given name = Q13582800 Per, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q101424903	P735	Q13582800	P1545	"1"	P7452	Q3409033
#   Q6066017 Jakob Reenstierna: P735 given name = Q16747395
Q6066017	P735	Q16747395
#   Q134626249 Gustaf Enebom: P735 given name = Q15646212 Gustaf
Q134626249	P735	Q15646212
#   Q135479974 Carl Erik Benzelstierna: P735 given name = Q2529610 Carl, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q135479974	P735	Q2529610	P1545	"1"	P7452	Q3409033
#   P735 given name = Q750186 Erik, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q135479974	P735	Q750186	P1545	"2"	P3831	Q245025
#   Q133283826 Sebastian Tham: P735 given name = Q4844560 Sebastian
Q133283826	P735	Q4844560
#   Q109835504 Henrietta Amalia Stackelberg: P735 given name = Q783677 Henrietta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q109835504	P735	Q783677	P1545	"1"	P7452	Q3409033
#   P735 given name = Q453020 Amalia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q109835504	P735	Q453020	P1545	"2"	P3831	Q245025
#   Q657814 Hans Henrik von Essen: P735 given name = Q594279 Henrik, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q657814	P735	Q594279	P1545	"2"	P3831	Q245025
#   Q109954365 Johanna Maria Papke: P735 given name = Q4120836 Johanna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q109954365	P735	Q4120836	P1545	"1"	P7452	Q3409033
#   P735 given name = Q325872 Maria, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q109954365	P735	Q325872	P1545	"2"	P3831	Q245025
#   Q64828819 Johanna Gustava Axelina Åberg: P735 given name = Q4120836 Johanna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q64828819	P735	Q4120836	P1545	"1"	P7452	Q3409033
#   P735 given name = Q21144392 Gustava, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q64828819	P735	Q21144392	P1545	"2"	P3831	Q245025
#   P735 given name = Q10423722 Axelina, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q64828819	P735	Q10423722	P1545	"3"	P3831	Q245025
#   Q10480021 Edvard Fredrik von Saltza: P735 given name = Q278835 Edward, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q10480021	P735	Q278835	P1545	"1"	P7452	Q3409033
#   Q109835201 Lovisa Löf: P735 given name = Q10570000 Lovisa
Q109835201	P735	Q10570000
#   Q6079275 Gustaf Fredrik von Rosen: P735 given name = Q4926491 Fredrik, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q6079275	P735	Q4926491	P1545	"2"	P3831	Q245025
#   Q4945900 Helena Maria Ehrenstråhle: P735 given name = Q325872 Maria, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q4945900	P735	Q325872	P1545	"2"	P3831	Q245025
#   Q5959480 Jonas Carl Linnerhielm: P735 given name = Q2529610 Carl, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5959480	P735	Q2529610	P1545	"2"	P3831	Q245025
#   Q6206421 Lars Gustaf Tersmeden: P735 given name = Q15646212 Gustaf, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q6206421	P735	Q15646212	P1545	"2"	P3831	Q245025
#   Q6206408 Jacob Johan Tersmeden: P735 given name = Q10989273 Johan, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q6206408	P735	Q10989273	P1545	"2"	P3831	Q245025
#   Q5712230 Johan Mattias von Engeström: P735 given name = Q10989273 Johan, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q5712230	P735	Q10989273	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16279186 Mattias, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5712230	P735	Q16279186	P1545	"2"	P3831	Q245025
#   Q124606874 Hans Didrik Mörner af Morlanda: P734 family name = Q141223484
Q124606874	P734	Q141223484
#   Q110395628 Maria Lovisa Ulrika Ehrenpohl: P735 given name = Q325872 Maria, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110395628	P735	Q325872	P1545	"1"	P7452	Q3409033
#   P735 given name = Q10570000 Lovisa, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110395628	P735	Q10570000	P1545	"2"	P3831	Q245025
#   P735 given name = Q18924998 Ulrika, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q110395628	P735	Q18924998	P1545	"3"	P3831	Q245025
#   Q105499437 Anders Henriksson Frosterus: P735 given name = Q8843357 Anders
Q105499437	P735	Q8843357
#   Q108743048 Augusta Maria Sophia Rålamb: P735 given name = Q1370330 Augusta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q108743048	P735	Q1370330	P1545	"1"	P7452	Q3409033
#   P735 given name = Q325872 Maria, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q108743048	P735	Q325872	P1545	"2"	P3831	Q245025
#   P735 given name = Q2302787 Sophia, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q108743048	P735	Q2302787	P1545	"3"	P3831	Q245025
#   Q6255155 Gustaf Fredrik Åkerhielm af Margretelund: P735 given name = Q4926491 Fredrik, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q6255155	P735	Q4926491	P1545	"2"	P3831	Q245025
#   Q5951795 Johan Wilhelm Johansson Liljencrantz: P735 given name = Q11027623, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5951795	P735	Q11027623	P1545	"2"	P3831	Q245025
#   Q5779529 Nils Gyllenstierna af Björksund och Helgö: P735 given name = Q16423038 Nils, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q5779529	P735	Q16423038	P1545	"1"	P7452	Q3409033
#   Q110303080 Louis De Geer: P735 given name = Q97156058 Louis, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110303080	P735	Q97156058	P1545	"1"	P7452	Q3409033
#   P734 family name = Q28605695 Geer
Q110303080	P734	Q28605695
#   Q110303124 Helena Tott af Skedebo: P735 given name = Q1035239 Helena, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110303124	P735	Q1035239	P1545	"1"	P7452	Q3409033
#   Q64829391 Abraham Johansson Fought dä: P735 given name = Q4055996 Abraham, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q64829391	P735	Q4055996	P1545	"1"	P7452	Q3409033
#   Q110558398 Helena von der Schulenburg: P735 given name = Q1035239 Helena, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110558398	P735	Q1035239	P1545	"1"	P7452	Q3409033
#   Q110260857 August von der Schulenburg: P735 given name = Q370731 August, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110260857	P735	Q370731	P1545	"1"	P7452	Q3409033
#   Q16650430 Per Gustaf G. Svedelius: P735 given name = Q13582800 Per, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q16650430	P735	Q13582800	P1545	"1"	P7452	Q3409033
#   P735 given name = Q19803504 G., qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q16650430	P735	Q19803504	P1545	"3"	P3831	Q245025
#   Q75495232 William Forbes: P735 given name = Q12344159 William
Q75495232	P735	Q12344159
#   P734 family name = Q16275858 Forbes
Q75495232	P734	Q16275858
#   Q94775402 Katharina Helene von Hagemeister: P735 given name = Q16277712 Katharina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q94775402	P735	Q16277712	P1545	"1"	P7452	Q3409033
#   P735 given name = Q971710 Helene, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q94775402	P735	Q971710	P1545	"2"	P3831	Q245025
#   Q57677031 Nikolai Christoph von Hagemeister, Linie Drostenhof u. Gotthardsberg: P735 given name = Q30442370 Nikolai, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q57677031	P735	Q30442370	P1545	"1"	P7452	Q3409033
#   P735 given name = Q17689481 Christoph, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q57677031	P735	Q17689481	P1545	"2"	P3831	Q245025
#   Q75445669 Johan Jöransson: P735 given name = Q10989273 Johan
Q75445669	P735	Q10989273
#   Q6015541 Erik Harald Nordlander: P735 given name = Q750186 Erik, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q6015541	P735	Q750186	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1530266 Harald, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q6015541	P735	Q1530266	P1545	"2"	P3831	Q245025
#   Q4944381 Brita Sofia De la Gardie: P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q4944381	P735	Q18201520	P1545	"2"	P3831	Q245025
#   Q98545952 Augusta Charlotte Alice Trolle: P735 given name = Q264002 Charlotte, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q98545952	P735	Q264002	P1545	"2"	P3831	Q245025
#   Q16945159 Nils Abraham Bruncrona: P735 given name = Q4055996 Abraham, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q16945159	P735	Q4055996	P1545	"2"	P3831	Q245025
#   Q66711908 Anna Christina Bruncrona: P735 given name = Q1083457 Christina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q66711908	P735	Q1083457	P1545	"2"	P3831	Q245025
#   Q6247235 Otto Gustaf Wrede af Elimä: P735 given name = Q18029644 Otto, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q6247235	P735	Q18029644	P1545	"1"	P7452	Q3409033
#   P735 given name = Q15646212 Gustaf, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q6247235	P735	Q15646212	P1545	"2"	P3831	Q245025
#   Q111998458 Sara de Marez: P735 given name = Q833345 Sara, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q111998458	P735	Q833345	P1545	"1"	P7452	Q3409033
#   P735 given name = Q8274988 Margareta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q4953277	P735	Q8274988	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q4953277	P735	Q1067071	P1545	"2"	P3831	Q245025
#   Q108654979 Petronella Ottilia Schwencken von Friesen: P735 given name = Q16423664 Petronella, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q108654979	P735	Q16423664	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1423455 Ottilia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q108654979	P735	Q1423455	P1545	"2"	P3831	Q245025
#   Q5983613 Daniel Melanderhielm: P735 given name = Q53787734 Daniel
Q5983613	P735	Q53787734
#   Q10511031 Gustaf Adolf Fredrik Wilhelm von Essen: P735 given name = Q18145837 Adolf, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q10511031	P735	Q18145837	P1545	"2"	P3831	Q245025
#   P735 given name = Q4926491 Fredrik, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q10511031	P735	Q4926491	P1545	"3"	P3831	Q245025
#   P735 given name = Q11027623, qualified P1545 series ordinal 4, P3831 object of statement has role Q245025 middle name
Q10511031	P735	Q11027623	P1545	"4"	P3831	Q245025
#   Q16649961 Olof Olofsson Nauclérus: P735 given name = Q18089653 Olof
Q16649961	P735	Q18089653
#   Q5605565 Germund Ludvig Cederhielm: P735 given name = Q12233911 Ludvig, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5605565	P735	Q12233911	P1545	"2"	P3831	Q245025
#   Q106206114 Hans Gustaf Vilhelm Elias Lagerheim: P735 given name = Q632842, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q106206114	P735	Q632842	P1545	"1"	P7452	Q3409033
#   P735 given name = Q15646212 Gustaf, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q106206114	P735	Q15646212	P1545	"2"	P3831	Q245025
#   P735 given name = Q12805716 Vilhelm, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q106206114	P735	Q12805716	P1545	"3"	P3831	Q245025
#   P735 given name = Q11878157 Elias, qualified P1545 series ordinal 4, P3831 object of statement has role Q245025 middle name
Q106206114	P735	Q11878157	P1545	"4"	P3831	Q245025
#   Q5628179 Pehr Jacob von Ehrenheim: P735 given name = Q25999604 Jacob, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5628179	P735	Q25999604	P1545	"2"	P3831	Q245025
#   Q16650429 Per Svedelius: P735 given name = Q13582800 Per
Q16650429	P735	Q13582800
#   Q5779439 Erik Gyllenstierna af Lundholm: P735 given name = Q750186 Erik, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q5779439	P735	Q750186	P1545	"1"	P7452	Q3409033
#   Q6197780 Vilhelm Erik Svedelius: P735 given name = Q12805716 Vilhelm, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q6197780	P735	Q12805716	P1545	"1"	P7452	Q3409033
#   Q141250253 Ulrika Henrika von Köhler: P25 mother = Q141250230 Henrika Birgitta Wachtmeister af Johannishus
Q141250253	P25	Q141250230	S2600	"6000000019568439151"
#   Q490686 Anders Abraham Grafström: P735 given name = Q4055996 Abraham, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q490686	P735	Q4055996	P1545	"2"	P3831	Q245025
#   Q141250231 Jacob Baltzar von Hartmansdorff: P26 spouse = Q141250226 Fredrika Grönhagen
Q141250231	P26	Q141250226	S2600	"6000000019659479506"
#   Q141250226 Fredrika Grönhagen: P26 spouse = Q141250231 Jacob Baltzar von Hartmansdorff
Q141250226	P26	Q141250231	S2600	"6000000019659634521"
#   Q5792035 Jacob August von Hartmansdorff: P735 given name = Q25999604 Jacob, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q5792035	P735	Q25999604	P1545	"1"	P7452	Q3409033
#   Q5818420 Israel Hwasser: P735 given name = Q1399596 Izrail
Q5818420	P735	Q1399596
#   Q110221372 Berndt Ulrik von Knorring: P735 given name = Q5412982 Ulrik, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110221372	P735	Q5412982	P1545	"2"	P3831	Q245025
#   Q5916183 Karl Johan Andersson Knös: P735 given name = Q136771753 Karl, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q5916183	P735	Q136771753	P1545	"1"	P7452	Q3409033
#   Q5605651 Fredrik Johan Cederschiöld: P735 given name = Q10989273 Johan, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5605651	P735	Q10989273	P1545	"2"	P3831	Q245025
#   Q5745627 Berge / Birger Frondin: P735 given name = Q773057 Birger, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q5745627	P735	Q773057	P1545	"3"	P3831	Q245025
#   Q4988935 Brita Hedvig Wijnbladh: P735 given name = Q13648620 Hedvig, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q4988935	P735	Q13648620	P1545	"2"	P3831	Q245025
#   P734 family name = Q53848242 Wijnbladh
Q4988935	P734	Q53848242
#   Q5916162 Anders Olofsson Knös: P735 given name = Q8843357 Anders
Q5916162	P735	Q8843357
#   Q94775227 Katharina Auguste Stenbock: P735 given name = Q16277712 Katharina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q94775227	P735	Q16277712	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18010311 Auguste, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q94775227	P735	Q18010311	P1545	"2"	P3831	Q245025
#   Q5977879 Hugo Wilhelm Martin: P735 given name = Q11027623, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5977879	P735	Q11027623	P1545	"2"	P3831	Q245025
#   Q110310488 Gustaf Fock Gyllencartau: P735 given name = Q15646212 Gustaf, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110310488	P735	Q15646212	P1545	"1"	P7452	Q3409033
#   Q768049 Augustin Rhaw: P735 given name = Q18398186 Augustin
Q768049	P735	Q18398186
#   Q130570562 Aurora Charlotta Skjöldebrand: P735 given name = Q1066178 Aurora, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q130570562	P735	Q1066178	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q130570562	P735	Q1067071	P1545	"2"	P3831	Q245025
#   Q64691034 Gotthard Johann* von Budberg: P735 given name = Q18177267 Gotthard, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q64691034	P735	Q18177267	P1545	"1"	P7452	Q3409033
#   Q110151674 Jakobina Gustava von Essen: P735 given name = Q21144392 Gustava, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110151674	P735	Q21144392	P1545	"2"	P3831	Q245025
#   Q1658721 Olof Johan Södermark: P735 given name = Q18089653 Olof, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q1658721	P735	Q18089653	P1545	"1"	P7452	Q3409033
#   P735 given name = Q10989273 Johan, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q1658721	P735	Q10989273	P1545	"2"	P3831	Q245025
#   Q110558406 Katharina Elisabeth von der Schulenburg: P735 given name = Q63611044 Elisabeth, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110558406	P735	Q63611044	P1545	"2"	P3831	Q245025
#   Q5779412 Göran Gyllenstierna af Lundholm: P735 given name = Q1559427 Göran, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q5779412	P735	Q1559427	P1545	"1"	P7452	Q3409033
#   Q16466645 Olena Ida Teresia Falkman: P735 given name = Q7086343 Olena, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q16466645	P735	Q7086343	P1545	"1"	P7452	Q3409033
#   P735 given name = Q644599 Ida, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q16466645	P735	Q644599	P1545	"2"	P3831	Q245025
#   P735 given name = Q18192713 Teresia, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q16466645	P735	Q18192713	P1545	"3"	P3831	Q245025
#   Q141257264 Lydik Rasmussen Amdal: P22 father = Q141257299 Rasmus Lydikson Amdal
Q141257264	P22	Q141257299	S2600	"6000000023605569477"
#   Q6060350 Lars Georg Rabenius: P735 given name = Q1985538 Georg, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q6060350	P735	Q1985538	P1545	"2"	P3831	Q245025
#   Q66316940 Anna Sofia Bäck: P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q66316940	P735	Q18201520	P1545	"2"	P3831	Q245025
#   Q2694124 Albrecht Elof Ihre d.y.: P735 given name = Q3366319 Elof, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q2694124	P735	Q3366319	P1545	"2"	P3831	Q245025
#   Q94790988 Martin Törngren: P735 given name = Q18002399 Martin
Q94790988	P735	Q18002399
#   Q110153084 Amalia Eleonora von Lepel: P735 given name = Q453020 Amalia, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110153084	P735	Q453020	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18759077 Eleonora, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110153084	P735	Q18759077	P1545	"2"	P3831	Q245025
#   Q16206992 Daniel Peter Layard MD: P735 given name = Q53787734 Daniel, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q16206992	P735	Q53787734	P1545	"1"	P7452	Q3409033
#   P735 given name = Q2793400 Peter, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q16206992	P735	Q2793400	P1545	"2"	P3831	Q245025
#   Q99207667 Judith Verplanck: P735 given name = Q5954149 Judith
Q99207667	P735	Q5954149
#   Q141250233 Joachim Johnson Lea: P40 child = Q141250238 Marta Joakimsdatter Lea
Q141250233	P40	Q141250238	S2600	"6000000025793788004"
#   Q141250238 Marta Joakimsdatter Lea: P22 father = Q141250233 Joachim Johnson Lea
Q141250238	P22	Q141250233	S2600	"6000000025810442031"
#   Q6092385 Axel Gösta* Fabian Sandels: P735 given name = Q5407300 Axel, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q6092385	P735	Q5407300	P1545	"1"	P7452	Q3409033
#   Q6066136 Johannes Petri Reftelius Ostrogothus: P735 given name = Q2117521 Johannes, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q6066136	P735	Q2117521	P1545	"1"	P7452	Q3409033
#   P735 given name = Q10625184 Petri, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q6066136	P735	Q10625184	P1545	"2"	P3831	Q245025
#   Q6066129 Johan Martin Reftelius: P735 given name = Q18002399 Martin, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q6066129	P735	Q18002399	P1545	"2"	P3831	Q245025
#   Q109807709 Dorothea von Schwerin: P735 given name = Q909253 Dorothea, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q109807709	P735	Q909253	P1545	"1"	P7452	Q3409033
#   P734 family name = Q37225673 Schwerin
Q109807709	P734	Q37225673
#   Q110304572 Cecilia Christophers: P735 given name = Q859234 Cecilia
Q110304572	P735	Q859234
#   Q110304541 Margareta Catharina von Finecke: P735 given name = Q8274988 Margareta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110304541	P735	Q8274988	P1545	"1"	P7452	Q3409033
#   P735 given name = Q17317997 Catharina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110304541	P735	Q17317997	P1545	"2"	P3831	Q245025
#   Q81363375 Claes Henrik Fries: P735 given name = Q19818179 Claes, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q81363375	P735	Q19818179	P1545	"1"	P7452	Q3409033
#   P735 given name = Q594279 Henrik, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q81363375	P735	Q594279	P1545	"2"	P3831	Q245025
#   Q6069858 Andreas Olai Rhyzelius: P735 given name = Q19384399 Olai, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q6069858	P735	Q19384399	P1545	"2"	P3831	Q245025
#   Q1446693 Ludwig von Pincier: P735 given name = Q14159020 Ludwig, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q1446693	P735	Q14159020	P1545	"1"	P7452	Q3409033
#   Q75579166 John Atchison Atchesonne Acheson: P22 father = Q75577007 Alexander Atchesonne
Q75579166	P22	Q75577007	S2600	"6000000032224244385"
#   P2600 Geni.com profile ID = 6000000032224244385 John Atchison Atchesonne Acheson, qualified P1810 subject named as John Atchison Atchesonne Acheson
Q75579166	P2600	"6000000032224244385"	P1810	"John Atchison Atchesonne Acheson"
#   P735 given name = Q4925477 John, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q75579166	P735	Q4925477	P1545	"1"	P7452	Q3409033
#   Q6183620 Nils Sommelius: P735 given name = Q16423038 Nils
Q6183620	P735	Q16423038
#   Q6092396 Karl Knutsson Sandels: P735 given name = Q136771753 Karl
Q6092396	P735	Q136771753
#   Q141257237 Julie Wilkens Engebretsen: P26 spouse = Q141257311 Waldemar Leopold Engebretsen
Q141257237	P26	Q141257311	S2600	"6000000036729993087"
#   Q141257311 Waldemar Leopold Engebretsen: P26 spouse = Q141257237 Julie Wilkens Engebretsen
Q141257311	P26	Q141257237	S2600	"6000000036747100847"
#   Q15079473 Alexander Johann Peterson: P735 given name = Q923 Alexander, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q15079473	P735	Q923	P1545	"1"	P7452	Q3409033
#   P735 given name = Q11122389 Johann, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q15079473	P735	Q11122389	P1545	"2"	P3831	Q245025
#   Q106590904 Elin Elisabet Maria von Heijne-Lillienberg: P735 given name = Q19833184 Elin, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q106590904	P735	Q19833184	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16423275 Elisabet, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q106590904	P735	Q16423275	P1545	"2"	P3831	Q245025
#   P735 given name = Q325872 Maria, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q106590904	P735	Q325872	P1545	"3"	P3831	Q245025
#   Q5547967 Erik Alstrin: P735 given name = Q750186 Erik
Q5547967	P735	Q750186
#   Q5653897 Harald Nordenson: P735 given name = Q1530266 Harald
Q5653897	P735	Q1530266
#   Q138495479 Friedrich Conrad Dietrich Adrian von Kleist: P735 given name = Q14038597 Friedrich, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q138495479	P735	Q14038597	P1545	"1"	P7452	Q3409033
#   P735 given name = Q17436400 Conrad, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q138495479	P735	Q17436400	P1545	"2"	P3831	Q245025
#   P735 given name = Q18145860 Dietrich, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q138495479	P735	Q18145860	P1545	"3"	P3831	Q245025
#   P735 given name = Q372250 Adrian, qualified P1545 series ordinal 4, P3831 object of statement has role Q245025 middle name
Q138495479	P735	Q372250	P1545	"4"	P3831	Q245025
#   Q14554945 Robert Magnus von Rosen: P735 given name = Q18109457 Magnus, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q14554945	P735	Q18109457	P1545	"2"	P3831	Q245025
#   Q100441649 Paolo Passionei: P735 given name = Q15731774 Paolo
Q100441649	P735	Q15731774
#   Q5702986 Carl Olof Delldén: P735 given name = Q18089653 Olof, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q5702986	P735	Q18089653	P1545	"2"	P3831	Q245025
#   Q108673638 Margareta Behm: P22 father = Q25451348 Jon Mickelsson Behm
Q108673638	P22	Q25451348	S2600	"6000000076005021009"
#   P2600 Geni.com profile ID = 6000000076005021009 Margareta Behm, qualified P1810 subject named as Margareta Behm
Q108673638	P2600	"6000000076005021009"	P1810	"Margareta Behm"
#   P735 given name = Q8274988 Margareta
Q108673638	P735	Q8274988
#   Q5819456 Zacharias Hæggström: P735 given name = Q97932747 Zacharias
Q5819456	P735	Q97932747
#   Q3359192 Elsa Beata Wrede af Elimä: P735 given name = Q338015 Beata, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q3359192	P735	Q338015	P1545	"2"	P3831	Q245025
#   Q130524451 Carl Henrik von Hofsten RSO: P735 given name = Q2529610 Carl, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q130524451	P735	Q2529610	P1545	"1"	P7452	Q3409033
#   P735 given name = Q594279 Henrik, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q130524451	P735	Q594279	P1545	"2"	P3831	Q245025
#   Q109335354 Johan Henrik Wegelin: P735 given name = Q10989273 Johan, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q109335354	P735	Q10989273	P1545	"1"	P7452	Q3409033
#   P735 given name = Q594279 Henrik, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q109335354	P735	Q594279	P1545	"2"	P3831	Q245025
#   Q5622753 Daniel Djurberg: P735 given name = Q53787734 Daniel
Q5622753	P735	Q53787734

