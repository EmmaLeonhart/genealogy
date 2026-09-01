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

# Jonson -- patronymic, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Jonson"
LAST	Len	"Jonson"
#   set the mul label to "Jonson"
LAST	Lmul	"Jonson"
#   set the en description to "patronymic"
LAST	Den	"patronymic"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141205903 Enok Jonson Rønneberg: P5056 patronym or matronym = the item just created, qualified P144 based on Q141216481 Jon Tørresson Soma
Q141205903	P5056	LAST	P144	Q141216481	S2600	"6000000001656464422"
#   Q141249595 Asbjørn Jonson Rønneberg: P5056 patronym or matronym = the item just created, qualified P144 based on Q141244102 Jon Torson Røyneberg
Q141249595	P5056	LAST	P144	Q141244102	S2600	"6000000003491988141"
#   Q141219349 Tørres Jonson Grannes: P5056 patronym or matronym = the item just created
Q141219349	P5056	LAST	S2600	"6000000005608892520"
#   Q141216470 Govert Jonson Årsvoll: P5056 patronym or matronym = the item just created
Q141216470	P5056	LAST	S2600	"6000000008174080446"

# Rasmussen -- patronymic, 4 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Rasmussen"
LAST	Len	"Rasmussen"
#   set the mul label to "Rasmussen"
LAST	Lmul	"Rasmussen"
#   set the en description to "patronymic"
LAST	Den	"patronymic"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141216381 Hans Rasmussen Låge-Håland: P5056 patronym or matronym = the item just created
Q141216381	P5056	LAST	S2600	"6000000009127934231"
#   Q141223738 Ola Rasmussen Bø: P5056 patronym or matronym = the item just created, qualified P144 based on Q141200074 Rasmus Olsen Bø
Q141223738	P5056	LAST	P144	Q141200074	S2600	"6000000196541254827"
#   Q141242406 Hans Rasmussen Bø: P5056 patronym or matronym = the item just created, qualified P144 based on Q141189099 Rasmus Helgesen Bø
Q141242406	P5056	LAST	P144	Q141189099	S2600	"6000000225376735889"
#   Q141242555 Ola Rasmussen Bø: P5056 patronym or matronym = the item just created, qualified P144 based on Q141189099 Rasmus Helgesen Bø
Q141242555	P5056	LAST	P144	Q141189099	S2600	"6000000225376871825"

# Asbjørnsdatter -- patronymic, 3 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "Asbjørnsdatter"
LAST	Len	"Asbjørnsdatter"
#   set the mul label to "Asbjørnsdatter"
LAST	Lmul	"Asbjørnsdatter"
#   set the en description to "patronymic"
LAST	Den	"patronymic"
#   P31 instance of = Q110874 patronymic
LAST	P31	Q110874
#   Q141224263 Karen Asbjørnsdatter Opstad: P5056 patronym or matronym = the item just created, qualified P144 based on Q141216458 Asbjørn Gunnarson Bø
Q141224263	P5056	LAST	P144	Q141216458	S2600	"6000000011046282612"
#   Q141242419 Sara Asbjørnsdatter Bø: P5056 patronym or matronym = the item just created, qualified P144 based on Q141216458 Asbjørn Gunnarson Bø
Q141242419	P5056	LAST	P144	Q141216458	S2600	"6000000222520233004"
#   Q141242459 Anna Asbjørnsdatter Bø: P5056 patronym or matronym = the item just created, qualified P144 based on Q141216458 Asbjørn Gunnarson Bø
Q141242459	P5056	LAST	P144	Q141216458	S2600	"6000000222520767827"

# 294 more name items are needed and wait for a later
# run -- 3 a day is her cap, not a limit of the data:
#   Frondin (family), 3 bearer(s)
#   Garfve (family), 3 bearer(s)
#   Hansson (patronymic), 3 bearer(s)
#   Helgesen (patronymic), 3 bearer(s)
#   Høle (family), 3 bearer(s)
#   Ingebretsdatter (patronymic), 3 bearer(s)
#   Kristiansen (patronymic), 3 bearer(s)
#   Låge-Håland (family), 3 bearer(s)
#   Magnusson (patronymic), 3 bearer(s)
#   Nedre (family), 3 bearer(s)
#   Olofsdotter (patronymic), 3 bearer(s)
#   Pedersdatter (patronymic), 3 bearer(s)
#   ... and 282 more

# ========================================================================
# THE DAY'S PEOPLE
# ========================================================================

# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   2050 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   add a mul alias "Ingrid Charlotta Carlsdotter Hansson"
Q141249609	Amul	"Ingrid Charlotta Carlsdotter Hansson"
#   set the ko label to "오르므 오논센"
Q141216499	Lko	"오르므 오논센"
#   set the ko label to "게오르그 루드빅 본 쾨흐레르"
Q6145888	Lko	"게오르그 루드빅 본 쾨흐레르"
#   set the ko label to "사로몬 본 쾨흐레르"
Q19721217	Lko	"사로몬 본 쾨흐레르"
#   set the ko label to "브죄르느 라우리첸 브죄르헤임"
Q141244210	Lko	"브죄르느 라우리첸 브죄르헤임"
#   Q141225244 Rakel Maria Govertsdatter Årsvoll: set the ko label to "라켈 마리아 고베르츠다테르 오르스볼르"
Q141225244	Lko	"라켈 마리아 고베르츠다테르 오르스볼르"
#   set the ko label to "존 톨라크손 아우크란드 입"
Q141199899	Lko	"존 톨라크손 아우크란드 입"
#   set the ko label to "토레 토레손 탈게"
Q141216648	Lko	"토레 토레손 탈게"
#   set the ko label to "이바르 발헤임"
Q141199891	Lko	"이바르 발헤임"
#   set the ja label to "シャルルマーニュ"
Q3044	Lja	"シャルルマーニュ"
#   set the zh label to "卡尔莱马格内"
Q3044	Lzh	"卡尔莱马格内"
#   set the ko label to "차르레막네"
Q3044	Lko	"차르레막네"
#   set the ko label to "군느브죄르느 토레손 텡스"
Q141199851	Lko	"군느브죄르느 토레손 텡스"
#   set the ko label to "베르기테 군느브죄르느스다테르 텡스"
Q141198835	Lko	"베르기테 군느브죄르느스다테르 텡스"
#   Q141216371 Guri Pedersdatter Foss: set the ko label to "구리 페데르스다테르 포스"
Q141216371	Lko	"구리 페데르스다테르 포스"

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the mul label to "NN"
LAST	Lmul	"NN"
#   set the ca label to "pare de Gunnhild Pedersdatter Skårland"
LAST	Lca	"pare de Gunnhild Pedersdatter Skårland"
#   set the da label to "far til Gunnhild Pedersdatter Skårland"
LAST	Lda	"far til Gunnhild Pedersdatter Skårland"
#   set the de label to "Vater von Gunnhild Pedersdatter Skårland"
LAST	Lde	"Vater von Gunnhild Pedersdatter Skårland"
#   set the en label to "father of Gunnhild Pedersdatter Skårland"
LAST	Len	"father of Gunnhild Pedersdatter Skårland"
#   set the es label to "padre de Gunnhild Pedersdatter Skårland"
LAST	Les	"padre de Gunnhild Pedersdatter Skårland"
#   set the fr label to "père de Gunnhild Pedersdatter Skårland"
LAST	Lfr	"père de Gunnhild Pedersdatter Skårland"
#   set the it label to "padre di Gunnhild Pedersdatter Skårland"
LAST	Lit	"padre di Gunnhild Pedersdatter Skårland"
#   set the ja label to "グンンヒルド・ペーデシュダッテル・スコールランドの父"
LAST	Lja	"グンンヒルド・ペーデシュダッテル・スコールランドの父"
#   set the ko label to "군느힐드 페데르스다테르 스코르란드의 아버지"
LAST	Lko	"군느힐드 페데르스다테르 스코르란드의 아버지"
#   set the nb label to "far til Gunnhild Pedersdatter Skårland"
LAST	Lnb	"far til Gunnhild Pedersdatter Skårland"
#   set the nl label to "vader van Gunnhild Pedersdatter Skårland"
LAST	Lnl	"vader van Gunnhild Pedersdatter Skårland"
#   set the pt label to "pai de Gunnhild Pedersdatter Skårland"
LAST	Lpt	"pai de Gunnhild Pedersdatter Skårland"
#   set the sv label to "far till Gunnhild Pedersdatter Skårland"
LAST	Lsv	"far till Gunnhild Pedersdatter Skårland"
#   set the zh label to "贡希尔德·佩德斯达特·斯科尔兰德之父"
LAST	Lzh	"贡希尔德·佩德斯达特·斯科尔兰德之父"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005609534696
LAST	P2600	"6000000005609534696"
#   P40 child = Q141242500 Gunnhild Pedersdatter Skårland
LAST	P40	Q141242500	S2600	"6000000005609534696"
#   Q141242500 Gunnhild Pedersdatter Skårland: P22 father = the item just created
Q141242500	P22	LAST	S2600	"6000000005609534696"

# create a new item
CREATE
#   the item just created: set the en label to "Anna Magdalena Ziervogel"
LAST	Len	"Anna Magdalena Ziervogel"
#   set the mul label to "Anna Magdalena Ziervogel"
LAST	Lmul	"Anna Magdalena Ziervogel"
#   set the ja label to "アンナ・マグダレーナ・ジエルヴォゲル"
LAST	Lja	"アンナ・マグダレーナ・ジエルヴォゲル"
#   set the zh label to "安娜·马格达莱纳·吉埃尔沃盖尔"
LAST	Lzh	"安娜·马格达莱纳·吉埃尔沃盖尔"
#   set the ko label to "안나 막다레나 지에르보겔"
LAST	Lko	"안나 막다레나 지에르보겔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000015620099230 Anna Magdalena Ziervogel, qualified P1810 subject named as Anna Barbara Strauch
LAST	P2600	"6000000015620099230"	P1810	"Anna Barbara Strauch"
#   P569 date of birth = +1679-07-21T00:00:00Z/11
LAST	P569	+1679-07-21T00:00:00Z/11	S2600	"6000000015620099230"
#   P570 date of death = +1749-06-22T00:00:00Z/11
LAST	P570	+1749-06-22T00:00:00Z/11	S2600	"6000000015620099230"
#   P40 child = Q141244224 Justina Sophie Naucler
LAST	P40	Q141244224	S2600	"6000000015620099230"
#   Q141244224 Justina Sophie Naucler: P25 mother = the item just created
Q141244224	P25	LAST	S2600	"6000000015620099230"

# create a new item
CREATE
#   the item just created: set the en label to "Asseline Svensdatter Lende"
LAST	Len	"Asseline Svensdatter Lende"
#   set the mul label to "Asseline Svensdatter Lende"
LAST	Lmul	"Asseline Svensdatter Lende"
#   add a mul alias "Asseline Svensdatter Slethei"
LAST	Amul	"Asseline Svensdatter Slethei"
#   set the ja label to "アセリネ・スヴェンスダッテル・レンデ"
LAST	Lja	"アセリネ・スヴェンスダッテル・レンデ"
#   set the zh label to "阿塞利内·斯文斯达特·伦德"
LAST	Lzh	"阿塞利内·斯文斯达特·伦德"
#   set the ko label to "아세리네 스벤스다테르 렌데"
LAST	Lko	"아세리네 스벤스다테르 렌데"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000013462214188 Asseline Svensdatter Lende, qualified P1810 subject named as Asseline Svensdatter Slethei
LAST	P2600	"6000000013462214188"	P1810	"Asseline Svensdatter Slethei"
#   P569 date of birth = +1814-10-24T00:00:00Z/11
LAST	P569	+1814-10-24T00:00:00Z/11	S2600	"6000000013462214188"
#   P570 date of death = +1887-06-01T00:00:00Z/11
LAST	P570	+1887-06-01T00:00:00Z/11	S2600	"6000000013462214188"
#   P40 child = Q141219050 Ane Olsdatter Bø
LAST	P40	Q141219050	S2600	"6000000013462214188"
#   Q141219050 Ane Olsdatter Bø: P25 mother = the item just created
Q141219050	P25	LAST	S2600	"6000000013462214188"
#   the item just created: P734 family name = Q30083619, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q30083619	P3831	Q28418670
#   add a mul alias "Asseline Lende"
LAST	Amul	"Asseline Lende"

# create a new item
CREATE
#   set the en label to "Bjørn Nilssøn Tau"
LAST	Len	"Bjørn Nilssøn Tau"
#   set the mul label to "Bjørn Nilssøn Tau"
LAST	Lmul	"Bjørn Nilssøn Tau"
#   set the ja label to "ビョルン・ニルソン・タウ"
LAST	Lja	"ビョルン・ニルソン・タウ"
#   set the zh label to "比约恩·尼尔松·塔乌"
LAST	Lzh	"比约恩·尼尔松·塔乌"
#   set the ko label to "브죄르느 닐쇤 타우"
LAST	Lko	"브죄르느 닐쇤 타우"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000007980729100 Bjørn Nilssøn Tau, qualified P1810 subject named as Bjørn (?) Nilssøn Tau
LAST	P2600	"6000000007980729100"	P1810	"Bjørn (?) Nilssøn Tau"
#   P570 date of death = +1521-00-00T00:00:00Z/9, qualified P1326 latest date +1521-00-00T00:00:00Z/9
LAST	P570	+1521-00-00T00:00:00Z/9	P1326	+1521-00-00T00:00:00Z/9	S2600	"6000000007980729100"
#   P40 child = Q141216460 Bjørnsdatter Tau
LAST	P40	Q141216460	S2600	"6000000007980729100"
#   Q141216460 Bjørnsdatter Tau: P22 father = the item just created
Q141216460	P22	LAST	S2600	"6000000007980729100"
#   the item just created: P735 given name = Q18918288 Bjørn, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q18918288	P1545	"1"	P7452	Q3409033
#   add a mul alias "? Tau"
LAST	Amul	"? Tau"

# create a new item
CREATE
#   set the en label to "Carl Rutger von Braunjohan"
LAST	Len	"Carl Rutger von Braunjohan"
#   set the mul label to "Carl Rutger von Braunjohan"
LAST	Lmul	"Carl Rutger von Braunjohan"
#   set the ja label to "カール・ルトガー・ヴォン・ブラウンヨハン"
LAST	Lja	"カール・ルトガー・ヴォン・ブラウンヨハン"
#   set the zh label to "卡尔·鲁特盖尔·翁·布拉温约汉"
LAST	Lzh	"卡尔·鲁特盖尔·翁·布拉温约汉"
#   set the ko label to "카르르 루트게르 본 브라우노한"
LAST	Lko	"카르르 루트게르 본 브라우노한"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000004352726281 Carl Rutger von Braunjohan, qualified P1810 subject named as Carl Rutger von Braunjohan
LAST	P2600	"6000000004352726281"	P1810	"Carl Rutger von Braunjohan"
#   P569 date of birth = +1680-00-00T00:00:00Z/9
LAST	P569	+1680-00-00T00:00:00Z/9	S2600	"6000000004352726281"
#   P570 date of death = +1759-07-03T00:00:00Z/11
LAST	P570	+1759-07-03T00:00:00Z/11	S2600	"6000000004352726281"
#   P40 child = Q141249602 Fredrika Ulrika Eleonora von Braunjohan
LAST	P40	Q141249602	S2600	"6000000004352726281"
#   Q141249602 Fredrika Ulrika Eleonora von Braunjohan: P22 father = the item just created
Q141249602	P22	LAST	S2600	"6000000004352726281"

# create a new item
CREATE
#   the item just created: set the en label to "Christina Beata Uf"
LAST	Len	"Christina Beata Uf"
#   set the mul label to "Christina Beata Uf"
LAST	Lmul	"Christina Beata Uf"
#   set the ja label to "クリスティーナ・ベアタ・ウフ"
LAST	Lja	"クリスティーナ・ベアタ・ウフ"
#   set the zh label to "克里斯蒂娜·贝阿塔·乌夫"
LAST	Lzh	"克里斯蒂娜·贝阿塔·乌夫"
#   set the ko label to "츠리스티나 베아타 우프"
LAST	Lko	"츠리스티나 베아타 우프"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000018089322771 Christina Beata Uf, qualified P1810 subject named as Christina Beata Uf
LAST	P2600	"6000000018089322771"	P1810	"Christina Beata Uf"
#   P569 date of birth = +1682-09-15T00:00:00Z/11
LAST	P569	+1682-09-15T00:00:00Z/11	S2600	"6000000018089322771"
#   P26 spouse = Q141249626 Samuel Ugla
LAST	P26	Q141249626	S2600	"6000000018089322771"
#   P40 child = Q124608453 Petrus Ugla
LAST	P40	Q124608453	S2600	"6000000018089322771"
#   Q141249626 Samuel Ugla: P26 spouse = the item just created
Q141249626	P26	LAST	S2600	"6000000018089322771"
#   Q124608453 Petrus Ugla: P25 mother = the item just created
Q124608453	P25	LAST	S2600	"6000000018089322771"
#   the item just created: P735 given name = Q1083457 Christina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q1083457	P1545	"1"	P7452	Q3409033
#   P735 given name = Q338015 Beata, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q338015	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Conrad Ludvig Transchiöld"
LAST	Len	"Conrad Ludvig Transchiöld"
#   set the mul label to "Conrad Ludvig Transchiöld"
LAST	Lmul	"Conrad Ludvig Transchiöld"
#   add a mul alias "Conrad Ludvig Trana"
LAST	Amul	"Conrad Ludvig Trana"
#   set the ja label to "コンラッド・ルズヴィ・トランシオルド"
LAST	Lja	"コンラッド・ルズヴィ・トランシオルド"
#   set the zh label to "康拉德·卢德维格·特兰西奥尔德"
LAST	Lzh	"康拉德·卢德维格·特兰西奥尔德"
#   set the ko label to "콘라드 루드빅 트란시욀드"
LAST	Lko	"콘라드 루드빅 트란시욀드"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000008908318641 Conrad Ludvig Transchiöld till Arnöberg, qualified P1810 subject named as Conrad Ludvig Trana till Arnöberg
LAST	P2600	"6000000008908318641"	P1810	"Conrad Ludvig Trana till Arnöberg"
#   P569 date of birth = +1696-07-16T00:00:00Z/11
LAST	P569	+1696-07-16T00:00:00Z/11	S2600	"6000000008908318641"
#   P570 date of death = +1765-05-15T00:00:00Z/11
LAST	P570	+1765-05-15T00:00:00Z/11	S2600	"6000000008908318641"
#   P40 child = Q141217415 Ottiliana Vilhelmina Conradsdotter Transchiöld
LAST	P40	Q141217415	S2600	"6000000008908318641"
#   Q141217415 Ottiliana Vilhelmina Conradsdotter Transchiöld: P22 father = the item just created
Q141217415	P22	LAST	S2600	"6000000008908318641"
#   the item just created: P735 given name = Q17436400 Conrad, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q17436400	P1545	"1"	P7452	Q3409033
#   P735 given name = Q12233911 Ludvig, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q12233911	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Eva Turesdotter Bielke"
LAST	Len	"Eva Turesdotter Bielke"
#   set the mul label to "Eva Turesdotter Bielke"
LAST	Lmul	"Eva Turesdotter Bielke"
#   set the ja label to "エヴァ・トレスドッテル・ビールケ"
LAST	Lja	"エヴァ・トレスドッテル・ビールケ"
#   set the zh label to "伊娃·图雷斯多特·比埃尔凯"
LAST	Lzh	"伊娃·图雷斯多特·比埃尔凯"
#   set the ko label to "에바 투레스도테르 비엘케"
LAST	Lko	"에바 투레스도테르 비엘케"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000006127206019 Eva Turesdotter Bielke, qualified P1810 subject named as Eva Turesdotter Bielke
LAST	P2600	"6000000006127206019"	P1810	"Eva Turesdotter Bielke"
#   P569 date of birth = +1712-00-00T00:00:00Z/9
LAST	P569	+1712-00-00T00:00:00Z/9	S2600	"6000000006127206019"
#   P570 date of death = +1714-00-00T00:00:00Z/9
LAST	P570	+1714-00-00T00:00:00Z/9	S2600	"6000000006127206019"
#   P22 father = Q5597349 Thure Stensson Bielke
LAST	P22	Q5597349	S2600	"6000000006127206019"
#   P25 mother = Q141244125 Ursula Christina Törne
LAST	P25	Q141244125	S2600	"6000000006127206019"
#   Q5597349 Thure Stensson Bielke: P40 child = the item just created
Q5597349	P40	LAST	S2600	"6000000006127206019"
#   Q141244125 Ursula Christina Törne: P40 child = the item just created
Q141244125	P40	LAST	S2600	"6000000006127206019"
#   the item just created: P735 given name = Q64412279 Eva
LAST	P735	Q64412279
#   P734 family name = Q37547315 Bielke
LAST	P734	Q37547315

# create a new item
CREATE
#   set the en label to "Johan Börgesson Carlberg"
LAST	Len	"Johan Börgesson Carlberg"
#   set the mul label to "Johan Börgesson Carlberg"
LAST	Lmul	"Johan Börgesson Carlberg"
#   add a mul alias "Johan Börjesson Carlberg"
LAST	Amul	"Johan Börjesson Carlberg"
#   set the ja label to "ヨハン・ボルゲソン・カルルベルグ"
LAST	Lja	"ヨハン・ボルゲソン・カルルベルグ"
#   set the zh label to "约翰·博尔盖松·卡尔尔贝尔格"
LAST	Lzh	"约翰·博尔盖松·卡尔尔贝尔格"
#   set the ko label to "조한 뵈르게손 카르르베르그"
LAST	Lko	"조한 뵈르게손 카르르베르그"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000006897169084 Johan Börgesson Carlberg, qualified P1810 subject named as Johan Börjesson Carlberg
LAST	P2600	"6000000006897169084"	P1810	"Johan Börjesson Carlberg"
#   P569 date of birth = +1606-06-24T00:00:00Z/11
LAST	P569	+1606-06-24T00:00:00Z/11	S2600	"6000000006897169084"
#   P570 date of death = +1676-03-09T00:00:00Z/11
LAST	P570	+1676-03-09T00:00:00Z/11	S2600	"6000000006897169084"
#   P40 child = Q141244109 Maria Carlberg
LAST	P40	Q141244109	S2600	"6000000006897169084"
#   Q141244109 Maria Carlberg: P22 father = the item just created
Q141244109	P22	LAST	S2600	"6000000006897169084"
#   the item just created: P735 given name = Q10989273 Johan
LAST	P735	Q10989273
#   add a mul alias "Börjesson Börgesson Carlberg"
LAST	Amul	"Börjesson Börgesson Carlberg"

# create a new item
CREATE
#   set the en label to "Kristina Olofsdotter Spaak"
LAST	Len	"Kristina Olofsdotter Spaak"
#   set the mul label to "Kristina Olofsdotter Spaak"
LAST	Lmul	"Kristina Olofsdotter Spaak"
#   set the ja label to "クリスティーナ・オロフスドッテル・スパーク"
LAST	Lja	"クリスティーナ・オロフスドッテル・スパーク"
#   set the zh label to "克里斯蒂娜·奥洛夫斯多特·斯巴克"
LAST	Lzh	"克里斯蒂娜·奥洛夫斯多特·斯巴克"
#   set the ko label to "크리스티나 오로프스도테르 스파아크"
LAST	Lko	"크리스티나 오로프스도테르 스파아크"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000006897337018 Kristina Olofsdotter Spaak, qualified P1810 subject named as Kristina Olofsdotter Spaak
LAST	P2600	"6000000006897337018"	P1810	"Kristina Olofsdotter Spaak"
#   P569 date of birth = +1616-00-00T00:00:00Z/9
LAST	P569	+1616-00-00T00:00:00Z/9	S2600	"6000000006897337018"
#   P570 date of death = +1679-00-00T00:00:00Z/9
LAST	P570	+1679-00-00T00:00:00Z/9	S2600	"6000000006897337018"
#   P40 child = Q141244109 Maria Carlberg
LAST	P40	Q141244109	S2600	"6000000006897337018"
#   Q141244109 Maria Carlberg: P25 mother = the item just created
Q141244109	P25	LAST	S2600	"6000000006897337018"
#   the item just created: P735 given name = Q19798802 Kristina
LAST	P735	Q19798802
#   add a mul alias "Christina Olofsdotter Spaak"
LAST	Amul	"Christina Olofsdotter Spaak"

# create a new item
CREATE
#   set the en label to "Margareta Catharina Clo"
LAST	Len	"Margareta Catharina Clo"
#   set the mul label to "Margareta Catharina Clo"
LAST	Lmul	"Margareta Catharina Clo"
#   set the ja label to "マルガレータ・カタリーナ・クロ"
LAST	Lja	"マルガレータ・カタリーナ・クロ"
#   set the zh label to "瑪格麗塔·卡塔里娜·克洛"
LAST	Lzh	"瑪格麗塔·卡塔里娜·克洛"
#   set the ko label to "마르가레타 카타리나 크로"
LAST	Lko	"마르가레타 카타리나 크로"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000020488764955 Margareta Catharina Clo, qualified P1810 subject named as Margareta Catharina Clo
LAST	P2600	"6000000020488764955"	P1810	"Margareta Catharina Clo"
#   P569 date of birth = +1664-10-07T00:00:00Z/11
LAST	P569	+1664-10-07T00:00:00Z/11	S2600	"6000000020488764955"
#   P570 date of death = +1747-01-17T00:00:00Z/11
LAST	P570	+1747-01-17T00:00:00Z/11	S2600	"6000000020488764955"
#   P40 child = Q141217381 Catharina Edenberg
LAST	P40	Q141217381	S2600	"6000000020488764955"
#   Q141217381 Catharina Edenberg: P25 mother = the item just created
Q141217381	P25	LAST	S2600	"6000000020488764955"
#   the item just created: P735 given name = Q8274988 Margareta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q8274988	P1545	"1"	P7452	Q3409033
#   P735 given name = Q17317997 Catharina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q17317997	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Margareta Helena Wennerstedt"
LAST	Len	"Margareta Helena Wennerstedt"
#   set the mul label to "Margareta Helena Wennerstedt"
LAST	Lmul	"Margareta Helena Wennerstedt"
#   set the ja label to "マルガレータ・ヘレナ・ヴェネルステドト"
LAST	Lja	"マルガレータ・ヘレナ・ヴェネルステドト"
#   set the zh label to "瑪格麗塔·海伦娜·韦内尔斯特德特"
LAST	Lzh	"瑪格麗塔·海伦娜·韦内尔斯特德特"
#   set the ko label to "마르가레타 헤레나 웨느네르스테드트"
LAST	Lko	"마르가레타 헤레나 웨느네르스테드트"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000008541457637 Margareta Helena Wennerstedt, qualified P1810 subject named as Margareta Helena Wennerstedt
LAST	P2600	"6000000008541457637"	P1810	"Margareta Helena Wennerstedt"
#   P569 date of birth = +1685-00-00T00:00:00Z/9
LAST	P569	+1685-00-00T00:00:00Z/9	S2600	"6000000008541457637"
#   P570 date of death = +1724-00-00T00:00:00Z/9
LAST	P570	+1724-00-00T00:00:00Z/9	S2600	"6000000008541457637"
#   P40 child = Q141249602 Fredrika Ulrika Eleonora von Braunjohan
LAST	P40	Q141249602	S2600	"6000000008541457637"
#   Q141249602 Fredrika Ulrika Eleonora von Braunjohan: P25 mother = the item just created
Q141249602	P25	LAST	S2600	"6000000008541457637"
#   the item just created: P735 given name = Q8274988 Margareta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q8274988	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1035239 Helena, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1035239	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Maria Gavelia"
LAST	Len	"Maria Gavelia"
#   set the mul label to "Maria Gavelia"
LAST	Lmul	"Maria Gavelia"
#   set the ja label to "マリア・ガヴェリア"
LAST	Lja	"マリア・ガヴェリア"
#   set the zh label to "玛丽亚·加韦利阿"
LAST	Lzh	"玛丽亚·加韦利阿"
#   set the ko label to "마리아 가베리아"
LAST	Lko	"마리아 가베리아"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000041320371511 Maria Gavelia, qualified P1810 subject named as Maria Gavelia
LAST	P2600	"6000000041320371511"	P1810	"Maria Gavelia"
#   P570 date of death = +1692-00-00T00:00:00Z/9
LAST	P570	+1692-00-00T00:00:00Z/9	S2600	"6000000041320371511"
#   P22 father = Q16649267 Elias Pedersson Gavelius
LAST	P22	Q16649267	S2600	"6000000041320371511"
#   P25 mother = Q141244213 Catharina Nilsdotter
LAST	P25	Q141244213	S2600	"6000000041320371511"
#   Q16649267 Elias Pedersson Gavelius: P40 child = the item just created
Q16649267	P40	LAST	S2600	"6000000041320371511"
#   Q141244213 Catharina Nilsdotter: P40 child = the item just created
Q141244213	P40	LAST	S2600	"6000000041320371511"

# create a new item
CREATE
#   the item just created: set the en label to "Mattias Edenberg"
LAST	Len	"Mattias Edenberg"
#   set the mul label to "Mattias Edenberg"
LAST	Lmul	"Mattias Edenberg"
#   set the ja label to "マティアス・エデンベルグ"
LAST	Lja	"マティアス・エデンベルグ"
#   set the zh label to "马蒂阿斯·埃登贝尔格"
LAST	Lzh	"马蒂阿斯·埃登贝尔格"
#   set the ko label to "마티아스 에덴베르그"
LAST	Lko	"마티아스 에덴베르그"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000007511893198 Mattias Edenberg, qualified P1810 subject named as Mattias Edenberg
LAST	P2600	"6000000007511893198"	P1810	"Mattias Edenberg"
#   P569 date of birth = +1640-03-11T00:00:00Z/11
LAST	P569	+1640-03-11T00:00:00Z/11	S2600	"6000000007511893198"
#   P570 date of death = +1709-03-30T00:00:00Z/11
LAST	P570	+1709-03-30T00:00:00Z/11	S2600	"6000000007511893198"
#   P40 child = Q141217381 Catharina Edenberg
LAST	P40	Q141217381	S2600	"6000000007511893198"
#   Q141217381 Catharina Edenberg: P22 father = the item just created
Q141217381	P22	LAST	S2600	"6000000007511893198"
#   the item just created: P735 given name = Q16279186 Mattias
LAST	P735	Q16279186

# create a new item
CREATE
#   set the en label to "Ole Thoreson Toresen Lende"
LAST	Len	"Ole Thoreson Toresen Lende"
#   set the mul label to "Ole Thoreson Toresen Lende"
LAST	Lmul	"Ole Thoreson Toresen Lende"
#   set the ja label to "オーレ・トレソン・トレセン・レンデ"
LAST	Lja	"オーレ・トレソン・トレセン・レンデ"
#   set the zh label to "奥勒·托雷松·托雷森·伦德"
LAST	Lzh	"奥勒·托雷松·托雷森·伦德"
#   set the ko label to "오레 토레손 토레센 렌데"
LAST	Lko	"오레 토레손 토레센 렌데"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000010517303222 Ole Thoreson Toresen Lende, qualified P1810 subject named as Ole Thoreson Toresen Lende
LAST	P2600	"6000000010517303222"	P1810	"Ole Thoreson Toresen Lende"
#   P569 date of birth = +1798-09-16T00:00:00Z/11
LAST	P569	+1798-09-16T00:00:00Z/11	S2600	"6000000010517303222"
#   P570 date of death = +1876-07-10T00:00:00Z/11
LAST	P570	+1876-07-10T00:00:00Z/11	S2600	"6000000010517303222"
#   P40 child = Q141219050 Ane Olsdatter Bø
LAST	P40	Q141219050	S2600	"6000000010517303222"
#   Q141219050 Ane Olsdatter Bø: P22 father = the item just created
Q141219050	P22	LAST	S2600	"6000000010517303222"
#   the item just created: P735 given name = Q2097883 Ole
LAST	P735	Q2097883
#   P734 family name = Q30083619
LAST	P734	Q30083619

# create a new item
CREATE
#   set the en label to "Olov Rudbeck"
LAST	Len	"Olov Rudbeck"
#   set the mul label to "Olov Rudbeck"
LAST	Lmul	"Olov Rudbeck"
#   set the ja label to "オロヴ・ルドベク"
LAST	Lja	"オロヴ・ルドベク"
#   set the zh label to "奥洛夫·鲁德贝克"
LAST	Lzh	"奥洛夫·鲁德贝克"
#   set the ko label to "오롭 루드베크"
LAST	Lko	"오롭 루드베크"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000006127612884 Olov Rudbeck, qualified P1810 subject named as Olov Rudbeck
LAST	P2600	"6000000006127612884"	P1810	"Olov Rudbeck"
#   P569 date of birth = +1712-09-09T00:00:00Z/11
LAST	P569	+1712-09-09T00:00:00Z/11	S2600	"6000000006127612884"
#   P570 date of death = +1736-00-00T00:00:00Z/9
LAST	P570	+1736-00-00T00:00:00Z/9	S2600	"6000000006127612884"
#   P22 father = Q103771956 Olof Rudbeck
LAST	P22	Q103771956	S2600	"6000000006127612884"
#   P25 mother = Q103771971 Anna Maria Törnstjerna, Törne
LAST	P25	Q103771971	S2600	"6000000006127612884"
#   Q103771956 Olof Rudbeck: P40 child = the item just created
Q103771956	P40	LAST	S2600	"6000000006127612884"
#   Q103771971 Anna Maria Törnstjerna, Törne: P40 child = the item just created
Q103771971	P40	LAST	S2600	"6000000006127612884"
#   the item just created: P735 given name = Q21061132 Olov
LAST	P735	Q21061132

# create a new item
CREATE
#   set the en label to "Peter Chydenius"
LAST	Len	"Peter Chydenius"
#   set the mul label to "Peter Chydenius"
LAST	Lmul	"Peter Chydenius"
#   set the ja label to "ピーター・キデニウス"
LAST	Lja	"ピーター・キデニウス"
#   set the zh label to "彼得·基德尼乌斯"
LAST	Lzh	"彼得·基德尼乌斯"
#   set the ko label to "페테르 치데뉴스"
LAST	Lko	"페테르 치데뉴스"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000001190443752 Peter Chydenius, qualified P1810 subject named as Peter Chydenius
LAST	P2600	"6000000001190443752"	P1810	"Peter Chydenius"
#   P569 date of birth = +1794-06-01T00:00:00Z/11
LAST	P569	+1794-06-01T00:00:00Z/11	S2600	"6000000001190443752"
#   P570 date of death = +1865-00-00T00:00:00Z/9
LAST	P570	+1865-00-00T00:00:00Z/9	S2600	"6000000001190443752"
#   P22 father = Q141225740 Jakob Chydenius
LAST	P22	Q141225740	S2600	"6000000001190443752"
#   Q141225740 Jakob Chydenius: P40 child = the item just created
Q141225740	P40	LAST	S2600	"6000000001190443752"
#   the item just created: P735 given name = Q2793400 Peter
LAST	P735	Q2793400
#   add a mul alias "Peter Christian Chydenius"
LAST	Amul	"Peter Christian Chydenius"

# create a new item
CREATE
#   set the en label to "Sigge Guttormson"
LAST	Len	"Sigge Guttormson"
#   set the mul label to "Sigge Guttormson"
LAST	Lmul	"Sigge Guttormson"
#   set the ja label to "シゲ・グトルムソン"
LAST	Lja	"シゲ・グトルムソン"
#   set the zh label to "西盖·古托尔姆松"
LAST	Lzh	"西盖·古托尔姆松"
#   set the ko label to "시게 구토르므손"
LAST	Lko	"시게 구토르므손"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000020999259543 Sigge Guttormson, qualified P1810 subject named as Sigge Guttormson
LAST	P2600	"6000000020999259543"	P1810	"Sigge Guttormson"
#   P22 father = Q10511224 Guttorm Ostmannson of Jämtland & Svealand
LAST	P22	Q10511224	S2600	"6000000020999259543"
#   P25 mother = Q141216349 Ingrid Guttormsdotter
LAST	P25	Q141216349	S2600	"6000000020999259543"
#   Q10511224 Guttorm Ostmannson of Jämtland & Svealand: P40 child = the item just created
Q10511224	P40	LAST	S2600	"6000000020999259543"
#   Q141216349 Ingrid Guttormsdotter: P40 child = the item just created
Q141216349	P40	LAST	S2600	"6000000020999259543"

# create a new item
CREATE
#   the item just created: set the en label to "Søren Jonson Aukland"
LAST	Len	"Søren Jonson Aukland"
#   set the mul label to "Søren Jonson Aukland"
LAST	Lmul	"Søren Jonson Aukland"
#   set the ja label to "セーレン・ヨンソン・アウクランド"
LAST	Lja	"セーレン・ヨンソン・アウクランド"
#   set the zh label to "索伦·永松·奥克兰德"
LAST	Lzh	"索伦·永松·奥克兰德"
#   set the ko label to "쇠렌 존손 아우크란드"
LAST	Lko	"쇠렌 존손 아우크란드"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005607349830 Søren Jonson Aukland, qualified P1810 subject named as Søren Jonson Aukland
LAST	P2600	"6000000005607349830"	P1810	"Søren Jonson Aukland"
#   P22 father = Q141199899 Jon Tollakson Aukland, IV
LAST	P22	Q141199899	S2600	"6000000005607349830"
#   P25 mother = Q141198835 Bergitte Gunnbjørnsdatter Aukland
LAST	P25	Q141198835	S2600	"6000000005607349830"
#   Q141199899 Jon Tollakson Aukland, IV: P40 child = the item just created
Q141199899	P40	LAST	S2600	"6000000005607349830"
#   Q141198835 Bergitte Gunnbjørnsdatter Aukland: P40 child = the item just created
Q141198835	P40	LAST	S2600	"6000000005607349830"

# create a new item
CREATE
#   the item just created: set the en label to "Welf"
LAST	Len	"Welf"
#   set the mul label to "Welf"
LAST	Lmul	"Welf"
#   set the ja label to "ヴェルフ"
LAST	Lja	"ヴェルフ"
#   set the zh label to "韦尔夫"
LAST	Lzh	"韦尔夫"
#   set the ko label to "웨르프"
LAST	Lko	"웨르프"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 4927821250240067090 Welf, qualified P1810 subject named as Welf
LAST	P2600	"4927821250240067090"	P1810	"Welf"
#   P569 date of birth = +1032-00-00T00:00:00Z/9
LAST	P569	+1032-00-00T00:00:00Z/9	S2600	"4927821250240067090"
#   P570 date of death = +1101-11-06T00:00:00Z/11
LAST	P570	+1101-11-06T00:00:00Z/11	S2600	"4927821250240067090"
#   P26 spouse = Q273181 Judith of Flanders
LAST	P26	Q273181	S2600	"4927821250240067090"
#   Q273181 Judith of Flanders: P26 spouse = the item just created
Q273181	P26	LAST	S2600	"4927821250240067090"
#   the item just created: P735 given name = Q73006108 Welf
LAST	P735	Q73006108
#   add a mul alias "Guelph IV of Bavaria"
LAST	Amul	"Guelph IV of Bavaria"
#   Q141249609 Ingrid Charlotta Carlsdotter Ekenbom: P26 spouse = Q141249606 Hans Olofsson Törne
Q141249609	P26	Q141249606	S2600	"6000000000410527402"
#   Q141249606 Hans Olofsson Törne: P26 spouse = Q141249609 Ingrid Charlotta Carlsdotter Ekenbom
Q141249606	P26	Q141249609	S2600	"6000000000410600770"
#   Q141249611 Ivar Toreson Tjentland: P26 spouse = Q141249593 Anna Jonesdatter Tøtland
Q141249611	P26	Q141249593	S2600	"6000000001169232790"
#   Q141249593 Anna Jonesdatter Tøtland: P26 spouse = Q141249611 Ivar Toreson Tjentland
Q141249593	P26	Q141249611	S2600	"6000000001169317582"
#   Q141244225 Karl Nilsson Polviander: P26 spouse = Q141244229 Margareta Katarina Polviander
Q141244225	P26	Q141244229	S2600	"6000000001966670019"
#   Q141244231 Ola Olson Bæreim: P26 spouse = Q141244216 Eli Olsdatter Bærheim
Q141244231	P26	Q141244216	S2600	"6000000002226706375"
#   Q141244226 Knut Bjørnson Bjørheim: P22 father = Q141244210 Bjørn Lauritsen Bjørheim
Q141244226	P22	Q141244210	S2600	"6000000002277957043"
#   Q141244210 Bjørn Lauritsen Bjørheim: P40 child = Q141244226 Knut Bjørnson Bjørheim
Q141244210	P40	Q141244226	S2600	"6000000002330809317"
#   Q141249620 Ola Kristoffersen Kartevoll: P26 spouse = Q141249615 Malena Olsdatter Tjåland
Q141249620	P26	Q141249615	S2600	"6000000002801159071"
#   Q141189070 John Jonassen Hegre: P40 child = Q138687615 Bertrand Olav Olsen Vigdel
Q141189070	P40	Q138687615	S2600	"6000000003491986951"
#   Q141244234 Torstein Gunnarson Frafjord: P26 spouse = Q141244227 Kristi Frafjord
Q141244234	P26	Q141244227	S2600	"6000000005607365222"
#   Q141249615 Malena Olsdatter Tjåland: P26 spouse = Q141249620 Ola Kristoffersen Kartevoll
Q141249615	P26	Q141249620	S2600	"6000000005609534715"
#   Q141244216 Eli Olsdatter Bærheim: P26 spouse = Q141244231 Ola Olson Bæreim
Q141244216	P26	Q141244231	S2600	"6000000006776171569"
#   Q141244212 Carl Åke Posse af Säby: P26 spouse = Q141244208 Beata Christina Hierta
Q141244212	P26	Q141244208	S2600	"6000000008507821635"
#   Q141244208 Beata Christina Hierta: P26 spouse = Q141244212 Carl Åke Posse af Säby
Q141244208	P26	Q141244212	S2600	"6000000008507926141"
#   Q141249602 Fredrika Ulrika Eleonora von Braunjohan: P26 spouse = Q141249599 Carl Hierta
Q141249602	P26	Q141249599	S2600	"6000000008508010957"
#   Q141249599 Carl Hierta: P26 spouse = Q141249602 Fredrika Ulrika Eleonora von Braunjohan
Q141249599	P26	Q141249602	S2600	"6000000008508097243"
#   Q141244229 Margareta Katarina Polviander: P26 spouse = Q141244225 Karl Nilsson Polviander
Q141244229	P26	Q141244225	S2600	"6000000012232723402"
#   Q141244227 Kristi Frafjord: P26 spouse = Q141244234 Torstein Gunnarson Frafjord
Q141244227	P26	Q141244234	S2600	"6000000014233913271"
#   Q141205896 Ane Marie Konstanse Amanda Kristine Hegre: P40 child = Q138687615 Bertrand Olav Olsen Vigdel
Q141205896	P40	Q138687615	S2600	"6000000018935780138"
#   Q141249608 Henriette Wilhelmine Kjelsen: P26 spouse = Q141249613 Jørgen Anton Wendt
Q141249608	P26	Q141249613	S2600	"6000000021080450944"
#   Q141249613 Jørgen Anton Wendt: P26 spouse = Q141249608 Henriette Wilhelmine Kjelsen
Q141249613	P26	Q141249608	S2600	"6000000021080514848"
#   Q141249614 Lovisa Sofia Benzelstierna: P40 child = Q141249623 Olof Bratt Benzelstierna
Q141249614	P40	Q141249623	S2600	"6000000030305287826"
#   Q141249590 Anna Christina Flygare: P22 father = Q141249604 Gustaf Schilling
Q141249590	P22	Q141249604	S2600	"6000000064143495006"
#   Q141249604 Gustaf Schilling: P40 child = Q141249590 Anna Christina Flygare
Q141249604	P40	Q141249590	S2600	"6000000180950236868"
#   Q141249623 Olof Bratt Benzelstierna: P25 mother = Q141249614 Lovisa Sofia Benzelstierna
Q141249623	P25	Q141249614	S2600	"6000000192504935864"

