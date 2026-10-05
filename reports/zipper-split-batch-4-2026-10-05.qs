# Zipper split batch 4 (2026-10-05): #342 Beaumont/Tosny, #361/#362 Oleśnica, #358-#360 Bilstein. Wrong links off (checked live), right ones on.
# Session duplicates found here go on the merge list (queue). Run with Run, never in background.
# 342: our Ralph V de Tosny Q141628264's wife is Marguerite de Beaumont Q59154744, not her sister Isabella Q75387844
-Q141628264	P26	Q75387844
-Q75387844	P26	Q141628264
Q141628264	P26	Q59154744	S2600	"6000000003243400873"
Q59154744	P26	Q141628264	S2600	"6000000003243400873"
# 361/362: our Henry IV Q141632296 is not his own brother (Q573417 is himself); his brother Bolesław is Q480572
-Q141632296	P3373	Q573417
-Q573417	P3373	Q141632296
Q141632296	P3373	Q480572	S2600	"6000000004533239291"
Q480572	P3373	Q141632296	S2600	"6000000004533239291"
# 359: our Willibirg Q141632148 and Werner Q141632237 are Wikidata's Willibirg Q61865807 and Werner III Q1346411 (merge list), not their parents
-Q141632148	P40	Q61865807
-Q61865807	P25	Q141632148
-Q141632237	P40	Q61865807
# 358/360: our von Gleiberg Q141628234 is the wife of Wigger III von Bilstein, not of Werner II; our Wigger II is not Werner II's father
-Q141628234	P26	Q2561600
-Q2561600	P26	Q141628234
-Q141628234	P40	Q1346411
-Q141628233	P40	Q2561600
# Hilja von Gudensberg, daughter of our Werner von Winterthur and Willibirg
CREATE
LAST	Lmul	"Hilja von Gudensberg"
LAST	Len	"Hilja von Gudensberg"
LAST	Den	"circa 1047 Holy Roman Empire - circa 1085 Bilstein, Germany"
LAST	P31	Q5
LAST	P21	Q6581072
LAST	P2600	"6000000002187823891"	P1810	"Hilja von Gudensberg"
LAST	P22	Q141632237	S2600	"6000000002187823891"
LAST	P25	Q141632148	S2600	"6000000002187823891"
Q141632237	P40	LAST	S2600	"6000000003828361722"
Q141632148	P40	LAST	S2600	"6000000004545929704"
# Wigger III von Bilstein, son of our Wigger II, husband of our von Gleiberg
CREATE
LAST	Lmul	"Wigger III von Bilstein"
LAST	Len	"Wigger III von Bilstein"
LAST	Den	"circa 1005 Bilstein, Germany - 24 Apr 1041 Bilstein, Germany"
LAST	P31	Q5
LAST	P21	Q6581097
LAST	P2600	"6000000002187823898"	P1810	"Wigger III von Bilstein"
LAST	P22	Q141628233	S2600	"6000000002187823898"
LAST	P26	Q141628234	S2600	"6000000002187823898"
Q141628233	P40	LAST	S2600	"6000000002187823913"
Q141628234	P26	LAST	S2600	"6000000002187823906"
# Rugger von Bilstein, son of our von Gleiberg (his father Wigger III and wife Hilja are linked in the next batch)
CREATE
LAST	Lmul	"Rugger von Bilstein"
LAST	Len	"Rugger von Bilstein"
LAST	Den	"1037 Bilstein - 1096 Bilstein"
LAST	P31	Q5
LAST	P21	Q6581097
LAST	P2600	"6000000002187823883"	P1810	"Rugger von Bilstein"
LAST	P25	Q141628234	S2600	"6000000002187823883"
Q141628234	P40	LAST	S2600	"6000000002187823906"
