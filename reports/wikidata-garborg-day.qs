# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   828 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   set the zh label to "奥托·赖因霍尔德·斯特罗姆费尔特"
Q2040261	Lzh	"奥托·赖因霍尔德·斯特罗姆费尔特"
#   Q141200604 Anna Nilsdotter: set the ja label to "アンナ・ニルスドッテル"
Q141200604	Lja	"アンナ・ニルスドッテル"
#   set the zh label to "安娜·尼尔斯多特"
Q141200604	Lzh	"安娜·尼尔斯多特"
#   Q141205931 Olof Olofsson: set the ja label to "オロフ・オロフソン"
Q141205931	Lja	"オロフ・オロフソン"
#   set the zh label to "奥洛夫·奥洛夫松"
Q141205931	Lzh	"奥洛夫·奥洛夫松"
#   Q5562579 Magnus Petri Aurivillius: add a mul alias "Magnus Petri Aurivillius"
Q5562579	Amul	"Magnus Petri Aurivillius"
#   set the ja label to "マグヌス・アウリヴィリウス"
Q5562579	Lja	"マグヌス・アウリヴィリウス"
#   set the zh label to "马格努斯·奥里维利乌斯"
Q5562579	Lzh	"马格努斯·奥里维利乌斯"
#   Q5613434 Börje Cronberg: set the mul label to "Börje Cronberg"
Q5613434	Lmul	"Börje Cronberg"
#   add a mul alias "Börje Olofsson Bureus"
Q5613434	Amul	"Börje Olofsson Bureus"
#   set the ja label to "ボリイェ・クロンベルグ"
Q5613434	Lja	"ボリイェ・クロンベルグ"
#   set the zh label to "博尔耶·克龙贝尔格"
Q5613434	Lzh	"博尔耶·克龙贝尔格"
#   Q141216605 Gunilla Jonsdotter: set the zh label to "古尼拉·永斯多特"
Q141216605	Lzh	"古尼拉·永斯多特"
#   Q5930987 Carl Otto Lagercrantz: set the mul label to "Carl Otto Lagercrantz"
Q5930987	Lmul	"Carl Otto Lagercrantz"
#   set the ja label to "カール・オットー・ラーゲルクランツ"
Q5930987	Lja	"カール・オットー・ラーゲルクランツ"

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Anna Asbjørnsdatter Bø"
LAST	Len	"Anna Asbjørnsdatter Bø"
#   set the mul label to "Anna Asbjørnsdatter Bø"
LAST	Lmul	"Anna Asbjørnsdatter Bø"
#   set the ja label to "アンナ・アスブヨルンスダッテル・ベー"
LAST	Lja	"アンナ・アスブヨルンスダッテル・ベー"
#   set the zh label to "安娜·阿斯布约尔恩斯达特·鲍伊"
LAST	Lzh	"安娜·阿斯布约尔恩斯达特·鲍伊"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000222520767827 Anna Asbjørnsdatter Bø, qualified P1810 subject named as Anna Asbjørnsdatter Bø
LAST	P2600	"6000000222520767827"	P1810	"Anna Asbjørnsdatter Bø"
#   P569 date of birth = +1771-00-00T00:00:00Z/9
LAST	P569	+1771-00-00T00:00:00Z/9	S2600	"6000000222520767827"
#   P570 date of death = +1838-12-11T00:00:00Z/11
LAST	P570	+1838-12-11T00:00:00Z/11	S2600	"6000000222520767827"
#   P22 father = Q141216458 Asbjørn Gunnarson Bø
LAST	P22	Q141216458	S2600	"6000000222520767827"
#   P25 mother = Q141216456 Anna Helgesdotter Opstad
LAST	P25	Q141216456	S2600	"6000000222520767827"
#   Q141216458 Asbjørn Gunnarson Bø: P40 child = the item just created
Q141216458	P40	LAST	S2600	"6000000222520767827"
#   Q141216456 Anna Helgesdotter Opstad: P40 child = the item just created
Q141216456	P40	LAST	S2600	"6000000222520767827"
#   the item just created: P735 given name = Q666578 Anna
LAST	P735	Q666578
#   P734 family name = Q30253098
LAST	P734	Q30253098

# create a new item
CREATE
#   set the en label to "Anne Serine Tollefsdotter Tunheim"
LAST	Len	"Anne Serine Tollefsdotter Tunheim"
#   set the mul label to "Anne Serine Tollefsdotter Tunheim"
LAST	Lmul	"Anne Serine Tollefsdotter Tunheim"
#   set the ja label to "アン・セリネ・トレフスドッテル・トゥンヘイム"
LAST	Lja	"アン・セリネ・トレフスドッテル・トゥンヘイム"
#   set the zh label to "安妮·塞里内·托莱夫斯多特·通海姆"
LAST	Lzh	"安妮·塞里内·托莱夫斯多特·通海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000037737863833 Anne Serine Tollefsdotter Tunheim, qualified P1810 subject named as Anne Serine Tollefsdotter Tunheim
LAST	P2600	"6000000037737863833"	P1810	"Anne Serine Tollefsdotter Tunheim"
#   P569 date of birth = +1861-08-24T00:00:00Z/11
LAST	P569	+1861-08-24T00:00:00Z/11	S2600	"6000000037737863833"
#   P570 date of death = +1875-05-25T00:00:00Z/11
LAST	P570	+1875-05-25T00:00:00Z/11	S2600	"6000000037737863833"
#   P22 father = Q141200112 Tollef Pederson Tunheim
LAST	P22	Q141200112	S2600	"6000000037737863833"
#   P25 mother = Q141199826 Anna Maria Samuelsdtr. Tunheim
LAST	P25	Q141199826	S2600	"6000000037737863833"
#   Q141200112 Tollef Pederson Tunheim: P40 child = the item just created
Q141200112	P40	LAST	S2600	"6000000037737863833"
#   Q141199826 Anna Maria Samuelsdtr. Tunheim: P40 child = the item just created
Q141199826	P40	LAST	S2600	"6000000037737863833"
#   the item just created: P735 given name = Q564684 Anne, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q564684	P1545	"1"	P7452	Q3409033
#   P735 given name = Q136121543, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q136121543	P1545	"2"	P3831	Q245025
#   P734 family name = Q36927172, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q36927172	P3831	Q28418670
#   add a mul alias "Anne Serine Tunheim"
LAST	Amul	"Anne Serine Tunheim"

# create a new item
CREATE
#   set the en label to "Elisabet Boije"
LAST	Len	"Elisabet Boije"
#   set the mul label to "Elisabet Boije"
LAST	Lmul	"Elisabet Boije"
#   set the ja label to "エリーザベト・ボイイェ"
LAST	Lja	"エリーザベト・ボイイェ"
#   set the zh label to "伊丽莎白·博伊耶"
LAST	Lzh	"伊丽莎白·博伊耶"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000009813964400 Elisabet Boije, qualified P1810 subject named as Elisabet Boije
LAST	P2600	"6000000009813964400"	P1810	"Elisabet Boije"
#   P569 date of birth = +1673-00-00T00:00:00Z/9
LAST	P569	+1673-00-00T00:00:00Z/9	S2600	"6000000009813964400"
#   P570 date of death = +1734-06-13T00:00:00Z/11
LAST	P570	+1734-06-13T00:00:00Z/11	S2600	"6000000009813964400"
#   P26 spouse = Q6229400 Elias von Walcker
LAST	P26	Q6229400	S2600	"6000000009813964400"
#   P40 child = Q141225681 Anna Margareta von Walcker
LAST	P40	Q141225681	S2600	"6000000009813964400"
#   Q6229400 Elias von Walcker: P26 spouse = the item just created
Q6229400	P26	LAST	S2600	"6000000009813964400"
#   Q141225681 Anna Margareta von Walcker: P25 mother = the item just created
Q141225681	P25	LAST	S2600	"6000000009813964400"
#   the item just created: P735 given name = Q16423275 Elisabet
LAST	P735	Q16423275
#   P734 family name = Q28149669 Boije
LAST	P734	Q28149669

# create a new item
CREATE
#   set the en label to "Gunnar Sahlin"
LAST	Len	"Gunnar Sahlin"
#   set the mul label to "Gunnar Sahlin"
LAST	Lmul	"Gunnar Sahlin"
#   set the ja label to "グンナー・サリン"
LAST	Lja	"グンナー・サリン"
#   set the zh label to "贡纳尔·萨林"
LAST	Lzh	"贡纳尔·萨林"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003002364630 Gunnar Sahlin, qualified P1810 subject named as Gunnar Sahlin
LAST	P2600	"6000000003002364630"	P1810	"Gunnar Sahlin"
#   P569 date of birth = +1914-09-10T00:00:00Z/11
LAST	P569	+1914-09-10T00:00:00Z/11	S2600	"6000000003002364630"
#   P570 date of death = +1980-06-13T00:00:00Z/11
LAST	P570	+1980-06-13T00:00:00Z/11	S2600	"6000000003002364630"
#   P26 spouse = Q141223742 Ragnhild Sofie Sahlin
LAST	P26	Q141223742	S2600	"6000000003002364630"
#   Q141223742 Ragnhild Sofie Sahlin: P26 spouse = the item just created
Q141223742	P26	LAST	S2600	"6000000003002364630"

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
#   set the en label to "Hedvig Augusta af Söderling"
LAST	Len	"Hedvig Augusta af Söderling"
#   set the mul label to "Hedvig Augusta af Söderling"
LAST	Lmul	"Hedvig Augusta af Söderling"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000011713042906 Hedvig Augusta af Söderling, qualified P1810 subject named as Hedvig Augusta af Söderling
LAST	P2600	"6000000011713042906"	P1810	"Hedvig Augusta af Söderling"
#   P569 date of birth = +1761-08-12T00:00:00Z/11
LAST	P569	+1761-08-12T00:00:00Z/11	S2600	"6000000011713042906"
#   P570 date of death = +1794-04-01T00:00:00Z/11
LAST	P570	+1794-04-01T00:00:00Z/11	S2600	"6000000011713042906"
#   P26 spouse = Q3462736 Samuel Gustaf Hermelin
LAST	P26	Q3462736	S2600	"6000000011713042906"
#   Q3462736 Samuel Gustaf Hermelin: P26 spouse = the item just created
Q3462736	P26	LAST	S2600	"6000000011713042906"
#   the item just created: P735 given name = Q13648620 Hedvig, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q13648620	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1370330 Augusta, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1370330	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Hedvig Jakobsdotter Cajanus"
LAST	Len	"Hedvig Jakobsdotter Cajanus"
#   set the mul label to "Hedvig Jakobsdotter Cajanus"
LAST	Lmul	"Hedvig Jakobsdotter Cajanus"
#   add a mul alias "Hedvig Jakobsdotter Chydenius"
LAST	Amul	"Hedvig Jakobsdotter Chydenius"
#   set the ja label to "ヘドヴィグ・ヤコブスドッテル・カヤヌス"
LAST	Lja	"ヘドヴィグ・ヤコブスドッテル・カヤヌス"
#   set the zh label to "海德维格·雅科布斯多特·卡雅努斯"
LAST	Lzh	"海德维格·雅科布斯多特·卡雅努斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000010760135378 Hedvig Jakobsdotter Cajanus, qualified P1810 subject named as Hedvig Jakobsdotter Chydenius
LAST	P2600	"6000000010760135378"	P1810	"Hedvig Jakobsdotter Chydenius"
#   P569 date of birth = +1743-03-23T00:00:00Z/11
LAST	P569	+1743-03-23T00:00:00Z/11	S2600	"6000000010760135378"
#   P570 date of death = +1817-11-17T00:00:00Z/11
LAST	P570	+1817-11-17T00:00:00Z/11	S2600	"6000000010760135378"
#   P22 father = Q141224209 Jacob Chydenius
LAST	P22	Q141224209	S2600	"6000000010760135378"
#   P25 mother = Q141224012 Hedvig Chydenius
LAST	P25	Q141224012	S2600	"6000000010760135378"
#   Q141224209 Jacob Chydenius: P40 child = the item just created
Q141224209	P40	LAST	S2600	"6000000010760135378"
#   Q141224012 Hedvig Chydenius: P40 child = the item just created
Q141224012	P40	LAST	S2600	"6000000010760135378"
#   the item just created: P735 given name = Q13648620 Hedvig
LAST	P735	Q13648620
#   add a mul alias "Chydenia Cajanus"
LAST	Amul	"Chydenia Cajanus"
#   add a mul alias "Hedvig Cajanus"
LAST	Amul	"Hedvig Cajanus"

# create a new item
CREATE
#   set the en label to "Jørgine Bergitte Paulsdatter Orre"
LAST	Len	"Jørgine Bergitte Paulsdatter Orre"
#   set the mul label to "Jørgine Bergitte Paulsdatter Orre"
LAST	Lmul	"Jørgine Bergitte Paulsdatter Orre"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000077299441506 Jørgine Bergitte Paulsdatter Orre, qualified P1810 subject named as Jørgine Bergitte Paulsdatter Orre
LAST	P2600	"6000000077299441506"	P1810	"Jørgine Bergitte Paulsdatter Orre"
#   P569 date of birth = +1854-03-16T00:00:00Z/11
LAST	P569	+1854-03-16T00:00:00Z/11	S2600	"6000000077299441506"
#   P570 date of death = +1945-01-06T00:00:00Z/11
LAST	P570	+1945-01-06T00:00:00Z/11	S2600	"6000000077299441506"
#   P22 father = Q141224861 Paul Pederson Borsheim
LAST	P22	Q141224861	S2600	"6000000077299441506"
#   Q141224861 Paul Pederson Borsheim: P40 child = the item just created
Q141224861	P40	LAST	S2600	"6000000077299441506"

# create a new item
CREATE
#   the item just created: set the en label to "Kirsti Olsdatter Bærheim"
LAST	Len	"Kirsti Olsdatter Bærheim"
#   set the mul label to "Kirsti Olsdatter Bærheim"
LAST	Lmul	"Kirsti Olsdatter Bærheim"
#   set the ja label to "キルスティ・オルスダッテル・ベルヘイム"
LAST	Lja	"キルスティ・オルスダッテル・ベルヘイム"
#   set the zh label to "基尔斯蒂·奥尔斯达特·贝尔赫伊姆"
LAST	Lzh	"基尔斯蒂·奥尔斯达特·贝尔赫伊姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003492083933 Kirsti Olsdatter Bærheim, qualified P1810 subject named as Kirsti Olsdatter Bærheim
LAST	P2600	"6000000003492083933"	P1810	"Kirsti Olsdatter Bærheim"
#   P569 date of birth = +1684-00-00T00:00:00Z/9
LAST	P569	+1684-00-00T00:00:00Z/9	S2600	"6000000003492083933"
#   P570 date of death = +1748-00-00T00:00:00Z/9
LAST	P570	+1748-00-00T00:00:00Z/9	S2600	"6000000003492083933"
#   P40 child = Q141219052 Anna Olsdatter Heigre
LAST	P40	Q141219052	S2600	"6000000003492083933"
#   Q141219052 Anna Olsdatter Heigre: P25 mother = the item just created
Q141219052	P25	LAST	S2600	"6000000003492083933"
#   the item just created: P735 given name = Q4349920 Kirsti
LAST	P735	Q4349920
#   P5056 patronym or matronym = Q51885688 Olsdatter
LAST	P5056	Q51885688
#   P734 family name = Q40246530 Bærheim, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q40246530	P3831	Q28418670
#   add a mul alias "Kirsti Bærheim"
LAST	Amul	"Kirsti Bærheim"

# create a new item
CREATE
#   set the en label to "Kristoffer Olson Tjåland"
LAST	Len	"Kristoffer Olson Tjåland"
#   set the mul label to "Kristoffer Olson Tjåland"
LAST	Lmul	"Kristoffer Olson Tjåland"
#   set the ja label to "クリストファー・オルソン・トヨーランド"
LAST	Lja	"クリストファー・オルソン・トヨーランド"
#   set the zh label to "克里斯托弗·奥尔森·特约兰德"
LAST	Lzh	"克里斯托弗·奥尔森·特约兰德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005609534679 Kristoffer Olson Tjåland, qualified P1810 subject named as Kristoffer Olson Tjåland
LAST	P2600	"6000000005609534679"	P1810	"Kristoffer Olson Tjåland"
#   P569 date of birth = +1689-00-00T00:00:00Z/9
LAST	P569	+1689-00-00T00:00:00Z/9	S2600	"6000000005609534679"
#   P570 date of death = +1759-00-00T00:00:00Z/9
LAST	P570	+1759-00-00T00:00:00Z/9	S2600	"6000000005609534679"
#   P40 child = Q141216609 Inger Kristoffersdatter Skårland
LAST	P40	Q141216609	S2600	"6000000005609534679"
#   Q141216609 Inger Kristoffersdatter Skårland: P22 father = the item just created
Q141216609	P22	LAST	S2600	"6000000005609534679"
#   the item just created: P735 given name = Q1789415 Kristoffer
LAST	P735	Q1789415
#   add a mul alias "Kristoffer Tjåland"
LAST	Amul	"Kristoffer Tjåland"

# create a new item
CREATE
#   set the en label to "Lars Osmundsen Nese"
LAST	Len	"Lars Osmundsen Nese"
#   set the mul label to "Lars Osmundsen Nese"
LAST	Lmul	"Lars Osmundsen Nese"
#   set the ja label to "ラース・オスムンドセン・ネセ"
LAST	Lja	"ラース・オスムンドセン・ネセ"
#   set the zh label to "拉尔斯·奥斯蒙德森·内塞"
LAST	Lzh	"拉尔斯·奥斯蒙德森·内塞"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000010480210324 Lars Osmundsen Nese, qualified P1810 subject named as Lars Osmundsen Nese
LAST	P2600	"6000000010480210324"	P1810	"Lars Osmundsen Nese"
#   P569 date of birth = +1815-01-29T00:00:00Z/11
LAST	P569	+1815-01-29T00:00:00Z/11	S2600	"6000000010480210324"
#   P570 date of death = +1901-04-12T00:00:00Z/11
LAST	P570	+1901-04-12T00:00:00Z/11	S2600	"6000000010480210324"
#   P22 father = Q141223432 Osmund Larsson Nese
LAST	P22	Q141223432	S2600	"6000000010480210324"
#   Q141223432 Osmund Larsson Nese: P40 child = the item just created
Q141223432	P40	LAST	S2600	"6000000010480210324"

# create a new item
CREATE
#   the item just created: set the en label to "Ola Rasmussen Bø"
LAST	Len	"Ola Rasmussen Bø"
#   set the mul label to "Ola Rasmussen Bø"
LAST	Lmul	"Ola Rasmussen Bø"
#   set the ja label to "オーラ・ラスムセン・ベー"
LAST	Lja	"オーラ・ラスムセン・ベー"
#   set the zh label to "奥拉·拉斯穆森·鲍伊"
LAST	Lzh	"奥拉·拉斯穆森·鲍伊"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000225376871825 Ola Rasmussen Bø, qualified P1810 subject named as Ola Rasmussen Bø
LAST	P2600	"6000000225376871825"	P1810	"Ola Rasmussen Bø"
#   P569 date of birth = +1883-07-17T00:00:00Z/11
LAST	P569	+1883-07-17T00:00:00Z/11	S2600	"6000000225376871825"
#   P22 father = Q141189099 Rasmus Helgesen Bø
LAST	P22	Q141189099	S2600	"6000000225376871825"
#   P25 mother = Q141219050 Ane Olsdatter Bø
LAST	P25	Q141219050	S2600	"6000000225376871825"
#   Q141189099 Rasmus Helgesen Bø: P40 child = the item just created
Q141189099	P40	LAST	S2600	"6000000225376871825"
#   Q141219050 Ane Olsdatter Bø: P40 child = the item just created
Q141219050	P40	LAST	S2600	"6000000225376871825"
#   the item just created: P735 given name = Q96675523 Ola
LAST	P735	Q96675523
#   P734 family name = Q30253098
LAST	P734	Q30253098

# create a new item
CREATE
#   set the en label to "Peder Jonsen Voster"
LAST	Len	"Peder Jonsen Voster"
#   set the mul label to "Peder Jonsen Voster"
LAST	Lmul	"Peder Jonsen Voster"
#   set the ja label to "ペーダー・ヨンセン・ヴォステル"
LAST	Lja	"ペーダー・ヨンセン・ヴォステル"
#   set the zh label to "彼泽·永森·沃斯特尔"
LAST	Lzh	"彼泽·永森·沃斯特尔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000007980605161 Peder Jonsen Voster, qualified P1810 subject named as Peder Jonsen Voster
LAST	P2600	"6000000007980605161"	P1810	"Peder Jonsen Voster"
#   P569 date of birth = +1560-00-00T00:00:00Z/9
LAST	P569	+1560-00-00T00:00:00Z/9	S2600	"6000000007980605161"
#   P570 date of death = +1637-00-00T00:00:00Z/9
LAST	P570	+1637-00-00T00:00:00Z/9	S2600	"6000000007980605161"
#   P40 child = Q141205913 Ingebret Pederson Voster
LAST	P40	Q141205913	S2600	"6000000007980605161"
#   Q141205913 Ingebret Pederson Voster: P22 father = the item just created
Q141205913	P22	LAST	S2600	"6000000007980605161"
#   the item just created: P735 given name = Q10622039 Peder
LAST	P735	Q10622039
#   add a mul alias "Peder Voster"
LAST	Amul	"Peder Voster"

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
#   the item just created: set the en label to "Ulrika von Düben"
LAST	Len	"Ulrika von Düben"
#   set the mul label to "Ulrika von Düben"
LAST	Lmul	"Ulrika von Düben"
#   set the ja label to "ウルリカ・ヴォン・ディベン"
LAST	Lja	"ウルリカ・ヴォン・ディベン"
#   set the zh label to "乌尔里卡·翁·迪本"
LAST	Lzh	"乌尔里卡·翁·迪本"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000009063273551 Ulrika von Düben, qualified P1810 subject named as Ulrika von Düben
LAST	P2600	"6000000009063273551"	P1810	"Ulrika von Düben"
#   P569 date of birth = +1749-01-26T00:00:00Z/11
LAST	P569	+1749-01-26T00:00:00Z/11	S2600	"6000000009063273551"
#   P570 date of death = +1777-01-13T00:00:00Z/11
LAST	P570	+1777-01-13T00:00:00Z/11	S2600	"6000000009063273551"
#   P26 spouse = Q5626148 Carl Wilhelm von Düben
LAST	P26	Q5626148	S2600	"6000000009063273551"
#   Q5626148 Carl Wilhelm von Düben: P26 spouse = the item just created
Q5626148	P26	LAST	S2600	"6000000009063273551"
#   the item just created: P735 given name = Q18924998 Ulrika
LAST	P735	Q18924998

# create a new item
CREATE
#   set the en label to "Åsa Gunnbjørnsdotter Stordrange"
LAST	Len	"Åsa Gunnbjørnsdotter Stordrange"
#   set the mul label to "Åsa Gunnbjørnsdotter Stordrange"
LAST	Lmul	"Åsa Gunnbjørnsdotter Stordrange"
#   set the ja label to "オーサ・グンンブヨルンスドッテル・ストルドランゲ"
LAST	Lja	"オーサ・グンンブヨルンスドッテル・ストルドランゲ"
#   set the zh label to "奥萨·贡布约尔恩斯多特·斯托尔德兰盖"
LAST	Lzh	"奥萨·贡布约尔恩斯多特·斯托尔德兰盖"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000004559874338 Åsa Gunnbjørnsdotter Stordrange, qualified P1810 subject named as Åsa Gunnbjørnsdotter Stordrange
LAST	P2600	"6000000004559874338"	P1810	"Åsa Gunnbjørnsdotter Stordrange"
#   P569 date of birth = +1450-00-00T00:00:00Z/9
LAST	P569	+1450-00-00T00:00:00Z/9	S2600	"6000000004559874338"
#   P22 father = Q141199851 Lagmann Gunnbjørn Toresson Tengs
LAST	P22	Q141199851	S2600	"6000000004559874338"
#   Q141199851 Lagmann Gunnbjørn Toresson Tengs: P40 child = the item just created
Q141199851	P40	LAST	S2600	"6000000004559874338"
#   Q141225179 Maren Ellingsdatter Tunheim: P26 spouse = Q141225230 Osmund Andersen Tunheim
Q141225179	P26	Q141225230	S2600	"340026788150007985"
#   Q141225740 Jakob Chydenius: P22 father = Q141224209 Jacob Chydenius
Q141225740	P22	Q141224209	S2600	"6000000000583631058"
#   P25 mother = Q141224012 Hedvig Chydenius
Q141225740	P25	Q141224012	S2600	"6000000000583631058"
#   P2600 Geni.com profile ID = 6000000000583631058 Jakob Chydenius, qualified P1810 subject named as Jakob Chydenius
Q141225740	P2600	"6000000000583631058"	P1810	"Jakob Chydenius"	S2600	"6000000000583631058"
#   Q141225749 Jon Pedersen Trevland: P22 father = Q141198831 Peder Larsen Mjølhus
Q141225749	P22	Q141198831	S2600	"6000000001770193504"
#   P25 mother = Q141205938 Ranveig Olsd Trevland
Q141225749	P25	Q141205938	S2600	"6000000001770193504"
#   P2600 Geni.com profile ID = 6000000001770193504 Jon Pedersen Trevland, qualified P1810 subject named as Jon Pedersen Trevland
Q141225749	P2600	"6000000001770193504"	P1810	"Jon Pedersen Trevland"	S2600	"6000000001770193504"
#   P735 given name = Q13501137 Jon
Q141225749	P735	Q13501137
#   P5056 patronym or matronym = Q130233025, qualified P144 based on Q141198831 Peder Larsen Mjølhus
Q141225749	P5056	Q130233025	P144	Q141198831
#   Q141199851 Lagmann Gunnbjørn Toresson Tengs: P40 child = Q141242383 Bjørn Gunnbjørnsson Kvåvig
Q141199851	P40	Q141242383	S2600	"6000000002463510938"
#   Q141216602 Berta Guria Davidsdatter Stokka: P40 child = Q141242395 David Torgerson Stokka
Q141216602	P40	Q141242395	S2600	"6000000002726900648"
#   Q141216653 Torger Torgerson Stokka: P40 child = Q141242395 David Torgerson Stokka
Q141216653	P40	Q141242395	S2600	"6000000002726968193"
#   Q141223432 Osmund Larsson Nese: P40 child = Q141242389 Christian Osmundsen Nese
Q141223432	P40	Q141242389	S2600	"6000000002744891329"
#   Q141225230 Osmund Andersen Tunheim: P26 spouse = Q141225179 Maren Ellingsdatter Tunheim
Q141225230	P26	Q141225179	S2600	"6000000002763481707"
#   Q141225713 Ingeborg Simonsdatter Ytre Lima: P40 child = Q141223933 Ola Svenson Ytre Lima
Q141225713	P40	Q141223933	S2600	"6000000002836363103"
#   P2600 Geni.com profile ID = 6000000002836363103 Ingeborg Simonsdatter Ytre Lima, qualified P1810 subject named as Ingeborg Simonsdatter Ravndal
Q141225713	P2600	"6000000002836363103"	P1810	"Ingeborg Simonsdatter Ravndal"	S2600	"6000000002836363103"
#   P735 given name = Q656590 Ingeborg, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141225713	P735	Q656590	P1545	"1"	P7452	Q3409033
#   P734 family name = Q11255517 Lima
Q141225713	P734	Q11255517
#   Q141198375 Astri Torchelsdatter Øvre Time: P40 child = Q141225066 NN
Q141198375	P40	Q141225066	S2600	"6000000003731596731"
#   Q141242383 Bjørn Gunnbjørnsson Kvåvig: P22 father = Q141199851 Lagmann Gunnbjørn Toresson Tengs
Q141242383	P22	Q141199851	S2600	"6000000004569609494"
#   P2600 Geni.com profile ID = 6000000004569609494 Bjørn Gunnbjørnsson Kvåvig, qualified P1810 subject named as Bjørn Gunnbjørnsson Kvåvig
Q141242383	P2600	"6000000004569609494"	P1810	"Bjørn Gunnbjørnsson Kvåvig"	S2600	"6000000004569609494"
#   Q141199862 Helga Bjørnsdatter Tengs: P40 child = Q141242383 Bjørn Gunnbjørnsson Kvåvig
Q141199862	P40	Q141242383	S2600	"6000000004697849241"
#   Q141217369 Anna Osmundsd Stokka: P40 child = Q141225175 Malene Larsdtr. Alvseike
Q141217369	P40	Q141225175	S2600	"6000000005609304839"
#   Q141225702 Erik Guttormsson: P22 father = Q141223732 Guttorm Guttormsson
Q141225702	P22	Q141223732	S2600	"6000000007328872457"
#   P25 mother = Q141225787 Kristine NN
Q141225702	P25	Q141225787	S2600	"6000000007328872457"
#   P2600 Geni.com profile ID = 6000000007328872457 Erik Guttormsson, qualified P1810 subject named as Erik Guttormsson
Q141225702	P2600	"6000000007328872457"	P1810	"Erik Guttormsson"	S2600	"6000000007328872457"
#   Q141225772 Katarina Johansdotter Ståhlbom: P40 child = Q141224012 Hedvig Chydenius
Q141225772	P40	Q141224012	S2600	"6000000007367019257"
#   P26 spouse = Q141224900 Samuel Samuelis Hornaeus
Q141225772	P26	Q141224900	S2600	"6000000007367019257"
#   P2600 Geni.com profile ID = 6000000007367019257 Katarina Johansdotter Ståhlbom, qualified P1810 subject named as Katarina Johansdotter Ståhlbom
Q141225772	P2600	"6000000007367019257"	P1810	"Katarina Johansdotter Ståhlbom"	S2600	"6000000007367019257"
#   Q141225089 Christina Maria Silfverschiöld: P26 spouse = Q141225119 Göran Ehrenpreus
Q141225089	P26	Q141225119	S2600	"6000000008989027097"
#   Q141225119 Göran Ehrenpreus: P26 spouse = Q141225089 Christina Maria Silfverschiöld
Q141225119	P26	Q141225089	S2600	"6000000008989193521"
#   Q141225111 Ericus Nicolai Gestrinius: P26 spouse = Q141225068 Anna Mårtensdotter
Q141225111	P26	Q141225068	S2600	"6000000009298900297"
#   P735 given name = Q19830590 Nicolai, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141225111	P735	Q19830590	P1545	"2"	P3831	Q245025
#   Q141225764 Karolina Andrietta Ström: P26 spouse = Q6240337 Per Henrik Widmark RVO
Q141225764	P26	Q6240337	S2600	"6000000009494606557"
#   P2600 Geni.com profile ID = 6000000009494606557 Karolina Andrietta Ström, qualified P1810 subject named as Karolina Andrietta Ström
Q141225764	P2600	"6000000009494606557"	P1810	"Karolina Andrietta Ström"	S2600	"6000000009494606557"
#   P735 given name = Q1734206 Karolina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141225764	P735	Q1734206	P1545	"1"	P7452	Q3409033
#   Q141242409 Henning Nilsson Skytte: P25 mother = Q141225104 Engel Danckwardt
Q141242409	P25	Q141225104	S2600	"6000000009499682160"
#   P40 child = Q141223728 Brita Schytte
Q141242409	P40	Q141223728	S2600	"6000000009499682160"
#   P26 spouse = Q141225104 Engel Danckwardt
Q141242409	P26	Q141225104	S2600	"6000000009499682160"
#   P2600 Geni.com profile ID = 6000000009499682160 Henning Nilsson Skytte, qualified P1810 subject named as Henning Nilsson Skytte
Q141242409	P2600	"6000000009499682160"	P1810	"Henning Nilsson Skytte"	S2600	"6000000009499682160"
#   P735 given name = Q18607880 Henning
Q141242409	P735	Q18607880
#   P5056 patronym or matronym = Q130233015 Nilsson
Q141242409	P5056	Q130233015
#   Q141225104 Engel Danckwardt: P40 child = Q141242409 Henning Nilsson Skytte
Q141225104	P40	Q141242409	S2600	"6000000009501167719"
#   P26 spouse = Q141242409 Henning Nilsson Skytte
Q141225104	P26	Q141242409	S2600	"6000000009501167719"
#   Q141225068 Anna Mårtensdotter: P26 spouse = Q141225111 Ericus Nicolai Gestrinius
Q141225068	P26	Q141225111	S2600	"6000000010310582104"
#   Q141223553 Ragnhild Kristine Øystensdatter Nese: P40 child = Q141242389 Christian Osmundsen Nese
Q141223553	P40	Q141242389	S2600	"6000000010479856178"
#   Q141242389 Christian Osmundsen Nese: P22 father = Q141223432 Osmund Larsson Nese
Q141242389	P22	Q141223432	S2600	"6000000011329696852"
#   P2600 Geni.com profile ID = 6000000011329696852 Christian Osmundsen Nese, qualified P1810 subject named as Christian Osmundsen Nese
Q141242389	P2600	"6000000011329696852"	P1810	"Christian Osmundsen Nese"	S2600	"6000000011329696852"
#   Q141223728 Brita Schytte: P22 father = Q141242409 Henning Nilsson Skytte
Q141223728	P22	Q141242409	S2600	"6000000012901496092"
#   Q141225804 Louise Helmine Jenssen: P22 father = Q141223516 Hans Otto Kristian Jenssen
Q141225804	P22	Q141223516	S2600	"6000000014196858070"
#   P25 mother = Q141219307 Petrike Margrete Jenssen
Q141225804	P25	Q141219307	S2600	"6000000014196858070"
#   P2600 Geni.com profile ID = 6000000014196858070 Louise Helmine Jenssen, qualified P1810 subject named as Louise Helmine Jenssen
Q141225804	P2600	"6000000014196858070"	P1810	"Louise Helmine Jenssen"	S2600	"6000000014196858070"
#   P735 given name = Q3215140 Louise, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141225804	P735	Q3215140	P1545	"1"	P7452	Q3409033
#   P735 given name = Q99659344, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141225804	P735	Q99659344	P1545	"2"	P3831	Q245025
#   Q141216476 Jon Jonsson Vatne: P26 spouse = Q141242410 Maria Gjeruldsdtr Vatne
Q141216476	P26	Q141242410	S2600	"6000000014516017872"
#   Q141242410 Maria Gjeruldsdtr Vatne: P26 spouse = Q141216476 Jon Jonsson Vatne
Q141242410	P26	Q141216476	S2600	"6000000014516776068"
#   P2600 Geni.com profile ID = 6000000014516776068 Maria Gjeruldsdtr Vatne, qualified P1810 subject named as Maria Gjeruldsdtr Vatne
Q141242410	P2600	"6000000014516776068"	P1810	"Maria Gjeruldsdtr Vatne"	S2600	"6000000014516776068"
#   P735 given name = Q325872 Maria, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141242410	P735	Q325872	P1545	"1"	P7452	Q3409033
#   P734 family name = Q30134985 Vatne
Q141242410	P734	Q30134985
#   Q141224751 Berta Serina Rasmusdatter Borsheim: P40 child = Q141242411 Palle Paulson Borsok
Q141224751	P40	Q141242411	S2600	"6000000014522158621"
#   Q141242408 Harald Sivert Vålnes: P26 spouse = Q141216501 Siri Garborg Talle
Q141242408	P26	Q141216501	S2600	"6000000014631341075"
#   P2600 Geni.com profile ID = 6000000014631341075 Harald Sivert Vålnes, qualified P1810 subject named as Harald Sivert Nilsen
Q141242408	P2600	"6000000014631341075"	P1810	"Harald Sivert Nilsen"	S2600	"6000000014631341075"
#   P735 given name = Q1530266 Harald, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141242408	P735	Q1530266	P1545	"1"	P7452	Q3409033
#   P735 given name = Q19869345 Sivert, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141242408	P735	Q19869345	P1545	"2"	P3831	Q245025
#   Q141242371 Alfred Ingerman Hoknes: P40 child = Q141224812 Caroline Signe Borsheim
Q141242371	P40	Q141224812	S2600	"6000000015117490925"
#   P26 spouse = Q141224807 Sophia Borgit Hoknes
Q141242371	P26	Q141224807	S2600	"6000000015117490925"
#   P2600 Geni.com profile ID = 6000000015117490925 Alfred Ingerman Hoknes, qualified P1810 subject named as Alfred Ingerman Hoknes
Q141242371	P2600	"6000000015117490925"	P1810	"Alfred Ingerman Hoknes"	S2600	"6000000015117490925"
#   Q141225085 Berger Mathisen Sparby: P26 spouse = Q141225209 Olea Gundersdatter Hibo
Q141225085	P26	Q141225209	S2600	"6000000016756929355"
#   Q141189099 Rasmus Helgesen Bø: P40 child = Q141242406 Hans Rasmussen Bø
Q141189099	P40	Q141242406	S2600	"6000000021133770643"
#   Q141219050 Ane Olsdatter Bø: P40 child = Q141242406 Hans Rasmussen Bø
Q141219050	P40	Q141242406	S2600	"6000000021133787411"
#   Q141225209 Olea Gundersdatter Hibo: P26 spouse = Q141225085 Berger Mathisen Sparby
Q141225209	P26	Q141225085	S2600	"6000000022341758896"
#   Q141225124 Halvar Larsson Mossige: P26 spouse = Q141225072 Anna Nilsdatter Mossige
Q141225124	P26	Q141225072	S2600	"6000000023784554708"
#   Q141225072 Anna Nilsdatter Mossige: P26 spouse = Q141225124 Halvar Larsson Mossige
Q141225072	P26	Q141225124	S2600	"6000000023784778055"
#   Q141225793 Laurentius Andreae Andreae Alstrinius: P40 child = Q5547967 Erik Alstrin
Q141225793	P40	Q5547967	S2600	"6000000025011507008"
#   P26 spouse = Q141225779 Kristina Eriksdotter Ångerman
Q141225793	P26	Q141225779	S2600	"6000000025011507008"
#   P2600 Geni.com profile ID = 6000000025011507008 Laurentius Andreae Andreae Alstrinius, qualified P1810 subject named as Laurentius Andreae Andreae Alstrinius
Q141225793	P2600	"6000000025011507008"	P1810	"Laurentius Andreae Andreae Alstrinius"	S2600	"6000000025011507008"
#   P735 given name = Q15635267 Laurentius, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141225793	P735	Q15635267	P1545	"1"	P7452	Q3409033
#   Q141242415 Samuel Tollefson Tunheim: P22 father = Q141200112 Tollef Pederson Tunheim
Q141242415	P22	Q141200112	S2600	"6000000028541553897"
#   P25 mother = Q141199826 Anna Maria Samuelsdtr. Tunheim
Q141242415	P25	Q141199826	S2600	"6000000028541553897"
#   P2600 Geni.com profile ID = 6000000028541553897 Samuel Tollefson Tunheim, qualified P1810 subject named as Samuel Tollefson Tunheim
Q141242415	P2600	"6000000028541553897"	P1810	"Samuel Tollefson Tunheim"	S2600	"6000000028541553897"
#   P735 given name = Q629347 Samuel
Q141242415	P735	Q629347
#   P734 family name = Q36927172
Q141242415	P734	Q36927172
#   Q141199826 Anna Maria Samuelsdtr. Tunheim: P40 child = Q141242415 Samuel Tollefson Tunheim
Q141199826	P40	Q141242415	S2600	"6000000029983034410"
#   Q141200112 Tollef Pederson Tunheim: P40 child = Q141242415 Samuel Tollefson Tunheim
Q141200112	P40	Q141242415	S2600	"6000000029983078557"
#   Q141242412 Peder Paulsen Borsok: P40 child = Q141224861 Paul Pederson Borsheim
Q141242412	P40	Q141224861	S2600	"6000000035525387457"
#   P26 spouse = Q141242379 Berte Karlsdatter Borsok
Q141242412	P26	Q141242379	S2600	"6000000035525387457"
#   P2600 Geni.com profile ID = 6000000035525387457 Peder Paulsen Borsok, qualified P1810 subject named as Peder Paulsen Borsok
Q141242412	P2600	"6000000035525387457"	P1810	"Peder Paulsen Borsok"	S2600	"6000000035525387457"
#   Q141242379 Berte Karlsdatter Borsok: P40 child = Q141224861 Paul Pederson Borsheim
Q141242379	P40	Q141224861	S2600	"6000000035525469386"
#   P26 spouse = Q141242412 Peder Paulsen Borsok
Q141242379	P26	Q141242412	S2600	"6000000035525469386"
#   P2600 Geni.com profile ID = 6000000035525469386 Berte Karlsdatter Borsok, qualified P1810 subject named as Berte Karlsdatter Borsok
Q141242379	P2600	"6000000035525469386"	P1810	"Berte Karlsdatter Borsok"	S2600	"6000000035525469386"
#   Q141224861 Paul Pederson Borsheim: P22 father = Q141242412 Peder Paulsen Borsok
Q141224861	P22	Q141242412	S2600	"6000000035525833995"
#   P40 child = Q141242411 Palle Paulson Borsok
Q141224861	P40	Q141242411	S2600	"6000000035525833995"
#   Q141242395 David Torgerson Stokka: P22 father = Q141216653 Torger Torgerson Stokka
Q141242395	P22	Q141216653	S2600	"6000000037795923833"
#   P25 mother = Q141216602 Berta Guria Davidsdatter Stokka
Q141242395	P25	Q141216602	S2600	"6000000037795923833"
#   P2600 Geni.com profile ID = 6000000037795923833 David Torgerson Stokka, qualified P1810 subject named as David Torgerson Stokka
Q141242395	P2600	"6000000037795923833"	P1810	"David Torgerson Stokka"	S2600	"6000000037795923833"
#   P735 given name = Q29937870 David
Q141242395	P735	Q29937870
#   P734 family name = Q37033285
Q141242395	P734	Q37033285
#   Q141225779 Kristina Eriksdotter Ångerman: P40 child = Q5547967 Erik Alstrin
Q141225779	P40	Q5547967	S2600	"6000000038458498753"
#   P26 spouse = Q141225793 Laurentius Andreae Andreae Alstrinius
Q141225779	P26	Q141225793	S2600	"6000000038458498753"
#   P2600 Geni.com profile ID = 6000000038458498753 Kristina Eriksdotter Ångerman, qualified P1810 subject named as Kristina Eriksdotter Ångerman
Q141225779	P2600	"6000000038458498753"	P1810	"Kristina Eriksdotter Ångerman"	S2600	"6000000038458498753"
#   P735 given name = Q19798802 Kristina
Q141225779	P735	Q19798802
#   P5056 patronym or matronym = Q130232912 Eriksdotter
Q141225779	P5056	Q130232912
#   Q141225787 Kristine NN: P40 child = Q141225702 Erik Guttormsson
Q141225787	P40	Q141225702	S2600	"6000000040760740831"
#   P26 spouse = Q141223732 Guttorm Guttormsson
Q141225787	P26	Q141223732	S2600	"6000000040760740831"
#   P2600 Geni.com profile ID = 6000000040760740831 Kristine NN
Q141225787	P2600	"6000000040760740831"	S2600	"6000000040760740831"
#   P735 given name = Q16859157 Kristine
Q141225787	P735	Q16859157
#   Q141216458 Asbjørn Gunnarson Bø: P40 child = Q141242419 Sara Asbjørnsdatter Bø
Q141216458	P40	Q141242419	S2600	"6000000042211257078"
#   Q141216456 Anna Helgesdotter Opstad: P40 child = Q141242419 Sara Asbjørnsdatter Bø
Q141216456	P40	Q141242419	S2600	"6000000042211257124"
#   Q141242411 Palle Paulson Borsok: P22 father = Q141224861 Paul Pederson Borsheim
Q141242411	P22	Q141224861	S2600	"6000000077299349615"
#   P25 mother = Q141224751 Berta Serina Rasmusdatter Borsheim
Q141242411	P25	Q141224751	S2600	"6000000077299349615"
#   P2600 Geni.com profile ID = 6000000077299349615 Palle Paulson Borsok, qualified P1810 subject named as Palle Paulson Borsok
Q141242411	P2600	"6000000077299349615"	P1810	"Palle Paulson Borsok"	S2600	"6000000077299349615"
#   Q141225708 Fru Tore: P40 child = Q141216507 Torborg Toresdatter Norheim
Q141225708	P40	Q141216507	S2600	"6000000150599235831"
#   P2600 Geni.com profile ID = 6000000150599235831 Fru Tore, qualified P1810 subject named as Fru Tore
Q141225708	P2600	"6000000150599235831"	P1810	"Fru Tore"	S2600	"6000000150599235831"
#   Q141216501 Siri Garborg Talle: P26 spouse = Q141242408 Harald Sivert Vålnes
Q141216501	P26	Q141242408	S2600	"6000000177687513857"
#   Q141224812 Caroline Signe Borsheim: P22 father = Q141242371 Alfred Ingerman Hoknes
Q141224812	P22	Q141242371	S2600	"6000000177921459072"
#   Q141224807 Sophia Borgit Hoknes: P26 spouse = Q141242371 Alfred Ingerman Hoknes
Q141224807	P26	Q141242371	S2600	"6000000177921459094"
#   Q141225729 Jacob Knutson Skiftun: P40 child = Q141216494 N.N. Jacobsdtr. Koll
Q141225729	P40	Q141216494	S2600	"6000000177945982827"
#   P2600 Geni.com profile ID = 6000000177945982827 Jacob Knutson Skiftun, qualified P1810 subject named as Jacob Knutson Koll
Q141225729	P2600	"6000000177945982827"	P1810	"Jacob Knutson Koll"	S2600	"6000000177945982827"
#   P735 given name = Q25999604 Jacob
Q141225729	P735	Q25999604
#   Q141225693 Carl Andersson: P40 child = Q141223907 Elly Olivia Frisk
Q141225693	P40	Q141223907	S2600	"6000000178279141871"
#   P2600 Geni.com profile ID = 6000000178279141871 Carl Andersson, qualified P1810 subject named as Carl Andersson
Q141225693	P2600	"6000000178279141871"	P1810	"Carl Andersson"	S2600	"6000000178279141871"
#   P735 given name = Q2529610 Carl
Q141225693	P735	Q2529610
#   Q141242419 Sara Asbjørnsdatter Bø: P22 father = Q141216458 Asbjørn Gunnarson Bø
Q141242419	P22	Q141216458	S2600	"6000000222520233004"
#   P25 mother = Q141216456 Anna Helgesdotter Opstad
Q141242419	P25	Q141216456	S2600	"6000000222520233004"
#   P2600 Geni.com profile ID = 6000000222520233004 Sara Asbjørnsdatter Bø, qualified P1810 subject named as Sara Asbjørnsdatter Bø
Q141242419	P2600	"6000000222520233004"	P1810	"Sara Asbjørnsdatter Bø"	S2600	"6000000222520233004"
#   P735 given name = Q833345 Sara
Q141242419	P735	Q833345
#   P734 family name = Q30253098
Q141242419	P734	Q30253098
#   Q141242406 Hans Rasmussen Bø: P22 father = Q141189099 Rasmus Helgesen Bø
Q141242406	P22	Q141189099	S2600	"6000000225376735889"
#   P25 mother = Q141219050 Ane Olsdatter Bø
Q141242406	P25	Q141219050	S2600	"6000000225376735889"
#   P2600 Geni.com profile ID = 6000000225376735889 Hans Rasmussen Bø, qualified P1810 subject named as Hans Rasmussen Bø
Q141242406	P2600	"6000000225376735889"	P1810	"Hans Rasmussen Bø"	S2600	"6000000225376735889"
#   P735 given name = Q632842
Q141242406	P735	Q632842
#   P734 family name = Q30253098
Q141242406	P734	Q30253098

