# Zipper split batch 6 (2026-10-05): splits #541, 553, 578, 584, 633, 677, 681, 688, 723, 768, 790 in zipper-pair-verdicts.tsv.
# Every removal checked live the same hour. Our duplicates of existing items go on the merge item in queue.md. Run with Run, never in background.
# 541: our Dietrich I von Wassenberg Q141628095 is Theodoric of Guelders Q2314141 himself (merge list), not his brother
-Q141628095	P3373	Q2314141
-Q2314141	P3373	Q141628095
# 553: Ekbert (Egbert the One-Eyed, Q1322356, already has his father) is not Bruno of Walbeck: our Wichmann II comes off Bruno
-Q116150272	P22	Q141626581
-Q141626581	P40	Q116150272
# 578: Iliana Åkesdotter Bååt is Ellen Åkesdatter Q98697728, whose mother Anne Gertsdatter Q98697731 is our Anna Gerhardsdotter Snakenborg (merge list); she is not NN Haraldsdotter's mother
-Q141632415	P40	Q101248475
# 584: our NN ferch Merfyn is the wife of Llew ap Llyminod Angel ap Pasgen Q116146051 (father of her son Lludd), not of King Llywelyn ap Merfyn
-Q141628357	P26	Q2343906
-Q2343906	P26	Q141628357
Q141628357	P26	Q116146051	S2600	"6000000003649734134"
Q116146051	P26	Q141628357	S2600	"6000000003649734134"
# 633: Wandelmode de Thiern is Q110894616, whose mother Adelaide of Châlon Q2192927 is our Adélaïde (merge list); she is not Auxilia
-Q141628288	P40	Q110894617
# 677: Udo of Hildesheim is rightly Mathilde's son; his brother Konrad von Reinhausen is created
CREATE
LAST	Lmul	"Konrad von Reinhausen"
LAST	Len	"Konrad von Reinhausen"
LAST	Den	"circa 1029 Germany - 28 Aug 1086"
LAST	P31	Q5
LAST	P21	Q6581097
LAST	P2600	"6000000003828083931"	P1810	"Konrad von Reinhausen"
LAST	P22	Q116030624	S2600	"6000000003828083931"
LAST	P25	Q141628100	S2600	"6000000003828083931"
Q116030624	P40	LAST	S2600	"6000000003828083931"
Q141628100	P40	LAST	S2600	"6000000003828083931"
# 681: Adila d'Amiens is the daughter of Drogon d'Amiens (son of Drogo of Mantes and Goda), not of his brother Walter III; Drogon is created
-Q1886661	P40	Q141628265
-Q141628265	P22	Q1886661
CREATE
LAST	Lmul	"Drogon d'Amiens"
LAST	Len	"Drogon d'Amiens"
LAST	Den	"1020 Amiens - 1069 Valois"
LAST	P31	Q5
LAST	P21	Q6581097
LAST	P2600	"6000000003828268865"	P1810	"Drogon d'Amiens I"
LAST	P22	Q727996	S2600	"6000000003828268865"
LAST	P25	Q3109791	S2600	"6000000003828268865"
LAST	P40	Q141628265	S2600	"6000000003828268865"
Q727996	P40	LAST	S2600	"6000000003828268865"
Q3109791	P40	LAST	S2600	"6000000003828268865"
Q141628265	P22	LAST	S2600	"6000000003828268865"
# 688: Torild Totilsson, son of our Totil Thordsson, is not Ragnvald Knaphövde; Torild is created
-Q1342231	P22	Q141635455
-Q141635455	P40	Q1342231
CREATE
LAST	Lmul	"Torild Totilsson"
LAST	Len	"Torild Totilsson"
LAST	Den	"1020 Uppsala County - circa 1070 Uppsala"
LAST	P31	Q5
LAST	P21	Q6581097
LAST	P2600	"6000000003858604945"	P1810	"Torild Totilsson"
LAST	P22	Q141635455	S2600	"6000000003858604945"
Q141635455	P40	LAST	S2600	"6000000003858604945"
# 723: Aufrica is Afrika Macduff Q75387783, already Harald Maddadsson's wife; our Duncan is not Hvarflod Macheth's brother
-Q141628268	P3373	Q18529094
-Q18529094	P3373	Q141628268
# 768: Alcwn ap Tegid is Alcwin Q112640606, son of Tegyd and our Anne
Q141628385	P40	Q112640606	S2600	"6000000004852812605"
Q112640606	P25	Q141628385	S2600	"6000000004852812605"
# 790: Karl Magnusson (Örnfot) is Q111954876, whose father riddare Magnus Ödeson Q131725928 is our Magnus Ödesson (merge list); he is not Erengisle Torkilsson
-Q141626643	P40	Q98697707
-Q98697707	P22	Q141626643
