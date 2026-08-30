# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   1006 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   Q141219065 Marta Torbjørnsdotter Gjesdal: set the zh label to "玛尔塔·托尔布约尔恩斯多特·耶斯达尔"
Q141219065	Lzh	"玛尔塔·托尔布约尔恩斯多特·耶斯达尔"
#   Q141216460 Bjørnsdatter Tau: set the zh label to "布约尔恩斯达特·塔乌"
Q141216460	Lzh	"布约尔恩斯达特·塔乌"
#   Q141216613 Karen Henriksdotter Raunes Våga: set the ja label to "カレン・ヘンリクスドッテル・ラウネス・ヴォーガ"
Q141216613	Lja	"カレン・ヘンリクスドッテル・ラウネス・ヴォーガ"
#   set the zh label to "凯伦·亨里克斯多特·拉乌内斯·沃加"
Q141216613	Lzh	"凯伦·亨里克斯多特·拉乌内斯·沃加"
#   Q141216384 Ingeborg Eriksdatter Time: set the zh label to "英格堡·埃里克斯达特·蒂梅"
Q141216384	Lzh	"英格堡·埃里克斯达特·蒂梅"
#   Q11959067 Arne Olaus Fjørtoft Garborg: set the ja label to "アルネ・オラウス・フョルトフト・ガルボルグ"
Q11959067	Lja	"アルネ・オラウス・フョルトフト・ガルボルグ"
#   set the zh label to "阿恩·奥劳斯·夫约托夫特·加尔博格"
Q11959067	Lzh	"阿恩·奥劳斯·夫约托夫特·加尔博格"
#   Q141219291 Maria Hansdatter Austrått: set the zh label to "玛丽亚·汉斯达特·奥斯特罗特"
Q141219291	Lzh	"玛丽亚·汉斯达特·奥斯特罗特"
#   Q141223436 Tore Underberge III: add a mul alias "Tore Underberge, III"
Q141223436	Amul	"Tore Underberge, III"
#   Q141205919 Malena Hansdatter Bø: add a mul alias "Malena Hansdatter Risa"
Q141205919	Amul	"Malena Hansdatter Risa"
#   set the ja label to "マレーナ・ハンスダッテル・ベー"
Q141205919	Lja	"マレーナ・ハンスダッテル・ベー"
#   set the zh label to "马莱纳·汉斯达特·鲍伊"
Q141205919	Lzh	"马莱纳·汉斯达特·鲍伊"
#   Q141216388 Jon Hansson St. Vatne: set the ja label to "ジョン・ハンソン・スト・ヴァトネ"
Q141216388	Lja	"ジョン・ハンソン・スト・ヴァトネ"
#   set the zh label to "乔恩·汉松·斯特·瓦特内"
Q141216388	Lzh	"乔恩·汉松·斯特·瓦特内"
#   Q141198832 Lars Gunnbjørnsen Mjølhus: set the ja label to "ラース・グンンブヨルンセン・ムヨルフス"
Q141198832	Lja	"ラース・グンンブヨルンセン・ムヨルフス"

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Bellest Bellestsen Lauvsnes d.e."
LAST	Len	"Bellest Bellestsen Lauvsnes d.e."
#   set the mul label to "Bellest Bellestsen Lauvsnes d.e."
LAST	Lmul	"Bellest Bellestsen Lauvsnes d.e."
#   set the ja label to "ベレスト・ベレストセン・ラウヴスネス・ドエ"
LAST	Lja	"ベレスト・ベレストセン・ラウヴスネス・ドエ"
#   set the zh label to "贝莱斯特·贝莱斯特森·拉乌夫斯内斯·德埃"
LAST	Lzh	"贝莱斯特·贝莱斯特森·拉乌夫斯内斯·德埃"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005608905668 Bellest Bellestsen Lauvsnes d.e., qualified P1810 subject named as Bellest Bellestsen Lauvsnes d.e.
LAST	P2600	"6000000005608905668"	P1810	"Bellest Bellestsen Lauvsnes d.e."
#   P569 date of birth = +1640-00-00T00:00:00Z/9
LAST	P569	+1640-00-00T00:00:00Z/9	S2600	"6000000005608905668"
#   P570 date of death = +1710-00-00T00:00:00Z/9
LAST	P570	+1710-00-00T00:00:00Z/9	S2600	"6000000005608905668"
#   P40 child = Q141198371 Anna Belestdatter Lauvsnes
LAST	P40	Q141198371	S2600	"6000000005608905668"
#   Q141198371 Anna Belestdatter Lauvsnes: P22 father = the item just created
Q141198371	P22	LAST	S2600	"6000000005608905668"

# create a new item
CREATE
#   the item just created: set the en label to "Berta Serina Rasmusdatter Borsheim"
LAST	Len	"Berta Serina Rasmusdatter Borsheim"
#   set the mul label to "Berta Serina Rasmusdatter Borsheim"
LAST	Lmul	"Berta Serina Rasmusdatter Borsheim"
#   set the ja label to "ベルタ・セリナ・ラスムスダッテル・ボルスハイム"
LAST	Lja	"ベルタ・セリナ・ラスムスダッテル・ボルスハイム"
#   set the zh label to "贝尔塔·塞里纳·拉斯穆斯达特·博尔斯海姆"
LAST	Lzh	"贝尔塔·塞里纳·拉斯穆斯达特·博尔斯海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000014522158621 Berta Serina Rasmusdatter Borsheim, qualified P1810 subject named as Berta Serina Rasmusdatter Borsheim
LAST	P2600	"6000000014522158621"	P1810	"Berta Serina Rasmusdatter Borsheim"
#   P569 date of birth = +1825-03-16T00:00:00Z/11
LAST	P569	+1825-03-16T00:00:00Z/11	S2600	"6000000014522158621"
#   P570 date of death = +1867-08-01T00:00:00Z/11
LAST	P570	+1867-08-01T00:00:00Z/11	S2600	"6000000014522158621"
#   P40 child = Q141223944 Rasmus (Paulson) Borsheim
LAST	P40	Q141223944	S2600	"6000000014522158621"
#   Q141223944 Rasmus (Paulson) Borsheim: P25 mother = the item just created
Q141223944	P25	LAST	S2600	"6000000014522158621"

# create a new item
CREATE
#   the item just created: set the en label to "Carl Benzelstierna"
LAST	Len	"Carl Benzelstierna"
#   set the mul label to "Carl Benzelstierna"
LAST	Lmul	"Carl Benzelstierna"
#   set the ja label to "カール・ベンゼルスティエルナ"
LAST	Lja	"カール・ベンゼルスティエルナ"
#   set the zh label to "卡尔·本泽尔斯蒂埃尔纳"
LAST	Lzh	"卡尔·本泽尔斯蒂埃尔纳"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000008659181816 Carl Benzelstierna, qualified P1810 subject named as Carl Benzelstierna
LAST	P2600	"6000000008659181816"	P1810	"Carl Benzelstierna"
#   P569 date of birth = +1723-10-18T00:00:00Z/11
LAST	P569	+1723-10-18T00:00:00Z/11	S2600	"6000000008659181816"
#   P570 date of death = +1808-04-03T00:00:00Z/11
LAST	P570	+1808-04-03T00:00:00Z/11	S2600	"6000000008659181816"
#   P22 father = Q5570928 Lars Benzelstierna
LAST	P22	Q5570928	S2600	"6000000008659181816"
#   P25 mother = Q141223425 Hedvig Swedenborg
LAST	P25	Q141223425	S2600	"6000000008659181816"
#   Q5570928 Lars Benzelstierna: P40 child = the item just created
Q5570928	P40	LAST	S2600	"6000000008659181816"
#   Q141223425 Hedvig Swedenborg: P40 child = the item just created
Q141223425	P40	LAST	S2600	"6000000008659181816"
#   the item just created: P735 given name = Q2529610 Carl
LAST	P735	Q2529610

# create a new item
CREATE
#   set the en label to "Helena Mikontytär Schulin"
LAST	Len	"Helena Mikontytär Schulin"
#   set the mul label to "Helena Mikontytär Schulin"
LAST	Lmul	"Helena Mikontytär Schulin"
#   set the ja label to "ヘレナ・ミコンティテル・シュリン"
LAST	Lja	"ヘレナ・ミコンティテル・シュリン"
#   set the zh label to "海伦娜·米孔蒂特尔·舒林"
LAST	Lzh	"海伦娜·米孔蒂特尔·舒林"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000000325079856 Helena Mikontytär Schulin, qualified P1810 subject named as Helena Mikontytär Schulin
LAST	P2600	"6000000000325079856"	P1810	"Helena Mikontytär Schulin"
#   P569 date of birth = +1755-10-05T00:00:00Z/11
LAST	P569	+1755-10-05T00:00:00Z/11	S2600	"6000000000325079856"
#   P570 date of death = +1811-05-03T00:00:00Z/11
LAST	P570	+1811-05-03T00:00:00Z/11	S2600	"6000000000325079856"
#   P26 spouse = Q141224376 Zacharias Fransson Franzén
LAST	P26	Q141224376	S2600	"6000000000325079856"
#   P40 child = Q333297 Frans Michael Zachrichsson Franzén
LAST	P40	Q333297	S2600	"6000000000325079856"
#   Q141224376 Zacharias Fransson Franzén: P26 spouse = the item just created
Q141224376	P26	LAST	S2600	"6000000000325079856"
#   Q333297 Frans Michael Zachrichsson Franzén: P25 mother = the item just created
Q333297	P25	LAST	S2600	"6000000000325079856"
#   the item just created: P735 given name = Q1035239 Helena, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q1035239	P1545	"1"	P7452	Q3409033

# create a new item
CREATE
#   set the en label to "Johan Falkenberg af Trystorp"
LAST	Len	"Johan Falkenberg af Trystorp"
#   set the mul label to "Johan Falkenberg af Trystorp"
LAST	Lmul	"Johan Falkenberg af Trystorp"
#   add a mul alias "Johan von Mentzer"
LAST	Amul	"Johan von Mentzer"
#   set the ja label to "ヨハン・ファルケンベルグ・アフ・トリストルプ"
LAST	Lja	"ヨハン・ファルケンベルグ・アフ・トリストルプ"
#   set the zh label to "约翰·法尔肯贝尔格·阿夫·特里斯托尔普"
LAST	Lzh	"约翰·法尔肯贝尔格·阿夫·特里斯托尔普"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 388325917570007375 Johan Falkenberg af Trystorp, qualified P1810 subject named as Johan von Mentzer
LAST	P2600	"388325917570007375"	P1810	"Johan von Mentzer"
#   P569 date of birth = +1670-09-15T00:00:00Z/11
LAST	P569	+1670-09-15T00:00:00Z/11	S2600	"388325917570007375"
#   P570 date of death = +1747-05-01T00:00:00Z/11
LAST	P570	+1747-05-01T00:00:00Z/11	S2600	"388325917570007375"
#   P26 spouse = Q141224102 Catharina Charlotta Falkenberg af Trystorp
LAST	P26	Q141224102	S2600	"388325917570007375"
#   P40 child = Q141217393 Magdalena von Mentzer
LAST	P40	Q141217393	S2600	"388325917570007375"
#   Q141224102 Catharina Charlotta Falkenberg af Trystorp: P26 spouse = the item just created
Q141224102	P26	LAST	S2600	"388325917570007375"
#   Q141217393 Magdalena von Mentzer: P22 father = the item just created
Q141217393	P22	LAST	S2600	"388325917570007375"
#   the item just created: P735 given name = Q10989273 Johan
LAST	P735	Q10989273
#   P734 family name = Q16869887 Falkenberg
LAST	P734	Q16869887

# create a new item
CREATE
#   set the en label to "Jon Olsen Trevland"
LAST	Len	"Jon Olsen Trevland"
#   set the mul label to "Jon Olsen Trevland"
LAST	Lmul	"Jon Olsen Trevland"
#   set the ja label to "ジョン・オルセン・トレヴランド"
LAST	Lja	"ジョン・オルセン・トレヴランド"
#   set the zh label to "乔恩·奥尔森·特雷夫兰德"
LAST	Lzh	"乔恩·奥尔森·特雷夫兰德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000226904750852 Jon Olsen Trevland, qualified P1810 subject named as Jon Olsen Trevland
LAST	P2600	"6000000226904750852"	P1810	"Jon Olsen Trevland"
#   P569 date of birth = +1540-00-00T00:00:00Z/9
LAST	P569	+1540-00-00T00:00:00Z/9	S2600	"6000000226904750852"
#   P570 date of death = +1631-00-00T00:00:00Z/9
LAST	P570	+1631-00-00T00:00:00Z/9	S2600	"6000000226904750852"
#   P22 father = Q141223431 Ola Taraldsen Trevland
LAST	P22	Q141223431	S2600	"6000000226904750852"
#   Q141223431 Ola Taraldsen Trevland: P40 child = the item just created
Q141223431	P40	LAST	S2600	"6000000226904750852"
#   the item just created: P735 given name = Q13501137 Jon
LAST	P735	Q13501137
#   add a mul alias "Jon Trevland"
LAST	Amul	"Jon Trevland"

# create a new item
CREATE
#   set the en label to "Malena Henriksdatter Lauvsnes"
LAST	Len	"Malena Henriksdatter Lauvsnes"
#   set the mul label to "Malena Henriksdatter Lauvsnes"
LAST	Lmul	"Malena Henriksdatter Lauvsnes"
#   add a mul alias "Malena Henriksdatter Steinnes"
LAST	Amul	"Malena Henriksdatter Steinnes"
#   set the ja label to "マレーナ・ヘンリクスダッテル・ラウヴスネス"
LAST	Lja	"マレーナ・ヘンリクスダッテル・ラウヴスネス"
#   set the zh label to "马莱纳·亨里克斯达特·拉乌夫斯内斯"
LAST	Lzh	"马莱纳·亨里克斯达特·拉乌夫斯内斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000008686123375 Malena Henriksdatter Lauvsnes, qualified P1810 subject named as Malena Henriksdatter Steinnes
LAST	P2600	"6000000008686123375"	P1810	"Malena Henriksdatter Steinnes"
#   P569 date of birth = +1645-00-00T00:00:00Z/9
LAST	P569	+1645-00-00T00:00:00Z/9	S2600	"6000000008686123375"
#   P40 child = Q141198371 Anna Belestdatter Lauvsnes
LAST	P40	Q141198371	S2600	"6000000008686123375"
#   Q141198371 Anna Belestdatter Lauvsnes: P25 mother = the item just created
Q141198371	P25	LAST	S2600	"6000000008686123375"
#   the item just created: P735 given name = Q5990536 Malena
LAST	P735	Q5990536
#   P734 family name = Q27892767 Steinnes, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q27892767	P3831	Q2507958
#   add a mul alias "Malena Lauvsnes"
LAST	Amul	"Malena Lauvsnes"

# create a new item
CREATE
#   set the en label to "Margareta Olausdotter Plantin"
LAST	Len	"Margareta Olausdotter Plantin"
#   set the mul label to "Margareta Olausdotter Plantin"
LAST	Lmul	"Margareta Olausdotter Plantin"
#   set the ja label to "マルガレータ・オーラウスドッテル・プランティン"
LAST	Lja	"マルガレータ・オーラウスドッテル・プランティン"
#   set the zh label to "瑪格麗塔·奥劳斯多特·普兰廷"
LAST	Lzh	"瑪格麗塔·奥劳斯多特·普兰廷"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000002994864380 Margareta Olausdotter Plantin, qualified P1810 subject named as Margareta Olausdotter Plantin
LAST	P2600	"6000000002994864380"	P1810	"Margareta Olausdotter Plantin"
#   P569 date of birth = +1627-09-30T00:00:00Z/11
LAST	P569	+1627-09-30T00:00:00Z/11	S2600	"6000000002994864380"
#   P570 date of death = +1701-05-12T00:00:00Z/11
LAST	P570	+1701-05-12T00:00:00Z/11	S2600	"6000000002994864380"
#   P22 father = Q10608167 Olaus Petri Niurenius
LAST	P22	Q10608167	S2600	"6000000002994864380"
#   P40 child = Q5959493 Jonas Petri Linnerius
LAST	P40	Q5959493	S2600	"6000000002994864380"
#   Q10608167 Olaus Petri Niurenius: P40 child = the item just created
Q10608167	P40	LAST	S2600	"6000000002994864380"
#   Q5959493 Jonas Petri Linnerius: P25 mother = the item just created
Q5959493	P25	LAST	S2600	"6000000002994864380"
#   the item just created: P735 given name = Q8274988 Margareta
LAST	P735	Q8274988

# create a new item
CREATE
#   set the en label to "Nils von Törne"
LAST	Len	"Nils von Törne"
#   set the mul label to "Nils von Törne"
LAST	Lmul	"Nils von Törne"
#   set the ja label to "ニルス・ヴォン・トルネ"
LAST	Lja	"ニルス・ヴォン・トルネ"
#   set the zh label to "尼尔斯·翁·托尔内"
LAST	Lzh	"尼尔斯·翁·托尔内"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000189780372889 Nils von Törne, qualified P1810 subject named as Nils von Törne
LAST	P2600	"6000000189780372889"	P1810	"Nils von Törne"
#   P569 date of birth = +1735-10-17T00:00:00Z/11
LAST	P569	+1735-10-17T00:00:00Z/11	S2600	"6000000189780372889"
#   P570 date of death = +1814-10-20T00:00:00Z/11
LAST	P570	+1814-10-20T00:00:00Z/11	S2600	"6000000189780372889"
#   P25 mother = Q141223730 Constantia Fehman
LAST	P25	Q141223730	S2600	"6000000189780372889"
#   Q141223730 Constantia Fehman: P40 child = the item just created
Q141223730	P40	LAST	S2600	"6000000189780372889"
#   the item just created: P735 given name = Q16423038 Nils
LAST	P735	Q16423038
#   P734 family name = Q65202241 Törne
LAST	P734	Q65202241

# create a new item
CREATE
#   set the en label to "Olav Gunbjørnson Rossavik"
LAST	Len	"Olav Gunbjørnson Rossavik"
#   set the mul label to "Olav Gunbjørnson Rossavik"
LAST	Lmul	"Olav Gunbjørnson Rossavik"
#   set the ja label to "オーラヴ・グンブヨルンソン・ロサヴィク"
LAST	Lja	"オーラヴ・グンブヨルンソン・ロサヴィク"
#   set the zh label to "奥拉夫·贡布约尔恩松·罗萨维克"
LAST	Lzh	"奥拉夫·贡布约尔恩松·罗萨维克"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003095071661 Olav Gunbjørnson Rossavik, qualified P1810 subject named as Olav Gunbjørnson Rossavik
LAST	P2600	"6000000003095071661"	P1810	"Olav Gunbjørnson Rossavik"
#   P569 date of birth = +1616-00-00T00:00:00Z/9
LAST	P569	+1616-00-00T00:00:00Z/9	S2600	"6000000003095071661"
#   P570 date of death = +1678-00-00T00:00:00Z/9
LAST	P570	+1678-00-00T00:00:00Z/9	S2600	"6000000003095071661"
#   P22 father = Q141216471 Gunnbjørn Gunnbjørnson Rossavik
LAST	P22	Q141216471	S2600	"6000000003095071661"
#   P25 mother = Q141224345 Signy Tormodsdatter Rossavik
LAST	P25	Q141224345	S2600	"6000000003095071661"
#   Q141216471 Gunnbjørn Gunnbjørnson Rossavik: P40 child = the item just created
Q141216471	P40	LAST	S2600	"6000000003095071661"
#   Q141224345 Signy Tormodsdatter Rossavik: P40 child = the item just created
Q141224345	P40	LAST	S2600	"6000000003095071661"
#   the item just created: P735 given name = Q16511262 Olav
LAST	P735	Q16511262
#   P734 family name = Q122838342
LAST	P734	Q122838342

# create a new item
CREATE
#   set the en label to "Paul Pederson Borsheim"
LAST	Len	"Paul Pederson Borsheim"
#   set the mul label to "Paul Pederson Borsheim"
LAST	Lmul	"Paul Pederson Borsheim"
#   set the ja label to "ポール・ペデルソン・ボルスハイム"
LAST	Lja	"ポール・ペデルソン・ボルスハイム"
#   set the zh label to "保罗·佩德尔松·博尔斯海姆"
LAST	Lzh	"保罗·佩德尔松·博尔斯海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000035525833995 Paul Pederson Borsheim, qualified P1810 subject named as Paul Pederson Borsheim
LAST	P2600	"6000000035525833995"	P1810	"Paul Pederson Borsheim"
#   P569 date of birth = +1814-06-07T00:00:00Z/11
LAST	P569	+1814-06-07T00:00:00Z/11	S2600	"6000000035525833995"
#   P570 date of death = +1891-09-20T00:00:00Z/11
LAST	P570	+1891-09-20T00:00:00Z/11	S2600	"6000000035525833995"
#   P40 child = Q141223944 Rasmus (Paulson) Borsheim
LAST	P40	Q141223944	S2600	"6000000035525833995"
#   Q141223944 Rasmus (Paulson) Borsheim: P22 father = the item just created
Q141223944	P22	LAST	S2600	"6000000035525833995"

# create a new item
CREATE
#   the item just created: set the en label to "Pauline Gasser"
LAST	Len	"Pauline Gasser"
#   set the mul label to "Pauline Gasser"
LAST	Lmul	"Pauline Gasser"
#   set the ja label to "ポーリン・ガセル"
LAST	Lja	"ポーリン・ガセル"
#   set the zh label to "波利娜·加塞尔"
LAST	Lzh	"波利娜·加塞尔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000000840175435 Pauline Gasser, qualified P1810 subject named as Pauline Gasser
LAST	P2600	"6000000000840175435"	P1810	"Pauline Gasser"
#   P569 date of birth = +1827-00-00T00:00:00Z/9
LAST	P569	+1827-00-00T00:00:00Z/9	S2600	"6000000000840175435"
#   P26 spouse = Q6190771 Carl Emil Knut Карлов Stjernvall-Walleen
LAST	P26	Q6190771	S2600	"6000000000840175435"
#   Q6190771 Carl Emil Knut Карлов Stjernvall-Walleen: P26 spouse = the item just created
Q6190771	P26	LAST	S2600	"6000000000840175435"
#   the item just created: P735 given name = Q18009833 Pauline
LAST	P735	Q18009833

# create a new item
CREATE
#   set the en label to "Petrus Jonae Jonæ Linnerius"
LAST	Len	"Petrus Jonae Jonæ Linnerius"
#   set the mul label to "Petrus Jonae Jonæ Linnerius"
LAST	Lmul	"Petrus Jonae Jonæ Linnerius"
#   add a mul alias "Petrus Jonae Jonsson"
LAST	Amul	"Petrus Jonae Jonsson"
#   set the ja label to "ペトルス・ヨナエ・ヨネ・リネリウス"
LAST	Lja	"ペトルス・ヨナエ・ヨネ・リネリウス"
#   set the zh label to "佩特鲁斯·约纳埃·约内·利内里乌斯"
LAST	Lzh	"佩特鲁斯·约纳埃·约内·利内里乌斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000006782697953 Petrus Jonae Jonæ Linnerius, qualified P1810 subject named as Petrus Jonae Jonsson
LAST	P2600	"6000000006782697953"	P1810	"Petrus Jonae Jonsson"
#   P569 date of birth = +1616-00-00T00:00:00Z/9
LAST	P569	+1616-00-00T00:00:00Z/9	S2600	"6000000006782697953"
#   P570 date of death = +1656-10-27T00:00:00Z/11
LAST	P570	+1656-10-27T00:00:00Z/11	S2600	"6000000006782697953"
#   P40 child = Q5959493 Jonas Petri Linnerius
LAST	P40	Q5959493	S2600	"6000000006782697953"
#   Q5959493 Jonas Petri Linnerius: P22 father = the item just created
Q5959493	P22	LAST	S2600	"6000000006782697953"
#   the item just created: P735 given name = Q15897708 Petrus, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q15897708	P1545	"1"	P7452	Q3409033
#   add a mul alias "Per Jonsson Jonæ Linnerius"
LAST	Amul	"Per Jonsson Jonæ Linnerius"

# create a new item
CREATE
#   set the en label to "Randolph Paulus Borsheim"
LAST	Len	"Randolph Paulus Borsheim"
#   set the mul label to "Randolph Paulus Borsheim"
LAST	Lmul	"Randolph Paulus Borsheim"
#   set the ja label to "ランドルフ・パウルス・ボルスハイム"
LAST	Lja	"ランドルフ・パウルス・ボルスハイム"
#   set the zh label to "伦道夫·保卢斯·博尔斯海姆"
LAST	Lzh	"伦道夫·保卢斯·博尔斯海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000177921459078 Randolph Paulus Borsheim, qualified P1810 subject named as Randolph Paulus Borsheim
LAST	P2600	"6000000177921459078"	P1810	"Randolph Paulus Borsheim"
#   P569 date of birth = +1926-00-00T00:00:00Z/9
LAST	P569	+1926-00-00T00:00:00Z/9	S2600	"6000000177921459078"
#   P570 date of death = +2015-00-00T00:00:00Z/9
LAST	P570	+2015-00-00T00:00:00Z/9	S2600	"6000000177921459078"
#   P22 father = Q141224339 Reinhert Borsheim
LAST	P22	Q141224339	S2600	"6000000177921459078"
#   Q141224339 Reinhert Borsheim: P40 child = the item just created
Q141224339	P40	LAST	S2600	"6000000177921459078"

# create a new item
CREATE
#   the item just created: set the en label to "Rosina Vilhelmina Matilda Berwald"
LAST	Len	"Rosina Vilhelmina Matilda Berwald"
#   set the mul label to "Rosina Vilhelmina Matilda Berwald"
LAST	Lmul	"Rosina Vilhelmina Matilda Berwald"
#   add a mul alias "Rosina Vilhelmina Matilda Scherer"
LAST	Amul	"Rosina Vilhelmina Matilda Scherer"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000018253998457 Rosina Vilhelmina Matilda Berwald, qualified P1810 subject named as Rosina Vilhelmina Matilda Scherer
LAST	P2600	"6000000018253998457"	P1810	"Rosina Vilhelmina Matilda Scherer"
#   P569 date of birth = +1817-04-06T00:00:00Z/11
LAST	P569	+1817-04-06T00:00:00Z/11	S2600	"6000000018253998457"
#   P570 date of death = +1888-07-15T00:00:00Z/11
LAST	P570	+1888-07-15T00:00:00Z/11	S2600	"6000000018253998457"
#   P26 spouse = Q217044 Franz Adolf Berwald
LAST	P26	Q217044	S2600	"6000000018253998457"
#   Q217044 Franz Adolf Berwald: P26 spouse = the item just created
Q217044	P26	LAST	S2600	"6000000018253998457"
#   the item just created: P735 given name = Q13403839 Rosina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q13403839	P1545	"1"	P7452	Q3409033
#   P735 given name = Q15711317 Vilhelmina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q15711317	P1545	"2"	P3831	Q245025
#   P735 given name = Q2054021 Matilda, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
LAST	P735	Q2054021	P1545	"3"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Samuel Samuelis Hornaeus"
LAST	Len	"Samuel Samuelis Hornaeus"
#   set the mul label to "Samuel Samuelis Hornaeus"
LAST	Lmul	"Samuel Samuelis Hornaeus"
#   set the ja label to "サミュエル・サムエリス・ホルナエウス"
LAST	Lja	"サミュエル・サムエリス・ホルナエウス"
#   set the zh label to "塞缪尔·萨穆埃利斯·霍尔纳厄斯"
LAST	Lzh	"塞缪尔·萨穆埃利斯·霍尔纳厄斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000007366595611 Samuel Samuelis Hornaeus, qualified P1810 subject named as Samuel Samuelis Hornaeus
LAST	P2600	"6000000007366595611"	P1810	"Samuel Samuelis Hornaeus"
#   P569 date of birth = +1673-00-00T00:00:00Z/9
LAST	P569	+1673-00-00T00:00:00Z/9	S2600	"6000000007366595611"
#   P570 date of death = +1740-00-00T00:00:00Z/9
LAST	P570	+1740-00-00T00:00:00Z/9	S2600	"6000000007366595611"
#   P40 child = Q141224012 Hedvig Chydenius
LAST	P40	Q141224012	S2600	"6000000007366595611"
#   Q141224012 Hedvig Chydenius: P22 father = the item just created
Q141224012	P22	LAST	S2600	"6000000007366595611"
#   the item just created: P735 given name = Q629347 Samuel, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q629347	P1545	"1"	P7452	Q3409033
#   P735 given name = Q22806387 Samuelis, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q22806387	P1545	"2"	P3831	Q245025
#   add a mul alias "Samuel Samuelis Aboënsis Hornaeus"
LAST	Amul	"Samuel Samuelis Aboënsis Hornaeus"

# create a new item
CREATE
#   set the mul label to "Segrid"
LAST	Lmul	"Segrid"
#   set the ca label to "mare de Malin Olofsdotter"
LAST	Lca	"mare de Malin Olofsdotter"
#   set the da label to "mor til Malin Olofsdotter"
LAST	Lda	"mor til Malin Olofsdotter"
#   set the de label to "Mutter von Malin Olofsdotter"
LAST	Lde	"Mutter von Malin Olofsdotter"
#   set the en label to "mother of Malin Olofsdotter"
LAST	Len	"mother of Malin Olofsdotter"
#   set the es label to "madre de Malin Olofsdotter"
LAST	Les	"madre de Malin Olofsdotter"
#   set the it label to "madre di Malin Olofsdotter"
LAST	Lit	"madre di Malin Olofsdotter"
#   set the ja label to "マリン・オロフスドッテルの母"
LAST	Lja	"マリン・オロフスドッテルの母"
#   set the nb label to "mor til Malin Olofsdotter"
LAST	Lnb	"mor til Malin Olofsdotter"
#   set the nl label to "moeder van Malin Olofsdotter"
LAST	Lnl	"moeder van Malin Olofsdotter"
#   set the pt label to "mãe de Malin Olofsdotter"
LAST	Lpt	"mãe de Malin Olofsdotter"
#   set the sv label to "mor till Malin Olofsdotter"
LAST	Lsv	"mor till Malin Olofsdotter"
#   set the zh label to "马林·奥洛夫斯多特之母"
LAST	Lzh	"马林·奥洛夫斯多特之母"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 4982922006040030712 Segrid NN
LAST	P2600	"4982922006040030712"
#   P569 date of birth = +1505-00-00T00:00:00Z/9
LAST	P569	+1505-00-00T00:00:00Z/9	S2600	"4982922006040030712"
#   P570 date of death = +1569-00-00T00:00:00Z/9
LAST	P570	+1569-00-00T00:00:00Z/9	S2600	"4982922006040030712"
#   P40 child = Q141216398 Malin Olofsdotter
LAST	P40	Q141216398	S2600	"4982922006040030712"
#   Q141216398 Malin Olofsdotter: P25 mother = the item just created
Q141216398	P25	LAST	S2600	"4982922006040030712"

# create a new item
CREATE
#   the item just created: set the en label to "Theoline Henrika Borsheim"
LAST	Len	"Theoline Henrika Borsheim"
#   set the mul label to "Theoline Henrika Borsheim"
LAST	Lmul	"Theoline Henrika Borsheim"
#   set the ja label to "テオリネ・ヘンリカ・ボルスハイム"
LAST	Lja	"テオリネ・ヘンリカ・ボルスハイム"
#   set the zh label to "特奥利内·亨里卡·博尔斯海姆"
LAST	Lzh	"特奥利内·亨里卡·博尔斯海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000169037819865 Theoline Henrika Borsheim, qualified P1810 subject named as Theoline Henrika Borsheim
LAST	P2600	"6000000169037819865"	P1810	"Theoline Henrika Borsheim"
#   P569 date of birth = +1895-12-10T00:00:00Z/11
LAST	P569	+1895-12-10T00:00:00Z/11	S2600	"6000000169037819865"
#   P570 date of death = +1992-01-00T00:00:00Z/10
LAST	P570	+1992-01-00T00:00:00Z/10	S2600	"6000000169037819865"
#   P26 spouse = Q141224339 Reinhert Borsheim
LAST	P26	Q141224339	S2600	"6000000169037819865"
#   Q141224339 Reinhert Borsheim: P26 spouse = the item just created
Q141224339	P26	LAST	S2600	"6000000169037819865"
#   Q141224279 Magdalena Wallwik: P26 spouse = Q141224371 Torsten Håkansson Rudén
Q141224279	P26	Q141224371	S2600	"6000000004548008767"
#   Q141224371 Torsten Håkansson Rudén: P26 spouse = Q141224279 Magdalena Wallwik
Q141224371	P26	Q141224279	S2600	"6000000004548321013"
#   Q141224222 Jens Wilhelm Wendt: P25 mother = Q141224161 Esther Hansine Wendt
Q141224222	P25	Q141224161	S2600	"6000000011470709855"
#   Q141223853 Rakel Rasmusdottir Borsheim: P40 child = Q141224339 Reinhert Borsheim
Q141223853	P40	Q141224339	S2600	"6000000020344732085"
#   Q141224339 Reinhert Borsheim: P734 family name = Q37328187
Q141224339	P734	Q37328187
#   Q141224161 Esther Hansine Wendt: P40 child = Q141224222 Jens Wilhelm Wendt
Q141224161	P40	Q141224222	S2600	"6000000048057114880"
#   Q141224249 Johannes John Jacobsen: P735 given name = Q4925477 John, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141224249	P735	Q4925477	P1545	"2"	P3831	Q245025
#   Q141224141 En dödfödd son Bielke: P735 given name = Q69523615, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141224141	P735	Q69523615	P1545	"1"	P7452	Q3409033
#   P735 given name = Q20111831, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q141224141	P735	Q20111831	P1545	"3"	P3831	Q245025
#   Q141224116 Clara Elfrida Tverdahl: P26 spouse = Q141224309 Ole Peter Tverdahl
Q141224116	P26	Q141224309	S2600	"6000000177172694835"
#   Q141224309 Ole Peter Tverdahl: P26 spouse = Q141224116 Clara Elfrida Tverdahl
Q141224309	P26	Q141224116	S2600	"6000000177202378835"
#   Q141224204 Inger Serine Lerma Gunderson: P25 mother = Q141224136 Dorte Sofie Nilsdatter Kyllingstad
Q141224204	P25	Q141224136	S2600	"6000000177921459129"
#   P735 given name = Q3358452 Inger, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141224204	P735	Q3358452	P1545	"1"	P7452	Q3409033
#   P735 given name = Q136121543, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141224204	P735	Q136121543	P1545	"2"	P3831	Q245025
#   Q141224136 Dorte Sofie Nilsdatter Kyllingstad: P40 child = Q141224204 Inger Serine Lerma Gunderson
Q141224136	P40	Q141224204	S2600	"6000000177969427823"
#   P735 given name = Q11166412 Dorte, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141224136	P735	Q11166412	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18201530 Sofie, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141224136	P735	Q18201530	P1545	"2"	P3831	Q245025
#   P5056 patronym or matronym = Q122837798 Nilsdatter
Q141224136	P5056	Q122837798
#   P734 family name = Q30080230
Q141224136	P734	Q30080230
#   Q141223907 Elly Olivia Frisk: P734 family name = Q27877507 Frisk
Q141223907	P734	Q27877507
#   Q141223999 Anna Ådnesdatter Lima: P40 child = Q141223972 Ådne Olsson Lima Kyllingstad. Lima
Q141223999	P40	Q141223972	S2600	"6000000178280363847"
#   P735 given name = Q666578 Anna
Q141223999	P735	Q666578
#   P734 family name = Q11255517 Lima
Q141223999	P734	Q11255517
#   Q141223972 Ådne Olsson Lima Kyllingstad. Lima: P735 given name = Q12011446, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q141223972	P735	Q12011446	P1545	"1"	P7452	Q3409033
#   P735 given name = Q67609267, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q141223972	P735	Q67609267	P1545	"2"	P3831	Q245025
#   P734 family name = Q11255517 Lima
Q141223972	P734	Q11255517

# create a new item
CREATE
#   set the en label to "Sophia Borgit Hoknes"
LAST	Len	"Sophia Borgit Hoknes"
#   set the mul label to "Sophia Borgit Hoknes"
LAST	Lmul	"Sophia Borgit Hoknes"
#   set the ja label to "ソフィア・ボルギト・ホクネス"
LAST	Lja	"ソフィア・ボルギト・ホクネス"
#   set the zh label to "索菲娅·博尔吉特·霍克内斯"
LAST	Lzh	"索菲娅·博尔吉特·霍克内斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000177921459094 Sophia Borgit Hoknes, qualified P1810 subject named as Sophia Borgit Hoknes
LAST	P2600	"6000000177921459094"	P1810	"Sophia Borgit Hoknes"
#   P569 date of birth = +1912-06-30T00:00:00Z/11
LAST	P569	+1912-06-30T00:00:00Z/11	S2600	"6000000177921459094"
#   P570 date of death = +1993-05-30T00:00:00Z/11
LAST	P570	+1993-05-30T00:00:00Z/11	S2600	"6000000177921459094"
#   P25 mother = Q141224204 Inger Serine Lerma Gunderson
LAST	P25	Q141224204	S2600	"6000000177921459094"
#   Q141224204 Inger Serine Lerma Gunderson: P40 child = the item just created
Q141224204	P40	LAST	S2600	"6000000177921459094"


# create a new item
CREATE
#   set the en label to "Caroline Signe Borsheim"
LAST	Len	"Caroline Signe Borsheim"
#   set the mul label to "Caroline Signe Borsheim"
LAST	Lmul	"Caroline Signe Borsheim"
#   set the ja label to "キャロライン・シグネ・ボルスハイム"
LAST	Lja	"キャロライン・シグネ・ボルスハイム"
#   set the zh label to "卡罗琳·西格内·博尔斯海姆"
LAST	Lzh	"卡罗琳·西格内·博尔斯海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000177921459072 Caroline Signe Borsheim, qualified P1810 subject named as Caroline Signe Borsheim
LAST	P2600	"6000000177921459072"	P1810	"Caroline Signe Borsheim"
#   P569 date of birth = +1932-11-06T00:00:00Z/11
LAST	P569	+1932-11-06T00:00:00Z/11	S2600	"6000000177921459072"
#   P570 date of death = +2007-12-04T00:00:00Z/11
LAST	P570	+2007-12-04T00:00:00Z/11	S2600	"6000000177921459072"


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
#   P21 sex or gender = Q6581097
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000177921459056 Richard Wade Borsheim, qualified P1810 subject named as Richard Wade Borsheim
LAST	P2600	"6000000177921459056"	P1810	"Richard Wade Borsheim"
#   P569 date of birth = +1963-10-20T00:00:00Z/11
LAST	P569	+1963-10-20T00:00:00Z/11	S2600	"6000000177921459056"
#   P26 spouse = Q141223923 Helen Frisk
LAST	P26	Q141223923	S2600	"6000000177921459056"
#   P40 child = Q140568870 Emma Himiko Leonhart
LAST	P40	Q140568870	S2600	"6000000177921459056"
#   Q141223923 Helen Frisk: P26 spouse = the item just created
Q141223923	P26	LAST	S2600	"6000000177921459056"
#   Q140568870 Emma Himiko Leonhart: P22 father = the item just created
Q140568870	P22	LAST	S2600	"6000000177921459056"
