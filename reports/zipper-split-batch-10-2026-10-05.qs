# Zipper split batch 10 (2026-10-05): the Formbach UNSURE pairs (#350, 351, 989), careful pass. Run with Run, never in background.
# Every removal checked live before the batch was written. Himiltrude Q141628101 and Kunigunde Q141628093 are our creations; their links to the Formbach men came from the zipper pairs alone.
# 989: Geni's Ulrich I. von Formbach is not Bertold of Formbach Q61314934 (different name; the only tie was position). Kunigunde comes off Bertold; Ulrich is created as her husband
-Q141628093	P26	Q61314934
-Q61314934	P26	Q141628093
# 351: Geni's Berthold im Schweinachgau is not Thiemo I of Formbach Q61314932 (different name; Thiemo I's own wife on Wikidata is NN Q116030622). Kunigunde and Himiltrude come off Thiemo I; Berthold is created as her son and Himiltrude's husband
-Q141628093	P40	Q61314932
-Q61314932	P25	Q141628093
-Q141628101	P26	Q61314932
-Q61314932	P26	Q141628101
# 350: Geni's Thiemo (Count in the Quinziggau) IS Tiemo von Formbach Q110570732 (same name, wife NN von Braunschweig, sons Heinrich and Thiemo); his father is disputed: Thiemo I (Wikidata) or Berthold (Geni). Both fathers are qualified disputed
Q110570732	P22	Q61314932	P1480	Q18912752
CREATE
LAST	Lmul	"Berthold im Schweinachgau"
LAST	Len	"Berthold im Schweinachgau"
LAST	Den	"circa 955 Traunstein,Schwaben,Bayern - circa 1005 Schweinachgau,Donaukreis Baden W Rttemberg"
LAST	P31	Q5
LAST	P21	Q6581097
LAST	P2600	"6000000002187796770"	P1810	"Berthold im Schweinachgau"
LAST	P25	Q141628093	S2600	"6000000002187796770"
LAST	P26	Q141628101	S2600	"6000000002187796770"
LAST	P40	Q110570732	S2600	"6000000002187796770"
Q141628093	P40	LAST	S2600	"6000000002187796770"
Q141628101	P26	LAST	S2600	"6000000002187796770"
Q110570732	P22	LAST	P1480	Q18912752	S2600	"6000000002187796770"
CREATE
LAST	Lmul	"Ulrich I. von Formbach"
LAST	Len	"Ulrich I. von Formbach"
LAST	Den	"circa 912 Traungau, Germany - circa 970 Traungau, Germany"
LAST	P31	Q5
LAST	P21	Q6581097
LAST	P2600	"6000000008522578894"	P1810	"Ulrich I. von Formbach"
LAST	P26	Q141628093	S2600	"6000000008522578894"
Q141628093	P26	LAST	S2600	"6000000008522578894"
