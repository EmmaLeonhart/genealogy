# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   732 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   Q6045829 Johan Teodor Petré: set the ja label to "ヨハン・テオドル・ペトレ"
Q6045829	Lja	"ヨハン・テオドル・ペトレ"
#   set the zh label to "约汉·特奥多尔·佩特雷"
Q6045829	Lzh	"约汉·特奥多尔·佩特雷"
#   Q116150299 Jon Reinmodsen: set the ja label to "ヨン・レインモドセン"
Q116150299	Lja	"ヨン・レインモドセン"
#   set the zh label to "永·雷因莫德森"
Q116150299	Lzh	"永·雷因莫德森"
#   Q5773287 Samuel Andreæ Grubb: set the ja label to "サムエル・アンドレエ・グルブ"
Q5773287	Lja	"サムエル・アンドレエ・グルブ"
#   set the zh label to "萨穆埃尔·安德雷埃·格鲁布"
Q5773287	Lzh	"萨穆埃尔·安德雷埃·格鲁布"
#   set the zh label to "卡尔尔·古斯塔夫·马内尔赫伊姆"
Q2415388	Lzh	"卡尔尔·古斯塔夫·马内尔赫伊姆"
#   Q5975022 Lars August Mannerheim: set the ja label to "ラーシュ・アウグスト・マネルヘイム"
Q5975022	Lja	"ラーシュ・アウグスト・マネルヘイム"
#   set the zh label to "拉尔斯·奥古斯特·马内尔赫伊姆"
Q5975022	Lzh	"拉尔斯·奥古斯特·马内尔赫伊姆"
#   set the zh label to "索菲阿·瓦登斯蒂埃尔纳"
Q141219332	Lzh	"索菲阿·瓦登斯蒂埃尔纳"
#   Q1814297 Carl Erik Mannerheim: set the ja label to "カルル・エリク・マネルヘイム"
Q1814297	Lja	"カルル・エリク・マネルヘイム"
#   set the zh label to "卡尔尔·埃里克·马内尔赫伊姆"
Q1814297	Lzh	"卡尔尔·埃里克·马内尔赫伊姆"
#   Q1036858 Carl August Ehrensvärd: set the ja label to "カルル・アウグスト・エレンスヴェルド"
Q1036858	Lja	"カルル・アウグスト・エレンスヴェルド"
#   set the zh label to "卡尔尔·奥古斯特·埃伦斯韦尔德"
Q1036858	Lzh	"卡尔尔·奥古斯特·埃伦斯韦尔德"
#   Q141216397 Malin Andersdotter: set the zh label to "马林·安德斯多特"
Q141216397	Lzh	"马林·安德斯多特"

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Anna Mårtensdotter"
LAST	Len	"Anna Mårtensdotter"
#   set the mul label to "Anna Mårtensdotter"
LAST	Lmul	"Anna Mårtensdotter"
#   set the ja label to "アンナ・モーテンスドッテル"
LAST	Lja	"アンナ・モーテンスドッテル"
#   set the zh label to "安娜·莫滕斯多特"
LAST	Lzh	"安娜·莫滕斯多特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000027467541000 Anna Mårtensdotter, qualified P1810 subject named as Anna Mårtensdotter
LAST	P2600	"6000000027467541000"	P1810	"Anna Mårtensdotter"
#   P22 father = Q141199959 Martinus Johannis
LAST	P22	Q141199959	S2600	"6000000027467541000"
#   P25 mother = Q141199822 Anna Jönsdotter
LAST	P25	Q141199822	S2600	"6000000027467541000"
#   Q141199959 Martinus Johannis: P40 child = the item just created
Q141199959	P40	LAST	S2600	"6000000027467541000"
#   Q141199822 Anna Jönsdotter: P40 child = the item just created
Q141199822	P40	LAST	S2600	"6000000027467541000"

# create a new item
CREATE
#   the item just created: set the en label to "Augusta Ulrika Mannerheim"
LAST	Len	"Augusta Ulrika Mannerheim"
#   set the mul label to "Augusta Ulrika Mannerheim"
LAST	Lmul	"Augusta Ulrika Mannerheim"
#   set the ja label to "アウグスタ・ウルリカ・マネルヘイム"
LAST	Lja	"アウグスタ・ウルリカ・マネルヘイム"
#   set the zh label to "奥古斯塔·乌尔里卡·马内尔赫伊姆"
LAST	Lzh	"奥古斯塔·乌尔里卡·马内尔赫伊姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000000047226410 Augusta Ulrika Mannerheim, qualified P1810 subject named as Augusta Ulrika Mannerheim
LAST	P2600	"6000000000047226410"	P1810	"Augusta Ulrika Mannerheim"
#   P569 date of birth = +1792-01-15T00:00:00Z/11
LAST	P569	+1792-01-15T00:00:00Z/11	S2600	"6000000000047226410"
#   P570 date of death = +1855-12-09T00:00:00Z/11
LAST	P570	+1855-12-09T00:00:00Z/11	S2600	"6000000000047226410"
#   P22 father = Q5975022 Lars August Mannerheim
LAST	P22	Q5975022	S2600	"6000000000047226410"
#   P25 mother = Q141219332 Sofia Wadenstierna
LAST	P25	Q141219332	S2600	"6000000000047226410"
#   Q5975022 Lars August Mannerheim: P40 child = the item just created
Q5975022	P40	LAST	S2600	"6000000000047226410"
#   Q141219332 Sofia Wadenstierna: P40 child = the item just created
Q141219332	P40	LAST	S2600	"6000000000047226410"
#   the item just created: P735 given name = Q1370330 Augusta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q1370330	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18924998 Ulrika, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q18924998	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Barbara Catharina Kristina Fabrin"
LAST	Len	"Barbara Catharina Kristina Fabrin"
#   set the mul label to "Barbara Catharina Kristina Fabrin"
LAST	Lmul	"Barbara Catharina Kristina Fabrin"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000006127951026 Barbara Catharina Kristina Fabrin, qualified P1810 subject named as Barbara Catharina Kristina Fabrin
LAST	P2600	"6000000006127951026"	P1810	"Barbara Catharina Kristina Fabrin"
#   P569 date of birth = +1728-07-24T00:00:00Z/11
LAST	P569	+1728-07-24T00:00:00Z/11	S2600	"6000000006127951026"
#   P570 date of death = +1780-05-22T00:00:00Z/11
LAST	P570	+1780-05-22T00:00:00Z/11	S2600	"6000000006127951026"
#   P26 spouse = Q5807136 Vilhelm Hising
LAST	P26	Q5807136	S2600	"6000000006127951026"
#   P40 child = Q900478 Vilhelm Hisinger
LAST	P40	Q900478	S2600	"6000000006127951026"
#   Q5807136 Vilhelm Hising: P26 spouse = the item just created
Q5807136	P26	LAST	S2600	"6000000006127951026"
#   Q900478 Vilhelm Hisinger: P25 mother = the item just created
Q900478	P25	LAST	S2600	"6000000006127951026"
#   the item just created: P735 given name = Q153957 Barbara, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q153957	P1545	"1"	P7452	Q3409033
#   P735 given name = Q17317997 Catharina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q17317997	P1545	"2"	P3831	Q245025
#   P735 given name = Q19798802 Kristina, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
LAST	P735	Q19798802	P1545	"3"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Elen Malena Halvorsdatter Tunheim"
LAST	Len	"Elen Malena Halvorsdatter Tunheim"
#   set the mul label to "Elen Malena Halvorsdatter Tunheim"
LAST	Lmul	"Elen Malena Halvorsdatter Tunheim"
#   add a mul alias "Elen Malena Halvorsdatter Mossige"
LAST	Amul	"Elen Malena Halvorsdatter Mossige"
#   set the ja label to "エレン・マレナ・ハルヴォルスダッテル・トゥンヘイム"
LAST	Lja	"エレン・マレナ・ハルヴォルスダッテル・トゥンヘイム"
#   set the zh label to "埃伦·马莱纳·哈尔沃尔斯达特·通海姆"
LAST	Lzh	"埃伦·马莱纳·哈尔沃尔斯达特·通海姆"
#   add a ja alias "エレン・マレナ・ハルヴォルスダッテル・モシゲ"
LAST	Aja	"エレン・マレナ・ハルヴォルスダッテル・モシゲ"
#   add a zh alias "埃伦·马莱纳·哈尔沃尔斯达特·莫西盖"
LAST	Azh	"埃伦·马莱纳·哈尔沃尔斯达特·莫西盖"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000029983713844 Elen Malena Halvorsdtr Tunheim, qualified P1810 subject named as Elen Malena Halvorsdtr Mossige
LAST	P2600	"6000000029983713844"	P1810	"Elen Malena Halvorsdtr Mossige"
#   P569 date of birth = +1800-00-00T00:00:00Z/9
LAST	P569	+1800-00-00T00:00:00Z/9	S2600	"6000000029983713844"
#   P570 date of death = +1879-04-21T00:00:00Z/11
LAST	P570	+1879-04-21T00:00:00Z/11	S2600	"6000000029983713844"
#   P40 child = Q141199826 Anna Maria Samuelsdtr. Tunheim
LAST	P40	Q141199826	S2600	"6000000029983713844"
#   Q141199826 Anna Maria Samuelsdtr. Tunheim: P25 mother = the item just created
Q141199826	P25	LAST	S2600	"6000000029983713844"
#   the item just created: P735 given name = Q11967041 Elen, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q11967041	P1545	"1"	P7452	Q3409033
#   P735 given name = Q5990536 Malena, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q5990536	P1545	"2"	P3831	Q245025
#   add a mul alias "Elen Malena Halvorsdtr Tunheim"
LAST	Amul	"Elen Malena Halvorsdtr Tunheim"

# create a new item
CREATE
#   set the en label to "Eva Carolina Leijonhufvud"
LAST	Len	"Eva Carolina Leijonhufvud"
#   set the mul label to "Eva Carolina Leijonhufvud"
LAST	Lmul	"Eva Carolina Leijonhufvud"
#   set the ja label to "エヴァ・カロリナ・レイヨンフフヴド"
LAST	Lja	"エヴァ・カロリナ・レイヨンフフヴド"
#   set the zh label to "埃瓦·卡罗利纳·莱伊永胡夫武德"
LAST	Lzh	"埃瓦·卡罗利纳·莱伊永胡夫武德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000011399293802 Eva Carolina Leijonhufvud, qualified P1810 subject named as Eva Carolina Leijonhufvud
LAST	P2600	"6000000011399293802"	P1810	"Eva Carolina Leijonhufvud"
#   P569 date of birth = +1771-05-01T00:00:00Z/11
LAST	P569	+1771-05-01T00:00:00Z/11	S2600	"6000000011399293802"
#   P570 date of death = +1855-02-17T00:00:00Z/11
LAST	P570	+1855-02-17T00:00:00Z/11	S2600	"6000000011399293802"
#   P26 spouse = Q6001589 Carl Stellan Mörner af Morlanda
LAST	P26	Q6001589	S2600	"6000000011399293802"
#   P40 child = Q19828095 Carl Mörner af Morlanda
LAST	P40	Q19828095	S2600	"6000000011399293802"
#   Q6001589 Carl Stellan Mörner af Morlanda: P26 spouse = the item just created
Q6001589	P26	LAST	S2600	"6000000011399293802"
#   Q19828095 Carl Mörner af Morlanda: P25 mother = the item just created
Q19828095	P25	LAST	S2600	"6000000011399293802"
#   the item just created: P735 given name = Q64412279 Eva, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q64412279	P1545	"1"	P7452	Q3409033
#   P735 given name = Q5044762 Carolina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q5044762	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Gunilla Margareta Frondin"
LAST	Len	"Gunilla Margareta Frondin"
#   set the mul label to "Gunilla Margareta Frondin"
LAST	Lmul	"Gunilla Margareta Frondin"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000011759927315 Gunilla Margareta Frondin, qualified P1810 subject named as Gunilla Margareta Frondin
LAST	P2600	"6000000011759927315"	P1810	"Gunilla Margareta Frondin"
#   P569 date of birth = +1757-00-00T00:00:00Z/9
LAST	P569	+1757-00-00T00:00:00Z/9	S2600	"6000000011759927315"
#   P570 date of death = +1783-02-01T00:00:00Z/11
LAST	P570	+1783-02-01T00:00:00Z/11	S2600	"6000000011759927315"
#   P22 father = Q5745627 Berge / Birger Frondin
LAST	P22	Q5745627	S2600	"6000000011759927315"
#   Q5745627 Berge / Birger Frondin: P40 child = the item just created
Q5745627	P40	LAST	S2600	"6000000011759927315"
#   the item just created: P735 given name = Q3909969 Gunilla, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q3909969	P1545	"1"	P7452	Q3409033
#   P735 given name = Q8274988 Margareta, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q8274988	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Harlverg B. Ekman"
LAST	Len	"Harlverg B. Ekman"
#   set the mul label to "Harlverg B. Ekman"
LAST	Lmul	"Harlverg B. Ekman"
#   set the ja label to "ハルルヴェルグ・ブ・エクマン"
LAST	Lja	"ハルルヴェルグ・ブ・エクマン"
#   set the zh label to "哈尔尔韦尔格·布·埃克曼"
LAST	Lzh	"哈尔尔韦尔格·布·埃克曼"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 285886949080005081 Harlverg B. Ekman, qualified P1810 subject named as Harlverg B. Ekman
LAST	P2600	"285886949080005081"	P1810	"Harlverg B. Ekman"
#   P22 father = Q141216640 Per Gustaf Ekman
LAST	P22	Q141216640	S2600	"285886949080005081"
#   P25 mother = Q141216639 Olufine Bergithe Ekman
LAST	P25	Q141216639	S2600	"285886949080005081"
#   Q141216640 Per Gustaf Ekman: P40 child = the item just created
Q141216640	P40	LAST	S2600	"285886949080005081"
#   Q141216639 Olufine Bergithe Ekman: P40 child = the item just created
Q141216639	P40	LAST	S2600	"285886949080005081"
#   the item just created: P735 given name = Q19803497 B., qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q19803497	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Harriet Lane Tunheim"
LAST	Len	"Harriet Lane Tunheim"
#   set the mul label to "Harriet Lane Tunheim"
LAST	Lmul	"Harriet Lane Tunheim"
#   add a mul alias "Harriet Berg"
LAST	Amul	"Harriet Berg"
#   set the ja label to "ハリエト・ラネ・トゥンヘイム"
LAST	Lja	"ハリエト・ラネ・トゥンヘイム"
#   set the zh label to "哈里埃特·拉内·通海姆"
LAST	Lzh	"哈里埃特·拉内·通海姆"
#   add a ja alias "ハリエト・ベルグ"
LAST	Aja	"ハリエト・ベルグ"
#   add a zh alias "哈里埃特·贝尔格"
LAST	Azh	"哈里埃特·贝尔格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000039510918938 Harriet Lane Tunheim, qualified P1810 subject named as Harriet Berg
LAST	P2600	"6000000039510918938"	P1810	"Harriet Berg"
#   P569 date of birth = +1921-05-26T00:00:00Z/11
LAST	P569	+1921-05-26T00:00:00Z/11	S2600	"6000000039510918938"
#   P570 date of death = +1996-11-26T00:00:00Z/11
LAST	P570	+1996-11-26T00:00:00Z/11	S2600	"6000000039510918938"
#   P26 spouse = Q141189101 Samuel Tunheim
LAST	P26	Q141189101	S2600	"6000000039510918938"
#   Q141189101 Samuel Tunheim: P26 spouse = the item just created
Q141189101	P26	LAST	S2600	"6000000039510918938"
#   the item just created: P735 given name = Q5486209 Harriet
LAST	P735	Q5486209
#   P734 family name = Q12785738 Berg, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q12785738	P3831	Q2507958
#   P734 family name = Q2754726 Lane, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q2754726	P3831	Q28418670

# create a new item
CREATE
#   set the en label to "Hedvig Swedenborg"
LAST	Len	"Hedvig Swedenborg"
#   set the mul label to "Hedvig Swedenborg"
LAST	Lmul	"Hedvig Swedenborg"
#   add a mul alias "Hedvig Behm"
LAST	Amul	"Hedvig Behm"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000006782610675 Hedvig Swedenborg, qualified P1810 subject named as Hedvig Behm
LAST	P2600	"6000000006782610675"	P1810	"Hedvig Behm"
#   P569 date of birth = +1690-11-30T00:00:00Z/11
LAST	P569	+1690-11-30T00:00:00Z/11	S2600	"6000000006782610675"
#   P570 date of death = +1728-12-19T00:00:00Z/11
LAST	P570	+1728-12-19T00:00:00Z/11	S2600	"6000000006782610675"
#   P26 spouse = Q5570928 Lars Benzelstierna
LAST	P26	Q5570928	S2600	"6000000006782610675"
#   P40 child = Q5570931 Lars Benzelstierna
LAST	P40	Q5570931	S2600	"6000000006782610675"
#   Q5570928 Lars Benzelstierna: P26 spouse = the item just created
Q5570928	P26	LAST	S2600	"6000000006782610675"
#   Q5570931 Lars Benzelstierna: P25 mother = the item just created
Q5570931	P25	LAST	S2600	"6000000006782610675"
#   the item just created: P735 given name = Q13648620 Hedvig
LAST	P735	Q13648620

# create a new item
CREATE
#   set the en label to "Isak Reinhold Sahlberg"
LAST	Len	"Isak Reinhold Sahlberg"
#   set the mul label to "Isak Reinhold Sahlberg"
LAST	Lmul	"Isak Reinhold Sahlberg"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 5580425653980118255 Isak Reinhold Sahlberg, qualified P1810 subject named as Isak Reinhold Sahlberg
LAST	P2600	"5580425653980118255"	P1810	"Isak Reinhold Sahlberg"
#   P569 date of birth = +1752-04-22T00:00:00Z/11
LAST	P569	+1752-04-22T00:00:00Z/11	S2600	"5580425653980118255"
#   P570 date of death = +1813-09-01T00:00:00Z/11
LAST	P570	+1813-09-01T00:00:00Z/11	S2600	"5580425653980118255"
#   P40 child = Q2361145 Carl Reinhold Sahlberg
LAST	P40	Q2361145	S2600	"5580425653980118255"
#   Q2361145 Carl Reinhold Sahlberg: P22 father = the item just created
Q2361145	P22	LAST	S2600	"5580425653980118255"
#   the item just created: P735 given name = Q18198729 Isak, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q18198729	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18091397 Reinhold, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q18091397	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Johanna Matilda Carlsdotter"
LAST	Len	"Johanna Matilda Carlsdotter"
#   set the mul label to "Johanna Matilda Carlsdotter"
LAST	Lmul	"Johanna Matilda Carlsdotter"
#   set the ja label to "ヨハナ・マチルダ・カルルスドッテル"
LAST	Lja	"ヨハナ・マチルダ・カルルスドッテル"
#   set the zh label to "约哈纳·玛蒂尔达·卡尔尔斯多特"
LAST	Lzh	"约哈纳·玛蒂尔达·卡尔尔斯多特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000177921458863 Johanna Matilda Carlsdotter, qualified P1810 subject named as Johanna Matilda Carlsdotter
LAST	P2600	"6000000177921458863"	P1810	"Johanna Matilda Carlsdotter"
#   P569 date of birth = +1866-03-15T00:00:00Z/11
LAST	P569	+1866-03-15T00:00:00Z/11	S2600	"6000000177921458863"
#   P570 date of death = +1933-05-08T00:00:00Z/11
LAST	P570	+1933-05-08T00:00:00Z/11	S2600	"6000000177921458863"
#   P25 mother = Q141219160 Christina, Sofia Carlsdotter
LAST	P25	Q141219160	S2600	"6000000177921458863"
#   Q141219160 Christina, Sofia Carlsdotter: P40 child = the item just created
Q141219160	P40	LAST	S2600	"6000000177921458863"

# create a new item
CREATE
#   the item just created: set the en label to "Lovisa Catharina Polviander"
LAST	Len	"Lovisa Catharina Polviander"
#   set the mul label to "Lovisa Catharina Polviander"
LAST	Lmul	"Lovisa Catharina Polviander"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 5580429510180056637 Lovisa Catharina Polviander, qualified P1810 subject named as Lovisa Catharina Polviander
LAST	P2600	"5580429510180056637"	P1810	"Lovisa Catharina Polviander"
#   P569 date of birth = +1755-05-23T00:00:00Z/11
LAST	P569	+1755-05-23T00:00:00Z/11	S2600	"5580429510180056637"
#   P570 date of death = +1798-03-28T00:00:00Z/11
LAST	P570	+1798-03-28T00:00:00Z/11	S2600	"5580429510180056637"
#   P40 child = Q2361145 Carl Reinhold Sahlberg
LAST	P40	Q2361145	S2600	"5580429510180056637"
#   Q2361145 Carl Reinhold Sahlberg: P25 mother = the item just created
Q2361145	P25	LAST	S2600	"5580429510180056637"
#   the item just created: P735 given name = Q10570000 Lovisa, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q10570000	P1545	"1"	P7452	Q3409033
#   P735 given name = Q17317997 Catharina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q17317997	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Magdalena Elisabet Tersmeden"
LAST	Len	"Magdalena Elisabet Tersmeden"
#   set the mul label to "Magdalena Elisabet Tersmeden"
LAST	Lmul	"Magdalena Elisabet Tersmeden"
#   set the ja label to "マグダレーナ・エリサベート・テルスメデン"
LAST	Lja	"マグダレーナ・エリサベート・テルスメデン"
#   set the zh label to "玛格达莱娜·伊丽莎白·特尔斯梅登"
LAST	Lzh	"玛格达莱娜·伊丽莎白·特尔斯梅登"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000002811030244 Magdalena Elisabet Tersmeden, qualified P1810 subject named as Magdalena Elisabet Tersmeden
LAST	P2600	"6000000002811030244"	P1810	"Magdalena Elisabet Tersmeden"
#   P569 date of birth = +1753-08-19T00:00:00Z/11
LAST	P569	+1753-08-19T00:00:00Z/11	S2600	"6000000002811030244"
#   P570 date of death = +1794-10-29T00:00:00Z/11
LAST	P570	+1794-10-29T00:00:00Z/11	S2600	"6000000002811030244"
#   P26 spouse = Q943803 Uno von Troil
LAST	P26	Q943803	S2600	"6000000002811030244"
#   Q943803 Uno von Troil: P26 spouse = the item just created
Q943803	P26	LAST	S2600	"6000000002811030244"
#   the item just created: P735 given name = Q842544 Magdalena, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q842544	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16423275 Elisabet, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q16423275	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Magdalena Sofia Falkenberg af Bålby"
LAST	Len	"Magdalena Sofia Falkenberg af Bålby"
#   set the mul label to "Magdalena Sofia Falkenberg af Bålby"
LAST	Lmul	"Magdalena Sofia Falkenberg af Bålby"
#   add a mul alias "Magdalena Sofia Falkenberg"
LAST	Amul	"Magdalena Sofia Falkenberg"
#   set the ja label to "マグダレーナ・ソフィア・ファルケンベルグ・アフ・ボールビ"
LAST	Lja	"マグダレーナ・ソフィア・ファルケンベルグ・アフ・ボールビ"
#   set the zh label to "玛格达莱娜·索菲阿·法尔肯贝尔格·阿夫·博尔比"
LAST	Lzh	"玛格达莱娜·索菲阿·法尔肯贝尔格·阿夫·博尔比"
#   add a ja alias "マグダレーナ・ソフィア・ファルケンベルグ"
LAST	Aja	"マグダレーナ・ソフィア・ファルケンベルグ"
#   add a zh alias "玛格达莱娜·索菲阿·法尔肯贝尔格"
LAST	Azh	"玛格达莱娜·索菲阿·法尔肯贝尔格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000008889736689 Magdalena Sofia Falkenberg af Bålby, qualified P1810 subject named as Magdalena Sofia Falkenberg
LAST	P2600	"6000000008889736689"	P1810	"Magdalena Sofia Falkenberg"
#   P569 date of birth = +1763-04-27T00:00:00Z/11
LAST	P569	+1763-04-27T00:00:00Z/11	S2600	"6000000008889736689"
#   P570 date of death = +1834-01-22T00:00:00Z/11
LAST	P570	+1834-01-22T00:00:00Z/11	S2600	"6000000008889736689"
#   P26 spouse = Q5931099 Israel Lagerfelt
LAST	P26	Q5931099	S2600	"6000000008889736689"
#   Q5931099 Israel Lagerfelt: P26 spouse = the item just created
Q5931099	P26	LAST	S2600	"6000000008889736689"
#   the item just created: P735 given name = Q842544 Magdalena, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q842544	P1545	"1"	P7452	Q3409033
#   P734 family name = Q16869887 Falkenberg, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q16869887	P3831	Q2507958
#   P734 family name = Q16869887 Falkenberg, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q16869887	P3831	Q28418670

# create a new item
CREATE
#   set the en label to "Ola Taraldsen Trevland"
LAST	Len	"Ola Taraldsen Trevland"
#   set the mul label to "Ola Taraldsen Trevland"
LAST	Lmul	"Ola Taraldsen Trevland"
#   set the ja label to "オーラ・タラルドセン・トレヴランド"
LAST	Lja	"オーラ・タラルドセン・トレヴランド"
#   set the zh label to "乌拉·塔拉尔德森·特雷夫兰德"
LAST	Lzh	"乌拉·塔拉尔德森·特雷夫兰德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000226904207910 Ola Taraldsen Trevland, qualified P1810 subject named as Ola Taraldsen Trevland
LAST	P2600	"6000000226904207910"	P1810	"Ola Taraldsen Trevland"
#   P569 date of birth = +1520-00-00T00:00:00Z/9
LAST	P569	+1520-00-00T00:00:00Z/9	S2600	"6000000226904207910"
#   P570 date of death = +1604-00-00T00:00:00Z/9
LAST	P570	+1604-00-00T00:00:00Z/9	S2600	"6000000226904207910"
#   P40 child = Q141205938 Ranveig Olsd Trevland
LAST	P40	Q141205938	S2600	"6000000226904207910"
#   Q141205938 Ranveig Olsd Trevland: P22 father = the item just created
Q141205938	P22	LAST	S2600	"6000000226904207910"
#   the item just created: P735 given name = Q96675523 Ola
LAST	P735	Q96675523
#   add a mul alias "Ola Trevland"
LAST	Amul	"Ola Trevland"

# create a new item
CREATE
#   set the en label to "Osmund Larsson Nese"
LAST	Len	"Osmund Larsson Nese"
#   set the mul label to "Osmund Larsson Nese"
LAST	Lmul	"Osmund Larsson Nese"
#   set the ja label to "オスムンド・ラーション・ネセ"
LAST	Lja	"オスムンド・ラーション・ネセ"
#   set the zh label to "奥斯蒙德·拉尔松·内塞"
LAST	Lzh	"奥斯蒙德·拉尔松·内塞"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000002744891329 Osmund Larsson Nese, qualified P1810 subject named as Osmund Larsson Nese
LAST	P2600	"6000000002744891329"	P1810	"Osmund Larsson Nese"
#   P569 date of birth = +1787-00-00T00:00:00Z/9
LAST	P569	+1787-00-00T00:00:00Z/9	S2600	"6000000002744891329"
#   P570 date of death = +1884-09-18T00:00:00Z/11
LAST	P570	+1884-09-18T00:00:00Z/11	S2600	"6000000002744891329"
#   P22 father = Q141219063 Lars Osmundsen Nese
LAST	P22	Q141219063	S2600	"6000000002744891329"
#   Q141219063 Lars Osmundsen Nese: P40 child = the item just created
Q141219063	P40	LAST	S2600	"6000000002744891329"

# create a new item
CREATE
#   the item just created: set the en label to "Samuel Aslakson Tunheim"
LAST	Len	"Samuel Aslakson Tunheim"
#   set the mul label to "Samuel Aslakson Tunheim"
LAST	Lmul	"Samuel Aslakson Tunheim"
#   set the ja label to "サムエル・アスラクソン・トゥンヘイム"
LAST	Lja	"サムエル・アスラクソン・トゥンヘイム"
#   set the zh label to "萨穆埃尔·阿斯拉克松·通海姆"
LAST	Lzh	"萨穆埃尔·阿斯拉克松·通海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000011971496046 Samuel Aslakson Tunheim, qualified P1810 subject named as Samuel Aslakson Tunheim
LAST	P2600	"6000000011971496046"	P1810	"Samuel Aslakson Tunheim"
#   P569 date of birth = +1795-00-00T00:00:00Z/9
LAST	P569	+1795-00-00T00:00:00Z/9	S2600	"6000000011971496046"
#   P570 date of death = +1879-05-24T00:00:00Z/11
LAST	P570	+1879-05-24T00:00:00Z/11	S2600	"6000000011971496046"
#   P40 child = Q141199826 Anna Maria Samuelsdtr. Tunheim
LAST	P40	Q141199826	S2600	"6000000011971496046"
#   Q141199826 Anna Maria Samuelsdtr. Tunheim: P22 father = the item just created
Q141199826	P22	LAST	S2600	"6000000011971496046"
#   the item just created: P735 given name = Q629347 Samuel
LAST	P735	Q629347
#   add a mul alias "Samuel Tunheim"
LAST	Amul	"Samuel Tunheim"

# create a new item
CREATE
#   set the en label to "Tore Underberge III"
LAST	Len	"Tore Underberge III"
#   set the mul label to "Tore Underberge III"
LAST	Lmul	"Tore Underberge III"
#   set the ja label to "トレ・ウンデルベルゲ・イイイ"
LAST	Lja	"トレ・ウンデルベルゲ・イイイ"
#   set the zh label to "托雷·温德尔贝尔盖·伊伊伊"
LAST	Lzh	"托雷·温德尔贝尔盖·伊伊伊"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005607672589 Tore Underberge III, qualified P1810 subject named as Tore Underberge, III
LAST	P2600	"6000000005607672589"	P1810	"Tore Underberge, III"
#   P569 date of birth = +1427-00-00T00:00:00Z/9
LAST	P569	+1427-00-00T00:00:00Z/9	S2600	"6000000005607672589"
#   P570 date of death = +1480-00-00T00:00:00Z/9
LAST	P570	+1480-00-00T00:00:00Z/9	S2600	"6000000005607672589"
#   P22 father = Q141205942 Tore II Gardson Gard
LAST	P22	Q141205942	S2600	"6000000005607672589"
#   Q141205942 Tore II Gardson Gard: P40 child = the item just created
Q141205942	P40	LAST	S2600	"6000000005607672589"

# create a new item
CREATE
#   the item just created: set the en label to "Ulrika Danielsdotter Djurberg"
LAST	Len	"Ulrika Danielsdotter Djurberg"
#   set the mul label to "Ulrika Danielsdotter Djurberg"
LAST	Lmul	"Ulrika Danielsdotter Djurberg"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000009988670487 Ulrika Danielsdotter Djurberg, qualified P1810 subject named as Ulrika Danielsdotter Djurberg
LAST	P2600	"6000000009988670487"	P1810	"Ulrika Danielsdotter Djurberg"
#   P569 date of birth = +1703-09-12T00:00:00Z/11
LAST	P569	+1703-09-12T00:00:00Z/11	S2600	"6000000009988670487"
#   P570 date of death = +1778-10-11T00:00:00Z/11
LAST	P570	+1778-10-11T00:00:00Z/11	S2600	"6000000009988670487"
#   P26 spouse = Q5783613 Engelbert Hallenius Biskop i Skara
LAST	P26	Q5783613	S2600	"6000000009988670487"
#   Q5783613 Engelbert Hallenius Biskop i Skara: P26 spouse = the item just created
Q5783613	P26	LAST	S2600	"6000000009988670487"
#   the item just created: P735 given name = Q18924998 Ulrika
LAST	P735	Q18924998
#   P5056 patronym or matronym = Q140226461
LAST	P5056	Q140226461
#   add a mul alias "Ulrika Djurberg"
LAST	Amul	"Ulrika Djurberg"

# create a new item
CREATE
#   set the en label to "Ulrika Lovisa Victorin"
LAST	Len	"Ulrika Lovisa Victorin"
#   set the mul label to "Ulrika Lovisa Victorin"
LAST	Lmul	"Ulrika Lovisa Victorin"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000006198882015 Ulrika Lovisa Victorin, qualified P1810 subject named as Ulrika Lovisa Victorin
LAST	P2600	"6000000006198882015"	P1810	"Ulrika Lovisa Victorin"
#   P569 date of birth = +1756-12-19T00:00:00Z/11
LAST	P569	+1756-12-19T00:00:00Z/11	S2600	"6000000006198882015"
#   P570 date of death = +1825-06-03T00:00:00Z/11
LAST	P570	+1825-06-03T00:00:00Z/11	S2600	"6000000006198882015"
#   P26 spouse = Q5797554 Detlof Heijkenskjöld
LAST	P26	Q5797554	S2600	"6000000006198882015"
#   P40 child = Q4953277 Margareta Charlotta Heijkenskjöld
LAST	P40	Q4953277	S2600	"6000000006198882015"
#   Q5797554 Detlof Heijkenskjöld: P26 spouse = the item just created
Q5797554	P26	LAST	S2600	"6000000006198882015"
#   the item just created: P735 given name = Q18924998 Ulrika, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q18924998	P1545	"1"	P7452	Q3409033
#   P735 given name = Q10570000 Lovisa, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q10570000	P1545	"2"	P3831	Q245025
#   Q141219324 Sofia Maria Mannerheim: P25 mother = Q141219332 Sofia Wadenstierna
Q141219324	P25	Q141219332	S2600	"6000000000047205391"
#   Q141219332 Sofia Wadenstierna: P40 child = Q141219324 Sofia Maria Mannerheim
Q141219332	P40	Q141219324	S2600	"6000000000047255126"
#   Q141219316 Reiar Einarsen Kydland: P26 spouse = Q141219269 Kari Tollaksdatter Kartevoll
Q141219316	P26	Q141219269	S2600	"6000000000496970049"
#   Q141189104 Siri Kristine Ivarsdatter Garborg: P40 child = Q139651594 Sigrid Garborg
Q141189104	P40	Q139651594	S2600	"6000000002954315535"
#   Q141219336 Tore Sebjørnsson Talgje, d.y: P25 mother = Q141200101 Sissel Jonsdatter Talje
Q141219336	P25	Q141200101	S2600	"6000000003043756033"
#   Q141200101 Sissel Jonsdatter Talje: P40 child = Q141219336 Tore Sebjørnsson Talgje, d.y
Q141200101	P40	Q141219336	S2600	"6000000003043806217"
#   Q141219227 Gitlaug Knutsdatter Garborg: P26 spouse = Q141219189 Eivind Svenson Sveinsen Garborg
Q141219227	P26	Q141219189	S2600	"6000000003491951383"
#   Q141152614 Jon Eivindson Garborg: P40 child = Q139651594 Sigrid Garborg
Q141152614	P40	Q139651594	S2600	"6000000003492005126"
#   Q141219189 Eivind Svenson Sveinsen Garborg: P26 spouse = Q141219227 Gitlaug Knutsdatter Garborg
Q141219189	P26	Q141219227	S2600	"6000000003492077372"
#   Q141219269 Kari Tollaksdatter Kartevoll: P26 spouse = Q141219316 Reiar Einarsen Kydland
Q141219269	P26	Q141219316	S2600	"6000000005606851268"
#   Q141219065 Marta Torbjørnsdotter Gjesdal: P40 child = Q141219250 Inger Sørensdatter Lima
Q141219065	P40	Q141219250	S2600	"6000000005607335640"
#   Q141219291 Maria Hansdatter Austrått: P26 spouse = Q141219349 Tørres Jonson Grannes
Q141219291	P26	Q141219349	S2600	"6000000005607475201"
#   Q141219349 Tørres Jonson Grannes: P26 spouse = Q141219291 Maria Hansdatter Austrått
Q141219349	P26	Q141219291	S2600	"6000000005608892520"
#   Q141168837 Ingebret Inge Garborg: P735 given name = Q8085241 Inge, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141168837	P735	Q8085241	P1545	"2"	P3831	Q245025
#   Q141219136 Amalia Charlotta Ehrenpreus: P40 child = Q141219155 Christina Maria Adelheim
Q141219136	P40	Q141219155	S2600	"6000000019041477898"
#   Q141219356 Ulrika Charlotta Klingenstierna: P40 child = Q141219214 Erik Samuel Fant
Q141219356	P40	Q141219214	S2600	"6000000019344079214"
#   Q141219155 Christina Maria Adelheim: P25 mother = Q141219136 Amalia Charlotta Ehrenpreus
Q141219155	P25	Q141219136	S2600	"6000000019413110402"
#   Q141219214 Erik Samuel Fant: P25 mother = Q141219356 Ulrika Charlotta Klingenstierna
Q141219214	P25	Q141219356	S2600	"6000000166407230823"
#   Q141219148 Carl Ersson: P40 child = Q141219160 Christina, Sofia Carlsdotter
Q141219148	P40	Q141219160	S2600	"6000000177920129826"
#   Q141219160 Christina, Sofia Carlsdotter: P22 father = Q141219148 Carl Ersson
Q141219160	P22	Q141219148	S2600	"6000000177921459033"
#   Q109660986 Eva Walaas: P735 given name = Q64412279 Eva
Q109660986	P735	Q64412279

