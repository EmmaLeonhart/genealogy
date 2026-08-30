# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   1146 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   set the zh label to "埃里库斯·奥拉伊·普兰廷"
Q16650154	Lzh	"埃里库斯·奥拉伊·普兰廷"
#   Q141205930 Olav Knutson Randa Håland: set the ja label to "オーラヴ・クヌートソン・ランダ・ホーランド"
Q141205930	Lja	"オーラヴ・クヌートソン・ランダ・ホーランド"
#   set the zh label to "奥拉夫·克努特松·兰达·霍兰"
Q141205930	Lzh	"奥拉夫·克努特松·兰达·霍兰"
#   Q141216487 Knut Johanson Håland: set the zh label to "克努特·约汉松·霍兰"
Q141216487	Lzh	"克努特·约汉松·霍兰"
#   Q6197518 Svantepolk Knutsson Knutsson Skarsholmsätten: add a mul alias "Svantepolk Knutsson"
Q6197518	Amul	"Svantepolk Knutsson"
#   set the mul label to "Svantepolk of Viby"
Q6197518	Lmul	"Svantepolk of Viby"
#   Q141216489 Laurits Leivson Bjørheim: set the ja label to "ラウリッツ・レイヴソン・ブヨルヘイム"
Q141216489	Lja	"ラウリッツ・レイヴソン・ブヨルヘイム"
#   set the zh label to "拉乌里特斯·莱伊夫松·布约尔赫伊姆"
Q141216489	Lzh	"拉乌里特斯·莱伊夫松·布约尔赫伊姆"
#   Q141216638 Olaug Jonsdatter Heigre: add a mul alias "Olaug Jonsdatter Røyneberg"
Q141216638	Amul	"Olaug Jonsdatter Røyneberg"
#   Q141219299 Per Asbjørnson Stokka: set the ja label to "ペール・アスブヨルンソン・ストカ"
Q141219299	Lja	"ペール・アスブヨルンソン・ストカ"
#   set the zh label to "佩尔·阿斯布约尔恩松·斯托卡"
Q141219299	Lzh	"佩尔·阿斯布约尔恩松·斯托卡"
#   Q141216637 Ola Person Persson Heigre: set the ja label to "オーラ・ペルソン・パーソン・ヘイグレ"
Q141216637	Lja	"オーラ・ペルソン・パーソン・ヘイグレ"
#   set the zh label to "奥拉·佩尔松·佩尔松·海格勒"
Q141216637	Lzh	"奥拉·佩尔松·佩尔松·海格勒"
#   Q141205914 Inger (Ingrid) Osmundsdatter Risa: add a mul alias "Inger (Ingrid) Osmundsdatter Tunheim"
Q141205914	Amul	"Inger (Ingrid) Osmundsdatter Tunheim"
#   set the ja label to "インゲル・オスムンドスダッテル・リサ"
Q141205914	Lja	"インゲル・オスムンドスダッテル・リサ"

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Charlotta Eleonora Falkenberg"
LAST	Len	"Charlotta Eleonora Falkenberg"
#   set the mul label to "Charlotta Eleonora Falkenberg"
LAST	Lmul	"Charlotta Eleonora Falkenberg"
#   add a mul alias "Charlotta Eleonora Silfverstolpe"
LAST	Amul	"Charlotta Eleonora Silfverstolpe"
#   set the ja label to "カルロタ・エレオノーラ・ファルケンベルグ"
LAST	Lja	"カルロタ・エレオノーラ・ファルケンベルグ"
#   set the zh label to "卡尔洛塔·埃莱奥诺拉·法尔肯贝尔格"
LAST	Lzh	"卡尔洛塔·埃莱奥诺拉·法尔肯贝尔格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000019325206143 Charlotta Eleonora Falkenberg, qualified P1810 subject named as Charlotta Eleonora Silfverstolpe
LAST	P2600	"6000000019325206143"	P1810	"Charlotta Eleonora Silfverstolpe"
#   P569 date of birth = +1836-03-20T00:00:00Z/11
LAST	P569	+1836-03-20T00:00:00Z/11	S2600	"6000000019325206143"
#   P570 date of death = +1911-07-09T00:00:00Z/11
LAST	P570	+1911-07-09T00:00:00Z/11	S2600	"6000000019325206143"
#   P22 father = Q6175945 Fredrik Otto Silfverstolpe
LAST	P22	Q6175945	S2600	"6000000019325206143"
#   Q6175945 Fredrik Otto Silfverstolpe: P40 child = the item just created
Q6175945	P40	LAST	S2600	"6000000019325206143"
#   the item just created: P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q1067071	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18759077 Eleonora, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q18759077	P1545	"2"	P3831	Q245025
#   P734 family name = Q16869887 Falkenberg, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q16869887	P3831	Q28418670
#   add a mul alias "Falkenberg"
LAST	Amul	"Falkenberg"

# create a new item
CREATE
#   set the en label to "Erik Monsen Bjorland"
LAST	Len	"Erik Monsen Bjorland"
#   set the mul label to "Erik Monsen Bjorland"
LAST	Lmul	"Erik Monsen Bjorland"
#   set the ja label to "エリック・モンセン・ブヨルランド"
LAST	Lja	"エリック・モンセン・ブヨルランド"
#   set the zh label to "埃里克·蒙森·布约尔兰德"
LAST	Lzh	"埃里克·蒙森·布约尔兰德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003491998017 Erik Monsen Bjorland, qualified P1810 subject named as Erik Monsen Bjorland
LAST	P2600	"6000000003491998017"	P1810	"Erik Monsen Bjorland"
#   P569 date of birth = +1637-00-00T00:00:00Z/9
LAST	P569	+1637-00-00T00:00:00Z/9	S2600	"6000000003491998017"
#   P570 date of death = +1694-00-00T00:00:00Z/9
LAST	P570	+1694-00-00T00:00:00Z/9	S2600	"6000000003491998017"
#   P40 child = Q141216383 Ingeborg Eriksdatter Bjorland
LAST	P40	Q141216383	S2600	"6000000003491998017"
#   Q141216383 Ingeborg Eriksdatter Bjorland: P22 father = the item just created
Q141216383	P22	LAST	S2600	"6000000003491998017"
#   the item just created: P735 given name = Q750186 Erik
LAST	P735	Q750186
#   P734 family name = Q123200450
LAST	P734	Q123200450

# create a new item
CREATE
#   set the en label to "Eva Augusta Löwen"
LAST	Len	"Eva Augusta Löwen"
#   set the mul label to "Eva Augusta Löwen"
LAST	Lmul	"Eva Augusta Löwen"
#   set the ja label to "エヴァ・オーガスタ・ロヴェン"
LAST	Lja	"エヴァ・オーガスタ・ロヴェン"
#   set the zh label to "伊娃·奧古斯塔·洛文"
LAST	Lzh	"伊娃·奧古斯塔·洛文"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000012839208314 Eva Augusta Löwen, qualified P1810 subject named as Eva Augusta Löwen
LAST	P2600	"6000000012839208314"	P1810	"Eva Augusta Löwen"
#   P569 date of birth = +1777-06-21T00:00:00Z/11
LAST	P569	+1777-06-21T00:00:00Z/11	S2600	"6000000012839208314"
#   P570 date of death = +1832-03-23T00:00:00Z/11
LAST	P570	+1832-03-23T00:00:00Z/11	S2600	"6000000012839208314"
#   P26 spouse = Q16650517 Mikael von Törne
LAST	P26	Q16650517	S2600	"6000000012839208314"
#   Q16650517 Mikael von Törne: P26 spouse = the item just created
Q16650517	P26	LAST	S2600	"6000000012839208314"
#   the item just created: P735 given name = Q64412279 Eva, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q64412279	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1370330 Augusta, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1370330	P1545	"2"	P3831	Q245025
#   P734 family name = Q54449198 Löwen, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q54449198	P3831	Q28418670

# create a new item
CREATE
#   set the en label to "Gustav Petersson Lejon"
LAST	Len	"Gustav Petersson Lejon"
#   set the mul label to "Gustav Petersson Lejon"
LAST	Lmul	"Gustav Petersson Lejon"
#   set the ja label to "グスタフ・ペテルソン・レヨン"
LAST	Lja	"グスタフ・ペテルソン・レヨン"
#   set the zh label to "古斯塔夫·佩特尔松·莱永"
LAST	Lzh	"古斯塔夫·佩特尔松·莱永"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003414711727 Gustav Petersson Lejon, qualified P1810 subject named as Gustav Petersson (trol. lejon)
LAST	P2600	"6000000003414711727"	P1810	"Gustav Petersson (trol. lejon)"
#   P569 date of birth = +1235-00-00T00:00:00Z/9
LAST	P569	+1235-00-00T00:00:00Z/9	S2600	"6000000003414711727"
#   P570 date of death = +1270-04-17T00:00:00Z/11
LAST	P570	+1270-04-17T00:00:00Z/11	S2600	"6000000003414711727"
#   P40 child = Q141198381 Bengt Hafridsson Lejon
LAST	P40	Q141198381	S2600	"6000000003414711727"
#   Q141198381 Bengt Hafridsson Lejon: P22 father = the item just created
Q141198381	P22	LAST	S2600	"6000000003414711727"

# create a new item
CREATE
#   the item just created: set the en label to "Hafrid Sigtryggsdotter Boberg"
LAST	Len	"Hafrid Sigtryggsdotter Boberg"
#   set the mul label to "Hafrid Sigtryggsdotter Boberg"
LAST	Lmul	"Hafrid Sigtryggsdotter Boberg"
#   set the ja label to "ハフリド・シグトリグスドッテル・ボベルグ"
LAST	Lja	"ハフリド・シグトリグスドッテル・ボベルグ"
#   set the zh label to "哈夫里德·西格特里格斯多特·博贝尔格"
LAST	Lzh	"哈夫里德·西格特里格斯多特·博贝尔格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003559734445 Hafrid Sigtryggsdotter Boberg, qualified P1810 subject named as Hafrid Sigtryggsdotter Boberg
LAST	P2600	"6000000003559734445"	P1810	"Hafrid Sigtryggsdotter Boberg"
#   P569 date of birth = +1229-00-00T00:00:00Z/9
LAST	P569	+1229-00-00T00:00:00Z/9	S2600	"6000000003559734445"
#   P570 date of death = +1286-10-20T00:00:00Z/11
LAST	P570	+1286-10-20T00:00:00Z/11	S2600	"6000000003559734445"
#   P40 child = Q141198381 Bengt Hafridsson Lejon
LAST	P40	Q141198381	S2600	"6000000003559734445"
#   Q141198381 Bengt Hafridsson Lejon: P25 mother = the item just created
Q141198381	P25	LAST	S2600	"6000000003559734445"

# create a new item
CREATE
#   the item just created: set the en label to "Helen Frisk"
LAST	Len	"Helen Frisk"
#   set the mul label to "Helen Frisk"
LAST	Lmul	"Helen Frisk"
#   set the ja label to "ヘレン・フリスク"
LAST	Lja	"ヘレン・フリスク"
#   set the zh label to "海伦·弗里斯克"
LAST	Lzh	"海伦·弗里斯克"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000177921459052 Helen Frisk, qualified P1810 subject named as Helen Frisk
LAST	P2600	"6000000177921459052"	P1810	"Helen Frisk"
#   P22 father = Q141223733 Hans Bertil Frisk
LAST	P22	Q141223733	S2600	"6000000177921459052"
#   Q141223733 Hans Bertil Frisk: P40 child = the item just created
Q141223733	P40	LAST	S2600	"6000000177921459052"

# create a new item
CREATE
#   the item just created: set the en label to "Jeannette Constance Tigerstedt"
LAST	Len	"Jeannette Constance Tigerstedt"
#   set the mul label to "Jeannette Constance Tigerstedt"
LAST	Lmul	"Jeannette Constance Tigerstedt"
#   add a mul alias "Jeannette Constance von Törne"
LAST	Amul	"Jeannette Constance von Törne"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000026930814601 Jeannette Constance Tigerstedt, qualified P1810 subject named as Jeannette Constance von Törne
LAST	P2600	"6000000026930814601"	P1810	"Jeannette Constance von Törne"
#   P569 date of birth = +1803-00-00T00:00:00Z/9
LAST	P569	+1803-00-00T00:00:00Z/9	S2600	"6000000026930814601"
#   P570 date of death = +1842-00-00T00:00:00Z/9
LAST	P570	+1842-00-00T00:00:00Z/9	S2600	"6000000026930814601"
#   P22 father = Q16650517 Mikael von Törne
LAST	P22	Q16650517	S2600	"6000000026930814601"
#   Q16650517 Mikael von Törne: P40 child = the item just created
Q16650517	P40	LAST	S2600	"6000000026930814601"
#   the item just created: P735 given name = Q1686048 Jeannette, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q1686048	P1545	"1"	P7452	Q3409033
#   P735 given name = Q679755 Constance, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q679755	P1545	"2"	P3831	Q245025
#   P734 family name = Q65202241 Törne, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q65202241	P3831	Q2507958

# create a new item
CREATE
#   set the en label to "Knut Larsson Rosså"
LAST	Len	"Knut Larsson Rosså"
#   set the mul label to "Knut Larsson Rosså"
LAST	Lmul	"Knut Larsson Rosså"
#   add a mul alias "Knut Larsson Mjølhus"
LAST	Amul	"Knut Larsson Mjølhus"
#   set the ja label to "クヌート・ラーション・ロソー"
LAST	Lja	"クヌート・ラーション・ロソー"
#   set the zh label to "克努特·拉森·罗索"
LAST	Lzh	"克努特·拉森·罗索"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000052571015068 Knut Larsson Rosså, qualified P1810 subject named as Knut Larsson Mjølhus
LAST	P2600	"6000000052571015068"	P1810	"Knut Larsson Mjølhus"
#   P569 date of birth = +1568-00-00T00:00:00Z/9
LAST	P569	+1568-00-00T00:00:00Z/9	S2600	"6000000052571015068"
#   P570 date of death = +1622-00-00T00:00:00Z/9
LAST	P570	+1622-00-00T00:00:00Z/9	S2600	"6000000052571015068"
#   P22 father = Q141198832 Lars Gunnbjørnsen Mjølhus
LAST	P22	Q141198832	S2600	"6000000052571015068"
#   P25 mother = Q141205922 Marit Ormsd Byre
LAST	P25	Q141205922	S2600	"6000000052571015068"
#   Q141198832 Lars Gunnbjørnsen Mjølhus: P40 child = the item just created
Q141198832	P40	LAST	S2600	"6000000052571015068"
#   Q141205922 Marit Ormsd Byre: P40 child = the item just created
Q141205922	P40	LAST	S2600	"6000000052571015068"
#   the item just created: P735 given name = Q943881 Knut
LAST	P735	Q943881
#   add a mul alias "Knut Rosså"
LAST	Amul	"Knut Rosså"

# create a new item
CREATE
#   set the en label to "Laurentius Olai"
LAST	Len	"Laurentius Olai"
#   set the mul label to "Laurentius Olai"
LAST	Lmul	"Laurentius Olai"
#   add a mul alias "Laurentius Olofsson"
LAST	Amul	"Laurentius Olofsson"
#   set the ja label to "ラウレンティウス・オライ"
LAST	Lja	"ラウレンティウス・オライ"
#   set the zh label to "拉乌伦蒂乌斯·奥拉伊"
LAST	Lzh	"拉乌伦蒂乌斯·奥拉伊"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000004334886671 Laurentius Olai, qualified P1810 subject named as Laurentius Olofsson
LAST	P2600	"6000000004334886671"	P1810	"Laurentius Olofsson"
#   P569 date of birth = +1514-00-00T00:00:00Z/9
LAST	P569	+1514-00-00T00:00:00Z/9	S2600	"6000000004334886671"
#   P570 date of death = +1571-00-00T00:00:00Z/9
LAST	P570	+1571-00-00T00:00:00Z/9	S2600	"6000000004334886671"
#   P22 father = Q141205932 Olof Timmerman
LAST	P22	Q141205932	S2600	"6000000004334886671"
#   P25 mother = Q141205926 NN
LAST	P25	Q141205926	S2600	"6000000004334886671"
#   Q141205932 Olof Timmerman: P40 child = the item just created
Q141205932	P40	LAST	S2600	"6000000004334886671"
#   Q141205926 NN: P40 child = the item just created
Q141205926	P40	LAST	S2600	"6000000004334886671"
#   the item just created: P735 given name = Q15635267 Laurentius
LAST	P735	Q15635267
#   add a mul alias "Lars Olofsson Olai"
LAST	Amul	"Lars Olofsson Olai"

# create a new item
CREATE
#   set the en label to "Maria Louisa Silfverstolpe"
LAST	Len	"Maria Louisa Silfverstolpe"
#   set the mul label to "Maria Louisa Silfverstolpe"
LAST	Lmul	"Maria Louisa Silfverstolpe"
#   add a mul alias "Maria Louisa Pettersson"
LAST	Amul	"Maria Louisa Pettersson"
#   set the ja label to "マリア・ルイーザ・シルフヴェルストルペ"
LAST	Lja	"マリア・ルイーザ・シルフヴェルストルペ"
#   set the zh label to "玛丽亚·路易莎·西尔夫韦尔斯托尔佩"
LAST	Lzh	"玛丽亚·路易莎·西尔夫韦尔斯托尔佩"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000006127758500 Maria Louisa Silfverstolpe, qualified P1810 subject named as Maria Louisa Pettersson
LAST	P2600	"6000000006127758500"	P1810	"Maria Louisa Pettersson"
#   P569 date of birth = +1813-00-00T00:00:00Z/9
LAST	P569	+1813-00-00T00:00:00Z/9	S2600	"6000000006127758500"
#   P570 date of death = +1891-01-25T00:00:00Z/11
LAST	P570	+1891-01-25T00:00:00Z/11	S2600	"6000000006127758500"
#   P26 spouse = Q6175945 Fredrik Otto Silfverstolpe
LAST	P26	Q6175945	S2600	"6000000006127758500"
#   Q6175945 Fredrik Otto Silfverstolpe: P26 spouse = the item just created
Q6175945	P26	LAST	S2600	"6000000006127758500"
#   the item just created: P735 given name = Q325872 Maria, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q325872	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16420967, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q16420967	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Marit Bjørnsdatter Bjorland"
LAST	Len	"Marit Bjørnsdatter Bjorland"
#   set the mul label to "Marit Bjørnsdatter Bjorland"
LAST	Lmul	"Marit Bjørnsdatter Bjorland"
#   add a mul alias "Marit Bjørnsdatter Hognestad"
LAST	Amul	"Marit Bjørnsdatter Hognestad"
#   set the ja label to "マリット・ブヨルンスダッテル・ブヨルランド"
LAST	Lja	"マリット・ブヨルンスダッテル・ブヨルランド"
#   set the zh label to "马里特·布约尔恩斯达特·布约尔兰德"
LAST	Lzh	"马里特·布约尔恩斯达特·布约尔兰德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005609529475 Marit Bjørnsdatter Bjorland, qualified P1810 subject named as Marit Bjørnsdatter Hognestad
LAST	P2600	"6000000005609529475"	P1810	"Marit Bjørnsdatter Hognestad"
#   P569 date of birth = +1637-00-00T00:00:00Z/9
LAST	P569	+1637-00-00T00:00:00Z/9	S2600	"6000000005609529475"
#   P570 date of death = +1694-00-00T00:00:00Z/9
LAST	P570	+1694-00-00T00:00:00Z/9	S2600	"6000000005609529475"
#   P40 child = Q141216383 Ingeborg Eriksdatter Bjorland
LAST	P40	Q141216383	S2600	"6000000005609529475"
#   Q141216383 Ingeborg Eriksdatter Bjorland: P25 mother = the item just created
Q141216383	P25	LAST	S2600	"6000000005609529475"
#   the item just created: P735 given name = Q1566153 Marit
LAST	P735	Q1566153
#   P734 family name = Q21509419 Hognestad, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q21509419	P3831	Q2507958
#   P734 family name = Q123200450, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q123200450	P3831	Q28418670
#   add a mul alias "Marit Bjorland"
LAST	Amul	"Marit Bjorland"

# create a new item
CREATE
#   set the en label to "Ola Helgeson Lima"
LAST	Len	"Ola Helgeson Lima"
#   set the mul label to "Ola Helgeson Lima"
LAST	Lmul	"Ola Helgeson Lima"
#   set the ja label to "オーラ・ヘルゲソン・リマ"
LAST	Lja	"オーラ・ヘルゲソン・リマ"
#   set the zh label to "奥拉·赫尔盖松·利马"
LAST	Lzh	"奥拉·赫尔盖松·利马"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000116694298987 Ola Helgeson Lima, qualified P1810 subject named as Ola Helgeson Lima
LAST	P2600	"6000000116694298987"	P1810	"Ola Helgeson Lima"
#   P569 date of birth = +1796-00-00T00:00:00Z/9
LAST	P569	+1796-00-00T00:00:00Z/9	S2600	"6000000116694298987"
#   P570 date of death = +1839-00-00T00:00:00Z/9
LAST	P570	+1839-00-00T00:00:00Z/9	S2600	"6000000116694298987"
#   P22 father = Q141223735 Helge Olsen Ytre Lima
LAST	P22	Q141223735	S2600	"6000000116694298987"
#   Q141223735 Helge Olsen Ytre Lima: P40 child = the item just created
Q141223735	P40	LAST	S2600	"6000000116694298987"

# create a new item
CREATE
#   the item just created: set the en label to "Olga Emily Ronneberg"
LAST	Len	"Olga Emily Ronneberg"
#   set the mul label to "Olga Emily Ronneberg"
LAST	Lmul	"Olga Emily Ronneberg"
#   set the ja label to "オルガ・エミリー・ロンネベルグ"
LAST	Lja	"オルガ・エミリー・ロンネベルグ"
#   set the zh label to "奥尔加·艾米丽·龙内贝格"
LAST	Lzh	"奥尔加·艾米丽·龙内贝格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000035698002658 Olga Emily Ronneberg, qualified P1810 subject named as Olga Emily Ronneberg
LAST	P2600	"6000000035698002658"	P1810	"Olga Emily Ronneberg"
#   P569 date of birth = +1901-00-00T00:00:00Z/9
LAST	P569	+1901-00-00T00:00:00Z/9	S2600	"6000000035698002658"
#   P570 date of death = +1930-00-00T00:00:00Z/9
LAST	P570	+1930-00-00T00:00:00Z/9	S2600	"6000000035698002658"
#   P22 father = Q141198510 Tønnes Emil Enokson Ronneberg
LAST	P22	Q141198510	S2600	"6000000035698002658"
#   P25 mother = Q141162043 Inger Marie Mary Eivindsdatter Ronneberg
LAST	P25	Q141162043	S2600	"6000000035698002658"
#   Q141198510 Tønnes Emil Enokson Ronneberg: P40 child = the item just created
Q141198510	P40	LAST	S2600	"6000000035698002658"
#   Q141162043 Inger Marie Mary Eivindsdatter Ronneberg: P40 child = the item just created
Q141162043	P40	LAST	S2600	"6000000035698002658"
#   the item just created: P735 given name = Q20187, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q20187	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18121477 Emily, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q18121477	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Ragnhild Østensd Stokka"
LAST	Len	"Ragnhild Østensd Stokka"
#   set the mul label to "Ragnhild Østensd Stokka"
LAST	Lmul	"Ragnhild Østensd Stokka"
#   add a mul alias "Ragnhild Østensd Egenes"
LAST	Amul	"Ragnhild Østensd Egenes"
#   set the ja label to "ラグンヒル・オステンスド・ストカ"
LAST	Lja	"ラグンヒル・オステンスド・ストカ"
#   set the zh label to "拉格希尔德·奥斯滕斯德·斯托卡"
LAST	Lzh	"拉格希尔德·奥斯滕斯德·斯托卡"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003315892160 Ragnhild Østensd Stokka, qualified P1810 subject named as Ragnhild Østensd Egenes
LAST	P2600	"6000000003315892160"	P1810	"Ragnhild Østensd Egenes"
#   P569 date of birth = +1563-00-00T00:00:00Z/9
LAST	P569	+1563-00-00T00:00:00Z/9	S2600	"6000000003315892160"
#   P570 date of death = +1642-00-00T00:00:00Z/9
LAST	P570	+1642-00-00T00:00:00Z/9	S2600	"6000000003315892160"
#   P40 child = Q141216611 Jon Villumson Raunes
LAST	P40	Q141216611	S2600	"6000000003315892160"
#   Q141216611 Jon Villumson Raunes: P25 mother = the item just created
Q141216611	P25	LAST	S2600	"6000000003315892160"
#   the item just created: P735 given name = Q1390292 Ragnhild, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q1390292	P1545	"1"	P7452	Q3409033
#   P734 family name = Q37033285, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q37033285	P3831	Q28418670

# create a new item
CREATE
#   set the en label to "Rakel Rasmusdottir Borsheim"
LAST	Len	"Rakel Rasmusdottir Borsheim"
#   set the mul label to "Rakel Rasmusdottir Borsheim"
LAST	Lmul	"Rakel Rasmusdottir Borsheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000020344732085 Rakel Rasmusdottir Borsheim, qualified P1810 subject named as Rakel Rasmusdottir Borsheim
LAST	P2600	"6000000020344732085"	P1810	"Rakel Rasmusdottir Borsheim"
#   P569 date of birth = +1866-02-09T00:00:00Z/11
LAST	P569	+1866-02-09T00:00:00Z/11	S2600	"6000000020344732085"
#   P570 date of death = +1961-11-30T00:00:00Z/11
LAST	P570	+1961-11-30T00:00:00Z/11	S2600	"6000000020344732085"
#   P22 father = Q141223744 Rasmus Wibye Andersson Lea
LAST	P22	Q141223744	S2600	"6000000020344732085"
#   Q141223744 Rasmus Wibye Andersson Lea: P40 child = the item just created
Q141223744	P40	LAST	S2600	"6000000020344732085"

# create a new item
CREATE
#   the item just created: set the en label to "Sofia Kristina Wester"
LAST	Len	"Sofia Kristina Wester"
#   set the mul label to "Sofia Kristina Wester"
LAST	Lmul	"Sofia Kristina Wester"
#   set the ja label to "ソフィア・クリスティーナ・ヴェステル"
LAST	Lja	"ソフィア・クリスティーナ・ヴェステル"
#   set the zh label to "索菲娅·克里斯蒂娜·韦斯特尔"
LAST	Lzh	"索菲娅·克里斯蒂娜·韦斯特尔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003396184357 Sofia Kristina Wester, qualified P1810 subject named as Sofia Kristina Wester
LAST	P2600	"6000000003396184357"	P1810	"Sofia Kristina Wester"
#   P569 date of birth = +1780-05-22T00:00:00Z/11
LAST	P569	+1780-05-22T00:00:00Z/11	S2600	"6000000003396184357"
#   P570 date of death = +1829-10-22T00:00:00Z/11
LAST	P570	+1829-10-22T00:00:00Z/11	S2600	"6000000003396184357"
#   P26 spouse = Q333297 Frans Michael Zachrichsson Franzén
LAST	P26	Q333297	S2600	"6000000003396184357"
#   Q333297 Frans Michael Zachrichsson Franzén: P26 spouse = the item just created
Q333297	P26	LAST	S2600	"6000000003396184357"
#   the item just created: P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q18201520	P1545	"1"	P7452	Q3409033
#   P735 given name = Q19798802 Kristina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q19798802	P1545	"2"	P3831	Q245025
#   add a mul alias "Sofia Christina Wester"
LAST	Amul	"Sofia Christina Wester"
#   Q141216349 Ingrid Guttormsdotter: P40 child = Q141223732 Guttorm Guttormsson
Q141216349	P40	Q141223732	S2600	"6000000000771986019"
#   Q141223742 Ragnhild Sofie Sahlin: P735 given name = Q1390292 Ragnhild, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141223742	P735	Q1390292	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18201530 Sofie, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141223742	P735	Q18201530	P1545	"2"	P3831	Q245025
#   Q141223735 Helge Olsen Ytre Lima: P735 given name = Q1602361 Helge, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141223735	P735	Q1602361	P1545	"1"	P7452	Q3409033
#   P734 family name = Q11255517 Lima
Q141223735	P734	Q11255517
#   Q141223744 Rasmus Wibye Andersson Lea: P735 given name = Q1785744 Rasmus, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141223744	P735	Q1785744	P1545	"1"	P7452	Q3409033
#   P734 family name = Q6508166 Lea
Q141223744	P734	Q6508166
#   Q141223731 Gustava Fant: P25 mother = Q141223729 Christina Brigitta Rydberg
Q141223731	P25	Q141223729	S2600	"6000000019352071101"
#   Q141223729 Christina Brigitta Rydberg: P40 child = Q141223731 Gustava Fant
Q141223729	P40	Q141223731	S2600	"6000000019467862742"
#   Q141223732 Guttorm Guttormsson: P735 given name = Q20755782 Guttorm
Q141223732	P735	Q20755782
#   Q141223736 Karl Emil Frisk: P40 child = Q141223733 Hans Bertil Frisk
Q141223736	P40	Q141223733	S2600	"6000000177921458827"
#   P735 given name = Q136771753 Karl, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141223736	P735	Q136771753	P1545	"1"	P7452	Q3409033
#   P735 given name = Q989320 Emil, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141223736	P735	Q989320	P1545	"2"	P3831	Q245025
#   P734 family name = Q27877507 Frisk
Q141223736	P734	Q27877507
#   Q141223733 Hans Bertil Frisk: P22 father = Q141223736 Karl Emil Frisk
Q141223733	P22	Q141223736	S2600	"6000000177921459066"
#   P735 given name = Q632842, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141223733	P735	Q632842	P1545	"1"	P7452	Q3409033
#   P735 given name = Q19687104 Bertil, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141223733	P735	Q19687104	P1545	"2"	P3831	Q245025
#   P734 family name = Q27877507 Frisk
Q141223733	P734	Q27877507

