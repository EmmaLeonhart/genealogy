# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   979 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   Q141224780 Johan Falkenberg af Trystorp: add a mul alias "Johan von Mentzer"
Q141224780	Amul	"Johan von Mentzer"
#   Q141224008 Gjøa Gunnbjørnsdatter Nedre Rossavik: add a mul alias "Gjøa Gunnbjørnsdatter Gunnbjørnsdatter"
Q141224008	Amul	"Gjøa Gunnbjørnsdatter Gunnbjørnsdatter"
#   Q141223846 Marit Bjørnsdatter Bjorland: add a mul alias "Marit Bjørnsdatter Hognestad"
Q141223846	Amul	"Marit Bjørnsdatter Hognestad"
#   Q141178200 Inger Kristoffersdatter: set the zh label to "英格·克里斯托弗斯达特"
Q141178200	Lzh	"英格·克里斯托弗斯达特"
#   Q141180408 Jon Larsson Mæle: add a mul alias "Jon Larson Mæle"
Q141180408	Amul	"Jon Larson Mæle"
#   Q141180412 Marta Rasmusdatter Li: add a mul alias "Marta Rasmusdatter Høle"
Q141180412	Amul	"Marta Rasmusdatter Høle"
#   Q141205916 Kari Olsdatter: set the ja label to "カリ・オルスダッテル"
Q141205916	Lja	"カリ・オルスダッテル"
#   set the zh label to "卡里·奥尔斯达特"
Q141205916	Lzh	"卡里·奥尔斯达特"
#   Q141216645 Reiar Reiersen Kydland: set the zh label to "雷伊阿尔·雷伊埃尔森·基德兰德"
Q141216645	Lzh	"雷伊阿尔·雷伊埃尔森·基德兰德"
#   Q141216609 Inger Kristoffersdatter Skårland: set the zh label to "英格·克里斯托弗斯达特·斯科尔兰德"
Q141216609	Lzh	"英格·克里斯托弗斯达特·斯科尔兰德"
#   Q28467896 Erik Knudsen til Skarsholm: add a mul alias "Erik Knudsen"
Q28467896	Amul	"Erik Knudsen"
#   set the mul label to "Erik Knudsen of Sønderhalland"
Q28467896	Lmul	"Erik Knudsen of Sønderhalland"
#   Q141205923 Mathilde Fredrikke Thams: set the ja label to "マティルデ・フレドリケ・タムス"
Q141205923	Lja	"マティルデ・フレドリケ・タムス"
#   set the zh label to "玛蒂尔德·夫雷德里凯·塔姆斯"
Q141205923	Lzh	"玛蒂尔德·夫雷德里凯·塔姆斯"
#   Q19842232 Algot Bryniolfsson: add a mul alias "Algot Bryniolfsson"
Q19842232	Amul	"Algot Bryniolfsson"

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Anna Nilsdotter"
LAST	Len	"Anna Nilsdotter"
#   set the mul label to "Anna Nilsdotter"
LAST	Lmul	"Anna Nilsdotter"
#   set the ja label to "アンナ・ニルスドッテル"
LAST	Lja	"アンナ・ニルスドッテル"
#   set the zh label to "安娜·尼尔斯多特"
LAST	Lzh	"安娜·尼尔斯多特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000011078617825 Anna Nilsdotter, qualified P1810 subject named as Anna Nilsdotter
LAST	P2600	"6000000011078617825"	P1810	"Anna Nilsdotter"
#   P569 date of birth = +1736-00-00T00:00:00Z/9
LAST	P569	+1736-00-00T00:00:00Z/9	S2600	"6000000011078617825"
#   P570 date of death = +1799-00-00T00:00:00Z/9
LAST	P570	+1799-00-00T00:00:00Z/9	S2600	"6000000011078617825"
#   P40 child = Q141219284 Maria Benjaminsdotter
LAST	P40	Q141219284	S2600	"6000000011078617825"
#   Q141219284 Maria Benjaminsdotter: P25 mother = the item just created
Q141219284	P25	LAST	S2600	"6000000011078617825"

# create a new item
CREATE
#   the item just created: set the en label to "Bellest Aslaksen Lauvsnes"
LAST	Len	"Bellest Aslaksen Lauvsnes"
#   set the mul label to "Bellest Aslaksen Lauvsnes"
LAST	Lmul	"Bellest Aslaksen Lauvsnes"
#   add a mul alias "Bellest Aslaksen Bu"
LAST	Amul	"Bellest Aslaksen Bu"
#   set the ja label to "ベレスト・アスラクセン・ラウヴスネス"
LAST	Lja	"ベレスト・アスラクセン・ラウヴスネス"
#   set the zh label to "贝莱斯特·阿斯拉克森·拉乌夫斯内斯"
LAST	Lzh	"贝莱斯特·阿斯拉克森·拉乌夫斯内斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000008686123397 Bellest Aslaksen Lauvsnes, qualified P1810 subject named as Bellest Aslaksen Bu
LAST	P2600	"6000000008686123397"	P1810	"Bellest Aslaksen Bu"
#   P569 date of birth = +1570-00-00T00:00:00Z/9
LAST	P569	+1570-00-00T00:00:00Z/9	S2600	"6000000008686123397"
#   P570 date of death = +1644-00-00T00:00:00Z/9
LAST	P570	+1644-00-00T00:00:00Z/9	S2600	"6000000008686123397"
#   P40 child = Q141224746 Bellest Bellestsen Lauvsnes d.e.
LAST	P40	Q141224746	S2600	"6000000008686123397"
#   Q141224746 Bellest Bellestsen Lauvsnes d.e.: P22 father = the item just created
Q141224746	P22	LAST	S2600	"6000000008686123397"
#   the item just created: P734 family name = Q4097588 Bu, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q4097588	P3831	Q2507958
#   add a mul alias "Bellest Lauvsnes"
LAST	Amul	"Bellest Lauvsnes"

# create a new item
CREATE
#   set the en label to "Benjamin Mårtensson"
LAST	Len	"Benjamin Mårtensson"
#   set the mul label to "Benjamin Mårtensson"
LAST	Lmul	"Benjamin Mårtensson"
#   set the ja label to "ベンジャミン・モールテンソン"
LAST	Lja	"ベンジャミン・モールテンソン"
#   set the zh label to "本杰明·莫尔滕松"
LAST	Lzh	"本杰明·莫尔滕松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000011078886609 Benjamin Mårtensson, qualified P1810 subject named as Benjamin Mårtensson
LAST	P2600	"6000000011078886609"	P1810	"Benjamin Mårtensson"
#   P569 date of birth = +1738-12-04T00:00:00Z/11
LAST	P569	+1738-12-04T00:00:00Z/11	S2600	"6000000011078886609"
#   P570 date of death = +1806-00-00T00:00:00Z/9
LAST	P570	+1806-00-00T00:00:00Z/9	S2600	"6000000011078886609"
#   P40 child = Q141219284 Maria Benjaminsdotter
LAST	P40	Q141219284	S2600	"6000000011078886609"
#   Q141219284 Maria Benjaminsdotter: P22 father = the item just created
Q141219284	P22	LAST	S2600	"6000000011078886609"

# create a new item
CREATE
#   the item just created: set the en label to "Berta Pedersdatter Stangeland"
LAST	Len	"Berta Pedersdatter Stangeland"
#   set the mul label to "Berta Pedersdatter Stangeland"
LAST	Lmul	"Berta Pedersdatter Stangeland"
#   add a mul alias "Berta Pedersdatter Pedersdatter"
LAST	Amul	"Berta Pedersdatter Pedersdatter"
#   set the ja label to "ベルタ・ペーデシュダッテル・スタンゲラン"
LAST	Lja	"ベルタ・ペーデシュダッテル・スタンゲラン"
#   set the zh label to "贝尔塔·佩德斯达特·斯坦格兰"
LAST	Lzh	"贝尔塔·佩德斯达特·斯坦格兰"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005102264552 Berta Pedersdatter Stangeland, qualified P1810 subject named as Berta Pedersdatter Pedersdatter
LAST	P2600	"6000000005102264552"	P1810	"Berta Pedersdatter Pedersdatter"
#   P569 date of birth = +1692-00-00T00:00:00Z/9
LAST	P569	+1692-00-00T00:00:00Z/9	S2600	"6000000005102264552"
#   P570 date of death = +1736-00-00T00:00:00Z/9
LAST	P570	+1736-00-00T00:00:00Z/9	S2600	"6000000005102264552"
#   P40 child = Q141200028 Per Jonson Øksnevad
LAST	P40	Q141200028	S2600	"6000000005102264552"
#   Q141200028 Per Jonson Øksnevad: P25 mother = the item just created
Q141200028	P25	LAST	S2600	"6000000005102264552"
#   the item just created: P735 given name = Q4092653 Berta
LAST	P735	Q4092653
#   P734 family name = Q21452049 Stangeland, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q21452049	P3831	Q28418670
#   add a mul alias "Berta Stangeland"
LAST	Amul	"Berta Stangeland"

# create a new item
CREATE
#   set the en label to "Brynhilda Toresdatter Underberge"
LAST	Len	"Brynhilda Toresdatter Underberge"
#   set the mul label to "Brynhilda Toresdatter Underberge"
LAST	Lmul	"Brynhilda Toresdatter Underberge"
#   set the ja label to "ブリンヒルダ・トーレスダッテル・ウンデルベルゲ"
LAST	Lja	"ブリンヒルダ・トーレスダッテル・ウンデルベルゲ"
#   set the zh label to "布林希尔达·托雷斯达特·温德尔贝尔盖"
LAST	Lzh	"布林希尔达·托雷斯达特·温德尔贝尔盖"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000076909442440 Brynhilda Toresdatter Underberge, qualified P1810 subject named as Brynhilda Toresdatter Underberge
LAST	P2600	"6000000076909442440"	P1810	"Brynhilda Toresdatter Underberge"
#   P569 date of birth = +1457-00-00T00:00:00Z/9
LAST	P569	+1457-00-00T00:00:00Z/9	S2600	"6000000076909442440"
#   P22 father = Q141223436 Tore Underberge III
LAST	P22	Q141223436	S2600	"6000000076909442440"
#   Q141223436 Tore Underberge III: P40 child = the item just created
Q141223436	P40	LAST	S2600	"6000000076909442440"

# create a new item
CREATE
#   the item just created: set the en label to "Charlotta Catharina Hård af Segerstad"
LAST	Len	"Charlotta Catharina Hård af Segerstad"
#   set the mul label to "Charlotta Catharina Hård af Segerstad"
LAST	Lmul	"Charlotta Catharina Hård af Segerstad"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000006127417435 Charlotta Catharina Hård af Segerstad, qualified P1810 subject named as Charlotta Catharina Hård af Segerstad
LAST	P2600	"6000000006127417435"	P1810	"Charlotta Catharina Hård af Segerstad"
#   P569 date of birth = +1760-12-09T00:00:00Z/11
LAST	P569	+1760-12-09T00:00:00Z/11	S2600	"6000000006127417435"
#   P570 date of death = +1836-01-08T00:00:00Z/11
LAST	P570	+1836-01-08T00:00:00Z/11	S2600	"6000000006127417435"
#   P26 spouse = Q5575580 Gustaf Ture Bielke
LAST	P26	Q5575580	S2600	"6000000006127417435"
#   Q5575580 Gustaf Ture Bielke: P26 spouse = the item just created
Q5575580	P26	LAST	S2600	"6000000006127417435"
#   the item just created: P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q1067071	P1545	"1"	P7452	Q3409033
#   P735 given name = Q17317997 Catharina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q17317997	P1545	"2"	P3831	Q245025
#   P734 family name = Q27888722 Hård
LAST	P734	Q27888722
#   add a mul alias "Charlotta Katarina Hård af Segerstad"
LAST	Amul	"Charlotta Katarina Hård af Segerstad"

# create a new item
CREATE
#   set the en label to "Elis Michael Fant"
LAST	Len	"Elis Michael Fant"
#   set the mul label to "Elis Michael Fant"
LAST	Lmul	"Elis Michael Fant"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000019467957450 Elis Michael Fant, qualified P1810 subject named as Elis Michael Fant
LAST	P2600	"6000000019467957450"	P1810	"Elis Michael Fant"
#   P569 date of birth = +1787-08-21T00:00:00Z/11
LAST	P569	+1787-08-21T00:00:00Z/11	S2600	"6000000019467957450"
#   P570 date of death = +1845-06-21T00:00:00Z/11
LAST	P570	+1845-06-21T00:00:00Z/11	S2600	"6000000019467957450"
#   P22 father = Q5725105 Eric Michael Fant
LAST	P22	Q5725105	S2600	"6000000019467957450"
#   P25 mother = Q141223729 Christina Brigitta Rydberg
LAST	P25	Q141223729	S2600	"6000000019467957450"
#   Q5725105 Eric Michael Fant: P40 child = the item just created
Q5725105	P40	LAST	S2600	"6000000019467957450"
#   Q141223729 Christina Brigitta Rydberg: P40 child = the item just created
Q141223729	P40	LAST	S2600	"6000000019467957450"
#   the item just created: P735 given name = Q12788312 Elis, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q12788312	P1545	"1"	P7452	Q3409033
#   P735 given name = Q4927524, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q4927524	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Ers"
LAST	Len	"Ers"
#   set the mul label to "Ers"
LAST	Lmul	"Ers"
#   set the ja label to "エルス"
LAST	Lja	"エルス"
#   set the zh label to "埃尔斯"
LAST	Lzh	"埃尔斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000177943460822 Ers, qualified P1810 subject named as Ers
LAST	P2600	"6000000177943460822"	P1810	"Ers"
#   P40 child = Q141219148 Carl Ersson
LAST	P40	Q141219148	S2600	"6000000177943460822"
#   Q141219148 Carl Ersson: P22 father = the item just created
Q141219148	P22	LAST	S2600	"6000000177943460822"

# create a new item
CREATE
#   the item just created: set the en label to "Hans Olofsson Törne"
LAST	Len	"Hans Olofsson Törne"
#   set the mul label to "Hans Olofsson Törne"
LAST	Lmul	"Hans Olofsson Törne"
#   set the ja label to "ハンス・オロフソン・トルネ"
LAST	Lja	"ハンス・オロフソン・トルネ"
#   set the zh label to "汉斯·奥洛夫松·托尔内"
LAST	Lzh	"汉斯·奥洛夫松·托尔内"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000000410600770 Hans Olofsson Törne, qualified P1810 subject named as Hans Olofsson Törne
LAST	P2600	"6000000000410600770"	P1810	"Hans Olofsson Törne"
#   P569 date of birth = +1612-08-00T00:00:00Z/10
LAST	P569	+1612-08-00T00:00:00Z/10	S2600	"6000000000410600770"
#   P570 date of death = +1671-03-09T00:00:00Z/11
LAST	P570	+1671-03-09T00:00:00Z/11	S2600	"6000000000410600770"
#   P40 child = Q141223930 Magdalena Törne
LAST	P40	Q141223930	S2600	"6000000000410600770"
#   Q141223930 Magdalena Törne: P22 father = the item just created
Q141223930	P22	LAST	S2600	"6000000000410600770"
#   the item just created: P735 given name = Q632842
LAST	P735	Q632842
#   P734 family name = Q65202241 Törne
LAST	P734	Q65202241
#   add a mul alias "Hans Törne"
LAST	Amul	"Hans Törne"

# create a new item
CREATE
#   set the en label to "Ingeborg Marie Eriksdatter Håland"
LAST	Len	"Ingeborg Marie Eriksdatter Håland"
#   set the mul label to "Ingeborg Marie Eriksdatter Håland"
LAST	Lmul	"Ingeborg Marie Eriksdatter Håland"
#   add a mul alias "Ingeborg Marie Eriksdatter Stangeland"
LAST	Amul	"Ingeborg Marie Eriksdatter Stangeland"
#   set the ja label to "インゲボルグ・マリー・エリクスダッテル・ホーランド"
LAST	Lja	"インゲボルグ・マリー・エリクスダッテル・ホーランド"
#   set the zh label to "英格堡·玛丽·埃里克斯达特·霍兰"
LAST	Lzh	"英格堡·玛丽·埃里克斯达特·霍兰"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000023248630216 Ingeborg Marie Eriksdatter Håland, qualified P1810 subject named as Ingeborg Marie Eriksdatter Stangeland
LAST	P2600	"6000000023248630216"	P1810	"Ingeborg Marie Eriksdatter Stangeland"
#   P569 date of birth = +1833-11-10T00:00:00Z/11
LAST	P569	+1833-11-10T00:00:00Z/11	S2600	"6000000023248630216"
#   P570 date of death = +1860-07-11T00:00:00Z/11
LAST	P570	+1860-07-11T00:00:00Z/11	S2600	"6000000023248630216"
#   P22 father = Q141198393 Erik Erikson Stangeland
LAST	P22	Q141198393	S2600	"6000000023248630216"
#   P25 mother = Q141198454 Lisabeth Larsdotter Stangeland
LAST	P25	Q141198454	S2600	"6000000023248630216"
#   Q141198393 Erik Erikson Stangeland: P40 child = the item just created
Q141198393	P40	LAST	S2600	"6000000023248630216"
#   Q141198454 Lisabeth Larsdotter Stangeland: P40 child = the item just created
Q141198454	P40	LAST	S2600	"6000000023248630216"
#   the item just created: P735 given name = Q656590 Ingeborg, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q656590	P1545	"1"	P7452	Q3409033
#   P735 given name = Q106674406 Marie, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q106674406	P1545	"2"	P3831	Q245025
#   P5056 patronym or matronym = Q141223487, qualified P144 based on Q141198393 Erik Erikson Stangeland
LAST	P5056	Q141223487	P144	Q141198393
#   P734 family name = Q21452049 Stangeland, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q21452049	P3831	Q2507958
#   P734 family name = Q30580079, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q30580079	P3831	Q28418670
#   add a mul alias "Ingeborg Marie Håland"
LAST	Amul	"Ingeborg Marie Håland"

# create a new item
CREATE
#   set the en label to "Jacob Andersson"
LAST	Len	"Jacob Andersson"
#   set the mul label to "Jacob Andersson"
LAST	Lmul	"Jacob Andersson"
#   set the ja label to "ジェイコブ・アンデション"
LAST	Lja	"ジェイコブ・アンデション"
#   set the zh label to "雅各布·安德松"
LAST	Lzh	"雅各布·安德松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000001144914191 Jacob Andersson, qualified P1810 subject named as Jacob Andersson
LAST	P2600	"6000000001144914191"	P1810	"Jacob Andersson"
#   P569 date of birth = +1456-00-00T00:00:00Z/9
LAST	P569	+1456-00-00T00:00:00Z/9	S2600	"6000000001144914191"
#   P570 date of death = +1535-00-00T00:00:00Z/9
LAST	P570	+1535-00-00T00:00:00Z/9	S2600	"6000000001144914191"
#   P40 child = Q141216357 Anders Jacobsson
LAST	P40	Q141216357	S2600	"6000000001144914191"
#   Q141216357 Anders Jacobsson: P22 father = the item just created
Q141216357	P22	LAST	S2600	"6000000001144914191"

# create a new item
CREATE
#   the item just created: set the en label to "John David af Sandeberg"
LAST	Len	"John David af Sandeberg"
#   set the mul label to "John David af Sandeberg"
LAST	Lmul	"John David af Sandeberg"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000006127147759 John David af Sandeberg, qualified P1810 subject named as John David af Sandeberg
LAST	P2600	"6000000006127147759"	P1810	"John David af Sandeberg"
#   P569 date of birth = +1788-08-03T00:00:00Z/11
LAST	P569	+1788-08-03T00:00:00Z/11	S2600	"6000000006127147759"
#   P570 date of death = +1866-05-02T00:00:00Z/11
LAST	P570	+1866-05-02T00:00:00Z/11	S2600	"6000000006127147759"
#   P26 spouse = Q141219155 Christina Maria Adelheim
LAST	P26	Q141219155	S2600	"6000000006127147759"
#   P40 child = Q141223918 Hedvig Vendela Maria af Sandeberg
LAST	P40	Q141223918	S2600	"6000000006127147759"
#   Q141219155 Christina Maria Adelheim: P26 spouse = the item just created
Q141219155	P26	LAST	S2600	"6000000006127147759"
#   Q141223918 Hedvig Vendela Maria af Sandeberg: P22 father = the item just created
Q141223918	P22	LAST	S2600	"6000000006127147759"
#   the item just created: P735 given name = Q4925477 John, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q4925477	P1545	"1"	P7452	Q3409033
#   P735 given name = Q29937870 David, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q29937870	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Jon Rasmusson Grude"
LAST	Len	"Jon Rasmusson Grude"
#   set the mul label to "Jon Rasmusson Grude"
LAST	Lmul	"Jon Rasmusson Grude"
#   set the ja label to "ジョン・ラスムソン・グルデ"
LAST	Lja	"ジョン・ラスムソン・グルデ"
#   set the zh label to "乔恩·拉斯穆松·格鲁德"
LAST	Lzh	"乔恩·拉斯穆松·格鲁德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005102264546 Jon Rasmusson Grude, qualified P1810 subject named as Jon Rasmusson Grude
LAST	P2600	"6000000005102264546"	P1810	"Jon Rasmusson Grude"
#   P569 date of birth = +1691-00-00T00:00:00Z/9
LAST	P569	+1691-00-00T00:00:00Z/9	S2600	"6000000005102264546"
#   P570 date of death = +1766-00-00T00:00:00Z/9
LAST	P570	+1766-00-00T00:00:00Z/9	S2600	"6000000005102264546"
#   P40 child = Q141200028 Per Jonson Øksnevad
LAST	P40	Q141200028	S2600	"6000000005102264546"
#   Q141200028 Per Jonson Øksnevad: P22 father = the item just created
Q141200028	P22	LAST	S2600	"6000000005102264546"

# create a new item
CREATE
#   the item just created: set the mul label to "Kälug"
LAST	Lmul	"Kälug"
#   set the ca label to "mare de Anders Jacobsson"
LAST	Lca	"mare de Anders Jacobsson"
#   set the da label to "mor til Anders Jacobsson"
LAST	Lda	"mor til Anders Jacobsson"
#   set the de label to "Mutter von Anders Jacobsson"
LAST	Lde	"Mutter von Anders Jacobsson"
#   set the en label to "mother of Anders Jacobsson"
LAST	Len	"mother of Anders Jacobsson"
#   set the es label to "madre de Anders Jacobsson"
LAST	Les	"madre de Anders Jacobsson"
#   set the it label to "madre di Anders Jacobsson"
LAST	Lit	"madre di Anders Jacobsson"
#   set the ja label to "アンデルス・ヤコブソンの母"
LAST	Lja	"アンデルス・ヤコブソンの母"
#   set the nb label to "mor til Anders Jacobsson"
LAST	Lnb	"mor til Anders Jacobsson"
#   set the nl label to "moeder van Anders Jacobsson"
LAST	Lnl	"moeder van Anders Jacobsson"
#   set the pt label to "mãe de Anders Jacobsson"
LAST	Lpt	"mãe de Anders Jacobsson"
#   set the sv label to "mor till Anders Jacobsson"
LAST	Lsv	"mor till Anders Jacobsson"
#   set the zh label to "安德斯·雅各布松之母"
LAST	Lzh	"安德斯·雅各布松之母"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000002574331178 Kälug NN
LAST	P2600	"6000000002574331178"
#   P569 date of birth = +1452-00-00T00:00:00Z/9
LAST	P569	+1452-00-00T00:00:00Z/9	S2600	"6000000002574331178"
#   P570 date of death = +1529-00-00T00:00:00Z/9
LAST	P570	+1529-00-00T00:00:00Z/9	S2600	"6000000002574331178"
#   P40 child = Q141216357 Anders Jacobsson
LAST	P40	Q141216357	S2600	"6000000002574331178"
#   Q141216357 Anders Jacobsson: P25 mother = the item just created
Q141216357	P25	LAST	S2600	"6000000002574331178"

# create a new item
CREATE
#   the item just created: set the en label to "Olaf Gunderson"
LAST	Len	"Olaf Gunderson"
#   set the mul label to "Olaf Gunderson"
LAST	Lmul	"Olaf Gunderson"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000015117958521 Olaf Gunderson, qualified P1810 subject named as Olaf Gunderson
LAST	P2600	"6000000015117958521"	P1810	"Olaf Gunderson"
#   P26 spouse = Q141224204 Inger Serine Lerma Gunderson
LAST	P26	Q141224204	S2600	"6000000015117958521"
#   P40 child = Q141224807 Sophia Borgit Hoknes
LAST	P40	Q141224807	S2600	"6000000015117958521"
#   Q141224204 Inger Serine Lerma Gunderson: P26 spouse = the item just created
Q141224204	P26	LAST	S2600	"6000000015117958521"
#   Q141224807 Sophia Borgit Hoknes: P22 father = the item just created
Q141224807	P22	LAST	S2600	"6000000015117958521"

# create a new item
CREATE
#   the item just created: set the en label to "Ragnhild Sæbjørnsdatter Underberge"
LAST	Len	"Ragnhild Sæbjørnsdatter Underberge"
#   set the mul label to "Ragnhild Sæbjørnsdatter Underberge"
LAST	Lmul	"Ragnhild Sæbjørnsdatter Underberge"
#   add a mul alias "Ragnhild Sæbjørnsdatter Bjørheim"
LAST	Amul	"Ragnhild Sæbjørnsdatter Bjørheim"
#   set the ja label to "ラグンヒル・セブヨルンスダッテル・ウンデルベルゲ"
LAST	Lja	"ラグンヒル・セブヨルンスダッテル・ウンデルベルゲ"
#   set the zh label to "拉格希尔德·塞布约尔恩斯达特·温德尔贝尔盖"
LAST	Lzh	"拉格希尔德·塞布约尔恩斯达特·温德尔贝尔盖"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000007834999145 Ragnhild Sæbjørnsdatter Underberge, qualified P1810 subject named as Ragnhild Sæbjørnsdatter Bjørheim
LAST	P2600	"6000000007834999145"	P1810	"Ragnhild Sæbjørnsdatter Bjørheim"
#   P569 date of birth = +1429-00-00T00:00:00Z/9
LAST	P569	+1429-00-00T00:00:00Z/9	S2600	"6000000007834999145"
#   P570 date of death = +1480-00-00T00:00:00Z/9
LAST	P570	+1480-00-00T00:00:00Z/9	S2600	"6000000007834999145"
#   P26 spouse = Q141223436 Tore Underberge III
LAST	P26	Q141223436	S2600	"6000000007834999145"
#   Q141223436 Tore Underberge III: P26 spouse = the item just created
Q141223436	P26	LAST	S2600	"6000000007834999145"
#   the item just created: P735 given name = Q1390292 Ragnhild
LAST	P735	Q1390292
#   P734 family name = Q30834379, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q30834379	P3831	Q2507958
#   add a mul alias "Ragnhild Underberge"
LAST	Amul	"Ragnhild Underberge"

# create a new item
CREATE
#   set the en label to "Rasmus Jonsson Auestad"
LAST	Len	"Rasmus Jonsson Auestad"
#   set the mul label to "Rasmus Jonsson Auestad"
LAST	Lmul	"Rasmus Jonsson Auestad"
#   add a mul alias "Rasmus Jonsson Lura"
LAST	Amul	"Rasmus Jonsson Lura"
#   set the ja label to "ラスムス・ヨンソン・アウエスタド"
LAST	Lja	"ラスムス・ヨンソン・アウエスタド"
#   set the zh label to "拉斯穆斯·永松·奥埃斯塔德"
LAST	Lzh	"拉斯穆斯·永松·奥埃斯塔德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000014276685725 Rasmus Jonsson Auestad, qualified P1810 subject named as Rasmus Jonsson Lura
LAST	P2600	"6000000014276685725"	P1810	"Rasmus Jonsson Lura"
#   P569 date of birth = +1807-00-00T00:00:00Z/9
LAST	P569	+1807-00-00T00:00:00Z/9	S2600	"6000000014276685725"
#   P570 date of death = +1893-06-27T00:00:00Z/11
LAST	P570	+1893-06-27T00:00:00Z/11	S2600	"6000000014276685725"
#   P22 father = Q141216481 Jon Tørresson Soma
LAST	P22	Q141216481	S2600	"6000000014276685725"
#   P25 mother = Q141216490 Malli Svensdatter Lura
LAST	P25	Q141216490	S2600	"6000000014276685725"
#   Q141216481 Jon Tørresson Soma: P40 child = the item just created
Q141216481	P40	LAST	S2600	"6000000014276685725"
#   Q141216490 Malli Svensdatter Lura: P40 child = the item just created
Q141216490	P40	LAST	S2600	"6000000014276685725"
#   the item just created: P735 given name = Q1785744 Rasmus
LAST	P735	Q1785744
#   P734 family name = Q37303374, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q37303374	P3831	Q2507958
#   P734 family name = Q27887968
LAST	P734	Q27887968
#   add a mul alias "Rasmus Auestad"
LAST	Amul	"Rasmus Auestad"

# create a new item
CREATE
#   set the en label to "Sigrid Poulsen"
LAST	Len	"Sigrid Poulsen"
#   set the mul label to "Sigrid Poulsen"
LAST	Lmul	"Sigrid Poulsen"
#   add a mul alias "Sigrid Nyvold"
LAST	Amul	"Sigrid Nyvold"
#   set the ja label to "シグリッド・ポールセン"
LAST	Lja	"シグリッド・ポールセン"
#   set the zh label to "西格丽·波乌尔森"
LAST	Lzh	"西格丽·波乌尔森"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000021198105854 Sigrid Poulsen, qualified P1810 subject named as Sigrid Nyvold
LAST	P2600	"6000000021198105854"	P1810	"Sigrid Nyvold"
#   P569 date of birth = +1892-03-23T00:00:00Z/11
LAST	P569	+1892-03-23T00:00:00Z/11	S2600	"6000000021198105854"
#   P570 date of death = +1963-07-04T00:00:00Z/11
LAST	P570	+1963-07-04T00:00:00Z/11	S2600	"6000000021198105854"
#   P22 father = Q138474188 Hans Syvertsen Nyvold
LAST	P22	Q138474188	S2600	"6000000021198105854"
#   P25 mother = Q141178197 Elisabeth Nyvold
LAST	P25	Q141178197	S2600	"6000000021198105854"
#   Q138474188 Hans Syvertsen Nyvold: P40 child = the item just created
Q138474188	P40	LAST	S2600	"6000000021198105854"
#   Q141178197 Elisabeth Nyvold: P40 child = the item just created
Q141178197	P40	LAST	S2600	"6000000021198105854"
#   the item just created: P735 given name = Q634916 Sigrid
LAST	P735	Q634916
#   P734 family name = Q1434084 Poulsen, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q1434084	P3831	Q28418670

# create a new item
CREATE
#   set the en label to "Siri Jonsdatter Lauvsnes"
LAST	Len	"Siri Jonsdatter Lauvsnes"
#   set the mul label to "Siri Jonsdatter Lauvsnes"
LAST	Lmul	"Siri Jonsdatter Lauvsnes"
#   add a mul alias "Siri Jonsdatter Jonsdatter"
LAST	Amul	"Siri Jonsdatter Jonsdatter"
#   set the ja label to "シリ・ヨンスダッテル・ラウヴスネス"
LAST	Lja	"シリ・ヨンスダッテル・ラウヴスネス"
#   set the zh label to "西里·永斯达特·拉乌夫斯内斯"
LAST	Lzh	"西里·永斯达特·拉乌夫斯内斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005607362736 Siri Jonsdtr. Lauvsnes, qualified P1810 subject named as Siri Jonsdtr. Jonsdatter
LAST	P2600	"6000000005607362736"	P1810	"Siri Jonsdtr. Jonsdatter"
#   P40 child = Q141224746 Bellest Bellestsen Lauvsnes d.e.
LAST	P40	Q141224746	S2600	"6000000005607362736"
#   Q141224746 Bellest Bellestsen Lauvsnes d.e.: P25 mother = the item just created
Q141224746	P25	LAST	S2600	"6000000005607362736"
#   the item just created: P735 given name = Q1772342 Siri, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q1772342	P1545	"1"	P7452	Q3409033
#   P5056 patronym or matronym = Q141189036
LAST	P5056	Q141189036
#   add a mul alias "Siri Jonsdtr. Lauvsnes"
LAST	Amul	"Siri Jonsdtr. Lauvsnes"

# create a new item
CREATE
#   set the en label to "Theoline Henrika Borsheim"
LAST	Len	"Theoline Henrika Borsheim"
#   set the mul label to "Theoline Henrika Borsheim"
LAST	Lmul	"Theoline Henrika Borsheim"
#   set the ja label to "テオリネ・ヘンリカ・ボルスハイム"
LAST	Lja	"テオリネ・ヘンリカ・ボルスハイム"
#   set the zh label to "特奥利内·亨里卡·博尔斯海姆"
LAST	Lzh	"特奥利内·亨里卡·博尔斯海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000169037819865 Theoline Henrika Borsheim, qualified P1810 subject named as Theoline Henrika Borsheim
LAST	P2600	"6000000169037819865"	P1810	"Theoline Henrika Borsheim"
#   P569 date of birth = +1895-12-10T00:00:00Z/11
LAST	P569	+1895-12-10T00:00:00Z/11	S2600	"6000000169037819865"
#   P570 date of death = +1992-01-00T00:00:00Z/10
LAST	P570	+1992-01-00T00:00:00Z/10	S2600	"6000000169037819865"
#   P26 spouse = Q141224339 Reinhert Borsheim
LAST	P26	Q141224339	S2600	"6000000169037819865"
#   P40 child = Q141224882 Randolph Paulus Borsheim
LAST	P40	Q141224882	S2600	"6000000169037819865"
#   Q141224339 Reinhert Borsheim: P26 spouse = the item just created
Q141224339	P26	LAST	S2600	"6000000169037819865"
#   Q141224882 Randolph Paulus Borsheim: P25 mother = the item just created
Q141224882	P25	LAST	S2600	"6000000169037819865"

# create a new item
CREATE
#   the item just created: set the en label to "Tormod Rasmusson Nedre Rossavik"
LAST	Len	"Tormod Rasmusson Nedre Rossavik"
#   set the mul label to "Tormod Rasmusson Nedre Rossavik"
LAST	Lmul	"Tormod Rasmusson Nedre Rossavik"
#   set the ja label to "トルモド・ラスムソン・ネドレ・ロサヴィク"
LAST	Lja	"トルモド・ラスムソン・ネドレ・ロサヴィク"
#   set the zh label to "托尔莫德·拉斯穆松·内德雷·罗萨维克"
LAST	Lzh	"托尔莫德·拉斯穆松·内德雷·罗萨维克"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005609571149 Tormod Rasmusson Nedre Rossavik, qualified P1810 subject named as Tormod Rasmusson Nedre Rossavik
LAST	P2600	"6000000005609571149"	P1810	"Tormod Rasmusson Nedre Rossavik"
#   P569 date of birth = +1719-00-00T00:00:00Z/9
LAST	P569	+1719-00-00T00:00:00Z/9	S2600	"6000000005609571149"
#   P570 date of death = +1801-00-00T00:00:00Z/9
LAST	P570	+1801-00-00T00:00:00Z/9	S2600	"6000000005609571149"
#   P22 father = Q141216644 Rasmus Asbjørnson Nedre Rossavik
LAST	P22	Q141216644	S2600	"6000000005609571149"
#   P25 mother = Q141205898 Anna Tormodsdatter Mele
LAST	P25	Q141205898	S2600	"6000000005609571149"
#   Q141216644 Rasmus Asbjørnson Nedre Rossavik: P40 child = the item just created
Q141216644	P40	LAST	S2600	"6000000005609571149"
#   Q141205898 Anna Tormodsdatter Mele: P40 child = the item just created
Q141205898	P40	LAST	S2600	"6000000005609571149"
#   the item just created: P735 given name = Q7825922 Tormod
LAST	P735	Q7825922
#   P734 family name = Q122838342
LAST	P734	Q122838342
#   add a mul alias "Tormod Nedre Rossavik"
LAST	Amul	"Tormod Nedre Rossavik"
#   Q141216397 Malin Andersdotter: P40 child = Q141199706 Anna Andersdotter
Q141216397	P40	Q141199706	S2600	"6000000000305413766"
#   Q141216357 Anders Jacobsson: P40 child = Q141199706 Anna Andersdotter
Q141216357	P40	Q141199706	S2600	"6000000001138735296"
#   Q141216467 Eldrid Jonsdatter: P5056 patronym or matronym = Q141189036
Q141216467	P5056	Q141189036
#   Q141224827 Margareta Olausdotter Plantin: P26 spouse = Q141224872 Petrus Jonae Jonæ Linnerius
Q141224827	P26	Q141224872	S2600	"6000000002994864380"
#   Q141200101 Sissel Jonsdatter Talje: P5056 patronym or matronym = Q141189036, qualified P144 based on Q141199899 Jon Tollakson Aukland, IV
Q141200101	P5056	Q141189036	P144	Q141199899
#   Q141216638 Olaug Jonsdatter Heigre: P5056 patronym or matronym = Q141189036
Q141216638	P5056	Q141189036
#   Q141199892 Jon Olsen Heigre: P5056 patronym or matronym = Q141223473, qualified P144 based on Q141216637 Ola Person Persson Heigre
Q141199892	P5056	Q141223473	P144	Q141216637
#   Q141200054 Rakel Jonsdatter Jonsdotter Vatne: P5056 patronym or matronym = Q141189036, qualified P144 based on Q141216388 Jon Hansson St. Vatne
Q141200054	P5056	Q141189036	P144	Q141216388
#   Q141216365 Berte Karine Jonsdatter Stokka: P5056 patronym or matronym = Q141189036, qualified P144 based on Q141199892 Jon Olsen Heigre
Q141216365	P5056	Q141189036	P144	Q141199892
#   Q141216635 Martha Eivindsdatter Heigre: P5056 patronym or matronym = Q141189042
Q141216635	P5056	Q141189042
#   Q141216622 Kristine Jonsdatter Malmeim: P5056 patronym or matronym = Q141189036, qualified P144 based on Q141168955 Jon Samuelsen Raustad
Q141216622	P5056	Q141189036	P144	Q141168955
#   Q141205921 Maria Jonsdatter Lura: P5056 patronym or matronym = Q141189036, qualified P144 based on Q141216388 Jon Hansson St. Vatne
Q141205921	P5056	Q141189036	P144	Q141216388
#   Q141199704 Andreas Olai: P26 spouse = Q141199706 Anna Andersdotter
Q141199704	P26	Q141199706	S2600	"6000000004334566448"
#   Q141216384 Ingeborg Eriksdatter Time: P5056 patronym or matronym = Q141223487
Q141216384	P5056	Q141223487
#   Q141223735 Helge Olsen Ytre Lima: P5056 patronym or matronym = Q141223473, qualified P144 based on Q141223933 Ola Svenson Ytre Lima
Q141223735	P5056	Q141223473	P144	Q141223933
#   Q141224746 Bellest Bellestsen Lauvsnes d.e.: P26 spouse = Q141224797 Malena Henriksdatter Lauvsnes
Q141224746	P26	Q141224797	S2600	"6000000005608905668"
#   Q141189071 Joren Jonsdatter Espedal: P5056 patronym or matronym = Q141189036, qualified P144 based on Q141198435 Jon Nilsson Espedal
Q141189071	P5056	Q141189036	P144	Q141198435
#   Q141224872 Petrus Jonae Jonæ Linnerius: P26 spouse = Q141224827 Margareta Olausdotter Plantin
Q141224872	P26	Q141224827	S2600	"6000000006782697953"
#   Q141224797 Malena Henriksdatter Lauvsnes: P26 spouse = Q141224746 Bellest Bellestsen Lauvsnes d.e.
Q141224797	P26	Q141224746	S2600	"6000000008686123375"
#   Q141178201 Marie Petrine Simensdatter Bergersen: P5056 patronym or matronym = Q141189030, qualified P144 based on Q141205940 Simen Olsen
Q141178201	P5056	Q141189030	P144	Q141205940
#   Q141168797 Christian Frederik Bergersen: P5056 patronym or matronym = Q141189030, qualified P144 based on Q141178199 Gunder Bergersen
Q141168797	P5056	Q141189030	P144	Q141178199
#   Q141224751 Berta Serina Rasmusdatter Borsheim: P26 spouse = Q141224861 Paul Pederson Borsheim
Q141224751	P26	Q141224861	S2600	"6000000014522158621"
#   P735 given name = Q4092653 Berta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141224751	P735	Q4092653	P1545	"1"	P7452	Q3409033
#   P735 given name = Q20000838 Serina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141224751	P735	Q20000838	P1545	"2"	P3831	Q245025
#   P5056 patronym or matronym = Q141223475
Q141224751	P5056	Q141223475
#   P734 family name = Q37328187
Q141224751	P734	Q37328187
#   Q141205940 Simen Olsen: P5056 patronym or matronym = Q141223473
Q141205940	P5056	Q141223473
#   Q141189064 Georg August Bergersen: P5056 patronym or matronym = Q141189030, qualified P144 based on Q141178199 Gunder Bergersen
Q141189064	P5056	Q141189030	P144	Q141178199
#   Q141189093 Oline Mathea Olsen: P5056 patronym or matronym = Q141223473, qualified P144 based on Q141178199 Gunder Bergersen
Q141189093	P5056	Q141223473	P144	Q141178199
#   Q141189076 Kristian Larsen Sør-Reime: P734 family name = Q141189041
Q141189076	P734	Q141189041
#   Q141189061 Carl Bergersen: P5056 patronym or matronym = Q141189030, qualified P144 based on Q141178199 Gunder Bergersen
Q141189061	P5056	Q141189030	P144	Q141178199
#   Q141224339 Reinhert Borsheim: P734 family name = Q37328187
Q141224339	P734	Q37328187
#   Q141224861 Paul Pederson Borsheim: P26 spouse = Q141224751 Berta Serina Rasmusdatter Borsheim
Q141224861	P26	Q141224751	S2600	"6000000035525833995"
#   P735 given name = Q4925623 Paul
Q141224861	P735	Q4925623
#   P734 family name = Q37328187
Q141224861	P734	Q37328187
#   Q141223533 Jorunn Jonsdatter Li: P5056 patronym or matronym = Q141189036, qualified P144 based on Q141180408 Jon Larsson Mæle
Q141223533	P5056	Q141189036	P144	Q141180408
#   Q141224161 Esther Hansine Wendt: P40 child = Q141224222 Jens Wilhelm Wendt
Q141224161	P40	Q141224222	S2600	"6000000048057114880"
#   Q141189091 Ole Nicolai Bergersen: P5056 patronym or matronym = Q141189030, qualified P144 based on Q141168797 Christian Frederik Bergersen
Q141189091	P5056	Q141189030	P144	Q141168797
#   Q141189068 Hilde Constance Marie Bergersen: P5056 patronym or matronym = Q141189030, qualified P144 based on Q141168797 Christian Frederik Bergersen
Q141189068	P5056	Q141189030	P144	Q141168797
#   Q141224249 Johannes John Jacobsen: P735 given name = Q4925477 John, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141224249	P735	Q4925477	P1545	"2"	P3831	Q245025
#   Q141224141 En dödfödd son Bielke: P735 given name = Q69523615, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141224141	P735	Q69523615	P1545	"1"	P7452	Q3409033
#   P735 given name = Q20111831, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q141224141	P735	Q20111831	P1545	"3"	P3831	Q245025
#   Q141224116 Clara Elfrida Tverdahl: P26 spouse = Q141224309 Ole Peter Tverdahl
Q141224116	P26	Q141224309	S2600	"6000000177172694835"
#   Q141224309 Ole Peter Tverdahl: P26 spouse = Q141224116 Clara Elfrida Tverdahl
Q141224309	P26	Q141224116	S2600	"6000000177202378835"
#   Q141224814 Richard Wade Borsheim: P22 father = Q141224882 Randolph Paulus Borsheim
Q141224814	P22	Q141224882	S2600	"6000000177921459056"
#   P25 mother = Q141224812 Caroline Signe Borsheim
Q141224814	P25	Q141224812	S2600	"6000000177921459056"
#   P735 given name = Q1249148 Richard, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141224814	P735	Q1249148	P1545	"1"	P7452	Q3409033
#   P735 given name = Q15630117 Wade, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141224814	P735	Q15630117	P1545	"2"	P3831	Q245025
#   P734 family name = Q37328187
Q141224814	P734	Q37328187
#   Q141224812 Caroline Signe Borsheim: P40 child = Q141224814 Richard Wade Borsheim
Q141224812	P40	Q141224814	S2600	"6000000177921459072"
#   P26 spouse = Q141224882 Randolph Paulus Borsheim
Q141224812	P26	Q141224882	S2600	"6000000177921459072"
#   P735 given name = Q16275172, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141224812	P735	Q16275172	P1545	"1"	P7452	Q3409033
#   P735 given name = Q2096893 Signe, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141224812	P735	Q2096893	P1545	"2"	P3831	Q245025
#   P734 family name = Q37328187
Q141224812	P734	Q37328187
#   Q141224882 Randolph Paulus Borsheim: P40 child = Q141224814 Richard Wade Borsheim
Q141224882	P40	Q141224814	S2600	"6000000177921459078"
#   P26 spouse = Q141224812 Caroline Signe Borsheim
Q141224882	P26	Q141224812	S2600	"6000000177921459078"
#   P735 given name = Q21485499 Randolph, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141224882	P735	Q21485499	P1545	"1"	P7452	Q3409033
#   P735 given name = Q4391614 Paulus, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141224882	P735	Q4391614	P1545	"2"	P3831	Q245025
#   P734 family name = Q37328187
Q141224882	P734	Q37328187
#   Q141224807 Sophia Borgit Hoknes: P40 child = Q141224812 Caroline Signe Borsheim
Q141224807	P40	Q141224812	S2600	"6000000177921459094"
#   P735 given name = Q2302787 Sophia, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141224807	P735	Q2302787	P1545	"1"	P7452	Q3409033
#   Q141224204 Inger Serine Lerma Gunderson: P25 mother = Q141224136 Dorte Sofie Nilsdatter Kyllingstad
Q141224204	P25	Q141224136	S2600	"6000000177921459129"
#   P735 given name = Q3358452 Inger, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141224204	P735	Q3358452	P1545	"1"	P7452	Q3409033
#   P735 given name = Q136121543, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141224204	P735	Q136121543	P1545	"2"	P3831	Q245025
#   Q141224136 Dorte Sofie Nilsdatter Kyllingstad: P40 child = Q141224204 Inger Serine Lerma Gunderson
Q141224136	P40	Q141224204	S2600	"6000000177969427823"
#   P735 given name = Q11166412 Dorte, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141224136	P735	Q11166412	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18201530 Sofie, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141224136	P735	Q18201530	P1545	"2"	P3831	Q245025
#   P5056 patronym or matronym = Q122837798 Nilsdatter
Q141224136	P5056	Q122837798
#   P734 family name = Q30080230
Q141224136	P734	Q30080230
#   Q141223907 Elly Olivia Frisk: P734 family name = Q27877507 Frisk
Q141223907	P734	Q27877507
#   Q141223999 Anna Ådnesdatter Lima: P40 child = Q141223972 Ådne Olsson Lima Kyllingstad. Lima
Q141223999	P40	Q141223972	S2600	"6000000178280363847"
#   P735 given name = Q666578 Anna
Q141223999	P735	Q666578
#   P734 family name = Q11255517 Lima
Q141223999	P734	Q11255517
#   Q141189062 Cecilie Jonsdatter: P5056 patronym or matronym = Q141189036, qualified P144 based on Q116150299 Jon Reinmodsen
Q141189062	P5056	Q141189036	P144	Q116150299
#   Q141223972 Ådne Olsson Lima Kyllingstad. Lima: P735 given name = Q12011446, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141223972	P735	Q12011446	P1545	"1"	P7452	Q3409033
#   P735 given name = Q67609267, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141223972	P735	Q67609267	P1545	"2"	P3831	Q245025
#   P734 family name = Q11255517 Lima
Q141223972	P734	Q11255517
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
#   Q141224789 Jon Olsen Trevland: P5056 patronym or matronym = Q141223473, qualified P144 based on Q141223431 Ola Taraldsen Trevland
Q141224789	P5056	Q141223473	P144	Q141223431

