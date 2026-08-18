# What Wikidata does with a middle initial, by language

Emma asked for evidence rather than an assertion — *"I want evidence of it being standard"* — and then for the question to be asked per language: *"I'm guessing Russian and Greek do it with transliterating the initial though and they should do that. Idk what Hindi does but do the standard for it too."*

**19,250 items** in the local store have an English label of the form `Given X Surname`, after excluding 2,264 regnal ordinals such as `Henry I of England`. **6,378** of them carry a label in at least one of the languages below.

**This is the local store, not all of Wikidata.** It is a Geni-shaped slice of roughly 1.4 million items seeded from `P2600` holders and their neighbours, so the claim is about the items we hold, and a different slice could differ.

`latin_initial` keeps the letter as itself (ジョセフ・C・オマホニー). `script_initial` renders it as one letter of the target script (Джозеф С. О'Махони) — this is what *transliterating the initial* means. `expanded` replaces it with the full middle name Wikidata knows and we do not (`Samuel S. Cox` → サミュエル・サリヴァン・コックス). **`expanded` is not an option available to us**: if we knew the name it would not be an initial.

| lang | labelled | `latin_initial` | `script_initial` | `expanded` | `dropped` | `unclear` | commonest |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `ja` | 2,744 | 1,501 (55%) | 7 (0%) | 269 (10%) | 967 (35%) | 0 (0%) | **latin_initial** |
| `zh` | 2,188 | 955 (44%) | 63 (3%) | 291 (13%) | 879 (40%) | 0 (0%) | **latin_initial** |
| `ko` | 1,404 | 985 (70%) | 190 (14%) | 56 (4%) | 173 (12%) | 0 (0%) | **latin_initial** |
| `ru` | 2,177 | 231 (11%) | 314 (14%) | 771 (35%) | 861 (40%) | 0 (0%) | **dropped** |
| `el` | 534 | 1 (0%) | 204 (38%) | 184 (34%) | 145 (27%) | 0 (0%) | **script_initial** |
| `hi` | 107 | 0 (0%) | 14 (13%) | 78 (73%) | 15 (14%) | 0 (0%) | **expanded** |
| `uk` | 796 | 118 (15%) | 98 (12%) | 232 (29%) | 348 (44%) | 0 (0%) | **dropped** |
| `bg` | 452 | 158 (35%) | 31 (7%) | 39 (9%) | 224 (50%) | 0 (0%) | **dropped** |
| `sr` | 243 | 62 (26%) | 85 (35%) | 24 (10%) | 72 (30%) | 0 (0%) | **script_initial** |
| `he` | 2,376 | 0 (0%) | 539 (23%) | 430 (18%) | 1,407 (59%) | 0 (0%) | **dropped** |
| `ar` | 3,818 | 0 (0%) | 2,182 (57%) | 1,039 (27%) | 597 (16%) | 0 (0%) | **script_initial** |
| `fa` | 2,550 | 1 (0%) | 1,817 (71%) | 421 (17%) | 311 (12%) | 0 (0%) | **script_initial** |
| `ta` | 98 | 0 (0%) | 4 (4%) | 59 (60%) | 35 (36%) | 0 (0%) | **expanded** |

## Excluding Roman-numeral initials

`I V X L C D M` are valid middle initials **and** the letters every regnal ordinal is made of, and `Nicolaus I Bernoulli` has no particle to give it away. These are the same figures over initials that cannot be an ordinal at all, and they are the safer read.

| lang | labelled | `latin_initial` | `script_initial` | `expanded` | `dropped` | `unclear` | commonest |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `ja` | 1,905 | 1,103 (58%) | 3 (0%) | 201 (11%) | 598 (31%) | 0 (0%) | **latin_initial** |
| `zh` | 1,536 | 704 (46%) | 49 (3%) | 232 (15%) | 551 (36%) | 0 (0%) | **latin_initial** |
| `ko` | 1,001 | 735 (73%) | 133 (13%) | 20 (2%) | 113 (11%) | 0 (0%) | **latin_initial** |
| `ru` | 1,416 | 5 (0%) | 232 (16%) | 555 (39%) | 624 (44%) | 0 (0%) | **dropped** |
| `el` | 283 | 0 (0%) | 141 (50%) | 44 (16%) | 98 (35%) | 0 (0%) | **script_initial** |
| `hi` | 79 | 0 (0%) | 8 (10%) | 61 (77%) | 10 (13%) | 0 (0%) | **expanded** |
| `uk` | 479 | 0 (0%) | 62 (13%) | 176 (37%) | 241 (50%) | 0 (0%) | **dropped** |
| `bg` | 209 | 0 (0%) | 24 (11%) | 27 (13%) | 158 (76%) | 0 (0%) | **dropped** |
| `sr` | 137 | 3 (2%) | 65 (47%) | 21 (15%) | 48 (35%) | 0 (0%) | **script_initial** |
| `he` | 1,712 | 0 (0%) | 389 (23%) | 314 (18%) | 1,009 (59%) | 0 (0%) | **dropped** |
| `ar` | 2,794 | 0 (0%) | 1,510 (54%) | 849 (30%) | 435 (16%) | 0 (0%) | **script_initial** |
| `fa` | 1,852 | 1 (0%) | 1,301 (70%) | 341 (18%) | 209 (11%) | 0 (0%) | **script_initial** |
| `ta` | 63 | 0 (0%) | 4 (6%) | 38 (60%) | 21 (33%) | 0 (0%) | **expanded** |

## Examples

### `ja`

| English | label | verdict |
| --- | --- | --- |
| Joseph C. O'Mahoney | ジョセフ・C・オマホニー | `latin_initial` |
| Robert J. Van de Graaff | ロバート・ジェミソン・ヴァン・デ・グラフ | `script_initial` |
| Samuel S. Cox | サミュエル・サリヴァン・コックス | `expanded` |
| Paul D. Boyer | ポール・ボイヤー | `dropped` |

### `zh`

| English | label | verdict |
| --- | --- | --- |
| Joseph C. O'Mahoney | 約瑟夫·C·奧馬孔利 | `latin_initial` |
| Robert O. Perrin | 罗伯特·奥·佩兰 | `script_initial` |
| Charles F. Curry | 查尔斯·福雷斯特·库里 | `expanded` |
| Paul D. Boyer | 保罗·博耶 | `dropped` |

### `ko`

| English | label | verdict |
| --- | --- | --- |
| Joseph C. O'Mahoney | 조지프 C. 오머호니 | `latin_initial` |
| Paul D. Boyer | 폴 D. 보이어 | `script_initial` |
| Alan J. Heeger | 앨런 제이 히거 | `expanded` |
| Thomas J. Sargent | 토머스 사전트 | `dropped` |

### `ru`

| English | label | verdict |
| --- | --- | --- |
| Obizzo I d’Este | Обиццо I д’Эсте | `latin_initial` |
| Mary L Williams | Мэри Л. Уильямс | `script_initial` |
| Alphons J. van der Grinten | Ван дер Гринтен, Альфонс | `expanded` |
| Joseph C. O'Mahoney | Джозеф О’Мэйони | `dropped` |

### `el`

| English | label | verdict |
| --- | --- | --- |
| Henry M. Montrésor | Henry M. Montrésor | `latin_initial` |
| Daniel L. Burrows | Ντάνιελ Λ. Μπάροους | `script_initial` |
| Obizzo I d’Este | Ομπίτσο Α΄ των Έστε | `expanded` |
| Audrey J. Walton | Όντρεϊ Γουόλτον | `dropped` |

### `hi`

| English | label | verdict |
| --- | --- | --- |
| Christopher A. Sims | क्रिस्टोफर ए॰ सिम्स | `script_initial` |
| Thomas J. Sargent | थॉमस जॉन सार्जेंट | `expanded` |
| Douglas L. Coleman | डगलस कोलमैन | `dropped` |

### `uk`

| English | label | verdict |
| --- | --- | --- |
| Obizzo I d’Este | Обіццо I д'Есте | `latin_initial` |
| Polly L. Herring (Reed) | Поллі Л.  Геррінґ (Рід) | `script_initial` |
| James A. Lindsay | Джеймс Ліндсей (конспіролог) | `expanded` |
| Paul D. Boyer | Пол Бойєр | `dropped` |

### `bg`

| English | label | verdict |
| --- | --- | --- |
| Obizzo I d’Este | Обицо I д’Есте | `latin_initial` |
| George B. Selden | Джордж Б. Селдън | `script_initial` |
| Christopher A. Sims | Кристофър Албърт Симс | `expanded` |
| Paul D. Boyer | Пол Бойер | `dropped` |

### `sr`

| English | label | verdict |
| --- | --- | --- |
| Ptolemy I Soter | Птолемеј I Сотер | `latin_initial` |
| Vladislav F. Ribnikar | Владислав Ф. Рибникар | `script_initial` |
| Robert W. Holley | Robert V. Holi | `expanded` |
| Harry S. Truman | Хари Труман | `dropped` |

### `he`

| English | label | verdict |
| --- | --- | --- |
| George T. Biden | ג'ורג' ט. ביידן | `script_initial` |
| James A. Lindsay | ג'יימס א' לינדזי | `expanded` |
| Joseph C. O'Mahoney | ג'וזף או'מאהוני | `dropped` |

### `ar`

| English | label | verdict |
| --- | --- | --- |
| Richard G. Salomon | ريتشارد جي. زالومون | `script_initial` |
| Burr W. Jones | بور دبليو. جونز | `expanded` |
| Paul D. Boyer | بول بوير | `dropped` |

### `fa`

| English | label | verdict |
| --- | --- | --- |
| William T. Blodgett | William T. Blodgett | `latin_initial` |
| Joseph C. O'Mahoney | جوزف سی. اوماهونی | `script_initial` |
| John N. Heiskell | جان ندرلند هیسکل | `expanded` |
| Paul D. Boyer | پل بویر | `dropped` |

### `ta`

| English | label | verdict |
| --- | --- | --- |
| Robert A. Heinlein | ராபர்ட் ஏ. ஐன்லைன் | `script_initial` |
| Alan J. Heeger | ஆலன் ஜெய் ஈகர் | `expanded` |
| James K. Polk | ஜேம்ஸ் போக் | `dropped` |
