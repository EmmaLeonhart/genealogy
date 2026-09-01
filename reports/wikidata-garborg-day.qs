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
#   2667 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   Q138582215 Eva Christina Eriksdotter de Besche: set the ja label to "エヴァ・クリスティーナ・エリクスドッテル・デ・ベシェ"
Q138582215	Lja	"エヴァ・クリスティーナ・エリクスドッテル・デ・ベシェ"
#   set the zh label to "伊娃·克里斯蒂娜·埃里克斯多塔·德·贝谢"
Q138582215	Lzh	"伊娃·克里斯蒂娜·埃里克斯多塔·德·贝谢"
#   set the ko label to "에바 츠리스티나 에리크스도테르 데 베세"
Q138582215	Lko	"에바 츠리스티나 에리크스도테르 데 베세"
#   Q109952542 Catharina Sabina Crail von Bamberg: set the ja label to "カタリーナ・サビナ・クライル・ヴォン・バムベルグ"
Q109952542	Lja	"カタリーナ・サビナ・クライル・ヴォン・バムベルグ"
#   set the zh label to "卡塔里娜·萨比娜·克拉伊尔·翁·巴姆贝尔格"
Q109952542	Lzh	"卡塔里娜·萨比娜·克拉伊尔·翁·巴姆贝尔格"
#   set the ko label to "카타리나 사비나 크라일 본 밤베르그"
Q109952542	Lko	"카타리나 사비나 크라일 본 밤베르그"
#   Q6011791 Ruben Frans Isendorf Nilson: set the ja label to "ルーベン・フランス・イセンドルフ・ニルソン"
Q6011791	Lja	"ルーベン・フランス・イセンドルフ・ニルソン"
#   set the zh label to "鲁本·弗兰斯·伊森多尔夫·尼尔松"
Q6011791	Lzh	"鲁本·弗兰斯·伊森多尔夫·尼尔松"
#   set the ko label to "루벤 프란스 이센도르프 닐손"
Q6011791	Lko	"루벤 프란스 이센도르프 닐손"
#   set the ja label to "カール・ヨハン・オスカー・ヴォン・ヌメルス"
Q104172926	Lja	"カール・ヨハン・オスカー・ヴォン・ヌメルス"
#   set the zh label to "卡尔·约翰·奥斯卡·翁·努梅尔斯"
Q104172926	Lzh	"卡尔·约翰·奥斯卡·翁·努梅尔斯"
#   set the ko label to "카르르 조한 오스카르 본 누메르스"
Q104172926	Lko	"카르르 조한 오스카르 본 누메르스"
#   Q101247544 Anna Göransdotter Snakenborg: set the ja label to "アンナ・ゴランスドッテル・スナケンボルグ"
Q101247544	Lja	"アンナ・ゴランスドッテル・スナケンボルグ"
#   set the zh label to "安娜·戈兰斯多特·斯纳肯博尔格"
Q101247544	Lzh	"安娜·戈兰斯多特·斯纳肯博尔格"
#   set the ko label to "안나 괴란스도테르 스나켄보르그"
Q101247544	Lko	"안나 괴란스도테르 스나켄보르그"

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Alfred Bakke"
LAST	Len	"Alfred Bakke"
#   set the mul label to "Alfred Bakke"
LAST	Lmul	"Alfred Bakke"
#   set the ja label to "アルフレッド・バッケ"
LAST	Lja	"アルフレッド・バッケ"
#   set the zh label to "阿尔弗雷德·巴凯"
LAST	Lzh	"阿尔弗雷德·巴凯"
#   set the ko label to "알프레드 바케"
LAST	Lko	"알프레드 바케"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000032101017397 Alfred Bakke, qualified P1810 subject named as Alfred Bakke
LAST	P2600	"6000000032101017397"	P1810	"Alfred Bakke"
#   P569 date of birth = +1896-01-14T00:00:00Z/11
LAST	P569	+1896-01-14T00:00:00Z/11	S2600	"6000000032101017397"
#   P570 date of death = +1982-02-06T00:00:00Z/11
LAST	P570	+1982-02-06T00:00:00Z/11	S2600	"6000000032101017397"
#   P22 father = Q141216359 Andrew J. Bakke
LAST	P22	Q141216359	S2600	"6000000032101017397"
#   P25 mother = Q141206058 Bertha Bakke
LAST	P25	Q141206058	S2600	"6000000032101017397"
#   Q141216359 Andrew J. Bakke: P40 child = the item just created
Q141216359	P40	LAST	S2600	"6000000032101017397"
#   Q141206058 Bertha Bakke: P40 child = the item just created
Q141206058	P40	LAST	S2600	"6000000032101017397"
#   the item just created: P735 given name = Q3480335 Alfred
LAST	P735	Q3480335
#   P734 family name = Q27887927 Bakke
LAST	P734	Q27887927

# create a new item
CREATE
#   set the en label to "Anna Christina Gyllenstierna af Björksund och Helgö"
LAST	Len	"Anna Christina Gyllenstierna af Björksund och Helgö"
#   set the mul label to "Anna Christina Gyllenstierna af Björksund och Helgö"
LAST	Lmul	"Anna Christina Gyllenstierna af Björksund och Helgö"
#   set the ja label to "アンナ・クリスティーナ・ユレンシェーナ・アフ・ブヨルクスンド・オク・ヘルゴ"
LAST	Lja	"アンナ・クリスティーナ・ユレンシェーナ・アフ・ブヨルクスンド・オク・ヘルゴ"
#   set the zh label to "安娜·克里斯蒂娜·吉伦斯蒂埃尔纳·阿夫·布约尔克孙德·奥克·赫尔戈"
LAST	Lzh	"安娜·克里斯蒂娜·吉伦斯蒂埃尔纳·阿夫·布约尔克孙德·奥克·赫尔戈"
#   set the ko label to "안나 츠리스티나 길렌스티에르나 아프 브죄르크순드 오츠 헬괴"
LAST	Lko	"안나 츠리스티나 길렌스티에르나 아프 브죄르크순드 오츠 헬괴"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000006704094498 Anna Christina Gyllenstierna af Björksund och Helgö, qualified P1810 subject named as Anna Christina Gyllenstierna af Björksund och Helgö
LAST	P2600	"6000000006704094498"	P1810	"Anna Christina Gyllenstierna af Björksund och Helgö"
#   P569 date of birth = +1657-11-13T00:00:00Z/11
LAST	P569	+1657-11-13T00:00:00Z/11	S2600	"6000000006704094498"
#   P570 date of death = +1715-08-25T00:00:00Z/11
LAST	P570	+1715-08-25T00:00:00Z/11	S2600	"6000000006704094498"
#   P40 child = Q4951688 Margareta Gyllenstierna af Fogelvik
LAST	P40	Q4951688	S2600	"6000000006704094498"
#   Q4951688 Margareta Gyllenstierna af Fogelvik: P25 mother = the item just created
Q4951688	P25	LAST	S2600	"6000000006704094498"
#   the item just created: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1083457 Christina, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1083457	P1545	"2"	P3831	Q245025
#   P734 family name = Q47456776 Gyllenstierna, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q47456776	P3831	Q28418670
#   P734 family name = Q37523137, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q37523137	P3831	Q28418670

# create a new item
CREATE
#   set the en label to "Anna Elisabet Gripenstierna"
LAST	Len	"Anna Elisabet Gripenstierna"
#   set the mul label to "Anna Elisabet Gripenstierna"
LAST	Lmul	"Anna Elisabet Gripenstierna"
#   set the ja label to "アンナ・エリーザベト・グリペンスティエルナ"
LAST	Lja	"アンナ・エリーザベト・グリペンスティエルナ"
#   set the zh label to "安娜·伊丽莎白·格里彭斯蒂埃尔纳"
LAST	Lzh	"安娜·伊丽莎白·格里彭斯蒂埃尔纳"
#   set the ko label to "안나 에리사베트 그리펜스티에르나"
LAST	Lko	"안나 에리사베트 그리펜스티에르나"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000032063019943 Anna Elisabet Gripenstierna, qualified P1810 subject named as Anna Elisabet Gripenstierna
LAST	P2600	"6000000032063019943"	P1810	"Anna Elisabet Gripenstierna"
#   P569 date of birth = +1708-01-17T00:00:00Z/11
LAST	P569	+1708-01-17T00:00:00Z/11	S2600	"6000000032063019943"
#   P570 date of death = +1798-11-26T00:00:00Z/11
LAST	P570	+1798-11-26T00:00:00Z/11	S2600	"6000000032063019943"
#   P26 spouse = Q141249726 Conrad Ludvig Transchiöld till Arnöberg
LAST	P26	Q141249726	S2600	"6000000032063019943"
#   P40 child = Q141217415 Ottiliana Vilhelmina Conradsdotter Transchiöld
LAST	P40	Q141217415	S2600	"6000000032063019943"
#   Q141249726 Conrad Ludvig Transchiöld till Arnöberg: P26 spouse = the item just created
Q141249726	P26	LAST	S2600	"6000000032063019943"
#   Q141217415 Ottiliana Vilhelmina Conradsdotter Transchiöld: P25 mother = the item just created
Q141217415	P25	LAST	S2600	"6000000032063019943"
#   the item just created: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P735 given name = Q16423275 Elisabet, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q16423275	P1545	"2"	P3831	Q245025
#   add a mul alias "Transchiöld Gripenstierna"
LAST	Amul	"Transchiöld Gripenstierna"

# create a new item
CREATE
#   set the en label to "Anna Maria Norn"
LAST	Len	"Anna Maria Norn"
#   set the mul label to "Anna Maria Norn"
LAST	Lmul	"Anna Maria Norn"
#   set the ja label to "アンナ・マリア・ノルン"
LAST	Lja	"アンナ・マリア・ノルン"
#   set the zh label to "安娜·玛丽亚·诺尔恩"
LAST	Lzh	"安娜·玛丽亚·诺尔恩"
#   set the ko label to "안나 마리아 노르느"
LAST	Lko	"안나 마리아 노르느"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000008496890948 Anna Maria Norn, qualified P1810 subject named as Anna Maria Norn
LAST	P2600	"6000000008496890948"	P1810	"Anna Maria Norn"
#   P569 date of birth = +1714-07-26T00:00:00Z/11
LAST	P569	+1714-07-26T00:00:00Z/11	S2600	"6000000008496890948"
#   P570 date of death = +1767-00-00T00:00:00Z/9
LAST	P570	+1767-00-00T00:00:00Z/9	S2600	"6000000008496890948"
#   P26 spouse = Q473225 Georg Brandt
LAST	P26	Q473225	S2600	"6000000008496890948"
#   P40 child = Q134546510 Catharina Elisabet Brandt
LAST	P40	Q134546510	S2600	"6000000008496890948"
#   Q473225 Georg Brandt: P26 spouse = the item just created
Q473225	P26	LAST	S2600	"6000000008496890948"
#   Q134546510 Catharina Elisabet Brandt: P25 mother = the item just created
Q134546510	P25	LAST	S2600	"6000000008496890948"
#   the item just created: P735 given name = Q666578 Anna, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q666578	P1545	"1"	P7452	Q3409033
#   P735 given name = Q325872 Maria, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q325872	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Anna Nilsdotter"
LAST	Len	"Anna Nilsdotter"
#   set the mul label to "Anna Nilsdotter"
LAST	Lmul	"Anna Nilsdotter"
#   set the ja label to "アンナ・ニルスドッテル"
LAST	Lja	"アンナ・ニルスドッテル"
#   set the zh label to "安娜·尼尔斯多特"
LAST	Lzh	"安娜·尼尔斯多特"
#   set the ko label to "안나 닐스도테르"
LAST	Lko	"안나 닐스도테르"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000011078617825 Anna Nilsdotter, qualified P1810 subject named as Anna Nilsdotter
LAST	P2600	"6000000011078617825"	P1810	"Anna Nilsdotter"
#   P569 date of birth = +1736-00-00T00:00:00Z/9
LAST	P569	+1736-00-00T00:00:00Z/9	S2600	"6000000011078617825"
#   P570 date of death = +1799-00-00T00:00:00Z/9
LAST	P570	+1799-00-00T00:00:00Z/9	S2600	"6000000011078617825"
#   P40 child = Q141219284 Maria Benjaminsdotter
LAST	P40	Q141219284	S2600	"6000000011078617825"
#   Q141219284 Maria Benjaminsdotter: P25 mother = the item just created
Q141219284	P25	LAST	S2600	"6000000011078617825"

# create a new item
CREATE
#   the item just created: set the en label to "Benjamin Mårtensson"
LAST	Len	"Benjamin Mårtensson"
#   set the mul label to "Benjamin Mårtensson"
LAST	Lmul	"Benjamin Mårtensson"
#   set the ja label to "ベンジャミン・モールテンソン"
LAST	Lja	"ベンジャミン・モールテンソン"
#   set the zh label to "本杰明·莫尔滕松"
LAST	Lzh	"本杰明·莫尔滕松"
#   set the ko label to "베나민 모르텐손"
LAST	Lko	"베나민 모르텐손"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000011078886609 Benjamin Mårtensson, qualified P1810 subject named as Benjamin Mårtensson
LAST	P2600	"6000000011078886609"	P1810	"Benjamin Mårtensson"
#   P569 date of birth = +1738-12-04T00:00:00Z/11
LAST	P569	+1738-12-04T00:00:00Z/11	S2600	"6000000011078886609"
#   P570 date of death = +1806-00-00T00:00:00Z/9
LAST	P570	+1806-00-00T00:00:00Z/9	S2600	"6000000011078886609"
#   P40 child = Q141219284 Maria Benjaminsdotter
LAST	P40	Q141219284	S2600	"6000000011078886609"
#   Q141219284 Maria Benjaminsdotter: P22 father = the item just created
Q141219284	P22	LAST	S2600	"6000000011078886609"

# create a new item
CREATE
#   the item just created: set the en label to "Bjørn Gunnarson Mele"
LAST	Len	"Bjørn Gunnarson Mele"
#   set the mul label to "Bjørn Gunnarson Mele"
LAST	Lmul	"Bjørn Gunnarson Mele"
#   add a mul alias "Bjørn Gunnarson Gunnarson"
LAST	Amul	"Bjørn Gunnarson Gunnarson"
#   set the ja label to "ビョルン・グナルソン・メーレ"
LAST	Lja	"ビョルン・グナルソン・メーレ"
#   set the zh label to "比约恩·古纳尔松·梅勒"
LAST	Lzh	"比约恩·古纳尔松·梅勒"
#   set the ko label to "브죄르느 군나르손 메레"
LAST	Lko	"브죄르느 군나르손 메레"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 4462693 Bjørn Gunnarson Mele, qualified P1810 subject named as Bjørn Gunnarson Gunnarson
LAST	P2600	"4462693"	P1810	"Bjørn Gunnarson Gunnarson"
#   P569 date of birth = +1577-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P569	+1577-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"4462693"
#   P570 date of death = +1661-00-00T00:00:00Z/9
LAST	P570	+1661-00-00T00:00:00Z/9	S2600	"4462693"
#   P40 child = Q141198507 Tormod Bjørnson Mele
LAST	P40	Q141198507	S2600	"4462693"
#   Q141198507 Tormod Bjørnson Mele: P22 father = the item just created
Q141198507	P22	LAST	S2600	"4462693"
#   the item just created: P735 given name = Q18918288 Bjørn
LAST	P735	Q18918288
#   add a mul alias "Bjørn Mele"
LAST	Amul	"Bjørn Mele"

# create a new item
CREATE
#   set the en label to "Brita Hansdotter"
LAST	Len	"Brita Hansdotter"
#   set the mul label to "Brita Hansdotter"
LAST	Lmul	"Brita Hansdotter"
#   set the ja label to "ブリッタ・ハンスドッテル"
LAST	Lja	"ブリッタ・ハンスドッテル"
#   set the zh label to "布里塔·汉斯多特"
LAST	Lzh	"布里塔·汉斯多特"
#   set the ko label to "브리타 한스도테르"
LAST	Lko	"브리타 한스도테르"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000007814095826 Brita Hansdotter, qualified P1810 subject named as Brita Hansdotter
LAST	P2600	"6000000007814095826"	P1810	"Brita Hansdotter"
#   P569 date of birth = +1636-00-00T00:00:00Z/9
LAST	P569	+1636-00-00T00:00:00Z/9	S2600	"6000000007814095826"
#   P570 date of death = +1660-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P570	+1660-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"6000000007814095826"
#   P26 spouse = Q5613434 Börje Cronberg
LAST	P26	Q5613434	S2600	"6000000007814095826"
#   Q5613434 Börje Cronberg: P26 spouse = the item just created
Q5613434	P26	LAST	S2600	"6000000007814095826"
#   the item just created: P735 given name = Q918013
LAST	P735	Q918013

# create a new item
CREATE
#   set the en label to "Brita Magdalena Eriksdotter Rahm"
LAST	Len	"Brita Magdalena Eriksdotter Rahm"
#   set the mul label to "Brita Magdalena Eriksdotter Rahm"
LAST	Lmul	"Brita Magdalena Eriksdotter Rahm"
#   set the ja label to "ブリッタ・マグダレーナ・エリクスドッテル・ラーム"
LAST	Lja	"ブリッタ・マグダレーナ・エリクスドッテル・ラーム"
#   set the zh label to "布里塔·马格达莱纳·埃里克斯多塔·拉姆"
LAST	Lzh	"布里塔·马格达莱纳·埃里克斯多塔·拉姆"
#   set the ko label to "브리타 막다레나 에리크스도테르 라흐므"
LAST	Lko	"브리타 막다레나 에리크스도테르 라흐므"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000001186122035 Brita Magdalena Eriksdotter Rahm, qualified P1810 subject named as Brita Magdalena Eriksdotter Rahm
LAST	P2600	"6000000001186122035"	P1810	"Brita Magdalena Eriksdotter Rahm"
#   P569 date of birth = +1755-02-09T00:00:00Z/11
LAST	P569	+1755-02-09T00:00:00Z/11	S2600	"6000000001186122035"
#   P570 date of death = +1815-06-29T00:00:00Z/11
LAST	P570	+1815-06-29T00:00:00Z/11	S2600	"6000000001186122035"
#   P26 spouse = Q141225740 Jakob Chydenius
LAST	P26	Q141225740	S2600	"6000000001186122035"
#   P40 child = Q141249739 Peter Chydenius
LAST	P40	Q141249739	S2600	"6000000001186122035"
#   Q141225740 Jakob Chydenius: P26 spouse = the item just created
Q141225740	P26	LAST	S2600	"6000000001186122035"
#   Q141249739 Peter Chydenius: P25 mother = the item just created
Q141249739	P25	LAST	S2600	"6000000001186122035"
#   the item just created: P735 given name = Q918013, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q918013	P1545	"1"	P7452	Q3409033
#   P735 given name = Q842544 Magdalena, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q842544	P1545	"2"	P3831	Q245025
#   P5056 patronym or matronym = Q130232912 Eriksdotter
LAST	P5056	Q130232912

# create a new item
CREATE
#   set the en label to "Carl Henrik Posse af Säby"
LAST	Len	"Carl Henrik Posse af Säby"
#   set the mul label to "Carl Henrik Posse af Säby"
LAST	Lmul	"Carl Henrik Posse af Säby"
#   set the ja label to "カール・ヘンリク・ポッセ・アフ・セビ"
LAST	Lja	"カール・ヘンリク・ポッセ・アフ・セビ"
#   set the zh label to "卡尔·亨里克·波塞·阿夫·塞比"
LAST	Lzh	"卡尔·亨里克·波塞·阿夫·塞比"
#   set the ko label to "카르르 헨리크 포세 아프 세비"
LAST	Lko	"카르르 헨리크 포세 아프 세비"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000007182710798 Carl Henrik Posse af Säby, qualified P1810 subject named as Carl Henrik Posse af Säby
LAST	P2600	"6000000007182710798"	P1810	"Carl Henrik Posse af Säby"
#   P569 date of birth = +1705-06-23T00:00:00Z/11
LAST	P569	+1705-06-23T00:00:00Z/11	S2600	"6000000007182710798"
#   P570 date of death = +1761-04-30T00:00:00Z/11
LAST	P570	+1761-04-30T00:00:00Z/11	S2600	"6000000007182710798"
#   P40 child = Q141244212 Carl Åke Posse af Säby
LAST	P40	Q141244212	S2600	"6000000007182710798"
#   Q141244212 Carl Åke Posse af Säby: P22 father = the item just created
Q141244212	P22	LAST	S2600	"6000000007182710798"

# create a new item
CREATE
#   the item just created: set the en label to "Claes Sandels"
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
#   set the en label to "Fredrika Grönhagen"
LAST	Len	"Fredrika Grönhagen"
#   set the mul label to "Fredrika Grönhagen"
LAST	Lmul	"Fredrika Grönhagen"
#   set the ja label to "フレデリカ・グロンハゲン"
LAST	Lja	"フレデリカ・グロンハゲン"
#   set the zh label to "夫雷德里卡·格龙哈根"
LAST	Lzh	"夫雷德里卡·格龙哈根"
#   set the ko label to "프레드리카 그뢴하겐"
LAST	Lko	"프레드리카 그뢴하겐"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000019659634521 Fredrika Grönhagen, qualified P1810 subject named as Fredrika Grönhagen
LAST	P2600	"6000000019659634521"	P1810	"Fredrika Grönhagen"
#   P569 date of birth = +1765-10-08T00:00:00Z/11
LAST	P569	+1765-10-08T00:00:00Z/11	S2600	"6000000019659634521"
#   P570 date of death = +1835-01-28T00:00:00Z/11
LAST	P570	+1835-01-28T00:00:00Z/11	S2600	"6000000019659634521"
#   P40 child = Q5792035 Jacob August von Hartmansdorff
LAST	P40	Q5792035	S2600	"6000000019659634521"
#   Q5792035 Jacob August von Hartmansdorff: P25 mother = the item just created
Q5792035	P25	LAST	S2600	"6000000019659634521"
#   the item just created: P735 given name = Q5499550 Fredrika
LAST	P735	Q5499550

# create a new item
CREATE
#   set the en label to "Helena Åkesdotter Soop"
LAST	Len	"Helena Åkesdotter Soop"
#   set the mul label to "Helena Åkesdotter Soop"
LAST	Lmul	"Helena Åkesdotter Soop"
#   set the ja label to "ヘレナ・オーケスドッテル・ソオプ"
LAST	Lja	"ヘレナ・オーケスドッテル・ソオプ"
#   set the zh label to "海伦娜·奥凯斯多特·索奥普"
LAST	Lzh	"海伦娜·奥凯斯多特·索奥普"
#   set the ko label to "헤레나 오케스도테르 수프"
LAST	Lko	"헤레나 오케스도테르 수프"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000007182716723 Helena Åkesdotter Soop, qualified P1810 subject named as Helena Åkesdotter Soop
LAST	P2600	"6000000007182716723"	P1810	"Helena Åkesdotter Soop"
#   P569 date of birth = +1712-06-28T00:00:00Z/11
LAST	P569	+1712-06-28T00:00:00Z/11	S2600	"6000000007182716723"
#   P570 date of death = +1796-06-06T00:00:00Z/11
LAST	P570	+1796-06-06T00:00:00Z/11	S2600	"6000000007182716723"
#   P40 child = Q141244212 Carl Åke Posse af Säby
LAST	P40	Q141244212	S2600	"6000000007182716723"
#   Q141244212 Carl Åke Posse af Säby: P25 mother = the item just created
Q141244212	P25	LAST	S2600	"6000000007182716723"

# create a new item
CREATE
#   the item just created: set the en label to "Henrika Birgitta Wachtmeister af Johannishus"
LAST	Len	"Henrika Birgitta Wachtmeister af Johannishus"
#   set the mul label to "Henrika Birgitta Wachtmeister af Johannishus"
LAST	Lmul	"Henrika Birgitta Wachtmeister af Johannishus"
#   set the ja label to "ヘンリカ・ビルギッタ・ヴァクトメイステル・アフ・ヨハニスフス"
LAST	Lja	"ヘンリカ・ビルギッタ・ヴァクトメイステル・アフ・ヨハニスフス"
#   set the zh label to "亨里卡·比尔吉塔·瓦克特梅伊斯特尔·阿夫·约哈尼斯胡斯"
LAST	Lzh	"亨里卡·比尔吉塔·瓦克特梅伊斯特尔·阿夫·约哈尼斯胡斯"
#   set the ko label to "헨리카 비르기타 와츠트메이스테르 아프 조한니수스"
LAST	Lko	"헨리카 비르기타 와츠트메이스테르 아프 조한니수스"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000006127526153 Henrika Birgitta Wachtmeister af Johannishus, qualified P1810 subject named as Henrika Birgitta Wachtmeister af Johannishus
LAST	P2600	"6000000006127526153"	P1810	"Henrika Birgitta Wachtmeister af Johannishus"
#   P569 date of birth = +1749-00-00T00:00:00Z/9
LAST	P569	+1749-00-00T00:00:00Z/9	S2600	"6000000006127526153"
#   P570 date of death = +1819-00-00T00:00:00Z/9
LAST	P570	+1819-00-00T00:00:00Z/9	S2600	"6000000006127526153"
#   P26 spouse = Q19721217 Salomon Christoffer von Köhler
LAST	P26	Q19721217	S2600	"6000000006127526153"
#   Q19721217 Salomon Christoffer von Köhler: P26 spouse = the item just created
Q19721217	P26	LAST	S2600	"6000000006127526153"
#   the item just created: P735 given name = Q19816187 Birgitta, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q19816187	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Jacob Baltzar von Hartmansdorff"
LAST	Len	"Jacob Baltzar von Hartmansdorff"
#   set the mul label to "Jacob Baltzar von Hartmansdorff"
LAST	Lmul	"Jacob Baltzar von Hartmansdorff"
#   set the ja label to "ジェイコブ・バルツァール・ヴォン・ハルトマンスドルフ"
LAST	Lja	"ジェイコブ・バルツァール・ヴォン・ハルトマンスドルフ"
#   set the zh label to "雅各布·巴尔特扎尔·翁·哈尔特曼斯多尔夫"
LAST	Lzh	"雅各布·巴尔特扎尔·翁·哈尔特曼斯多尔夫"
#   set the ko label to "자콥 발트자르 본 하르트만스도르프"
LAST	Lko	"자콥 발트자르 본 하르트만스도르프"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000019659479506 Jacob Baltzar von Hartmansdorff, qualified P1810 subject named as Jacob Baltzar von Hartmansdorff
LAST	P2600	"6000000019659479506"	P1810	"Jacob Baltzar von Hartmansdorff"
#   P569 date of birth = +1752-04-09T00:00:00Z/11
LAST	P569	+1752-04-09T00:00:00Z/11	S2600	"6000000019659479506"
#   P570 date of death = +1802-08-26T00:00:00Z/11
LAST	P570	+1802-08-26T00:00:00Z/11	S2600	"6000000019659479506"
#   P40 child = Q5792035 Jacob August von Hartmansdorff
LAST	P40	Q5792035	S2600	"6000000019659479506"
#   Q5792035 Jacob August von Hartmansdorff: P22 father = the item just created
Q5792035	P22	LAST	S2600	"6000000019659479506"
#   the item just created: P735 given name = Q25999604 Jacob, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q25999604	P1545	"1"	P7452	Q3409033

# create a new item
CREATE
#   set the en label to "Joachim Johnson Lea"
LAST	Len	"Joachim Johnson Lea"
#   set the mul label to "Joachim Johnson Lea"
LAST	Lmul	"Joachim Johnson Lea"
#   set the ja label to "ヨアヒム・ジョンソン・リー"
LAST	Lja	"ヨアヒム・ジョンソン・リー"
#   set the zh label to "约阿希姆·约翰逊·莉亚"
LAST	Lzh	"约阿希姆·约翰逊·莉亚"
#   set the ko label to "조아침 조흐느손 레아"
LAST	Lko	"조아침 조흐느손 레아"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000025793788004 Joachim Johnson Lea, qualified P1810 subject named as Joachim Johnson Lea
LAST	P2600	"6000000025793788004"	P1810	"Joachim Johnson Lea"
#   P569 date of birth = +1874-10-16T00:00:00Z/11
LAST	P569	+1874-10-16T00:00:00Z/11	S2600	"6000000025793788004"
#   P570 date of death = +1960-06-29T00:00:00Z/11
LAST	P570	+1960-06-29T00:00:00Z/11	S2600	"6000000025793788004"
#   P26 spouse = Q141189081 Lotte Birgithe Gustava Jonasdatter Lea
LAST	P26	Q141189081	S2600	"6000000025793788004"
#   Q141189081 Lotte Birgithe Gustava Jonasdatter Lea: P26 spouse = the item just created
Q141189081	P26	LAST	S2600	"6000000025793788004"
#   the item just created: P735 given name = Q4926961 Joachim
LAST	P735	Q4926961
#   P734 family name = Q6508166 Lea
LAST	P734	Q6508166

# create a new item
CREATE
#   set the en label to "Margareta Johansdotter Wallensteen"
LAST	Len	"Margareta Johansdotter Wallensteen"
#   set the mul label to "Margareta Johansdotter Wallensteen"
LAST	Lmul	"Margareta Johansdotter Wallensteen"
#   set the ja label to "マルガレータ・ヨハンスドッテル・ヴァレンステエン"
LAST	Lja	"マルガレータ・ヨハンスドッテル・ヴァレンステエン"
#   set the zh label to "瑪格麗塔·约汉斯多特·瓦伦斯特恩"
LAST	Lzh	"瑪格麗塔·约汉斯多特·瓦伦斯特恩"
#   set the ko label to "마르가레타 조한스도테르 와르렌스틴"
LAST	Lko	"마르가레타 조한스도테르 와르렌스틴"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000002255382033 Margareta Johansdotter Wallensteen, qualified P1810 subject named as Margareta Johansdotter Wallensteen
LAST	P2600	"6000000002255382033"	P1810	"Margareta Johansdotter Wallensteen"
#   P569 date of birth = +1676-00-00T00:00:00Z/9
LAST	P569	+1676-00-00T00:00:00Z/9	S2600	"6000000002255382033"
#   P570 date of death = +1722-00-00T00:00:00Z/9
LAST	P570	+1722-00-00T00:00:00Z/9	S2600	"6000000002255382033"
#   P40 child = Q141249601 Christina Juslenius
LAST	P40	Q141249601	S2600	"6000000002255382033"
#   Q141249601 Christina Juslenius: P25 mother = the item just created
Q141249601	P25	LAST	S2600	"6000000002255382033"
#   the item just created: P735 given name = Q8274988 Margareta
LAST	P735	Q8274988

# create a new item
CREATE
#   set the en label to "Margareta Sofia Rabenius"
LAST	Len	"Margareta Sofia Rabenius"
#   set the mul label to "Margareta Sofia Rabenius"
LAST	Lmul	"Margareta Sofia Rabenius"
#   set the ja label to "マルガレータ・ソフィア・ラベニウス"
LAST	Lja	"マルガレータ・ソフィア・ラベニウス"
#   set the zh label to "瑪格麗塔·索菲娅·拉贝尼乌斯"
LAST	Lzh	"瑪格麗塔·索菲娅·拉贝尼乌斯"
#   set the ko label to "마르가레타 소피아 라베뉴스"
LAST	Lko	"마르가레타 소피아 라베뉴스"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000010763555352 Margareta Sofia Rabenius, qualified P1810 subject named as Margareta Sofia Rabenius
LAST	P2600	"6000000010763555352"	P1810	"Margareta Sofia Rabenius"
#   P569 date of birth = +1765-02-27T00:00:00Z/11
LAST	P569	+1765-02-27T00:00:00Z/11	S2600	"6000000010763555352"
#   P570 date of death = +1812-12-03T00:00:00Z/11
LAST	P570	+1812-12-03T00:00:00Z/11	S2600	"6000000010763555352"
#   P22 father = Q6060365 Olof Ingelsson Rabenius
LAST	P22	Q6060365	S2600	"6000000010763555352"
#   P25 mother = Q66711908 Anna Christina Bruncrona
LAST	P25	Q66711908	S2600	"6000000010763555352"
#   Q6060365 Olof Ingelsson Rabenius: P40 child = the item just created
Q6060365	P40	LAST	S2600	"6000000010763555352"
#   Q66711908 Anna Christina Bruncrona: P40 child = the item just created
Q66711908	P40	LAST	S2600	"6000000010763555352"
#   the item just created: P735 given name = Q8274988 Margareta, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q8274988	P1545	"1"	P7452	Q3409033
#   P735 given name = Q18201520 Sofia, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q18201520	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Marta Joakimsdatter Lea"
LAST	Len	"Marta Joakimsdatter Lea"
#   set the mul label to "Marta Joakimsdatter Lea"
LAST	Lmul	"Marta Joakimsdatter Lea"
#   set the ja label to "マルタ・ヨアキムスダッテル・リー"
LAST	Lja	"マルタ・ヨアキムスダッテル・リー"
#   set the zh label to "玛尔塔·约阿基姆斯达特·莉亚"
LAST	Lzh	"玛尔塔·约阿基姆斯达特·莉亚"
#   set the ko label to "마르타 조아킴스다테르 레아"
LAST	Lko	"마르타 조아킴스다테르 레아"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000025810442031 Marta Joakimsdatter Lea, qualified P1810 subject named as Marta Joakimsdatter Lea
LAST	P2600	"6000000025810442031"	P1810	"Marta Joakimsdatter Lea"
#   P569 date of birth = +1901-02-24T00:00:00Z/11
LAST	P569	+1901-02-24T00:00:00Z/11	S2600	"6000000025810442031"
#   P570 date of death = +1984-01-21T00:00:00Z/11
LAST	P570	+1984-01-21T00:00:00Z/11	S2600	"6000000025810442031"
#   P25 mother = Q141189081 Lotte Birgithe Gustava Jonasdatter Lea
LAST	P25	Q141189081	S2600	"6000000025810442031"
#   Q141189081 Lotte Birgithe Gustava Jonasdatter Lea: P40 child = the item just created
Q141189081	P40	LAST	S2600	"6000000025810442031"
#   the item just created: P735 given name = Q846741 Marta
LAST	P735	Q846741
#   P734 family name = Q6508166 Lea
LAST	P734	Q6508166

# create a new item
CREATE
#   set the en label to "Ole LarsenLauritsen Larsen"
LAST	Len	"Ole LarsenLauritsen Larsen"
#   set the mul label to "Ole LarsenLauritsen Larsen"
LAST	Lmul	"Ole LarsenLauritsen Larsen"
#   add a mul alias "Ole LarsenLauritsen Tjaland"
LAST	Amul	"Ole LarsenLauritsen Tjaland"
#   set the ja label to "オーレ・ラルセンラウリトセン・ラーセン"
LAST	Lja	"オーレ・ラルセンラウリトセン・ラーセン"
#   set the zh label to "奥勒·拉尔森拉乌里特森·拉森"
LAST	Lzh	"奥勒·拉尔森拉乌里特森·拉森"
#   set the ko label to "오레 라르센라우리첸 라르센"
LAST	Lko	"오레 라르센라우리첸 라르센"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000026088722196 Ole LarsenLauritsen Larsen, qualified P1810 subject named as Ole LarsenLauritsen Tjaland *
LAST	P2600	"6000000026088722196"	P1810	"Ole LarsenLauritsen Tjaland *"
#   P569 date of birth = +1649-00-00T00:00:00Z/9
LAST	P569	+1649-00-00T00:00:00Z/9	S2600	"6000000026088722196"
#   P40 child = Q141249615 Malena Olsdatter Tjåland
LAST	P40	Q141249615	S2600	"6000000026088722196"
#   Q141249615 Malena Olsdatter Tjåland: P22 father = the item just created
Q141249615	P22	LAST	S2600	"6000000026088722196"
#   the item just created: P735 given name = Q2097883 Ole
LAST	P735	Q2097883
#   P734 family name = Q13099004 Larsen
LAST	P734	Q13099004
#   add a mul alias "Ole Larsen"
LAST	Amul	"Ole Larsen"

# create a new item
CREATE
#   set the en label to "Rakel Hegre"
LAST	Len	"Rakel Hegre"
#   set the mul label to "Rakel Hegre"
LAST	Lmul	"Rakel Hegre"
#   set the ja label to "ラケル・ヘグレ"
LAST	Lja	"ラケル・ヘグレ"
#   set the zh label to "拉凯尔·赫格雷"
LAST	Lzh	"拉凯尔·赫格雷"
#   set the ko label to "라켈 헤그레"
LAST	Lko	"라켈 헤그레"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000176726399844 Rakel Hegre, qualified P1810 subject named as Rakel Hegre
LAST	P2600	"6000000176726399844"	P1810	"Rakel Hegre"
#   P569 date of birth = +1904-03-05T00:00:00Z/11
LAST	P569	+1904-03-05T00:00:00Z/11	S2600	"6000000176726399844"
#   P570 date of death = +1983-11-17T00:00:00Z/11
LAST	P570	+1983-11-17T00:00:00Z/11	S2600	"6000000176726399844"
#   P22 father = Q141189070 John Jonassen Hegre
LAST	P22	Q141189070	S2600	"6000000176726399844"
#   P25 mother = Q141205896 Ane Marie Konstanse Amanda Kristine Hegre
LAST	P25	Q141205896	S2600	"6000000176726399844"
#   Q141189070 John Jonassen Hegre: P40 child = the item just created
Q141189070	P40	LAST	S2600	"6000000176726399844"
#   Q141205896 Ane Marie Konstanse Amanda Kristine Hegre: P40 child = the item just created
Q141205896	P40	LAST	S2600	"6000000176726399844"
#   the item just created: P735 given name = Q16424094 Rakel
LAST	P735	Q16424094
#   P734 family name = Q36955626
LAST	P734	Q36955626

# create a new item
CREATE
#   set the en label to "Rasmus Hansen Nord-Varhaug"
LAST	Len	"Rasmus Hansen Nord-Varhaug"
#   set the mul label to "Rasmus Hansen Nord-Varhaug"
LAST	Lmul	"Rasmus Hansen Nord-Varhaug"
#   add a mul alias "Rasmus Hansen Låge-Håland"
LAST	Amul	"Rasmus Hansen Låge-Håland"
#   set the ja label to "ラスムス・ハンセン・ノール・ヴァールハウグ"
LAST	Lja	"ラスムス・ハンセン・ノール・ヴァールハウグ"
#   set the zh label to "拉斯穆斯·汉森·诺尔·瓦尔豪格"
LAST	Lzh	"拉斯穆斯·汉森·诺尔·瓦尔豪格"
#   set the ko label to "라스무스 한센 노르드바르하욱"
LAST	Lko	"라스무스 한센 노르드바르하욱"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000087451690855 Rasmus Hansen Nord-Varhaug, qualified P1810 subject named as Rasmus Hansen Låge-Håland
LAST	P2600	"6000000087451690855"	P1810	"Rasmus Hansen Låge-Håland"
#   P569 date of birth = +1710-00-00T00:00:00Z/9
LAST	P569	+1710-00-00T00:00:00Z/9	S2600	"6000000087451690855"
#   P570 date of death = +1774-06-18T00:00:00Z/11, qualified P1326 latest date +1774-06-18T00:00:00Z/11
LAST	P570	+1774-06-18T00:00:00Z/11	P1326	+1774-06-18T00:00:00Z/11	S2600	"6000000087451690855"
#   P22 father = Q141216381 Hans Rasmussen Låge-Håland
LAST	P22	Q141216381	S2600	"6000000087451690855"
#   P25 mother = Q141216383 Ingeborg Eriksdatter Bjorland
LAST	P25	Q141216383	S2600	"6000000087451690855"
#   Q141216381 Hans Rasmussen Låge-Håland: P40 child = the item just created
Q141216381	P40	LAST	S2600	"6000000087451690855"
#   Q141216383 Ingeborg Eriksdatter Bjorland: P40 child = the item just created
Q141216383	P40	LAST	S2600	"6000000087451690855"
#   the item just created: P735 given name = Q1785744 Rasmus
LAST	P735	Q1785744
#   add a mul alias "Rasmus Nord-Varhaug"
LAST	Amul	"Rasmus Nord-Varhaug"

# create a new item
CREATE
#   set the en label to "Sara Carlberg"
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
#   the item just created: set the en label to "Signe Bjørnsdotter Kvavik"
LAST	Len	"Signe Bjørnsdotter Kvavik"
#   set the mul label to "Signe Bjørnsdotter Kvavik"
LAST	Lmul	"Signe Bjørnsdotter Kvavik"
#   add a mul alias "Signe Bjørnsdotter Tengs?"
LAST	Amul	"Signe Bjørnsdotter Tengs?"
#   set the ja label to "シグネ・ブヨルンスドッテル・クヴァヴィク"
LAST	Lja	"シグネ・ブヨルンスドッテル・クヴァヴィク"
#   set the zh label to "西格内·布约尔恩斯多特·克瓦维克"
LAST	Lzh	"西格内·布约尔恩斯多特·克瓦维克"
#   set the ko label to "식네 브죄르느스도테르 크바비크"
LAST	Lko	"식네 브죄르느스도테르 크바비크"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000004569540770 Signe Bjørnsdotter Kvavik, qualified P1810 subject named as Signe Bjørnsdotter Tengs?
LAST	P2600	"6000000004569540770"	P1810	"Signe Bjørnsdotter Tengs?"
#   P569 date of birth = +1470-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P569	+1470-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"6000000004569540770"
#   P22 father = Q141242383 Bjørn Gunnbjørnsson Kvåvig
LAST	P22	Q141242383	S2600	"6000000004569540770"
#   Q141242383 Bjørn Gunnbjørnsson Kvåvig: P40 child = the item just created
Q141242383	P40	LAST	S2600	"6000000004569540770"
#   the item just created: P735 given name = Q2096893 Signe
LAST	P735	Q2096893
#   add a mul alias "Signe Kvavik"
LAST	Amul	"Signe Kvavik"

# create a new item
CREATE
#   set the en label to "Sissel Knutsdatter Bjørheim"
LAST	Len	"Sissel Knutsdatter Bjørheim"
#   set the mul label to "Sissel Knutsdatter Bjørheim"
LAST	Lmul	"Sissel Knutsdatter Bjørheim"
#   add a mul alias "Sissel Knutsdatter Knutsdatter"
LAST	Amul	"Sissel Knutsdatter Knutsdatter"
#   set the ja label to "シセル・クヌトスダッテル・ブヨルヘイム"
LAST	Lja	"シセル・クヌトスダッテル・ブヨルヘイム"
#   set the zh label to "西塞尔·克努特斯达特·布约尔赫伊姆"
LAST	Lzh	"西塞尔·克努特斯达特·布约尔赫伊姆"
#   set the ko label to "시셀 크누츠다테르 브죄르헤임"
LAST	Lko	"시셀 크누츠다테르 브죄르헤임"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 4462761 Sissel Knutsdatter Bjørheim, qualified P1810 subject named as Sissel Knutsdatter Knutsdatter
LAST	P2600	"4462761"	P1810	"Sissel Knutsdatter Knutsdatter"
#   P569 date of birth = +1595-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P569	+1595-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"4462761"
#   P570 date of death = +1703-02-25T00:00:00Z/11
LAST	P570	+1703-02-25T00:00:00Z/11	S2600	"4462761"
#   P22 father = Q141244226 Knut Bjørnson Bjørheim
LAST	P22	Q141244226	S2600	"4462761"
#   P40 child = Q141198507 Tormod Bjørnson Mele
LAST	P40	Q141198507	S2600	"4462761"
#   Q141244226 Knut Bjørnson Bjørheim: P40 child = the item just created
Q141244226	P40	LAST	S2600	"4462761"
#   Q141198507 Tormod Bjørnson Mele: P25 mother = the item just created
Q141198507	P25	LAST	S2600	"4462761"
#   the item just created: P735 given name = Q4571101 Sissel
LAST	P735	Q4571101
#   P734 family name = Q30834379, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q30834379	P3831	Q28418670
#   add a mul alias "Sissel Bjørheim"
LAST	Amul	"Sissel Bjørheim"

# create a new item
CREATE
#   set the en label to "Tollak Jonson Aukland"
LAST	Len	"Tollak Jonson Aukland"
#   set the mul label to "Tollak Jonson Aukland"
LAST	Lmul	"Tollak Jonson Aukland"
#   set the ja label to "トラク・ヨンソン・アウクランド"
LAST	Lja	"トラク・ヨンソン・アウクランド"
#   set the zh label to "托拉克·永松·奥克兰德"
LAST	Lzh	"托拉克·永松·奥克兰德"
#   set the ko label to "톨라크 존손 아우크란드"
LAST	Lko	"톨라크 존손 아우크란드"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000011671617514 Tollak Jonson Aukland, qualified P1810 subject named as Tollak Jonson Aukland
LAST	P2600	"6000000011671617514"	P1810	"Tollak Jonson Aukland"
#   P569 date of birth = +1510-00-00T00:00:00Z/9
LAST	P569	+1510-00-00T00:00:00Z/9	S2600	"6000000011671617514"
#   P570 date of death = +1591-00-00T00:00:00Z/9, qualified P1480 sourcing circumstances Q5727902 circa
LAST	P570	+1591-00-00T00:00:00Z/9	P1480	Q5727902	S2600	"6000000011671617514"
#   P22 father = Q141199899 Jon Tollakson Aukland, IV
LAST	P22	Q141199899	S2600	"6000000011671617514"
#   P25 mother = Q141198835 Bergitte Gunnbjørnsdatter Aukland
LAST	P25	Q141198835	S2600	"6000000011671617514"
#   Q141199899 Jon Tollakson Aukland, IV: P40 child = the item just created
Q141199899	P40	LAST	S2600	"6000000011671617514"
#   Q141198835 Bergitte Gunnbjørnsdatter Aukland: P40 child = the item just created
Q141198835	P40	LAST	S2600	"6000000011671617514"

# create a new item
CREATE
#   the item just created: set the en label to "Ulrika Henrika von Köhler"
LAST	Len	"Ulrika Henrika von Köhler"
#   set the mul label to "Ulrika Henrika von Köhler"
LAST	Lmul	"Ulrika Henrika von Köhler"
#   set the ja label to "ウルリカ・ヘンリカ・ヴォン・ケーラー"
LAST	Lja	"ウルリカ・ヘンリカ・ヴォン・ケーラー"
#   set the zh label to "乌尔里卡·亨里卡·翁·科莱尔"
LAST	Lzh	"乌尔里卡·亨里卡·翁·科莱尔"
#   set the ko label to "울리카 헨리카 본 쾨흐레르"
LAST	Lko	"울리카 헨리카 본 쾨흐레르"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000019568439151 Ulrika Henrika von Köhler, qualified P1810 subject named as Ulrika Henrika von Köhler
LAST	P2600	"6000000019568439151"	P1810	"Ulrika Henrika von Köhler"
#   P569 date of birth = +1780-03-05T00:00:00Z/11
LAST	P569	+1780-03-05T00:00:00Z/11	S2600	"6000000019568439151"
#   P570 date of death = +1822-01-27T00:00:00Z/11
LAST	P570	+1822-01-27T00:00:00Z/11	S2600	"6000000019568439151"
#   P22 father = Q19721217 Salomon Christoffer von Köhler
LAST	P22	Q19721217	S2600	"6000000019568439151"
#   Q19721217 Salomon Christoffer von Köhler: P40 child = the item just created
Q19721217	P40	LAST	S2600	"6000000019568439151"
#   the item just created: P735 given name = Q18924998 Ulrika, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q18924998	P1545	"1"	P7452	Q3409033
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
#   Q134546510 Catharina Elisabet Brandt: P735 given name = Q17317997 Catharina, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
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

