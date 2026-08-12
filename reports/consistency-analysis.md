# The "impossible" dates: what is actually going on with them

**Emma, 2026-08-11:** *"it's your job to do analysis on these to figure out
what's actually going on with them. The chances are there is actually something
going on with them, and you're just deeming them impossible or whatever… you have
to do the research on it."*

She was right, and the mechanism is specific.

## The defect

`consistency.check` compares `person.birth_year` against `parent.birth_year` —
**bare integers**. `GedcomDate` already carries `raw`, `modifier`, `year_end` and
`is_exact`, and none of it reaches the comparison. So a child recorded `ABT 1500`
against a parent recorded `ABT 1512` is reported as born twelve years before their
own parent, on two dates that the source explicitly declines to assert.

**5,094 of 6,734 findings
(75.6%)
involve at least one date carrying `ABT`, `BEF`, `AFT` or `BET`.**

## What survives when a date is read as the interval it denotes

`ABT` becomes year ± tolerance; `BEF y` becomes (−∞, y]; `AFT y` becomes [y, +∞);
`BET x AND y` becomes [x, y]; a plain year stays a point. A contradiction is real
only when the intervals cannot be reconciled at all.

**The `ABT` tolerance is not chosen here.** Survival is given at four values so
the sensitivity is visible and the choice is Emma's.

| rule | kind | findings | all dates exact | ±0 | ±2 | ±5 | ±10 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| born-after-parent-died | impossible | 3,126 | 916 | 2,580 | 2,309 | 2,056 | 1,837 |
| parent-under-12 | implausible | 2,479 | 456 | 2,216 | 1,551 | 1,116 | 727 |
| born-before-parent-born | impossible | 1,003 | 208 | 888 | 816 | 684 | 593 |
| born-after-own-death | impossible | 67 | 29 | 58 | 56 | 54 | 50 |
| lifespan-over-120 | implausible | 59 | 31 | 55 | 52 | 46 | 45 |
| **total** | | **6,734** | **1,640** | 5,797 | 4,784 | 3,956 | 3,252 |

**At ±5 years, 3,956 of 6,734 findings survive — 58.7%.**
The other 2,778 are artefacts of comparing approximations as if they were
assertions.

## What the surviving findings look like

Every one is in `reports/consistency-surviving.csv`. Up to eight per rule here.

### born-after-parent-died — survives

| person | dates |
| --- | --- |
| `6000000001422108482` Cornelia | b -1 / d ABT 30 · other `6000000030500209802` Lucius Cornelius: b -35 / d -3 |
| `6000000008406763901` Berenice | b -100 / d — · other `6000000006101240223` Attalus Philometor Euergetes .: b ABT -170 / d -133 |
| `6000000041087974277` Ariarathes . | b -101 / d -96 · other `6000000002187617502` Ariarathes: b — / d -116 |
| `6000000003223071336` Duathathor-Henuttawy | b ABT -1060 / d -992 · other `6000000002187610715` Ramesses XI: b ABT -1107 / d ABT -1078 |
| `6000000000795550634` Da'ud ben Shemaya . | b ABT -110 / d ABT -65 · other `6000000000795569798` Shemaya .: b ABT -140 / d ABT -129 |
| `6000000028714321402` 고 해 고 | b -12 / d 9 · other `6000000028527405533` 송 송: b -32 / d -17 |
| `6000000003897579687` Samos Theosebes Dikaios | b -120 / d -63 · other `6000000006971357246` Ptolemy: b -202 / d ABT -130 |
| `6000000008630614631` Usimare Ramesses | b ABT -1217 / d APR -1155 · other `6000000006101038160` Tiy-Merenese: b -1235 / d -1225 |

### parent-under-12 — survives

| person | dates |
| --- | --- |
| `6000000003828382561` Gaius Vipstanus Messalla Gallus | b ABT -10 / d AFT 60 · other `6000000003828382547` Valeria .: b ABT -10 / d — |
| `6000000000700918979` Alexander II | b -100 / d -49 · other `6000000003827406874` Aristobulus II: b ABT -100 / d -48 |
| `6000000007224757915` Tentsepeh | b -1015 / d — · other `6000000007224956995` Methenweshket: b -1025 / d — |
| `6000000041199817885` Marcus Valerius Messalla Rufus | b BET -104 AND -103 / d -26 · other `6000000007550597526` Marcus Valerius Messalla Niger: b ABT -104 / d ABT -50 |
| `6000000008952510667` Servius Sulpicius (106-43 BC) | b -106 / d -43 · other `6000000041235437422` Servius Sulpicius Rufus: b ABT -106 / d -43 |
| `6000000016652352230` Menkheperre High Priest of Amun at Thebes . | b ABT -1065 / d ABT -992 · other `6000000002187604838` Pinedjem I Setepenre .: b ABT -1065 / d ABT -1032 |
| `6000000006758025668` Herihor | b -1140 / d ABT -1074 · other `6000000002837446392` Ast .: b ABT -1140 / d — |
| `6000000005757895476` Fulvia (or Crossutia) | b ABT -125 / d — · other `6000000002187600052` Marcus Fulvius Flaccus Bambalus: b -125 / d — |

### born-before-parent-born — survives

| person | dates |
| --- | --- |
| `6000000000961703967` Shimon II haZaken | b -10 / d 70 · other `6000000001288397755` Gamaliel HaZaken ben Shimon: b ABT 50 / d 68 |
| `6000000004089129056` Lepidus Aemilius | b -100 / d -39 · other `6000000006605840379` Vipsania Julia Agrippina: b ABT -19 / d 29 |
| `6000000000701087672` Lucius Scribonius Libo | b ABT -110 / d ABT -80 · other `6000000012941409453` Lucius Scribonius Libo: b ABT -80 / d ABT -34 |
| `6000000008564095591` Udd Al-Adnani | b -110 / d — · other `6000000023841490785` Tamlik: b -90 / d — |
| `6000000003645870484` Marcus Licinius Crassus | b -115 / d -53 · other `6000000003513086312` Publius Licinius Crassus Dives: b ABT 170 / d -97 |
| `6000000000104035781` Hú Gōng 胡公 Guī Mǎn 媯滿 | b 12 NOV -1150 / d 4 MAR -1094 · other `6000000000111616776` È Fù 閼父: b ABT -1089 / d — |
| `6000000027291827257` Marcus Aemilius Lepidus | b -121 / d -77 · other `6000000027291865558` Paullus Aemilius: b -67 / d — |
| `6000000027291827257` Marcus Aemilius Lepidus | b -121 / d -77 · other `6000000027294681948` Cornelia: b -52 / d 16 |

### born-after-own-death — survives

| person | dates |
| --- | --- |
| `6000000013185679355` Li-Wah | b -1150 / d ABT -1200 |
| `6000000019331409868` BRIHADBAL | b ABT -1375 / d NOV -3067 |
| `6000000004868812861` Khakheperre Senusret II | b -1869 / d -1878 |
| `6000000011137018624` Nakhtnebtepnefer Intef III | b -2110 / d -2112 |
| `6000000004869093796` Raneb Kaiechos | b -2800 / d -2848 |
| `6000000019390579209` ANIRUDDHA | b ABT -2950 / d -3030 |
| `6000000009706826580` Pradyumna | b ABT -3015 / d -3030 |
| `6000000000437398754` Artaxias I I Unknown | b -42 / d -78 |

### lifespan-over-120 — survives

| person | dates |
| --- | --- |
| `6000000012691516920` Publius Licinius Crassus Dives Mucianus | b ABT -180 / d 130 |
| `6000000020682271048` Marcus Aemilius Lepidus | b -266 / d AFT 218 |
| `6000000008211577682` Demetrius | b -285 / d ABT 248 |
| `6000000001829634518` 大日本根子彦太瓊尊 | b -342 / d 27 MAR -215 |
| `6000000080574550752` Menander I of Bactria | b -350 / d -225 |
| `6000000006101234809` Perdiccas | b -355 / d 321 |
| `6000000001829735102` 日本足彦国押人尊 | b -427 / d 27 FEB -291 |
| `6000000001829687293` Emperor Suinin | b 26 JAN -69 / d 8 AUG 70 |

## What the check was reporting that it should not have been

Up to eight per rule, all of them dissolved by reading the modifier.

### born-after-parent-died — dissolves

| person | dates |
| --- | --- |
| `6000000003828382359` Decimus Junius Silanus | b ABT -105 / d ABT -60 · other `6000000003828399783` Marcus Junius Silanus: b — / d AFT -109 |
| `6000000002187604838` Pinedjem I Setepenre . | b ABT -1065 / d ABT -1032 · other `6000000006759042444` Piankh: b -1120 / d -1070 |
| `6000000002188187746` Adnan | b ABT -122 / d — · other `6000000004533752571` Udd Al-Qaydari: b -170 / d -128 |
| `6000000074176986109` Gaius Julius Caesar Strabo Vopiscus | b ABT -126 / d -87 · other `6000000000312008327` Lucius Julius Caesar: b -143 / d -129 |
| `6000000011816577338` Caecilia Metella | b -130 / d -50 · other `6000000003828196721` Lucius Caecilius Metellus Calvus: b ABT -160 / d AFT -139 |
| `6000000011816671316` Quintus Caecilius Metellus | b ABT -130 / d — · other `6000000003828196721` Lucius Caecilius Metellus Calvus: b ABT -160 / d AFT -139 |
| `6000000012690455112` Caecilia Metella Calva | b ABT -135 / d — · other `6000000003828196721` Lucius Caecilius Metellus Calvus: b ABT -160 / d AFT -139 |
| `6000000006856952085` Sextus Julius Caesar | b ABT -137 / d -90 · other `6000000005759156012` Gaius Julius Caesar: b ABT -163 / d -140 |

### parent-under-12 — dissolves

| person | dates |
| --- | --- |
| `6000000003828382561` Gaius Vipstanus Messalla Gallus | b ABT -10 / d AFT 60 · other `6000000003828382554` Lucius Vipstanus Gallus: b ABT -15 / d 17 |
| `6000000003645890657` Mutnodjmet | b -1050 / d — · other `6000000003223071336` Duathathor-Henuttawy: b ABT -1060 / d -992 |
| `6000000003323015123` Berenice | b BET -135 AND -130 / d -69 · other `6000000002415234643` Ptolemy: b -142 / d -81 |
| `6000000012767436560` Kiya | b BET -1393 AND -1341 / d -1330 · other `6000000002465068862` Tiye [Taia, Tiy and Tiyi]: b ABT -1398 / d ABT -1338 |
| `6000000018558311297` BRIHATKARMAN | b BEF -1407 / d -1384 · other `6000000009716047143` SUKSHATRA: b BEF -1415 / d -1407 |
| `6000000019129135495` Amihud ibn Shemaya | b ABT -159 / d — · other `6000000019081775951` Obadya Elida ibn Shemaya: b -167 / d ABT -90 |
| `6000000012692647383` Marcus Licinius Crassus Agelastus | b ABT -175 / d — · other `6000000012691516920` Publius Licinius Crassus Dives Mucianus: b ABT -180 / d 130 |
| `6000000012461596213` Al-Humaisi'a Al-Qaydari | b ABT -175 / d — · other `6000000007825346589` Salaman Al-Qaydari: b ABT -180 / d — |

### born-before-parent-born — dissolves

| person | dates |
| --- | --- |
| `6000000004089129056` Lepidus Aemilius | b -100 / d -39 · other `6000000000976947983` Lucius Æmilius Paullus: b BEF -29 / d 14 |
| `6000000016652352230` Menkheperre High Priest of Amun at Thebes . | b ABT -1065 / d ABT -992 · other `6000000003223071336` Duathathor-Henuttawy: b ABT -1060 / d -992 |
| `6000000006758798461` King Akheperre Psibkha’emne of Egypt, Pharaoh of Egypt | b ABT -1070 / d ABT -991 · other `6000000002187604838` Pinedjem I Setepenre .: b ABT -1065 / d ABT -1032 |
| `6000000006758798461` King Akheperre Psibkha’emne of Egypt, Pharaoh of Egypt | b ABT -1070 / d ABT -991 · other `6000000003223071336` Duathathor-Henuttawy: b ABT -1060 / d -992 |
| `6000000003645890234` Julius Polemon . | b ABT -11 / d 74 · other `6000000003828261173` Antonia Tryphaena: b -10 / d 55 |
| `6000000005757895476` Fulvia (or Crossutia) | b ABT -125 / d — · other `6000000002187600063` Sempronia Tuditana: b ABT -123 / d -63 |
| `6000000012396223564` Marcus Julius Lysimachus | b -14 / d 44 · other `6000000012396513433` Alexander Lysimachus: b ABT -10 / d 69 |
| `6000000074177759931` Quintus Lutatius Catulus | b ABT -149 / d -87 · other `6000000006859413853` Popillia: b -145 / d DEC -110 |

### born-after-own-death — dissolves

| person | dates |
| --- | --- |
| `6000000001442038829` JARĀSANDHA | b BEF -1760 / d -3083 |
| `6000000027287341110` C. Junius Junius Brutus Brutus | b ABT -330 / d AFT -470 |
| `6000000002416846052` Kunigunde von Henneberg | b 1180 / d BET 1170 AND 1200 |
| `6000000192641152821` Dutugamunu | b BEF 135 / d -137 |
| `6000000035154271885` Pedro Fernandes de | b BEF 1357 / d ABT 1258 |
| `6000000007991573586` Anders Nielsen Basse i Drøsselbjerg | b 1398 / d AFT 1382 |
| `6000000011603868214` Maria | b ABT 1550 / d ABT 1541 |
| `6000000176011692014` Katherin Coulton | b BEF 3 JUL 1609 / d 12 |

### lifespan-over-120 — dissolves

| person | dates |
| --- | --- |
| `6000000030651754449` 환 환 | b ABT 2 MAY -2370 / d ABT 15 MAR -2240 |
| `6000000000232618899` Beatrix | b ABT 1022 / d BEF 1180 |
| `6000000054755271849` NN | b ABT 1024 / d 1145 |
| `6000000004058612331` Ednyfed ab Iorwerth | b ABT 1080 / d 1201 |
| `6000000011092591917` Tiberius Claudius Bassus Capitolinus | b ABT 120 / d AFT 245 |
| `6000000028587495120` Khodja Kuncheck Tukatimur | b ABT 1270 / d AFT 1395 |
| `6000000048492110875` Martim | b BEF 1312 / d ABT 1435 |
| `6000000007428629223` Pangeran Undung / Sunan Ngudung / Sayyid Utsman Haji Rd. Santri | b BET 1385 AND 1443 / d 1524 |

