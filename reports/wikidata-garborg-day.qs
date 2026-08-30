# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   942 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   Q543935 Count Gustaf Mauritz Armfelt: set the mul label to "Gustaf Mauritz Armfelt"
Q543935	Lmul	"Gustaf Mauritz Armfelt"
#   add a mul alias "Count Gustaf Mauritz Armfelt"
Q543935	Amul	"Count Gustaf Mauritz Armfelt"
#   set the zh label to "古斯塔夫·马乌里特兹·阿尔姆费尔特"
Q543935	Lzh	"古斯塔夫·马乌里特兹·阿尔姆费尔特"
#   Q6079648 Nils Eberhardsson Rosenblad: set the mul label to "Nils Rosenblad"
Q6079648	Lmul	"Nils Rosenblad"
#   add a mul alias "Nils Eberhardsson Rosenblad"
Q6079648	Amul	"Nils Eberhardsson Rosenblad"
#   Q2965864 Christina Charlotta Cederström: set the mul label to "Christina Charlotta Cederström"
Q2965864	Lmul	"Christina Charlotta Cederström"
#   set the ja label to "クリスティーナ・カルロタ・セーデルストレム"
Q2965864	Lja	"クリスティーナ・カルロタ・セーデルストレム"
#   set the zh label to "克里斯蒂娜·卡尔洛塔·塞德尔斯特罗姆"
Q2965864	Lzh	"克里斯蒂娜·卡尔洛塔·塞德尔斯特罗姆"
#   Q6001555 Carl Claes Mörner af Morlanda: set the mul label to "Carl Claes Mörner"
Q6001555	Lmul	"Carl Claes Mörner"
#   add a mul alias "Carl Claes Mörner af Morlanda"
Q6001555	Amul	"Carl Claes Mörner af Morlanda"
#   set the ja label to "カール・クレス・モルネル"
Q6001555	Lja	"カール・クレス・モルネル"
#   set the zh label to "卡尔·克拉斯·莫尔内尔"
Q6001555	Lzh	"卡尔·克拉斯·莫尔内尔"
#   Q6001608 Hampus Elof Mörner af Morlanda: set the mul label to "Hampus Mörner"
Q6001608	Lmul	"Hampus Mörner"
#   add a mul alias "Hampus Elof Mörner"
Q6001608	Amul	"Hampus Elof Mörner"
#   set the ja label to "ハムプス・モルネル"
Q6001608	Lja	"ハムプス・モルネル"

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Anders Rasmusson Lea"
LAST	Len	"Anders Rasmusson Lea"
#   set the mul label to "Anders Rasmusson Lea"
LAST	Lmul	"Anders Rasmusson Lea"
#   set the ja label to "アンデルス・ラスムソン・リー"
LAST	Lja	"アンデルス・ラスムソン・リー"
#   set the zh label to "安德斯·拉斯穆松·莉亚"
LAST	Lzh	"安德斯·拉斯穆松·莉亚"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005607296161 Anders Rasmusson Lea, qualified P1810 subject named as Anders Rasmusson Lea
LAST	P2600	"6000000005607296161"	P1810	"Anders Rasmusson Lea"
#   P569 date of birth = +1788-00-00T00:00:00Z/9
LAST	P569	+1788-00-00T00:00:00Z/9	S2600	"6000000005607296161"
#   P570 date of death = +1864-03-21T00:00:00Z/11
LAST	P570	+1864-03-21T00:00:00Z/11	S2600	"6000000005607296161"
#   P40 child = Q141223744 Rasmus Wibye Andersson Lea
LAST	P40	Q141223744	S2600	"6000000005607296161"
#   Q141223744 Rasmus Wibye Andersson Lea: P22 father = the item just created
Q141223744	P22	LAST	S2600	"6000000005607296161"

# create a new item
CREATE
#   the item just created: set the en label to "Anna Margareta von Walcker"
LAST	Len	"Anna Margareta von Walcker"
#   set the mul label to "Anna Margareta von Walcker"
LAST	Lmul	"Anna Margareta von Walcker"
#   set the ja label to "アンナ・マルガレータ・ヴォン・ヴァルケル"
LAST	Lja	"アンナ・マルガレータ・ヴォン・ヴァルケル"
#   set the zh label to "安娜·瑪格麗塔·翁·瓦尔凯尔"
LAST	Lzh	"安娜·瑪格麗塔·翁·瓦尔凯尔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000009813973540 Anna Margareta von Walcker, qualified P1810 subject named as Anna Margareta von Walcker
LAST	P2600	"6000000009813973540"	P1810	"Anna Margareta von Walcker"
#   P569 date of birth = +1694-00-00T00:00:00Z/9
LAST	P569	+1694-00-00T00:00:00Z/9	S2600	"6000000009813973540"
#   P570 date of death = +1763-07-05T00:00:00Z/11
LAST	P570	+1763-07-05T00:00:00Z/11	S2600	"6000000009813973540"
#   P22 father = Q6229400 Elias von Walcker
LAST	P22	Q6229400	S2600	"6000000009813973540"
#   Q6229400 Elias von Walcker: P40 child = the item just created
Q6229400	P40	LAST	S2600	"6000000009813973540"
#   the item just created: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P735 given name = Q8274988 Margareta, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q8274988	P1545	"2"	P3831	Q245025
#   add a mul alias "Wolker von Walcker"
LAST	Amul	"Wolker von Walcker"

# create a new item
CREATE
#   set the en label to "Carl Andersson"
LAST	Len	"Carl Andersson"
#   set the mul label to "Carl Andersson"
LAST	Lmul	"Carl Andersson"
#   set the ja label to "カール・アンデション"
LAST	Lja	"カール・アンデション"
#   set the zh label to "卡尔·安德松"
LAST	Lzh	"卡尔·安德松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000178279141871 Carl Andersson, qualified P1810 subject named as Carl Andersson
LAST	P2600	"6000000178279141871"	P1810	"Carl Andersson"
#   P40 child = Q141223907 Elly Olivia Frisk
LAST	P40	Q141223907	S2600	"6000000178279141871"
#   Q141223907 Elly Olivia Frisk: P22 father = the item just created
Q141223907	P22	LAST	S2600	"6000000178279141871"
#   the item just created: P735 given name = Q2529610 Carl
LAST	P735	Q2529610
#   P734 family name = Q2817217 Andersson
LAST	P734	Q2817217

# create a new item
CREATE
#   set the en label to "Erik Guttormsson"
LAST	Len	"Erik Guttormsson"
#   set the mul label to "Erik Guttormsson"
LAST	Lmul	"Erik Guttormsson"
#   set the ja label to "エリック・グトルムソン"
LAST	Lja	"エリック・グトルムソン"
#   set the zh label to "埃里克·古托尔姆松"
LAST	Lzh	"埃里克·古托尔姆松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000007328872457 Erik Guttormsson, qualified P1810 subject named as Erik Guttormsson
LAST	P2600	"6000000007328872457"	P1810	"Erik Guttormsson"
#   P569 date of birth = +1222-00-00T00:00:00Z/9
LAST	P569	+1222-00-00T00:00:00Z/9	S2600	"6000000007328872457"
#   P570 date of death = +1270-00-00T00:00:00Z/9
LAST	P570	+1270-00-00T00:00:00Z/9	S2600	"6000000007328872457"
#   P22 father = Q141223732 Guttorm Guttormsson
LAST	P22	Q141223732	S2600	"6000000007328872457"
#   Q141223732 Guttorm Guttormsson: P40 child = the item just created
Q141223732	P40	LAST	S2600	"6000000007328872457"

# create a new item
CREATE
#   the item just created: set the en label to "Fru Tore"
LAST	Len	"Fru Tore"
#   set the mul label to "Fru Tore"
LAST	Lmul	"Fru Tore"
#   set the ja label to "フル・トーレ"
LAST	Lja	"フル・トーレ"
#   set the zh label to "夫鲁·托雷"
LAST	Lzh	"夫鲁·托雷"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000150599235831 Fru Tore, qualified P1810 subject named as Fru Tore
LAST	P2600	"6000000150599235831"	P1810	"Fru Tore"
#   P569 date of birth = +1663-00-00T00:00:00Z/9
LAST	P569	+1663-00-00T00:00:00Z/9	S2600	"6000000150599235831"
#   P40 child = Q141216507 Torborg Toresdatter Norheim
LAST	P40	Q141216507	S2600	"6000000150599235831"
#   Q141216507 Torborg Toresdatter Norheim: P25 mother = the item just created
Q141216507	P25	LAST	S2600	"6000000150599235831"

# create a new item
CREATE
#   the item just created: set the en label to "Ingeborg Simonsdatter Ytre Lima"
LAST	Len	"Ingeborg Simonsdatter Ytre Lima"
#   set the mul label to "Ingeborg Simonsdatter Ytre Lima"
LAST	Lmul	"Ingeborg Simonsdatter Ytre Lima"
#   add a mul alias "Ingeborg Simonsdatter Ravndal"
LAST	Amul	"Ingeborg Simonsdatter Ravndal"
#   set the ja label to "インゲボルグ・シモンスダッテル・イトレ・リマ"
LAST	Lja	"インゲボルグ・シモンスダッテル・イトレ・リマ"
#   set the zh label to "英格堡·西蒙斯达特·伊特雷·利马"
LAST	Lzh	"英格堡·西蒙斯达特·伊特雷·利马"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000002836363103 Ingeborg Simonsdatter Ytre Lima, qualified P1810 subject named as Ingeborg Simonsdatter Ravndal
LAST	P2600	"6000000002836363103"	P1810	"Ingeborg Simonsdatter Ravndal"
#   P569 date of birth = +1677-00-00T00:00:00Z/9
LAST	P569	+1677-00-00T00:00:00Z/9	S2600	"6000000002836363103"
#   P570 date of death = +1738-00-00T00:00:00Z/9
LAST	P570	+1738-00-00T00:00:00Z/9	S2600	"6000000002836363103"
#   P40 child = Q141223933 Ola Svenson Ytre Lima
LAST	P40	Q141223933	S2600	"6000000002836363103"
#   Q141223933 Ola Svenson Ytre Lima: P25 mother = the item just created
Q141223933	P25	LAST	S2600	"6000000002836363103"
#   the item just created: P735 given name = Q656590 Ingeborg
LAST	P735	Q656590
#   P734 family name = Q30503907, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q30503907	P3831	Q2507958
#   P734 family name = Q30340328, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q30340328	P3831	Q28418670
#   P734 family name = Q11255517 Lima, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q11255517	P3831	Q28418670
#   add a mul alias "Ingeborg Ytre Lima"
LAST	Amul	"Ingeborg Ytre Lima"

# create a new item
CREATE
#   set the en label to "Jacob Knutson Skiftun"
LAST	Len	"Jacob Knutson Skiftun"
#   set the mul label to "Jacob Knutson Skiftun"
LAST	Lmul	"Jacob Knutson Skiftun"
#   add a mul alias "Jacob Knutson Koll"
LAST	Amul	"Jacob Knutson Koll"
#   set the ja label to "ジェイコブ・クヌートソン・スキフトン"
LAST	Lja	"ジェイコブ・クヌートソン・スキフトン"
#   set the zh label to "雅各布·克努特松·斯基夫通"
LAST	Lzh	"雅各布·克努特松·斯基夫通"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000177945982827 Jacob Knutson Skiftun, qualified P1810 subject named as Jacob Knutson Koll
LAST	P2600	"6000000177945982827"	P1810	"Jacob Knutson Koll"
#   P40 child = Q141216494 N.N. Jacobsdtr. Koll
LAST	P40	Q141216494	S2600	"6000000177945982827"
#   Q141216494 N.N. Jacobsdtr. Koll: P22 father = the item just created
Q141216494	P22	LAST	S2600	"6000000177945982827"
#   the item just created: P735 given name = Q25999604 Jacob
LAST	P735	Q25999604
#   P734 family name = Q21510541, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q21510541	P3831	Q2507958
#   add a mul alias "Jacob Skiftun"
LAST	Amul	"Jacob Skiftun"

# create a new item
CREATE
#   set the en label to "Jakob Chydenius"
LAST	Len	"Jakob Chydenius"
#   set the mul label to "Jakob Chydenius"
LAST	Lmul	"Jakob Chydenius"
#   set the ja label to "ヤーコプ・キデニウス"
LAST	Lja	"ヤーコプ・キデニウス"
#   set the zh label to "雅各布·基德尼乌斯"
LAST	Lzh	"雅各布·基德尼乌斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000000583631058 Jakob Chydenius, qualified P1810 subject named as Jakob Chydenius
LAST	P2600	"6000000000583631058"	P1810	"Jakob Chydenius"
#   P569 date of birth = +1732-02-26T00:00:00Z/11
LAST	P569	+1732-02-26T00:00:00Z/11	S2600	"6000000000583631058"
#   P570 date of death = +1809-04-20T00:00:00Z/11
LAST	P570	+1809-04-20T00:00:00Z/11	S2600	"6000000000583631058"
#   P22 father = Q141224209 Jacob Chydenius
LAST	P22	Q141224209	S2600	"6000000000583631058"
#   P25 mother = Q141224012 Hedvig Chydenius
LAST	P25	Q141224012	S2600	"6000000000583631058"
#   Q141224209 Jacob Chydenius: P40 child = the item just created
Q141224209	P40	LAST	S2600	"6000000000583631058"
#   Q141224012 Hedvig Chydenius: P40 child = the item just created
Q141224012	P40	LAST	S2600	"6000000000583631058"

# create a new item
CREATE
#   the item just created: set the en label to "Jon Pedersen Trevland"
LAST	Len	"Jon Pedersen Trevland"
#   set the mul label to "Jon Pedersen Trevland"
LAST	Lmul	"Jon Pedersen Trevland"
#   set the ja label to "ジョン・ペデルセン・トレヴランド"
LAST	Lja	"ジョン・ペデルセン・トレヴランド"
#   set the zh label to "乔恩·佩德森·特雷夫兰德"
LAST	Lzh	"乔恩·佩德森·特雷夫兰德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000001770193504 Jon Pedersen Trevland, qualified P1810 subject named as Jon Pedersen Trevland
LAST	P2600	"6000000001770193504"	P1810	"Jon Pedersen Trevland"
#   P569 date of birth = +1613-00-00T00:00:00Z/9
LAST	P569	+1613-00-00T00:00:00Z/9	S2600	"6000000001770193504"
#   P570 date of death = +1697-00-00T00:00:00Z/9
LAST	P570	+1697-00-00T00:00:00Z/9	S2600	"6000000001770193504"
#   P22 father = Q141198831 Peder Larsen Mjølhus
LAST	P22	Q141198831	S2600	"6000000001770193504"
#   P25 mother = Q141205938 Ranveig Olsd Trevland
LAST	P25	Q141205938	S2600	"6000000001770193504"
#   Q141198831 Peder Larsen Mjølhus: P40 child = the item just created
Q141198831	P40	LAST	S2600	"6000000001770193504"
#   Q141205938 Ranveig Olsd Trevland: P40 child = the item just created
Q141205938	P40	LAST	S2600	"6000000001770193504"
#   the item just created: P735 given name = Q13501137 Jon
LAST	P735	Q13501137
#   P5056 patronym or matronym = Q130233025, qualified P144 based on Q141198831 Peder Larsen Mjølhus
LAST	P5056	Q130233025	P144	Q141198831
#   add a mul alias "Jon Tveita Trevland"
LAST	Amul	"Jon Tveita Trevland"
#   add a mul alias "Jon Trevland"
LAST	Amul	"Jon Trevland"

# create a new item
CREATE
#   set the en label to "Karolina Andrietta Ström"
LAST	Len	"Karolina Andrietta Ström"
#   set the mul label to "Karolina Andrietta Ström"
LAST	Lmul	"Karolina Andrietta Ström"
#   set the ja label to "カロリナ・アンドリエタ・ストローム"
LAST	Lja	"カロリナ・アンドリエタ・ストローム"
#   set the zh label to "卡罗利纳·安德里埃塔·斯特罗姆"
LAST	Lzh	"卡罗利纳·安德里埃塔·斯特罗姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000009494606557 Karolina Andrietta Ström, qualified P1810 subject named as Karolina Andrietta Ström
LAST	P2600	"6000000009494606557"	P1810	"Karolina Andrietta Ström"
#   P569 date of birth = +1808-07-02T00:00:00Z/11
LAST	P569	+1808-07-02T00:00:00Z/11	S2600	"6000000009494606557"
#   P570 date of death = +1843-02-22T00:00:00Z/11
LAST	P570	+1843-02-22T00:00:00Z/11	S2600	"6000000009494606557"
#   P26 spouse = Q6240337 Per Henrik Widmark RVO
LAST	P26	Q6240337	S2600	"6000000009494606557"
#   Q6240337 Per Henrik Widmark RVO: P26 spouse = the item just created
Q6240337	P26	LAST	S2600	"6000000009494606557"
#   the item just created: P735 given name = Q1734206 Karolina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q1734206	P1545	"1"	P7452	Q3409033

# create a new item
CREATE
#   set the en label to "Katarina Johansdotter Ståhlbom"
LAST	Len	"Katarina Johansdotter Ståhlbom"
#   set the mul label to "Katarina Johansdotter Ståhlbom"
LAST	Lmul	"Katarina Johansdotter Ståhlbom"
#   set the ja label to "カタリーナ・ヨハンスドッテル・ストールボム"
LAST	Lja	"カタリーナ・ヨハンスドッテル・ストールボム"
#   set the zh label to "卡塔里纳·约汉斯多特·斯托尔博姆"
LAST	Lzh	"卡塔里纳·约汉斯多特·斯托尔博姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000007367019257 Katarina Johansdotter Ståhlbom, qualified P1810 subject named as Katarina Johansdotter Ståhlbom
LAST	P2600	"6000000007367019257"	P1810	"Katarina Johansdotter Ståhlbom"
#   P569 date of birth = +1670-00-00T00:00:00Z/9
LAST	P569	+1670-00-00T00:00:00Z/9	S2600	"6000000007367019257"
#   P570 date of death = +1715-00-00T00:00:00Z/9
LAST	P570	+1715-00-00T00:00:00Z/9	S2600	"6000000007367019257"
#   P26 spouse = Q141224900 Samuel Samuelis Hornaeus
LAST	P26	Q141224900	S2600	"6000000007367019257"
#   P40 child = Q141224012 Hedvig Chydenius
LAST	P40	Q141224012	S2600	"6000000007367019257"
#   Q141224900 Samuel Samuelis Hornaeus: P26 spouse = the item just created
Q141224900	P26	LAST	S2600	"6000000007367019257"
#   Q141224012 Hedvig Chydenius: P25 mother = the item just created
Q141224012	P25	LAST	S2600	"6000000007367019257"

# create a new item
CREATE
#   the item just created: set the en label to "Kristina Eriksdotter Ångerman"
LAST	Len	"Kristina Eriksdotter Ångerman"
#   set the mul label to "Kristina Eriksdotter Ångerman"
LAST	Lmul	"Kristina Eriksdotter Ångerman"
#   set the ja label to "クリスティーナ・エリクスドッテル・オーンゲルマン"
LAST	Lja	"クリスティーナ・エリクスドッテル・オーンゲルマン"
#   set the zh label to "克里斯蒂娜·埃里克斯多塔·翁盖尔曼"
LAST	Lzh	"克里斯蒂娜·埃里克斯多塔·翁盖尔曼"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000038458498753 Kristina Eriksdotter Ångerman, qualified P1810 subject named as Kristina Eriksdotter Ångerman
LAST	P2600	"6000000038458498753"	P1810	"Kristina Eriksdotter Ångerman"
#   P570 date of death = +1692-05-07T00:00:00Z/11
LAST	P570	+1692-05-07T00:00:00Z/11	S2600	"6000000038458498753"
#   P40 child = Q5547967 Erik Alstrin
LAST	P40	Q5547967	S2600	"6000000038458498753"
#   Q5547967 Erik Alstrin: P25 mother = the item just created
Q5547967	P25	LAST	S2600	"6000000038458498753"
#   the item just created: P735 given name = Q19798802 Kristina
LAST	P735	Q19798802
#   P5056 patronym or matronym = Q130232912 Eriksdotter
LAST	P5056	Q130232912

# create a new item
CREATE
#   set the mul label to "Kristine"
LAST	Lmul	"Kristine"
#   set the ca label to "mare de Erik Guttormsson"
LAST	Lca	"mare de Erik Guttormsson"
#   set the da label to "mor til Erik Guttormsson"
LAST	Lda	"mor til Erik Guttormsson"
#   set the de label to "Mutter von Erik Guttormsson"
LAST	Lde	"Mutter von Erik Guttormsson"
#   set the en label to "mother of Erik Guttormsson"
LAST	Len	"mother of Erik Guttormsson"
#   set the es label to "madre de Erik Guttormsson"
LAST	Les	"madre de Erik Guttormsson"
#   set the it label to "madre di Erik Guttormsson"
LAST	Lit	"madre di Erik Guttormsson"
#   set the ja label to "エリック・グトルムソンの母"
LAST	Lja	"エリック・グトルムソンの母"
#   set the nb label to "mor til Erik Guttormsson"
LAST	Lnb	"mor til Erik Guttormsson"
#   set the nl label to "moeder van Erik Guttormsson"
LAST	Lnl	"moeder van Erik Guttormsson"
#   set the pt label to "mãe de Erik Guttormsson"
LAST	Lpt	"mãe de Erik Guttormsson"
#   set the sv label to "mor till Erik Guttormsson"
LAST	Lsv	"mor till Erik Guttormsson"
#   set the zh label to "埃里克·古托尔姆松之母"
LAST	Lzh	"埃里克·古托尔姆松之母"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000040760740831 Kristine NN
LAST	P2600	"6000000040760740831"
#   P569 date of birth = +1200-00-00T00:00:00Z/9
LAST	P569	+1200-00-00T00:00:00Z/9	S2600	"6000000040760740831"
#   P570 date of death = +1236-00-00T00:00:00Z/9
LAST	P570	+1236-00-00T00:00:00Z/9	S2600	"6000000040760740831"
#   P26 spouse = Q141223732 Guttorm Guttormsson
LAST	P26	Q141223732	S2600	"6000000040760740831"
#   Q141223732 Guttorm Guttormsson: P26 spouse = the item just created
Q141223732	P26	LAST	S2600	"6000000040760740831"

# create a new item
CREATE
#   the item just created: set the en label to "Laurentius Andreae Andreae Alstrinius"
LAST	Len	"Laurentius Andreae Andreae Alstrinius"
#   set the mul label to "Laurentius Andreae Andreae Alstrinius"
LAST	Lmul	"Laurentius Andreae Andreae Alstrinius"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000025011507008 Laurentius Andreae Andreae Alstrinius, qualified P1810 subject named as Laurentius Andreae Andreae Alstrinius
LAST	P2600	"6000000025011507008"	P1810	"Laurentius Andreae Andreae Alstrinius"
#   P569 date of birth = +1649-00-00T00:00:00Z/9
LAST	P569	+1649-00-00T00:00:00Z/9	S2600	"6000000025011507008"
#   P570 date of death = +1702-03-04T00:00:00Z/11
LAST	P570	+1702-03-04T00:00:00Z/11	S2600	"6000000025011507008"
#   P40 child = Q5547967 Erik Alstrin
LAST	P40	Q5547967	S2600	"6000000025011507008"
#   Q5547967 Erik Alstrin: P22 father = the item just created
Q5547967	P22	LAST	S2600	"6000000025011507008"
#   the item just created: P735 given name = Q15635267 Laurentius, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q15635267	P1545	"1"	P7452	Q3409033
#   add a mul alias "Lars Andersson Alstrinius"
LAST	Amul	"Lars Andersson Alstrinius"

# create a new item
CREATE
#   set the en label to "Louise Helmine Jenssen"
LAST	Len	"Louise Helmine Jenssen"
#   set the mul label to "Louise Helmine Jenssen"
LAST	Lmul	"Louise Helmine Jenssen"
#   set the ja label to "ルイーズ・ヘルミネ・イェンセン"
LAST	Lja	"ルイーズ・ヘルミネ・イェンセン"
#   set the zh label to "路易丝·赫尔米内·延森"
LAST	Lzh	"路易丝·赫尔米内·延森"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000014196858070 Louise Helmine Jenssen, qualified P1810 subject named as Louise Helmine Jenssen
LAST	P2600	"6000000014196858070"	P1810	"Louise Helmine Jenssen"
#   P569 date of birth = +1887-00-00T00:00:00Z/9
LAST	P569	+1887-00-00T00:00:00Z/9	S2600	"6000000014196858070"
#   P22 father = Q141223516 Hans Otto Kristian Jenssen
LAST	P22	Q141223516	S2600	"6000000014196858070"
#   P25 mother = Q141219307 Petrike Margrete Jenssen
LAST	P25	Q141219307	S2600	"6000000014196858070"
#   Q141223516 Hans Otto Kristian Jenssen: P40 child = the item just created
Q141223516	P40	LAST	S2600	"6000000014196858070"
#   Q141219307 Petrike Margrete Jenssen: P40 child = the item just created
Q141219307	P40	LAST	S2600	"6000000014196858070"
#   the item just created: P735 given name = Q3215140 Louise, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q3215140	P1545	"1"	P7452	Q3409033
#   P735 given name = Q99659344, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q99659344	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Marite Olufsdatter Håland"
LAST	Len	"Marite Olufsdatter Håland"
#   set the mul label to "Marite Olufsdatter Håland"
LAST	Lmul	"Marite Olufsdatter Håland"
#   set the ja label to "マリテ・オルフスダッテル・ホーランド"
LAST	Lja	"マリテ・オルフスダッテル・ホーランド"
#   set the zh label to "马里特·奥卢夫斯达特·霍兰"
LAST	Lzh	"马里特·奥卢夫斯达特·霍兰"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000007980352331 Marite Olufsdatter Håland, qualified P1810 subject named as Marite Olufsdatter Håland
LAST	P2600	"6000000007980352331"	P1810	"Marite Olufsdatter Håland"
#   P569 date of birth = +1595-00-00T00:00:00Z/9
LAST	P569	+1595-00-00T00:00:00Z/9	S2600	"6000000007980352331"
#   P22 father = Q141205930 Olav Knutson Randa Håland
LAST	P22	Q141205930	S2600	"6000000007980352331"
#   Q141205930 Olav Knutson Randa Håland: P40 child = the item just created
Q141205930	P40	LAST	S2600	"6000000007980352331"

# create a new item
CREATE
#   the item just created: set the en label to "Ragnhild Jonsdatter Lea"
LAST	Len	"Ragnhild Jonsdatter Lea"
#   set the mul label to "Ragnhild Jonsdatter Lea"
LAST	Lmul	"Ragnhild Jonsdatter Lea"
#   set the ja label to "ラグンヒル・ヨンスダッテル・リー"
LAST	Lja	"ラグンヒル・ヨンスダッテル・リー"
#   set the zh label to "拉格希尔德·永斯达特·莉亚"
LAST	Lzh	"拉格希尔德·永斯达特·莉亚"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005609547635 Ragnhild Jonsdatter Lea, qualified P1810 subject named as Ragnhild Jonsdatter Lea
LAST	P2600	"6000000005609547635"	P1810	"Ragnhild Jonsdatter Lea"
#   P569 date of birth = +1787-00-00T00:00:00Z/9
LAST	P569	+1787-00-00T00:00:00Z/9	S2600	"6000000005609547635"
#   P570 date of death = +1819-03-05T00:00:00Z/11
LAST	P570	+1819-03-05T00:00:00Z/11	S2600	"6000000005609547635"
#   P40 child = Q141223744 Rasmus Wibye Andersson Lea
LAST	P40	Q141223744	S2600	"6000000005609547635"
#   Q141223744 Rasmus Wibye Andersson Lea: P25 mother = the item just created
Q141223744	P25	LAST	S2600	"6000000005609547635"

# create a new item
CREATE
#   the item just created: set the en label to "Søren Jonson Aukland"
LAST	Len	"Søren Jonson Aukland"
#   set the mul label to "Søren Jonson Aukland"
LAST	Lmul	"Søren Jonson Aukland"
#   set the ja label to "セーレン・ヨンソン・アウクランド"
LAST	Lja	"セーレン・ヨンソン・アウクランド"
#   set the zh label to "索伦·永松·奥克兰德"
LAST	Lzh	"索伦·永松·奥克兰德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005607349830 Søren Jonson Aukland, qualified P1810 subject named as Søren Jonson Aukland
LAST	P2600	"6000000005607349830"	P1810	"Søren Jonson Aukland"
#   P22 father = Q141199899 Jon Tollakson Aukland, IV
LAST	P22	Q141199899	S2600	"6000000005607349830"
#   Q141199899 Jon Tollakson Aukland, IV: P40 child = the item just created
Q141199899	P40	LAST	S2600	"6000000005607349830"

# create a new item
CREATE
#   the item just created: set the en label to "Tore"
LAST	Len	"Tore"
#   set the mul label to "Tore"
LAST	Lmul	"Tore"
#   set the ja label to "トーレ"
LAST	Lja	"トーレ"
#   set the zh label to "托雷"
LAST	Lzh	"托雷"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000150599235822 Tore, qualified P1810 subject named as Tore
LAST	P2600	"6000000150599235822"	P1810	"Tore"
#   P569 date of birth = +1658-00-00T00:00:00Z/9
LAST	P569	+1658-00-00T00:00:00Z/9	S2600	"6000000150599235822"
#   P40 child = Q141216507 Torborg Toresdatter Norheim
LAST	P40	Q141216507	S2600	"6000000150599235822"
#   Q141216507 Torborg Toresdatter Norheim: P22 father = the item just created
Q141216507	P22	LAST	S2600	"6000000150599235822"
#   the item just created: P735 given name = Q1548096 Tore
LAST	P735	Q1548096
#   Q141225179 Maren Ellingsdatter Tunheim: P26 spouse = Q141225230 Osmund Andersen Tunheim
Q141225179	P26	Q141225230	S2600	"340026788150007985"
#   Q141225230 Osmund Andersen Tunheim: P26 spouse = Q141225179 Maren Ellingsdatter Tunheim
Q141225230	P26	Q141225179	S2600	"6000000002763481707"
#   Q141198375 Astri Torchelsdatter Øvre Time: P40 child = Q141225066 NN
Q141198375	P40	Q141225066	S2600	"6000000003731596731"
#   Q141217369 Anna Osmundsd Stokka: P40 child = Q141225175 Malene Larsdtr. Alvseike
Q141217369	P40	Q141225175	S2600	"6000000005609304839"
#   Q141225089 Christina Maria Silfverschiöld: P26 spouse = Q141225119 Göran Ehrenpreus
Q141225089	P26	Q141225119	S2600	"6000000008989027097"
#   Q141225119 Göran Ehrenpreus: P26 spouse = Q141225089 Christina Maria Silfverschiöld
Q141225119	P26	Q141225089	S2600	"6000000008989193521"
#   Q141225111 Ericus Nicolai Gestrinius: P26 spouse = Q141225068 Anna Mårtensdotter
Q141225111	P26	Q141225068	S2600	"6000000009298900297"
#   P735 given name = Q19830590 Nicolai, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141225111	P735	Q19830590	P1545	"2"	P3831	Q245025
#   Q141225068 Anna Mårtensdotter: P26 spouse = Q141225111 Ericus Nicolai Gestrinius
Q141225068	P26	Q141225111	S2600	"6000000010310582104"
#   Q141225085 Berger Mathisen Sparby: P26 spouse = Q141225209 Olea Gundersdatter Hibo
Q141225085	P26	Q141225209	S2600	"6000000016756929355"
#   Q141223853 Rakel Rasmusdottir Borsheim: P40 child = Q141225080 Annie Stangeland
Q141223853	P40	Q141225080	S2600	"6000000020344732085"
#   Q141225209 Olea Gundersdatter Hibo: P26 spouse = Q141225085 Berger Mathisen Sparby
Q141225209	P26	Q141225085	S2600	"6000000022341758896"
#   Q141225124 Halvar Larsson Mossige: P26 spouse = Q141225072 Anna Nilsdatter Mossige
Q141225124	P26	Q141225072	S2600	"6000000023784554708"
#   Q141225072 Anna Nilsdatter Mossige: P26 spouse = Q141225124 Halvar Larsson Mossige
Q141225072	P26	Q141225124	S2600	"6000000023784778055"
#   Q141189076 Kristian Larsen Sør-Reime: P734 family name = Q141189041
Q141189076	P734	Q141189041
#   Q141205912 Herborg Johannesdatter Sør-Reime: P734 family name = Q141189041
Q141205912	P734	Q141189041
#   Q141189067 Helmik Kristiansen Sør-Reime: P734 family name = Q141189041
Q141189067	P734	Q141189041
#   Q141198390 Elisabet Marie Osmundsdatter Sør-Reime: P734 family name = Q141189041
Q141198390	P734	Q141189041
#   Q141189078 Lars Kristiansen Sør-Reime: P734 family name = Q141189041
Q141189078	P734	Q141189041
#   Q141189077 Lars Bernhard Kristiansen Sør-Reime: P734 family name = Q141189041
Q141189077	P734	Q141189041

