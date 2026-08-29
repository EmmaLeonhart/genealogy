# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   2181 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   Q141180412: ja was transliterated from a superseded mul ('マルタ・ラスムスダッテル・ヘーレ'); mul now says 'Marta Rasmusdatter Li'
Q141180412	Lja	"マルタ・ラスムスダッテル・リ"
#   Q141180412: zh was transliterated from a superseded mul ('玛尔塔·拉斯穆斯达特·赫勒'); mul now says 'Marta Rasmusdatter Li'
Q141180412	Lzh	"玛尔塔·拉斯穆斯达特·李"
#   Q141180413: ja was transliterated from a superseded mul ('トーマス・マットソン'); mul now says 'Thomas Matthiæ'
Q141180413	Lja	"トーマス・マティエ"
#   Q141180413: zh was transliterated from a superseded mul ('托马斯·马特松'); mul now says 'Thomas Matthiæ'
Q141180413	Lzh	"托马斯·马蒂埃"
#   Q141189076: ja was transliterated from a superseded mul ('クリスティアン・ラーシェン・ノール・ヴァールハウグ'); mul now says 'Kristian Larsen Sør-Reime'
Q141189076	Lja	"クリスティアン・ラーシェン・セール・レイメ"
#   Q141189076: zh was transliterated from a superseded mul ('克里斯蒂安·拉尔森·诺尔·瓦尔豪格'); mul now says 'Kristian Larsen Sør-Reime'
Q141189076	Lzh	"克里斯蒂安·拉尔森·瑟尔·雷梅"
#   Q141189081: ja was transliterated from a superseded mul ('ロッテ・ビルギーテ・グスタヴァ・ヨナスダッテル・ヘイグレ'); mul now says 'Lotte Birgithe Gustava Jonasdatter Lea'
Q141189081	Lja	"ロッテ・ビルギーテ・グスタヴァ・ヨナスダッテル・レア"
#   Q141189081: zh was transliterated from a superseded mul ('洛特·比尔吉特·古斯塔娃·约纳斯达特·海格勒'); mul now says 'Lotte Birgithe Gustava Jonasdatter Lea'
Q141189081	Lzh	"洛特·比尔吉特·古斯塔娃·约纳斯达特·莱阿"
#   Q141189083: ja was transliterated from a superseded mul ('マルタ・エリーダ・ベルゲルセン'); mul now says 'Martha Elida Frenning'
Q141189083	Lja	"マルタ・エリーダ・フレニング"
#   Q141189083: zh was transliterated from a superseded mul ('玛尔塔·埃利达·贝格尔森'); mul now says 'Martha Elida Frenning'
Q141189083	Lzh	"玛尔塔·埃利达·夫雷尼恩格"
#   Q141189104: ja was transliterated from a superseded mul ('シーリ・クリスティーネ・イーヴァシュダッテル・サンスマルク'); mul now says 'Siri Kristine Ivarsdatter Garborg'
Q141189104	Lja	"シーリ・クリスティーネ・イーヴァシュダッテル・ガルボルグ"
#   Q141189104: zh was transliterated from a superseded mul ('西丽·克丽丝汀·伊瓦斯达特·桑斯马克'); mul now says 'Siri Kristine Ivarsdatter Garborg'
Q141189104	Lzh	"西丽·克丽丝汀·伊瓦斯达特·加尔博格"
#   Q141189108: ja was transliterated from a superseded mul ('ティリー・ベッツィ・トゥンヘイム'); mul now says 'Tillie Betsy Amundson'
Q141189108	Lja	"ティリー・ベッツィ・アムンドソン"
#   Q141189108: zh was transliterated from a superseded mul ('蒂莉·贝齐·通海姆'); mul now says 'Tillie Betsy Amundson'
Q141189108	Lzh	"蒂莉·贝齐·阿穆恩德松"
#   Q141189112: ja was transliterated from a superseded mul ('ヴィルヘルミーネ・ソフィー・ベルゲルセン'); mul now says 'Wilhelmine Sophie Christiansen'
Q141189112	Lja	"ヴィルヘルミーネ・ソフィー・クリスチャンセン"

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Aagot Garborg Koloboff"
LAST	Len	"Aagot Garborg Koloboff"
#   set the mul label to "Aagot Garborg Koloboff"
LAST	Lmul	"Aagot Garborg Koloboff"
#   add a mul alias "Aagot Engebretsen"
LAST	Amul	"Aagot Engebretsen"
#   set the ja label to "オーゴット・ガルボルグ・コロボフ"
LAST	Lja	"オーゴット・ガルボルグ・コロボフ"
#   set the zh label to "奥高特·加尔博格·科洛博夫"
LAST	Lzh	"奥高特·加尔博格·科洛博夫"
#   add a ja alias "オーゴット・エンゲブレトセン"
LAST	Aja	"オーゴット・エンゲブレトセン"
#   add a zh alias "奥高特·埃恩盖布雷特森"
LAST	Azh	"奥高特·埃恩盖布雷特森"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000036746925255 Aagot Garborg Koloboff, qualified P1810 subject named as Aagot Engebretsen
LAST	P2600	"6000000036746925255"	P1810	"Aagot Engebretsen"
#   P569 date of birth = +1892-08-19T00:00:00Z/11
LAST	P569	+1892-08-19T00:00:00Z/11	S2600	"6000000036746925255"
#   P570 date of death = +1948-01-21T00:00:00Z/11
LAST	P570	+1948-01-21T00:00:00Z/11	S2600	"6000000036746925255"
#   P26 spouse = Q141168837 Ingebret Garborg
LAST	P26	Q141168837	S2600	"6000000036746925255"
#   P40 child = Q141216408 Unn (Bitten) Mørck
LAST	P40	Q141216408	S2600	"6000000036746925255"
#   Q141168837 Ingebret Garborg: P26 spouse = the item just created
Q141168837	P26	LAST	S2600	"6000000036746925255"
#   Q141216408 Unn (Bitten) Mørck: P25 mother = the item just created
Q141216408	P25	LAST	S2600	"6000000036746925255"
#   the item just created: P735 given name = Q3482557 Aagot
LAST	P735	Q3482557
#   P734 family name = Q30250555 Garborg, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q30250555	P3831	Q28418670

# create a new item
CREATE
#   set the en label to "Alice Lillian Tunheim Nelson"
LAST	Len	"Alice Lillian Tunheim Nelson"
#   set the mul label to "Alice Lillian Tunheim Nelson"
LAST	Lmul	"Alice Lillian Tunheim Nelson"
#   add a mul alias "Alice Lillian Horton"
LAST	Amul	"Alice Lillian Horton"
#   set the ja label to "アリス・リリアン・トゥンヘイム・ネルソン"
LAST	Lja	"アリス・リリアン・トゥンヘイム・ネルソン"
#   set the zh label to "艾丽丝·利利阿恩·通海姆·内尔松"
LAST	Lzh	"艾丽丝·利利阿恩·通海姆·内尔松"
#   add a ja alias "アリス・リリアン・ホルトン"
LAST	Aja	"アリス・リリアン・ホルトン"
#   add a zh alias "艾丽丝·利利阿恩·霍尔托恩"
LAST	Azh	"艾丽丝·利利阿恩·霍尔托恩"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000039510815149 Alice Lillian Tunheim Nelson, qualified P1810 subject named as Alice Lillian Horton
LAST	P2600	"6000000039510815149"	P1810	"Alice Lillian Horton"
#   P569 date of birth = +1920-01-01T00:00:00Z/11
LAST	P569	+1920-01-01T00:00:00Z/11	S2600	"6000000039510815149"
#   P570 date of death = +1992-06-23T00:00:00Z/11
LAST	P570	+1992-06-23T00:00:00Z/11	S2600	"6000000039510815149"
#   P26 spouse = Q141189101 Samuel Tunheim
LAST	P26	Q141189101	S2600	"6000000039510815149"
#   Q141189101 Samuel Tunheim: P26 spouse = the item just created
Q141189101	P26	LAST	S2600	"6000000039510815149"
#   the item just created: P735 given name = Q650689 Alice, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q650689	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16420442 Lillian, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q16420442	P1545	"2"	P3831	Q245025
#   P734 family name = Q16870893 Horton, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q16870893	P3831	Q2507958
#   P734 family name = Q2782528 Nelson, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q2782528	P3831	Q28418670

# create a new item
CREATE
#   set the en label to "Anders Persson"
LAST	Len	"Anders Persson"
#   set the mul label to "Anders Persson"
LAST	Lmul	"Anders Persson"
#   set the ja label to "アンデルス・ペルソン"
LAST	Lja	"アンデルス・ペルソン"
#   set the zh label to "阿恩德尔斯·佩尔松"
LAST	Lzh	"阿恩德尔斯·佩尔松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 375734886370012680 Anders Persson, qualified P1810 subject named as Anders Persson
LAST	P2600	"375734886370012680"	P1810	"Anders Persson"
#   P569 date of birth = +1630-00-00T00:00:00Z/9
LAST	P569	+1630-00-00T00:00:00Z/9	S2600	"375734886370012680"
#   P570 date of death = +1680-00-00T00:00:00Z/9
LAST	P570	+1680-00-00T00:00:00Z/9	S2600	"375734886370012680"
#   P26 spouse = Q141216401 Mariet Danielsdotter
LAST	P26	Q141216401	S2600	"375734886370012680"
#   Q141216401 Mariet Danielsdotter: P26 spouse = the item just created
Q141216401	P26	LAST	S2600	"375734886370012680"
#   the item just created: P735 given name = Q8843357 Anders
LAST	P735	Q8843357
#   P734 family name = Q27876648 Persson
LAST	P734	Q27876648

# create a new item
CREATE
#   set the en label to "Anna Helgesdotter Opstad"
LAST	Len	"Anna Helgesdotter Opstad"
#   set the mul label to "Anna Helgesdotter Opstad"
LAST	Lmul	"Anna Helgesdotter Opstad"
#   set the ja label to "アンナ・ヘルゲスドッテル・オプスタド"
LAST	Lja	"アンナ・ヘルゲスドッテル・オプスタド"
#   set the zh label to "安娜·赫尔盖斯多特·奥普斯塔德"
LAST	Lzh	"安娜·赫尔盖斯多特·奥普斯塔德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000042211257124 Anna Helgesdotter Opstad, qualified P1810 subject named as Anna Helgesdotter Opstad
LAST	P2600	"6000000042211257124"	P1810	"Anna Helgesdotter Opstad"
#   P569 date of birth = +1730-00-00T00:00:00Z/9
LAST	P569	+1730-00-00T00:00:00Z/9	S2600	"6000000042211257124"
#   P570 date of death = +1785-00-00T00:00:00Z/9
LAST	P570	+1785-00-00T00:00:00Z/9	S2600	"6000000042211257124"
#   P40 child = Q141216382 Helge Asbjørnsen Bø
LAST	P40	Q141216382	S2600	"6000000042211257124"
#   Q141216382 Helge Asbjørnsen Bø: P25 mother = the item just created
Q141216382	P25	LAST	S2600	"6000000042211257124"
#   the item just created: P734 family name = Q37268235 Opstad
LAST	P734	Q37268235

# create a new item
CREATE
#   set the en label to "Asbjørn Gunnarson Bø"
LAST	Len	"Asbjørn Gunnarson Bø"
#   set the mul label to "Asbjørn Gunnarson Bø"
LAST	Lmul	"Asbjørn Gunnarson Bø"
#   set the ja label to "アスブヨルン・グナルソン・ベー"
LAST	Lja	"アスブヨルン・グナルソン・ベー"
#   set the zh label to "阿斯布永尔恩·古纳尔松·贝"
LAST	Lzh	"阿斯布永尔恩·古纳尔松·贝"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000042211257078 Asbjørn Gunnarson Bø, qualified P1810 subject named as Asbjørn Gunnarson Bø
LAST	P2600	"6000000042211257078"	P1810	"Asbjørn Gunnarson Bø"
#   P569 date of birth = +1728-00-00T00:00:00Z/9
LAST	P569	+1728-00-00T00:00:00Z/9	S2600	"6000000042211257078"
#   P570 date of death = +1798-00-00T00:00:00Z/9
LAST	P570	+1798-00-00T00:00:00Z/9	S2600	"6000000042211257078"
#   P40 child = Q141216382 Helge Asbjørnsen Bø
LAST	P40	Q141216382	S2600	"6000000042211257078"
#   Q141216382 Helge Asbjørnsen Bø: P22 father = the item just created
Q141216382	P22	LAST	S2600	"6000000042211257078"
#   the item just created: P735 given name = Q721398 Asbjørn
LAST	P735	Q721398

# create a new item
CREATE
#   set the en label to "Astrid Grimelund Wendt"
LAST	Len	"Astrid Grimelund Wendt"
#   set the mul label to "Astrid Grimelund Wendt"
LAST	Lmul	"Astrid Grimelund Wendt"
#   set the ja label to "アストリッド・グリメルンド・ヴェント"
LAST	Lja	"アストリッド・グリメルンド・ヴェント"
#   set the zh label to "阿斯特丽德·格里梅卢恩德·温特"
LAST	Lzh	"阿斯特丽德·格里梅卢恩德·温特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000048057251830 Astrid Grimelund Wendt, qualified P1810 subject named as Astrid Grimelund Wendt
LAST	P2600	"6000000048057251830"	P1810	"Astrid Grimelund Wendt"
#   P569 date of birth = +1895-01-30T00:00:00Z/11
LAST	P569	+1895-01-30T00:00:00Z/11	S2600	"6000000048057251830"
#   P570 date of death = +1900-08-29T00:00:00Z/11
LAST	P570	+1900-08-29T00:00:00Z/11	S2600	"6000000048057251830"
#   P22 father = Q141216386 Jens Wilhelm Wendt
LAST	P22	Q141216386	S2600	"6000000048057251830"
#   P25 mother = Q141216377 Hanna Sofie Wendt
LAST	P25	Q141216377	S2600	"6000000048057251830"
#   Q141216386 Jens Wilhelm Wendt: P40 child = the item just created
Q141216386	P40	LAST	S2600	"6000000048057251830"
#   Q141216377 Hanna Sofie Wendt: P40 child = the item just created
Q141216377	P40	LAST	S2600	"6000000048057251830"
#   the item just created: P735 given name = Q167755 Astrid, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q167755	P1545	"1"	P7452	Q3409033

# create a new item
CREATE
#   set the en label to "Bjørnsdatter Tau"
LAST	Len	"Bjørnsdatter Tau"
#   set the mul label to "Bjørnsdatter Tau"
LAST	Lmul	"Bjørnsdatter Tau"
#   set the ja label to "ブヨルンスダッテル・タウ"
LAST	Lja	"ブヨルンスダッテル・タウ"
#   set the zh label to "布永尔恩斯达特·塔乌"
LAST	Lzh	"布永尔恩斯达特·塔乌"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005607353362 Bjørnsdatter Tau, qualified P1810 subject named as Bjørnsdatter Tau
LAST	P2600	"6000000005607353362"	P1810	"Bjørnsdatter Tau"
#   P569 date of birth = +1500-00-00T00:00:00Z/9
LAST	P569	+1500-00-00T00:00:00Z/9	S2600	"6000000005607353362"
#   P40 child = Q141216400 Margreta Lauritsdatter Øvre Bjørheim
LAST	P40	Q141216400	S2600	"6000000005607353362"
#   Q141216400 Margreta Lauritsdatter Øvre Bjørheim: P25 mother = the item just created
Q141216400	P25	LAST	S2600	"6000000005607353362"

# create a new item
CREATE
#   the item just created: set the en label to "Daniel Andersson"
LAST	Len	"Daniel Andersson"
#   set the mul label to "Daniel Andersson"
LAST	Lmul	"Daniel Andersson"
#   set the ja label to "ダニエル・アンデルソン"
LAST	Lja	"ダニエル・アンデルソン"
#   set the zh label to "达尼埃尔·阿恩德尔松"
LAST	Lzh	"达尼埃尔·阿恩德尔松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000018528235866 Daniel Andersson, qualified P1810 subject named as Daniel Andersson
LAST	P2600	"6000000018528235866"	P1810	"Daniel Andersson"
#   P569 date of birth = +1674-00-00T00:00:00Z/9
LAST	P569	+1674-00-00T00:00:00Z/9	S2600	"6000000018528235866"
#   P570 date of death = +1766-00-00T00:00:00Z/9
LAST	P570	+1766-00-00T00:00:00Z/9	S2600	"6000000018528235866"
#   P25 mother = Q141216401 Mariet Danielsdotter
LAST	P25	Q141216401	S2600	"6000000018528235866"
#   Q141216401 Mariet Danielsdotter: P40 child = the item just created
Q141216401	P40	LAST	S2600	"6000000018528235866"
#   the item just created: P735 given name = Q53787734 Daniel
LAST	P735	Q53787734

# create a new item
CREATE
#   set the en label to "Eldrid Jonsdatter"
LAST	Len	"Eldrid Jonsdatter"
#   set the mul label to "Eldrid Jonsdatter"
LAST	Lmul	"Eldrid Jonsdatter"
#   add a mul alias "Eldrid Jonsdtr Blindheim"
LAST	Amul	"Eldrid Jonsdtr Blindheim"
#   set the ja label to "エルドリド・ヨンスダッテル"
LAST	Lja	"エルドリド・ヨンスダッテル"
#   set the zh label to "埃尔德里德·永斯达特"
LAST	Lzh	"埃尔德里德·永斯达特"
#   add a ja alias "エルドリド・ヨンスダッテル・ブリンドヘイム"
LAST	Aja	"エルドリド・ヨンスダッテル・ブリンドヘイム"
#   add a zh alias "埃尔德里德·永恩斯达特·布利恩德赫伊姆"
LAST	Azh	"埃尔德里德·永恩斯达特·布利恩德赫伊姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000001200204262 Eldrid Jonsdatter, qualified P1810 subject named as Eldrid Jonsdtr Blindheim
LAST	P2600	"6000000001200204262"	P1810	"Eldrid Jonsdtr Blindheim"
#   P569 date of birth = +1114-00-00T00:00:00Z/9
LAST	P569	+1114-00-00T00:00:00Z/9	S2600	"6000000001200204262"
#   P570 date of death = +1144-00-00T00:00:00Z/9
LAST	P570	+1144-00-00T00:00:00Z/9	S2600	"6000000001200204262"
#   P26 spouse = Q19061035 Guttorm Àsulfsson à Rein
LAST	P26	Q19061035	S2600	"6000000001200204262"
#   P40 child = Q141216349 Ingrid Guttormsdotter
LAST	P40	Q141216349	S2600	"6000000001200204262"
#   Q19061035 Guttorm Àsulfsson à Rein: P26 spouse = the item just created
Q19061035	P26	LAST	S2600	"6000000001200204262"
#   Q141216349 Ingrid Guttormsdotter: P25 mother = the item just created
Q141216349	P25	LAST	S2600	"6000000001200204262"
#   the item just created: P735 given name = Q12714450 Eldrid
LAST	P735	Q12714450
#   P1449 nickname = en:"Elvi Huk"
LAST	P1449	en:"Elvi Huk"
#   add a mul alias "Elvi Huk Jonsdatter"
LAST	Amul	"Elvi Huk Jonsdatter"

# create a new item
CREATE
#   set the en label to "Erik Hansson Gausland"
LAST	Len	"Erik Hansson Gausland"
#   set the mul label to "Erik Hansson Gausland"
LAST	Lmul	"Erik Hansson Gausland"
#   set the ja label to "エリク・ハンソン・ガウスランド"
LAST	Lja	"エリク・ハンソン・ガウスランド"
#   set the zh label to "埃里克·哈恩松·加乌斯拉恩德"
LAST	Lzh	"埃里克·哈恩松·加乌斯拉恩德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000053561772011 Erik Hansson Gausland, qualified P1810 subject named as Erik Hansson Gausland
LAST	P2600	"6000000053561772011"	P1810	"Erik Hansson Gausland"
#   P569 date of birth = +1698-00-00T00:00:00Z/9
LAST	P569	+1698-00-00T00:00:00Z/9	S2600	"6000000053561772011"
#   P570 date of death = +1747-04-07T00:00:00Z/11
LAST	P570	+1747-04-07T00:00:00Z/11	S2600	"6000000053561772011"
#   P22 father = Q141216381 Hans Rasmussen Låge-Håland
LAST	P22	Q141216381	S2600	"6000000053561772011"
#   P25 mother = Q141216383 Ingeborg Eriksdatter Bjorland
LAST	P25	Q141216383	S2600	"6000000053561772011"
#   Q141216381 Hans Rasmussen Låge-Håland: P40 child = the item just created
Q141216381	P40	LAST	S2600	"6000000053561772011"
#   Q141216383 Ingeborg Eriksdatter Bjorland: P40 child = the item just created
Q141216383	P40	LAST	S2600	"6000000053561772011"
#   the item just created: P735 given name = Q750186 Erik
LAST	P735	Q750186

# create a new item
CREATE
#   set the en label to "Govert Jonson Årsvoll"
LAST	Len	"Govert Jonson Årsvoll"
#   set the mul label to "Govert Jonson Årsvoll"
LAST	Lmul	"Govert Jonson Årsvoll"
#   add a mul alias "Govert Jonson Sveinsvoll"
LAST	Amul	"Govert Jonson Sveinsvoll"
#   set the ja label to "ゴヴェルト・ヨンソン・オールスヴォル"
LAST	Lja	"ゴヴェルト・ヨンソン・オールスヴォル"
#   set the zh label to "戈韦尔特·永松·奥尔斯沃尔"
LAST	Lzh	"戈韦尔特·永松·奥尔斯沃尔"
#   add a ja alias "ゴヴェルト・ヨンソン・スヴェインスヴォル"
LAST	Aja	"ゴヴェルト・ヨンソン・スヴェインスヴォル"
#   add a zh alias "戈韦尔特·永松·斯韦伊恩斯沃尔"
LAST	Azh	"戈韦尔特·永松·斯韦伊恩斯沃尔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000008174080446 Govert Jonson Årsvoll, qualified P1810 subject named as Govert Jonson Sveinsvoll
LAST	P2600	"6000000008174080446"	P1810	"Govert Jonson Sveinsvoll"
#   P569 date of birth = +1778-00-00T00:00:00Z/9
LAST	P569	+1778-00-00T00:00:00Z/9	S2600	"6000000008174080446"
#   P40 child = Q141216363 Anne Govertsdtr. Bratland
LAST	P40	Q141216363	S2600	"6000000008174080446"
#   Q141216363 Anne Govertsdtr. Bratland: P22 father = the item just created
Q141216363	P22	LAST	S2600	"6000000008174080446"
#   the item just created: P735 given name = Q20725207 Govert
LAST	P735	Q20725207
#   add a mul alias "Govert Årsvoll"
LAST	Amul	"Govert Årsvoll"

# create a new item
CREATE
#   set the en label to "Gunnbjørn Gunnbjørnson Rossavik"
LAST	Len	"Gunnbjørn Gunnbjørnson Rossavik"
#   set the mul label to "Gunnbjørn Gunnbjørnson Rossavik"
LAST	Lmul	"Gunnbjørn Gunnbjørnson Rossavik"
#   add a mul alias "Gunnbjørn Gunnbjørnson Mjølhus"
LAST	Amul	"Gunnbjørn Gunnbjørnson Mjølhus"
#   set the ja label to "グンブヨルン・グンブヨルンソン・ロサヴィク"
LAST	Lja	"グンブヨルン・グンブヨルンソン・ロサヴィク"
#   set the zh label to "古恩布永尔恩·古恩布永尔恩松·罗萨维克"
LAST	Lzh	"古恩布永尔恩·古恩布永尔恩松·罗萨维克"
#   add a ja alias "グンブヨルン・グンブヨルンソン・ムヨルフス"
LAST	Aja	"グンブヨルン・グンブヨルンソン・ムヨルフス"
#   add a zh alias "古恩布永尔恩·古恩布永尔恩松·姆永尔胡斯"
LAST	Azh	"古恩布永尔恩·古恩布永尔恩松·姆永尔胡斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003095080090 Gunnbjørn Gunnbjørnson Rossavik, qualified P1810 subject named as Gunnbjørn Gunnbjørnson Mjølhus
LAST	P2600	"6000000003095080090"	P1810	"Gunnbjørn Gunnbjørnson Mjølhus"
#   P569 date of birth = +1570-00-00T00:00:00Z/9
LAST	P569	+1570-00-00T00:00:00Z/9	S2600	"6000000003095080090"
#   P570 date of death = +1620-00-00T00:00:00Z/9
LAST	P570	+1620-00-00T00:00:00Z/9	S2600	"6000000003095080090"
#   P22 father = Q141198834 Gunnbjørn Jonson Mjølhus
LAST	P22	Q141198834	S2600	"6000000003095080090"
#   P25 mother = Q141205924 N.N. Aukland
LAST	P25	Q141205924	S2600	"6000000003095080090"
#   Q141198834 Gunnbjørn Jonson Mjølhus: P40 child = the item just created
Q141198834	P40	LAST	S2600	"6000000003095080090"
#   Q141205924 N.N. Aukland: P40 child = the item just created
Q141205924	P40	LAST	S2600	"6000000003095080090"
#   the item just created: add a mul alias "Gunnbjørn Rossavik"
LAST	Amul	"Gunnbjørn Rossavik"

# create a new item
CREATE
#   set the en label to "Guttorm Ostmannson of Jämtland & Svealand"
LAST	Len	"Guttorm Ostmannson of Jämtland & Svealand"
#   set the mul label to "Guttorm Ostmannson of Jämtland & Svealand"
LAST	Lmul	"Guttorm Ostmannson of Jämtland & Svealand"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000010859543717 Guttorm Ostmannson of Jämtland & Svealand, qualified P1810 subject named as Guttorm Ostmannson of Jämtland & Svealand
LAST	P2600	"6000000010859543717"	P1810	"Guttorm Ostmannson of Jämtland & Svealand"
#   P569 date of birth = +1120-00-00T00:00:00Z/9
LAST	P569	+1120-00-00T00:00:00Z/9	S2600	"6000000010859543717"
#   P570 date of death = +1171-04-14T00:00:00Z/11
LAST	P570	+1171-04-14T00:00:00Z/11	S2600	"6000000010859543717"
#   P26 spouse = Q141216349 Ingrid Guttormsdotter
LAST	P26	Q141216349	S2600	"6000000010859543717"
#   P40 child = Q4953376 Helena Guttormsdatter
LAST	P40	Q4953376	S2600	"6000000010859543717"
#   Q141216349 Ingrid Guttormsdotter: P26 spouse = the item just created
Q141216349	P26	LAST	S2600	"6000000010859543717"
#   Q4953376 Helena Guttormsdatter: P22 father = the item just created
Q4953376	P22	LAST	S2600	"6000000010859543717"
#   the item just created: P735 given name = Q20755782 Guttorm
LAST	P735	Q20755782
#   P1449 nickname = en:"Jarl i Jamtland og Svealand"
LAST	P1449	en:"Jarl i Jamtland og Svealand"
#   add a mul alias "Jarl i Jamtland og Svealand Ostmannson"
LAST	Amul	"Jarl i Jamtland og Svealand Ostmannson"

# create a new item
CREATE
#   set the en label to "Jon Jonsson Vatne"
LAST	Len	"Jon Jonsson Vatne"
#   set the mul label to "Jon Jonsson Vatne"
LAST	Lmul	"Jon Jonsson Vatne"
#   set the ja label to "ヨン・ヨンソン・ヴァトネ"
LAST	Lja	"ヨン・ヨンソン・ヴァトネ"
#   set the zh label to "永·永松·瓦特内"
LAST	Lzh	"永·永松·瓦特内"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000014516017872 Jon Jonsson Vatne, qualified P1810 subject named as Jon Jonsson Vatne
LAST	P2600	"6000000014516017872"	P1810	"Jon Jonsson Vatne"
#   P569 date of birth = +1817-05-01T00:00:00Z/11
LAST	P569	+1817-05-01T00:00:00Z/11	S2600	"6000000014516017872"
#   P22 father = Q141216388 Jon Hansson St. Vatne
LAST	P22	Q141216388	S2600	"6000000014516017872"
#   P25 mother = Q141206057 Berte Tørresdotter Austrått
LAST	P25	Q141206057	S2600	"6000000014516017872"
#   Q141216388 Jon Hansson St. Vatne: P40 child = the item just created
Q141216388	P40	LAST	S2600	"6000000014516017872"
#   Q141206057 Berte Tørresdotter Austrått: P40 child = the item just created
Q141206057	P40	LAST	S2600	"6000000014516017872"
#   the item just created: P735 given name = Q13501137 Jon
LAST	P735	Q13501137
#   P734 family name = Q30134985 Vatne
LAST	P734	Q30134985

# create a new item
CREATE
#   set the en label to "Jon Tørresson Soma"
LAST	Len	"Jon Tørresson Soma"
#   set the mul label to "Jon Tørresson Soma"
LAST	Lmul	"Jon Tørresson Soma"
#   set the ja label to "ヨン・トレソン・ソマ"
LAST	Lja	"ヨン・トレソン・ソマ"
#   set the zh label to "永·托雷松·索马"
LAST	Lzh	"永·托雷松·索马"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000014277496029 Jon Tørresson Soma, qualified P1810 subject named as Jon Tørresson Soma
LAST	P2600	"6000000014277496029"	P1810	"Jon Tørresson Soma"
#   P569 date of birth = +1764-00-00T00:00:00Z/9
LAST	P569	+1764-00-00T00:00:00Z/9	S2600	"6000000014277496029"
#   P570 date of death = +1837-05-07T00:00:00Z/11
LAST	P570	+1837-05-07T00:00:00Z/11	S2600	"6000000014277496029"
#   P40 child = Q141205903 Enok Jonson Rønneberg
LAST	P40	Q141205903	S2600	"6000000014277496029"
#   Q141205903 Enok Jonson Rønneberg: P22 father = the item just created
Q141205903	P22	LAST	S2600	"6000000014277496029"
#   the item just created: P735 given name = Q13501137 Jon
LAST	P735	Q13501137

# create a new item
CREATE
#   set the en label to "Karen Malena Rasmusdatter Tjelta"
LAST	Len	"Karen Malena Rasmusdatter Tjelta"
#   set the mul label to "Karen Malena Rasmusdatter Tjelta"
LAST	Lmul	"Karen Malena Rasmusdatter Tjelta"
#   add a mul alias "Karen Malena Rasmusdatter Pighaug"
LAST	Amul	"Karen Malena Rasmusdatter Pighaug"
#   set the ja label to "カーレン・マレナ・ラスムスダッテル・トイェルタ"
LAST	Lja	"カーレン・マレナ・ラスムスダッテル・トイェルタ"
#   set the zh label to "卡伦·马莱纳·拉斯穆斯达特·特耶尔塔"
LAST	Lzh	"卡伦·马莱纳·拉斯穆斯达特·特耶尔塔"
#   add a ja alias "カーレン・マレナ・ラスムスダッテル・ピグハウグ"
LAST	Aja	"カーレン・マレナ・ラスムスダッテル・ピグハウグ"
#   add a zh alias "卡伦·马莱纳·拉斯穆斯达特·皮格哈乌格"
LAST	Azh	"卡伦·马莱纳·拉斯穆斯达特·皮格哈乌格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000008173986703 Karen Malena Rasmusdatter Tjelta, qualified P1810 subject named as Karen Malena Rasmusdatter Pighaug
LAST	P2600	"6000000008173986703"	P1810	"Karen Malena Rasmusdatter Pighaug"
#   P569 date of birth = +1785-00-00T00:00:00Z/9
LAST	P569	+1785-00-00T00:00:00Z/9	S2600	"6000000008173986703"
#   P570 date of death = +1836-00-00T00:00:00Z/9
LAST	P570	+1836-00-00T00:00:00Z/9	S2600	"6000000008173986703"
#   P40 child = Q141216363 Anne Govertsdtr. Bratland
LAST	P40	Q141216363	S2600	"6000000008173986703"
#   Q141216363 Anne Govertsdtr. Bratland: P25 mother = the item just created
Q141216363	P25	LAST	S2600	"6000000008173986703"
#   the item just created: P735 given name = Q5990536 Malena, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q5990536	P1545	"2"	P3831	Q245025
#   add a mul alias "Karen Malena Tjelta"
LAST	Amul	"Karen Malena Tjelta"

# create a new item
CREATE
#   set the en label to "Knut Johanson Håland"
LAST	Len	"Knut Johanson Håland"
#   set the mul label to "Knut Johanson Håland"
LAST	Lmul	"Knut Johanson Håland"
#   set the ja label to "クヌート・ヨハンソン・ホーランド"
LAST	Lja	"クヌート・ヨハンソン・ホーランド"
#   set the zh label to "克努特·永哈恩松·霍兰"
LAST	Lzh	"克努特·永哈恩松·霍兰"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003376453205 Knut Johanson Håland, qualified P1810 subject named as Knut Johanson Håland
LAST	P2600	"6000000003376453205"	P1810	"Knut Johanson Håland"
#   P569 date of birth = +1500-00-00T00:00:00Z/9
LAST	P569	+1500-00-00T00:00:00Z/9	S2600	"6000000003376453205"
#   P570 date of death = +1546-00-00T00:00:00Z/9
LAST	P570	+1546-00-00T00:00:00Z/9	S2600	"6000000003376453205"
#   P40 child = Q141205930 Olav Knutson Randa Håland
LAST	P40	Q141205930	S2600	"6000000003376453205"
#   Q141205930 Olav Knutson Randa Håland: P22 father = the item just created
Q141205930	P22	LAST	S2600	"6000000003376453205"
#   the item just created: P735 given name = Q943881 Knut
LAST	P735	Q943881

# create a new item
CREATE
#   set the en label to "Lars Jonsen Landsnes"
LAST	Len	"Lars Jonsen Landsnes"
#   set the mul label to "Lars Jonsen Landsnes"
LAST	Lmul	"Lars Jonsen Landsnes"
#   add a mul alias "Lars Jonsen Raunes"
LAST	Amul	"Lars Jonsen Raunes"
#   set the ja label to "ラーシュ・ヨンセン・ランドスネス"
LAST	Lja	"ラーシュ・ヨンセン・ランドスネス"
#   set the zh label to "拉尔斯·永森·拉恩德斯内斯"
LAST	Lzh	"拉尔斯·永森·拉恩德斯内斯"
#   add a ja alias "ラーシュ・ヨンセン・ラウネス"
LAST	Aja	"ラーシュ・ヨンセン・ラウネス"
#   add a zh alias "拉尔斯·永森·拉乌内斯"
LAST	Azh	"拉尔斯·永森·拉乌内斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005607123730 Lars Jonsen Landsnes, qualified P1810 subject named as Lars Jonsen Raunes
LAST	P2600	"6000000005607123730"	P1810	"Lars Jonsen Raunes"
#   P569 date of birth = +1625-00-00T00:00:00Z/9
LAST	P569	+1625-00-00T00:00:00Z/9	S2600	"6000000005607123730"
#   P570 date of death = +1664-00-00T00:00:00Z/9
LAST	P570	+1664-00-00T00:00:00Z/9	S2600	"6000000005607123730"
#   P26 spouse = Q141216371 Guri Pedersdatter Foss
LAST	P26	Q141216371	S2600	"6000000005607123730"
#   Q141216371 Guri Pedersdatter Foss: P26 spouse = the item just created
Q141216371	P26	LAST	S2600	"6000000005607123730"
#   the item just created: P735 given name = Q15635262 Lars
LAST	P735	Q15635262
#   P1449 nickname = en:"Lars Landsnes"
LAST	P1449	en:"Lars Landsnes"
#   add a mul alias "Lars Landsnes"
LAST	Amul	"Lars Landsnes"

# create a new item
CREATE
#   set the en label to "Laurits Leivson Bjørheim"
LAST	Len	"Laurits Leivson Bjørheim"
#   set the mul label to "Laurits Leivson Bjørheim"
LAST	Lmul	"Laurits Leivson Bjørheim"
#   set the ja label to "ラウリトス・レイヴソン・ブヨルヘイム"
LAST	Lja	"ラウリトス・レイヴソン・ブヨルヘイム"
#   set the zh label to "拉乌里特斯·莱伊夫松·布永尔赫伊姆"
LAST	Lzh	"拉乌里特斯·莱伊夫松·布永尔赫伊姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003422289517 Laurits Leivson Bjørheim, qualified P1810 subject named as Laurits Leivson Bjørheim
LAST	P2600	"6000000003422289517"	P1810	"Laurits Leivson Bjørheim"
#   P569 date of birth = +1495-00-00T00:00:00Z/9
LAST	P569	+1495-00-00T00:00:00Z/9	S2600	"6000000003422289517"
#   P570 date of death = +1570-00-00T00:00:00Z/9
LAST	P570	+1570-00-00T00:00:00Z/9	S2600	"6000000003422289517"
#   P40 child = Q141216400 Margreta Lauritsdatter Øvre Bjørheim
LAST	P40	Q141216400	S2600	"6000000003422289517"
#   Q141216400 Margreta Lauritsdatter Øvre Bjørheim: P22 father = the item just created
Q141216400	P22	LAST	S2600	"6000000003422289517"
#   the item just created: P735 given name = Q21061253 Laurits
LAST	P735	Q21061253
#   P1449 nickname = en:"Leifsen"
LAST	P1449	en:"Leifsen"
#   add a mul alias "Leifsen Bjørheim"
LAST	Amul	"Leifsen Bjørheim"
#   add a mul alias "Laurits Bjørheim"
LAST	Amul	"Laurits Bjørheim"

# create a new item
CREATE
#   set the en label to "Malli Svensdatter Lura"
LAST	Len	"Malli Svensdatter Lura"
#   set the mul label to "Malli Svensdatter Lura"
LAST	Lmul	"Malli Svensdatter Lura"
#   set the ja label to "マリ・スヴェンスダッテル・ルラ"
LAST	Lja	"マリ・スヴェンスダッテル・ルラ"
#   set the zh label to "马利·斯韦恩斯达特·卢拉"
LAST	Lzh	"马利·斯韦恩斯达特·卢拉"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000014277480039 Malli Svensdatter Lura, qualified P1810 subject named as Malli Svensdatter Lura
LAST	P2600	"6000000014277480039"	P1810	"Malli Svensdatter Lura"
#   P569 date of birth = +1774-00-00T00:00:00Z/9
LAST	P569	+1774-00-00T00:00:00Z/9	S2600	"6000000014277480039"
#   P570 date of death = +1831-00-00T00:00:00Z/9
LAST	P570	+1831-00-00T00:00:00Z/9	S2600	"6000000014277480039"
#   P40 child = Q141205903 Enok Jonson Rønneberg
LAST	P40	Q141205903	S2600	"6000000014277480039"
#   Q141205903 Enok Jonson Rønneberg: P25 mother = the item just created
Q141205903	P25	LAST	S2600	"6000000014277480039"

# create a new item
CREATE
#   the item just created: set the en label to "Margareta Lejon"
LAST	Len	"Margareta Lejon"
#   set the mul label to "Margareta Lejon"
LAST	Lmul	"Margareta Lejon"
#   add a mul alias "Margareta Bengtsdotter"
LAST	Amul	"Margareta Bengtsdotter"
#   set the ja label to "マルガレータ・レヨン"
LAST	Lja	"マルガレータ・レヨン"
#   set the zh label to "玛格丽塔·莱永恩"
LAST	Lzh	"玛格丽塔·莱永恩"
#   add a ja alias "マルガレータ・ベングトスドッテル"
LAST	Aja	"マルガレータ・ベングトスドッテル"
#   add a zh alias "玛格丽塔·贝恩格特斯多特"
LAST	Azh	"玛格丽塔·贝恩格特斯多特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003827763101 Margareta Lejon, qualified P1810 subject named as Margareta Bengtsdotter
LAST	P2600	"6000000003827763101"	P1810	"Margareta Bengtsdotter"
#   P569 date of birth = +1260-00-00T00:00:00Z/9
LAST	P569	+1260-00-00T00:00:00Z/9	S2600	"6000000003827763101"
#   P570 date of death = +1315-00-00T00:00:00Z/9
LAST	P570	+1315-00-00T00:00:00Z/9	S2600	"6000000003827763101"
#   P26 spouse = Q141198381 Bengt Hafridsson Lejon
LAST	P26	Q141198381	S2600	"6000000003827763101"
#   P40 child = Q5588874 Bryniolf Bengtsson (Hafridssons ätt)
LAST	P40	Q5588874	S2600	"6000000003827763101"
#   Q141198381 Bengt Hafridsson Lejon: P26 spouse = the item just created
Q141198381	P26	LAST	S2600	"6000000003827763101"
#   Q5588874 Bryniolf Bengtsson (Hafridssons ätt): P25 mother = the item just created
Q5588874	P25	LAST	S2600	"6000000003827763101"
#   the item just created: P735 given name = Q8274988 Margareta
LAST	P735	Q8274988
#   P1449 nickname = en:"Margareta Bengtsdotter"
LAST	P1449	en:"Margareta Bengtsdotter"
#   add a mul alias "Margareta Bengtsdotter Lejon"
LAST	Amul	"Margareta Bengtsdotter Lejon"

# create a new item
CREATE
#   set the en label to "Marta Eriksdatter Fotland"
LAST	Len	"Marta Eriksdatter Fotland"
#   set the mul label to "Marta Eriksdatter Fotland"
LAST	Lmul	"Marta Eriksdatter Fotland"
#   set the ja label to "マルタ・エリクスダッテル・フォトランド"
LAST	Lja	"マルタ・エリクスダッテル・フォトランド"
#   set the zh label to "玛尔塔·埃里克斯达特·福特拉恩德"
LAST	Lzh	"玛尔塔·埃里克斯达特·福特拉恩德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000007974940020 Marta Eriksdatter Fotland, qualified P1810 subject named as Marta Eriksdatter Fotland
LAST	P2600	"6000000007974940020"	P1810	"Marta Eriksdatter Fotland"
#   P569 date of birth = +1735-00-00T00:00:00Z/9
LAST	P569	+1735-00-00T00:00:00Z/9	S2600	"6000000007974940020"
#   P570 date of death = +1773-00-00T00:00:00Z/9
LAST	P570	+1773-00-00T00:00:00Z/9	S2600	"6000000007974940020"
#   P40 child = Q141205904 Erik Tollefson Foss-Eikeland
LAST	P40	Q141205904	S2600	"6000000007974940020"
#   Q141205904 Erik Tollefson Foss-Eikeland: P25 mother = the item just created
Q141205904	P25	LAST	S2600	"6000000007974940020"
#   the item just created: P735 given name = Q846741 Marta
LAST	P735	Q846741
#   P734 family name = Q29726874 Fotland
LAST	P734	Q29726874

# create a new item
CREATE
#   set the en label to "Minnie Ronneberg"
LAST	Len	"Minnie Ronneberg"
#   set the mul label to "Minnie Ronneberg"
LAST	Lmul	"Minnie Ronneberg"
#   add a mul alias "Minnie Stromsmoe"
LAST	Amul	"Minnie Stromsmoe"
#   set the ja label to "ミニエ・ロンネベルグ"
LAST	Lja	"ミニエ・ロンネベルグ"
#   set the zh label to "米尼埃·龙内贝格"
LAST	Lzh	"米尼埃·龙内贝格"
#   add a ja alias "ミニエ・ストロムスモエ"
LAST	Aja	"ミニエ・ストロムスモエ"
#   add a zh alias "米尼埃·斯特罗姆斯莫埃"
LAST	Azh	"米尼埃·斯特罗姆斯莫埃"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000117729569834 Minnie Ronneberg, qualified P1810 subject named as Minnie Stromsmoe
LAST	P2600	"6000000117729569834"	P1810	"Minnie Stromsmoe"
#   P569 date of birth = +1900-02-13T00:00:00Z/11
LAST	P569	+1900-02-13T00:00:00Z/11	S2600	"6000000117729569834"
#   P570 date of death = +1971-10-09T00:00:00Z/11
LAST	P570	+1971-10-09T00:00:00Z/11	S2600	"6000000117729569834"
#   P26 spouse = Q141168789 Arnold Ronneberg
LAST	P26	Q141168789	S2600	"6000000117729569834"
#   Q141168789 Arnold Ronneberg: P26 spouse = the item just created
Q141168789	P26	LAST	S2600	"6000000117729569834"
#   the item just created: P735 given name = Q4963706 Minnie
LAST	P735	Q4963706

# create a new item
CREATE
#   set the mul label to "N.N. Jacobsdtr. Koll"
LAST	Lmul	"N.N. Jacobsdtr. Koll"
#   set the ca label to "mare de Olav Knutson Randa Håland"
LAST	Lca	"mare de Olav Knutson Randa Håland"
#   set the da label to "mor til Olav Knutson Randa Håland"
LAST	Lda	"mor til Olav Knutson Randa Håland"
#   set the de label to "Mutter von Olav Knutson Randa Håland"
LAST	Lde	"Mutter von Olav Knutson Randa Håland"
#   set the en label to "mother of Olav Knutson Randa Håland"
LAST	Len	"mother of Olav Knutson Randa Håland"
#   set the es label to "madre de Olav Knutson Randa Håland"
LAST	Les	"madre de Olav Knutson Randa Håland"
#   set the it label to "madre di Olav Knutson Randa Håland"
LAST	Lit	"madre di Olav Knutson Randa Håland"
#   set the ja label to "オラヴ・クヌートソン・ランダ・ホーランドの母"
LAST	Lja	"オラヴ・クヌートソン・ランダ・ホーランドの母"
#   set the nb label to "mor til Olav Knutson Randa Håland"
LAST	Lnb	"mor til Olav Knutson Randa Håland"
#   set the nl label to "moeder van Olav Knutson Randa Håland"
LAST	Lnl	"moeder van Olav Knutson Randa Håland"
#   set the pt label to "mãe de Olav Knutson Randa Håland"
LAST	Lpt	"mãe de Olav Knutson Randa Håland"
#   set the sv label to "mor till Olav Knutson Randa Håland"
LAST	Lsv	"mor till Olav Knutson Randa Håland"
#   set the zh label to "奥拉夫·克努特松·拉恩达·霍兰之母"
LAST	Lzh	"奥拉夫·克努特松·拉恩达·霍兰之母"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000030876120040 N.N. Jacobsdtr. Koll, qualified P1810 subject named as N.N. Jacobsdtr. Koll
LAST	P2600	"6000000030876120040"	P1810	"N.N. Jacobsdtr. Koll"
#   P569 date of birth = +1502-00-00T00:00:00Z/9
LAST	P569	+1502-00-00T00:00:00Z/9	S2600	"6000000030876120040"
#   P570 date of death = +1562-00-00T00:00:00Z/9
LAST	P570	+1562-00-00T00:00:00Z/9	S2600	"6000000030876120040"
#   P40 child = Q141205930 Olav Knutson Randa Håland
LAST	P40	Q141205930	S2600	"6000000030876120040"
#   Q141205930 Olav Knutson Randa Håland: P25 mother = the item just created
Q141205930	P25	LAST	S2600	"6000000030876120040"

# create a new item
CREATE
#   the item just created: set the mul label to "NN (Frille)"
LAST	Lmul	"NN (Frille)"
#   set the ca label to "mare de Ramborg Knutsdotter Lejon"
LAST	Lca	"mare de Ramborg Knutsdotter Lejon"
#   set the da label to "mor til Ramborg Knutsdotter Lejon"
LAST	Lda	"mor til Ramborg Knutsdotter Lejon"
#   set the de label to "Mutter von Ramborg Knutsdotter Lejon"
LAST	Lde	"Mutter von Ramborg Knutsdotter Lejon"
#   set the en label to "mother of Ramborg Knutsdotter Lejon"
LAST	Len	"mother of Ramborg Knutsdotter Lejon"
#   set the es label to "madre de Ramborg Knutsdotter Lejon"
LAST	Les	"madre de Ramborg Knutsdotter Lejon"
#   set the it label to "madre di Ramborg Knutsdotter Lejon"
LAST	Lit	"madre di Ramborg Knutsdotter Lejon"
#   set the ja label to "ラムボルグ・クヌトスドッテル・レヨンの母"
LAST	Lja	"ラムボルグ・クヌトスドッテル・レヨンの母"
#   set the nb label to "mor til Ramborg Knutsdotter Lejon"
LAST	Lnb	"mor til Ramborg Knutsdotter Lejon"
#   set the nl label to "moeder van Ramborg Knutsdotter Lejon"
LAST	Lnl	"moeder van Ramborg Knutsdotter Lejon"
#   set the pt label to "mãe de Ramborg Knutsdotter Lejon"
LAST	Lpt	"mãe de Ramborg Knutsdotter Lejon"
#   set the sv label to "mor till Ramborg Knutsdotter Lejon"
LAST	Lsv	"mor till Ramborg Knutsdotter Lejon"
#   set the zh label to "拉姆博尔格·克努特斯多特·莱永恩之母"
LAST	Lzh	"拉姆博尔格·克努特斯多特·莱永恩之母"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000004645401302 NN (Frille), qualified P1810 subject named as NN (Frille)
LAST	P2600	"6000000004645401302"	P1810	"NN (Frille)"
#   P26 spouse = Q5915800 Knut Algotsson
LAST	P26	Q5915800	S2600	"6000000004645401302"
#   P40 child = Q141216350 Ramborg Knutsdotter Lejon
LAST	P40	Q141216350	S2600	"6000000004645401302"
#   Q5915800 Knut Algotsson: P26 spouse = the item just created
Q5915800	P26	LAST	S2600	"6000000004645401302"
#   Q141216350 Ramborg Knutsdotter Lejon: P25 mother = the item just created
Q141216350	P25	LAST	S2600	"6000000004645401302"

# create a new item
CREATE
#   the item just created: set the en label to "Nils Larsen Raunes"
LAST	Len	"Nils Larsen Raunes"
#   set the mul label to "Nils Larsen Raunes"
LAST	Lmul	"Nils Larsen Raunes"
#   add a mul alias "Nils Larsen Landsnes"
LAST	Amul	"Nils Larsen Landsnes"
#   set the ja label to "ニルス・ラーシェン・ラウネス"
LAST	Lja	"ニルス・ラーシェン・ラウネス"
#   set the zh label to "尼尔斯·拉尔森·拉乌内斯"
LAST	Lzh	"尼尔斯·拉尔森·拉乌内斯"
#   add a ja alias "ニルス・ラーシェン・ランドスネス"
LAST	Aja	"ニルス・ラーシェン・ランドスネス"
#   add a zh alias "尼尔斯·拉尔森·拉恩德斯内斯"
LAST	Azh	"尼尔斯·拉尔森·拉恩德斯内斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000001770188397 Nils Larsen Raunes, qualified P1810 subject named as Nils Larsen Landsnes
LAST	P2600	"6000000001770188397"	P1810	"Nils Larsen Landsnes"
#   P569 date of birth = +1652-00-00T00:00:00Z/9
LAST	P569	+1652-00-00T00:00:00Z/9	S2600	"6000000001770188397"
#   P570 date of death = +1729-00-00T00:00:00Z/9
LAST	P570	+1729-00-00T00:00:00Z/9	S2600	"6000000001770188397"
#   P25 mother = Q141216371 Guri Pedersdatter Foss
LAST	P25	Q141216371	S2600	"6000000001770188397"
#   Q141216371 Guri Pedersdatter Foss: P40 child = the item just created
Q141216371	P40	LAST	S2600	"6000000001770188397"
#   the item just created: P735 given name = Q16423038 Nils
LAST	P735	Q16423038
#   P1449 nickname = en:"Nils Raunes"
LAST	P1449	en:"Nils Raunes"
#   add a mul alias "Nils Raunes"
LAST	Amul	"Nils Raunes"

# create a new item
CREATE
#   set the en label to "Norman Charles Tunheim"
LAST	Len	"Norman Charles Tunheim"
#   set the mul label to "Norman Charles Tunheim"
LAST	Lmul	"Norman Charles Tunheim"
#   set the ja label to "ノルマン・カルレス・トゥンヘイム"
LAST	Lja	"ノルマン・カルレス・トゥンヘイム"
#   set the zh label to "诺尔马恩·卡尔莱斯·通海姆"
LAST	Lzh	"诺尔马恩·卡尔莱斯·通海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000009736181790 Norman Charles Tunheim, qualified P1810 subject named as Norman Charles Tunheim
LAST	P2600	"6000000009736181790"	P1810	"Norman Charles Tunheim"
#   P569 date of birth = +1940-10-06T00:00:00Z/11
LAST	P569	+1940-10-06T00:00:00Z/11	S2600	"6000000009736181790"
#   P570 date of death = +1992-05-18T00:00:00Z/11
LAST	P570	+1992-05-18T00:00:00Z/11	S2600	"6000000009736181790"
#   P22 father = Q141189101 Samuel Tunheim
LAST	P22	Q141189101	S2600	"6000000009736181790"
#   Q141189101 Samuel Tunheim: P40 child = the item just created
Q141189101	P40	LAST	S2600	"6000000009736181790"
#   the item just created: P735 given name = Q1218555 Norman, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q1218555	P1545	"1"	P7452	Q3409033
#   P735 given name = Q2958359 Charles, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q2958359	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Orm Ånonsen"
LAST	Len	"Orm Ånonsen"
#   set the mul label to "Orm Ånonsen"
LAST	Lmul	"Orm Ånonsen"
#   add a mul alias "Orm Ånensen"
LAST	Amul	"Orm Ånensen"
#   set the ja label to "オルム・オーノンセン"
LAST	Lja	"オルム・オーノンセン"
#   set the zh label to "奥尔姆·奥诺恩森"
LAST	Lzh	"奥尔姆·奥诺恩森"
#   add a ja alias "オルム・オーネンセン"
LAST	Aja	"オルム・オーネンセン"
#   add a zh alias "奥尔姆·奥内恩森"
LAST	Azh	"奥尔姆·奥内恩森"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000002301437734 Orm Ånonsen, qualified P1810 subject named as Orm Ånensen
LAST	P2600	"6000000002301437734"	P1810	"Orm Ånensen"
#   P569 date of birth = +1520-00-00T00:00:00Z/9
LAST	P569	+1520-00-00T00:00:00Z/9	S2600	"6000000002301437734"
#   P570 date of death = +1601-00-00T00:00:00Z/9
LAST	P570	+1601-00-00T00:00:00Z/9	S2600	"6000000002301437734"
#   P40 child = Q141205922 Marit Ormsd Byre
LAST	P40	Q141205922	S2600	"6000000002301437734"
#   Q141205922 Marit Ormsd Byre: P22 father = the item just created
Q141205922	P22	LAST	S2600	"6000000002301437734"
#   the item just created: P735 given name = Q5199298 Orm
LAST	P735	Q5199298
#   P1449 nickname = en:"Orm Stokka"
LAST	P1449	en:"Orm Stokka"
#   add a mul alias "Orm Stokka Ånonsen"
LAST	Amul	"Orm Stokka Ånonsen"

# create a new item
CREATE
#   set the mul label to "NN"
LAST	Lmul	"NN"
#   set the ca label to "fill de Arnold Ronneberg"
LAST	Lca	"fill de Arnold Ronneberg"
#   set the da label to "søn af Arnold Ronneberg"
LAST	Lda	"søn af Arnold Ronneberg"
#   set the de label to "Sohn von Arnold Ronneberg"
LAST	Lde	"Sohn von Arnold Ronneberg"
#   set the en label to "son of Arnold Ronneberg"
LAST	Len	"son of Arnold Ronneberg"
#   set the es label to "hijo de Arnold Ronneberg"
LAST	Les	"hijo de Arnold Ronneberg"
#   set the it label to "figlio di Arnold Ronneberg"
LAST	Lit	"figlio di Arnold Ronneberg"
#   set the ja label to "アルノルド・ロンネベルグの息子"
LAST	Lja	"アルノルド・ロンネベルグの息子"
#   set the nb label to "sønn av Arnold Ronneberg"
LAST	Lnb	"sønn av Arnold Ronneberg"
#   set the nl label to "zoon van Arnold Ronneberg"
LAST	Lnl	"zoon van Arnold Ronneberg"
#   set the pt label to "filho de Arnold Ronneberg"
LAST	Lpt	"filho de Arnold Ronneberg"
#   set the sv label to "son till Arnold Ronneberg"
LAST	Lsv	"son till Arnold Ronneberg"
#   set the zh label to "阿诺德·龙内贝格之子"
LAST	Lzh	"阿诺德·龙内贝格之子"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000117728698004 NN Private, qualified P1810 subject named as Private
LAST	P2600	"6000000117728698004"	P1810	"Private"
#   P22 father = Q141168789 Arnold Ronneberg
LAST	P22	Q141168789	S2600	"6000000117728698004"
#   Q141168789 Arnold Ronneberg: P40 child = the item just created
Q141168789	P40	LAST	S2600	"6000000117728698004"

# create a new item
CREATE
#   the item just created: set the en label to "Siri Garborg Talle"
LAST	Len	"Siri Garborg Talle"
#   set the mul label to "Siri Garborg Talle"
LAST	Lmul	"Siri Garborg Talle"
#   set the ja label to "シーリ・ガルボルグ・タッレ"
LAST	Lja	"シーリ・ガルボルグ・タッレ"
#   set the zh label to "西丽·加尔博格·塔勒"
LAST	Lzh	"西丽·加尔博格·塔勒"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000177687513857 Siri Garborg Talle, qualified P1810 subject named as Siri Garborg Talle
LAST	P2600	"6000000177687513857"	P1810	"Siri Garborg Talle"
#   P569 date of birth = +1928-11-12T00:00:00Z/11
LAST	P569	+1928-11-12T00:00:00Z/11	S2600	"6000000177687513857"
#   P570 date of death = +2019-03-29T00:00:00Z/11
LAST	P570	+2019-03-29T00:00:00Z/11	S2600	"6000000177687513857"
#   P22 father = Q141216404 Sigurd Sverre Ravn Talle
LAST	P22	Q141216404	S2600	"6000000177687513857"
#   P25 mother = Q141168830 Ingeborg Talle
LAST	P25	Q141168830	S2600	"6000000177687513857"
#   Q141216404 Sigurd Sverre Ravn Talle: P40 child = the item just created
Q141216404	P40	LAST	S2600	"6000000177687513857"
#   Q141168830 Ingeborg Talle: P40 child = the item just created
Q141168830	P40	LAST	S2600	"6000000177687513857"
#   the item just created: P735 given name = Q1772342 Siri, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q1772342	P1545	"1"	P7452	Q3409033

# create a new item
CREATE
#   set the en label to "Sverre Helmer Wendt"
LAST	Len	"Sverre Helmer Wendt"
#   set the mul label to "Sverre Helmer Wendt"
LAST	Lmul	"Sverre Helmer Wendt"
#   set the ja label to "スヴェレ・ヘルメル・ヴェント"
LAST	Lja	"スヴェレ・ヘルメル・ヴェント"
#   set the zh label to "斯韦雷·赫尔梅尔·温特"
LAST	Lzh	"斯韦雷·赫尔梅尔·温特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000048057134821 Sverre Helmer Wendt, qualified P1810 subject named as Sverre Helmer Wendt
LAST	P2600	"6000000048057134821"	P1810	"Sverre Helmer Wendt"
#   P569 date of birth = +1890-09-17T00:00:00Z/11
LAST	P569	+1890-09-17T00:00:00Z/11	S2600	"6000000048057134821"
#   P570 date of death = +1963-10-26T00:00:00Z/11
LAST	P570	+1963-10-26T00:00:00Z/11	S2600	"6000000048057134821"
#   P22 father = Q141216386 Jens Wilhelm Wendt
LAST	P22	Q141216386	S2600	"6000000048057134821"
#   P25 mother = Q141216377 Hanna Sofie Wendt
LAST	P25	Q141216377	S2600	"6000000048057134821"
#   Q141216386 Jens Wilhelm Wendt: P40 child = the item just created
Q141216386	P40	LAST	S2600	"6000000048057134821"
#   Q141216377 Hanna Sofie Wendt: P40 child = the item just created
Q141216377	P40	LAST	S2600	"6000000048057134821"
#   the item just created: P735 given name = Q970810 Sverre, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q970810	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1603195 Helmer, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1603195	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Thekla Cecilie Dybo"
LAST	Len	"Thekla Cecilie Dybo"
#   set the mul label to "Thekla Cecilie Dybo"
LAST	Lmul	"Thekla Cecilie Dybo"
#   add a mul alias "Thekla Cecilie Nyvold"
LAST	Amul	"Thekla Cecilie Nyvold"
#   set the ja label to "テクラ・セシリエ・ディボ"
LAST	Lja	"テクラ・セシリエ・ディボ"
#   set the zh label to "特克拉·塞西莉厄·迪博"
LAST	Lzh	"特克拉·塞西莉厄·迪博"
#   add a ja alias "テクラ・セシリエ・ニーヴォル"
LAST	Aja	"テクラ・セシリエ・ニーヴォル"
#   add a zh alias "特克拉·塞西莉厄·尼沃尔"
LAST	Azh	"特克拉·塞西莉厄·尼沃尔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000021198276198 Thekla Cecilie Dybo, qualified P1810 subject named as Thekla Cecilie Nyvold
LAST	P2600	"6000000021198276198"	P1810	"Thekla Cecilie Nyvold"
#   P569 date of birth = +1889-08-14T00:00:00Z/11
LAST	P569	+1889-08-14T00:00:00Z/11	S2600	"6000000021198276198"
#   P570 date of death = +1983-06-07T00:00:00Z/11
LAST	P570	+1983-06-07T00:00:00Z/11	S2600	"6000000021198276198"
#   P22 father = Q138474188 Hans Syvertsen Nyvold
LAST	P22	Q138474188	S2600	"6000000021198276198"
#   P25 mother = Q141178197 Elisabeth Nyvold
LAST	P25	Q141178197	S2600	"6000000021198276198"
#   Q138474188 Hans Syvertsen Nyvold: P40 child = the item just created
Q138474188	P40	LAST	S2600	"6000000021198276198"
#   Q141178197 Elisabeth Nyvold: P40 child = the item just created
Q141178197	P40	LAST	S2600	"6000000021198276198"
#   the item just created: P735 given name = Q16275183 Cecilie, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q16275183	P1545	"2"	P3831	Q245025
#   P1449 nickname = en:"Tekla Cecilie Nyvold"
LAST	P1449	en:"Tekla Cecilie Nyvold"
#   add a mul alias "Tekla Cecilie Nyvold Dybo"
LAST	Amul	"Tekla Cecilie Nyvold Dybo"

# create a new item
CREATE
#   set the en label to "Torborg Toresdatter Norheim"
LAST	Len	"Torborg Toresdatter Norheim"
#   set the mul label to "Torborg Toresdatter Norheim"
LAST	Lmul	"Torborg Toresdatter Norheim"
#   add a mul alias "Torborg Toresdatter Store Oma"
LAST	Amul	"Torborg Toresdatter Store Oma"
#   set the ja label to "トルボルグ・トーレスダッテル・ノルヘイム"
LAST	Lja	"トルボルグ・トーレスダッテル・ノルヘイム"
#   set the zh label to "托尔博尔格·托雷斯达特·诺尔赫伊姆"
LAST	Lzh	"托尔博尔格·托雷斯达特·诺尔赫伊姆"
#   add a ja alias "トルボルグ・トーレスダッテル・ストレ・オマ"
LAST	Aja	"トルボルグ・トーレスダッテル・ストレ・オマ"
#   add a zh alias "托尔博尔格·托雷斯达特·斯托雷·奥马"
LAST	Azh	"托尔博尔格·托雷斯达特·斯托雷·奥马"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000009152152523 Torborg Toresdatter Norheim, qualified P1810 subject named as Torborg Toresdatter Store Oma
LAST	P2600	"6000000009152152523"	P1810	"Torborg Toresdatter Store Oma"
#   P569 date of birth = +1683-00-00T00:00:00Z/9
LAST	P569	+1683-00-00T00:00:00Z/9	S2600	"6000000009152152523"
#   P570 date of death = +1733-00-00T00:00:00Z/9
LAST	P570	+1733-00-00T00:00:00Z/9	S2600	"6000000009152152523"
#   P40 child = Q141200127 Ådne Hansen Grøtheim
LAST	P40	Q141200127	S2600	"6000000009152152523"
#   Q141200127 Ådne Hansen Grøtheim: P25 mother = the item just created
Q141200127	P25	LAST	S2600	"6000000009152152523"
#   the item just created: P735 given name = Q33101446 Torborg
LAST	P735	Q33101446
#   P734 family name = Q30350309 Norheim, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q30350309	P3831	Q28418670
#   add a mul alias "Torborg Norheim"
LAST	Amul	"Torborg Norheim"

# create a new item
CREATE
#   set the en label to "Torger Torgerson Stokka"
LAST	Len	"Torger Torgerson Stokka"
#   set the mul label to "Torger Torgerson Stokka"
LAST	Lmul	"Torger Torgerson Stokka"
#   set the ja label to "トルゲル・トルゲルソン・ストカ"
LAST	Lja	"トルゲル・トルゲルソン・ストカ"
#   set the zh label to "托尔盖尔·托尔盖尔松·斯托卡"
LAST	Lzh	"托尔盖尔·托尔盖尔松·斯托卡"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003491986806 Torger Torgerson Stokka, qualified P1810 subject named as Torger Torgerson Stokka
LAST	P2600	"6000000003491986806"	P1810	"Torger Torgerson Stokka"
#   P569 date of birth = +1833-11-28T00:00:00Z/11
LAST	P569	+1833-11-28T00:00:00Z/11	S2600	"6000000003491986806"
#   P570 date of death = +1914-01-06T00:00:00Z/11
LAST	P570	+1914-01-06T00:00:00Z/11	S2600	"6000000003491986806"
#   P26 spouse = Q141216365 Berte Karine Jonsdatter Stokka
LAST	P26	Q141216365	S2600	"6000000003491986806"
#   Q141216365 Berte Karine Jonsdatter Stokka: P26 spouse = the item just created
Q141216365	P26	LAST	S2600	"6000000003491986806"
#   the item just created: P735 given name = Q2444019 Torger
LAST	P735	Q2444019
#   Q141216403 Olof Nilsson: P26 spouse = Q141216398 Malin Olofsdotter
Q141216403	P26	Q141216398	S2600	"375729629520007230"
#   Q141216398 Malin Olofsdotter: P26 spouse = Q141216403 Olof Nilsson
Q141216398	P26	Q141216403	S2600	"4982890984490082253"
#   Q141216397 Malin Andersdotter: P26 spouse = Q141216357 Anders Jacobsson
Q141216397	P26	Q141216357	S2600	"6000000000305413766"
#   Q141216357 Anders Jacobsson: P26 spouse = Q141216397 Malin Andersdotter
Q141216357	P26	Q141216397	S2600	"6000000001138735296"
#   Q19061035 Guttorm Àsulfsson à Rein: P735 given name = Q20755782 Guttorm, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q19061035	P735	Q20755782	P1545	"1"	P7452	Q3409033
#   P734 family name = Q25521651 Rein
Q19061035	P734	Q25521651
#   Q141216369 Gard Toresson Talgje: P26 spouse = Q141216350 Ramborg Knutsdotter Lejon
Q141216369	P26	Q141216350	S2600	"6000000002572728015"
#   Q141216387 Johannes Svensen Obrestad: P26 spouse = Q141216363 Anne Govertsdtr. Bratland
Q141216387	P26	Q141216363	S2600	"6000000003491978246"
#   Q141216350 Ramborg Knutsdotter Lejon: P26 spouse = Q141216369 Gard Toresson Talgje
Q141216350	P26	Q141216369	S2600	"6000000004870648136"
#   Q141216377 Hanna Sofie Wendt: P26 spouse = Q141216386 Jens Wilhelm Wendt
Q141216377	P26	Q141216386	S2600	"6000000005441361475"
#   Q141216396 Lisbet Olavsdatter Håland: P25 mother = Q141216400 Margreta Lauritsdatter Øvre Bjørheim
Q141216396	P25	Q141216400	S2600	"6000000005607268895"
#   Q141216381 Hans Rasmussen Låge-Håland: P26 spouse = Q141216383 Ingeborg Eriksdatter Bjorland
Q141216381	P26	Q141216383	S2600	"6000000009127934231"
#   Q101247444 Ingegerd Svantepolksdotter: P40 child = Q19842232 Algot Bryniolfsson
Q101247444	P40	Q19842232	S2600	"6000000011239201122"
#   Q141216389 Jon Jonsson: P26 spouse = Q141216399 Margareta Nilsdotter
Q141216389	P26	Q141216399	S2600	"6000000013354249769"
#   Q141216383 Ingeborg Eriksdatter Bjorland: P26 spouse = Q141216381 Hans Rasmussen Låge-Håland
Q141216383	P26	Q141216381	S2600	"6000000014100949863"
#   Q141216400 Margreta Lauritsdatter Øvre Bjørheim: P40 child = Q141216396 Lisbet Olavsdatter Håland
Q141216400	P40	Q141216396	S2600	"6000000016246443406"
#   Q141216401 Mariet Danielsdotter: P5056 patronym or matronym = Q140226461, qualified P144 based on Q141205902 Daniel Olofsson
Q141216401	P5056	Q140226461	P144	Q141205902
#   Q141216399 Margareta Nilsdotter: P26 spouse = Q141216389 Jon Jonsson
Q141216399	P26	Q141216389	S2600	"6000000017799612472"
#   Q141216386 Jens Wilhelm Wendt: P26 spouse = Q141216377 Hanna Sofie Wendt
Q141216386	P26	Q141216377	S2600	"6000000021079642735"
#   Q141216354 NN Garborg: P734 family name = Q30250555 Garborg
Q141216354	P734	Q30250555
#   Q141216363 Anne Govertsdtr. Bratland: P26 spouse = Q141216387 Johannes Svensen Obrestad
Q141216363	P26	Q141216387	S2600	"6000000169074443823"
#   Q141216379 Hans Halvardsen Grøtheim: P22 father = Q141216374 Halvard Assersen Grøtheim
Q141216379	P22	Q141216374	S2600	"6000000224130977838"
#   Q141216374 Halvard Assersen Grøtheim: P40 child = Q141216379 Hans Halvardsen Grøtheim
Q141216374	P40	Q141216379	S2600	"6000000225229552897"

