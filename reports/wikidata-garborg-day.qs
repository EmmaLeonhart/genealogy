# ------------------------------------------------------------------------
# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at 15, both
#   her instruction: "any label changes should occur at the beginning of the
#   batch and be limited to a count of 15 labels added per batch". A label set
#   at CREATION time is neither counted nor capped -- "a label added during item
#   creation is good".
#   2086 more are held for a later run; a repeat is a no-op, so nothing is lost.
# ------------------------------------------------------------------------
#   Q45484995: set the sv label
Q45484995	Lsv	"man av Chen-ätten, från Shengzhou Jiangning"
#   Q45484995: set the de label
Q45484995	Lde	"Mann des Klans Chen, aus Shengzhou Jiangning"
#   Q45484995: set the it label
Q45484995	Lit	"uomo del clan Chen, da Shengzhou Jiangning"
#   Q45484995: set the pt label
Q45484995	Lpt	"homem do clã Chen, de Shengzhou Jiangning"
#   Q45484995: set the ca label
Q45484995	Lca	"home del clan Chen, de Shengzhou Jiangning"
#   Q45485126 (陳 of 京兆長安): mul label = NN
Q45485126	Lmul	"NN"
#   Q45485126: set the nb label
Q45485126	Lnb	"mann av Chen-slekten, fra Jingzhao Chang'an"
#   Q45485126: set the da label
Q45485126	Lda	"mand af Chen-slægten, fra Jingzhao Chang'an"
#   Q45485126: set the sv label
Q45485126	Lsv	"man av Chen-ätten, från Jingzhao Chang'an"
#   Q45485126: set the de label
Q45485126	Lde	"Mann des Klans Chen, aus Jingzhao Chang'an"
#   Q45485126: set the it label
Q45485126	Lit	"uomo del clan Chen, da Jingzhao Chang'an"
#   Q45485126: set the pt label
Q45485126	Lpt	"homem do clã Chen, de Jingzhao Chang'an"
#   Q45485126: set the ca label
Q45485126	Lca	"home del clan Chen, de Jingzhao Chang'an"
#   Q45485317 (陳 of 京兆長安): mul label = NN
Q45485317	Lmul	"NN"
#   Q45485317: set the nb label
Q45485317	Lnb	"mann av Chen-slekten, fra Jingzhao Chang'an"

# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the en label to "Amalia Charlotta Ehrenpreus"
LAST	Len	"Amalia Charlotta Ehrenpreus"
#   set the mul label to "Amalia Charlotta Ehrenpreus"
LAST	Lmul	"Amalia Charlotta Ehrenpreus"
#   set the ja label to "アマリア・カルロタ・エレンプレウス"
LAST	Lja	"アマリア・カルロタ・エレンプレウス"
#   set the zh label to "阿马利阿·卡尔洛塔·埃雷恩普雷乌斯"
LAST	Lzh	"阿马利阿·卡尔洛塔·埃雷恩普雷乌斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000019041477898 Amalia Charlotta Ehrenpreus, qualified P1810 subject named as Amalia Charlotta Ehrenpreus
LAST	P2600	"6000000019041477898"	P1810	"Amalia Charlotta Ehrenpreus"
#   P569 date of birth = +1780-01-17T00:00:00Z/11
LAST	P569	+1780-01-17T00:00:00Z/11	S2600	"6000000019041477898"
#   P570 date of death = +1805-12-12T00:00:00Z/11
LAST	P570	+1805-12-12T00:00:00Z/11	S2600	"6000000019041477898"
#   P26 spouse = Q5542574 Johan Fredrik Adelheim Borgström
LAST	P26	Q5542574	S2600	"6000000019041477898"
#   Q5542574 Johan Fredrik Adelheim Borgström: P26 spouse = the item just created
Q5542574	P26	LAST	S2600	"6000000019041477898"
#   the item just created: P735 given name = Q453020 Amalia, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q453020	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1067071	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Carl Ersson"
LAST	Len	"Carl Ersson"
#   set the mul label to "Carl Ersson"
LAST	Lmul	"Carl Ersson"
#   set the ja label to "カルル・エルソン"
LAST	Lja	"カルル・エルソン"
#   set the zh label to "卡尔尔·埃尔松"
LAST	Lzh	"卡尔尔·埃尔松"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000177920129826 Carl Ersson, qualified P1810 subject named as Carl Ersson
LAST	P2600	"6000000177920129826"	P1810	"Carl Ersson"
#   P569 date of birth = +1809-02-01T00:00:00Z/11
LAST	P569	+1809-02-01T00:00:00Z/11	S2600	"6000000177920129826"
#   P26 spouse = Q141219071 Ulrika Persdotter
LAST	P26	Q141219071	S2600	"6000000177920129826"
#   Q141219071 Ulrika Persdotter: P26 spouse = the item just created
Q141219071	P26	LAST	S2600	"6000000177920129826"
#   the item just created: P735 given name = Q2529610 Carl
LAST	P735	Q2529610

# create a new item
CREATE
#   set the en label to "Christina Maria Adelheim"
LAST	Len	"Christina Maria Adelheim"
#   set the mul label to "Christina Maria Adelheim"
LAST	Lmul	"Christina Maria Adelheim"
#   set the ja label to "クリスティナ・マリア・アデルヘイム"
LAST	Lja	"クリスティナ・マリア・アデルヘイム"
#   set the zh label to "克里斯蒂纳·马里阿·阿德尔赫伊姆"
LAST	Lzh	"克里斯蒂纳·马里阿·阿德尔赫伊姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000019413110402 Christina Maria Adelheim, qualified P1810 subject named as Christina Maria Adelheim
LAST	P2600	"6000000019413110402"	P1810	"Christina Maria Adelheim"
#   P569 date of birth = +1803-07-03T00:00:00Z/11
LAST	P569	+1803-07-03T00:00:00Z/11	S2600	"6000000019413110402"
#   P570 date of death = +1843-03-16T00:00:00Z/11
LAST	P570	+1843-03-16T00:00:00Z/11	S2600	"6000000019413110402"
#   P22 father = Q5542574 Johan Fredrik Adelheim Borgström
LAST	P22	Q5542574	S2600	"6000000019413110402"
#   Q5542574 Johan Fredrik Adelheim Borgström: P40 child = the item just created
Q5542574	P40	LAST	S2600	"6000000019413110402"

# create a new item
CREATE
#   the item just created: set the en label to "Christina, Sofia Carlsdotter"
LAST	Len	"Christina, Sofia Carlsdotter"
#   set the mul label to "Christina, Sofia Carlsdotter"
LAST	Lmul	"Christina, Sofia Carlsdotter"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000177921459033 Christina, Sofia Carlsdotter, qualified P1810 subject named as Christina, Sofia Carlsdotter
LAST	P2600	"6000000177921459033"	P1810	"Christina, Sofia Carlsdotter"
#   P569 date of birth = +1837-08-10T00:00:00Z/11
LAST	P569	+1837-08-10T00:00:00Z/11	S2600	"6000000177921459033"
#   P570 date of death = +1866-04-02T00:00:00Z/11
LAST	P570	+1866-04-02T00:00:00Z/11	S2600	"6000000177921459033"
#   P25 mother = Q141219071 Ulrika Persdotter
LAST	P25	Q141219071	S2600	"6000000177921459033"
#   Q141219071 Ulrika Persdotter: P40 child = the item just created
Q141219071	P40	LAST	S2600	"6000000177921459033"

# create a new item
CREATE
#   the item just created: set the en label to "David Robert Tunheim"
LAST	Len	"David Robert Tunheim"
#   set the mul label to "David Robert Tunheim"
LAST	Lmul	"David Robert Tunheim"
#   set the ja label to "ダヴィド・ロベルト・トゥンヘイム"
LAST	Lja	"ダヴィド・ロベルト・トゥンヘイム"
#   set the zh label to "达维德·罗贝尔特·通海姆"
LAST	Lzh	"达维德·罗贝尔特·通海姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000180041622897 David Robert Tunheim, qualified P1810 subject named as David Robert Tunheim
LAST	P2600	"6000000180041622897"	P1810	"David Robert Tunheim"
#   P569 date of birth = +1942-08-06T00:00:00Z/11
LAST	P569	+1942-08-06T00:00:00Z/11	S2600	"6000000180041622897"
#   P570 date of death = +1992-10-03T00:00:00Z/11
LAST	P570	+1992-10-03T00:00:00Z/11	S2600	"6000000180041622897"
#   P22 father = Q141189101 Samuel Tunheim
LAST	P22	Q141189101	S2600	"6000000180041622897"
#   P25 mother = Q141216454 Alice Lillian Tunheim Nelson
LAST	P25	Q141216454	S2600	"6000000180041622897"
#   Q141189101 Samuel Tunheim: P40 child = the item just created
Q141189101	P40	LAST	S2600	"6000000180041622897"
#   Q141216454 Alice Lillian Tunheim Nelson: P40 child = the item just created
Q141216454	P40	LAST	S2600	"6000000180041622897"
#   the item just created: P735 given name = Q29937870 David, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q29937870	P1545	"1"	P7452	Q3409033

# create a new item
CREATE
#   set the en label to "Eivind Ogmundsson Byre på Høyland"
LAST	Len	"Eivind Ogmundsson Byre på Høyland"
#   set the mul label to "Eivind Ogmundsson Byre på Høyland"
LAST	Lmul	"Eivind Ogmundsson Byre på Høyland"
#   set the ja label to "エイヴィン・オグムンドソン・ビレ・ポー・ホイランド"
LAST	Lja	"エイヴィン・オグムンドソン・ビレ・ポー・ホイランド"
#   set the zh label to "埃温·奥格穆恩德松·比雷·波·霍伊拉恩德"
LAST	Lzh	"埃温·奥格穆恩德松·比雷·波·霍伊拉恩德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000004870612250 Eivind Ogmundsson Byre på Høyland, qualified P1810 subject named as Eivind Ogmundsson Byre på Høyland
LAST	P2600	"6000000004870612250"	P1810	"Eivind Ogmundsson Byre på Høyland"
#   P569 date of birth = +1375-00-00T00:00:00Z/9
LAST	P569	+1375-00-00T00:00:00Z/9	S2600	"6000000004870612250"
#   P570 date of death = +1416-00-00T00:00:00Z/9
LAST	P570	+1416-00-00T00:00:00Z/9	S2600	"6000000004870612250"
#   P26 spouse = Q141216603 Brynhild Hallvardsdotter
LAST	P26	Q141216603	S2600	"6000000004870612250"
#   P40 child = Q141205937 Ragnhild Eyvindsdotter Eyvindsdotter
LAST	P40	Q141205937	S2600	"6000000004870612250"
#   Q141216603 Brynhild Hallvardsdotter: P26 spouse = the item just created
Q141216603	P26	LAST	S2600	"6000000004870612250"
#   Q141205937 Ragnhild Eyvindsdotter Eyvindsdotter: P22 father = the item just created
Q141205937	P22	LAST	S2600	"6000000004870612250"
#   the item just created: P735 given name = Q3358418 Eivind
LAST	P735	Q3358418
#   P1449 nickname = en:"Byre"
LAST	P1449	en:"Byre"
#   add a mul alias "Byre"
LAST	Amul	"Byre"
#   add a mul alias "Eivind Byre"
LAST	Amul	"Eivind Byre"

# create a new item
CREATE
#   set the en label to "Eivind Svenson Sveinsen Garborg"
LAST	Len	"Eivind Svenson Sveinsen Garborg"
#   set the mul label to "Eivind Svenson Sveinsen Garborg"
LAST	Lmul	"Eivind Svenson Sveinsen Garborg"
#   add a mul alias "Eivind Svenson Sveinsen Fosse"
LAST	Amul	"Eivind Svenson Sveinsen Fosse"
#   set the ja label to "エイヴィン・スヴェンソン・スヴェインセン・ガルボルグ"
LAST	Lja	"エイヴィン・スヴェンソン・スヴェインセン・ガルボルグ"
#   set the zh label to "埃温·斯韦恩松·斯韦伊恩森·加尔博格"
LAST	Lzh	"埃温·斯韦恩松·斯韦伊恩森·加尔博格"
#   add a ja alias "エイヴィン・スヴェンソン・スヴェインセン・フォセ"
LAST	Aja	"エイヴィン・スヴェンソン・スヴェインセン・フォセ"
#   add a zh alias "埃温·斯韦恩松·斯韦伊恩森·福塞"
LAST	Azh	"埃温·斯韦恩松·斯韦伊恩森·福塞"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003492077372 Eivind Svenson Sveinsen Garborg, qualified P1810 subject named as Eivind Svenson Sveinsen Fosse
LAST	P2600	"6000000003492077372"	P1810	"Eivind Svenson Sveinsen Fosse"
#   P569 date of birth = +1665-00-00T00:00:00Z/9
LAST	P569	+1665-00-00T00:00:00Z/9	S2600	"6000000003492077372"
#   P570 date of death = +1722-09-00T00:00:00Z/10
LAST	P570	+1722-09-00T00:00:00Z/10	S2600	"6000000003492077372"
#   P40 child = Q141199925 Knut Elvindson Garborg
LAST	P40	Q141199925	S2600	"6000000003492077372"
#   Q141199925 Knut Elvindson Garborg: P22 father = the item just created
Q141199925	P22	LAST	S2600	"6000000003492077372"
#   the item just created: P735 given name = Q3358418 Eivind
LAST	P735	Q3358418
#   P734 family name = Q26884133 Fosse, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q26884133	P3831	Q2507958
#   P734 family name = Q30250555 Garborg
LAST	P734	Q30250555
#   add a mul alias "Eivind Garborg"
LAST	Amul	"Eivind Garborg"

# create a new item
CREATE
#   set the en label to "Elen Kristoffersdotter Nese"
LAST	Len	"Elen Kristoffersdotter Nese"
#   set the mul label to "Elen Kristoffersdotter Nese"
LAST	Lmul	"Elen Kristoffersdotter Nese"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000012587664964 Elen Kristoffersdotter Nese, qualified P1810 subject named as Elen Kristoffersdotter Nese
LAST	P2600	"6000000012587664964"	P1810	"Elen Kristoffersdotter Nese"
#   P569 date of birth = +1760-00-00T00:00:00Z/9
LAST	P569	+1760-00-00T00:00:00Z/9	S2600	"6000000012587664964"
#   P570 date of death = +1831-01-04T00:00:00Z/11
LAST	P570	+1831-01-04T00:00:00Z/11	S2600	"6000000012587664964"
#   P26 spouse = Q141219063 Lars Osmundsen Nese
LAST	P26	Q141219063	S2600	"6000000012587664964"
#   Q141219063 Lars Osmundsen Nese: P26 spouse = the item just created
Q141219063	P26	LAST	S2600	"6000000012587664964"
#   the item just created: P735 given name = Q11967041 Elen
LAST	P735	Q11967041
#   P1449 nickname = en:"Christophersdatter"
LAST	P1449	en:"Christophersdatter"
#   add a mul alias "Christophersdatter Nese"
LAST	Amul	"Christophersdatter Nese"

# create a new item
CREATE
#   set the en label to "Erik Samuel Fant"
LAST	Len	"Erik Samuel Fant"
#   set the mul label to "Erik Samuel Fant"
LAST	Lmul	"Erik Samuel Fant"
#   set the ja label to "エリク・サムエル・ファント"
LAST	Lja	"エリク・サムエル・ファント"
#   set the zh label to "埃里克·萨穆埃尔·法恩特"
LAST	Lzh	"埃里克·萨穆埃尔·法恩特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000166407230823 Erik Samuel Fant, qualified P1810 subject named as Erik Samuel Fant
LAST	P2600	"6000000166407230823"	P1810	"Erik Samuel Fant"
#   P569 date of birth = +1804-04-15T00:00:00Z/11
LAST	P569	+1804-04-15T00:00:00Z/11	S2600	"6000000166407230823"
#   P570 date of death = +1865-07-19T00:00:00Z/11
LAST	P570	+1865-07-19T00:00:00Z/11	S2600	"6000000166407230823"
#   P22 father = Q5725105 Eric Michael Fant
LAST	P22	Q5725105	S2600	"6000000166407230823"
#   Q5725105 Eric Michael Fant: P40 child = the item just created
Q5725105	P40	LAST	S2600	"6000000166407230823"
#   the item just created: P735 given name = Q750186 Erik, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q750186	P1545	"1"	P7452	Q3409033
#   P735 given name = Q629347 Samuel, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q629347	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Gitlaug Knutsdatter Garborg"
LAST	Len	"Gitlaug Knutsdatter Garborg"
#   set the mul label to "Gitlaug Knutsdatter Garborg"
LAST	Lmul	"Gitlaug Knutsdatter Garborg"
#   set the ja label to "ギトラウグ・クヌトスダッテル・ガルボルグ"
LAST	Lja	"ギトラウグ・クヌトスダッテル・ガルボルグ"
#   set the zh label to "吉特拉乌格·克努特斯达特·加尔博格"
LAST	Lzh	"吉特拉乌格·克努特斯达特·加尔博格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003491951383 Gitlaug Knutsdatter Garborg, qualified P1810 subject named as Gitlaug Knutsdatter Garborg
LAST	P2600	"6000000003491951383"	P1810	"Gitlaug Knutsdatter Garborg"
#   P569 date of birth = +1670-00-00T00:00:00Z/9
LAST	P569	+1670-00-00T00:00:00Z/9	S2600	"6000000003491951383"
#   P570 date of death = +1743-00-00T00:00:00Z/9
LAST	P570	+1743-00-00T00:00:00Z/9	S2600	"6000000003491951383"
#   P40 child = Q141199925 Knut Elvindson Garborg
LAST	P40	Q141199925	S2600	"6000000003491951383"
#   Q141199925 Knut Elvindson Garborg: P25 mother = the item just created
Q141199925	P25	LAST	S2600	"6000000003491951383"
#   the item just created: P734 family name = Q30250555 Garborg
LAST	P734	Q30250555

# create a new item
CREATE
#   set the en label to "Guri Torkjellsdatter Foss-Eikeland"
LAST	Len	"Guri Torkjellsdatter Foss-Eikeland"
#   set the mul label to "Guri Torkjellsdatter Foss-Eikeland"
LAST	Lmul	"Guri Torkjellsdatter Foss-Eikeland"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000035769326152 Guri Torkjellsdatter Foss-Eikeland, qualified P1810 subject named as Guri Torkjellsdatter Foss-Eikeland
LAST	P2600	"6000000035769326152"	P1810	"Guri Torkjellsdatter Foss-Eikeland"
#   P569 date of birth = +1727-00-00T00:00:00Z/9
LAST	P569	+1727-00-00T00:00:00Z/9	S2600	"6000000035769326152"
#   P570 date of death = +1773-00-00T00:00:00Z/9
LAST	P570	+1773-00-00T00:00:00Z/9	S2600	"6000000035769326152"
#   P26 spouse = Q141217404 Osmund Larsen Raunes
LAST	P26	Q141217404	S2600	"6000000035769326152"
#   P40 child = Q141219063 Lars Osmundsen Nese
LAST	P40	Q141219063	S2600	"6000000035769326152"
#   Q141217404 Osmund Larsen Raunes: P26 spouse = the item just created
Q141217404	P26	LAST	S2600	"6000000035769326152"
#   Q141219063 Lars Osmundsen Nese: P25 mother = the item just created
Q141219063	P25	LAST	S2600	"6000000035769326152"
#   the item just created: P735 given name = Q11973376 Guri
LAST	P735	Q11973376

# create a new item
CREATE
#   set the en label to "Hindrik Fransson vintappare"
LAST	Len	"Hindrik Fransson vintappare"
#   set the mul label to "Hindrik Fransson vintappare"
LAST	Lmul	"Hindrik Fransson vintappare"
#   set the ja label to "ヒンドリク・フランソン・ヴィンタパレ"
LAST	Lja	"ヒンドリク・フランソン・ヴィンタパレ"
#   set the zh label to "希恩德里克·夫拉恩松·维恩塔帕雷"
LAST	Lzh	"希恩德里克·夫拉恩松·维恩塔帕雷"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000027488689563 Hindrik Fransson vintappare, qualified P1810 subject named as Hindrik Fransson vintappare
LAST	P2600	"6000000027488689563"	P1810	"Hindrik Fransson vintappare"
#   P26 spouse = Q141189058 Brita Thomasdotter
LAST	P26	Q141189058	S2600	"6000000027488689563"
#   Q141189058 Brita Thomasdotter: P26 spouse = the item just created
Q141189058	P26	LAST	S2600	"6000000027488689563"
#   the item just created: P1449 nickname = en:"Henrik Heinrich Frantzson"
LAST	P1449	en:"Henrik Heinrich Frantzson"
#   add a mul alias "Henrik Heinrich Frantzson Fransson vintappare"
LAST	Amul	"Henrik Heinrich Frantzson Fransson vintappare"

# create a new item
CREATE
#   set the en label to "Inger Sørensdatter Lima"
LAST	Len	"Inger Sørensdatter Lima"
#   set the mul label to "Inger Sørensdatter Lima"
LAST	Lmul	"Inger Sørensdatter Lima"
#   add a mul alias "Inger Sørensdatter Gjesdal"
LAST	Amul	"Inger Sørensdatter Gjesdal"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000065991527068 Inger Sørensdatter Lima, qualified P1810 subject named as Inger Sørensdatter Gjesdal
LAST	P2600	"6000000065991527068"	P1810	"Inger Sørensdatter Gjesdal"
#   P569 date of birth = +1770-00-00T00:00:00Z/9
LAST	P569	+1770-00-00T00:00:00Z/9	S2600	"6000000065991527068"
#   P570 date of death = +1841-08-02T00:00:00Z/11
LAST	P570	+1841-08-02T00:00:00Z/11	S2600	"6000000065991527068"
#   P22 father = Q141219069 Søren Sørenson Gjesdal
LAST	P22	Q141219069	S2600	"6000000065991527068"
#   Q141219069 Søren Sørenson Gjesdal: P40 child = the item just created
Q141219069	P40	LAST	S2600	"6000000065991527068"
#   the item just created: P735 given name = Q3358452 Inger
LAST	P735	Q3358452
#   P734 family name = Q27888954 Gjesdal, qualified P3831 object of statement has role Q2507958 birth name
LAST	P734	Q27888954	P3831	Q2507958
#   P734 family name = Q11255517 Lima, qualified P3831 object of statement has role Q28418670 married name
LAST	P734	Q11255517	P3831	Q28418670
#   add a mul alias "Inger Lima"
LAST	Amul	"Inger Lima"

# create a new item
CREATE
#   set the en label to "Kari Tollaksdatter Kartevoll"
LAST	Len	"Kari Tollaksdatter Kartevoll"
#   set the mul label to "Kari Tollaksdatter Kartevoll"
LAST	Lmul	"Kari Tollaksdatter Kartevoll"
#   set the ja label to "カリ・トラクスダッテル・カルテヴォル"
LAST	Lja	"カリ・トラクスダッテル・カルテヴォル"
#   set the zh label to "卡里·托拉克斯达特·卡尔特沃尔"
LAST	Lzh	"卡里·托拉克斯达特·卡尔特沃尔"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005606851268 Kari Tollaksdatter Kartevoll, qualified P1810 subject named as Kari Tollaksdatter Kartevoll
LAST	P2600	"6000000005606851268"	P1810	"Kari Tollaksdatter Kartevoll"
#   P569 date of birth = +1687-00-00T00:00:00Z/9
LAST	P569	+1687-00-00T00:00:00Z/9	S2600	"6000000005606851268"
#   P570 date of death = +1765-10-18T00:00:00Z/11
LAST	P570	+1765-10-18T00:00:00Z/11	S2600	"6000000005606851268"
#   P40 child = Q141219053 Barbro Reiersdatter Storhaug
LAST	P40	Q141219053	S2600	"6000000005606851268"
#   P40 child = Q141216645 Reiar Reiersen Kydland
LAST	P40	Q141216645	S2600	"6000000005606851268"
#   Q141219053 Barbro Reiersdatter Storhaug: P25 mother = the item just created
Q141219053	P25	LAST	S2600	"6000000005606851268"
#   Q141216645 Reiar Reiersen Kydland: P25 mother = the item just created
Q141216645	P25	LAST	S2600	"6000000005606851268"
#   the item just created: P735 given name = Q1333594 Kari
LAST	P735	Q1333594

# create a new item
CREATE
#   set the en label to "Maria Benjaminsdotter"
LAST	Len	"Maria Benjaminsdotter"
#   set the mul label to "Maria Benjaminsdotter"
LAST	Lmul	"Maria Benjaminsdotter"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000011078807545 Maria Benjaminsdotter, qualified P1810 subject named as Maria Benjaminsdotter
LAST	P2600	"6000000011078807545"	P1810	"Maria Benjaminsdotter"
#   P569 date of birth = +1772-03-24T00:00:00Z/11
LAST	P569	+1772-03-24T00:00:00Z/11	S2600	"6000000011078807545"
#   P570 date of death = +1834-08-23T00:00:00Z/11
LAST	P570	+1834-08-23T00:00:00Z/11	S2600	"6000000011078807545"
#   P26 spouse = Q141217433 Per Persson Hagman
LAST	P26	Q141217433	S2600	"6000000011078807545"
#   P40 child = Q141219071 Ulrika Persdotter
LAST	P40	Q141219071	S2600	"6000000011078807545"
#   Q141217433 Per Persson Hagman: P26 spouse = the item just created
Q141217433	P26	LAST	S2600	"6000000011078807545"
#   Q141219071 Ulrika Persdotter: P25 mother = the item just created
Q141219071	P25	LAST	S2600	"6000000011078807545"

# create a new item
CREATE
#   the item just created: set the en label to "Maria Hansdatter Austrått"
LAST	Len	"Maria Hansdatter Austrått"
#   set the mul label to "Maria Hansdatter Austrått"
LAST	Lmul	"Maria Hansdatter Austrått"
#   set the ja label to "マリア・ハンスダッテル・アウストロート"
LAST	Lja	"マリア・ハンスダッテル・アウストロート"
#   set the zh label to "马里阿·汉斯达特·奥斯特罗特"
LAST	Lzh	"马里阿·汉斯达特·奥斯特罗特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005607475201 Maria Hansdatter Austrått, qualified P1810 subject named as Maria Hansdatter Austrått
LAST	P2600	"6000000005607475201"	P1810	"Maria Hansdatter Austrått"
#   P569 date of birth = +1751-00-00T00:00:00Z/9
LAST	P569	+1751-00-00T00:00:00Z/9	S2600	"6000000005607475201"
#   P570 date of death = +1837-04-18T00:00:00Z/11
LAST	P570	+1837-04-18T00:00:00Z/11	S2600	"6000000005607475201"
#   P40 child = Q141206057 Berte Tørresdotter Austrått
LAST	P40	Q141206057	S2600	"6000000005607475201"
#   Q141206057 Berte Tørresdotter Austrått: P25 mother = the item just created
Q141206057	P25	LAST	S2600	"6000000005607475201"
#   the item just created: add a mul alias "Maria Austrått"
LAST	Amul	"Maria Austrått"

# create a new item
CREATE
#   set the en label to "Per Asbjørnson Stokka"
LAST	Len	"Per Asbjørnson Stokka"
#   set the mul label to "Per Asbjørnson Stokka"
LAST	Lmul	"Per Asbjørnson Stokka"
#   set the ja label to "ペル・アスブヨルンソン・ストカ"
LAST	Lja	"ペル・アスブヨルンソン・ストカ"
#   set the zh label to "佩尔·阿斯布永尔恩松·斯托卡"
LAST	Lzh	"佩尔·阿斯布永尔恩松·斯托卡"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003491933576 Per Asbjørnson Stokka, qualified P1810 subject named as Per Asbjørnson Stokka
LAST	P2600	"6000000003491933576"	P1810	"Per Asbjørnson Stokka"
#   P569 date of birth = +1725-01-24T00:00:00Z/11
LAST	P569	+1725-01-24T00:00:00Z/11	S2600	"6000000003491933576"
#   P570 date of death = +1798-00-00T00:00:00Z/9
LAST	P570	+1798-00-00T00:00:00Z/9	S2600	"6000000003491933576"
#   P26 spouse = Q141219052 Anna Olsdatter Heigre
LAST	P26	Q141219052	S2600	"6000000003491933576"
#   P40 child = Q141216637 Ola Person Persson Heigre
LAST	P40	Q141216637	S2600	"6000000003491933576"
#   Q141219052 Anna Olsdatter Heigre: P26 spouse = the item just created
Q141219052	P26	LAST	S2600	"6000000003491933576"
#   Q141216637 Ola Person Persson Heigre: P22 father = the item just created
Q141216637	P22	LAST	S2600	"6000000003491933576"
#   the item just created: P735 given name = Q13582800 Per
LAST	P735	Q13582800
#   add a mul alias "Per Stokka"
LAST	Amul	"Per Stokka"

# create a new item
CREATE
#   set the en label to "Petrike Margrete Jenssen"
LAST	Len	"Petrike Margrete Jenssen"
#   set the mul label to "Petrike Margrete Jenssen"
LAST	Lmul	"Petrike Margrete Jenssen"
#   add a mul alias "Petrike Margrete Andreasdatter"
LAST	Amul	"Petrike Margrete Andreasdatter"
#   set the ja label to "ペトリケ・マルグレテ・イェンセン"
LAST	Lja	"ペトリケ・マルグレテ・イェンセン"
#   set the zh label to "佩特里凯·马尔格雷特·耶恩森"
LAST	Lzh	"佩特里凯·马尔格雷特·耶恩森"
#   add a ja alias "ペトリケ・マルグレテ・アンドレアスダッテル"
LAST	Aja	"ペトリケ・マルグレテ・アンドレアスダッテル"
#   add a zh alias "佩特里凯·马尔格雷特·阿恩德雷阿斯达特"
LAST	Azh	"佩特里凯·马尔格雷特·阿恩德雷阿斯达特"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000014188713060 Petrike Margrete Jenssen, qualified P1810 subject named as Petrike Margrete Andreasdatter
LAST	P2600	"6000000014188713060"	P1810	"Petrike Margrete Andreasdatter"
#   P569 date of birth = +1851-00-00T00:00:00Z/9
LAST	P569	+1851-00-00T00:00:00Z/9	S2600	"6000000014188713060"
#   P40 child = Q141216639 Olufine Bergithe Ekman
LAST	P40	Q141216639	S2600	"6000000014188713060"
#   Q141216639 Olufine Bergithe Ekman: P25 mother = the item just created
Q141216639	P25	LAST	S2600	"6000000014188713060"
#   the item just created: P735 given name = Q17457544 Margrete, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q17457544	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Reiar Einarsen Kydland"
LAST	Len	"Reiar Einarsen Kydland"
#   set the mul label to "Reiar Einarsen Kydland"
LAST	Lmul	"Reiar Einarsen Kydland"
#   set the ja label to "レイアル・エイナルセン・キドランド"
LAST	Lja	"レイアル・エイナルセン・キドランド"
#   set the zh label to "雷伊阿尔·艾纳尔森·基德拉恩德"
LAST	Lzh	"雷伊阿尔·艾纳尔森·基德拉恩德"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000000496970049 Reiar Einarsen Kydland, qualified P1810 subject named as Reiar Einarsen Kydland
LAST	P2600	"6000000000496970049"	P1810	"Reiar Einarsen Kydland"
#   P569 date of birth = +1667-00-00T00:00:00Z/9
LAST	P569	+1667-00-00T00:00:00Z/9	S2600	"6000000000496970049"
#   P570 date of death = +1734-00-00T00:00:00Z/9
LAST	P570	+1734-00-00T00:00:00Z/9	S2600	"6000000000496970049"
#   P40 child = Q141219053 Barbro Reiersdatter Storhaug
LAST	P40	Q141219053	S2600	"6000000000496970049"
#   P40 child = Q141216645 Reiar Reiersen Kydland
LAST	P40	Q141216645	S2600	"6000000000496970049"
#   Q141219053 Barbro Reiersdatter Storhaug: P22 father = the item just created
Q141219053	P22	LAST	S2600	"6000000000496970049"
#   Q141216645 Reiar Reiersen Kydland: P22 father = the item just created
Q141216645	P22	LAST	S2600	"6000000000496970049"

# create a new item
CREATE
#   the item just created: set the en label to "Sofia Maria Mannerheim"
LAST	Len	"Sofia Maria Mannerheim"
#   set the mul label to "Sofia Maria Mannerheim"
LAST	Lmul	"Sofia Maria Mannerheim"
#   set the ja label to "ソフィア・マリア・マネルヘイム"
LAST	Lja	"ソフィア・マリア・マネルヘイム"
#   set the zh label to "索菲阿·马里阿·马内尔赫伊姆"
LAST	Lzh	"索菲阿·马里阿·马内尔赫伊姆"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000000047205391 Sofia Maria Mannerheim, qualified P1810 subject named as Sofia Maria Mannerheim
LAST	P2600	"6000000000047205391"	P1810	"Sofia Maria Mannerheim"
#   P569 date of birth = +1788-08-10T00:00:00Z/11
LAST	P569	+1788-08-10T00:00:00Z/11	S2600	"6000000000047205391"
#   P570 date of death = +1788-08-18T00:00:00Z/11
LAST	P570	+1788-08-18T00:00:00Z/11	S2600	"6000000000047205391"
#   P22 father = Q5975022 Lars August Mannerheim
LAST	P22	Q5975022	S2600	"6000000000047205391"
#   Q5975022 Lars August Mannerheim: P40 child = the item just created
Q5975022	P40	LAST	S2600	"6000000000047205391"

# create a new item
CREATE
#   the item just created: set the en label to "Sofia Wadenstierna"
LAST	Len	"Sofia Wadenstierna"
#   set the mul label to "Sofia Wadenstierna"
LAST	Lmul	"Sofia Wadenstierna"
#   set the ja label to "ソフィア・ヴァデンスティエルナ"
LAST	Lja	"ソフィア・ヴァデンスティエルナ"
#   set the zh label to "索菲阿·瓦德恩斯蒂埃尔纳"
LAST	Lzh	"索菲阿·瓦德恩斯蒂埃尔纳"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000000047255126 Sofia Wadenstierna, qualified P1810 subject named as Sofia Wadenstierna
LAST	P2600	"6000000000047255126"	P1810	"Sofia Wadenstierna"
#   P569 date of birth = +1758-08-13T00:00:00Z/11
LAST	P569	+1758-08-13T00:00:00Z/11	S2600	"6000000000047255126"
#   P570 date of death = +1830-01-12T00:00:00Z/11
LAST	P570	+1830-01-12T00:00:00Z/11	S2600	"6000000000047255126"
#   P26 spouse = Q5975022 Lars August Mannerheim
LAST	P26	Q5975022	S2600	"6000000000047255126"
#   Q5975022 Lars August Mannerheim: P26 spouse = the item just created
Q5975022	P26	LAST	S2600	"6000000000047255126"

# create a new item
CREATE
#   the item just created: set the en label to "Tore Sebjørnsson Talgje d.y"
LAST	Len	"Tore Sebjørnsson Talgje d.y"
#   set the mul label to "Tore Sebjørnsson Talgje d.y"
LAST	Lmul	"Tore Sebjørnsson Talgje d.y"
#   set the ja label to "トレ・セブヨルンソン・タルイェ・ドイ"
LAST	Lja	"トレ・セブヨルンソン・タルイェ・ドイ"
#   set the zh label to "托雷·塞布永尔恩松·塔尔耶·德伊"
LAST	Lzh	"托雷·塞布永尔恩松·塔尔耶·德伊"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003043756033 Tore Sebjørnsson Talgje d.y, qualified P1810 subject named as Tore Sebjørnsson Talgje d.y
LAST	P2600	"6000000003043756033"	P1810	"Tore Sebjørnsson Talgje d.y"
#   P569 date of birth = +1535-00-00T00:00:00Z/9
LAST	P569	+1535-00-00T00:00:00Z/9	S2600	"6000000003043756033"
#   P570 date of death = +1595-00-00T00:00:00Z/9
LAST	P570	+1595-00-00T00:00:00Z/9	S2600	"6000000003043756033"
#   P22 father = Q141200111 Sæbjørn Toresson Talgje
LAST	P22	Q141200111	S2600	"6000000003043756033"
#   Q141200111 Sæbjørn Toresson Talgje: P40 child = the item just created
Q141200111	P40	LAST	S2600	"6000000003043756033"
#   the item just created: P735 given name = Q1548096 Tore
LAST	P735	Q1548096
#   P1449 nickname = en:"Tore Sebjornson"
LAST	P1449	en:"Tore Sebjornson"
#   add a mul alias "Tore Sebjornson Talgje"
LAST	Amul	"Tore Sebjornson Talgje"
#   add a mul alias "Tore Talgje"
LAST	Amul	"Tore Talgje"

# create a new item
CREATE
#   set the en label to "Tørres Jonson Grannes"
LAST	Len	"Tørres Jonson Grannes"
#   set the mul label to "Tørres Jonson Grannes"
LAST	Lmul	"Tørres Jonson Grannes"
#   set the ja label to "トレス・ヨンソン・グラネス"
LAST	Lja	"トレス・ヨンソン・グラネス"
#   set the zh label to "托雷斯·永松·格拉内斯"
LAST	Lzh	"托雷斯·永松·格拉内斯"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005608892520 Tørres Jonson Grannes, qualified P1810 subject named as Tørres Jonson Grannes
LAST	P2600	"6000000005608892520"	P1810	"Tørres Jonson Grannes"
#   P569 date of birth = +1741-00-00T00:00:00Z/9
LAST	P569	+1741-00-00T00:00:00Z/9	S2600	"6000000005608892520"
#   P570 date of death = +1819-01-17T00:00:00Z/11
LAST	P570	+1819-01-17T00:00:00Z/11	S2600	"6000000005608892520"
#   P40 child = Q141206057 Berte Tørresdotter Austrått
LAST	P40	Q141206057	S2600	"6000000005608892520"
#   Q141206057 Berte Tørresdotter Austrått: P22 father = the item just created
Q141206057	P22	LAST	S2600	"6000000005608892520"
#   the item just created: P734 family name = Q37442010 Grannes
LAST	P734	Q37442010
#   add a mul alias "Tørres Grannes"
LAST	Amul	"Tørres Grannes"

# create a new item
CREATE
#   set the en label to "Ulrika Charlotta Klingenstierna"
LAST	Len	"Ulrika Charlotta Klingenstierna"
#   set the mul label to "Ulrika Charlotta Klingenstierna"
LAST	Lmul	"Ulrika Charlotta Klingenstierna"
#   set the ja label to "ウルリカ・カルロタ・クリンゲンスティエルナ"
LAST	Lja	"ウルリカ・カルロタ・クリンゲンスティエルナ"
#   set the zh label to "乌尔里卡·卡尔洛塔·克利恩盖恩斯蒂埃尔纳"
LAST	Lzh	"乌尔里卡·卡尔洛塔·克利恩盖恩斯蒂埃尔纳"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000019344079214 Ulrika Charlotta Klingenstierna, qualified P1810 subject named as Ulrika Charlotta Klingenstierna
LAST	P2600	"6000000019344079214"	P1810	"Ulrika Charlotta Klingenstierna"
#   P569 date of birth = +1778-10-14T00:00:00Z/11
LAST	P569	+1778-10-14T00:00:00Z/11	S2600	"6000000019344079214"
#   P570 date of death = +1825-03-07T00:00:00Z/11
LAST	P570	+1825-03-07T00:00:00Z/11	S2600	"6000000019344079214"
#   P26 spouse = Q5725105 Eric Michael Fant
LAST	P26	Q5725105	S2600	"6000000019344079214"
#   Q5725105 Eric Michael Fant: P26 spouse = the item just created
Q5725105	P26	LAST	S2600	"6000000019344079214"
#   the item just created: P735 given name = Q18924998 Ulrika, qualified P1545 series ordinal 1, P7452 reason for preferred rank Q3409033 usual forename
LAST	P735	Q18924998	P1545	"1"	P7452	Q3409033
#   P735 given name = Q1067071 Charlotta, qualified P1545 series ordinal 2, P3831 object of statement has role Q245025 middle name
LAST	P735	Q1067071	P1545	"2"	P3831	Q245025
#   Q141219059 Gustava Maria Sofia Mannerheim: P3373 sibling = Q2415388 Carl Gustaf Mannerheim
Q141219059	P3373	Q2415388	S2600	"4143225"
#   Q2415388 Carl Gustaf Mannerheim: P3373 sibling = Q141219059 Gustava Maria Sofia Mannerheim
Q2415388	P3373	Q141219059	S2600	"6000000000047165787"
#   Q141198422 Iver Pedersen Sandsmark: P40 child = Q141205928 NN Jonsdotter
Q141198422	P40	Q141205928	S2600	"6000000002954100954"
#   Q141219069 Søren Sørenson Gjesdal: P26 spouse = Q141219065 Marta Torbjørnsdotter Gjesdal
Q141219069	P26	Q141219065	S2600	"6000000003095047808"
#   Q141219053 Barbro Reiersdatter Storhaug: P26 spouse = Q141219060 Halvor Johannesson Hobberstad
Q141219053	P26	Q141219060	S2600	"6000000005606976869"
#   Q141219065 Marta Torbjørnsdotter Gjesdal: P26 spouse = Q141219069 Søren Sørenson Gjesdal
Q141219065	P26	Q141219069	S2600	"6000000005607335640"
#   Q141219060 Halvor Johannesson Hobberstad: P26 spouse = Q141219053 Barbro Reiersdatter Storhaug
Q141219060	P26	Q141219053	S2600	"6000000005609265668"
#   Q141180408 Jon Larsson Mæle: P40 child = Q141216399 Margareta Nilsdotter
Q141180408	P40	Q141216399	S2600	"6000000005609534542"
#   Q141219054 Carl Emil Cronhielm af Hakunge: P26 spouse = Q141219062 Hedvig Ulrika Boije af Gennäs
Q141219054	P26	Q141219062	S2600	"6000000008178453589"
#   Q5542632: P25 mother = Q5542628
Q5542632	P25	Q5542628	S2600	"6000000009726668887"
#   Q141219062 Hedvig Ulrika Boije af Gennäs: P26 spouse = Q141219054 Carl Emil Cronhielm af Hakunge
Q141219062	P26	Q141219054	S2600	"6000000012888307497"
#   P40 child = Q141198422 Iver Pedersen Sandsmark
Q141205928	P40	Q141198422	S2600	"6000000017093875188"
#   Q141216399 Margareta Nilsdotter: P22 father = Q141180408 Jon Larsson Mæle
Q141216399	P22	Q141180408	S2600	"6000000017799612472"
#   Q4953277: P25 mother = Q5797554
Q4953277	P25	Q5797554	S2600	"6000000017986416972"
#   Q141219056 Christian Frenning: P40 child = Q141219061 Harriet Hjørdis Simensen
Q141219056	P40	Q141219061	S2600	"6000000019540497660"
#   Q141168784 Aagot Wendt: P40 child = Q141198370 NN Skårland
Q141168784	P40	Q141198370	S2600	"6000000021079935250"
#   Q141219061 Harriet Hjørdis Simensen: P22 father = Q141219056 Christian Frenning
Q141219061	P22	Q141219056	S2600	"6000000021122676911"
#   Q141219050 Ane Olsdatter Bø: P40 child = Q141219058 Elisabet Rasmusdatter Moen
Q141219050	P40	Q141219058	S2600	"6000000021133787411"
#   Q141219067 NN Private: P22 father = Q141219064 Lloyd Obert Dokken
Q141219067	P22	Q141219064	S2600	"6000000189964478852"
#   Q141219064 Lloyd Obert Dokken: P40 child = Q141219067 NN Private
Q141219064	P40	Q141219067	S2600	"6000000189964580833"
#   Q141219058 Elisabet Rasmusdatter Moen: P25 mother = Q141219050 Ane Olsdatter Bø
Q141219058	P25	Q141219050	S2600	"6000000225376733918"

