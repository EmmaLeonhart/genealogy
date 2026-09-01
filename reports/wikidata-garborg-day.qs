# ========================================================================
# NAME ITEMS FIRST. One file, her instruction of 2026-08-30 -- there is no
# longer a second batch to remember to run.
# ========================================================================
# Name items the Garborg batches need, AND the statements that use them.
#
# Each CREATE is followed by `Qperson  Pprop  LAST` for every bearer who
# ALREADY holds a QID -- LAST is exactly how you point at what was just
# created. A person this run is also CREATING cannot be linked here, because
# LAST would then name the person; they wait for the next run.
#
# A patronymic is its own item even where the spelling exists as a given
# name: CLAUDE.md, one name item per USAGE. Emma's Q141152710 Aadnesson is
# the pattern -- labels, P31, nothing else.

# Frondin -- family, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Frondin"
LAST	Len	"Frondin"
#   set the mul label to "Frondin"
LAST	Lmul	"Frondin"
#   set the en description to "family name"
LAST	Den	"family name"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q141223420 Gunilla Margareta Frondin: P734 family name = the item just created, qualified P3831 object of statement has role Q28418670 married name
Q141223420	P734	LAST	P3831	Q28418670	S2600	"6000000011759927315"
#   Q5745634 Elias Frondin: P734 family name = the item just created
Q5745634	P734	LAST	S2600	"6000000018625238474"
#   Q5745627 Berge / Birger Frondin: P734 family name = the item just created
Q5745627	P734	LAST	S2600	"6000000020128505901"

# Nedre -- family, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Nedre"
LAST	Len	"Nedre"
#   set the mul label to "Nedre"
LAST	Lmul	"Nedre"
#   set the en description to "family name"
LAST	Den	"family name"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q141216644 Rasmus Asbjørnson Nedre Rossavik: P734 family name = the item just created
Q141216644	P734	LAST	S2600	"6000000003192698959"
#   Q141224008 Gjøa Gunnbjørnsdatter Nedre Rossavik: P734 family name = the item just created, qualified P3831 object of statement has role Q28418670 married name
Q141224008	P734	LAST	P3831	Q28418670	S2600	"6000000005609443674"
#   Q141216599 Anna Rasmusdatter Nedre Rossavik: P734 family name = the item just created
Q141216599	P734	LAST	S2600	"6000000008916446714"

# Olofsdotter -- patronymic, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Olofsdotter"
LAST	Len	"Olofsdotter"
#   set the mul label to "Olofsdotter"
LAST	Lmul	"Olofsdotter"
#   set the en description to "patronymic"
LAST	Den	"patronymic"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141216618 Karin Olofsdotter: P5056 patronym or matronym = the item just created, qualified P144 based on Q141216403 Olof Nilsson
Q141216618	P5056	LAST	P144	Q141216403	S2600	"348968026630001429"
#   Q141224093 Beata Magdalena Olofsdotter Mellberg: P5056 patronym or matronym = the item just created
Q141224093	P5056	LAST	S2600	"6000000001865185124"
#   Q141249729 Kristina Olofsdotter Spaak: P5056 patronym or matronym = the item just created
Q141249729	P5056	LAST	S2600	"6000000006897337018"
#   Q141244092 Christina Olofsdotter Hammar: P5056 patronym or matronym = the item just created
Q141244092	P5056	LAST	S2600	"6000000009492573975"

# 305 more name items are needed and wait for a later
# run -- 3 a day is her cap, not a limit of the data:
#   Pedersdatter (patronymic), 4 bearer(s)
#   Tollefson (patronymic), 4 bearer(s)
#   Bjørnson (patronymic), 3 bearer(s)
#   Garfve (family), 3 bearer(s)
#   Hansson (patronymic), 3 bearer(s)
#   Helgesen (patronymic), 3 bearer(s)
#   Høle (family), 3 bearer(s)
#   Ingebretsdatter (patronymic), 3 bearer(s)
#   Kristiansen (patronymic), 3 bearer(s)
#   Larsdatter (patronymic), 3 bearer(s)
#   Larsson (patronymic), 3 bearer(s)
#   Låge-Håland (family), 3 bearer(s)
#   ... and 293 more

# ========================================================================
# THE DAY'S PEOPLE
# ========================================================================

# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   2658 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   Q141250216 Bjørn Gunnarson Mele: add a mul alias "Bjørn Gunnarson Gunnarson"
Q141250216	Amul	"Bjørn Gunnarson Gunnarson"
#   Q550343 Welf: add a mul alias "Welf I & IV"
Q550343	Amul	"Welf I & IV"
#   set the mul label to "Welf I, Duke of Bavaria"
Q550343	Lmul	"Welf I, Duke of Bavaria"
#   set the ja label to "ヴェルフ・I・デューク・オフ・バイエルン"
Q550343	Lja	"ヴェルフ・I・デューク・オフ・バイエルン"
#   set the zh label to "韦尔夫·I·杜克·奥夫·拜恩"
Q550343	Lzh	"韦尔夫·I·杜克·奥夫·拜恩"
#   set the ko label to "웨르프 이 두케 오프 바바리아"
Q550343	Lko	"웨르프 이 두케 오프 바바리아"
#   Q75917080 Catherine Constantia Pellew: set the ja label to "キャサリン・コンスタンティア・ペレヴ"
Q75917080	Lja	"キャサリン・コンスタンティア・ペレヴ"
#   set the zh label to "凯瑟琳·孔斯坦蒂阿·佩莱夫"
Q75917080	Lzh	"凯瑟琳·孔斯坦蒂阿·佩莱夫"
#   set the ko label to "카테리네 콘스탄티아 펠레우"
Q75917080	Lko	"카테리네 콘스탄티아 펠레우"
#   set the ja label to "カール・ラゲルボルグ"
Q135441621	Lja	"カール・ラゲルボルグ"
#   set the zh label to "卡尔·拉盖尔博尔格"
Q135441621	Lzh	"卡尔·拉盖尔博尔格"
#   set the ko label to "카르르 라게르보르그"
Q135441621	Lko	"카르르 라게르보르그"
#   Q56403540 Daniel Lindh: set the ja label to "ダニエル・リンド"
Q56403540	Lja	"ダニエル・リンド"
#   set the zh label to "丹尼尔·林德"
Q56403540	Lzh	"丹尼尔·林德"
#   set the ko label to "다니엘 린드흐"
Q56403540	Lko	"다니엘 린드흐"

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the mul label to "NN"
LAST	Lmul	"NN"
#   set the ca label to "esposa de Glen Archie Tunheim"
LAST	Lca	"esposa de Glen Archie Tunheim"
#   set the da label to "hustru til Glen Archie Tunheim"
LAST	Lda	"hustru til Glen Archie Tunheim"
#   set the de label to "Ehefrau von Glen Archie Tunheim"
LAST	Lde	"Ehefrau von Glen Archie Tunheim"
#   set the en label to "wife of Glen Archie Tunheim"
LAST	Len	"wife of Glen Archie Tunheim"
#   set the es label to "esposa de Glen Archie Tunheim"
LAST	Les	"esposa de Glen Archie Tunheim"
#   set the fr label to "épouse de Glen Archie Tunheim"
LAST	Lfr	"épouse de Glen Archie Tunheim"
#   set the it label to "moglie di Glen Archie Tunheim"
LAST	Lit	"moglie di Glen Archie Tunheim"
#   set the ja label to "グレン・アーチー・トゥンヘイムの妻"
LAST	Lja	"グレン・アーチー・トゥンヘイムの妻"
#   set the ko label to "그렌 아르치에 툰헤임의 아내"
LAST	Lko	"그렌 아르치에 툰헤임의 아내"
#   set the nb label to "hustru til Glen Archie Tunheim"
LAST	Lnb	"hustru til Glen Archie Tunheim"
#   set the nl label to "echtgenote van Glen Archie Tunheim"
LAST	Lnl	"echtgenote van Glen Archie Tunheim"
#   set the pt label to "esposa de Glen Archie Tunheim"
LAST	Lpt	"esposa de Glen Archie Tunheim"
#   set the sv label to "maka till Glen Archie Tunheim"
LAST	Lsv	"maka till Glen Archie Tunheim"
#   set the zh label to "格伦·阿奇·通海姆之妻"
LAST	Lzh	"格伦·阿奇·通海姆之妻"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000180037076876
LAST	P2600	"6000000180037076876"
#   P26 spouse = Q141223515 Glen Archie Tunheim
LAST	P26	Q141223515	S2600	"6000000180037076876"
#   Q141223515 Glen Archie Tunheim: P26 spouse = the item just created
Q141223515	P26	LAST	S2600	"6000000180037076876"

# create a new item
CREATE
#   the item just created: set the en label to "Anna Ormsd Byre"
LAST	Len	"Anna Ormsd Byre"
#   set the mul label to "Anna Ormsd Byre"
LAST	Lmul	"Anna Ormsd Byre"
#   set the ja label to "アンナ・オルムスド・ビレ"
LAST	Lja	"アンナ・オルムスド・ビレ"
#   set the zh label to "安娜·奥尔姆斯德·比雷"
LAST	Lzh	"安娜·奥尔姆斯德·比雷"
#   set the ko label to "안나 오르므스드 비레"
LAST	Lko	"안나 오르므스드 비레"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000002376475916 Anna Ormsd Byre, qualified P1810 subject named as Anna Ormsd Byre
LAST	P2600	"6000000002376475916"	P1810	"Anna Ormsd Byre"
#   P569 date of birth = +1538-00-00T00:00:00Z/9
LAST	P569	+1538-00-00T00:00:00Z/9	S2600	"6000000002376475916"
#   P570 date of death = +1599-00-00T00:00:00Z/9
LAST	P570	+1599-00-00T00:00:00Z/9	S2600	"6000000002376475916"
#   P22 father = Q141216499 Orm Ånonsen
LAST	P22	Q141216499	S2600	"6000000002376475916"
#   P25 mother = Q141216598 Anna Ivarsd Stokka
LAST	P25	Q141216598	S2600	"6000000002376475916"
#   P40 child = Q141206080 Peder Tormodsen Foss
LAST	P40	Q141206080	S2600	"6000000002376475916"
#   Q141216499 Orm Ånonsen: P40 child = the item just created
Q141216499	P40	LAST	S2600	"6000000002376475916"
#   Q141216598 Anna Ivarsd Stokka: P40 child = the item just created
Q141216598	P40	LAST	S2600	"6000000002376475916"
#   Q141206080 Peder Tormodsen Foss: P25 mother = the item just created
Q141206080	P25	LAST	S2600	"6000000002376475916"
#   the item just created: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P734 family name = Q37515983
LAST	P734	Q37515983
#   add a mul alias "Anna Ormsd Stokka Byre"
LAST	Amul	"Anna Ormsd Stokka Byre"

# create a new item
CREATE
#   set the en label to "Beata Behmer"
LAST	Len	"Beata Behmer"
#   set the mul label to "Beata Behmer"
LAST	Lmul	"Beata Behmer"
#   set the ja label to "ベアタ・ベメル"
LAST	Lja	"ベアタ・ベメル"
#   set the zh label to "贝阿塔·贝梅尔"
LAST	Lzh	"贝阿塔·贝梅尔"
#   set the ko label to "베아타 베흐메르"
LAST	Lko	"베아타 베흐메르"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000007486728223 Beata Behmer, qualified P1810 subject named as Beata Behmer
LAST	P2600	"6000000007486728223"	P1810	"Beata Behmer"
#   P569 date of birth = +1670-06-25T00:00:00Z/11
LAST	P569	+1670-06-25T00:00:00Z/11	S2600	"6000000007486728223"
#   P570 date of death = +1712-00-00T00:00:00Z/9
LAST	P570	+1712-00-00T00:00:00Z/9	S2600	"6000000007486728223"
#   P22 father = Q5568857 Daniel Jonsson Behmer
LAST	P22	Q5568857	S2600	"6000000007486728223"
#   Q5568857 Daniel Jonsson Behmer: P40 child = the item just created
Q5568857	P40	LAST	S2600	"6000000007486728223"
#   the item just created: P735 given name = Q338015 Beata
LAST	P735	Q338015

# create a new item
CREATE
#   set the en label to "Beata Fredrika Charlotta Wrangel af Sauss"
LAST	Len	"Beata Fredrika Charlotta Wrangel af Sauss"
#   set the mul label to "Beata Fredrika Charlotta Wrangel af Sauss"
LAST	Lmul	"Beata Fredrika Charlotta Wrangel af Sauss"
#   set the ja label to "ベアタ・フレデリカ・カルロタ・ウランゲル・アフ・サウス"
LAST	Lja	"ベアタ・フレデリカ・カルロタ・ウランゲル・アフ・サウス"
#   set the zh label to "贝阿塔·夫雷德里卡·卡尔洛塔·弗兰格尔·阿夫·萨乌斯"
LAST	Lzh	"贝阿塔·夫雷德里卡·卡尔洛塔·弗兰格尔·阿夫·萨乌斯"
#   set the ko label to "베아타 프레드리카 차르로타 우라엘 아프 사우스"
LAST	Lko	"베아타 프레드리카 차르로타 우라엘 아프 사우스"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000007509814422 Beata Fredrika Charlotta Wrangel af Sauss, qualified P1810 subject named as Beata Fredrika Charlotta Wrangel af Sauss
LAST	P2600	"6000000007509814422"	P1810	"Beata Fredrika Charlotta Wrangel af Sauss"
#   P569 date of birth = +1812-03-03T00:00:00Z/11
LAST	P569	+1812-03-03T00:00:00Z/11	S2600	"6000000007509814422"
#   P570 date of death = +1837-08-03T00:00:00Z/11
LAST	P570	+1837-08-03T00:00:00Z/11	S2600	"6000000007509814422"
#   P26 spouse = Q6175942 David Wilhelm Silfverstolpe
LAST	P26	Q6175942	S2600	"6000000007509814422"
#   Q6175942 David Wilhelm Silfverstolpe: P26 spouse = the item just created
Q6175942	P26	LAST	S2600	"6000000007509814422"
#   the item just created: P735 given name = Q338015 Beata, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q338015	P1545	"1"	P7452	Q3409033
#   P735 given name = Q5499550 Fredrika, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q5499550	P1545	"2"	P3831	Q245025
#   P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1067071	P1545	"3"	P3831	Q245025
#   P734 family name = Q35930488 Wrangel, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q35930488	P3831	Q28418670

# create a new item
CREATE
#   set the en label to "Catharina Björnklou"
LAST	Len	"Catharina Björnklou"
#   set the mul label to "Catharina Björnklou"
LAST	Lmul	"Catharina Björnklou"
#   set the ja label to "カタリーナ・ブヨルンクロウ"
LAST	Lja	"カタリーナ・ブヨルンクロウ"
#   set the zh label to "卡塔里娜·布约尔恩克洛乌"
LAST	Lzh	"卡塔里娜·布约尔恩克洛乌"
#   set the ko label to "카타리나 브죄르느크루"
LAST	Lko	"카타리나 브죄르느크루"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000006634676009 Catharina Björnklou, qualified P1810 subject named as Catharina Björnklou
LAST	P2600	"6000000006634676009"	P1810	"Catharina Björnklou"
#   P570 date of death = +1678-00-00T00:00:00Z/9
LAST	P570	+1678-00-00T00:00:00Z/9	S2600	"6000000006634676009"
#   P40 child = Q141249730 Margareta Catharina Clo
LAST	P40	Q141249730	S2600	"6000000006634676009"
#   Q141249730 Margareta Catharina Clo: P25 mother = the item just created
Q141249730	P25	LAST	S2600	"6000000006634676009"
#   the item just created: P735 given name = Q17317997 Catharina
LAST	P735	Q17317997

# create a new item
CREATE
#   set the en label to "Claes Sandels"
LAST	Len	"Claes Sandels"
#   set the mul label to "Claes Sandels"
LAST	Lmul	"Claes Sandels"
#   set the ja label to "クレス・サンデルス"
LAST	Lja	"クレス・サンデルス"
#   set the zh label to "克拉斯·桑德尔斯"
LAST	Lzh	"克拉斯·桑德尔斯"
#   set the ko label to "크래스 산델스"
LAST	Lko	"크래스 산델스"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000042116230266 Claes Sandels, qualified P1810 subject named as Claes Sandels
LAST	P2600	"6000000042116230266"	P1810	"Claes Sandels"
#   P569 date of birth = +1873-09-07T00:00:00Z/11
LAST	P569	+1873-09-07T00:00:00Z/11	S2600	"6000000042116230266"
#   P570 date of death = +1962-04-27T00:00:00Z/11
LAST	P570	+1962-04-27T00:00:00Z/11	S2600	"6000000042116230266"
#   P26 spouse = Q141244220 Herta Lovisa Charlotta Sandels
LAST	P26	Q141244220	S2600	"6000000042116230266"
#   P40 child = Q4976863 Stina Claesdotter Sandels
LAST	P40	Q4976863	S2600	"6000000042116230266"
#   Q141244220 Herta Lovisa Charlotta Sandels: P26 spouse = the item just created
Q141244220	P26	LAST	S2600	"6000000042116230266"
#   Q4976863 Stina Claesdotter Sandels: P22 father = the item just created
Q4976863	P22	LAST	S2600	"6000000042116230266"
#   the item just created: P735 given name = Q19818179 Claes
LAST	P735	Q19818179

# create a new item
CREATE
#   set the en label to "Conrad von Braunjohan"
LAST	Len	"Conrad von Braunjohan"
#   set the mul label to "Conrad von Braunjohan"
LAST	Lmul	"Conrad von Braunjohan"
#   set the ja label to "コンラッド・ヴォン・ブラウンヨハン"
LAST	Lja	"コンラッド・ヴォン・ブラウンヨハン"
#   set the zh label to "康拉德·翁·布拉温约汉"
LAST	Lzh	"康拉德·翁·布拉温约汉"
#   set the ko label to "콘라드 본 브라우노한"
LAST	Lko	"콘라드 본 브라우노한"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000006436219130 Conrad von Braunjohan, qualified P1810 subject named as Conrad von Braunjohan
LAST	P2600	"6000000006436219130"	P1810	"Conrad von Braunjohan"
#   P569 date of birth = +1636-11-12T00:00:00Z/11
LAST	P569	+1636-11-12T00:00:00Z/11	S2600	"6000000006436219130"
#   P570 date of death = +1691-04-13T00:00:00Z/11
LAST	P570	+1691-04-13T00:00:00Z/11	S2600	"6000000006436219130"
#   P40 child = Q141249724 Carl Rutger von Braunjohan
LAST	P40	Q141249724	S2600	"6000000006436219130"
#   Q141249724 Carl Rutger von Braunjohan: P22 father = the item just created
Q141249724	P22	LAST	S2600	"6000000006436219130"
#   the item just created: P735 given name = Q17436400 Conrad
LAST	P735	Q17436400

# create a new item
CREATE
#   set the en label to "Erik Christophersson Boije"
LAST	Len	"Erik Christophersson Boije"
#   set the mul label to "Erik Christophersson Boije"
LAST	Lmul	"Erik Christophersson Boije"
#   set the ja label to "エリック・クリストプヘルソン・ボイイェ"
LAST	Lja	"エリック・クリストプヘルソン・ボイイェ"
#   set the zh label to "埃里克·克里斯托普赫尔松·博伊耶"
LAST	Lzh	"埃里克·克里斯托普赫尔松·博伊耶"
#   set the ko label to "에리크 크리스토페르손 보이제"
LAST	Lko	"에리크 크리스토페르손 보이제"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000026435776251 Erik Christophersson Boije, qualified P1810 subject named as Erik Christophersson Boije
LAST	P2600	"6000000026435776251"	P1810	"Erik Christophersson Boije"
#   P570 date of death = +1698-00-00T00:00:00Z/9
LAST	P570	+1698-00-00T00:00:00Z/9	S2600	"6000000026435776251"
#   P40 child = Q141242498 Elisabet Boije
LAST	P40	Q141242498	S2600	"6000000026435776251"
#   Q141242498 Elisabet Boije: P22 father = the item just created
Q141242498	P22	LAST	S2600	"6000000026435776251"
#   the item just created: P735 given name = Q750186 Erik
LAST	P735	Q750186
#   P734 family name = Q28149669 Boije
LAST	P734	Q28149669
#   add a mul alias "Erik Boije"
LAST	Amul	"Erik Boije"

# create a new item
CREATE
#   set the en label to "Hanna Regine Halvardsdatter Larsen"
LAST	Len	"Hanna Regine Halvardsdatter Larsen"
#   set the mul label to "Hanna Regine Halvardsdatter Larsen"
LAST	Lmul	"Hanna Regine Halvardsdatter Larsen"
#   add a mul alias "Hanna Regine Halvardsdatter Årsvoll"
LAST	Amul	"Hanna Regine Halvardsdatter Årsvoll"
#   set the ja label to "ハンナ・レギネ・ハルヴァルドスダッテル・ラーセン"
LAST	Lja	"ハンナ・レギネ・ハルヴァルドスダッテル・ラーセン"
#   set the zh label to "汉娜·雷吉内·哈尔瓦尔德斯达特·拉森"
LAST	Lzh	"汉娜·雷吉内·哈尔瓦尔德斯达特·拉森"
#   set the ko label to "한나 레기네 할바르드스다테르 라르센"
LAST	Lko	"한나 레기네 할바르드스다테르 라르센"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000026477018004 Hanna Regine Halvardsdatter Larsen, qualified P1810 subject named as Hanna Regine Halvardsdatter Årsvoll
LAST	P2600	"6000000026477018004"	P1810	"Hanna Regine Halvardsdatter Årsvoll"
#   P569 date of birth = +1853-11-29T00:00:00Z/11
LAST	P569	+1853-11-29T00:00:00Z/11	S2600	"6000000026477018004"
#   P25 mother = Q141225244 Rakel Maria Govertsdatter Årsvoll
LAST	P25	Q141225244	S2600	"6000000026477018004"
#   Q141225244 Rakel Maria Govertsdatter Årsvoll: P40 child = the item just created
Q141225244	P40	LAST	S2600	"6000000026477018004"
#   the item just created: P735 given name = Q1554377 Hannah, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q1554377	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18179222 Regine, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q18179222	P1545	"2"	P3831	Q245025
#   P734 family name = Q13099004 Larsen, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q13099004	P3831	Q28418670
#   add a mul alias "Hanna Regine Larsen"
LAST	Amul	"Hanna Regine Larsen"

# create a new item
CREATE
#   set the en label to "Hans Jonsson"
LAST	Len	"Hans Jonsson"
#   set the mul label to "Hans Jonsson"
LAST	Lmul	"Hans Jonsson"
#   set the ja label to "ハンス・ヨンソン"
LAST	Lja	"ハンス・ヨンソン"
#   set the zh label to "汉斯·永松"
LAST	Lzh	"汉斯·永松"
#   set the ko label to "한스 존손"
LAST	Lko	"한스 존손"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 1899596 Hans Jonsson, qualified P1810 subject named as Hans Jonsson
LAST	P2600	"1899596"	P1810	"Hans Jonsson"
#   P569 date of birth = +1739-12-05T00:00:00Z/11
LAST	P569	+1739-12-05T00:00:00Z/11	S2600	"1899596"
#   P570 date of death = +1800-00-00T00:00:00Z/9
LAST	P570	+1800-00-00T00:00:00Z/9	S2600	"1899596"
#   P40 child = Q5976894 Gabriel Hansson Marklin
LAST	P40	Q5976894	S2600	"1899596"
#   Q5976894 Gabriel Hansson Marklin: P22 father = the item just created
Q5976894	P22	LAST	S2600	"1899596"
#   the item just created: P735 given name = Q632842
LAST	P735	Q632842

# create a new item
CREATE
#   set the en label to "Jakob Henrik Forbus"
LAST	Len	"Jakob Henrik Forbus"
#   set the mul label to "Jakob Henrik Forbus"
LAST	Lmul	"Jakob Henrik Forbus"
#   set the ja label to "ヤーコプ・ヘンリク・フォルブス"
LAST	Lja	"ヤーコプ・ヘンリク・フォルブス"
#   set the zh label to "雅各布·亨里克·福尔布斯"
LAST	Lzh	"雅各布·亨里克·福尔布斯"
#   set the ko label to "자콥 헨리크 포르부스"
LAST	Lko	"자콥 헨리크 포르부스"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000090769932838 Jakob Henrik Forbus, qualified P1810 subject named as Jakob Henrik Forbus
LAST	P2600	"6000000090769932838"	P1810	"Jakob Henrik Forbus"
#   P569 date of birth = +1640-12-20T00:00:00Z/11
LAST	P569	+1640-12-20T00:00:00Z/11	S2600	"6000000090769932838"
#   P570 date of death = +1664-01-19T00:00:00Z/11
LAST	P570	+1664-01-19T00:00:00Z/11	S2600	"6000000090769932838"
#   P22 father = Q5735890 Arvid Ernaldsson Forbus till Kumo
LAST	P22	Q5735890	S2600	"6000000090769932838"
#   Q5735890 Arvid Ernaldsson Forbus till Kumo: P40 child = the item just created
Q5735890	P40	LAST	S2600	"6000000090769932838"
#   the item just created: P735 given name = Q16747395, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q16747395	P1545	"1"	P7452	Q3409033
#   P735 given name = Q594279 Henrik, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q594279	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Jakob Jonasson Bure"
LAST	Len	"Jakob Jonasson Bure"
#   set the mul label to "Jakob Jonasson Bure"
LAST	Lmul	"Jakob Jonasson Bure"
#   set the ja label to "ヤーコプ・ヨナソン・ブレ"
LAST	Lja	"ヤーコプ・ヨナソン・ブレ"
#   set the zh label to "雅各布·约纳松·布雷"
LAST	Lzh	"雅各布·约纳松·布雷"
#   set the ko label to "자콥 조나손 부레"
LAST	Lko	"자콥 조나손 부레"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000089104937893 Jakob Jonasson Bure, qualified P1810 subject named as Jakob Jonasson Bure
LAST	P2600	"6000000089104937893"	P1810	"Jakob Jonasson Bure"
#   P22 father = Q5590143 Jonas Engelbertsson Bure
LAST	P22	Q5590143	S2600	"6000000089104937893"
#   Q5590143 Jonas Engelbertsson Bure: P40 child = the item just created
Q5590143	P40	LAST	S2600	"6000000089104937893"
#   the item just created: P735 given name = Q16747395
LAST	P735	Q16747395
#   P734 family name = Q11335012 Bure
LAST	P734	Q11335012
#   add a mul alias "Jakob Bure"
LAST	Amul	"Jakob Bure"

# create a new item
CREATE
#   set the en label to "Johan Ståhlbom"
LAST	Len	"Johan Ståhlbom"
#   set the mul label to "Johan Ståhlbom"
LAST	Lmul	"Johan Ståhlbom"
#   set the ja label to "ヨハン・ストールボム"
LAST	Lja	"ヨハン・ストールボム"
#   set the zh label to "约翰·斯托尔博姆"
LAST	Lzh	"约翰·斯托尔博姆"
#   set the ko label to "조한 스토흐르봄"
LAST	Lko	"조한 스토흐르봄"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000007367592462 Johan Ståhlbom, qualified P1810 subject named as Johan Ståhlbom
LAST	P2600	"6000000007367592462"	P1810	"Johan Ståhlbom"
#   P569 date of birth = +1638-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P569	+1638-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"6000000007367592462"
#   P570 date of death = +1678-05-01T00:00:00Z/11
LAST	P570	+1678-05-01T00:00:00Z/11	S2600	"6000000007367592462"
#   P40 child = Q141225772 Katarina Johansdotter Ståhlbom
LAST	P40	Q141225772	S2600	"6000000007367592462"
#   Q141225772 Katarina Johansdotter Ståhlbom: P22 father = the item just created
Q141225772	P22	LAST	S2600	"6000000007367592462"

# create a new item
CREATE
#   the item just created: set the en label to "Jon Voster"
LAST	Len	"Jon Voster"
#   set the mul label to "Jon Voster"
LAST	Lmul	"Jon Voster"
#   set the ja label to "ジョン・ヴォステル"
LAST	Lja	"ジョン・ヴォステル"
#   set the zh label to "乔恩·沃斯特尔"
LAST	Lzh	"乔恩·沃斯特尔"
#   set the ko label to "존 보스테르"
LAST	Lko	"존 보스테르"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000007980605167 Jon Voster, qualified P1810 subject named as Jon Voster
LAST	P2600	"6000000007980605167"	P1810	"Jon Voster"
#   P569 date of birth = +1525-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P569	+1525-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"6000000007980605167"
#   P570 date of death = +1574-00-00T00:00:00Z/9
LAST	P570	+1574-00-00T00:00:00Z/9	S2600	"6000000007980605167"
#   P40 child = Q141242562 Peder Jonsen Voster
LAST	P40	Q141242562	S2600	"6000000007980605167"
#   Q141242562 Peder Jonsen Voster: P22 father = the item just created
Q141242562	P22	LAST	S2600	"6000000007980605167"
#   the item just created: P735 given name = Q13501137 Jon
LAST	P735	Q13501137

# create a new item
CREATE
#   set the en label to "Karl Torsen Kalberg"
LAST	Len	"Karl Torsen Kalberg"
#   set the mul label to "Karl Torsen Kalberg"
LAST	Lmul	"Karl Torsen Kalberg"
#   set the ja label to "カール・トルセン・カルベルグ"
LAST	Lja	"カール・トルセン・カルベルグ"
#   set the zh label to "卡尔·托尔森·卡尔贝尔格"
LAST	Lzh	"卡尔·托尔森·卡尔贝尔格"
#   set the ko label to "카르르 토르센 칼베르그"
LAST	Lko	"카르르 토르센 칼베르그"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000009109484400 Karl Torsen Kalberg, qualified P1810 subject named as Karl Torsen Kalberg
LAST	P2600	"6000000009109484400"	P1810	"Karl Torsen Kalberg"
#   P569 date of birth = +1745-00-00T00:00:00Z/9
LAST	P569	+1745-00-00T00:00:00Z/9	S2600	"6000000009109484400"
#   P40 child = Q141242379 Berte Karlsdatter Borsok
LAST	P40	Q141242379	S2600	"6000000009109484400"
#   Q141242379 Berte Karlsdatter Borsok: P22 father = the item just created
Q141242379	P22	LAST	S2600	"6000000009109484400"

# create a new item
CREATE
#   the item just created: set the en label to "Lars Mauritz Wilhelm Silfverstolpe"
LAST	Len	"Lars Mauritz Wilhelm Silfverstolpe"
#   set the mul label to "Lars Mauritz Wilhelm Silfverstolpe"
LAST	Lmul	"Lars Mauritz Wilhelm Silfverstolpe"
#   set the ja label to "ラース・マウリッツ・ヴィルヘルム・シルフヴェルストルペ"
LAST	Lja	"ラース・マウリッツ・ヴィルヘルム・シルフヴェルストルペ"
#   set the zh label to "拉尔斯·马乌里特兹·威廉·西尔夫韦尔斯托尔佩"
LAST	Lzh	"拉尔斯·马乌里特兹·威廉·西尔夫韦尔斯托尔佩"
#   set the ko label to "라르스 마우리트즈 위르헬므 실프베르스톨페"
LAST	Lko	"라르스 마우리트즈 위르헬므 실프베르스톨페"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000007510197248 Lars Mauritz Wilhelm Silfverstolpe, qualified P1810 subject named as Lars Mauritz Wilhelm Silfverstolpe
LAST	P2600	"6000000007510197248"	P1810	"Lars Mauritz Wilhelm Silfverstolpe"
#   P569 date of birth = +1836-01-01T00:00:00Z/11
LAST	P569	+1836-01-01T00:00:00Z/11	S2600	"6000000007510197248"
#   P570 date of death = +1884-07-12T00:00:00Z/11
LAST	P570	+1884-07-12T00:00:00Z/11	S2600	"6000000007510197248"
#   P22 father = Q6175942 David Wilhelm Silfverstolpe
LAST	P22	Q6175942	S2600	"6000000007510197248"
#   Q6175942 David Wilhelm Silfverstolpe: P40 child = the item just created
Q6175942	P40	LAST	S2600	"6000000007510197248"
#   the item just created: P735 given name = Q15635262 Lars, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q15635262	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18760871 Mauritz, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q18760871	P1545	"2"	P3831	Q245025
#   P735 given name = Q11027623, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
LAST	P735	Q11027623	P1545	"3"	P3831	Q245025

# create a new item
CREATE
#   set the mul label to "NN"
LAST	Lmul	"NN"
#   set the ca label to "mare de Villum Jonsen Gautun"
LAST	Lca	"mare de Villum Jonsen Gautun"
#   set the da label to "mor til Villum Jonsen Gautun"
LAST	Lda	"mor til Villum Jonsen Gautun"
#   set the de label to "Mutter von Villum Jonsen Gautun"
LAST	Lde	"Mutter von Villum Jonsen Gautun"
#   set the en label to "mother of Villum Jonsen Gautun"
LAST	Len	"mother of Villum Jonsen Gautun"
#   set the es label to "madre de Villum Jonsen Gautun"
LAST	Les	"madre de Villum Jonsen Gautun"
#   set the fr label to "mère de Villum Jonsen Gautun"
LAST	Lfr	"mère de Villum Jonsen Gautun"
#   set the it label to "madre di Villum Jonsen Gautun"
LAST	Lit	"madre di Villum Jonsen Gautun"
#   set the ja label to "ヴィルム・ヨンセン・ガウトンの母"
LAST	Lja	"ヴィルム・ヨンセン・ガウトンの母"
#   set the ko label to "빌룸 존센 가우툰의 어머니"
LAST	Lko	"빌룸 존센 가우툰의 어머니"
#   set the nb label to "mor til Villum Jonsen Gautun"
LAST	Lnb	"mor til Villum Jonsen Gautun"
#   set the nl label to "moeder van Villum Jonsen Gautun"
LAST	Lnl	"moeder van Villum Jonsen Gautun"
#   set the pt label to "mãe de Villum Jonsen Gautun"
LAST	Lpt	"mãe de Villum Jonsen Gautun"
#   set the sv label to "mor till Villum Jonsen Gautun"
LAST	Lsv	"mor till Villum Jonsen Gautun"
#   set the zh label to "维卢姆·永森·加乌通之母"
LAST	Lzh	"维卢姆·永森·加乌通之母"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000001770277395 NN
LAST	P2600	"6000000001770277395"
#   P569 date of birth = +1534-00-00T00:00:00Z/9
LAST	P569	+1534-00-00T00:00:00Z/9	S2600	"6000000001770277395"
#   P570 date of death = +1623-00-00T00:00:00Z/9
LAST	P570	+1623-00-00T00:00:00Z/9	S2600	"6000000001770277395"
#   P40 child = Q141223970 Villum Jonsen Gautun
LAST	P40	Q141223970	S2600	"6000000001770277395"
#   Q141223970 Villum Jonsen Gautun: P25 mother = the item just created
Q141223970	P25	LAST	S2600	"6000000001770277395"

# create a new item
CREATE
#   the item just created: set the mul label to "NN"
LAST	Lmul	"NN"
#   set the ca label to "mare de Peder Jonsen Voster"
LAST	Lca	"mare de Peder Jonsen Voster"
#   set the da label to "mor til Peder Jonsen Voster"
LAST	Lda	"mor til Peder Jonsen Voster"
#   set the de label to "Mutter von Peder Jonsen Voster"
LAST	Lde	"Mutter von Peder Jonsen Voster"
#   set the en label to "mother of Peder Jonsen Voster"
LAST	Len	"mother of Peder Jonsen Voster"
#   set the es label to "madre de Peder Jonsen Voster"
LAST	Les	"madre de Peder Jonsen Voster"
#   set the fr label to "mère de Peder Jonsen Voster"
LAST	Lfr	"mère de Peder Jonsen Voster"
#   set the it label to "madre di Peder Jonsen Voster"
LAST	Lit	"madre di Peder Jonsen Voster"
#   set the ja label to "ペーダー・ヨンセン・ヴォステルの母"
LAST	Lja	"ペーダー・ヨンセン・ヴォステルの母"
#   set the ko label to "페데르 존센 보스테르의 어머니"
LAST	Lko	"페데르 존센 보스테르의 어머니"
#   set the nb label to "mor til Peder Jonsen Voster"
LAST	Lnb	"mor til Peder Jonsen Voster"
#   set the nl label to "moeder van Peder Jonsen Voster"
LAST	Lnl	"moeder van Peder Jonsen Voster"
#   set the pt label to "mãe de Peder Jonsen Voster"
LAST	Lpt	"mãe de Peder Jonsen Voster"
#   set the sv label to "mor till Peder Jonsen Voster"
LAST	Lsv	"mor till Peder Jonsen Voster"
#   set the zh label to "彼泽·永森·沃斯特尔之母"
LAST	Lzh	"彼泽·永森·沃斯特尔之母"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000007980728931 NN
LAST	P2600	"6000000007980728931"
#   P569 date of birth = +1535-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P569	+1535-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"6000000007980728931"
#   P40 child = Q141242562 Peder Jonsen Voster
LAST	P40	Q141242562	S2600	"6000000007980728931"
#   Q141242562 Peder Jonsen Voster: P25 mother = the item just created
Q141242562	P25	LAST	S2600	"6000000007980728931"

# create a new item
CREATE
#   the item just created: set the en label to "Sara Carlberg"
LAST	Len	"Sara Carlberg"
#   set the mul label to "Sara Carlberg"
LAST	Lmul	"Sara Carlberg"
#   set the ja label to "サラ・カルルベルグ"
LAST	Lja	"サラ・カルルベルグ"
#   set the zh label to "萨拉·卡尔尔贝尔格"
LAST	Lzh	"萨拉·卡尔尔贝尔格"
#   set the ko label to "사라 카르르베르그"
LAST	Lko	"사라 카르르베르그"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000006435949669 Sara Carlberg, qualified P1810 subject named as Sara Carlberg
LAST	P2600	"6000000006435949669"	P1810	"Sara Carlberg"
#   P569 date of birth = +1647-01-31T00:00:00Z/11
LAST	P569	+1647-01-31T00:00:00Z/11	S2600	"6000000006435949669"
#   P570 date of death = +1701-00-00T00:00:00Z/9
LAST	P570	+1701-00-00T00:00:00Z/9	S2600	"6000000006435949669"
#   P22 father = Q141249728 Johan Börgesson Carlberg
LAST	P22	Q141249728	S2600	"6000000006435949669"
#   P25 mother = Q141249729 Kristina Olofsdotter Spaak
LAST	P25	Q141249729	S2600	"6000000006435949669"
#   P40 child = Q141249724 Carl Rutger von Braunjohan
LAST	P40	Q141249724	S2600	"6000000006435949669"
#   Q141249728 Johan Börgesson Carlberg: P40 child = the item just created
Q141249728	P40	LAST	S2600	"6000000006435949669"
#   Q141249729 Kristina Olofsdotter Spaak: P40 child = the item just created
Q141249729	P40	LAST	S2600	"6000000006435949669"
#   Q141249724 Carl Rutger von Braunjohan: P25 mother = the item just created
Q141249724	P25	LAST	S2600	"6000000006435949669"

# create a new item
CREATE
#   the item just created: set the en label to "Sara Ericsdotter"
LAST	Len	"Sara Ericsdotter"
#   set the mul label to "Sara Ericsdotter"
LAST	Lmul	"Sara Ericsdotter"
#   set the ja label to "サラ・エリクスドッテル"
LAST	Lja	"サラ・エリクスドッテル"
#   set the zh label to "萨拉·埃里克斯多特"
LAST	Lzh	"萨拉·埃里克斯多特"
#   set the ko label to "사라 에리크스도테르"
LAST	Lko	"사라 에리크스도테르"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 4184733660450025774 Sara Ericsdotter, qualified P1810 subject named as Sara Ericsdotter
LAST	P2600	"4184733660450025774"	P1810	"Sara Ericsdotter"
#   P569 date of birth = +1740-10-18T00:00:00Z/11
LAST	P569	+1740-10-18T00:00:00Z/11	S2600	"4184733660450025774"
#   P570 date of death = +1809-10-27T00:00:00Z/11
LAST	P570	+1809-10-27T00:00:00Z/11	S2600	"4184733660450025774"
#   P40 child = Q5976894 Gabriel Hansson Marklin
LAST	P40	Q5976894	S2600	"4184733660450025774"
#   Q5976894 Gabriel Hansson Marklin: P25 mother = the item just created
Q5976894	P25	LAST	S2600	"4184733660450025774"
#   the item just created: P735 given name = Q833345 Sara
LAST	P735	Q833345

# create a new item
CREATE
#   set the en label to "Steinvor Sørensdatter Gjesdal"
LAST	Len	"Steinvor Sørensdatter Gjesdal"
#   set the mul label to "Steinvor Sørensdatter Gjesdal"
LAST	Lmul	"Steinvor Sørensdatter Gjesdal"
#   set the ja label to "ステインヴォル・ソレンスダッテル・イェスダール"
LAST	Lja	"ステインヴォル・ソレンスダッテル・イェスダール"
#   set the zh label to "斯特因沃尔·索伦斯达特·耶斯达尔"
LAST	Lzh	"斯特因沃尔·索伦斯达特·耶斯达尔"
#   set the ko label to "스테인보르 쇠렌스다테르 게스달"
LAST	Lko	"스테인보르 쇠렌스다테르 게스달"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000065992673830 Steinvor Sørensdatter Gjesdal, qualified P1810 subject named as Steinvor Sørensdatter Gjesdal
LAST	P2600	"6000000065992673830"	P1810	"Steinvor Sørensdatter Gjesdal"
#   P569 date of birth = +1778-00-00T00:00:00Z/9
LAST	P569	+1778-00-00T00:00:00Z/9	S2600	"6000000065992673830"
#   P22 father = Q141219069 Søren Sørenson Gjesdal
LAST	P22	Q141219069	S2600	"6000000065992673830"
#   P25 mother = Q141219065 Marta Torbjørnsdotter Gjesdal
LAST	P25	Q141219065	S2600	"6000000065992673830"
#   Q141219069 Søren Sørenson Gjesdal: P40 child = the item just created
Q141219069	P40	LAST	S2600	"6000000065992673830"
#   Q141219065 Marta Torbjørnsdotter Gjesdal: P40 child = the item just created
Q141219065	P40	LAST	S2600	"6000000065992673830"

# create a new item
CREATE
#   the item just created: set the en label to "Tormod Olavsen Foss"
LAST	Len	"Tormod Olavsen Foss"
#   set the mul label to "Tormod Olavsen Foss"
LAST	Lmul	"Tormod Olavsen Foss"
#   set the ja label to "トルモド・オラヴセン・フォス"
LAST	Lja	"トルモド・オラヴセン・フォス"
#   set the zh label to "托尔莫德·奥拉夫森·福斯"
LAST	Lzh	"托尔莫德·奥拉夫森·福斯"
#   set the ko label to "토르모드 오랍센 포스"
LAST	Lko	"토르모드 오랍센 포스"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000002376687013 Tormod Olavsen Foss, qualified P1810 subject named as Tormod Olavsen Foss
LAST	P2600	"6000000002376687013"	P1810	"Tormod Olavsen Foss"
#   P569 date of birth = +1535-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P569	+1535-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"6000000002376687013"
#   P570 date of death = +1614-00-00T00:00:00Z/9
LAST	P570	+1614-00-00T00:00:00Z/9	S2600	"6000000002376687013"
#   P40 child = Q141206080 Peder Tormodsen Foss
LAST	P40	Q141206080	S2600	"6000000002376687013"
#   Q141206080 Peder Tormodsen Foss: P22 father = the item just created
Q141206080	P22	LAST	S2600	"6000000002376687013"
#   the item just created: P735 given name = Q7825922 Tormod
LAST	P735	Q7825922
#   P734 family name = Q16870001 Foss
LAST	P734	Q16870001
#   Q6235986 Carl Gustaf Wennerstedt: P3373 sibling = Q141249733 Margareta Helena Wennerstedt
Q6235986	P3373	Q141249733	S2600	"1552522"
#   Q4830275 Axel Gustaf Gyllenkrok: P3373 sibling = Q136376245 Fredrik Elof Gyllenkrok RSO
Q4830275	P3373	Q136376245	S2600	"344146815060011563"
#   Q105796231 Margareta Gödiksdotter Fincke till Kanckas: P735 given name = Q8274988 Margareta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q105796231	P735	Q8274988	P1545	"1"	P7452	Q3409033
#   Q110386205 Lars Bengtsson Hierta till Kålsholmen: P735 given name = Q15635262 Lars, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110386205	P735	Q15635262	P1545	"1"	P7452	Q3409033
#   Q104172926 Carl Johan Oskar von Numers: P735 given name = Q2529610 Carl, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q104172926	P735	Q2529610	P1545	"1"	P7452	Q3409033
#   P735 given name = Q10989273 Johan, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q104172926	P735	Q10989273	P1545	"2"	P3831	Q245025
#   P735 given name = Q18145769 Oskar, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q104172926	P735	Q18145769	P1545	"3"	P3831	Q245025
#   Q135441621 Carl Lagerborg: P735 given name = Q2529610 Carl
Q135441621	P735	Q2529610
#   Q110561236 Christina Fjodorovna Rosladin: P735 given name = Q1083457 Christina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110561236	P735	Q1083457	P1545	"1"	P7452	Q3409033
#   Q133861599 Beata Sofia Stierncrona: P735 given name = Q338015 Beata, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q133861599	P735	Q338015	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q133861599	P735	Q18201520	P1545	"2"	P3831	Q245025
#   Q108082048 Adolf Vilhelm Boije af Gennäs: P735 given name = Q18145837 Adolf, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q108082048	P735	Q18145837	P1545	"1"	P7452	Q3409033
#   P735 given name = Q12805716 Vilhelm, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q108082048	P735	Q12805716	P1545	"2"	P3831	Q245025
#   P734 family name = Q141223490
Q108082048	P734	Q141223490
#   Q104383015 Evert Wilhelm Bruncrona: P735 given name = Q13580919 Evert, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q104383015	P735	Q13580919	P1545	"1"	P7452	Q3409033
#   P735 given name = Q11027623, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q104383015	P735	Q11027623	P1545	"2"	P3831	Q245025
#   Q136376387 Ebba Kristina Carlsdotter: P735 given name = Q2242896 Ebba, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q136376387	P735	Q2242896	P1545	"1"	P7452	Q3409033
#   P735 given name = Q19798802 Kristina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q136376387	P735	Q19798802	P1545	"2"	P3831	Q245025
#   Q73762646 Barbara Josefsdr Pipping: P26 spouse = Q73762532 Hans Henrik Wittfooth
Q73762646	P26	Q73762532	S2600	"6000000000624795275"
#   P2600 Geni.com profile ID = 6000000000624795275 Barbara Josefsdr Pipping, qualified P1810 subject named as Barbara Josefsdr Pipping
Q73762646	P2600	"6000000000624795275"	P1810	"Barbara Josefsdr Pipping"
#   Q110304710 Leveke Dorothea von Levetzow: P735 given name = Q909253 Dorothea, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110304710	P735	Q909253	P1545	"2"	P3831	Q245025
#   Q130683609 Cecilia Lucia Brodersen: P735 given name = Q859234 Cecilia, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q130683609	P735	Q859234	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1160640 Lucia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q130683609	P735	Q1160640	P1545	"2"	P3831	Q245025
#   Q136376245 Fredrik Elof Gyllenkrok RSO: P735 given name = Q4926491 Fredrik, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q136376245	P735	Q4926491	P1545	"1"	P7452	Q3409033
#   P735 given name = Q3366319 Elof, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q136376245	P735	Q3366319	P1545	"2"	P3831	Q245025
#   Q110547994 Elisabeth von Saveland: P735 given name = Q63611044 Elisabeth, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110547994	P735	Q63611044	P1545	"1"	P7452	Q3409033
#   Q30879127 Guiges Guy de Forez VII: P735 given name = Q1159023 Guy, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q30879127	P735	Q1159023	P1545	"2"	P3831	Q245025
#   Q110378177 Adelheid von Plain: P735 given name = Q4057477 Adelheid, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110378177	P735	Q4057477	P1545	"1"	P7452	Q3409033
#   Q116007123 Costanza di Niccolò Cavalcanti: P735 given name = Q19816831 Costanza, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q116007123	P735	Q19816831	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1984713 Niccolò, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q116007123	P735	Q1984713	P1545	"3"	P3831	Q245025
#   P734 family name = Q21450357 Cavalcanti
Q116007123	P734	Q21450357
#   Q110548816 Lovisa Thott: P735 given name = Q10570000 Lovisa
Q110548816	P735	Q10570000
#   P734 family name = Q47528688 Thott
Q110548816	P734	Q47528688
#   Q141249724 Carl Rutger von Braunjohan: P26 spouse = Q141249733 Margareta Helena Wennerstedt
Q141249724	P26	Q141249733	S2600	"6000000004352726281"
#   Q130564935 Christoph Ernst von Platen: P735 given name = Q17689481 Christoph, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q130564935	P735	Q17689481	P1545	"1"	P7452	Q3409033
#   P735 given name = Q292691 Ernst, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q130564935	P735	Q292691	P1545	"2"	P3831	Q245025
#   Q110303165 Sofia Elisabeth Augusta von Buchwaldt: P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110303165	P735	Q18201520	P1545	"1"	P7452	Q3409033
#   P735 given name = Q63611044 Elisabeth, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110303165	P735	Q63611044	P1545	"2"	P3831	Q245025
#   P735 given name = Q1370330 Augusta, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q110303165	P735	Q1370330	P1545	"3"	P3831	Q245025
#   Q110304545 Charlotta Lovisa Gyllenkrok: P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110304545	P735	Q1067071	P1545	"1"	P7452	Q3409033
#   P735 given name = Q10570000 Lovisa, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110304545	P735	Q10570000	P1545	"2"	P3831	Q245025
#   Q76250299 Vendela Sofia von Wright: P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q76250299	P735	Q18201520	P1545	"2"	P3831	Q245025
#   P734 family name = Q2594455 Wright
Q76250299	P734	Q2594455
#   Q110548033 Marie Emilie Reuterskiöld: P735 given name = Q106674406 Marie, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110548033	P735	Q106674406	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16275679 Emilie, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110548033	P735	Q16275679	P1545	"2"	P3831	Q245025
#   Q110151673 Jeanna Christina von Essen: P40 child = Q110395711 Charlotta Eleonora Hedvig von Krassow
Q110151673	P40	Q110395711	S2600	"6000000006127783693"
#   P2600 Geni.com profile ID = 6000000006127783693 Jeanna Christina von Essen, qualified P1810 subject named as Jeanna Christina von Essen
Q110151673	P2600	"6000000006127783693"	P1810	"Jeanna Christina von Essen"
#   P735 given name = Q1083457 Christina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110151673	P735	Q1083457	P1545	"2"	P3831	Q245025
#   Q110151781 Carl Detlof von Krassow: P26 spouse = Q110151789 Hedvig Maria Fredrika Lillienstedt
Q110151781	P26	Q110151789	S2600	"6000000006127830565"
#   P2600 Geni.com profile ID = 6000000006127830565 Carl Detlof von Krassow, qualified P1810 subject named as Carl Detlof von Krassow
Q110151781	P2600	"6000000006127830565"	P1810	"Carl Detlof von Krassow"
#   Q110395728 Eugenia Karolina Desideria von Essen: P735 given name = Q962602 Eugenia, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110395728	P735	Q962602	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1734206 Karolina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110395728	P735	Q1734206	P1545	"2"	P3831	Q245025
#   P735 given name = Q682121 Desideria, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q110395728	P735	Q682121	P1545	"3"	P3831	Q245025
#   Q6215610 Erik Birger Trolle: P26 spouse = Q98545952 Augusta Charlotte Alice Trolle
Q6215610	P26	Q98545952	S2600	"6000000006128193232"
#   P2600 Geni.com profile ID = 6000000006128193232 Erik Birger Trolle, qualified P1810 subject named as Erik Birger Trolle
Q6215610	P2600	"6000000006128193232"	P1810	"Erik Birger Trolle"
#   Q133861600 Catharina Elisabet Lamoni: P735 given name = Q17317997 Catharina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q133861600	P735	Q17317997	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16423275 Elisabet, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q133861600	P735	Q16423275	P1545	"2"	P3831	Q245025
#   Q99202612 Maria Eleonora von Busseck: P735 given name = Q325872 Maria, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q99202612	P735	Q325872	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18759077 Eleonora, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q99202612	P735	Q18759077	P1545	"2"	P3831	Q245025
#   Q75577007 Alexander Atchesonne: P40 child = Q75579166 John Atchison Atchesonne Acheson
Q75577007	P40	Q75579166	S2600	"6000000006537152001"
#   P2600 Geni.com profile ID = 6000000006537152001 Alexander Atchesonne, qualified P1810 subject named as Alexander Atchesonne
Q75577007	P2600	"6000000006537152001"	P1810	"Alexander Atchesonne"
#   Q141249728 Johan Börgesson Carlberg: P26 spouse = Q141249729 Kristina Olofsdotter Spaak
Q141249728	P26	Q141249729	S2600	"6000000006897169084"
#   Q141249729 Kristina Olofsdotter Spaak: P26 spouse = Q141249728 Johan Börgesson Carlberg
Q141249729	P26	Q141249728	S2600	"6000000006897337018"
#   Q136660380 Maria Andersdotter Bergia: P735 given name = Q325872 Maria
Q136660380	P735	Q325872
#   Q136376354 Agneta Sofia Löwenhielm: P735 given name = Q3354746 Agneta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q136376354	P735	Q3354746	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q136376354	P735	Q18201520	P1545	"2"	P3831	Q245025
#   Q109546615 Catharina Ihre: P26 spouse = Q6069858 Andreas Olai Rhyzelius
Q109546615	P26	Q6069858	S2600	"6000000007343898358"
#   P2600 Geni.com profile ID = 6000000007343898358 Catharina Ihre, qualified P1810 subject named as Catharina Ihre
Q109546615	P2600	"6000000007343898358"	P1810	"Catharina Ihre"
#   Q109852820 Gustav Adolf Järnefelt: P735 given name = Q746076, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q109852820	P735	Q746076	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18145837 Adolf, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q109852820	P735	Q18145837	P1545	"2"	P3831	Q245025
#   Q136028286 Margareta Charlotta Ihre: P22 father = Q719983 Johan Ihre
Q136028286	P22	Q719983	S2600	"6000000007460832349"
#   P2600 Geni.com profile ID = 6000000007460832349 Margareta Charlotta Ihre, qualified P1810 subject named as Margareta Charlotta Ihre
Q136028286	P2600	"6000000007460832349"	P1810	"Margareta Charlotta Ihre"
#   P735 given name = Q8274988 Margareta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q136028286	P735	Q8274988	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q136028286	P735	Q1067071	P1545	"2"	P3831	Q245025
#   Q141249736 Mattias Edenberg: P26 spouse = Q141249730 Margareta Catharina Clo
Q141249736	P26	Q141249730	S2600	"6000000007511893198"
#   Q133283834 Nils Gabriel Danckwardt-Lillieström till Gälsebo: P735 given name = Q16423038 Nils, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q133283834	P735	Q16423038	P1545	"1"	P7452	Q3409033
#   P735 given name = Q4925914 Gabriel, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q133283834	P735	Q4925914	P1545	"2"	P3831	Q245025
#   Q110548896 Ebba Lidman: P735 given name = Q2242896 Ebba
Q110548896	P735	Q2242896
#   Q135665878 Anna Christina Stålhammar: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q135665878	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1083457 Christina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q135665878	P735	Q1083457	P1545	"2"	P3831	Q245025
#   Q110457041 Anna Sofia Stålhammar: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110457041	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110457041	P735	Q18201520	P1545	"2"	P3831	Q245025
#   Q109835051 Ulrika Fredrika Ekström: P40 child = Q134498447 Elisabet Charlotta von Stedingk
Q109835051	P40	Q134498447	S2600	"6000000008269915234"
#   P2600 Geni.com profile ID = 6000000008269915234 Ulrika Fredrika Ekström, qualified P1810 subject named as Ulrika Fredrika Ekström
Q109835051	P2600	"6000000008269915234"	P1810	"Ulrika Fredrika Ekström"
#   P735 given name = Q18924998 Ulrika, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q109835051	P735	Q18924998	P1545	"1"	P7452	Q3409033
#   P735 given name = Q5499550 Fredrika, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q109835051	P735	Q5499550	P1545	"2"	P3831	Q245025
#   Q134546510 Catharina Elisabet Brandt: P25 mother = Q141250213 Anna Maria Norn
Q134546510	P25	Q141250213	S2600	"6000000008496890939"
#   P2600 Geni.com profile ID = 6000000008496890939 Catharina Elisabet Brandt, qualified P1810 subject named as Catharina Elisabet Brandt
Q134546510	P2600	"6000000008496890939"	P1810	"Catharina Elisabet Brandt"
#   P735 given name = Q17317997 Catharina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q134546510	P735	Q17317997	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16423275 Elisabet, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q134546510	P735	Q16423275	P1545	"2"	P3831	Q245025
#   P734 family name = Q11941314 Brandt
Q134546510	P734	Q11941314
#   Q141249733 Margareta Helena Wennerstedt: P26 spouse = Q141249724 Carl Rutger von Braunjohan
Q141249733	P26	Q141249724	S2600	"6000000008541457637"
#   Q109835490 Catharina Eleonora Temminck: P40 child = Q130665779 Ulrika von Düben
Q109835490	P40	Q130665779	S2600	"6000000008659258932"
#   P2600 Geni.com profile ID = 6000000008659258932 Catharina Eleonora Temminck, qualified P1810 subject named as Catharina Eleonora Temminck
Q109835490	P2600	"6000000008659258932"	P1810	"Catharina Eleonora Temminck"
#   Q5855920 Odert Reinhold von Essen d.y.: P40 child = Q135661262 Carl Reinhold von Essen af Zellie
Q5855920	P40	Q135661262	S2600	"6000000008881777692"
#   P2600 Geni.com profile ID = 6000000008881777692 Odert Reinhold von Essen d.y., qualified P1810 subject named as Odert Reinhold von Essen d.y.
Q5855920	P2600	"6000000008881777692"	P1810	"Odert Reinhold von Essen d.y."
#   Q134895550 Maria Hoffman: P735 given name = Q325872 Maria
Q134895550	P735	Q325872
#   Q110304544 Sophie Magdalena Magdalena von Essen: P735 given name = Q14942517 Sophie, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110304544	P735	Q14942517	P1545	"1"	P7452	Q3409033
#   P735 given name = Q842544 Magdalena, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110304544	P735	Q842544	P1545	"2"	P3831	Q245025
#   P735 given name = Q842544 Magdalena, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q110304544	P735	Q842544	P1545	"3"	P3831	Q245025
#   Q110548812 Maria Stiernblad: P735 given name = Q325872 Maria
Q110548812	P735	Q325872
#   Q135480259 Elsa Barbro Gabrielsdotter Leijonhufwudh: P26 spouse = Q135480258 Carl Leonard Leijonhufvud
Q135480259	P26	Q135480258	S2600	"6000000009693821507"
#   P2600 Geni.com profile ID = 6000000009693821507 Elsa Barbro Gabrielsdotter Leijonhufwudh, qualified P1810 subject named as Elsa Barbro Gabrielsdotter Oxenstierna af Croneborg
Q135480259	P2600	"6000000009693821507"	P1810	"Elsa Barbro Gabrielsdotter Oxenstierna af Croneborg"
#   P735 given name = Q1077181 Elsa, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q135480259	P735	Q1077181	P1545	"1"	P7452	Q3409033
#   P735 given name = Q807877 Barbro, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q135480259	P735	Q807877	P1545	"2"	P3831	Q245025
#   Q135480258 Carl Leonard Leijonhufvud: P26 spouse = Q135480259 Elsa Barbro Gabrielsdotter Leijonhufwudh
Q135480258	P26	Q135480259	S2600	"6000000009693938328"
#   P2600 Geni.com profile ID = 6000000009693938328 Carl Leonard Leijonhufvud, qualified P1810 subject named as Carl Leonard Leijonhufvud
Q135480258	P2600	"6000000009693938328"	P1810	"Carl Leonard Leijonhufvud"
#   P735 given name = Q2529610 Carl, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q135480258	P735	Q2529610	P1545	"1"	P7452	Q3409033
#   P735 given name = Q948418 Leonard, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q135480258	P735	Q948418	P1545	"2"	P3831	Q245025
#   Q110386180 Elisabet Ramsvärd: P735 given name = Q16423275 Elisabet
Q110386180	P735	Q16423275
#   Q110457058 Johanna Christina Tham: P26 spouse = Q110457053 Abraham Petersen
Q110457058	P26	Q110457053	S2600	"6000000010082399733"
#   P2600 Geni.com profile ID = 6000000010082399733 Johanna Christina Tham, qualified P1810 subject named as Johanna Christina Tham
Q110457058	P2600	"6000000010082399733"	P1810	"Johanna Christina Tham"
#   Q127270620 Johan Olofsson: P735 given name = Q10989273 Johan
Q127270620	P735	Q10989273
#   Q141249737 Ole Thoreson Toresen Lende: P26 spouse = Q141249721 Asseline Svensdatter Lende
Q141249737	P26	Q141249721	S2600	"6000000010517303222"
#   Q131740910 Herman af Petersens till Ersta: P26 spouse = Q131740911 Anna Elisabet Silfverschiöld
Q131740910	P26	Q131740911	S2600	"6000000010800923744"
#   P2600 Geni.com profile ID = 6000000010800923744 Herman af Petersens till Ersta, qualified P1810 subject named as Herman Petersen till Ersta
Q131740910	P2600	"6000000010800923744"	P1810	"Herman Petersen till Ersta"
#   P735 given name = Q16276646 Herman, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q131740910	P735	Q16276646	P1545	"1"	P7452	Q3409033
#   Q110457053 Abraham Petersen: P26 spouse = Q110457058 Johanna Christina Tham
Q110457053	P26	Q110457058	S2600	"6000000010801213418"
#   P2600 Geni.com profile ID = 6000000010801213418 Abraham Petersen, qualified P1810 subject named as Abraham Petersen
Q110457053	P2600	"6000000010801213418"	P1810	"Abraham Petersen"
#   P735 given name = Q4055996 Abraham
Q110457053	P735	Q4055996
#   Q131740913 Hedvig Sofia Hamilton: P735 given name = Q13648620 Hedvig, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q131740913	P735	Q13648620	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q131740913	P735	Q18201520	P1545	"2"	P3831	Q245025
#   Q131740911 Anna Elisabet Silfverschiöld: P26 spouse = Q131740910 Herman af Petersens till Ersta
Q131740911	P26	Q131740910	S2600	"6000000010801393457"
#   P2600 Geni.com profile ID = 6000000010801393457 Anna Elisabet Silfverschiöld, qualified P1810 subject named as Anna Elisabet Silfverschiöld
Q131740911	P2600	"6000000010801393457"	P1810	"Anna Elisabet Silfverschiöld"
#   P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q131740911	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16423275 Elisabet, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q131740911	P735	Q16423275	P1545	"2"	P3831	Q245025
#   Q5916852 Lorentz Kockum: P735 given name = Q21061236 Lorentz
Q5916852	P735	Q21061236
#   Q141250214 Anna Nilsdotter: P26 spouse = Q141250215 Benjamin Mårtensson
Q141250214	P26	Q141250215	S2600	"6000000011078617825"
#   Q141250215 Benjamin Mårtensson: P26 spouse = Q141250214 Anna Nilsdotter
Q141250215	P26	Q141250214	S2600	"6000000011078886609"
#   Q719983 Johan Ihre: P40 child = Q136028286 Margareta Charlotta Ihre
Q719983	P40	Q136028286	S2600	"6000000011116437821"
#   Q109296145 Charlotta Florentina Beata Ingelotz: P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q109296145	P735	Q1067071	P1545	"1"	P7452	Q3409033
#   P735 given name = Q610489 Florentina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q109296145	P735	Q610489	P1545	"2"	P3831	Q245025
#   P735 given name = Q338015 Beata, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q109296145	P735	Q338015	P1545	"3"	P3831	Q245025
#   Q73762532 Hans Henrik Wittfooth: P26 spouse = Q73762646 Barbara Josefsdr Pipping
Q73762532	P26	Q73762646	S2600	"6000000011539022692"
#   P2600 Geni.com profile ID = 6000000011539022692 Hans Henrik Wittfooth, qualified P1810 subject named as Hans Henrik Wittfooth
Q73762532	P2600	"6000000011539022692"	P1810	"Hans Henrik Wittfooth"
#   Q135479987 Eleonora Sofia Stiernblad: P26 spouse = Q135479974 Carl Erik Benzelstierna
Q135479987	P26	Q135479974	S2600	"6000000011660493986"
#   P2600 Geni.com profile ID = 6000000011660493986 Eleonora Sofia Stiernblad, qualified P1810 subject named as Eleonora Sofia Stiernblad
Q135479987	P2600	"6000000011660493986"	P1810	"Eleonora Sofia Stiernblad"
#   P735 given name = Q18759077 Eleonora, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q135479987	P735	Q18759077	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q135479987	P735	Q18201520	P1545	"2"	P3831	Q245025
#   Q109835643 Maria Catharina Douglies: P735 given name = Q325872 Maria, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q109835643	P735	Q325872	P1545	"1"	P7452	Q3409033
#   P735 given name = Q17317997 Catharina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q109835643	P735	Q17317997	P1545	"2"	P3831	Q245025
#   Q131726979 Vilhelmina Lovisa Fredrika Ulrika Iserhielm: P735 given name = Q15711317 Vilhelmina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q131726979	P735	Q15711317	P1545	"1"	P7452	Q3409033
#   P735 given name = Q10570000 Lovisa, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q131726979	P735	Q10570000	P1545	"2"	P3831	Q245025
#   P735 given name = Q5499550 Fredrika, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q131726979	P735	Q5499550	P1545	"3"	P3831	Q245025
#   P735 given name = Q18924998 Ulrika, qualified P1545 series ordinal 4, P3831 object of statement has role Q245025 middle name
Q131726979	P735	Q18924998	P1545	"4"	P3831	Q245025
#   Q101247028 Anna Catharina Fleming af Liebelitz: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q101247028	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P735 given name = Q17317997 Catharina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q101247028	P735	Q17317997	P1545	"2"	P3831	Q245025
#   Q135661264 Elisabet Charlotta In de Betou: P26 spouse = Q135661262 Carl Reinhold von Essen af Zellie
Q135661264	P26	Q135661262	S2600	"6000000011851554953"
#   P2600 Geni.com profile ID = 6000000011851554953 Elisabet Charlotta In de Betou, qualified P1810 subject named as Elisabet Charlotta In de Betou
Q135661264	P2600	"6000000011851554953"	P1810	"Elisabet Charlotta In de Betou"
#   P735 given name = Q16423275 Elisabet, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q135661264	P735	Q16423275	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q135661264	P735	Q1067071	P1545	"2"	P3831	Q245025
#   Q135661262 Carl Reinhold von Essen af Zellie: P26 spouse = Q135661264 Elisabet Charlotta In de Betou
Q135661262	P26	Q135661264	S2600	"6000000011851638339"
#   P2600 Geni.com profile ID = 6000000011851638339 Carl Reinhold von Essen af Zellie, qualified P1810 subject named as Carl Reinhold von Essen af Zellie
Q135661262	P2600	"6000000011851638339"	P1810	"Carl Reinhold von Essen af Zellie"
#   P735 given name = Q2529610 Carl, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q135661262	P735	Q2529610	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18091397 Reinhold, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q135661262	P735	Q18091397	P1545	"2"	P3831	Q245025
#   Q136536614 Ture Johansson Sandelin: P735 given name = Q2460609 Ture
Q136536614	P735	Q2460609
#   Q110548038 Axel Didrik Reuterskiöld: P26 spouse = Q110548051 Eva Anna Wefverstedt
Q110548038	P26	Q110548051	S2600	"6000000012566638313"
#   P2600 Geni.com profile ID = 6000000012566638313 Axel Didrik Reuterskiöld, qualified P1810 subject named as Axel Didrik Lagersparre
Q110548038	P2600	"6000000012566638313"	P1810	"Axel Didrik Lagersparre"
#   Q134626249 Gustaf Enebom: P735 given name = Q15646212 Gustaf
Q134626249	P735	Q15646212
#   Q135479974 Carl Erik Benzelstierna: P26 spouse = Q135479987 Eleonora Sofia Stiernblad
Q135479974	P26	Q135479987	S2600	"6000000012587936505"
#   P2600 Geni.com profile ID = 6000000012587936505 Carl Erik Benzelstierna, qualified P1810 subject named as Carl Erik Benzelstierna
Q135479974	P2600	"6000000012587936505"	P1810	"Carl Erik Benzelstierna"
#   Q135480230 Johan Munck af Rosenschöld: P26 spouse = Q135480235 Maria Rebecca Munck af Rosenschôld
Q135480230	P26	Q135480235	S2600	"6000000012640406848"
#   P2600 Geni.com profile ID = 6000000012640406848 Johan Munck af Rosenschöld, qualified P1810 subject named as Johan Munck af Rosenschöld
Q135480230	P2600	"6000000012640406848"	P1810	"Johan Munck af Rosenschöld"
#   P735 given name = Q10989273 Johan, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q135480230	P735	Q10989273	P1545	"1"	P7452	Q3409033
#   Q135480235 Maria Rebecca Munck af Rosenschôld: P26 spouse = Q135480230 Johan Munck af Rosenschöld
Q135480235	P26	Q135480230	S2600	"6000000012641171021"
#   P2600 Geni.com profile ID = 6000000012641171021 Maria Rebecca Munck af Rosenschôld, qualified P1810 subject named as Maria Rebecka Lemchen
Q135480235	P2600	"6000000012641171021"	P1810	"Maria Rebecka Lemchen"
#   P735 given name = Q325872 Maria, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q135480235	P735	Q325872	P1545	"1"	P7452	Q3409033
#   P735 given name = Q503607 Rebecca, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q135480235	P735	Q503607	P1545	"2"	P3831	Q245025
#   Q110548051 Eva Anna Wefverstedt: P26 spouse = Q110548038 Axel Didrik Reuterskiöld
Q110548051	P26	Q110548038	S2600	"6000000012819676325"
#   P2600 Geni.com profile ID = 6000000012819676325 Eva Anna Wefverstedt, qualified P1810 subject named as Eva Anna Wefverstedt
Q110548051	P2600	"6000000012819676325"	P1810	"Eva Anna Wefverstedt"
#   P735 given name = Q64412279 Eva, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110548051	P735	Q64412279	P1545	"1"	P7452	Q3409033
#   P735 given name = Q666578 Anna, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110548051	P735	Q666578	P1545	"2"	P3831	Q245025
#   Q64828819 Johanna Gustava Axelina Åberg: P735 given name = Q4120836 Johanna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q64828819	P735	Q4120836	P1545	"1"	P7452	Q3409033
#   P735 given name = Q21144392 Gustava, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q64828819	P735	Q21144392	P1545	"2"	P3831	Q245025
#   P735 given name = Q10423722 Axelina, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q64828819	P735	Q10423722	P1545	"3"	P3831	Q245025
#   Q134498447 Elisabet Charlotta von Stedingk: P25 mother = Q109835051 Ulrika Fredrika Ekström
Q134498447	P25	Q109835051	S2600	"6000000012875573275"
#   P2600 Geni.com profile ID = 6000000012875573275 Elisabet Charlotta von Stedingk, qualified P1810 subject named as Elisabet Charlotta von Stedingk
Q134498447	P2600	"6000000012875573275"	P1810	"Elisabet Charlotta von Stedingk"
#   P735 given name = Q16423275 Elisabet, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q134498447	P735	Q16423275	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q134498447	P735	Q1067071	P1545	"2"	P3831	Q245025
#   Q110304566 Johan Vilhelm Ankarcrona: P26 spouse = Q110304582 Gustava Magdalena Cronhielm af Hakunge
Q110304566	P26	Q110304582	S2600	"6000000012959953951"
#   P2600 Geni.com profile ID = 6000000012959953951 Johan Vilhelm Ankarcrona, qualified P1810 subject named as Johan Vilhelm Ankarcrona
Q110304566	P2600	"6000000012959953951"	P1810	"Johan Vilhelm Ankarcrona"
#   P735 given name = Q10989273 Johan, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110304566	P735	Q10989273	P1545	"1"	P7452	Q3409033
#   P735 given name = Q12805716 Vilhelm, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110304566	P735	Q12805716	P1545	"2"	P3831	Q245025
#   Q110304582 Gustava Magdalena Cronhielm af Hakunge: P26 spouse = Q110304566 Johan Vilhelm Ankarcrona
Q110304582	P26	Q110304566	S2600	"6000000012959992080"
#   P2600 Geni.com profile ID = 6000000012959992080 Gustava Magdalena Cronhielm af Hakunge, qualified P1810 subject named as Gustava Magdalena Cronhielm af Hakunge
Q110304582	P2600	"6000000012959992080"	P1810	"Gustava Magdalena Cronhielm af Hakunge"
#   P735 given name = Q21144392 Gustava, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110304582	P735	Q21144392	P1545	"1"	P7452	Q3409033
#   P735 given name = Q842544 Magdalena, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110304582	P735	Q842544	P1545	"2"	P3831	Q245025
#   Q109835201 Lovisa Löf: P735 given name = Q10570000 Lovisa
Q109835201	P735	Q10570000
#   Q110395628 Maria Lovisa Ulrika Ehrenpohl: P735 given name = Q325872 Maria, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110395628	P735	Q325872	P1545	"1"	P7452	Q3409033
#   P735 given name = Q10570000 Lovisa, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110395628	P735	Q10570000	P1545	"2"	P3831	Q245025
#   P735 given name = Q18924998 Ulrika, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q110395628	P735	Q18924998	P1545	"3"	P3831	Q245025
#   Q108743048 Augusta Maria Sophia Rålamb: P735 given name = Q1370330 Augusta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q108743048	P735	Q1370330	P1545	"1"	P7452	Q3409033
#   P735 given name = Q325872 Maria, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q108743048	P735	Q325872	P1545	"2"	P3831	Q245025
#   P735 given name = Q2302787 Sophia, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q108743048	P735	Q2302787	P1545	"3"	P3831	Q245025
#   Q110457060 Gertrud Helgers: P40 child = Q110457058 Johanna Christina Tham
Q110457060	P40	Q110457058	S2600	"6000000013397856067"
#   P2600 Geni.com profile ID = 6000000013397856067 Gertrud Helgers, qualified P1810 subject named as Gertrud Helgers
Q110457060	P2600	"6000000013397856067"	P1810	"Gertrud Helgers"
#   P735 given name = Q18180972 Gertrud
Q110457060	P735	Q18180972
#   Q141249721 Asseline Svensdatter Lende: P26 spouse = Q141249737 Ole Thoreson Toresen Lende
Q141249721	P26	Q141249737	S2600	"6000000013462214188"
#   Q64829391 Abraham Johansson Fought dä: P735 given name = Q4055996 Abraham, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q64829391	P735	Q4055996	P1545	"1"	P7452	Q3409033
#   Q110260857 August von der Schulenburg: P26 spouse = Q110558406 Katharina Elisabeth von der Schulenburg
Q110260857	P26	Q110558406	S2600	"6000000014024644179"
#   P2600 Geni.com profile ID = 6000000014024644179 August von der Schulenburg, qualified P1810 subject named as August von der Schulenburg
Q110260857	P2600	"6000000014024644179"	P1810	"August von der Schulenburg"
#   Q140223521 Sophie Luise Ernestine von Platen: P26 spouse = Q97207794 Joachim IV. Johann von Alvensleben
Q140223521	P26	Q97207794	S2600	"6000000014024808964"
#   P2600 Geni.com profile ID = 6000000014024808964 Sophie Luise Ernestine von Platen, qualified P1810 subject named as Sophie Luise Ernestine von Platen
Q140223521	P2600	"6000000014024808964"	P1810	"Sophie Luise Ernestine von Platen"
#   P735 given name = Q14942517 Sophie, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q140223521	P735	Q14942517	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18219764 Luise, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q140223521	P735	Q18219764	P1545	"2"	P3831	Q245025
#   P735 given name = Q20899030 Ernestine, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q140223521	P735	Q20899030	P1545	"3"	P3831	Q245025
#   Q94775402 Katharina Helene von Hagemeister: P26 spouse = Q57677031 Nikolai Christoph von Hagemeister, Linie Drostenhof u. Gotthardsberg
Q94775402	P26	Q57677031	S2600	"6000000014803594888"
#   P2600 Geni.com profile ID = 6000000014803594888 Katharina Helene von Hagemeister, qualified P1810 subject named as Katharina Helene Berens von Rautenfeld
Q94775402	P2600	"6000000014803594888"	P1810	"Katharina Helene Berens von Rautenfeld"
#   Q57677031 Nikolai Christoph von Hagemeister, Linie Drostenhof u. Gotthardsberg: P26 spouse = Q94775402 Katharina Helene von Hagemeister
Q57677031	P26	Q94775402	S2600	"6000000014803664573"
#   P2600 Geni.com profile ID = 6000000014803664573 Nikolai Christoph von Hagemeister, Linie Drostenhof u. Gotthardsberg, qualified P1810 subject named as Nikolai Christoph von Hagemeister, Linie Drostenhof u. Gotthardsberg
Q57677031	P2600	"6000000014803664573"	P1810	"Nikolai Christoph von Hagemeister, Linie Drostenhof u. Gotthardsberg"
#   Q62075421 Lovisa Christina Herman: P26 spouse = Q62075393 Johan Christian Schönherr
Q62075421	P26	Q62075393	S2600	"6000000016647986464"
#   P2600 Geni.com profile ID = 6000000016647986464 Lovisa Christina Herman, qualified P1810 subject named as Lovisa Christina Herman
Q62075421	P2600	"6000000016647986464"	P1810	"Lovisa Christina Herman"
#   Q62075393 Johan Christian Schönherr: P26 spouse = Q62075421 Lovisa Christina Herman
Q62075393	P26	Q62075421	S2600	"6000000016648152369"
#   P2600 Geni.com profile ID = 6000000016648152369 Johan Christian Schönherr, qualified P1810 subject named as Johan Christian Schönherr
Q62075393	P2600	"6000000016648152369"	P1810	"Johan Christian Schönherr"
#   Q98545952 Augusta Charlotte Alice Trolle: P26 spouse = Q6215610 Erik Birger Trolle
Q98545952	P26	Q6215610	S2600	"6000000016831353327"
#   P2600 Geni.com profile ID = 6000000016831353327 Augusta Charlotte Alice Trolle, qualified P1810 subject named as Augusta Charlotte Alice Gyldenstolpe
Q98545952	P2600	"6000000016831353327"	P1810	"Augusta Charlotte Alice Gyldenstolpe"
#   Q111998458 Sara de Marez: P735 given name = Q833345 Sara, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q111998458	P735	Q833345	P1545	"1"	P7452	Q3409033
#   Q108654979 Petronella Ottilia Schwencken von Friesen: P735 given name = Q16423664 Petronella, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q108654979	P735	Q16423664	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1423455 Ottilia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q108654979	P735	Q1423455	P1545	"2"	P3831	Q245025
#   Q141249730 Margareta Catharina Clo: P26 spouse = Q141249736 Mattias Edenberg
Q141249730	P26	Q141249736	S2600	"6000000020488764955"
#   Q5950427 Sven Fredrik Lidman: P40 child = Q110548896 Ebba Lidman
Q5950427	P40	Q110548896	S2600	"6000000021077800433"
#   P2600 Geni.com profile ID = 6000000021077800433 Sven Fredrik Lidman, qualified P1810 subject named as Sven Fredrik Lidman
Q5950427	P2600	"6000000021077800433"	P1810	"Sven Fredrik Lidman"
#   Q110151674 Jakobina Gustava von Essen: P735 given name = Q21144392 Gustava, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110151674	P735	Q21144392	P1545	"2"	P3831	Q245025
#   Q110558406 Katharina Elisabeth von der Schulenburg: P26 spouse = Q110260857 August von der Schulenburg
Q110558406	P26	Q110260857	S2600	"6000000022710683442"
#   P2600 Geni.com profile ID = 6000000022710683442 Katharina Elisabeth von der Schulenburg, qualified P1810 subject named as Katharina Elisabeth Schenk von Flechtingen
Q110558406	P2600	"6000000022710683442"	P1810	"Katharina Elisabeth Schenk von Flechtingen"
#   Q110153084 Amalia Eleonora von Lepel: P735 given name = Q453020 Amalia, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110153084	P735	Q453020	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18759077 Eleonora, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110153084	P735	Q18759077	P1545	"2"	P3831	Q245025
#   Q110304572 Cecilia Christophers: P735 given name = Q859234 Cecilia
Q110304572	P735	Q859234
#   Q110304541 Margareta Catharina von Finecke: P735 given name = Q8274988 Margareta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q110304541	P735	Q8274988	P1545	"1"	P7452	Q3409033
#   P735 given name = Q17317997 Catharina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q110304541	P735	Q17317997	P1545	"2"	P3831	Q245025
#   Q6069858 Andreas Olai Rhyzelius: P26 spouse = Q109546615 Catharina Ihre
Q6069858	P26	Q109546615	S2600	"6000000029247327107"
#   P2600 Geni.com profile ID = 6000000029247327107 Andreas Olai Rhyzelius, qualified P1810 subject named as Andreas Olofsson
Q6069858	P2600	"6000000029247327107"	P1810	"Andreas Olofsson"
#   Q110151789 Hedvig Maria Fredrika Lillienstedt: P26 spouse = Q110151781 Carl Detlof von Krassow
Q110151789	P26	Q110151781	S2600	"6000000032879859227"
#   P2600 Geni.com profile ID = 6000000032879859227 Hedvig Maria Fredrika Lillienstedt, qualified P1810 subject named as Hedvig Maria Fredrika Lillienstedt
Q110151789	P2600	"6000000032879859227"	P1810	"Hedvig Maria Fredrika Lillienstedt"
#   Q138495479 Friedrich Conrad Dietrich Adrian von Kleist: P735 given name = Q14038597 Friedrich, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q138495479	P735	Q14038597	P1545	"1"	P7452	Q3409033
#   P735 given name = Q17436400 Conrad, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q138495479	P735	Q17436400	P1545	"2"	P3831	Q245025
#   P735 given name = Q18145860 Dietrich, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q138495479	P735	Q18145860	P1545	"3"	P3831	Q245025
#   P735 given name = Q372250 Adrian, qualified P1545 series ordinal 4, P3831 object of statement has role Q245025 middle name
Q138495479	P735	Q372250	P1545	"4"	P3831	Q245025
#   Q97207794 Joachim IV. Johann von Alvensleben: P26 spouse = Q140223521 Sophie Luise Ernestine von Platen
Q97207794	P26	Q140223521	S2600	"6000000058353999857"
#   P2600 Geni.com profile ID = 6000000058353999857 Joachim IV. Johann von Alvensleben, qualified P1810 subject named as Joachim IV. Johann von Alvensleben
Q97207794	P2600	"6000000058353999857"	P1810	"Joachim IV. Johann von Alvensleben"
#   P735 given name = Q4926961 Joachim, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q97207794	P735	Q4926961	P1545	"1"	P7452	Q3409033
#   P735 given name = Q11122389 Johann, qualified P1545 series ordinal 3, P3831 object of statement has role Q245025 middle name
Q97207794	P735	Q11122389	P1545	"3"	P3831	Q245025
#   Q130524451 Carl Henrik von Hofsten RSO: P735 given name = Q2529610 Carl, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
Q130524451	P735	Q2529610	P1545	"1"	P7452	Q3409033
#   P735 given name = Q594279 Henrik, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
Q130524451	P735	Q594279	P1545	"2"	P3831	Q245025

