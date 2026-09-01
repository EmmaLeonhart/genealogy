# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   1169 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   add a mul alias "Justina Sofia Ziervogel"
Q141244224	Amul	"Justina Sofia Ziervogel"
#   Q141244230 Maria Elisabet Wærn: set the ja label to "マリア・エリーザベト・ヴェルン"
Q141244230	Lja	"マリア・エリーザベト・ヴェルン"
#   set the zh label to "玛丽亚·伊丽莎白·韦尔恩"
Q141244230	Lzh	"玛丽亚·伊丽莎白·韦尔恩"
#   set the zh label to "卡尔·卢德维格·赫登贝尔格"
Q141244087	Lzh	"卡尔·卢德维格·赫登贝尔格"
#   set the ja label to "ルイ・テ・ピオウス"
Q43974	Lja	"ルイ・テ・ピオウス"
#   set the zh label to "路易·特·皮奥乌斯"
Q43974	Lzh	"路易·特·皮奥乌斯"
#   set the ja label to "アクセル・ヴォン・フェルセン・テ・ヨウンゲル"
Q455071	Lja	"アクセル・ヴォン・フェルセン・テ・ヨウンゲル"
#   set the zh label to "阿克塞尔·翁·费尔森·特·约温盖尔"
Q455071	Lzh	"阿克塞尔·翁·费尔森·特·约温盖尔"
#   set the ja label to "ベレンガル・I・オフ・イタリ"
Q274606	Lja	"ベレンガル・I・オフ・イタリ"
#   set the zh label to "贝伦加尔·I·奥夫·伊塔利"
Q274606	Lzh	"贝伦加尔·I·奥夫·伊塔利"
#   Q75933086: set the ja label to "グイラウメ・I・デ・ガルランデ・セイグネウル・デ・ガルランデ"
Q75933086	Lja	"グイラウメ・I・デ・ガルランデ・セイグネウル・デ・ガルランデ"
#   set the zh label to "古伊拉乌梅·I·德·加尔兰德·塞伊格内乌尔·德·加尔兰德"
Q75933086	Lzh	"古伊拉乌梅·I·德·加尔兰德·塞伊格内乌尔·德·加尔兰德"
#   Q141223730 Constantia Fehman: set the ja label to "コンスタンティア・フェマン"
Q141223730	Lja	"コンスタンティア・フェマン"
#   set the zh label to "孔斯坦蒂阿·费曼"
Q141223730	Lzh	"孔斯坦蒂阿·费曼"
#   set the ja label to "カール・ニルソン・ポルヴィアンデル"
Q141244225	Lja	"カール・ニルソン・ポルヴィアンデル"

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the mul label to "NN"
LAST	Lmul	"NN"
#   set the ca label to "fill de Astri Torchelsdatter Øvre Time"
LAST	Lca	"fill de Astri Torchelsdatter Øvre Time"
#   set the da label to "søn af Astri Torchelsdatter Øvre Time"
LAST	Lda	"søn af Astri Torchelsdatter Øvre Time"
#   set the de label to "Sohn von Astri Torchelsdatter Øvre Time"
LAST	Lde	"Sohn von Astri Torchelsdatter Øvre Time"
#   set the en label to "son of Astri Torchelsdatter Øvre Time"
LAST	Len	"son of Astri Torchelsdatter Øvre Time"
#   set the es label to "hijo de Astri Torchelsdatter Øvre Time"
LAST	Les	"hijo de Astri Torchelsdatter Øvre Time"
#   set the fr label to "fils de Astri Torchelsdatter Øvre Time"
LAST	Lfr	"fils de Astri Torchelsdatter Øvre Time"
#   set the it label to "figlio di Astri Torchelsdatter Øvre Time"
LAST	Lit	"figlio di Astri Torchelsdatter Øvre Time"
#   set the ja label to "アストリ・トルケルスダッテル・オヴレ・ティメの息子"
LAST	Lja	"アストリ・トルケルスダッテル・オヴレ・ティメの息子"
#   set the nb label to "sønn av Astri Torchelsdatter Øvre Time"
LAST	Lnb	"sønn av Astri Torchelsdatter Øvre Time"
#   set the nl label to "zoon van Astri Torchelsdatter Øvre Time"
LAST	Lnl	"zoon van Astri Torchelsdatter Øvre Time"
#   set the pt label to "filho de Astri Torchelsdatter Øvre Time"
LAST	Lpt	"filho de Astri Torchelsdatter Øvre Time"
#   set the sv label to "son till Astri Torchelsdatter Øvre Time"
LAST	Lsv	"son till Astri Torchelsdatter Øvre Time"
#   set the zh label to "阿斯特丽·托尔凯尔斯达特·奥夫雷·蒂梅之子"
LAST	Lzh	"阿斯特丽·托尔凯尔斯达特·奥夫雷·蒂梅之子"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003732714443 NN
LAST	P2600	"6000000003732714443"
#   P22 father = Q141198370 NN Skårland
LAST	P22	Q141198370	S2600	"6000000003732714443"
#   P25 mother = Q141198375 Astri Torchelsdatter Øvre Time
LAST	P25	Q141198375	S2600	"6000000003732714443"
#   Q141198370 NN Skårland: P40 child = the item just created
Q141198370	P40	LAST	S2600	"6000000003732714443"
#   Q141198375 Astri Torchelsdatter Øvre Time: P40 child = the item just created
Q141198375	P40	LAST	S2600	"6000000003732714443"

# create a new item
CREATE
#   the item just created: set the en label to "Anna Christina Flygare"
LAST	Len	"Anna Christina Flygare"
#   set the mul label to "Anna Christina Flygare"
LAST	Lmul	"Anna Christina Flygare"
#   add a mul alias "Anna Christina Schilling"
LAST	Amul	"Anna Christina Schilling"
#   set the ja label to "アンナ・クリスティーナ・フリガレ"
LAST	Lja	"アンナ・クリスティーナ・フリガレ"
#   set the zh label to "安娜·克里斯蒂娜·夫利加雷"
LAST	Lzh	"安娜·克里斯蒂娜·夫利加雷"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000064143495006 Anna Christina Flygare, qualified P1810 subject named as Anna Christina Schilling
LAST	P2600	"6000000064143495006"	P1810	"Anna Christina Schilling"
#   P569 date of birth = +1720-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P569	+1720-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"6000000064143495006"
#   P570 date of death = +1772-00-00T00:00:00Z/9
LAST	P570	+1772-00-00T00:00:00Z/9	S2600	"6000000064143495006"
#   P25 mother = Q141244107 Margareta Kalsenia
LAST	P25	Q141244107	S2600	"6000000064143495006"
#   Q141244107 Margareta Kalsenia: P40 child = the item just created
Q141244107	P40	LAST	S2600	"6000000064143495006"
#   the item just created: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1083457 Christina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1083457	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Anna Christina von Hermansson"
LAST	Len	"Anna Christina von Hermansson"
#   set the mul label to "Anna Christina von Hermansson"
LAST	Lmul	"Anna Christina von Hermansson"
#   set the ja label to "アンナ・クリスティーナ・ヴォン・ハーマンソン"
LAST	Lja	"アンナ・クリスティーナ・ヴォン・ハーマンソン"
#   set the zh label to "安娜·克里斯蒂娜·翁·赫尔曼松"
LAST	Lzh	"安娜·克里斯蒂娜·翁·赫尔曼松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000009842925791 Anna Christina von Hermansson, qualified P1810 subject named as Anna Christina von Hermansson
LAST	P2600	"6000000009842925791"	P1810	"Anna Christina von Hermansson"
#   P569 date of birth = +1718-00-00T00:00:00Z/9
LAST	P569	+1718-00-00T00:00:00Z/9	S2600	"6000000009842925791"
#   P570 date of death = +1782-00-00T00:00:00Z/9
LAST	P570	+1782-00-00T00:00:00Z/9	S2600	"6000000009842925791"
#   P40 child = Q6080164 Nils Rosén von Rosenstein
LAST	P40	Q6080164	S2600	"6000000009842925791"
#   Q6080164 Nils Rosén von Rosenstein: P25 mother = the item just created
Q6080164	P25	LAST	S2600	"6000000009842925791"
#   the item just created: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1083457 Christina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1083457	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Anna Jonesdatter Tøtland"
LAST	Len	"Anna Jonesdatter Tøtland"
#   set the mul label to "Anna Jonesdatter Tøtland"
LAST	Lmul	"Anna Jonesdatter Tøtland"
#   set the ja label to "アンナ・ヨネスダッテル・トトランド"
LAST	Lja	"アンナ・ヨネスダッテル・トトランド"
#   set the zh label to "安娜·约内斯达特·托特兰德"
LAST	Lzh	"安娜·约内斯达特·托特兰德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000001169317582 Anna Jonesdatter Tøtland, qualified P1810 subject named as Anna Jonesdatter Tøtland
LAST	P2600	"6000000001169317582"	P1810	"Anna Jonesdatter Tøtland"
#   P569 date of birth = +1565-00-00T00:00:00Z/9
LAST	P569	+1565-00-00T00:00:00Z/9	S2600	"6000000001169317582"
#   P570 date of death = +1620-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P570	+1620-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"6000000001169317582"
#   P40 child = Q141205899 Bergitte Ivarsdatter Tjentland
LAST	P40	Q141205899	S2600	"6000000001169317582"
#   Q141205899 Bergitte Ivarsdatter Tjentland: P25 mother = the item just created
Q141205899	P25	LAST	S2600	"6000000001169317582"
#   the item just created: P735 given name = Q666578 Anna
LAST	P735	Q666578
#   add a mul alias "Jonesdatter Tøtland"
LAST	Amul	"Jonesdatter Tøtland"

# create a new item
CREATE
#   set the en label to "Asbjørn Jonson Rønneberg"
LAST	Len	"Asbjørn Jonson Rønneberg"
#   set the mul label to "Asbjørn Jonson Rønneberg"
LAST	Lmul	"Asbjørn Jonson Rønneberg"
#   set the ja label to "アスブヨルン・ヨンソン・レンネベルグ"
LAST	Lja	"アスブヨルン・ヨンソン・レンネベルグ"
#   set the zh label to "阿斯布约尔恩·永松·伦内贝格"
LAST	Lzh	"阿斯布约尔恩·永松·伦内贝格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003491988141 Asbjørn Jonson Rønneberg, qualified P1810 subject named as Asbjørn Jonson Rønneberg
LAST	P2600	"6000000003491988141"	P1810	"Asbjørn Jonson Rønneberg"
#   P569 date of birth = +1778-00-00T00:00:00Z/9
LAST	P569	+1778-00-00T00:00:00Z/9	S2600	"6000000003491988141"
#   P570 date of death = +1778-00-00T00:00:00Z/9
LAST	P570	+1778-00-00T00:00:00Z/9	S2600	"6000000003491988141"
#   P22 father = Q141244102 Jon Torson Røyneberg
LAST	P22	Q141244102	S2600	"6000000003491988141"
#   P25 mother = Q141244209 Berta Asbjørnsdotter Røyneberg
LAST	P25	Q141244209	S2600	"6000000003491988141"
#   Q141244102 Jon Torson Røyneberg: P40 child = the item just created
Q141244102	P40	LAST	S2600	"6000000003491988141"
#   Q141244209 Berta Asbjørnsdotter Røyneberg: P40 child = the item just created
Q141244209	P40	LAST	S2600	"6000000003491988141"
#   the item just created: P735 given name = Q721398 Asbjørn
LAST	P735	Q721398
#   P734 family name = Q7386722 Rønneberg
LAST	P734	Q7386722

# create a new item
CREATE
#   set the en label to "Beata Elisabet Unge"
LAST	Len	"Beata Elisabet Unge"
#   set the mul label to "Beata Elisabet Unge"
LAST	Lmul	"Beata Elisabet Unge"
#   set the ja label to "ベアタ・エリーザベト・ウンゲ"
LAST	Lja	"ベアタ・エリーザベト・ウンゲ"
#   set the zh label to "贝阿塔·伊丽莎白·温盖"
LAST	Lzh	"贝阿塔·伊丽莎白·温盖"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000006911465252 Beata Elisabet Unge, qualified P1810 subject named as Beata Elisabet Unge
LAST	P2600	"6000000006911465252"	P1810	"Beata Elisabet Unge"
#   P569 date of birth = +1753-00-00T00:00:00Z/9
LAST	P569	+1753-00-00T00:00:00Z/9	S2600	"6000000006911465252"
#   P570 date of death = +1801-00-00T00:00:00Z/9
LAST	P570	+1801-00-00T00:00:00Z/9	S2600	"6000000006911465252"
#   P26 spouse = Q139996297 Anders Törnebladh
LAST	P26	Q139996297	S2600	"6000000006911465252"
#   P40 child = Q6218068 Carl Peter Peter Törnebladh
LAST	P40	Q6218068	S2600	"6000000006911465252"
#   Q139996297 Anders Törnebladh: P26 spouse = the item just created
Q139996297	P26	LAST	S2600	"6000000006911465252"
#   Q6218068 Carl Peter Peter Törnebladh: P25 mother = the item just created
Q6218068	P25	LAST	S2600	"6000000006911465252"
#   the item just created: P735 given name = Q338015 Beata, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q338015	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16423275 Elisabet, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q16423275	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Carl Hierta"
LAST	Len	"Carl Hierta"
#   set the mul label to "Carl Hierta"
LAST	Lmul	"Carl Hierta"
#   set the ja label to "カール・ヒエルタ"
LAST	Lja	"カール・ヒエルタ"
#   set the zh label to "卡尔·希埃尔塔"
LAST	Lzh	"卡尔·希埃尔塔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000008508097243 Carl Hierta, qualified P1810 subject named as Carl Hierta
LAST	P2600	"6000000008508097243"	P1810	"Carl Hierta"
#   P569 date of birth = +1702-12-05T00:00:00Z/11, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P569	+1702-12-05T00:00:00Z/11	P1480	Q5727902	S2600	"6000000008508097243"
#   P570 date of death = +1766-02-18T00:00:00Z/11
LAST	P570	+1766-02-18T00:00:00Z/11	S2600	"6000000008508097243"
#   P40 child = Q141244208 Beata Christina Hierta
LAST	P40	Q141244208	S2600	"6000000008508097243"
#   Q141244208 Beata Christina Hierta: P22 father = the item just created
Q141244208	P22	LAST	S2600	"6000000008508097243"
#   the item just created: P735 given name = Q2529610 Carl
LAST	P735	Q2529610

# create a new item
CREATE
#   set the en label to "Christina Fant"
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
#   set the en label to "Fredrika Ulrika Eleonora von Braunjohan"
LAST	Len	"Fredrika Ulrika Eleonora von Braunjohan"
#   set the mul label to "Fredrika Ulrika Eleonora von Braunjohan"
LAST	Lmul	"Fredrika Ulrika Eleonora von Braunjohan"
#   set the ja label to "フレデリカ・ウルリカ・エレオノーラ・ヴォン・ブラウンヨハン"
LAST	Lja	"フレデリカ・ウルリカ・エレオノーラ・ヴォン・ブラウンヨハン"
#   set the zh label to "夫雷德里卡·乌尔里卡·埃莱奥诺拉·翁·布拉温约汉"
LAST	Lzh	"夫雷德里卡·乌尔里卡·埃莱奥诺拉·翁·布拉温约汉"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000008508010957 Fredrika Ulrika Eleonora von Braunjohan, qualified P1810 subject named as Fredrika Ulrika Eleonora von Braunjohan
LAST	P2600	"6000000008508010957"	P1810	"Fredrika Ulrika Eleonora von Braunjohan"
#   P569 date of birth = +1722-05-23T00:00:00Z/11, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P569	+1722-05-23T00:00:00Z/11	P1480	Q5727902	S2600	"6000000008508010957"
#   P570 date of death = +1809-05-14T00:00:00Z/11, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P570	+1809-05-14T00:00:00Z/11	P1480	Q5727902	S2600	"6000000008508010957"
#   P40 child = Q141244208 Beata Christina Hierta
LAST	P40	Q141244208	S2600	"6000000008508010957"
#   Q141244208 Beata Christina Hierta: P25 mother = the item just created
Q141244208	P25	LAST	S2600	"6000000008508010957"

# create a new item
CREATE
#   the item just created: set the en label to "Gustaf Schilling"
LAST	Len	"Gustaf Schilling"
#   set the mul label to "Gustaf Schilling"
LAST	Lmul	"Gustaf Schilling"
#   set the ja label to "グスタフ・シリング"
LAST	Lja	"グスタフ・シリング"
#   set the zh label to "古斯塔夫·西林"
LAST	Lzh	"古斯塔夫·西林"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000180950236868 Gustaf Schilling, qualified P1810 subject named as Gustaf Schilling
LAST	P2600	"6000000180950236868"	P1810	"Gustaf Schilling"
#   P569 date of birth = +1674-12-25T00:00:00Z/11
LAST	P569	+1674-12-25T00:00:00Z/11	S2600	"6000000180950236868"
#   P570 date of death = +1723-03-14T00:00:00Z/11
LAST	P570	+1723-03-14T00:00:00Z/11	S2600	"6000000180950236868"
#   P26 spouse = Q141244107 Margareta Kalsenia
LAST	P26	Q141244107	S2600	"6000000180950236868"
#   Q141244107 Margareta Kalsenia: P26 spouse = the item just created
Q141244107	P26	LAST	S2600	"6000000180950236868"
#   the item just created: P735 given name = Q15646212 Gustaf
LAST	P735	Q15646212

# create a new item
CREATE
#   set the en label to "Hans Olofsson Törne"
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
#   set the en label to "Henriette Wilhelmine Kjelsen"
LAST	Len	"Henriette Wilhelmine Kjelsen"
#   set the mul label to "Henriette Wilhelmine Kjelsen"
LAST	Lmul	"Henriette Wilhelmine Kjelsen"
#   set the ja label to "アンリエット・ヴィルヘルミーネ・ヒェルセン"
LAST	Lja	"アンリエット・ヴィルヘルミーネ・ヒェルセン"
#   set the zh label to "亨丽埃特·威廉明妮·谢尔森"
LAST	Lzh	"亨丽埃特·威廉明妮·谢尔森"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000021080450944 Henriette Wilhelmine Kjelsen, qualified P1810 subject named as Henriette Wilhelmine Kjelsen
LAST	P2600	"6000000021080450944"	P1810	"Henriette Wilhelmine Kjelsen"
#   P569 date of birth = +1837-03-13T00:00:00Z/11
LAST	P569	+1837-03-13T00:00:00Z/11	S2600	"6000000021080450944"
#   P570 date of death = +1935-04-01T00:00:00Z/11
LAST	P570	+1935-04-01T00:00:00Z/11	S2600	"6000000021080450944"
#   P40 child = Q141216386 Jens Wilhelm Wendt
LAST	P40	Q141216386	S2600	"6000000021080450944"
#   Q141216386 Jens Wilhelm Wendt: P25 mother = the item just created
Q141216386	P25	LAST	S2600	"6000000021080450944"
#   the item just created: P735 given name = Q19688844 Henriette, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q19688844	P1545	"1"	P7452	Q3409033
#   P735 given name = Q15728223 Wilhelmine, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q15728223	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Ingrid Charlotta Carlsdotter Ekenbom"
LAST	Len	"Ingrid Charlotta Carlsdotter Ekenbom"
#   set the mul label to "Ingrid Charlotta Carlsdotter Ekenbom"
LAST	Lmul	"Ingrid Charlotta Carlsdotter Ekenbom"
#   add a mul alias "Ingrid Charlotta Carlsdotter Hansson"
LAST	Amul	"Ingrid Charlotta Carlsdotter Hansson"
#   set the ja label to "イングリッド・カルロタ・カルルスドッテル・エケンボム"
LAST	Lja	"イングリッド・カルロタ・カルルスドッテル・エケンボム"
#   set the zh label to "英格丽·卡尔洛塔·卡尔尔斯多特·埃肯博姆"
LAST	Lzh	"英格丽·卡尔洛塔·卡尔尔斯多特·埃肯博姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000000410527402 Ingrid Charlotta Carlsdotter Ekenbom, qualified P1810 subject named as Ingrid Charlotta Carlsdotter Hansson
LAST	P2600	"6000000000410527402"	P1810	"Ingrid Charlotta Carlsdotter Hansson"
#   P569 date of birth = +1627-11-06T00:00:00Z/11
LAST	P569	+1627-11-06T00:00:00Z/11	S2600	"6000000000410527402"
#   P570 date of death = +1703-00-00T00:00:00Z/9
LAST	P570	+1703-00-00T00:00:00Z/9	S2600	"6000000000410527402"
#   P40 child = Q141223930 Magdalena Törne
LAST	P40	Q141223930	S2600	"6000000000410527402"
#   Q141223930 Magdalena Törne: P25 mother = the item just created
Q141223930	P25	LAST	S2600	"6000000000410527402"
#   the item just created: P735 given name = Q903741 Ingrid, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q903741	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1067071	P1545	"2"	P3831	Q245025
#   add a mul alias "Ingrid Charlotta Ekenbom"
LAST	Amul	"Ingrid Charlotta Ekenbom"

# create a new item
CREATE
#   set the en label to "Ivar Toreson Tjentland"
LAST	Len	"Ivar Toreson Tjentland"
#   set the mul label to "Ivar Toreson Tjentland"
LAST	Lmul	"Ivar Toreson Tjentland"
#   set the ja label to "イヴァル・トレソン・トイェントランド"
LAST	Lja	"イヴァル・トレソン・トイェントランド"
#   set the zh label to "伊瓦尔·托雷松·特延特兰德"
LAST	Lzh	"伊瓦尔·托雷松·特延特兰德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000001169232790 Ivar Toreson Tjentland, qualified P1810 subject named as Ivar Toreson Tjentland
LAST	P2600	"6000000001169232790"	P1810	"Ivar Toreson Tjentland"
#   P569 date of birth = +1560-00-00T00:00:00Z/9
LAST	P569	+1560-00-00T00:00:00Z/9	S2600	"6000000001169232790"
#   P570 date of death = +1640-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P570	+1640-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"6000000001169232790"
#   P40 child = Q141205899 Bergitte Ivarsdatter Tjentland
LAST	P40	Q141205899	S2600	"6000000001169232790"
#   Q141205899 Bergitte Ivarsdatter Tjentland: P22 father = the item just created
Q141205899	P22	LAST	S2600	"6000000001169232790"
#   the item just created: P735 given name = Q127069 Ivar
LAST	P735	Q127069

# create a new item
CREATE
#   set the en label to "Justina Elisabet Schotte"
LAST	Len	"Justina Elisabet Schotte"
#   set the mul label to "Justina Elisabet Schotte"
LAST	Lmul	"Justina Elisabet Schotte"
#   set the ja label to "ジャスティナ・エリーザベト・ショテ"
LAST	Lja	"ジャスティナ・エリーザベト・ショテ"
#   set the zh label to "尤斯蒂纳·伊丽莎白·肖特"
LAST	Lzh	"尤斯蒂纳·伊丽莎白·肖特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000018964557693 Justina Elisabet Schotte, qualified P1810 subject named as Justina Elisabet Schotte
LAST	P2600	"6000000018964557693"	P1810	"Justina Elisabet Schotte"
#   P569 date of birth = +1757-10-03T00:00:00Z/11
LAST	P569	+1757-10-03T00:00:00Z/11	S2600	"6000000018964557693"
#   P570 date of death = +1805-02-22T00:00:00Z/11
LAST	P570	+1805-02-22T00:00:00Z/11	S2600	"6000000018964557693"
#   P40 child = Q16650430 Per Gustaf G. Svedelius
LAST	P40	Q16650430	S2600	"6000000018964557693"
#   Q16650430 Per Gustaf G. Svedelius: P25 mother = the item just created
Q16650430	P25	LAST	S2600	"6000000018964557693"
#   the item just created: P735 given name = Q18211002 Justina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q18211002	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16423275 Elisabet, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q16423275	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Jørgen Anton Wendt"
LAST	Len	"Jørgen Anton Wendt"
#   set the mul label to "Jørgen Anton Wendt"
LAST	Lmul	"Jørgen Anton Wendt"
#   set the ja label to "ヨルゲン・アントン・ヴェント"
LAST	Lja	"ヨルゲン・アントン・ヴェント"
#   set the zh label to "约尔根·安东·温特"
LAST	Lzh	"约尔根·安东·温特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000021080514848 Jørgen Anton Wendt, qualified P1810 subject named as Jørgen Anton Wendt
LAST	P2600	"6000000021080514848"	P1810	"Jørgen Anton Wendt"
#   P569 date of birth = +1824-00-00T00:00:00Z/9
LAST	P569	+1824-00-00T00:00:00Z/9	S2600	"6000000021080514848"
#   P570 date of death = +1866-00-00T00:00:00Z/9
LAST	P570	+1866-00-00T00:00:00Z/9	S2600	"6000000021080514848"
#   P40 child = Q141216386 Jens Wilhelm Wendt
LAST	P40	Q141216386	S2600	"6000000021080514848"
#   Q141216386 Jens Wilhelm Wendt: P22 father = the item just created
Q141216386	P22	LAST	S2600	"6000000021080514848"
#   the item just created: P735 given name = Q13409273 Jørgen, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q13409273	P1545	"1"	P7452	Q3409033
#   P735 given name = Q5401576 Anton, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q5401576	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Lovisa Sofia Benzelstierna"
LAST	Len	"Lovisa Sofia Benzelstierna"
#   set the mul label to "Lovisa Sofia Benzelstierna"
LAST	Lmul	"Lovisa Sofia Benzelstierna"
#   add a mul alias "Lovisa Sofia Bratt"
LAST	Amul	"Lovisa Sofia Bratt"
#   set the ja label to "ロヴィサ・ソフィア・ベンゼルスティエルナ"
LAST	Lja	"ロヴィサ・ソフィア・ベンゼルスティエルナ"
#   set the zh label to "洛维萨·索菲娅·本泽尔斯蒂埃尔纳"
LAST	Lzh	"洛维萨·索菲娅·本泽尔斯蒂埃尔纳"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000030305287826 Lovisa Sofia Benzelstierna, qualified P1810 subject named as Lovisa Sofia Bratt
LAST	P2600	"6000000030305287826"	P1810	"Lovisa Sofia Bratt"
#   P569 date of birth = +1739-10-07T00:00:00Z/11
LAST	P569	+1739-10-07T00:00:00Z/11	S2600	"6000000030305287826"
#   P570 date of death = +1780-03-24T00:00:00Z/11
LAST	P570	+1780-03-24T00:00:00Z/11	S2600	"6000000030305287826"
#   P26 spouse = Q141224756 Carl Benzelstierna
LAST	P26	Q141224756	S2600	"6000000030305287826"
#   Q141224756 Carl Benzelstierna: P26 spouse = the item just created
Q141224756	P26	LAST	S2600	"6000000030305287826"
#   the item just created: P735 given name = Q10570000 Lovisa, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q10570000	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q18201520	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Malena Olsdatter Tjåland"
LAST	Len	"Malena Olsdatter Tjåland"
#   set the mul label to "Malena Olsdatter Tjåland"
LAST	Lmul	"Malena Olsdatter Tjåland"
#   set the ja label to "マレーナ・オルスダッテル・トヨーランド"
LAST	Lja	"マレーナ・オルスダッテル・トヨーランド"
#   set the zh label to "马莱纳·奥尔斯达特·特约兰德"
LAST	Lzh	"马莱纳·奥尔斯达特·特约兰德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005609534715 Malena Olsdatter Tjåland *, qualified P1810 subject named as Malena Olsdatter Tjåland *
LAST	P2600	"6000000005609534715"	P1810	"Malena Olsdatter Tjåland *"
#   P40 child = Q141242542 Kristoffer Olson Tjåland
LAST	P40	Q141242542	S2600	"6000000005609534715"
#   Q141242542 Kristoffer Olson Tjåland: P25 mother = the item just created
Q141242542	P25	LAST	S2600	"6000000005609534715"
#   the item just created: P735 given name = Q5990536 Malena
LAST	P735	Q5990536
#   P5056 patronym or matronym = Q51885688 Olsdatter
LAST	P5056	Q51885688

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
#   set the en label to "Maria Elisabet Lagerfelt"
LAST	Len	"Maria Elisabet Lagerfelt"
#   set the mul label to "Maria Elisabet Lagerfelt"
LAST	Lmul	"Maria Elisabet Lagerfelt"
#   set the ja label to "マリア・エリーザベト・ラゲルフェルト"
LAST	Lja	"マリア・エリーザベト・ラゲルフェルト"
#   set the zh label to "玛丽亚·伊丽莎白·拉盖尔费尔特"
LAST	Lzh	"玛丽亚·伊丽莎白·拉盖尔费尔特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000008840834179 Maria Elisabet Lagerfelt, qualified P1810 subject named as Maria Elisabet Lagerfelt
LAST	P2600	"6000000008840834179"	P1810	"Maria Elisabet Lagerfelt"
#   P569 date of birth = +1701-11-03T00:00:00Z/11
LAST	P569	+1701-11-03T00:00:00Z/11	S2600	"6000000008840834179"
#   P570 date of death = +1726-04-13T00:00:00Z/11
LAST	P570	+1726-04-13T00:00:00Z/11	S2600	"6000000008840834179"
#   P22 father = Q109835397 Carl Gustaf Lagerfelt
LAST	P22	Q109835397	S2600	"6000000008840834179"
#   P25 mother = Q109835398 Maria Elisabet von der Osten
LAST	P25	Q109835398	S2600	"6000000008840834179"
#   Q109835397 Carl Gustaf Lagerfelt: P40 child = the item just created
Q109835397	P40	LAST	S2600	"6000000008840834179"
#   Q109835398 Maria Elisabet von der Osten: P40 child = the item just created
Q109835398	P40	LAST	S2600	"6000000008840834179"
#   the item just created: P735 given name = Q325872 Maria, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q325872	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16423275 Elisabet, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q16423275	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Ola Kristoffersen Kartevoll"
LAST	Len	"Ola Kristoffersen Kartevoll"
#   set the mul label to "Ola Kristoffersen Kartevoll"
LAST	Lmul	"Ola Kristoffersen Kartevoll"
#   set the ja label to "オーラ・クリストフェルセン・カルテヴォル"
LAST	Lja	"オーラ・クリストフェルセン・カルテヴォル"
#   set the zh label to "奥拉·克里斯托费尔森·卡尔特沃尔"
LAST	Lzh	"奥拉·克里斯托费尔森·卡尔特沃尔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000002801159071 Ola Kristoffersen Kartevoll *, qualified P1810 subject named as Ola Kristoffersen Kartevoll *
LAST	P2600	"6000000002801159071"	P1810	"Ola Kristoffersen Kartevoll *"
#   P569 date of birth = +1649-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P569	+1649-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"6000000002801159071"
#   P570 date of death = +1741-05-00T00:00:00Z/10
LAST	P570	+1741-05-00T00:00:00Z/10	S2600	"6000000002801159071"
#   P40 child = Q141242542 Kristoffer Olson Tjåland
LAST	P40	Q141242542	S2600	"6000000002801159071"
#   Q141242542 Kristoffer Olson Tjåland: P22 father = the item just created
Q141242542	P22	LAST	S2600	"6000000002801159071"
#   the item just created: P735 given name = Q96675523 Ola
LAST	P735	Q96675523
#   add a mul alias "Tjåland Kartevoll"
LAST	Amul	"Tjåland Kartevoll"

# create a new item
CREATE
#   set the en label to "Ola Pederson Foss"
LAST	Len	"Ola Pederson Foss"
#   set the mul label to "Ola Pederson Foss"
LAST	Lmul	"Ola Pederson Foss"
#   set the ja label to "オーラ・ペデルソン・フォス"
LAST	Lja	"オーラ・ペデルソン・フォス"
#   set the zh label to "奥拉·佩德尔松·福斯"
LAST	Lzh	"奥拉·佩德尔松·福斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005607362393 Ola Pederson Foss, qualified P1810 subject named as Ola Pederson Foss
LAST	P2600	"6000000005607362393"	P1810	"Ola Pederson Foss"
#   P569 date of birth = +1612-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P569	+1612-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"6000000005607362393"
#   P570 date of death = +1691-00-00T00:00:00Z/9
LAST	P570	+1691-00-00T00:00:00Z/9	S2600	"6000000005607362393"
#   P22 father = Q141206080 Peder Tormodsen Foss
LAST	P22	Q141206080	S2600	"6000000005607362393"
#   P25 mother = Q141206061 Cecilie Olsdatter Håland
LAST	P25	Q141206061	S2600	"6000000005607362393"
#   Q141206080 Peder Tormodsen Foss: P40 child = the item just created
Q141206080	P40	LAST	S2600	"6000000005607362393"
#   Q141206061 Cecilie Olsdatter Håland: P40 child = the item just created
Q141206061	P40	LAST	S2600	"6000000005607362393"

# create a new item
CREATE
#   the item just created: set the en label to "Olof Bratt Benzelstierna"
LAST	Len	"Olof Bratt Benzelstierna"
#   set the mul label to "Olof Bratt Benzelstierna"
LAST	Lmul	"Olof Bratt Benzelstierna"
#   set the ja label to "オロフ・ブラト・ベンゼルスティエルナ"
LAST	Lja	"オロフ・ブラト・ベンゼルスティエルナ"
#   set the zh label to "奥洛夫·布拉特·本泽尔斯蒂埃尔纳"
LAST	Lzh	"奥洛夫·布拉特·本泽尔斯蒂埃尔纳"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000192504935864 Olof Bratt Benzelstierna, qualified P1810 subject named as Olof Bratt Benzelstierna
LAST	P2600	"6000000192504935864"	P1810	"Olof Bratt Benzelstierna"
#   P22 father = Q141224756 Carl Benzelstierna
LAST	P22	Q141224756	S2600	"6000000192504935864"
#   Q141224756 Carl Benzelstierna: P40 child = the item just created
Q141224756	P40	LAST	S2600	"6000000192504935864"
#   the item just created: P735 given name = Q18089653 Olof
LAST	P735	Q18089653

# create a new item
CREATE
#   set the en label to "Samuel Ugla"
LAST	Len	"Samuel Ugla"
#   set the mul label to "Samuel Ugla"
LAST	Lmul	"Samuel Ugla"
#   set the ja label to "サミュエル・ウグラ"
LAST	Lja	"サミュエル・ウグラ"
#   set the zh label to "塞缪尔·乌格拉"
LAST	Lzh	"塞缪尔·乌格拉"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000018089329158 Samuel Ugla, qualified P1810 subject named as Samuel Ugla
LAST	P2600	"6000000018089329158"	P1810	"Samuel Ugla"
#   P569 date of birth = +1678-05-26T00:00:00Z/11
LAST	P569	+1678-05-26T00:00:00Z/11	S2600	"6000000018089329158"
#   P570 date of death = +1743-01-27T00:00:00Z/11
LAST	P570	+1743-01-27T00:00:00Z/11	S2600	"6000000018089329158"
#   P40 child = Q124608453 Petrus Ugla
LAST	P40	Q124608453	S2600	"6000000018089329158"
#   Q124608453 Petrus Ugla: P22 father = the item just created
Q124608453	P22	LAST	S2600	"6000000018089329158"
#   the item just created: P735 given name = Q629347 Samuel
LAST	P735	Q629347

# create a new item
CREATE
#   set the en label to "Sofia Helena Mannerheim"
LAST	Len	"Sofia Helena Mannerheim"
#   set the mul label to "Sofia Helena Mannerheim"
LAST	Lmul	"Sofia Helena Mannerheim"
#   set the ja label to "ソフィア・ヘレナ・マンネルヘイム"
LAST	Lja	"ソフィア・ヘレナ・マンネルヘイム"
#   set the zh label to "索菲娅·海伦娜·曼纳海姆"
LAST	Lzh	"索菲娅·海伦娜·曼纳海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000000047222573 Sofia Helena Mannerheim, qualified P1810 subject named as Sofia Helena Mannerheim
LAST	P2600	"6000000000047222573"	P1810	"Sofia Helena Mannerheim"
#   P569 date of birth = +1794-04-15T00:00:00Z/11
LAST	P569	+1794-04-15T00:00:00Z/11	S2600	"6000000000047222573"
#   P570 date of death = +1854-09-09T00:00:00Z/11
LAST	P570	+1854-09-09T00:00:00Z/11	S2600	"6000000000047222573"
#   P22 father = Q5975022 Lars August Mannerheim
LAST	P22	Q5975022	S2600	"6000000000047222573"
#   P25 mother = Q141219332 Sofia Wadenstierna
LAST	P25	Q141219332	S2600	"6000000000047222573"
#   Q5975022 Lars August Mannerheim: P40 child = the item just created
Q5975022	P40	LAST	S2600	"6000000000047222573"
#   Q141219332 Sofia Wadenstierna: P40 child = the item just created
Q141219332	P40	LAST	S2600	"6000000000047222573"
#   the item just created: P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q18201520	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1035239 Helena, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1035239	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Stephen Frisk"
LAST	Len	"Stephen Frisk"
#   set the mul label to "Stephen Frisk"
LAST	Lmul	"Stephen Frisk"
#   set the ja label to "ステプヘン・フリスク"
LAST	Lja	"ステプヘン・フリスク"
#   set the zh label to "斯特普亨·弗里斯克"
LAST	Lzh	"斯特普亨·弗里斯克"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000178116652845 Stephen Frisk, qualified P1810 subject named as Stephen Frisk
LAST	P2600	"6000000178116652845"	P1810	"Stephen Frisk"
#   P22 father = Q141223733 Hans Bertil Frisk
LAST	P22	Q141223733	S2600	"6000000178116652845"
#   P25 mother = Q141223907 Elly Olivia Frisk
LAST	P25	Q141223907	S2600	"6000000178116652845"
#   Q141223733 Hans Bertil Frisk: P40 child = the item just created
Q141223733	P40	LAST	S2600	"6000000178116652845"
#   Q141223907 Elly Olivia Frisk: P40 child = the item just created
Q141223907	P40	LAST	S2600	"6000000178116652845"
#   Q141244224 Justina Sophie Naucler: P735 given name = Q14942517 Sophie, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141244224	P735	Q14942517	P1545	"2"	P3831	Q245025
#   Q141244207 Anna M. Ekman: P3373 sibling = Q141223423 Harlverg B. Ekman
Q141244207	P3373	Q141223423	S2600	"285884854200005085"
#   P3373 sibling = Q141205908 Gotfred Olai Ekman
Q141244207	P3373	Q141205908	S2600	"285884854200005085"
#   Q141223423 Harlverg B. Ekman: P3373 sibling = Q141244207 Anna M. Ekman
Q141223423	P3373	Q141244207	S2600	"285886949080005081"
#   Q141244225 Karl Nilsson Polviander: P26 spouse = Q141244229 Margareta Katarina Polviander
Q141244225	P26	Q141244229	S2600	"6000000001966670019"
#   Q141244231 Ola Olson Bæreim: P26 spouse = Q141244216 Eli Olsdatter Bærheim
Q141244231	P26	Q141244216	S2600	"6000000002226706375"
#   Q141244226 Knut Bjørnson Bjørheim: P22 father = Q141244210 Bjørn Lauritsen Bjørheim
Q141244226	P22	Q141244210	S2600	"6000000002277957043"
#   Q141244210 Bjørn Lauritsen Bjørheim: P40 child = Q141244226 Knut Bjørnson Bjørheim
Q141244210	P40	Q141244226	S2600	"6000000002330809317"
#   Q141189070 John Jonassen Hegre: P40 child = Q138687615 Bertrand Olav Olsen Vigdel
Q141189070	P40	Q138687615	S2600	"6000000003491986951"
#   Q141244234 Torstein Gunnarson Frafjord: P26 spouse = Q141244227 Kristi Frafjord
Q141244234	P26	Q141244227	S2600	"6000000005607365222"
#   Q141244216 Eli Olsdatter Bærheim: P26 spouse = Q141244231 Ola Olson Bæreim
Q141244216	P26	Q141244231	S2600	"6000000006776171569"
#   Q141244212 Carl Åke Posse af Säby: P26 spouse = Q141244208 Beata Christina Hierta
Q141244212	P26	Q141244208	S2600	"6000000008507821635"
#   Q141244208 Beata Christina Hierta: P26 spouse = Q141244212 Carl Åke Posse af Säby
Q141244208	P26	Q141244212	S2600	"6000000008507926141"
#   Q141244229 Margareta Katarina Polviander: P26 spouse = Q141244225 Karl Nilsson Polviander
Q141244229	P26	Q141244225	S2600	"6000000012232723402"
#   Q141244227 Kristi Frafjord: P26 spouse = Q141244234 Torstein Gunnarson Frafjord
Q141244227	P26	Q141244234	S2600	"6000000014233913271"
#   Q141205896 Ane Marie Konstanse Amanda Kristine Hegre: P40 child = Q138687615 Bertrand Olav Olsen Vigdel
Q141205896	P40	Q138687615	S2600	"6000000018935780138"

