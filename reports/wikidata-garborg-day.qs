# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   822 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   Q141216357 Anders Jacobsson: set the zh label to "安德斯·雅各布松"
Q141216357	Lzh	"安德斯·雅各布松"
#   Q141205902 Daniel Olofsson: set the ja label to "ダニエル・オロフソン"
Q141205902	Lja	"ダニエル・オロフソン"
#   set the zh label to "丹尼尔·奥洛夫松"
Q141205902	Lzh	"丹尼尔·奥洛夫松"
#   Q141216611 Jon Villumson Raunes: set the ja label to "ジョン・ヴィルムソン・ラウネス"
Q141216611	Lja	"ジョン・ヴィルムソン・ラウネス"
#   set the zh label to "乔恩·维卢姆松·拉乌内斯"
Q141216611	Lzh	"乔恩·维卢姆松·拉乌内斯"
#   Q141205909 Gudrun Sæbjørnsdatter Talgje: set the ja label to "グドルーン・セブヨルンスダッテル・タルイェ"
Q141205909	Lja	"グドルーン・セブヨルンスダッテル・タルイェ"
#   set the zh label to "古德龙·塞布约尔恩斯达特·塔尔耶"
Q141205909	Lzh	"古德龙·塞布约尔恩斯达特·塔尔耶"
#   Q19061035 Guttorm Àsulfsson à Rein: set the ja label to "グットルム・アスルフソン・ア・レイン"
Q19061035	Lja	"グットルム・アスルフソン・ア・レイン"
#   set the zh label to "古托尔姆·阿苏尔夫松·阿·赖因"
Q19061035	Lzh	"古托尔姆·阿苏尔夫松·阿·赖因"
#   Q6057321 Olof Andersson Pryss: set the ja label to "オロフ・アンデション・プリス"
Q6057321	Lja	"オロフ・アンデション・プリス"
#   set the zh label to "奥洛夫·安德松·普里斯"
Q6057321	Lzh	"奥洛夫·安德松·普里斯"
#   Q26405863 Olof Engelbertsson Bure: set the ja label to "オロフ・エンゲルベルトソン・ブレ"
Q26405863	Lja	"オロフ・エンゲルベルトソン・ブレ"
#   set the zh label to "奥洛夫·恩盖尔贝尔特松·布雷"
Q26405863	Lzh	"奥洛夫·恩盖尔贝尔特松·布雷"
#   Q5548897 Gregorius Aminoff: set the ja label to "グレゴリウス・アミノフ"
Q5548897	Lja	"グレゴリウス・アミノフ"
#   set the zh label to "格雷戈里乌斯·阿米诺夫"
Q5548897	Lzh	"格雷戈里乌斯·阿米诺夫"

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
#   the item just created: P735 given name = Q666578 Anna
LAST	P735	Q666578

# create a new item
CREATE
#   set the en label to "Augusta Ulrika Mannerheim"
LAST	Len	"Augusta Ulrika Mannerheim"
#   set the mul label to "Augusta Ulrika Mannerheim"
LAST	Lmul	"Augusta Ulrika Mannerheim"
#   set the ja label to "オーガスタ・ウルリカ・マンネルヘイム"
LAST	Lja	"オーガスタ・ウルリカ・マンネルヘイム"
#   set the zh label to "奧古斯塔·乌尔里卡·曼纳海姆"
LAST	Lzh	"奧古斯塔·乌尔里卡·曼纳海姆"
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
#   set the ja label to "エレン・マレーナ・ハルヴォルスダッテル・トゥンヘイム"
LAST	Lja	"エレン・マレーナ・ハルヴォルスダッテル・トゥンヘイム"
#   set the zh label to "埃伦·马莱纳·哈尔沃尔斯达特·通海姆"
LAST	Lzh	"埃伦·马莱纳·哈尔沃尔斯达特·通海姆"
#   add a ja alias "エレン・マレーナ・ハルヴォルスダッテル・モシゲ"
LAST	Aja	"エレン・マレーナ・ハルヴォルスダッテル・モシゲ"
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
#   P734 family name = Q30229737, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q30229737	P3831	Q2507958
#   P734 family name = Q36927172, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q36927172	P3831	Q28418670
#   add a mul alias "Elen Malena Halvorsdtr Tunheim"
LAST	Amul	"Elen Malena Halvorsdtr Tunheim"

# create a new item
CREATE
#   set the en label to "Eva Carolina Leijonhufvud"
LAST	Len	"Eva Carolina Leijonhufvud"
#   set the mul label to "Eva Carolina Leijonhufvud"
LAST	Lmul	"Eva Carolina Leijonhufvud"
#   set the ja label to "エヴァ・カロリーナ・レイヨンフフヴド"
LAST	Lja	"エヴァ・カロリーナ・レイヨンフフヴド"
#   set the zh label to "伊娃·卡罗琳娜·莱伊永胡夫武德"
LAST	Lzh	"伊娃·卡罗琳娜·莱伊永胡夫武德"
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
#   set the ja label to "ハリエット・レーン・トゥンヘイム"
LAST	Lja	"ハリエット・レーン・トゥンヘイム"
#   set the zh label to "哈丽雅特·莱恩·通海姆"
LAST	Lzh	"哈丽雅特·莱恩·通海姆"
#   add a ja alias "ハリエット・ベルク"
LAST	Aja	"ハリエット・ベルク"
#   add a zh alias "哈丽雅特·伯格"
LAST	Azh	"哈丽雅特·伯格"
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
#   P734 family name = Q36927172, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q36927172	P3831	Q28418670

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
#   set the ja label to "ヨハンナ・マティルダ・カルルスドッテル"
LAST	Lja	"ヨハンナ・マティルダ・カルルスドッテル"
#   set the zh label to "约翰娜·玛蒂尔达·卡尔尔斯多特"
LAST	Lzh	"约翰娜·玛蒂尔达·卡尔尔斯多特"
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
#   set the ja label to "マグダレーナ・エリーザベト・テルスメデン"
LAST	Lja	"マグダレーナ・エリーザベト・テルスメデン"
#   set the zh label to "马格达莱纳·伊丽莎白·特尔斯梅登"
LAST	Lzh	"马格达莱纳·伊丽莎白·特尔斯梅登"
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
#   set the zh label to "马格达莱纳·索菲娅·法尔肯贝尔格·阿夫·博尔比"
LAST	Lzh	"马格达莱纳·索菲娅·法尔肯贝尔格·阿夫·博尔比"
#   add a ja alias "マグダレーナ・ソフィア・ファルケンベルグ"
LAST	Aja	"マグダレーナ・ソフィア・ファルケンベルグ"
#   add a zh alias "马格达莱纳·索菲娅·法尔肯贝尔格"
LAST	Azh	"马格达莱纳·索菲娅·法尔肯贝尔格"
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
#   P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q18201520	P1545	"2"	P3831	Q245025
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
#   set the zh label to "奥拉·塔拉尔德森·特雷夫兰德"
LAST	Lzh	"奥拉·塔拉尔德森·特雷夫兰德"
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
#   set the zh label to "奥斯蒙德·拉森·内塞"
LAST	Lzh	"奥斯蒙德·拉森·内塞"
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
#   set the ja label to "サミュエル・アスラクソン・トゥンヘイム"
LAST	Lja	"サミュエル・アスラクソン・トゥンヘイム"
#   set the zh label to "塞缪尔·阿斯拉克松·通海姆"
LAST	Lzh	"塞缪尔·阿斯拉克松·通海姆"
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
#   P734 family name = Q36927172
LAST	P734	Q36927172
#   add a mul alias "Samuel Tunheim"
LAST	Amul	"Samuel Tunheim"

# create a new item
CREATE
#   set the en label to "Tore Underberge III"
LAST	Len	"Tore Underberge III"
#   set the mul label to "Tore Underberge III"
LAST	Lmul	"Tore Underberge III"
#   set the ja label to "トーレ・ウンデルベルゲ・イイイ"
LAST	Lja	"トーレ・ウンデルベルゲ・イイイ"
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
#   Q141219059 Gustava Maria Sofia Mannerheim: P735 given name = Q325872 Maria, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141219059	P735	Q325872	P1545	"2"	P3831	Q245025
#   P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q141219059	P735	Q18201520	P1545	"3"	P3831	Q245025
#   Q141219324 Sofia Maria Mannerheim: P25 mother = Q141219332 Sofia Wadenstierna
Q141219324	P25	Q141219332	S2600	"6000000000047205391"
#   P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141219324	P735	Q18201520	P1545	"1"	P7452	Q3409033
#   P735 given name = Q325872 Maria, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141219324	P735	Q325872	P1545	"2"	P3831	Q245025
#   Q141219332 Sofia Wadenstierna: P40 child = Q141219324 Sofia Maria Mannerheim
Q141219332	P40	Q141219324	S2600	"6000000000047255126"
#   P735 given name = Q18201520 Sofia
Q141219332	P735	Q18201520
#   Q141219316 Reiar Einarsen Kydland: P26 spouse = Q141219269 Kari Tollaksdatter Kartevoll
Q141219316	P26	Q141219269	S2600	"6000000000496970049"
#   P734 family name = Q30514142
Q141219316	P734	Q30514142
#   Q141205922 Marit Ormsd Byre: P734 family name = Q37515983
Q141205922	P734	Q37515983
#   Q141199851 Lagmann Gunnbjørn Toresson Tengs: P735 given name = Q136849653, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141199851	P735	Q136849653	P1545	"2"	P3831	Q245025
#   P734 family name = Q55233230
Q141199851	P734	Q55233230
#   Q141206061 Cecilie Olsdatter Håland: P734 family name = Q30580079
Q141206061	P734	Q30580079
#   Q141205942 Tore II Gardson Gard: P734 family name = Q37475140
Q141205942	P734	Q37475140
#   Q141217384 David Tjølson Edland: P734 family name = Q31454737
Q141217384	P734	Q31454737
#   Q141216602 Berta Guria Davidsdatter Stokka: P734 family name = Q37033285
Q141216602	P734	Q37033285
#   Q141216653 Torger Torgerson Stokka: P734 family name = Q37033285
Q141216653	P734	Q37033285
#   Q141198422 Iver Pedersen Sandsmark: P734 family name = Q37541803
Q141198422	P734	Q37541803
#   Q141198414 Ingeborg Olsdatter Sandsmark: P734 family name = Q37541803
Q141198414	P734	Q37541803
#   Q141189104 Siri Kristine Ivarsdatter Garborg: P40 child = Q139651594 Sigrid Garborg
Q141189104	P40	Q139651594	S2600	"6000000002954315535"
#   Q141198396 Erling Juel Wendt: P735 given name = Q123820113, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141198396	P735	Q123820113	P1545	"2"	P3831	Q245025
#   Q141219336 Tore Sebjørnsson Talgje, d.y: P25 mother = Q141200101 Sissel Jonsdatter Talje
Q141219336	P25	Q141200101	S2600	"6000000003043756033"
#   Q141200101 Sissel Jonsdatter Talje: P40 child = Q141219336 Tore Sebjørnsson Talgje, d.y
Q141200101	P40	Q141219336	S2600	"6000000003043806217"
#   Q141198382 Berita Larsdatter Rossavik: P734 family name = Q122838342
Q141198382	P734	Q122838342
#   Q141189055 Astri Torkelsdatter Gilja: P734 family name = Q122836259
Q141189055	P734	Q122836259
#   Q141216471 Gunnbjørn Gunnbjørnson Rossavik: P735 given name = Q136849653
Q141216471	P735	Q136849653
#   P734 family name = Q122838342
Q141216471	P734	Q122838342
#   Q141198435 Jon Nilsson Espedal: P734 family name = Q27892902
Q141198435	P734	Q27892902
#   Q141198503 Tore Erikson Håland: P734 family name = Q30580079
Q141198503	P734	Q30580079
#   Q141200094 Siri Rasmusdtr. Erevik: P734 family name = Q35855266
Q141200094	P734	Q35855266
#   Q141199819 Anna Andersdotter: P735 given name = Q666578 Anna
Q141199819	P735	Q666578
#   Q141216644 Rasmus Asbjørnson Nedre Rossavik: P734 family name = Q122838342
Q141216644	P734	Q122838342
#   Q141205930 Olav Knutson Randa Håland: P734 family name = Q30580079
Q141205930	P734	Q30580079
#   Q141216487 Knut Johanson Håland: P734 family name = Q30580079
Q141216487	P734	Q30580079
#   Q141216489 Laurits Leivson Bjørheim: P734 family name = Q30834379
Q141216489	P734	Q30834379
#   Q141216638 Olaug Jonsdatter Heigre: P734 family name = Q45305861
Q141216638	P734	Q45305861
#   Q141219299 Per Asbjørnson Stokka: P734 family name = Q37033285
Q141219299	P734	Q37033285
#   Q141216637 Ola Person Persson Heigre: P734 family name = Q45305861
Q141216637	P734	Q45305861
#   Q141219227 Gitlaug Knutsdatter Garborg: P26 spouse = Q141219189 Eivind Svenson Sveinsen Garborg
Q141219227	P26	Q141219189	S2600	"6000000003491951383"
#   Q141205914 Inger (Ingrid) Osmundsdatter Risa: P734 family name = Q36931214
Q141205914	P734	Q36931214
#   Q141216387 Johannes Svensen Obrestad: P734 family name = Q40353802
Q141216387	P734	Q40353802
#   Q141199892 Jon Olsen Heigre: P734 family name = Q45305861
Q141199892	P734	Q45305861
#   Q141216365 Berte Karine Jonsdatter Stokka: P734 family name = Q37033285
Q141216365	P734	Q37033285
#   Q141216510 Torger Torgerson Stokka: P734 family name = Q37033285
Q141216510	P734	Q37033285
#   Q141189070 John Jonassen Hegre: P735 given name = Q4925477 John
Q141189070	P735	Q4925477
#   P734 family name = Q36955626
Q141189070	P734	Q36955626
#   Q141189098 Rakel Jonasdatter Heigre: P734 family name = Q45305861
Q141189098	P734	Q45305861
#   Q141216635 Martha Eivindsdatter Heigre: P735 given name = Q16279062
Q141216635	P735	Q16279062
#   P734 family name = Q45305861
Q141216635	P734	Q45305861
#   Q141216643 Ragna Enevaldsdatter Heigre: P734 family name = Q45305861
Q141216643	P734	Q45305861
#   Q141178381 Marta Jonsdatter Li: P734 family name = Q686223 Li
Q141178381	P734	Q686223
#   Q141205921 Maria Jonsdatter Lura: P735 given name = Q325872 Maria
Q141205921	P735	Q325872
#   P734 family name = Q37303374
Q141205921	P734	Q37303374
#   Q141216594 Ane Maria Olsdatter Vestre Stangaland: P735 given name = Q325872 Maria, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141216594	P735	Q325872	P1545	"2"	P3831	Q245025
#   Q141152614 Jon Eivindson Garborg: P40 child = Q139651594 Sigrid Garborg
Q141152614	P40	Q139651594	S2600	"6000000003492005126"
#   Q141162043 Inger Marie Mary Eivindsdatter Ronneberg: P735 given name = Q734578 Mary, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q141162043	P735	Q734578	P1545	"3"	P3831	Q245025
#   Q141162046 Ane Oline Lena Eivindsdatter Tunheim: P735 given name = Q654581 Lena, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q141162046	P735	Q654581	P1545	"3"	P3831	Q245025
#   Q141169072 Ådne Olsen Garborg: P735 given name = Q12011446
Q141169072	P735	Q12011446
#   Q141189066 Helge Rasmusson Bø: P734 family name = Q30253098
Q141189066	P734	Q30253098
#   Q141216407 Torkel Torbjørnson Høyland: P734 family name = Q27888882
Q141216407	P734	Q27888882
#   Q141219189 Eivind Svenson Sveinsen Garborg: P26 spouse = Q141219227 Gitlaug Knutsdatter Garborg
Q141219189	P26	Q141219227	S2600	"6000000003492077372"
#   Q141198370 NN Skårland: P734 family name = Q40480033
Q141198370	P734	Q40480033
#   Q141198375 Astri Torchelsdatter Øvre Time: P734 family name = Q37494555
Q141198375	P734	Q37494555
#   Q141216356 NN Undheim: P734 family name = Q27888846
Q141216356	P734	Q27888846
#   Q141216598 Anna Ivarsd Stokka: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141216598	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P734 family name = Q37033285
Q141216598	P734	Q37033285
#   Q141199704 Andreas Olai: P735 given name = Q4926263 Andreas
Q141199704	P735	Q4926263
#   Q141180413 Thomas Matthiæ: P735 given name = Q16428906
Q141180413	P735	Q16428906
#   Q141216495 NN (Frille): P734 family name = Q54366191
Q141216495	P734	Q54366191
#   Q141199862 Helga Bjørnsdatter Tengs: P734 family name = Q55233230
Q141199862	P734	Q55233230
#   Q141219176 Eivind Ogmundsson Byre på Høyland: P734 family name = Q27888882
Q141219176	P734	Q27888882
#   Q141216377 Hanna Sofie Wendt: P735 given name = Q1554377 Hannah, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141216377	P735	Q1554377	P1545	"1"	P7452	Q3409033
#   Q141219269 Kari Tollaksdatter Kartevoll: P26 spouse = Q141219316 Reiar Einarsen Kydland
Q141219269	P26	Q141219316	S2600	"6000000005606851268"
#   Q141216488 Lars Jonsen Landsnes: P734 family name = Q122837341
Q141216488	P734	Q122837341
#   Q141216632 Magdalena Lauritsd Hogganvik: P734 family name = Q55240992
Q141216632	P734	Q55240992
#   Q141216396 Lisbet Olavsdatter Håland: P734 family name = Q30580079
Q141216396	P734	Q30580079
#   Q141219065 Marta Torbjørnsdotter Gjesdal: P40 child = Q141219250 Inger Sørensdatter Lima
Q141219065	P40	Q141219250	S2600	"6000000005607335640"
#   Q141198834 Gunnbjørn Jonson Mjølhus: P735 given name = Q136849653
Q141198834	P735	Q136849653
#   Q141216613 Karen Henriksdotter Raunes Våga: P735 given name = Q1221747 Karen, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141216613	P735	Q1221747	P1545	"1"	P7452	Q3409033
#   P734 family name = Q40306448
Q141216613	P734	Q40306448
#   Q141216384 Ingeborg Eriksdatter Time: P734 family name = Q37494555
Q141216384	P734	Q37494555
#   Q141168827 Hans Eivind Garborg: P735 given name = Q632842, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141168827	P735	Q632842	P1545	"1"	P7452	Q3409033
#   Q141219291 Maria Hansdatter Austrått: P26 spouse = Q141219349 Tørres Jonson Grannes
Q141219291	P26	Q141219349	S2600	"6000000005607475201"
#   P735 given name = Q325872 Maria
Q141219291	P735	Q325872
#   Q141205919 Malena Hansdatter Bø: P734 family name = Q30253098
Q141205919	P734	Q30253098
#   Q141219349 Tørres Jonson Grannes: P26 spouse = Q141219291 Maria Hansdatter Austrått
Q141219349	P26	Q141219291	S2600	"6000000005608892520"
#   P735 given name = Q12008164
Q141219349	P735	Q12008164
#   Q141205898 Anna Tormodsdatter Mele: P735 given name = Q666578 Anna
Q141205898	P735	Q666578
#   Q141219060 Halvor Johannesson Hobberstad: P734 family name = Q40703807
Q141219060	P734	Q40703807
#   Q141217369 Anna Osmundsd Stokka: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141217369	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P734 family name = Q37033285
Q141217369	P734	Q37033285
#   Q141198371 Anna Belestdatter Lauvsnes: P735 given name = Q666578 Anna
Q141198371	P735	Q666578
#   Q141189071 Joren Jonsdatter Espedal: P735 given name = Q2554259
Q141189071	P735	Q2554259
#   P734 family name = Q27892902
Q141189071	P734	Q27892902
#   Q141180408 Jon Larsson Mæle: P734 family name = Q34190986
Q141180408	P734	Q34190986
#   Q141180412 Marta Rasmusdatter Li: P734 family name = Q686223 Li
Q141180412	P734	Q686223
#   Q141216645 Reiar Reiersen Kydland: P734 family name = Q30514142
Q141216645	P734	Q30514142
#   Q141216609 Inger Kristoffersdatter Skårland: P734 family name = Q40480033
Q141216609	P734	Q40480033
#   Q141219051 Anna Börjesdotter Bothniensis: P735 given name = Q666578 Anna
Q141219051	P735	Q666578
#   Q141205900 Bertrand Olav Olsen Vigdel: P735 given name = Q3637880, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141205900	P735	Q3637880	P1545	"1"	P7452	Q3409033
#   Q141205938 Ranveig Olsd Trevland: P735 given name = Q30836047, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141205938	P735	Q30836047	P1545	"1"	P7452	Q3409033
#   Q141168837 Ingebret Inge Garborg: P735 given name = Q8085241 Inge, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141168837	P735	Q8085241	P1545	"2"	P3831	Q245025
#   Q141205911 Hans Svensen Risa I: P735 given name = Q632842, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141205911	P735	Q632842	P1545	"1"	P7452	Q3409033
#   Q141200074 Rasmus Olsen Bø: P734 family name = Q30253098
Q141200074	P734	Q30253098
#   Q141189088 Ola Knutsen Grøtheim: P734 family name = Q122836435
Q141189088	P734	Q122836435
#   Q141199809 Ane Marie Helgesdatter Bø: P734 family name = Q30253098
Q141199809	P734	Q30253098
#   Q141217387 Ivar Stokka: P734 family name = Q37033285
Q141217387	P734	Q37033285
#   Q141198755 Anna Ingebretsdatter Voster: P735 given name = Q666578 Anna
Q141198755	P735	Q666578
#   Q141198751 Lars Person Nedre Rossavik: P734 family name = Q122838342
Q141198751	P734	Q122838342
#   Q141216483 Karen Malena Rasmusdatter Tjelta: P735 given name = Q1221747 Karen, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141216483	P735	Q1221747	P1545	"1"	P7452	Q3409033
#   P734 family name = Q38898383
Q141216483	P734	Q38898383
#   Q141189069 Ingeborg Ådnesdatter Grøtheim: P734 family name = Q122836435
Q141189069	P734	Q122836435
#   Q141199830 Anna Rasmusdatter Grøtheim: P735 given name = Q666578 Anna
Q141199830	P735	Q666578
#   P734 family name = Q122836435
Q141199830	P734	Q122836435
#   Q141216600 Astrid Omundsdatter Grøtheim: P734 family name = Q122836435
Q141216600	P734	Q122836435
#   Q141216380 Hans Olsen Grøtheim: P735 given name = Q632842
Q141216380	P735	Q632842
#   P734 family name = Q122836435
Q141216380	P734	Q122836435
#   Q141216382 Helge Asbjørnsen Bø: P734 family name = Q30253098
Q141216382	P734	Q30253098
#   Q141217394 Margareta Christina von Numers: P735 given name = Q1083457 Christina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141217394	P735	Q1083457	P1545	"2"	P3831	Q245025
#   Q141216599 Anna Rasmusdatter Nedre Rossavik: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141216599	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P734 family name = Q122838342
Q141216599	P734	Q122838342
#   Q141216381 Hans Rasmussen Låge-Håland: P735 given name = Q632842
Q141216381	P735	Q632842
#   Q141216607 Hans Erikson Øvre Håland: P735 given name = Q632842, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141216607	P735	Q632842	P1545	"1"	P7452	Q3409033
#   P734 family name = Q30580079
Q141216607	P734	Q30580079
#   Q141216498 Norman Charles Tunheim: P734 family name = Q36927172
Q141216498	P734	Q36927172
#   Q141219284 Maria Benjaminsdotter: P735 given name = Q325872 Maria
Q141219284	P735	Q325872
#   Q141216595 Anna Danielsdotter: P735 given name = Q666578 Anna
Q141216595	P735	Q666578
#   Q141219202 Elen Kristoffersdotter Nese: P734 family name = Q37543374
Q141219202	P734	Q37543374
#   Q141217359 Anna Elisabet Angerstein: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141217359	P735	Q666578	P1545	"1"	P7452	Q3409033
#   Q141189083 Martha Elida Frenning: P735 given name = Q16279062, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141189083	P735	Q16279062	P1545	"1"	P7452	Q3409033
#   Q141216383 Ingeborg Eriksdatter Bjorland: P734 family name = Q123200450
Q141216383	P734	Q123200450
#   Q141216490 Malli Svensdatter Lura: P735 given name = Q106145589
Q141216490	P735	Q106145589
#   P734 family name = Q37303374
Q141216490	P734	Q37303374
#   Q141216481 Jon Tørresson Soma: P734 family name = Q37104818
Q141216481	P734	Q37104818
#   Q141219070 Tørres Jonsson Vatne: P735 given name = Q12008164
Q141219070	P735	Q12008164
#   Q141216400 Margreta Lauritsdatter Øvre Bjørheim: P734 family name = Q30834379
Q141216400	P734	Q30834379
#   Q141205895 Andreas Christiansen: P735 given name = Q4926263 Andreas
Q141205895	P735	Q4926263
#   Q141216401 Mariet Danielsdotter: P735 given name = Q117599926
Q141216401	P735	Q117599926
#   Q141205896 Ane Marie Konstanse Amanda Kristine Hegre: P735 given name = Q19572240, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q141205896	P735	Q19572240	P1545	"3"	P3831	Q245025
#   P734 family name = Q36955626
Q141205896	P734	Q36955626
#   Q141219136 Amalia Charlotta Ehrenpreus: P40 child = Q141219155 Christina Maria Adelheim
Q141219136	P40	Q141219155	S2600	"6000000019041477898"
#   Q141219356 Ulrika Charlotta Klingenstierna: P40 child = Q141219214 Erik Samuel Fant
Q141219356	P40	Q141219214	S2600	"6000000019344079214"
#   Q141189084 Martin Tollefson Tunheim: P734 family name = Q36927172
Q141189084	P734	Q36927172
#   Q141219155 Christina Maria Adelheim: P25 mother = Q141219136 Amalia Charlotta Ehrenpreus
Q141219155	P25	Q141219136	S2600	"6000000019413110402"
#   P735 given name = Q1083457 Christina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141219155	P735	Q1083457	P1545	"1"	P7452	Q3409033
#   P735 given name = Q325872 Maria, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141219155	P735	Q325872	P1545	"2"	P3831	Q245025
#   Q141199930 Knut Olsen Gudmestad: P734 family name = Q37015437
Q141199930	P734	Q37015437
#   Q141198441 Kirsten Olsdatter Grøtheim: P734 family name = Q122836435
Q141198441	P734	Q122836435
#   Q141189065 Gustav Adolf Gundersen: P735 given name = Q746076, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141189065	P735	Q746076	P1545	"1"	P7452	Q3409033
#   Q141216386 Jens Wilhelm Wendt: P735 given name = Q11027623, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141216386	P735	Q11027623	P1545	"2"	P3831	Q245025
#   Q141189090 Ole Christopher Christiansen: P735 given name = Q1084472 Christopher, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141189090	P735	Q1084472	P1545	"2"	P3831	Q245025
#   Q141189099 Rasmus Helgesen Bø: P734 family name = Q30253098
Q141189099	P734	Q30253098
#   Q141219050 Ane Olsdatter Bø: P734 family name = Q30253098
Q141219050	P734	Q30253098
#   Q141199909 Karen Sophie Pedersdatter: P735 given name = Q1221747 Karen, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141199909	P735	Q1221747	P1545	"1"	P7452	Q3409033
#   Q138474188 Hans Syvertsen Nyvold: P735 given name = Q632842
Q138474188	P735	Q632842
#   Q141216505 Thekla Cecilie Dybo: P735 given name = Q21147318 Thekla, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141216505	P735	Q21147318	P1545	"1"	P7452	Q3409033
#   Q141189111 Tørres Jonasson Hegre: P735 given name = Q12008164
Q141189111	P735	Q12008164
#   P734 family name = Q36955626
Q141189111	P734	Q36955626
#   Q141217398 Måns Moge: P734 family name = Q12796950
Q141217398	P734	Q12796950
#   Q141217396 Maria No name: P735 given name = Q325872 Maria, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141217396	P735	Q325872	P1545	"1"	P7452	Q3409033
#   P735 given name = Q21148356, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141217396	P735	Q21148356	P1545	"2"	P3831	Q245025
#   Q141199822 Anna Jönsdotter: P735 given name = Q666578 Anna
Q141199822	P735	Q666578
#   Q141189058 Brita Thomasdotter: P735 given name = Q918013
Q141189058	P735	Q918013
#   Q141199826 Anna Maria Samuelsdtr. Tunheim: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141199826	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P735 given name = Q325872 Maria, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141199826	P735	Q325872	P1545	"2"	P3831	Q245025
#   P734 family name = Q36927172
Q141199826	P734	Q36927172
#   Q141200112 Tollef Pederson Tunheim: P734 family name = Q36927172
Q141200112	P734	Q36927172
#   Q141216494 N.N. Jacobsdtr. Koll: P734 family name = Q21510541
Q141216494	P734	Q21510541
#   Q141189105 Sophia Birgitta Gundersen: P735 given name = Q2302787 Sophia, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141189105	P735	Q2302787	P1545	"1"	P7452	Q3409033
#   Q141189052 Anna Carine Gundersen: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141189052	P735	Q666578	P1545	"1"	P7452	Q3409033
#   Q141198472 Olga E. Garborg Oswald: P735 given name = Q20187, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141198472	P735	Q20187	P1545	"1"	P7452	Q3409033
#   Q141219052 Anna Olsdatter Heigre: P735 given name = Q666578 Anna
Q141219052	P735	Q666578
#   P734 family name = Q45305861
Q141219052	P734	Q45305861
#   Q141199992 Myrtle Lenora Tunheim: P734 family name = Q36927172
Q141199992	P734	Q36927172
#   Q141216405 Tabite Tollefsdotter Tunheim: P734 family name = Q36927172
Q141216405	P734	Q36927172
#   Q141205918 Mabel Tunheim: P734 family name = Q36927172
Q141205918	P734	Q36927172
#   Q141199833 Bertha Ingeborg Tunheim: P734 family name = Q36927172
Q141199833	P734	Q36927172
#   Q141189107 Theodore Roosevelt Tunheim: P734 family name = Q36927172
Q141189107	P734	Q36927172
#   Q141189102 Sigrid Sally Manilva Ekman: P735 given name = Q19816532 Sally, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141189102	P735	Q19816532	P1545	"2"	P3831	Q245025
#   Q141189074 Joseph Tunheim: P734 family name = Q36927172
Q141189074	P734	Q36927172
#   Q141189049 Alfred Tunheim: P734 family name = Q36927172
Q141189049	P734	Q36927172
#   Q141200084 Selma Johanna Tunheim: P734 family name = Q36927172
Q141200084	P734	Q36927172
#   Q141189101 Samuel Tunheim: P734 family name = Q36927172
Q141189101	P734	Q36927172
#   Q141189095 Peter Tunheim: P734 family name = Q36927172
Q141189095	P734	Q36927172
#   Q141189109 Tollef Bud Tunheim: P734 family name = Q36927172
Q141189109	P734	Q36927172
#   Q141199836 Florence June Tunheim Cosman: P735 given name = Q1152453 June, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141199836	P735	Q1152453	P1545	"2"	P3831	Q245025
#   Q141205894 Agnes Tunheim: P734 family name = Q36927172
Q141205894	P734	Q36927172
#   Q141216458 Asbjørn Gunnarson Bø: P734 family name = Q30253098
Q141216458	P734	Q30253098
#   Q141216456 Anna Helgesdotter Opstad: P735 given name = Q666578 Anna
Q141216456	P735	Q666578
#   Q141216468 Erik Hansson Gausland: P734 family name = Q132192515
Q141216468	P734	Q132192515
#   Q141219063 Lars Osmundsen Nese: P734 family name = Q37543374
Q141219063	P734	Q37543374
#   Q141199918 Kirsten Hansdatter Grøtheim: P734 family name = Q122836435
Q141199918	P734	Q122836435
#   Q141219214 Erik Samuel Fant: P25 mother = Q141219356 Ulrika Charlotta Klingenstierna
Q141219214	P25	Q141219356	S2600	"6000000166407230823"
#   Q141216363 Anne Govertsdtr. Bratland: P735 given name = Q564684 Anne, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141216363	P735	Q564684	P1545	"1"	P7452	Q3409033
#   Q141219148 Carl Ersson: P40 child = Q141219160 Christina, Sofia Carlsdotter
Q141219148	P40	Q141219160	S2600	"6000000177920129826"
#   Q141219160 Christina, Sofia Carlsdotter: P22 father = Q141219148 Carl Ersson
Q141219160	P22	Q141219148	S2600	"6000000177921459033"
#   P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141219160	P735	Q18201520	P1545	"2"	P3831	Q245025
#   Q141198399 Eugene LeRoy Tunheim: P735 given name = Q545971, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141198399	P735	Q545971	P1545	"1"	P7452	Q3409033
#   P735 given name = Q19839067 Leroy, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141198399	P735	Q19839067	P1545	"2"	P3831	Q245025
#   P734 family name = Q36927172
Q141198399	P734	Q36927172
#   Q141219164 David Robert Tunheim: P735 given name = Q4927937 Robert, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141219164	P735	Q4927937	P1545	"2"	P3831	Q245025
#   P734 family name = Q36927172
Q141219164	P734	Q36927172
#   Q141189054 Anna Maria Helgesdatter Bø: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141189054	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P735 given name = Q325872 Maria, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141189054	P735	Q325872	P1545	"2"	P3831	Q245025
#   P734 family name = Q30253098
Q141189054	P734	Q30253098
#   Q141189113 Ådne Helgesen Bø: P735 given name = Q12011446
Q141189113	P735	Q12011446
#   P734 family name = Q30253098
Q141189113	P734	Q30253098
#   Q141217392 Larine Eriksdatter Heigre: P734 family name = Q45305861
Q141217392	P734	Q45305861
#   Q141217390 Johan Johannessen Obrestad: P734 family name = Q40353802
Q141217390	P734	Q40353802
#   Q141206056 Asbjørn Helgesen Bø: P734 family name = Q30253098
Q141206056	P734	Q30253098
#   Q141216379 Hans Halvardsen Grøtheim: P735 given name = Q632842
Q141216379	P735	Q632842
#   P734 family name = Q122836435
Q141216379	P734	Q122836435
#   Q141216374 Halvard Assersen Grøtheim: P734 family name = Q122836435
Q141216374	P734	Q122836435
#   Q141200127 Ådne Hansen Grøtheim: P735 given name = Q12011446
Q141200127	P735	Q12011446
#   P734 family name = Q122836435
Q141200127	P734	Q122836435
#   Q141216608 Hans Ådnesen Grøtheim: P735 given name = Q632842
Q141216608	P735	Q632842
#   P734 family name = Q122836435
Q141216608	P734	Q122836435
#   Q109660986 Eva Walaas: P735 given name = Q64412279 Eva
Q109660986	P735	Q64412279

