# INDIVIDUALS. Each is linked only to items that already exist; links
#    between two people created here wait for tomorrow, when they have
#    QIDs -- two items minted in one batch cannot point at each other.

# create a new item
CREATE
#   the item just created: set the mul label to "NN Skårland"
LAST	Lmul	"NN Skårland"
#   set the ca label to "pare de Inger Kristoffersdatter"
LAST	Lca	"pare de Inger Kristoffersdatter"
#   set the da label to "far til Inger Kristoffersdatter"
LAST	Lda	"far til Inger Kristoffersdatter"
#   set the de label to "Vater von Inger Kristoffersdatter"
LAST	Lde	"Vater von Inger Kristoffersdatter"
#   set the en label to "father of Inger Kristoffersdatter"
LAST	Len	"father of Inger Kristoffersdatter"
#   set the es label to "padre de Inger Kristoffersdatter"
LAST	Les	"padre de Inger Kristoffersdatter"
#   set the it label to "padre di Inger Kristoffersdatter"
LAST	Lit	"padre di Inger Kristoffersdatter"
#   set the ja label to "インゲル・クリストッフェシュダッテルの父"
LAST	Lja	"インゲル・クリストッフェシュダッテルの父"
#   set the nb label to "far til Inger Kristoffersdatter"
LAST	Lnb	"far til Inger Kristoffersdatter"
#   set the nl label to "vader van Inger Kristoffersdatter"
LAST	Lnl	"vader van Inger Kristoffersdatter"
#   set the pt label to "pai de Inger Kristoffersdatter"
LAST	Lpt	"pai de Inger Kristoffersdatter"
#   set the sv label to "far till Inger Kristoffersdatter"
LAST	Lsv	"far till Inger Kristoffersdatter"
#   set the zh label to "英厄尔·克里斯托弗斯达特之父"
LAST	Lzh	"英厄尔·克里斯托弗斯达特之父"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003686206816 <private> Skårland
LAST	P2600	"6000000003686206816"
#   P40 child = Q141178200 Inger Kristoffersdatter
LAST	P40	Q141178200	S2600	"6000000003686206816"
#   Q141178200 Inger Kristoffersdatter: P22 father = the item just created
Q141178200	P22	LAST	S2600	"6000000003686206816"

# create a new item
CREATE
#   the item just created: set the en label to "Anna Belestdatter Lauvsnes"
LAST	Len	"Anna Belestdatter Lauvsnes"
#   set the mul label to "Anna Belestdatter Lauvsnes"
LAST	Lmul	"Anna Belestdatter Lauvsnes"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005609418895 Anna Belestdatter Lauvsnes
LAST	P2600	"6000000005609418895"
#   P569 date of birth = +1670-00-00T00:00:00Z/9
LAST	P569	+1670-00-00T00:00:00Z/9	S2600	"6000000005609418895"
#   P570 date of death = +1727-00-00T00:00:00Z/9
LAST	P570	+1727-00-00T00:00:00Z/9	S2600	"6000000005609418895"
#   P40 child = Q141189071 Joren Jonsdatter Espedal
LAST	P40	Q141189071	S2600	"6000000005609418895"
#   Q141189071 Joren Jonsdatter Espedal: P25 mother = the item just created
Q141189071	P25	LAST	S2600	"6000000005609418895"
#   the item just created: add a mul alias "Anna Lauvsnes"
LAST	Amul	"Anna Lauvsnes"

# create a new item
CREATE
#   set the en label to "Astri Torchelsdatter Øvre Time"
LAST	Len	"Astri Torchelsdatter Øvre Time"
#   set the mul label to "Astri Torchelsdatter Øvre Time"
LAST	Lmul	"Astri Torchelsdatter Øvre Time"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003731596731 Astri Torchelsdatter Øvre Time
LAST	P2600	"6000000003731596731"
#   P569 date of birth = +1758-00-00T00:00:00Z/9
LAST	P569	+1758-00-00T00:00:00Z/9	S2600	"6000000003731596731"
#   P570 date of death = +1834-03-09T00:00:00Z/11
LAST	P570	+1834-03-09T00:00:00Z/11	S2600	"6000000003731596731"
#   P40 child = Q141178200 Inger Kristoffersdatter
LAST	P40	Q141178200	S2600	"6000000003731596731"
#   Q141178200 Inger Kristoffersdatter: P25 mother = the item just created
Q141178200	P25	LAST	S2600	"6000000003731596731"
#   the item just created: P735 given name = Q30132931 Astri
LAST	P735	Q30132931
#   add a mul alias "Astri Øvre Time"
LAST	Amul	"Astri Øvre Time"

# create a new item
CREATE
#   set the en label to "Benedicta Sunesdotter Folkungaätten"
LAST	Len	"Benedicta Sunesdotter Folkungaätten"
#   set the mul label to "Benedicta Sunesdotter Folkungaätten"
LAST	Lmul	"Benedicta Sunesdotter Folkungaätten"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000002601672538 Benedicta Sunesdotter Folkungaätten
LAST	P2600	"6000000002601672538"
#   P569 date of birth = +1220-00-00T00:00:00Z/9
LAST	P569	+1220-00-00T00:00:00Z/9	S2600	"6000000002601672538"
#   P570 date of death = +1261-00-00T00:00:00Z/9
LAST	P570	+1261-00-00T00:00:00Z/9	S2600	"6000000002601672538"
#   P26 spouse = Q6197518 Svantepolk Knutsson Viby Skarsholmsätten
LAST	P26	Q6197518	S2600	"6000000002601672538"
#   P40 child = Q101247444 Ingegerd Svantepolksdotter
LAST	P40	Q101247444	S2600	"6000000002601672538"
#   Q6197518 Svantepolk Knutsson Viby Skarsholmsätten: P26 spouse = the item just created
Q6197518	P26	LAST	S2600	"6000000002601672538"
#   Q101247444 Ingegerd Svantepolksdotter: P25 mother = the item just created
Q101247444	P25	LAST	S2600	"6000000002601672538"
#   the item just created: P735 given name = Q21147545 Benedicta
LAST	P735	Q21147545
#   P1449 nickname = en:"Bjälbo"
LAST	P1449	en:"Bjälbo"
#   add a mul alias "Bjälbo Folkungaätten"
LAST	Amul	"Bjälbo Folkungaätten"

# create a new item
CREATE
#   set the en label to "Bengt Hafridsson Lejon"
LAST	Len	"Bengt Hafridsson Lejon"
#   set the mul label to "Bengt Hafridsson Lejon"
LAST	Lmul	"Bengt Hafridsson Lejon"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000005795638104 Bengt Hafridsson Lejon
LAST	P2600	"6000000005795638104"
#   P569 date of birth = +1255-00-00T00:00:00Z/9
LAST	P569	+1255-00-00T00:00:00Z/9	S2600	"6000000005795638104"
#   P570 date of death = +1307-00-00T00:00:00Z/9
LAST	P570	+1307-00-00T00:00:00Z/9	S2600	"6000000005795638104"
#   P40 child = Q141189059 Bryniolf Bengtsson (Hafridssons ätt)
LAST	P40	Q141189059	S2600	"6000000005795638104"
#   Q141189059 Bryniolf Bengtsson (Hafridssons ätt): P22 father = the item just created
Q141189059	P22	LAST	S2600	"6000000005795638104"
#   the item just created: P735 given name = Q817199 Bengt
LAST	P735	Q817199
#   P1449 nickname = en:"Hafridssons ätt"
LAST	P1449	en:"Hafridssons ätt"
#   add a mul alias "Hafridssons ätt Lejon"
LAST	Amul	"Hafridssons ätt Lejon"

# create a new item
CREATE
#   set the en label to "Berita Larsdatter Rossavik"
LAST	Len	"Berita Larsdatter Rossavik"
#   set the mul label to "Berita Larsdatter Rossavik"
LAST	Lmul	"Berita Larsdatter Rossavik"
#   add a mul alias "Berita Larsdatter Nedre Rossavik"
LAST	Amul	"Berita Larsdatter Nedre Rossavik"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003095034654 Berita Larsdatter Nedre Rossavik
LAST	P2600	"6000000003095034654"
#   P569 date of birth = +1639-00-00T00:00:00Z/9
LAST	P569	+1639-00-00T00:00:00Z/9	S2600	"6000000003095034654"
#   P570 date of death = +1729-01-27T00:00:00Z/11
LAST	P570	+1729-01-27T00:00:00Z/11	S2600	"6000000003095034654"
#   P40 child = Q141189079 Lars Tormodsen Mele
LAST	P40	Q141189079	S2600	"6000000003095034654"
#   Q141189079 Lars Tormodsen Mele: P25 mother = the item just created
Q141189079	P25	LAST	S2600	"6000000003095034654"
#   the item just created: add a mul alias "Berita Rossavik"
LAST	Amul	"Berita Rossavik"

# create a new item
CREATE
#   set the en label to "Carl Johan Edlund"
LAST	Len	"Carl Johan Edlund"
#   set the mul label to "Carl Johan Edlund"
LAST	Lmul	"Carl Johan Edlund"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000055825108079 Carl Johan Edlund
LAST	P2600	"6000000055825108079"
#   P26 spouse = Q141178201 Marie Petrine Simensdatter Bergersen
LAST	P26	Q141178201	S2600	"6000000055825108079"
#   P40 child = Q141189094 Oskar Edlund
LAST	P40	Q141189094	S2600	"6000000055825108079"
#   Q141178201 Marie Petrine Simensdatter Bergersen: P26 spouse = the item just created
Q141178201	P26	LAST	S2600	"6000000055825108079"
#   Q141189094 Oskar Edlund: P22 father = the item just created
Q141189094	P22	LAST	S2600	"6000000055825108079"
#   the item just created: P735 given name = Q2529610 Carl, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q2529610	P1545	"1"	P7452	Q3409033
#   P735 given name = Q10989273 Johan, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q10989273	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Donald Herbert Pierson"
LAST	Len	"Donald Herbert Pierson"
#   set the mul label to "Donald Herbert Pierson"
LAST	Lmul	"Donald Herbert Pierson"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000180042586884 Donald Herbert Pierson
LAST	P2600	"6000000180042586884"
#   P569 date of birth = +1943-07-01T00:00:00Z/11
LAST	P569	+1943-07-01T00:00:00Z/11	S2600	"6000000180042586884"
#   P570 date of death = +1993-06-02T00:00:00Z/11
LAST	P570	+1993-06-02T00:00:00Z/11	S2600	"6000000180042586884"
#   P25 mother = Q141168801 Cora Estelle Tunheim
LAST	P25	Q141168801	S2600	"6000000180042586884"
#   Q141168801 Cora Estelle Tunheim: P40 child = the item just created
Q141168801	P40	LAST	S2600	"6000000180042586884"
#   the item just created: P735 given name = Q13422248 Donald, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q13422248	P1545	"1"	P7452	Q3409033
#   P735 given name = Q4926833 Herbert, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q4926833	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Eberhard margrave & duke of Friuli"
LAST	Len	"Eberhard margrave & duke of Friuli"
#   set the mul label to "Eberhard margrave & duke of Friuli"
LAST	Lmul	"Eberhard margrave & duke of Friuli"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003495348447 Eberhard margrave & duke of Friuli
LAST	P2600	"6000000003495348447"
#   P569 date of birth = +0815-00-00T00:00:00Z/9
LAST	P569	+0815-00-00T00:00:00Z/9	S2600	"6000000003495348447"
#   P570 date of death = +0867-12-16T00:00:00Z/11
LAST	P570	+0867-12-16T00:00:00Z/11	S2600	"6000000003495348447"
#   P26 spouse = Q284400 Giséle de Cysoing
LAST	P26	Q284400	S2600	"6000000003495348447"
#   P40 child = Q274606 Berengar I margrave of Friuli, king of Italy
LAST	P40	Q274606	S2600	"6000000003495348447"
#   Q284400 Giséle de Cysoing: P26 spouse = the item just created
Q284400	P26	LAST	S2600	"6000000003495348447"
#   Q274606 Berengar I margrave of Friuli, king of Italy: P22 father = the item just created
Q274606	P22	LAST	S2600	"6000000003495348447"
#   the item just created: P735 given name = Q1278816 Eberhard
LAST	P735	Q1278816
#   P1449 nickname = en:"Everardo"
LAST	P1449	en:"Everardo"
#   add a mul alias "Everardo"
LAST	Amul	"Everardo"

# create a new item
CREATE
#   set the en label to "Elisabet Marie Osmundsdatter Sør-Reime"
LAST	Len	"Elisabet Marie Osmundsdatter Sør-Reime"
#   set the mul label to "Elisabet Marie Osmundsdatter Sør-Reime"
LAST	Lmul	"Elisabet Marie Osmundsdatter Sør-Reime"
#   add a mul alias "Elisabet Marie Osmundsdatter Nygaard"
LAST	Amul	"Elisabet Marie Osmundsdatter Nygaard"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000224702448856 Elisabet Marie Osmundsdatter Nygaard
LAST	P2600	"6000000224702448856"
#   P569 date of birth = +1870-12-25T00:00:00Z/11
LAST	P569	+1870-12-25T00:00:00Z/11	S2600	"6000000224702448856"
#   P26 spouse = Q141189077 Lars Bernhard Kristiansen Sør-Reime
LAST	P26	Q141189077	S2600	"6000000224702448856"
#   Q141189077 Lars Bernhard Kristiansen Sør-Reime: P26 spouse = the item just created
Q141189077	P26	LAST	S2600	"6000000224702448856"
#   the item just created: P735 given name = Q16423275 Elisabet, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q16423275	P1545	"1"	P7452	Q3409033
#   P735 given name = Q106674406 Marie, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q106674406	P1545	"2"	P3831	Q245025
#   P734 family name = Q16880608 Nygaard, qualified object of statement has role Q2507958 birth name
LAST	P734	Q16880608	P3831	Q2507958
#   add a mul alias "Elisabet Marie Sør-Reime"
LAST	Amul	"Elisabet Marie Sør-Reime"

# create a new item
CREATE
#   set the en label to "Erik Erikson Stangeland"
LAST	Len	"Erik Erikson Stangeland"
#   set the mul label to "Erik Erikson Stangeland"
LAST	Lmul	"Erik Erikson Stangeland"
#   add a mul alias "Erik Erikson Time"
LAST	Amul	"Erik Erikson Time"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000011198194484 Erik Erikson Time
LAST	P2600	"6000000011198194484"
#   P569 date of birth = +1803-00-00T00:00:00Z/9
LAST	P569	+1803-00-00T00:00:00Z/9	S2600	"6000000011198194484"
#   P570 date of death = +1876-05-23T00:00:00Z/11
LAST	P570	+1876-05-23T00:00:00Z/11	S2600	"6000000011198194484"
#   P40 child = Q141178196 Elisabet Kirstine Eriksdatter Stangeland
LAST	P40	Q141178196	S2600	"6000000011198194484"
#   Q141178196 Elisabet Kirstine Eriksdatter Stangeland: P22 father = the item just created
Q141178196	P22	LAST	S2600	"6000000011198194484"
#   the item just created: P735 given name = Q750186 Erik
LAST	P735	Q750186
#   P734 family name = Q21452049 Stangeland
LAST	P734	Q21452049
#   P1449 nickname = en:"Erik Foss-Eikeland"
LAST	P1449	en:"Erik Foss-Eikeland"
#   add a mul alias "Erik Foss-Eikeland Stangeland"
LAST	Amul	"Erik Foss-Eikeland Stangeland"
#   add a mul alias "Erik Stangeland"
LAST	Amul	"Erik Stangeland"

# create a new item
CREATE
#   set the en label to "Erling Juel Wendt"
LAST	Len	"Erling Juel Wendt"
#   set the mul label to "Erling Juel Wendt"
LAST	Lmul	"Erling Juel Wendt"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003002459585 Erling Juel Wendt
LAST	P2600	"6000000003002459585"
#   P569 date of birth = +1893-04-16T00:00:00Z/11
LAST	P569	+1893-04-16T00:00:00Z/11	S2600	"6000000003002459585"
#   P570 date of death = +1979-12-11T00:00:00Z/11
LAST	P570	+1979-12-11T00:00:00Z/11	S2600	"6000000003002459585"
#   P26 spouse = Q141168784 Aagot Garborg
LAST	P26	Q141168784	S2600	"6000000003002459585"
#   Q141168784 Aagot Garborg: P26 spouse = the item just created
Q141168784	P26	LAST	S2600	"6000000003002459585"
#   the item just created: P735 given name = Q472066 Erling, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q472066	P1545	"1"	P7452	Q3409033

# create a new item
CREATE
#   set the en label to "Eugene LeRoy Tunheim"
LAST	Len	"Eugene LeRoy Tunheim"
#   set the mul label to "Eugene LeRoy Tunheim"
LAST	Lmul	"Eugene LeRoy Tunheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000180028300872 Eugene LeRoy Tunheim
LAST	P2600	"6000000180028300872"
#   P569 date of birth = +1918-10-14T00:00:00Z/11
LAST	P569	+1918-10-14T00:00:00Z/11	S2600	"6000000180028300872"
#   P570 date of death = +1973-08-15T00:00:00Z/11
LAST	P570	+1973-08-15T00:00:00Z/11	S2600	"6000000180028300872"
#   P22 father = Q141168809 Edward Tunheim
LAST	P22	Q141168809	S2600	"6000000180028300872"
#   Q141168809 Edward Tunheim: P40 child = the item just created
Q141168809	P40	LAST	S2600	"6000000180028300872"

# create a new item
CREATE
#   the item just created: set the en label to "Hedvig Svantepolks de Gdańsk of Danzig"
LAST	Len	"Hedvig Svantepolks de Gdańsk of Danzig"
#   set the mul label to "Hedvig Svantepolks de Gdańsk of Danzig"
LAST	Lmul	"Hedvig Svantepolks de Gdańsk of Danzig"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000003358192683 Hedvig Svantepolks de Gdańsk of Danzig
LAST	P2600	"6000000003358192683"
#   P569 date of birth = +1210-00-00T00:00:00Z/9
LAST	P569	+1210-00-00T00:00:00Z/9	S2600	"6000000003358192683"
#   P570 date of death = +1266-00-00T00:00:00Z/9
LAST	P570	+1266-00-00T00:00:00Z/9	S2600	"6000000003358192683"
#   P26 spouse = Q3743799 Knut Valdemarsson Duke of Estland, Blekinge and Lolland
LAST	P26	Q3743799	S2600	"6000000003358192683"
#   P40 child = Q6197518 Svantepolk Knutsson Viby Skarsholmsätten
LAST	P40	Q6197518	S2600	"6000000003358192683"
#   Q3743799 Knut Valdemarsson Duke of Estland, Blekinge and Lolland: P26 spouse = the item just created
Q3743799	P26	LAST	S2600	"6000000003358192683"
#   Q6197518 Svantepolk Knutsson Viby Skarsholmsätten: P25 mother = the item just created
Q6197518	P25	LAST	S2600	"6000000003358192683"
#   the item just created: P735 given name = Q13648620 Hedvig, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q13648620	P1545	"1"	P7452	Q3409033
#   P1449 nickname = en:"Hedwig of Pomorze Gdanskie"
LAST	P1449	en:"Hedwig of Pomorze Gdanskie"
#   add a mul alias "Hedwig of Pomorze Gdanskie de Gdańsk"
LAST	Amul	"Hedwig of Pomorze Gdanskie de Gdańsk"

# create a new item
CREATE
#   set the en label to "Helen Frisk"
LAST	Len	"Helen Frisk"
#   set the mul label to "Helen Frisk"
LAST	Lmul	"Helen Frisk"
#   set the ja label to "ヘレン・フリスク"
LAST	Lja	"ヘレン・フリスク"
#   set the zh label to "海伦·弗里斯克"
LAST	Lzh	"海伦·弗里斯克"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000177921459052 Helen Frisk
LAST	P2600	"6000000177921459052"
#   P40 child = Q140568870 Emma Leonhart
LAST	P40	Q140568870	S2600	"6000000177921459052"
#   Q140568870 Emma Leonhart: P25 mother = the item just created
Q140568870	P25	LAST	S2600	"6000000177921459052"
#   the item just created: P735 given name = Q13376892 Helen
LAST	P735	Q13376892
#   P734 family name = Q27877507 Frisk
LAST	P734	Q27877507

# create a new item
CREATE
#   set the en label to "Herbert August Pierson"
LAST	Len	"Herbert August Pierson"
#   set the mul label to "Herbert August Pierson"
LAST	Lmul	"Herbert August Pierson"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000039512930731 Herbert August Pierson
LAST	P2600	"6000000039512930731"
#   P569 date of birth = +1902-07-13T00:00:00Z/11
LAST	P569	+1902-07-13T00:00:00Z/11	S2600	"6000000039512930731"
#   P570 date of death = +1950-06-23T00:00:00Z/11
LAST	P570	+1950-06-23T00:00:00Z/11	S2600	"6000000039512930731"
#   P26 spouse = Q141168801 Cora Estelle Tunheim
LAST	P26	Q141168801	S2600	"6000000039512930731"
#   Q141168801 Cora Estelle Tunheim: P26 spouse = the item just created
Q141168801	P26	LAST	S2600	"6000000039512930731"
#   the item just created: P735 given name = Q4926833 Herbert, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q4926833	P1545	"1"	P7452	Q3409033
#   P735 given name = Q370731 August, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q370731	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Ingeborg Olsdatter Sandsmark"
LAST	Len	"Ingeborg Olsdatter Sandsmark"
#   set the mul label to "Ingeborg Olsdatter Sandsmark"
LAST	Lmul	"Ingeborg Olsdatter Sandsmark"
#   add a mul alias "Ingeborg Olsdatter Ueland"
LAST	Amul	"Ingeborg Olsdatter Ueland"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000002954137517 Ingeborg Olsdatter Ueland
LAST	P2600	"6000000002954137517"
#   P569 date of birth = +1837-06-01T00:00:00Z/11
LAST	P569	+1837-06-01T00:00:00Z/11	S2600	"6000000002954137517"
#   P570 date of death = +1920-04-20T00:00:00Z/11
LAST	P570	+1920-04-20T00:00:00Z/11	S2600	"6000000002954137517"
#   P40 child = Q141189104 Siri Kristine Ivarsdatter Sandsmark
LAST	P40	Q141189104	S2600	"6000000002954137517"
#   Q141189104 Siri Kristine Ivarsdatter Sandsmark: P25 mother = the item just created
Q141189104	P25	LAST	S2600	"6000000002954137517"
#   the item just created: P735 given name = Q656590 Ingeborg
LAST	P735	Q656590
#   P5056 patronym or matronym = Q51885688 Olsdatter
LAST	P5056	Q51885688
#   P734 family name = Q27889293 Ueland, qualified object of statement has role Q2507958 birth name
LAST	P734	Q27889293	P3831	Q2507958
#   add a mul alias "Ingeborg Sandsmark"
LAST	Amul	"Ingeborg Sandsmark"

# create a new item
CREATE
#   set the en label to "Iver Pedersen Sandsmark"
LAST	Len	"Iver Pedersen Sandsmark"
#   set the mul label to "Iver Pedersen Sandsmark"
LAST	Lmul	"Iver Pedersen Sandsmark"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000002954100954 Iver Pedersen Sandsmark
LAST	P2600	"6000000002954100954"
#   P569 date of birth = +1830-09-01T00:00:00Z/11
LAST	P569	+1830-09-01T00:00:00Z/11	S2600	"6000000002954100954"
#   P570 date of death = +1885-07-13T00:00:00Z/11
LAST	P570	+1885-07-13T00:00:00Z/11	S2600	"6000000002954100954"
#   P40 child = Q141189104 Siri Kristine Ivarsdatter Sandsmark
LAST	P40	Q141189104	S2600	"6000000002954100954"
#   Q141189104 Siri Kristine Ivarsdatter Sandsmark: P22 father = the item just created
Q141189104	P22	LAST	S2600	"6000000002954100954"
#   the item just created: P735 given name = Q11977747 Iver
LAST	P735	Q11977747
#   P5056 patronym or matronym = Q130233025
LAST	P5056	Q130233025

# create a new item
CREATE
#   set the en label to "Jacob Johannessen Jacobson"
LAST	Len	"Jacob Johannessen Jacobson"
#   set the mul label to "Jacob Johannessen Jacobson"
LAST	Lmul	"Jacob Johannessen Jacobson"
#   add a mul alias "Jacob Johannessen Aabø"
LAST	Amul	"Jacob Johannessen Aabø"
#   set the ja label to "ヤコブ・ヨハンネセン・ヤコブソン"
LAST	Lja	"ヤコブ・ヨハンネセン・ヤコブソン"
#   set the zh label to "雅各布·约翰内森·雅各布松"
LAST	Lzh	"雅各布·约翰内森·雅各布松"
#   add a ja alias "ヤコブ・ヨハンネセン・オーベー"
LAST	Aja	"ヤコブ・ヨハンネセン・オーベー"
#   add a zh alias "雅各布·约翰内森·奥贝"
LAST	Azh	"雅各布·约翰内森·奥贝"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000019384694298 Jacob Johannessen Aabø
LAST	P2600	"6000000019384694298"
#   P569 date of birth = +1853-03-11T00:00:00Z/11
LAST	P569	+1853-03-11T00:00:00Z/11	S2600	"6000000019384694298"
#   P570 date of death = +1877-00-00T00:00:00Z/9
LAST	P570	+1877-00-00T00:00:00Z/9	S2600	"6000000019384694298"
#   P26 spouse = Q141152600 Stine Stena Eivindsdatter Garborg
LAST	P26	Q141152600	S2600	"6000000019384694298"
#   P40 child = Q141168794 Betsy Jacobson
LAST	P40	Q141168794	S2600	"6000000019384694298"
#   Q141152600 Stine Stena Eivindsdatter Garborg: P26 spouse = the item just created
Q141152600	P26	LAST	S2600	"6000000019384694298"
#   Q141168794 Betsy Jacobson: P22 father = the item just created
Q141168794	P22	LAST	S2600	"6000000019384694298"
#   the item just created: P735 given name = Q25999604 Jacob
LAST	P735	Q25999604
#   P734 family name = Q4160058 Jacobson
LAST	P734	Q4160058
#   add a mul alias "Jacob Jacobson"
LAST	Amul	"Jacob Jacobson"

# create a new item
CREATE
#   set the en label to "Jon Nilsson Espedal"
LAST	Len	"Jon Nilsson Espedal"
#   set the mul label to "Jon Nilsson Espedal"
LAST	Lmul	"Jon Nilsson Espedal"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003095137629 Jon Nilsson Espedal
LAST	P2600	"6000000003095137629"
#   P570 date of death = +1696-00-00T00:00:00Z/9
LAST	P570	+1696-00-00T00:00:00Z/9	S2600	"6000000003095137629"
#   P40 child = Q141189071 Joren Jonsdatter Espedal
LAST	P40	Q141189071	S2600	"6000000003095137629"
#   Q141189071 Joren Jonsdatter Espedal: P22 father = the item just created
Q141189071	P22	LAST	S2600	"6000000003095137629"
#   the item just created: P735 given name = Q13501137 Jon
LAST	P735	Q13501137
#   P5056 patronym or matronym = Q130233015 Nilsson
LAST	P5056	Q130233015

# create a new item
CREATE
#   set the en label to "Kirsten Olsdatter Grøtheim"
LAST	Len	"Kirsten Olsdatter Grøtheim"
#   set the mul label to "Kirsten Olsdatter Grøtheim"
LAST	Lmul	"Kirsten Olsdatter Grøtheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000019668822075 Kirsten Olsdatter Grøtheim
LAST	P2600	"6000000019668822075"
#   P569 date of birth = +1775-00-00T00:00:00Z/9
LAST	P569	+1775-00-00T00:00:00Z/9	S2600	"6000000019668822075"
#   P22 father = Q141189088 Ola Knutsen Garborg
LAST	P22	Q141189088	S2600	"6000000019668822075"
#   P25 mother = Q141189069 Ingeborg Ådnesdatter Grøtheim
LAST	P25	Q141189069	S2600	"6000000019668822075"
#   Q141189088 Ola Knutsen Garborg: P40 child = the item just created
Q141189088	P40	LAST	S2600	"6000000019668822075"
#   Q141189069 Ingeborg Ådnesdatter Grøtheim: P40 child = the item just created
Q141189069	P40	LAST	S2600	"6000000019668822075"
#   the item just created: P735 given name = Q256744 Kirsten
LAST	P735	Q256744
#   P5056 patronym or matronym = Q51885688 Olsdatter, qualified based on Q141189088 Ola Knutsen Garborg
LAST	P5056	Q51885688	P144	Q141189088

# create a new item
CREATE
#   set the en label to "Kristina Tolvesdotter Näs"
LAST	Len	"Kristina Tolvesdotter Näs"
#   set the mul label to "Kristina Tolvesdotter Näs"
LAST	Lmul	"Kristina Tolvesdotter Näs"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 340342479380013975 Kristina Tolvesdotter Näs
LAST	P2600	"340342479380013975"
#   P569 date of birth = +1290-00-00T00:00:00Z/9
LAST	P569	+1290-00-00T00:00:00Z/9	S2600	"340342479380013975"
#   P570 date of death = +1330-00-00T00:00:00Z/9
LAST	P570	+1330-00-00T00:00:00Z/9	S2600	"340342479380013975"
#   P26 spouse = Q141189050 Algot Bryniolfsson
LAST	P26	Q141189050	S2600	"340342479380013975"
#   P40 child = Q5915800 Knut Algotsson
LAST	P40	Q5915800	S2600	"340342479380013975"
#   Q141189050 Algot Bryniolfsson: P26 spouse = the item just created
Q141189050	P26	LAST	S2600	"340342479380013975"
#   Q5915800 Knut Algotsson: P25 mother = the item just created
Q5915800	P25	LAST	S2600	"340342479380013975"
#   the item just created: P735 given name = Q19798802 Kristina
LAST	P735	Q19798802
#   P1449 nickname = en:"Tolveætten"
LAST	P1449	en:"Tolveætten"
#   add a mul alias "Tolveætten Näs"
LAST	Amul	"Tolveætten Näs"

# create a new item
CREATE
#   set the en label to "Lars Jonsen Kvam"
LAST	Len	"Lars Jonsen Kvam"
#   set the mul label to "Lars Jonsen Kvam"
LAST	Lmul	"Lars Jonsen Kvam"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000194934774831 Lars Jonsen Kvam
LAST	P2600	"6000000194934774831"
#   P735 given name = Q15635262 Lars
LAST	P735	Q15635262
#   P734 family name = Q30086760 Kvam
LAST	P734	Q30086760

# create a new item
CREATE
#   set the en label to "Lisabeth Larsdotter Stangeland"
LAST	Len	"Lisabeth Larsdotter Stangeland"
#   set the mul label to "Lisabeth Larsdotter Stangeland"
LAST	Lmul	"Lisabeth Larsdotter Stangeland"
#   add a mul alias "Lisabeth Larsdotter Vasshus"
LAST	Amul	"Lisabeth Larsdotter Vasshus"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000011198310542 Lisabeth Larsdotter Vasshus
LAST	P2600	"6000000011198310542"
#   P569 date of birth = +1800-00-00T00:00:00Z/9
LAST	P569	+1800-00-00T00:00:00Z/9	S2600	"6000000011198310542"
#   P570 date of death = +1841-08-29T00:00:00Z/11
LAST	P570	+1841-08-29T00:00:00Z/11	S2600	"6000000011198310542"
#   P40 child = Q141178196 Elisabet Kirstine Eriksdatter Stangeland
LAST	P40	Q141178196	S2600	"6000000011198310542"
#   Q141178196 Elisabet Kirstine Eriksdatter Stangeland: P25 mother = the item just created
Q141178196	P25	LAST	S2600	"6000000011198310542"
#   the item just created: P735 given name = Q21148195 Lisabeth
LAST	P735	Q21148195
#   P734 family name = Q21452049 Stangeland, qualified object of statement has role Q28418670 married name
LAST	P734	Q21452049	P3831	Q28418670
#   P1449 nickname = en:"Lisabet"
LAST	P1449	en:"Lisabet"
#   add a mul alias "Lisabet Stangeland"
LAST	Amul	"Lisabet Stangeland"
#   add a mul alias "Lisabeth Stangeland"
LAST	Amul	"Lisabeth Stangeland"

# create a new item
CREATE
#   set the en label to "Maren Olsdatter"
LAST	Len	"Maren Olsdatter"
#   set the mul label to "Maren Olsdatter"
LAST	Lmul	"Maren Olsdatter"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000055822300842 Maren Olsdatter
LAST	P2600	"6000000055822300842"
#   P26 spouse = Q141168797 Christian Frederik Bergersen
LAST	P26	Q141168797	S2600	"6000000055822300842"
#   P40 child = Q141189091 Ole Nicolai Bergersen
LAST	P40	Q141189091	S2600	"6000000055822300842"
#   P40 child = Q141189068 Hilde Constance Marie Bergersen
LAST	P40	Q141189068	S2600	"6000000055822300842"
#   Q141168797 Christian Frederik Bergersen: P26 spouse = the item just created
Q141168797	P26	LAST	S2600	"6000000055822300842"
#   Q141189091 Ole Nicolai Bergersen: P25 mother = the item just created
Q141189091	P25	LAST	S2600	"6000000055822300842"
#   Q141189068 Hilde Constance Marie Bergersen: P25 mother = the item just created
Q141189068	P25	LAST	S2600	"6000000055822300842"
#   the item just created: P735 given name = Q1666203 Maren
LAST	P735	Q1666203

# create a new item
CREATE
#   set the en label to "Olga E. Garborg Oswald"
LAST	Len	"Olga E. Garborg Oswald"
#   set the mul label to "Olga E. Garborg Oswald"
LAST	Lmul	"Olga E. Garborg Oswald"
#   add a mul alias "Olga E. Tunheim"
LAST	Amul	"Olga E. Tunheim"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000033773801550 Olga E. Tunheim
LAST	P2600	"6000000033773801550"
#   P569 date of birth = +1900-10-25T00:00:00Z/11
LAST	P569	+1900-10-25T00:00:00Z/11	S2600	"6000000033773801550"
#   P570 date of death = +1961-01-27T00:00:00Z/11
LAST	P570	+1961-01-27T00:00:00Z/11	S2600	"6000000033773801550"
#   P22 father = Q141189084 Martin Tollefson Tunheim
LAST	P22	Q141189084	S2600	"6000000033773801550"
#   P25 mother = Q141162046 Ane Oline Lena Eivindsdatter Garborg
LAST	P25	Q141162046	S2600	"6000000033773801550"
#   Q141189084 Martin Tollefson Tunheim: P40 child = the item just created
Q141189084	P40	LAST	S2600	"6000000033773801550"
#   Q141162046 Ane Oline Lena Eivindsdatter Garborg: P40 child = the item just created
Q141162046	P40	LAST	S2600	"6000000033773801550"
#   the item just created: P735 given name = Q19803501 E., qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q19803501	P1545	"2"	P3831	Q245025
#   P734 family name = Q30250555 Garborg, qualified object of statement has role Q28418670 married name
LAST	P734	Q30250555	P3831	Q28418670
#   P734 family name = Q1260183 Oswald, qualified object of statement has role Q28418670 married name
LAST	P734	Q1260183	P3831	Q28418670

# create a new item
CREATE
#   set the mul label to "NN"
LAST	Lmul	"NN"
#   set the ca label to "filla de Erling Juel Wendt"
LAST	Lca	"filla de Erling Juel Wendt"
#   set the da label to "datter af Erling Juel Wendt"
LAST	Lda	"datter af Erling Juel Wendt"
#   set the de label to "Tochter von Erling Juel Wendt"
LAST	Lde	"Tochter von Erling Juel Wendt"
#   set the en label to "daughter of Erling Juel Wendt"
LAST	Len	"daughter of Erling Juel Wendt"
#   set the es label to "hija de Erling Juel Wendt"
LAST	Les	"hija de Erling Juel Wendt"
#   set the it label to "figlia di Erling Juel Wendt"
LAST	Lit	"figlia di Erling Juel Wendt"
#   set the nb label to "datter av Erling Juel Wendt"
LAST	Lnb	"datter av Erling Juel Wendt"
#   set the nl label to "dochter van Erling Juel Wendt"
LAST	Lnl	"dochter van Erling Juel Wendt"
#   set the pt label to "filha de Erling Juel Wendt"
LAST	Lpt	"filha de Erling Juel Wendt"
#   set the sv label to "dotter till Erling Juel Wendt"
LAST	Lsv	"dotter till Erling Juel Wendt"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000021080190248 Private
LAST	P2600	"6000000021080190248"
#   P25 mother = Q141168784 Aagot Garborg
LAST	P25	Q141168784	S2600	"6000000021080190248"
#   Q141168784 Aagot Garborg: P40 child = the item just created
Q141168784	P40	LAST	S2600	"6000000021080190248"

# create a new item
CREATE
#   the item just created: set the en label to "Rangdi Rasmusdatter Sollienseie"
LAST	Len	"Rangdi Rasmusdatter Sollienseie"
#   set the mul label to "Rangdi Rasmusdatter Sollienseie"
LAST	Lmul	"Rangdi Rasmusdatter Sollienseie"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000021122137597 Rangdi Rasmusdatter Sollienseie
LAST	P2600	"6000000021122137597"
#   P569 date of birth = +1842-07-17T00:00:00Z/11
LAST	P569	+1842-07-17T00:00:00Z/11	S2600	"6000000021122137597"
#   P26 spouse = Q141168797 Christian Frederik Bergersen
LAST	P26	Q141168797	S2600	"6000000021122137597"
#   P40 child = Q141189090 Ole Christopher Christiansen
LAST	P40	Q141189090	S2600	"6000000021122137597"
#   Q141168797 Christian Frederik Bergersen: P26 spouse = the item just created
Q141168797	P26	LAST	S2600	"6000000021122137597"
#   Q141189090 Ole Christopher Christiansen: P25 mother = the item just created
Q141189090	P25	LAST	S2600	"6000000021122137597"
#   the item just created: add a mul alias "Rangdi Sollienseie"
LAST	Amul	"Rangdi Sollienseie"

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
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000177921459056 Richard Wade Borsheim
LAST	P2600	"6000000177921459056"
#   P569 date of birth = +1963-10-20T00:00:00Z/11
LAST	P569	+1963-10-20T00:00:00Z/11	S2600	"6000000177921459056"
#   P40 child = Q140568870 Emma Leonhart
LAST	P40	Q140568870	S2600	"6000000177921459056"
#   Q140568870 Emma Leonhart: P22 father = the item just created
Q140568870	P22	LAST	S2600	"6000000177921459056"
#   the item just created: P735 given name = Q1249148 Richard, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q1249148	P1545	"1"	P7452	Q3409033
#   P735 given name = Q15630117 Wade, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q15630117	P1545	"2"	P3831	Q245025

# create a new item
CREATE
#   set the en label to "Sigrid Garborg"
LAST	Len	"Sigrid Garborg"
#   set the mul label to "Sigrid Garborg"
LAST	Lmul	"Sigrid Garborg"
#   set the ja label to "シーグリ・ガルボルグ"
LAST	Lja	"シーグリ・ガルボルグ"
#   set the zh label to "西格丽·加尔博格"
LAST	Lzh	"西格丽·加尔博格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000006571991649 Sigrid Garborg
LAST	P2600	"6000000006571991649"
#   P569 date of birth = +1892-10-28T00:00:00Z/11
LAST	P569	+1892-10-28T00:00:00Z/11	S2600	"6000000006571991649"
#   P570 date of death = +1972-03-11T00:00:00Z/11
LAST	P570	+1972-03-11T00:00:00Z/11	S2600	"6000000006571991649"
#   P22 father = Q141152614 Jon Eivindson Garborg
LAST	P22	Q141152614	S2600	"6000000006571991649"
#   P25 mother = Q141189104 Siri Kristine Ivarsdatter Sandsmark
LAST	P25	Q141189104	S2600	"6000000006571991649"
#   Q141152614 Jon Eivindson Garborg: P40 child = the item just created
Q141152614	P40	LAST	S2600	"6000000006571991649"
#   Q141189104 Siri Kristine Ivarsdatter Sandsmark: P40 child = the item just created
Q141189104	P40	LAST	S2600	"6000000006571991649"
#   the item just created: P735 given name = Q634916 Sigrid
LAST	P735	Q634916
#   P734 family name = Q30250555 Garborg
LAST	P734	Q30250555

# create a new item
CREATE
#   set the en label to "Solveig Garborg"
LAST	Len	"Solveig Garborg"
#   set the mul label to "Solveig Garborg"
LAST	Lmul	"Solveig Garborg"
#   set the ja label to "ソルヴェイグ・ガルボルグ"
LAST	Lja	"ソルヴェイグ・ガルボルグ"
#   set the zh label to "索尔维格·加尔博格"
LAST	Lzh	"索尔维格·加尔博格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000006571580688 Solveig Garborg
LAST	P2600	"6000000006571580688"
#   P569 date of birth = +1904-07-15T00:00:00Z/11
LAST	P569	+1904-07-15T00:00:00Z/11	S2600	"6000000006571580688"
#   P570 date of death = +1988-12-24T00:00:00Z/11
LAST	P570	+1988-12-24T00:00:00Z/11	S2600	"6000000006571580688"
#   P22 father = Q141152614 Jon Eivindson Garborg
LAST	P22	Q141152614	S2600	"6000000006571580688"
#   P25 mother = Q141189104 Siri Kristine Ivarsdatter Sandsmark
LAST	P25	Q141189104	S2600	"6000000006571580688"
#   Q141152614 Jon Eivindson Garborg: P40 child = the item just created
Q141152614	P40	LAST	S2600	"6000000006571580688"
#   Q141189104 Siri Kristine Ivarsdatter Sandsmark: P40 child = the item just created
Q141189104	P40	LAST	S2600	"6000000006571580688"
#   the item just created: P735 given name = Q1533508 Solveig
LAST	P735	Q1533508
#   P734 family name = Q30250555 Garborg
LAST	P734	Q30250555

# create a new item
CREATE
#   set the en label to "Tore Erikson Håland"
LAST	Len	"Tore Erikson Håland"
#   set the mul label to "Tore Erikson Håland"
LAST	Lmul	"Tore Erikson Håland"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003095166856 Tore Erikson Håland
LAST	P2600	"6000000003095166856"
#   P569 date of birth = +1640-00-00T00:00:00Z/9
LAST	P569	+1640-00-00T00:00:00Z/9	S2600	"6000000003095166856"
#   P570 date of death = +1717-07-18T00:00:00Z/11
LAST	P570	+1717-07-18T00:00:00Z/11	S2600	"6000000003095166856"
#   P40 child = Q141189097 Ragnhild Toresdatter Håland i Gjesdal
LAST	P40	Q141189097	S2600	"6000000003095166856"
#   Q141189097 Ragnhild Toresdatter Håland i Gjesdal: P22 father = the item just created
Q141189097	P22	LAST	S2600	"6000000003095166856"
#   the item just created: P735 given name = Q1548096 Tore
LAST	P735	Q1548096
#   add a mul alias "Tore Håland"
LAST	Amul	"Tore Håland"

# create a new item
CREATE
#   set the en label to "Tormod Bjørnson Mele"
LAST	Len	"Tormod Bjørnson Mele"
#   set the mul label to "Tormod Bjørnson Mele"
LAST	Lmul	"Tormod Bjørnson Mele"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000007980617631 Tormod Bjørnson Mele
LAST	P2600	"6000000007980617631"
#   P569 date of birth = +1638-00-00T00:00:00Z/9
LAST	P569	+1638-00-00T00:00:00Z/9	S2600	"6000000007980617631"
#   P570 date of death = +1703-02-25T00:00:00Z/11
LAST	P570	+1703-02-25T00:00:00Z/11	S2600	"6000000007980617631"
#   P40 child = Q141189079 Lars Tormodsen Mele
LAST	P40	Q141189079	S2600	"6000000007980617631"
#   Q141189079 Lars Tormodsen Mele: P22 father = the item just created
Q141189079	P22	LAST	S2600	"6000000007980617631"
#   the item just created: P735 given name = Q7825922 Tormod
LAST	P735	Q7825922
#   add a mul alias "Tormod Mele"
LAST	Amul	"Tormod Mele"

# create a new item
CREATE
#   set the en label to "Tønnes Emil Enokson Ronneberg"
LAST	Len	"Tønnes Emil Enokson Ronneberg"
#   set the mul label to "Tønnes Emil Enokson Ronneberg"
LAST	Lmul	"Tønnes Emil Enokson Ronneberg"
#   add a mul alias "Tønnes Emil Enokson Rønneberg"
LAST	Amul	"Tønnes Emil Enokson Rønneberg"
#   set the ja label to "テンネス・エミール・エノクソン・ロンネベルグ"
LAST	Lja	"テンネス・エミール・エノクソン・ロンネベルグ"
#   set the zh label to "滕内斯·埃米尔·埃诺克松·龙内贝格"
LAST	Lzh	"滕内斯·埃米尔·埃诺克松·龙内贝格"
#   add a ja alias "テンネス・エミール・エノクソン・レンネベルグ"
LAST	Aja	"テンネス・エミール・エノクソン・レンネベルグ"
#   add a zh alias "滕内斯·埃米尔·埃诺克松·伦内贝格"
LAST	Azh	"滕内斯·埃米尔·埃诺克松·伦内贝格"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581097 male
LAST	P21	Q6581097
#   P2600 Geni.com profile ID = 6000000003491995164 Tønnes Emil Enokson Rønneberg
LAST	P2600	"6000000003491995164"
#   P569 date of birth = +1859-09-05T00:00:00Z/11
LAST	P569	+1859-09-05T00:00:00Z/11	S2600	"6000000003491995164"
#   P570 date of death = +1927-03-18T00:00:00Z/11
LAST	P570	+1927-03-18T00:00:00Z/11	S2600	"6000000003491995164"
#   P26 spouse = Q141162043 Inger Marie Mary Eivindsdatter Garborg
LAST	P26	Q141162043	S2600	"6000000003491995164"
#   P40 child = Q141168820 Eliza Ronneberg
LAST	P40	Q141168820	S2600	"6000000003491995164"
#   P40 child = Q141168789 Arnold Ronneberg
LAST	P40	Q141168789	S2600	"6000000003491995164"
#   P40 child = Q141168805 Edward Ronneberg
LAST	P40	Q141168805	S2600	"6000000003491995164"
#   P40 child = Q141168786 Alice Ronneberg
LAST	P40	Q141168786	S2600	"6000000003491995164"
#   P40 child = Q141168824 Ernest Anton Ronneberg
LAST	P40	Q141168824	S2600	"6000000003491995164"
#   Q141162043 Inger Marie Mary Eivindsdatter Garborg: P26 spouse = the item just created
Q141162043	P26	LAST	S2600	"6000000003491995164"
#   Q141168820 Eliza Ronneberg: P22 father = the item just created
Q141168820	P22	LAST	S2600	"6000000003491995164"
#   Q141168789 Arnold Ronneberg: P22 father = the item just created
Q141168789	P22	LAST	S2600	"6000000003491995164"
#   Q141168805 Edward Ronneberg: P22 father = the item just created
Q141168805	P22	LAST	S2600	"6000000003491995164"
#   Q141168786 Alice Ronneberg: P22 father = the item just created
Q141168786	P22	LAST	S2600	"6000000003491995164"
#   Q141168824 Ernest Anton Ronneberg: P22 father = the item just created
Q141168824	P22	LAST	S2600	"6000000003491995164"
#   the item just created: P735 given name = Q12008141 Tønnes, qualified series ordinal 1, reason for preferred rank Q3409033 usual forename
LAST	P735	Q12008141	P1545	"1"	P7452	Q3409033
#   P735 given name = Q989320 Emil, qualified series ordinal 2, object of statement has role Q245025 middle name
LAST	P735	Q989320	P1545	"2"	P3831	Q245025
#   P734 family name = Q7386722 Rønneberg, qualified object of statement has role Q2507958 birth name
LAST	P734	Q7386722	P3831	Q2507958
#   P1449 nickname = en:"Thom"
LAST	P1449	en:"Thom"
#   add a mul alias "Thom Ronneberg"
LAST	Amul	"Thom Ronneberg"
#   add a mul alias "Tønnes Emil Ronneberg"
LAST	Amul	"Tønnes Emil Ronneberg"

# create a new item
CREATE
#   set the en label to "nn Gunnarsdatter Frafjord"
LAST	Len	"nn Gunnarsdatter Frafjord"
#   set the mul label to "nn Gunnarsdatter Frafjord"
LAST	Lmul	"nn Gunnarsdatter Frafjord"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000005609418157 nn Gunnarsdatter Frafjord
LAST	P2600	"6000000005609418157"
#   P40 child = Q141189097 Ragnhild Toresdatter Håland i Gjesdal
LAST	P40	Q141189097	S2600	"6000000005609418157"
#   Q141189097 Ragnhild Toresdatter Håland i Gjesdal: P25 mother = the item just created
Q141189097	P25	LAST	S2600	"6000000005609418157"
#   the item just created: P734 family name = Q38902733 Frafjord, qualified object of statement has role Q28418670 married name
LAST	P734	Q38902733	P3831	Q28418670
#   add a mul alias "nn Frafjord"
LAST	Amul	"nn Frafjord"

# create a new item
CREATE
#   set the mul label to "덕장 부여"
LAST	Lmul	"덕장 부여"
#   P31 instance of = Q5 human
LAST	P31	Q5
#   P21 sex or gender = Q6581072 female
LAST	P21	Q6581072
#   P2600 Geni.com profile ID = 6000000186285688269 덕장 부여
LAST	P2600	"6000000186285688269"
#   P26 spouse = Q19657284 Buyeo Deokjang
LAST	P26	Q19657284	S2600	"6000000186285688269"
#   P40 child = Q12598947 Taebi Buyeo
LAST	P40	Q12598947	S2600	"6000000186285688269"
#   Q19657284 Buyeo Deokjang: P26 spouse = the item just created
Q19657284	P26	LAST	S2600	"6000000186285688269"
#   Q12598947 Taebi Buyeo: P25 mother = the item just created
Q12598947	P25	LAST	S2600	"6000000186285688269"

# RELATIONSHIPS between items that already exist -- the links yesterday's
#    creations made possible, and the properties never emitted. Every subject
#    and every value already has a QID, so this section depends on nothing above
#    it. It is emitted LAST, per her order: individuals, names, relationships.

#   Q116150300 Cecilie Ebbesdatter Hvide: P40 child = Q141189062 Cecilie Jonsdatter
Q116150300	P40	Q141189062	S2600	"305332989800002467"
#   P40 child = Q141189110 Tøre Jonsen
Q116150300	P40	Q141189110	S2600	"305332989800002467"
#   P40 child = Q141189080 Lave
Q116150300	P40	Q141189080	S2600	"305332989800002467"
#   set the ja label to "セシリエ・エッベスダッテル・ヴィーデ"
Q116150300	Lja	"セシリエ・エッベスダッテル・ヴィーデ"
#   set the zh label to "塞西莉厄·埃贝斯达特·维德"
Q116150300	Lzh	"塞西莉厄·埃贝斯达特·维德"
#   Q5915800 Knut Algotsson: set the ja label to "クヌート・アルゴットソン"
Q5915800	Lja	"クヌート・アルゴットソン"
#   set the zh label to "克努特·阿尔戈特松"
Q5915800	Lzh	"克努特·阿尔戈特松"
#   Q141189104 Siri Kristine Ivarsdatter Sandsmark: set the ja label to "シーリ・クリスティーネ・イーヴァシュダッテル・サンスマルク"
Q141189104	Lja	"シーリ・クリスティーネ・イーヴァシュダッテル・サンスマルク"
#   set the zh label to "西丽·克丽丝汀·伊瓦斯达特·桑斯马克"
Q141189104	Lzh	"西丽·克丽丝汀·伊瓦斯达特·桑斯马克"
#   Q141189055 Astri Torkelsdatter Gilja: P26 spouse = Q141189079 Lars Tormodsen Mele
Q141189055	P26	Q141189079	S2600	"6000000003095034747"
#   set the ja label to "アストリ・トルケルスダッテル・ギリヤ"
Q141189055	Lja	"アストリ・トルケルスダッテル・ギリヤ"
#   set the zh label to "阿斯特丽·托克尔斯达特·吉利亚"
Q141189055	Lzh	"阿斯特丽·托克尔斯达特·吉利亚"
#   Q141168957 Jonas Jonson Heigre: set the ja label to "ヨナス・ヨンソン・ヘイグレ"
Q141168957	Lja	"ヨナス・ヨンソン・ヘイグレ"
#   set the zh label to "约纳斯·永松·海格勒"
Q141168957	Lzh	"约纳斯·永松·海格勒"
#   Q141178196 Elisabet Kirstine Eriksdatter Stangeland: set the ja label to "エリサベート・シシュティーネ・エリクスダッテル・スタンゲラン"
Q141178196	Lja	"エリサベート・シシュティーネ・エリクスダッテル・スタンゲラン"
#   set the zh label to "伊丽莎白·谢什蒂内·埃里克斯达特·斯坦格兰"
Q141178196	Lzh	"伊丽莎白·谢什蒂内·埃里克斯达特·斯坦格兰"
#   Q141152523 Ane Oline Jonsdatter Raugstad: set the ja label to "アーネ・オリーネ・ヨンスダッテル・ラウグスタード"
Q141152523	Lja	"アーネ・オリーネ・ヨンスダッテル・ラウグスタード"
#   set the zh label to "安内·奥利内·永斯达特·劳格斯塔"
Q141152523	Lzh	"安内·奥利内·永斯达特·劳格斯塔"
#   Q141189070 John Jonassen Heigre: P3373 sibling = Q141178198 Enevald Jonasson Heigre
Q141189070	P3373	Q141178198	S2600	"6000000003491986951"
#   P3373 sibling = Q141189098 Rakel Jonasdatter Heigre
Q141189070	P3373	Q141189098	S2600	"6000000003491986951"
#   P3373 sibling = Q141189111 Tørres Jonasson Hegre
Q141189070	P3373	Q141189111	S2600	"6000000003491986951"
#   P3373 sibling = Q141189081 Lotte Birgithe Gustava Jonasdatter Heigre
Q141189070	P3373	Q141189081	S2600	"6000000003491986951"
#   Q141178198 Enevald Jonasson Heigre: P3373 sibling = Q141189070 John Jonassen Heigre
Q141178198	P3373	Q141189070	S2600	"6000000003491986956"
#   P3373 sibling = Q141189098 Rakel Jonasdatter Heigre
Q141178198	P3373	Q141189098	S2600	"6000000003491986956"
#   P3373 sibling = Q141189111 Tørres Jonasson Hegre
Q141178198	P3373	Q141189111	S2600	"6000000003491986956"
#   set the ja label to "エーネヴァル・ヨナソン・ヘイグレ"
Q141178198	Lja	"エーネヴァル・ヨナソン・ヘイグレ"
#   set the zh label to "埃内瓦尔德·约纳松·海格勒"
Q141178198	Lzh	"埃内瓦尔德·约纳松·海格勒"
#   Q141169046 Samuel Jonson: set the ja label to "サムエル・ヨンソン"
Q141169046	Lja	"サムエル・ヨンソン"
#   set the zh label to "萨穆埃尔·永松"
Q141169046	Lzh	"萨穆埃尔·永松"
#   Q141178381 Marta Jonsdatter Li: set the ja label to "マルタ・ヨンスダッテル・リ"
Q141178381	Lja	"マルタ・ヨンスダッテル・リ"
#   set the zh label to "玛尔塔·永斯达特·李"
Q141178381	Lzh	"玛尔塔·永斯达特·李"
#   Q141178380 Samuel Jonson Raustad: set the ja label to "サムエル・ヨンソン・ラウスタード"
Q141178380	Lja	"サムエル・ヨンソン・ラウスタード"
#   set the zh label to "萨穆埃尔·永松·劳斯塔"
Q141178380	Lzh	"萨穆埃尔·永松·劳斯塔"
#   Q141152512 Eivind Aadnesson Garborg: set the ja label to "エイヴィン・オードネソン・ガルボルグ"
Q141152512	Lja	"エイヴィン・オードネソン・ガルボルグ"
#   set the zh label to "埃温·奥德内松·加尔博格"
Q141152512	Lzh	"埃温·奥德内松·加尔博格"
#   Q141152600 Stine Stena Eivindsdatter Garborg: set the ja label to "スティーネ・ステーナ・エイヴィンスダッテル・ガルボルグ"
Q141152600	Lja	"スティーネ・ステーナ・エイヴィンスダッテル・ガルボルグ"
#   set the zh label to "斯蒂内·斯泰娜·埃温斯达特·加尔博格"
Q141152600	Lzh	"斯蒂内·斯泰娜·埃温斯达特·加尔博格"
#   Q141152614 Jon Eivindson Garborg: set the ja label to "ヨン・エイヴィンソン・ガルボルグ"
Q141152614	Lja	"ヨン・エイヴィンソン・ガルボルグ"
#   set the zh label to "永·埃温松·加尔博格"
Q141152614	Lzh	"永·埃温松·加尔博格"
#   Q141162040 Samuel Eivindsen Garborg: set the ja label to "サムエル・エイヴィンセン・ガルボルグ"
Q141162040	Lja	"サムエル・エイヴィンセン・ガルボルグ"
#   set the zh label to "萨穆埃尔·埃温森·加尔博格"
Q141162040	Lzh	"萨穆埃尔·埃温森·加尔博格"
#   Q141162041 Even Eivindson Garborg: set the ja label to "エーヴェン・エイヴィンソン・ガルボルグ"
Q141162041	Lja	"エーヴェン・エイヴィンソン・ガルボルグ"
#   set the zh label to "埃文·埃温松·加尔博格"
Q141162041	Lzh	"埃文·埃温松·加尔博格"
#   Q141162043 Inger Marie Mary Eivindsdatter Garborg: set the ja label to "インゲル・マリー・メアリー・エイヴィンスダッテル・ガルボルグ"
Q141162043	Lja	"インゲル・マリー・メアリー・エイヴィンスダッテル・ガルボルグ"
#   set the zh label to "英厄尔·玛丽·玛丽·埃温斯达特·加尔博格"
Q141162043	Lzh	"英厄尔·玛丽·玛丽·埃温斯达特·加尔博格"
#   Q141162044 Abel Eivindsen Garborg: set the ja label to "アーベル・エイヴィンセン・ガルボルグ"
Q141162044	Lja	"アーベル・エイヴィンセン・ガルボルグ"
#   set the zh label to "阿贝尔·埃温森·加尔博格"
Q141162044	Lzh	"阿贝尔·埃温森·加尔博格"
#   Q141162045 Ole Eivindsen Garborg: set the ja label to "オーレ・エイヴィンセン・ガルボルグ"
Q141162045	Lja	"オーレ・エイヴィンセン・ガルボルグ"
#   set the zh label to "奥勒·埃温森·加尔博格"
Q141162045	Lzh	"奥勒·埃温森·加尔博格"
#   Q141162046 Ane Oline Lena Eivindsdatter Garborg: set the ja label to "アーネ・オリーネ・レーナ・エイヴィンスダッテル・ガルボルグ"
Q141162046	Lja	"アーネ・オリーネ・レーナ・エイヴィンスダッテル・ガルボルグ"
#   set the zh label to "安内·奥利内·莱娜·埃温斯达特·加尔博格"
Q141162046	Lzh	"安内·奥利内·莱娜·埃温斯达特·加尔博格"
#   Q141169072 Ådne Olsen Grøtheim: set the ja label to "オードネ・オルセン・グレートヘイム"
Q141169072	Lja	"オードネ・オルセン・グレートヘイム"
#   set the zh label to "奥德内·奥尔森·格勒特海姆"
Q141169072	Lzh	"奥德内·奥尔森·格勒特海姆"
#   Q141178202 Stine Persdatter Øksnevad: set the ja label to "スティーネ・ペシュダッテル・エクスネヴァード"
Q141178202	Lja	"スティーネ・ペシュダッテル・エクスネヴァード"
#   set the zh label to "斯蒂内·佩斯达特·厄克斯内瓦"
Q141178202	Lzh	"斯蒂内·佩斯达特·厄克斯内瓦"
#   Q141168833 Ingeborg Gurie Ådnesdatter Garborg: set the ja label to "インゲボルグ・グーリエ・オードネスダッテル・ガルボルグ"
Q141168833	Lja	"インゲボルグ・グーリエ・オードネスダッテル・ガルボルグ"
#   set the zh label to "英厄堡·古里·奥德内斯达特·加尔博格"
Q141168833	Lzh	"英厄堡·古里·奥德内斯达特·加尔博格"
#   Q141168816 Elisabet Ådnesdatter Garborg: set the ja label to "エリサベート・オードネスダッテル・ガルボルグ"
Q141168816	Lja	"エリサベート・オードネスダッテル・ガルボルグ"
#   set the zh label to "伊丽莎白·奥德内斯达特·加尔博格"
Q141168816	Lzh	"伊丽莎白·奥德内斯达特·加尔博格"
#   Q141189066 Helge Rasmusson Bø: P40 child = Q141189099 Rasmus Helgesen Bø
Q141189066	P40	Q141189099	S2600	"6000000003492005191"
#   P40 child = Q141189054 Anna Maria Helgesdatter Bø
Q141189066	P40	Q141189054	S2600	"6000000003492005191"
#   P40 child = Q141189113 Ådne Helgesen Bø
Q141189066	P40	Q141189113	S2600	"6000000003492005191"
#   Q141168955 Jon Samuelsen Raustad: P26 spouse = Q141178200 Inger Kristoffersdatter
Q141168955	P26	Q141178200	S2600	"6000000003732742137"
#   set the ja label to "ヨン・サムエルセン・ラウスタード"
Q141168955	Lja	"ヨン・サムエルセン・ラウスタード"
#   set the zh label to "永·萨穆埃尔森·劳斯塔"
Q141168955	Lzh	"永·萨穆埃尔森·劳斯塔"
#   Q633094 Johannes Tomasson: P26 spouse = Q141180410 Margareta Mårtensdotter Bång
Q633094	P26	Q141180410	S2600	"6000000004334763223"
#   set the zh label to "约翰内斯·托马松"
Q633094	Lzh	"约翰内斯·托马松"
#   Q141180413 Thomas Mattsson: set the ja label to "トーマス・マットソン"
Q141180413	Lja	"トーマス・マットソン"
#   set the zh label to "托马斯·马特松"
Q141180413	Lzh	"托马斯·马特松"
#   Q141178149 Anna Fartegnsdatter Seim: set the ja label to "アンナ・ファルテグンスダッテル・セイム"
Q141178149	Lja	"アンナ・ファルテグンスダッテル・セイム"
#   set the zh label to "安娜·法尔特格恩斯达特·塞姆"
Q141178149	Lzh	"安娜·法尔特格恩斯达特·塞姆"
#   Q3143008 Karen Hulda Bergersen: P25 mother = Q141178201 Marie Petrine Simensdatter Bergersen
Q3143008	P25	Q141178201	S2600	"6000000005606976813"
#   Q11959067 Arne Olaus Fjørtoft Garborg: set the ja label to "アルネ・オーラウス・フョルトフト・ガルボルグ"
Q11959067	Lja	"アルネ・オーラウス・フョルトフト・ガルボルグ"
#   set the zh label to "阿尔内·奥劳斯·夫约托夫特·加尔博格"
Q11959067	Lzh	"阿尔内·奥劳斯·夫约托夫特·加尔博格"
#   Q141168827 Hans Eivind Garborg: set the ja label to "ハンス・エイヴィン・ガルボルグ"
Q141168827	Lja	"ハンス・エイヴィン・ガルボルグ"
#   set the zh label to "汉斯·埃温·加尔博格"
Q141168827	Lzh	"汉斯·埃温·加尔博格"
#   Q141189079 Lars Tormodsen Mele: P26 spouse = Q141189055 Astri Torkelsdatter Gilja
Q141189079	P26	Q141189055	S2600	"6000000005609425379"
#   P26 spouse = Q141189071 Joren Jonsdatter Espedal
Q141189079	P26	Q141189071	S2600	"6000000005609425379"
#   P26 spouse = Q141189097 Ragnhild Toresdatter Håland i Gjesdal
Q141189079	P26	Q141189097	S2600	"6000000005609425379"
#   set the ja label to "ラーシュ・トルモドセン・メーレ"
Q141189079	Lja	"ラーシュ・トルモドセン・メーレ"
#   set the zh label to "拉尔斯·托尔莫德森·梅勒"
Q141189079	Lzh	"拉尔斯·托尔莫德森·梅勒"
#   Q141189071 Joren Jonsdatter Espedal: P26 spouse = Q141189079 Lars Tormodsen Mele
Q141189071	P26	Q141189079	S2600	"6000000005609425388"
#   set the ja label to "ヨーレン・ヨンスダッテル・エスペダール"
Q141189071	Lja	"ヨーレン・ヨンスダッテル・エスペダール"
#   set the zh label to "约伦·永斯达特·埃斯佩达尔"
Q141189071	Lzh	"约伦·永斯达特·埃斯佩达尔"
#   Q141189097 Ragnhild Toresdatter Håland i Gjesdal: P26 spouse = Q141189079 Lars Tormodsen Mele
Q141189097	P26	Q141189079	S2600	"6000000005609425396"
#   Q141178200 Inger Kristoffersdatter: set the ja label to "インゲル・クリストッフェシュダッテル"
Q141178200	Lja	"インゲル・クリストッフェシュダッテル"
#   set the zh label to "英厄尔·克里斯托弗斯达特"
Q141178200	Lzh	"英厄尔·克里斯托弗斯达特"
#   Q141180408 Jon Larsson Li: P26 spouse = Q141180412 Marta Rasmusdatter Høle
Q141180408	P26	Q141180412	S2600	"6000000005609534542"
#   set the ja label to "ヨン・ラーション・リ"
Q141180408	Lja	"ヨン・ラーション・リ"
#   set the zh label to "永·拉尔松·李"
Q141180408	Lzh	"永·拉尔松·李"
#   Q141180412 Marta Rasmusdatter Høle: P26 spouse = Q141180408 Jon Larsson Li
Q141180412	P26	Q141180408	S2600	"6000000005609534550"
#   set the ja label to "マルタ・ラスムスダッテル・ヘーレ"
Q141180412	Lja	"マルタ・ラスムスダッテル・ヘーレ"
#   set the zh label to "玛尔塔·拉斯穆斯达特·赫勒"
Q141180412	Lzh	"玛尔塔·拉斯穆斯达特·赫勒"
#   Q141189050 Algot Bryniolfsson: P22 father = Q141189059 Bryniolf Bengtsson (Hafridssons ätt)
Q141189050	P22	Q141189059	S2600	"6000000005795638082"
#   set the ja label to "アルゴット・ブリニオルフソン"
Q141189050	Lja	"アルゴット・ブリニオルフソン"
#   set the zh label to "阿尔戈特·布吕尼奥尔夫松"
Q141189050	Lzh	"阿尔戈特·布吕尼奥尔夫松"
#   Q141180409 Magdalena Andersdotter Bure: set the ja label to "マグダレーナ・アンデシュドッテル・ブーレ"
Q141180409	Lja	"マグダレーナ・アンデシュドッテル・ブーレ"
#   set the zh label to "玛格达莱娜·安德斯多特·布雷"
Q141180409	Lzh	"玛格达莱娜·安德斯多特·布雷"
#   Q141168811 Eivind Garborg: set the ja label to "エイヴィン・ガルボルグ"
Q141168811	Lja	"エイヴィン・ガルボルグ"
#   set the zh label to "埃温·加尔博格"
Q141168811	Lzh	"埃温·加尔博格"
#   Q141168792 Astrid Garborg: set the ja label to "アストリッド・ガルボルグ"
Q141168792	Lja	"アストリッド・ガルボルグ"
#   set the zh label to "阿斯特丽德·加尔博格"
Q141168792	Lzh	"阿斯特丽德·加尔博格"
#   Q141168837 Ingebret Garborg: set the ja label to "インゲブレート・ガルボルグ"
Q141168837	Lja	"インゲブレート・ガルボルグ"
#   set the zh label to "英厄布雷特·加尔博格"
Q141168837	Lzh	"英厄布雷特·加尔博格"
#   Q141168830 Ingeborg Garborg: set the ja label to "インゲボルグ・ガルボルグ"
Q141168830	Lja	"インゲボルグ・ガルボルグ"
#   set the zh label to "英厄堡·加尔博格"
Q141168830	Lzh	"英厄堡·加尔博格"
#   Q141168954 Jon Garborg: set the ja label to "ヨン・ガルボルグ"
Q141168954	Lja	"ヨン・ガルボルグ"
#   set the zh label to "永·加尔博格"
Q141168954	Lzh	"永·加尔博格"
#   Q141189088 Ola Knutsen Garborg: P26 spouse = Q141189069 Ingeborg Ådnesdatter Grøtheim
Q141189088	P26	Q141189069	S2600	"6000000007744588495"
#   Q141189069 Ingeborg Ådnesdatter Grøtheim: P26 spouse = Q141189088 Ola Knutsen Garborg
Q141189069	P26	Q141189088	S2600	"6000000008176802346"
#   set the ja label to "インゲボルグ・オードネスダッテル・グレートヘイム"
Q141189069	Lja	"インゲボルグ・オードネスダッテル・グレートヘイム"
#   set the zh label to "英厄堡·奥德内斯达特·格勒特海姆"
Q141189069	Lzh	"英厄堡·奥德内斯达特·格勒特海姆"
#   Q141189108 Tillie Betsy Tunheim: set the ja label to "ティリー・ベッツィ・トゥンヘイム"
Q141189108	Lja	"ティリー・ベッツィ・トゥンヘイム"
#   set the zh label to "蒂莉·贝齐·通海姆"
Q141189108	Lzh	"蒂莉·贝齐·通海姆"
#   Q141178201 Marie Petrine Simensdatter Bergersen: set the ja label to "マリー・ペトリーネ・シメンスダッテル・ベルゲルセン"
Q141178201	Lja	"マリー・ペトリーネ・シメンスダッテル・ベルゲルセン"
#   set the zh label to "玛丽·佩特里内·西门斯达特·贝格尔森"
Q141178201	Lzh	"玛丽·佩特里内·西门斯达特·贝格尔森"
#   Q141168797 Christian Frederik Bergersen: P22 father = Q141178199 Gunder Bergersen
Q141168797	P22	Q141178199	S2600	"6000000009126453497"
#   P25 mother = Q141180395 Maren Gulbrandsdatter Ommestad
Q141168797	P25	Q141180395	S2600	"6000000009126453497"
#   P26 spouse = Q141178201 Marie Petrine Simensdatter Bergersen
Q141168797	P26	Q141178201	S2600	"6000000009126453497"
#   set the ja label to "クリスチャン・フレデリク・ベルゲルセン"
Q141168797	Lja	"クリスチャン・フレデリク・ベルゲルセン"
#   set the zh label to "克里斯蒂安·弗雷德里克·贝格尔森"
Q141168797	Lzh	"克里斯蒂安·弗雷德里克·贝格尔森"
#   Q101247444 Ingegerd Svantepolksdotter: set the ja label to "インゲゲルド・スヴァンテポルクスドッテル"
Q101247444	Lja	"インゲゲルド・スヴァンテポルクスドッテル"
#   set the zh label to "英格格德·斯万特波尔克斯多特"
Q101247444	Lzh	"英格格德·斯万特波尔克斯多特"
#   Q141189059 Bryniolf Bengtsson (Hafridssons ätt): P40 child = Q141189050 Algot Bryniolfsson
Q141189059	P40	Q141189050	S2600	"6000000011239545575"
#   Q141180410 Margareta Mårtensdotter Bång: set the ja label to "マルガレータ・モーテンスドッテル・ボング"
Q141180410	Lja	"マルガレータ・モーテンスドッテル・ボング"
#   set the zh label to "玛格丽塔·莫滕斯多特·邦格"
Q141180410	Lzh	"玛格丽塔·莫滕斯多特·邦格"
#   Q141189112 Wilhelmine Sophie Bergersen: set the ja label to "ヴィルヘルミーネ・ソフィー・ベルゲルセン"
Q141189112	Lja	"ヴィルヘルミーネ・ソフィー・ベルゲルセン"
#   set the zh label to "威廉明妮·索菲·贝格尔森"
Q141189112	Lzh	"威廉明妮·索菲·贝格尔森"
#   Q141189083 Martha Elida Bergersen: set the ja label to "マルタ・エリーダ・ベルゲルセン"
Q141189083	Lja	"マルタ・エリーダ・ベルゲルセン"
#   set the zh label to "玛尔塔·埃利达·贝格尔森"
Q141189083	Lzh	"玛尔塔·埃利达·贝格尔森"
#   Q141178199 Gunder Bergersen: P26 spouse = Q141180395 Maren Gulbrandsdatter Ommestad
Q141178199	P26	Q141180395	S2600	"6000000016756402733"
#   set the ja label to "グンデル・ベルゲルセン"
Q141178199	Lja	"グンデル・ベルゲルセン"
#   set the zh label to "贡德尔·贝格尔森"
Q141178199	Lzh	"贡德尔·贝格尔森"
#   Q141189084 Martin Tollefson Tunheim: set the ja label to "マルティン・トレフソン・トゥンヘイム"
Q141189084	Lja	"マルティン・トレフソン・トゥンヘイム"
#   set the zh label to "马丁·托勒夫松·通海姆"
Q141189084	Lzh	"马丁·托勒夫松·通海姆"
#   Q141180395 Maren Gulbrandsdatter Ommestad: P26 spouse = Q141178199 Gunder Bergersen
Q141180395	P26	Q141178199	S2600	"6000000020221673906"
#   set the ja label to "マーレン・グルブランスダッテル・オンメスタード"
Q141180395	Lja	"マーレン・グルブランスダッテル・オンメスタード"
#   set the zh label to "马伦·古尔布兰斯达特·翁梅斯塔德"
Q141180395	Lzh	"马伦·古尔布兰斯达特·翁梅斯塔德"
#   Q141168784 Aagot Garborg: set the ja label to "オーゴット・ガルボルグ"
Q141168784	Lja	"オーゴット・ガルボルグ"
#   set the zh label to "奥高特·加尔博格"
Q141168784	Lzh	"奥高特·加尔博格"
#   Q141189099 Rasmus Helgesen Bø: P22 father = Q141189066 Helge Rasmusson Bø
Q141189099	P22	Q141189066	S2600	"6000000021133770643"
#   Q138474188 Hans Syvertsen Nyvold: P26 spouse = Q141178197 Elisabeth Johannesen
Q138474188	P26	Q141178197	S2600	"6000000021197598122"
#   set the ja label to "ハンス・シーヴェシェン・ニーヴォル"
Q138474188	Lja	"ハンス・シーヴェシェン・ニーヴォル"
#   set the zh label to "汉斯·西韦特森·尼沃尔"
Q138474188	Lzh	"汉斯·西韦特森·尼沃尔"
#   Q141168785 Aagot Nyvold: P25 mother = Q141178197 Elisabeth Johannesen
Q141168785	P25	Q141178197	S2600	"6000000021197722738"
#   set the ja label to "オーゴット・ニーヴォル"
Q141168785	Lja	"オーゴット・ニーヴォル"
#   set the zh label to "奥高特·尼沃尔"
Q141168785	Lzh	"奥高特·尼沃尔"
#   Q141168803 Dagny Nyvold: P25 mother = Q141178197 Elisabeth Johannesen
Q141168803	P25	Q141178197	S2600	"6000000021197841042"
#   set the ja label to "ダグニー・ニーヴォル"
Q141168803	Lja	"ダグニー・ニーヴォル"
#   set the zh label to "达格妮·尼沃尔"
Q141168803	Lzh	"达格妮·尼沃尔"
#   Q141178197 Elisabeth Johannesen: P26 spouse = Q138474188 Hans Syvertsen Nyvold
Q141178197	P26	Q138474188	S2600	"6000000021198042859"
#   set the ja label to "エリーサベト・ヨハンネセン"
Q141178197	Lja	"エリーサベト・ヨハンネセン"
#   set the zh label to "伊丽莎白·约翰内森"
Q141178197	Lzh	"伊丽莎白·约翰内森"
#   Q141189081 Lotte Birgithe Gustava Jonasdatter Heigre: set the ja label to "ロッテ・ビルギーテ・グスタヴァ・ヨナスダッテル・ヘイグレ"
Q141189081	Lja	"ロッテ・ビルギーテ・グスタヴァ・ヨナスダッテル・ヘイグレ"
#   set the zh label to "洛特·比尔吉特·古斯塔娃·约纳斯达特·海格勒"
Q141189081	Lzh	"洛特·比尔吉特·古斯塔娃·约纳斯达特·海格勒"
#   Q141180406 Ingeborg Gyntesdotter: set the ja label to "インゲボルグ・ギュンテスドッテル"
Q141180406	Lja	"インゲボルグ・ギュンテスドッテル"
#   set the zh label to "英厄堡·金特斯多特"
Q141180406	Lzh	"英厄堡·金特斯多特"
#   Q141189076 Kristian Larsen Nord-Varhaug: P40 child = Q141189067 Helmik Kristiansen Sør-Reime
Q141189076	P40	Q141189067	S2600	"6000000029302543031"
#   P40 child = Q141189078 Lars Kristiansen Sør-Reime
Q141189076	P40	Q141189078	S2600	"6000000029302543031"
#   P40 child = Q141189077 Lars Bernhard Kristiansen Sør-Reime
Q141189076	P40	Q141189077	S2600	"6000000029302543031"
#   set the ja label to "クリスティアン・ラーシェン・ノール・ヴァールハウグ"
Q141189076	Lja	"クリスティアン・ラーシェン・ノール・ヴァールハウグ"
#   set the zh label to "克里斯蒂安·拉尔森·诺尔·瓦尔豪格"
Q141189076	Lzh	"克里斯蒂安·拉尔森·诺尔·瓦尔豪格"
#   Q141169062 Thoralf Tunheim: set the ja label to "トーラルフ・トゥンヘイム"
Q141169062	Lja	"トーラルフ・トゥンヘイム"
#   set the zh label to "托拉尔夫·通海姆"
Q141169062	Lzh	"托拉尔夫·通海姆"
#   Q141168801 Cora Estelle Tunheim: set the ja label to "コーラ・エステル・トゥンヘイム"
Q141168801	Lja	"コーラ・エステル・トゥンヘイム"
#   set the zh label to "科拉·埃斯特尔·通海姆"
Q141168801	Lzh	"科拉·埃斯特尔·通海姆"
#   Q141168809 Edward Tunheim: set the ja label to "エドワード・トゥンヘイム"
Q141168809	Lja	"エドワード・トゥンヘイム"
#   set the zh label to "爱德华·通海姆"
Q141168809	Lzh	"爱德华·通海姆"
#   Q141168787 Alma Matilda Tunheim: set the ja label to "アルマ・マチルダ・トゥンヘイム"
Q141168787	Lja	"アルマ・マチルダ・トゥンヘイム"
#   set the zh label to "阿尔玛·玛蒂尔达·通海姆"
Q141168787	Lzh	"阿尔玛·玛蒂尔达·通海姆"
#   Q141169041 Olaf Tunheim: set the ja label to "オーラフ・トゥンヘイム"
Q141169041	Lja	"オーラフ・トゥンヘイム"
#   set the zh label to "奥拉夫·通海姆"
Q141169041	Lzh	"奥拉夫·通海姆"
#   Q4953376 Helena Guttormsdatter: set the ja label to "ヘレナ・グットルムスダッテル"
Q4953376	Lja	"ヘレナ・グットルムスダッテル"
#   set the zh label to "海伦娜·古托尔姆斯达特"
Q4953376	Lzh	"海伦娜·古托尔姆斯达特"
#   Q141168820 Eliza Ronneberg: set the ja label to "エリザ・ロンネベルグ"
Q141168820	Lja	"エリザ・ロンネベルグ"
#   set the zh label to "伊莱扎·龙内贝格"
Q141168820	Lzh	"伊莱扎·龙内贝格"
#   Q141168789 Arnold Ronneberg: set the ja label to "アルノルド・ロンネベルグ"
Q141168789	Lja	"アルノルド・ロンネベルグ"
#   set the zh label to "阿诺德·龙内贝格"
Q141168789	Lzh	"阿诺德·龙内贝格"
#   Q141168805 Edward Ronneberg: set the ja label to "エドワード・ロンネベルグ"
Q141168805	Lja	"エドワード・ロンネベルグ"
#   set the zh label to "爱德华·龙内贝格"
Q141168805	Lzh	"爱德华·龙内贝格"
#   Q141168786 Alice Ronneberg: set the ja label to "アリス・ロンネベルグ"
Q141168786	Lja	"アリス・ロンネベルグ"
#   set the zh label to "艾丽丝·龙内贝格"
Q141168786	Lzh	"艾丽丝·龙内贝格"
#   Q141168824 Ernest Anton Ronneberg: set the ja label to "アーネスト・アントン・ロンネベルグ"
Q141168824	Lja	"アーネスト・アントン・ロンネベルグ"
#   set the zh label to "欧内斯特·安东·龙内贝格"
Q141168824	Lzh	"欧内斯特·安东·龙内贝格"
#   Q141168788 Arne Garborg Tunheim: set the ja label to "アルネ・ガルボルグ・トゥンヘイム"
Q141168788	Lja	"アルネ・ガルボルグ・トゥンヘイム"
#   set the zh label to "阿尔内·加尔博格·通海姆"
Q141168788	Lzh	"阿尔内·加尔博格·通海姆"
#   Q141180396 Tollef Tollefson Tunheim: set the ja label to "トッレヴ・トレフソン・トゥンヘイム"
Q141180396	Lja	"トッレヴ・トレフソン・トゥンヘイム"
#   set the zh label to "托勒夫·托勒夫松·通海姆"
Q141180396	Lzh	"托勒夫·托勒夫松·通海姆"
#   Q141168794 Betsy Jacobson: set the ja label to "ベッツィ・ヤコブソン"
Q141168794	Lja	"ベッツィ・ヤコブソン"
#   set the zh label to "贝齐·雅各布松"
Q141168794	Lzh	"贝齐·雅各布松"
#   Q141189101 Samuel Tunheim: set the ja label to "サムエル・トゥンヘイム"
Q141189101	Lja	"サムエル・トゥンヘイム"
#   set the zh label to "萨穆埃尔·通海姆"
Q141189101	Lzh	"萨穆埃尔·通海姆"
#   Q140568870 Emma Leonhart: P735 given name = Q541194 Emma
Q140568870	P735	Q541194
#   Q141189062 Cecilie Jonsdatter: set the ja label to "セシリエ・ヨンスダッテル"
Q141189062	Lja	"セシリエ・ヨンスダッテル"
#   set the zh label to "塞西莉厄·永斯达特"
Q141189062	Lzh	"塞西莉厄·永斯达特"
#   Q141189080 Lave: set the ja label to "ラーヴェ"
Q141189080	Lja	"ラーヴェ"
#   set the zh label to "拉弗"
Q141189080	Lzh	"拉弗"
#   Q141189054 Anna Maria Helgesdatter Bø: P22 father = Q141189066 Helge Rasmusson Bø
Q141189054	P22	Q141189066	S2600	"6000000196542059842"
#   Q141189113 Ådne Helgesen Bø: P22 father = Q141189066 Helge Rasmusson Bø
Q141189113	P22	Q141189066	S2600	"6000000196542455825"
#   Q141189067 Helmik Kristiansen Sør-Reime: P22 father = Q141189076 Kristian Larsen Nord-Varhaug
Q141189067	P22	Q141189076	S2600	"6000000221449620901"
#   Q141189078 Lars Kristiansen Sør-Reime: P22 father = Q141189076 Kristian Larsen Nord-Varhaug
Q141189078	P22	Q141189076	S2600	"6000000224702528843"
#   set the ja label to "ラーシュ・クリスティアンセン・セール・レイメ"
Q141189078	Lja	"ラーシュ・クリスティアンセン・セール・レイメ"
#   set the zh label to "拉尔斯·克里斯蒂安森·瑟尔·雷梅"
Q141189078	Lzh	"拉尔斯·克里斯蒂安森·瑟尔·雷梅"
#   Q141189077 Lars Bernhard Kristiansen Sør-Reime: P22 father = Q141189076 Kristian Larsen Nord-Varhaug
Q141189077	P22	Q141189076	S2600	"6000000224702710821"
#   Q135579480 Yasutaka Kitajima: P22 father = Q135579474 Tokitaka Kitajima
Q135579480	P22	Q135579474	S2600	"6000000227335224861"
#   Q135579474 Tokitaka Kitajima: P40 child = Q135579480 Yasutaka Kitajima
Q135579474	P40	Q135579480	S2600	"6000000227335393824"

