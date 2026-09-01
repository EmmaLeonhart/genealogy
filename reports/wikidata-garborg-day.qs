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

# Gunnarson -- patronymic, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Gunnarson"
LAST	Len	"Gunnarson"
#   set the mul label to "Gunnarson"
LAST	Lmul	"Gunnarson"
#   set the en description to "patronymic"
LAST	Den	"patronymic"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141250216 Bjørn Gunnarson Mele: P5056 patronym or matronym = the item just created
Q141250216	P5056	LAST	S2600	"4462693"
#   Q141244234 Torstein Gunnarson Frafjord: P5056 patronym or matronym = the item just created
Q141244234	P5056	LAST	S2600	"6000000005607365222"
#   Q141216458 Asbjørn Gunnarson Bø: P5056 patronym or matronym = the item just created
Q141216458	P5056	LAST	S2600	"6000000042211257078"

# Låge-Håland -- family, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Låge-Håland"
LAST	Len	"Låge-Håland"
#   set the mul label to "Låge-Håland"
LAST	Lmul	"Låge-Håland"
#   set the en description to "family name"
LAST	Den	"family name"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q141216634 Marit Hansdatter Stavnheim: P734 family name = the item just created, qualified P3831 object of statement has role Q2507958 birth name
Q141216634	P734	LAST	P3831	Q2507958	S2600	"6000000009127909254"
#   Q141216381 Hans Rasmussen Låge-Håland: P734 family name = the item just created
Q141216381	P734	LAST	S2600	"6000000009127934231"
#   Q141250244 Rasmus Hansen Nord-Varhaug: P734 family name = the item just created, qualified P3831 object of statement has role Q2507958 birth name
Q141250244	P734	LAST	P3831	Q2507958	S2600	"6000000087451690855"
#   Q141199918 Kirsten Hansdatter Grøtheim: P734 family name = the item just created, qualified P3831 object of statement has role Q2507958 birth name
Q141199918	P734	LAST	P3831	Q2507958	S2600	"6000000087451897836"

# Årsvoll -- family, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Årsvoll"
LAST	Len	"Årsvoll"
#   set the mul label to "Årsvoll"
LAST	Lmul	"Årsvoll"
#   set the en description to "family name"
LAST	Den	"family name"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q141225244 Rakel Maria Govertsdatter Årsvoll: P734 family name = the item just created
Q141225244	P734	LAST	S2600	"6000000002335691955"
#   Q141216470 Govert Jonson Årsvoll: P734 family name = the item just created
Q141216470	P734	LAST	S2600	"6000000008174080446"
#   Q141216363 Anne Govertsdtr. Bratland: P734 family name = the item just created, qualified P3831 object of statement has role Q2507958 birth name
Q141216363	P734	LAST	P3831	Q2507958	S2600	"6000000169074443823"

# 323 more name items are needed and wait for a later
# run -- 3 a day is her cap, not a limit of the data:
#   Garfve (family), 3 bearer(s)
#   Hakunge (family), 3 bearer(s)
#   Hansen (patronymic), 3 bearer(s)
#   Hansson (patronymic), 3 bearer(s)
#   Helgesen (patronymic), 3 bearer(s)
#   Høle (family), 3 bearer(s)
#   Ingebretsdatter (patronymic), 3 bearer(s)
#   Johansdotter (patronymic), 3 bearer(s)
#   Knutsdatter (patronymic), 3 bearer(s)
#   Kristiansen (patronymic), 3 bearer(s)
#   Magnusson (patronymic), 3 bearer(s)
#   Pedersdatter (patronymic), 3 bearer(s)
#   ... and 311 more

# ========================================================================
# THE DAY'S PEOPLE
# ========================================================================

# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   2715 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   Q135480235: holds 'Maria Rebecka Lemchen'; ours is 'Maria Rebecca Munck af Rosenschôld'
#   Q135480235: keep the outgoing label as an alias before it is replaced
Q135480235	Amul	"Maria Rebecka Lemchen"
#   Q135480235: set the mul label to 'Maria Rebecca Munck af Rosenschôld'
Q135480235	Lmul	"Maria Rebecca Munck af Rosenschôld"
#   Q135480235: set the en label to 'Maria Rebecca Munck af Rosenschôld'
Q135480235	Len	"Maria Rebecca Munck af Rosenschôld"
#   Q135480235: set the ja label
Q135480235	Lja	"マリア・レベッカ・ムンク・アフ・ロセンショルド"
#   Q135480235: set the zh label
Q135480235	Lzh	"玛丽亚·丽贝卡·蒙克·阿夫·罗森肖尔德"
#   Q135480235: set the ko label
Q135480235	Lko	"마리아 레베카 문크 아프 로센솔드"
#   add a mul alias "Sissel Knutsdatter Knutsdatter"
Q141250249	Amul	"Sissel Knutsdatter Knutsdatter"
#   set the ja label to "クリスティーナ・フヨドロヴナ・ロスラディン"
Q110561236	Lja	"クリスティーナ・フヨドロヴナ・ロスラディン"
#   set the zh label to "克里斯蒂娜·夫约多罗夫纳·罗斯拉丁"
Q110561236	Lzh	"克里斯蒂娜·夫约多罗夫纳·罗斯拉丁"
#   set the ko label to "츠리스티나 프조도롭나 로스라딘"
Q110561236	Lko	"츠리스티나 프조도롭나 로스라딘"
#   Q6371586 Carl August Ramsay: set the ja label to "カール・アウグスト・ラムゼイ"
Q6371586	Lja	"カール・アウグスト・ラムゼイ"
#   set the zh label to "卡尔·奥古斯特·拉姆齐"
Q6371586	Lzh	"卡尔·奥古斯特·拉姆齐"
#   set the ko label to "카르르 아우구스트 람사이"
Q6371586	Lko	"카르르 아우구스트 람사이"
#   Q130772654 Hedvig Christina Creutz: set the ja label to "ヘドヴィグ・クリスティーナ・クレウトズ"
Q130772654	Lja	"ヘドヴィグ・クリスティーナ・クレウトズ"
#   set the zh label to "海德维格·克里斯蒂娜·克雷乌特兹"
Q130772654	Lzh	"海德维格·克里斯蒂娜·克雷乌特兹"

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the mul label to "NN"
LAST	Lmul	"NN"
#   set the ca label to "fill de Norman Charles Tunheim"
LAST	Lca	"fill de Norman Charles Tunheim"
#   set the da label to "søn af Norman Charles Tunheim"
LAST	Lda	"søn af Norman Charles Tunheim"
#   set the de label to "Sohn von Norman Charles Tunheim"
LAST	Lde	"Sohn von Norman Charles Tunheim"
#   set the en label to "son of Norman Charles Tunheim"
LAST	Len	"son of Norman Charles Tunheim"
#   set the es label to "hijo de Norman Charles Tunheim"
LAST	Les	"hijo de Norman Charles Tunheim"
#   set the fr label to "fils de Norman Charles Tunheim"
LAST	Lfr	"fils de Norman Charles Tunheim"
#   set the it label to "figlio di Norman Charles Tunheim"
LAST	Lit	"figlio di Norman Charles Tunheim"
#   set the ja label to "ノーマン・チャールズ・トゥンヘイムの息子"
LAST	Lja	"ノーマン・チャールズ・トゥンヘイムの息子"
#   set the ko label to "노르만 차르레스 툰헤임의 아들"
LAST	Lko	"노르만 차르레스 툰헤임의 아들"
#   set the nb label to "sønn av Norman Charles Tunheim"
LAST	Lnb	"sønn av Norman Charles Tunheim"
#   set the nl label to "zoon van Norman Charles Tunheim"
LAST	Lnl	"zoon van Norman Charles Tunheim"
#   set the pt label to "filho de Norman Charles Tunheim"
LAST	Lpt	"filho de Norman Charles Tunheim"
#   set the sv label to "son till Norman Charles Tunheim"
LAST	Lsv	"son till Norman Charles Tunheim"
#   set the zh label to "诺曼·查尔斯·通海姆之子"
LAST	Lzh	"诺曼·查尔斯·通海姆之子"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000009735783838
LAST	P2600	"6000000009735783838"
#   P22 father = Q141216498 Norman Charles Tunheim
LAST	P22	Q141216498	S2600	"6000000009735783838"
#   Q141216498 Norman Charles Tunheim: P40 child = the item just created
Q141216498	P40	LAST	S2600	"6000000009735783838"

# create a new item
CREATE
#   the item just created: set the mul label to "NN"
LAST	Lmul	"NN"
#   set the ca label to "esposa de Norman Charles Tunheim"
LAST	Lca	"esposa de Norman Charles Tunheim"
#   set the da label to "hustru til Norman Charles Tunheim"
LAST	Lda	"hustru til Norman Charles Tunheim"
#   set the de label to "Ehefrau von Norman Charles Tunheim"
LAST	Lde	"Ehefrau von Norman Charles Tunheim"
#   set the en label to "wife of Norman Charles Tunheim"
LAST	Len	"wife of Norman Charles Tunheim"
#   set the es label to "esposa de Norman Charles Tunheim"
LAST	Les	"esposa de Norman Charles Tunheim"
#   set the fr label to "épouse de Norman Charles Tunheim"
LAST	Lfr	"épouse de Norman Charles Tunheim"
#   set the it label to "moglie di Norman Charles Tunheim"
LAST	Lit	"moglie di Norman Charles Tunheim"
#   set the ja label to "ノーマン・チャールズ・トゥンヘイムの妻"
LAST	Lja	"ノーマン・チャールズ・トゥンヘイムの妻"
#   set the ko label to "노르만 차르레스 툰헤임의 아내"
LAST	Lko	"노르만 차르레스 툰헤임의 아내"
#   set the nb label to "hustru til Norman Charles Tunheim"
LAST	Lnb	"hustru til Norman Charles Tunheim"
#   set the nl label to "echtgenote van Norman Charles Tunheim"
LAST	Lnl	"echtgenote van Norman Charles Tunheim"
#   set the pt label to "esposa de Norman Charles Tunheim"
LAST	Lpt	"esposa de Norman Charles Tunheim"
#   set the sv label to "maka till Norman Charles Tunheim"
LAST	Lsv	"maka till Norman Charles Tunheim"
#   set the zh label to "诺曼·查尔斯·通海姆之妻"
LAST	Lzh	"诺曼·查尔斯·通海姆之妻"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000009590833493
LAST	P2600	"6000000009590833493"
#   P26 spouse = Q141216498 Norman Charles Tunheim
LAST	P26	Q141216498	S2600	"6000000009590833493"
#   Q141216498 Norman Charles Tunheim: P26 spouse = the item just created
Q141216498	P26	LAST	S2600	"6000000009590833493"

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
#   set the ko label to "알프힐드 훌다 에르푸르트"
LAST	Lko	"알프힐드 훌다 에르푸르트"
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
#   set the en label to "Berta Kristine Kristiansdatter Rangen"
LAST	Len	"Berta Kristine Kristiansdatter Rangen"
#   set the mul label to "Berta Kristine Kristiansdatter Rangen"
LAST	Lmul	"Berta Kristine Kristiansdatter Rangen"
#   add a mul alias "Berta Kristine Kristiansdatter Sør-Reime"
LAST	Amul	"Berta Kristine Kristiansdatter Sør-Reime"
#   set the ja label to "ベルタ・クリスティン・クリスティアンスダッテル・ランゲン"
LAST	Lja	"ベルタ・クリスティン・クリスティアンスダッテル・ランゲン"
#   set the zh label to "贝尔塔·克丽丝汀·克里斯蒂安斯达特·兰根"
LAST	Lzh	"贝尔塔·克丽丝汀·克里斯蒂安斯达特·兰根"
#   set the ko label to "베르타 크리스티네 크리스티안스다테르 라엔"
LAST	Lko	"베르타 크리스티네 크리스티안스다테르 라엔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000029302608975 Berta Kristine Kristiansdatter Rangen, qualified P1810 subject named as Berta Kristine Kristiansdatter Sør-Reime
LAST	P2600	"6000000029302608975"	P1810	"Berta Kristine Kristiansdatter Sør-Reime"
#   P569 date of birth = +1886-02-07T00:00:00Z/11
LAST	P569	+1886-02-07T00:00:00Z/11	S2600	"6000000029302608975"
#   P570 date of death = +1936-12-01T00:00:00Z/11
LAST	P570	+1936-12-01T00:00:00Z/11	S2600	"6000000029302608975"
#   P22 father = Q141189076 Kristian Larsen Sør-Reime
LAST	P22	Q141189076	S2600	"6000000029302608975"
#   the item just created: P735 given name = Q4092653 Berta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q4092653	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16859157 Kristine, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q16859157	P1545	"2"	P3831	Q245025
#   P734 family name = Q141189041, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q141189041	P3831	Q2507958
#   add a mul alias "Berta Kristine Rangen"
LAST	Amul	"Berta Kristine Rangen"

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
#   set the en label to "Christina Charlotta von Köhler"
LAST	Len	"Christina Charlotta von Köhler"
#   set the mul label to "Christina Charlotta von Köhler"
LAST	Lmul	"Christina Charlotta von Köhler"
#   set the ja label to "クリスティーナ・カルロタ・ヴォン・ケーラー"
LAST	Lja	"クリスティーナ・カルロタ・ヴォン・ケーラー"
#   set the zh label to "克里斯蒂娜·卡尔洛塔·翁·科莱尔"
LAST	Lzh	"克里斯蒂娜·卡尔洛塔·翁·科莱尔"
#   set the ko label to "츠리스티나 차르로타 본 쾨흐레르"
LAST	Lko	"츠리스티나 차르로타 본 쾨흐레르"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000006127120926 Christina Charlotta von Köhler, qualified P1810 subject named as Christina Charlotta von Köhler
LAST	P2600	"6000000006127120926"	P1810	"Christina Charlotta von Köhler"
#   P569 date of birth = +1735-10-00T00:00:00Z/10
LAST	P569	+1735-10-00T00:00:00Z/10	S2600	"6000000006127120926"
#   P570 date of death = +1819-12-26T00:00:00Z/11
LAST	P570	+1819-12-26T00:00:00Z/11	S2600	"6000000006127120926"
#   P40 child = Q5580888 Erik Gustaf Boije af Gennäs
LAST	P40	Q5580888	S2600	"6000000006127120926"
#   P40 child = Q141219062 Hedvig Ulrika Boije af Gennäs
LAST	P40	Q141219062	S2600	"6000000006127120926"
#   the item just created: P735 given name = Q1083457 Christina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q1083457	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1067071	P1545	"2"	P3831	Q245025

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
#   set the en label to "Helena Maria Linnerhielm ogift"
LAST	Len	"Helena Maria Linnerhielm ogift"
#   set the mul label to "Helena Maria Linnerhielm ogift"
LAST	Lmul	"Helena Maria Linnerhielm ogift"
#   set the ja label to "ヘレナ・マリア・リネルヒエルム・オギフト"
LAST	Lja	"ヘレナ・マリア・リネルヒエルム・オギフト"
#   set the zh label to "海伦娜·玛丽亚·利内尔希埃尔姆·奥吉夫特"
LAST	Lzh	"海伦娜·玛丽亚·利内尔希埃尔姆·奥吉夫特"
#   set the ko label to "헤레나 마리아 린네르히엘므 오기프트"
LAST	Lko	"헤레나 마리아 린네르히엘므 오기프트"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000175545619828 Helena Maria Linnerhielm ogift, qualified P1810 subject named as Helena Maria Linnerhielm ogift
LAST	P2600	"6000000175545619828"	P1810	"Helena Maria Linnerhielm ogift"
#   P569 date of birth = +1793-10-21T00:00:00Z/11
LAST	P569	+1793-10-21T00:00:00Z/11	S2600	"6000000175545619828"
#   P570 date of death = +1867-06-15T00:00:00Z/11
LAST	P570	+1867-06-15T00:00:00Z/11	S2600	"6000000175545619828"
#   P22 father = Q5959480 Jonas Carl Linnerhielm
LAST	P22	Q5959480	S2600	"6000000175545619828"
#   P25 mother = Q4945900 Helena Maria Ehrenstråhle
LAST	P25	Q4945900	S2600	"6000000175545619828"
#   Q5959480 Jonas Carl Linnerhielm: P40 child = the item just created
Q5959480	P40	LAST	S2600	"6000000175545619828"
#   Q4945900 Helena Maria Ehrenstråhle: P40 child = the item just created
Q4945900	P40	LAST	S2600	"6000000175545619828"
#   the item just created: P735 given name = Q1035239 Helena, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q1035239	P1545	"1"	P7452	Q3409033
#   P735 given name = Q325872 Maria, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q325872	P1545	"2"	P3831	Q245025
#   add a mul alias "Lene-Marie Linnerhielm"
LAST	Amul	"Lene-Marie Linnerhielm"
#   add a mul alias "Helena Maria Linnerhielm"
LAST	Amul	"Helena Maria Linnerhielm"

# create a new item
CREATE
#   set the en label to "Ingeborg Pedersdatter Vestly"
LAST	Len	"Ingeborg Pedersdatter Vestly"
#   set the mul label to "Ingeborg Pedersdatter Vestly"
LAST	Lmul	"Ingeborg Pedersdatter Vestly"
#   add a mul alias "Ingeborg Pedersdatter Folkvår"
LAST	Amul	"Ingeborg Pedersdatter Folkvår"
#   set the ja label to "インゲボルグ・ペーデシュダッテル・ヴェストリ"
LAST	Lja	"インゲボルグ・ペーデシュダッテル・ヴェストリ"
#   set the zh label to "英格堡·佩德斯达特·韦斯特利"
LAST	Lzh	"英格堡·佩德斯达特·韦斯特利"
#   set the ko label to "이에보르그 페데르스다테르 베스트리"
LAST	Lko	"이에보르그 페데르스다테르 베스트리"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000025170379012 Ingeborg Pedersdatter Vestly, qualified P1810 subject named as Ingeborg Pedersdatter Folkvår
LAST	P2600	"6000000025170379012"	P1810	"Ingeborg Pedersdatter Folkvår"
#   P569 date of birth = +1755-00-00T00:00:00Z/9
LAST	P569	+1755-00-00T00:00:00Z/9	S2600	"6000000025170379012"
#   P570 date of death = +1848-02-06T00:00:00Z/11
LAST	P570	+1848-02-06T00:00:00Z/11	S2600	"6000000025170379012"
#   P40 child = Q141242412 Peder Paulsen Borsok
LAST	P40	Q141242412	S2600	"6000000025170379012"
#   Q141242412 Peder Paulsen Borsok: P25 mother = the item just created
Q141242412	P25	LAST	S2600	"6000000025170379012"
#   the item just created: P735 given name = Q656590 Ingeborg
LAST	P735	Q656590
#   P734 family name = Q40000023 Vestly, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q40000023	P3831	Q28418670
#   add a mul alias "Ingeborg Persdatter Folkvår Vestly"
LAST	Amul	"Ingeborg Persdatter Folkvår Vestly"
#   add a mul alias "Ingeborg Vestly"
LAST	Amul	"Ingeborg Vestly"

# create a new item
CREATE
#   set the en label to "Johan Gustaf Boije af Gennäs"
LAST	Len	"Johan Gustaf Boije af Gennäs"
#   set the mul label to "Johan Gustaf Boije af Gennäs"
LAST	Lmul	"Johan Gustaf Boije af Gennäs"
#   set the ja label to "ヨハン・グスタフ・ボイイェ・アフ・ゲネス"
LAST	Lja	"ヨハン・グスタフ・ボイイェ・アフ・ゲネス"
#   set the zh label to "约翰·古斯塔夫·博伊耶·阿夫·盖内斯"
LAST	Lzh	"约翰·古斯塔夫·博伊耶·阿夫·盖内斯"
#   set the ko label to "조한 구스타프 보이제 아프 겐네스"
LAST	Lko	"조한 구스타프 보이제 아프 겐네스"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000006127120919 Johan Gustaf Boije af Gennäs, qualified P1810 subject named as Johan Gustaf Boije af Gennäs
LAST	P2600	"6000000006127120919"	P1810	"Johan Gustaf Boije af Gennäs"
#   P569 date of birth = +1723-01-28T00:00:00Z/11
LAST	P569	+1723-01-28T00:00:00Z/11	S2600	"6000000006127120919"
#   P570 date of death = +1785-01-26T00:00:00Z/11
LAST	P570	+1785-01-26T00:00:00Z/11	S2600	"6000000006127120919"
#   P40 child = Q5580888 Erik Gustaf Boije af Gennäs
LAST	P40	Q5580888	S2600	"6000000006127120919"
#   P40 child = Q141219062 Hedvig Ulrika Boije af Gennäs
LAST	P40	Q141219062	S2600	"6000000006127120919"
#   the item just created: P735 given name = Q10989273 Johan, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q10989273	P1545	"1"	P7452	Q3409033
#   P735 given name = Q15646212 Gustaf, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q15646212	P1545	"2"	P3831	Q245025
#   P734 family name = Q28149669 Boije
LAST	P734	Q28149669
#   P734 family name = Q141223490
LAST	P734	Q141223490

# create a new item
CREATE
#   set the en label to "Knut Olson Garborg"
LAST	Len	"Knut Olson Garborg"
#   set the mul label to "Knut Olson Garborg"
LAST	Lmul	"Knut Olson Garborg"
#   set the ja label to "クヌート・オルソン・ガルボルグ"
LAST	Lja	"クヌート・オルソン・ガルボルグ"
#   set the zh label to "克努特·奥尔森·加尔博格"
LAST	Lzh	"克努特·奥尔森·加尔博格"
#   set the ko label to "크누트 올손 가르보르그"
LAST	Lko	"크누트 올손 가르보르그"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000007612151312 Knut Olson Garborg, qualified P1810 subject named as Knut Olson Garborg
LAST	P2600	"6000000007612151312"	P1810	"Knut Olson Garborg"
#   P569 date of birth = +1623-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P569	+1623-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"6000000007612151312"
#   P570 date of death = +1691-00-00T00:00:00Z/9
LAST	P570	+1691-00-00T00:00:00Z/9	S2600	"6000000007612151312"
#   P40 child = Q141219227 Gitlaug Knutsdatter Garborg
LAST	P40	Q141219227	S2600	"6000000007612151312"
#   Q141219227 Gitlaug Knutsdatter Garborg: P22 father = the item just created
Q141219227	P22	LAST	S2600	"6000000007612151312"
#   the item just created: P735 given name = Q943881 Knut
LAST	P735	Q943881
#   P734 family name = Q30250555 Garborg
LAST	P734	Q30250555

# create a new item
CREATE
#   set the en label to "Marit Hansdatter Reiestad"
LAST	Len	"Marit Hansdatter Reiestad"
#   set the mul label to "Marit Hansdatter Reiestad"
LAST	Lmul	"Marit Hansdatter Reiestad"
#   add a mul alias "Marit Hansdatter Hansdatter"
LAST	Amul	"Marit Hansdatter Hansdatter"
#   set the ja label to "マリット・ハンスダッテル・レイエスタド"
LAST	Lja	"マリット・ハンスダッテル・レイエスタド"
#   set the zh label to "马里特·汉斯达特·雷伊埃斯塔德"
LAST	Lzh	"马里特·汉斯达特·雷伊埃斯塔德"
#   set the ko label to "마리트 한스다테르 레이에스타드"
LAST	Lko	"마리트 한스다테르 레이에스타드"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000035349796879 Marit Hansdatter Reiestad, qualified P1810 subject named as Marit Hansdatter Hansdatter
LAST	P2600	"6000000035349796879"	P1810	"Marit Hansdatter Hansdatter"
#   P569 date of birth = +1703-00-00T00:00:00Z/9
LAST	P569	+1703-00-00T00:00:00Z/9	S2600	"6000000035349796879"
#   P22 father = Q141216381 Hans Rasmussen Låge-Håland
LAST	P22	Q141216381	S2600	"6000000035349796879"
#   P25 mother = Q141216383 Ingeborg Eriksdatter Bjorland
LAST	P25	Q141216383	S2600	"6000000035349796879"
#   Q141216381 Hans Rasmussen Låge-Håland: P40 child = the item just created
Q141216381	P40	LAST	S2600	"6000000035349796879"
#   Q141216383 Ingeborg Eriksdatter Bjorland: P40 child = the item just created
Q141216383	P40	LAST	S2600	"6000000035349796879"
#   the item just created: P735 given name = Q1566153 Marit
LAST	P735	Q1566153
#   P5056 patronym or matronym = Q141223482, qualified P144 based on Q141216381 Hans Rasmussen Låge-Håland
LAST	P5056	Q141223482	P144	Q141216381
#   add a mul alias "Marta Reiestad"
LAST	Amul	"Marta Reiestad"
#   add a mul alias "Marit Reiestad"
LAST	Amul	"Marit Reiestad"

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
#   set the fr label to "mère de Orm Ånonsen"
LAST	Lfr	"mère de Orm Ånonsen"
#   set the it label to "madre di Orm Ånonsen"
LAST	Lit	"madre di Orm Ånonsen"
#   set the ja label to "オルム・オーノンセンの母"
LAST	Lja	"オルム・オーノンセンの母"
#   set the ko label to "오르므 오논센의 어머니"
LAST	Lko	"오르므 오논센의 어머니"
#   set the nb label to "mor til Orm Ånonsen"
LAST	Lnb	"mor til Orm Ånonsen"
#   set the nl label to "moeder van Orm Ånonsen"
LAST	Lnl	"moeder van Orm Ånonsen"
#   set the pt label to "mãe de Orm Ånonsen"
LAST	Lpt	"mãe de Orm Ånonsen"
#   set the sv label to "mor till Orm Ånonsen"
LAST	Lsv	"mor till Orm Ånonsen"
#   set the zh label to "奥尔姆·奥农森之母"
LAST	Lzh	"奥尔姆·奥农森之母"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000001770277407 NN
LAST	P2600	"6000000001770277407"
#   P569 date of birth = +1487-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P569	+1487-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"6000000001770277407"
#   P40 child = Q141216499 Orm Ånonsen
LAST	P40	Q141216499	S2600	"6000000001770277407"
#   Q141216499 Orm Ånonsen: P25 mother = the item just created
Q141216499	P25	LAST	S2600	"6000000001770277407"

# create a new item
CREATE
#   the item just created: set the en label to "Nils Sundius"
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
#   set the en label to "Ola Olson Lende"
LAST	Len	"Ola Olson Lende"
#   set the mul label to "Ola Olson Lende"
LAST	Lmul	"Ola Olson Lende"
#   set the ja label to "オーラ・オルソン・レンデ"
LAST	Lja	"オーラ・オルソン・レンデ"
#   set the zh label to "奥拉·奥尔森·伦德"
LAST	Lzh	"奥拉·奥尔森·伦德"
#   set the ko label to "오라 올손 렌데"
LAST	Lko	"오라 올손 렌데"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000021134033255 Ola Olson Lende, qualified P1810 subject named as Ola Olson Lende
LAST	P2600	"6000000021134033255"	P1810	"Ola Olson Lende"
#   P569 date of birth = +1845-08-23T00:00:00Z/11
LAST	P569	+1845-08-23T00:00:00Z/11	S2600	"6000000021134033255"
#   P22 father = Q141249737 Ole Thoreson Toresen Lende
LAST	P22	Q141249737	S2600	"6000000021134033255"
#   P25 mother = Q141249721 Asseline Svensdatter Lende
LAST	P25	Q141249721	S2600	"6000000021134033255"
#   Q141249737 Ole Thoreson Toresen Lende: P40 child = the item just created
Q141249737	P40	LAST	S2600	"6000000021134033255"
#   Q141249721 Asseline Svensdatter Lende: P40 child = the item just created
Q141249721	P40	LAST	S2600	"6000000021134033255"
#   the item just created: P735 given name = Q96675523 Ola
LAST	P735	Q96675523
#   P734 family name = Q30083619
LAST	P734	Q30083619

# create a new item
CREATE
#   set the en label to "Olof Carlberg"
LAST	Len	"Olof Carlberg"
#   set the mul label to "Olof Carlberg"
LAST	Lmul	"Olof Carlberg"
#   set the ja label to "オロフ・カルルベルグ"
LAST	Lja	"オロフ・カルルベルグ"
#   set the zh label to "奥洛夫·卡尔尔贝尔格"
LAST	Lzh	"奥洛夫·卡尔尔贝尔格"
#   set the ko label to "오로프 카르르베르그"
LAST	Lko	"오로프 카르르베르그"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003133682482 Olof Carlberg, qualified P1810 subject named as Olof Carlberg
LAST	P2600	"6000000003133682482"	P1810	"Olof Carlberg"
#   P569 date of birth = +1658-00-00T00:00:00Z/9
LAST	P569	+1658-00-00T00:00:00Z/9	S2600	"6000000003133682482"
#   P22 father = Q141249728 Johan Börgesson Carlberg
LAST	P22	Q141249728	S2600	"6000000003133682482"
#   P25 mother = Q141249729 Kristina Olofsdotter Spaak
LAST	P25	Q141249729	S2600	"6000000003133682482"
#   Q141249728 Johan Börgesson Carlberg: P40 child = the item just created
Q141249728	P40	LAST	S2600	"6000000003133682482"
#   Q141249729 Kristina Olofsdotter Spaak: P40 child = the item just created
Q141249729	P40	LAST	S2600	"6000000003133682482"
#   the item just created: P735 given name = Q18089653 Olof
LAST	P735	Q18089653

# create a new item
CREATE
#   set the en label to "Pål Jørgenson Vestly"
LAST	Len	"Pål Jørgenson Vestly"
#   set the mul label to "Pål Jørgenson Vestly"
LAST	Lmul	"Pål Jørgenson Vestly"
#   set the ja label to "ポール・ヨルゲンソン・ヴェストリ"
LAST	Lja	"ポール・ヨルゲンソン・ヴェストリ"
#   set the zh label to "波尔·约尔根松·韦斯特利"
LAST	Lzh	"波尔·约尔根松·韦斯特利"
#   set the ko label to "폴 죄르겐손 베스트리"
LAST	Lko	"폴 죄르겐손 베스트리"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000025170500054 Pål Jørgenson Vestly, qualified P1810 subject named as Pål Jørgenson Vestly
LAST	P2600	"6000000025170500054"	P1810	"Pål Jørgenson Vestly"
#   P569 date of birth = +1742-00-00T00:00:00Z/9
LAST	P569	+1742-00-00T00:00:00Z/9	S2600	"6000000025170500054"
#   P570 date of death = +1793-11-11T00:00:00Z/11
LAST	P570	+1793-11-11T00:00:00Z/11	S2600	"6000000025170500054"
#   P40 child = Q141242412 Peder Paulsen Borsok
LAST	P40	Q141242412	S2600	"6000000025170500054"
#   Q141242412 Peder Paulsen Borsok: P22 father = the item just created
Q141242412	P22	LAST	S2600	"6000000025170500054"

# create a new item
CREATE
#   the item just created: set the en label to "Torger Olsen Ålgård"
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
#   the item just created: set the en label to "Tormod Pederson Kalsheim"
LAST	Len	"Tormod Pederson Kalsheim"
#   set the mul label to "Tormod Pederson Kalsheim"
LAST	Lmul	"Tormod Pederson Kalsheim"
#   set the ja label to "トルモド・ペデルソン・カルスヘイム"
LAST	Lja	"トルモド・ペデルソン・カルスヘイム"
#   set the zh label to "托尔莫德·佩德尔松·卡尔斯赫伊姆"
LAST	Lzh	"托尔莫德·佩德尔松·卡尔斯赫伊姆"
#   set the ko label to "토르모드 페데르손 칼세임"
LAST	Lko	"토르모드 페데르손 칼세임"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005607362456 Tormod Pederson Kalsheim, qualified P1810 subject named as Tormod Pederson Kalsheim
LAST	P2600	"6000000005607362456"	P1810	"Tormod Pederson Kalsheim"
#   P569 date of birth = +1605-00-00T00:00:00Z/9
LAST	P569	+1605-00-00T00:00:00Z/9	S2600	"6000000005607362456"
#   P570 date of death = +1650-00-00T00:00:00Z/9
LAST	P570	+1650-00-00T00:00:00Z/9	S2600	"6000000005607362456"
#   P22 father = Q141206080 Peder Tormodsen Foss
LAST	P22	Q141206080	S2600	"6000000005607362456"
#   P25 mother = Q141206061 Cecilie Olsdatter Håland
LAST	P25	Q141206061	S2600	"6000000005607362456"
#   Q141206080 Peder Tormodsen Foss: P40 child = the item just created
Q141206080	P40	LAST	S2600	"6000000005607362456"
#   Q141206061 Cecilie Olsdatter Håland: P40 child = the item just created
Q141206061	P40	LAST	S2600	"6000000005607362456"

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

# create a new item
CREATE
#   set the en label to "Åsa Børildsdatter Garborg"
LAST	Len	"Åsa Børildsdatter Garborg"
#   set the mul label to "Åsa Børildsdatter Garborg"
LAST	Lmul	"Åsa Børildsdatter Garborg"
#   add a mul alias "Åsa Børildsdatter Børildsdatter"
LAST	Amul	"Åsa Børildsdatter Børildsdatter"
#   set the ja label to "オーサ・ボリルドスダッテル・ガルボルグ"
LAST	Lja	"オーサ・ボリルドスダッテル・ガルボルグ"
#   set the zh label to "奥萨·博里尔德斯达特·加尔博格"
LAST	Lzh	"奥萨·博里尔德斯达特·加尔博格"
#   set the ko label to "오사 뵈릴드스다테르 가르보르그"
LAST	Lko	"오사 뵈릴드스다테르 가르보르그"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005609460067 Åsa Børildsdatter Garborg, qualified P1810 subject named as Åsa Børildsdatter Børildsdatter
LAST	P2600	"6000000005609460067"	P1810	"Åsa Børildsdatter Børildsdatter"
#   P569 date of birth = +1621-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P569	+1621-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"6000000005609460067"
#   P40 child = Q141219227 Gitlaug Knutsdatter Garborg
LAST	P40	Q141219227	S2600	"6000000005609460067"
#   Q141219227 Gitlaug Knutsdatter Garborg: P25 mother = the item just created
Q141219227	P25	LAST	S2600	"6000000005609460067"
#   the item just created: P735 given name = Q18571895 Åsa
LAST	P735	Q18571895
#   P734 family name = Q30250555 Garborg, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q30250555	P3831	Q28418670
#   add a mul alias "Åsa Garborg"
LAST	Amul	"Åsa Garborg"
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

