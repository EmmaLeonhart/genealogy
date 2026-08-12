# `NSFX`: what is in it, and whether Wikidata's labels keep it

`correspondence.md` marked this **TO ANALYSE** rather than guessing that the
field always holds a title. Censused from `reports/display-names.csv`; every
instance is a row in `reports/nsfx-census.csv`.

**36,072 of 444,874 `NAME` records carry an `NSFX`** (8.1%), holding **19,875 distinct values**.

`NSFX` appears inside the rendered display name in **35,995 of 36,072** (99.8%) — GEDCOM renders `NPFX GIVN /SPFX SURN/ NSFX`,
so this is the specification holding, measured rather than assumed.

## What is actually in the field — top 40 by frequency

| value | records |
| --- | ---: |
| `II` | 825 |
| `一` | 762 |
| `I` | 755 |
| `二` | 653 |
| `Jr.` | 460 |
| `III` | 437 |
| `三` | 416 |
| `Sr.` | 415 |
| `Graf` | 278 |
| `四` | 264 |
| `IV` | 196 |
| `五` | 179 |
| `Jr` | 121 |
| `Herzog` | 118 |
| `Prinz` | 118 |
| `六` | 114 |
| `Gräfin` | 114 |
| `Pharaoh of Egypt` | 107 |
| `Saint` | 104 |
| `Capitán` | 99 |
| `V` | 96 |
| `Sr` | 95 |
| `książę` | 94 |
| `七` | 83 |
| `Prinzessin` | 78 |
| `132, 91, 44, 9` | 66 |
| `Prince` | 64 |
| `d.y.` | 61 |
| `133, 92, 45, 10` | 57 |
| `144, 103, 56, 21` | 54 |
| `Queen of Egypt` | 53 |
| `VI` | 51 |
| `八` | 49 |
| `133, 93, 46, 9` | 46 |
| `Princess` | 44 |
| `Kunigaikštis` | 41 |
| `Count` | 40 |
| `145, 104, 57, 22` | 38 |
| `o Velho` | 37 |
| `131, 90, 43, 8` | 37 |

## By script

| script | records |
| --- | ---: |
| Latin | 30,653 |
| Han | 3,050 |
| Han+Latin | 982 |
| Latin+Masculine | 624 |
| Cyrillic | 324 |
| Cyrillic+Latin | 162 |
| Hebrew | 88 |
| Feminine+Latin | 67 |
| Latin+Modifier | 49 |
| Greek | 24 |

## Does Wikidata's own English label keep the suffix?

Emma's rule, 2026-08-11, is that the Latin display name becomes the `en` label
**with the suffix left in**, because a noble suffix is how the name is written
in English. This measures what Wikidata did for the people carrying both IDs.

Of the 5,700 `NSFX`-carrying records whose person has an English label:

| Wikidata's label | records | share |
| --- | ---: | ---: |
| keeps every suffix token | 536 | 9.4% |
| keeps part | 1,017 | 17.8% |
| keeps none | 4,147 | 72.8% |

### And "keeps none" is two different things

A label sharing no suffix token may have **dropped the suffix** from the same
name, or may be a **different name entirely** — the trap
`reports/display-names.md` already hit, where `Vittorio Emanuele … di Savoia`
against `Victor Emmanuel II of Italy` is not a stripped suffix at all. Splitting
the bucket by whether the name *without* its suffix survives into the label:

| | records | share of "keeps none" |
| --- | ---: | ---: |
| different name entirely | 1,959 | 47.2% |
| name partly shared | 1,544 | 37.2% |
| same name, suffix dropped | 615 | 14.8% |
| suffix was the whole name | 29 | 0.7% |

**This does not overturn the rule.** Wikidata's label is what Wikidata chose;
Emma's rule is about what *we* produce for people who have no label yet, and
`correspondence.md` already records that labels are only in scope for people
carrying both IDs and that Wikidata is definitive where it has one. What the
table sizes is how far the two conventions differ where both exist.

### Where Wikidata keeps none of the suffix

| geni | item | Geni display name | Wikidata `en` |
| --- | --- | --- | --- |
| `1354718` | Q168691 | Vittorio Emanuele Maria Alberto Eugenio Ferdinando Tommaso di Savoia re d'Italia e Sardegna | Victor Emmanuel II of Italy |
| `2430192` | Q182840 | Louis II | Louis the Stammerer |
| `2430192` | Q182840 | Louis II | Louis the Stammerer |
| `2430192` | Q182840 | Lodewijk II | Louis the Stammerer |
| `2430192` | Q182840 | Ludvig II | Louis the Stammerer |
| `284138677450001022` | Q6082487 | Nicolaus Iohannis Johansson Jr. | Nicolaus Johannis Rudbeckius |
| `284138677450001022` | Q6082487 | Nicolaus Johannis nuorempi | Nicolaus Johannis Rudbeckius |
| `284138677450001022` | Q6082487 | Nicolaus Johannis Johansson d.y. | Nicolaus Johannis Rudbeckius |
| `288390320120001964` | Q3301 | Charles "Martel" Mayor of the Palace | Charles Martel |
| `288390320120001964` | Q3301 | Karl "Martell" fränkischer Hausmeier | Charles Martel |
| `288390320120001964` | Q3301 | Charles "Martel" Duc des Austrasiens, Prince des Français | Charles Martel |
| `288390320120001964` | Q3301 | Carolus "Martellus" Maior domus | Charles Martel |

### Where Wikidata keeps part of it

| geni | item | Geni display name | Wikidata `en` |
| --- | --- | --- | --- |
| `1064102` | Q108743020 | Jean d'O Seigneur d'O & de Maillebois | Jean d'O, Seigneur d'O, Fresnes, Baillet, Maillebois, Franconville |
| `1077060` | Q108743022 | Robert VII dit Robin D'O Seigneur d'O & de Maillebois | Robert VII d'O, seigneur d'O et de Maillebois |
| `1354801` | Q434077 | Napoléon Joseph Charles Paul Bonaparte 3rd prince de Montfort | Prince Napoléon-Jérôme, Prince Napoléon |
| `2434385` | Q2121164 | Wolfert van Brederode heer van Cloetinge en Zwammerdam | Wolfert van Brederode |
| `298740371650007964` | Q1819709 | Leopold II of Habsburg 2nd Duke of of Austria | Leopold II, Duke of Austria |
| `299466839860007954` | Q793616 | Oscar Carl Wilhelm von Bernadotte Prins, Hertig av Västergötland | Prince Carl, Duke of Västergötland |
| `300340430900007929` | Q604419 | María Josefa Carmela Бурбон Infanta de España | Infanta Maria Josefa of Spain |
| `302107417920002914` | Q2720659 | Luigi Carlo Maria Giuseppe di Borbone delle Due Sicilie Conde de Áquila | Prince Louis, Count of Aquila |
| `304435320540004195` | Q57989 | Charles Louis Wittelsbach Elector of the Palatine, K.G. | Charles I Louis, Elector Palatine |
| `312473166720001563` | Q170398 | Wilhelm Friedrich Karl of Württemberg King of Württemberg | Wilhelm I of Württemberg |
| `312473166720001563` | Q170398 | Wilhelm Friedrich Karl von Württemberg König zu Württemberg | Wilhelm I of Württemberg |
| `312479826640001569` | Q168674 | Sophie Frederika Mathilde von Württemberg Queen consort of the Netherlands | Sophie of Württemberg |

### Where Wikidata keeps all of it

| geni | item | Geni display name | Wikidata `en` |
| --- | --- | --- | --- |
| `283896414940007239` | Q125472016 | John Sargent Jr. | John Sargent, Jr. |
| `294414873430006408` | Q1346964 | Lambert margrave of Tuscany | Lambert, Margrave of Tuscany |
| `331624398740011365` | Q104537663 | Levi Moss Sr. | Levi Moss, Sr. |
| `363886034950010574` | Q3228728 | Leszek Mazowiecki Duke of Masovia | Leszek, Duke of Masovia |
| `3825252` | Q112958671 | Samuel S. Terry Sr. | Samuel S. Terry, Sr. |
| `3996690188820126654` | Q84201 | Karl (Charles) Ludwig, Archduke Charles, of Austria-Teschen Archduke | Archduke Charles, Duke of Teschen |
| `3996789354360035440` | Q310807 | Albrecht Friedrich Rudolf Dominik Habsburg-Lothringen Duke of Teschen | Archduke Albrecht, Duke of Teschen |
| `4076230` | Q316398 | Håkon Härdabred Sigurdsson II | Haakon II of Norway |
| `4136631104320028008` | Q103783977 | Niels Iversen Rosenkrantz til Hevringholm | squire Niels Iversen|Ingvordsen til (Hevringholm) |
| `4136631104320028008` | Q103783977 | Niels Iversen Rosenkrantz til Hevringholm | squire Niels Iversen|Ingvordsen til (Hevringholm) |
| `4136631104320028008` | Q103783977 | Niels Iversen Rosenkrantz til Hevringholm | squire Niels Iversen|Ingvordsen til (Hevringholm) |
| `4181250114820035915` | Q310152 | Eric Jedvardsson of Sweden IX | Eric IX of Sweden |

