# Merges to do - by hand

**Emma's file, 2026-08-31**: *"Just make a 'merges to do' file that records these merges and the wikidata duplicates and all the other things we went over that's a file I'll use tomorrow to do merges manually on my own with the quickstatements session"*.

Regenerate with `python scripts/build-merges-to-do.py`. Every link is prefilled; nothing here has been executed.

**Direction:** Wikidata's `Help:Merge` keeps the **lower** Q number, so each line below merges the higher into the lower. Where that is the wrong way round - the higher item is the better-populated one - merge the other way and let the redirect fall where it should.


## 1. Wikidata duplicates in your own ledger - 16

One Geni profile carrying two Wikidata items, where the ledger tracks that person. This is a double-creation, not the two-ids-on-one-item case CLAUDE.md says to leave alone. The ledger records people we track rather than only items you made, so a few of these pair one of ours against an item that already existed - `Garlande` below is that shape, and there the lower number is also the better-populated item.

**Spot-checked live against Wikidata on 2026-08-31**: 12 of the 16 were fetched with `wbgetentities`, none is already a redirect, and each pair carries the same `P2600`. They are live duplicates, not an artefact of a stale download.

**15 of these are near-consecutive Q numbers**, which means one run created each person twice rather than two runs colliding months apart.

- **Guillaume I de Garlande, Seigneur de Garlande** - Geni `6000000001744821812`
    - merge **Q75933086** into **Q3120330** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q75933086&to=Q3120330
- **Anders Rasmusson Lea** - Geni `6000000005607296161`
    - merge **Q141225676** into **Q141225673** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q141225676&to=Q141225673
- **Anna Margareta von Walcker** - Geni `6000000009813973540`
    - merge **Q141225681** into **Q141225679** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q141225681&to=Q141225679
- **Carl Andersson** - Geni `6000000178279141871`
    - merge **Q141225694** into **Q141225693** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q141225694&to=Q141225693
- **Erik Guttormsson** - Geni `6000000007328872457`
    - merge **Q141225703** into **Q141225702** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q141225703&to=Q141225702
- **Fru Tore** - Geni `6000000150599235831`
    - merge **Q141225709** into **Q141225708** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q141225709&to=Q141225708
- **Ingeborg Simonsdatter Ytre Lima** - Geni `6000000002836363103`
    - merge **Q141225714** into **Q141225713** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q141225714&to=Q141225713
- **Jacob Knutson Skiftun** - Geni `6000000177945982827`
    - merge **Q141225730** into **Q141225729** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q141225730&to=Q141225729
- **Jakob Chydenius** - Geni `6000000000583631058`
    - merge **Q141225741** into **Q141225740** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q141225741&to=Q141225740
- **Jon Pedersen Trevland** - Geni `6000000001770193504`
    - merge **Q141225750** into **Q141225749** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q141225750&to=Q141225749
- **Karolina Andrietta Ström** - Geni `6000000009494606557`
    - merge **Q141225765** into **Q141225764** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q141225765&to=Q141225764
- **Katarina Johansdotter Ståhlbom** - Geni `6000000007367019257`
    - merge **Q141225773** into **Q141225772** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q141225773&to=Q141225772
- **Kristina Eriksdotter Ångerman** - Geni `6000000038458498753`
    - merge **Q141225780** into **Q141225779** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q141225780&to=Q141225779
- **Kristine mother of Erik Guttormsson** - Geni `6000000040760740831`
    - merge **Q141225788** into **Q141225787** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q141225788&to=Q141225787
- **Laurentius Andreae Andreae Alstrinius** - Geni `6000000025011507008`
    - merge **Q141225794** into **Q141225793** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q141225794&to=Q141225793
- **Louise Helmine Jenssen** - Geni `6000000014196858070`
    - merge **Q141225805** into **Q141225804** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q141225805&to=Q141225804

## 2. Wikidata duplicates outside your ledger - 67

Same shape, but these items are not ones the ledger records you making, so some will be somebody else's duplicates rather than ours. Lower priority, and worth a look at the item before merging.

- **6000000181286447901** - Geni `6000000181286447901`
    - merge **Q15914619** into **Q709067** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q15914619&to=Q709067
- **Johann Ernst II von Nassau-Siegen Prinz** - Geni `6000000007258599843`
    - merge **Q107637377** into **Q1694707** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q107637377&to=Q1694707
- **Dmitry Mikhailovich Koriat** - Geni `6000000008877466651`
    - merge **Q7569679** into **Q2033112** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q7569679&to=Q2033112
- **6000000222203355825** - Geni `6000000222203355825`
    - merge **Q2424758** into **Q2150277** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q2424758&to=Q2150277
- **Constantine Кориятович Koriat** - Geni `6000000033241523682`
    - merge **Q44059398** into **Q2587652** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q44059398&to=Q2587652
- **Ivan Janos Bagdonaitis Sapieha** - Geni `6000000009542502714`
    - merge **Q61791331** into **Q2614767** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q61791331&to=Q2614767
- **6000000190348432821** - Geni `6000000190348432821`
    - merge **Q55856631** into **Q3510235** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q55856631&to=Q3510235
- **6000000022147624604** - Geni `6000000022147624604`
    - merge **Q137824810** into **Q4079835** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q137824810&to=Q4079835
- **6000000008874153298** - Geni `6000000008874153298`
    - merge **Q16654743** into **Q4143538** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q16654743&to=Q4143538
- **6000000122737965912** - Geni `6000000122737965912`
    - merge **Q23988466** into **Q6170702** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q23988466&to=Q6170702
- **6000000013320216533** - Geni `6000000013320216533`
    - merge **Q123553591** into **Q7287688** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q123553591&to=Q7287688
- **6000000020237257561** - Geni `6000000020237257561`
    - merge **Q64024755** into **Q11729871** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q64024755&to=Q11729871
- **Johann Joseph Kos Koss** - Geni `6000000015232466758`
    - merge **Q54817335** into **Q11730584** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q54817335&to=Q11730584
- **Fyodor Корибутович Nesvitsky and Podolsky** - Geni `6000000003524588434`
    - merge **Q17565243** into **Q13033264** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q17565243&to=Q13033264
- **6000000002460337190** - Geni `6000000002460337190`
    - merge **Q22813806** into **Q16588013** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q22813806&to=Q16588013
- **6000000027822596267** - Geni `6000000027822596267`
    - merge **Q135841431** into **Q18011853** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q135841431&to=Q18011853
- **6000000028265655898** - Geni `6000000028265655898`
    - merge **Q121009606** into **Q24263178** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q121009606&to=Q24263178
- **Lubov Ivanovna of Moscow** - Geni `6000000033241899724`
    - merge **Q130389513** into **Q27031142** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q130389513&to=Q27031142
- **6000000014959053284** - Geni `6000000014959053284`
    - merge **Q27037997** into **Q27037989** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q27037997&to=Q27037989
- **6000000015339706261** - Geni `6000000015339706261`
    - merge **Q123998132** into **Q48809122** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q123998132&to=Q48809122
- **6000000006878830960** - Geni `6000000006878830960`
    - merge **Q105338590** into **Q55654045** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q105338590&to=Q55654045
- **6000000074825133860** - Geni `6000000074825133860`
    - merge **Q115574147** into **Q55849619** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q115574147&to=Q55849619
- **6000000011243047286** - Geni `6000000011243047286`
    - merge **Q64229816** into **Q64029409** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q64229816&to=Q64029409
- **6000000049984380848** - Geni `6000000049984380848`
    - merge **Q96598227** into **Q64236100** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q96598227&to=Q64236100
- **6000000006796376321** - Geni `6000000006796376321`
    - merge **Q111577500** into **Q65553166** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q111577500&to=Q65553166
- **6000000039011963879** - Geni `6000000039011963879`
    - merge **Q105565695** into **Q65933459** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q105565695&to=Q65933459
- **6000000086468284005** - Geni `6000000086468284005`
    - merge **Q111906830** into **Q66777976** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q111906830&to=Q66777976
- **6000000005599120081** - Geni `6000000005599120081`
    - merge **Q75381684** into **Q75273565** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q75381684&to=Q75273565
- **6000000057238218914** - Geni `6000000057238218914`
    - merge **Q75944406** into **Q75923553** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q75944406&to=Q75923553
- **6000000013775952915** - Geni `6000000013775952915`
    - merge **Q75992119** into **Q75992117** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q75992119&to=Q75992117
- **6000000002860967961** - Geni `6000000002860967961`
    - merge **Q120599025** into **Q96207667** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q120599025&to=Q96207667
- **Semyon Andryevich Kurakin Boyar** - Geni `6000000011242532340`
    - merge **Q113411923** into **Q102856512** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q113411923&to=Q102856512
- **6000000014882880868** - Geni `6000000014882880868`
    - merge **Q130885409** into **Q103819279** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q130885409&to=Q103819279
- **6000000015972329829** - Geni `6000000015972329829`
    - merge **Q108372045** into **Q103922542** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q108372045&to=Q103922542
- **6000000179964487850** - Geni `6000000179964487850`
    - merge **Q104811700** into **Q104704111** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q104811700&to=Q104704111
- **6000000064865319259** - Geni `6000000064865319259`
    - merge **Q105512751** into **Q105364110** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q105512751&to=Q105364110
- **6000000178715103822** - Geni `6000000178715103822`
    - merge **Q105512921** into **Q105454550** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q105512921&to=Q105454550
- **6000000015163699130** - Geni `6000000015163699130`
    - merge **Q137766722** into **Q108379406** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q137766722&to=Q108379406
- **6000000011424147943** - Geni `6000000011424147943`
    - merge **Q126995882** into **Q108654961** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q126995882&to=Q108654961
- **6000000017255784111** - Geni `6000000017255784111`
    - merge **Q134287388** into **Q110106057** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q134287388&to=Q110106057
- **6000000024682955809** - Geni `6000000024682955809`
    - merge **Q110504869** into **Q110151011** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q110504869&to=Q110151011
- **6000000024775108318** - Geni `6000000024775108318`
    - merge **Q110504870** into **Q110151012** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q110504870&to=Q110151012
- **6000000012770852334** - Geni `6000000012770852334`
    - merge **Q130748682** into **Q110363080** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q130748682&to=Q110363080
- **Nicolaus* Andreas Graf von Maltzahn, Freiherr zu Wartenberg und Penzlin** - Geni `6000000105706792946`
    - merge **Q128070478** into **Q110410743** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q128070478&to=Q110410743
- **6000000018947989438** - Geni `6000000018947989438`
    - merge **Q134290774** into **Q111133765** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q134290774&to=Q111133765
- **6000000014959439326** - Geni `6000000014959439326`
    - merge **Q121028157** into **Q111961568** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q121028157&to=Q111961568
- **6000000013071012314** - Geni `6000000013071012314`
    - merge **Q128046540** into **Q113251690** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q128046540&to=Q113251690
- **6000000018400226735** - Geni `6000000018400226735`
    - merge **Q128048436** into **Q116471168** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q128048436&to=Q116471168
- **6000000130737087039** - Geni `6000000130737087039`
    - merge **Q131480109** into **Q120759118** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q131480109&to=Q120759118
- **Anna Sapiega** - Geni `6000000020070514278`
    - merge **Q122925808** into **Q122925780** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q122925808&to=Q122925780
- **Fredrik Pfeiff** - Geni `6000000023180016165`
    - merge **Q128049736** into **Q122958274** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q128049736&to=Q122958274
- **6000000019344873694** - Geni `6000000019344873694`
    - merge **Q128160134** into **Q123604501** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q128160134&to=Q123604501
- **6000000025067047958** - Geni `6000000025067047958`
    - merge **Q138463984** into **Q124598682** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q138463984&to=Q124598682
- **6000000023663972906** - Geni `6000000023663972906`
    - merge **Q136463735** into **Q126904573** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q136463735&to=Q126904573
- **Alexander Aleksy Czetwertynski** - Geni `6000000014067654981`
    - merge **Q131411864** into **Q127325158** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q131411864&to=Q127325158
- **6000000002598298740** - Geni `6000000002598298740`
    - merge **Q129160455** into **Q127598463** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q129160455&to=Q127598463
- **6000000001827504600** - Geni `6000000001827504600`
    - merge **Q136912711** into **Q128043243** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q136912711&to=Q128043243
- **6000000012768218201** - Geni `6000000012768218201`
    - merge **Q134695058** into **Q128158598** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q134695058&to=Q128158598
- **6000000201641958861** - Geni `6000000201641958861`
    - merge **Q138297797** into **Q128197913** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q138297797&to=Q128197913
- **6000000013294621009** - Geni `6000000013294621009`
    - merge **Q134269883** into **Q134267712** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q134269883&to=Q134267712
- **6000000219324635826** - Geni `6000000219324635826`
    - merge **Q135107244** into **Q135107221** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q135107244&to=Q135107221
    - merge **Q135107247** into **Q135107221** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q135107247&to=Q135107221
    - merge **Q135107434** into **Q135107221** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q135107434&to=Q135107221
    - merge **Q135107514** into **Q135107221** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q135107514&to=Q135107221
- **6000000186712720840** - Geni `6000000186712720840`
    - merge **Q140502546** into **Q135657856** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q140502546&to=Q135657856
- **6000000006201749414** - Geni `6000000006201749414`
    - merge **Q136147671** into **Q136084762** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q136147671&to=Q136084762
- **Jacob Hansson Hummel** - Geni `6000000015284496874`
    - merge **Q136822535** into **Q136812848** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q136822535&to=Q136812848
- **Carl Christoffer von Kothen** - Geni `6000000013254785075`
    - merge **Q138411953** into **Q138411942** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q138411953&to=Q138411942
- **6000000007632275745** - Geni `6000000007632275745`
    - merge **Q138978274** into **Q138978241** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q138978274&to=Q138978241
- **6000000049542888882** - Geni `6000000049542888882`
    - merge **Q139047034** into **Q139046841** - https://www.wikidata.org/wiki/Special:MergeItems?from=Q139047034&to=Q139046841

## 3. Geni merges that cross a manager

Real duplicates where the other profile belongs to somebody else, so the merge is a request another editor sees. The Izumo pair that was entirely yours (`Munetoshi 71 Senge`) is already merged; `Okinaga no Sukune` was merged before we got there.

- **Shigeyasu Takaoka** - yours `6000000227331730906` (19 Aug placeholder, `Q135579463` in the About) against `6000000217687134824`, added by **Isao Takaoka** in April 2025 and managed by him: b.1437, d.1483, father of Joan Bingo-nyudo Takaoka. Same name, same father `Shigeyori Takaoka`.
    - https://www.geni.com/people/x/6000000227331730906
    - https://www.geni.com/people/x/6000000217687134824

- **The 40 largest CJK groups** are in `reports/geni-merge-worklist.md` and are not repeated here. The `坂上` groups under a `Tanba` parent are the real signal - eight of them, 3 to 6 profiles each. The bare one-token surname groups (`杨`, `黄`, `邱`) are an artefact of the name column and are **not** evidence of duplication.


## 4. Items you flagged as wrong, to look at in the same sitting

Not duplicates - three you called erroneous on 2026-08-30. None has been investigated, and each is still its own queue item.

- **`Q141223488`** and the item merged into it - *"both just completely erroneous"*. https://www.wikidata.org/wiki/Q141223488
- **`Q6197518`** - the `mul` label was "corrected" to an English-only one and you did not understand why. https://www.wikidata.org/wiki/Q6197518
- **"En dödfödd son Bielke"** - created as a label, which is a description of a stillborn child rather than a name.


## 5. Name items that look like Wikidata duplicates

**43 distinct item pairs**, across 59 name strings. Two items for one name with **identical English descriptions** and nothing else to tell them apart — `Schloss` is `Q105540652` *family name* and `Q37300956` *family name*.

`reports/name-ambiguity-causes.md` found this bucket and its verdict was *"worth reporting upstream rather than choosing between"*. **An identical description is evidence, not proof** — the description may simply be too thin to distinguish two real names — so these are candidates to look at, not merges to run blind. They do not feed the name plan and nothing here depends on them.

Some pairs appear under more than one spelling, which is itself a hint: `Strauss` and `Strauß` resolve to the same two items, as do `FitzGerald` and `Fitzgerald`.

- **Schloss, Schloß** — family, 118 bearer(s), both described *family name*
    - merge **Q105540652** into **Q37300956** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q105540652&to=Q37300956
- **STRAUSS, Strauss, Strauß** — family, 116 bearer(s), both described *family name*
    - merge **Q15731389** into **Q10450274** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q15731389&to=Q10450274
- **Joanna** — given, 97 bearer(s), both described *female given name*
    - merge **Q106481439** into **Q4248351** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q106481439&to=Q4248351
- **De Sousa, de Sousa** — family, 70 bearer(s), both described *family name*
    - merge **Q99908123** into **Q55739047** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q99908123&to=Q55739047
- **FitzGerald, Fitzgerald, fitzGerald, fitzgerald** — family, 45 bearer(s), both described *family name*
    - merge **Q55550590** into **Q16466739** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q55550590&to=Q16466739
- **LeRoy, Leroy** — given, 35 bearer(s), both described *male given name*
    - merge **Q19839124** into **Q19839067** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q19839124&to=Q19839067
- **Rodríguez** — family, 33 bearer(s), both described *family name*
    - merge **Q63315319** into **Q1654058** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q63315319&to=Q1654058
- **Reiss, Reiß** — family, 28 bearer(s), both described *family name*
    - merge **Q60170844** into **Q15725918** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q60170844&to=Q15725918
- **Hess, Heß** — family, 25 bearer(s), both described *family name*
    - merge **Q57661293** into **Q21482735** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q57661293&to=Q21482735
- **FitzRoy, Fitzroy, fitzRoy** — family, 21 bearer(s), both described *family name*
    - merge **Q92288868** into **Q21233885** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q92288868&to=Q21233885
- **Da Costa, da Costa** — family, 16 bearer(s), both described *family name*
    - merge **Q63677459** into **Q23038711** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q63677459&to=Q23038711
- **Demetrios** — given, 11 bearer(s), both described *male given name*
    - merge **Q30127367** into **Q19803788** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q30127367&to=Q19803788
- **de Mesquita** — family, 10 bearer(s), both described *family name*
    - merge **Q130724081** into **Q101038014** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q130724081&to=Q101038014
- **Gross** — family, 8 bearer(s), both described *family name*
    - merge **Q57645534** into **Q14290163** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q57645534&to=Q14290163
- **Angress** — family, 7 bearer(s), both described *family name*
    - merge **Q107527023** into **Q105975011** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q107527023&to=Q105975011
- **Haussmann, Haußmann** — family, 7 bearer(s), both described *family name*
    - merge **Q74081542** into **Q1591313** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q74081542&to=Q1591313
- **MacDonald, Macdonald** — family, 7 bearer(s), both described *family name*
    - merge **Q52984204** into **Q2778569** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q52984204&to=Q2778569
- **de Zúñiga** — family, 5 bearer(s), both described *family name*
    - merge **Q133254410** into **Q99981154** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q133254410&to=Q99981154
- **Mackay** — family, 4 bearer(s), both described *family name*
    - merge **Q63978307** into **Q21506751** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q63978307&to=Q21506751
- **Evaristo** — given, 4 bearer(s), both described *male given name*
    - merge **Q21156914** into **Q18402192** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q21156914&to=Q18402192
- **Máximo** — given, 4 bearer(s), both described *male given name*
    - merge **Q20000642** into **Q4475314** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q20000642&to=Q4475314
- **Pruss** — family, 3 bearer(s), both described *family name*
    - merge **Q83495364** into **Q37491734** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q83495364&to=Q37491734
- **MacWilliam** — family, 3 bearer(s), both described *family name*
    - merge **Q105623240** into **Q36873851** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q105623240&to=Q36873851
- **de Witt** — family, 3 bearer(s), both described *family name*
    - merge **Q106352426** into **Q16869461** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q106352426&to=Q16869461
- **de Vries** — family, 3 bearer(s), both described *family name*
    - merge **Q83345792** into **Q1180481** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q83345792&to=Q1180481
- **MacKenzie** — family, 3 bearer(s), both described *family name*
    - merge **Q59196750** into **Q13553907** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q59196750&to=Q13553907
- **Macdonald** — given, 3 bearer(s), both described *male given name*
    - merge **Q55747656** into **Q21513094** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q55747656&to=Q21513094
- **Nussbaum, Nußbaum** — family, 3 bearer(s), both described *family name*
    - merge **Q83500875** into **Q30106376** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q83500875&to=Q30106376
- **van Cleef** — family, 2 bearer(s), both described *family name*
    - merge **Q136230075** into **Q21492169** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q136230075&to=Q21492169
- **du Parc** — family, 2 bearer(s), both described *family name*
    - merge **Q104594425** into **Q62705779** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q104594425&to=Q62705779
- **de Guevara** — family, 2 bearer(s), both described *family name*
    - merge **Q111669728** into **Q99981096** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q111669728&to=Q99981096
- **Dubois** — family, 2 bearer(s), both described *family name*
    - merge **Q57905938** into **Q16798403** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q57905938&to=Q16798403
- **Yael** — given, 2 bearer(s), both described *female given name*
    - merge **Q104409736** into **Q8046631** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q104409736&to=Q8046631
- **MacDowall** — family, 1 bearer(s), both described *family name*
    - merge **Q99910038** into **Q6723006** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q99910038&to=Q6723006
- **Sass** — family, 1 bearer(s), both described *family name*
    - merge **Q111605746** into **Q21484988** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q111605746&to=Q21484988
- **Glass** — family, 1 bearer(s), both described *family name*
    - merge **Q57249851** into **Q16870200** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q57249851&to=Q16870200
- **Clauss** — family, 1 bearer(s), both described *family name*
    - merge **Q83500996** into **Q21482988** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q83500996&to=Q21482988
- **MacMillan** — family, 1 bearer(s), both described *family name*
    - merge **Q77024917** into **Q26709983** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q77024917&to=Q26709983
- **Maclean** — given, 1 bearer(s), both described *male given name*
    - merge **Q64349020** into **Q29960616** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q64349020&to=Q29960616
- **Fitzroy** — given, 1 bearer(s), both described *male given name*
    - merge **Q92240617** into **Q21079620** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q92240617&to=Q21079620
- **Marsden** — given, 1 bearer(s), both described *given name*
    - merge **Q104265037** into **Q52186513** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q104265037&to=Q52186513
- **Mackenzie** — given, 1 bearer(s), both described *unisex given name*
    - merge **Q84323319** into **Q14667660** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q84323319&to=Q14667660
- **Maryanne** — given, 1 bearer(s), both described *female given name*
    - merge **Q63339460** into **Q20898971** — https://www.wikidata.org/wiki/Special:MergeItems?from=Q63339460&to=Q20898971

## 6. Created by a batch, and needing a merge afterwards

**Emma flagged this one herself, 2026-08-31**, while running the batch: *"we are gonna want to merge https://www.wikidata.org/wiki/Q130665779 with our recently created thing at some point"*.

- **Ulrika von Düben** — `Q130665779` (sv *svensk friherrinna*, b. 1749-01-26, d. 1777-01-13) against the item `reports/wikidata-garborg-day.qs` creates for Geni `6000000009063273551`.
    - merge the newly created item **into `Q130665779`** — it is the older and far better populated one, carrying `P22`, `P25`, `P26`, `P27`, `P40`×2, `P569`, `P570`, `P734` and `P735`.
    - https://www.wikidata.org/wiki/Q130665779

**Why the duplicate guard did not stop it, which is the part worth knowing.** `build-garborg-day.py` blocks a creation when `out/wikidata/p2600-all.tsv` already links that Geni id — and **`Q130665779` carries no `P2600` at all**, so there was nothing to match on. The guard is a `P2600` join and is blind to an item that has never been linked to Geni.

**They are the same person on STRUCTURE, not on the name.** Our `6000000009063273551` has spouse `6000000007680468910`, which the ledger holds as `Q5626148` *Carl Wilhelm von Düben*; `Q130665779` carries `P26 Q5626148` — the same husband. That is a closed-slot match of the kind `CLAUDE.md` permits, not a name similarity.

**Creating then merging is not a defect here.** `CLAUDE.md` § *Her own duplicates are DELIBERATE* records that a creation followed by a merge leaves the edit trail she wants, and she raised this as something to do *at some point* rather than something to prevent.


## 7. Name items merged away by other editors

Your 2026-08-29 note: name items we created were merged into existing ones, and *"creating the name objects and having them merged by somebody else... is a thing that gets attention in a bad way"*. `Tunheim` is the one that already happened. The fix - invert the default so an existing name item is reused - is a queue item, not something for this sitting; it is here so the merges are in one place.

