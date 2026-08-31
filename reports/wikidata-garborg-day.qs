# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   773 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   set the ja label to "サミュエル・トロイリウス"
Q1168365	Lja	"サミュエル・トロイリウス"
#   set the zh label to "塞缪尔·特罗伊利乌斯"
Q1168365	Lzh	"塞缪尔·特罗伊利乌斯"
#   Q5779125 Adolf Fredrik Nils Gyldenstolpe: add a mul alias "Adolf Fredrik Nils Gyldenstolpe"
Q5779125	Amul	"Adolf Fredrik Nils Gyldenstolpe"
#   Q6175942 David Wilhelm Silfverstolpe: set the mul label to "David Silfverstolpe"
Q6175942	Lmul	"David Silfverstolpe"
#   add a mul alias "David Wilhelm Silfverstolpe"
Q6175942	Amul	"David Wilhelm Silfverstolpe"
#   set the ja label to "デイヴィッド・シルフヴェルストルペ"
Q6175942	Lja	"デイヴィッド・シルフヴェルストルペ"
#   set the zh label to "大卫·西尔夫韦尔斯托尔佩"
Q6175942	Lzh	"大卫·西尔夫韦尔斯托尔佩"
#   Q5960165 Carolus Nicolai Lithman: add a mul alias "Carolus Nicolai Bothniensis"
Q5960165	Amul	"Carolus Nicolai Bothniensis"
#   set the ja label to "カール・リトマン"
Q5960165	Lja	"カール・リトマン"
#   set the zh label to "卡尔·利特曼"
Q5960165	Lzh	"卡尔·利特曼"
#   Q11858191 Erik Johan Abrahamsson af Palén: add a mul alias "Erik Johan Abrahamsson Palén"
Q11858191	Amul	"Erik Johan Abrahamsson Palén"
#   set the ja label to "エリック・アフ・パレン"
Q11858191	Lja	"エリック・アフ・パレン"
#   set the zh label to "埃里克·阿夫·帕伦"
Q11858191	Lzh	"埃里克·阿夫·帕伦"
#   Q2490612 Johan Graan till Ånsta: set the mul label to "Johan Graan"
Q2490612	Lmul	"Johan Graan"
#   add a mul alias "Johan Gertsson till Ånsta"
Q2490612	Amul	"Johan Gertsson till Ånsta"

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Anna Wilhelmina Nordenfeldt"
LAST	Len	"Anna Wilhelmina Nordenfeldt"
#   set the mul label to "Anna Wilhelmina Nordenfeldt"
LAST	Lmul	"Anna Wilhelmina Nordenfeldt"
#   set the ja label to "アンナ・ウィルヘルミナ・ノルデンフェルドト"
LAST	Lja	"アンナ・ウィルヘルミナ・ノルデンフェルドト"
#   set the zh label to "安娜·维尔赫尔米纳·诺尔登费尔德特"
LAST	Lzh	"安娜·维尔赫尔米纳·诺尔登费尔德特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000001994951163 Anna Wilhelmina Nordenfeldt, qualified P1810 subject named as Friherrinna Anna Wilhelmina Posse af Säby
LAST	P2600	"6000000001994951163"	P1810	"Friherrinna Anna Wilhelmina Posse af Säby"
#   P569 date of birth = +1779-10-28T00:00:00Z/11
LAST	P569	+1779-10-28T00:00:00Z/11	S2600	"6000000001994951163"
#   P570 date of death = +1858-11-21T00:00:00Z/11
LAST	P570	+1858-11-21T00:00:00Z/11	S2600	"6000000001994951163"
#   P40 child = Q6014618 Enar Vilhelm Nordenfelt
LAST	P40	Q6014618	S2600	"6000000001994951163"
#   Q6014618 Enar Vilhelm Nordenfelt: P25 mother = the item just created
Q6014618	P25	LAST	S2600	"6000000001994951163"

# create a new item
CREATE
#   the item just created: set the en label to "Anne Serine Tollefsdotter Tunheim"
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
#   set the en label to "Asbjørn Erikson Røyneberg"
LAST	Len	"Asbjørn Erikson Røyneberg"
#   set the mul label to "Asbjørn Erikson Røyneberg"
LAST	Lmul	"Asbjørn Erikson Røyneberg"
#   set the ja label to "アスブヨルン・エリクソン・ロイネベルグ"
LAST	Lja	"アスブヨルン・エリクソン・ロイネベルグ"
#   set the zh label to "阿斯布约尔恩·埃里克松·罗伊内贝尔格"
LAST	Lzh	"阿斯布约尔恩·埃里克松·罗伊内贝尔格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003491933566 Asbjørn Erikson Røyneberg, qualified P1810 subject named as Asbjørn Erikson Røyneberg
LAST	P2600	"6000000003491933566"	P1810	"Asbjørn Erikson Røyneberg"
#   P569 date of birth = +1693-08-23T00:00:00Z/11
LAST	P569	+1693-08-23T00:00:00Z/11	S2600	"6000000003491933566"
#   P570 date of death = +1765-12-20T00:00:00Z/11
LAST	P570	+1765-12-20T00:00:00Z/11	S2600	"6000000003491933566"
#   P40 child = Q141219299 Per Asbjørnson Stokka
LAST	P40	Q141219299	S2600	"6000000003491933566"
#   Q141219299 Per Asbjørnson Stokka: P22 father = the item just created
Q141219299	P22	LAST	S2600	"6000000003491933566"
#   the item just created: P735 given name = Q721398 Asbjørn
LAST	P735	Q721398
#   add a mul alias "Asbjørn Røyneberg"
LAST	Amul	"Asbjørn Røyneberg"

# create a new item
CREATE
#   set the en label to "Asgjerd Klausdatter Aabø"
LAST	Len	"Asgjerd Klausdatter Aabø"
#   set the mul label to "Asgjerd Klausdatter Aabø"
LAST	Lmul	"Asgjerd Klausdatter Aabø"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000206911240984 Asgjerd Klausdtr. Aabø, qualified P1810 subject named as Asgjerd Klausdtr. Aabø
LAST	P2600	"6000000206911240984"	P1810	"Asgjerd Klausdtr. Aabø"
#   P569 date of birth = +1796-00-00T00:00:00Z/9
LAST	P569	+1796-00-00T00:00:00Z/9	S2600	"6000000206911240984"
#   P570 date of death = +1883-10-26T00:00:00Z/11
LAST	P570	+1883-10-26T00:00:00Z/11	S2600	"6000000206911240984"
#   P40 child = Q141224249 Johannes Jacobsen
LAST	P40	Q141224249	S2600	"6000000206911240984"
#   Q141224249 Johannes Jacobsen: P25 mother = the item just created
Q141224249	P25	LAST	S2600	"6000000206911240984"
#   the item just created: add a mul alias "Asgjerd Klausdtr. Aabø"
LAST	Amul	"Asgjerd Klausdtr. Aabø"

# create a new item
CREATE
#   set the en label to "Bergine Paulsdatter Kleppe"
LAST	Len	"Bergine Paulsdatter Kleppe"
#   set the mul label to "Bergine Paulsdatter Kleppe"
LAST	Lmul	"Bergine Paulsdatter Kleppe"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000013894129541 Bergine Paulsdatter Kleppe, qualified P1810 subject named as Bergine Paulsdatter Kleppe
LAST	P2600	"6000000013894129541"	P1810	"Bergine Paulsdatter Kleppe"
#   P569 date of birth = +1865-02-24T00:00:00Z/11
LAST	P569	+1865-02-24T00:00:00Z/11	S2600	"6000000013894129541"
#   P22 father = Q141224861 Paul Pederson Borsheim
LAST	P22	Q141224861	S2600	"6000000013894129541"
#   P25 mother = Q141224751 Berta Serina Rasmusdatter Borsheim
LAST	P25	Q141224751	S2600	"6000000013894129541"
#   Q141224861 Paul Pederson Borsheim: P40 child = the item just created
Q141224861	P40	LAST	S2600	"6000000013894129541"
#   Q141224751 Berta Serina Rasmusdatter Borsheim: P40 child = the item just created
Q141224751	P40	LAST	S2600	"6000000013894129541"

# create a new item
CREATE
#   the item just created: set the en label to "Bjørn Gunnarson Mele"
LAST	Len	"Bjørn Gunnarson Mele"
#   set the mul label to "Bjørn Gunnarson Mele"
LAST	Lmul	"Bjørn Gunnarson Mele"
#   add a mul alias "Bjørn Gunnarson Gunnarson"
LAST	Amul	"Bjørn Gunnarson Gunnarson"
#   set the ja label to "ビョルン・グナルソン・メーレ"
LAST	Lja	"ビョルン・グナルソン・メーレ"
#   set the zh label to "比约恩·古纳尔松·梅勒"
LAST	Lzh	"比约恩·古纳尔松·梅勒"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 4462693 Bjørn Gunnarson Mele, qualified P1810 subject named as Bjørn Gunnarson Gunnarson
LAST	P2600	"4462693"	P1810	"Bjørn Gunnarson Gunnarson"
#   P569 date of birth = +1577-00-00T00:00:00Z/9
LAST	P569	+1577-00-00T00:00:00Z/9	S2600	"4462693"
#   P570 date of death = +1661-00-00T00:00:00Z/9
LAST	P570	+1661-00-00T00:00:00Z/9	S2600	"4462693"
#   P40 child = Q141198507 Tormod Bjørnson Mele
LAST	P40	Q141198507	S2600	"4462693"
#   Q141198507 Tormod Bjørnson Mele: P22 father = the item just created
Q141198507	P22	LAST	S2600	"4462693"
#   the item just created: P735 given name = Q18918288 Bjørn
LAST	P735	Q18918288
#   add a mul alias "Bjørn Mele"
LAST	Amul	"Bjørn Mele"

# create a new item
CREATE
#   set the en label to "Catharina Ysing"
LAST	Len	"Catharina Ysing"
#   set the mul label to "Catharina Ysing"
LAST	Lmul	"Catharina Ysing"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000007910838142 Catharina Ysing, qualified P1810 subject named as Catharina Ysing
LAST	P2600	"6000000007910838142"	P1810	"Catharina Ysing"
#   P569 date of birth = +1674-00-00T00:00:00Z/9
LAST	P569	+1674-00-00T00:00:00Z/9	S2600	"6000000007910838142"
#   P570 date of death = +1704-00-00T00:00:00Z/9
LAST	P570	+1704-00-00T00:00:00Z/9	S2600	"6000000007910838142"
#   P40 child = Q473225 Georg Brandt
LAST	P40	Q473225	S2600	"6000000007910838142"
#   Q473225 Georg Brandt: P25 mother = the item just created
Q473225	P25	LAST	S2600	"6000000007910838142"
#   the item just created: P735 given name = Q17317997 Catharina
LAST	P735	Q17317997

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
#   set the en label to "Georg Jürgen Brandt"
LAST	Len	"Georg Jürgen Brandt"
#   set the mul label to "Georg Jürgen Brandt"
LAST	Lmul	"Georg Jürgen Brandt"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000007910835508 Georg Jürgen Brandt, qualified P1810 subject named as Georg Jürgen Brandt
LAST	P2600	"6000000007910835508"	P1810	"Georg Jürgen Brandt"
#   P569 date of birth = +1647-08-24T00:00:00Z/11
LAST	P569	+1647-08-24T00:00:00Z/11	S2600	"6000000007910835508"
#   P570 date of death = +1714-03-21T00:00:00Z/11
LAST	P570	+1714-03-21T00:00:00Z/11	S2600	"6000000007910835508"
#   P40 child = Q473225 Georg Brandt
LAST	P40	Q473225	S2600	"6000000007910835508"
#   Q473225 Georg Brandt: P22 father = the item just created
Q473225	P22	LAST	S2600	"6000000007910835508"
#   the item just created: P735 given name = Q1985538 Georg, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q1985538	P1545	"1"	P7452	Q3409033
#   P734 family name = Q11941314 Brandt
LAST	P734	Q11941314

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
#   the item just created: set the en label to "Inger Pedersdatter Stokka"
LAST	Len	"Inger Pedersdatter Stokka"
#   set the mul label to "Inger Pedersdatter Stokka"
LAST	Lmul	"Inger Pedersdatter Stokka"
#   set the ja label to "インゲル・ペーデシュダッテル・ストカ"
LAST	Lja	"インゲル・ペーデシュダッテル・ストカ"
#   set the zh label to "英格·佩德斯达特·斯托卡"
LAST	Lzh	"英格·佩德斯达特·斯托卡"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003491933571 Inger Pedersdatter Stokka, qualified P1810 subject named as Inger Pedersdatter Stokka
LAST	P2600	"6000000003491933571"	P1810	"Inger Pedersdatter Stokka"
#   P569 date of birth = +1703-12-20T00:00:00Z/11
LAST	P569	+1703-12-20T00:00:00Z/11	S2600	"6000000003491933571"
#   P570 date of death = +1754-00-00T00:00:00Z/9
LAST	P570	+1754-00-00T00:00:00Z/9	S2600	"6000000003491933571"
#   P40 child = Q141219299 Per Asbjørnson Stokka
LAST	P40	Q141219299	S2600	"6000000003491933571"
#   Q141219299 Per Asbjørnson Stokka: P25 mother = the item just created
Q141219299	P25	LAST	S2600	"6000000003491933571"
#   the item just created: P735 given name = Q3358452 Inger
LAST	P735	Q3358452
#   P734 family name = Q37033285
LAST	P734	Q37033285

# create a new item
CREATE
#   set the en label to "Jakob Johannesson Johannesson"
LAST	Len	"Jakob Johannesson Johannesson"
#   set the mul label to "Jakob Johannesson Johannesson"
LAST	Lmul	"Jakob Johannesson Johannesson"
#   set the ja label to "ヤーコプ・ヨハネソン・ヨハネソン"
LAST	Lja	"ヤーコプ・ヨハネソン・ヨハネソン"
#   set the zh label to "雅各布·约哈内松·约哈内松"
LAST	Lzh	"雅各布·约哈内松·约哈内松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000208664806836 Jakob Johannesson Johannesson, qualified P1810 subject named as Jakob Johannesson Johannesson
LAST	P2600	"6000000208664806836"	P1810	"Jakob Johannesson Johannesson"
#   P569 date of birth = +1792-00-00T00:00:00Z/9
LAST	P569	+1792-00-00T00:00:00Z/9	S2600	"6000000208664806836"
#   P570 date of death = +1849-04-02T00:00:00Z/11
LAST	P570	+1849-04-02T00:00:00Z/11	S2600	"6000000208664806836"
#   P40 child = Q141224249 Johannes Jacobsen
LAST	P40	Q141224249	S2600	"6000000208664806836"
#   Q141224249 Johannes Jacobsen: P22 father = the item just created
Q141224249	P22	LAST	S2600	"6000000208664806836"
#   the item just created: P735 given name = Q16747395
LAST	P735	Q16747395

# create a new item
CREATE
#   set the en label to "Jakob Mikael Svedelius"
LAST	Len	"Jakob Mikael Svedelius"
#   set the mul label to "Jakob Mikael Svedelius"
LAST	Lmul	"Jakob Mikael Svedelius"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000019362691691 Jakob Mikael Svedelius, qualified P1810 subject named as Jakob Mikael Svedelius
LAST	P2600	"6000000019362691691"	P1810	"Jakob Mikael Svedelius"
#   P569 date of birth = +1779-04-30T00:00:00Z/11
LAST	P569	+1779-04-30T00:00:00Z/11	S2600	"6000000019362691691"
#   P570 date of death = +1834-03-24T00:00:00Z/11
LAST	P570	+1834-03-24T00:00:00Z/11	S2600	"6000000019362691691"
#   P40 child = Q6197780 Vilhelm Erik Svedelius
LAST	P40	Q6197780	S2600	"6000000019362691691"
#   Q6197780 Vilhelm Erik Svedelius: P22 father = the item just created
Q6197780	P22	LAST	S2600	"6000000019362691691"
#   the item just created: P735 given name = Q16747395, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q16747395	P1545	"1"	P7452	Q3409033
#   P735 given name = Q15620350 Mikael, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q15620350	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Jon Olofsson"
LAST	Len	"Jon Olofsson"
#   set the mul label to "Jon Olofsson"
LAST	Lmul	"Jon Olofsson"
#   set the ja label to "ジョン・オロフソン"
LAST	Lja	"ジョン・オロフソン"
#   set the zh label to "乔恩·奥洛夫松"
LAST	Lzh	"乔恩·奥洛夫松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 5671689391980027024 Jon Olofsson, qualified P1810 subject named as Jon Olofsson
LAST	P2600	"5671689391980027024"	P1810	"Jon Olofsson"
#   P570 date of death = +1590-00-00T00:00:00Z/9
LAST	P570	+1590-00-00T00:00:00Z/9	S2600	"5671689391980027024"
#   P40 child = Q141216389 Jon Jonsson
LAST	P40	Q141216389	S2600	"5671689391980027024"
#   Q141216389 Jon Jonsson: P22 father = the item just created
Q141216389	P22	LAST	S2600	"5671689391980027024"
#   the item just created: P735 given name = Q13501137 Jon
LAST	P735	Q13501137
#   P734 family name = Q23645132 Olofsson
LAST	P734	Q23645132

# create a new item
CREATE
#   set the en label to "Kristofer Sahlin"
LAST	Len	"Kristofer Sahlin"
#   set the mul label to "Kristofer Sahlin"
LAST	Lmul	"Kristofer Sahlin"
#   set the ja label to "クリストファー・サリン"
LAST	Lja	"クリストファー・サリン"
#   set the zh label to "克里斯托费尔·萨林"
LAST	Lzh	"克里斯托费尔·萨林"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003002231602 Kristofer Sahlin, qualified P1810 subject named as Kristofer Sahlin
LAST	P2600	"6000000003002231602"	P1810	"Kristofer Sahlin"
#   P569 date of birth = +1863-09-04T00:00:00Z/11
LAST	P569	+1863-09-04T00:00:00Z/11	S2600	"6000000003002231602"
#   P570 date of death = +1926-12-04T00:00:00Z/11
LAST	P570	+1926-12-04T00:00:00Z/11	S2600	"6000000003002231602"
#   P25 mother = Q116760688 Maria Nordenfelt
LAST	P25	Q116760688	S2600	"6000000003002231602"
#   Q116760688 Maria Nordenfelt: P40 child = the item just created
Q116760688	P40	LAST	S2600	"6000000003002231602"

# create a new item
CREATE
#   the item just created: set the en label to "Lars Osmundsen Nese"
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
#   P25 mother = Q141223553 Ragnhild Kristine Øystensdatter Nese
LAST	P25	Q141223553	S2600	"6000000010480210324"
#   Q141223432 Osmund Larsson Nese: P40 child = the item just created
Q141223432	P40	LAST	S2600	"6000000010480210324"
#   Q141223553 Ragnhild Kristine Øystensdatter Nese: P40 child = the item just created
Q141223553	P40	LAST	S2600	"6000000010480210324"

# create a new item
CREATE
#   the item just created: set the en label to "Margareta Maria Schultén"
LAST	Len	"Margareta Maria Schultén"
#   set the mul label to "Margareta Maria Schultén"
LAST	Lmul	"Margareta Maria Schultén"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000023896531451 Margareta Maria Schultén, qualified P1810 subject named as Margareta Maria Schultén
LAST	P2600	"6000000023896531451"	P1810	"Margareta Maria Schultén"
#   P569 date of birth = +1790-03-24T00:00:00Z/11
LAST	P569	+1790-03-24T00:00:00Z/11	S2600	"6000000023896531451"
#   P570 date of death = +1819-04-03T00:00:00Z/11
LAST	P570	+1819-04-03T00:00:00Z/11	S2600	"6000000023896531451"
#   P26 spouse = Q6060350 Lars Georg Rabenius
LAST	P26	Q6060350	S2600	"6000000023896531451"
#   Q6060350 Lars Georg Rabenius: P26 spouse = the item just created
Q6060350	P26	LAST	S2600	"6000000023896531451"
#   the item just created: P735 given name = Q8274988 Margareta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q8274988	P1545	"1"	P7452	Q3409033
#   P735 given name = Q325872 Maria, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q325872	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Maria Carlberg"
LAST	Len	"Maria Carlberg"
#   set the mul label to "Maria Carlberg"
LAST	Lmul	"Maria Carlberg"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003133670452 Maria Carlberg, qualified P1810 subject named as Maria Carlberg
LAST	P2600	"6000000003133670452"	P1810	"Maria Carlberg"
#   P569 date of birth = +1639-12-25T00:00:00Z/11
LAST	P569	+1639-12-25T00:00:00Z/11	S2600	"6000000003133670452"
#   P570 date of death = +1722-02-05T00:00:00Z/11
LAST	P570	+1722-02-05T00:00:00Z/11	S2600	"6000000003133670452"
#   P26 spouse = Q26239714 Jonas Jonae Rudberus
LAST	P26	Q26239714	S2600	"6000000003133670452"
#   Q26239714 Jonas Jonae Rudberus: P26 spouse = the item just created
Q26239714	P26	LAST	S2600	"6000000003133670452"

# create a new item
CREATE
#   the item just created: set the en label to "Marta Eriksdotter Alsnes"
LAST	Len	"Marta Eriksdotter Alsnes"
#   set the mul label to "Marta Eriksdotter Alsnes"
LAST	Lmul	"Marta Eriksdotter Alsnes"
#   add a mul alias "Marta Eriksdotter Time"
LAST	Amul	"Marta Eriksdotter Time"
#   set the ja label to "マルタ・エリクスドッテル・アルスネス"
LAST	Lja	"マルタ・エリクスドッテル・アルスネス"
#   set the zh label to "玛尔塔·埃里克斯多塔·阿尔斯内斯"
LAST	Lzh	"玛尔塔·埃里克斯多塔·阿尔斯内斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000046742992460 Marta Eriksdotter Alsnes, qualified P1810 subject named as Marta Eriksdotter Time
LAST	P2600	"6000000046742992460"	P1810	"Marta Eriksdotter Time"
#   P569 date of birth = +1797-00-00T00:00:00Z/9
LAST	P569	+1797-00-00T00:00:00Z/9	S2600	"6000000046742992460"
#   P570 date of death = +1845-04-22T00:00:00Z/11
LAST	P570	+1845-04-22T00:00:00Z/11	S2600	"6000000046742992460"
#   P22 father = Q141205904 Erik Tollefson Foss-Eikeland
LAST	P22	Q141205904	S2600	"6000000046742992460"
#   P25 mother = Q141216384 Ingeborg Eriksdatter Time
LAST	P25	Q141216384	S2600	"6000000046742992460"
#   Q141205904 Erik Tollefson Foss-Eikeland: P40 child = the item just created
Q141205904	P40	LAST	S2600	"6000000046742992460"
#   Q141216384 Ingeborg Eriksdatter Time: P40 child = the item just created
Q141216384	P40	LAST	S2600	"6000000046742992460"
#   the item just created: P735 given name = Q846741 Marta
LAST	P735	Q846741
#   P5056 patronym or matronym = Q130232912 Eriksdotter, qualified P144 based on Q141205904 Erik Tollefson Foss-Eikeland
LAST	P5056	Q130232912	P144	Q141205904
#   P734 family name = Q37494555, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q37494555	P3831	Q2507958
#   add a mul alias "Marta Foss-Eikeland Alsnes"
LAST	Amul	"Marta Foss-Eikeland Alsnes"
#   add a mul alias "Marta Alsnes"
LAST	Amul	"Marta Alsnes"

# create a new item
CREATE
#   set the en label to "Ola Rasmussen Bø"
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
#   set the en label to "Sissel Knutsdatter Bjørheim"
LAST	Len	"Sissel Knutsdatter Bjørheim"
#   set the mul label to "Sissel Knutsdatter Bjørheim"
LAST	Lmul	"Sissel Knutsdatter Bjørheim"
#   add a mul alias "Sissel Knutsdatter Knutsdatter"
LAST	Amul	"Sissel Knutsdatter Knutsdatter"
#   set the ja label to "シセル・クヌトスダッテル・ブヨルヘイム"
LAST	Lja	"シセル・クヌトスダッテル・ブヨルヘイム"
#   set the zh label to "西塞尔·克努特斯达特·布约尔赫伊姆"
LAST	Lzh	"西塞尔·克努特斯达特·布约尔赫伊姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 4462761 Sissel Knutsdatter Bjørheim, qualified P1810 subject named as Sissel Knutsdatter Knutsdatter
LAST	P2600	"4462761"	P1810	"Sissel Knutsdatter Knutsdatter"
#   P569 date of birth = +1595-00-00T00:00:00Z/9
LAST	P569	+1595-00-00T00:00:00Z/9	S2600	"4462761"
#   P570 date of death = +1703-02-25T00:00:00Z/11
LAST	P570	+1703-02-25T00:00:00Z/11	S2600	"4462761"
#   P40 child = Q141198507 Tormod Bjørnson Mele
LAST	P40	Q141198507	S2600	"4462761"
#   Q141198507 Tormod Bjørnson Mele: P25 mother = the item just created
Q141198507	P25	LAST	S2600	"4462761"
#   the item just created: P735 given name = Q4571101 Sissel
LAST	P735	Q4571101
#   P734 family name = Q30834379, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q30834379	P3831	Q28418670
#   add a mul alias "Sissel Bjørheim"
LAST	Amul	"Sissel Bjørheim"

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
#   P25 mother = Q141199862 Helga Bjørnsdatter Tengs
LAST	P25	Q141199862	S2600	"6000000004559874338"
#   Q141199851 Lagmann Gunnbjørn Toresson Tengs: P40 child = the item just created
Q141199851	P40	LAST	S2600	"6000000004559874338"
#   Q141199862 Helga Bjørnsdatter Tengs: P40 child = the item just created
Q141199862	P40	LAST	S2600	"6000000004559874338"
#   Q141225179 Maren Ellingsdatter Tunheim: P26 spouse = Q141225230 Osmund Andersen Tunheim
Q141225179	P26	Q141225230	S2600	"340026788150007985"
#   Q6014618 Enar Vilhelm Nordenfelt: P40 child = Q116760688 Maria Nordenfelt
Q6014618	P40	Q116760688	S2600	"4198641"
#   P2600 Geni.com profile ID = 4198641 Enar Vilhelm Nordenfelt, qualified P1810 subject named as Enar Vilhelm Nordenfelt
Q6014618	P2600	"4198641"	P1810	"Enar Vilhelm Nordenfelt"	S2600	"4198641"
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
#   Q141223432 Osmund Larsson Nese: P25 mother = Q141219202 Elen Kristoffersdotter Nese
Q141223432	P25	Q141219202	S2600	"6000000002744891329"
#   P40 child = Q141242389 Christian Osmundsen Nese
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
#   Q141225066 NN: P25 mother = Q141198375 Astri Torchelsdatter Øvre Time
Q141225066	P25	Q141198375	S2600	"6000000003732714453"
#   Q141242383 Bjørn Gunnbjørnsson Kvåvig: P22 father = Q141199851 Lagmann Gunnbjørn Toresson Tengs
Q141242383	P22	Q141199851	S2600	"6000000004569609494"
#   P25 mother = Q141199862 Helga Bjørnsdatter Tengs
Q141242383	P25	Q141199862	S2600	"6000000004569609494"
#   P2600 Geni.com profile ID = 6000000004569609494 Bjørn Gunnbjørnsson Kvåvig, qualified P1810 subject named as Bjørn Gunnbjørnsson Kvåvig
Q141242383	P2600	"6000000004569609494"	P1810	"Bjørn Gunnbjørnsson Kvåvig"	S2600	"6000000004569609494"
#   Q141199862 Helga Bjørnsdatter Tengs: P40 child = Q141242383 Bjørn Gunnbjørnsson Kvåvig
Q141199862	P40	Q141242383	S2600	"6000000004697849241"
#   Q141223436 Tore Underberge III: P25 mother = Q141205937 Ragnhild Eyvindsdotter Eyvindsdotter
Q141223436	P25	Q141205937	S2600	"6000000005607672589"
#   Q141217369 Anna Osmundsd Stokka: P40 child = Q141225175 Malene Larsdtr. Alvseike
Q141217369	P40	Q141225175	S2600	"6000000005609304839"
#   Q109265381 Jonas Benedicti Rudberus: P40 child = Q26239714 Jonas Jonae Rudberus
Q109265381	P40	Q26239714	S2600	"6000000006828534420"
#   P26 spouse = Q109266155 Magdalena Johansdotter Bure
Q109265381	P26	Q109266155	S2600	"6000000006828534420"
#   P2600 Geni.com profile ID = 6000000006828534420 Jonas Benedicti Rudberus, qualified P1810 subject named as Jonas Benedicti Rudberus
Q109265381	P2600	"6000000006828534420"	P1810	"Jonas Benedicti Rudberus"	S2600	"6000000006828534420"
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
#   Q141223903 Elen Margrethe Stangeland: P25 mother = Q141217372 Berta Larsdatter Stangeland
Q141223903	P25	Q141217372	S2600	"6000000011039570406"
#   Q141242389 Christian Osmundsen Nese: P22 father = Q141223432 Osmund Larsson Nese
Q141242389	P22	Q141223432	S2600	"6000000011329696852"
#   P25 mother = Q141223553 Ragnhild Kristine Øystensdatter Nese
Q141242389	P25	Q141223553	S2600	"6000000011329696852"
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
#   Q141225080 Annie Stangeland: P25 mother = Q141223853 Rakel Rasmusdottir Borsheim
Q141225080	P25	Q141223853	S2600	"6000000020344692199"
#   Q141223853 Rakel Rasmusdottir Borsheim: P25 mother = Q141223503 Anne Berta Osmundsdatter Nese
Q141223853	P25	Q141223503	S2600	"6000000020344732085"
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
#   Q141225175 Malene Larsdtr. Alvseike: P25 mother = Q141217369 Anna Osmundsd Stokka
Q141225175	P25	Q141217369	S2600	"6000000030085852982"
#   Q141224339 Reinhert Borsheim: P25 mother = Q141223853 Rakel Rasmusdottir Borsheim
Q141224339	P25	Q141223853	S2600	"6000000032068841409"
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
#   P25 mother = Q141242379 Berte Karlsdatter Borsok
Q141224861	P25	Q141242379	S2600	"6000000035525833995"
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
#   Q141223732 Guttorm Guttormsson: P25 mother = Q141216349 Ingrid Guttormsdotter
Q141223732	P25	Q141216349	S2600	"6000000040760707837"
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
#   Q141219250 Inger Sørensdatter Lima: P25 mother = Q141219065 Marta Torbjørnsdotter Gjesdal
Q141219250	P25	Q141219065	S2600	"6000000065991527068"
#   Q141242411 Palle Paulson Borsok: P22 father = Q141224861 Paul Pederson Borsheim
Q141242411	P22	Q141224861	S2600	"6000000077299349615"
#   P25 mother = Q141224751 Berta Serina Rasmusdatter Borsheim
Q141242411	P25	Q141224751	S2600	"6000000077299349615"
#   P2600 Geni.com profile ID = 6000000077299349615 Palle Paulson Borsok, qualified P1810 subject named as Palle Paulson Borsok
Q141242411	P2600	"6000000077299349615"	P1810	"Palle Paulson Borsok"	S2600	"6000000077299349615"
#   Q141223849 Ola Helgeson Lima: P25 mother = Q141219250 Inger Sørensdatter Lima
Q141223849	P25	Q141219250	S2600	"6000000116694298987"
#   Q141225708 Fru Tore: P40 child = Q141216507 Torborg Toresdatter Norheim
Q141225708	P40	Q141216507	S2600	"6000000150599235831"
#   P2600 Geni.com profile ID = 6000000150599235831 Fru Tore, qualified P1810 subject named as Fru Tore
Q141225708	P2600	"6000000150599235831"	P1810	"Fru Tore"	S2600	"6000000150599235831"
#   Q141216501 Siri Garborg Talle: P26 spouse = Q141242408 Harald Sivert Vålnes
Q141216501	P26	Q141242408	S2600	"6000000177687513857"
#   Q141223923 Helen Frisk: P25 mother = Q141223907 Elly Olivia Frisk
Q141223923	P25	Q141223907	S2600	"6000000177921459052"
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
#   Q141223972 Ådne Olsson Lima Kyllingstad. Lima: P25 mother = Q141223999 Anna Ådnesdatter Lima
Q141223972	P25	Q141223999	S2600	"6000000182737012832"
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


# ------------------------------------------------------------------------
# EMMA-CONFIRMED IDENTITIES -- 13 blocked creations she judged the same person,
#    2026-08-31, one AskUserQuestion each. The duplicate guard was holding each of these
#    because the person's PARENT already named a child item on Wikidata that nothing
#    accounted for. She confirmed the child item IS our person, so the item gets the Geni id
#    and becomes an existing network member -- no creation, and an anchor for its neighbours.
#    Her instruction: "You should be adding the geni id and treating as an existing network
#    member if I approve."
# ------------------------------------------------------------------------
#   Q2066886: P2600 = 6000000001515228463 Hedvig Catharina Charlotta De la Gardie
Q2066886	P2600	"6000000001515228463"	P1810	"Hedvig Catharina Charlotta De la Gardie"
#   Q66316940: P2600 = 6000000024161876529 Anna Sofia Bäck
Q66316940	P2600	"6000000024161876529"	P1810	"Anna Sofia Bäck"
#   Q109829800: P2600 = 6000000006127732211 Eva Helena Adelswärd
Q109829800	P2600	"6000000006127732211"	P1810	"Eva Helena von Fersen"
#   Q110231041: P2600 = 6000000007311831371 Anna Tersera
Q110231041	P2600	"6000000007311831371"	P1810	"Anna Tersera"
#   Q109296043: P2600 = 6000000006127576609 Ulrika Catharina Koskull
Q109296043	P2600	"6000000006127576609"	P1810	"Ulrika Catharina Koskull"
#   Q108615809: P2600 = 6000000007755407668 Margareta Jacobsdotter Jernstedt
Q108615809	P2600	"6000000007755407668"	P1810	"Margareta Jacobsdotter Jernstedt"
#   Q4951688: P2600 = 6000000011637291315 Margareta Gyllenstierna af Fogelvik
Q4951688	P2600	"6000000011637291315"	P1810	"Margareta Gyllenstierna af Fogelvik"
#   Q109835400: P2600 = 6000000008889872098 Magdalena Christina Appelbom
Q109835400	P2600	"6000000008889872098"	P1810	"Magdalena Christina Appelbom"
#   Q110547956: P2600 = 6000000009401513008 Catharina Funck
Q110547956	P2600	"6000000009401513008"	P1810	"Catharina Funck"
#   Q66711908: P2600 = 6000000017425559123 Anna Christina Bruncrona
Q66711908	P2600	"6000000017425559123"	P1810	"Anna Christina Bruncrona"
#   Q110395711: P2600 = 6000000007948266424 Charlotta Eleonora Hedvig von Krassow
Q110395711	P2600	"6000000007948266424"	P1810	"Charlotta Eleonora Hedvig von Krassow"
#   Q111989591: P2600 = 6000000011533226330 Margareta Frodbom
Q111989591	P2600	"6000000011533226330"	P1810	"Margareta Frodbom"
#   Q113007770: P2600 = 6000000013296788468 Maria Sofia Stierncrona
Q113007770	P2600	"6000000013296788468"	P1810	"Maria Sofia Welt"
