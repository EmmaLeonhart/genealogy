# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   807 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   Q6014779 Otto Henrik Nordenskiöld: set the ja label to "オットー・ヘンリク・ノルデンショルド"
Q6014779	Lja	"オットー・ヘンリク・ノルデンショルド"
#   set the zh label to "奥托·亨里克·诺尔登斯基奥尔德"
Q6014779	Lzh	"奥托·亨里克·诺尔登斯基奥尔德"
#   Q141205903 Enok Jonson Rønneberg: set the ja label to "エノク・ヨンソン・レンネベルグ"
Q141205903	Lja	"エノク・ヨンソン・レンネベルグ"
#   set the zh label to "埃诺克·永松·伦内贝格"
Q141205903	Lzh	"埃诺克·永松·伦内贝格"
#   Q16650163 Samuel Andersson Pryss: set the ja label to "サミュエル・アンデション・プリス"
Q16650163	Lja	"サミュエル・アンデション・プリス"
#   set the zh label to "塞缪尔·安德松·普里斯"
Q16650163	Lzh	"塞缪尔·安德松·普里斯"
#   Q141216496 Nils Larsen Raunes: set the ja label to "ニルス・ラーセン・ラウネス"
Q141216496	Lja	"ニルス・ラーセン・ラウネス"
#   set the zh label to "尼尔斯·拉森·拉乌内斯"
Q141216496	Lzh	"尼尔斯·拉森·拉乌内斯"
#   Q5575607 Nils Adam Turesson Bielke: set the ja label to "ニルス・アダム・トレソン・ビールケ"
Q5575607	Lja	"ニルス・アダム・トレソン・ビールケ"
#   set the zh label to "尼尔斯·亚当·图雷松·比埃尔凯"
Q5575607	Lzh	"尼尔斯·亚当·图雷松·比埃尔凯"
#   Q5575580 Gustaf Ture Bielke: set the ja label to "グスタフ・トゥーレ・ビールケ"
Q5575580	Lja	"グスタフ・トゥーレ・ビールケ"
#   set the zh label to "古斯塔夫·图雷·比埃尔凯"
Q5575580	Lzh	"古斯塔夫·图雷·比埃尔凯"
#   Q490870 Anders Jacobsson Chydenius: set the ja label to "アンデルス・ヤコブソン・キデニウス"
Q490870	Lja	"アンデルス・ヤコブソン・キデニウス"
#   set the zh label to "安德斯·雅各布松·基德尼乌斯"
Q490870	Lzh	"安德斯·雅各布松·基德尼乌斯"
#   Q6161733 Carl Fredrik Piper till Krageholm: set the ja label to "カール・フレドリク・パイパー・ティル・クラゲホルム"
Q6161733	Lja	"カール・フレドリク・パイパー・ティル・クラゲホルム"

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Anna Danielsdotter Behmer"
LAST	Len	"Anna Danielsdotter Behmer"
#   set the mul label to "Anna Danielsdotter Behmer"
LAST	Lmul	"Anna Danielsdotter Behmer"
#   set the ja label to "アンナ・ダニエルスドッテル・ベメル"
LAST	Lja	"アンナ・ダニエルスドッテル・ベメル"
#   set the zh label to "安娜·达尼埃尔斯多特·贝梅尔"
LAST	Lzh	"安娜·达尼埃尔斯多特·贝梅尔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000012724205355 Anna Danielsdotter Behmer, qualified P1810 subject named as Anna Danielsdotter Behmer
LAST	P2600	"6000000012724205355"	P1810	"Anna Danielsdotter Behmer"
#   P569 date of birth = +1645-00-00T00:00:00Z/9
LAST	P569	+1645-00-00T00:00:00Z/9	S2600	"6000000012724205355"
#   P570 date of death = +1730-00-00T00:00:00Z/9
LAST	P570	+1730-00-00T00:00:00Z/9	S2600	"6000000012724205355"
#   P22 father = Q5568857 Daniel Jonsson Behmer
LAST	P22	Q5568857	S2600	"6000000012724205355"
#   Q5568857 Daniel Jonsson Behmer: P40 child = the item just created
Q5568857	P40	LAST	S2600	"6000000012724205355"
#   the item just created: P735 given name = Q666578 Anna
LAST	P735	Q666578
#   P5056 patronym or matronym = Q140226461, qualified P144 based on Q5568857 Daniel Jonsson Behmer
LAST	P5056	Q140226461	P144	Q5568857

# create a new item
CREATE
#   set the en label to "Anna Martens"
LAST	Len	"Anna Martens"
#   set the mul label to "Anna Martens"
LAST	Lmul	"Anna Martens"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000018604581410 Anna Martens, qualified P1810 subject named as Anna Martens
LAST	P2600	"6000000018604581410"	P1810	"Anna Martens"
#   P40 child = Q108615842 Mårten Bunge
LAST	P40	Q108615842	S2600	"6000000018604581410"
#   Q108615842 Mårten Bunge: P25 mother = the item just created
Q108615842	P25	LAST	S2600	"6000000018604581410"
#   the item just created: P735 given name = Q666578 Anna
LAST	P735	Q666578

# create a new item
CREATE
#   set the en label to "Anne Berta Osmundsdatter Nese"
LAST	Len	"Anne Berta Osmundsdatter Nese"
#   set the mul label to "Anne Berta Osmundsdatter Nese"
LAST	Lmul	"Anne Berta Osmundsdatter Nese"
#   set the ja label to "アン・ベルタ・オスムンドスダッテル・ネセ"
LAST	Lja	"アン・ベルタ・オスムンドスダッテル・ネセ"
#   set the zh label to "安妮·贝尔塔·奥斯蒙德斯达特·内塞"
LAST	Lzh	"安妮·贝尔塔·奥斯蒙德斯达特·内塞"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005609547544 Anne Berta Osmundsdatter Nese, qualified P1810 subject named as Anne Berta Osmundsdatter Nese
LAST	P2600	"6000000005609547544"	P1810	"Anne Berta Osmundsdatter Nese"
#   P569 date of birth = +1828-03-24T00:00:00Z/11
LAST	P569	+1828-03-24T00:00:00Z/11	S2600	"6000000005609547544"
#   P22 father = Q141223432 Osmund Larsson Nese
LAST	P22	Q141223432	S2600	"6000000005609547544"
#   Q141223432 Osmund Larsson Nese: P40 child = the item just created
Q141223432	P40	LAST	S2600	"6000000005609547544"

# create a new item
CREATE
#   the item just created: set the en label to "Beda Elvira Wedberg"
LAST	Len	"Beda Elvira Wedberg"
#   set the mul label to "Beda Elvira Wedberg"
LAST	Lmul	"Beda Elvira Wedberg"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000177921458833 Beda Elvira Wedberg, qualified P1810 subject named as Beda Elvira Wedberg
LAST	P2600	"6000000177921458833"	P1810	"Beda Elvira Wedberg"
#   P569 date of birth = +1906-03-09T00:00:00Z/11
LAST	P569	+1906-03-09T00:00:00Z/11	S2600	"6000000177921458833"
#   P570 date of death = +1979-10-02T00:00:00Z/11
LAST	P570	+1979-10-02T00:00:00Z/11	S2600	"6000000177921458833"
#   P25 mother = Q141223427 Johanna Matilda Carlsdotter
LAST	P25	Q141223427	S2600	"6000000177921458833"
#   Q141223427 Johanna Matilda Carlsdotter: P40 child = the item just created
Q141223427	P40	LAST	S2600	"6000000177921458833"

# create a new item
CREATE
#   the item just created: set the en label to "Carl, Johan Ersson"
LAST	Len	"Carl, Johan Ersson"
#   set the mul label to "Carl, Johan Ersson"
LAST	Lmul	"Carl, Johan Ersson"
#   set the ja label to "カール・ヨハン・エルソン"
LAST	Lja	"カール・ヨハン・エルソン"
#   set the zh label to "卡尔·约翰·埃尔松"
LAST	Lzh	"卡尔·约翰·埃尔松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000177921459028 Carl, Johan Ersson, qualified P1810 subject named as Carl, Johan Ersson
LAST	P2600	"6000000177921459028"	P1810	"Carl, Johan Ersson"
#   P569 date of birth = +1833-02-21T00:00:00Z/11
LAST	P569	+1833-02-21T00:00:00Z/11	S2600	"6000000177921459028"
#   P26 spouse = Q141219160 Christina, Sofia Carlsdotter
LAST	P26	Q141219160	S2600	"6000000177921459028"
#   P40 child = Q141223427 Johanna Matilda Carlsdotter
LAST	P40	Q141223427	S2600	"6000000177921459028"
#   Q141219160 Christina, Sofia Carlsdotter: P26 spouse = the item just created
Q141219160	P26	LAST	S2600	"6000000177921459028"
#   Q141223427 Johanna Matilda Carlsdotter: P22 father = the item just created
Q141223427	P22	LAST	S2600	"6000000177921459028"

# create a new item
CREATE
#   the item just created: set the en label to "Catharina Charlotta Haijock"
LAST	Len	"Catharina Charlotta Haijock"
#   set the mul label to "Catharina Charlotta Haijock"
LAST	Lmul	"Catharina Charlotta Haijock"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000021122825341 Catharina Charlotta Haijock, qualified P1810 subject named as Catharina Charlotta Haijock
LAST	P2600	"6000000021122825341"	P1810	"Catharina Charlotta Haijock"
#   P570 date of death = +1758-00-00T00:00:00Z/9
LAST	P570	+1758-00-00T00:00:00Z/9	S2600	"6000000021122825341"
#   P26 spouse = Q5745627 Berge / Birger Frondin
LAST	P26	Q5745627	S2600	"6000000021122825341"
#   P40 child = Q141223420 Gunilla Margareta Frondin
LAST	P40	Q141223420	S2600	"6000000021122825341"
#   Q5745627 Berge / Birger Frondin: P26 spouse = the item just created
Q5745627	P26	LAST	S2600	"6000000021122825341"
#   Q141223420 Gunilla Margareta Frondin: P25 mother = the item just created
Q141223420	P25	LAST	S2600	"6000000021122825341"
#   the item just created: P735 given name = Q17317997 Catharina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q17317997	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1067071	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Eva Fredrika Hæggström"
LAST	Len	"Eva Fredrika Hæggström"
#   set the mul label to "Eva Fredrika Hæggström"
LAST	Lmul	"Eva Fredrika Hæggström"
#   add a mul alias "Eva Fredrika Burström"
LAST	Amul	"Eva Fredrika Burström"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000019629335126 Eva Fredrika Hæggström, qualified P1810 subject named as Eva Fredrika Burström
LAST	P2600	"6000000019629335126"	P1810	"Eva Fredrika Burström"
#   P569 date of birth = +1803-05-23T00:00:00Z/11
LAST	P569	+1803-05-23T00:00:00Z/11	S2600	"6000000019629335126"
#   P570 date of death = +1883-02-17T00:00:00Z/11
LAST	P570	+1883-02-17T00:00:00Z/11	S2600	"6000000019629335126"
#   P26 spouse = Q5819456 Zacharias Hæggström
LAST	P26	Q5819456	S2600	"6000000019629335126"
#   Q5819456 Zacharias Hæggström: P26 spouse = the item just created
Q5819456	P26	LAST	S2600	"6000000019629335126"
#   the item just created: P735 given name = Q64412279 Eva, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q64412279	P1545	"1"	P7452	Q3409033
#   P735 given name = Q5499550 Fredrika, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q5499550	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Glen Archie Tunheim"
LAST	Len	"Glen Archie Tunheim"
#   set the mul label to "Glen Archie Tunheim"
LAST	Lmul	"Glen Archie Tunheim"
#   set the ja label to "グレン・アーチー・トゥンヘイム"
LAST	Lja	"グレン・アーチー・トゥンヘイム"
#   set the zh label to "格伦·阿奇·通海姆"
LAST	Lzh	"格伦·阿奇·通海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000180036723850 Glen Archie Tunheim, qualified P1810 subject named as Glen Archie Tunheim
LAST	P2600	"6000000180036723850"	P1810	"Glen Archie Tunheim"
#   P569 date of birth = +1935-04-02T00:00:00Z/11
LAST	P569	+1935-04-02T00:00:00Z/11	S2600	"6000000180036723850"
#   P570 date of death = +1984-05-13T00:00:00Z/11
LAST	P570	+1984-05-13T00:00:00Z/11	S2600	"6000000180036723850"
#   P22 father = Q141168809 Edward Tunheim
LAST	P22	Q141168809	S2600	"6000000180036723850"
#   P25 mother = Q141205894 Agnes Tunheim
LAST	P25	Q141205894	S2600	"6000000180036723850"
#   Q141168809 Edward Tunheim: P40 child = the item just created
Q141168809	P40	LAST	S2600	"6000000180036723850"
#   Q141205894 Agnes Tunheim: P40 child = the item just created
Q141205894	P40	LAST	S2600	"6000000180036723850"
#   the item just created: P735 given name = Q16276007 Glen, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q16276007	P1545	"1"	P7452	Q3409033
#   P735 given name = Q19826472 Archie, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q19826472	P1545	"2"	P3831	Q245025
#   P734 family name = Q36927172
LAST	P734	Q36927172

# create a new item
CREATE
#   set the en label to "Hans Otto Kristian Jenssen"
LAST	Len	"Hans Otto Kristian Jenssen"
#   set the mul label to "Hans Otto Kristian Jenssen"
LAST	Lmul	"Hans Otto Kristian Jenssen"
#   set the ja label to "ハンス・オットー・クリスチャン・イェンセン"
LAST	Lja	"ハンス・オットー・クリスチャン・イェンセン"
#   set the zh label to "汉斯·奥托·克里斯蒂安·延森"
LAST	Lzh	"汉斯·奥托·克里斯蒂安·延森"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000014188476819 Hans Otto Kristian Jenssen, qualified P1810 subject named as Hans Otto Kristian Jenssen
LAST	P2600	"6000000014188476819"	P1810	"Hans Otto Kristian Jenssen"
#   P569 date of birth = +1852-00-00T00:00:00Z/9
LAST	P569	+1852-00-00T00:00:00Z/9	S2600	"6000000014188476819"
#   P26 spouse = Q141219307 Petrike Margrete Jenssen
LAST	P26	Q141219307	S2600	"6000000014188476819"
#   P40 child = Q141216639 Olufine Bergithe Ekman
LAST	P40	Q141216639	S2600	"6000000014188476819"
#   Q141219307 Petrike Margrete Jenssen: P26 spouse = the item just created
Q141219307	P26	LAST	S2600	"6000000014188476819"
#   Q141216639 Olufine Bergithe Ekman: P22 father = the item just created
Q141216639	P22	LAST	S2600	"6000000014188476819"
#   the item just created: P735 given name = Q632842, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q632842	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18029644 Otto, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q18029644	P1545	"2"	P3831	Q245025
#   P735 given name = Q12794332 Kristian, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
LAST	P735	Q12794332	P1545	"3"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Hilma Petrine Jenssen"
LAST	Len	"Hilma Petrine Jenssen"
#   set the mul label to "Hilma Petrine Jenssen"
LAST	Lmul	"Hilma Petrine Jenssen"
#   set the ja label to "ヒルマ・ペトリーネ・イェンセン"
LAST	Lja	"ヒルマ・ペトリーネ・イェンセン"
#   set the zh label to "希尔马·佩特里内·延森"
LAST	Lzh	"希尔马·佩特里内·延森"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000014196669652 Hilma Petrine Jenssen, qualified P1810 subject named as Hilma Petrine Jenssen
LAST	P2600	"6000000014196669652"	P1810	"Hilma Petrine Jenssen"
#   P569 date of birth = +1877-00-00T00:00:00Z/9
LAST	P569	+1877-00-00T00:00:00Z/9	S2600	"6000000014196669652"
#   P25 mother = Q141219307 Petrike Margrete Jenssen
LAST	P25	Q141219307	S2600	"6000000014196669652"
#   Q141219307 Petrike Margrete Jenssen: P40 child = the item just created
Q141219307	P40	LAST	S2600	"6000000014196669652"
#   the item just created: P735 given name = Q4356711 Hilma, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q4356711	P1545	"1"	P7452	Q3409033
#   P735 given name = Q107227465 Petrine, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q107227465	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Jakob Bunge"
LAST	Len	"Jakob Bunge"
#   set the mul label to "Jakob Bunge"
LAST	Lmul	"Jakob Bunge"
#   set the ja label to "ヤーコプ・ブンゲ"
LAST	Lja	"ヤーコプ・ブンゲ"
#   set the zh label to "雅各布·邦格"
LAST	Lzh	"雅各布·邦格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000018604538988 Jakob Bunge, qualified P1810 subject named as Jakob Bunge
LAST	P2600	"6000000018604538988"	P1810	"Jakob Bunge"
#   P570 date of death = +1630-00-00T00:00:00Z/9
LAST	P570	+1630-00-00T00:00:00Z/9	S2600	"6000000018604538988"
#   P40 child = Q108615842 Mårten Bunge
LAST	P40	Q108615842	S2600	"6000000018604538988"
#   Q108615842 Mårten Bunge: P22 father = the item just created
Q108615842	P22	LAST	S2600	"6000000018604538988"
#   the item just created: P735 given name = Q16747395
LAST	P735	Q16747395
#   P734 family name = Q16865161 Bunge
LAST	P734	Q16865161
#   add a mul alias "Jacob Bunge"
LAST	Amul	"Jacob Bunge"

# create a new item
CREATE
#   set the en label to "Johan Fredrik Wedberg"
LAST	Len	"Johan Fredrik Wedberg"
#   set the mul label to "Johan Fredrik Wedberg"
LAST	Lmul	"Johan Fredrik Wedberg"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000021652410546 Johan Fredrik Wedberg, qualified P1810 subject named as Johan Fredrik Wedberg
LAST	P2600	"6000000021652410546"	P1810	"Johan Fredrik Wedberg"
#   P569 date of birth = +1855-09-07T00:00:00Z/11
LAST	P569	+1855-09-07T00:00:00Z/11	S2600	"6000000021652410546"
#   P570 date of death = +1934-03-04T00:00:00Z/11
LAST	P570	+1934-03-04T00:00:00Z/11	S2600	"6000000021652410546"
#   P26 spouse = Q141223427 Johanna Matilda Carlsdotter
LAST	P26	Q141223427	S2600	"6000000021652410546"
#   Q141223427 Johanna Matilda Carlsdotter: P26 spouse = the item just created
Q141223427	P26	LAST	S2600	"6000000021652410546"

# create a new item
CREATE
#   the item just created: set the en label to "Johanna Elisabet Hjärne"
LAST	Len	"Johanna Elisabet Hjärne"
#   set the mul label to "Johanna Elisabet Hjärne"
LAST	Lmul	"Johanna Elisabet Hjärne"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000012898544484 Johanna Elisabet Hjärne, qualified P1810 subject named as Johanna Elisabet Hjärne
LAST	P2600	"6000000012898544484"	P1810	"Johanna Elisabet Hjärne"
#   P569 date of birth = +1747-00-00T00:00:00Z/9
LAST	P569	+1747-00-00T00:00:00Z/9	S2600	"6000000012898544484"
#   P570 date of death = +1803-00-00T00:00:00Z/9
LAST	P570	+1803-00-00T00:00:00Z/9	S2600	"6000000012898544484"
#   P26 spouse = Q16650516 Mikael von Törne
LAST	P26	Q16650516	S2600	"6000000012898544484"
#   P40 child = Q16650517 Mikael von Törne
LAST	P40	Q16650517	S2600	"6000000012898544484"
#   Q16650516 Mikael von Törne: P26 spouse = the item just created
Q16650516	P26	LAST	S2600	"6000000012898544484"
#   Q16650517 Mikael von Törne: P25 mother = the item just created
Q16650517	P25	LAST	S2600	"6000000012898544484"
#   the item just created: P735 given name = Q4120836 Johanna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q4120836	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16423275 Elisabet, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q16423275	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Jorunn Jonsdatter Li"
LAST	Len	"Jorunn Jonsdatter Li"
#   set the mul label to "Jorunn Jonsdatter Li"
LAST	Lmul	"Jorunn Jonsdatter Li"
#   set the ja label to "ヨルンン・ヨンスダッテル・リー"
LAST	Lja	"ヨルンン・ヨンスダッテル・リー"
#   set the zh label to "约伦·永斯达特·李"
LAST	Lzh	"约伦·永斯达特·李"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000038211894304 Jorunn Jonsdatter Li, qualified P1810 subject named as Jorunn Jonsdatter Li
LAST	P2600	"6000000038211894304"	P1810	"Jorunn Jonsdatter Li"
#   P569 date of birth = +1746-00-00T00:00:00Z/9
LAST	P569	+1746-00-00T00:00:00Z/9	S2600	"6000000038211894304"
#   P570 date of death = +1814-00-00T00:00:00Z/9
LAST	P570	+1814-00-00T00:00:00Z/9	S2600	"6000000038211894304"
#   P22 father = Q141180408 Jon Larsson Mæle
LAST	P22	Q141180408	S2600	"6000000038211894304"
#   P25 mother = Q141180412 Marta Rasmusdatter Li
LAST	P25	Q141180412	S2600	"6000000038211894304"
#   Q141180408 Jon Larsson Mæle: P40 child = the item just created
Q141180408	P40	LAST	S2600	"6000000038211894304"
#   Q141180412 Marta Rasmusdatter Li: P40 child = the item just created
Q141180412	P40	LAST	S2600	"6000000038211894304"
#   the item just created: P735 given name = Q1799021 Jorunn
LAST	P735	Q1799021
#   P734 family name = Q686223 Li, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q686223	P3831	Q28418670
#   add a mul alias "Jorunn Li"
LAST	Amul	"Jorunn Li"

# create a new item
CREATE
#   set the en label to "Malena Larsdatter Opstad"
LAST	Len	"Malena Larsdatter Opstad"
#   set the mul label to "Malena Larsdatter Opstad"
LAST	Lmul	"Malena Larsdatter Opstad"
#   add a mul alias "Malena Larsdatter Kvia"
LAST	Amul	"Malena Larsdatter Kvia"
#   set the ja label to "マレーナ・ラーシュダッテル・オプスタド"
LAST	Lja	"マレーナ・ラーシュダッテル・オプスタド"
#   set the zh label to "马莱纳·拉尔斯达特·奥普斯塔德"
LAST	Lzh	"马莱纳·拉尔斯达特·奥普斯塔德"
#   add a ja alias "マレーナ・ラーシュダッテル・クヴィア"
LAST	Aja	"マレーナ・ラーシュダッテル・クヴィア"
#   add a zh alias "马莱纳·拉尔斯达特·克维阿"
LAST	Azh	"马莱纳·拉尔斯达特·克维阿"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003492049563 Malena Larsdatter Opstad, qualified P1810 subject named as Malena Larsdatter Kvia
LAST	P2600	"6000000003492049563"	P1810	"Malena Larsdatter Kvia"
#   P569 date of birth = +1704-00-00T00:00:00Z/9
LAST	P569	+1704-00-00T00:00:00Z/9	S2600	"6000000003492049563"
#   P570 date of death = +1791-00-00T00:00:00Z/9
LAST	P570	+1791-00-00T00:00:00Z/9	S2600	"6000000003492049563"
#   P40 child = Q141216600 Astrid Omundsdatter Grøtheim
LAST	P40	Q141216600	S2600	"6000000003492049563"
#   Q141216600 Astrid Omundsdatter Grøtheim: P25 mother = the item just created
Q141216600	P25	LAST	S2600	"6000000003492049563"
#   the item just created: P735 given name = Q5990536 Malena
LAST	P735	Q5990536
#   P734 family name = Q40200002, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q40200002	P3831	Q2507958
#   P734 family name = Q37268235 Opstad, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q37268235	P3831	Q28418670
#   add a mul alias "Malena Opstad"
LAST	Amul	"Malena Opstad"

# create a new item
CREATE
#   set the en label to "Margareta Elisabet Roos"
LAST	Len	"Margareta Elisabet Roos"
#   set the mul label to "Margareta Elisabet Roos"
LAST	Lmul	"Margareta Elisabet Roos"
#   set the ja label to "マルガレータ・エリーザベト・ルース"
LAST	Lja	"マルガレータ・エリーザベト・ルース"
#   set the zh label to "瑪格麗塔·伊丽莎白·罗奥斯"
LAST	Lzh	"瑪格麗塔·伊丽莎白·罗奥斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000002759919665 Margareta Elisabet Roos, qualified P1810 subject named as Margareta Elisabet Roos
LAST	P2600	"6000000002759919665"	P1810	"Margareta Elisabet Roos"
#   P569 date of birth = +1779-09-16T00:00:00Z/11
LAST	P569	+1779-09-16T00:00:00Z/11	S2600	"6000000002759919665"
#   P570 date of death = +1806-03-20T00:00:00Z/11
LAST	P570	+1806-03-20T00:00:00Z/11	S2600	"6000000002759919665"
#   P26 spouse = Q333297 Frans Michael Zachrichsson Franzén
LAST	P26	Q333297	S2600	"6000000002759919665"
#   Q333297 Frans Michael Zachrichsson Franzén: P26 spouse = the item just created
Q333297	P26	LAST	S2600	"6000000002759919665"
#   the item just created: P735 given name = Q8274988 Margareta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q8274988	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16423275 Elisabet, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q16423275	P1545	"2"	P3831	Q245025
#   P734 family name = Q10656802 Roos
LAST	P734	Q10656802
#   add a mul alias "Lilly Roos"
LAST	Amul	"Lilly Roos"

# create a new item
CREATE
#   set the mul label to "NN"
LAST	Lmul	"NN"
#   set the ca label to "mare de Anders Persson"
LAST	Lca	"mare de Anders Persson"
#   set the da label to "mor til Anders Persson"
LAST	Lda	"mor til Anders Persson"
#   set the de label to "Mutter von Anders Persson"
LAST	Lde	"Mutter von Anders Persson"
#   set the en label to "mother of Anders Persson"
LAST	Len	"mother of Anders Persson"
#   set the es label to "madre de Anders Persson"
LAST	Les	"madre de Anders Persson"
#   set the it label to "madre di Anders Persson"
LAST	Lit	"madre di Anders Persson"
#   set the ja label to "アンデルス・パーソンの母"
LAST	Lja	"アンデルス・パーソンの母"
#   set the nb label to "mor til Anders Persson"
LAST	Lnb	"mor til Anders Persson"
#   set the nl label to "moeder van Anders Persson"
LAST	Lnl	"moeder van Anders Persson"
#   set the pt label to "mãe de Anders Persson"
LAST	Lpt	"mãe de Anders Persson"
#   set the sv label to "mor till Anders Persson"
LAST	Lsv	"mor till Anders Persson"
#   set the zh label to "安德斯·佩尔松之母"
LAST	Lzh	"安德斯·佩尔松之母"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000017535915136 NN, qualified P1810 subject named as NN
LAST	P2600	"6000000017535915136"	P1810	"NN"
#   P569 date of birth = +1600-00-00T00:00:00Z/9
LAST	P569	+1600-00-00T00:00:00Z/9	S2600	"6000000017535915136"
#   P570 date of death = +1673-00-00T00:00:00Z/9
LAST	P570	+1673-00-00T00:00:00Z/9	S2600	"6000000017535915136"
#   P40 child = Q141216455 Anders Persson
LAST	P40	Q141216455	S2600	"6000000017535915136"
#   Q141216455 Anders Persson: P25 mother = the item just created
Q141216455	P25	LAST	S2600	"6000000017535915136"

# create a new item
CREATE
#   the item just created: set the en label to "Per Nilsson"
LAST	Len	"Per Nilsson"
#   set the mul label to "Per Nilsson"
LAST	Lmul	"Per Nilsson"
#   set the ja label to "ペール・ニルソン"
LAST	Lja	"ペール・ニルソン"
#   set the zh label to "佩尔·尼尔松"
LAST	Lzh	"佩尔·尼尔松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000019178738670 Per Nilsson, qualified P1810 subject named as Per Nilsson
LAST	P2600	"6000000019178738670"	P1810	"Per Nilsson"
#   P569 date of birth = +1600-00-00T00:00:00Z/9
LAST	P569	+1600-00-00T00:00:00Z/9	S2600	"6000000019178738670"
#   P570 date of death = +1677-00-00T00:00:00Z/9
LAST	P570	+1677-00-00T00:00:00Z/9	S2600	"6000000019178738670"
#   P40 child = Q141216455 Anders Persson
LAST	P40	Q141216455	S2600	"6000000019178738670"
#   Q141216455 Anders Persson: P22 father = the item just created
Q141216455	P22	LAST	S2600	"6000000019178738670"
#   the item just created: P735 given name = Q13582800 Per
LAST	P735	Q13582800
#   P734 family name = Q15829860 Nilsson
LAST	P734	Q15829860

# create a new item
CREATE
#   set the mul label to "NN"
LAST	Lmul	"NN"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000184732995834 NN Private, qualified P1810 subject named as Private
LAST	P2600	"6000000184732995834"	P1810	"Private"
#   P22 father = Q141216500 NN Private
LAST	P22	Q141216500	S2600	"6000000184732995834"
#   Q141216500 NN Private: P40 child = the item just created
Q141216500	P40	LAST	S2600	"6000000184732995834"

# create a new item
CREATE
#   the item just created: set the mul label to "NN"
LAST	Lmul	"NN"
#   set the ca label to "filla de Herbert August Pierson"
LAST	Lca	"filla de Herbert August Pierson"
#   set the da label to "datter af Herbert August Pierson"
LAST	Lda	"datter af Herbert August Pierson"
#   set the de label to "Tochter von Herbert August Pierson"
LAST	Lde	"Tochter von Herbert August Pierson"
#   set the en label to "daughter of Herbert August Pierson"
LAST	Len	"daughter of Herbert August Pierson"
#   set the es label to "hija de Herbert August Pierson"
LAST	Les	"hija de Herbert August Pierson"
#   set the it label to "figlia di Herbert August Pierson"
LAST	Lit	"figlia di Herbert August Pierson"
#   set the ja label to "ハーバート・アウグスト・ピアソンの娘"
LAST	Lja	"ハーバート・アウグスト・ピアソンの娘"
#   set the nb label to "datter av Herbert August Pierson"
LAST	Lnb	"datter av Herbert August Pierson"
#   set the nl label to "dochter van Herbert August Pierson"
LAST	Lnl	"dochter van Herbert August Pierson"
#   set the pt label to "filha de Herbert August Pierson"
LAST	Lpt	"filha de Herbert August Pierson"
#   set the sv label to "dotter till Herbert August Pierson"
LAST	Lsv	"dotter till Herbert August Pierson"
#   set the zh label to "赫伯特·奥古斯特·皮尔逊之女"
LAST	Lzh	"赫伯特·奥古斯特·皮尔逊之女"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000180043041886 NN Private, qualified P1810 subject named as Private
LAST	P2600	"6000000180043041886"	P1810	"Private"
#   P22 father = Q141198408 Herbert August Pierson
LAST	P22	Q141198408	S2600	"6000000180043041886"
#   P25 mother = Q141168801 Cora Estelle Pierson
LAST	P25	Q141168801	S2600	"6000000180043041886"
#   Q141198408 Herbert August Pierson: P40 child = the item just created
Q141198408	P40	LAST	S2600	"6000000180043041886"
#   Q141168801 Cora Estelle Pierson: P40 child = the item just created
Q141168801	P40	LAST	S2600	"6000000180043041886"

# create a new item
CREATE
#   the item just created: set the en label to "Ragnhild Ingebretsdatter Voster"
LAST	Len	"Ragnhild Ingebretsdatter Voster"
#   set the mul label to "Ragnhild Ingebretsdatter Voster"
LAST	Lmul	"Ragnhild Ingebretsdatter Voster"
#   set the ja label to "ラグンヒル・インゲブレトスダッテル・ヴォステル"
LAST	Lja	"ラグンヒル・インゲブレトスダッテル・ヴォステル"
#   set the zh label to "拉格希尔德·因盖布雷特斯达特·沃斯特尔"
LAST	Lzh	"拉格希尔德·因盖布雷特斯达特·沃斯特尔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000007980728958 Ragnhild Ingebretsdatter Voster, qualified P1810 subject named as Ragnhild Ingebretsdatter Voster
LAST	P2600	"6000000007980728958"	P1810	"Ragnhild Ingebretsdatter Voster"
#   P569 date of birth = +1617-00-00T00:00:00Z/9
LAST	P569	+1617-00-00T00:00:00Z/9	S2600	"6000000007980728958"
#   P570 date of death = +1708-00-00T00:00:00Z/9
LAST	P570	+1708-00-00T00:00:00Z/9	S2600	"6000000007980728958"
#   P22 father = Q141205913 Ingebret Pederson Voster
LAST	P22	Q141205913	S2600	"6000000007980728958"
#   P25 mother = Q141205899 Bergitte Ivarsdatter Tjentland
LAST	P25	Q141205899	S2600	"6000000007980728958"
#   Q141205913 Ingebret Pederson Voster: P40 child = the item just created
Q141205913	P40	LAST	S2600	"6000000007980728958"
#   Q141205899 Bergitte Ivarsdatter Tjentland: P40 child = the item just created
Q141205899	P40	LAST	S2600	"6000000007980728958"
#   the item just created: P735 given name = Q1390292 Ragnhild
LAST	P735	Q1390292

# create a new item
CREATE
#   set the en label to "Ragnhild Kristine Øystensdatter Nese"
LAST	Len	"Ragnhild Kristine Øystensdatter Nese"
#   set the mul label to "Ragnhild Kristine Øystensdatter Nese"
LAST	Lmul	"Ragnhild Kristine Øystensdatter Nese"
#   set the ja label to "ラグンヒル・クリスティン・オイステンスダッテル・ネセ"
LAST	Lja	"ラグンヒル・クリスティン・オイステンスダッテル・ネセ"
#   set the zh label to "拉格希尔德·克丽丝汀·奥伊斯滕斯达特·内塞"
LAST	Lzh	"拉格希尔德·克丽丝汀·奥伊斯滕斯达特·内塞"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000010479856178 Ragnhild Kristine Øystensdatter Nese, qualified P1810 subject named as Ragnhild Kristine Øystensdatter Nese
LAST	P2600	"6000000010479856178"	P1810	"Ragnhild Kristine Øystensdatter Nese"
#   P569 date of birth = +1786-09-05T00:00:00Z/11
LAST	P569	+1786-09-05T00:00:00Z/11	S2600	"6000000010479856178"
#   P570 date of death = +1871-02-06T00:00:00Z/11
LAST	P570	+1871-02-06T00:00:00Z/11	S2600	"6000000010479856178"
#   P26 spouse = Q141223432 Osmund Larsson Nese
LAST	P26	Q141223432	S2600	"6000000010479856178"
#   Q141223432 Osmund Larsson Nese: P26 spouse = the item just created
Q141223432	P26	LAST	S2600	"6000000010479856178"
#   Q141223423 Harlverg B. Ekman: P3373 sibling = Q141205908 Gotfred Olai Ekman
Q141223423	P3373	Q141205908	S2600	"285886949080005081"
#   Q141219059 Gustava Maria Sofia Mannerheim: P735 given name = Q325872 Maria, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141219059	P735	Q325872	P1545	"2"	P3831	Q245025
#   P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q141219059	P735	Q18201520	P1545	"3"	P3831	Q245025
#   Q141223426 Isak Reinhold Sahlberg: P26 spouse = Q141223428 Lovisa Catharina Polviander
Q141223426	P26	Q141223428	S2600	"5580425653980118255"
#   Q141223428 Lovisa Catharina Polviander: P26 spouse = Q141223426 Isak Reinhold Sahlberg
Q141223428	P26	Q141223426	S2600	"5580429510180056637"
#   Q141219324 Sofia Maria Mannerheim: P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141219324	P735	Q18201520	P1545	"1"	P7452	Q3409033
#   P735 given name = Q325872 Maria, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141219324	P735	Q325872	P1545	"2"	P3831	Q245025
#   Q141219332 Sofia Wadenstierna: P735 given name = Q18201520 Sofia
Q141219332	P735	Q18201520
#   Q141219316 Reiar Einarsen Kydland: P734 family name = Q30514142
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
#   Q141223432 Osmund Larsson Nese: P735 given name = Q7107242 Osmund
Q141223432	P735	Q7107242
#   P734 family name = Q37543374
Q141223432	P734	Q37543374
#   Q141198422 Iver Pedersen Sandsmark: P734 family name = Q37541803
Q141198422	P734	Q37541803
#   Q141198414 Ingeborg Olsdatter Sandsmark: P734 family name = Q37541803
Q141198414	P734	Q37541803
#   Q141198396 Erling Juel Wendt: P735 given name = Q123820113, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141198396	P735	Q123820113	P1545	"2"	P3831	Q245025
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
#   Q141216488 Lars Jonsen Landsnes: P734 family name = Q122837341
Q141216488	P734	Q122837341
#   Q141216632 Magdalena Lauritsd Hogganvik: P734 family name = Q55240992
Q141216632	P734	Q55240992
#   Q141216396 Lisbet Olavsdatter Håland: P734 family name = Q30580079
Q141216396	P734	Q30580079
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
#   Q141219291 Maria Hansdatter Austrått: P735 given name = Q325872 Maria
Q141219291	P735	Q325872
#   Q141223436 Tore Underberge III: P735 given name = Q1548096 Tore, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141223436	P735	Q1548096	P1545	"1"	P7452	Q3409033
#   Q141205919 Malena Hansdatter Bø: P734 family name = Q30253098
Q141205919	P734	Q30253098
#   Q141219349 Tørres Jonson Grannes: P735 given name = Q12008164
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
#   Q141205937 Ragnhild Eyvindsdotter Eyvindsdotter: P40 child = Q141223436 Tore Underberge III
Q141205937	P40	Q141223436	S2600	"6000000008686109792"
#   Q141223430 Magdalena Sofia Falkenberg af Bålby: P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141223430	P735	Q18201520	P1545	"2"	P3831	Q245025
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
#   Q141223434 Samuel Aslakson Tunheim: P26 spouse = Q141223417 Elen Malena Halvorsdtr Tunheim
Q141223434	P26	Q141223417	S2600	"6000000011971496046"
#   P734 family name = Q36927172
Q141223434	P734	Q36927172
#   Q141219202 Elen Kristoffersdotter Nese: P40 child = Q141223432 Osmund Larsson Nese
Q141219202	P40	Q141223432	S2600	"6000000012587664964"
#   P734 family name = Q37543374
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
#   Q141189084 Martin Tollefson Tunheim: P734 family name = Q36927172
Q141189084	P734	Q36927172
#   Q141219155 Christina Maria Adelheim: P735 given name = Q1083457 Christina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
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
#   Q141223411 Anna Mårtensdotter: P735 given name = Q666578 Anna
Q141223411	P735	Q666578
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
#   Q141223417 Elen Malena Halvorsdtr Tunheim: P26 spouse = Q141223434 Samuel Aslakson Tunheim
Q141223417	P26	Q141223434	S2600	"6000000029983713844"
#   P734 family name = Q36927172
Q141223417	P734	Q36927172
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
#   Q141223424 Harriet Lane Tunheim: P734 family name = Q36927172
Q141223424	P734	Q36927172
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
#   Q141216363 Anne Govertsdtr. Bratland: P735 given name = Q564684 Anne, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141216363	P735	Q564684	P1545	"1"	P7452	Q3409033
#   Q141223427 Johanna Matilda Carlsdotter: P735 given name = Q4120836 Johanna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141223427	P735	Q4120836	P1545	"1"	P7452	Q3409033
#   P735 given name = Q2054021 Matilda, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141223427	P735	Q2054021	P1545	"2"	P3831	Q245025
#   Q141219160 Christina, Sofia Carlsdotter: P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
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

