# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Algot Bryniolfsson"
LAST	Len	"Algot Bryniolfsson"
#   set the mul label to "Algot Bryniolfsson"
LAST	Lmul	"Algot Bryniolfsson"
#   set the ja label to "アルゴット・ブリニオルフソン"
LAST	Lja	"アルゴット・ブリニオルフソン"
#   set the zh label to "阿尔戈特·布吕尼奥尔夫松"
LAST	Lzh	"阿尔戈特·布吕尼奥尔夫松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005795638082 Algot Bryniolfsson
LAST	P2600	"6000000005795638082"
#   P569 date of birth = +1285-00-00T00:00:00Z/9
LAST	P569	+1285-00-00T00:00:00Z/9	S2600	"6000000005795638082"
#   P570 date of death = +1332-00-00T00:00:00Z/9
LAST	P570	+1332-00-00T00:00:00Z/9	S2600	"6000000005795638082"
#   P25 mother = Q101247444 Ingegerd Svantepolksdotter
LAST	P25	Q101247444	S2600	"6000000005795638082"
#   P40 child = Q5915800 Knut Algotsson
LAST	P40	Q5915800	S2600	"6000000005795638082"
#   Q101247444 Ingegerd Svantepolksdotter: P40 child = the item just created
Q101247444	P40	LAST	S2600	"6000000005795638082"
#   Q5915800 Knut Algotsson: P22 father = the item just created
Q5915800	P22	LAST	S2600	"6000000005795638082"
#   the item just created: P735 given name = Q10405157 Algot
LAST	P735	Q10405157
#   P1449 nickname = en:"Algot Brynolfsson"
LAST	P1449	en:"Algot Brynolfsson"
#   add a mul alias "Algot Brynolfsson Bryniolfsson"
LAST	Amul	"Algot Brynolfsson Bryniolfsson"

# create a new item
CREATE
#   set the en label to "Astri Torkelsdatter Gilja"
LAST	Len	"Astri Torkelsdatter Gilja"
#   set the mul label to "Astri Torkelsdatter Gilja"
LAST	Lmul	"Astri Torkelsdatter Gilja"
#   set the ja label to "アストリ・トルケルスダッテル・ギリヤ"
LAST	Lja	"アストリ・トルケルスダッテル・ギリヤ"
#   set the zh label to "阿斯特丽·托克尔斯达特·吉利亚"
LAST	Lzh	"阿斯特丽·托克尔斯达特·吉利亚"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003095034747 Astri Torkelsdatter Gilja
LAST	P2600	"6000000003095034747"
#   P570 date of death = +1716-00-00T00:00:00Z/9
LAST	P570	+1716-00-00T00:00:00Z/9	S2600	"6000000003095034747"
#   P735 given name = Q30132931 Astri
LAST	P735	Q30132931
#   add a mul alias "Astri Gilja"
LAST	Amul	"Astri Gilja"

# create a new item
CREATE
#   set the en label to "Benedicta Sunesdotter Folkungaätten"
LAST	Len	"Benedicta Sunesdotter Folkungaätten"
#   set the mul label to "Benedicta Sunesdotter Folkungaätten"
LAST	Lmul	"Benedicta Sunesdotter Folkungaätten"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000002601672538 Benedicta Sunesdotter Folkungaätten
LAST	P2600	"6000000002601672538"
#   P569 date of birth = +1220-00-00T00:00:00Z/9
LAST	P569	+1220-00-00T00:00:00Z/9	S2600	"6000000002601672538"
#   P570 date of death = +1261-00-00T00:00:00Z/9
LAST	P570	+1261-00-00T00:00:00Z/9	S2600	"6000000002601672538"
#   P26 spouse = Q6197518 Svantepolk Knutsson Viby Skarsholmsätten
LAST	P26	Q6197518	S2600	"6000000002601672538"
#   P40 child = Q101247444 Ingegerd Svantepolksdotter
LAST	P40	Q101247444	S2600	"6000000002601672538"
#   Q6197518 Svantepolk Knutsson Viby Skarsholmsätten: P26 spouse = the item just created
Q6197518	P26	LAST	S2600	"6000000002601672538"
#   Q101247444 Ingegerd Svantepolksdotter: P25 mother = the item just created
Q101247444	P25	LAST	S2600	"6000000002601672538"
#   the item just created: P735 given name = Q21147545 Benedicta, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q21147545	P1545	"1"	P7452	Q3409033
#   P1449 nickname = en:"Bjälbo"
LAST	P1449	en:"Bjälbo"
#   add a mul alias "Bjälbo Folkungaätten"
LAST	Amul	"Bjälbo Folkungaätten"

# create a new item
CREATE
#   set the en label to "Bertila"
LAST	Len	"Bertila"
#   set the mul label to "Bertila"
LAST	Lmul	"Bertila"
#   set the ja label to "ベルティラ"
LAST	Lja	"ベルティラ"
#   set the zh label to "贝尔蒂拉"
LAST	Lzh	"贝尔蒂拉"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005936931116 Bertila
LAST	P2600	"6000000005936931116"
#   P569 date of birth = +0850-00-00T00:00:00Z/9
LAST	P569	+0850-00-00T00:00:00Z/9	S2600	"6000000005936931116"
#   P570 date of death = +0915-12-00T00:00:00Z/10
LAST	P570	+0915-12-00T00:00:00Z/10	S2600	"6000000005936931116"
#   P26 spouse = Q274606 Berengar I margrave of Friuli, king of Italy
LAST	P26	Q274606	S2600	"6000000005936931116"
#   Q274606 Berengar I margrave of Friuli, king of Italy: P26 spouse = the item just created
Q274606	P26	LAST	S2600	"6000000005936931116"

# create a new item
CREATE
#   the item just created: set the en label to "Bryniolf Bengtsson (Hafridssons ätt)"
LAST	Len	"Bryniolf Bengtsson (Hafridssons ätt)"
#   set the mul label to "Bryniolf Bengtsson (Hafridssons ätt)"
LAST	Lmul	"Bryniolf Bengtsson (Hafridssons ätt)"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000011239545575 Bryniolf Bengtsson (Hafridssons ätt)
LAST	P2600	"6000000011239545575"
#   P569 date of birth = +1276-00-00T00:00:00Z/9
LAST	P569	+1276-00-00T00:00:00Z/9	S2600	"6000000011239545575"
#   P570 date of death = +1313-00-00T00:00:00Z/9
LAST	P570	+1313-00-00T00:00:00Z/9	S2600	"6000000011239545575"
#   P26 spouse = Q101247444 Ingegerd Svantepolksdotter
LAST	P26	Q101247444	S2600	"6000000011239545575"
#   Q101247444 Ingegerd Svantepolksdotter: P26 spouse = the item just created
Q101247444	P26	LAST	S2600	"6000000011239545575"

# create a new item
CREATE
#   the item just created: set the en label to "Eberhard margrave & duke of Friuli"
LAST	Len	"Eberhard margrave & duke of Friuli"
#   set the mul label to "Eberhard margrave & duke of Friuli"
LAST	Lmul	"Eberhard margrave & duke of Friuli"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003495348447 Eberhard margrave & duke of Friuli
LAST	P2600	"6000000003495348447"
#   P569 date of birth = +0815-00-00T00:00:00Z/9
LAST	P569	+0815-00-00T00:00:00Z/9	S2600	"6000000003495348447"
#   P570 date of death = +0867-12-16T00:00:00Z/11
LAST	P570	+0867-12-16T00:00:00Z/11	S2600	"6000000003495348447"
#   P26 spouse = Q284400 Giséle de Cysoing
LAST	P26	Q284400	S2600	"6000000003495348447"
#   P40 child = Q274606 Berengar I margrave of Friuli, king of Italy
LAST	P40	Q274606	S2600	"6000000003495348447"
#   Q284400 Giséle de Cysoing: P26 spouse = the item just created
Q284400	P26	LAST	S2600	"6000000003495348447"
#   Q274606 Berengar I margrave of Friuli, king of Italy: P22 father = the item just created
Q274606	P22	LAST	S2600	"6000000003495348447"
#   the item just created: P735 given name = Q1278816 Eberhard
LAST	P735	Q1278816
#   P1449 nickname = en:"Everardo"
LAST	P1449	en:"Everardo"
#   add a mul alias "Everardo"
LAST	Amul	"Everardo"

# create a new item
CREATE
#   set the en label to "Fartegn Matsson Matsson"
LAST	Len	"Fartegn Matsson Matsson"
#   set the mul label to "Fartegn Matsson Matsson"
LAST	Lmul	"Fartegn Matsson Matsson"
#   add a mul alias "Fartegn Matsson Æne"
LAST	Amul	"Fartegn Matsson Æne"
#   set the ja label to "ファルテグン・マットソン・マットソン"
LAST	Lja	"ファルテグン・マットソン・マットソン"
#   set the zh label to "法尔特格恩·马特松·马特松"
LAST	Lzh	"法尔特格恩·马特松·马特松"
#   add a ja alias "ファルテグン・マットソン・エーネ"
LAST	Aja	"ファルテグン・マットソン・エーネ"
#   add a zh alias "法尔特格恩·马特松·埃内"
LAST	Azh	"法尔特格恩·马特松·埃内"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000000574078388 Fartegn Matsson Æne
LAST	P2600	"6000000000574078388"
#   P569 date of birth = +1477-00-00T00:00:00Z/9
LAST	P569	+1477-00-00T00:00:00Z/9	S2600	"6000000000574078388"
#   P570 date of death = +1564-00-00T00:00:00Z/9
LAST	P570	+1564-00-00T00:00:00Z/9	S2600	"6000000000574078388"
#   P40 child = Q141178149 Anna Fartegnsdatter Seim
LAST	P40	Q141178149	S2600	"6000000000574078388"
#   Q141178149 Anna Fartegnsdatter Seim: P22 father = the item just created
Q141178149	P22	LAST	S2600	"6000000000574078388"
#   the item just created: P734 family name = Q27881920 Matsson
LAST	P734	Q27881920
#   P1449 nickname = en:"Losna-ætten"
LAST	P1449	en:"Losna-ætten"
#   add a mul alias "Losna-ætten Matsson"
LAST	Amul	"Losna-ætten Matsson"
#   add a mul alias "Fartegn Matsson"
LAST	Amul	"Fartegn Matsson"

# create a new item
CREATE
#   set the en label to "Hedvig Svantepolks de Gdańsk of Danzig"
LAST	Len	"Hedvig Svantepolks de Gdańsk of Danzig"
#   set the mul label to "Hedvig Svantepolks de Gdańsk of Danzig"
LAST	Lmul	"Hedvig Svantepolks de Gdańsk of Danzig"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003358192683 Hedvig Svantepolks de Gdańsk of Danzig
LAST	P2600	"6000000003358192683"
#   P569 date of birth = +1210-00-00T00:00:00Z/9
LAST	P569	+1210-00-00T00:00:00Z/9	S2600	"6000000003358192683"
#   P570 date of death = +1266-00-00T00:00:00Z/9
LAST	P570	+1266-00-00T00:00:00Z/9	S2600	"6000000003358192683"
#   P26 spouse = Q3743799 Knut Valdemarsson Duke of Estland, Blekinge and Lolland
LAST	P26	Q3743799	S2600	"6000000003358192683"
#   P40 child = Q6197518 Svantepolk Knutsson Viby Skarsholmsätten
LAST	P40	Q6197518	S2600	"6000000003358192683"
#   Q3743799 Knut Valdemarsson Duke of Estland, Blekinge and Lolland: P26 spouse = the item just created
Q3743799	P26	LAST	S2600	"6000000003358192683"
#   Q6197518 Svantepolk Knutsson Viby Skarsholmsätten: P25 mother = the item just created
Q6197518	P25	LAST	S2600	"6000000003358192683"
#   the item just created: P735 given name = Q13648620 Hedvig, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q13648620	P1545	"1"	P7452	Q3409033
#   P1449 nickname = en:"Hedwig of Pomorze Gdanskie"
LAST	P1449	en:"Hedwig of Pomorze Gdanskie"
#   add a mul alias "Hedwig of Pomorze Gdanskie de Gdańsk"
LAST	Amul	"Hedwig of Pomorze Gdanskie de Gdańsk"

# create a new item
CREATE
#   set the en label to "Helen Frisk"
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
#   P2600 Geni.com profile ID = 6000000177921459052 Helen Frisk
LAST	P2600	"6000000177921459052"
#   P40 child = Q140568870 Emma Leonhart
LAST	P40	Q140568870	S2600	"6000000177921459052"
#   Q140568870 Emma Leonhart: P25 mother = the item just created
Q140568870	P25	LAST	S2600	"6000000177921459052"
#   the item just created: P735 given name = Q13376892 Helen
LAST	P735	Q13376892
#   P734 family name = Q27877507 Frisk
LAST	P734	Q27877507

# create a new item
CREATE
#   set the en label to "Jacob Johannessen Jacobson"
LAST	Len	"Jacob Johannessen Jacobson"
#   set the mul label to "Jacob Johannessen Jacobson"
LAST	Lmul	"Jacob Johannessen Jacobson"
#   add a mul alias "Jacob Johannessen Aabø"
LAST	Amul	"Jacob Johannessen Aabø"
#   set the ja label to "ヤコブ・ヨハンネセン・ヤコブソン"
LAST	Lja	"ヤコブ・ヨハンネセン・ヤコブソン"
#   set the zh label to "雅各布·约翰内森·雅各布松"
LAST	Lzh	"雅各布·约翰内森·雅各布松"
#   add a ja alias "ヤコブ・ヨハンネセン・オーベー"
LAST	Aja	"ヤコブ・ヨハンネセン・オーベー"
#   add a zh alias "雅各布·约翰内森·奥贝"
LAST	Azh	"雅各布·约翰内森·奥贝"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000019384694298 Jacob Johannessen Aabø
LAST	P2600	"6000000019384694298"
#   P569 date of birth = +1853-03-11T00:00:00Z/11
LAST	P569	+1853-03-11T00:00:00Z/11	S2600	"6000000019384694298"
#   P570 date of death = +1877-00-00T00:00:00Z/9
LAST	P570	+1877-00-00T00:00:00Z/9	S2600	"6000000019384694298"
#   P26 spouse = Q141152600 Stine Stena Eivindsdatter Garborg
LAST	P26	Q141152600	S2600	"6000000019384694298"
#   P40 child = Q141168794 Betsy Jacobson
LAST	P40	Q141168794	S2600	"6000000019384694298"
#   Q141152600 Stine Stena Eivindsdatter Garborg: P26 spouse = the item just created
Q141152600	P26	LAST	S2600	"6000000019384694298"
#   Q141168794 Betsy Jacobson: P22 father = the item just created
Q141168794	P22	LAST	S2600	"6000000019384694298"
#   the item just created: P735 given name = Q25999604 Jacob
LAST	P735	Q25999604
#   P734 family name = Q4160058 Jacobson
LAST	P734	Q4160058
#   add a mul alias "Jacob Jacobson"
LAST	Amul	"Jacob Jacobson"

# create a new item
CREATE
#   set the en label to "Jon Olson Raustad"
LAST	Len	"Jon Olson Raustad"
#   set the mul label to "Jon Olson Raustad"
LAST	Lmul	"Jon Olson Raustad"
#   set the ja label to "ヨン・オルソン・ラウスタード"
LAST	Lja	"ヨン・オルソン・ラウスタード"
#   set the zh label to "永·奥尔松·劳斯塔"
LAST	Lzh	"永·奥尔松·劳斯塔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003491988836 Jon Olson Raustad
LAST	P2600	"6000000003491988836"
#   P569 date of birth = +1708-09-29T00:00:00Z/11
LAST	P569	+1708-09-29T00:00:00Z/11	S2600	"6000000003491988836"
#   P570 date of death = +1769-00-00T00:00:00Z/9
LAST	P570	+1769-00-00T00:00:00Z/9	S2600	"6000000003491988836"
#   P40 child = Q141178380 Samuel Jonson Raustad
LAST	P40	Q141178380	S2600	"6000000003491988836"
#   Q141178380 Samuel Jonson Raustad: P22 father = the item just created
Q141178380	P22	LAST	S2600	"6000000003491988836"
#   the item just created: P735 given name = Q13501137 Jon
LAST	P735	Q13501137

# create a new item
CREATE
#   set the en label to "Joren Jonsdatter Espedal"
LAST	Len	"Joren Jonsdatter Espedal"
#   set the mul label to "Joren Jonsdatter Espedal"
LAST	Lmul	"Joren Jonsdatter Espedal"
#   set the ja label to "ヨーレン・ヨンスダッテル・エスペダール"
LAST	Lja	"ヨーレン・ヨンスダッテル・エスペダール"
#   set the zh label to "约伦·永斯达特·埃斯佩达尔"
LAST	Lzh	"约伦·永斯达特·埃斯佩达尔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005609425388 Joren Jonsdatter Espedal
LAST	P2600	"6000000005609425388"
#   P570 date of death = +1757-00-00T00:00:00Z/9
LAST	P570	+1757-00-00T00:00:00Z/9	S2600	"6000000005609425388"
#   P40 child = Q141180408 Jon Larsson Li
LAST	P40	Q141180408	S2600	"6000000005609425388"
#   Q141180408 Jon Larsson Li: P25 mother = the item just created
Q141180408	P25	LAST	S2600	"6000000005609425388"
#   the item just created: P1449 nickname = en:"Joren J Mæle"
LAST	P1449	en:"Joren J Mæle"
#   add a mul alias "Joren J Mæle Espedal"
LAST	Amul	"Joren J Mæle Espedal"
#   add a mul alias "Joren Espedal"
LAST	Amul	"Joren Espedal"

# create a new item
CREATE
#   set the en label to "Karen Sophie Pedersdatter"
LAST	Len	"Karen Sophie Pedersdatter"
#   set the mul label to "Karen Sophie Pedersdatter"
LAST	Lmul	"Karen Sophie Pedersdatter"
#   set the ja label to "カーレン・ソフィー・ペーデシュダッテル"
LAST	Lja	"カーレン・ソフィー・ペーデシュダッテル"
#   set the zh label to "卡伦·索菲·佩德斯达特"
LAST	Lzh	"卡伦·索菲·佩德斯达特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000021137401277 Karen Sophie Pedersdatter
LAST	P2600	"6000000021137401277"
#   P40 child = Q141178201 Marie Petrine Simensdatter Bergersen
LAST	P40	Q141178201	S2600	"6000000021137401277"
#   Q141178201 Marie Petrine Simensdatter Bergersen: P25 mother = the item just created
Q141178201	P25	LAST	S2600	"6000000021137401277"
#   the item just created: P735 given name = Q14942517 Sophie, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q14942517	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Karen Toresdatter Kold"
LAST	Len	"Karen Toresdatter Kold"
#   set the mul label to "Karen Toresdatter Kold"
LAST	Lmul	"Karen Toresdatter Kold"
#   set the ja label to "カーレン・トーレスダッテル・コル"
LAST	Lja	"カーレン・トーレスダッテル・コル"
#   set the zh label to "卡伦·托雷斯达特·科尔德"
LAST	Lzh	"卡伦·托雷斯达特·科尔德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000175321141191 Karen Toresdatter Kold
LAST	P2600	"6000000175321141191"
#   P569 date of birth = +1470-00-00T00:00:00Z/9
LAST	P569	+1470-00-00T00:00:00Z/9	S2600	"6000000175321141191"
#   P570 date of death = +1515-00-00T00:00:00Z/9
LAST	P570	+1515-00-00T00:00:00Z/9	S2600	"6000000175321141191"
#   P40 child = Q141178149 Anna Fartegnsdatter Seim
LAST	P40	Q141178149	S2600	"6000000175321141191"
#   Q141178149 Anna Fartegnsdatter Seim: P25 mother = the item just created
Q141178149	P25	LAST	S2600	"6000000175321141191"
#   the item just created: add a mul alias "Karen Kold"
LAST	Amul	"Karen Kold"

# create a new item
CREATE
#   set the en label to "Kirsten Gabrielsdatter Austråt"
LAST	Len	"Kirsten Gabrielsdatter Austråt"
#   set the mul label to "Kirsten Gabrielsdatter Austråt"
LAST	Lmul	"Kirsten Gabrielsdatter Austråt"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003491988841 Kirsten Gabrielsdatter Austråt
LAST	P2600	"6000000003491988841"
#   P569 date of birth = +1712-03-05T00:00:00Z/11
LAST	P569	+1712-03-05T00:00:00Z/11	S2600	"6000000003491988841"
#   P570 date of death = +1778-03-08T00:00:00Z/11
LAST	P570	+1778-03-08T00:00:00Z/11	S2600	"6000000003491988841"
#   P40 child = Q141178380 Samuel Jonson Raustad
LAST	P40	Q141178380	S2600	"6000000003491988841"
#   Q141178380 Samuel Jonson Raustad: P25 mother = the item just created
Q141178380	P25	LAST	S2600	"6000000003491988841"
#   the item just created: P735 given name = Q256744 Kirsten
LAST	P735	Q256744

# create a new item
CREATE
#   set the en label to "Kourei-tenno (Oyamatonekohikofutoni)"
LAST	Len	"Kourei-tenno (Oyamatonekohikofutoni)"
#   set the mul label to "Kourei-tenno (Oyamatonekohikofutoni)"
LAST	Lmul	"Kourei-tenno (Oyamatonekohikofutoni)"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000001829634518 Kourei-tenno (Oyamatonekohikofutoni)
LAST	P2600	"6000000001829634518"
#   P569 date of birth = -0342-00-00T00:00:00Z/9
LAST	P569	-0342-00-00T00:00:00Z/9	S2600	"6000000001829634518"
#   P570 date of death = -0215-03-27T00:00:00Z/11
LAST	P570	-0215-03-27T00:00:00Z/11	S2600	"6000000001829634518"
#   P40 child = Q11596350 Wakatakehiko
LAST	P40	Q11596350	S2600	"6000000001829634518"
#   Q11596350 Wakatakehiko: P22 father = the item just created
Q11596350	P22	LAST	S2600	"6000000001829634518"
#   the item just created: add a mul alias "大日本根子彦太瓊尊 孝霊天皇"
LAST	Amul	"大日本根子彦太瓊尊 孝霊天皇"

# create a new item
CREATE
#   set the en label to "Kristian Larsen Sør-Reime"
LAST	Len	"Kristian Larsen Sør-Reime"
#   set the mul label to "Kristian Larsen Sør-Reime"
LAST	Lmul	"Kristian Larsen Sør-Reime"
#   add a mul alias "Kristian Larsen Nord-Varhaug"
LAST	Amul	"Kristian Larsen Nord-Varhaug"
#   set the ja label to "クリスティアン・ラーシェン・セール・レイメ"
LAST	Lja	"クリスティアン・ラーシェン・セール・レイメ"
#   set the zh label to "克里斯蒂安·拉尔森·瑟尔·雷梅"
LAST	Lzh	"克里斯蒂安·拉尔森·瑟尔·雷梅"
#   add a ja alias "クリスティアン・ラーシェン・ノール・ヴァールハウグ"
LAST	Aja	"クリスティアン・ラーシェン・ノール・ヴァールハウグ"
#   add a zh alias "克里斯蒂安·拉尔森·诺尔·瓦尔豪格"
LAST	Azh	"克里斯蒂安·拉尔森·诺尔·瓦尔豪格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000029302543031 Kristian Larsen Nord-Varhaug
LAST	P2600	"6000000029302543031"
#   P569 date of birth = +1829-02-15T00:00:00Z/11
LAST	P569	+1829-02-15T00:00:00Z/11	S2600	"6000000029302543031"
#   P570 date of death = +1917-02-09T00:00:00Z/11
LAST	P570	+1917-02-09T00:00:00Z/11	S2600	"6000000029302543031"
#   P26 spouse = Q141168816 Elisabet Ådnesdatter Garborg
LAST	P26	Q141168816	S2600	"6000000029302543031"
#   Q141168816 Elisabet Ådnesdatter Garborg: P26 spouse = the item just created
Q141168816	P26	LAST	S2600	"6000000029302543031"
#   the item just created: P735 given name = Q12794332 Kristian
LAST	P735	Q12794332
#   add a mul alias "Kristian Sør-Reime"
LAST	Amul	"Kristian Sør-Reime"

# create a new item
CREATE
#   set the en label to "Kristina Tolvesdotter Näs"
LAST	Len	"Kristina Tolvesdotter Näs"
#   set the mul label to "Kristina Tolvesdotter Näs"
LAST	Lmul	"Kristina Tolvesdotter Näs"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 340342479380013975 Kristina Tolvesdotter Näs
LAST	P2600	"340342479380013975"
#   P569 date of birth = +1290-00-00T00:00:00Z/9
LAST	P569	+1290-00-00T00:00:00Z/9	S2600	"340342479380013975"
#   P570 date of death = +1330-00-00T00:00:00Z/9
LAST	P570	+1330-00-00T00:00:00Z/9	S2600	"340342479380013975"
#   P40 child = Q5915800 Knut Algotsson
LAST	P40	Q5915800	S2600	"340342479380013975"
#   Q5915800 Knut Algotsson: P25 mother = the item just created
Q5915800	P25	LAST	S2600	"340342479380013975"
#   the item just created: P735 given name = Q19798802 Kristina, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q19798802	P1545	"1"	P7452	Q3409033
#   P1449 nickname = en:"Tolveætten"
LAST	P1449	en:"Tolveætten"
#   add a mul alias "Tolveætten Näs"
LAST	Amul	"Tolveætten Näs"

# create a new item
CREATE
#   set the en label to "Lars Kristiansen Sør-Reime"
LAST	Len	"Lars Kristiansen Sør-Reime"
#   set the mul label to "Lars Kristiansen Sør-Reime"
LAST	Lmul	"Lars Kristiansen Sør-Reime"
#   set the ja label to "ラーシュ・クリスティアンセン・セール・レイメ"
LAST	Lja	"ラーシュ・クリスティアンセン・セール・レイメ"
#   set the zh label to "拉尔斯·克里斯蒂安森·瑟尔·雷梅"
LAST	Lzh	"拉尔斯·克里斯蒂安森·瑟尔·雷梅"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000224702528843 Lars Kristiansen Sør-Reime
LAST	P2600	"6000000224702528843"
#   P569 date of birth = +1861-05-21T00:00:00Z/11
LAST	P569	+1861-05-21T00:00:00Z/11	S2600	"6000000224702528843"
#   P570 date of death = +1866-02-25T00:00:00Z/11
LAST	P570	+1866-02-25T00:00:00Z/11	S2600	"6000000224702528843"
#   P25 mother = Q141168816 Elisabet Ådnesdatter Garborg
LAST	P25	Q141168816	S2600	"6000000224702528843"
#   Q141168816 Elisabet Ådnesdatter Garborg: P40 child = the item just created
Q141168816	P40	LAST	S2600	"6000000224702528843"
#   the item just created: P735 given name = Q15635262 Lars
LAST	P735	Q15635262

# create a new item
CREATE
#   set the en label to "Lars Tormodsen Mele"
LAST	Len	"Lars Tormodsen Mele"
#   set the mul label to "Lars Tormodsen Mele"
LAST	Lmul	"Lars Tormodsen Mele"
#   set the ja label to "ラーシュ・トルモドセン・メーレ"
LAST	Lja	"ラーシュ・トルモドセン・メーレ"
#   set the zh label to "拉尔斯·托尔莫德森·梅勒"
LAST	Lzh	"拉尔斯·托尔莫德森·梅勒"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005609425379 Lars Tormodsen Mele
LAST	P2600	"6000000005609425379"
#   P569 date of birth = +1664-00-00T00:00:00Z/9
LAST	P569	+1664-00-00T00:00:00Z/9	S2600	"6000000005609425379"
#   P570 date of death = +1744-00-00T00:00:00Z/9
LAST	P570	+1744-00-00T00:00:00Z/9	S2600	"6000000005609425379"
#   P40 child = Q141180408 Jon Larsson Li
LAST	P40	Q141180408	S2600	"6000000005609425379"
#   Q141180408 Jon Larsson Li: P22 father = the item just created
Q141180408	P22	LAST	S2600	"6000000005609425379"
#   the item just created: P735 given name = Q15635262 Lars
LAST	P735	Q15635262
#   P1449 nickname = en:"Mæle"
LAST	P1449	en:"Mæle"
#   add a mul alias "Mæle Mele"
LAST	Amul	"Mæle Mele"
#   add a mul alias "Lars Mele"
LAST	Amul	"Lars Mele"

# create a new item
CREATE
#   set the en label to "Lave"
LAST	Len	"Lave"
#   set the mul label to "Lave"
LAST	Lmul	"Lave"
#   set the ja label to "ラーヴェ"
LAST	Lja	"ラーヴェ"
#   set the zh label to "拉弗"
LAST	Lzh	"拉弗"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000181444356836 Lave
LAST	P2600	"6000000181444356836"
#   P735 given name = Q134450528 Lave
LAST	P735	Q134450528

# create a new item
CREATE
#   set the en label to "Lotte Birgithe Gustava Jonasdatter Lea"
LAST	Len	"Lotte Birgithe Gustava Jonasdatter Lea"
#   set the mul label to "Lotte Birgithe Gustava Jonasdatter Lea"
LAST	Lmul	"Lotte Birgithe Gustava Jonasdatter Lea"
#   add a mul alias "Lotte Birgithe Gustava Jonasdatter Heigre"
LAST	Amul	"Lotte Birgithe Gustava Jonasdatter Heigre"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000025793394310 Lotte Birgithe Gustava Jonasdatter Heigre
LAST	P2600	"6000000025793394310"
#   P569 date of birth = +1876-07-07T00:00:00Z/11
LAST	P569	+1876-07-07T00:00:00Z/11	S2600	"6000000025793394310"
#   P570 date of death = +1943-02-17T00:00:00Z/11
LAST	P570	+1943-02-17T00:00:00Z/11	S2600	"6000000025793394310"
#   P22 father = Q141168957 Jonas Jonson Heigre
LAST	P22	Q141168957	S2600	"6000000025793394310"
#   P25 mother = Q141178196 Elisabet Kirstine Eriksdatter Stangeland
LAST	P25	Q141178196	S2600	"6000000025793394310"
#   Q141168957 Jonas Jonson Heigre: P40 child = the item just created
Q141168957	P40	LAST	S2600	"6000000025793394310"
#   Q141178196 Elisabet Kirstine Eriksdatter Stangeland: P40 child = the item just created
Q141178196	P40	LAST	S2600	"6000000025793394310"
#   the item just created: P735 given name = Q2352826 Lotte, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q2352826	P1545	"1"	P7452	Q3409033
#   P735 given name = Q117322332 Birgithe, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q117322332	P1545	"2"	P3831	Q245025
#   P735 given name = Q21144392 Gustava, qualified series ordinal 3, object of statement has role Q245025 middle name
LAST	P735	Q21144392	P1545	"3"	P3831	Q245025
#   P734 family name = Q6508166 Lea, qualified object of statement has role Q28418670 married name
LAST	P734	Q6508166	P3831	Q28418670
#   add a mul alias "Lotte Birgithe Gustava Lea"
LAST	Amul	"Lotte Birgithe Gustava Lea"

# create a new item
CREATE
#   set the en label to "Martin Tollefson Tunheim"
LAST	Len	"Martin Tollefson Tunheim"
#   set the mul label to "Martin Tollefson Tunheim"
LAST	Lmul	"Martin Tollefson Tunheim"
#   set the ja label to "マルティン・トレフソン・トゥンヘイム"
LAST	Lja	"マルティン・トレフソン・トゥンヘイム"
#   set the zh label to "马丁·托勒夫松·通海姆"
LAST	Lzh	"马丁·托勒夫松·通海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000019384841547 Martin Tollefson Tunheim
LAST	P2600	"6000000019384841547"
#   P569 date of birth = +1867-12-03T00:00:00Z/11
LAST	P569	+1867-12-03T00:00:00Z/11	S2600	"6000000019384841547"
#   P570 date of death = +1937-04-14T00:00:00Z/11
LAST	P570	+1937-04-14T00:00:00Z/11	S2600	"6000000019384841547"
#   P26 spouse = Q141162046 Ane Oline Lena Eivindsdatter Garborg
LAST	P26	Q141162046	S2600	"6000000019384841547"
#   P40 child = Q141169062 Thoralf Tunheim
LAST	P40	Q141169062	S2600	"6000000019384841547"
#   P40 child = Q141168801 Cora Estelle Tunheim
LAST	P40	Q141168801	S2600	"6000000019384841547"
#   P40 child = Q141168809 Edward Tunheim
LAST	P40	Q141168809	S2600	"6000000019384841547"
#   P40 child = Q141168787 Alma Matilda Tunheim
LAST	P40	Q141168787	S2600	"6000000019384841547"
#   P40 child = Q141169041 Olaf Tunheim
LAST	P40	Q141169041	S2600	"6000000019384841547"
#   P40 child = Q141168788 Arne Garborg Tunheim
LAST	P40	Q141168788	S2600	"6000000019384841547"
#   Q141162046 Ane Oline Lena Eivindsdatter Garborg: P26 spouse = the item just created
Q141162046	P26	LAST	S2600	"6000000019384841547"
#   Q141169062 Thoralf Tunheim: P22 father = the item just created
Q141169062	P22	LAST	S2600	"6000000019384841547"
#   Q141168801 Cora Estelle Tunheim: P22 father = the item just created
Q141168801	P22	LAST	S2600	"6000000019384841547"
#   Q141168809 Edward Tunheim: P22 father = the item just created
Q141168809	P22	LAST	S2600	"6000000019384841547"
#   Q141168787 Alma Matilda Tunheim: P22 father = the item just created
Q141168787	P22	LAST	S2600	"6000000019384841547"
#   Q141169041 Olaf Tunheim: P22 father = the item just created
Q141169041	P22	LAST	S2600	"6000000019384841547"
#   Q141168788 Arne Garborg Tunheim: P22 father = the item just created
Q141168788	P22	LAST	S2600	"6000000019384841547"
#   the item just created: P735 given name = Q18002399 Martin
LAST	P735	Q18002399

# create a new item
CREATE
#   set the en label to "Ola Jonson Li"
LAST	Len	"Ola Jonson Li"
#   set the mul label to "Ola Jonson Li"
LAST	Lmul	"Ola Jonson Li"
#   set the ja label to "オーラ・ヨンソン・リ"
LAST	Lja	"オーラ・ヨンソン・リ"
#   set the zh label to "乌拉·永松·李"
LAST	Lzh	"乌拉·永松·李"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003095034832 Ola Jonson Li
LAST	P2600	"6000000003095034832"
#   P22 father = Q141180408 Jon Larsson Li
LAST	P22	Q141180408	S2600	"6000000003095034832"
#   P25 mother = Q141180412 Marta Rasmusdatter Høle
LAST	P25	Q141180412	S2600	"6000000003095034832"
#   Q141180408 Jon Larsson Li: P40 child = the item just created
Q141180408	P40	LAST	S2600	"6000000003095034832"
#   Q141180412 Marta Rasmusdatter Høle: P40 child = the item just created
Q141180412	P40	LAST	S2600	"6000000003095034832"
#   the item just created: P735 given name = Q96675523 Ola
LAST	P735	Q96675523

# create a new item
CREATE
#   set the en label to "Olga E. Garborg Oswald"
LAST	Len	"Olga E. Garborg Oswald"
#   set the mul label to "Olga E. Garborg Oswald"
LAST	Lmul	"Olga E. Garborg Oswald"
#   add a mul alias "Olga E. Tunheim"
LAST	Amul	"Olga E. Tunheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000033773801550 Olga E. Tunheim
LAST	P2600	"6000000033773801550"
#   P569 date of birth = +1900-10-25T00:00:00Z/11
LAST	P569	+1900-10-25T00:00:00Z/11	S2600	"6000000033773801550"
#   P570 date of death = +1961-01-27T00:00:00Z/11
LAST	P570	+1961-01-27T00:00:00Z/11	S2600	"6000000033773801550"
#   P25 mother = Q141162046 Ane Oline Lena Eivindsdatter Garborg
LAST	P25	Q141162046	S2600	"6000000033773801550"
#   Q141162046 Ane Oline Lena Eivindsdatter Garborg: P40 child = the item just created
Q141162046	P40	LAST	S2600	"6000000033773801550"
#   the item just created: P735 given name = Q19803501 E., qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q19803501	P1545	"2"	P3831	Q245025
#   P734 family name = Q30250555 Garborg, qualified object of statement has role Q28418670 married name
LAST	P734	Q30250555	P3831	Q28418670
#   P734 family name = Q1260183 Oswald, qualified object of statement has role Q28418670 married name
LAST	P734	Q1260183	P3831	Q28418670

# create a new item
CREATE
#   set the en label to "Ragnhild Toresdatter Håland i Gjesdal"
LAST	Len	"Ragnhild Toresdatter Håland i Gjesdal"
#   set the mul label to "Ragnhild Toresdatter Håland i Gjesdal"
LAST	Lmul	"Ragnhild Toresdatter Håland i Gjesdal"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005609425396 Ragnhild Toresdatter Håland i Gjesdal
LAST	P2600	"6000000005609425396"
#   P569 date of birth = +1661-00-00T00:00:00Z/9
LAST	P569	+1661-00-00T00:00:00Z/9	S2600	"6000000005609425396"
#   P570 date of death = +1709-00-00T00:00:00Z/9
LAST	P570	+1709-00-00T00:00:00Z/9	S2600	"6000000005609425396"
#   P735 given name = Q1390292 Ragnhild
LAST	P735	Q1390292
#   P734 family name = Q27888954 Gjesdal
LAST	P734	Q27888954

# create a new item
CREATE
#   set the en label to "Richard Wade Borsheim"
LAST	Len	"Richard Wade Borsheim"
#   set the mul label to "Richard Wade Borsheim"
LAST	Lmul	"Richard Wade Borsheim"
#   set the ja label to "リチャード・ウェイド・ボルスハイム"
LAST	Lja	"リチャード・ウェイド・ボルスハイム"
#   set the zh label to "理查德·韦德·博尔斯海姆"
LAST	Lzh	"理查德·韦德·博尔斯海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000177921459056 Richard Wade Borsheim
LAST	P2600	"6000000177921459056"
#   P569 date of birth = +1963-10-20T00:00:00Z/11
LAST	P569	+1963-10-20T00:00:00Z/11	S2600	"6000000177921459056"
#   P40 child = Q140568870 Emma Leonhart
LAST	P40	Q140568870	S2600	"6000000177921459056"
#   Q140568870 Emma Leonhart: P22 father = the item just created
Q140568870	P22	LAST	S2600	"6000000177921459056"
#   the item just created: P735 given name = Q1249148 Richard, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q1249148	P1545	"1"	P7452	Q3409033
#   P735 given name = Q15630117 Wade, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q15630117	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Simen Olsen"
LAST	Len	"Simen Olsen"
#   set the mul label to "Simen Olsen"
LAST	Lmul	"Simen Olsen"
#   set the ja label to "シーメン・オルセン"
LAST	Lja	"シーメン・オルセン"
#   set the zh label to "西门·奥尔森"
LAST	Lzh	"西门·奥尔森"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000016756376445 Simen Olsen
LAST	P2600	"6000000016756376445"
#   P40 child = Q141178201 Marie Petrine Simensdatter Bergersen
LAST	P40	Q141178201	S2600	"6000000016756376445"
#   Q141178201 Marie Petrine Simensdatter Bergersen: P22 father = the item just created
Q141178201	P22	LAST	S2600	"6000000016756376445"
#   the item just created: P735 given name = Q2287061 Simen
LAST	P735	Q2287061
#   P734 family name = Q12042571 Olsen
LAST	P734	Q12042571

# create a new item
CREATE
#   set the en label to "Siri Kristine Ivarsdatter Garborg"
LAST	Len	"Siri Kristine Ivarsdatter Garborg"
#   set the mul label to "Siri Kristine Ivarsdatter Garborg"
LAST	Lmul	"Siri Kristine Ivarsdatter Garborg"
#   add a mul alias "Siri Kristine Ivarsdatter Sandsmark"
LAST	Amul	"Siri Kristine Ivarsdatter Sandsmark"
#   set the ja label to "シーリ・クリスティーネ・イーヴァシュダッテル・ガルボルグ"
LAST	Lja	"シーリ・クリスティーネ・イーヴァシュダッテル・ガルボルグ"
#   set the zh label to "西丽·克丽丝汀·伊瓦斯达特·加尔博格"
LAST	Lzh	"西丽·克丽丝汀·伊瓦斯达特·加尔博格"
#   add a ja alias "シーリ・クリスティーネ・イーヴァシュダッテル・サンスマルク"
LAST	Aja	"シーリ・クリスティーネ・イーヴァシュダッテル・サンスマルク"
#   add a zh alias "西丽·克丽丝汀·伊瓦斯达特·桑斯马克"
LAST	Azh	"西丽·克丽丝汀·伊瓦斯达特·桑斯马克"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000002954315535 Siri Kristine Ivarsdatter Sandsmark
LAST	P2600	"6000000002954315535"
#   P569 date of birth = +1863-01-19T00:00:00Z/11
LAST	P569	+1863-01-19T00:00:00Z/11	S2600	"6000000002954315535"
#   P570 date of death = +1939-10-19T00:00:00Z/11
LAST	P570	+1939-10-19T00:00:00Z/11	S2600	"6000000002954315535"
#   P26 spouse = Q141152614 Jon Eivindson Garborg
LAST	P26	Q141152614	S2600	"6000000002954315535"
#   P40 child = Q141168811 Eivind Garborg
LAST	P40	Q141168811	S2600	"6000000002954315535"
#   P40 child = Q141168792 Astrid Garborg
LAST	P40	Q141168792	S2600	"6000000002954315535"
#   P40 child = Q141168837 Ingebret Garborg
LAST	P40	Q141168837	S2600	"6000000002954315535"
#   P40 child = Q141168830 Ingeborg Garborg
LAST	P40	Q141168830	S2600	"6000000002954315535"
#   P40 child = Q141168954 Jon Garborg
LAST	P40	Q141168954	S2600	"6000000002954315535"
#   P40 child = Q141168784 Aagot Garborg
LAST	P40	Q141168784	S2600	"6000000002954315535"
#   Q141152614 Jon Eivindson Garborg: P26 spouse = the item just created
Q141152614	P26	LAST	S2600	"6000000002954315535"
#   Q141168811 Eivind Garborg: P25 mother = the item just created
Q141168811	P25	LAST	S2600	"6000000002954315535"
#   Q141168792 Astrid Garborg: P25 mother = the item just created
Q141168792	P25	LAST	S2600	"6000000002954315535"
#   Q141168837 Ingebret Garborg: P25 mother = the item just created
Q141168837	P25	LAST	S2600	"6000000002954315535"
#   Q141168830 Ingeborg Garborg: P25 mother = the item just created
Q141168830	P25	LAST	S2600	"6000000002954315535"
#   Q141168954 Jon Garborg: P25 mother = the item just created
Q141168954	P25	LAST	S2600	"6000000002954315535"
#   Q141168784 Aagot Garborg: P25 mother = the item just created
Q141168784	P25	LAST	S2600	"6000000002954315535"
#   the item just created: P735 given name = Q1772342 Siri, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q1772342	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16859157 Kristine, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q16859157	P1545	"2"	P3831	Q245025
#   P734 family name = Q30250555 Garborg, qualified object of statement has role Q28418670 married name
LAST	P734	Q30250555	P3831	Q28418670
#   add a mul alias "Siri Kristine Garborg"
LAST	Amul	"Siri Kristine Garborg"

# create a new item
CREATE
#   set the en label to "Thekla Cecilie Dybo"
LAST	Len	"Thekla Cecilie Dybo"
#   set the mul label to "Thekla Cecilie Dybo"
LAST	Lmul	"Thekla Cecilie Dybo"
#   add a mul alias "Thekla Cecilie Nyvold"
LAST	Amul	"Thekla Cecilie Nyvold"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000021198276198 Thekla Cecilie Nyvold
LAST	P2600	"6000000021198276198"
#   P569 date of birth = +1889-08-14T00:00:00Z/11
LAST	P569	+1889-08-14T00:00:00Z/11	S2600	"6000000021198276198"
#   P570 date of death = +1983-06-07T00:00:00Z/11
LAST	P570	+1983-06-07T00:00:00Z/11	S2600	"6000000021198276198"
#   P22 father = Q138474188 Hans Syvertsen Nyvold
LAST	P22	Q138474188	S2600	"6000000021198276198"
#   P25 mother = Q141178197 Elisabeth Johannesen
LAST	P25	Q141178197	S2600	"6000000021198276198"
#   Q138474188 Hans Syvertsen Nyvold: P40 child = the item just created
Q138474188	P40	LAST	S2600	"6000000021198276198"
#   Q141178197 Elisabeth Johannesen: P40 child = the item just created
Q141178197	P40	LAST	S2600	"6000000021198276198"
#   the item just created: P735 given name = Q16275183 Cecilie, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q16275183	P1545	"2"	P3831	Q245025
#   P1449 nickname = en:"Tekla Cecilie Nyvold"
LAST	P1449	en:"Tekla Cecilie Nyvold"
#   add a mul alias "Tekla Cecilie Nyvold Dybo"
LAST	Amul	"Tekla Cecilie Nyvold Dybo"

# create a new item
CREATE
#   set the en label to "Tillie Betsy Amundson"
LAST	Len	"Tillie Betsy Amundson"
#   set the mul label to "Tillie Betsy Amundson"
LAST	Lmul	"Tillie Betsy Amundson"
#   add a mul alias "Tillie Betsy Tunheim"
LAST	Amul	"Tillie Betsy Tunheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000008542267056 Tillie Betsy Tunheim
LAST	P2600	"6000000008542267056"
#   P569 date of birth = +1914-03-14T00:00:00Z/11
LAST	P569	+1914-03-14T00:00:00Z/11	S2600	"6000000008542267056"
#   P570 date of death = +1997-03-07T00:00:00Z/11
LAST	P570	+1997-03-07T00:00:00Z/11	S2600	"6000000008542267056"
#   P22 father = Q141180396 Tollef Tollefson Tunheim
LAST	P22	Q141180396	S2600	"6000000008542267056"
#   P25 mother = Q141168794 Betsy Jacobson
LAST	P25	Q141168794	S2600	"6000000008542267056"
#   Q141180396 Tollef Tollefson Tunheim: P40 child = the item just created
Q141180396	P40	LAST	S2600	"6000000008542267056"
#   Q141168794 Betsy Jacobson: P40 child = the item just created
Q141168794	P40	LAST	S2600	"6000000008542267056"
#   the item just created: P735 given name = Q27700115 Tillie, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q27700115	P1545	"1"	P7452	Q3409033
#   P735 given name = Q832242 Betsy, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q832242	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Tønnes Emil Enokson Ronneberg"
LAST	Len	"Tønnes Emil Enokson Ronneberg"
#   set the mul label to "Tønnes Emil Enokson Ronneberg"
LAST	Lmul	"Tønnes Emil Enokson Ronneberg"
#   add a mul alias "Tønnes Emil Enokson Rønneberg"
LAST	Amul	"Tønnes Emil Enokson Rønneberg"
#   set the ja label to "テンネス・エミール・エノクソン・ロンネベルグ"
LAST	Lja	"テンネス・エミール・エノクソン・ロンネベルグ"
#   set the zh label to "滕内斯·埃米尔·埃诺克松·龙内贝格"
LAST	Lzh	"滕内斯·埃米尔·埃诺克松·龙内贝格"
#   add a ja alias "テンネス・エミール・エノクソン・レンネベルグ"
LAST	Aja	"テンネス・エミール・エノクソン・レンネベルグ"
#   add a zh alias "滕内斯·埃米尔·埃诺克松·伦内贝格"
LAST	Azh	"滕内斯·埃米尔·埃诺克松·伦内贝格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003491995164 Tønnes Emil Enokson Rønneberg
LAST	P2600	"6000000003491995164"
#   P569 date of birth = +1859-09-05T00:00:00Z/11
LAST	P569	+1859-09-05T00:00:00Z/11	S2600	"6000000003491995164"
#   P570 date of death = +1927-03-18T00:00:00Z/11
LAST	P570	+1927-03-18T00:00:00Z/11	S2600	"6000000003491995164"
#   P26 spouse = Q141162043 Inger Marie Mary Eivindsdatter Garborg
LAST	P26	Q141162043	S2600	"6000000003491995164"
#   P40 child = Q141168820 Eliza Ronneberg
LAST	P40	Q141168820	S2600	"6000000003491995164"
#   P40 child = Q141168789 Arnold Ronneberg
LAST	P40	Q141168789	S2600	"6000000003491995164"
#   P40 child = Q141168805 Edward Ronneberg
LAST	P40	Q141168805	S2600	"6000000003491995164"
#   P40 child = Q141168786 Alice Ronneberg
LAST	P40	Q141168786	S2600	"6000000003491995164"
#   P40 child = Q141168824 Ernest Anton Ronneberg
LAST	P40	Q141168824	S2600	"6000000003491995164"
#   Q141162043 Inger Marie Mary Eivindsdatter Garborg: P26 spouse = the item just created
Q141162043	P26	LAST	S2600	"6000000003491995164"
#   Q141168820 Eliza Ronneberg: P22 father = the item just created
Q141168820	P22	LAST	S2600	"6000000003491995164"
#   Q141168789 Arnold Ronneberg: P22 father = the item just created
Q141168789	P22	LAST	S2600	"6000000003491995164"
#   Q141168805 Edward Ronneberg: P22 father = the item just created
Q141168805	P22	LAST	S2600	"6000000003491995164"
#   Q141168786 Alice Ronneberg: P22 father = the item just created
Q141168786	P22	LAST	S2600	"6000000003491995164"
#   Q141168824 Ernest Anton Ronneberg: P22 father = the item just created
Q141168824	P22	LAST	S2600	"6000000003491995164"
#   the item just created: P735 given name = Q12008141 Tønnes, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q12008141	P1545	"1"	P7452	Q3409033
#   P735 given name = Q989320 Emil, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q989320	P1545	"2"	P3831	Q245025
#   P734 family name = Q7386722 Rønneberg, qualified object of statement has role Q2507958 birth name
LAST	P734	Q7386722	P3831	Q2507958
#   P1449 nickname = en:"Thom"
LAST	P1449	en:"Thom"
#   add a mul alias "Thom Ronneberg"
LAST	Amul	"Thom Ronneberg"
#   add a mul alias "Tønnes Emil Ronneberg"
LAST	Amul	"Tønnes Emil Ronneberg"

# create a new item
CREATE
#   set the en label to "Willa of Tuscany"
LAST	Len	"Willa of Tuscany"
#   set the mul label to "Willa of Tuscany"
LAST	Lmul	"Willa of Tuscany"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000007141651300 Willa of Tuscany
LAST	P2600	"6000000007141651300"
#   P569 date of birth = +0912-00-00T00:00:00Z/9
LAST	P569	+0912-00-00T00:00:00Z/9	S2600	"6000000007141651300"
#   P570 date of death = +0963-00-00T00:00:00Z/9
LAST	P570	+0963-00-00T00:00:00Z/9	S2600	"6000000007141651300"
#   P40 child = Q466257 Rozala d'Ivrea
LAST	P40	Q466257	S2600	"6000000007141651300"
#   Q466257 Rozala d'Ivrea: P25 mother = the item just created
Q466257	P25	LAST	S2600	"6000000007141651300"
#   the item just created: P735 given name = Q20899018 Willa
LAST	P735	Q20899018
#   P1449 nickname = en:"Willa d'Arles"
LAST	P1449	en:"Willa d'Arles"
#   add a mul alias "Willa d'Arles of Tuscany"
LAST	Amul	"Willa d'Arles of Tuscany"

# create a new item
CREATE
#   set the en label to "Yung Buyeo"
LAST	Len	"Yung Buyeo"
#   set the mul label to "Yung Buyeo"
LAST	Lmul	"Yung Buyeo"
#   set the ja label to "ユン・プヨ"
LAST	Lja	"ユン・プヨ"
#   set the zh label to "隆·扶余"
LAST	Lzh	"隆·扶余"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000012925092093 Yung Buyeo
LAST	P2600	"6000000012925092093"
#   P40 child = Q19657284 Buyeo Deokjang
LAST	P40	Q19657284	S2600	"6000000012925092093"
#   Q19657284 Buyeo Deokjang: P22 father = the item just created
Q19657284	P22	LAST	S2600	"6000000012925092093"

# create a new item
CREATE
#   the item just created: set the mul label to "덕장 부여"
LAST	Lmul	"덕장 부여"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000186285688269 덕장 부여
LAST	P2600	"6000000186285688269"
#   P26 spouse = Q19657284 Buyeo Deokjang
LAST	P26	Q19657284	S2600	"6000000186285688269"
#   P40 child = Q12598947 Taebi Buyeo
LAST	P40	Q12598947	S2600	"6000000186285688269"
#   Q19657284 Buyeo Deokjang: P26 spouse = the item just created
Q19657284	P26	LAST	S2600	"6000000186285688269"
#   Q12598947 Taebi Buyeo: P25 mother = the item just created
Q12598947	P25	LAST	S2600	"6000000186285688269"

# create a new item
CREATE
#   the item just created: set the mul label to "부여융 무명"
LAST	Lmul	"부여융 무명"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000186285688241 부여융 무명
LAST	P2600	"6000000186285688241"
#   P40 child = Q19657284 Buyeo Deokjang
LAST	P40	Q19657284	S2600	"6000000186285688241"
#   Q19657284 Buyeo Deokjang: P25 mother = the item just created
Q19657284	P25	LAST	S2600	"6000000186285688241"

# RELATIONSHIPS between items that already exist -- the links yesterday's
#    creations made possible, and the properties never emitted. Every subject
#    and every value already has a QID, so this section depends on nothing above
#    it. It is emitted LAST, per her order: individuals, names, relationships.

#   Q116150300 Cecilie Ebbesdatter Hvide: P3373 sibling = Q2183430 Bengta Ebbesdotter Ebbesdatter Galen Queen of Sweden
Q116150300	P3373	Q2183430	S2600	"305332989800002467"
#   P735 given name = Q16275183 Cecilie
Q116150300	P735	Q16275183
#   P734 family name = Q55222347 Hvide
Q116150300	P734	Q55222347
#   set the ja label to "セシリエ・エッベスダッテル・ヴィーデ"
Q116150300	Lja	"セシリエ・エッベスダッテル・ヴィーデ"
#   set the zh label to "塞西莉厄·埃贝斯达特·维德"
Q116150300	Lzh	"塞西莉厄·埃贝斯达特·维德"
#   Q2183430 Bengta Ebbesdotter Ebbesdatter Galen Queen of Sweden: P3373 sibling = Q116150300 Cecilie Ebbesdatter Hvide
Q2183430	P3373	Q116150300	S2600	"4947248545210089938"
#   Q284400 Giséle de Cysoing: P40 child = Q274606 Berengar I margrave of Friuli, king of Italy
Q284400	P40	Q274606	S2600	"6000000000424624719"
#   Q11596350 Wakatakehiko: P40 child = Q11078587 Harima no Inabi no Ōiratsume
Q11596350	P40	Q11078587	S2600	"6000000001835522164"
#   Q5915800 Knut Algotsson: set the ja label to "クヌート・アルゴットソン"
Q5915800	Lja	"クヌート・アルゴットソン"
#   set the zh label to "克努特·阿尔戈特松"
Q5915800	Lzh	"克努特·阿尔戈特松"
#   Q3743799 Knut Valdemarsson Duke of Estland, Blekinge and Lolland: P40 child = Q6197518 Svantepolk Knutsson Viby Skarsholmsätten
Q3743799	P40	Q6197518	S2600	"6000000003076221220"
#   Q6197518 Svantepolk Knutsson Viby Skarsholmsätten: P40 child = Q101247444 Ingegerd Svantepolksdotter
Q6197518	P40	Q101247444	S2600	"6000000003418900347"
#   Q141168957 Jonas Jonson Heigre: P40 child = Q141178198 Enevald Jonasson Heigre
Q141168957	P40	Q141178198	S2600	"6000000003491986771"
#   P26 spouse = Q141178196 Elisabet Kirstine Eriksdatter Stangeland
Q141168957	P26	Q141178196	S2600	"6000000003491986771"
#   P26 spouse = Q141152523 Ane Oline Jonsdatter Raugstad
Q141168957	P26	Q141152523	S2600	"6000000003491986771"
#   P735 given name = Q16646115 Jonas
Q141168957	P735	Q16646115
#   set the ja label to "ヨナス・ヨンソン・ヘイグレ"
Q141168957	Lja	"ヨナス・ヨンソン・ヘイグレ"
#   set the zh label to "约纳斯·永松·海格勒"
Q141168957	Lzh	"约纳斯·永松·海格勒"
#   Q141178196 Elisabet Kirstine Eriksdatter Stangeland: P40 child = Q141178198 Enevald Jonasson Heigre
Q141178196	P40	Q141178198	S2600	"6000000003491986941"
#   P26 spouse = Q141168957 Jonas Jonson Heigre
Q141178196	P26	Q141168957	S2600	"6000000003491986941"
#   P735 given name = Q16423275 Elisabet, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141178196	P735	Q16423275	P1545	"1"	P7452	Q3409033
#   P735 given name = Q11980788 Kirstine, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141178196	P735	Q11980788	P1545	"2"	P3831	Q245025
#   P734 family name = Q21452049 Stangeland
Q141178196	P734	Q21452049
#   set the ja label to "エリサベート・シシュティーネ・エリクスダッテル・スタンゲラン"
Q141178196	Lja	"エリサベート・シシュティーネ・エリクスダッテル・スタンゲラン"
#   set the zh label to "伊丽莎白·谢什蒂内·埃里克斯达特·斯坦格兰"
Q141178196	Lzh	"伊丽莎白·谢什蒂内·埃里克斯达特·斯坦格兰"
#   Q141152523 Ane Oline Jonsdatter Raugstad: P22 father = Q141168955 Jon Samuelsen Raustad
Q141152523	P22	Q141168955	S2600	"6000000003491986946"
#   P25 mother = Q141178200 Inger Kristoffersdatter
Q141152523	P25	Q141178200	S2600	"6000000003491986946"
#   P40 child = Q467497 Aadne Eivindson Garborg
Q141152523	P40	Q467497	S2600	"6000000003491986946"
#   P40 child = Q141152600 Stine Stena Eivindsdatter Garborg
Q141152523	P40	Q141152600	S2600	"6000000003491986946"
#   P40 child = Q141152614 Jon Eivindson Garborg
Q141152523	P40	Q141152614	S2600	"6000000003491986946"
#   P40 child = Q141162040 Samuel Eivindsen Garborg
Q141152523	P40	Q141162040	S2600	"6000000003491986946"
#   P40 child = Q141162041 Even Eivindson Garborg
Q141152523	P40	Q141162041	S2600	"6000000003491986946"
#   P40 child = Q141162043 Inger Marie Mary Eivindsdatter Garborg
Q141152523	P40	Q141162043	S2600	"6000000003491986946"
#   P40 child = Q141162044 Abel Eivindsen Garborg
Q141152523	P40	Q141162044	S2600	"6000000003491986946"
#   P40 child = Q141162045 Ole Eivindsen Garborg
Q141152523	P40	Q141162045	S2600	"6000000003491986946"
#   P40 child = Q141162046 Ane Oline Lena Eivindsdatter Garborg
Q141152523	P40	Q141162046	S2600	"6000000003491986946"
#   P3373 sibling = Q141169046 Samuel Jonson
Q141152523	P3373	Q141169046	S2600	"6000000003491986946"
#   P26 spouse = Q141168957 Jonas Jonson Heigre
Q141152523	P26	Q141168957	S2600	"6000000003491986946"
#   P26 spouse = Q141152512 Eivind Aadnesson Garborg
Q141152523	P26	Q141152512	S2600	"6000000003491986946"
#   P735 given name = Q11958077 Ane, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141152523	P735	Q11958077	P1545	"1"	P7452	Q3409033
#   P735 given name = Q11993741 Oline, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141152523	P735	Q11993741	P1545	"2"	P3831	Q245025
#   set the ja label to "アーネ・オリーネ・ヨンスダッテル・ラウグスタード"
Q141152523	Lja	"アーネ・オリーネ・ヨンスダッテル・ラウグスタード"
#   set the zh label to "安内·奥利内·永斯达特·劳格斯塔"
Q141152523	Lzh	"安内·奥利内·永斯达特·劳格斯塔"
#   Q141178198 Enevald Jonasson Heigre: P22 father = Q141168957 Jonas Jonson Heigre
Q141178198	P22	Q141168957	S2600	"6000000003491986956"
#   P25 mother = Q141178196 Elisabet Kirstine Eriksdatter Stangeland
Q141178198	P25	Q141178196	S2600	"6000000003491986956"
#   P735 given name = Q111085860 Enevald
Q141178198	P735	Q111085860
#   set the ja label to "エーネヴァル・ヨナソン・ヘイグレ"
Q141178198	Lja	"エーネヴァル・ヨナソン・ヘイグレ"
#   set the zh label to "埃内瓦尔德·约纳松·海格勒"
Q141178198	Lzh	"埃内瓦尔德·约纳松·海格勒"
#   Q141169046 Samuel Jonson: P22 father = Q141168955 Jon Samuelsen Raustad
Q141169046	P22	Q141168955	S2600	"6000000003491988821"
#   P25 mother = Q141178200 Inger Kristoffersdatter
Q141169046	P25	Q141178200	S2600	"6000000003491988821"
#   P3373 sibling = Q141152523 Ane Oline Jonsdatter Raugstad
Q141169046	P3373	Q141152523	S2600	"6000000003491988821"
#   P735 given name = Q629347 Samuel
Q141169046	P735	Q629347
#   set the ja label to "サムエル・ヨンソン"
Q141169046	Lja	"サムエル・ヨンソン"
#   set the zh label to "萨穆埃尔·永松"
Q141169046	Lzh	"萨穆埃尔·永松"
#   Q141178381 Marta Jonsdatter Li: P22 father = Q141180408 Jon Larsson Li
Q141178381	P22	Q141180408	S2600	"6000000003491988826"
#   P25 mother = Q141180412 Marta Rasmusdatter Høle
Q141178381	P25	Q141180412	S2600	"6000000003491988826"
#   P40 child = Q141168955 Jon Samuelsen Raustad
Q141178381	P40	Q141168955	S2600	"6000000003491988826"
#   P26 spouse = Q141178380 Samuel Jonson Raustad
Q141178381	P26	Q141178380	S2600	"6000000003491988826"
#   P735 given name = Q846741 Marta
Q141178381	P735	Q846741
#   set the ja label to "マルタ・ヨンスダッテル・リ"
Q141178381	Lja	"マルタ・ヨンスダッテル・リ"
#   set the zh label to "玛尔塔·永斯达特·李"
Q141178381	Lzh	"玛尔塔·永斯达特·李"
#   Q141178380 Samuel Jonson Raustad: P40 child = Q141168955 Jon Samuelsen Raustad
Q141178380	P40	Q141168955	S2600	"6000000003491988831"
#   P26 spouse = Q141178381 Marta Jonsdatter Li
Q141178380	P26	Q141178381	S2600	"6000000003491988831"
#   P735 given name = Q629347 Samuel
Q141178380	P735	Q629347
#   set the ja label to "サムエル・ヨンソン・ラウスタード"
Q141178380	Lja	"サムエル・ヨンソン・ラウスタード"
#   set the zh label to "萨穆埃尔·永松·劳斯塔"
Q141178380	Lzh	"萨穆埃尔·永松·劳斯塔"
#   Q141152512 Eivind Aadnesson Garborg: P22 father = Q141169072 Ådne Olsen Grøtheim
Q141152512	P22	Q141169072	S2600	"6000000003492005111"
#   P25 mother = Q141178202 Stine Persdatter Øksnevad
Q141152512	P25	Q141178202	S2600	"6000000003492005111"
#   P40 child = Q467497 Aadne Eivindson Garborg
Q141152512	P40	Q467497	S2600	"6000000003492005111"
#   P40 child = Q141152600 Stine Stena Eivindsdatter Garborg
Q141152512	P40	Q141152600	S2600	"6000000003492005111"
#   P40 child = Q141152614 Jon Eivindson Garborg
Q141152512	P40	Q141152614	S2600	"6000000003492005111"
#   P40 child = Q141162040 Samuel Eivindsen Garborg
Q141152512	P40	Q141162040	S2600	"6000000003492005111"
#   P40 child = Q141162041 Even Eivindson Garborg
Q141152512	P40	Q141162041	S2600	"6000000003492005111"
#   P40 child = Q141162043 Inger Marie Mary Eivindsdatter Garborg
Q141152512	P40	Q141162043	S2600	"6000000003492005111"
#   P40 child = Q141162044 Abel Eivindsen Garborg
Q141152512	P40	Q141162044	S2600	"6000000003492005111"
#   P40 child = Q141162045 Ole Eivindsen Garborg
Q141152512	P40	Q141162045	S2600	"6000000003492005111"
#   P40 child = Q141162046 Ane Oline Lena Eivindsdatter Garborg
Q141152512	P40	Q141162046	S2600	"6000000003492005111"
#   P3373 sibling = Q141168833 Ingeborg Gurie Ådnesdatter Garborg
Q141152512	P3373	Q141168833	S2600	"6000000003492005111"
#   P3373 sibling = Q141168816 Elisabet Ådnesdatter Garborg
Q141152512	P3373	Q141168816	S2600	"6000000003492005111"
#   P26 spouse = Q141152523 Ane Oline Jonsdatter Raugstad
Q141152512	P26	Q141152523	S2600	"6000000003492005111"
#   set the ja label to "エイヴィン・オードネソン・ガルボルグ"
Q141152512	Lja	"エイヴィン・オードネソン・ガルボルグ"
#   set the zh label to "埃温·奥德内松·加尔博格"
Q141152512	Lzh	"埃温·奥德内松·加尔博格"
#   Q467497 Aadne Eivindson Garborg: P40 child = Q11959067 Arne Olaus Fjørtoft Garborg
Q467497	P40	Q11959067	S2600	"6000000003492005116"
#   P3373 sibling = Q141152600 Stine Stena Eivindsdatter Garborg
Q467497	P3373	Q141152600	S2600	"6000000003492005116"
#   P3373 sibling = Q141152614 Jon Eivindson Garborg
Q467497	P3373	Q141152614	S2600	"6000000003492005116"
#   P3373 sibling = Q141162040 Samuel Eivindsen Garborg
Q467497	P3373	Q141162040	S2600	"6000000003492005116"
#   P3373 sibling = Q141162041 Even Eivindson Garborg
Q467497	P3373	Q141162041	S2600	"6000000003492005116"
#   P26 spouse = Q3143008 Karen Hulda Bergersen
Q467497	P26	Q3143008	S2600	"6000000003492005116"
#   Q141152600 Stine Stena Eivindsdatter Garborg: P40 child = Q141168794 Betsy Jacobson
Q141152600	P40	Q141168794	S2600	"6000000003492005121"
#   P735 given name = Q20022872 Stine, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141152600	P735	Q20022872	P1545	"1"	P7452	Q3409033
#   P734 family name = Q30250555 Garborg
Q141152600	P734	Q30250555
#   set the ja label to "スティーネ・ステーナ・エイヴィンスダッテル・ガルボルグ"
Q141152600	Lja	"スティーネ・ステーナ・エイヴィンスダッテル・ガルボルグ"
#   set the zh label to "斯蒂内·斯泰娜·埃温斯达特·加尔博格"
Q141152600	Lzh	"斯蒂内·斯泰娜·埃温斯达特·加尔博格"
#   Q141152614 Jon Eivindson Garborg: P40 child = Q141168811 Eivind Garborg
Q141152614	P40	Q141168811	S2600	"6000000003492005126"
#   P40 child = Q141168792 Astrid Garborg
Q141152614	P40	Q141168792	S2600	"6000000003492005126"
#   P40 child = Q141168837 Ingebret Garborg
Q141152614	P40	Q141168837	S2600	"6000000003492005126"
#   P40 child = Q141168830 Ingeborg Garborg
Q141152614	P40	Q141168830	S2600	"6000000003492005126"
#   P40 child = Q141168954 Jon Garborg
Q141152614	P40	Q141168954	S2600	"6000000003492005126"
#   P40 child = Q141168784 Aagot Garborg
Q141152614	P40	Q141168784	S2600	"6000000003492005126"
#   P735 given name = Q13501137 Jon
Q141152614	P735	Q13501137
#   P734 family name = Q30250555 Garborg
Q141152614	P734	Q30250555
#   set the ja label to "ヨン・エイヴィンソン・ガルボルグ"
Q141152614	Lja	"ヨン・エイヴィンソン・ガルボルグ"
#   set the zh label to "永·埃温松·加尔博格"
Q141152614	Lzh	"永·埃温松·加尔博格"
#   Q141162040 Samuel Eivindsen Garborg: P735 given name = Q629347 Samuel
Q141162040	P735	Q629347
#   P734 family name = Q30250555 Garborg
Q141162040	P734	Q30250555
#   set the ja label to "サムエル・エイヴィンセン・ガルボルグ"
Q141162040	Lja	"サムエル・エイヴィンセン・ガルボルグ"
#   set the zh label to "萨穆埃尔·埃温森·加尔博格"
Q141162040	Lzh	"萨穆埃尔·埃温森·加尔博格"
#   Q141162041 Even Eivindson Garborg: P735 given name = Q4567129 Even
Q141162041	P735	Q4567129
#   P734 family name = Q30250555 Garborg
Q141162041	P734	Q30250555
#   set the ja label to "エーヴェン・エイヴィンソン・ガルボルグ"
Q141162041	Lja	"エーヴェン・エイヴィンソン・ガルボルグ"
#   set the zh label to "埃文·埃温松·加尔博格"
Q141162041	Lzh	"埃文·埃温松·加尔博格"
#   Q141162043 Inger Marie Mary Eivindsdatter Garborg: P40 child = Q141168820 Eliza Ronneberg
Q141162043	P40	Q141168820	S2600	"6000000003492005141"
#   P40 child = Q141168789 Arnold Ronneberg
Q141162043	P40	Q141168789	S2600	"6000000003492005141"
#   P40 child = Q141168805 Edward Ronneberg
Q141162043	P40	Q141168805	S2600	"6000000003492005141"
#   P40 child = Q141168786 Alice Ronneberg
Q141162043	P40	Q141168786	S2600	"6000000003492005141"
#   P40 child = Q141168824 Ernest Anton Ronneberg
Q141162043	P40	Q141168824	S2600	"6000000003492005141"
#   P735 given name = Q3358452 Inger, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141162043	P735	Q3358452	P1545	"1"	P7452	Q3409033
#   P735 given name = Q106674406 Marie, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141162043	P735	Q106674406	P1545	"2"	P3831	Q245025
#   P734 family name = Q30250555 Garborg
Q141162043	P734	Q30250555
#   set the ja label to "インゲル・マリー・メアリー・エイヴィンスダッテル・ガルボルグ"
Q141162043	Lja	"インゲル・マリー・メアリー・エイヴィンスダッテル・ガルボルグ"
#   set the zh label to "英厄尔·玛丽·玛丽·埃温斯达特·加尔博格"
Q141162043	Lzh	"英厄尔·玛丽·玛丽·埃温斯达特·加尔博格"
#   Q141162044 Abel Eivindsen Garborg: P735 given name = Q318375 Abel
Q141162044	P735	Q318375
#   P734 family name = Q30250555 Garborg
Q141162044	P734	Q30250555
#   set the ja label to "アーベル・エイヴィンセン・ガルボルグ"
Q141162044	Lja	"アーベル・エイヴィンセン・ガルボルグ"
#   set the zh label to "阿贝尔·埃温森·加尔博格"
Q141162044	Lzh	"阿贝尔·埃温森·加尔博格"
#   Q141162045 Ole Eivindsen Garborg: P735 given name = Q2097883 Ole
Q141162045	P735	Q2097883
#   P734 family name = Q30250555 Garborg
Q141162045	P734	Q30250555
#   set the ja label to "オーレ・エイヴィンセン・ガルボルグ"
Q141162045	Lja	"オーレ・エイヴィンセン・ガルボルグ"
#   set the zh label to "奥勒·埃温森·加尔博格"
Q141162045	Lzh	"奥勒·埃温森·加尔博格"
#   Q141162046 Ane Oline Lena Eivindsdatter Garborg: P40 child = Q141169062 Thoralf Tunheim
Q141162046	P40	Q141169062	S2600	"6000000003492005156"
#   P40 child = Q141168801 Cora Estelle Tunheim
Q141162046	P40	Q141168801	S2600	"6000000003492005156"
#   P40 child = Q141168809 Edward Tunheim
Q141162046	P40	Q141168809	S2600	"6000000003492005156"
#   P40 child = Q141168787 Alma Matilda Tunheim
Q141162046	P40	Q141168787	S2600	"6000000003492005156"
#   P40 child = Q141169041 Olaf Tunheim
Q141162046	P40	Q141169041	S2600	"6000000003492005156"
#   P40 child = Q141168788 Arne Garborg Tunheim
Q141162046	P40	Q141168788	S2600	"6000000003492005156"
#   P735 given name = Q11958077 Ane, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141162046	P735	Q11958077	P1545	"1"	P7452	Q3409033
#   P735 given name = Q11993741 Oline, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141162046	P735	Q11993741	P1545	"2"	P3831	Q245025
#   P734 family name = Q30250555 Garborg
Q141162046	P734	Q30250555
#   set the ja label to "アーネ・オリーネ・レーナ・エイヴィンスダッテル・ガルボルグ"
Q141162046	Lja	"アーネ・オリーネ・レーナ・エイヴィンスダッテル・ガルボルグ"
#   set the zh label to "安内·奥利内·莱娜·埃温斯达特·加尔博格"
Q141162046	Lzh	"安内·奥利内·莱娜·埃温斯达特·加尔博格"
#   Q141169072 Ådne Olsen Grøtheim: P40 child = Q141152512 Eivind Aadnesson Garborg
Q141169072	P40	Q141152512	S2600	"6000000003492005161"
#   P40 child = Q141168833 Ingeborg Gurie Ådnesdatter Garborg
Q141169072	P40	Q141168833	S2600	"6000000003492005161"
#   P40 child = Q141168816 Elisabet Ådnesdatter Garborg
Q141169072	P40	Q141168816	S2600	"6000000003492005161"
#   P26 spouse = Q141178202 Stine Persdatter Øksnevad
Q141169072	P26	Q141178202	S2600	"6000000003492005161"
#   set the ja label to "オードネ・オルセン・グレートヘイム"
Q141169072	Lja	"オードネ・オルセン・グレートヘイム"
#   set the zh label to "奥德内·奥尔森·格勒特海姆"
Q141169072	Lzh	"奥德内·奥尔森·格勒特海姆"
#   Q141178202 Stine Persdatter Øksnevad: P40 child = Q141152512 Eivind Aadnesson Garborg
Q141178202	P40	Q141152512	S2600	"6000000003492005166"
#   P40 child = Q141168833 Ingeborg Gurie Ådnesdatter Garborg
Q141178202	P40	Q141168833	S2600	"6000000003492005166"
#   P40 child = Q141168816 Elisabet Ådnesdatter Garborg
Q141178202	P40	Q141168816	S2600	"6000000003492005166"
#   P26 spouse = Q141169072 Ådne Olsen Grøtheim
Q141178202	P26	Q141169072	S2600	"6000000003492005166"
#   P735 given name = Q20022872 Stine
Q141178202	P735	Q20022872
#   P734 family name = Q30583490 Øksnevad
Q141178202	P734	Q30583490
#   set the ja label to "スティーネ・ペシュダッテル・エクスネヴァード"
Q141178202	Lja	"スティーネ・ペシュダッテル・エクスネヴァード"
#   set the zh label to "斯蒂内·佩斯达特·厄克斯内瓦"
Q141178202	Lzh	"斯蒂内·佩斯达特·厄克斯内瓦"
#   Q141168833 Ingeborg Gurie Ådnesdatter Garborg: P22 father = Q141169072 Ådne Olsen Grøtheim
Q141168833	P22	Q141169072	S2600	"6000000003492005171"
#   P25 mother = Q141178202 Stine Persdatter Øksnevad
Q141168833	P25	Q141178202	S2600	"6000000003492005171"
#   P735 given name = Q656590 Ingeborg, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141168833	P735	Q656590	P1545	"1"	P7452	Q3409033
#   P734 family name = Q30250555 Garborg
Q141168833	P734	Q30250555
#   set the ja label to "インゲボルグ・グーリエ・オードネスダッテル・ガルボルグ"
Q141168833	Lja	"インゲボルグ・グーリエ・オードネスダッテル・ガルボルグ"
#   set the zh label to "英厄堡·古里·奥德内斯达特·加尔博格"
Q141168833	Lzh	"英厄堡·古里·奥德内斯达特·加尔博格"
#   Q141168816 Elisabet Ådnesdatter Garborg: P22 father = Q141169072 Ådne Olsen Grøtheim
Q141168816	P22	Q141169072	S2600	"6000000003492005176"
#   P25 mother = Q141178202 Stine Persdatter Øksnevad
Q141168816	P25	Q141178202	S2600	"6000000003492005176"
#   P735 given name = Q16423275 Elisabet
Q141168816	P735	Q16423275
#   P734 family name = Q30250555 Garborg
Q141168816	P734	Q30250555
#   set the ja label to "エリサベート・オードネスダッテル・ガルボルグ"
Q141168816	Lja	"エリサベート・オードネスダッテル・ガルボルグ"
#   set the zh label to "伊丽莎白·奥德内斯达特·加尔博格"
Q141168816	Lzh	"伊丽莎白·奥德内斯达特·加尔博格"
#   Q141168955 Jon Samuelsen Raustad: P22 father = Q141178380 Samuel Jonson Raustad
Q141168955	P22	Q141178380	S2600	"6000000003732742137"
#   P25 mother = Q141178381 Marta Jonsdatter Li
Q141168955	P25	Q141178381	S2600	"6000000003732742137"
#   P40 child = Q141152523 Ane Oline Jonsdatter Raugstad
Q141168955	P40	Q141152523	S2600	"6000000003732742137"
#   P40 child = Q141169046 Samuel Jonson
Q141168955	P40	Q141169046	S2600	"6000000003732742137"
#   P26 spouse = Q141178200 Inger Kristoffersdatter
Q141168955	P26	Q141178200	S2600	"6000000003732742137"
#   P735 given name = Q13501137 Jon
Q141168955	P735	Q13501137
#   set the ja label to "ヨン・サムエルセン・ラウスタード"
Q141168955	Lja	"ヨン・サムエルセン・ラウスタード"
#   set the zh label to "永·萨穆埃尔森·劳斯塔"
Q141168955	Lzh	"永·萨穆埃尔森·劳斯塔"
#   Q633094 Johannes Tomasson: P22 father = Q141180413 Thomas Mattsson
Q633094	P22	Q141180413	S2600	"6000000004334763223"
#   P25 mother = Q141180409 Magdalena Andersdotter Bure
Q633094	P25	Q141180409	S2600	"6000000004334763223"
#   P26 spouse = Q141180410 Margareta Mårtensdotter Bång
Q633094	P26	Q141180410	S2600	"6000000004334763223"
#   P26 spouse = Q141180406 Ingeborg Gyntesdotter
Q633094	P26	Q141180406	S2600	"6000000004334763223"
#   set the zh label to "约翰内斯·托马松"
Q633094	Lzh	"约翰内斯·托马松"
#   Q141180413 Thomas Mattsson: P40 child = Q633094 Johannes Tomasson
Q141180413	P40	Q633094	S2600	"6000000004334768506"
#   P26 spouse = Q141180409 Magdalena Andersdotter Bure
Q141180413	P26	Q141180409	S2600	"6000000004334768506"
#   set the ja label to "トーマス・マットソン"
Q141180413	Lja	"トーマス・マットソン"
#   set the zh label to "托马斯·马特松"
Q141180413	Lzh	"托马斯·马特松"
#   Q141178149 Anna Fartegnsdatter Seim: P734 family name = Q30088373 Seim
Q141178149	P734	Q30088373
#   set the ja label to "アンナ・ファルテグンスダッテル・セイム"
Q141178149	Lja	"アンナ・ファルテグンスダッテル・セイム"
#   set the zh label to "安娜·法尔特格恩斯达特·塞姆"
Q141178149	Lzh	"安娜·法尔特格恩斯达特·塞姆"
#   Q3143008 Karen Hulda Bergersen: P22 father = Q141168797 Christian Frederik Bergersen
Q3143008	P22	Q141168797	S2600	"6000000005606976813"
#   P25 mother = Q141178201 Marie Petrine Simensdatter Bergersen
Q3143008	P25	Q141178201	S2600	"6000000005606976813"
#   P40 child = Q11959067 Arne Olaus Fjørtoft Garborg
Q3143008	P40	Q11959067	S2600	"6000000005606976813"
#   P26 spouse = Q467497 Aadne Eivindson Garborg
Q3143008	P26	Q467497	S2600	"6000000005606976813"
#   Q11959067 Arne Olaus Fjørtoft Garborg: P40 child = Q141168827 Hans Eivind Garborg
Q11959067	P40	Q141168827	S2600	"6000000005607426327"
#   P26 spouse = Q141168785 Aagot Nyvold
Q11959067	P26	Q141168785	S2600	"6000000005607426327"
#   P26 spouse = Q141168803 Dagny Nyvold
Q11959067	P26	Q141168803	S2600	"6000000005607426327"
#   set the ja label to "アルネ・オーラウス・フョルトフト・ガルボルグ"
Q11959067	Lja	"アルネ・オーラウス・フョルトフト・ガルボルグ"
#   set the zh label to "阿尔内·奥劳斯·夫约托夫特·加尔博格"
Q11959067	Lzh	"阿尔内·奥劳斯·夫约托夫特·加尔博格"
#   Q141168827 Hans Eivind Garborg: P22 father = Q11959067 Arne Olaus Fjørtoft Garborg
Q141168827	P22	Q11959067	S2600	"6000000005607426344"
#   P25 mother = Q141168785 Aagot Nyvold
Q141168827	P25	Q141168785	S2600	"6000000005607426344"
#   P735 given name = Q3358418 Eivind, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141168827	P735	Q3358418	P1545	"2"	P3831	Q245025
#   P734 family name = Q30250555 Garborg
Q141168827	P734	Q30250555
#   set the ja label to "ハンス・エイヴィン・ガルボルグ"
Q141168827	Lja	"ハンス・エイヴィン・ガルボルグ"
#   set the zh label to "汉斯·埃温·加尔博格"
Q141168827	Lzh	"汉斯·埃温·加尔博格"
#   Q141178200 Inger Kristoffersdatter: P40 child = Q141152523 Ane Oline Jonsdatter Raugstad
Q141178200	P40	Q141152523	S2600	"6000000005609534511"
#   P40 child = Q141169046 Samuel Jonson
Q141178200	P40	Q141169046	S2600	"6000000005609534511"
#   P26 spouse = Q141168955 Jon Samuelsen Raustad
Q141178200	P26	Q141168955	S2600	"6000000005609534511"
#   P735 given name = Q3358452 Inger
Q141178200	P735	Q3358452
#   set the ja label to "インゲル・クリストッフェシュダッテル"
Q141178200	Lja	"インゲル・クリストッフェシュダッテル"
#   set the zh label to "英厄尔·克里斯托弗斯达特"
Q141178200	Lzh	"英厄尔·克里斯托弗斯达特"
#   Q141180408 Jon Larsson Li: P40 child = Q141178381 Marta Jonsdatter Li
Q141180408	P40	Q141178381	S2600	"6000000005609534542"
#   P26 spouse = Q141180412 Marta Rasmusdatter Høle
Q141180408	P26	Q141180412	S2600	"6000000005609534542"
#   P735 given name = Q13501137 Jon
Q141180408	P735	Q13501137
#   set the ja label to "ヨン・ラーション・リ"
Q141180408	Lja	"ヨン・ラーション・リ"
#   set the zh label to "永·拉尔松·李"
Q141180408	Lzh	"永·拉尔松·李"
#   Q141180412 Marta Rasmusdatter Høle: P40 child = Q141178381 Marta Jonsdatter Li
Q141180412	P40	Q141178381	S2600	"6000000005609534550"
#   P26 spouse = Q141180408 Jon Larsson Li
Q141180412	P26	Q141180408	S2600	"6000000005609534550"
#   P735 given name = Q846741 Marta
Q141180412	P735	Q846741
#   set the ja label to "マルタ・ラスムスダッテル・ヘーレ"
Q141180412	Lja	"マルタ・ラスムスダッテル・ヘーレ"
#   set the zh label to "玛尔塔·拉斯穆斯达特·赫勒"
Q141180412	Lzh	"玛尔塔·拉斯穆斯达特·赫勒"
#   Q141180409 Magdalena Andersdotter Bure: P40 child = Q633094 Johannes Tomasson
Q141180409	P40	Q633094	S2600	"6000000006127859575"
#   P26 spouse = Q141180413 Thomas Mattsson
Q141180409	P26	Q141180413	S2600	"6000000006127859575"
#   P735 given name = Q842544 Magdalena, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141180409	P735	Q842544	P1545	"1"	P7452	Q3409033
#   set the ja label to "マグダレーナ・アンデシュドッテル・ブーレ"
Q141180409	Lja	"マグダレーナ・アンデシュドッテル・ブーレ"
#   set the zh label to "玛格达莱娜·安德斯多特·布雷"
Q141180409	Lzh	"玛格达莱娜·安德斯多特·布雷"
#   Q141168811 Eivind Garborg: P22 father = Q141152614 Jon Eivindson Garborg
Q141168811	P22	Q141152614	S2600	"6000000006570861816"
#   P735 given name = Q3358418 Eivind
Q141168811	P735	Q3358418
#   P734 family name = Q30250555 Garborg
Q141168811	P734	Q30250555
#   set the ja label to "エイヴィン・ガルボルグ"
Q141168811	Lja	"エイヴィン・ガルボルグ"
#   set the zh label to "埃温·加尔博格"
Q141168811	Lzh	"埃温·加尔博格"
#   Q141168792 Astrid Garborg: P22 father = Q141152614 Jon Eivindson Garborg
Q141168792	P22	Q141152614	S2600	"6000000006572523374"
#   P735 given name = Q167755 Astrid
Q141168792	P735	Q167755
#   P734 family name = Q30250555 Garborg
Q141168792	P734	Q30250555
#   set the ja label to "アストリッド・ガルボルグ"
Q141168792	Lja	"アストリッド・ガルボルグ"
#   set the zh label to "阿斯特丽德·加尔博格"
Q141168792	Lzh	"阿斯特丽德·加尔博格"
#   Q141168837 Ingebret Garborg: P22 father = Q141152614 Jon Eivindson Garborg
Q141168837	P22	Q141152614	S2600	"6000000006572799149"
#   P735 given name = Q30229695 Ingebret
Q141168837	P735	Q30229695
#   P734 family name = Q30250555 Garborg
Q141168837	P734	Q30250555
#   set the ja label to "インゲブレート・ガルボルグ"
Q141168837	Lja	"インゲブレート・ガルボルグ"
#   set the zh label to "英厄布雷特·加尔博格"
Q141168837	Lzh	"英厄布雷特·加尔博格"
#   Q141168830 Ingeborg Garborg: P22 father = Q141152614 Jon Eivindson Garborg
Q141168830	P22	Q141152614	S2600	"6000000006573130134"
#   P735 given name = Q656590 Ingeborg
Q141168830	P735	Q656590
#   P734 family name = Q30250555 Garborg
Q141168830	P734	Q30250555
#   set the ja label to "インゲボルグ・ガルボルグ"
Q141168830	Lja	"インゲボルグ・ガルボルグ"
#   set the zh label to "英厄堡·加尔博格"
Q141168830	Lzh	"英厄堡·加尔博格"
#   Q141168954 Jon Garborg: P22 father = Q141152614 Jon Eivindson Garborg
Q141168954	P22	Q141152614	S2600	"6000000006573294012"
#   P735 given name = Q13501137 Jon
Q141168954	P735	Q13501137
#   P734 family name = Q30250555 Garborg
Q141168954	P734	Q30250555
#   set the ja label to "ヨン・ガルボルグ"
Q141168954	Lja	"ヨン・ガルボルグ"
#   set the zh label to "永·加尔博格"
Q141168954	Lzh	"永·加尔博格"
#   Q141178201 Marie Petrine Simensdatter Bergersen: P40 child = Q3143008 Karen Hulda Bergersen
Q141178201	P40	Q3143008	S2600	"6000000009126235990"
#   P26 spouse = Q141168797 Christian Frederik Bergersen
Q141178201	P26	Q141168797	S2600	"6000000009126235990"
#   P735 given name = Q106674406 Marie, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141178201	P735	Q106674406	P1545	"1"	P7452	Q3409033
#   P735 given name = Q107227465 Petrine, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141178201	P735	Q107227465	P1545	"2"	P3831	Q245025
#   set the ja label to "マリー・ペトリーネ・シメンスダッテル・ベルゲルセン"
Q141178201	Lja	"マリー・ペトリーネ・シメンスダッテル・ベルゲルセン"
#   set the zh label to "玛丽·佩特里内·西门斯达特·贝格尔森"
Q141178201	Lzh	"玛丽·佩特里内·西门斯达特·贝格尔森"
#   Q141168797 Christian Frederik Bergersen: P22 father = Q141178199 Gunder Bergersen
Q141168797	P22	Q141178199	S2600	"6000000009126453497"
#   P25 mother = Q141180395 Maren Gulbrandsdatter Ommestad
Q141168797	P25	Q141180395	S2600	"6000000009126453497"
#   P40 child = Q3143008 Karen Hulda Bergersen
Q141168797	P40	Q3143008	S2600	"6000000009126453497"
#   P26 spouse = Q141178201 Marie Petrine Simensdatter Bergersen
Q141168797	P26	Q141178201	S2600	"6000000009126453497"
#   P735 given name = Q18001597 Christian, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141168797	P735	Q18001597	P1545	"1"	P7452	Q3409033
#   P735 given name = Q17539077 Frederik, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141168797	P735	Q17539077	P1545	"2"	P3831	Q245025
#   set the ja label to "クリスチャン・フレデリク・ベルゲルセン"
Q141168797	Lja	"クリスチャン・フレデリク・ベルゲルセン"
#   set the zh label to "克里斯蒂安·弗雷德里克·贝格尔森"
Q141168797	Lzh	"克里斯蒂安·弗雷德里克·贝格尔森"
#   Q101247444 Ingegerd Svantepolksdotter: set the ja label to "インゲゲルド・スヴァンテポルクスドッテル"
Q101247444	Lja	"インゲゲルド・スヴァンテポルクスドッテル"
#   set the zh label to "英格格德·斯万特波尔克斯多特"
Q101247444	Lzh	"英格格德·斯万特波尔克斯多特"
#   Q141180410 Margareta Mårtensdotter Bång: P26 spouse = Q633094 Johannes Tomasson
Q141180410	P26	Q633094	S2600	"6000000012566410426"
#   P735 given name = Q8274988 Margareta, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141180410	P735	Q8274988	P1545	"1"	P7452	Q3409033
#   set the ja label to "マルガレータ・モーテンスドッテル・ボング"
Q141180410	Lja	"マルガレータ・モーテンスドッテル・ボング"
#   set the zh label to "玛格丽塔·莫滕斯多特·邦格"
Q141180410	Lzh	"玛格丽塔·莫滕斯多特·邦格"
#   Q141178199 Gunder Bergersen: P40 child = Q141168797 Christian Frederik Bergersen
Q141178199	P40	Q141168797	S2600	"6000000016756402733"
#   P26 spouse = Q141180395 Maren Gulbrandsdatter Ommestad
Q141178199	P26	Q141180395	S2600	"6000000016756402733"
#   P735 given name = Q989832 Gunder
Q141178199	P735	Q989832
#   set the ja label to "グンデル・ベルゲルセン"
Q141178199	Lja	"グンデル・ベルゲルセン"
#   set the zh label to "贡德尔·贝格尔森"
Q141178199	Lzh	"贡德尔·贝格尔森"
#   Q141180395 Maren Gulbrandsdatter Ommestad: P40 child = Q141168797 Christian Frederik Bergersen
Q141180395	P40	Q141168797	S2600	"6000000020221673906"
#   P26 spouse = Q141178199 Gunder Bergersen
Q141180395	P26	Q141178199	S2600	"6000000020221673906"
#   P735 given name = Q1666203 Maren
Q141180395	P735	Q1666203
#   set the ja label to "マーレン・グルブランスダッテル・オンメスタード"
Q141180395	Lja	"マーレン・グルブランスダッテル・オンメスタード"
#   set the zh label to "马伦·古尔布兰斯达特·翁梅斯塔德"
Q141180395	Lzh	"马伦·古尔布兰斯达特·翁梅斯塔德"
#   Q141168784 Aagot Garborg: P22 father = Q141152614 Jon Eivindson Garborg
Q141168784	P22	Q141152614	S2600	"6000000021079935250"
#   P735 given name = Q3482557 Aagot
Q141168784	P735	Q3482557
#   P734 family name = Q30250555 Garborg
Q141168784	P734	Q30250555
#   set the ja label to "オーゴット・ガルボルグ"
Q141168784	Lja	"オーゴット・ガルボルグ"
#   set the zh label to "奥高特·加尔博格"
Q141168784	Lzh	"奥高特·加尔博格"
#   Q138474188 Hans Syvertsen Nyvold: P40 child = Q141168785 Aagot Nyvold
Q138474188	P40	Q141168785	S2600	"6000000021197598122"
#   P40 child = Q141168803 Dagny Nyvold
Q138474188	P40	Q141168803	S2600	"6000000021197598122"
#   P26 spouse = Q141178197 Elisabeth Johannesen
Q138474188	P26	Q141178197	S2600	"6000000021197598122"
#   set the ja label to "ハンス・シーヴェシェン・ニーヴォル"
Q138474188	Lja	"ハンス・シーヴェシェン・ニーヴォル"
#   set the zh label to "汉斯·西韦特森·尼沃尔"
Q138474188	Lzh	"汉斯·西韦特森·尼沃尔"
#   Q141168785 Aagot Nyvold: P22 father = Q138474188 Hans Syvertsen Nyvold
Q141168785	P22	Q138474188	S2600	"6000000021197722738"
#   P25 mother = Q141178197 Elisabeth Johannesen
Q141168785	P25	Q141178197	S2600	"6000000021197722738"
#   P40 child = Q141168827 Hans Eivind Garborg
Q141168785	P40	Q141168827	S2600	"6000000021197722738"
#   P26 spouse = Q11959067 Arne Olaus Fjørtoft Garborg
Q141168785	P26	Q11959067	S2600	"6000000021197722738"
#   P735 given name = Q3482557 Aagot
Q141168785	P735	Q3482557
#   set the ja label to "オーゴット・ニーヴォル"
Q141168785	Lja	"オーゴット・ニーヴォル"
#   set the zh label to "奥高特·尼沃尔"
Q141168785	Lzh	"奥高特·尼沃尔"
#   Q141168803 Dagny Nyvold: P22 father = Q138474188 Hans Syvertsen Nyvold
Q141168803	P22	Q138474188	S2600	"6000000021197841042"
#   P25 mother = Q141178197 Elisabeth Johannesen
Q141168803	P25	Q141178197	S2600	"6000000021197841042"
#   P26 spouse = Q11959067 Arne Olaus Fjørtoft Garborg
Q141168803	P26	Q11959067	S2600	"6000000021197841042"
#   P735 given name = Q1157346 Dagny
Q141168803	P735	Q1157346
#   set the ja label to "ダグニー・ニーヴォル"
Q141168803	Lja	"ダグニー・ニーヴォル"
#   set the zh label to "达格妮·尼沃尔"
Q141168803	Lzh	"达格妮·尼沃尔"
#   Q141178197 Elisabeth Johannesen: P40 child = Q141168785 Aagot Nyvold
Q141178197	P40	Q141168785	S2600	"6000000021198042859"
#   P40 child = Q141168803 Dagny Nyvold
Q141178197	P40	Q141168803	S2600	"6000000021198042859"
#   P26 spouse = Q138474188 Hans Syvertsen Nyvold
Q141178197	P26	Q138474188	S2600	"6000000021198042859"
#   P735 given name = Q63611044 Elisabeth
Q141178197	P735	Q63611044
#   set the ja label to "エリーサベト・ヨハンネセン"
Q141178197	Lja	"エリーサベト・ヨハンネセン"
#   set the zh label to "伊丽莎白·约翰内森"
Q141178197	Lzh	"伊丽莎白·约翰内森"
#   Q141180406 Ingeborg Gyntesdotter: P26 spouse = Q633094 Johannes Tomasson
Q141180406	P26	Q633094	S2600	"6000000027324391291"
#   P735 given name = Q656590 Ingeborg
Q141180406	P735	Q656590
#   set the ja label to "インゲボルグ・ギュンテスドッテル"
Q141180406	Lja	"インゲボルグ・ギュンテスドッテル"
#   set the zh label to "英厄堡·金特斯多特"
Q141180406	Lzh	"英厄堡·金特斯多特"
#   Q141169062 Thoralf Tunheim: P25 mother = Q141162046 Ane Oline Lena Eivindsdatter Garborg
Q141169062	P25	Q141162046	S2600	"6000000033773881611"
#   set the ja label to "トーラルフ・トゥンヘイム"
Q141169062	Lja	"トーラルフ・トゥンヘイム"
#   set the zh label to "托拉尔夫·通海姆"
Q141169062	Lzh	"托拉尔夫·通海姆"
#   Q141168801 Cora Estelle Tunheim: P25 mother = Q141162046 Ane Oline Lena Eivindsdatter Garborg
Q141168801	P25	Q141162046	S2600	"6000000033773908408"
#   P735 given name = Q714938 Cora, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141168801	P735	Q714938	P1545	"1"	P7452	Q3409033
#   P735 given name = Q744012 Estelle, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141168801	P735	Q744012	P1545	"2"	P3831	Q245025
#   set the ja label to "コーラ・エステル・トゥンヘイム"
Q141168801	Lja	"コーラ・エステル・トゥンヘイム"
#   set the zh label to "科拉·埃斯特尔·通海姆"
Q141168801	Lzh	"科拉·埃斯特尔·通海姆"
#   Q141168809 Edward Tunheim: P25 mother = Q141162046 Ane Oline Lena Eivindsdatter Garborg
Q141168809	P25	Q141162046	S2600	"6000000033773925586"
#   P735 given name = Q278835 Edward
Q141168809	P735	Q278835
#   set the ja label to "エドワード・トゥンヘイム"
Q141168809	Lja	"エドワード・トゥンヘイム"
#   set the zh label to "爱德华·通海姆"
Q141168809	Lzh	"爱德华·通海姆"
#   Q141168787 Alma Matilda Tunheim: P25 mother = Q141162046 Ane Oline Lena Eivindsdatter Garborg
Q141168787	P25	Q141162046	S2600	"6000000033774070464"
#   P735 given name = Q656870 Alma, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141168787	P735	Q656870	P1545	"1"	P7452	Q3409033
#   P735 given name = Q2054021 Matilda, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141168787	P735	Q2054021	P1545	"2"	P3831	Q245025
#   set the ja label to "アルマ・マチルダ・トゥンヘイム"
Q141168787	Lja	"アルマ・マチルダ・トゥンヘイム"
#   set the zh label to "阿尔玛·玛蒂尔达·通海姆"
Q141168787	Lzh	"阿尔玛·玛蒂尔达·通海姆"
#   Q141169041 Olaf Tunheim: P25 mother = Q141162046 Ane Oline Lena Eivindsdatter Garborg
Q141169041	P25	Q141162046	S2600	"6000000033774204088"
#   P735 given name = Q3881452 Olaf
Q141169041	P735	Q3881452
#   set the ja label to "オーラフ・トゥンヘイム"
Q141169041	Lja	"オーラフ・トゥンヘイム"
#   set the zh label to "奥拉夫·通海姆"
Q141169041	Lzh	"奥拉夫·通海姆"
#   Q4953376 Helena Guttormsdatter: P40 child = Q3743799 Knut Valdemarsson Duke of Estland, Blekinge and Lolland
Q4953376	P40	Q3743799	S2600	"6000000034013672054"
#   set the ja label to "ヘレナ・グットルムスダッテル"
Q4953376	Lja	"ヘレナ・グットルムスダッテル"
#   set the zh label to "海伦娜·古托尔姆斯达特"
Q4953376	Lzh	"海伦娜·古托尔姆斯达特"
#   Q141168820 Eliza Ronneberg: P25 mother = Q141162043 Inger Marie Mary Eivindsdatter Garborg
Q141168820	P25	Q141162043	S2600	"6000000035698428095"
#   P735 given name = Q858305 Eliza
Q141168820	P735	Q858305
#   set the ja label to "エリザ・ロンネベルグ"
Q141168820	Lja	"エリザ・ロンネベルグ"
#   set the zh label to "伊莱扎·龙内贝格"
Q141168820	Lzh	"伊莱扎·龙内贝格"
#   Q141168789 Arnold Ronneberg: P25 mother = Q141162043 Inger Marie Mary Eivindsdatter Garborg
Q141168789	P25	Q141162043	S2600	"6000000035698494074"
#   P735 given name = Q3623461 Arnold
Q141168789	P735	Q3623461
#   set the ja label to "アルノルド・ロンネベルグ"
Q141168789	Lja	"アルノルド・ロンネベルグ"
#   set the zh label to "阿诺德·龙内贝格"
Q141168789	Lzh	"阿诺德·龙内贝格"
#   Q141168805 Edward Ronneberg: P25 mother = Q141162043 Inger Marie Mary Eivindsdatter Garborg
Q141168805	P25	Q141162043	S2600	"6000000035698546990"
#   P735 given name = Q278835 Edward
Q141168805	P735	Q278835
#   set the ja label to "エドワード・ロンネベルグ"
Q141168805	Lja	"エドワード・ロンネベルグ"
#   set the zh label to "爱德华·龙内贝格"
Q141168805	Lzh	"爱德华·龙内贝格"
#   Q141168786 Alice Ronneberg: P25 mother = Q141162043 Inger Marie Mary Eivindsdatter Garborg
Q141168786	P25	Q141162043	S2600	"6000000035698611873"
#   P735 given name = Q650689 Alice
Q141168786	P735	Q650689
#   set the ja label to "アリス・ロンネベルグ"
Q141168786	Lja	"アリス・ロンネベルグ"
#   set the zh label to "艾丽丝·龙内贝格"
Q141168786	Lzh	"艾丽丝·龙内贝格"
#   Q141168824 Ernest Anton Ronneberg: P25 mother = Q141162043 Inger Marie Mary Eivindsdatter Garborg
Q141168824	P25	Q141162043	S2600	"6000000035698619913"
#   P735 given name = Q5401576 Anton, qualified series ordinal 2, object of statement has role Q245025 middle name
Q141168824	P735	Q5401576	P1545	"2"	P3831	Q245025
#   set the ja label to "アーネスト・アントン・ロンネベルグ"
Q141168824	Lja	"アーネスト・アントン・ロンネベルグ"
#   set the zh label to "欧内斯特·安东·龙内贝格"
Q141168824	Lzh	"欧内斯特·安东·龙内贝格"
#   Q141168788 Arne Garborg Tunheim: P25 mother = Q141162046 Ane Oline Lena Eivindsdatter Garborg
Q141168788	P25	Q141162046	S2600	"6000000037693739967"
#   P735 given name = Q645757 Arne, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
Q141168788	P735	Q645757	P1545	"1"	P7452	Q3409033
#   set the ja label to "アルネ・ガルボルグ・トゥンヘイム"
Q141168788	Lja	"アルネ・ガルボルグ・トゥンヘイム"
#   set the zh label to "阿尔内·加尔博格·通海姆"
Q141168788	Lzh	"阿尔内·加尔博格·通海姆"
#   Q141180396 Tollef Tollefson Tunheim: P26 spouse = Q141168794 Betsy Jacobson
Q141180396	P26	Q141168794	S2600	"6000000037737683245"
#   P735 given name = Q12006598 Tollef
Q141180396	P735	Q12006598
#   set the ja label to "トッレヴ・トレフソン・トゥンヘイム"
Q141180396	Lja	"トッレヴ・トレフソン・トゥンヘイム"
#   set the zh label to "托勒夫·托勒夫松·通海姆"
Q141180396	Lzh	"托勒夫·托勒夫松·通海姆"
#   Q141168794 Betsy Jacobson: P25 mother = Q141152600 Stine Stena Eivindsdatter Garborg
Q141168794	P25	Q141152600	S2600	"6000000037737979829"
#   P26 spouse = Q141180396 Tollef Tollefson Tunheim
Q141168794	P26	Q141180396	S2600	"6000000037737979829"
#   P735 given name = Q832242 Betsy
Q141168794	P735	Q832242
#   set the ja label to "ベッツィ・ヤコブソン"
Q141168794	Lja	"ベッツィ・ヤコブソン"
#   set the zh label to "贝齐·雅各布松"
Q141168794	Lzh	"贝齐·雅各布松"
#   Q140568870 Emma Leonhart: P735 given name = Q541194 Emma
Q140568870	P735	Q541194
#   Q19657284 Buyeo Deokjang: P40 child = Q12598947 Taebi Buyeo
Q19657284	P40	Q12598947	S2600	"6000000186285688253"
#   Q135579480 Yasutaka Kitajima: P22 father = Q135579474 Tokitaka Kitajima
Q135579480	P22	Q135579474	S2600	"6000000227335224861"
#   Q135579474 Tokitaka Kitajima: P40 child = Q135579480 Yasutaka Kitajima
Q135579474	P40	Q135579480	S2600	"6000000227335393824"

