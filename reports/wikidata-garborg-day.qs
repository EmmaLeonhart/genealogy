# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   2157 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   Q45448943: set the nb label
Q45448943	Lnb	"mann av Xiao-slekten, fra Lanling"
#   Q45448943: set the da label
Q45448943	Lda	"mand af Xiao-slægten, fra Lanling"
#   Q45448943: set the sv label
Q45448943	Lsv	"man av Xiao-ätten, från Lanling"
#   Q45448943: set the de label
Q45448943	Lde	"Mann des Klans Xiao, aus Lanling"
#   Q45448943: set the it label
Q45448943	Lit	"uomo del clan Xiao, da Lanling"
#   Q45448943: set the pt label
Q45448943	Lpt	"homem do clã Xiao, de Lanling"
#   Q45448943: set the ca label
Q45448943	Lca	"home del clan Xiao, de Lanling"
#   Q45449130 (蕭 of 蘭陵): mul label = NN
Q45449130	Lmul	"NN"
#   Q45449130: set the nb label
Q45449130	Lnb	"mann av Xiao-slekten, fra Lanling"
#   Q45449130: set the da label
Q45449130	Lda	"mand af Xiao-slægten, fra Lanling"
#   Q45449130: set the sv label
Q45449130	Lsv	"man av Xiao-ätten, från Lanling"
#   Q45449130: set the de label
Q45449130	Lde	"Mann des Klans Xiao, aus Lanling"
#   Q45449130: set the it label
Q45449130	Lit	"uomo del clan Xiao, da Lanling"
#   Q45449130: set the pt label
Q45449130	Lpt	"homem do clã Xiao, de Lanling"
#   Q45449130: set the ca label
Q45449130	Lca	"home del clan Xiao, de Lanling"

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Anna Elisabet Angerstein"
LAST	Len	"Anna Elisabet Angerstein"
#   set the mul label to "Anna Elisabet Angerstein"
LAST	Lmul	"Anna Elisabet Angerstein"
#   set the ja label to "アンナ・エリサベート・アンゲルステイン"
LAST	Lja	"アンナ・エリサベート・アンゲルステイン"
#   set the zh label to "安娜·伊丽莎白·阿恩盖尔斯特伊恩"
LAST	Lzh	"安娜·伊丽莎白·阿恩盖尔斯特伊恩"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000013252126990 Anna Elisabet Angerstein, qualified P1810 subject named as Anna Elisabet Angerstein
LAST	P2600	"6000000013252126990"	P1810	"Anna Elisabet Angerstein"
#   P569 date of birth = +1716-06-16T00:00:00Z/11
LAST	P569	+1716-06-16T00:00:00Z/11	S2600	"6000000013252126990"
#   P570 date of death = +1750-09-03T00:00:00Z/11
LAST	P570	+1750-09-03T00:00:00Z/11	S2600	"6000000013252126990"
#   P26 spouse = Q1168365 Samuel Olofsson Troilius
LAST	P26	Q1168365	S2600	"6000000013252126990"
#   P40 child = Q943803 Uno von Troil
LAST	P40	Q943803	S2600	"6000000013252126990"
#   Q1168365 Samuel Olofsson Troilius: P26 spouse = the item just created
Q1168365	P26	LAST	S2600	"6000000013252126990"
#   Q943803 Uno von Troil: P25 mother = the item just created
Q943803	P25	LAST	S2600	"6000000013252126990"
#   the item just created: P735 given name = Q16423275 Elisabet, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q16423275	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Anna Osmundsd Stokka"
LAST	Len	"Anna Osmundsd Stokka"
#   set the mul label to "Anna Osmundsd Stokka"
LAST	Lmul	"Anna Osmundsd Stokka"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005609304839 Anna Osmundsd Stokka, qualified P1810 subject named as Anna Osmundsd Stokka
LAST	P2600	"6000000005609304839"	P1810	"Anna Osmundsd Stokka"
#   P569 date of birth = +1700-00-00T00:00:00Z/9
LAST	P569	+1700-00-00T00:00:00Z/9	S2600	"6000000005609304839"
#   P570 date of death = +1766-06-02T00:00:00Z/11
LAST	P570	+1766-06-02T00:00:00Z/11	S2600	"6000000005609304839"
#   P26 spouse = Q141216627 Lars Nilsen Raunes
LAST	P26	Q141216627	S2600	"6000000005609304839"
#   Q141216627 Lars Nilsen Raunes: P26 spouse = the item just created
Q141216627	P26	LAST	S2600	"6000000005609304839"

# create a new item
CREATE
#   the item just created: set the en label to "Berta Larsdatter Stangeland"
LAST	Len	"Berta Larsdatter Stangeland"
#   set the mul label to "Berta Larsdatter Stangeland"
LAST	Lmul	"Berta Larsdatter Stangeland"
#   add a mul alias "Berta Larsdatter Øksnevad"
LAST	Amul	"Berta Larsdatter Øksnevad"
#   set the ja label to "ベルタ・ラーシュダッテル・スタンゲラン"
LAST	Lja	"ベルタ・ラーシュダッテル・スタンゲラン"
#   set the zh label to "贝尔塔·拉尔斯达特·斯坦格兰"
LAST	Lzh	"贝尔塔·拉尔斯达特·斯坦格兰"
#   add a ja alias "ベルタ・ラーシュダッテル・エクスネヴァード"
LAST	Aja	"ベルタ・ラーシュダッテル・エクスネヴァード"
#   add a zh alias "贝尔塔·拉尔斯达特·厄克斯内瓦"
LAST	Azh	"贝尔塔·拉尔斯达特·厄克斯内瓦"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000023500402302 Berta Larsdatter Stangeland, qualified P1810 subject named as Berta Larsdatter Øksnevad
LAST	P2600	"6000000023500402302"	P1810	"Berta Larsdatter Øksnevad"
#   P569 date of birth = +1815-07-30T00:00:00Z/11
LAST	P569	+1815-07-30T00:00:00Z/11	S2600	"6000000023500402302"
#   P570 date of death = +1866-08-18T00:00:00Z/11
LAST	P570	+1866-08-18T00:00:00Z/11	S2600	"6000000023500402302"
#   P26 spouse = Q141198393 Erik Erikson Stangeland
LAST	P26	Q141198393	S2600	"6000000023500402302"
#   Q141198393 Erik Erikson Stangeland: P26 spouse = the item just created
Q141198393	P26	LAST	S2600	"6000000023500402302"
#   the item just created: P735 given name = Q4092653 Berta
LAST	P735	Q4092653
#   P734 family name = Q30583490 Øksnevad, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q30583490	P3831	Q2507958
#   P734 family name = Q21452049 Stangeland, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q21452049	P3831	Q28418670
#   add a mul alias "Berta Stangeland"
LAST	Amul	"Berta Stangeland"

# create a new item
CREATE
#   set the en label to "Catharina Edenberg"
LAST	Len	"Catharina Edenberg"
#   set the mul label to "Catharina Edenberg"
LAST	Lmul	"Catharina Edenberg"
#   add a mul alias "Catharina Edenberg nr 617"
LAST	Amul	"Catharina Edenberg nr 617"
#   set the ja label to "カタリナ・エデンベルグ"
LAST	Lja	"カタリナ・エデンベルグ"
#   set the zh label to "卡塔里纳·埃德恩贝尔格"
LAST	Lzh	"卡塔里纳·埃德恩贝尔格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000012640936007 Catharina Edenberg, qualified P1810 subject named as Catharina Edenberg nr 617
LAST	P2600	"6000000012640936007"	P1810	"Catharina Edenberg nr 617"
#   P569 date of birth = +1693-04-24T00:00:00Z/11
LAST	P569	+1693-04-24T00:00:00Z/11	S2600	"6000000012640936007"
#   P570 date of death = +1765-06-23T00:00:00Z/11
LAST	P570	+1765-06-23T00:00:00Z/11	S2600	"6000000012640936007"
#   P26 spouse = Q1340357 Jakob Benzelius
LAST	P26	Q1340357	S2600	"6000000012640936007"
#   Q1340357 Jakob Benzelius: P26 spouse = the item just created
Q1340357	P26	LAST	S2600	"6000000012640936007"
#   the item just created: P735 given name = Q17317997 Catharina
LAST	P735	Q17317997

# create a new item
CREATE
#   set the en label to "Charlotta Johanna Gerner"
LAST	Len	"Charlotta Johanna Gerner"
#   set the mul label to "Charlotta Johanna Gerner"
LAST	Lmul	"Charlotta Johanna Gerner"
#   set the ja label to "カルロタ・ヨハナ・ゲルネル"
LAST	Lja	"カルロタ・ヨハナ・ゲルネル"
#   set the zh label to "卡尔洛塔·永哈纳·盖尔内尔"
LAST	Lzh	"卡尔洛塔·永哈纳·盖尔内尔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000013081666315 Charlotta Johanna Gerner, qualified P1810 subject named as Charlotta Johanna Gerner
LAST	P2600	"6000000013081666315"	P1810	"Charlotta Johanna Gerner"
#   P569 date of birth = +1728-00-00T00:00:00Z/9
LAST	P569	+1728-00-00T00:00:00Z/9	S2600	"6000000013081666315"
#   P570 date of death = +1822-05-31T00:00:00Z/11
LAST	P570	+1822-05-31T00:00:00Z/11	S2600	"6000000013081666315"
#   P26 spouse = Q719983 Johan Ihre
LAST	P26	Q719983	S2600	"6000000013081666315"
#   P40 child = Q5822415 Albrecht Ihre
LAST	P40	Q5822415	S2600	"6000000013081666315"
#   Q719983 Johan Ihre: P26 spouse = the item just created
Q719983	P26	LAST	S2600	"6000000013081666315"
#   Q5822415 Albrecht Ihre: P25 mother = the item just created
Q5822415	P25	LAST	S2600	"6000000013081666315"
#   the item just created: P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q1067071	P1545	"1"	P7452	Q3409033
#   P735 given name = Q4120836 Johanna, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q4120836	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "David Tjølson Edland"
LAST	Len	"David Tjølson Edland"
#   set the mul label to "David Tjølson Edland"
LAST	Lmul	"David Tjølson Edland"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000002690086678 David Tjølson Edland, qualified P1810 subject named as David Tjølson Edland
LAST	P2600	"6000000002690086678"	P1810	"David Tjølson Edland"
#   P569 date of birth = +1772-00-00T00:00:00Z/9
LAST	P569	+1772-00-00T00:00:00Z/9	S2600	"6000000002690086678"
#   P570 date of death = +1854-00-00T00:00:00Z/9
LAST	P570	+1854-00-00T00:00:00Z/9	S2600	"6000000002690086678"
#   P40 child = Q141216602 Berta Guria Davidsdatter Stokka
LAST	P40	Q141216602	S2600	"6000000002690086678"
#   Q141216602 Berta Guria Davidsdatter Stokka: P22 father = the item just created
Q141216602	P22	LAST	S2600	"6000000002690086678"
#   the item just created: P735 given name = Q29937870 David
LAST	P735	Q29937870
#   add a mul alias "David Edland"
LAST	Amul	"David Edland"

# create a new item
CREATE
#   set the en label to "Guri Persdatter Øksnevad"
LAST	Len	"Guri Persdatter Øksnevad"
#   set the mul label to "Guri Persdatter Øksnevad"
LAST	Lmul	"Guri Persdatter Øksnevad"
#   set the ja label to "グリ・ペシュダッテル・エクスネヴァード"
LAST	Lja	"グリ・ペシュダッテル・エクスネヴァード"
#   set the zh label to "古里·佩斯达特·厄克斯内瓦"
LAST	Lzh	"古里·佩斯达特·厄克斯内瓦"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005607155246 Guri Persdatter Øksnevad, qualified P1810 subject named as Guri Persdatter Øksnevad
LAST	P2600	"6000000005607155246"	P1810	"Guri Persdatter Øksnevad"
#   P569 date of birth = +1788-00-00T00:00:00Z/9
LAST	P569	+1788-00-00T00:00:00Z/9	S2600	"6000000005607155246"
#   P570 date of death = +1816-12-29T00:00:00Z/11
LAST	P570	+1816-12-29T00:00:00Z/11	S2600	"6000000005607155246"
#   P22 father = Q141200028 Per Jonson Øksnevad
LAST	P22	Q141200028	S2600	"6000000005607155246"
#   P25 mother = Q141199937 Maren Halvorsdatter Øksnevad
LAST	P25	Q141199937	S2600	"6000000005607155246"
#   Q141200028 Per Jonson Øksnevad: P40 child = the item just created
Q141200028	P40	LAST	S2600	"6000000005607155246"
#   Q141199937 Maren Halvorsdatter Øksnevad: P40 child = the item just created
Q141199937	P40	LAST	S2600	"6000000005607155246"
#   the item just created: P735 given name = Q11973376 Guri
LAST	P735	Q11973376
#   P734 family name = Q30583490 Øksnevad
LAST	P734	Q30583490

# create a new item
CREATE
#   set the en label to "Ivar Stokka"
LAST	Len	"Ivar Stokka"
#   set the mul label to "Ivar Stokka"
LAST	Lmul	"Ivar Stokka"
#   set the ja label to "イーヴァル・ストカ"
LAST	Lja	"イーヴァル・ストカ"
#   set the zh label to "伊瓦尔·斯托卡"
LAST	Lzh	"伊瓦尔·斯托卡"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000007980728818 Ivar Stokka, qualified P1810 subject named as Ivar Stokka
LAST	P2600	"6000000007980728818"	P1810	"Ivar Stokka"
#   P570 date of death = +1521-00-00T00:00:00Z/9
LAST	P570	+1521-00-00T00:00:00Z/9	S2600	"6000000007980728818"
#   P40 child = Q141216598 Anna Ivarsd Stokka
LAST	P40	Q141216598	S2600	"6000000007980728818"
#   Q141216598 Anna Ivarsd Stokka: P22 father = the item just created
Q141216598	P22	LAST	S2600	"6000000007980728818"
#   the item just created: P735 given name = Q127069 Ivar
LAST	P735	Q127069

# create a new item
CREATE
#   set the en label to "Johan Johannessen Obrestad"
LAST	Len	"Johan Johannessen Obrestad"
#   set the mul label to "Johan Johannessen Obrestad"
LAST	Lmul	"Johan Johannessen Obrestad"
#   set the ja label to "ヨハン・ヨハンネセン・オブレスタド"
LAST	Lja	"ヨハン・ヨハンネセン・オブレスタド"
#   set the zh label to "永哈恩·约翰内森·奥布雷斯塔德"
LAST	Lzh	"永哈恩·约翰内森·奥布雷斯塔德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000206974233871 Johan Johannessen Obrestad, qualified P1810 subject named as Johan Johannessen Obrestad
LAST	P2600	"6000000206974233871"	P1810	"Johan Johannessen Obrestad"
#   P569 date of birth = +1863-06-12T00:00:00Z/11
LAST	P569	+1863-06-12T00:00:00Z/11	S2600	"6000000206974233871"
#   P22 father = Q141216387 Johannes Svensen Obrestad
LAST	P22	Q141216387	S2600	"6000000206974233871"
#   P25 mother = Q141216363 Anne Govertsdtr. Bratland
LAST	P25	Q141216363	S2600	"6000000206974233871"
#   Q141216387 Johannes Svensen Obrestad: P40 child = the item just created
Q141216387	P40	LAST	S2600	"6000000206974233871"
#   Q141216363 Anne Govertsdtr. Bratland: P40 child = the item just created
Q141216363	P40	LAST	S2600	"6000000206974233871"
#   the item just created: P735 given name = Q10989273 Johan
LAST	P735	Q10989273

# create a new item
CREATE
#   set the en label to "Kristine Sørensdatter Gjesdal"
LAST	Len	"Kristine Sørensdatter Gjesdal"
#   set the mul label to "Kristine Sørensdatter Gjesdal"
LAST	Lmul	"Kristine Sørensdatter Gjesdal"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005607335630 Kristine Sørensdatter Gjesdal, qualified P1810 subject named as Kristine Sørensdatter Gjesdal
LAST	P2600	"6000000005607335630"	P1810	"Kristine Sørensdatter Gjesdal"
#   P569 date of birth = +1782-00-00T00:00:00Z/9
LAST	P569	+1782-00-00T00:00:00Z/9	S2600	"6000000005607335630"
#   P570 date of death = +1867-00-00T00:00:00Z/9
LAST	P570	+1867-00-00T00:00:00Z/9	S2600	"6000000005607335630"
#   P40 child = Q141216602 Berta Guria Davidsdatter Stokka
LAST	P40	Q141216602	S2600	"6000000005607335630"
#   Q141216602 Berta Guria Davidsdatter Stokka: P25 mother = the item just created
Q141216602	P25	LAST	S2600	"6000000005607335630"
#   the item just created: P735 given name = Q16859157 Kristine
LAST	P735	Q16859157
#   P734 family name = Q27888954 Gjesdal
LAST	P734	Q27888954

# create a new item
CREATE
#   set the en label to "Larine Eriksdatter Heigre"
LAST	Len	"Larine Eriksdatter Heigre"
#   set the mul label to "Larine Eriksdatter Heigre"
LAST	Lmul	"Larine Eriksdatter Heigre"
#   add a mul alias "Larine Eriksdatter Stangeland"
LAST	Amul	"Larine Eriksdatter Stangeland"
#   set the ja label to "ラリネ・エリクスダッテル・ヘイグレ"
LAST	Lja	"ラリネ・エリクスダッテル・ヘイグレ"
#   set the zh label to "拉里内·埃里克斯达特·海格勒"
LAST	Lzh	"拉里内·埃里克斯达特·海格勒"
#   add a ja alias "ラリネ・エリクスダッテル・スタンゲラン"
LAST	Aja	"ラリネ・エリクスダッテル・スタンゲラン"
#   add a zh alias "拉里内·埃里克斯达特·斯坦格兰"
LAST	Azh	"拉里内·埃里克斯达特·斯坦格兰"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000201256773828 Larine Eriksdatter Heigre, qualified P1810 subject named as Larine Eriksdatter Stangeland
LAST	P2600	"6000000201256773828"	P1810	"Larine Eriksdatter Stangeland"
#   P569 date of birth = +1848-04-18T00:00:00Z/11
LAST	P569	+1848-04-18T00:00:00Z/11	S2600	"6000000201256773828"
#   P22 father = Q141198393 Erik Erikson Stangeland
LAST	P22	Q141198393	S2600	"6000000201256773828"
#   Q141198393 Erik Erikson Stangeland: P40 child = the item just created
Q141198393	P40	LAST	S2600	"6000000201256773828"
#   the item just created: P734 family name = Q21452049 Stangeland, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q21452049	P3831	Q2507958
#   add a mul alias "Larine Heigre"
LAST	Amul	"Larine Heigre"

# create a new item
CREATE
#   set the en label to "Magdalena von Mentzer"
LAST	Len	"Magdalena von Mentzer"
#   set the mul label to "Magdalena von Mentzer"
LAST	Lmul	"Magdalena von Mentzer"
#   set the ja label to "マグダレーナ・ヴォン・メントゼル"
LAST	Lja	"マグダレーナ・ヴォン・メントゼル"
#   set the zh label to "玛格达莱娜·沃恩·梅恩特泽尔"
LAST	Lzh	"玛格达莱娜·沃恩·梅恩特泽尔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000012617083513 Magdalena von Mentzer, qualified P1810 subject named as Magdalena von Mentzer
LAST	P2600	"6000000012617083513"	P1810	"Magdalena von Mentzer"
#   P569 date of birth = +1726-10-15T00:00:00Z/11
LAST	P569	+1726-10-15T00:00:00Z/11	S2600	"6000000012617083513"
#   P570 date of death = +1809-02-06T00:00:00Z/11
LAST	P570	+1809-02-06T00:00:00Z/11	S2600	"6000000012617083513"
#   P26 spouse = Q6082455 Thure Gustaf Rudbeck
LAST	P26	Q6082455	S2600	"6000000012617083513"
#   Q6082455 Thure Gustaf Rudbeck: P26 spouse = the item just created
Q6082455	P26	LAST	S2600	"6000000012617083513"
#   the item just created: P735 given name = Q842544 Magdalena
LAST	P735	Q842544

# create a new item
CREATE
#   set the en label to "Margareta Christina von Numers"
LAST	Len	"Margareta Christina von Numers"
#   set the mul label to "Margareta Christina von Numers"
LAST	Lmul	"Margareta Christina von Numers"
#   set the ja label to "マルガレータ・クリスティナ・ヴォン・ヌメルス"
LAST	Lja	"マルガレータ・クリスティナ・ヴォン・ヌメルス"
#   set the zh label to "玛格丽塔·克里斯蒂纳·沃恩·努梅尔斯"
LAST	Lzh	"玛格丽塔·克里斯蒂纳·沃恩·努梅尔斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000008391104730 Margareta Christina von Numers, qualified P1810 subject named as Margareta Christina von Numers
LAST	P2600	"6000000008391104730"	P1810	"Margareta Christina von Numers"
#   P569 date of birth = +1694-08-13T00:00:00Z/11
LAST	P569	+1694-08-13T00:00:00Z/11	S2600	"6000000008391104730"
#   P570 date of death = +1781-02-15T00:00:00Z/11
LAST	P570	+1781-02-15T00:00:00Z/11	S2600	"6000000008391104730"
#   P26 spouse = Q5562579 Magnus Petri Aurivillius
LAST	P26	Q5562579	S2600	"6000000008391104730"
#   P40 child = Q5562598 Samuel Aurivillius
LAST	P40	Q5562598	S2600	"6000000008391104730"
#   P40 child = Q1527696 Carl Aurivillius
LAST	P40	Q1527696	S2600	"6000000008391104730"
#   Q5562579 Magnus Petri Aurivillius: P26 spouse = the item just created
Q5562579	P26	LAST	S2600	"6000000008391104730"
#   Q5562598 Samuel Aurivillius: P25 mother = the item just created
Q5562598	P25	LAST	S2600	"6000000008391104730"
#   Q1527696 Carl Aurivillius: P25 mother = the item just created
Q1527696	P25	LAST	S2600	"6000000008391104730"
#   the item just created: P735 given name = Q8274988 Margareta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q8274988	P1545	"1"	P7452	Q3409033

# create a new item
CREATE
#   set the en label to "Maria No name"
LAST	Len	"Maria No name"
#   set the mul label to "Maria No name"
LAST	Lmul	"Maria No name"
#   set the ja label to "マリア・ノ・ナメ"
LAST	Lja	"マリア・ノ・ナメ"
#   set the zh label to "马里阿·诺·纳梅"
LAST	Lzh	"马里阿·诺·纳梅"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000027470028034 Maria No name, qualified P1810 subject named as Maria No name
LAST	P2600	"6000000027470028034"	P1810	"Maria No name"
#   P40 child = Q141205917 Kerstin Månsdotter
LAST	P40	Q141205917	S2600	"6000000027470028034"
#   Q141205917 Kerstin Månsdotter: P25 mother = the item just created
Q141205917	P25	LAST	S2600	"6000000027470028034"

# create a new item
CREATE
#   the item just created: set the en label to "Måns Moge"
LAST	Len	"Måns Moge"
#   set the mul label to "Måns Moge"
LAST	Lmul	"Måns Moge"
#   set the ja label to "モーンス・モゲ"
LAST	Lja	"モーンス・モゲ"
#   set the zh label to "莫恩斯·莫盖"
LAST	Lzh	"莫恩斯·莫盖"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000027469942604 Måns Moge, qualified P1810 subject named as Måns Moge
LAST	P2600	"6000000027469942604"	P1810	"Måns Moge"
#   P40 child = Q141205917 Kerstin Månsdotter
LAST	P40	Q141205917	S2600	"6000000027469942604"
#   Q141205917 Kerstin Månsdotter: P22 father = the item just created
Q141205917	P22	LAST	S2600	"6000000027469942604"
#   the item just created: P735 given name = Q19799975 Måns
LAST	P735	Q19799975

# create a new item
CREATE
#   set the en label to "Nils Albrektsson"
LAST	Len	"Nils Albrektsson"
#   set the mul label to "Nils Albrektsson"
LAST	Lmul	"Nils Albrektsson"
#   set the ja label to "ニルス・アルブレクトソン"
LAST	Lja	"ニルス・アルブレクトソン"
#   set the zh label to "尼尔斯·阿尔布雷克特松"
LAST	Lzh	"尼尔斯·阿尔布雷克特松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 375732740000012611 Nils Albrektsson, qualified P1810 subject named as Nils Albrektsson
LAST	P2600	"375732740000012611"	P1810	"Nils Albrektsson"
#   P569 date of birth = +1505-00-00T00:00:00Z/9
LAST	P569	+1505-00-00T00:00:00Z/9	S2600	"375732740000012611"
#   P570 date of death = +1573-00-00T00:00:00Z/9
LAST	P570	+1573-00-00T00:00:00Z/9	S2600	"375732740000012611"
#   P26 spouse = Q141216605 Gunilla Jonsdotter
LAST	P26	Q141216605	S2600	"375732740000012611"
#   P40 child = Q141216403 Olof Nilsson
LAST	P40	Q141216403	S2600	"375732740000012611"
#   Q141216605 Gunilla Jonsdotter: P26 spouse = the item just created
Q141216605	P26	LAST	S2600	"375732740000012611"
#   Q141216403 Olof Nilsson: P22 father = the item just created
Q141216403	P22	LAST	S2600	"375732740000012611"
#   the item just created: P735 given name = Q16423038 Nils
LAST	P735	Q16423038

# create a new item
CREATE
#   set the en label to "Osmund Larsen Raunes"
LAST	Len	"Osmund Larsen Raunes"
#   set the mul label to "Osmund Larsen Raunes"
LAST	Lmul	"Osmund Larsen Raunes"
#   set the ja label to "オスムンド・ラーシェン・ラウネス"
LAST	Lja	"オスムンド・ラーシェン・ラウネス"
#   set the zh label to "奥斯穆恩德·拉尔森·拉乌内斯"
LAST	Lzh	"奥斯穆恩德·拉尔森·拉乌内斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000012587690898 Osmund Larsen Raunes, qualified P1810 subject named as Osmund Larsen Raunes
LAST	P2600	"6000000012587690898"	P1810	"Osmund Larsen Raunes"
#   P569 date of birth = +1730-00-00T00:00:00Z/9
LAST	P569	+1730-00-00T00:00:00Z/9	S2600	"6000000012587690898"
#   P570 date of death = +1766-00-00T00:00:00Z/9
LAST	P570	+1766-00-00T00:00:00Z/9	S2600	"6000000012587690898"
#   P22 father = Q141216627 Lars Nilsen Raunes
LAST	P22	Q141216627	S2600	"6000000012587690898"
#   Q141216627 Lars Nilsen Raunes: P40 child = the item just created
Q141216627	P40	LAST	S2600	"6000000012587690898"
#   the item just created: P735 given name = Q7107242 Osmund
LAST	P735	Q7107242
#   P1449 nickname = en:"Lars Foss-Eikeland"
LAST	P1449	en:"Lars Foss-Eikeland"
#   add a mul alias "Lars Foss-Eikeland Raunes"
LAST	Amul	"Lars Foss-Eikeland Raunes"

# create a new item
CREATE
#   set the en label to "Ottiliana Vilhelmina Conradsdotter Transchiöld"
LAST	Len	"Ottiliana Vilhelmina Conradsdotter Transchiöld"
#   set the mul label to "Ottiliana Vilhelmina Conradsdotter Transchiöld"
LAST	Lmul	"Ottiliana Vilhelmina Conradsdotter Transchiöld"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000013400386736 Ottiliana Vilhelmina Conradsdotter Transchiöld, qualified P1810 subject named as Ottiliana Vilhelmina Conradsdotter Transchiöld
LAST	P2600	"6000000013400386736"	P1810	"Ottiliana Vilhelmina Conradsdotter Transchiöld"
#   P569 date of birth = +1741-01-30T00:00:00Z/11
LAST	P569	+1741-01-30T00:00:00Z/11	S2600	"6000000013400386736"
#   P570 date of death = +1788-08-12T00:00:00Z/11
LAST	P570	+1788-08-12T00:00:00Z/11	S2600	"6000000013400386736"
#   P26 spouse = Q5951779 Johan Liljencrantz
LAST	P26	Q5951779	S2600	"6000000013400386736"
#   P40 child = Q5951795 Johan Wilhelm Johansson Liljencrantz
LAST	P40	Q5951795	S2600	"6000000013400386736"
#   Q5951779 Johan Liljencrantz: P26 spouse = the item just created
Q5951779	P26	LAST	S2600	"6000000013400386736"
#   Q5951795 Johan Wilhelm Johansson Liljencrantz: P25 mother = the item just created
Q5951795	P25	LAST	S2600	"6000000013400386736"
#   the item just created: P735 given name = Q15711317 Vilhelmina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q15711317	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Per Andersson Storskytt"
LAST	Len	"Per Andersson Storskytt"
#   set the mul label to "Per Andersson Storskytt"
LAST	Lmul	"Per Andersson Storskytt"
#   add a mul alias "Per Andersson"
LAST	Amul	"Per Andersson"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000011078829655 Per Andersson Storskytt, qualified P1810 subject named as Per Andersson
LAST	P2600	"6000000011078829655"	P1810	"Per Andersson"
#   P569 date of birth = +1720-00-00T00:00:00Z/9
LAST	P569	+1720-00-00T00:00:00Z/9	S2600	"6000000011078829655"
#   P570 date of death = +1802-05-24T00:00:00Z/11
LAST	P570	+1802-05-24T00:00:00Z/11	S2600	"6000000011078829655"
#   P26 spouse = Q141216595 Anna Danielsdotter
LAST	P26	Q141216595	S2600	"6000000011078829655"
#   Q141216595 Anna Danielsdotter: P26 spouse = the item just created
Q141216595	P26	LAST	S2600	"6000000011078829655"
#   the item just created: P735 given name = Q13582800 Per
LAST	P735	Q13582800
#   P734 family name = Q2817217 Andersson
LAST	P734	Q2817217

# create a new item
CREATE
#   set the en label to "Per Persson Hagman"
LAST	Len	"Per Persson Hagman"
#   set the mul label to "Per Persson Hagman"
LAST	Lmul	"Per Persson Hagman"
#   add a mul alias "Per Persson"
LAST	Amul	"Per Persson"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000011078726908 Per Persson Hagman, qualified P1810 subject named as Per Persson
LAST	P2600	"6000000011078726908"	P1810	"Per Persson"
#   P569 date of birth = +1754-09-24T00:00:00Z/11
LAST	P569	+1754-09-24T00:00:00Z/11	S2600	"6000000011078726908"
#   P570 date of death = +1840-08-18T00:00:00Z/11
LAST	P570	+1840-08-18T00:00:00Z/11	S2600	"6000000011078726908"
#   P25 mother = Q141216595 Anna Danielsdotter
LAST	P25	Q141216595	S2600	"6000000011078726908"
#   Q141216595 Anna Danielsdotter: P40 child = the item just created
Q141216595	P40	LAST	S2600	"6000000011078726908"
#   the item just created: P735 given name = Q13582800 Per
LAST	P735	Q13582800
#   P734 family name = Q27876648 Persson
LAST	P734	Q27876648

# create a new item
CREATE
#   set the en label to "Sissel Sæbjørnsdatter Talgje"
LAST	Len	"Sissel Sæbjørnsdatter Talgje"
#   set the mul label to "Sissel Sæbjørnsdatter Talgje"
LAST	Lmul	"Sissel Sæbjørnsdatter Talgje"
#   set the ja label to "シセル・セブヨルンスダッテル・タルイェ"
LAST	Lja	"シセル・セブヨルンスダッテル・タルイェ"
#   set the zh label to "西塞尔·塞布永尔恩斯达特·塔尔耶"
LAST	Lzh	"西塞尔·塞布永尔恩斯达特·塔尔耶"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000004214055821 Sissel Sæbjørnsdatter Talgje, qualified P1810 subject named as Sissel Sæbjørnsdatter Talgje
LAST	P2600	"6000000004214055821"	P1810	"Sissel Sæbjørnsdatter Talgje"
#   P569 date of birth = +1540-00-00T00:00:00Z/9
LAST	P569	+1540-00-00T00:00:00Z/9	S2600	"6000000004214055821"
#   P570 date of death = +1614-00-00T00:00:00Z/9
LAST	P570	+1614-00-00T00:00:00Z/9	S2600	"6000000004214055821"
#   P22 father = Q141200111 Sæbjørn Toresson Talgje
LAST	P22	Q141200111	S2600	"6000000004214055821"
#   P25 mother = Q141200101 Sissel Jonsdatter Talje
LAST	P25	Q141200101	S2600	"6000000004214055821"
#   Q141200111 Sæbjørn Toresson Talgje: P40 child = the item just created
Q141200111	P40	LAST	S2600	"6000000004214055821"
#   Q141200101 Sissel Jonsdatter Talje: P40 child = the item just created
Q141200101	P40	LAST	S2600	"6000000004214055821"
#   the item just created: P735 given name = Q4571101 Sissel
LAST	P735	Q4571101
#   Q141216618 Karin Olofsdotter: P3373 sibling = Q141205931 Olof Olofsson
Q141216618	P3373	Q141205931	S2600	"348968026630001429"
#   Q141216611 Jon Villumson Raunes: P26 spouse = Q141216632 Magdalena Lauritsd Hogganvik
Q141216611	P26	Q141216632	S2600	"6000000001169146145"
#   Q141216602 Berta Guria Davidsdatter Stokka: P26 spouse = Q141216653 Torger Torgerson Stokka
Q141216602	P26	Q141216653	S2600	"6000000002726900648"
#   Q141216653 Torger Torgerson Stokka: P26 spouse = Q141216602 Berta Guria Davidsdatter Stokka
Q141216653	P26	Q141216602	S2600	"6000000002726968193"
#   Q141199819 Anna Andersdotter: P40 child = Q141199734 Nils Andersson
Q141199819	P40	Q141199734	S2600	"6000000003125438035"
#   Q141216644 Rasmus Asbjørnson Nedre Rossavik: P40 child = Q141216599 Anna Rasmusdatter Nedre Rossavik
Q141216644	P40	Q141216599	S2600	"6000000003192698959"
#   Q141216638 Olaug Jonsdatter Heigre: P26 spouse = Q141216637 Ola Person Persson Heigre
Q141216638	P26	Q141216637	S2600	"6000000003491933401"
#   Q141216637 Ola Person Persson Heigre: P26 spouse = Q141216638 Olaug Jonsdatter Heigre
Q141216637	P26	Q141216638	S2600	"6000000003491947917"
#   Q141216635 Martha Eivindsdatter Heigre: P40 child = Q141216643 Ragna Enevaldsdatter Heigre
Q141216635	P40	Q141216643	S2600	"6000000003491988061"
#   Q141216643 Ragna Enevaldsdatter Heigre: P25 mother = Q141216635 Martha Eivindsdatter Heigre
Q141216643	P25	Q141216635	S2600	"6000000003491988081"
#   Q141216632 Magdalena Lauritsd Hogganvik: P26 spouse = Q141216611 Jon Villumson Raunes
Q141216632	P26	Q141216611	S2600	"6000000005607268671"
#   Q141216613 Karen Henriksdotter Raunes Våga: P40 child = Q141216627 Lars Nilsen Raunes
Q141216613	P40	Q141216627	S2600	"6000000005607377021"
#   Q141216627 Lars Nilsen Raunes: P25 mother = Q141216613 Karen Henriksdotter Raunes Våga
Q141216627	P25	Q141216613	S2600	"6000000005609304829"
#   Q141216645 Reiar Reiersen Kydland: P26 spouse = Q141216609 Inger Kristoffersdatter Skårland
Q141216645	P26	Q141216609	S2600	"6000000005609534659"
#   Q141216609 Inger Kristoffersdatter Skårland: P26 spouse = Q141216645 Reiar Reiersen Kydland
Q141216609	P26	Q141216645	S2600	"6000000005609534669"
#   Q141216599 Anna Rasmusdatter Nedre Rossavik: P22 father = Q141216644 Rasmus Asbjørnson Nedre Rossavik
Q141216599	P22	Q141216644	S2600	"6000000008916446714"
#   Q141216633 Malin Jacobsdotter: P40 child = Q141216595 Anna Danielsdotter
Q141216633	P40	Q141216595	S2600	"6000000011078760054"
#   Q141216595 Anna Danielsdotter: P25 mother = Q141216633 Malin Jacobsdotter
Q141216595	P25	Q141216633	S2600	"6000000011078918407"
#   P5056 patronym or matronym = Q140226461, qualified P144 based on Q141216461 Daniel Andersson
Q141216595	P5056	Q140226461	P144	Q141216461
#   Q141216639 Olufine Bergithe Ekman: P26 spouse = Q141216640 Per Gustaf Ekman
Q141216639	P26	Q141216640	S2600	"6000000014196479728"
#   Q141216640 Per Gustaf Ekman: P26 spouse = Q141216639 Olufine Bergithe Ekman
Q141216640	P26	Q141216639	S2600	"6000000032811550619"
#   Q141200083 Sara NN: P26 spouse = Q141199734 Nils Andersson
Q141200083	P26	Q141199734	S2600	"6000000059888596942"

