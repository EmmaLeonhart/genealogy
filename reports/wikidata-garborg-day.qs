# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   1168 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   set the ja label to "エナル・ノルデンフェルト"
Q6014618	Lja	"エナル・ノルデンフェルト"
#   set the zh label to "埃纳尔·诺尔登费尔特"
Q6014618	Lzh	"埃纳尔·诺尔登费尔特"
#   set the ja label to "ロザラ・オフ・イタリ"
Q466257	Lja	"ロザラ・オフ・イタリ"
#   set the zh label to "罗扎拉·奥夫·伊塔利"
Q466257	Lzh	"罗扎拉·奥夫·伊塔利"
#   set the ja label to "ジュディス・オフ・フランダース・コウンテス・オフ・ノルトムブリア"
Q273181	Lja	"ジュディス・オフ・フランダース・コウンテス・オフ・ノルトムブリア"
#   set the zh label to "朱迪斯·奥夫·夫兰德尔斯·科温特斯·奥夫·诺尔图姆布里阿"
Q273181	Lzh	"朱迪斯·奥夫·夫兰德尔斯·科温特斯·奥夫·诺尔图姆布里阿"
#   set the ja label to "ベネディクタ・エッベスドッテル・オフ・ヴィーデ"
Q2183430	Lja	"ベネディクタ・エッベスドッテル・オフ・ヴィーデ"
#   set the zh label to "贝内迪克塔·埃贝斯多特·奥夫·维德"
Q2183430	Lzh	"贝内迪克塔·埃贝斯多特·奥夫·维德"
#   Q141224907 Segrid NN: set the ja label to "モテル・オフ・マリン・オロフスドッテル"
Q141224907	Lja	"モテル・オフ・マリン・オロフスドッテル"
#   set the zh label to "莫特尔·奥夫·马林·奥洛夫斯多特"
Q141224907	Lzh	"莫特尔·奥夫·马林·奥洛夫斯多特"
#   Q141223426 Isak Reinhold Sahlberg: set the ja label to "イサク・ラインホルト・サルベルグ"
Q141223426	Lja	"イサク・ラインホルト・サルベルグ"
#   set the zh label to "伊萨克·赖因霍尔德·萨尔贝尔格"
Q141223426	Lzh	"伊萨克·赖因霍尔德·萨尔贝尔格"
#   Q2361145 Carl Reinhold Sahlberg: set the ja label to "カール・ラインホルト・サルベルグ"
Q2361145	Lja	"カール・ラインホルト・サルベルグ"
#   set the zh label to "卡尔·赖因霍尔德·萨尔贝尔格"
Q2361145	Lzh	"卡尔·赖因霍尔德·萨尔贝尔格"
#   set the ja label to "カール・ルズヴィ・ヘデンベルグ"
Q141244087	Lja	"カール・ルズヴィ・ヘデンベルグ"

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Anna M. Ekman"
LAST	Len	"Anna M. Ekman"
#   set the mul label to "Anna M. Ekman"
LAST	Lmul	"Anna M. Ekman"
#   set the ja label to "アンナ・ム・エクマン"
LAST	Lja	"アンナ・ム・エクマン"
#   set the zh label to "安娜·姆·埃克曼"
LAST	Lzh	"安娜·姆·埃克曼"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 285884854200005085 Anna M. Ekman, qualified P1810 subject named as Anna M. Ekman
LAST	P2600	"285884854200005085"	P1810	"Anna M. Ekman"
#   P22 father = Q141216640 Per Gustaf Ekman
LAST	P22	Q141216640	S2600	"285884854200005085"
#   P25 mother = Q141216639 Olufine Bergithe Ekman
LAST	P25	Q141216639	S2600	"285884854200005085"
#   Q141216640 Per Gustaf Ekman: P40 child = the item just created
Q141216640	P40	LAST	S2600	"285884854200005085"
#   Q141216639 Olufine Bergithe Ekman: P40 child = the item just created
Q141216639	P40	LAST	S2600	"285884854200005085"
#   the item just created: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P735 given name = Q19803510 M., qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q19803510	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Beata Christina Hierta"
LAST	Len	"Beata Christina Hierta"
#   set the mul label to "Beata Christina Hierta"
LAST	Lmul	"Beata Christina Hierta"
#   set the ja label to "ベアタ・クリスティーナ・ヒエルタ"
LAST	Lja	"ベアタ・クリスティーナ・ヒエルタ"
#   set the zh label to "贝阿塔·克里斯蒂娜·希埃尔塔"
LAST	Lzh	"贝阿塔·克里斯蒂娜·希埃尔塔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000008507926141 Beata Christina Hierta, qualified P1810 subject named as Beata Christina Hierta
LAST	P2600	"6000000008507926141"	P1810	"Beata Christina Hierta"
#   P569 date of birth = +1742-04-07T00:00:00Z/11, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P569	+1742-04-07T00:00:00Z/11	P1480	Q5727902	S2600	"6000000008507926141"
#   P570 date of death = +1792-07-13T00:00:00Z/11
LAST	P570	+1792-07-13T00:00:00Z/11	S2600	"6000000008507926141"
#   P40 child = Q141244084 Anna Wilhelmina Nordenfeldt
LAST	P40	Q141244084	S2600	"6000000008507926141"
#   Q141244084 Anna Wilhelmina Nordenfeldt: P25 mother = the item just created
Q141244084	P25	LAST	S2600	"6000000008507926141"

# create a new item
CREATE
#   the item just created: set the en label to "Berta Asbjørnsdotter Røyneberg"
LAST	Len	"Berta Asbjørnsdotter Røyneberg"
#   set the mul label to "Berta Asbjørnsdotter Røyneberg"
LAST	Lmul	"Berta Asbjørnsdotter Røyneberg"
#   add a mul alias "Berta Asbjørnsdotter Stokka"
LAST	Amul	"Berta Asbjørnsdotter Stokka"
#   set the ja label to "ベルタ・アスブヨルンスドッテル・ロイネベルグ"
LAST	Lja	"ベルタ・アスブヨルンスドッテル・ロイネベルグ"
#   set the zh label to "贝尔塔·阿斯布约尔恩斯多特·罗伊内贝尔格"
LAST	Lzh	"贝尔塔·阿斯布约尔恩斯多特·罗伊内贝尔格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003491933642 Berta Asbjørnsdotter Røyneberg, qualified P1810 subject named as Berta Asbjørnsdotter Stokka
LAST	P2600	"6000000003491933642"	P1810	"Berta Asbjørnsdotter Stokka"
#   P569 date of birth = +1739-00-00T00:00:00Z/9
LAST	P569	+1739-00-00T00:00:00Z/9	S2600	"6000000003491933642"
#   P570 date of death = +1779-00-00T00:00:00Z/9
LAST	P570	+1779-00-00T00:00:00Z/9	S2600	"6000000003491933642"
#   P26 spouse = Q141244102 Jon Torson Røyneberg
LAST	P26	Q141244102	S2600	"6000000003491933642"
#   P40 child = Q141216638 Olaug Jonsdatter Heigre
LAST	P40	Q141216638	S2600	"6000000003491933642"
#   Q141244102 Jon Torson Røyneberg: P26 spouse = the item just created
Q141244102	P26	LAST	S2600	"6000000003491933642"
#   Q141216638 Olaug Jonsdatter Heigre: P25 mother = the item just created
Q141216638	P25	LAST	S2600	"6000000003491933642"
#   the item just created: P735 given name = Q4092653 Berta
LAST	P735	Q4092653
#   P734 family name = Q37033285, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q37033285	P3831	Q2507958
#   add a mul alias "Berte Rønneberg Røyneberg"
LAST	Amul	"Berte Rønneberg Røyneberg"
#   add a mul alias "Berta Røyneberg"
LAST	Amul	"Berta Røyneberg"

# create a new item
CREATE
#   set the en label to "Bjørn Lauritsen Bjørheim"
LAST	Len	"Bjørn Lauritsen Bjørheim"
#   set the mul label to "Bjørn Lauritsen Bjørheim"
LAST	Lmul	"Bjørn Lauritsen Bjørheim"
#   set the ja label to "ビョルン・ラウリトセン・ブヨルヘイム"
LAST	Lja	"ビョルン・ラウリトセン・ブヨルヘイム"
#   set the zh label to "比约恩·拉乌里特森·布约尔赫伊姆"
LAST	Lzh	"比约恩·拉乌里特森·布约尔赫伊姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000002330809317 Bjørn Lauritsen Bjørheim, qualified P1810 subject named as Bjørn Lauritsen Bjørheim
LAST	P2600	"6000000002330809317"	P1810	"Bjørn Lauritsen Bjørheim"
#   P569 date of birth = +1530-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P569	+1530-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"6000000002330809317"
#   P570 date of death = +1596-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P570	+1596-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"6000000002330809317"
#   P22 father = Q141216489 Laurits Leivson Bjørheim
LAST	P22	Q141216489	S2600	"6000000002330809317"
#   P25 mother = Q141216460 Bjørnsdatter Tau
LAST	P25	Q141216460	S2600	"6000000002330809317"
#   P26 spouse = Q141217434 Sissel Sæbjørnsdatter Talgje
LAST	P26	Q141217434	S2600	"6000000002330809317"
#   Q141216489 Laurits Leivson Bjørheim: P40 child = the item just created
Q141216489	P40	LAST	S2600	"6000000002330809317"
#   Q141216460 Bjørnsdatter Tau: P40 child = the item just created
Q141216460	P40	LAST	S2600	"6000000002330809317"
#   Q141217434 Sissel Sæbjørnsdatter Talgje: P26 spouse = the item just created
Q141217434	P26	LAST	S2600	"6000000002330809317"
#   the item just created: P735 given name = Q18918288 Bjørn
LAST	P735	Q18918288
#   P734 family name = Q30834379
LAST	P734	Q30834379
#   add a mul alias "Bjørn Larsen Bjørheim"
LAST	Amul	"Bjørn Larsen Bjørheim"

# create a new item
CREATE
#   set the en label to "Carl Magnus Lagerfelt"
LAST	Len	"Carl Magnus Lagerfelt"
#   set the mul label to "Carl Magnus Lagerfelt"
LAST	Lmul	"Carl Magnus Lagerfelt"
#   set the ja label to "カール・マグヌス・ラゲルフェルト"
LAST	Lja	"カール・マグヌス・ラゲルフェルト"
#   set the zh label to "卡尔·马格努斯·拉盖尔费尔特"
LAST	Lzh	"卡尔·马格努斯·拉盖尔费尔特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000012524450777 Carl Magnus Lagerfelt, qualified P1810 subject named as Carl Magnus Lagerfelt
LAST	P2600	"6000000012524450777"	P1810	"Carl Magnus Lagerfelt"
#   P569 date of birth = +1696-00-00T00:00:00Z/9
LAST	P569	+1696-00-00T00:00:00Z/9	S2600	"6000000012524450777"
#   P570 date of death = +1727-00-00T00:00:00Z/9
LAST	P570	+1727-00-00T00:00:00Z/9	S2600	"6000000012524450777"
#   P22 father = Q109835397 Carl Gustaf Lagerfelt
LAST	P22	Q109835397	S2600	"6000000012524450777"
#   P25 mother = Q109835398 Maria Elisabet von der Osten
LAST	P25	Q109835398	S2600	"6000000012524450777"
#   Q109835397 Carl Gustaf Lagerfelt: P40 child = the item just created
Q109835397	P40	LAST	S2600	"6000000012524450777"
#   Q109835398 Maria Elisabet von der Osten: P40 child = the item just created
Q109835398	P40	LAST	S2600	"6000000012524450777"
#   the item just created: P735 given name = Q2529610 Carl, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q2529610	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18109457 Magnus, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q18109457	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Carl Åke Posse af Säby"
LAST	Len	"Carl Åke Posse af Säby"
#   set the mul label to "Carl Åke Posse af Säby"
LAST	Lmul	"Carl Åke Posse af Säby"
#   set the ja label to "カール・オーケ・ポセ・アフ・セビ"
LAST	Lja	"カール・オーケ・ポセ・アフ・セビ"
#   set the zh label to "卡尔·奥克·波塞·阿夫·塞比"
LAST	Lzh	"卡尔·奥克·波塞·阿夫·塞比"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000008507821635 Carl Åke Posse af Säby, qualified P1810 subject named as Carl Åke Posse af Säby
LAST	P2600	"6000000008507821635"	P1810	"Carl Åke Posse af Säby"
#   P569 date of birth = +1738-00-00T00:00:00Z/9
LAST	P569	+1738-00-00T00:00:00Z/9	S2600	"6000000008507821635"
#   P570 date of death = +1809-00-00T00:00:00Z/9
LAST	P570	+1809-00-00T00:00:00Z/9	S2600	"6000000008507821635"
#   P40 child = Q141244084 Anna Wilhelmina Nordenfeldt
LAST	P40	Q141244084	S2600	"6000000008507821635"
#   Q141244084 Anna Wilhelmina Nordenfeldt: P22 father = the item just created
Q141244084	P22	LAST	S2600	"6000000008507821635"

# create a new item
CREATE
#   the item just created: set the en label to "Catharina Nilsdotter"
LAST	Len	"Catharina Nilsdotter"
#   set the mul label to "Catharina Nilsdotter"
LAST	Lmul	"Catharina Nilsdotter"
#   set the ja label to "カタリーナ・ニルスドッテル"
LAST	Lja	"カタリーナ・ニルスドッテル"
#   set the zh label to "卡塔里娜·尼尔斯多特"
LAST	Lzh	"卡塔里娜·尼尔斯多特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000010807476638 Catharina Nilsdotter, qualified P1810 subject named as Catharina Nilsdotter
LAST	P2600	"6000000010807476638"	P1810	"Catharina Nilsdotter"
#   P569 date of birth = +1604-00-00T00:00:00Z/9
LAST	P569	+1604-00-00T00:00:00Z/9	S2600	"6000000010807476638"
#   P570 date of death = +1674-11-05T00:00:00Z/11
LAST	P570	+1674-11-05T00:00:00Z/11	S2600	"6000000010807476638"
#   P26 spouse = Q16649267 Elias Pedersson Gavelius
LAST	P26	Q16649267	S2600	"6000000010807476638"
#   P40 child = Q5605668 Petrus Eliae Cederschiöld till Lidboholm
LAST	P40	Q5605668	S2600	"6000000010807476638"
#   Q16649267 Elias Pedersson Gavelius: P26 spouse = the item just created
Q16649267	P26	LAST	S2600	"6000000010807476638"
#   Q5605668 Petrus Eliae Cederschiöld till Lidboholm: P25 mother = the item just created
Q5605668	P25	LAST	S2600	"6000000010807476638"

# create a new item
CREATE
#   the item just created: set the en label to "Christina Fant"
LAST	Len	"Christina Fant"
#   set the mul label to "Christina Fant"
LAST	Lmul	"Christina Fant"
#   set the ja label to "クリスティーナ・ファント"
LAST	Lja	"クリスティーナ・ファント"
#   set the zh label to "克里斯蒂娜·凡特"
LAST	Lzh	"克里斯蒂娜·凡特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000002734687344 Christina Fant, qualified P1810 subject named as Christina Fant
LAST	P2600	"6000000002734687344"	P1810	"Christina Fant"
#   P569 date of birth = +1732-11-17T00:00:00Z/11
LAST	P569	+1732-11-17T00:00:00Z/11	S2600	"6000000002734687344"
#   P570 date of death = +1769-02-08T00:00:00Z/11
LAST	P570	+1769-02-08T00:00:00Z/11	S2600	"6000000002734687344"
#   P26 spouse = Q5725186 Michael Fant
LAST	P26	Q5725186	S2600	"6000000002734687344"
#   P40 child = Q5725105 Eric Michael Fant
LAST	P40	Q5725105	S2600	"6000000002734687344"
#   Q5725186 Michael Fant: P26 spouse = the item just created
Q5725186	P26	LAST	S2600	"6000000002734687344"
#   Q5725105 Eric Michael Fant: P25 mother = the item just created
Q5725105	P25	LAST	S2600	"6000000002734687344"
#   the item just created: P735 given name = Q1083457 Christina
LAST	P735	Q1083457

# create a new item
CREATE
#   set the en label to "Christina Juslenius"
LAST	Len	"Christina Juslenius"
#   set the mul label to "Christina Juslenius"
LAST	Lmul	"Christina Juslenius"
#   set the ja label to "クリスティーナ・ユスレニウス"
LAST	Lja	"クリスティーナ・ユスレニウス"
#   set the zh label to "克里斯蒂娜·尤斯莱尼乌斯"
LAST	Lzh	"克里斯蒂娜·尤斯莱尼乌斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000002254696782 Christina Juslenius, qualified P1810 subject named as Christina Juslenius
LAST	P2600	"6000000002254696782"	P1810	"Christina Juslenius"
#   P569 date of birth = +1713-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P569	+1713-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"6000000002254696782"
#   P570 date of death = +1787-01-22T00:00:00Z/11
LAST	P570	+1787-01-22T00:00:00Z/11	S2600	"6000000002254696782"
#   P26 spouse = Q73763454 Sigfrid Porthan
LAST	P26	Q73763454	S2600	"6000000002254696782"
#   P40 child = Q333651 Henrik Gabriel Porthan
LAST	P40	Q333651	S2600	"6000000002254696782"
#   Q73763454 Sigfrid Porthan: P26 spouse = the item just created
Q73763454	P26	LAST	S2600	"6000000002254696782"
#   Q333651 Henrik Gabriel Porthan: P25 mother = the item just created
Q333651	P25	LAST	S2600	"6000000002254696782"
#   the item just created: P735 given name = Q1083457 Christina
LAST	P735	Q1083457

# create a new item
CREATE
#   set the en label to "Dordi Marie Bratterud"
LAST	Len	"Dordi Marie Bratterud"
#   set the mul label to "Dordi Marie Bratterud"
LAST	Lmul	"Dordi Marie Bratterud"
#   add a mul alias "Dordi Marie Tverdahl"
LAST	Amul	"Dordi Marie Tverdahl"
#   set the ja label to "ドルディ・マリー・ブラテルド"
LAST	Lja	"ドルディ・マリー・ブラテルド"
#   set the zh label to "多尔迪·玛丽·布拉特鲁德"
LAST	Lzh	"多尔迪·玛丽·布拉特鲁德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000177203754841 Dordi Marie Bratterud, qualified P1810 subject named as Dordi Marie Tverdahl
LAST	P2600	"6000000177203754841"	P1810	"Dordi Marie Tverdahl"
#   P569 date of birth = +1923-01-20T00:00:00Z/11
LAST	P569	+1923-01-20T00:00:00Z/11	S2600	"6000000177203754841"
#   P570 date of death = +1994-02-14T00:00:00Z/11
LAST	P570	+1994-02-14T00:00:00Z/11	S2600	"6000000177203754841"
#   P22 father = Q141224309 Ole Peter Tverdahl
LAST	P22	Q141224309	S2600	"6000000177203754841"
#   P25 mother = Q141224116 Clara Elfrida Tverdahl
LAST	P25	Q141224116	S2600	"6000000177203754841"
#   Q141224309 Ole Peter Tverdahl: P40 child = the item just created
Q141224309	P40	LAST	S2600	"6000000177203754841"
#   Q141224116 Clara Elfrida Tverdahl: P40 child = the item just created
Q141224116	P40	LAST	S2600	"6000000177203754841"
#   the item just created: P735 given name = Q124708817, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q124708817	P1545	"1"	P7452	Q3409033
#   P735 given name = Q106674406 Marie, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q106674406	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Eli Olsdatter Bærheim"
LAST	Len	"Eli Olsdatter Bærheim"
#   set the mul label to "Eli Olsdatter Bærheim"
LAST	Lmul	"Eli Olsdatter Bærheim"
#   add a mul alias "Eli Olsdatter Soma"
LAST	Amul	"Eli Olsdatter Soma"
#   set the ja label to "イーライ・オルスダッテル・ベルヘイム"
LAST	Lja	"イーライ・オルスダッテル・ベルヘイム"
#   set the zh label to "伊莱·奥尔斯达特·贝尔赫伊姆"
LAST	Lzh	"伊莱·奥尔斯达特·贝尔赫伊姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000006776171569 Eli Olsdatter Bærheim, qualified P1810 subject named as Eli Olsdatter Soma
LAST	P2600	"6000000006776171569"	P1810	"Eli Olsdatter Soma"
#   P570 date of death = +1741-00-00T00:00:00Z/9
LAST	P570	+1741-00-00T00:00:00Z/9	S2600	"6000000006776171569"
#   P40 child = Q141242526 Kirsti Olsdatter Bærheim
LAST	P40	Q141242526	S2600	"6000000006776171569"
#   Q141242526 Kirsti Olsdatter Bærheim: P25 mother = the item just created
Q141242526	P25	LAST	S2600	"6000000006776171569"
#   the item just created: P735 given name = Q1328791 Eli
LAST	P735	Q1328791
#   P5056 patronym or matronym = Q51885688 Olsdatter
LAST	P5056	Q51885688
#   P734 family name = Q37104818, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q37104818	P3831	Q2507958
#   P734 family name = Q40246530 Bærheim, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q40246530	P3831	Q28418670
#   add a mul alias "Eli Bærheim"
LAST	Amul	"Eli Bærheim"

# create a new item
CREATE
#   set the en label to "Emerentia Mårtensdotter"
LAST	Len	"Emerentia Mårtensdotter"
#   set the mul label to "Emerentia Mårtensdotter"
LAST	Lmul	"Emerentia Mårtensdotter"
#   set the ja label to "エメレンティア・モーテンスドッテル"
LAST	Lja	"エメレンティア・モーテンスドッテル"
#   set the zh label to "埃梅伦蒂阿·莫滕斯多特"
LAST	Lzh	"埃梅伦蒂阿·莫滕斯多特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000027467257347 Emerentia Mårtensdotter, qualified P1810 subject named as Emerentia Mårtensdotter
LAST	P2600	"6000000027467257347"	P1810	"Emerentia Mårtensdotter"
#   P22 father = Q141199959 Martinus Johannis
LAST	P22	Q141199959	S2600	"6000000027467257347"
#   P25 mother = Q141199822 Anna Jönsdotter
LAST	P25	Q141199822	S2600	"6000000027467257347"
#   Q141199959 Martinus Johannis: P40 child = the item just created
Q141199959	P40	LAST	S2600	"6000000027467257347"
#   Q141199822 Anna Jönsdotter: P40 child = the item just created
Q141199822	P40	LAST	S2600	"6000000027467257347"
#   the item just created: P735 given name = Q74913247 Emerentia
LAST	P735	Q74913247

# create a new item
CREATE
#   set the en label to "Emilia Helena Carolina Braun"
LAST	Len	"Emilia Helena Carolina Braun"
#   set the mul label to "Emilia Helena Carolina Braun"
LAST	Lmul	"Emilia Helena Carolina Braun"
#   set the ja label to "エミリア・ヘレナ・カロリーナ・ブラウン"
LAST	Lja	"エミリア・ヘレナ・カロリーナ・ブラウン"
#   set the zh label to "埃米莉亚·海伦娜·卡罗琳娜·布劳恩"
LAST	Lzh	"埃米莉亚·海伦娜·卡罗琳娜·布劳恩"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000020984683047 Emilia Helena Carolina Braun, qualified P1810 subject named as Emilia Helena Carolina Braun
LAST	P2600	"6000000020984683047"	P1810	"Emilia Helena Carolina Braun"
#   P569 date of birth = +1829-04-11T00:00:00Z/11
LAST	P569	+1829-04-11T00:00:00Z/11	S2600	"6000000020984683047"
#   P570 date of death = +1910-08-06T00:00:00Z/11
LAST	P570	+1910-08-06T00:00:00Z/11	S2600	"6000000020984683047"
#   P40 child = Q5977879 Hugo Wilhelm Martin
LAST	P40	Q5977879	S2600	"6000000020984683047"
#   Q5977879 Hugo Wilhelm Martin: P25 mother = the item just created
Q5977879	P25	LAST	S2600	"6000000020984683047"
#   the item just created: P735 given name = Q1495413 Emilia, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q1495413	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1035239 Helena, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1035239	P1545	"2"	P3831	Q245025
#   P735 given name = Q5044762 Carolina, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
LAST	P735	Q5044762	P1545	"3"	P3831	Q245025
#   P734 family name = Q354330 Braun
LAST	P734	Q354330

# create a new item
CREATE
#   set the en label to "Fredrika Lovisa Uggla"
LAST	Len	"Fredrika Lovisa Uggla"
#   set the mul label to "Fredrika Lovisa Uggla"
LAST	Lmul	"Fredrika Lovisa Uggla"
#   set the ja label to "フレデリカ・ロヴィサ・ウグラ"
LAST	Lja	"フレデリカ・ロヴィサ・ウグラ"
#   set the zh label to "夫雷德里卡·洛维萨·乌格拉"
LAST	Lzh	"夫雷德里卡·洛维萨·乌格拉"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000013400765266 Fredrika Lovisa Uggla, qualified P1810 subject named as Fredrika Lovisa Uggla
LAST	P2600	"6000000013400765266"	P1810	"Fredrika Lovisa Uggla"
#   P569 date of birth = +1746-00-00T00:00:00Z/9
LAST	P569	+1746-00-00T00:00:00Z/9	S2600	"6000000013400765266"
#   P570 date of death = +1794-00-00T00:00:00Z/9
LAST	P570	+1794-00-00T00:00:00Z/9	S2600	"6000000013400765266"
#   P26 spouse = Q122980318 Samuel Fredrik Åkerhielm af Margretelund
LAST	P26	Q122980318	S2600	"6000000013400765266"
#   P40 child = Q6255155 Gustaf Fredrik Åkerhielm af Margretelund
LAST	P40	Q6255155	S2600	"6000000013400765266"
#   Q122980318 Samuel Fredrik Åkerhielm af Margretelund: P26 spouse = the item just created
Q122980318	P26	LAST	S2600	"6000000013400765266"
#   Q6255155 Gustaf Fredrik Åkerhielm af Margretelund: P25 mother = the item just created
Q6255155	P25	LAST	S2600	"6000000013400765266"
#   the item just created: P735 given name = Q5499550 Fredrika, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q5499550	P1545	"1"	P7452	Q3409033
#   P735 given name = Q10570000 Lovisa, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q10570000	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Helena Gangia"
LAST	Len	"Helena Gangia"
#   set the mul label to "Helena Gangia"
LAST	Lmul	"Helena Gangia"
#   set the ja label to "ヘレナ・ガンギア"
LAST	Lja	"ヘレナ・ガンギア"
#   set the zh label to "海伦娜·甘吉阿"
LAST	Lzh	"海伦娜·甘吉阿"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000002810895810 Helena Gangia, qualified P1810 subject named as Helena Gangia
LAST	P2600	"6000000002810895810"	P1810	"Helena Gangia"
#   P569 date of birth = +1677-09-05T00:00:00Z/11
LAST	P569	+1677-09-05T00:00:00Z/11	S2600	"6000000002810895810"
#   P570 date of death = +1760-05-16T00:00:00Z/11
LAST	P570	+1760-05-16T00:00:00Z/11	S2600	"6000000002810895810"
#   P26 spouse = Q48562235 Prost Olaus Troilius
LAST	P26	Q48562235	S2600	"6000000002810895810"
#   P40 child = Q1168365 Ärkebiskop Samuelis Olai Troilius
LAST	P40	Q1168365	S2600	"6000000002810895810"
#   Q48562235 Prost Olaus Troilius: P26 spouse = the item just created
Q48562235	P26	LAST	S2600	"6000000002810895810"
#   Q1168365 Ärkebiskop Samuelis Olai Troilius: P25 mother = the item just created
Q1168365	P25	LAST	S2600	"6000000002810895810"
#   the item just created: P735 given name = Q1035239 Helena
LAST	P735	Q1035239

# create a new item
CREATE
#   set the en label to "Herta Lovisa Charlotta Sandels"
LAST	Len	"Herta Lovisa Charlotta Sandels"
#   set the mul label to "Herta Lovisa Charlotta Sandels"
LAST	Lmul	"Herta Lovisa Charlotta Sandels"
#   add a mul alias "Herta Lovisa Charlotta Amnéus"
LAST	Amul	"Herta Lovisa Charlotta Amnéus"
#   set the ja label to "ハータ・ロヴィサ・カルロタ・サンデルス"
LAST	Lja	"ハータ・ロヴィサ・カルロタ・サンデルス"
#   set the zh label to "赫塔·洛维萨·卡尔洛塔·桑德尔斯"
LAST	Lzh	"赫塔·洛维萨·卡尔洛塔·桑德尔斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000019068623814 Herta Lovisa Charlotta Sandels, qualified P1810 subject named as Herta Lovisa Charlotta Amnéus
LAST	P2600	"6000000019068623814"	P1810	"Herta Lovisa Charlotta Amnéus"
#   P569 date of birth = +1879-12-01T00:00:00Z/11
LAST	P569	+1879-12-01T00:00:00Z/11	S2600	"6000000019068623814"
#   P570 date of death = +1960-07-08T00:00:00Z/11
LAST	P570	+1960-07-08T00:00:00Z/11	S2600	"6000000019068623814"
#   P40 child = Q4976863 Stina Claesdotter Sandels
LAST	P40	Q4976863	S2600	"6000000019068623814"
#   Q4976863 Stina Claesdotter Sandels: P25 mother = the item just created
Q4976863	P25	LAST	S2600	"6000000019068623814"
#   the item just created: P735 given name = Q10570000 Lovisa, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q10570000	P1545	"2"	P3831	Q245025
#   P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1067071	P1545	"3"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Justina Margareta Djurberg"
LAST	Len	"Justina Margareta Djurberg"
#   set the mul label to "Justina Margareta Djurberg"
LAST	Lmul	"Justina Margareta Djurberg"
#   set the ja label to "ジャスティナ・マルガレータ・ドユルベルグ"
LAST	Lja	"ジャスティナ・マルガレータ・ドユルベルグ"
#   set the zh label to "尤斯蒂纳·瑪格麗塔·德尤尔贝尔格"
LAST	Lzh	"尤斯蒂纳·瑪格麗塔·德尤尔贝尔格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000018646675929 Justina Margareta Djurberg, qualified P1810 subject named as Justina Margareta Djurberg
LAST	P2600	"6000000018646675929"	P1810	"Justina Margareta Djurberg"
#   P569 date of birth = +1696-02-11T00:00:00Z/11
LAST	P569	+1696-02-11T00:00:00Z/11	S2600	"6000000018646675929"
#   P570 date of death = +1774-11-01T00:00:00Z/11
LAST	P570	+1774-11-01T00:00:00Z/11	S2600	"6000000018646675929"
#   P26 spouse = Q19976772 Simon Melander
LAST	P26	Q19976772	S2600	"6000000018646675929"
#   P40 child = Q5983613 Daniel Melanderhielm
LAST	P40	Q5983613	S2600	"6000000018646675929"
#   Q19976772 Simon Melander: P26 spouse = the item just created
Q19976772	P26	LAST	S2600	"6000000018646675929"
#   Q5983613 Daniel Melanderhielm: P25 mother = the item just created
Q5983613	P25	LAST	S2600	"6000000018646675929"
#   the item just created: P735 given name = Q18211002 Justina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q18211002	P1545	"1"	P7452	Q3409033
#   P735 given name = Q8274988 Margareta, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q8274988	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Justina Sophie Naucler"
LAST	Len	"Justina Sophie Naucler"
#   set the mul label to "Justina Sophie Naucler"
LAST	Lmul	"Justina Sophie Naucler"
#   set the ja label to "ジャスティナ・ソフィー・ナウクレル"
LAST	Lja	"ジャスティナ・ソフィー・ナウクレル"
#   set the zh label to "尤斯蒂纳·索菲·纳乌克莱尔"
LAST	Lzh	"尤斯蒂纳·索菲·纳乌克莱尔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 1609740 Justina Sophie Naucler, qualified P1810 subject named as Justina Sofia Ziervogel
LAST	P2600	"1609740"	P1810	"Justina Sofia Ziervogel"
#   P569 date of birth = +1702-00-00T00:00:00Z/9
LAST	P569	+1702-00-00T00:00:00Z/9	S2600	"1609740"
#   P570 date of death = +1783-00-00T00:00:00Z/9
LAST	P570	+1783-00-00T00:00:00Z/9	S2600	"1609740"
#   P26 spouse = Q16649961 Olof Olofsson Nauclérus
LAST	P26	Q16649961	S2600	"1609740"
#   P40 child = Q16649960 Olof Nauclér
LAST	P40	Q16649960	S2600	"1609740"
#   Q16649961 Olof Olofsson Nauclérus: P26 spouse = the item just created
Q16649961	P26	LAST	S2600	"1609740"
#   Q16649960 Olof Nauclér: P25 mother = the item just created
Q16649960	P25	LAST	S2600	"1609740"
#   the item just created: P735 given name = Q18211002 Justina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q18211002	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q18201520	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Knut Bjørnson Bjørheim"
LAST	Len	"Knut Bjørnson Bjørheim"
#   set the mul label to "Knut Bjørnson Bjørheim"
LAST	Lmul	"Knut Bjørnson Bjørheim"
#   set the ja label to "クヌート・ビョルンソン・ブヨルヘイム"
LAST	Lja	"クヌート・ビョルンソン・ブヨルヘイム"
#   set the zh label to "克努特·布约尔恩松·布约尔赫伊姆"
LAST	Lzh	"克努特·布约尔恩松·布约尔赫伊姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000002277957043 Knut Bjørnson Bjørheim, qualified P1810 subject named as Knut Bjørnson Bjørheim
LAST	P2600	"6000000002277957043"	P1810	"Knut Bjørnson Bjørheim"
#   P569 date of birth = +1563-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P569	+1563-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"6000000002277957043"
#   P570 date of death = +1659-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P570	+1659-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"6000000002277957043"
#   P25 mother = Q141217434 Sissel Sæbjørnsdatter Talgje
LAST	P25	Q141217434	S2600	"6000000002277957043"
#   Q141217434 Sissel Sæbjørnsdatter Talgje: P40 child = the item just created
Q141217434	P40	LAST	S2600	"6000000002277957043"
#   the item just created: P735 given name = Q943881 Knut
LAST	P735	Q943881
#   P734 family name = Q30834379
LAST	P734	Q30834379

# create a new item
CREATE
#   set the en label to "Margareta Carlsdotter Sparre"
LAST	Len	"Margareta Carlsdotter Sparre"
#   set the mul label to "Margareta Carlsdotter Sparre"
LAST	Lmul	"Margareta Carlsdotter Sparre"
#   set the ja label to "マルガレータ・カルルスドッテル・シュパラー"
LAST	Lja	"マルガレータ・カルルスドッテル・シュパラー"
#   set the zh label to "瑪格麗塔·卡尔尔斯多特·斯帕雷"
LAST	Lzh	"瑪格麗塔·卡尔尔斯多特·斯帕雷"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000000044429416 Margareta Carlsdotter Sparre, qualified P1810 subject named as Margareta Carlsdotter Sparre
LAST	P2600	"6000000000044429416"	P1810	"Margareta Carlsdotter Sparre"
#   P570 date of death = +1720-08-13T00:00:00Z/11
LAST	P570	+1720-08-13T00:00:00Z/11	S2600	"6000000000044429416"
#   P26 spouse = Q130755124 Johan Gustav Boije af Gennäs
LAST	P26	Q130755124	S2600	"6000000000044429416"
#   P40 child = Q5580881 Carl Gustaf Boije af Gennäs
LAST	P40	Q5580881	S2600	"6000000000044429416"
#   Q130755124 Johan Gustav Boije af Gennäs: P26 spouse = the item just created
Q130755124	P26	LAST	S2600	"6000000000044429416"
#   the item just created: P735 given name = Q8274988 Margareta
LAST	P735	Q8274988
#   P734 family name = Q30136491 Sparre
LAST	P734	Q30136491

# create a new item
CREATE
#   set the en label to "Ola Olson Bæreim"
LAST	Len	"Ola Olson Bæreim"
#   set the mul label to "Ola Olson Bæreim"
LAST	Lmul	"Ola Olson Bæreim"
#   set the ja label to "オーラ・オルソン・ベレイム"
LAST	Lja	"オーラ・オルソン・ベレイム"
#   set the zh label to "奥拉·奥尔森·贝雷伊姆"
LAST	Lzh	"奥拉·奥尔森·贝雷伊姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000002226706375 Ola Olson Bæreim, qualified P1810 subject named as Ola Olson Bæreim
LAST	P2600	"6000000002226706375"	P1810	"Ola Olson Bæreim"
#   P569 date of birth = +1656-00-00T00:00:00Z/9
LAST	P569	+1656-00-00T00:00:00Z/9	S2600	"6000000002226706375"
#   P40 child = Q141242526 Kirsti Olsdatter Bærheim
LAST	P40	Q141242526	S2600	"6000000002226706375"
#   Q141242526 Kirsti Olsdatter Bærheim: P22 father = the item just created
Q141242526	P22	LAST	S2600	"6000000002226706375"
#   the item just created: P735 given name = Q96675523 Ola
LAST	P735	Q96675523
#   add a mul alias "Ola Bæreim"
LAST	Amul	"Ola Bæreim"

# create a new item
CREATE
#   set the en label to "Ramfrid Gustavsdotter Lejon"
LAST	Len	"Ramfrid Gustavsdotter Lejon"
#   set the mul label to "Ramfrid Gustavsdotter Lejon"
LAST	Lmul	"Ramfrid Gustavsdotter Lejon"
#   set the ja label to "ラムフリド・グスタヴスドッテル・レヨン"
LAST	Lja	"ラムフリド・グスタヴスドッテル・レヨン"
#   set the zh label to "拉姆夫里德·古斯塔夫斯多特·莱永"
LAST	Lzh	"拉姆夫里德·古斯塔夫斯多特·莱永"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003414518688 Ramfrid Gustavsdotter Lejon, qualified P1810 subject named as Ramfrid Gustavsdotter Lejon
LAST	P2600	"6000000003414518688"	P1810	"Ramfrid Gustavsdotter Lejon"
#   P569 date of birth = +1255-00-00T00:00:00Z/9
LAST	P569	+1255-00-00T00:00:00Z/9	S2600	"6000000003414518688"
#   P570 date of death = +1307-00-00T00:00:00Z/9, qualified P1319 earliest date +1307-00-00T00:00:00Z/9
LAST	P570	+1307-00-00T00:00:00Z/9	P1319	+1307-00-00T00:00:00Z/9	S2600	"6000000003414518688"
#   P22 father = Q141223837 Gustav Petersson Lejon
LAST	P22	Q141223837	S2600	"6000000003414518688"
#   P25 mother = Q141223838 Hafrid Sigtryggsdotter Boberg
LAST	P25	Q141223838	S2600	"6000000003414518688"
#   Q141223837 Gustav Petersson Lejon: P40 child = the item just created
Q141223837	P40	LAST	S2600	"6000000003414518688"
#   Q141223838 Hafrid Sigtryggsdotter Boberg: P40 child = the item just created
Q141223838	P40	LAST	S2600	"6000000003414518688"

# create a new item
CREATE
#   the item just created: set the en label to "Reier Halvorson Vashus"
LAST	Len	"Reier Halvorson Vashus"
#   set the mul label to "Reier Halvorson Vashus"
LAST	Lmul	"Reier Halvorson Vashus"
#   add a mul alias "Reier Halvorson Storhaug"
LAST	Amul	"Reier Halvorson Storhaug"
#   set the ja label to "レイエル・ハルヴォルソン・ヴァスフス"
LAST	Lja	"レイエル・ハルヴォルソン・ヴァスフス"
#   set the zh label to "雷伊埃尔·哈尔沃尔松·瓦斯胡斯"
LAST	Lzh	"雷伊埃尔·哈尔沃尔松·瓦斯胡斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000006771426726 Reier Halvorson Vashus, qualified P1810 subject named as Reier Halvorson Storhaug
LAST	P2600	"6000000006771426726"	P1810	"Reier Halvorson Storhaug"
#   P569 date of birth = +1745-00-00T00:00:00Z/9
LAST	P569	+1745-00-00T00:00:00Z/9	S2600	"6000000006771426726"
#   P570 date of death = +1836-01-06T00:00:00Z/11
LAST	P570	+1836-01-06T00:00:00Z/11	S2600	"6000000006771426726"
#   P22 father = Q141219060 Halvor Johannesson Hobberstad
LAST	P22	Q141219060	S2600	"6000000006771426726"
#   P25 mother = Q141219053 Barbro Reiersdatter Storhaug
LAST	P25	Q141219053	S2600	"6000000006771426726"
#   Q141219060 Halvor Johannesson Hobberstad: P40 child = the item just created
Q141219060	P40	LAST	S2600	"6000000006771426726"
#   Q141219053 Barbro Reiersdatter Storhaug: P40 child = the item just created
Q141219053	P40	LAST	S2600	"6000000006771426726"
#   the item just created: P735 given name = Q21147248 Reier
LAST	P735	Q21147248
#   P734 family name = Q27892826 Storhaug, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q27892826	P3831	Q2507958
#   add a mul alias "Reier Vashus"
LAST	Amul	"Reier Vashus"

# create a new item
CREATE
#   set the en label to "Ture Turesson Bielke"
LAST	Len	"Ture Turesson Bielke"
#   set the mul label to "Ture Turesson Bielke"
LAST	Lmul	"Ture Turesson Bielke"
#   set the ja label to "トゥーレ・トレソン・ビールケ"
LAST	Lja	"トゥーレ・トレソン・ビールケ"
#   set the zh label to "图雷·图雷松·比埃尔凯"
LAST	Lzh	"图雷·图雷松·比埃尔凯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000006127206029 Ture Turesson Bielke, qualified P1810 subject named as Ture Turesson Bielke
LAST	P2600	"6000000006127206029"	P1810	"Ture Turesson Bielke"
#   P569 date of birth = +1713-00-00T00:00:00Z/9
LAST	P569	+1713-00-00T00:00:00Z/9	S2600	"6000000006127206029"
#   P570 date of death = +1738-07-20T00:00:00Z/11
LAST	P570	+1738-07-20T00:00:00Z/11	S2600	"6000000006127206029"
#   P22 father = Q5597349 Thure Stensson Bielke
LAST	P22	Q5597349	S2600	"6000000006127206029"
#   P25 mother = Q141244125 Ursula Christina Törne
LAST	P25	Q141244125	S2600	"6000000006127206029"
#   Q5597349 Thure Stensson Bielke: P40 child = the item just created
Q5597349	P40	LAST	S2600	"6000000006127206029"
#   Q141244125 Ursula Christina Törne: P40 child = the item just created
Q141244125	P40	LAST	S2600	"6000000006127206029"
#   the item just created: P735 given name = Q2460609 Ture
LAST	P735	Q2460609
#   P5056 patronym or matronym = Q130232969 Turesson, qualified P144 based on Q5597349 Thure Stensson Bielke
LAST	P5056	Q130232969	P144	Q5597349
#   P734 family name = Q37547315 Bielke
LAST	P734	Q37547315

# create a new item
CREATE
#   set the en label to "Ulrika Charlotta Rotkirch"
LAST	Len	"Ulrika Charlotta Rotkirch"
#   set the mul label to "Ulrika Charlotta Rotkirch"
LAST	Lmul	"Ulrika Charlotta Rotkirch"
#   set the ja label to "ウルリカ・カルロタ・ロトキルク"
LAST	Lja	"ウルリカ・カルロタ・ロトキルク"
#   set the zh label to "乌尔里卡·卡尔洛塔·罗特基尔克"
LAST	Lzh	"乌尔里卡·卡尔洛塔·罗特基尔克"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000002681115184 Ulrika Charlotta Rotkirch, qualified P1810 subject named as Ulrika Charlotta Rotkirch
LAST	P2600	"6000000002681115184"	P1810	"Ulrika Charlotta Rotkirch"
#   P569 date of birth = +1713-11-23T00:00:00Z/11
LAST	P569	+1713-11-23T00:00:00Z/11	S2600	"6000000002681115184"
#   P570 date of death = +1787-04-07T00:00:00Z/11
LAST	P570	+1787-04-07T00:00:00Z/11	S2600	"6000000002681115184"
#   P40 child = Q593496 Anton Rolandsson Martin
LAST	P40	Q593496	S2600	"6000000002681115184"
#   Q593496 Anton Rolandsson Martin: P25 mother = the item just created
Q593496	P25	LAST	S2600	"6000000002681115184"
#   the item just created: P735 given name = Q18924998 Ulrika, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q18924998	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1067071	P1545	"2"	P3831	Q245025
#   Q141244118 Nils Nilsson Midt-Fister d.y: P22 father = Q141244117 Nils Fister
Q141244118	P22	Q141244117	S2600	"328122852240006970"
#   Q141244117 Nils Fister: P40 child = Q141244118 Nils Nilsson Midt-Fister d.y
Q141244117	P40	Q141244118	S2600	"328126701460004633"
#   Q5773287 Samuel Andreæ Grubb: P3373 sibling = Q141244086 Brita Andersdotter Grubb
Q5773287	P3373	Q141244086	S2600	"5105724209600128719"
#   Q141244087 Carl Ludvig Hedenberg: P25 mother = Q141244082 Anna Elisabet Charlotta Andersdotter Rehbinder
Q141244087	P25	Q141244082	S2600	"6000000000909055457"
#   Q141244082 Anna Elisabet Charlotta Andersdotter Rehbinder: P40 child = Q141244087 Carl Ludvig Hedenberg
Q141244082	P40	Q141244087	S2600	"6000000000909142439"
#   Q141244110 Maria Carolina Elisabet Sahlin: P26 spouse = Q141244103 Kristofer Sahlin
Q141244110	P26	Q141244103	S2600	"6000000002986902894"
#   Q141244103 Kristofer Sahlin: P26 spouse = Q141244110 Maria Carolina Elisabet Sahlin
Q141244103	P26	Q141244110	S2600	"6000000003002231602"
#   Q141244120 Ragnhild Jonsdatter Grannes: P26 spouse = Q141244099 Hans Hansson Store Vatne
Q141244120	P26	Q141244099	S2600	"6000000005608892528"
#   Q141244099 Hans Hansson Store Vatne: P26 spouse = Q141244120 Ragnhild Jonsdatter Grannes
Q141244099	P26	Q141244120	S2600	"6000000005608892535"
#   Q141244101 Haquinus Thorstani Rudenius: P26 spouse = Q141244093 Christina Torstensdotter Falk
Q141244101	P26	Q141244093	S2600	"6000000006833125349"
#   Q141244093 Christina Torstensdotter Falk: P26 spouse = Q141244101 Haquinus Thorstani Rudenius
Q141244093	P26	Q141244101	S2600	"6000000006833371173"
#   Q141244081 Anders Alstrin: P26 spouse = Q141244096 Gunilla Nilsdotter
Q141244081	P26	Q141244096	S2600	"6000000019263256732"
#   Q141244096 Gunilla Nilsdotter: P26 spouse = Q141244081 Anders Alstrin
Q141244096	P26	Q141244081	S2600	"6000000040336826716"
#   Q3359192 Elsa Beata Wrede af Elimä: P40 child = Q16945169 Mårten Bunge till Beateberg
Q3359192	P40	Q16945169	S2600	"6000000138755587213"
#   P26 spouse = Q5589959 Sven Bunge till Beateberg
Q3359192	P26	Q5589959	S2600	"6000000138755587213"
#   P2600 Geni.com profile ID = 6000000138755587213 Elsa Beata Wrede af Elimä, qualified P1810 subject named as Elsa Beata Wrede
Q3359192	P2600	"6000000138755587213"	P1810	"Elsa Beata Wrede"
#   Q141223923 Helen Frisk: P25 mother = Q141223907 Elly Olivia Frisk
Q141223923	P25	Q141223907	S2600	"6000000177921459052"
#   Q141223972 Ådne Olsson Lima Kyllingstad. Lima: P25 mother = Q141223999 Anna Ådnesdatter Lima
Q141223972	P25	Q141223999	S2600	"6000000182737012832"
#   Q141223897 Adolf Adelswärd: P25 mother = Q110547956 Catharina Funck
Q141223897	P25	Q110547956	S2600	"6000000205630579893"

