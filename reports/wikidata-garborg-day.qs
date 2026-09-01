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

# Olofsdotter -- patronymic, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Olofsdotter"
LAST	Len	"Olofsdotter"
#   set the mul label to "Olofsdotter"
LAST	Lmul	"Olofsdotter"
#   set the en description to "patronymic"
LAST	Den	"patronymic"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141216618 Karin Olofsdotter: P5056 patronym or matronym = the item just created, qualified P144 based on Q141216403 Olof Nilsson
Q141216618	P5056	LAST	P144	Q141216403	S2600	"348968026630001429"
#   Q141224093 Beata Magdalena Olofsdotter Mellberg: P5056 patronym or matronym = the item just created
Q141224093	P5056	LAST	S2600	"6000000001865185124"
#   Q141249729 Kristina Olofsdotter Spaak: P5056 patronym or matronym = the item just created
Q141249729	P5056	LAST	S2600	"6000000006897337018"
#   Q141244092 Christina Olofsdotter Hammar: P5056 patronym or matronym = the item just created
Q141244092	P5056	LAST	S2600	"6000000009492573975"

# Frondin -- family, 3 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Frondin"
LAST	Len	"Frondin"
#   set the mul label to "Frondin"
LAST	Lmul	"Frondin"
#   set the en description to "family name"
LAST	Den	"family name"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q141223420 Gunilla Margareta Frondin: P734 family name = the item just created, qualified P3831 object of statement has role Q28418670 married name
Q141223420	P734	LAST	P3831	Q28418670	S2600	"6000000011759927315"
#   Q5745634 Elias Frondin: P734 family name = the item just created
Q5745634	P734	LAST	S2600	"6000000018625238474"
#   Q5745627 Berge / Birger Frondin: P734 family name = the item just created
Q5745627	P734	LAST	S2600	"6000000020128505901"

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

# 298 more name items are needed and wait for a later
# run -- 3 a day is her cap, not a limit of the data:
#   Hansson (patronymic), 3 bearer(s)
#   Helgesen (patronymic), 3 bearer(s)
#   Høle (family), 3 bearer(s)
#   Ingebretsdatter (patronymic), 3 bearer(s)
#   Kristiansen (patronymic), 3 bearer(s)
#   Låge-Håland (family), 3 bearer(s)
#   Magnusson (patronymic), 3 bearer(s)
#   Nedre (family), 3 bearer(s)
#   Pedersdatter (patronymic), 3 bearer(s)
#   Røyneberg (family), 3 bearer(s)
#   Söfdeborg (family), 3 bearer(s)
#   Tollefson (patronymic), 3 bearer(s)
#   ... and 286 more

# ========================================================================
# THE DAY'S PEOPLE
# ========================================================================

# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   2097 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   Q29246906 Eleonora Juliana Wiggman: set the ja label to "エレオノーラ・ジュリアナ・ヴィグマン"
Q29246906	Lja	"エレオノーラ・ジュリアナ・ヴィグマン"
#   set the zh label to "埃莱奥诺拉·朱莉安娜·维格曼"
Q29246906	Lzh	"埃莱奥诺拉·朱莉安娜·维格曼"
#   set the ko label to "에레오노라 주리아나 위그만"
Q29246906	Lko	"에레오노라 주리아나 위그만"
#   set the ja label to "マルガレータ・ゴディクスドッテル・フィンケ"
Q105796231	Lja	"マルガレータ・ゴディクスドッテル・フィンケ"
#   set the zh label to "瑪格麗塔·戈迪克斯多特·芬凯"
Q105796231	Lzh	"瑪格麗塔·戈迪克斯多特·芬凯"
#   set the ko label to "마르가레타 괴디크스도테르 핀케"
Q105796231	Lko	"마르가레타 괴디크스도테르 핀케"
#   set the ja label to "ラース・ベントソン・ヒエルタ"
Q110386205	Lja	"ラース・ベントソン・ヒエルタ"
#   set the zh label to "拉尔斯·本格特松·希埃尔塔"
Q110386205	Lzh	"拉尔斯·本格特松·希埃尔塔"
#   set the ko label to "라르스 벵촌 히에르타"
Q110386205	Lko	"라르스 벵촌 히에르타"
#   Q72388326 Isabel de Vipont: set the ja label to "イザベル・デ・ヴィポント"
Q72388326	Lja	"イザベル・デ・ヴィポント"
#   set the zh label to "伊莎贝尔·德·维蓬特"
Q72388326	Lzh	"伊莎贝尔·德·维蓬特"
#   set the ko label to "이사벨 데 비폰트"
Q72388326	Lko	"이사벨 데 비폰트"
#   set the ja label to "セシリア・ルチア・ブロデルセン"
Q130683609	Lja	"セシリア・ルチア・ブロデルセン"
#   set the zh label to "塞西莉亚·露西娅·布罗德尔森"
Q130683609	Lzh	"塞西莉亚·露西娅·布罗德尔森"
#   set the ko label to "케키리아 루키아 브로데르센"
Q130683609	Lko	"케키리아 루키아 브로데르센"

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Berta Larsdatter Kvam"
LAST	Len	"Berta Larsdatter Kvam"
#   set the mul label to "Berta Larsdatter Kvam"
LAST	Lmul	"Berta Larsdatter Kvam"
#   add a mul alias "Berta Larsdatter Nedre Rossavik"
LAST	Amul	"Berta Larsdatter Nedre Rossavik"
#   set the ja label to "ベルタ・ラーシュダッテル・クヴァム"
LAST	Lja	"ベルタ・ラーシュダッテル・クヴァム"
#   set the zh label to "贝尔塔·拉尔斯达特·克瓦姆"
LAST	Lzh	"贝尔塔·拉尔斯达特·克瓦姆"
#   set the ko label to "베르타 라르스다테르 크밤"
LAST	Lko	"베르타 라르스다테르 크밤"
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
#   P734 family name = Q122838342, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q122838342	P3831	Q2507958
#   P734 family name = Q30086760 Kvam, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q30086760	P3831	Q28418670
#   add a mul alias "Berete Kvam"
LAST	Amul	"Berete Kvam"
#   add a mul alias "Berta Kvam"
LAST	Amul	"Berta Kvam"

# create a new item
CREATE
#   set the en label to "Brita Magdalena Eriksdotter Rahm"
LAST	Len	"Brita Magdalena Eriksdotter Rahm"
#   set the mul label to "Brita Magdalena Eriksdotter Rahm"
LAST	Lmul	"Brita Magdalena Eriksdotter Rahm"
#   set the ja label to "ブリッタ・マグダレーナ・エリクスドッテル・ラーム"
LAST	Lja	"ブリッタ・マグダレーナ・エリクスドッテル・ラーム"
#   set the zh label to "布里塔·马格达莱纳·埃里克斯多塔·拉姆"
LAST	Lzh	"布里塔·马格达莱纳·埃里克斯多塔·拉姆"
#   set the ko label to "브리타 막다레나 에리크스도테르 라흐므"
LAST	Lko	"브리타 막다레나 에리크스도테르 라흐므"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000001186122035 Brita Magdalena Eriksdotter Rahm, qualified P1810 subject named as Brita Magdalena Eriksdotter Rahm
LAST	P2600	"6000000001186122035"	P1810	"Brita Magdalena Eriksdotter Rahm"
#   P569 date of birth = +1755-02-09T00:00:00Z/11
LAST	P569	+1755-02-09T00:00:00Z/11	S2600	"6000000001186122035"
#   P570 date of death = +1815-06-29T00:00:00Z/11
LAST	P570	+1815-06-29T00:00:00Z/11	S2600	"6000000001186122035"
#   P26 spouse = Q141225740 Jakob Chydenius
LAST	P26	Q141225740	S2600	"6000000001186122035"
#   P40 child = Q141249739 Peter Chydenius
LAST	P40	Q141249739	S2600	"6000000001186122035"
#   Q141225740 Jakob Chydenius: P26 spouse = the item just created
Q141225740	P26	LAST	S2600	"6000000001186122035"
#   Q141249739 Peter Chydenius: P25 mother = the item just created
Q141249739	P25	LAST	S2600	"6000000001186122035"
#   the item just created: P735 given name = Q918013, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q918013	P1545	"1"	P7452	Q3409033
#   P735 given name = Q842544 Magdalena, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q842544	P1545	"2"	P3831	Q245025
#   P5056 patronym or matronym = Q130232912 Eriksdotter
LAST	P5056	Q130232912

# create a new item
CREATE
#   set the en label to "Christina Frondin"
LAST	Len	"Christina Frondin"
#   set the mul label to "Christina Frondin"
LAST	Lmul	"Christina Frondin"
#   set the ja label to "クリスティーナ・フロンディン"
LAST	Lja	"クリスティーナ・フロンディン"
#   set the zh label to "克里斯蒂娜·夫龙丁"
LAST	Lzh	"克里斯蒂娜·夫龙丁"
#   set the ko label to "츠리스티나 프론딘"
LAST	Lko	"츠리스티나 프론딘"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000018625286380 Christina Frondin, qualified P1810 subject named as Christina Frondin
LAST	P2600	"6000000018625286380"	P1810	"Christina Frondin"
#   P569 date of birth = +1655-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P569	+1655-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"6000000018625286380"
#   P570 date of death = +1696-00-00T00:00:00Z/9, qualified P1319 earliest date +1696-00-00T00:00:00Z/9
LAST	P570	+1696-00-00T00:00:00Z/9	P1319	+1696-00-00T00:00:00Z/9	S2600	"6000000018625286380"
#   P40 child = Q19976772 Simon Melander
LAST	P40	Q19976772	S2600	"6000000018625286380"
#   Q19976772 Simon Melander: P25 mother = the item just created
Q19976772	P25	LAST	S2600	"6000000018625286380"
#   the item just created: P735 given name = Q1083457 Christina
LAST	P735	Q1083457

# create a new item
CREATE
#   set the en label to "Conrad von Braunjohan"
LAST	Len	"Conrad von Braunjohan"
#   set the mul label to "Conrad von Braunjohan"
LAST	Lmul	"Conrad von Braunjohan"
#   set the ja label to "コンラッド・ヴォン・ブラウンヨハン"
LAST	Lja	"コンラッド・ヴォン・ブラウンヨハン"
#   set the zh label to "康拉德·翁·布拉温约汉"
LAST	Lzh	"康拉德·翁·布拉温约汉"
#   set the ko label to "콘라드 본 브라우노한"
LAST	Lko	"콘라드 본 브라우노한"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000006436219130 Conrad von Braunjohan, qualified P1810 subject named as Conrad von Braunjohan
LAST	P2600	"6000000006436219130"	P1810	"Conrad von Braunjohan"
#   P569 date of birth = +1636-11-12T00:00:00Z/11
LAST	P569	+1636-11-12T00:00:00Z/11	S2600	"6000000006436219130"
#   P570 date of death = +1691-04-13T00:00:00Z/11
LAST	P570	+1691-04-13T00:00:00Z/11	S2600	"6000000006436219130"
#   P40 child = Q141249724 Carl Rutger von Braunjohan
LAST	P40	Q141249724	S2600	"6000000006436219130"
#   Q141249724 Carl Rutger von Braunjohan: P22 father = the item just created
Q141249724	P22	LAST	S2600	"6000000006436219130"
#   the item just created: P735 given name = Q17436400 Conrad
LAST	P735	Q17436400

# create a new item
CREATE
#   set the en label to "Guri Ivarsdotter Jørpeland"
LAST	Len	"Guri Ivarsdotter Jørpeland"
#   set the mul label to "Guri Ivarsdotter Jørpeland"
LAST	Lmul	"Guri Ivarsdotter Jørpeland"
#   set the ja label to "グリ・イヴァルスドッテル・ヨルペランド"
LAST	Lja	"グリ・イヴァルスドッテル・ヨルペランド"
#   set the zh label to "古里·伊瓦尔斯多特·约尔佩兰德"
LAST	Lzh	"古里·伊瓦尔斯多特·约尔佩兰德"
#   set the ko label to "구리 이바르스도테르 죄르페란드"
LAST	Lko	"구리 이바르스도테르 죄르페란드"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000007980806681 Guri Ivarsdotter Jørpeland, qualified P1810 subject named as Guri Ivarsdotter Jørpeland
LAST	P2600	"6000000007980806681"	P1810	"Guri Ivarsdotter Jørpeland"
#   P569 date of birth = +1603-00-00T00:00:00Z/9
LAST	P569	+1603-00-00T00:00:00Z/9	S2600	"6000000007980806681"
#   P570 date of death = +1671-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P570	+1671-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"6000000007980806681"
#   P26 spouse = Q141249611 Ivar Toreson Tjentland
LAST	P26	Q141249611	S2600	"6000000007980806681"
#   Q141249611 Ivar Toreson Tjentland: P26 spouse = the item just created
Q141249611	P26	LAST	S2600	"6000000007980806681"
#   the item just created: P735 given name = Q11973376 Guri
LAST	P735	Q11973376

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
#   set the en label to "Hans Rasmussen Bø"
LAST	Len	"Hans Rasmussen Bø"
#   set the mul label to "Hans Rasmussen Bø"
LAST	Lmul	"Hans Rasmussen Bø"
#   set the ja label to "ハンス・ラスムセン・ベー"
LAST	Lja	"ハンス・ラスムセン・ベー"
#   set the zh label to "汉斯·拉斯穆森·鲍伊"
LAST	Lzh	"汉斯·拉斯穆森·鲍伊"
#   set the ko label to "한스 라스무센 뵈"
LAST	Lko	"한스 라스무센 뵈"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000196541335826 Hans Rasmussen Bø, qualified P1810 subject named as Hans Rasmussen Bø
LAST	P2600	"6000000196541335826"	P1810	"Hans Rasmussen Bø"
#   P569 date of birth = +1815-08-12T00:00:00Z/11
LAST	P569	+1815-08-12T00:00:00Z/11	S2600	"6000000196541335826"
#   P570 date of death = +1816-09-03T00:00:00Z/11
LAST	P570	+1816-09-03T00:00:00Z/11	S2600	"6000000196541335826"
#   P22 father = Q141200074 Rasmus Olsen Bø
LAST	P22	Q141200074	S2600	"6000000196541335826"
#   P25 mother = Q141199809 Ane Marie Helgesdatter Bø
LAST	P25	Q141199809	S2600	"6000000196541335826"
#   Q141200074 Rasmus Olsen Bø: P40 child = the item just created
Q141200074	P40	LAST	S2600	"6000000196541335826"
#   Q141199809 Ane Marie Helgesdatter Bø: P40 child = the item just created
Q141199809	P40	LAST	S2600	"6000000196541335826"
#   the item just created: P735 given name = Q632842
LAST	P735	Q632842
#   P734 family name = Q30253098
LAST	P734	Q30253098

# create a new item
CREATE
#   set the en label to "Ivar Ivarson Tjentland I"
LAST	Len	"Ivar Ivarson Tjentland I"
#   set the mul label to "Ivar Ivarson Tjentland I"
LAST	Lmul	"Ivar Ivarson Tjentland I"
#   set the ja label to "イヴァル・イーヴァルソン・トイェントランド・I"
LAST	Lja	"イヴァル・イーヴァルソン・トイェントランド・I"
#   set the zh label to "伊瓦尔·伊瓦尔松·特延特兰德·I"
LAST	Lzh	"伊瓦尔·伊瓦尔松·特延特兰德·I"
#   set the ko label to "이바르 이바르손 첸트란드 이"
LAST	Lko	"이바르 이바르손 첸트란드 이"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000007980617695 Ivar Ivarson Tjentland I, qualified P1810 subject named as Ivar Ivarson Tjentland I
LAST	P2600	"6000000007980617695"	P1810	"Ivar Ivarson Tjentland I"
#   P569 date of birth = +1630-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P569	+1630-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"6000000007980617695"
#   P570 date of death = +1681-00-00T00:00:00Z/9
LAST	P570	+1681-00-00T00:00:00Z/9	S2600	"6000000007980617695"
#   P22 father = Q141249611 Ivar Toreson Tjentland
LAST	P22	Q141249611	S2600	"6000000007980617695"
#   Q141249611 Ivar Toreson Tjentland: P40 child = the item just created
Q141249611	P40	LAST	S2600	"6000000007980617695"
#   the item just created: P735 given name = Q127069 Ivar
LAST	P735	Q127069

# create a new item
CREATE
#   set the en label to "Johanna Charlotta Stierncrona"
LAST	Len	"Johanna Charlotta Stierncrona"
#   set the mul label to "Johanna Charlotta Stierncrona"
LAST	Lmul	"Johanna Charlotta Stierncrona"
#   set the ja label to "ヨハンナ・カルロタ・スティアンクロナ"
LAST	Lja	"ヨハンナ・カルロタ・スティアンクロナ"
#   set the zh label to "约翰娜·卡尔洛塔·斯蒂恩克罗纳"
LAST	Lzh	"约翰娜·卡尔洛塔·斯蒂恩克罗纳"
#   set the ko label to "조한나 차르로타 스티에르느크로나"
LAST	Lko	"조한나 차르로타 스티에르느크로나"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000010154259111 Johanna Charlotta Stierncrona, qualified P1810 subject named as Johanna Charlotta Stierncrona
LAST	P2600	"6000000010154259111"	P1810	"Johanna Charlotta Stierncrona"
#   P569 date of birth = +1779-10-14T00:00:00Z/11, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P569	+1779-10-14T00:00:00Z/11	P1480	Q5727902	S2600	"6000000010154259111"
#   P570 date of death = +1816-04-01T00:00:00Z/11, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P570	+1816-04-01T00:00:00Z/11	P1480	Q5727902	S2600	"6000000010154259111"
#   P26 spouse = Q19975889 Fredrik August August Adelswärd
LAST	P26	Q19975889	S2600	"6000000010154259111"
#   Q19975889 Fredrik August August Adelswärd: P26 spouse = the item just created
Q19975889	P26	LAST	S2600	"6000000010154259111"
#   the item just created: P735 given name = Q4120836 Johanna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q4120836	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1067071	P1545	"2"	P3831	Q245025

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
#   set the en label to "Katarina Gottschalksdotter"
LAST	Len	"Katarina Gottschalksdotter"
#   set the mul label to "Katarina Gottschalksdotter"
LAST	Lmul	"Katarina Gottschalksdotter"
#   set the ja label to "カタリーナ・ゴトシャルクスドッテル"
LAST	Lja	"カタリーナ・ゴトシャルクスドッテル"
#   set the zh label to "卡塔里纳·戈特沙尔克斯多特"
LAST	Lzh	"卡塔里纳·戈特沙尔克斯多特"
#   set the ko label to "카타리나 고츠찰크스도테르"
LAST	Lko	"카타리나 고츠찰크스도테르"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000007677668316 Katarina Gottschalksdotter, qualified P1810 subject named as Katarina Gottschalksdotter
LAST	P2600	"6000000007677668316"	P1810	"Katarina Gottschalksdotter"
#   P569 date of birth = +1612-00-00T00:00:00Z/9, qualified P1326 latest date +1612-00-00T00:00:00Z/9
LAST	P569	+1612-00-00T00:00:00Z/9	P1326	+1612-00-00T00:00:00Z/9	S2600	"6000000007677668316"
#   P26 spouse = Q5773252 Lars Grubbe
LAST	P26	Q5773252	S2600	"6000000007677668316"
#   Q5773252 Lars Grubbe: P26 spouse = the item just created
Q5773252	P26	LAST	S2600	"6000000007677668316"
#   the item just created: P735 given name = Q16277703 Katarina
LAST	P735	Q16277703
#   add a mul alias "Karin"
LAST	Amul	"Karin"

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
#   set the en label to "Maria Christina Nordenflycht"
LAST	Len	"Maria Christina Nordenflycht"
#   set the mul label to "Maria Christina Nordenflycht"
LAST	Lmul	"Maria Christina Nordenflycht"
#   set the ja label to "マリア・クリスティーナ・ノルデンフリクト"
LAST	Lja	"マリア・クリスティーナ・ノルデンフリクト"
#   set the zh label to "玛丽亚·克里斯蒂娜·诺尔登夫利克特"
LAST	Lzh	"玛丽亚·克里斯蒂娜·诺尔登夫利克特"
#   set the ko label to "마리아 츠리스티나 노르덴프리츠트"
LAST	Lko	"마리아 츠리스티나 노르덴프리츠트"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000012361827945 Maria Christina Nordenflycht, qualified P1810 subject named as Maria Christina Nordenflycht
LAST	P2600	"6000000012361827945"	P1810	"Maria Christina Nordenflycht"
#   P569 date of birth = +1707-00-00T00:00:00Z/9
LAST	P569	+1707-00-00T00:00:00Z/9	S2600	"6000000012361827945"
#   P570 date of death = +1772-00-00T00:00:00Z/9
LAST	P570	+1772-00-00T00:00:00Z/9	S2600	"6000000012361827945"
#   P40 child = Q141244218 Fredrika Lovisa Uggla
LAST	P40	Q141244218	S2600	"6000000012361827945"
#   Q141244218 Fredrika Lovisa Uggla: P25 mother = the item just created
Q141244218	P25	LAST	S2600	"6000000012361827945"
#   the item just created: P735 given name = Q325872 Maria, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q325872	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1083457 Christina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1083457	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the mul label to "NN"
LAST	Lmul	"NN"
#   set the ca label to "pare de Albrekt"
LAST	Lca	"pare de Albrekt"
#   set the da label to "far til Albrekt"
LAST	Lda	"far til Albrekt"
#   set the de label to "Vater von Albrekt"
LAST	Lde	"Vater von Albrekt"
#   set the en label to "father of Albrekt"
LAST	Len	"father of Albrekt"
#   set the es label to "padre de Albrekt"
LAST	Les	"padre de Albrekt"
#   set the fr label to "père de Albrekt"
LAST	Lfr	"père de Albrekt"
#   set the it label to "padre di Albrekt"
LAST	Lit	"padre di Albrekt"
#   set the ja label to "アルブレクトの父"
LAST	Lja	"アルブレクトの父"
#   set the ko label to "알브레크트의 아버지"
LAST	Lko	"알브레크트의 아버지"
#   set the nb label to "far til Albrekt"
LAST	Lnb	"far til Albrekt"
#   set the nl label to "vader van Albrekt"
LAST	Lnl	"vader van Albrekt"
#   set the pt label to "pai de Albrekt"
LAST	Lpt	"pai de Albrekt"
#   set the sv label to "far till Albrekt"
LAST	Lsv	"far till Albrekt"
#   set the zh label to "阿尔布雷克特之父"
LAST	Lzh	"阿尔布雷克特之父"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000011088574034 NN
LAST	P2600	"6000000011088574034"
#   P40 child = Q141244206 Albrekt
LAST	P40	Q141244206	S2600	"6000000011088574034"
#   Q141244206 Albrekt: P22 father = the item just created
Q141244206	P22	LAST	S2600	"6000000011088574034"

# create a new item
CREATE
#   the item just created: set the mul label to "NN"
LAST	Lmul	"NN"
#   set the ca label to "mare de Albrekt"
LAST	Lca	"mare de Albrekt"
#   set the da label to "mor til Albrekt"
LAST	Lda	"mor til Albrekt"
#   set the de label to "Mutter von Albrekt"
LAST	Lde	"Mutter von Albrekt"
#   set the en label to "mother of Albrekt"
LAST	Len	"mother of Albrekt"
#   set the es label to "madre de Albrekt"
LAST	Les	"madre de Albrekt"
#   set the fr label to "mère de Albrekt"
LAST	Lfr	"mère de Albrekt"
#   set the it label to "madre di Albrekt"
LAST	Lit	"madre di Albrekt"
#   set the ja label to "アルブレクトの母"
LAST	Lja	"アルブレクトの母"
#   set the ko label to "알브레크트의 어머니"
LAST	Lko	"알브레크트의 어머니"
#   set the nb label to "mor til Albrekt"
LAST	Lnb	"mor til Albrekt"
#   set the nl label to "moeder van Albrekt"
LAST	Lnl	"moeder van Albrekt"
#   set the pt label to "mãe de Albrekt"
LAST	Lpt	"mãe de Albrekt"
#   set the sv label to "mor till Albrekt"
LAST	Lsv	"mor till Albrekt"
#   set the zh label to "阿尔布雷克特之母"
LAST	Lzh	"阿尔布雷克特之母"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000011089056376 NN
LAST	P2600	"6000000011089056376"
#   P40 child = Q141244206 Albrekt
LAST	P40	Q141244206	S2600	"6000000011089056376"
#   Q141244206 Albrekt: P25 mother = the item just created
Q141244206	P25	LAST	S2600	"6000000011089056376"

# create a new item
CREATE
#   the item just created: set the mul label to "NN Alanus"
LAST	Lmul	"NN Alanus"
#   set the ca label to "pare de Margareta Katarina Polviander"
LAST	Lca	"pare de Margareta Katarina Polviander"
#   set the da label to "far til Margareta Katarina Polviander"
LAST	Lda	"far til Margareta Katarina Polviander"
#   set the de label to "Vater von Margareta Katarina Polviander"
LAST	Lde	"Vater von Margareta Katarina Polviander"
#   set the en label to "father of Margareta Katarina Polviander"
LAST	Len	"father of Margareta Katarina Polviander"
#   set the es label to "padre de Margareta Katarina Polviander"
LAST	Les	"padre de Margareta Katarina Polviander"
#   set the fr label to "père de Margareta Katarina Polviander"
LAST	Lfr	"père de Margareta Katarina Polviander"
#   set the it label to "padre di Margareta Katarina Polviander"
LAST	Lit	"padre di Margareta Katarina Polviander"
#   set the ja label to "マルガレータ・カタリーナ・ポルヴィアンデルの父"
LAST	Lja	"マルガレータ・カタリーナ・ポルヴィアンデルの父"
#   set the ko label to "마르가레타 카타리나 폴비안데르의 아버지"
LAST	Lko	"마르가레타 카타리나 폴비안데르의 아버지"
#   set the nb label to "far til Margareta Katarina Polviander"
LAST	Lnb	"far til Margareta Katarina Polviander"
#   set the nl label to "vader van Margareta Katarina Polviander"
LAST	Lnl	"vader van Margareta Katarina Polviander"
#   set the pt label to "pai de Margareta Katarina Polviander"
LAST	Lpt	"pai de Margareta Katarina Polviander"
#   set the sv label to "far till Margareta Katarina Polviander"
LAST	Lsv	"far till Margareta Katarina Polviander"
#   set the zh label to "瑪格麗塔·卡塔里纳·波尔维安德尔之父"
LAST	Lzh	"瑪格麗塔·卡塔里纳·波尔维安德尔之父"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000227469393830 NN Alanus
LAST	P2600	"6000000227469393830"
#   P40 child = Q141244229 Margareta Katarina Polviander
LAST	P40	Q141244229	S2600	"6000000227469393830"
#   Q141244229 Margareta Katarina Polviander: P22 father = the item just created
Q141244229	P22	LAST	S2600	"6000000227469393830"

# create a new item
CREATE
#   the item just created: set the mul label to "NN Voster"
LAST	Lmul	"NN Voster"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000227513637856 NN Voster
LAST	P2600	"6000000227513637856"
#   P40 child = Q141244116 NN Voster
LAST	P40	Q141244116	S2600	"6000000227513637856"
#   Q141244116 NN Voster: P22 father = the item just created
Q141244116	P22	LAST	S2600	"6000000227513637856"

# create a new item
CREATE
#   the item just created: set the en label to "Nils Nilsson"
LAST	Len	"Nils Nilsson"
#   set the mul label to "Nils Nilsson"
LAST	Lmul	"Nils Nilsson"
#   set the ja label to "ニルス・ニルソン"
LAST	Lja	"ニルス・ニルソン"
#   set the zh label to "尼尔斯·尼尔松"
LAST	Lzh	"尼尔斯·尼尔松"
#   set the ko label to "닐스 닐손"
LAST	Lko	"닐스 닐손"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000059889323852 Nils Nilsson, qualified P1810 subject named as Nils Nilsson
LAST	P2600	"6000000059889323852"	P1810	"Nils Nilsson"
#   P569 date of birth = +1583-07-06T00:00:00Z/11
LAST	P569	+1583-07-06T00:00:00Z/11	S2600	"6000000059889323852"
#   P22 father = Q141199734 Nils Andersson
LAST	P22	Q141199734	S2600	"6000000059889323852"
#   P25 mother = Q141200083 Sara
LAST	P25	Q141200083	S2600	"6000000059889323852"
#   Q141199734 Nils Andersson: P40 child = the item just created
Q141199734	P40	LAST	S2600	"6000000059889323852"
#   Q141200083 Sara: P40 child = the item just created
Q141200083	P40	LAST	S2600	"6000000059889323852"

# create a new item
CREATE
#   the item just created: set the en label to "Olava Pedersdatter Malmeim"
LAST	Len	"Olava Pedersdatter Malmeim"
#   set the mul label to "Olava Pedersdatter Malmeim"
LAST	Lmul	"Olava Pedersdatter Malmeim"
#   set the ja label to "オラヴァ・ペーデシュダッテル・マルメイム"
LAST	Lja	"オラヴァ・ペーデシュダッテル・マルメイム"
#   set the zh label to "奥拉瓦·佩德斯达特·马尔梅伊姆"
LAST	Lzh	"奥拉瓦·佩德斯达特·马尔梅伊姆"
#   set the ko label to "오라바 페데르스다테르 말메임"
LAST	Lko	"오라바 페데르스다테르 말메임"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003491988284 Olava Pedersdatter Malmeim, qualified P1810 subject named as Olava Pedersdatter Malmeim
LAST	P2600	"6000000003491988284"	P1810	"Olava Pedersdatter Malmeim"
#   P569 date of birth = +1852-08-11T00:00:00Z/11
LAST	P569	+1852-08-11T00:00:00Z/11	S2600	"6000000003491988284"
#   P25 mother = Q141216622 Kristine Jonsdatter Malmeim
LAST	P25	Q141216622	S2600	"6000000003491988284"
#   Q141216622 Kristine Jonsdatter Malmeim: P40 child = the item just created
Q141216622	P40	LAST	S2600	"6000000003491988284"
#   the item just created: P735 given name = Q11993504 Olava
LAST	P735	Q11993504
#   add a mul alias "Olava Malmeim"
LAST	Amul	"Olava Malmeim"

# create a new item
CREATE
#   set the en label to "Olof Hising"
LAST	Len	"Olof Hising"
#   set the mul label to "Olof Hising"
LAST	Lmul	"Olof Hising"
#   set the ja label to "オロフ・ヒシング"
LAST	Lja	"オロフ・ヒシング"
#   set the zh label to "奥洛夫·希辛"
LAST	Lzh	"奥洛夫·希辛"
#   set the ko label to "오로프 히싱"
LAST	Lko	"오로프 히싱"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000009492436475 Olof Hising, qualified P1810 subject named as Olof Hising
LAST	P2600	"6000000009492436475"	P1810	"Olof Hising"
#   P570 date of death = +1728-00-00T00:00:00Z/9
LAST	P570	+1728-00-00T00:00:00Z/9	S2600	"6000000009492436475"
#   P22 father = Q110313452 Carl Hising
LAST	P22	Q110313452	S2600	"6000000009492436475"
#   P25 mother = Q127270462 Barbro Petré
LAST	P25	Q127270462	S2600	"6000000009492436475"
#   Q110313452 Carl Hising: P40 child = the item just created
Q110313452	P40	LAST	S2600	"6000000009492436475"
#   Q127270462 Barbro Petré: P40 child = the item just created
Q127270462	P40	LAST	S2600	"6000000009492436475"
#   the item just created: P735 given name = Q18089653 Olof
LAST	P735	Q18089653
#   P734 family name = Q47462118 Hising
LAST	P734	Q47462118

# create a new item
CREATE
#   set the en label to "Peder Pederson Malmeim"
LAST	Len	"Peder Pederson Malmeim"
#   set the mul label to "Peder Pederson Malmeim"
LAST	Lmul	"Peder Pederson Malmeim"
#   set the ja label to "ペーダー・ペデルソン・マルメイム"
LAST	Lja	"ペーダー・ペデルソン・マルメイム"
#   set the zh label to "彼泽·佩德尔松·马尔梅伊姆"
LAST	Lzh	"彼泽·佩德尔松·马尔梅伊姆"
#   set the ko label to "페데르 페데르손 말메임"
LAST	Lko	"페데르 페데르손 말메임"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003491988194 Peder Pederson Malmeim, qualified P1810 subject named as Peder Pederson Malmeim
LAST	P2600	"6000000003491988194"	P1810	"Peder Pederson Malmeim"
#   P569 date of birth = +1823-08-02T00:00:00Z/11
LAST	P569	+1823-08-02T00:00:00Z/11	S2600	"6000000003491988194"
#   P570 date of death = +1894-08-24T00:00:00Z/11
LAST	P570	+1894-08-24T00:00:00Z/11	S2600	"6000000003491988194"
#   P26 spouse = Q141216622 Kristine Jonsdatter Malmeim
LAST	P26	Q141216622	S2600	"6000000003491988194"
#   Q141216622 Kristine Jonsdatter Malmeim: P26 spouse = the item just created
Q141216622	P26	LAST	S2600	"6000000003491988194"

# create a new item
CREATE
#   the item just created: set the en label to "Peder Tollefson Tunheim"
LAST	Len	"Peder Tollefson Tunheim"
#   set the mul label to "Peder Tollefson Tunheim"
LAST	Lmul	"Peder Tollefson Tunheim"
#   set the ja label to "ペーダー・トレフソン・トゥンヘイム"
LAST	Lja	"ペーダー・トレフソン・トゥンヘイム"
#   set the zh label to "彼泽·托勒夫松·通海姆"
LAST	Lzh	"彼泽·托勒夫松·通海姆"
#   set the ko label to "페데르 톨레프손 툰헤임"
LAST	Lko	"페데르 톨레프손 툰헤임"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000037693988358 Peder Tollefson Tunheim, qualified P1810 subject named as Peder Tollefson Tunheim
LAST	P2600	"6000000037693988358"	P1810	"Peder Tollefson Tunheim"
#   P569 date of birth = +1852-02-26T00:00:00Z/11
LAST	P569	+1852-02-26T00:00:00Z/11	S2600	"6000000037693988358"
#   P570 date of death = +1871-03-25T00:00:00Z/11
LAST	P570	+1871-03-25T00:00:00Z/11	S2600	"6000000037693988358"
#   P22 father = Q141200112 Tollef Pederson Tunheim
LAST	P22	Q141200112	S2600	"6000000037693988358"
#   P25 mother = Q141199826 Anna Maria Samuelsdtr. Tunheim
LAST	P25	Q141199826	S2600	"6000000037693988358"
#   Q141200112 Tollef Pederson Tunheim: P40 child = the item just created
Q141200112	P40	LAST	S2600	"6000000037693988358"
#   Q141199826 Anna Maria Samuelsdtr. Tunheim: P40 child = the item just created
Q141199826	P40	LAST	S2600	"6000000037693988358"
#   the item just created: P735 given name = Q10622039 Peder
LAST	P735	Q10622039
#   P734 family name = Q36927172
LAST	P734	Q36927172
#   add a mul alias "Peder Tunheim"
LAST	Amul	"Peder Tunheim"

# create a new item
CREATE
#   set the en label to "Sara Carlberg"
LAST	Len	"Sara Carlberg"
#   set the mul label to "Sara Carlberg"
LAST	Lmul	"Sara Carlberg"
#   set the ja label to "サラ・カルルベルグ"
LAST	Lja	"サラ・カルルベルグ"
#   set the zh label to "萨拉·卡尔尔贝尔格"
LAST	Lzh	"萨拉·卡尔尔贝尔格"
#   set the ko label to "사라 카르르베르그"
LAST	Lko	"사라 카르르베르그"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000006435949669 Sara Carlberg, qualified P1810 subject named as Sara Carlberg
LAST	P2600	"6000000006435949669"	P1810	"Sara Carlberg"
#   P569 date of birth = +1647-01-31T00:00:00Z/11
LAST	P569	+1647-01-31T00:00:00Z/11	S2600	"6000000006435949669"
#   P570 date of death = +1701-00-00T00:00:00Z/9
LAST	P570	+1701-00-00T00:00:00Z/9	S2600	"6000000006435949669"
#   P22 father = Q141249728 Johan Börgesson Carlberg
LAST	P22	Q141249728	S2600	"6000000006435949669"
#   P25 mother = Q141249729 Kristina Olofsdotter Spaak
LAST	P25	Q141249729	S2600	"6000000006435949669"
#   P40 child = Q141249724 Carl Rutger von Braunjohan
LAST	P40	Q141249724	S2600	"6000000006435949669"
#   Q141249728 Johan Börgesson Carlberg: P40 child = the item just created
Q141249728	P40	LAST	S2600	"6000000006435949669"
#   Q141249729 Kristina Olofsdotter Spaak: P40 child = the item just created
Q141249729	P40	LAST	S2600	"6000000006435949669"
#   Q141249724 Carl Rutger von Braunjohan: P25 mother = the item just created
Q141249724	P25	LAST	S2600	"6000000006435949669"

# create a new item
CREATE
#   the item just created: set the en label to "Sven Bjørnson Hognestad"
LAST	Len	"Sven Bjørnson Hognestad"
#   set the mul label to "Sven Bjørnson Hognestad"
LAST	Lmul	"Sven Bjørnson Hognestad"
#   set the ja label to "スヴェン・ビョルンソン・ホグネスタド"
LAST	Lja	"スヴェン・ビョルンソン・ホグネスタド"
#   set the zh label to "斯文·布约尔恩松·霍格内斯塔德"
LAST	Lzh	"斯文·布约尔恩松·霍格内斯塔德"
#   set the ko label to "스벤 브죄르느손 혹네스타드"
LAST	Lko	"스벤 브죄르느손 혹네스타드"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000006964530073 Sven Bjørnson Hognestad, qualified P1810 subject named as Sven Bjørnson Hognestad
LAST	P2600	"6000000006964530073"	P1810	"Sven Bjørnson Hognestad"
#   P569 date of birth = +1625-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P569	+1625-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"6000000006964530073"
#   P570 date of death = +1709-05-21T00:00:00Z/11
LAST	P570	+1709-05-21T00:00:00Z/11	S2600	"6000000006964530073"
#   P40 child = Q141219189 Eivind Svenson Sveinsen Garborg
LAST	P40	Q141219189	S2600	"6000000006964530073"
#   Q141219189 Eivind Svenson Sveinsen Garborg: P22 father = the item just created
Q141219189	P22	LAST	S2600	"6000000006964530073"
#   the item just created: P735 given name = Q2370957 Sven
LAST	P735	Q2370957
#   P734 family name = Q21509419 Hognestad
LAST	P734	Q21509419

# create a new item
CREATE
#   set the en label to "Tormod Larsson Mele"
LAST	Len	"Tormod Larsson Mele"
#   set the mul label to "Tormod Larsson Mele"
LAST	Lmul	"Tormod Larsson Mele"
#   set the ja label to "トルモド・ラーション・メーレ"
LAST	Lja	"トルモド・ラーション・メーレ"
#   set the zh label to "托尔莫德·拉森·梅勒"
LAST	Lzh	"托尔莫德·拉森·梅勒"
#   set the ko label to "토르모드 라르손 메레"
LAST	Lko	"토르모드 라르손 메레"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003095034818 Tormod Larsson Mele, qualified P1810 subject named as Tormod Larsson Mele
LAST	P2600	"6000000003095034818"	P1810	"Tormod Larsson Mele"
#   P569 date of birth = +1732-00-00T00:00:00Z/9
LAST	P569	+1732-00-00T00:00:00Z/9	S2600	"6000000003095034818"
#   P22 father = Q141189079 Lars Tormodsen Mele
LAST	P22	Q141189079	S2600	"6000000003095034818"
#   P25 mother = Q141189071 Joren Jonsdatter Espedal
LAST	P25	Q141189071	S2600	"6000000003095034818"
#   Q141189079 Lars Tormodsen Mele: P40 child = the item just created
Q141189079	P40	LAST	S2600	"6000000003095034818"
#   Q141189071 Joren Jonsdatter Espedal: P40 child = the item just created
Q141189071	P40	LAST	S2600	"6000000003095034818"
#   the item just created: P735 given name = Q7825922 Tormod
LAST	P735	Q7825922
#   Q6235986 Carl Gustaf Wennerstedt: P3373 sibling = Q141249733 Margareta Helena Wennerstedt
Q6235986	P3373	Q141249733	S2600	"1552522"
#   Q105796231 Margareta Gödiksdotter Fincke till Kanckas: P735 given name = Q8274988 Margareta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q105796231	P735	Q8274988	P1545	"1"	P7452	Q3409033
#   Q110386205 Lars Bengtsson Hierta till Kålsholmen: P735 given name = Q15635262 Lars, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110386205	P735	Q15635262	P1545	"1"	P7452	Q3409033
#   Q130683609 Cecilia Lucia Brodersen: P735 given name = Q859234 Cecilia, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q130683609	P735	Q859234	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1160640 Lucia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q130683609	P735	Q1160640	P1545	"2"	P3831	Q245025
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
#   Q141249724 Carl Rutger von Braunjohan: P26 spouse = Q141249733 Margareta Helena Wennerstedt
Q141249724	P26	Q141249733	S2600	"6000000004352726281"
#   Q141249728 Johan Börgesson Carlberg: P26 spouse = Q141249729 Kristina Olofsdotter Spaak
Q141249728	P26	Q141249729	S2600	"6000000006897169084"
#   Q141249729 Kristina Olofsdotter Spaak: P26 spouse = Q141249728 Johan Börgesson Carlberg
Q141249729	P26	Q141249728	S2600	"6000000006897337018"
#   Q141249736 Mattias Edenberg: P26 spouse = Q141249730 Margareta Catharina Clo
Q141249736	P26	Q141249730	S2600	"6000000007511893198"
#   Q141249733 Margareta Helena Wennerstedt: P26 spouse = Q141249724 Carl Rutger von Braunjohan
Q141249733	P26	Q141249724	S2600	"6000000008541457637"
#   Q141249737 Ole Thoreson Toresen Lende: P26 spouse = Q141249721 Asseline Svensdatter Lende
Q141249737	P26	Q141249721	S2600	"6000000010517303222"
#   Q141249721 Asseline Svensdatter Lende: P26 spouse = Q141249737 Ole Thoreson Toresen Lende
Q141249721	P26	Q141249737	S2600	"6000000013462214188"
#   Q111998458 Sara de Marez: P735 given name = Q833345 Sara, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q111998458	P735	Q833345	P1545	"1"	P7452	Q3409033
#   Q141249730 Margareta Catharina Clo: P26 spouse = Q141249736 Mattias Edenberg
Q141249730	P26	Q141249736	S2600	"6000000020488764955"

