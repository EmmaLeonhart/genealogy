# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   2217 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------

# ------------------------------------------------------------------------
# LABEL CORRECTIONS -- existing items whose label is not what our tree now
#   says. derive-labels.py made the married form primary on 2026-08-29 and
#   these items predate it. The outgoing label is preserved as an Amul on
#   the line above the Lmul that replaces it, so nothing hand-written is
#   lost. This block SHRINKS as it is run -- it is not the clan block.
# ------------------------------------------------------------------------
#   Q141168784: holds 'Aagot Garborg'; ours is 'Aagot Wendt'
#   Q141168784: keep the outgoing label as an alias before it is replaced
Q141168784	Amul	"Aagot Garborg"
#   Q141168784: set the mul label to 'Aagot Wendt'
Q141168784	Lmul	"Aagot Wendt"
#   Q141168784: set the en label to 'Aagot Wendt'
Q141168784	Len	"Aagot Wendt"
#   Q141168784: set the ja label
Q141168784	Lja	"オーゴット・ヴェント"
#   Q141168784: set the zh label
Q141168784	Lzh	"奥高特·温特"
#   Q141168830: holds 'Ingeborg Garborg'; ours is 'Ingeborg Talle'
#   Q141168830: keep the outgoing label as an alias before it is replaced
Q141168830	Amul	"Ingeborg Garborg"
#   Q141168830: set the mul label to 'Ingeborg Talle'
Q141168830	Lmul	"Ingeborg Talle"
#   Q141168830: set the en label to 'Ingeborg Talle'
Q141168830	Len	"Ingeborg Talle"
#   Q141168830: set the ja label
Q141168830	Lja	"インゲボルグ・タッレ"
#   Q141168830: set the zh label
Q141168830	Lzh	"英厄堡·塔勒"
#   Q141198834: holds 'Gunnbjørn Jonson Aukland'; ours is 'Gunnbjørn Jonson Mjølhus'
#   Q141198834: keep the outgoing label as an alias before it is replaced
Q141198834	Amul	"Gunnbjørn Jonson Aukland"
#   Q141198834: set the mul label to 'Gunnbjørn Jonson Mjølhus'
Q141198834	Lmul	"Gunnbjørn Jonson Mjølhus"
#   Q141198834: set the en label to 'Gunnbjørn Jonson Mjølhus'
Q141198834	Len	"Gunnbjørn Jonson Mjølhus"
#   Q141198834: set the ja label
Q141198834	Lja	"グンブヨルン・ヨンソン・ムヨルフス"
#   Q141198834: set the zh label
Q141198834	Lzh	"古恩布永尔恩·永松·姆永尔胡斯"

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Ingrid Guttormsdotter"
LAST	Len	"Ingrid Guttormsdotter"
#   set the mul label to "Ingrid Guttormsdotter"
LAST	Lmul	"Ingrid Guttormsdotter"
#   set the ja label to "イングリド・グトルムスドッテル"
LAST	Lja	"イングリド・グトルムスドッテル"
#   set the zh label to "伊恩格里德·古托尔姆斯多特"
LAST	Lzh	"伊恩格里德·古托尔姆斯多特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000000771986019 Ingrid Guttormsdotter, qualified P1810 subject named as Ingrid Guttormsdotter
LAST	P2600	"6000000000771986019"	P1810	"Ingrid Guttormsdotter"
#   P569 date of birth = +1135-00-00T00:00:00Z/9
LAST	P569	+1135-00-00T00:00:00Z/9	S2600	"6000000000771986019"
#   P40 child = Q4953376 Helena Guttormsdatter
LAST	P40	Q4953376	S2600	"6000000000771986019"
#   Q4953376 Helena Guttormsdatter: P25 mother = the item just created
Q4953376	P25	LAST	S2600	"6000000000771986019"
#   the item just created: P735 given name = Q903741 Ingrid
LAST	P735	Q903741
#   P1449 nickname = en:"Ingridr Guðþormsdóttir Rein"
LAST	P1449	en:"Ingridr Guðþormsdóttir Rein"
#   add a mul alias "Ingridr Guðþormsdóttir Rein Guttormsdotter"
LAST	Amul	"Ingridr Guðþormsdóttir Rein Guttormsdotter"

# create a new item
CREATE
#   set the en label to "Ramborg Knutsdotter Lejon"
LAST	Len	"Ramborg Knutsdotter Lejon"
#   set the mul label to "Ramborg Knutsdotter Lejon"
LAST	Lmul	"Ramborg Knutsdotter Lejon"
#   set the ja label to "ラムボルグ・クヌトスドッテル・レヨン"
LAST	Lja	"ラムボルグ・クヌトスドッテル・レヨン"
#   set the zh label to "拉姆博尔格·克努特斯多特·莱永恩"
LAST	Lzh	"拉姆博尔格·克努特斯多特·莱永恩"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000004870648136 Ramborg Knutsdotter Lejon, qualified P1810 subject named as Ramborg Knutsdotter Lejon
LAST	P2600	"6000000004870648136"	P1810	"Ramborg Knutsdotter Lejon"
#   P569 date of birth = +1360-00-00T00:00:00Z/9
LAST	P569	+1360-00-00T00:00:00Z/9	S2600	"6000000004870648136"
#   P570 date of death = +1408-00-00T00:00:00Z/9
LAST	P570	+1408-00-00T00:00:00Z/9	S2600	"6000000004870648136"
#   P22 father = Q5915800 Knut Algotsson
LAST	P22	Q5915800	S2600	"6000000004870648136"
#   P40 child = Q141205942 Tore II Gardson Gard
LAST	P40	Q141205942	S2600	"6000000004870648136"
#   Q5915800 Knut Algotsson: P40 child = the item just created
Q5915800	P40	LAST	S2600	"6000000004870648136"
#   Q141205942 Tore II Gardson Gard: P25 mother = the item just created
Q141205942	P25	LAST	S2600	"6000000004870648136"
#   the item just created: add a mul alias "Ramborg Lejon"
LAST	Amul	"Ramborg Lejon"

# create a new item
CREATE
#   set the mul label to "NN Garborg"
LAST	Lmul	"NN Garborg"
#   set the ca label to "filla de Arne Olaus Fjørtoft Garborg"
LAST	Lca	"filla de Arne Olaus Fjørtoft Garborg"
#   set the da label to "datter af Arne Olaus Fjørtoft Garborg"
LAST	Lda	"datter af Arne Olaus Fjørtoft Garborg"
#   set the de label to "Tochter von Arne Olaus Fjørtoft Garborg"
LAST	Lde	"Tochter von Arne Olaus Fjørtoft Garborg"
#   set the en label to "daughter of Arne Olaus Fjørtoft Garborg"
LAST	Len	"daughter of Arne Olaus Fjørtoft Garborg"
#   set the es label to "hija de Arne Olaus Fjørtoft Garborg"
LAST	Les	"hija de Arne Olaus Fjørtoft Garborg"
#   set the it label to "figlia di Arne Olaus Fjørtoft Garborg"
LAST	Lit	"figlia di Arne Olaus Fjørtoft Garborg"
#   set the ja label to "アルネ・オーラウス・フョルトフト・ガルボルグの娘"
LAST	Lja	"アルネ・オーラウス・フョルトフト・ガルボルグの娘"
#   set the nb label to "datter av Arne Olaus Fjørtoft Garborg"
LAST	Lnb	"datter av Arne Olaus Fjørtoft Garborg"
#   set the nl label to "dochter van Arne Olaus Fjørtoft Garborg"
LAST	Lnl	"dochter van Arne Olaus Fjørtoft Garborg"
#   set the pt label to "filha de Arne Olaus Fjørtoft Garborg"
LAST	Lpt	"filha de Arne Olaus Fjørtoft Garborg"
#   set the sv label to "dotter till Arne Olaus Fjørtoft Garborg"
LAST	Lsv	"dotter till Arne Olaus Fjørtoft Garborg"
#   set the zh label to "阿尔内·奥劳斯·夫约托夫特·加尔博格之女"
LAST	Lzh	"阿尔内·奥劳斯·夫约托夫特·加尔博格之女"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000021223364767 NN Garborg, qualified P1810 subject named as <private> Garborg
LAST	P2600	"6000000021223364767"	P1810	"<private> Garborg"
#   P22 father = Q11959067 Arne Olaus Fjørtoft Garborg
LAST	P22	Q11959067	S2600	"6000000021223364767"
#   P25 mother = Q141168785 Aagot Garborg
LAST	P25	Q141168785	S2600	"6000000021223364767"
#   Q11959067 Arne Olaus Fjørtoft Garborg: P40 child = the item just created
Q11959067	P40	LAST	S2600	"6000000021223364767"
#   Q141168785 Aagot Garborg: P40 child = the item just created
Q141168785	P40	LAST	S2600	"6000000021223364767"

# create a new item
CREATE
#   the item just created: set the mul label to "NN Undheim"
LAST	Lmul	"NN Undheim"
#   set the ca label to "filla de Astri Torchelsdatter Øvre Time"
LAST	Lca	"filla de Astri Torchelsdatter Øvre Time"
#   set the da label to "datter af Astri Torchelsdatter Øvre Time"
LAST	Lda	"datter af Astri Torchelsdatter Øvre Time"
#   set the de label to "Tochter von Astri Torchelsdatter Øvre Time"
LAST	Lde	"Tochter von Astri Torchelsdatter Øvre Time"
#   set the en label to "daughter of Astri Torchelsdatter Øvre Time"
LAST	Len	"daughter of Astri Torchelsdatter Øvre Time"
#   set the es label to "hija de Astri Torchelsdatter Øvre Time"
LAST	Les	"hija de Astri Torchelsdatter Øvre Time"
#   set the it label to "figlia di Astri Torchelsdatter Øvre Time"
LAST	Lit	"figlia di Astri Torchelsdatter Øvre Time"
#   set the ja label to "アストリ・トルケルスダッテル・オヴレ・ティメの娘"
LAST	Lja	"アストリ・トルケルスダッテル・オヴレ・ティメの娘"
#   set the nb label to "datter av Astri Torchelsdatter Øvre Time"
LAST	Lnb	"datter av Astri Torchelsdatter Øvre Time"
#   set the nl label to "dochter van Astri Torchelsdatter Øvre Time"
LAST	Lnl	"dochter van Astri Torchelsdatter Øvre Time"
#   set the pt label to "filha de Astri Torchelsdatter Øvre Time"
LAST	Lpt	"filha de Astri Torchelsdatter Øvre Time"
#   set the sv label to "dotter till Astri Torchelsdatter Øvre Time"
LAST	Lsv	"dotter till Astri Torchelsdatter Øvre Time"
#   set the zh label to "阿斯特丽·托尔凯尔斯达特·奥夫雷·蒂梅之女"
LAST	Lzh	"阿斯特丽·托尔凯尔斯达特·奥夫雷·蒂梅之女"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003731955050 NN Undheim, qualified P1810 subject named as <private> Undheim
LAST	P2600	"6000000003731955050"	P1810	"<private> Undheim"
#   P22 father = Q141198370 NN Skårland
LAST	P22	Q141198370	S2600	"6000000003731955050"
#   P25 mother = Q141198375 Astri Torchelsdatter Øvre Time
LAST	P25	Q141198375	S2600	"6000000003731955050"
#   Q141198370 NN Skårland: P40 child = the item just created
Q141198370	P40	LAST	S2600	"6000000003731955050"
#   Q141198375 Astri Torchelsdatter Øvre Time: P40 child = the item just created
Q141198375	P40	LAST	S2600	"6000000003731955050"

# create a new item
CREATE
#   the item just created: set the en label to "Anders Jacobsson"
LAST	Len	"Anders Jacobsson"
#   set the mul label to "Anders Jacobsson"
LAST	Lmul	"Anders Jacobsson"
#   set the ja label to "アンデルス・ヤコブソン"
LAST	Lja	"アンデルス・ヤコブソン"
#   set the zh label to "阿恩德尔斯·雅各布松"
LAST	Lzh	"阿恩德尔斯·雅各布松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000001138735296 Anders Jacobsson, qualified P1810 subject named as Anders Jacobsson
LAST	P2600	"6000000001138735296"	P1810	"Anders Jacobsson"
#   P569 date of birth = +1488-00-00T00:00:00Z/9
LAST	P569	+1488-00-00T00:00:00Z/9	S2600	"6000000001138735296"
#   P570 date of death = +1539-00-00T00:00:00Z/9
LAST	P570	+1539-00-00T00:00:00Z/9	S2600	"6000000001138735296"
#   P40 child = Q141199819 Anna Andersdotter
LAST	P40	Q141199819	S2600	"6000000001138735296"
#   Q141199819 Anna Andersdotter: P22 father = the item just created
Q141199819	P22	LAST	S2600	"6000000001138735296"
#   the item just created: P735 given name = Q8843357 Anders
LAST	P735	Q8843357

# create a new item
CREATE
#   set the en label to "Andrew J. Bakke"
LAST	Len	"Andrew J. Bakke"
#   set the mul label to "Andrew J. Bakke"
LAST	Lmul	"Andrew J. Bakke"
#   add a mul alias "Andrew J. Iverson Bakke"
LAST	Amul	"Andrew J. Iverson Bakke"
#   set the ja label to "アンドレヴ・イ・バケ"
LAST	Lja	"アンドレヴ・イ・バケ"
#   set the zh label to "阿恩德雷夫·伊·巴凯"
LAST	Lzh	"阿恩德雷夫·伊·巴凯"
#   add a ja alias "アンドレヴ・イ・イーヴェション・バケ"
LAST	Aja	"アンドレヴ・イ・イーヴェション・バケ"
#   add a zh alias "阿恩德雷夫·伊·艾弗森·巴凯"
LAST	Azh	"阿恩德雷夫·伊·艾弗森·巴凯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000053155754864 Andrew J. Bakke, qualified P1810 subject named as Andrew J. Iverson Bakke
LAST	P2600	"6000000053155754864"	P1810	"Andrew J. Iverson Bakke"
#   P569 date of birth = +1862-04-23T00:00:00Z/11
LAST	P569	+1862-04-23T00:00:00Z/11	S2600	"6000000053155754864"
#   P570 date of death = +1955-02-23T00:00:00Z/11
LAST	P570	+1955-02-23T00:00:00Z/11	S2600	"6000000053155754864"
#   P26 spouse = Q141206058 Bertha Betsy Bakke
LAST	P26	Q141206058	S2600	"6000000053155754864"
#   P40 child = Q141205894 Agnes Tunheim
LAST	P40	Q141205894	S2600	"6000000053155754864"
#   Q141206058 Bertha Betsy Bakke: P26 spouse = the item just created
Q141206058	P26	LAST	S2600	"6000000053155754864"
#   Q141205894 Agnes Tunheim: P22 father = the item just created
Q141205894	P22	LAST	S2600	"6000000053155754864"
#   the item just created: P735 given name = Q18042461 Andrew, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q18042461	P1545	"1"	P7452	Q3409033
#   P735 given name = Q19803507 J., qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q19803507	P1545	"2"	P3831	Q245025
#   P734 family name = Q27887927 Bakke, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q27887927	P3831	Q2507958
#   P734 family name = Q27887927 Bakke
LAST	P734	Q27887927

# create a new item
CREATE
#   set the en label to "Anne Govertsdatter Bratland"
LAST	Len	"Anne Govertsdatter Bratland"
#   set the mul label to "Anne Govertsdatter Bratland"
LAST	Lmul	"Anne Govertsdatter Bratland"
#   add a mul alias "Anne Govertsdatter Årsvoll"
LAST	Amul	"Anne Govertsdatter Årsvoll"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000169074443823 Anne Govertsdtr. Bratland, qualified P1810 subject named as Anne Govertsdtr. Årsvoll
LAST	P2600	"6000000169074443823"	P1810	"Anne Govertsdtr. Årsvoll"
#   P569 date of birth = +1825-02-09T00:00:00Z/11
LAST	P569	+1825-02-09T00:00:00Z/11	S2600	"6000000169074443823"
#   P570 date of death = +1901-10-06T00:00:00Z/11
LAST	P570	+1901-10-06T00:00:00Z/11	S2600	"6000000169074443823"
#   P40 child = Q141205912 Herborg Johannesdatter Sør-Reime
LAST	P40	Q141205912	S2600	"6000000169074443823"
#   Q141205912 Herborg Johannesdatter Sør-Reime: P25 mother = the item just created
Q141205912	P25	LAST	S2600	"6000000169074443823"
#   the item just created: P734 family name = Q27892819 Bratland, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q27892819	P3831	Q28418670
#   add a mul alias "Anne Govertsdtr. Bratland"
LAST	Amul	"Anne Govertsdtr. Bratland"

# create a new item
CREATE
#   set the en label to "Berte Karine Jonsdatter Stokka"
LAST	Len	"Berte Karine Jonsdatter Stokka"
#   set the mul label to "Berte Karine Jonsdatter Stokka"
LAST	Lmul	"Berte Karine Jonsdatter Stokka"
#   add a mul alias "Berte Karine Jonsdatter Heigre"
LAST	Amul	"Berte Karine Jonsdatter Heigre"
#   set the ja label to "ベルテ・カリネ・ヨンスダッテル・ストカ"
LAST	Lja	"ベルテ・カリネ・ヨンスダッテル・ストカ"
#   set the zh label to "贝尔特·卡里内·永斯达特·斯托卡"
LAST	Lzh	"贝尔特·卡里内·永斯达特·斯托卡"
#   add a ja alias "ベルテ・カリネ・ヨンスダッテル・ヘイグレ"
LAST	Aja	"ベルテ・カリネ・ヨンスダッテル・ヘイグレ"
#   add a zh alias "贝尔特·卡里内·永斯达特·海格勒"
LAST	Azh	"贝尔特·卡里内·永斯达特·海格勒"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003491986786 Berte Karine Jonsdatter Stokka, qualified P1810 subject named as Berte Karine Jonsdatter Heigre
LAST	P2600	"6000000003491986786"	P1810	"Berte Karine Jonsdatter Heigre"
#   P569 date of birth = +1839-01-27T00:00:00Z/11
LAST	P569	+1839-01-27T00:00:00Z/11	S2600	"6000000003491986786"
#   P570 date of death = +1869-01-03T00:00:00Z/11
LAST	P570	+1869-01-03T00:00:00Z/11	S2600	"6000000003491986786"
#   P22 father = Q141199892 Jon Olsen Heigre
LAST	P22	Q141199892	S2600	"6000000003491986786"
#   P25 mother = Q141200054 Rakel Jonsdatter Jonsdotter Vatne
LAST	P25	Q141200054	S2600	"6000000003491986786"
#   Q141199892 Jon Olsen Heigre: P40 child = the item just created
Q141199892	P40	LAST	S2600	"6000000003491986786"
#   Q141200054 Rakel Jonsdatter Jonsdotter Vatne: P40 child = the item just created
Q141200054	P40	LAST	S2600	"6000000003491986786"
#   the item just created: P735 given name = Q11960827 Berte, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q11960827	P1545	"1"	P7452	Q3409033
#   P735 given name = Q13365966 Karine, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q13365966	P1545	"2"	P3831	Q245025
#   add a mul alias "Berte Karine Stokka"
LAST	Amul	"Berte Karine Stokka"

# create a new item
CREATE
#   set the en label to "Donald V. Schantzen"
LAST	Len	"Donald V. Schantzen"
#   set the mul label to "Donald V. Schantzen"
LAST	Lmul	"Donald V. Schantzen"
#   set the ja label to "ドナルド・ヴ・シャントゼン"
LAST	Lja	"ドナルド・ヴ・シャントゼン"
#   set the zh label to "多纳尔德·夫·沙恩特泽恩"
LAST	Lzh	"多纳尔德·夫·沙恩特泽恩"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000180011287821 Donald V. Schantzen, qualified P1810 subject named as Donald V. Schantzen
LAST	P2600	"6000000180011287821"	P1810	"Donald V. Schantzen"
#   P569 date of birth = +1927-06-24T00:00:00Z/11
LAST	P569	+1927-06-24T00:00:00Z/11	S2600	"6000000180011287821"
#   P570 date of death = +1984-03-17T00:00:00Z/11
LAST	P570	+1984-03-17T00:00:00Z/11	S2600	"6000000180011287821"
#   P26 spouse = Q141199966 Mildred Lorraine Schantzen
LAST	P26	Q141199966	S2600	"6000000180011287821"
#   Q141199966 Mildred Lorraine Schantzen: P26 spouse = the item just created
Q141199966	P26	LAST	S2600	"6000000180011287821"
#   the item just created: P735 given name = Q13422248 Donald, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q13422248	P1545	"1"	P7452	Q3409033
#   P735 given name = Q19803522 V., qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q19803522	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Gard Toresson Talgje"
LAST	Len	"Gard Toresson Talgje"
#   set the mul label to "Gard Toresson Talgje"
LAST	Lmul	"Gard Toresson Talgje"
#   add a mul alias "Gard Toresson Garaa"
LAST	Amul	"Gard Toresson Garaa"
#   set the ja label to "ガルド・トレソン・タルイェ"
LAST	Lja	"ガルド・トレソン・タルイェ"
#   set the zh label to "加尔德·托雷松·塔尔耶"
LAST	Lzh	"加尔德·托雷松·塔尔耶"
#   add a ja alias "ガルド・トレソン・ガロー"
LAST	Aja	"ガルド・トレソン・ガロー"
#   add a zh alias "加尔德·托雷松·加罗"
LAST	Azh	"加尔德·托雷松·加罗"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000002572728015 Gard Toresson Talgje, qualified P1810 subject named as Gard Toresson Garaa
LAST	P2600	"6000000002572728015"	P1810	"Gard Toresson Garaa"
#   P569 date of birth = +1373-00-00T00:00:00Z/9
LAST	P569	+1373-00-00T00:00:00Z/9	S2600	"6000000002572728015"
#   P570 date of death = +1427-00-00T00:00:00Z/9
LAST	P570	+1427-00-00T00:00:00Z/9	S2600	"6000000002572728015"
#   P40 child = Q141205942 Tore II Gardson Gard
LAST	P40	Q141205942	S2600	"6000000002572728015"
#   Q141205942 Tore II Gardson Gard: P22 father = the item just created
Q141205942	P22	LAST	S2600	"6000000002572728015"
#   the item just created: P735 given name = Q12717105 Gard
LAST	P735	Q12717105
#   P1449 nickname = en:"Toresson"
LAST	P1449	en:"Toresson"
#   add a mul alias "Toresson Talgje"
LAST	Amul	"Toresson Talgje"
#   add a mul alias "Gard Talgje"
LAST	Amul	"Gard Talgje"

# create a new item
CREATE
#   set the en label to "Guri Pedersdatter Foss"
LAST	Len	"Guri Pedersdatter Foss"
#   set the mul label to "Guri Pedersdatter Foss"
LAST	Lmul	"Guri Pedersdatter Foss"
#   set the ja label to "グリ・ペーデシュダッテル・フォス"
LAST	Lja	"グリ・ペーデシュダッテル・フォス"
#   set the zh label to "古里·佩德斯达特·福斯"
LAST	Lzh	"古里·佩德斯达特·福斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000002482084257 Guri Pedersdatter Foss, qualified P1810 subject named as Guri Pedersdatter Foss
LAST	P2600	"6000000002482084257"	P1810	"Guri Pedersdatter Foss"
#   P569 date of birth = +1620-00-00T00:00:00Z/9
LAST	P569	+1620-00-00T00:00:00Z/9	S2600	"6000000002482084257"
#   P570 date of death = +1667-00-00T00:00:00Z/9
LAST	P570	+1667-00-00T00:00:00Z/9	S2600	"6000000002482084257"
#   P22 father = Q141206080 Peder Tormodson Foss
LAST	P22	Q141206080	S2600	"6000000002482084257"
#   P25 mother = Q141206061 Cecilie Olsdatter Håland
LAST	P25	Q141206061	S2600	"6000000002482084257"
#   Q141206080 Peder Tormodson Foss: P40 child = the item just created
Q141206080	P40	LAST	S2600	"6000000002482084257"
#   Q141206061 Cecilie Olsdatter Håland: P40 child = the item just created
Q141206061	P40	LAST	S2600	"6000000002482084257"
#   the item just created: P735 given name = Q11973376 Guri
LAST	P735	Q11973376
#   P734 family name = Q16870001 Foss
LAST	P734	Q16870001
#   P1449 nickname = en:"Guri Pedersdtr.Foss"
LAST	P1449	en:"Guri Pedersdtr.Foss"
#   add a mul alias "Guri Pedersdtr.Foss Foss"
LAST	Amul	"Guri Pedersdtr.Foss Foss"

# create a new item
CREATE
#   set the en label to "Halvard Assersen Grøtheim"
LAST	Len	"Halvard Assersen Grøtheim"
#   set the mul label to "Halvard Assersen Grøtheim"
LAST	Lmul	"Halvard Assersen Grøtheim"
#   set the ja label to "ハルヴァルド・アセルセン・グレートヘイム"
LAST	Lja	"ハルヴァルド・アセルセン・グレートヘイム"
#   set the zh label to "哈尔瓦尔德·阿塞尔森·格勒特海姆"
LAST	Lzh	"哈尔瓦尔德·阿塞尔森·格勒特海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000225229552897 Halvard Assersen Grøtheim, qualified P1810 subject named as Halvard Assersen Grøtheim
LAST	P2600	"6000000225229552897"	P1810	"Halvard Assersen Grøtheim"
#   P569 date of birth = +1663-00-00T00:00:00Z/9
LAST	P569	+1663-00-00T00:00:00Z/9	S2600	"6000000225229552897"
#   P570 date of death = +1739-09-01T00:00:00Z/11
LAST	P570	+1739-09-01T00:00:00Z/11	S2600	"6000000225229552897"
#   P26 spouse = Q141199918 Kirsten Hansdatter Grøtheim
LAST	P26	Q141199918	S2600	"6000000225229552897"
#   Q141199918 Kirsten Hansdatter Grøtheim: P26 spouse = the item just created
Q141199918	P26	LAST	S2600	"6000000225229552897"
#   the item just created: P735 given name = Q18002157 Halvard
LAST	P735	Q18002157
#   add a mul alias "Halvard Grøtheim"
LAST	Amul	"Halvard Grøtheim"

# create a new item
CREATE
#   set the en label to "Hanna Sofie Wendt"
LAST	Len	"Hanna Sofie Wendt"
#   set the mul label to "Hanna Sofie Wendt"
LAST	Lmul	"Hanna Sofie Wendt"
#   add a mul alias "Hanna Sofie Helmer"
LAST	Amul	"Hanna Sofie Helmer"
#   set the ja label to "ハナ・ソフィエ・ヴェント"
LAST	Lja	"ハナ・ソフィエ・ヴェント"
#   set the zh label to "哈纳·索菲埃·温特"
LAST	Lzh	"哈纳·索菲埃·温特"
#   add a ja alias "ハナ・ソフィエ・ヘルメル"
LAST	Aja	"ハナ・ソフィエ・ヘルメル"
#   add a zh alias "哈纳·索菲埃·赫尔梅尔"
LAST	Azh	"哈纳·索菲埃·赫尔梅尔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005441361475 Hanna Sofie Wendt, qualified P1810 subject named as Hanna Sofie Helmer
LAST	P2600	"6000000005441361475"	P1810	"Hanna Sofie Helmer"
#   P569 date of birth = +1865-01-05T00:00:00Z/11
LAST	P569	+1865-01-05T00:00:00Z/11	S2600	"6000000005441361475"
#   P570 date of death = +1951-08-27T00:00:00Z/11
LAST	P570	+1951-08-27T00:00:00Z/11	S2600	"6000000005441361475"
#   P40 child = Q141198396 Erling Juel Wendt
LAST	P40	Q141198396	S2600	"6000000005441361475"
#   Q141198396 Erling Juel Wendt: P25 mother = the item just created
Q141198396	P25	LAST	S2600	"6000000005441361475"
#   the item just created: P735 given name = Q18201530 Sofie, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q18201530	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Hans Halvardsen Grøtheim"
LAST	Len	"Hans Halvardsen Grøtheim"
#   set the mul label to "Hans Halvardsen Grøtheim"
LAST	Lmul	"Hans Halvardsen Grøtheim"
#   set the ja label to "ハンス・ハルヴァルドセン・グレートヘイム"
LAST	Lja	"ハンス・ハルヴァルドセン・グレートヘイム"
#   set the zh label to "汉斯·哈尔瓦尔德森·格勒特海姆"
LAST	Lzh	"汉斯·哈尔瓦尔德森·格勒特海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000224130977838 Hans Halvardsen Grøtheim, qualified P1810 subject named as Hans Halvardsen Grøtheim
LAST	P2600	"6000000224130977838"	P1810	"Hans Halvardsen Grøtheim"
#   P569 date of birth = +1736-00-00T00:00:00Z/9
LAST	P569	+1736-00-00T00:00:00Z/9	S2600	"6000000224130977838"
#   P25 mother = Q141199918 Kirsten Hansdatter Grøtheim
LAST	P25	Q141199918	S2600	"6000000224130977838"
#   Q141199918 Kirsten Hansdatter Grøtheim: P40 child = the item just created
Q141199918	P40	LAST	S2600	"6000000224130977838"

# create a new item
CREATE
#   the item just created: set the en label to "Hans Olsen Grøtheim"
LAST	Len	"Hans Olsen Grøtheim"
#   set the mul label to "Hans Olsen Grøtheim"
LAST	Lmul	"Hans Olsen Grøtheim"
#   set the ja label to "ハンス・オルセン・グレートヘイム"
LAST	Lja	"ハンス・オルセン・グレートヘイム"
#   set the zh label to "汉斯·奥尔森·格勒特海姆"
LAST	Lzh	"汉斯·奥尔森·格勒特海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000008176954243 Hans Olsen Grøtheim, qualified P1810 subject named as Hans Olsen Grøtheim
LAST	P2600	"6000000008176954243"	P1810	"Hans Olsen Grøtheim"
#   P569 date of birth = +1790-02-07T00:00:00Z/11
LAST	P569	+1790-02-07T00:00:00Z/11	S2600	"6000000008176954243"
#   P570 date of death = +1801-00-00T00:00:00Z/9
LAST	P570	+1801-00-00T00:00:00Z/9	S2600	"6000000008176954243"
#   P22 father = Q141189088 Ola Knutsen Grøtheim
LAST	P22	Q141189088	S2600	"6000000008176954243"
#   P25 mother = Q141199830 Anna Rasmusdatter Grøtheim
LAST	P25	Q141199830	S2600	"6000000008176954243"
#   Q141189088 Ola Knutsen Grøtheim: P40 child = the item just created
Q141189088	P40	LAST	S2600	"6000000008176954243"
#   Q141199830 Anna Rasmusdatter Grøtheim: P40 child = the item just created
Q141199830	P40	LAST	S2600	"6000000008176954243"

# create a new item
CREATE
#   the item just created: set the en label to "Hans Rasmussen Låge-Håland"
LAST	Len	"Hans Rasmussen Låge-Håland"
#   set the mul label to "Hans Rasmussen Låge-Håland"
LAST	Lmul	"Hans Rasmussen Låge-Håland"
#   add a mul alias "Hans Rasmussen Tvihaug"
LAST	Amul	"Hans Rasmussen Tvihaug"
#   set the ja label to "ハンス・ラスムセン・ローゲホーランド"
LAST	Lja	"ハンス・ラスムセン・ローゲホーランド"
#   set the zh label to "汉斯·拉斯穆森·洛盖霍拉恩德"
LAST	Lzh	"汉斯·拉斯穆森·洛盖霍拉恩德"
#   add a ja alias "ハンス・ラスムセン・トヴィハウグ"
LAST	Aja	"ハンス・ラスムセン・トヴィハウグ"
#   add a zh alias "汉斯·拉斯穆森·特维哈乌格"
LAST	Azh	"汉斯·拉斯穆森·特维哈乌格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000009127934231 Hans Rasmussen Låge-Håland, qualified P1810 subject named as Hans Rasmussen Tvihaug
LAST	P2600	"6000000009127934231"	P1810	"Hans Rasmussen Tvihaug"
#   P569 date of birth = +1656-00-00T00:00:00Z/9
LAST	P569	+1656-00-00T00:00:00Z/9	S2600	"6000000009127934231"
#   P570 date of death = +1712-00-00T00:00:00Z/9
LAST	P570	+1712-00-00T00:00:00Z/9	S2600	"6000000009127934231"
#   P40 child = Q141199918 Kirsten Hansdatter Grøtheim
LAST	P40	Q141199918	S2600	"6000000009127934231"
#   Q141199918 Kirsten Hansdatter Grøtheim: P22 father = the item just created
Q141199918	P22	LAST	S2600	"6000000009127934231"
#   the item just created: add a mul alias "Hans Låge-Håland"
LAST	Amul	"Hans Låge-Håland"

# create a new item
CREATE
#   set the en label to "Helge Asbjørnsen Bø"
LAST	Len	"Helge Asbjørnsen Bø"
#   set the mul label to "Helge Asbjørnsen Bø"
LAST	Lmul	"Helge Asbjørnsen Bø"
#   set the ja label to "ヘルゲ・アスブヨルンセン・ベー"
LAST	Lja	"ヘルゲ・アスブヨルンセン・ベー"
#   set the zh label to "赫尔盖·阿斯布永尔恩森·贝"
LAST	Lzh	"赫尔盖·阿斯布永尔恩森·贝"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000008309908854 Helge Asbjørnsen Bø, qualified P1810 subject named as Helge Asbjørnsen Bø
LAST	P2600	"6000000008309908854"	P1810	"Helge Asbjørnsen Bø"
#   P569 date of birth = +1755-00-00T00:00:00Z/9
LAST	P569	+1755-00-00T00:00:00Z/9	S2600	"6000000008309908854"
#   P570 date of death = +1823-06-07T00:00:00Z/11
LAST	P570	+1823-06-07T00:00:00Z/11	S2600	"6000000008309908854"
#   P26 spouse = Q141205919 Malena Hansdatter Bø
LAST	P26	Q141205919	S2600	"6000000008309908854"
#   P40 child = Q141199809 Ane Marie Helgesdatter Bø
LAST	P40	Q141199809	S2600	"6000000008309908854"
#   P40 child = Q141206056 Asbjørn Helgesen Bø
LAST	P40	Q141206056	S2600	"6000000008309908854"
#   Q141205919 Malena Hansdatter Bø: P26 spouse = the item just created
Q141205919	P26	LAST	S2600	"6000000008309908854"
#   Q141199809 Ane Marie Helgesdatter Bø: P22 father = the item just created
Q141199809	P22	LAST	S2600	"6000000008309908854"
#   Q141206056 Asbjørn Helgesen Bø: P22 father = the item just created
Q141206056	P22	LAST	S2600	"6000000008309908854"
#   the item just created: P735 given name = Q1602361 Helge
LAST	P735	Q1602361

# create a new item
CREATE
#   set the en label to "Ingeborg Eriksdatter Bjorland"
LAST	Len	"Ingeborg Eriksdatter Bjorland"
#   set the mul label to "Ingeborg Eriksdatter Bjorland"
LAST	Lmul	"Ingeborg Eriksdatter Bjorland"
#   set the ja label to "インゲボルグ・エリクスダッテル・ブヨルランド"
LAST	Lja	"インゲボルグ・エリクスダッテル・ブヨルランド"
#   set the zh label to "英厄堡·埃里克斯达特·布永尔拉恩德"
LAST	Lzh	"英厄堡·埃里克斯达特·布永尔拉恩德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000014100949863 Ingeborg Eriksdatter Bjorland, qualified P1810 subject named as Ingeborg Eriksdatter Bjorland
LAST	P2600	"6000000014100949863"	P1810	"Ingeborg Eriksdatter Bjorland"
#   P569 date of birth = +1680-00-00T00:00:00Z/9
LAST	P569	+1680-00-00T00:00:00Z/9	S2600	"6000000014100949863"
#   P570 date of death = +1751-10-11T00:00:00Z/11
LAST	P570	+1751-10-11T00:00:00Z/11	S2600	"6000000014100949863"
#   P40 child = Q141199918 Kirsten Hansdatter Grøtheim
LAST	P40	Q141199918	S2600	"6000000014100949863"
#   Q141199918 Kirsten Hansdatter Grøtheim: P25 mother = the item just created
Q141199918	P25	LAST	S2600	"6000000014100949863"
#   the item just created: P735 given name = Q656590 Ingeborg
LAST	P735	Q656590

# create a new item
CREATE
#   set the en label to "Ingeborg Eriksdatter Time"
LAST	Len	"Ingeborg Eriksdatter Time"
#   set the mul label to "Ingeborg Eriksdatter Time"
LAST	Lmul	"Ingeborg Eriksdatter Time"
#   add a mul alias "Ingeborg Eriksdatter Netland"
LAST	Amul	"Ingeborg Eriksdatter Netland"
#   set the ja label to "インゲボルグ・エリクスダッテル・ティメ"
LAST	Lja	"インゲボルグ・エリクスダッテル・ティメ"
#   set the zh label to "英厄堡·埃里克斯达特·蒂梅"
LAST	Lzh	"英厄堡·埃里克斯达特·蒂梅"
#   add a ja alias "インゲボルグ・エリクスダッテル・ネトランド"
LAST	Aja	"インゲボルグ・エリクスダッテル・ネトランド"
#   add a zh alias "英厄堡·埃里克斯达特·内特拉恩德"
LAST	Azh	"英厄堡·埃里克斯达特·内特拉恩德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005607411844 Ingeborg Eriksdatter Time, qualified P1810 subject named as Ingeborg Eriksdatter Netland
LAST	P2600	"6000000005607411844"	P1810	"Ingeborg Eriksdatter Netland"
#   P569 date of birth = +1765-00-00T00:00:00Z/9
LAST	P569	+1765-00-00T00:00:00Z/9	S2600	"6000000005607411844"
#   P26 spouse = Q141205904 Erik Tollefson Foss-Eikeland
LAST	P26	Q141205904	S2600	"6000000005607411844"
#   P40 child = Q141198393 Erik Erikson Stangeland
LAST	P40	Q141198393	S2600	"6000000005607411844"
#   Q141205904 Erik Tollefson Foss-Eikeland: P26 spouse = the item just created
Q141205904	P26	LAST	S2600	"6000000005607411844"
#   Q141198393 Erik Erikson Stangeland: P25 mother = the item just created
Q141198393	P25	LAST	S2600	"6000000005607411844"
#   the item just created: P735 given name = Q656590 Ingeborg
LAST	P735	Q656590
#   add a mul alias "Ingeborg Time"
LAST	Amul	"Ingeborg Time"

# create a new item
CREATE
#   set the en label to "Jens Wilhelm Wendt"
LAST	Len	"Jens Wilhelm Wendt"
#   set the mul label to "Jens Wilhelm Wendt"
LAST	Lmul	"Jens Wilhelm Wendt"
#   set the ja label to "イェンス・ヴィルヘルム・ヴェント"
LAST	Lja	"イェンス・ヴィルヘルム・ヴェント"
#   set the zh label to "耶恩斯·维尔赫尔姆·温特"
LAST	Lzh	"耶恩斯·维尔赫尔姆·温特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000021079642735 Jens Wilhelm Wendt, qualified P1810 subject named as Jens Wilhelm Wendt
LAST	P2600	"6000000021079642735"	P1810	"Jens Wilhelm Wendt"
#   P569 date of birth = +1861-12-29T00:00:00Z/11
LAST	P569	+1861-12-29T00:00:00Z/11	S2600	"6000000021079642735"
#   P570 date of death = +1922-05-12T00:00:00Z/11
LAST	P570	+1922-05-12T00:00:00Z/11	S2600	"6000000021079642735"
#   P40 child = Q141198396 Erling Juel Wendt
LAST	P40	Q141198396	S2600	"6000000021079642735"
#   Q141198396 Erling Juel Wendt: P22 father = the item just created
Q141198396	P22	LAST	S2600	"6000000021079642735"
#   the item just created: P735 given name = Q2246251 Jens, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q2246251	P1545	"1"	P7452	Q3409033

# create a new item
CREATE
#   set the en label to "Johannes Svensen Obrestad"
LAST	Len	"Johannes Svensen Obrestad"
#   set the mul label to "Johannes Svensen Obrestad"
LAST	Lmul	"Johannes Svensen Obrestad"
#   add a mul alias "Johannes Svensen Bratland"
LAST	Amul	"Johannes Svensen Bratland"
#   set the ja label to "ヨハンネス・スヴェンセン・オブレスタド"
LAST	Lja	"ヨハンネス・スヴェンセン・オブレスタド"
#   set the zh label to "约翰内斯·斯韦恩森·奥布雷斯塔德"
LAST	Lzh	"约翰内斯·斯韦恩森·奥布雷斯塔德"
#   add a ja alias "ヨハンネス・スヴェンセン・ブラトランド"
LAST	Aja	"ヨハンネス・スヴェンセン・ブラトランド"
#   add a zh alias "约翰内斯·斯韦恩森·布拉特拉恩德"
LAST	Azh	"约翰内斯·斯韦恩森·布拉特拉恩德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003491978246 Johannes Svensen Obrestad, qualified P1810 subject named as Johannes Svensen Bratland
LAST	P2600	"6000000003491978246"	P1810	"Johannes Svensen Bratland"
#   P569 date of birth = +1798-09-09T00:00:00Z/11
LAST	P569	+1798-09-09T00:00:00Z/11	S2600	"6000000003491978246"
#   P570 date of death = +1876-08-27T00:00:00Z/11
LAST	P570	+1876-08-27T00:00:00Z/11	S2600	"6000000003491978246"
#   P40 child = Q141205912 Herborg Johannesdatter Sør-Reime
LAST	P40	Q141205912	S2600	"6000000003491978246"
#   Q141205912 Herborg Johannesdatter Sør-Reime: P22 father = the item just created
Q141205912	P22	LAST	S2600	"6000000003491978246"
#   the item just created: P735 given name = Q2117521 Johannes
LAST	P735	Q2117521
#   P734 family name = Q27892819 Bratland, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q27892819	P3831	Q2507958
#   add a mul alias "Johannes Obrestad"
LAST	Amul	"Johannes Obrestad"

# create a new item
CREATE
#   set the en label to "Jon Hansson St. Vatne"
LAST	Len	"Jon Hansson St. Vatne"
#   set the mul label to "Jon Hansson St. Vatne"
LAST	Lmul	"Jon Hansson St. Vatne"
#   set the ja label to "ヨン・ハンソン・スト・ヴァトネ"
LAST	Lja	"ヨン・ハンソン・スト・ヴァトネ"
#   set the zh label to "永·哈恩松·斯特·瓦特内"
LAST	Lzh	"永·哈恩松·斯特·瓦特内"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005608892743 Jon Hansson St. Vatne, qualified P1810 subject named as Jon Hansson St. Vatne
LAST	P2600	"6000000005608892743"	P1810	"Jon Hansson St. Vatne"
#   P569 date of birth = +1773-00-00T00:00:00Z/9
LAST	P569	+1773-00-00T00:00:00Z/9	S2600	"6000000005608892743"
#   P570 date of death = +1828-00-00T00:00:00Z/9
LAST	P570	+1828-00-00T00:00:00Z/9	S2600	"6000000005608892743"
#   P26 spouse = Q141206057 Berte Tørresdotter Austrått
LAST	P26	Q141206057	S2600	"6000000005608892743"
#   P40 child = Q141200054 Rakel Jonsdatter Jonsdotter Vatne
LAST	P40	Q141200054	S2600	"6000000005608892743"
#   P40 child = Q141205921 Maria Jonsdatter Lura
LAST	P40	Q141205921	S2600	"6000000005608892743"
#   Q141206057 Berte Tørresdotter Austrått: P26 spouse = the item just created
Q141206057	P26	LAST	S2600	"6000000005608892743"
#   Q141200054 Rakel Jonsdatter Jonsdotter Vatne: P22 father = the item just created
Q141200054	P22	LAST	S2600	"6000000005608892743"
#   Q141205921 Maria Jonsdatter Lura: P22 father = the item just created
Q141205921	P22	LAST	S2600	"6000000005608892743"
#   the item just created: P735 given name = Q13501137 Jon
LAST	P735	Q13501137
#   P734 family name = Q30134985 Vatne
LAST	P734	Q30134985
#   add a mul alias "Jon St. Vatne"
LAST	Amul	"Jon St. Vatne"

# create a new item
CREATE
#   set the en label to "Jon Jonsson"
LAST	Len	"Jon Jonsson"
#   set the mul label to "Jon Jonsson"
LAST	Lmul	"Jon Jonsson"
#   set the ja label to "ヨン・ヨンソン"
LAST	Lja	"ヨン・ヨンソン"
#   set the zh label to "永·永松"
LAST	Lzh	"永·永松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000013354249769 Jon Jonsson, qualified P1810 subject named as Jon Jonsson
LAST	P2600	"6000000013354249769"	P1810	"Jon Jonsson"
#   P569 date of birth = +1580-00-00T00:00:00Z/9
LAST	P569	+1580-00-00T00:00:00Z/9	S2600	"6000000013354249769"
#   P570 date of death = +1636-00-00T00:00:00Z/9
LAST	P570	+1636-00-00T00:00:00Z/9	S2600	"6000000013354249769"
#   P40 child = Q141205928 NN Jonsdotter
LAST	P40	Q141205928	S2600	"6000000013354249769"
#   Q141205928 NN Jonsdotter: P22 father = the item just created
Q141205928	P22	LAST	S2600	"6000000013354249769"
#   the item just created: P735 given name = Q13501137 Jon
LAST	P735	Q13501137
#   P734 family name = Q21509276 Jonsson
LAST	P734	Q21509276

# create a new item
CREATE
#   set the en label to "Kirsten Gabrielsdatter Austråt"
LAST	Len	"Kirsten Gabrielsdatter Austråt"
#   set the mul label to "Kirsten Gabrielsdatter Austråt"
LAST	Lmul	"Kirsten Gabrielsdatter Austråt"
#   set the ja label to "シシュテン・ガブリエルスダッテル・アウストロート"
LAST	Lja	"シシュテン・ガブリエルスダッテル・アウストロート"
#   set the zh label to "谢什滕·加布里埃尔斯达特·奥斯特罗特"
LAST	Lzh	"谢什滕·加布里埃尔斯达特·奥斯特罗特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003491988841 Kirsten Gabrielsdatter Austråt, qualified P1810 subject named as Kirsten Gabrielsdatter Austråt
LAST	P2600	"6000000003491988841"	P1810	"Kirsten Gabrielsdatter Austråt"
#   P569 date of birth = +1712-03-05T00:00:00Z/11
LAST	P569	+1712-03-05T00:00:00Z/11	S2600	"6000000003491988841"
#   P570 date of death = +1778-03-08T00:00:00Z/11
LAST	P570	+1778-03-08T00:00:00Z/11	S2600	"6000000003491988841"
#   P26 spouse = Q141206082 Jon Olson Raustad
LAST	P26	Q141206082	S2600	"6000000003491988841"
#   P40 child = Q141178380 Samuel Jonson Raustad
LAST	P40	Q141178380	S2600	"6000000003491988841"
#   Q141206082 Jon Olson Raustad: P26 spouse = the item just created
Q141206082	P26	LAST	S2600	"6000000003491988841"
#   Q141178380 Samuel Jonson Raustad: P25 mother = the item just created
Q141178380	P25	LAST	S2600	"6000000003491988841"
#   the item just created: P735 given name = Q256744 Kirsten
LAST	P735	Q256744

# create a new item
CREATE
#   set the en label to "Kristian Monsen Stangeland"
LAST	Len	"Kristian Monsen Stangeland"
#   set the mul label to "Kristian Monsen Stangeland"
LAST	Lmul	"Kristian Monsen Stangeland"
#   set the ja label to "クリスティアン・モンセン・スタンゲラン"
LAST	Lja	"クリスティアン・モンセン・スタンゲラン"
#   set the zh label to "克里斯蒂安·莫恩森·斯坦格兰"
LAST	Lzh	"克里斯蒂安·莫恩森·斯坦格兰"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000018935761194 Kristian Monsen Stangeland, qualified P1810 subject named as Kristian Monsen Stangeland
LAST	P2600	"6000000018935761194"	P1810	"Kristian Monsen Stangeland"
#   P569 date of birth = +1846-10-06T00:00:00Z/11
LAST	P569	+1846-10-06T00:00:00Z/11	S2600	"6000000018935761194"
#   P570 date of death = +1921-08-21T00:00:00Z/11
LAST	P570	+1921-08-21T00:00:00Z/11	S2600	"6000000018935761194"
#   P40 child = Q141205896 Ane Marie Konstanse Amanda Kristine Hegre
LAST	P40	Q141205896	S2600	"6000000018935761194"
#   Q141205896 Ane Marie Konstanse Amanda Kristine Hegre: P22 father = the item just created
Q141205896	P22	LAST	S2600	"6000000018935761194"
#   the item just created: P735 given name = Q12794332 Kristian
LAST	P735	Q12794332
#   P734 family name = Q21452049 Stangeland
LAST	P734	Q21452049

# create a new item
CREATE
#   set the en label to "Lisbet Olavsdatter Håland"
LAST	Len	"Lisbet Olavsdatter Håland"
#   set the mul label to "Lisbet Olavsdatter Håland"
LAST	Lmul	"Lisbet Olavsdatter Håland"
#   add a mul alias "Lisbet Olavsdatter Olavsdatter"
LAST	Amul	"Lisbet Olavsdatter Olavsdatter"
#   set the ja label to "リスベト・オラヴスダッテル・ホーランド"
LAST	Lja	"リスベト・オラヴスダッテル・ホーランド"
#   set the zh label to "利斯贝特·奥拉夫斯达特·霍兰"
LAST	Lzh	"利斯贝特·奥拉夫斯达特·霍兰"
#   add a ja alias "リスベト・オラヴスダッテル・オラヴスダッテル"
LAST	Aja	"リスベト・オラヴスダッテル・オラヴスダッテル"
#   add a zh alias "利斯贝特·奥拉夫斯达特·奥拉夫斯达特"
LAST	Azh	"利斯贝特·奥拉夫斯达特·奥拉夫斯达特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005607268895 Lisbet Olavsdatter Håland, qualified P1810 subject named as Lisbet Olavsdatter Olavsdatter
LAST	P2600	"6000000005607268895"	P1810	"Lisbet Olavsdatter Olavsdatter"
#   P569 date of birth = +1560-00-00T00:00:00Z/9
LAST	P569	+1560-00-00T00:00:00Z/9	S2600	"6000000005607268895"
#   P570 date of death = +1620-00-00T00:00:00Z/9
LAST	P570	+1620-00-00T00:00:00Z/9	S2600	"6000000005607268895"
#   P22 father = Q141205930 Olav Knutson Randa Håland
LAST	P22	Q141205930	S2600	"6000000005607268895"
#   Q141205930 Olav Knutson Randa Håland: P40 child = the item just created
Q141205930	P40	LAST	S2600	"6000000005607268895"
#   the item just created: P735 given name = Q19869334 Lisbet
LAST	P735	Q19869334
#   add a mul alias "Lisbet Håland"
LAST	Amul	"Lisbet Håland"

# create a new item
CREATE
#   set the en label to "Malin Andersdotter"
LAST	Len	"Malin Andersdotter"
#   set the mul label to "Malin Andersdotter"
LAST	Lmul	"Malin Andersdotter"
#   set the ja label to "マリン・アンデシュドッテル"
LAST	Lja	"マリン・アンデシュドッテル"
#   set the zh label to "马利恩·安德斯多特"
LAST	Lzh	"马利恩·安德斯多特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000000305413766 Malin Andersdotter, qualified P1810 subject named as Malin Andersdotter
LAST	P2600	"6000000000305413766"	P1810	"Malin Andersdotter"
#   P569 date of birth = +1481-00-00T00:00:00Z/9
LAST	P569	+1481-00-00T00:00:00Z/9	S2600	"6000000000305413766"
#   P570 date of death = +1552-00-00T00:00:00Z/9
LAST	P570	+1552-00-00T00:00:00Z/9	S2600	"6000000000305413766"
#   P40 child = Q141199819 Anna Andersdotter
LAST	P40	Q141199819	S2600	"6000000000305413766"
#   Q141199819 Anna Andersdotter: P25 mother = the item just created
Q141199819	P25	LAST	S2600	"6000000000305413766"
#   the item just created: P735 given name = Q18369928 Malin
LAST	P735	Q18369928
#   P1449 nickname = en:"Malin"
LAST	P1449	en:"Malin"

# create a new item
CREATE
#   set the en label to "Malin Olofsdotter"
LAST	Len	"Malin Olofsdotter"
#   set the mul label to "Malin Olofsdotter"
LAST	Lmul	"Malin Olofsdotter"
#   set the ja label to "マリン・オロフスドッテル"
LAST	Lja	"マリン・オロフスドッテル"
#   set the zh label to "马利恩·奥洛夫斯多特"
LAST	Lzh	"马利恩·奥洛夫斯多特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 4982890984490082253 Malin Olofsdotter, qualified P1810 subject named as Malin Olofsdotter
LAST	P2600	"4982890984490082253"	P1810	"Malin Olofsdotter"
#   P569 date of birth = +1533-00-00T00:00:00Z/9
LAST	P569	+1533-00-00T00:00:00Z/9	S2600	"4982890984490082253"
#   P570 date of death = +1627-00-00T00:00:00Z/9
LAST	P570	+1627-00-00T00:00:00Z/9	S2600	"4982890984490082253"
#   P40 child = Q141205931 Olof Olofsson
LAST	P40	Q141205931	S2600	"4982890984490082253"
#   Q141205931 Olof Olofsson: P25 mother = the item just created
Q141205931	P25	LAST	S2600	"4982890984490082253"
#   the item just created: P735 given name = Q18369928 Malin
LAST	P735	Q18369928

# create a new item
CREATE
#   set the en label to "Margareta Nilsdotter"
LAST	Len	"Margareta Nilsdotter"
#   set the mul label to "Margareta Nilsdotter"
LAST	Lmul	"Margareta Nilsdotter"
#   set the ja label to "マルガレータ・ニルスドッテル"
LAST	Lja	"マルガレータ・ニルスドッテル"
#   set the zh label to "玛格丽塔·尼尔斯多特"
LAST	Lzh	"玛格丽塔·尼尔斯多特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000017799612472 Margareta Nilsdotter, qualified P1810 subject named as Margareta Nilsdotter
LAST	P2600	"6000000017799612472"	P1810	"Margareta Nilsdotter"
#   P569 date of birth = +1585-00-00T00:00:00Z/9
LAST	P569	+1585-00-00T00:00:00Z/9	S2600	"6000000017799612472"
#   P40 child = Q141205928 NN Jonsdotter
LAST	P40	Q141205928	S2600	"6000000017799612472"
#   Q141205928 NN Jonsdotter: P25 mother = the item just created
Q141205928	P25	LAST	S2600	"6000000017799612472"
#   the item just created: P735 given name = Q8274988 Margareta
LAST	P735	Q8274988

# create a new item
CREATE
#   set the en label to "Margreta Lauritsdatter Øvre Bjørheim"
LAST	Len	"Margreta Lauritsdatter Øvre Bjørheim"
#   set the mul label to "Margreta Lauritsdatter Øvre Bjørheim"
LAST	Lmul	"Margreta Lauritsdatter Øvre Bjørheim"
#   add a mul alias "Margreta Lauritsdatter Leivsen Øvre Bjørheim"
LAST	Amul	"Margreta Lauritsdatter Leivsen Øvre Bjørheim"
#   set the ja label to "マルグレタ・ラウリトスダッテル・オヴレ・ブヨルヘイム"
LAST	Lja	"マルグレタ・ラウリトスダッテル・オヴレ・ブヨルヘイム"
#   set the zh label to "马尔格雷塔·拉乌里特斯达特·奥夫雷·布永尔赫伊姆"
LAST	Lzh	"马尔格雷塔·拉乌里特斯达特·奥夫雷·布永尔赫伊姆"
#   add a ja alias "マルグレタ・ラウリトスダッテル・レイヴセン・オヴレ・ブヨルヘイム"
LAST	Aja	"マルグレタ・ラウリトスダッテル・レイヴセン・オヴレ・ブヨルヘイム"
#   add a zh alias "马尔格雷塔·拉乌里特斯达特·莱伊夫森·奥夫雷·布永尔赫伊姆"
LAST	Azh	"马尔格雷塔·拉乌里特斯达特·莱伊夫森·奥夫雷·布永尔赫伊姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000016246443406 Margreta Lauritsdatter Øvre Bjørheim, qualified P1810 subject named as Margreta Lauritsdatter Leivsen Øvre Bjørheim
LAST	P2600	"6000000016246443406"	P1810	"Margreta Lauritsdatter Leivsen Øvre Bjørheim"
#   P569 date of birth = +1540-00-00T00:00:00Z/9
LAST	P569	+1540-00-00T00:00:00Z/9	S2600	"6000000016246443406"
#   P570 date of death = +1578-00-00T00:00:00Z/9
LAST	P570	+1578-00-00T00:00:00Z/9	S2600	"6000000016246443406"
#   P26 spouse = Q141205930 Olav Knutson Randa Håland
LAST	P26	Q141205930	S2600	"6000000016246443406"
#   Q141205930 Olav Knutson Randa Håland: P26 spouse = the item just created
Q141205930	P26	LAST	S2600	"6000000016246443406"
#   the item just created: P735 given name = Q21143359 Margreta
LAST	P735	Q21143359
#   add a mul alias "Margreta Øvre Bjørheim"
LAST	Amul	"Margreta Øvre Bjørheim"

# create a new item
CREATE
#   set the en label to "Mariet Danielsdotter"
LAST	Len	"Mariet Danielsdotter"
#   set the mul label to "Mariet Danielsdotter"
LAST	Lmul	"Mariet Danielsdotter"
#   set the ja label to "マリエト・ダニエルスドッテル"
LAST	Lja	"マリエト・ダニエルスドッテル"
#   set the zh label to "马里埃特·达尼埃尔斯多特"
LAST	Lzh	"马里埃特·达尼埃尔斯多特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000017535961052 Mariet Danielsdotter, qualified P1810 subject named as Mariet Danielsdotter
LAST	P2600	"6000000017535961052"	P1810	"Mariet Danielsdotter"
#   P569 date of birth = +1640-00-00T00:00:00Z/9
LAST	P569	+1640-00-00T00:00:00Z/9	S2600	"6000000017535961052"
#   P570 date of death = +1684-00-00T00:00:00Z/9
LAST	P570	+1684-00-00T00:00:00Z/9	S2600	"6000000017535961052"
#   P22 father = Q141205902 Daniel Olofsson
LAST	P22	Q141205902	S2600	"6000000017535961052"
#   P25 mother = Q141205928 NN Jonsdotter
LAST	P25	Q141205928	S2600	"6000000017535961052"
#   Q141205902 Daniel Olofsson: P40 child = the item just created
Q141205902	P40	LAST	S2600	"6000000017535961052"
#   Q141205928 NN Jonsdotter: P40 child = the item just created
Q141205928	P40	LAST	S2600	"6000000017535961052"

# create a new item
CREATE
#   the item just created: set the en label to "Olof Nilsson"
LAST	Len	"Olof Nilsson"
#   set the mul label to "Olof Nilsson"
LAST	Lmul	"Olof Nilsson"
#   set the ja label to "オロフ・ニルソン"
LAST	Lja	"オロフ・ニルソン"
#   set the zh label to "奥洛夫·尼尔松"
LAST	Lzh	"奥洛夫·尼尔松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 375729629520007230 Olof Nilsson, qualified P1810 subject named as Olof Nilsson
LAST	P2600	"375729629520007230"	P1810	"Olof Nilsson"
#   P569 date of birth = +1539-00-00T00:00:00Z/9
LAST	P569	+1539-00-00T00:00:00Z/9	S2600	"375729629520007230"
#   P570 date of death = +1627-00-00T00:00:00Z/9
LAST	P570	+1627-00-00T00:00:00Z/9	S2600	"375729629520007230"
#   P40 child = Q141205931 Olof Olofsson
LAST	P40	Q141205931	S2600	"375729629520007230"
#   Q141205931 Olof Olofsson: P22 father = the item just created
Q141205931	P22	LAST	S2600	"375729629520007230"
#   the item just created: P735 given name = Q18089653 Olof
LAST	P735	Q18089653
#   P5056 patronym or matronym = Q130233015 Nilsson
LAST	P5056	Q130233015

# create a new item
CREATE
#   set the mul label to "NN"
LAST	Lmul	"NN"
#   set the ca label to "fill de Sigurd Sverre Ravn Talle"
LAST	Lca	"fill de Sigurd Sverre Ravn Talle"
#   set the da label to "søn af Sigurd Sverre Ravn Talle"
LAST	Lda	"søn af Sigurd Sverre Ravn Talle"
#   set the de label to "Sohn von Sigurd Sverre Ravn Talle"
LAST	Lde	"Sohn von Sigurd Sverre Ravn Talle"
#   set the en label to "son of Sigurd Sverre Ravn Talle"
LAST	Len	"son of Sigurd Sverre Ravn Talle"
#   set the es label to "hijo de Sigurd Sverre Ravn Talle"
LAST	Les	"hijo de Sigurd Sverre Ravn Talle"
#   set the it label to "figlio di Sigurd Sverre Ravn Talle"
LAST	Lit	"figlio di Sigurd Sverre Ravn Talle"
#   set the ja label to "シグルド・スヴェレ・ラヴン・タッレの息子"
LAST	Lja	"シグルド・スヴェレ・ラヴン・タッレの息子"
#   set the nb label to "sønn av Sigurd Sverre Ravn Talle"
LAST	Lnb	"sønn av Sigurd Sverre Ravn Talle"
#   set the nl label to "zoon van Sigurd Sverre Ravn Talle"
LAST	Lnl	"zoon van Sigurd Sverre Ravn Talle"
#   set the pt label to "filho de Sigurd Sverre Ravn Talle"
LAST	Lpt	"filho de Sigurd Sverre Ravn Talle"
#   set the sv label to "son till Sigurd Sverre Ravn Talle"
LAST	Lsv	"son till Sigurd Sverre Ravn Talle"
#   set the zh label to "西古尔德·斯韦雷·拉夫恩·塔勒之子"
LAST	Lzh	"西古尔德·斯韦雷·拉夫恩·塔勒之子"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000177688399821 NN Private, qualified P1810 subject named as Private
LAST	P2600	"6000000177688399821"	P1810	"Private"
#   P25 mother = Q141168830 Ingeborg Talle
LAST	P25	Q141168830	S2600	"6000000177688399821"
#   Q141168830 Ingeborg Talle: P40 child = the item just created
Q141168830	P40	LAST	S2600	"6000000177688399821"

# create a new item
CREATE
#   the item just created: set the en label to "Sigurd Sverre Ravn Talle"
LAST	Len	"Sigurd Sverre Ravn Talle"
#   set the mul label to "Sigurd Sverre Ravn Talle"
LAST	Lmul	"Sigurd Sverre Ravn Talle"
#   set the ja label to "シグルド・スヴェレ・ラヴン・タッレ"
LAST	Lja	"シグルド・スヴェレ・ラヴン・タッレ"
#   set the zh label to "西古尔德·斯韦雷·拉夫恩·塔勒"
LAST	Lzh	"西古尔德·斯韦雷·拉夫恩·塔勒"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000107274277935 Sigurd Sverre Ravn Talle, qualified P1810 subject named as Sigurd Sverre Ravn Talle
LAST	P2600	"6000000107274277935"	P1810	"Sigurd Sverre Ravn Talle"
#   P569 date of birth = +1891-05-25T00:00:00Z/11
LAST	P569	+1891-05-25T00:00:00Z/11	S2600	"6000000107274277935"
#   P570 date of death = +1964-07-28T00:00:00Z/11
LAST	P570	+1964-07-28T00:00:00Z/11	S2600	"6000000107274277935"
#   P26 spouse = Q141168830 Ingeborg Talle
LAST	P26	Q141168830	S2600	"6000000107274277935"
#   Q141168830 Ingeborg Talle: P26 spouse = the item just created
Q141168830	P26	LAST	S2600	"6000000107274277935"
#   the item just created: P735 given name = Q1315397 Sigurd, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q1315397	P1545	"1"	P7452	Q3409033
#   P735 given name = Q970810 Sverre, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q970810	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Tabite Tollefsdotter Tunheim"
LAST	Len	"Tabite Tollefsdotter Tunheim"
#   set the mul label to "Tabite Tollefsdotter Tunheim"
LAST	Lmul	"Tabite Tollefsdotter Tunheim"
#   set the ja label to "タビテ・トレフスドッテル・トゥンヘイム"
LAST	Lja	"タビテ・トレフスドッテル・トゥンヘイム"
#   set the zh label to "塔比特·托莱夫斯多特·通海姆"
LAST	Lzh	"塔比特·托莱夫斯多特·通海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000037735915741 Tabite Tollefsdotter Tunheim, qualified P1810 subject named as Tabite Tollefsdotter Tunheim
LAST	P2600	"6000000037735915741"	P1810	"Tabite Tollefsdotter Tunheim"
#   P569 date of birth = +1855-00-00T00:00:00Z/9
LAST	P569	+1855-00-00T00:00:00Z/9	S2600	"6000000037735915741"
#   P570 date of death = +1855-00-00T00:00:00Z/9
LAST	P570	+1855-00-00T00:00:00Z/9	S2600	"6000000037735915741"
#   P22 father = Q141200112 Tollef Pederson Tunheim
LAST	P22	Q141200112	S2600	"6000000037735915741"
#   P25 mother = Q141199826 Anna Maria Samuelsdtr. Tunheim
LAST	P25	Q141199826	S2600	"6000000037735915741"
#   Q141200112 Tollef Pederson Tunheim: P40 child = the item just created
Q141200112	P40	LAST	S2600	"6000000037735915741"
#   Q141199826 Anna Maria Samuelsdtr. Tunheim: P40 child = the item just created
Q141199826	P40	LAST	S2600	"6000000037735915741"
#   the item just created: add a mul alias "Tabite Tunheim"
LAST	Amul	"Tabite Tunheim"

# create a new item
CREATE
#   set the en label to "Tabitha Tollefsdatter Johnson"
LAST	Len	"Tabitha Tollefsdatter Johnson"
#   set the mul label to "Tabitha Tollefsdatter Johnson"
LAST	Lmul	"Tabitha Tollefsdatter Johnson"
#   add a mul alias "Tabitha Tollefsdatter Tunheim"
LAST	Amul	"Tabitha Tollefsdatter Tunheim"
#   set the ja label to "タビタ・トレフスダッテル・ヨンソン"
LAST	Lja	"タビタ・トレフスダッテル・ヨンソン"
#   set the zh label to "塔比塔·托莱夫斯达特·永恩松"
LAST	Lzh	"塔比塔·托莱夫斯达特·永恩松"
#   add a ja alias "タビタ・トレフスダッテル・トゥンヘイム"
LAST	Aja	"タビタ・トレフスダッテル・トゥンヘイム"
#   add a zh alias "塔比塔·托莱夫斯达特·通海姆"
LAST	Azh	"塔比塔·托莱夫斯达特·通海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000008262061116 Tabitha Tollefsdatter Johnson, qualified P1810 subject named as Tabitha Tollefsdatter Tunheim
LAST	P2600	"6000000008262061116"	P1810	"Tabitha Tollefsdatter Tunheim"
#   P569 date of birth = +1856-05-17T00:00:00Z/11
LAST	P569	+1856-05-17T00:00:00Z/11	S2600	"6000000008262061116"
#   P570 date of death = +1917-04-15T00:00:00Z/11
LAST	P570	+1917-04-15T00:00:00Z/11	S2600	"6000000008262061116"
#   P22 father = Q141200112 Tollef Pederson Tunheim
LAST	P22	Q141200112	S2600	"6000000008262061116"
#   P25 mother = Q141199826 Anna Maria Samuelsdtr. Tunheim
LAST	P25	Q141199826	S2600	"6000000008262061116"
#   Q141200112 Tollef Pederson Tunheim: P40 child = the item just created
Q141200112	P40	LAST	S2600	"6000000008262061116"
#   Q141199826 Anna Maria Samuelsdtr. Tunheim: P40 child = the item just created
Q141199826	P40	LAST	S2600	"6000000008262061116"
#   the item just created: P735 given name = Q18985757 Tabitha
LAST	P735	Q18985757
#   P734 family name = Q1158485 Johnson, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q1158485	P3831	Q28418670
#   add a mul alias "Tabitha Johnson"
LAST	Amul	"Tabitha Johnson"

# create a new item
CREATE
#   set the en label to "Torkel Torbjørnson Høyland"
LAST	Len	"Torkel Torbjørnson Høyland"
#   set the mul label to "Torkel Torbjørnson Høyland"
LAST	Lmul	"Torkel Torbjørnson Høyland"
#   set the ja label to "トルケル・トルブヨルンソン・ホイランド"
LAST	Lja	"トルケル・トルブヨルンソン・ホイランド"
#   set the zh label to "托尔凯尔·托尔布永尔恩松·霍伊拉恩德"
LAST	Lzh	"托尔凯尔·托尔布永尔恩松·霍伊拉恩德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003492072756 Torkel Torbjørnson Høyland, qualified P1810 subject named as Torkel Torbjørnson Høyland
LAST	P2600	"6000000003492072756"	P1810	"Torkel Torbjørnson Høyland"
#   P569 date of birth = +1731-00-00T00:00:00Z/9
LAST	P569	+1731-00-00T00:00:00Z/9	S2600	"6000000003492072756"
#   P570 date of death = +1791-00-00T00:00:00Z/9
LAST	P570	+1791-00-00T00:00:00Z/9	S2600	"6000000003492072756"
#   P26 spouse = Q141205916 Kari Olsdatter
LAST	P26	Q141205916	S2600	"6000000003492072756"
#   P40 child = Q141198375 Astri Torchelsdatter Øvre Time
LAST	P40	Q141198375	S2600	"6000000003492072756"
#   Q141205916 Kari Olsdatter: P26 spouse = the item just created
Q141205916	P26	LAST	S2600	"6000000003492072756"
#   Q141198375 Astri Torchelsdatter Øvre Time: P22 father = the item just created
Q141198375	P22	LAST	S2600	"6000000003492072756"
#   the item just created: P735 given name = Q12719075 Torkel
LAST	P735	Q12719075
#   add a mul alias "Torkel Høyland"
LAST	Amul	"Torkel Høyland"

# create a new item
CREATE
#   set the en label to "Unn Mørck"
LAST	Len	"Unn Mørck"
#   set the mul label to "Unn Mørck"
LAST	Lmul	"Unn Mørck"
#   add a mul alias "Unn Garborg"
LAST	Amul	"Unn Garborg"
#   set the ja label to "ウン・モルクク"
LAST	Lja	"ウン・モルクク"
#   set the zh label to "乌恩·莫尔克克"
LAST	Lzh	"乌恩·莫尔克克"
#   add a ja alias "ウン・ガルボルグ"
LAST	Aja	"ウン・ガルボルグ"
#   add a zh alias "乌恩·加尔博格"
LAST	Azh	"乌恩·加尔博格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000116938744834 Unn (Bitten) Mørck, qualified P1810 subject named as Unn (Bitten) Garborg
LAST	P2600	"6000000116938744834"	P1810	"Unn (Bitten) Garborg"
#   P569 date of birth = +1917-03-19T00:00:00Z/11
LAST	P569	+1917-03-19T00:00:00Z/11	S2600	"6000000116938744834"
#   P570 date of death = +1988-08-26T00:00:00Z/11
LAST	P570	+1988-08-26T00:00:00Z/11	S2600	"6000000116938744834"
#   P22 father = Q141168837 Ingebret Garborg
LAST	P22	Q141168837	S2600	"6000000116938744834"
#   Q141168837 Ingebret Garborg: P40 child = the item just created
Q141168837	P40	LAST	S2600	"6000000116938744834"
#   the item just created: P735 given name = Q12719272 Unn
LAST	P735	Q12719272
#   P734 family name = Q30250555 Garborg, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q30250555	P3831	Q2507958
#   P1449 nickname = en:"Bitten"
LAST	P1449	en:"Bitten"
#   add a mul alias "Bitten Mørck"
LAST	Amul	"Bitten Mørck"
#   Q141198447 Kristina Tolvesdotter Näs: P26 spouse = Q19842232 Algot Bryniolfsson
Q141198447	P26	Q19842232	S2600	"340342479380013975"
#   Q141198835 Bergitte Gunnbjørnsdatter Aukland: P734 family name = Q4821650 Aukland
Q141198835	P734	Q4821650
#   Q141205932 Olof Timmerman: P40 child = Q141199704 Andreas Olai
Q141205932	P40	Q141199704	S2600	"6000000003125391522"
#   Q141199819 Anna Andersdotter: P26 spouse = Q141199704 Andreas Olai
Q141199819	P26	Q141199704	S2600	"6000000003125438035"
#   Q141199704 Andreas Olai: P22 father = Q141205932 Olof Timmerman
Q141199704	P22	Q141205932	S2600	"6000000004334566448"
#   P25 mother = Q141205926 NN
Q141199704	P25	Q141205926	S2600	"6000000004334566448"
#   P40 child = Q141200016 Nils Andersson
Q141199704	P40	Q141200016	S2600	"6000000004334566448"
#   P26 spouse = Q141199819 Anna Andersdotter
Q141199704	P26	Q141199819	S2600	"6000000004334566448"
#   Q19842232 Algot Bryniolfsson: P26 spouse = Q141198447 Kristina Tolvesdotter Näs
Q19842232	P26	Q141198447	S2600	"6000000005795638082"
#   Q141198381 Bengt Hafridsson Lejon: P40 child = Q5588874 Bryniolf Bengtsson (Hafridssons ätt)
Q141198381	P40	Q5588874	S2600	"6000000005795638104"
#   Q141200016 Nils Andersson: P22 father = Q141199704 Andreas Olai
Q141200016	P22	Q141199704	S2600	"6000000006127859612"
#   Q141205926 NN: P40 child = Q141199704 Andreas Olai
Q141205926	P40	Q141199704	S2600	"6000000006828575883"
#   Q101247444 Ingegerd Svantepolksdotter: P40 child = Q19842232 Algot Bryniolfsson
Q101247444	P40	Q19842232	S2600	"6000000011239201122"
#   P26 spouse = Q5588874 Bryniolf Bengtsson (Hafridssons ätt)
Q101247444	P26	Q5588874	S2600	"6000000011239201122"
#   Q141205924 N.N. Aukland: P734 family name = Q4821650 Aukland
Q141205924	P734	Q4821650

