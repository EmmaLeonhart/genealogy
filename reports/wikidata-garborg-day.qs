# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   845 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   Q141225714 Ingeborg Simonsdatter Ytre Lima: add a mul alias "Ingeborg Simonsdatter Ravndal"
Q141225714	Amul	"Ingeborg Simonsdatter Ravndal"
#   Q141205938 Ranveig Olsd Trevland: set the ja label to "ランヴェイグ・オルスド・トレヴランド"
Q141205938	Lja	"ランヴェイグ・オルスド・トレヴランド"
#   set the zh label to "兰韦伊格·奥尔斯德·特雷夫兰德"
Q141205938	Lzh	"兰韦伊格·奥尔斯德·特雷夫兰德"
#   Q364270 Carl Gustaf Patrik de Laval: set the mul label to "Gustaf de Laval"
Q364270	Lmul	"Gustaf de Laval"
#   add a mul alias "Carl Gustaf Patrik de Laval"
Q364270	Amul	"Carl Gustaf Patrik de Laval"
#   Q141199881 Ivar Sandsmark Garborg: set the ja label to "イヴァル・サンスマルク・ガルボルグ"
Q141199881	Lja	"イヴァル・サンスマルク・ガルボルグ"
#   Q139651594 Sigrid Garborg: set the ja label to "シグリッド・ガルボルグ"
Q139651594	Lja	"シグリッド・ガルボルグ"
#   Q141168837 Ingebret Inge Garborg: add a mul alias "Ingebret Inge Garborg"
Q141168837	Amul	"Ingebret Inge Garborg"
#   Q141168954 Jon Garborg: set the ja label to "ジョン・ガルボルグ"
Q141168954	Lja	"ジョン・ガルボルグ"
#   set the zh label to "乔恩·加尔博格"
Q141168954	Lzh	"乔恩·加尔博格"
#   Q141205915 Jöns Jakobsson guldsmed: set the ja label to "ヨンス・ヤコブソン・グルドスメド"
Q141205915	Lja	"ヨンス・ヤコブソン・グルドスメド"
#   set the zh label to "永斯·雅各布松·古尔德斯梅德"
Q141205915	Lzh	"永斯·雅各布松·古尔德斯梅德"
#   Q1340357 Jakob Benzelius: set the mul label to "Jacob Benzelius"
Q1340357	Lmul	"Jacob Benzelius"
#   set the ja label to "ジェイコブ・ベンゼリウス"
Q1340357	Lja	"ジェイコブ・ベンゼリウス"
#   set the zh label to "雅各布·本泽利乌斯"
Q1340357	Lzh	"雅各布·本泽利乌斯"

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Alfred Ingerman Hoknes"
LAST	Len	"Alfred Ingerman Hoknes"
#   set the mul label to "Alfred Ingerman Hoknes"
LAST	Lmul	"Alfred Ingerman Hoknes"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000015117490925 Alfred Ingerman Hoknes, qualified P1810 subject named as Alfred Ingerman Hoknes
LAST	P2600	"6000000015117490925"	P1810	"Alfred Ingerman Hoknes"
#   P569 date of birth = +1905-02-06T00:00:00Z/11
LAST	P569	+1905-02-06T00:00:00Z/11	S2600	"6000000015117490925"
#   P570 date of death = +1979-08-20T00:00:00Z/11
LAST	P570	+1979-08-20T00:00:00Z/11	S2600	"6000000015117490925"
#   P26 spouse = Q141224807 Sophia Borgit Hoknes
LAST	P26	Q141224807	S2600	"6000000015117490925"
#   P40 child = Q141224812 Caroline Signe Borsheim
LAST	P40	Q141224812	S2600	"6000000015117490925"
#   Q141224807 Sophia Borgit Hoknes: P26 spouse = the item just created
Q141224807	P26	LAST	S2600	"6000000015117490925"
#   Q141224812 Caroline Signe Borsheim: P22 father = the item just created
Q141224812	P22	LAST	S2600	"6000000015117490925"

# create a new item
CREATE
#   the item just created: set the en label to "Berte Karlsdatter Borsok"
LAST	Len	"Berte Karlsdatter Borsok"
#   set the mul label to "Berte Karlsdatter Borsok"
LAST	Lmul	"Berte Karlsdatter Borsok"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000035525469386 Berte Karlsdatter Borsok, qualified P1810 subject named as Berte Karlsdatter Borsok
LAST	P2600	"6000000035525469386"	P1810	"Berte Karlsdatter Borsok"
#   P569 date of birth = +1784-00-00T00:00:00Z/9
LAST	P569	+1784-00-00T00:00:00Z/9	S2600	"6000000035525469386"
#   P570 date of death = +1876-02-27T00:00:00Z/11
LAST	P570	+1876-02-27T00:00:00Z/11	S2600	"6000000035525469386"
#   P40 child = Q141224861 Paul Pederson Borsheim
LAST	P40	Q141224861	S2600	"6000000035525469386"
#   Q141224861 Paul Pederson Borsheim: P25 mother = the item just created
Q141224861	P25	LAST	S2600	"6000000035525469386"

# create a new item
CREATE
#   the item just created: set the en label to "Bjørn Gunnbjørnsson Kvåvig"
LAST	Len	"Bjørn Gunnbjørnsson Kvåvig"
#   set the mul label to "Bjørn Gunnbjørnsson Kvåvig"
LAST	Lmul	"Bjørn Gunnbjørnsson Kvåvig"
#   set the ja label to "ビョルン・グンンブヨルンソン・クヴォーヴィグ"
LAST	Lja	"ビョルン・グンンブヨルンソン・クヴォーヴィグ"
#   set the zh label to "比约恩·贡布约尔恩松·克沃维格"
LAST	Lzh	"比约恩·贡布约尔恩松·克沃维格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000004569609494 Bjørn Gunnbjørnsson Kvåvig, qualified P1810 subject named as Bjørn Gunnbjørnsson Kvåvig
LAST	P2600	"6000000004569609494"	P1810	"Bjørn Gunnbjørnsson Kvåvig"
#   P569 date of birth = +1460-00-00T00:00:00Z/9
LAST	P569	+1460-00-00T00:00:00Z/9	S2600	"6000000004569609494"
#   P570 date of death = +1538-00-00T00:00:00Z/9
LAST	P570	+1538-00-00T00:00:00Z/9	S2600	"6000000004569609494"
#   P22 father = Q141199851 Lagmann Gunnbjørn Toresson Tengs
LAST	P22	Q141199851	S2600	"6000000004569609494"
#   Q141199851 Lagmann Gunnbjørn Toresson Tengs: P40 child = the item just created
Q141199851	P40	LAST	S2600	"6000000004569609494"

# create a new item
CREATE
#   the item just created: set the en label to "Christian Osmundsen Nese"
LAST	Len	"Christian Osmundsen Nese"
#   set the mul label to "Christian Osmundsen Nese"
LAST	Lmul	"Christian Osmundsen Nese"
#   set the ja label to "クリスチャン・オスムンドセン・ネセ"
LAST	Lja	"クリスチャン・オスムンドセン・ネセ"
#   set the zh label to "克里斯蒂安·奥斯蒙德森·内塞"
LAST	Lzh	"克里斯蒂安·奥斯蒙德森·内塞"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000011329696852 Christian Osmundsen Nese, qualified P1810 subject named as Christian Osmundsen Nese
LAST	P2600	"6000000011329696852"	P1810	"Christian Osmundsen Nese"
#   P569 date of birth = +1821-07-15T00:00:00Z/11
LAST	P569	+1821-07-15T00:00:00Z/11	S2600	"6000000011329696852"
#   P570 date of death = +1904-06-06T00:00:00Z/11
LAST	P570	+1904-06-06T00:00:00Z/11	S2600	"6000000011329696852"
#   P22 father = Q141223432 Osmund Larsson Nese
LAST	P22	Q141223432	S2600	"6000000011329696852"
#   Q141223432 Osmund Larsson Nese: P40 child = the item just created
Q141223432	P40	LAST	S2600	"6000000011329696852"

# create a new item
CREATE
#   the item just created: set the en label to "David Torgerson Stokka"
LAST	Len	"David Torgerson Stokka"
#   set the mul label to "David Torgerson Stokka"
LAST	Lmul	"David Torgerson Stokka"
#   set the ja label to "デイヴィッド・トルゲルソン・ストカ"
LAST	Lja	"デイヴィッド・トルゲルソン・ストカ"
#   set the zh label to "大卫·托尔盖尔松·斯托卡"
LAST	Lzh	"大卫·托尔盖尔松·斯托卡"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000037795923833 David Torgerson Stokka, qualified P1810 subject named as David Torgerson Stokka
LAST	P2600	"6000000037795923833"	P1810	"David Torgerson Stokka"
#   P569 date of birth = +1841-04-08T00:00:00Z/11
LAST	P569	+1841-04-08T00:00:00Z/11	S2600	"6000000037795923833"
#   P570 date of death = +1865-07-25T00:00:00Z/11
LAST	P570	+1865-07-25T00:00:00Z/11	S2600	"6000000037795923833"
#   P22 father = Q141216653 Torger Torgerson Stokka
LAST	P22	Q141216653	S2600	"6000000037795923833"
#   P25 mother = Q141216602 Berta Guria Davidsdatter Stokka
LAST	P25	Q141216602	S2600	"6000000037795923833"
#   Q141216653 Torger Torgerson Stokka: P40 child = the item just created
Q141216653	P40	LAST	S2600	"6000000037795923833"
#   Q141216602 Berta Guria Davidsdatter Stokka: P40 child = the item just created
Q141216602	P40	LAST	S2600	"6000000037795923833"
#   the item just created: P735 given name = Q29937870 David
LAST	P735	Q29937870
#   P734 family name = Q37526882
LAST	P734	Q37526882
#   P734 family name = Q37033285
LAST	P734	Q37033285

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
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000225376735889 Hans Rasmussen Bø, qualified P1810 subject named as Hans Rasmussen Bø
LAST	P2600	"6000000225376735889"	P1810	"Hans Rasmussen Bø"
#   P569 date of birth = +1882-01-20T00:00:00Z/11
LAST	P569	+1882-01-20T00:00:00Z/11	S2600	"6000000225376735889"
#   P570 date of death = +1940-00-00T00:00:00Z/9
LAST	P570	+1940-00-00T00:00:00Z/9	S2600	"6000000225376735889"
#   P22 father = Q141189099 Rasmus Helgesen Bø
LAST	P22	Q141189099	S2600	"6000000225376735889"
#   P25 mother = Q141219050 Ane Olsdatter Bø
LAST	P25	Q141219050	S2600	"6000000225376735889"
#   Q141189099 Rasmus Helgesen Bø: P40 child = the item just created
Q141189099	P40	LAST	S2600	"6000000225376735889"
#   Q141219050 Ane Olsdatter Bø: P40 child = the item just created
Q141219050	P40	LAST	S2600	"6000000225376735889"
#   the item just created: P735 given name = Q632842
LAST	P735	Q632842
#   P734 family name = Q30253098
LAST	P734	Q30253098

# create a new item
CREATE
#   set the en label to "Harald Sivert Vålnes"
LAST	Len	"Harald Sivert Vålnes"
#   set the mul label to "Harald Sivert Vålnes"
LAST	Lmul	"Harald Sivert Vålnes"
#   add a mul alias "Harald Sivert Nilsen"
LAST	Amul	"Harald Sivert Nilsen"
#   set the ja label to "ハラルド・シヴェルト・ヴォールネス"
LAST	Lja	"ハラルド・シヴェルト・ヴォールネス"
#   set the zh label to "哈拉尔德·西韦尔特·沃尔内斯"
LAST	Lzh	"哈拉尔德·西韦尔特·沃尔内斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000014631341075 Harald Sivert Vålnes, qualified P1810 subject named as Harald Sivert Nilsen
LAST	P2600	"6000000014631341075"	P1810	"Harald Sivert Nilsen"
#   P569 date of birth = +1917-02-03T00:00:00Z/11
LAST	P569	+1917-02-03T00:00:00Z/11	S2600	"6000000014631341075"
#   P570 date of death = +1991-06-20T00:00:00Z/11
LAST	P570	+1991-06-20T00:00:00Z/11	S2600	"6000000014631341075"
#   P26 spouse = Q141216501 Siri Garborg Talle
LAST	P26	Q141216501	S2600	"6000000014631341075"
#   Q141216501 Siri Garborg Talle: P26 spouse = the item just created
Q141216501	P26	LAST	S2600	"6000000014631341075"
#   the item just created: P735 given name = Q1530266 Harald, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q1530266	P1545	"1"	P7452	Q3409033
#   P735 given name = Q19869345 Sivert, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q19869345	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Henning Nilsson Skytte"
LAST	Len	"Henning Nilsson Skytte"
#   set the mul label to "Henning Nilsson Skytte"
LAST	Lmul	"Henning Nilsson Skytte"
#   set the ja label to "ヘニング・ニルソン・スキテ"
LAST	Lja	"ヘニング・ニルソン・スキテ"
#   set the zh label to "亨宁·尼尔松·斯基特"
LAST	Lzh	"亨宁·尼尔松·斯基特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000009499682160 Henning Nilsson Skytte, qualified P1810 subject named as Henning Nilsson Skytte
LAST	P2600	"6000000009499682160"	P1810	"Henning Nilsson Skytte"
#   P569 date of birth = +1595-00-00T00:00:00Z/9
LAST	P569	+1595-00-00T00:00:00Z/9	S2600	"6000000009499682160"
#   P570 date of death = +1646-00-00T00:00:00Z/9
LAST	P570	+1646-00-00T00:00:00Z/9	S2600	"6000000009499682160"
#   P25 mother = Q141225104 Engel Danckwardt
LAST	P25	Q141225104	S2600	"6000000009499682160"
#   P26 spouse = Q141225104 Engel Danckwardt
LAST	P26	Q141225104	S2600	"6000000009499682160"
#   P40 child = Q141223728 Brita Schytte
LAST	P40	Q141223728	S2600	"6000000009499682160"
#   Q141225104 Engel Danckwardt: P40 child = the item just created
Q141225104	P40	LAST	S2600	"6000000009499682160"
#   P26 spouse = the item just created
Q141225104	P26	LAST	S2600	"6000000009499682160"
#   Q141223728 Brita Schytte: P22 father = the item just created
Q141223728	P22	LAST	S2600	"6000000009499682160"
#   the item just created: P735 given name = Q18607880 Henning
LAST	P735	Q18607880
#   P5056 patronym or matronym = Q130233015 Nilsson
LAST	P5056	Q130233015
#   add a mul alias "Skytte"
LAST	Amul	"Skytte"
#   add a mul alias "Henning Skytte"
LAST	Amul	"Henning Skytte"

# create a new item
CREATE
#   set the en label to "Maria Gjeruldsdatter Vatne"
LAST	Len	"Maria Gjeruldsdatter Vatne"
#   set the mul label to "Maria Gjeruldsdatter Vatne"
LAST	Lmul	"Maria Gjeruldsdatter Vatne"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000014516776068 Maria Gjeruldsdtr Vatne, qualified P1810 subject named as Maria Gjeruldsdtr Vatne
LAST	P2600	"6000000014516776068"	P1810	"Maria Gjeruldsdtr Vatne"
#   P569 date of birth = +1827-00-00T00:00:00Z/9
LAST	P569	+1827-00-00T00:00:00Z/9	S2600	"6000000014516776068"
#   P26 spouse = Q141216476 Jon Jonsson Vatne
LAST	P26	Q141216476	S2600	"6000000014516776068"
#   Q141216476 Jon Jonsson Vatne: P26 spouse = the item just created
Q141216476	P26	LAST	S2600	"6000000014516776068"
#   the item just created: P735 given name = Q325872 Maria, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q325872	P1545	"1"	P7452	Q3409033
#   P734 family name = Q30134985 Vatne
LAST	P734	Q30134985

# create a new item
CREATE
#   set the en label to "Palle Paulson Borsok"
LAST	Len	"Palle Paulson Borsok"
#   set the mul label to "Palle Paulson Borsok"
LAST	Lmul	"Palle Paulson Borsok"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000077299349615 Palle Paulson Borsok, qualified P1810 subject named as Palle Paulson Borsok
LAST	P2600	"6000000077299349615"	P1810	"Palle Paulson Borsok"
#   P569 date of birth = +1860-02-07T00:00:00Z/11
LAST	P569	+1860-02-07T00:00:00Z/11	S2600	"6000000077299349615"
#   P570 date of death = +1949-12-26T00:00:00Z/11
LAST	P570	+1949-12-26T00:00:00Z/11	S2600	"6000000077299349615"
#   P22 father = Q141224861 Paul Pederson Borsheim
LAST	P22	Q141224861	S2600	"6000000077299349615"
#   P25 mother = Q141224751 Berta Serina Rasmusdatter Borsheim
LAST	P25	Q141224751	S2600	"6000000077299349615"
#   Q141224861 Paul Pederson Borsheim: P40 child = the item just created
Q141224861	P40	LAST	S2600	"6000000077299349615"
#   Q141224751 Berta Serina Rasmusdatter Borsheim: P40 child = the item just created
Q141224751	P40	LAST	S2600	"6000000077299349615"

# create a new item
CREATE
#   the item just created: set the en label to "Peder Paulsen Borsok"
LAST	Len	"Peder Paulsen Borsok"
#   set the mul label to "Peder Paulsen Borsok"
LAST	Lmul	"Peder Paulsen Borsok"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000035525387457 Peder Paulsen Borsok, qualified P1810 subject named as Peder Paulsen Borsok
LAST	P2600	"6000000035525387457"	P1810	"Peder Paulsen Borsok"
#   P569 date of birth = +1783-00-00T00:00:00Z/9
LAST	P569	+1783-00-00T00:00:00Z/9	S2600	"6000000035525387457"
#   P570 date of death = +1875-05-01T00:00:00Z/11
LAST	P570	+1875-05-01T00:00:00Z/11	S2600	"6000000035525387457"
#   P40 child = Q141224861 Paul Pederson Borsheim
LAST	P40	Q141224861	S2600	"6000000035525387457"
#   Q141224861 Paul Pederson Borsheim: P22 father = the item just created
Q141224861	P22	LAST	S2600	"6000000035525387457"

# create a new item
CREATE
#   the item just created: set the en label to "Samuel Tollefson Tunheim"
LAST	Len	"Samuel Tollefson Tunheim"
#   set the mul label to "Samuel Tollefson Tunheim"
LAST	Lmul	"Samuel Tollefson Tunheim"
#   set the ja label to "サミュエル・トレフソン・トゥンヘイム"
LAST	Lja	"サミュエル・トレフソン・トゥンヘイム"
#   set the zh label to "塞缪尔·托勒夫松·通海姆"
LAST	Lzh	"塞缪尔·托勒夫松·通海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000028541553897 Samuel Tollefson Tunheim, qualified P1810 subject named as Samuel Tollefson Tunheim
LAST	P2600	"6000000028541553897"	P1810	"Samuel Tollefson Tunheim"
#   P569 date of birth = +1858-12-01T00:00:00Z/11
LAST	P569	+1858-12-01T00:00:00Z/11	S2600	"6000000028541553897"
#   P570 date of death = +1918-02-23T00:00:00Z/11
LAST	P570	+1918-02-23T00:00:00Z/11	S2600	"6000000028541553897"
#   P22 father = Q141200112 Tollef Pederson Tunheim
LAST	P22	Q141200112	S2600	"6000000028541553897"
#   P25 mother = Q141199826 Anna Maria Samuelsdtr. Tunheim
LAST	P25	Q141199826	S2600	"6000000028541553897"
#   Q141200112 Tollef Pederson Tunheim: P40 child = the item just created
Q141200112	P40	LAST	S2600	"6000000028541553897"
#   Q141199826 Anna Maria Samuelsdtr. Tunheim: P40 child = the item just created
Q141199826	P40	LAST	S2600	"6000000028541553897"
#   the item just created: P735 given name = Q629347 Samuel
LAST	P735	Q629347
#   P734 family name = Q36927172
LAST	P734	Q36927172
#   add a mul alias "Samuel Tunheim"
LAST	Amul	"Samuel Tunheim"

# create a new item
CREATE
#   set the en label to "Sara Asbjørnsdatter Bø"
LAST	Len	"Sara Asbjørnsdatter Bø"
#   set the mul label to "Sara Asbjørnsdatter Bø"
LAST	Lmul	"Sara Asbjørnsdatter Bø"
#   set the ja label to "サラ・アスブヨルンスダッテル・ベー"
LAST	Lja	"サラ・アスブヨルンスダッテル・ベー"
#   set the zh label to "萨拉·阿斯布约尔恩斯达特·鲍伊"
LAST	Lzh	"萨拉·阿斯布约尔恩斯达特·鲍伊"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000222520233004 Sara Asbjørnsdatter Bø, qualified P1810 subject named as Sara Asbjørnsdatter Bø
LAST	P2600	"6000000222520233004"	P1810	"Sara Asbjørnsdatter Bø"
#   P569 date of birth = +1762-00-00T00:00:00Z/9
LAST	P569	+1762-00-00T00:00:00Z/9	S2600	"6000000222520233004"
#   P22 father = Q141216458 Asbjørn Gunnarson Bø
LAST	P22	Q141216458	S2600	"6000000222520233004"
#   P25 mother = Q141216456 Anna Helgesdotter Opstad
LAST	P25	Q141216456	S2600	"6000000222520233004"
#   Q141216458 Asbjørn Gunnarson Bø: P40 child = the item just created
Q141216458	P40	LAST	S2600	"6000000222520233004"
#   Q141216456 Anna Helgesdotter Opstad: P40 child = the item just created
Q141216456	P40	LAST	S2600	"6000000222520233004"
#   the item just created: P735 given name = Q833345 Sara
LAST	P735	Q833345
#   P734 family name = Q30253098
LAST	P734	Q30253098
#   Q141225179 Maren Ellingsdatter Tunheim: P26 spouse = Q141225230 Osmund Andersen Tunheim
Q141225179	P26	Q141225230	S2600	"340026788150007985"
#   Q141225230 Osmund Andersen Tunheim: P26 spouse = Q141225179 Maren Ellingsdatter Tunheim
Q141225230	P26	Q141225179	S2600	"6000000002763481707"
#   Q141198375 Astri Torchelsdatter Øvre Time: P40 child = Q141225066 NN
Q141198375	P40	Q141225066	S2600	"6000000003731596731"
#   Q141217369 Anna Osmundsd Stokka: P40 child = Q141225175 Malene Larsdtr. Alvseike
Q141217369	P40	Q141225175	S2600	"6000000005609304839"
#   Q141225703 Erik Guttormsson: P25 mother = Q141225788 Kristine NN
Q141225703	P25	Q141225788	S2600	"6000000007328872457"
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
#   Q141225794 Laurentius Andreae Andreae Alstrinius: P26 spouse = Q141225780 Kristina Eriksdotter Ångerman
Q141225794	P26	Q141225780	S2600	"6000000025011507008"
#   Q141225780 Kristina Eriksdotter Ångerman: P26 spouse = Q141225794 Laurentius Andreae Andreae Alstrinius
Q141225780	P26	Q141225794	S2600	"6000000038458498753"
#   Q141225788 Kristine NN: P40 child = Q141225703 Erik Guttormsson
Q141225788	P40	Q141225703	S2600	"6000000040760740831"
#   P735 given name = Q16859157 Kristine
Q141225788	P735	Q16859157

