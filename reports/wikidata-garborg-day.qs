# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   797 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   set the zh label to "伊娃·霍恩·阿夫·埃凯比霍尔姆"
Q19678400	Lzh	"伊娃·霍恩·阿夫·埃凯比霍尔姆"
#   set the ja label to "アンナ・アンデシュドッテル・ブヨルンラム"
Q110621422	Lja	"アンナ・アンデシュドッテル・ブヨルンラム"
#   set the zh label to "安娜·安德斯多特·布约尔恩拉姆"
Q110621422	Lzh	"安娜·安德斯多特·布约尔恩拉姆"
#   set the ja label to "ジョン・ミケルソン・ベム"
Q25451348	Lja	"ジョン・ミケルソン・ベム"
#   set the zh label to "乔恩·米凯尔松·贝姆"
Q25451348	Lzh	"乔恩·米凯尔松·贝姆"
#   set the ja label to "ヨハン・グローン"
Q2490612	Lja	"ヨハン・グローン"
#   set the zh label to "约翰·格龙"
Q2490612	Lzh	"约翰·格龙"
#   set the ja label to "ゲルハルト・ヨネ"
Q16649517	Lja	"ゲルハルト・ヨネ"
#   set the zh label to "格哈德·约内"
Q16649517	Lzh	"格哈德·约内"
#   Q5757435 Martinus Erici Gestrinius: set the mul label to "Martinus Gestrinius"
Q5757435	Lmul	"Martinus Gestrinius"
#   add a mul alias "Martinus Eriksson Gestrin"
Q5757435	Amul	"Martinus Eriksson Gestrin"
#   set the ja label to "マルティヌス・ゲストリニウス"
Q5757435	Lja	"マルティヌス・ゲストリニウス"
#   set the zh label to "马尔蒂努斯·盖斯特里尼乌斯"
Q5757435	Lzh	"马尔蒂努斯·盖斯特里尼乌斯"
#   set the ja label to "ハンス・ゲオルク・ストロムフェルト"
Q121362501	Lja	"ハンス・ゲオルク・ストロムフェルト"
#   set the zh label to "汉斯·格奥尔格·斯特罗姆费尔特"
Q121362501	Lzh	"汉斯·格奥尔格·斯特罗姆费尔特"

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Agnes Karolina Lindblom"
LAST	Len	"Agnes Karolina Lindblom"
#   set the mul label to "Agnes Karolina Lindblom"
LAST	Lmul	"Agnes Karolina Lindblom"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000017425988068 Agnes Karolina Lindblom, qualified P1810 subject named as Agnes Karolina Lindblom
LAST	P2600	"6000000017425988068"	P1810	"Agnes Karolina Lindblom"
#   P569 date of birth = +1882-02-06T00:00:00Z/11
LAST	P569	+1882-02-06T00:00:00Z/11	S2600	"6000000017425988068"
#   P570 date of death = +1976-02-24T00:00:00Z/11
LAST	P570	+1976-02-24T00:00:00Z/11	S2600	"6000000017425988068"
#   P26 spouse = Q329253 Ivar Henning Mankell
LAST	P26	Q329253	S2600	"6000000017425988068"
#   Q329253 Ivar Henning Mankell: P26 spouse = the item just created
Q329253	P26	LAST	S2600	"6000000017425988068"
#   the item just created: P735 given name = Q394431 Agnes, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q394431	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1734206 Karolina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1734206	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Anders Alstrin"
LAST	Len	"Anders Alstrin"
#   set the mul label to "Anders Alstrin"
LAST	Lmul	"Anders Alstrin"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000019263256732 Anders Alstrin, qualified P1810 subject named as Anders Björnsson
LAST	P2600	"6000000019263256732"	P1810	"Anders Björnsson"
#   P569 date of birth = +1630-00-00T00:00:00Z/9
LAST	P569	+1630-00-00T00:00:00Z/9	S2600	"6000000019263256732"
#   P570 date of death = +1699-00-00T00:00:00Z/9
LAST	P570	+1699-00-00T00:00:00Z/9	S2600	"6000000019263256732"
#   P40 child = Q141225793 Laurentius Andreae Andreae Alstrinius
LAST	P40	Q141225793	S2600	"6000000019263256732"
#   Q141225793 Laurentius Andreae Andreae Alstrinius: P22 father = the item just created
Q141225793	P22	LAST	S2600	"6000000019263256732"
#   the item just created: P735 given name = Q8843357 Anders
LAST	P735	Q8843357

# create a new item
CREATE
#   set the en label to "Anna Elisabet Charlotta Andersdotter Rehbinder"
LAST	Len	"Anna Elisabet Charlotta Andersdotter Rehbinder"
#   set the mul label to "Anna Elisabet Charlotta Andersdotter Rehbinder"
LAST	Lmul	"Anna Elisabet Charlotta Andersdotter Rehbinder"
#   add a mul alias "Anna Elisabet Charlotta Andersdotter Hedenberg"
LAST	Amul	"Anna Elisabet Charlotta Andersdotter Hedenberg"
#   set the ja label to "アンナ・エリーザベト・カルロタ・アンデシュドッテル・レビンデル"
LAST	Lja	"アンナ・エリーザベト・カルロタ・アンデシュドッテル・レビンデル"
#   set the zh label to "安娜·伊丽莎白·卡尔洛塔·安德斯多特·雷宾德尔"
LAST	Lzh	"安娜·伊丽莎白·卡尔洛塔·安德斯多特·雷宾德尔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000000909142439 Anna Elisabet Charlotta Andersdotter Rehbinder, qualified P1810 subject named as Anna Elisabet Charlotta Andersdotter Hedenberg
LAST	P2600	"6000000000909142439"	P1810	"Anna Elisabet Charlotta Andersdotter Hedenberg"
#   P569 date of birth = +1788-08-23T00:00:00Z/11
LAST	P569	+1788-08-23T00:00:00Z/11	S2600	"6000000000909142439"
#   P570 date of death = +1845-08-25T00:00:00Z/11
LAST	P570	+1845-08-25T00:00:00Z/11	S2600	"6000000000909142439"
#   P26 spouse = Q2575818 Robert Henrik Rehbinder till Viksberg
LAST	P26	Q2575818	S2600	"6000000000909142439"
#   Q2575818 Robert Henrik Rehbinder till Viksberg: P26 spouse = the item just created
Q2575818	P26	LAST	S2600	"6000000000909142439"
#   the item just created: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16423275 Elisabet, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q16423275	P1545	"2"	P3831	Q245025
#   P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1067071	P1545	"3"	P3831	Q245025
#   add a mul alias "Anna Elisabet Charlotta Rehbinder"
LAST	Amul	"Anna Elisabet Charlotta Rehbinder"

# create a new item
CREATE
#   set the en label to "Anna Helena Silvius"
LAST	Len	"Anna Helena Silvius"
#   set the mul label to "Anna Helena Silvius"
LAST	Lmul	"Anna Helena Silvius"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000021890809973 Anna Helena Silvius, qualified P1810 subject named as Anna Helena Silvius
LAST	P2600	"6000000021890809973"	P1810	"Anna Helena Silvius"
#   P569 date of birth = +1773-05-23T00:00:00Z/11
LAST	P569	+1773-05-23T00:00:00Z/11	S2600	"6000000021890809973"
#   P570 date of death = +1822-03-11T00:00:00Z/11
LAST	P570	+1822-03-11T00:00:00Z/11	S2600	"6000000021890809973"
#   P26 spouse = Q5916183 Karl Johan Andersson Knös
LAST	P26	Q5916183	S2600	"6000000021890809973"
#   P40 child = Q5916153 Anders Erik Knös
LAST	P40	Q5916153	S2600	"6000000021890809973"
#   Q5916183 Karl Johan Andersson Knös: P26 spouse = the item just created
Q5916183	P26	LAST	S2600	"6000000021890809973"
#   Q5916153 Anders Erik Knös: P25 mother = the item just created
Q5916153	P25	LAST	S2600	"6000000021890809973"
#   the item just created: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1035239 Helena, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1035239	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Anna Wilhelmina Nordenfeldt"
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
#   the item just created: set the en label to "Beata von Essen"
LAST	Len	"Beata von Essen"
#   set the mul label to "Beata von Essen"
LAST	Lmul	"Beata von Essen"
#   set the ja label to "ベアタ・ヴォン・エッセン"
LAST	Lja	"ベアタ・ヴォン・エッセン"
#   set the zh label to "贝阿塔·翁·埃森"
LAST	Lzh	"贝阿塔·翁·埃森"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000012641619366 Beata von Essen, qualified P1810 subject named as Beata von Essen
LAST	P2600	"6000000012641619366"	P1810	"Beata von Essen"
#   P569 date of birth = +1764-03-22T00:00:00Z/11
LAST	P569	+1764-03-22T00:00:00Z/11	S2600	"6000000012641619366"
#   P570 date of death = +1803-06-16T00:00:00Z/11
LAST	P570	+1803-06-16T00:00:00Z/11	S2600	"6000000012641619366"
#   P26 spouse = Q124694235 Måns Palmstierna till Grimstorp
LAST	P26	Q124694235	S2600	"6000000012641619366"
#   P40 child = Q6034157 Carl Otto Palmstierna
LAST	P40	Q6034157	S2600	"6000000012641619366"
#   Q124694235 Måns Palmstierna till Grimstorp: P26 spouse = the item just created
Q124694235	P26	LAST	S2600	"6000000012641619366"
#   Q6034157 Carl Otto Palmstierna: P25 mother = the item just created
Q6034157	P25	LAST	S2600	"6000000012641619366"
#   the item just created: P735 given name = Q338015 Beata
LAST	P735	Q338015

# create a new item
CREATE
#   set the en label to "Brita Andersdotter Grubb"
LAST	Len	"Brita Andersdotter Grubb"
#   set the mul label to "Brita Andersdotter Grubb"
LAST	Lmul	"Brita Andersdotter Grubb"
#   set the ja label to "ブリッタ・アンデシュドッテル・グルブ"
LAST	Lja	"ブリッタ・アンデシュドッテル・グルブ"
#   set the zh label to "布里塔·安德斯多特·格鲁布"
LAST	Lzh	"布里塔·安德斯多特·格鲁布"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000007548088462 Brita Andersdotter Grubb, qualified P1810 subject named as Brita Andersdotter Grubb
LAST	P2600	"6000000007548088462"	P1810	"Brita Andersdotter Grubb"
#   P569 date of birth = +1555-00-00T00:00:00Z/9
LAST	P569	+1555-00-00T00:00:00Z/9	S2600	"6000000007548088462"
#   P570 date of death = +1624-00-00T00:00:00Z/9
LAST	P570	+1624-00-00T00:00:00Z/9	S2600	"6000000007548088462"
#   P25 mother = Q127270437 Kristina Samuelsdotter
LAST	P25	Q127270437	S2600	"6000000007548088462"
#   P26 spouse = Q16649517 Gerhard Jonæ
LAST	P26	Q16649517	S2600	"6000000007548088462"
#   P40 child = Q2490612 Johan Graan till Ånsta
LAST	P40	Q2490612	S2600	"6000000007548088462"
#   Q127270437 Kristina Samuelsdotter: P40 child = the item just created
Q127270437	P40	LAST	S2600	"6000000007548088462"
#   Q16649517 Gerhard Jonæ: P26 spouse = the item just created
Q16649517	P26	LAST	S2600	"6000000007548088462"
#   Q2490612 Johan Graan till Ånsta: P25 mother = the item just created
Q2490612	P25	LAST	S2600	"6000000007548088462"

# create a new item
CREATE
#   the item just created: set the en label to "Carl Ludvig Hedenberg"
LAST	Len	"Carl Ludvig Hedenberg"
#   set the mul label to "Carl Ludvig Hedenberg"
LAST	Lmul	"Carl Ludvig Hedenberg"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000000909055457 Carl Ludvig Hedenberg, qualified P1810 subject named as Carl Ludvig Hedenberg
LAST	P2600	"6000000000909055457"	P1810	"Carl Ludvig Hedenberg"
#   P569 date of birth = +1802-12-13T00:00:00Z/11
LAST	P569	+1802-12-13T00:00:00Z/11	S2600	"6000000000909055457"
#   P570 date of death = +1858-01-20T00:00:00Z/11
LAST	P570	+1858-01-20T00:00:00Z/11	S2600	"6000000000909055457"
#   P22 father = Q2575818 Robert Henrik Rehbinder till Viksberg
LAST	P22	Q2575818	S2600	"6000000000909055457"
#   Q2575818 Robert Henrik Rehbinder till Viksberg: P40 child = the item just created
Q2575818	P40	LAST	S2600	"6000000000909055457"
#   the item just created: P735 given name = Q2529610 Carl, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q2529610	P1545	"1"	P7452	Q3409033
#   P735 given name = Q12233911 Ludvig, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q12233911	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Catharina Charlotta Samuelsdotter Wallenstierna"
LAST	Len	"Catharina Charlotta Samuelsdotter Wallenstierna"
#   set the mul label to "Catharina Charlotta Samuelsdotter Wallenstierna"
LAST	Lmul	"Catharina Charlotta Samuelsdotter Wallenstierna"
#   set the ja label to "カタリーナ・カルロタ・サムエルスドッテル・ヴァレンスティエルナ"
LAST	Lja	"カタリーナ・カルロタ・サムエルスドッテル・ヴァレンスティエルナ"
#   set the zh label to "卡塔里娜·卡尔洛塔·萨穆埃尔斯多特·瓦伦斯蒂埃尔纳"
LAST	Lzh	"卡塔里娜·卡尔洛塔·萨穆埃尔斯多特·瓦伦斯蒂埃尔纳"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000001208487154 Catharina Charlotta Samuelsdotter Wallenstierna, qualified P1810 subject named as Catharina Charlotta Samuelsdotter Wallenstierna
LAST	P2600	"6000000001208487154"	P1810	"Catharina Charlotta Samuelsdotter Wallenstierna"
#   P569 date of birth = +1671-00-00T00:00:00Z/9
LAST	P569	+1671-00-00T00:00:00Z/9	S2600	"6000000001208487154"
#   P570 date of death = +1735-04-07T00:00:00Z/11
LAST	P570	+1735-04-07T00:00:00Z/11	S2600	"6000000001208487154"
#   P26 spouse = Q20250108 Anders Andersson Pryss
LAST	P26	Q20250108	S2600	"6000000001208487154"
#   P40 child = Q6057321 Olof Andersson Pryss
LAST	P40	Q6057321	S2600	"6000000001208487154"
#   P40 child = Q16650163 Samuel Andersson Pryss
LAST	P40	Q16650163	S2600	"6000000001208487154"
#   Q20250108 Anders Andersson Pryss: P26 spouse = the item just created
Q20250108	P26	LAST	S2600	"6000000001208487154"
#   Q6057321 Olof Andersson Pryss: P25 mother = the item just created
Q6057321	P25	LAST	S2600	"6000000001208487154"
#   Q16650163 Samuel Andersson Pryss: P25 mother = the item just created
Q16650163	P25	LAST	S2600	"6000000001208487154"
#   the item just created: P735 given name = Q17317997 Catharina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q17317997	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1067071	P1545	"2"	P3831	Q245025
#   add a mul alias "Katharina Vallenstierna Wallenstierna"
LAST	Amul	"Katharina Vallenstierna Wallenstierna"

# create a new item
CREATE
#   set the en label to "Catharina Kram"
LAST	Len	"Catharina Kram"
#   set the mul label to "Catharina Kram"
LAST	Lmul	"Catharina Kram"
#   set the ja label to "カタリーナ・クラム"
LAST	Lja	"カタリーナ・クラム"
#   set the zh label to "卡塔里娜·克拉姆"
LAST	Lzh	"卡塔里娜·克拉姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003770393284 Catharina Kram, qualified P1810 subject named as Catharina Kram
LAST	P2600	"6000000003770393284"	P1810	"Catharina Kram"
#   P569 date of birth = +1669-07-02T00:00:00Z/11
LAST	P569	+1669-07-02T00:00:00Z/11	S2600	"6000000003770393284"
#   P570 date of death = +1746-09-15T00:00:00Z/11
LAST	P570	+1746-09-15T00:00:00Z/11	S2600	"6000000003770393284"
#   P26 spouse = Q5783620 Laurentius Jonæ Hallenius
LAST	P26	Q5783620	S2600	"6000000003770393284"
#   P40 child = Q5783613 Engelbert Hallenius Biskop i Skara
LAST	P40	Q5783613	S2600	"6000000003770393284"
#   Q5783620 Laurentius Jonæ Hallenius: P26 spouse = the item just created
Q5783620	P26	LAST	S2600	"6000000003770393284"
#   Q5783613 Engelbert Hallenius Biskop i Skara: P25 mother = the item just created
Q5783613	P25	LAST	S2600	"6000000003770393284"
#   the item just created: P735 given name = Q17317997 Catharina
LAST	P735	Q17317997
#   add a mul alias "Krum? Kram"
LAST	Amul	"Krum? Kram"

# create a new item
CREATE
#   set the en label to "Cecilia Olsdotter"
LAST	Len	"Cecilia Olsdotter"
#   set the mul label to "Cecilia Olsdotter"
LAST	Lmul	"Cecilia Olsdotter"
#   set the ja label to "セシリア・オルスドッテル"
LAST	Lja	"セシリア・オルスドッテル"
#   set the zh label to "塞西莉亚·奥尔斯多特"
LAST	Lzh	"塞西莉亚·奥尔斯多特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000006408507489 Cecilia Olsdotter, qualified P1810 subject named as Cecilia Olsdotter
LAST	P2600	"6000000006408507489"	P1810	"Cecilia Olsdotter"
#   P569 date of birth = +1520-00-00T00:00:00Z/9
LAST	P569	+1520-00-00T00:00:00Z/9	S2600	"6000000006408507489"
#   P570 date of death = +1569-03-03T00:00:00Z/11
LAST	P570	+1569-03-03T00:00:00Z/11	S2600	"6000000006408507489"
#   P22 father = Q141205932 Olof Timmerman
LAST	P22	Q141205932	S2600	"6000000006408507489"
#   P25 mother = Q141205926 NN
LAST	P25	Q141205926	S2600	"6000000006408507489"
#   Q141205932 Olof Timmerman: P40 child = the item just created
Q141205932	P40	LAST	S2600	"6000000006408507489"
#   Q141205926 NN: P40 child = the item just created
Q141205926	P40	LAST	S2600	"6000000006408507489"
#   the item just created: P735 given name = Q859234 Cecilia
LAST	P735	Q859234

# create a new item
CREATE
#   set the en label to "Christina Olofsdotter Hammar"
LAST	Len	"Christina Olofsdotter Hammar"
#   set the mul label to "Christina Olofsdotter Hammar"
LAST	Lmul	"Christina Olofsdotter Hammar"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000009492573975 Christina Olofsdotter Hammar, qualified P1810 subject named as Christina Olofsdotter Hammar
LAST	P2600	"6000000009492573975"	P1810	"Christina Olofsdotter Hammar"
#   P569 date of birth = +1690-00-00T00:00:00Z/9
LAST	P569	+1690-00-00T00:00:00Z/9	S2600	"6000000009492573975"
#   P570 date of death = +1752-00-00T00:00:00Z/9
LAST	P570	+1752-00-00T00:00:00Z/9	S2600	"6000000009492573975"
#   P26 spouse = Q26239902 Abraham Falkengréen
LAST	P26	Q26239902	S2600	"6000000009492573975"
#   P40 child = Q5724521 Christopher Falkengréen
LAST	P40	Q5724521	S2600	"6000000009492573975"
#   Q26239902 Abraham Falkengréen: P26 spouse = the item just created
Q26239902	P26	LAST	S2600	"6000000009492573975"
#   Q5724521 Christopher Falkengréen: P25 mother = the item just created
Q5724521	P25	LAST	S2600	"6000000009492573975"
#   the item just created: P735 given name = Q1083457 Christina
LAST	P735	Q1083457

# create a new item
CREATE
#   set the en label to "Christina Torstensdotter Falk"
LAST	Len	"Christina Torstensdotter Falk"
#   set the mul label to "Christina Torstensdotter Falk"
LAST	Lmul	"Christina Torstensdotter Falk"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000006833371173 Christina Torstensdotter Falk, qualified P1810 subject named as Christina Torstensdotter Falk
LAST	P2600	"6000000006833371173"	P1810	"Christina Torstensdotter Falk"
#   P569 date of birth = +1635-00-00T00:00:00Z/9
LAST	P569	+1635-00-00T00:00:00Z/9	S2600	"6000000006833371173"
#   P570 date of death = +1700-02-06T00:00:00Z/11
LAST	P570	+1700-02-06T00:00:00Z/11	S2600	"6000000006833371173"
#   P40 child = Q141224371 Torsten Håkansson Rudén
LAST	P40	Q141224371	S2600	"6000000006833371173"
#   Q141224371 Torsten Håkansson Rudén: P25 mother = the item just created
Q141224371	P25	LAST	S2600	"6000000006833371173"
#   the item just created: P735 given name = Q1083457 Christina
LAST	P735	Q1083457
#   P734 family name = Q16390676 Falk
LAST	P734	Q16390676

# create a new item
CREATE
#   set the en label to "Gunder Asbjørnsen Bøe"
LAST	Len	"Gunder Asbjørnsen Bøe"
#   set the mul label to "Gunder Asbjørnsen Bøe"
LAST	Lmul	"Gunder Asbjørnsen Bøe"
#   set the ja label to "グンデル・アスブヨルンセン・ボエ"
LAST	Lja	"グンデル・アスブヨルンセン・ボエ"
#   set the zh label to "贡德尔·阿斯布约尔恩森·博埃"
LAST	Lzh	"贡德尔·阿斯布约尔恩森·博埃"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000013476756495 Gunder Asbjørnsen Bøe, qualified P1810 subject named as Gunder Asbjørnsen Bøe
LAST	P2600	"6000000013476756495"	P1810	"Gunder Asbjørnsen Bøe"
#   P569 date of birth = +1753-00-00T00:00:00Z/9
LAST	P569	+1753-00-00T00:00:00Z/9	S2600	"6000000013476756495"
#   P570 date of death = +1816-12-09T00:00:00Z/11
LAST	P570	+1816-12-09T00:00:00Z/11	S2600	"6000000013476756495"
#   P22 father = Q141216458 Asbjørn Gunnarson Bø
LAST	P22	Q141216458	S2600	"6000000013476756495"
#   P25 mother = Q141216456 Anna Helgesdotter Opstad
LAST	P25	Q141216456	S2600	"6000000013476756495"
#   Q141216458 Asbjørn Gunnarson Bø: P40 child = the item just created
Q141216458	P40	LAST	S2600	"6000000013476756495"
#   Q141216456 Anna Helgesdotter Opstad: P40 child = the item just created
Q141216456	P40	LAST	S2600	"6000000013476756495"
#   the item just created: P735 given name = Q989832 Gunder
LAST	P735	Q989832
#   P734 family name = Q5005210
LAST	P734	Q5005210
#   add a mul alias "Bøll Asbjørnsen Bøe"
LAST	Amul	"Bøll Asbjørnsen Bøe"

# create a new item
CREATE
#   set the en label to "Gunilla Nilsdotter"
LAST	Len	"Gunilla Nilsdotter"
#   set the mul label to "Gunilla Nilsdotter"
LAST	Lmul	"Gunilla Nilsdotter"
#   set the ja label to "グニラ・ニルスドッテル"
LAST	Lja	"グニラ・ニルスドッテル"
#   set the zh label to "古尼拉·尼尔斯多特"
LAST	Lzh	"古尼拉·尼尔斯多特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000040336826716 Gunilla Nilsdotter, qualified P1810 subject named as Gunilla Nilsdotter
LAST	P2600	"6000000040336826716"	P1810	"Gunilla Nilsdotter"
#   P569 date of birth = +1625-00-00T00:00:00Z/9
LAST	P569	+1625-00-00T00:00:00Z/9	S2600	"6000000040336826716"
#   P40 child = Q141225793 Laurentius Andreae Andreae Alstrinius
LAST	P40	Q141225793	S2600	"6000000040336826716"
#   Q141225793 Laurentius Andreae Andreae Alstrinius: P25 mother = the item just created
Q141225793	P25	LAST	S2600	"6000000040336826716"
#   the item just created: P735 given name = Q3909969 Gunilla
LAST	P735	Q3909969

# create a new item
CREATE
#   set the en label to "Gunilla Rommel"
LAST	Len	"Gunilla Rommel"
#   set the mul label to "Gunilla Rommel"
LAST	Lmul	"Gunilla Rommel"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000021221473369 Gunilla Rommel, qualified P1810 subject named as Gunilla Rommel
LAST	P2600	"6000000021221473369"	P1810	"Gunilla Rommel"
#   P26 spouse = Q5745634 Elias Frondin
LAST	P26	Q5745634	S2600	"6000000021221473369"
#   P40 child = Q5745627 Berge / Birger Frondin
LAST	P40	Q5745627	S2600	"6000000021221473369"
#   Q5745634 Elias Frondin: P26 spouse = the item just created
Q5745634	P26	LAST	S2600	"6000000021221473369"
#   Q5745627 Berge / Birger Frondin: P25 mother = the item just created
Q5745627	P25	LAST	S2600	"6000000021221473369"
#   the item just created: P735 given name = Q3909969 Gunilla
LAST	P735	Q3909969

# create a new item
CREATE
#   set the en label to "Hans Hansson Store Vatne"
LAST	Len	"Hans Hansson Store Vatne"
#   set the mul label to "Hans Hansson Store Vatne"
LAST	Lmul	"Hans Hansson Store Vatne"
#   set the ja label to "ハンス・ハンソン・ストレ・ヴァトネ"
LAST	Lja	"ハンス・ハンソン・ストレ・ヴァトネ"
#   set the zh label to "汉斯·汉松·斯托雷·瓦特内"
LAST	Lzh	"汉斯·汉松·斯托雷·瓦特内"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005608892535 Hans Hansson Store Vatne, qualified P1810 subject named as Hans Hansson Store Vatne
LAST	P2600	"6000000005608892535"	P1810	"Hans Hansson Store Vatne"
#   P569 date of birth = +1740-00-00T00:00:00Z/9
LAST	P569	+1740-00-00T00:00:00Z/9	S2600	"6000000005608892535"
#   P570 date of death = +1816-07-05T00:00:00Z/11
LAST	P570	+1816-07-05T00:00:00Z/11	S2600	"6000000005608892535"
#   P40 child = Q141216388 Jon Hansson St. Vatne
LAST	P40	Q141216388	S2600	"6000000005608892535"
#   Q141216388 Jon Hansson St. Vatne: P22 father = the item just created
Q141216388	P22	LAST	S2600	"6000000005608892535"
#   the item just created: P735 given name = Q632842
LAST	P735	Q632842
#   P734 family name = Q30087270
LAST	P734	Q30087270
#   P734 family name = Q30134985 Vatne
LAST	P734	Q30134985
#   add a mul alias "Hans Store Vatne"
LAST	Amul	"Hans Store Vatne"

# create a new item
CREATE
#   set the en label to "Haquinus Thorstani Rudenius"
LAST	Len	"Haquinus Thorstani Rudenius"
#   set the mul label to "Haquinus Thorstani Rudenius"
LAST	Lmul	"Haquinus Thorstani Rudenius"
#   add a mul alias "Haquinus Thorstani Håkan Torstensson"
LAST	Amul	"Haquinus Thorstani Håkan Torstensson"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000006833125349 Haquinus Thorstani Rudenius, qualified P1810 subject named as Haquinus Thorstani Håkan Torstensson
LAST	P2600	"6000000006833125349"	P1810	"Haquinus Thorstani Håkan Torstensson"
#   P569 date of birth = +1613-04-01T00:00:00Z/11
LAST	P569	+1613-04-01T00:00:00Z/11	S2600	"6000000006833125349"
#   P570 date of death = +1697-06-19T00:00:00Z/11
LAST	P570	+1697-06-19T00:00:00Z/11	S2600	"6000000006833125349"
#   P40 child = Q141224371 Torsten Håkansson Rudén
LAST	P40	Q141224371	S2600	"6000000006833125349"
#   Q141224371 Torsten Håkansson Rudén: P22 father = the item just created
Q141224371	P22	LAST	S2600	"6000000006833125349"
#   the item just created: add a mul alias "Haquinis Rudenius"
LAST	Amul	"Haquinis Rudenius"

# create a new item
CREATE
#   set the en label to "Jon Torson Røyneberg"
LAST	Len	"Jon Torson Røyneberg"
#   set the mul label to "Jon Torson Røyneberg"
LAST	Lmul	"Jon Torson Røyneberg"
#   add a mul alias "Jon Torson Godeset"
LAST	Amul	"Jon Torson Godeset"
#   set the ja label to "ジョン・トルソン・ロイネベルグ"
LAST	Lja	"ジョン・トルソン・ロイネベルグ"
#   set the zh label to "乔恩·托尔松·罗伊内贝尔格"
LAST	Lzh	"乔恩·托尔松·罗伊内贝尔格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005609102976 Jon Torson Røyneberg, qualified P1810 subject named as Jon Torson Godeset
LAST	P2600	"6000000005609102976"	P1810	"Jon Torson Godeset"
#   P569 date of birth = +1720-00-00T00:00:00Z/9
LAST	P569	+1720-00-00T00:00:00Z/9	S2600	"6000000005609102976"
#   P570 date of death = +1790-00-00T00:00:00Z/9
LAST	P570	+1790-00-00T00:00:00Z/9	S2600	"6000000005609102976"
#   P40 child = Q141216638 Olaug Jonsdatter Heigre
LAST	P40	Q141216638	S2600	"6000000005609102976"
#   Q141216638 Olaug Jonsdatter Heigre: P22 father = the item just created
Q141216638	P22	LAST	S2600	"6000000005609102976"
#   the item just created: P735 given name = Q13501137 Jon
LAST	P735	Q13501137
#   add a mul alias "Jon Røyneberg"
LAST	Amul	"Jon Røyneberg"

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
#   P40 child = Q141242499 Gunnar Sahlin
LAST	P40	Q141242499	S2600	"6000000003002231602"
#   Q116760688 Maria Nordenfelt: P40 child = the item just created
Q116760688	P40	LAST	S2600	"6000000003002231602"
#   Q141242499 Gunnar Sahlin: P22 father = the item just created
Q141242499	P22	LAST	S2600	"6000000003002231602"

# create a new item
CREATE
#   the item just created: set the en label to "Magdalena Sofia Wrangel af Sauss"
LAST	Len	"Magdalena Sofia Wrangel af Sauss"
#   set the mul label to "Magdalena Sofia Wrangel af Sauss"
LAST	Lmul	"Magdalena Sofia Wrangel af Sauss"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000013022865578 Magdalena Sofia Wrangel af Sauss, qualified P1810 subject named as Magdalena Sofia Wrangel af Sauss
LAST	P2600	"6000000013022865578"	P1810	"Magdalena Sofia Wrangel af Sauss"
#   P569 date of birth = +1764-00-00T00:00:00Z/9
LAST	P569	+1764-00-00T00:00:00Z/9	S2600	"6000000013022865578"
#   P570 date of death = +1788-00-00T00:00:00Z/9
LAST	P570	+1788-00-00T00:00:00Z/9	S2600	"6000000013022865578"
#   P26 spouse = Q6003542 Henrik Johan Nauckhoff
LAST	P26	Q6003542	S2600	"6000000013022865578"
#   P40 child = Q16649958 Johan Otto Nauckhoff
LAST	P40	Q16649958	S2600	"6000000013022865578"
#   Q6003542 Henrik Johan Nauckhoff: P26 spouse = the item just created
Q6003542	P26	LAST	S2600	"6000000013022865578"
#   Q16649958 Johan Otto Nauckhoff: P25 mother = the item just created
Q16649958	P25	LAST	S2600	"6000000013022865578"
#   the item just created: P735 given name = Q842544 Magdalena, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q842544	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q18201520	P1545	"2"	P3831	Q245025
#   P734 family name = Q35930488 Wrangel
LAST	P734	Q35930488

# create a new item
CREATE
#   set the en label to "Margareta Kalsenia"
LAST	Len	"Margareta Kalsenia"
#   set the mul label to "Margareta Kalsenia"
LAST	Lmul	"Margareta Kalsenia"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000035049072634 Margareta Kalsenia, qualified P1810 subject named as Margareta Kalsenia
LAST	P2600	"6000000035049072634"	P1810	"Margareta Kalsenia"
#   P569 date of birth = +1698-10-13T00:00:00Z/11
LAST	P569	+1698-10-13T00:00:00Z/11	S2600	"6000000035049072634"
#   P570 date of death = +1772-05-03T00:00:00Z/11
LAST	P570	+1772-05-03T00:00:00Z/11	S2600	"6000000035049072634"
#   P26 spouse = Q16650170 Ingeldus Laurentii Rabenius
LAST	P26	Q16650170	S2600	"6000000035049072634"
#   P40 child = Q6060365 Olof Ingelsson Rabenius
LAST	P40	Q6060365	S2600	"6000000035049072634"
#   Q16650170 Ingeldus Laurentii Rabenius: P26 spouse = the item just created
Q16650170	P26	LAST	S2600	"6000000035049072634"
#   Q6060365 Olof Ingelsson Rabenius: P25 mother = the item just created
Q6060365	P25	LAST	S2600	"6000000035049072634"
#   the item just created: P735 given name = Q8274988 Margareta
LAST	P735	Q8274988

# create a new item
CREATE
#   set the en label to "Margareta Stecksenia"
LAST	Len	"Margareta Stecksenia"
#   set the mul label to "Margareta Stecksenia"
LAST	Lmul	"Margareta Stecksenia"
#   set the ja label to "マルガレータ・ステクセニア"
LAST	Lja	"マルガレータ・ステクセニア"
#   set the zh label to "瑪格麗塔·斯特克塞尼阿"
LAST	Lzh	"瑪格麗塔·斯特克塞尼阿"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000012736539557 Margareta Stecksenia, qualified P1810 subject named as Margareta Stecksenia
LAST	P2600	"6000000012736539557"	P1810	"Margareta Stecksenia"
#   P569 date of birth = +1721-00-00T00:00:00Z/9
LAST	P569	+1721-00-00T00:00:00Z/9	S2600	"6000000012736539557"
#   P570 date of death = +1793-04-03T00:00:00Z/11
LAST	P570	+1793-04-03T00:00:00Z/11	S2600	"6000000012736539557"
#   P26 spouse = Q99373530 Carl Magnus Nordin
LAST	P26	Q99373530	S2600	"6000000012736539557"
#   P40 child = Q6015299 Friherre Johan Magnus af Nordin
LAST	P40	Q6015299	S2600	"6000000012736539557"
#   P40 child = Q4993033 Carl Gustaf Nordin
LAST	P40	Q4993033	S2600	"6000000012736539557"
#   Q99373530 Carl Magnus Nordin: P26 spouse = the item just created
Q99373530	P26	LAST	S2600	"6000000012736539557"
#   Q6015299 Friherre Johan Magnus af Nordin: P25 mother = the item just created
Q6015299	P25	LAST	S2600	"6000000012736539557"
#   Q4993033 Carl Gustaf Nordin: P25 mother = the item just created
Q4993033	P25	LAST	S2600	"6000000012736539557"

# create a new item
CREATE
#   the item just created: set the en label to "Maria Carlberg"
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
#   the item just created: set the en label to "Maria Carolina Elisabet Sahlin"
LAST	Len	"Maria Carolina Elisabet Sahlin"
#   set the mul label to "Maria Carolina Elisabet Sahlin"
LAST	Lmul	"Maria Carolina Elisabet Sahlin"
#   set the ja label to "マリア・カロリーナ・エリーザベト・サリン"
LAST	Lja	"マリア・カロリーナ・エリーザベト・サリン"
#   set the zh label to "玛丽亚·卡罗琳娜·伊丽莎白·萨林"
LAST	Lzh	"玛丽亚·卡罗琳娜·伊丽莎白·萨林"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000002986902894 Maria Carolina Elisabet Sahlin, qualified P1810 subject named as Elisabet Sahlin (Kastman)
LAST	P2600	"6000000002986902894"	P1810	"Elisabet Sahlin (Kastman)"
#   P569 date of birth = +1871-02-28T00:00:00Z/11
LAST	P569	+1871-02-28T00:00:00Z/11	S2600	"6000000002986902894"
#   P570 date of death = +1962-06-13T00:00:00Z/11
LAST	P570	+1962-06-13T00:00:00Z/11	S2600	"6000000002986902894"
#   P40 child = Q141242499 Gunnar Sahlin
LAST	P40	Q141242499	S2600	"6000000002986902894"
#   Q141242499 Gunnar Sahlin: P25 mother = the item just created
Q141242499	P25	LAST	S2600	"6000000002986902894"

# create a new item
CREATE
#   the item just created: set the en label to "Maria Magdalena Lochner"
LAST	Len	"Maria Magdalena Lochner"
#   set the mul label to "Maria Magdalena Lochner"
LAST	Lmul	"Maria Magdalena Lochner"
#   set the ja label to "マリア・マグダレーナ・ロクネル"
LAST	Lja	"マリア・マグダレーナ・ロクネル"
#   set the zh label to "玛丽亚·马格达莱纳·洛克纳"
LAST	Lzh	"玛丽亚·马格达莱纳·洛克纳"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000019582909951 Maria Magdalena Lochner, qualified P1810 subject named as Maria Magdalena Lochner
LAST	P2600	"6000000019582909951"	P1810	"Maria Magdalena Lochner"
#   P569 date of birth = +1760-00-00T00:00:00Z/9
LAST	P569	+1760-00-00T00:00:00Z/9	S2600	"6000000019582909951"
#   P570 date of death = +1824-04-03T00:00:00Z/11
LAST	P570	+1824-04-03T00:00:00Z/11	S2600	"6000000019582909951"
#   P26 spouse = Q116439449 Abraham Grafström
LAST	P26	Q116439449	S2600	"6000000019582909951"
#   P40 child = Q490686 Anders Abraham Grafström
LAST	P40	Q490686	S2600	"6000000019582909951"
#   Q116439449 Abraham Grafström: P26 spouse = the item just created
Q116439449	P26	LAST	S2600	"6000000019582909951"
#   Q490686 Anders Abraham Grafström: P25 mother = the item just created
Q490686	P25	LAST	S2600	"6000000019582909951"
#   the item just created: P735 given name = Q325872 Maria, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q325872	P1545	"1"	P7452	Q3409033
#   P735 given name = Q842544 Magdalena, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q842544	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Märta Elisabeth Bure"
LAST	Len	"Märta Elisabeth Bure"
#   set the mul label to "Märta Elisabeth Bure"
LAST	Lmul	"Märta Elisabeth Bure"
#   set the ja label to "メルタ・エリーザベト・ブレ"
LAST	Lja	"メルタ・エリーザベト・ブレ"
#   set the zh label to "梅尔塔·伊丽莎白·布雷"
LAST	Lzh	"梅尔塔·伊丽莎白·布雷"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000006127557060 Märta Elisabeth Bure, qualified P1810 subject named as Märta Elisabeth Bure
LAST	P2600	"6000000006127557060"	P1810	"Märta Elisabeth Bure"
#   P569 date of birth = +1710-01-28T00:00:00Z/11
LAST	P569	+1710-01-28T00:00:00Z/11	S2600	"6000000006127557060"
#   P570 date of death = +1752-09-30T00:00:00Z/11
LAST	P570	+1752-09-30T00:00:00Z/11	S2600	"6000000006127557060"
#   P26 spouse = Q124606874 Hans Didrik Mörner af Morlanda
LAST	P26	Q124606874	S2600	"6000000006127557060"
#   P40 child = Q6001555 Carl Claes Mörner af Morlanda
LAST	P40	Q6001555	S2600	"6000000006127557060"
#   Q124606874 Hans Didrik Mörner af Morlanda: P26 spouse = the item just created
Q124606874	P26	LAST	S2600	"6000000006127557060"
#   the item just created: P735 given name = Q1576232 Märta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q1576232	P1545	"1"	P7452	Q3409033
#   P735 given name = Q63611044 Elisabeth, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q63611044	P1545	"2"	P3831	Q245025
#   P734 family name = Q11335012 Bure
LAST	P734	Q11335012

# create a new item
CREATE
#   set the mul label to "N.N. Voster"
LAST	Lmul	"N.N. Voster"
#   set the ca label to "mare de Ingebret Pederson Voster"
LAST	Lca	"mare de Ingebret Pederson Voster"
#   set the da label to "mor til Ingebret Pederson Voster"
LAST	Lda	"mor til Ingebret Pederson Voster"
#   set the de label to "Mutter von Ingebret Pederson Voster"
LAST	Lde	"Mutter von Ingebret Pederson Voster"
#   set the en label to "mother of Ingebret Pederson Voster"
LAST	Len	"mother of Ingebret Pederson Voster"
#   set the es label to "madre de Ingebret Pederson Voster"
LAST	Les	"madre de Ingebret Pederson Voster"
#   set the it label to "madre di Ingebret Pederson Voster"
LAST	Lit	"madre di Ingebret Pederson Voster"
#   set the ja label to "インゲブレート・ペデルソン・ヴォステルの母"
LAST	Lja	"インゲブレート・ペデルソン・ヴォステルの母"
#   set the nb label to "mor til Ingebret Pederson Voster"
LAST	Lnb	"mor til Ingebret Pederson Voster"
#   set the nl label to "moeder van Ingebret Pederson Voster"
LAST	Lnl	"moeder van Ingebret Pederson Voster"
#   set the pt label to "mãe de Ingebret Pederson Voster"
LAST	Lpt	"mãe de Ingebret Pederson Voster"
#   set the sv label to "mor till Ingebret Pederson Voster"
LAST	Lsv	"mor till Ingebret Pederson Voster"
#   set the zh label to "英厄布雷特·佩德尔松·沃斯特尔之母"
LAST	Lzh	"英厄布雷特·佩德尔松·沃斯特尔之母"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000015302207141 N.N. Voster
LAST	P2600	"6000000015302207141"
#   P26 spouse = Q141242562 Peder Jonsen Voster
LAST	P26	Q141242562	S2600	"6000000015302207141"
#   P40 child = Q141205913 Ingebret Pederson Voster
LAST	P40	Q141205913	S2600	"6000000015302207141"
#   Q141242562 Peder Jonsen Voster: P26 spouse = the item just created
Q141242562	P26	LAST	S2600	"6000000015302207141"
#   Q141205913 Ingebret Pederson Voster: P25 mother = the item just created
Q141205913	P25	LAST	S2600	"6000000015302207141"

# create a new item
CREATE
#   the item just created: set the en label to "Nils Fister"
LAST	Len	"Nils Fister"
#   set the mul label to "Nils Fister"
LAST	Lmul	"Nils Fister"
#   set the ja label to "ニルス・フィステル"
LAST	Lja	"ニルス・フィステル"
#   set the zh label to "尼尔斯·菲斯特尔"
LAST	Lzh	"尼尔斯·菲斯特尔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 328126701460004633 Nils Fister, qualified P1810 subject named as Nils Fister
LAST	P2600	"328126701460004633"	P1810	"Nils Fister"
#   P569 date of birth = +1533-00-00T00:00:00Z/9
LAST	P569	+1533-00-00T00:00:00Z/9	S2600	"328126701460004633"
#   P570 date of death = +1580-00-00T00:00:00Z/9
LAST	P570	+1580-00-00T00:00:00Z/9	S2600	"328126701460004633"
#   P26 spouse = Q141205922 Marit Ormsd Byre
LAST	P26	Q141205922	S2600	"328126701460004633"
#   Q141205922 Marit Ormsd Byre: P26 spouse = the item just created
Q141205922	P26	LAST	S2600	"328126701460004633"
#   the item just created: P735 given name = Q16423038 Nils
LAST	P735	Q16423038

# create a new item
CREATE
#   set the en label to "Nils Nilsson Midt-Fister"
LAST	Len	"Nils Nilsson Midt-Fister"
#   set the mul label to "Nils Nilsson Midt-Fister"
LAST	Lmul	"Nils Nilsson Midt-Fister"
#   add a mul alias "Nils Nilsson Fister"
LAST	Amul	"Nils Nilsson Fister"
#   set the ja label to "ニルス・ニルソン・ミドトフィステル"
LAST	Lja	"ニルス・ニルソン・ミドトフィステル"
#   set the zh label to "尼尔斯·尼尔松·米德特菲斯特尔"
LAST	Lzh	"尼尔斯·尼尔松·米德特菲斯特尔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 328122852240006970 Nils Nilsson Midt-Fister d.y, qualified P1810 subject named as Nils Nilsson Fister d.y
LAST	P2600	"328122852240006970"	P1810	"Nils Nilsson Fister d.y"
#   P569 date of birth = +1570-00-00T00:00:00Z/9
LAST	P569	+1570-00-00T00:00:00Z/9	S2600	"328122852240006970"
#   P570 date of death = +1648-00-00T00:00:00Z/9
LAST	P570	+1648-00-00T00:00:00Z/9	S2600	"328122852240006970"
#   P25 mother = Q141205922 Marit Ormsd Byre
LAST	P25	Q141205922	S2600	"328122852240006970"
#   Q141205922 Marit Ormsd Byre: P40 child = the item just created
Q141205922	P40	LAST	S2600	"328122852240006970"
#   the item just created: P735 given name = Q16423038 Nils
LAST	P735	Q16423038
#   P5056 patronym or matronym = Q130233015 Nilsson
LAST	P5056	Q130233015
#   add a mul alias "Nils Midt-Fister"
LAST	Amul	"Nils Midt-Fister"

# create a new item
CREATE
#   set the en label to "Nils Skytte"
LAST	Len	"Nils Skytte"
#   set the mul label to "Nils Skytte"
LAST	Lmul	"Nils Skytte"
#   set the ja label to "ニルス・スキテ"
LAST	Lja	"ニルス・スキテ"
#   set the zh label to "尼尔斯·斯基特"
LAST	Lzh	"尼尔斯·斯基特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000008412100548 Nils Skytte, qualified P1810 subject named as Nils Skytte
LAST	P2600	"6000000008412100548"	P1810	"Nils Skytte"
#   P26 spouse = Q141225104 Engel Danckwardt
LAST	P26	Q141225104	S2600	"6000000008412100548"
#   P40 child = Q141242409 Henning Nilsson Skytte
LAST	P40	Q141242409	S2600	"6000000008412100548"
#   Q141225104 Engel Danckwardt: P26 spouse = the item just created
Q141225104	P26	LAST	S2600	"6000000008412100548"
#   Q141242409 Henning Nilsson Skytte: P22 father = the item just created
Q141242409	P22	LAST	S2600	"6000000008412100548"
#   the item just created: P735 given name = Q16423038 Nils
LAST	P735	Q16423038

# create a new item
CREATE
#   set the en label to "Ragnhild Jonsdatter Grannes"
LAST	Len	"Ragnhild Jonsdatter Grannes"
#   set the mul label to "Ragnhild Jonsdatter Grannes"
LAST	Lmul	"Ragnhild Jonsdatter Grannes"
#   set the ja label to "ラグンヒル・ヨンスダッテル・グラネス"
LAST	Lja	"ラグンヒル・ヨンスダッテル・グラネス"
#   set the zh label to "拉格希尔德·永斯达特·格拉内斯"
LAST	Lzh	"拉格希尔德·永斯达特·格拉内斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005608892528 Ragnhild Jonsdatter Grannes, qualified P1810 subject named as Ragnhild Jonsdatter Grannes
LAST	P2600	"6000000005608892528"	P1810	"Ragnhild Jonsdatter Grannes"
#   P569 date of birth = +1738-00-00T00:00:00Z/9
LAST	P569	+1738-00-00T00:00:00Z/9	S2600	"6000000005608892528"
#   P570 date of death = +1817-01-22T00:00:00Z/11
LAST	P570	+1817-01-22T00:00:00Z/11	S2600	"6000000005608892528"
#   P40 child = Q141216388 Jon Hansson St. Vatne
LAST	P40	Q141216388	S2600	"6000000005608892528"
#   Q141216388 Jon Hansson St. Vatne: P25 mother = the item just created
Q141216388	P25	LAST	S2600	"6000000005608892528"
#   the item just created: P735 given name = Q1390292 Ragnhild
LAST	P735	Q1390292
#   P5056 patronym or matronym = Q141189036
LAST	P5056	Q141189036
#   P734 family name = Q37442010 Grannes, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q37442010	P3831	Q28418670
#   add a mul alias "Ragnhild Grannes"
LAST	Amul	"Ragnhild Grannes"

# create a new item
CREATE
#   set the en label to "Ragnhild Jonsdatter Lea"
LAST	Len	"Ragnhild Jonsdatter Lea"
#   set the mul label to "Ragnhild Jonsdatter Lea"
LAST	Lmul	"Ragnhild Jonsdatter Lea"
#   set the ja label to "ラグンヒル・ヨンスダッテル・リー"
LAST	Lja	"ラグンヒル・ヨンスダッテル・リー"
#   set the zh label to "拉格希尔德·永斯达特·莉亚"
LAST	Lzh	"拉格希尔德·永斯达特·莉亚"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005609547635 Ragnhild Jonsdatter Lea, qualified P1810 subject named as Ragnhild Jonsdatter Lea
LAST	P2600	"6000000005609547635"	P1810	"Ragnhild Jonsdatter Lea"
#   P569 date of birth = +1787-00-00T00:00:00Z/9
LAST	P569	+1787-00-00T00:00:00Z/9	S2600	"6000000005609547635"
#   P570 date of death = +1819-03-05T00:00:00Z/11
LAST	P570	+1819-03-05T00:00:00Z/11	S2600	"6000000005609547635"
#   P26 spouse = Q141225676 Anders Rasmusson Lea
LAST	P26	Q141225676	S2600	"6000000005609547635"
#   P40 child = Q141223744 Rasmus Wibye Andersson Lea
LAST	P40	Q141223744	S2600	"6000000005609547635"
#   Q141225676 Anders Rasmusson Lea: P26 spouse = the item just created
Q141225676	P26	LAST	S2600	"6000000005609547635"
#   Q141223744 Rasmus Wibye Andersson Lea: P25 mother = the item just created
Q141223744	P25	LAST	S2600	"6000000005609547635"

# create a new item
CREATE
#   the item just created: set the en label to "Sara Lucia Indebetou"
LAST	Len	"Sara Lucia Indebetou"
#   set the mul label to "Sara Lucia Indebetou"
LAST	Lmul	"Sara Lucia Indebetou"
#   set the ja label to "サラ・ルチア・インデベトウ"
LAST	Lja	"サラ・ルチア・インデベトウ"
#   set the zh label to "萨拉·露西娅·因德贝托乌"
LAST	Lzh	"萨拉·露西娅·因德贝托乌"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000012736684384 Sara Lucia Indebetou, qualified P1810 subject named as Sara Lucia Indebetou
LAST	P2600	"6000000012736684384"	P1810	"Sara Lucia Indebetou"
#   P569 date of birth = +1748-12-11T00:00:00Z/11
LAST	P569	+1748-12-11T00:00:00Z/11	S2600	"6000000012736684384"
#   P570 date of death = +1787-10-04T00:00:00Z/11
LAST	P570	+1787-10-04T00:00:00Z/11	S2600	"6000000012736684384"
#   P26 spouse = Q6015299 Friherre Johan Magnus af Nordin
LAST	P26	Q6015299	S2600	"6000000012736684384"
#   P40 child = Q6015181 Carl Johan af Nordin
LAST	P40	Q6015181	S2600	"6000000012736684384"
#   Q6015299 Friherre Johan Magnus af Nordin: P26 spouse = the item just created
Q6015299	P26	LAST	S2600	"6000000012736684384"
#   Q6015181 Carl Johan af Nordin: P25 mother = the item just created
Q6015181	P25	LAST	S2600	"6000000012736684384"
#   the item just created: P735 given name = Q833345 Sara, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q833345	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1160640 Lucia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1160640	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Seth Mikael Franzén"
LAST	Len	"Seth Mikael Franzén"
#   set the mul label to "Seth Mikael Franzén"
LAST	Lmul	"Seth Mikael Franzén"
#   set the ja label to "セス・ミカエル・フランツェーン"
LAST	Lja	"セス・ミカエル・フランツェーン"
#   set the zh label to "塞思·米卡埃尔·夫兰曾"
LAST	Lzh	"塞思·米卡埃尔·夫兰曾"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000032504851016 Seth Mikael Franzén, qualified P1810 subject named as Seth Mikael Franzén
LAST	P2600	"6000000032504851016"	P1810	"Seth Mikael Franzén"
#   P569 date of birth = +1816-05-26T00:00:00Z/11
LAST	P569	+1816-05-26T00:00:00Z/11	S2600	"6000000032504851016"
#   P570 date of death = +1897-04-09T00:00:00Z/11
LAST	P570	+1897-04-09T00:00:00Z/11	S2600	"6000000032504851016"
#   P22 father = Q333297 Frans Michael Zachrichsson Franzén
LAST	P22	Q333297	S2600	"6000000032504851016"
#   P25 mother = Q141223854 Sofia Kristina Wester
LAST	P25	Q141223854	S2600	"6000000032504851016"
#   Q333297 Frans Michael Zachrichsson Franzén: P40 child = the item just created
Q333297	P40	LAST	S2600	"6000000032504851016"
#   Q141223854 Sofia Kristina Wester: P40 child = the item just created
Q141223854	P40	LAST	S2600	"6000000032504851016"
#   the item just created: P735 given name = Q3958283 Seth, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q3958283	P1545	"1"	P7452	Q3409033
#   P735 given name = Q15620350 Mikael, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q15620350	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Ursula Christina Törne"
LAST	Len	"Ursula Christina Törne"
#   set the mul label to "Ursula Christina Törne"
LAST	Lmul	"Ursula Christina Törne"
#   set the ja label to "ウルスラ・クリスティーナ・トルネ"
LAST	Lja	"ウルスラ・クリスティーナ・トルネ"
#   set the zh label to "乌尔苏拉·克里斯蒂娜·托尔内"
LAST	Lzh	"乌尔苏拉·克里斯蒂娜·托尔内"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000002960353877 Ursula Christina Törne, qualified P1810 subject named as Ursula Christina Törne
LAST	P2600	"6000000002960353877"	P1810	"Ursula Christina Törne"
#   P569 date of birth = +1682-01-21T00:00:00Z/11
LAST	P569	+1682-01-21T00:00:00Z/11	S2600	"6000000002960353877"
#   P570 date of death = +1765-03-11T00:00:00Z/11
LAST	P570	+1765-03-11T00:00:00Z/11	S2600	"6000000002960353877"
#   P26 spouse = Q5597349 Thure Stensson Bielke
LAST	P26	Q5597349	S2600	"6000000002960353877"
#   P40 child = Q362485 Sten Carl Turesson Bielke
LAST	P40	Q362485	S2600	"6000000002960353877"
#   Q5597349 Thure Stensson Bielke: P26 spouse = the item just created
Q5597349	P26	LAST	S2600	"6000000002960353877"
#   Q362485 Sten Carl Turesson Bielke: P25 mother = the item just created
Q362485	P25	LAST	S2600	"6000000002960353877"
#   the item just created: P735 given name = Q1087262 Ursula, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q1087262	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1083457 Christina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1083457	P1545	"2"	P3831	Q245025
#   P734 family name = Q65202241 Törne
LAST	P734	Q65202241

# create a new item
CREATE
#   set the en label to "Valborg Ingebretsdatter Voster"
LAST	Len	"Valborg Ingebretsdatter Voster"
#   set the mul label to "Valborg Ingebretsdatter Voster"
LAST	Lmul	"Valborg Ingebretsdatter Voster"
#   set the ja label to "ヴァルボルグ・インゲブレトスダッテル・ヴォステル"
LAST	Lja	"ヴァルボルグ・インゲブレトスダッテル・ヴォステル"
#   set the zh label to "瓦尔博尔格·因盖布雷特斯达特·沃斯特尔"
LAST	Lzh	"瓦尔博尔格·因盖布雷特斯达特·沃斯特尔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000007980728964 Valborg Ingebretsdatter Voster, qualified P1810 subject named as Valborg Ingebretsdatter Voster
LAST	P2600	"6000000007980728964"	P1810	"Valborg Ingebretsdatter Voster"
#   P569 date of birth = +1620-00-00T00:00:00Z/9
LAST	P569	+1620-00-00T00:00:00Z/9	S2600	"6000000007980728964"
#   P570 date of death = +1653-00-00T00:00:00Z/9
LAST	P570	+1653-00-00T00:00:00Z/9	S2600	"6000000007980728964"
#   P22 father = Q141205913 Ingebret Pederson Voster
LAST	P22	Q141205913	S2600	"6000000007980728964"
#   P25 mother = Q141205899 Bergitte Ivarsdatter Tjentland
LAST	P25	Q141205899	S2600	"6000000007980728964"
#   Q141205913 Ingebret Pederson Voster: P40 child = the item just created
Q141205913	P40	LAST	S2600	"6000000007980728964"
#   Q141205899 Bergitte Ivarsdatter Tjentland: P40 child = the item just created
Q141205899	P40	LAST	S2600	"6000000007980728964"
#   the item just created: P735 given name = Q20726370 Valborg
LAST	P735	Q20726370
#   Q6014618 Enar Vilhelm Nordenfelt: P40 child = Q116760688 Maria Nordenfelt
Q6014618	P40	Q116760688	S2600	"4198641"
#   P2600 Geni.com profile ID = 4198641 Enar Vilhelm Nordenfelt, qualified P1810 subject named as Enar Vilhelm Nordenfelt
Q6014618	P2600	"4198641"	P1810	"Enar Vilhelm Nordenfelt"
#   Q48562235 Prost Olaus Troilius: P40 child = Q1168365 Ärkebiskop Samuelis Olai Troilius
Q48562235	P40	Q1168365	S2600	"4377269"
#   P2600 Geni.com profile ID = 4377269 Prost Olaus Troilius, qualified P1810 subject named as Prost Olaus Troilius
Q48562235	P2600	"4377269"	P1810	"Prost Olaus Troilius"
#   Q273181 Judith of Flanders: P40 child = Q6180419 Skule Torstigson
Q273181	P40	Q6180419	S2600	"4927821238910067084"
#   P2600 Geni.com profile ID = 4927821238910067084 Judith of Flanders, qualified P1810 subject named as Judith of Flanders
Q273181	P2600	"4927821238910067084"	P1810	"Judith of Flanders"
#   Q112969835 Helena Maria Söderhielm: P40 child = Q5975022 Lars August Mannerheim
Q112969835	P40	Q5975022	S2600	"6000000000047260007"
#   P40 child = Q1814297 Carl Erik Mannerheim
Q112969835	P40	Q1814297	S2600	"6000000000047260007"
#   P2600 Geni.com profile ID = 6000000000047260007 Helena Maria Söderhielm, qualified P1810 subject named as Helena Maria Söderhielm
Q112969835	P2600	"6000000000047260007"	P1810	"Helena Maria Söderhielm"
#   P735 given name = Q1035239 Helena, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q112969835	P735	Q1035239	P1545	"1"	P7452	Q3409033
#   P735 given name = Q325872 Maria, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q112969835	P735	Q325872	P1545	"2"	P3831	Q245025
#   Q116775360 Helena Mariana Sparre af Söfdeborg: P40 child = Q6184934 Erik Samuel Sparre af Söfdeborg
Q116775360	P40	Q6184934	S2600	"6000000000572198595"
#   P40 child = Q6184896 Grev Carl Georg Georg Sparre af Söfdeborg
Q116775360	P40	Q6184896	S2600	"6000000000572198595"
#   P2600 Geni.com profile ID = 6000000000572198595 Helena Mariana Sparre af Söfdeborg, qualified P1810 subject named as Helena Mariana Ehrenkrona
Q116775360	P2600	"6000000000572198595"	P1810	"Helena Mariana Ehrenkrona"
#   Q110457044 Anna Magdalena Pauli: P40 child = Q2624238 Wilhelm Mauritz Klingspor
Q110457044	P40	Q2624238	S2600	"6000000000581186204"
#   P40 child = Q5914181 Otto Reinhold Klingspor
Q110457044	P40	Q5914181	S2600	"6000000000581186204"
#   P40 child = Q5914160 Fredrik Filip Klingspor
Q110457044	P40	Q5914160	S2600	"6000000000581186204"
#   P2600 Geni.com profile ID = 6000000000581186204 Anna Magdalena Pauli, qualified P1810 subject named as Anna Magdalena Pauli
Q110457044	P2600	"6000000000581186204"	P1810	"Anna Magdalena Pauli"
#   Q43974 Louis I, The Pious: P40 child = Q284400 Giséle of Cysoing
Q43974	P40	Q284400	S2600	"6000000001266578142"
#   P2600 Geni.com profile ID = 6000000001266578142 Louis I, The Pious, qualified P1810 subject named as Louis I, The Pious
Q43974	P2600	"6000000001266578142"	P1810	"Louis I, The Pious"
#   Q110313452 Carl Hising: P40 child = Q5807131 Mikael Hising
Q110313452	P40	Q5807131	S2600	"6000000001334601101"
#   P26 spouse = Q127270462 Barbro Petré
Q110313452	P26	Q127270462	S2600	"6000000001334601101"
#   P2600 Geni.com profile ID = 6000000001334601101 Carl Hising, qualified P1810 subject named as Carl Hising
Q110313452	P2600	"6000000001334601101"	P1810	"Carl Hising"
#   Q378177 Baldwin IV the Bearded, count of Flanders: P40 child = Q273181 Judith of Flanders
Q378177	P40	Q273181	S2600	"6000000001412935350"
#   P2600 Geni.com profile ID = 6000000001412935350 Baldwin IV the Bearded, count of Flanders, qualified P1810 subject named as Baldwin IV the Bearded, count of Flanders
Q378177	P2600	"6000000001412935350"	P1810	"Baldwin IV the Bearded, count of Flanders"
#   Q2066886 Hedvig Catharina Charlotta De la Gardie: P40 child = Q469962 Eva Sophia Sofia von Fersen
Q2066886	P40	Q469962	S2600	"6000000001515228463"
#   P40 child = Q455071 Hans Axel von Fersen
Q2066886	P40	Q455071	S2600	"6000000001515228463"
#   P40 child = Q3129338 Hedvig Eleonora von Fersen
Q2066886	P40	Q3129338	S2600	"6000000001515228463"
#   P40 child = Q19312912 Fabian Reinhold von Fersen
Q2066886	P40	Q19312912	S2600	"6000000001515228463"
#   P2600 Geni.com profile ID = 6000000001515228463 Hedvig Catharina Charlotta De la Gardie, qualified P1810 subject named as Hedvig Catharina Charlotta De la Gardie
Q2066886	P2600	"6000000001515228463"	P1810	"Hedvig Catharina Charlotta De la Gardie"
#   Q75291928 Åsulv Skulesson: P40 child = Q19061035 Guttorm Àsulfsson à Rein
Q75291928	P40	Q19061035	S2600	"6000000001827562649"
#   P2600 Geni.com profile ID = 6000000001827562649 Åsulv Skulesson, qualified P1810 subject named as Åsulv Skulesson
Q75291928	P2600	"6000000001827562649"	P1810	"Åsulv Skulesson"
#   Q110386164 Ulrika Christina Mörner af Morlanda: P40 child = Q4973002 Christina Charlotta Piper
Q110386164	P40	Q4973002	S2600	"6000000001882580286"
#   P26 spouse = Q6161733 Carl Fredrik Piper till Krageholm
Q110386164	P26	Q6161733	S2600	"6000000001882580286"
#   P2600 Geni.com profile ID = 6000000001882580286 Ulrika Christina Mörner af Morlanda, qualified P1810 subject named as Ulrika Christina Mörner af Morlanda
Q110386164	P2600	"6000000001882580286"	P1810	"Ulrika Christina Mörner af Morlanda"
#   P735 given name = Q18924998 Ulrika, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110386164	P735	Q18924998	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1083457 Christina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110386164	P735	Q1083457	P1545	"2"	P3831	Q245025
#   P734 family name = Q141223484
Q110386164	P734	Q141223484
#   Q16649267 Elias Pedersson Gavelius: P40 child = Q5605668 Petrus Eliae Cederschiöld till Lidboholm
Q16649267	P40	Q5605668	S2600	"6000000002063115439"
#   P2600 Geni.com profile ID = 6000000002063115439 Elias Pedersson Gavelius, qualified P1810 subject named as Elias Pedersson Gavelius
Q16649267	P2600	"6000000002063115439"	P1810	"Elias Pedersson Gavelius"
#   Q3044 Charlemagne: P40 child = Q43974 Louis I, The Pious
Q3044	P40	Q43974	S2600	"6000000002457013227"
#   P2600 Geni.com profile ID = 6000000002457013227 Charlemagne, qualified P1810 subject named as Charlemagne
Q3044	P2600	"6000000002457013227"	P1810	"Charlemagne"
#   Q5725186 Michael Fant: P40 child = Q5725105 Eric Michael Fant
Q5725186	P40	Q5725105	S2600	"6000000002734683252"
#   P2600 Geni.com profile ID = 6000000002734683252 Michael Fant, qualified P1810 subject named as Michael Fant
Q5725186	P2600	"6000000002734683252"	P1810	"Michael Fant"
#   Q141223432 Osmund Larsson Nese: P25 mother = Q141219202 Elen Kristoffersdotter Nese
Q141223432	P25	Q141219202	S2600	"6000000002744891329"
#   Q5597349 Thure Stensson Bielke: P40 child = Q362485 Sten Carl Turesson Bielke
Q5597349	P40	Q362485	S2600	"6000000002960482301"
#   P2600 Geni.com profile ID = 6000000002960482301 Thure Stensson Bielke, qualified P1810 subject named as Thure Stensson Bielke
Q5597349	P2600	"6000000002960482301"	P1810	"Thure Stensson Bielke"
#   Q6082455 Thure Gustaf Rudbeck: P40 child = Q108937197 Catharina Charlotta Rudbeck
Q6082455	P40	Q108937197	S2600	"6000000003580303855"
#   Q6180419 Skule Torstigson: P40 child = Q75291928 Åsulv Skulesson
Q6180419	P40	Q75291928	S2600	"6000000003645683608"
#   P2600 Geni.com profile ID = 6000000003645683608 Skule Torstigson, qualified P1810 subject named as Skule Torstigson
Q6180419	P2600	"6000000003645683608"	P1810	"Skule Torstigson"
#   Q141225066 NN: P25 mother = Q141198375 Astri Torchelsdatter Øvre Time
Q141225066	P25	Q141198375	S2600	"6000000003732714453"
#   Q5783620 Laurentius Jonæ Hallenius: P40 child = Q5783613 Engelbert Hallenius Biskop i Skara
Q5783620	P40	Q5783613	S2600	"6000000003770421312"
#   P2600 Geni.com profile ID = 6000000003770421312 Laurentius Jonæ Hallenius, qualified P1810 subject named as Laurentius Jonæ Hallenius
Q5783620	P2600	"6000000003770421312"	P1810	"Laurentius Jonæ Hallenius"
#   Q103771971 Anna Maria Törnstjerna, Törne: P40 child = Q6082455 Thure Gustaf Rudbeck
Q103771971	P40	Q6082455	S2600	"6000000003883345592"
#   P26 spouse = Q103771956 Olof Rudbeck
Q103771971	P26	Q103771956	S2600	"6000000003883345592"
#   P2600 Geni.com profile ID = 6000000003883345592 Anna Maria Törnstjerna, Törne, qualified P1810 subject named as Anna Maria Törnstjerna, Törne
Q103771971	P2600	"6000000003883345592"	P1810	"Anna Maria Törnstjerna, Törne"
#   Q103771956 Olof Rudbeck: P40 child = Q6082455 Thure Gustaf Rudbeck
Q103771956	P40	Q6082455	S2600	"6000000003883549023"
#   P26 spouse = Q103771971 Anna Maria Törnstjerna, Törne
Q103771956	P26	Q103771971	S2600	"6000000003883549023"
#   P2600 Geni.com profile ID = 6000000003883549023 Olof Rudbeck, qualified P1810 subject named as Olof Rudbeck
Q103771956	P2600	"6000000003883549023"	P1810	"Olof Rudbeck"
#   Q141242569 Åsa Gunnbjørnsdotter Stordrange: P25 mother = Q141199862 Helga Bjørnsdatter Tengs
Q141242569	P25	Q141199862	S2600	"6000000004559874338"
#   Q141242383 Bjørn Gunnbjørnsson Kvåvig: P25 mother = Q141199862 Helga Bjørnsdatter Tengs
Q141242383	P25	Q141199862	S2600	"6000000004569609494"
#   Q141199862 Helga Bjørnsdatter Tengs: P40 child = Q141242569 Åsa Gunnbjørnsdotter Stordrange
Q141199862	P40	Q141242569	S2600	"6000000004697849241"
#   P40 child = Q141242383 Bjørn Gunnbjørnsson Kvåvig
Q141199862	P40	Q141242383	S2600	"6000000004697849241"
#   Q6003542 Henrik Johan Nauckhoff: P40 child = Q16649958 Johan Otto Nauckhoff
Q6003542	P40	Q16649958	S2600	"6000000005393641057"
#   P2600 Geni.com profile ID = 6000000005393641057 Henrik Johan Nauckhoff, qualified P1810 subject named as Henrik Johan Nauckhoff
Q6003542	P2600	"6000000005393641057"	P1810	"Henrik Johan Nauckhoff"
#   Q141223436 Tore Underberge III: P25 mother = Q141205937 Ragnhild Eyvindsdotter Eyvindsdotter
Q141223436	P25	Q141205937	S2600	"6000000005607672589"
#   Q141242542 Kristoffer Olson Tjåland: P26 spouse = Q141242500 Gunnhild Pedersdatter Skårland
Q141242542	P26	Q141242500	S2600	"6000000005609534679"
#   Q141242500 Gunnhild Pedersdatter Skårland: P26 spouse = Q141242542 Kristoffer Olson Tjåland
Q141242500	P26	Q141242542	S2600	"6000000005609534687"
#   Q314521 Berengar II of Ivrea, king of Italy: P40 child = Q466257 Rozala of Italy
Q314521	P40	Q466257	S2600	"6000000005936551695"
#   P2600 Geni.com profile ID = 6000000005936551695 Berengar II of Ivrea, king of Italy, qualified P1810 subject named as Berengar II of Ivrea, king of Italy
Q314521	P2600	"6000000005936551695"	P1810	"Berengar II of Ivrea, king of Italy"
#   Q6184934 Erik Samuel Sparre af Söfdeborg: P25 mother = Q116775360 Helena Mariana Sparre af Söfdeborg
Q6184934	P25	Q116775360	S2600	"6000000006127346098"
#   Q130755124 Johan Gustav Boije af Gennäs: P40 child = Q5580881 Carl Gustaf Boije af Gennäs
Q130755124	P40	Q5580881	S2600	"6000000006127355736"
#   P2600 Geni.com profile ID = 6000000006127355736 Johan Gustav Boije af Gennäs, qualified P1810 subject named as Johan Gustav Boije af Gennäs
Q130755124	P2600	"6000000006127355736"	P1810	"Johan Gustav Boije af Gennäs"
#   Q131726951 Catharina Elisabet Arosell Adlerheim: P40 child = Q1036858 Carl August Ehrensvärd
Q131726951	P40	Q1036858	S2600	"6000000006127409064"
#   P2600 Geni.com profile ID = 6000000006127409064 Catharina Elisabet Arosell Adlerheim, qualified P1810 subject named as Catharina Elisabet Arosell Adlerheim
Q131726951	P2600	"6000000006127409064"	P1810	"Catharina Elisabet Arosell Adlerheim"
#   P735 given name = Q17317997 Catharina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q131726951	P735	Q17317997	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16423275 Elisabet, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q131726951	P735	Q16423275	P1545	"2"	P3831	Q245025
#   Q109296398 Fredrika Eleonora Arvidsdotter Horn af Ekebyholm: P40 child = Q6188777 Arvid Nils Gustafsson Stenbock
Q109296398	P40	Q6188777	S2600	"6000000006127496847"
#   P2600 Geni.com profile ID = 6000000006127496847 Fredrika Eleonora Arvidsdotter Horn af Ekebyholm, qualified P1810 subject named as Fredrika Eleonora Arvidsdotter Horn af Ekebyholm
Q109296398	P2600	"6000000006127496847"	P1810	"Fredrika Eleonora Arvidsdotter Horn af Ekebyholm"
#   Q109296043 Ulrika Catharina Koskull: P40 child = Q5584506 Magnus Brahe
Q109296043	P40	Q5584506	S2600	"6000000006127576609"
#   P26 spouse = Q352296 Magnus Fredrik Brahe till Skokloster
Q109296043	P26	Q352296	S2600	"6000000006127576609"
#   P2600 Geni.com profile ID = 6000000006127576609 Ulrika Catharina Koskull, qualified P1810 subject named as Ulrika Catharina Koskull
Q109296043	P2600	"6000000006127576609"	P1810	"Ulrika Catharina Koskull"
#   P735 given name = Q18924998 Ulrika, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q109296043	P735	Q18924998	P1545	"1"	P7452	Q3409033
#   P735 given name = Q17317997 Catharina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q109296043	P735	Q17317997	P1545	"2"	P3831	Q245025
#   Q130684265 Carl Philip Strömfelt: P40 child = Q27863581 Johan Carl Strömfelt
Q130684265	P40	Q27863581	S2600	"6000000006127651336"
#   P26 spouse = Q130684369 Agneta Johansdotter Ållongren
Q130684265	P26	Q130684369	S2600	"6000000006127651336"
#   P2600 Geni.com profile ID = 6000000006127651336 Carl Philip Strömfelt, qualified P1810 subject named as Carl Philip Strömfelt
Q130684265	P2600	"6000000006127651336"	P1810	"Carl Philip Strömfelt"
#   Q130684369 Agneta Johansdotter Ållongren: P40 child = Q27863581 Johan Carl Strömfelt
Q130684369	P40	Q27863581	S2600	"6000000006127651347"
#   P26 spouse = Q130684265 Carl Philip Strömfelt
Q130684369	P26	Q130684265	S2600	"6000000006127651347"
#   P2600 Geni.com profile ID = 6000000006127651347 Agneta Johansdotter Ållongren, qualified P1810 subject named as Agneta Johansdotter Ållongren
Q130684369	P2600	"6000000006127651347"	P1810	"Agneta Johansdotter Ållongren"
#   Q109829800 Eva Helena Adelswärd: P40 child = Q19975889 Fredrik August August Adelswärd
Q109829800	P40	Q19975889	S2600	"6000000006127732211"
#   P40 child = Q5542632 Eric Reinhold Adelswärd
Q109829800	P40	Q5542632	S2600	"6000000006127732211"
#   P26 spouse = Q5542628 Erik Göran Adelswärd
Q109829800	P26	Q5542628	S2600	"6000000006127732211"
#   P2600 Geni.com profile ID = 6000000006127732211 Eva Helena Adelswärd, qualified P1810 subject named as Eva Helena von Fersen
Q109829800	P2600	"6000000006127732211"	P1810	"Eva Helena von Fersen"
#   Q1340357 Jakob Benzelius: P25 mother = Q115631647 Margareta Odhelia
Q1340357	P25	Q115631647	S2600	"6000000006645210002"
#   Q5570928 Lars Benzelstierna: P25 mother = Q115631647 Margareta Odhelia
Q5570928	P25	Q115631647	S2600	"6000000006782861172"
#   Q109265381 Jonas Benedicti Rudberus: P40 child = Q26239714 Jonas Jonae Rudberus
Q109265381	P40	Q26239714	S2600	"6000000006828534420"
#   P26 spouse = Q109266155 Magdalena Johansdotter Bure
Q109265381	P26	Q109266155	S2600	"6000000006828534420"
#   P2600 Geni.com profile ID = 6000000006828534420 Jonas Benedicti Rudberus, qualified P1810 subject named as Jonas Benedicti Rudberus
Q109265381	P2600	"6000000006828534420"	P1810	"Jonas Benedicti Rudberus"
#   Q139996297 Anders Törnebladh: P40 child = Q6218068 Carl Peter Peter Törnebladh
Q139996297	P40	Q6218068	S2600	"6000000006911473220"
#   P2600 Geni.com profile ID = 6000000006911473220 Anders Törnebladh, qualified P1810 subject named as Anders Törnebladh
Q139996297	P2600	"6000000006911473220"	P1810	"Anders Törnebladh"
#   Q5570926 Gustaf Benzelstierna: P25 mother = Q115631647 Margareta Odhelia
Q5570926	P25	Q115631647	S2600	"6000000007247592424"
#   Q692994 Henrik Benzelius: P25 mother = Q115631647 Margareta Odhelia
Q692994	P25	Q115631647	S2600	"6000000007247681864"
#   Q19678400 Eva Horn af Ekebyholm: P40 child = Q4989142 Eva Helena Löwen
Q19678400	P40	Q4989142	S2600	"6000000007286110282"
#   P2600 Geni.com profile ID = 6000000007286110282 Eva Horn af Ekebyholm, qualified P1810 subject named as Eva Horn af Ekebyholm
Q19678400	P2600	"6000000007286110282"	P1810	"Eva Horn af Ekebyholm"
#   Q110621422 Anna Andersdotter Björnram: P40 child = Q5773252 Lars Grubbe
Q110621422	P40	Q5773252	S2600	"6000000007289863298"
#   P2600 Geni.com profile ID = 6000000007289863298 Anna Andersdotter Björnram, qualified P1810 subject named as Anna Andersdotter Björnram
Q110621422	P2600	"6000000007289863298"	P1810	"Anna Andersdotter Björnram"
#   Q110231041 Anna Tersera: P40 child = Q6330080 Elof Steuch till Duveke
Q110231041	P40	Q6330080	S2600	"6000000007311831371"
#   P26 spouse = Q456456 Matthias Petri Steuchius
Q110231041	P26	Q456456	S2600	"6000000007311831371"
#   P2600 Geni.com profile ID = 6000000007311831371 Anna Tersera, qualified P1810 subject named as Anna Tersera
Q110231041	P2600	"6000000007311831371"	P1810	"Anna Tersera"
#   Q25451348 Jon Mickelsson Behm: P40 child = Q5568857 Daniel Jonsson Behmer
Q25451348	P40	Q5568857	S2600	"6000000007314101475"
#   P2600 Geni.com profile ID = 6000000007314101475 Jon Mickelsson Behm, qualified P1810 subject named as Jon Mickelsson Behm
Q25451348	P2600	"6000000007314101475"	P1810	"Jon Mickelsson Behm"
#   Q124608453 Petrus Ugla: P40 child = Q3946660 Samuel af Ugglas
Q124608453	P40	Q3946660	S2600	"6000000007473614567"
#   P2600 Geni.com profile ID = 6000000007473614567 Petrus Ugla, qualified P1810 subject named as Petrus Ugla
Q124608453	P2600	"6000000007473614567"	P1810	"Petrus Ugla"
#   Q136028287 Anna Brita Carré: P40 child = Q6175942 David Wilhelm Silfverstolpe
Q136028287	P40	Q6175942	S2600	"6000000007509570928"
#   P2600 Geni.com profile ID = 6000000007509570928 Anna Brita Carré, qualified P1810 subject named as Anna Brita Carré
Q136028287	P2600	"6000000007509570928"	P1810	"Anna Brita Carré"
#   P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q136028287	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P735 given name = Q918013, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q136028287	P735	Q918013	P1545	"2"	P3831	Q245025
#   Q16649517 Gerhard Jonæ: P40 child = Q2490612 Johan Graan till Ånsta
Q16649517	P40	Q2490612	S2600	"6000000007548056402"
#   P2600 Geni.com profile ID = 6000000007548056402 Gerhard Jonæ, qualified P1810 subject named as Gerhard Jonæ
Q16649517	P2600	"6000000007548056402"	P1810	"Gerhard Jonæ"
#   Q121362501 Hans Georg Strömfelt: P40 child = Q19860752 Carl Harald Strömfelt
Q121362501	P40	Q19860752	S2600	"6000000007598076234"
#   P26 spouse = Q133825293 Christina Ebba Leijonhufvud
Q121362501	P26	Q133825293	S2600	"6000000007598076234"
#   P2600 Geni.com profile ID = 6000000007598076234 Hans Georg Strömfelt, qualified P1810 subject named as Hans Georg Strömfelt
Q121362501	P2600	"6000000007598076234"	P1810	"Hans Georg Strömfelt"
#   Q110457049 Christina Elisabet Taube af Karlö: P40 child = Q2040261 Otto Reinhold Strömfelt
Q110457049	P40	Q2040261	S2600	"6000000007602850104"
#   P26 spouse = Q12363134 Gustaf Adolf Strömfelt till Strömhult
Q110457049	P26	Q12363134	S2600	"6000000007602850104"
#   P2600 Geni.com profile ID = 6000000007602850104 Christina Elisabet Taube af Karlö, qualified P1810 subject named as Christina Elisabet Taube af Karlö
Q110457049	P2600	"6000000007602850104"	P1810	"Christina Elisabet Taube af Karlö"
#   P735 given name = Q1083457 Christina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110457049	P735	Q1083457	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16423275 Elisabet, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110457049	P735	Q16423275	P1545	"2"	P3831	Q245025
#   P735 given name = Q106145920 Taube, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q110457049	P735	Q106145920	P1545	"3"	P3831	Q245025
#   Q12363134 Gustaf Adolf Strömfelt till Strömhult: P40 child = Q2040261 Otto Reinhold Strömfelt
Q12363134	P40	Q2040261	S2600	"6000000007602857711"
#   P26 spouse = Q110457049 Christina Elisabet Taube af Karlö
Q12363134	P26	Q110457049	S2600	"6000000007602857711"
#   P2600 Geni.com profile ID = 6000000007602857711 Gustaf Adolf Strömfelt till Strömhult, qualified P1810 subject named as Gustaf Adolf Strömfelt till Strömhult
Q12363134	P2600	"6000000007602857711"	P1810	"Gustaf Adolf Strömfelt till Strömhult"
#   Q108615809 Margareta Jacobsdotter Jernstedt: P40 child = Q5589950 Jakob Bunge
Q108615809	P40	Q5589950	S2600	"6000000007755407668"
#   P26 spouse = Q108615842 Mårten Bunge
Q108615809	P26	Q108615842	S2600	"6000000007755407668"
#   P2600 Geni.com profile ID = 6000000007755407668 Margareta Jacobsdotter Jernstedt, qualified P1810 subject named as Margareta Jacobsdotter Jernstedt
Q108615809	P2600	"6000000007755407668"	P1810	"Margareta Jacobsdotter Jernstedt"
#   Q104550167 Karin Mattsdotter Björnram: P40 child = Q5735890 Arvid Ernaldsson Forbus till Kumo
Q104550167	P40	Q5735890	S2600	"6000000007787563524"
#   P26 spouse = Q104550158 Ernald Mattsson Forbes of Corsindae
Q104550167	P26	Q104550158	S2600	"6000000007787563524"
#   P2600 Geni.com profile ID = 6000000007787563524 Karin Mattsdotter Björnram, qualified P1810 subject named as Karin Mattsdotter Björnram
Q104550167	P2600	"6000000007787563524"	P1810	"Karin Mattsdotter Björnram"
#   P735 given name = Q1814118 Karin
Q104550167	P735	Q1814118
#   Q110395711 Charlotta Eleonora Hedvig von Krassow: P40 child = Q10511031 Gustaf Adolf Fredrik Wilhelm von Essen
Q110395711	P40	Q10511031	S2600	"6000000007948266424"
#   P26 spouse = Q657814 Hans Henrik von Essen
Q110395711	P26	Q657814	S2600	"6000000007948266424"
#   P2600 Geni.com profile ID = 6000000007948266424 Charlotta Eleonora Hedvig von Krassow, qualified P1810 subject named as Charlotta Eleonora Hedvig von Krassow
Q110395711	P2600	"6000000007948266424"	P1810	"Charlotta Eleonora Hedvig von Krassow"
#   P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110395711	P735	Q1067071	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18759077 Eleonora, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110395711	P735	Q18759077	P1545	"2"	P3831	Q245025
#   P735 given name = Q13648620 Hedvig, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q110395711	P735	Q13648620	P1545	"3"	P3831	Q245025
#   Q73763454 Sigfrid Porthan: P40 child = Q333651 Henrik Gabriel Porthan
Q73763454	P40	Q333651	S2600	"6000000008047204297"
#   P2600 Geni.com profile ID = 6000000008047204297 Sigfrid Porthan, qualified P1810 subject named as Sigfrid Porthanus
Q73763454	P2600	"6000000008047204297"	P1810	"Sigfrid Porthanus"
#   Q5589959 Sven Bunge till Beateberg: P40 child = Q16945169 Mårten Bunge till Beateberg
Q5589959	P40	Q16945169	S2600	"6000000008151349039"
#   P26 spouse = Q3359192 Elsa Beata Wrede af Elimä
Q5589959	P26	Q3359192	S2600	"6000000008151349039"
#   P2600 Geni.com profile ID = 6000000008151349039 Sven Bunge till Beateberg, qualified P1810 subject named as Sven Bunge till Beateberg
Q5589959	P2600	"6000000008151349039"	P1810	"Sven Bunge till Beateberg"
#   Q133825293 Christina Ebba Leijonhufvud: P40 child = Q19860752 Carl Harald Strömfelt
Q133825293	P40	Q19860752	S2600	"6000000008467554009"
#   P26 spouse = Q121362501 Hans Georg Strömfelt
Q133825293	P26	Q121362501	S2600	"6000000008467554009"
#   P2600 Geni.com profile ID = 6000000008467554009 Christina Ebba Leijonhufvud, qualified P1810 subject named as Christina Ebba Bielkenstierna
Q133825293	P2600	"6000000008467554009"	P1810	"Christina Ebba Bielkenstierna"
#   P735 given name = Q1083457 Christina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q133825293	P735	Q1083457	P1545	"1"	P7452	Q3409033
#   P735 given name = Q2242896 Ebba, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q133825293	P735	Q2242896	P1545	"2"	P3831	Q245025
#   Q115631647 Margareta Odhelia: P40 child = Q1340357 Jakob Benzelius
Q115631647	P40	Q1340357	S2600	"6000000008496913568"
#   P40 child = Q1340404 Eric Benzelius d.y.
Q115631647	P40	Q1340404	S2600	"6000000008496913568"
#   P40 child = Q5570928 Lars Benzelstierna
Q115631647	P40	Q5570928	S2600	"6000000008496913568"
#   P40 child = Q5570926 Gustaf Benzelstierna
Q115631647	P40	Q5570926	S2600	"6000000008496913568"
#   P40 child = Q692994 Henrik Benzelius
Q115631647	P40	Q692994	S2600	"6000000008496913568"
#   P2600 Geni.com profile ID = 6000000008496913568 Margareta Odhelia, qualified P1810 subject named as Margareta Eriksdotter
Q115631647	P2600	"6000000008496913568"	P1810	"Margareta Eriksdotter"
#   P735 given name = Q8274988 Margareta
Q115631647	P735	Q8274988
#   Q3769073 Gisela of Friuli: P40 child = Q314521 Berengar II of Ivrea, king of Italy
Q3769073	P40	Q314521	S2600	"6000000008592343633"
#   P2600 Geni.com profile ID = 6000000008592343633 Gisela of Friuli, qualified P1810 subject named as Gisela of Friuli
Q3769073	P2600	"6000000008592343633"	P1810	"Gisela of Friuli"
#   Q109835397 Carl Gustaf Lagerfelt: P40 child = Q5931081 Gustaf Adolf Lagerfelt
Q109835397	P40	Q5931081	S2600	"6000000008840975651"
#   P26 spouse = Q109835398 Maria Elisabet von der Osten
Q109835397	P26	Q109835398	S2600	"6000000008840975651"
#   P2600 Geni.com profile ID = 6000000008840975651 Carl Gustaf Lagerfelt, qualified P1810 subject named as Carl Gustaf Lagerfelt
Q109835397	P2600	"6000000008840975651"	P1810	"Carl Gustaf Lagerfelt"
#   Q109835398 Maria Elisabet von der Osten: P40 child = Q5931081 Gustaf Adolf Lagerfelt
Q109835398	P40	Q5931081	S2600	"6000000008841179321"
#   P26 spouse = Q109835397 Carl Gustaf Lagerfelt
Q109835398	P26	Q109835397	S2600	"6000000008841179321"
#   P2600 Geni.com profile ID = 6000000008841179321 Maria Elisabet von der Osten, qualified P1810 subject named as Maria Elisabet von der Osten
Q109835398	P2600	"6000000008841179321"	P1810	"Maria Elisabet von der Osten"
#   P735 given name = Q325872 Maria, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q109835398	P735	Q325872	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16423275 Elisabet, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q109835398	P735	Q16423275	P1545	"2"	P3831	Q245025
#   P734 family name = Q20726980 Osten
Q109835398	P734	Q20726980
#   Q109835400 Magdalena Christina Appelbom: P40 child = Q19976679 Otto Johan Lagerfelt
Q109835400	P40	Q19976679	S2600	"6000000008889872098"
#   P26 spouse = Q5931081 Gustaf Adolf Lagerfelt
Q109835400	P26	Q5931081	S2600	"6000000008889872098"
#   P2600 Geni.com profile ID = 6000000008889872098 Magdalena Christina Appelbom, qualified P1810 subject named as Magdalena Christina Appelbom
Q109835400	P2600	"6000000008889872098"	P1810	"Magdalena Christina Appelbom"
#   Q110547941 Altea Silfverström: P40 child = Q5542622 Johan Adelswärd
Q110547941	P40	Q5542622	S2600	"6000000008935291612"
#   P26 spouse = Q110547936 Johan Hultman Adelswärd
Q110547941	P26	Q110547936	S2600	"6000000008935291612"
#   P2600 Geni.com profile ID = 6000000008935291612 Altea Silfverström, qualified P1810 subject named as Altea Silfverström
Q110547941	P2600	"6000000008935291612"	P1810	"Altea Silfverström"
#   Q26239902 Abraham Falkengréen: P40 child = Q5724521 Christopher Falkengréen
Q26239902	P40	Q5724521	S2600	"6000000008979112162"
#   P2600 Geni.com profile ID = 6000000008979112162 Abraham Falkengréen, qualified P1810 subject named as Abraham Falkengren
Q26239902	P2600	"6000000008979112162"	P1810	"Abraham Falkengren"
#   Q124694235 Måns Palmstierna till Grimstorp: P40 child = Q6034157 Carl Otto Palmstierna
Q124694235	P40	Q6034157	S2600	"6000000008988775900"
#   P2600 Geni.com profile ID = 6000000008988775900 Måns Palmstierna till Grimstorp, qualified P1810 subject named as Måns Palmstierna till Grimstorp
Q124694235	P2600	"6000000008988775900"	P1810	"Måns Palmstierna till Grimstorp"
#   Q20250108 Anders Andersson Pryss: P40 child = Q6057321 Olof Andersson Pryss
Q20250108	P40	Q6057321	S2600	"6000000009014627733"
#   P40 child = Q16650163 Samuel Andersson Pryss
Q20250108	P40	Q16650163	S2600	"6000000009014627733"
#   P2600 Geni.com profile ID = 6000000009014627733 Anders Andersson Pryss, qualified P1810 subject named as Anders Andersson Pryss
Q20250108	P2600	"6000000009014627733"	P1810	"Anders Andersson Pryss"
#   Q108937197 Catharina Charlotta Rudbeck: P22 father = Q6082455 Thure Gustaf Rudbeck
Q108937197	P22	Q6082455	S2600	"6000000009217450213"
#   P25 mother = Q141217393 Magdalena von Mentzer
Q108937197	P25	Q141217393	S2600	"6000000009217450213"
#   P40 child = Q546949 Sofia Magdalena Silfverstolpe
Q108937197	P40	Q546949	S2600	"6000000009217450213"
#   P2600 Geni.com profile ID = 6000000009217450213 Catharina Charlotta Rudbeck, qualified P1810 subject named as Catharina Charlotta Rudbeck
Q108937197	P2600	"6000000009217450213"	P1810	"Catharina Charlotta Rudbeck"
#   Q110547956 Catharina Funck: P40 child = Q5542628 Erik Göran Adelswärd
Q110547956	P40	Q5542628	S2600	"6000000009401513008"
#   P40 child = Q141223897 Adolf Adelswärd
Q110547956	P40	Q141223897	S2600	"6000000009401513008"
#   P26 spouse = Q5542622 Johan Adelswärd
Q110547956	P26	Q5542622	S2600	"6000000009401513008"
#   P2600 Geni.com profile ID = 6000000009401513008 Catharina Funck, qualified P1810 subject named as Catharina Funck
Q110547956	P2600	"6000000009401513008"	P1810	"Catharina Funck"
#   Q110547936 Johan Hultman Adelswärd: P40 child = Q5542622 Johan Adelswärd
Q110547936	P40	Q5542622	S2600	"6000000009401706934"
#   P26 spouse = Q110547941 Altea Silfverström
Q110547936	P26	Q110547941	S2600	"6000000009401706934"
#   P2600 Geni.com profile ID = 6000000009401706934 Johan Hultman Adelswärd, qualified P1810 subject named as Johan Hultman Hultman
Q110547936	P2600	"6000000009401706934"	P1810	"Johan Hultman Hultman"
#   Q141223553 Ragnhild Kristine Øystensdatter Nese: P40 child = Q141242551 Lars Osmundsen Nese
Q141223553	P40	Q141242551	S2600	"6000000010479856178"
#   P40 child = Q141242389 Christian Osmundsen Nese
Q141223553	P40	Q141242389	S2600	"6000000010479856178"
#   Q141242551 Lars Osmundsen Nese: P25 mother = Q141223553 Ragnhild Kristine Øystensdatter Nese
Q141242551	P25	Q141223553	S2600	"6000000010480210324"
#   Q122980318 Samuel Fredrik Åkerhielm af Margretelund: P40 child = Q6255155 Gustaf Fredrik Åkerhielm af Margretelund
Q122980318	P40	Q6255155	S2600	"6000000010573777066"
#   P2600 Geni.com profile ID = 6000000010573777066 Samuel Fredrik Åkerhielm af Margretelund, qualified P1810 subject named as Samuel Fredrik Åkerhielm af Margretelund
Q122980318	P2600	"6000000010573777066"	P1810	"Samuel Fredrik Åkerhielm af Margretelund"
#   Q98180381 Kristina Elisabeth Nordenadler: P40 child = Q6045829 Johan Teodor Petré
Q98180381	P40	Q6045829	S2600	"6000000010934387089"
#   P2600 Geni.com profile ID = 6000000010934387089 Kristina Elisabeth Nordenadler, qualified P1810 subject named as Kristina Elisabeth Nordenadler
Q98180381	P2600	"6000000010934387089"	P1810	"Kristina Elisabeth Nordenadler"
#   Q141223903 Elen Margrethe Stangeland: P25 mother = Q141217372 Berta Larsdatter Stangeland
Q141223903	P25	Q141217372	S2600	"6000000011039570406"
#   Q2424918 Tomas Ihre: P40 child = Q719983 Johan Ihre
Q2424918	P40	Q719983	S2600	"6000000011115929762"
#   P2600 Geni.com profile ID = 6000000011115929762 Tomas Ihre, qualified P1810 subject named as Tomas Ihre
Q2424918	P2600	"6000000011115929762"	P1810	"Tomas Ihre"
#   Q141242389 Christian Osmundsen Nese: P25 mother = Q141223553 Ragnhild Kristine Øystensdatter Nese
Q141242389	P25	Q141223553	S2600	"6000000011329696852"
#   Q127270462 Barbro Petré: P40 child = Q5807131 Mikael Hising
Q127270462	P40	Q5807131	S2600	"6000000011533077050"
#   P26 spouse = Q110313452 Carl Hising
Q127270462	P26	Q110313452	S2600	"6000000011533077050"
#   P2600 Geni.com profile ID = 6000000011533077050 Barbro Petré, qualified P1810 subject named as Barbro Petré
Q127270462	P2600	"6000000011533077050"	P1810	"Barbro Petré"
#   P735 given name = Q807877 Barbro
Q127270462	P735	Q807877
#   Q111989591 Margareta Frodbom: P40 child = Q5807136 Vilhelm Hising
Q111989591	P40	Q5807136	S2600	"6000000011533226330"
#   P40 child = Q3450190 Johan Hisinger till Fagervik
Q111989591	P40	Q3450190	S2600	"6000000011533226330"
#   P26 spouse = Q5807131 Mikael Hising
Q111989591	P26	Q5807131	S2600	"6000000011533226330"
#   P2600 Geni.com profile ID = 6000000011533226330 Margareta Frodbom, qualified P1810 subject named as Margareta Frodbom
Q111989591	P2600	"6000000011533226330"	P1810	"Margareta Frodbom"
#   P735 given name = Q8274988 Margareta
Q111989591	P735	Q8274988
#   Q3450190 Johan Hisinger till Fagervik: P25 mother = Q111989591 Margareta Frodbom
Q3450190	P25	Q111989591	S2600	"6000000011539184038"
#   Q4951688 Margareta Gyllenstierna af Fogelvik: P40 child = Q109296398 Fredrika Eleonora Arvidsdotter Horn af Ekebyholm
Q4951688	P40	Q109296398	S2600	"6000000011637291315"
#   P40 child = Q5813616 Adam Horn af Ekebyholm till Ekebyholm
Q4951688	P40	Q5813616	S2600	"6000000011637291315"
#   P40 child = Q19678400 Eva Horn af Ekebyholm
Q4951688	P40	Q19678400	S2600	"6000000011637291315"
#   P26 spouse = Q717179 Arvid Bernhard Horn af Ekebyholm
Q4951688	P26	Q717179	S2600	"6000000011637291315"
#   P2600 Geni.com profile ID = 6000000011637291315 Margareta Gyllenstierna af Fogelvik, qualified P1810 subject named as Margareta Gyllenstierna af Fogelvik
Q4951688	P2600	"6000000011637291315"	P1810	"Margareta Gyllenstierna af Fogelvik"
#   Q141242507 Hedvig Augusta af Söderling: P40 child = Q109829893 Ulrika Elisabet Hermelin
Q141242507	P40	Q109829893	S2600	"6000000011713042906"
#   Q109829893 Ulrika Elisabet Hermelin: P40 child = Q6092404 Samuel August Sandels
Q109829893	P40	Q6092404	S2600	"6000000011714588237"
#   P2600 Geni.com profile ID = 6000000011714588237 Ulrika Elisabet Hermelin, qualified P1810 subject named as Ulrika Elisabet Hermelin
Q109829893	P2600	"6000000011714588237"	P1810	"Ulrika Elisabet Hermelin"
#   P735 given name = Q18924998 Ulrika, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q109829893	P735	Q18924998	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16423275 Elisabet, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q109829893	P735	Q16423275	P1545	"2"	P3831	Q245025
#   Q141217393 Magdalena von Mentzer: P40 child = Q108937197 Catharina Charlotta Rudbeck
Q141217393	P40	Q108937197	S2600	"6000000012617083513"
#   Q6015299 Friherre Johan Magnus af Nordin: P40 child = Q6015181 Carl Johan af Nordin
Q6015299	P40	Q6015181	S2600	"6000000012734285538"
#   P2600 Geni.com profile ID = 6000000012734285538 Friherre Johan Magnus af Nordin, qualified P1810 subject named as Friherre Johan Magnus af Nordin
Q6015299	P2600	"6000000012734285538"	P1810	"Friherre Johan Magnus af Nordin"
#   Q99373530 Carl Magnus Nordin: P40 child = Q6015299 Friherre Johan Magnus af Nordin
Q99373530	P40	Q6015299	S2600	"6000000012736619268"
#   P40 child = Q4993033 Carl Gustaf Nordin
Q99373530	P40	Q4993033	S2600	"6000000012736619268"
#   P2600 Geni.com profile ID = 6000000012736619268 Carl Magnus Nordin, qualified P1810 subject named as Carl Magnus Nordin
Q99373530	P2600	"6000000012736619268"	P1810	"Carl Magnus Nordin"
#   Q104550158 Ernald Mattsson Forbes of Corsindae: P40 child = Q5735890 Arvid Ernaldsson Forbus till Kumo
Q104550158	P40	Q5735890	S2600	"6000000013007809177"
#   P26 spouse = Q104550167 Karin Mattsdotter Björnram
Q104550158	P26	Q104550167	S2600	"6000000013007809177"
#   P2600 Geni.com profile ID = 6000000013007809177 Ernald Mattsson Forbes of Corsindae, qualified P1810 subject named as Ernald Mattsson Forbes of Corsindae
Q104550158	P2600	"6000000013007809177"	P1810	"Ernald Mattsson Forbes of Corsindae"
#   Q124606874 Hans Didrik Mörner af Morlanda: P40 child = Q6001555 Carl Claes Mörner af Morlanda
Q124606874	P40	Q6001555	S2600	"6000000013257070935"
#   P2600 Geni.com profile ID = 6000000013257070935 Hans Didrik Mörner af Morlanda, qualified P1810 subject named as Hans Didrik Mörner af Morlanda
Q124606874	P2600	"6000000013257070935"	P1810	"Hans Didrik Mörner af Morlanda"
#   Q113007770 Maria Sofia Stierncrona: P40 child = Q5587236 Carl Johan Gyllenborg
Q113007770	P40	Q5587236	S2600	"6000000013296788468"
#   P26 spouse = Q763053 Henning Adolf Gyllenborg
Q113007770	P26	Q763053	S2600	"6000000013296788468"
#   P2600 Geni.com profile ID = 6000000013296788468 Maria Sofia Stierncrona, qualified P1810 subject named as Maria Sofia Welt
Q113007770	P2600	"6000000013296788468"	P1810	"Maria Sofia Welt"
#   Q141224751 Berta Serina Rasmusdatter Borsheim: P40 child = Q141242522 Jørgine Bergitte Paulsdatter Orre
Q141224751	P40	Q141242522	S2600	"6000000014522158621"
#   Q66711908 Anna Christina Bruncrona: P40 child = Q16945159 Nils Abraham Bruncrona
Q66711908	P40	Q16945159	S2600	"6000000017425559123"
#   P40 child = Q6060350 Lars Georg Rabenius
Q66711908	P40	Q6060350	S2600	"6000000017425559123"
#   P26 spouse = Q6060365 Olof Ingelsson Rabenius
Q66711908	P26	Q6060365	S2600	"6000000017425559123"
#   P2600 Geni.com profile ID = 6000000017425559123 Anna Christina Bruncrona, qualified P1810 subject named as Anna Christina Bruncrona
Q66711908	P2600	"6000000017425559123"	P1810	"Anna Christina Bruncrona"
#   Q141216401 Mariet Danielsdotter: P40 child = Q141242565 Per Andersson
Q141216401	P40	Q141242565	S2600	"6000000017535961052"
#   Q5745634 Elias Frondin: P40 child = Q5745627 Berge / Birger Frondin
Q5745634	P40	Q5745627	S2600	"6000000018625238474"
#   P2600 Geni.com profile ID = 6000000018625238474 Elias Frondin, qualified P1810 subject named as Elias Frondin
Q5745634	P2600	"6000000018625238474"	P1810	"Elias Frondin"
#   Q19976772 Simon Melander: P40 child = Q5983613 Daniel Melanderhielm
Q19976772	P40	Q5983613	S2600	"6000000018625507007"
#   P2600 Geni.com profile ID = 6000000018625507007 Simon Melander, qualified P1810 subject named as Simon Melander
Q19976772	P2600	"6000000018625507007"	P1810	"Simon Melander"
#   Q16649961 Olof Olofsson Nauclérus: P40 child = Q16649960 Olof Nauclér
Q16649961	P40	Q16649960	S2600	"6000000018985534304"
#   P2600 Geni.com profile ID = 6000000018985534304 Olof Olofsson Nauclérus, qualified P1810 subject named as Olof Olofsson Nauclérus
Q16649961	P2600	"6000000018985534304"	P1810	"Olof Olofsson Nauclérus"
#   Q141242565 Per Andersson: P25 mother = Q141216401 Mariet Danielsdotter
Q141242565	P25	Q141216401	S2600	"6000000019176344694"
#   Q116439449 Abraham Grafström: P40 child = Q490686 Anders Abraham Grafström
Q116439449	P40	Q490686	S2600	"6000000019583224446"
#   P2600 Geni.com profile ID = 6000000019583224446 Abraham Grafström, qualified P1810 subject named as Abraham Grafström
Q116439449	P2600	"6000000019583224446"	P1810	"Abraham Grafström"
#   P735 given name = Q4055996 Abraham
Q116439449	P735	Q4055996
#   Q5916183 Karl Johan Andersson Knös: P40 child = Q5916153 Anders Erik Knös
Q5916183	P40	Q5916153	S2600	"6000000019933609341"
#   P2600 Geni.com profile ID = 6000000019933609341 Karl Johan Andersson Knös, qualified P1810 subject named as Karl Johan Andersson Knös
Q5916183	P2600	"6000000019933609341"	P1810	"Karl Johan Andersson Knös"
#   Q141225080 Annie Stangeland: P25 mother = Q141223853 Rakel Rasmusdottir Borsheim
Q141225080	P25	Q141223853	S2600	"6000000020344692199"
#   Q141223853 Rakel Rasmusdottir Borsheim: P25 mother = Q141223503 Anne Berta Osmundsdatter Nese
Q141223853	P25	Q141223503	S2600	"6000000020344732085"
#   Q4988935 Brita Hedvig Wijnbladh: P40 child = Q5916183 Karl Johan Andersson Knös
Q4988935	P40	Q5916183	S2600	"6000000020393995501"
#   P40 child = Q4225027 Olof Andersson Knös
Q4988935	P40	Q4225027	S2600	"6000000020393995501"
#   P40 child = Q5916189 Gustaf Andersson Knös
Q4988935	P40	Q5916189	S2600	"6000000020393995501"
#   P26 spouse = Q5916162 Anders Olofsson Knös
Q4988935	P26	Q5916162	S2600	"6000000020393995501"
#   P2600 Geni.com profile ID = 6000000020393995501 Brita Hedvig Wijnbladh, qualified P1810 subject named as Brita Hedvig Wijnbladh
Q4988935	P2600	"6000000020393995501"	P1810	"Brita Hedvig Wijnbladh"
#   Q5916162 Anders Olofsson Knös: P40 child = Q5916183 Karl Johan Andersson Knös
Q5916162	P40	Q5916183	S2600	"6000000020394079179"
#   P40 child = Q4225027 Olof Andersson Knös
Q5916162	P40	Q4225027	S2600	"6000000020394079179"
#   P40 child = Q5916189 Gustaf Andersson Knös
Q5916162	P40	Q5916189	S2600	"6000000020394079179"
#   P26 spouse = Q4988935 Brita Hedvig Wijnbladh
Q5916162	P26	Q4988935	S2600	"6000000020394079179"
#   P2600 Geni.com profile ID = 6000000020394079179 Anders Olofsson Knös, qualified P1810 subject named as Anders Olofsson Knös
Q5916162	P2600	"6000000020394079179"	P1810	"Anders Olofsson Knös"
#   Q127270437 Kristina Samuelsdotter: P40 child = Q5773287 Samuel Andreæ Grubb
Q127270437	P40	Q5773287	S2600	"6000000023140541858"
#   P2600 Geni.com profile ID = 6000000023140541858 Kristina Samuelsdotter, qualified P1810 subject named as Kristina Samuelsdotter
Q127270437	P2600	"6000000023140541858"	P1810	"Kristina Samuelsdotter"
#   Q66316940 Anna Sofia Bäck: P40 child = Q2694124 Albrecht Elof Ihre d.y.
Q66316940	P40	Q2694124	S2600	"6000000024161876529"
#   P26 spouse = Q5822415 Albrecht Ihre
Q66316940	P26	Q5822415	S2600	"6000000024161876529"
#   P2600 Geni.com profile ID = 6000000024161876529 Anna Sofia Bäck, qualified P1810 subject named as Anna Sofia Bäck
Q66316940	P2600	"6000000024161876529"	P1810	"Anna Sofia Bäck"
#   Q141225793 Laurentius Andreae Andreae Alstrinius: P26 spouse = Q141225779 Kristina Eriksdotter Ångerman
Q141225793	P26	Q141225779	S2600	"6000000025011507008"
#   Q16650170 Ingeldus Laurentii Rabenius: P40 child = Q6060365 Olof Ingelsson Rabenius
Q16650170	P40	Q6060365	S2600	"6000000028475780607"
#   P2600 Geni.com profile ID = 6000000028475780607 Ingeldus Laurentii Rabenius, qualified P1810 subject named as Ingeldus Laurentii Rabenius
Q16650170	P2600	"6000000028475780607"	P1810	"Ingeldus Laurentii Rabenius"
#   Q141225175 Malene Larsdtr. Alvseike: P25 mother = Q141217369 Anna Osmundsd Stokka
Q141225175	P25	Q141217369	S2600	"6000000030085852982"
#   Q141224339 Reinhert Borsheim: P25 mother = Q141223853 Rakel Rasmusdottir Borsheim
Q141224339	P25	Q141223853	S2600	"6000000032068841409"
#   Q141242412 Peder Paulsen Borsok: P26 spouse = Q141242379 Berte Karlsdatter Borsok
Q141242412	P26	Q141242379	S2600	"6000000035525387457"
#   Q141242379 Berte Karlsdatter Borsok: P26 spouse = Q141242412 Peder Paulsen Borsok
Q141242379	P26	Q141242412	S2600	"6000000035525469386"
#   Q141225779 Kristina Eriksdotter Ångerman: P26 spouse = Q141225793 Laurentius Andreae Andreae Alstrinius
Q141225779	P26	Q141225793	S2600	"6000000038458498753"
#   Q141223732 Guttorm Guttormsson: P25 mother = Q141216349 Ingrid Guttormsdotter
Q141223732	P25	Q141216349	S2600	"6000000040760707837"
#   Q141219250 Inger Sørensdatter Lima: P25 mother = Q141219065 Marta Torbjørnsdotter Gjesdal
Q141219250	P25	Q141219065	S2600	"6000000065991527068"
#   Q141242522 Jørgine Bergitte Paulsdatter Orre: P25 mother = Q141224751 Berta Serina Rasmusdatter Borsheim
Q141242522	P25	Q141224751	S2600	"6000000077299441506"
#   Q141223849 Ola Helgeson Lima: P25 mother = Q141219250 Inger Sørensdatter Lima
Q141223849	P25	Q141219250	S2600	"6000000116694298987"
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

