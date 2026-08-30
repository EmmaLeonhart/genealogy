# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   897 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   Q5807136 Vilhelm Hising: set the mul label to "Vilhelm Hising"
Q5807136	Lmul	"Vilhelm Hising"
#   set the ja label to "ヴィルヘルム・ヒシング"
Q5807136	Lja	"ヴィルヘルム・ヒシング"
#   set the zh label to "威廉·希辛"
Q5807136	Lzh	"威廉·希辛"
#   Q5580703 Carl Julius Bernhard von Bohlen: set the mul label to "Carl Julius Bernhard von Bohlen"
Q5580703	Lmul	"Carl Julius Bernhard von Bohlen"
#   set the ja label to "カール・ユリウス・ベルンハルト・ヴォン・ボーレン"
Q5580703	Lja	"カール・ユリウス・ベルンハルト・ヴォン・ボーレン"
#   set the zh label to "卡尔·尤利乌斯·伯恩哈德·翁·博伦"
Q5580703	Lzh	"卡尔·尤利乌斯·伯恩哈德·翁·博伦"
#   Q5802535 Mattias von Hermansson: set the mul label to "Matthias von Hermansson"
Q5802535	Lmul	"Matthias von Hermansson"
#   add a mul alias "Mattias von Hermansson"
Q5802535	Amul	"Mattias von Hermansson"
#   Q141219051 Anna Börjesdotter Bothniensis: set the ja label to "アンナ・ボルイェスドッテル・ボトニエンシス"
Q141219051	Lja	"アンナ・ボルイェスドッテル・ボトニエンシス"
#   set the zh label to "安娜·博尔耶斯多特·博特尼恩西斯"
Q141219051	Lzh	"安娜·博尔耶斯多特·博特尼恩西斯"
#   Q141205900 Bertrand Olav Olsen Vigdel: set the ja label to "ベルトラン・オーラヴ・オルセン・ヴィグデル"
Q141205900	Lja	"ベルトラン・オーラヴ・オルセン・ヴィグデル"
#   set the zh label to "贝特朗·奥拉夫·奥尔森·维格德尔"
Q141205900	Lzh	"贝特朗·奥拉夫·奥尔森·维格德尔"
#   Q4945294 Ulrika Eleonora von Düben: set the mul label to "Ulrika Eleonora von Düben"
Q4945294	Lmul	"Ulrika Eleonora von Düben"
#   set the ja label to "ウルリカ・エレオノーラ・ヴォン・ディベン"
Q4945294	Lja	"ウルリカ・エレオノーラ・ヴォン・ディベン"
#   set the zh label to "乌尔里卡·埃莱奥诺拉·翁·迪本"
Q4945294	Lzh	"乌尔里卡·埃莱奥诺拉·翁·迪本"

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Anna, Stina Broman"
LAST	Len	"Anna, Stina Broman"
#   set the mul label to "Anna, Stina Broman"
LAST	Lmul	"Anna, Stina Broman"
#   set the ja label to "アンナ・スティーナ・ブロマン"
LAST	Lja	"アンナ・スティーナ・ブロマン"
#   set the zh label to "安娜·斯蒂纳·布罗曼"
LAST	Lzh	"安娜·斯蒂纳·布罗曼"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000177921561828 Anna, Stina Broman, qualified P1810 subject named as Anna, Stina Broman
LAST	P2600	"6000000177921561828"	P1810	"Anna, Stina Broman"
#   P569 date of birth = +1794-04-06T00:00:00Z/11
LAST	P569	+1794-04-06T00:00:00Z/11	S2600	"6000000177921561828"
#   P570 date of death = +1881-08-25T00:00:00Z/11
LAST	P570	+1881-08-25T00:00:00Z/11	S2600	"6000000177921561828"
#   P40 child = Q141223507 Carl, Johan Ersson
LAST	P40	Q141223507	S2600	"6000000177921561828"
#   Q141223507 Carl, Johan Ersson: P25 mother = the item just created
Q141223507	P25	LAST	S2600	"6000000177921561828"
#   the item just created: P735 given name = Q1770143 Stina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1770143	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Carolina Gustafsdotter Wittfooth"
LAST	Len	"Carolina Gustafsdotter Wittfooth"
#   set the mul label to "Carolina Gustafsdotter Wittfooth"
LAST	Lmul	"Carolina Gustafsdotter Wittfooth"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000013285902007 Carolina Gustafsdotter Wittfooth, qualified P1810 subject named as Carolina Gustafsdotter Wittfooth
LAST	P2600	"6000000013285902007"	P1810	"Carolina Gustafsdotter Wittfooth"
#   P569 date of birth = +1765-03-01T00:00:00Z/11
LAST	P569	+1765-03-01T00:00:00Z/11	S2600	"6000000013285902007"
#   P570 date of death = +1810-07-05T00:00:00Z/11
LAST	P570	+1810-07-05T00:00:00Z/11	S2600	"6000000013285902007"
#   P26 spouse = Q3946660 Samuel af Ugglas
LAST	P26	Q3946660	S2600	"6000000013285902007"
#   Q3946660 Samuel af Ugglas: P26 spouse = the item just created
Q3946660	P26	LAST	S2600	"6000000013285902007"
#   the item just created: P735 given name = Q5044762 Carolina
LAST	P735	Q5044762
#   add a mul alias "Wittfoth Wittfooth"
LAST	Amul	"Wittfoth Wittfooth"

# create a new item
CREATE
#   set the en label to "Erik Ersson"
LAST	Len	"Erik Ersson"
#   set the mul label to "Erik Ersson"
LAST	Lmul	"Erik Ersson"
#   set the ja label to "エリック・エルソン"
LAST	Lja	"エリック・エルソン"
#   set the zh label to "埃里克·埃尔松"
LAST	Lzh	"埃里克·埃尔松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000177921561822 Erik Ersson, qualified P1810 subject named as Erik Ersson
LAST	P2600	"6000000177921561822"	P1810	"Erik Ersson"
#   P569 date of birth = +1798-03-25T00:00:00Z/11
LAST	P569	+1798-03-25T00:00:00Z/11	S2600	"6000000177921561822"
#   P570 date of death = +1882-02-21T00:00:00Z/11
LAST	P570	+1882-02-21T00:00:00Z/11	S2600	"6000000177921561822"
#   P40 child = Q141223507 Carl, Johan Ersson
LAST	P40	Q141223507	S2600	"6000000177921561822"
#   Q141223507 Carl, Johan Ersson: P22 father = the item just created
Q141223507	P22	LAST	S2600	"6000000177921561822"
#   the item just created: P735 given name = Q750186 Erik
LAST	P735	Q750186

# create a new item
CREATE
#   set the en label to "Erik Rasmusson Norheim"
LAST	Len	"Erik Rasmusson Norheim"
#   set the mul label to "Erik Rasmusson Norheim"
LAST	Lmul	"Erik Rasmusson Norheim"
#   add a mul alias "Erik Rasmusson Rasmussen"
LAST	Amul	"Erik Rasmusson Rasmussen"
#   set the ja label to "エリック・ラスムソン・ノルヘイム"
LAST	Lja	"エリック・ラスムソン・ノルヘイム"
#   set the zh label to "埃里克·拉斯穆松·诺尔赫伊姆"
LAST	Lzh	"埃里克·拉斯穆松·诺尔赫伊姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000006776185092 Erik Rasmusson Norheim, qualified P1810 subject named as Erik Rasmusson Rasmussen
LAST	P2600	"6000000006776185092"	P1810	"Erik Rasmusson Rasmussen"
#   P569 date of birth = +1633-00-00T00:00:00Z/9
LAST	P569	+1633-00-00T00:00:00Z/9	S2600	"6000000006776185092"
#   P40 child = Q141216607 Hans Erikson Øvre Håland
LAST	P40	Q141216607	S2600	"6000000006776185092"
#   Q141216607 Hans Erikson Øvre Håland: P22 father = the item just created
Q141216607	P22	LAST	S2600	"6000000006776185092"
#   the item just created: P735 given name = Q750186 Erik
LAST	P735	Q750186
#   P734 family name = Q30350309 Norheim
LAST	P734	Q30350309
#   add a mul alias "Erik Norheim"
LAST	Amul	"Erik Norheim"

# create a new item
CREATE
#   set the en label to "Grace Kathleen Borsheim"
LAST	Len	"Grace Kathleen Borsheim"
#   set the mul label to "Grace Kathleen Borsheim"
LAST	Lmul	"Grace Kathleen Borsheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000177921458906 Grace Kathleen Borsheim, qualified P1810 subject named as Grace Kathleen Borsheim
LAST	P2600	"6000000177921458906"	P1810	"Grace Kathleen Borsheim"
#   P22 father = Q141224882 Randolph Paulus Borsheim
LAST	P22	Q141224882	S2600	"6000000177921458906"
#   P25 mother = Q141224812 Caroline Signe Borsheim
LAST	P25	Q141224812	S2600	"6000000177921458906"
#   Q141224882 Randolph Paulus Borsheim: P40 child = the item just created
Q141224882	P40	LAST	S2600	"6000000177921458906"
#   Q141224812 Caroline Signe Borsheim: P40 child = the item just created
Q141224812	P40	LAST	S2600	"6000000177921458906"

# create a new item
CREATE
#   the item just created: set the en label to "Gunnhild Pedersdatter Skårland"
LAST	Len	"Gunnhild Pedersdatter Skårland"
#   set the mul label to "Gunnhild Pedersdatter Skårland"
LAST	Lmul	"Gunnhild Pedersdatter Skårland"
#   set the ja label to "グンンヒルド・ペーデシュダッテル・スコールランド"
LAST	Lja	"グンンヒルド・ペーデシュダッテル・スコールランド"
#   set the zh label to "贡希尔德·佩德斯达特·斯科尔兰德"
LAST	Lzh	"贡希尔德·佩德斯达特·斯科尔兰德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005609534687 Gunnhild Pedersdatter Skårland, qualified P1810 subject named as Gunnhild Pedersdatter Skårland
LAST	P2600	"6000000005609534687"	P1810	"Gunnhild Pedersdatter Skårland"
#   P569 date of birth = +1692-00-00T00:00:00Z/9
LAST	P569	+1692-00-00T00:00:00Z/9	S2600	"6000000005609534687"
#   P40 child = Q141216609 Inger Kristoffersdatter Skårland
LAST	P40	Q141216609	S2600	"6000000005609534687"
#   Q141216609 Inger Kristoffersdatter Skårland: P25 mother = the item just created
Q141216609	P25	LAST	S2600	"6000000005609534687"
#   the item just created: P735 given name = Q33101910 Gunnhild
LAST	P735	Q33101910
#   P734 family name = Q40480033, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q40480033	P3831	Q28418670
#   add a mul alias "Gunnhild Skårland"
LAST	Amul	"Gunnhild Skårland"

# create a new item
CREATE
#   set the en label to "Hans Bertil Schemmelkorn"
LAST	Len	"Hans Bertil Schemmelkorn"
#   set the mul label to "Hans Bertil Schemmelkorn"
LAST	Lmul	"Hans Bertil Schemmelkorn"
#   add a mul alias "Hans Bertil Schütte av Sätra"
LAST	Amul	"Hans Bertil Schütte av Sätra"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000025620314016 Hans Bertil Schemmelkorn, qualified P1810 subject named as Hans Bertil Schütte av Sätra
LAST	P2600	"6000000025620314016"	P1810	"Hans Bertil Schütte av Sätra"
#   P25 mother = Q141225104 Engel Danckwardt
LAST	P25	Q141225104	S2600	"6000000025620314016"
#   Q141225104 Engel Danckwardt: P40 child = the item just created
Q141225104	P40	LAST	S2600	"6000000025620314016"
#   the item just created: P735 given name = Q632842, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q632842	P1545	"1"	P7452	Q3409033
#   P735 given name = Q19687104 Bertil, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q19687104	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Hans Jonsson"
LAST	Len	"Hans Jonsson"
#   set the mul label to "Hans Jonsson"
LAST	Lmul	"Hans Jonsson"
#   set the ja label to "ハンス・ヨンソン"
LAST	Lja	"ハンス・ヨンソン"
#   set the zh label to "汉斯·永松"
LAST	Lzh	"汉斯·永松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 1899596 Hans Jonsson, qualified P1810 subject named as Hans Jonsson
LAST	P2600	"1899596"	P1810	"Hans Jonsson"
#   P569 date of birth = +1739-12-05T00:00:00Z/11
LAST	P569	+1739-12-05T00:00:00Z/11	S2600	"1899596"
#   P570 date of death = +1800-00-00T00:00:00Z/9
LAST	P570	+1800-00-00T00:00:00Z/9	S2600	"1899596"
#   P40 child = Q5976894 Gabriel Hansson Marklin
LAST	P40	Q5976894	S2600	"1899596"
#   Q5976894 Gabriel Hansson Marklin: P22 father = the item just created
Q5976894	P22	LAST	S2600	"1899596"
#   the item just created: P735 given name = Q632842
LAST	P735	Q632842

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
#   set the en label to "Kristina Eriksdotter Ångerman"
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
#   set the en label to "Mareta Hansdotter Oma"
LAST	Len	"Mareta Hansdotter Oma"
#   set the mul label to "Mareta Hansdotter Oma"
LAST	Lmul	"Mareta Hansdotter Oma"
#   add a mul alias "Mareta Hansdotter Hansdatter"
LAST	Amul	"Mareta Hansdotter Hansdatter"
#   set the ja label to "マレタ・ハンスドッテル・オマ"
LAST	Lja	"マレタ・ハンスドッテル・オマ"
#   set the zh label to "马雷塔·汉斯多特·奥马"
LAST	Lzh	"马雷塔·汉斯多特·奥马"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000017825204157 Mareta Hansdotter Oma, qualified P1810 subject named as Mareta Hansdotter Hansdatter
LAST	P2600	"6000000017825204157"	P1810	"Mareta Hansdotter Hansdatter"
#   P569 date of birth = +1718-08-00T00:00:00Z/10
LAST	P569	+1718-08-00T00:00:00Z/10	S2600	"6000000017825204157"
#   P570 date of death = +1735-04-00T00:00:00Z/10
LAST	P570	+1735-04-00T00:00:00Z/10	S2600	"6000000017825204157"
#   P22 father = Q141216607 Hans Erikson Øvre Håland
LAST	P22	Q141216607	S2600	"6000000017825204157"
#   P25 mother = Q141216507 Torborg Toresdatter Norheim
LAST	P25	Q141216507	S2600	"6000000017825204157"
#   Q141216607 Hans Erikson Øvre Håland: P40 child = the item just created
Q141216607	P40	LAST	S2600	"6000000017825204157"
#   Q141216507 Torborg Toresdatter Norheim: P40 child = the item just created
Q141216507	P40	LAST	S2600	"6000000017825204157"
#   the item just created: P735 given name = Q65177322
LAST	P735	Q65177322
#   P5056 patronym or matronym = Q141223482, qualified P144 based on Q141216607 Hans Erikson Øvre Håland
LAST	P5056	Q141223482	P144	Q141216607
#   P734 family name = Q39043105, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q39043105	P3831	Q28418670
#   add a mul alias "Mareta Oma"
LAST	Amul	"Mareta Oma"

# create a new item
CREATE
#   set the en label to "Margareta Elisabet Johansdotter Amnell"
LAST	Len	"Margareta Elisabet Johansdotter Amnell"
#   set the mul label to "Margareta Elisabet Johansdotter Amnell"
LAST	Lmul	"Margareta Elisabet Johansdotter Amnell"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000001208357524 Margareta Elisabet Johansdotter Amnell, qualified P1810 subject named as Margareta Elisabet Johansdotter Amnell
LAST	P2600	"6000000001208357524"	P1810	"Margareta Elisabet Johansdotter Amnell"
#   P569 date of birth = +1733-07-11T00:00:00Z/11
LAST	P569	+1733-07-11T00:00:00Z/11	S2600	"6000000001208357524"
#   P570 date of death = +1771-03-20T00:00:00Z/11
LAST	P570	+1771-03-20T00:00:00Z/11	S2600	"6000000001208357524"
#   P26 spouse = Q6057321 Olof Andersson Pryss
LAST	P26	Q6057321	S2600	"6000000001208357524"
#   Q6057321 Olof Andersson Pryss: P26 spouse = the item just created
Q6057321	P26	LAST	S2600	"6000000001208357524"
#   the item just created: P735 given name = Q8274988 Margareta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q8274988	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16423275 Elisabet, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q16423275	P1545	"2"	P3831	Q245025
#   add a mul alias "Margareta Elisabet Amnell"
LAST	Amul	"Margareta Elisabet Amnell"

# create a new item
CREATE
#   set the en label to "Marite Olsdtr"
LAST	Len	"Marite Olsdtr"
#   set the mul label to "Marite Olsdtr"
LAST	Lmul	"Marite Olsdtr"
#   set the ja label to "マリテ・オルスダッテル"
LAST	Lja	"マリテ・オルスダッテル"
#   set the zh label to "马里特·奥尔斯达特"
LAST	Lzh	"马里特·奥尔斯达特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005609488533 Marite Olsdtr, qualified P1810 subject named as Marite Olsdtr
LAST	P2600	"6000000005609488533"	P1810	"Marite Olsdtr"
#   P570 date of death = +1683-00-00T00:00:00Z/9
LAST	P570	+1683-00-00T00:00:00Z/9	S2600	"6000000005609488533"
#   P40 child = Q141216607 Hans Erikson Øvre Håland
LAST	P40	Q141216607	S2600	"6000000005609488533"
#   Q141216607 Hans Erikson Øvre Håland: P25 mother = the item just created
Q141216607	P25	LAST	S2600	"6000000005609488533"
#   the item just created: P735 given name = Q48719725
LAST	P735	Q48719725

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
#   the item just created: set the en label to "Natanael Elias Cederschiöld"
LAST	Len	"Natanael Elias Cederschiöld"
#   set the mul label to "Natanael Elias Cederschiöld"
LAST	Lmul	"Natanael Elias Cederschiöld"
#   set the ja label to "ナタナエル・エリアス・セデルシオルド"
LAST	Lja	"ナタナエル・エリアス・セデルシオルド"
#   set the zh label to "纳塔纳埃尔·伊莱亚斯·塞德尔西奥尔德"
LAST	Lzh	"纳塔纳埃尔·伊莱亚斯·塞德尔西奥尔德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000012162436677 Natanael Elias Cederschiöld, qualified P1810 subject named as Natanael Elias Cederschiöld
LAST	P2600	"6000000012162436677"	P1810	"Natanael Elias Cederschiöld"
#   P569 date of birth = +1671-06-24T00:00:00Z/11
LAST	P569	+1671-06-24T00:00:00Z/11	S2600	"6000000012162436677"
#   P570 date of death = +1745-07-13T00:00:00Z/11
LAST	P570	+1745-07-13T00:00:00Z/11	S2600	"6000000012162436677"
#   P22 father = Q5605668 Petrus Eliae Cederschiöld till Lidboholm
LAST	P22	Q5605668	S2600	"6000000012162436677"
#   Q5605668 Petrus Eliae Cederschiöld till Lidboholm: P40 child = the item just created
Q5605668	P40	LAST	S2600	"6000000012162436677"
#   the item just created: P735 given name = Q1966292 Natanael, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q1966292	P1545	"1"	P7452	Q3409033
#   P735 given name = Q11878157 Elias, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q11878157	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Nils Skytte"
LAST	Len	"Nils Skytte"
#   set the mul label to "Nils Skytte"
LAST	Lmul	"Nils Skytte"
#   set the ja label to "ニルス・スキテ"
LAST	Lja	"ニルス・スキテ"
#   set the zh label to "尼尔斯·斯基特"
LAST	Lzh	"尼尔斯·斯基特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000008412100548 Nils Skytte, qualified P1810 subject named as Nils Skytte
LAST	P2600	"6000000008412100548"	P1810	"Nils Skytte"
#   P26 spouse = Q141225104 Engel Danckwardt
LAST	P26	Q141225104	S2600	"6000000008412100548"
#   Q141225104 Engel Danckwardt: P26 spouse = the item just created
Q141225104	P26	LAST	S2600	"6000000008412100548"
#   the item just created: P735 given name = Q16423038 Nils
LAST	P735	Q16423038

# create a new item
CREATE
#   set the en label to "Per Andersson"
LAST	Len	"Per Andersson"
#   set the mul label to "Per Andersson"
LAST	Lmul	"Per Andersson"
#   set the ja label to "ペール・アンデション"
LAST	Lja	"ペール・アンデション"
#   set the zh label to "佩尔·安德松"
LAST	Lzh	"佩尔·安德松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000019176344694 Per Andersson, qualified P1810 subject named as Per Andersson
LAST	P2600	"6000000019176344694"	P1810	"Per Andersson"
#   P569 date of birth = +1662-00-00T00:00:00Z/9
LAST	P569	+1662-00-00T00:00:00Z/9	S2600	"6000000019176344694"
#   P570 date of death = +1755-00-00T00:00:00Z/9
LAST	P570	+1755-00-00T00:00:00Z/9	S2600	"6000000019176344694"
#   P22 father = Q141216455 Anders Persson
LAST	P22	Q141216455	S2600	"6000000019176344694"
#   Q141216455 Anders Persson: P40 child = the item just created
Q141216455	P40	LAST	S2600	"6000000019176344694"

# create a new item
CREATE
#   the item just created: set the en label to "Sara Ericsdotter"
LAST	Len	"Sara Ericsdotter"
#   set the mul label to "Sara Ericsdotter"
LAST	Lmul	"Sara Ericsdotter"
#   set the ja label to "サラ・エリクスドッテル"
LAST	Lja	"サラ・エリクスドッテル"
#   set the zh label to "萨拉·埃里克斯多特"
LAST	Lzh	"萨拉·埃里克斯多特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 4184733660450025774 Sara Ericsdotter, qualified P1810 subject named as Sara Ericsdotter
LAST	P2600	"4184733660450025774"	P1810	"Sara Ericsdotter"
#   P569 date of birth = +1740-10-18T00:00:00Z/11
LAST	P569	+1740-10-18T00:00:00Z/11	S2600	"4184733660450025774"
#   P570 date of death = +1809-10-27T00:00:00Z/11
LAST	P570	+1809-10-27T00:00:00Z/11	S2600	"4184733660450025774"
#   P40 child = Q5976894 Gabriel Hansson Marklin
LAST	P40	Q5976894	S2600	"4184733660450025774"
#   Q5976894 Gabriel Hansson Marklin: P25 mother = the item just created
Q5976894	P25	LAST	S2600	"4184733660450025774"
#   the item just created: P735 given name = Q833345 Sara
LAST	P735	Q833345

# create a new item
CREATE
#   set the en label to "Søren Jonson Aukland"
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

