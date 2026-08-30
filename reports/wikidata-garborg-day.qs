# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   729 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   set the zh label to "拉斯穆斯·谢蒂尔松·赫勒"
Q141200067	Lzh	"拉斯穆斯·谢蒂尔松·赫勒"
#   Q141198831 Peder Larsen Mjølhus: set the ja label to "ペーダー・ラーセン・ムヨルフス"
Q141198831	Lja	"ペーダー・ラーセン・ムヨルフス"
#   set the zh label to "彼泽·拉森·姆约尔胡斯"
Q141198831	Lzh	"彼泽·拉森·姆约尔胡斯"
#   Q141219069 Søren Sørenson Gjesdal: set the ja label to "セーレン・ソレンソン・イェスダール"
Q141219069	Lja	"セーレン・ソレンソン・イェスダール"
#   set the zh label to "索伦·索雷恩松·耶斯达尔"
Q141219069	Lzh	"索伦·索雷恩松·耶斯达尔"
#   Q141216471 Gunnbjørn Gunnbjørnson Rossavik: set the ja label to "グンンブヨルン・グンンブヨルンソン・ロサヴィク"
Q141216471	Lja	"グンンブヨルン・グンンブヨルンソン・ロサヴィク"
#   set the zh label to "贡布约尔恩·贡布约尔恩松·罗萨维克"
Q141216471	Lzh	"贡布约尔恩·贡布约尔恩松·罗萨维克"
#   Q141198435 Jon Nilsson Espedal: set the ja label to "ジョン・ニルソン・エスペダール"
Q141198435	Lja	"ジョン・ニルソン・エスペダール"
#   set the zh label to "乔恩·尼尔松·埃斯佩达尔"
Q141198435	Lzh	"乔恩·尼尔松·埃斯佩达尔"
#   Q141198503 Tore Erikson Håland: set the ja label to "トーレ・エリクソン・ホーランド"
Q141198503	Lja	"トーレ・エリクソン・ホーランド"
#   set the zh label to "托雷·埃里克松·霍兰"
Q141198503	Lzh	"托雷·埃里克松·霍兰"
#   Q10608167 Olaus Petri Niurenius: set the ja label to "オラウス・ペトリ・ニウレニウス"
Q10608167	Lja	"オラウス・ペトリ・ニウレニウス"
#   set the zh label to "奥劳斯·佩特里·尼乌雷尼乌斯"
Q10608167	Lzh	"奥劳斯·佩特里·尼乌雷尼乌斯"
#   Q141205932 Olof Timmerman: set the ja label to "オロフ・ティメルマン"
Q141205932	Lja	"オロフ・ティメルマン"
#   set the zh label to "奥洛夫·蒂梅尔曼"
Q141205932	Lzh	"奥洛夫·蒂梅尔曼"

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the mul label to ""
LAST	Lmul	""
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000184732963823
LAST	P2600	"6000000184732963823"
#   P26 spouse = Q141216500 NN Private
LAST	P26	Q141216500	S2600	"6000000184732963823"
#   P40 child = Q141223549 NN Private
LAST	P40	Q141223549	S2600	"6000000184732963823"
#   Q141216500 NN Private: P26 spouse = the item just created
Q141216500	P26	LAST	S2600	"6000000184732963823"
#   Q141223549 NN Private: P25 mother = the item just created
Q141223549	P25	LAST	S2600	"6000000184732963823"

# create a new item
CREATE
#   the item just created: set the mul label to "NN Wendt"
LAST	Lmul	"NN Wendt"
#   set the ca label to "fill de Erling Juel Wendt"
LAST	Lca	"fill de Erling Juel Wendt"
#   set the da label to "søn af Erling Juel Wendt"
LAST	Lda	"søn af Erling Juel Wendt"
#   set the de label to "Sohn von Erling Juel Wendt"
LAST	Lde	"Sohn von Erling Juel Wendt"
#   set the en label to "son of Erling Juel Wendt"
LAST	Len	"son of Erling Juel Wendt"
#   set the es label to "hijo de Erling Juel Wendt"
LAST	Les	"hijo de Erling Juel Wendt"
#   set the it label to "figlio di Erling Juel Wendt"
LAST	Lit	"figlio di Erling Juel Wendt"
#   set the ja label to "エーリング・ユール・ヴェントの息子"
LAST	Lja	"エーリング・ユール・ヴェントの息子"
#   set the nb label to "sønn av Erling Juel Wendt"
LAST	Lnb	"sønn av Erling Juel Wendt"
#   set the nl label to "zoon van Erling Juel Wendt"
LAST	Lnl	"zoon van Erling Juel Wendt"
#   set the pt label to "filho de Erling Juel Wendt"
LAST	Lpt	"filho de Erling Juel Wendt"
#   set the sv label to "son till Erling Juel Wendt"
LAST	Lsv	"son till Erling Juel Wendt"
#   set the zh label to "埃尔林·尤埃尔·温特之子"
LAST	Lzh	"埃尔林·尤埃尔·温特之子"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000226088890841 NN Wendt
LAST	P2600	"6000000226088890841"
#   P22 father = Q141198396 Erling Juel Wendt
LAST	P22	Q141198396	S2600	"6000000226088890841"
#   P25 mother = Q141168784 Aagot Wendt
LAST	P25	Q141168784	S2600	"6000000226088890841"
#   Q141198396 Erling Juel Wendt: P40 child = the item just created
Q141198396	P40	LAST	S2600	"6000000226088890841"
#   Q141168784 Aagot Wendt: P40 child = the item just created
Q141168784	P40	LAST	S2600	"6000000226088890841"

# create a new item
CREATE
#   the item just created: set the en label to "Brita Maria Alenius"
LAST	Len	"Brita Maria Alenius"
#   set the mul label to "Brita Maria Alenius"
LAST	Lmul	"Brita Maria Alenius"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000021333571691 Brita Maria Alenius, qualified P1810 subject named as Brita Maria Alenius
LAST	P2600	"6000000021333571691"	P1810	"Brita Maria Alenius"
#   P569 date of birth = +1746-04-00T00:00:00Z/10
LAST	P569	+1746-04-00T00:00:00Z/10	S2600	"6000000021333571691"
#   P570 date of death = +1809-12-29T00:00:00Z/11
LAST	P570	+1809-12-29T00:00:00Z/11	S2600	"6000000021333571691"
#   P40 child = Q5955392 Johan Anders Johansson Linder
LAST	P40	Q5955392	S2600	"6000000021333571691"
#   Q5955392 Johan Anders Johansson Linder: P25 mother = the item just created
Q5955392	P25	LAST	S2600	"6000000021333571691"
#   the item just created: P735 given name = Q918013, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q918013	P1545	"1"	P7452	Q3409033
#   P735 given name = Q325872 Maria, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q325872	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Brita Schytte"
LAST	Len	"Brita Schytte"
#   set the mul label to "Brita Schytte"
LAST	Lmul	"Brita Schytte"
#   set the ja label to "ブリッタ・シテ"
LAST	Lja	"ブリッタ・シテ"
#   set the zh label to "布里塔·西特"
LAST	Lzh	"布里塔·西特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000012901496092 Brita Schytte, qualified P1810 subject named as Brita Schytte
LAST	P2600	"6000000012901496092"	P1810	"Brita Schytte"
#   P569 date of birth = +1623-11-10T00:00:00Z/11
LAST	P569	+1623-11-10T00:00:00Z/11	S2600	"6000000012901496092"
#   P570 date of death = +1668-05-18T00:00:00Z/11
LAST	P570	+1668-05-18T00:00:00Z/11	S2600	"6000000012901496092"
#   P26 spouse = Q5568857 Daniel Jonsson Behmer
LAST	P26	Q5568857	S2600	"6000000012901496092"
#   P40 child = Q141223499 Anna Danielsdotter Behmer
LAST	P40	Q141223499	S2600	"6000000012901496092"
#   Q5568857 Daniel Jonsson Behmer: P26 spouse = the item just created
Q5568857	P26	LAST	S2600	"6000000012901496092"
#   Q141223499 Anna Danielsdotter Behmer: P25 mother = the item just created
Q141223499	P25	LAST	S2600	"6000000012901496092"
#   the item just created: P735 given name = Q918013
LAST	P735	Q918013
#   P734 family name = Q30132664 Schytte, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q30132664	P3831	Q28418670

# create a new item
CREATE
#   set the en label to "Christina Brigitta Rydberg"
LAST	Len	"Christina Brigitta Rydberg"
#   set the mul label to "Christina Brigitta Rydberg"
LAST	Lmul	"Christina Brigitta Rydberg"
#   set the ja label to "クリスティーナ・ブリギッタ・リュードベリ"
LAST	Lja	"クリスティーナ・ブリギッタ・リュードベリ"
#   set the zh label to "克里斯蒂娜·布里吉塔·里德贝尔格"
LAST	Lzh	"克里斯蒂娜·布里吉塔·里德贝尔格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000019467862742 Christina Brigitta Rydberg, qualified P1810 subject named as Christina Brigitta Rydberg
LAST	P2600	"6000000019467862742"	P1810	"Christina Brigitta Rydberg"
#   P569 date of birth = +1762-09-22T00:00:00Z/11
LAST	P569	+1762-09-22T00:00:00Z/11	S2600	"6000000019467862742"
#   P570 date of death = +1802-01-03T00:00:00Z/11
LAST	P570	+1802-01-03T00:00:00Z/11	S2600	"6000000019467862742"
#   P26 spouse = Q5725105 Eric Michael Fant
LAST	P26	Q5725105	S2600	"6000000019467862742"
#   Q5725105 Eric Michael Fant: P26 spouse = the item just created
Q5725105	P26	LAST	S2600	"6000000019467862742"
#   the item just created: P735 given name = Q1083457 Christina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q1083457	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18190928 Brigitta, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q18190928	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Constantia Fehman"
LAST	Len	"Constantia Fehman"
#   set the mul label to "Constantia Fehman"
LAST	Lmul	"Constantia Fehman"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000001920682589 Constantia Fehman, qualified P1810 subject named as Constantia Fehman
LAST	P2600	"6000000001920682589"	P1810	"Constantia Fehman"
#   P569 date of birth = +1698-12-00T00:00:00Z/10
LAST	P569	+1698-12-00T00:00:00Z/10	S2600	"6000000001920682589"
#   P570 date of death = +1766-03-20T00:00:00Z/11
LAST	P570	+1766-03-20T00:00:00Z/11	S2600	"6000000001920682589"
#   P40 child = Q16650516 Mikael von Törne
LAST	P40	Q16650516	S2600	"6000000001920682589"
#   Q16650516 Mikael von Törne: P25 mother = the item just created
Q16650516	P25	LAST	S2600	"6000000001920682589"
#   the item just created: P735 given name = Q1127708 Constantia
LAST	P735	Q1127708

# create a new item
CREATE
#   set the en label to "Gustava Fant"
LAST	Len	"Gustava Fant"
#   set the mul label to "Gustava Fant"
LAST	Lmul	"Gustava Fant"
#   set the ja label to "グスタヴァ・ファント"
LAST	Lja	"グスタヴァ・ファント"
#   set the zh label to "古斯塔娃·凡特"
LAST	Lzh	"古斯塔娃·凡特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000019352071101 Gustava Fant, qualified P1810 subject named as Gustava Fant
LAST	P2600	"6000000019352071101"	P1810	"Gustava Fant"
#   P569 date of birth = +1792-03-31T00:00:00Z/11
LAST	P569	+1792-03-31T00:00:00Z/11	S2600	"6000000019352071101"
#   P570 date of death = +1835-02-28T00:00:00Z/11
LAST	P570	+1835-02-28T00:00:00Z/11	S2600	"6000000019352071101"
#   P22 father = Q5725105 Eric Michael Fant
LAST	P22	Q5725105	S2600	"6000000019352071101"
#   Q5725105 Eric Michael Fant: P40 child = the item just created
Q5725105	P40	LAST	S2600	"6000000019352071101"
#   the item just created: P735 given name = Q21144392 Gustava
LAST	P735	Q21144392

# create a new item
CREATE
#   set the en label to "Guttorm Guttormsson"
LAST	Len	"Guttorm Guttormsson"
#   set the mul label to "Guttorm Guttormsson"
LAST	Lmul	"Guttorm Guttormsson"
#   set the ja label to "グットルム・グトルムソン"
LAST	Lja	"グットルム・グトルムソン"
#   set the zh label to "古托尔姆·古托尔姆松"
LAST	Lzh	"古托尔姆·古托尔姆松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000040760707837 Guttorm Guttormsson, qualified P1810 subject named as Guttorm Guttormsson
LAST	P2600	"6000000040760707837"	P1810	"Guttorm Guttormsson"
#   P569 date of birth = +1165-00-00T00:00:00Z/9
LAST	P569	+1165-00-00T00:00:00Z/9	S2600	"6000000040760707837"
#   P570 date of death = +1240-00-00T00:00:00Z/9
LAST	P570	+1240-00-00T00:00:00Z/9	S2600	"6000000040760707837"
#   P22 father = Q10511224 Guttorm Ostmannson of Jämtland & Svealand
LAST	P22	Q10511224	S2600	"6000000040760707837"
#   Q10511224 Guttorm Ostmannson of Jämtland & Svealand: P40 child = the item just created
Q10511224	P40	LAST	S2600	"6000000040760707837"

# create a new item
CREATE
#   the item just created: set the en label to "Hans Bertil Frisk"
LAST	Len	"Hans Bertil Frisk"
#   set the mul label to "Hans Bertil Frisk"
LAST	Lmul	"Hans Bertil Frisk"
#   set the ja label to "ハンス・ベルティル・フリスク"
LAST	Lja	"ハンス・ベルティル・フリスク"
#   set the zh label to "汉斯·贝蒂尔·弗里斯克"
LAST	Lzh	"汉斯·贝蒂尔·弗里斯克"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000177921459066 Hans Bertil Frisk, qualified P1810 subject named as Hans Bertil Frisk
LAST	P2600	"6000000177921459066"	P1810	"Hans Bertil Frisk"
#   P569 date of birth = +1930-08-26T00:00:00Z/11
LAST	P569	+1930-08-26T00:00:00Z/11	S2600	"6000000177921459066"
#   P570 date of death = +1991-05-00T00:00:00Z/10
LAST	P570	+1991-05-00T00:00:00Z/10	S2600	"6000000177921459066"
#   P25 mother = Q141223506 Beda Elvira Wedberg
LAST	P25	Q141223506	S2600	"6000000177921459066"
#   Q141223506 Beda Elvira Wedberg: P40 child = the item just created
Q141223506	P40	LAST	S2600	"6000000177921459066"

# create a new item
CREATE
#   the item just created: set the en label to "Helge Olsen Ytre Lima"
LAST	Len	"Helge Olsen Ytre Lima"
#   set the mul label to "Helge Olsen Ytre Lima"
LAST	Lmul	"Helge Olsen Ytre Lima"
#   set the ja label to "ヘルゲ・オルセン・イトレ・リマ"
LAST	Lja	"ヘルゲ・オルセン・イトレ・リマ"
#   set the zh label to "黑尔格·奥尔森·伊特雷·利马"
LAST	Lzh	"黑尔格·奥尔森·伊特雷·利马"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005607599821 Helge Olsen Ytre Lima, qualified P1810 subject named as Helge Olsen Ytre Lima
LAST	P2600	"6000000005607599821"	P1810	"Helge Olsen Ytre Lima"
#   P569 date of birth = +1768-00-00T00:00:00Z/9
LAST	P569	+1768-00-00T00:00:00Z/9	S2600	"6000000005607599821"
#   P570 date of death = +1852-00-00T00:00:00Z/9
LAST	P570	+1852-00-00T00:00:00Z/9	S2600	"6000000005607599821"
#   P26 spouse = Q141219250 Inger Sørensdatter Lima
LAST	P26	Q141219250	S2600	"6000000005607599821"
#   Q141219250 Inger Sørensdatter Lima: P26 spouse = the item just created
Q141219250	P26	LAST	S2600	"6000000005607599821"

# create a new item
CREATE
#   the item just created: set the en label to "Karl Emil Frisk"
LAST	Len	"Karl Emil Frisk"
#   set the mul label to "Karl Emil Frisk"
LAST	Lmul	"Karl Emil Frisk"
#   set the ja label to "カール・エミール・フリスク"
LAST	Lja	"カール・エミール・フリスク"
#   set the zh label to "卡尔·埃米尔·弗里斯克"
LAST	Lzh	"卡尔·埃米尔·弗里斯克"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000177921458827 Karl Emil Frisk, qualified P1810 subject named as Karl Emil Frisk
LAST	P2600	"6000000177921458827"	P1810	"Karl Emil Frisk"
#   P569 date of birth = +1902-01-28T00:00:00Z/11
LAST	P569	+1902-01-28T00:00:00Z/11	S2600	"6000000177921458827"
#   P570 date of death = +1983-11-04T00:00:00Z/11
LAST	P570	+1983-11-04T00:00:00Z/11	S2600	"6000000177921458827"
#   P26 spouse = Q141223506 Beda Elvira Wedberg
LAST	P26	Q141223506	S2600	"6000000177921458827"
#   Q141223506 Beda Elvira Wedberg: P26 spouse = the item just created
Q141223506	P26	LAST	S2600	"6000000177921458827"

# create a new item
CREATE
#   the item just created: set the en label to "Margareta Asp"
LAST	Len	"Margareta Asp"
#   set the mul label to "Margareta Asp"
LAST	Lmul	"Margareta Asp"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000019093195195 Margareta Asp, qualified P1810 subject named as Margareta Asp
LAST	P2600	"6000000019093195195"	P1810	"Margareta Asp"
#   P569 date of birth = +1706-08-03T00:00:00Z/11
LAST	P569	+1706-08-03T00:00:00Z/11	S2600	"6000000019093195195"
#   P570 date of death = +1765-03-03T00:00:00Z/11
LAST	P570	+1765-03-03T00:00:00Z/11	S2600	"6000000019093195195"
#   P26 spouse = Q5547967 Erik Alstrin
LAST	P26	Q5547967	S2600	"6000000019093195195"
#   Q5547967 Erik Alstrin: P26 spouse = the item just created
Q5547967	P26	LAST	S2600	"6000000019093195195"
#   the item just created: P735 given name = Q8274988 Margareta
LAST	P735	Q8274988

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
#   P2600 Geni.com profile ID = 6000000196541254827 Ola Rasmussen Bø, qualified P1810 subject named as Ola Rasmussen Bø
LAST	P2600	"6000000196541254827"	P1810	"Ola Rasmussen Bø"
#   P569 date of birth = +1810-02-26T00:00:00Z/11
LAST	P569	+1810-02-26T00:00:00Z/11	S2600	"6000000196541254827"
#   P570 date of death = +1825-00-00T00:00:00Z/9
LAST	P570	+1825-00-00T00:00:00Z/9	S2600	"6000000196541254827"
#   P22 father = Q141200074 Rasmus Olsen Bø
LAST	P22	Q141200074	S2600	"6000000196541254827"
#   P25 mother = Q141199809 Ane Marie Helgesdatter Bø
LAST	P25	Q141199809	S2600	"6000000196541254827"
#   Q141200074 Rasmus Olsen Bø: P40 child = the item just created
Q141200074	P40	LAST	S2600	"6000000196541254827"
#   Q141199809 Ane Marie Helgesdatter Bø: P40 child = the item just created
Q141199809	P40	LAST	S2600	"6000000196541254827"
#   the item just created: P735 given name = Q96675523 Ola
LAST	P735	Q96675523
#   P734 family name = Q30253098
LAST	P734	Q30253098

# create a new item
CREATE
#   set the en label to "Omund Tjærandsen Opstad"
LAST	Len	"Omund Tjærandsen Opstad"
#   set the mul label to "Omund Tjærandsen Opstad"
LAST	Lmul	"Omund Tjærandsen Opstad"
#   add a mul alias "Omund Tjærandsen Nord-Tjemsland"
LAST	Amul	"Omund Tjærandsen Nord-Tjemsland"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000009341204797 Omund Tjærandsen Opstad, qualified P1810 subject named as Omund Tjærandsen Nord-Tjemsland
LAST	P2600	"6000000009341204797"	P1810	"Omund Tjærandsen Nord-Tjemsland"
#   P569 date of birth = +1670-00-00T00:00:00Z/9
LAST	P569	+1670-00-00T00:00:00Z/9	S2600	"6000000009341204797"
#   P570 date of death = +1747-00-00T00:00:00Z/9
LAST	P570	+1747-00-00T00:00:00Z/9	S2600	"6000000009341204797"
#   P26 spouse = Q141223539 Malena Larsdatter Opstad
LAST	P26	Q141223539	S2600	"6000000009341204797"
#   P40 child = Q141216600 Astrid Omundsdatter Grøtheim
LAST	P40	Q141216600	S2600	"6000000009341204797"
#   Q141223539 Malena Larsdatter Opstad: P26 spouse = the item just created
Q141223539	P26	LAST	S2600	"6000000009341204797"
#   Q141216600 Astrid Omundsdatter Grøtheim: P22 father = the item just created
Q141216600	P22	LAST	S2600	"6000000009341204797"
#   the item just created: P735 given name = Q30817828 Omund
LAST	P735	Q30817828
#   P734 family name = Q37268235 Opstad
LAST	P734	Q37268235
#   add a mul alias "Omund Opstad"
LAST	Amul	"Omund Opstad"

# create a new item
CREATE
#   set the en label to "Pernel Velaine Tunheim"
LAST	Len	"Pernel Velaine Tunheim"
#   set the mul label to "Pernel Velaine Tunheim"
LAST	Lmul	"Pernel Velaine Tunheim"
#   add a mul alias "Pernel Velaine Shern"
LAST	Amul	"Pernel Velaine Shern"
#   set the ja label to "ペルネル・ヴェライネ・トゥンヘイム"
LAST	Lja	"ペルネル・ヴェライネ・トゥンヘイム"
#   set the zh label to "佩尔内尔·韦拉伊内·通海姆"
LAST	Lzh	"佩尔内尔·韦拉伊内·通海姆"
#   add a ja alias "ペルネル・ヴェライネ・スヘルン"
LAST	Aja	"ペルネル・ヴェライネ・スヘルン"
#   add a zh alias "佩尔内尔·韦拉伊内·斯赫尔恩"
LAST	Azh	"佩尔内尔·韦拉伊内·斯赫尔恩"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000180029736834 Pernel Velaine Tunheim, qualified P1810 subject named as Pernel Velaine Shern
LAST	P2600	"6000000180029736834"	P1810	"Pernel Velaine Shern"
#   P569 date of birth = +1929-08-13T00:00:00Z/11
LAST	P569	+1929-08-13T00:00:00Z/11	S2600	"6000000180029736834"
#   P570 date of death = +2011-04-05T00:00:00Z/11
LAST	P570	+2011-04-05T00:00:00Z/11	S2600	"6000000180029736834"
#   P26 spouse = Q141198399 Eugene LeRoy Tunheim
LAST	P26	Q141198399	S2600	"6000000180029736834"
#   Q141198399 Eugene LeRoy Tunheim: P26 spouse = the item just created
Q141198399	P26	LAST	S2600	"6000000180029736834"
#   the item just created: P734 family name = Q36927172, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q36927172	P3831	Q28418670

# create a new item
CREATE
#   set the en label to "Ragnhild Sofie Sahlin"
LAST	Len	"Ragnhild Sofie Sahlin"
#   set the mul label to "Ragnhild Sofie Sahlin"
LAST	Lmul	"Ragnhild Sofie Sahlin"
#   set the ja label to "ラグンヒル・ソフィー・サリン"
LAST	Lja	"ラグンヒル・ソフィー・サリン"
#   set the zh label to "拉格希尔德·索菲埃·萨林"
LAST	Lzh	"拉格希尔德·索菲埃·萨林"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003002538177 Ragnhild Sofie Sahlin, qualified P1810 subject named as Ragnhild Sahlin Wendt
LAST	P2600	"6000000003002538177"	P1810	"Ragnhild Sahlin Wendt"
#   P569 date of birth = +1920-11-04T00:00:00Z/11
LAST	P569	+1920-11-04T00:00:00Z/11	S2600	"6000000003002538177"
#   P570 date of death = +2001-11-06T00:00:00Z/11
LAST	P570	+2001-11-06T00:00:00Z/11	S2600	"6000000003002538177"
#   P22 father = Q141198396 Erling Juel Wendt
LAST	P22	Q141198396	S2600	"6000000003002538177"
#   P25 mother = Q141168784 Aagot Wendt
LAST	P25	Q141168784	S2600	"6000000003002538177"
#   Q141198396 Erling Juel Wendt: P40 child = the item just created
Q141198396	P40	LAST	S2600	"6000000003002538177"
#   Q141168784 Aagot Wendt: P40 child = the item just created
Q141168784	P40	LAST	S2600	"6000000003002538177"

# create a new item
CREATE
#   the item just created: set the en label to "Rasmus Wibye Andersson Lea"
LAST	Len	"Rasmus Wibye Andersson Lea"
#   set the mul label to "Rasmus Wibye Andersson Lea"
LAST	Lmul	"Rasmus Wibye Andersson Lea"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005609547535 Rasmus Wibye Andersson Lea, qualified P1810 subject named as Rasmus Wibye Andersson Lea
LAST	P2600	"6000000005609547535"	P1810	"Rasmus Wibye Andersson Lea"
#   P569 date of birth = +1813-00-00T00:00:00Z/9
LAST	P569	+1813-00-00T00:00:00Z/9	S2600	"6000000005609547535"
#   P570 date of death = +1880-03-27T00:00:00Z/11
LAST	P570	+1880-03-27T00:00:00Z/11	S2600	"6000000005609547535"
#   P26 spouse = Q141223503 Anne Berta Osmundsdatter Nese
LAST	P26	Q141223503	S2600	"6000000005609547535"
#   Q141223503 Anne Berta Osmundsdatter Nese: P26 spouse = the item just created
Q141223503	P26	LAST	S2600	"6000000005609547535"

# create a new item
CREATE
#   the item just created: set the en label to "Thomas Linder"
LAST	Len	"Thomas Linder"
#   set the mul label to "Thomas Linder"
LAST	Lmul	"Thomas Linder"
#   add a mul alias "Thomas Johansson"
LAST	Amul	"Thomas Johansson"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000012501208346 Thomas Linder, qualified P1810 subject named as Thomas Johansson
LAST	P2600	"6000000012501208346"	P1810	"Thomas Johansson"
#   P569 date of birth = +1754-07-05T00:00:00Z/11
LAST	P569	+1754-07-05T00:00:00Z/11	S2600	"6000000012501208346"
#   P570 date of death = +1785-01-15T00:00:00Z/11
LAST	P570	+1785-01-15T00:00:00Z/11	S2600	"6000000012501208346"
#   P40 child = Q5955392 Johan Anders Johansson Linder
LAST	P40	Q5955392	S2600	"6000000012501208346"
#   Q5955392 Johan Anders Johansson Linder: P22 father = the item just created
Q5955392	P22	LAST	S2600	"6000000012501208346"
#   the item just created: P735 given name = Q16428906
LAST	P735	Q16428906
#   Q141223503 Anne Berta Osmundsdatter Nese: P25 mother = Q141223553 Ragnhild Kristine Øystensdatter Nese
Q141223503	P25	Q141223553	S2600	"6000000005609547544"
#   P735 given name = Q564684 Anne, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141223503	P735	Q564684	P1545	"1"	P7452	Q3409033
#   P735 given name = Q4092653 Berta, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141223503	P735	Q4092653	P1545	"2"	P3831	Q245025
#   P734 family name = Q37543374
Q141223503	P734	Q37543374
#   Q141223553 Ragnhild Kristine Øystensdatter Nese: P40 child = Q141223503 Anne Berta Osmundsdatter Nese
Q141223553	P40	Q141223503	S2600	"6000000010479856178"
#   P735 given name = Q1390292 Ragnhild, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141223553	P735	Q1390292	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16859157 Kristine, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141223553	P735	Q16859157	P1545	"2"	P3831	Q245025
#   P734 family name = Q37543374
Q141223553	P734	Q37543374
#   Q141223516 Hans Otto Kristian Jenssen: P40 child = Q141223517 Hilma Petrine Jenssen
Q141223516	P40	Q141223517	S2600	"6000000014188476819"
#   Q141223517 Hilma Petrine Jenssen: P22 father = Q141223516 Hans Otto Kristian Jenssen
Q141223517	P22	Q141223516	S2600	"6000000014196669652"
#   Q141223547 NN: P26 spouse = Q141223548 Per Nilsson
Q141223547	P26	Q141223548	S2600	"6000000017535915136"
#   Q141223518 Jakob Bunge: P26 spouse = Q141223502 Anna Martens
Q141223518	P26	Q141223502	S2600	"6000000018604538988"
#   Q141223502 Anna Martens: P26 spouse = Q141223518 Jakob Bunge
Q141223502	P26	Q141223518	S2600	"6000000018604581410"
#   Q141223548 Per Nilsson: P26 spouse = Q141223547 NN
Q141223548	P26	Q141223547	S2600	"6000000019178738670"
#   P5056 patronym or matronym = Q130233015 Nilsson
Q141223548	P5056	Q130233015
#   Q138474188 Hans Syvertsen Nyvold: P735 given name = Q632842
Q138474188	P735	Q632842
#   Q141223523 Johan Fredrik Wedberg: P40 child = Q141223506 Beda Elvira Wedberg
Q141223523	P40	Q141223506	S2600	"6000000021652410546"
#   P735 given name = Q10989273 Johan, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141223523	P735	Q10989273	P1545	"1"	P7452	Q3409033
#   P735 given name = Q4926491 Fredrik, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141223523	P735	Q4926491	P1545	"2"	P3831	Q245025
#   P734 family name = Q54444784
Q141223523	P734	Q54444784
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
#   Q141223506 Beda Elvira Wedberg: P22 father = Q141223523 Johan Fredrik Wedberg
Q141223506	P22	Q141223523	S2600	"6000000177921458833"
#   P735 given name = Q3051870 Elvira, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141223506	P735	Q3051870	P1545	"2"	P3831	Q245025
#   P734 family name = Q54444784
Q141223506	P734	Q54444784
#   Q141223427 Johanna Matilda Carlsdotter: P735 given name = Q4120836 Johanna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141223427	P735	Q4120836	P1545	"1"	P7452	Q3409033
#   P735 given name = Q2054021 Matilda, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141223427	P735	Q2054021	P1545	"2"	P3831	Q245025
#   Q141223507 Carl, Johan Ersson: P735 given name = Q10989273 Johan, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141223507	P735	Q10989273	P1545	"2"	P3831	Q245025
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

