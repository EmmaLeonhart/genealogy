# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   2067 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   Q45484869: set the de label
Q45484869	Lde	"Mann des Klans Chen, aus Shengzhou Jiangning"
#   Q45484869: set the it label
Q45484869	Lit	"uomo del clan Chen, da Shengzhou Jiangning"
#   Q45484869: set the pt label
Q45484869	Lpt	"homem do clã Chen, de Shengzhou Jiangning"
#   Q45484869: set the ca label
Q45484869	Lca	"home del clan Chen, de Shengzhou Jiangning"
#   Q45484932 (陳 of 昇州江寧): mul label = NN
Q45484932	Lmul	"NN"
#   Q45484932: set the nb label
Q45484932	Lnb	"mann av Chen-slekten, fra Shengzhou Jiangning"
#   Q45484932: set the da label
Q45484932	Lda	"mand af Chen-slægten, fra Shengzhou Jiangning"
#   Q45484932: set the sv label
Q45484932	Lsv	"man av Chen-ätten, från Shengzhou Jiangning"
#   Q45484932: set the de label
Q45484932	Lde	"Mann des Klans Chen, aus Shengzhou Jiangning"
#   Q45484932: set the it label
Q45484932	Lit	"uomo del clan Chen, da Shengzhou Jiangning"
#   Q45484932: set the pt label
Q45484932	Lpt	"homem do clã Chen, de Shengzhou Jiangning"
#   Q45484932: set the ca label
Q45484932	Lca	"home del clan Chen, de Shengzhou Jiangning"
#   Q45484995 (陳 of 昇州江寧): mul label = NN
Q45484995	Lmul	"NN"
#   Q45484995: set the nb label
Q45484995	Lnb	"mann av Chen-slekten, fra Shengzhou Jiangning"
#   Q45484995: set the da label
Q45484995	Lda	"mand af Chen-slægten, fra Shengzhou Jiangning"

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Ane Olsdatter Bø"
LAST	Len	"Ane Olsdatter Bø"
#   set the mul label to "Ane Olsdatter Bø"
LAST	Lmul	"Ane Olsdatter Bø"
#   add a mul alias "Ane Olsdatter Lende"
LAST	Amul	"Ane Olsdatter Lende"
#   set the ja label to "アーネ・オルスダッテル・ベー"
LAST	Lja	"アーネ・オルスダッテル・ベー"
#   set the zh label to "安内·奥尔斯达特·贝"
LAST	Lzh	"安内·奥尔斯达特·贝"
#   add a ja alias "アーネ・オルスダッテル・レンデ"
LAST	Aja	"アーネ・オルスダッテル・レンデ"
#   add a zh alias "安内·奥尔斯达特·莱恩德"
LAST	Azh	"安内·奥尔斯达特·莱恩德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000021133787411 Ane Olsdatter Bø, qualified P1810 subject named as Ane Olsdatter Lende
LAST	P2600	"6000000021133787411"	P1810	"Ane Olsdatter Lende"
#   P569 date of birth = +1857-03-22T00:00:00Z/11
LAST	P569	+1857-03-22T00:00:00Z/11	S2600	"6000000021133787411"
#   P570 date of death = +1934-03-21T00:00:00Z/11
LAST	P570	+1934-03-21T00:00:00Z/11	S2600	"6000000021133787411"
#   P26 spouse = Q141189099 Rasmus Helgesen Bø
LAST	P26	Q141189099	S2600	"6000000021133787411"
#   Q141189099 Rasmus Helgesen Bø: P26 spouse = the item just created
Q141189099	P26	LAST	S2600	"6000000021133787411"
#   the item just created: P735 given name = Q11958077 Ane
LAST	P735	Q11958077
#   P5056 patronym or matronym = Q51885688 Olsdatter
LAST	P5056	Q51885688
#   add a mul alias "Ane Bø"
LAST	Amul	"Ane Bø"

# create a new item
CREATE
#   set the en label to "Anna Börjesdotter Bothniensis"
LAST	Len	"Anna Börjesdotter Bothniensis"
#   set the mul label to "Anna Börjesdotter Bothniensis"
LAST	Lmul	"Anna Börjesdotter Bothniensis"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000006128124091 Anna Börjesdotter Bothniensis, qualified P1810 subject named as Anna Börjesdotter Bothniensis
LAST	P2600	"6000000006128124091"	P1810	"Anna Börjesdotter Bothniensis"
#   P569 date of birth = +1590-00-00T00:00:00Z/9
LAST	P569	+1590-00-00T00:00:00Z/9	S2600	"6000000006128124091"
#   P570 date of death = +1624-05-11T00:00:00Z/11
LAST	P570	+1624-05-11T00:00:00Z/11	S2600	"6000000006128124091"
#   P26 spouse = Q16649477 Nicolaus Jacobi Bothniensis
LAST	P26	Q16649477	S2600	"6000000006128124091"
#   P40 child = Q5960165 Carolus Nicolai Lithman
LAST	P40	Q5960165	S2600	"6000000006128124091"
#   Q16649477 Nicolaus Jacobi Bothniensis: P26 spouse = the item just created
Q16649477	P26	LAST	S2600	"6000000006128124091"
#   Q5960165 Carolus Nicolai Lithman: P25 mother = the item just created
Q5960165	P25	LAST	S2600	"6000000006128124091"
#   the item just created: P1449 nickname = en:"Anna Birgersdotter"
LAST	P1449	en:"Anna Birgersdotter"
#   add a mul alias "Anna Birgersdotter Bothniensis"
LAST	Amul	"Anna Birgersdotter Bothniensis"

# create a new item
CREATE
#   set the en label to "Anna Olsdatter Heigre"
LAST	Len	"Anna Olsdatter Heigre"
#   set the mul label to "Anna Olsdatter Heigre"
LAST	Lmul	"Anna Olsdatter Heigre"
#   set the ja label to "アンナ・オルスダッテル・ヘイグレ"
LAST	Lja	"アンナ・オルスダッテル・ヘイグレ"
#   set the zh label to "安娜·奥尔斯达特·海格勒"
LAST	Lzh	"安娜·奥尔斯达特·海格勒"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000033810806905 Anna Olsdatter Heigre, qualified P1810 subject named as Anna Olsdatter Heigre
LAST	P2600	"6000000033810806905"	P1810	"Anna Olsdatter Heigre"
#   P569 date of birth = +1729-08-25T00:00:00Z/11
LAST	P569	+1729-08-25T00:00:00Z/11	S2600	"6000000033810806905"
#   P570 date of death = +1795-00-00T00:00:00Z/9
LAST	P570	+1795-00-00T00:00:00Z/9	S2600	"6000000033810806905"
#   P40 child = Q141216637 Ola Person Persson Heigre
LAST	P40	Q141216637	S2600	"6000000033810806905"
#   Q141216637 Ola Person Persson Heigre: P25 mother = the item just created
Q141216637	P25	LAST	S2600	"6000000033810806905"
#   the item just created: P5056 patronym or matronym = Q51885688 Olsdatter
LAST	P5056	Q51885688
#   add a mul alias "Anna Heigre"
LAST	Amul	"Anna Heigre"

# create a new item
CREATE
#   set the en label to "Barbro Reiersdatter Storhaug"
LAST	Len	"Barbro Reiersdatter Storhaug"
#   set the mul label to "Barbro Reiersdatter Storhaug"
LAST	Lmul	"Barbro Reiersdatter Storhaug"
#   add a mul alias "Barbro Reiersdatter Kydland"
LAST	Amul	"Barbro Reiersdatter Kydland"
#   set the ja label to "バルブロ・レイエルスダッテル・ストルハウグ"
LAST	Lja	"バルブロ・レイエルスダッテル・ストルハウグ"
#   set the zh label to "巴尔布罗·雷伊埃尔斯达特·斯托尔哈乌格"
LAST	Lzh	"巴尔布罗·雷伊埃尔斯达特·斯托尔哈乌格"
#   add a ja alias "バルブロ・レイエルスダッテル・キドランド"
LAST	Aja	"バルブロ・レイエルスダッテル・キドランド"
#   add a zh alias "巴尔布罗·雷伊埃尔斯达特·基德拉恩德"
LAST	Azh	"巴尔布罗·雷伊埃尔斯达特·基德拉恩德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005606976869 Barbro Reiersdatter Storhaug, qualified P1810 subject named as Barbro Reiersdatter Kydland
LAST	P2600	"6000000005606976869"	P1810	"Barbro Reiersdatter Kydland"
#   P569 date of birth = +1725-00-00T00:00:00Z/9
LAST	P569	+1725-00-00T00:00:00Z/9	S2600	"6000000005606976869"
#   P570 date of death = +1804-10-14T00:00:00Z/11
LAST	P570	+1804-10-14T00:00:00Z/11	S2600	"6000000005606976869"
#   P40 child = Q141199937 Maren Halvorsdatter Øksnevad
LAST	P40	Q141199937	S2600	"6000000005606976869"
#   Q141199937 Maren Halvorsdatter Øksnevad: P25 mother = the item just created
Q141199937	P25	LAST	S2600	"6000000005606976869"
#   the item just created: P735 given name = Q807877 Barbro
LAST	P735	Q807877
#   P734 family name = Q27892826 Storhaug, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q27892826	P3831	Q28418670
#   add a mul alias "Barbro Storhaug"
LAST	Amul	"Barbro Storhaug"

# create a new item
CREATE
#   set the en label to "Carl Emil Cronhielm af Hakunge"
LAST	Len	"Carl Emil Cronhielm af Hakunge"
#   set the mul label to "Carl Emil Cronhielm af Hakunge"
LAST	Lmul	"Carl Emil Cronhielm af Hakunge"
#   set the ja label to "カルル・エミール・クロンヒエルム・アフ・ハクンゲ"
LAST	Lja	"カルル・エミール・クロンヒエルム・アフ・ハクンゲ"
#   set the zh label to "卡尔尔·埃米尔·克罗恩希埃尔姆·阿夫·哈库恩盖"
LAST	Lzh	"卡尔尔·埃米尔·克罗恩希埃尔姆·阿夫·哈库恩盖"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000008178453589 Carl Emil Cronhielm af Hakunge, qualified P1810 subject named as Carl Emil Cronhielm af Hakunge
LAST	P2600	"6000000008178453589"	P1810	"Carl Emil Cronhielm af Hakunge"
#   P569 date of birth = +1752-09-09T00:00:00Z/11
LAST	P569	+1752-09-09T00:00:00Z/11	S2600	"6000000008178453589"
#   P570 date of death = +1806-12-03T00:00:00Z/11
LAST	P570	+1806-12-03T00:00:00Z/11	S2600	"6000000008178453589"
#   P40 child = Q4938400 Christina Charlotta Cronhielm af Hakunge
LAST	P40	Q4938400	S2600	"6000000008178453589"
#   Q4938400 Christina Charlotta Cronhielm af Hakunge: P22 father = the item just created
Q4938400	P22	LAST	S2600	"6000000008178453589"
#   the item just created: P735 given name = Q2529610 Carl, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q2529610	P1545	"1"	P7452	Q3409033
#   P735 given name = Q989320 Emil, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q989320	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Christian Frenning"
LAST	Len	"Christian Frenning"
#   set the mul label to "Christian Frenning"
LAST	Lmul	"Christian Frenning"
#   set the ja label to "クリスチャン・フレニング"
LAST	Lja	"クリスチャン・フレニング"
#   set the zh label to "克里斯蒂安·夫雷尼恩格"
LAST	Lzh	"克里斯蒂安·夫雷尼恩格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000019540497660 Christian Frenning, qualified P1810 subject named as Christian Frenning
LAST	P2600	"6000000019540497660"	P1810	"Christian Frenning"
#   P569 date of birth = +1840-05-13T00:00:00Z/11
LAST	P569	+1840-05-13T00:00:00Z/11	S2600	"6000000019540497660"
#   P570 date of death = +1930-02-22T00:00:00Z/11
LAST	P570	+1930-02-22T00:00:00Z/11	S2600	"6000000019540497660"
#   P26 spouse = Q141189083 Martha Elida Frenning
LAST	P26	Q141189083	S2600	"6000000019540497660"
#   Q141189083 Martha Elida Frenning: P26 spouse = the item just created
Q141189083	P26	LAST	S2600	"6000000019540497660"
#   the item just created: P735 given name = Q18001597 Christian
LAST	P735	Q18001597

# create a new item
CREATE
#   set the en label to "Daniel Andreasson"
LAST	Len	"Daniel Andreasson"
#   set the mul label to "Daniel Andreasson"
LAST	Lmul	"Daniel Andreasson"
#   set the ja label to "ダニエル・アンドレアソン"
LAST	Lja	"ダニエル・アンドレアソン"
#   set the zh label to "达尼埃尔·阿恩德雷阿松"
LAST	Lzh	"达尼埃尔·阿恩德雷阿松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000006127859581 Daniel Andreasson, qualified P1810 subject named as Daniel Andreasson
LAST	P2600	"6000000006127859581"	P1810	"Daniel Andreasson"
#   P569 date of birth = +1544-12-09T00:00:00Z/11
LAST	P569	+1544-12-09T00:00:00Z/11	S2600	"6000000006127859581"
#   P22 father = Q141199704 Andreas Olai
LAST	P22	Q141199704	S2600	"6000000006127859581"
#   P25 mother = Q141199819 Anna Andersdotter
LAST	P25	Q141199819	S2600	"6000000006127859581"
#   Q141199704 Andreas Olai: P40 child = the item just created
Q141199704	P40	LAST	S2600	"6000000006127859581"
#   Q141199819 Anna Andersdotter: P40 child = the item just created
Q141199819	P40	LAST	S2600	"6000000006127859581"
#   the item just created: P735 given name = Q53787734 Daniel
LAST	P735	Q53787734

# create a new item
CREATE
#   set the en label to "Elisabet Rasmusdatter Moen"
LAST	Len	"Elisabet Rasmusdatter Moen"
#   set the mul label to "Elisabet Rasmusdatter Moen"
LAST	Lmul	"Elisabet Rasmusdatter Moen"
#   add a mul alias "Elisabet Rasmusdatter Bø"
LAST	Amul	"Elisabet Rasmusdatter Bø"
#   set the ja label to "エリサベート・ラスムスダッテル・モエン"
LAST	Lja	"エリサベート・ラスムスダッテル・モエン"
#   set the zh label to "伊丽莎白·拉斯穆斯达特·莫埃恩"
LAST	Lzh	"伊丽莎白·拉斯穆斯达特·莫埃恩"
#   add a ja alias "エリサベート・ラスムスダッテル・ベー"
LAST	Aja	"エリサベート・ラスムスダッテル・ベー"
#   add a zh alias "伊丽莎白·拉斯穆斯达特·贝"
LAST	Azh	"伊丽莎白·拉斯穆斯达特·贝"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000225376733918 Elisabet Rasmusdatter Moen, qualified P1810 subject named as Elisabet Rasmusdatter Bø
LAST	P2600	"6000000225376733918"	P1810	"Elisabet Rasmusdatter Bø"
#   P569 date of birth = +1887-06-09T00:00:00Z/11
LAST	P569	+1887-06-09T00:00:00Z/11	S2600	"6000000225376733918"
#   P22 father = Q141189099 Rasmus Helgesen Bø
LAST	P22	Q141189099	S2600	"6000000225376733918"
#   Q141189099 Rasmus Helgesen Bø: P40 child = the item just created
Q141189099	P40	LAST	S2600	"6000000225376733918"
#   the item just created: P735 given name = Q16423275 Elisabet
LAST	P735	Q16423275
#   P734 family name = Q16934183 Moen, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q16934183	P3831	Q28418670
#   add a mul alias "Elisabet Moen"
LAST	Amul	"Elisabet Moen"

# create a new item
CREATE
#   set the en label to "Gustava Maria Sofia Mannerheim"
LAST	Len	"Gustava Maria Sofia Mannerheim"
#   set the mul label to "Gustava Maria Sofia Mannerheim"
LAST	Lmul	"Gustava Maria Sofia Mannerheim"
#   set the ja label to "グスタヴァ・マリア・ソフィア・マネルヘイム"
LAST	Lja	"グスタヴァ・マリア・ソフィア・マネルヘイム"
#   set the zh label to "古斯塔娃·马里阿·索菲阿·马内尔赫伊姆"
LAST	Lzh	"古斯塔娃·马里阿·索菲阿·马内尔赫伊姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 4143225 Gustava Maria Sofia Mannerheim, qualified P1810 subject named as Gustava Maria Sofia Mannerheim
LAST	P2600	"4143225"	P1810	"Gustava Maria Sofia Mannerheim"
#   P569 date of birth = +1801-04-30T00:00:00Z/11
LAST	P569	+1801-04-30T00:00:00Z/11	S2600	"4143225"
#   P570 date of death = +1822-02-17T00:00:00Z/11
LAST	P570	+1822-02-17T00:00:00Z/11	S2600	"4143225"
#   P22 father = Q1814297 Carl Erik Mannerheim
LAST	P22	Q1814297	S2600	"4143225"
#   Q1814297 Carl Erik Mannerheim: P40 child = the item just created
Q1814297	P40	LAST	S2600	"4143225"
#   the item just created: P735 given name = Q21144392 Gustava, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q21144392	P1545	"1"	P7452	Q3409033

# create a new item
CREATE
#   set the en label to "Halvor Johannesson Hobberstad"
LAST	Len	"Halvor Johannesson Hobberstad"
#   set the mul label to "Halvor Johannesson Hobberstad"
LAST	Lmul	"Halvor Johannesson Hobberstad"
#   set the ja label to "ハルヴォル・ヨハネソン・ホベルスタド"
LAST	Lja	"ハルヴォル・ヨハネソン・ホベルスタド"
#   set the zh label to "哈尔沃尔·永哈内松·霍贝尔斯塔德"
LAST	Lzh	"哈尔沃尔·永哈内松·霍贝尔斯塔德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005609265668 Halvor Johannesson Hobberstad, qualified P1810 subject named as Halvor Johannesson Hobberstad
LAST	P2600	"6000000005609265668"	P1810	"Halvor Johannesson Hobberstad"
#   P569 date of birth = +1720-00-00T00:00:00Z/9
LAST	P569	+1720-00-00T00:00:00Z/9	S2600	"6000000005609265668"
#   P570 date of death = +1794-07-16T00:00:00Z/11
LAST	P570	+1794-07-16T00:00:00Z/11	S2600	"6000000005609265668"
#   P40 child = Q141199937 Maren Halvorsdatter Øksnevad
LAST	P40	Q141199937	S2600	"6000000005609265668"
#   Q141199937 Maren Halvorsdatter Øksnevad: P22 father = the item just created
Q141199937	P22	LAST	S2600	"6000000005609265668"
#   the item just created: P735 given name = Q16276226 Halvor
LAST	P735	Q16276226

# create a new item
CREATE
#   set the en label to "Harriet Hjørdis Simensen"
LAST	Len	"Harriet Hjørdis Simensen"
#   set the mul label to "Harriet Hjørdis Simensen"
LAST	Lmul	"Harriet Hjørdis Simensen"
#   add a mul alias "Harriet Hjørdis Frenning"
LAST	Amul	"Harriet Hjørdis Frenning"
#   set the ja label to "ハリエト・ヨルディス・シーメンセン"
LAST	Lja	"ハリエト・ヨルディス・シーメンセン"
#   set the zh label to "哈里埃特·永尔迪斯·西门森"
LAST	Lzh	"哈里埃特·永尔迪斯·西门森"
#   add a ja alias "ハリエト・ヨルディス・フレニング"
LAST	Aja	"ハリエト・ヨルディス・フレニング"
#   add a zh alias "哈里埃特·永尔迪斯·夫雷尼恩格"
LAST	Azh	"哈里埃特·永尔迪斯·夫雷尼恩格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000021122676911 Harriet Hjørdis Simensen, qualified P1810 subject named as Harriet Hjørdis Frenning
LAST	P2600	"6000000021122676911"	P1810	"Harriet Hjørdis Frenning"
#   P569 date of birth = +1877-03-11T00:00:00Z/11
LAST	P569	+1877-03-11T00:00:00Z/11	S2600	"6000000021122676911"
#   P570 date of death = +1962-09-01T00:00:00Z/11
LAST	P570	+1962-09-01T00:00:00Z/11	S2600	"6000000021122676911"
#   P25 mother = Q141189083 Martha Elida Frenning
LAST	P25	Q141189083	S2600	"6000000021122676911"
#   Q141189083 Martha Elida Frenning: P40 child = the item just created
Q141189083	P40	LAST	S2600	"6000000021122676911"
#   the item just created: P735 given name = Q5486209 Harriet, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q5486209	P1545	"1"	P7452	Q3409033
#   P735 given name = Q33093456 Hjørdis, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q33093456	P1545	"2"	P3831	Q245025
#   P734 family name = Q30317167 Simensen, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q30317167	P3831	Q28418670

# create a new item
CREATE
#   set the en label to "Hedvig Ulrika Boije af Gennäs"
LAST	Len	"Hedvig Ulrika Boije af Gennäs"
#   set the mul label to "Hedvig Ulrika Boije af Gennäs"
LAST	Lmul	"Hedvig Ulrika Boije af Gennäs"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000012888307497 Hedvig Ulrika Boije af Gennäs, qualified P1810 subject named as Hedvig Ulrika Boije af Gennäs
LAST	P2600	"6000000012888307497"	P1810	"Hedvig Ulrika Boije af Gennäs"
#   P569 date of birth = +1761-05-26T00:00:00Z/11
LAST	P569	+1761-05-26T00:00:00Z/11	S2600	"6000000012888307497"
#   P570 date of death = +1843-09-27T00:00:00Z/11
LAST	P570	+1843-09-27T00:00:00Z/11	S2600	"6000000012888307497"
#   P40 child = Q4938400 Christina Charlotta Cronhielm af Hakunge
LAST	P40	Q4938400	S2600	"6000000012888307497"
#   Q4938400 Christina Charlotta Cronhielm af Hakunge: P25 mother = the item just created
Q4938400	P25	LAST	S2600	"6000000012888307497"
#   the item just created: P735 given name = Q13648620 Hedvig, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q13648620	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18924998 Ulrika, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q18924998	P1545	"2"	P3831	Q245025
#   P734 family name = Q28149669 Boije, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q28149669	P3831	Q28418670

# create a new item
CREATE
#   set the en label to "Lars Osmundsen Nese"
LAST	Len	"Lars Osmundsen Nese"
#   set the mul label to "Lars Osmundsen Nese"
LAST	Lmul	"Lars Osmundsen Nese"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000069466362236 Lars Osmundsen Nese, qualified P1810 subject named as Lars Osmundsen Foss-Eikeland d. y.
LAST	P2600	"6000000069466362236"	P1810	"Lars Osmundsen Foss-Eikeland d. y."
#   P569 date of birth = +1759-00-00T00:00:00Z/9
LAST	P569	+1759-00-00T00:00:00Z/9	S2600	"6000000069466362236"
#   P570 date of death = +1840-09-16T00:00:00Z/11
LAST	P570	+1840-09-16T00:00:00Z/11	S2600	"6000000069466362236"
#   P22 father = Q141217404 Osmund Larsen Raunes
LAST	P22	Q141217404	S2600	"6000000069466362236"
#   Q141217404 Osmund Larsen Raunes: P40 child = the item just created
Q141217404	P40	LAST	S2600	"6000000069466362236"
#   the item just created: P735 given name = Q15635262 Lars
LAST	P735	Q15635262

# create a new item
CREATE
#   set the en label to "Lloyd Obert Dokken"
LAST	Len	"Lloyd Obert Dokken"
#   set the mul label to "Lloyd Obert Dokken"
LAST	Lmul	"Lloyd Obert Dokken"
#   set the ja label to "ロイド・オベルト・ドケン"
LAST	Lja	"ロイド・オベルト・ドケン"
#   set the zh label to "洛伊德·奥贝尔特·多凯恩"
LAST	Lzh	"洛伊德·奥贝尔特·多凯恩"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000189964580833 Lloyd Obert Dokken, qualified P1810 subject named as Lloyd Obert Dokken
LAST	P2600	"6000000189964580833"	P1810	"Lloyd Obert Dokken"
#   P569 date of birth = +1894-06-00T00:00:00Z/10
LAST	P569	+1894-06-00T00:00:00Z/10	S2600	"6000000189964580833"
#   P570 date of death = +1976-03-25T00:00:00Z/11
LAST	P570	+1976-03-25T00:00:00Z/11	S2600	"6000000189964580833"
#   P26 spouse = Q141168786 Alice Ronneberg
LAST	P26	Q141168786	S2600	"6000000189964580833"
#   Q141168786 Alice Ronneberg: P26 spouse = the item just created
Q141168786	P26	LAST	S2600	"6000000189964580833"
#   the item just created: P735 given name = Q13478831 Lloyd, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q13478831	P1545	"1"	P7452	Q3409033

# create a new item
CREATE
#   set the en label to "Marta Torbjørnsdotter Gjesdal"
LAST	Len	"Marta Torbjørnsdotter Gjesdal"
#   set the mul label to "Marta Torbjørnsdotter Gjesdal"
LAST	Lmul	"Marta Torbjørnsdotter Gjesdal"
#   set the ja label to "マルタ・トルブヨルンスドッテル・イェスダール"
LAST	Lja	"マルタ・トルブヨルンスドッテル・イェスダール"
#   set the zh label to "玛尔塔·托尔布永尔恩斯多特·耶斯达尔"
LAST	Lzh	"玛尔塔·托尔布永尔恩斯多特·耶斯达尔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005607335640 Marta Torbjørnsdotter Gjesdal, qualified P1810 subject named as Marta Torbjørnsdotter Gjesdal
LAST	P2600	"6000000005607335640"	P1810	"Marta Torbjørnsdotter Gjesdal"
#   P569 date of birth = +1745-00-00T00:00:00Z/9
LAST	P569	+1745-00-00T00:00:00Z/9	S2600	"6000000005607335640"
#   P570 date of death = +1801-00-00T00:00:00Z/9
LAST	P570	+1801-00-00T00:00:00Z/9	S2600	"6000000005607335640"
#   P40 child = Q141217391 Kristine Sørensdatter Gjesdal
LAST	P40	Q141217391	S2600	"6000000005607335640"
#   Q141217391 Kristine Sørensdatter Gjesdal: P25 mother = the item just created
Q141217391	P25	LAST	S2600	"6000000005607335640"
#   the item just created: P735 given name = Q846741 Marta
LAST	P735	Q846741
#   P734 family name = Q27888954 Gjesdal
LAST	P734	Q27888954
#   P1449 nickname = en:"Martha Torbiørnsdatter Giestdahl"
LAST	P1449	en:"Martha Torbiørnsdatter Giestdahl"
#   add a mul alias "Martha Torbiørnsdatter Giestdahl Gjesdal"
LAST	Amul	"Martha Torbiørnsdatter Giestdahl Gjesdal"

# create a new item
CREATE
#   set the en label to "Per Danielsson"
LAST	Len	"Per Danielsson"
#   set the mul label to "Per Danielsson"
LAST	Lmul	"Per Danielsson"
#   set the ja label to "ペル・ダニエルソン"
LAST	Lja	"ペル・ダニエルソン"
#   set the zh label to "佩尔·达尼埃尔松"
LAST	Lzh	"佩尔·达尼埃尔松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000220774881848 Per Danielsson, qualified P1810 subject named as Per Danielsson
LAST	P2600	"6000000220774881848"	P1810	"Per Danielsson"
#   P569 date of birth = +1725-00-00T00:00:00Z/9
LAST	P569	+1725-00-00T00:00:00Z/9	S2600	"6000000220774881848"
#   P22 father = Q141216461 Daniel Andersson
LAST	P22	Q141216461	S2600	"6000000220774881848"
#   P25 mother = Q141216633 Malin Jacobsdotter
LAST	P25	Q141216633	S2600	"6000000220774881848"
#   Q141216461 Daniel Andersson: P40 child = the item just created
Q141216461	P40	LAST	S2600	"6000000220774881848"
#   Q141216633 Malin Jacobsdotter: P40 child = the item just created
Q141216633	P40	LAST	S2600	"6000000220774881848"
#   the item just created: P735 given name = Q13582800 Per
LAST	P735	Q13582800

# create a new item
CREATE
#   set the mul label to "NN"
LAST	Lmul	"NN"
#   set the ca label to "fill de Lloyd Obert Dokken"
LAST	Lca	"fill de Lloyd Obert Dokken"
#   set the da label to "søn af Lloyd Obert Dokken"
LAST	Lda	"søn af Lloyd Obert Dokken"
#   set the de label to "Sohn von Lloyd Obert Dokken"
LAST	Lde	"Sohn von Lloyd Obert Dokken"
#   set the en label to "son of Lloyd Obert Dokken"
LAST	Len	"son of Lloyd Obert Dokken"
#   set the es label to "hijo de Lloyd Obert Dokken"
LAST	Les	"hijo de Lloyd Obert Dokken"
#   set the it label to "figlio di Lloyd Obert Dokken"
LAST	Lit	"figlio di Lloyd Obert Dokken"
#   set the ja label to "ロイド・オベルト・ドケンの息子"
LAST	Lja	"ロイド・オベルト・ドケンの息子"
#   set the nb label to "sønn av Lloyd Obert Dokken"
LAST	Lnb	"sønn av Lloyd Obert Dokken"
#   set the nl label to "zoon van Lloyd Obert Dokken"
LAST	Lnl	"zoon van Lloyd Obert Dokken"
#   set the pt label to "filho de Lloyd Obert Dokken"
LAST	Lpt	"filho de Lloyd Obert Dokken"
#   set the sv label to "son till Lloyd Obert Dokken"
LAST	Lsv	"son till Lloyd Obert Dokken"
#   set the zh label to "洛伊德·奥贝尔特·多凯恩之子"
LAST	Lzh	"洛伊德·奥贝尔特·多凯恩之子"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000189964478852 NN Private, qualified P1810 subject named as Private
LAST	P2600	"6000000189964478852"	P1810	"Private"
#   P25 mother = Q141168786 Alice Ronneberg
LAST	P25	Q141168786	S2600	"6000000189964478852"
#   Q141168786 Alice Ronneberg: P40 child = the item just created
Q141168786	P40	LAST	S2600	"6000000189964478852"

# create a new item
CREATE
#   the item just created: set the en label to "Ragnhild Sofie Jensdatter Wendt"
LAST	Len	"Ragnhild Sofie Jensdatter Wendt"
#   set the mul label to "Ragnhild Sofie Jensdatter Wendt"
LAST	Lmul	"Ragnhild Sofie Jensdatter Wendt"
#   set the ja label to "ラグンヒル・ソフィエ・イェンスダッテル・ヴェント"
LAST	Lja	"ラグンヒル・ソフィエ・イェンスダッテル・ヴェント"
#   set the zh label to "拉格希尔德·索菲埃·耶恩斯达特·温特"
LAST	Lzh	"拉格希尔德·索菲埃·耶恩斯达特·温特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000048056977090 Ragnhild Sofie Jensdatter Wendt, qualified P1810 subject named as Ragnhild Sofie Jensdatter Wendt
LAST	P2600	"6000000048056977090"	P1810	"Ragnhild Sofie Jensdatter Wendt"
#   P569 date of birth = +1888-08-31T00:00:00Z/11
LAST	P569	+1888-08-31T00:00:00Z/11	S2600	"6000000048056977090"
#   P570 date of death = +1899-11-27T00:00:00Z/11
LAST	P570	+1899-11-27T00:00:00Z/11	S2600	"6000000048056977090"
#   P22 father = Q141216386 Jens Wilhelm Wendt
LAST	P22	Q141216386	S2600	"6000000048056977090"
#   P25 mother = Q141216377 Hanna Sofie Wendt
LAST	P25	Q141216377	S2600	"6000000048056977090"
#   Q141216386 Jens Wilhelm Wendt: P40 child = the item just created
Q141216386	P40	LAST	S2600	"6000000048056977090"
#   Q141216377 Hanna Sofie Wendt: P40 child = the item just created
Q141216377	P40	LAST	S2600	"6000000048056977090"
#   the item just created: P735 given name = Q1390292 Ragnhild, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q1390292	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18201530 Sofie, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q18201530	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Søren Sørenson Gjesdal"
LAST	Len	"Søren Sørenson Gjesdal"
#   set the mul label to "Søren Sørenson Gjesdal"
LAST	Lmul	"Søren Sørenson Gjesdal"
#   add a mul alias "Søren Sørenson Helland"
LAST	Amul	"Søren Sørenson Helland"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003095047808 Søren Sørenson Gjesdal, qualified P1810 subject named as Søren Sørenson Helland
LAST	P2600	"6000000003095047808"	P1810	"Søren Sørenson Helland"
#   P569 date of birth = +1739-00-00T00:00:00Z/9
LAST	P569	+1739-00-00T00:00:00Z/9	S2600	"6000000003095047808"
#   P570 date of death = +1806-00-00T00:00:00Z/9
LAST	P570	+1806-00-00T00:00:00Z/9	S2600	"6000000003095047808"
#   P40 child = Q141217391 Kristine Sørensdatter Gjesdal
LAST	P40	Q141217391	S2600	"6000000003095047808"
#   Q141217391 Kristine Sørensdatter Gjesdal: P22 father = the item just created
Q141217391	P22	LAST	S2600	"6000000003095047808"
#   the item just created: P735 given name = Q7174941 Søren
LAST	P735	Q7174941
#   P734 family name = Q30085478 Helland, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q30085478	P3831	Q2507958
#   P734 family name = Q27888954 Gjesdal
LAST	P734	Q27888954
#   add a mul alias "Søren Gjesdal"
LAST	Amul	"Søren Gjesdal"

# create a new item
CREATE
#   set the en label to "Tørres Jonsson Vatne"
LAST	Len	"Tørres Jonsson Vatne"
#   set the mul label to "Tørres Jonsson Vatne"
LAST	Lmul	"Tørres Jonsson Vatne"
#   set the ja label to "トレス・ヨンソン・ヴァトネ"
LAST	Lja	"トレス・ヨンソン・ヴァトネ"
#   set the zh label to "托雷斯·永松·瓦特内"
LAST	Lzh	"托雷斯·永松·瓦特内"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000014516687339 Tørres Jonsson Vatne, qualified P1810 subject named as Tørres Jonsson Vatne
LAST	P2600	"6000000014516687339"	P1810	"Tørres Jonsson Vatne"
#   P569 date of birth = +1816-02-17T00:00:00Z/11
LAST	P569	+1816-02-17T00:00:00Z/11	S2600	"6000000014516687339"
#   P22 father = Q141216388 Jon Hansson St. Vatne
LAST	P22	Q141216388	S2600	"6000000014516687339"
#   P25 mother = Q141206057 Berte Tørresdotter Austrått
LAST	P25	Q141206057	S2600	"6000000014516687339"
#   Q141216388 Jon Hansson St. Vatne: P40 child = the item just created
Q141216388	P40	LAST	S2600	"6000000014516687339"
#   Q141206057 Berte Tørresdotter Austrått: P40 child = the item just created
Q141206057	P40	LAST	S2600	"6000000014516687339"
#   the item just created: P734 family name = Q30134985 Vatne
LAST	P734	Q30134985

# create a new item
CREATE
#   set the en label to "Ulrika Persdotter"
LAST	Len	"Ulrika Persdotter"
#   set the mul label to "Ulrika Persdotter"
LAST	Lmul	"Ulrika Persdotter"
#   set the ja label to "ウルリカ・ペルスドッテル"
LAST	Lja	"ウルリカ・ペルスドッテル"
#   set the zh label to "乌尔里卡·佩尔斯多特"
LAST	Lzh	"乌尔里卡·佩尔斯多特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000177920129831 Ulrika Persdotter, qualified P1810 subject named as Ulrika Persdotter
LAST	P2600	"6000000177920129831"	P1810	"Ulrika Persdotter"
#   P569 date of birth = +1811-07-16T00:00:00Z/11
LAST	P569	+1811-07-16T00:00:00Z/11	S2600	"6000000177920129831"
#   P570 date of death = +1894-02-05T00:00:00Z/11
LAST	P570	+1894-02-05T00:00:00Z/11	S2600	"6000000177920129831"
#   P22 father = Q141217433 Per Persson Hagman
LAST	P22	Q141217433	S2600	"6000000177920129831"
#   Q141217433 Per Persson Hagman: P40 child = the item just created
Q141217433	P40	LAST	S2600	"6000000177920129831"
#   the item just created: P735 given name = Q18924998 Ulrika
LAST	P735	Q18924998
#   Q141217384 David Tjølson Edland: P26 spouse = Q141217391 Kristine Sørensdatter Gjesdal
Q141217384	P26	Q141217391	S2600	"6000000002690086678"
#   Q141217391 Kristine Sørensdatter Gjesdal: P26 spouse = Q141217384 David Tjølson Edland
Q141217391	P26	Q141217384	S2600	"6000000005607335630"
#   Q141217369 Anna Osmundsd Stokka: P40 child = Q141217404 Osmund Larsen Raunes
Q141217369	P40	Q141217404	S2600	"6000000005609304839"
#   Q141217433 Per Persson Hagman: P22 father = Q141217431 Per Andersson Storskytt
Q141217433	P22	Q141217431	S2600	"6000000011078726908"
#   Q141217431 Per Andersson Storskytt: P40 child = Q141217433 Per Persson Hagman
Q141217431	P40	Q141217433	S2600	"6000000011078829655"
#   Q141217404 Osmund Larsen Raunes: P25 mother = Q141217369 Anna Osmundsd Stokka
Q141217404	P25	Q141217369	S2600	"6000000012587690898"
#   Q141217372 Berta Larsdatter Stangeland: P40 child = Q141217392 Larine Eriksdatter Heigre
Q141217372	P40	Q141217392	S2600	"6000000023500402302"
#   Q141217398 Måns Moge: P26 spouse = Q141217396 Maria No name
Q141217398	P26	Q141217396	S2600	"6000000027469942604"
#   Q141217396 Maria No name: P26 spouse = Q141217398 Måns Moge
Q141217396	P26	Q141217398	S2600	"6000000027470028034"
#   Q141217392 Larine Eriksdatter Heigre: P25 mother = Q141217372 Berta Larsdatter Stangeland
Q141217392	P25	Q141217372	S2600	"6000000201256773828"

