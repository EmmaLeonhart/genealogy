# The Geni → Wikidata field model

What every GEDCOM structure in the corpus is, how often it is filled, and what
it would become on Wikidata. Counts are from the 151-export merge: **298,591
people, 149,613 families**, every structure counted by its full tag path.

Nothing here is applied to anything. Mappings marked **decided** are Emma's;
mappings marked **open** need her.

## The point is adding, not correcting

Emma, 2026-08-10: *"the entire purpose of this is to add it… Correcting stuff on
Wikidata is actually such a pain that it's almost effectively out of the
question. We will be more prone to adding in contradictory information cited to
Geni than we are to correcting information."*

So the number that matters is not where the two sides disagree, it is where Geni
has a value and **Wikidata is silent**. Measured over the 14,157 people carrying
both IDs:

| Geni field | → Wikidata | Geni has | Wikidata also has | **addable** |
| --- | --- | ---: | ---: | ---: |
| `NAME/GIVN` | `P735` | 14,118 | 6,903 | **7,215** |
| `NAME/SURN` | `P734` | 11,777 | 7,300 | **4,477** |
| `BIRT` place | `P19` | 6,667 | 3,165 | **3,502** |
| `DEAT` place | `P20` | 6,118 | 3,381 | **2,737** |
| `BIRT/DATE` | `P569` | 8,850 | 7,131 | **1,719** |
| `BURI` place | `P119` | 3,272 | 1,712 | **1,560** |
| `OCCU` | `P106` | 4,024 | 2,763 | **1,261** |
| `DEAT/DATE` | `P570` | 11,174 | 9,926 | **1,248** |
| `TITL` | `P97` | 1,524 | 599 | **925** |
| `BAPM/DATE` | `P1636` | 324 | 12 | **312** |
| `SEX` | `P21` | 14,155 | 14,154 | **1** |
| | | | **total** | **24,957** |

**~25,000 addable statements from 14,157 people**, against 930 conflicts. The
additive population is twenty-seven times the contradictory one, which is the
proportion this project should work in.

`P21` is already saturated — one person in 14,157 lacks a sex statement. Name
components are the largest gap by a wide margin, which is why
`reports/names-spec.md` exists.

Labels, same population:

| label | present | missing |
| --- | ---: | ---: |
| English | 13,656 (96.5%) | **501** |
| Japanese | 3,996 (28.2%) | **10,161** |
| `mul` | 2,206 (15.6%) | **11,951** |

## Identity

| Geni | filled | of people | → Wikidata | status |
| --- | ---: | ---: | --- | --- |
| `INDI/RFN` (`geni:…`) | 298,591 | **100%** | `P2600` | the join key, already used |
| `INDI/SEX` | 298,130 | **99.8%** | `P21` sex or gender | open |
| `INDI/NAME` | 444,874 | 1.49 each | label / alias | **decided** — Wikidata is authoritative for labels; only touch people carrying both IDs |
| `INDI/NAME/GIVN` | 352,545 | 118% | `P735` given name | open |
| `INDI/NAME/_MARNM` | 244,392 | 82% | married name | open — non-standard tag |
| `INDI/NAME/SURN` | 219,117 | 73% | `P734` family name | open |
| `INDI/NAME/NICK` | 66,926 | 22% | alias | open |
| `INDI/NAME/NSFX` | 36,072 | 12% | title/suffix, or `P97` | open |
| `INDI/TITL` | 9,277 | 3% | `P97` noble title | open |

`SEX` at 99.8% and `RFN` at 100% are the only near-universal fields. Everything
else below is a minority of the tree, which bounds what any batch can assert.

## Events

| Geni | filled | of people | → Wikidata |
| --- | ---: | ---: | --- |
| `INDI/BIRT` | 159,913 | 54% | |
| `INDI/BIRT/DATE` | 150,229 | **50%** | `P569` date of birth |
| `INDI/DEAT` | 131,084 | 44% | |
| `INDI/DEAT/DATE` | 118,950 | **40%** | `P570` date of death |
| `INDI/OCCU` | 128,703 | 43% | `P106` occupation |
| `INDI/BURI` | 25,614 | 9% | `P119` place of burial |
| `INDI/BURI/DATE` | 11,921 | 4% | — Wikidata has no burial *date* property in common use |
| `INDI/BAPM` | 9,358 | 3% | |
| `INDI/BAPM/DATE` | 9,097 | 3% | `P1636` date of baptism |
| `INDI/OCCU/DATE` | 2,887 | 1% | `P106` qualified with `P580`/`P582` |

**Half the tree has a birth date and two fifths a death date.** That is the
ceiling on any date-based work.

## Places — the structured block is the main one, not the string

**This corrects an earlier note in `queue.md` drawn from a single record.** Geni
does not primarily store places as comma-strings. It stores them **twice**, and
the structured form is about twice as well filled:

| event | `PLAC` (free text) | `ADDR` (structured) | ratio |
| --- | ---: | ---: | ---: |
| birth | 58,562 | **112,887** | 1.9× |
| death | 38,990 | **78,876** | 2.0× |
| burial | 16,360 | **23,728** | 1.5× |
| marriage | 10,779 | **21,415** | 2.0× |

And `ADDR` decomposes, with completeness falling as it narrows:

| birth address part | filled |
| --- | ---: |
| `CTRY` country | 66,750 |
| `STAE` state/region | 59,847 |
| `CITY` city | 47,054 |
| `POST` postcode | 1,827 |
| `ADR1` street | 899 (burial only) |

So place resolution should start from `ADDR/CTRY` + `STAE` + `CITY` — three
comparable tokens — rather than from parsing `PLAC`. The `PLAC` string is the
fallback, and it is the field that carries prose: Eleanor of Aquitaine's reads
`Nieul-sur-Autize, Vendée or Château de Belin, Guyenne or Palais d'Ombrière,
Bordeaux`, three candidates joined by "or".

**Places are not resolvable offline.** The download walked people, so no place
item is in the store — `Q5933` Westminster Abbey, `Q29265` Canterbury Cathedral
and every other are absent. Resolution needs `scripts/fetch-labels.py`, one
batched query.

## Families

| Geni | filled | → Wikidata |
| --- | ---: | --- |
| `FAM/CHIL` | 267,517 | `P40` child, and `P22`/`P25` from the child's side |
| `FAM/HUSB` | 126,894 | `P26` spouse |
| `FAM/WIFE` | 89,543 | `P26` spouse |
| `FAM/MARR` | 36,314 | the `P26` statement itself |
| `FAM/MARR/DATE` | 36,275 | `P26` qualifier `P580` start time |
| `FAM/MARR/ADDR` | 21,415 | `P26` qualifier `P2842` place of marriage |
| `FAM/MARR/PLAC` | 10,779 | as above, fallback |

**`HUSB` outnumbers `WIFE` by 37,351.** Half of all families (74,773) name only
one spouse, and 22,513 name one spouse with no children and no marriage event.
Emma's reading: relationships Geni knows whose partner was not in the export's
scope.

**Marriage data with no spouse cannot be represented.** 16,229 of the 36,275
dated marriages name no spouse at all. `P580` and `P2842` are qualifiers on
`P26`, so with no spouse there is no statement to hang them on. Emma: *"These
aren't anything meaningful because they can't be represented on wikidata."*

## Provenance, and what is mostly volume

| Geni | count | note |
| --- | ---: | --- |
| `INDI/NOTE/CONT` | **1,820,267** | continuation lines — the bulk of the corpus by volume |
| `INDI/NOTE/CONC` | 556,214 | |
| `INDI/SOUR/DATA/TEXT` | 506,960 | which field the source is claimed to support |
| `INDI/SOUR` | 253,480 | **decided** — collect, do not trust |
| `INDI/OBJE` | 204,356 | image attachments |
| `INDI/CHAN/DATE` | 298,591 | Geni's last-modified stamp, one per person |

`SOUR/DATA/TEXT` names the field a citation claims to support — "Date of Birth",
"First Name". Henry III's cites his *son's* Find A Grave memorial for two of
them, which is why these are collected and not trusted.

Notes are 2.4M lines and are **not** the current job: useful only where they
disambiguate a structured field. Nine of Henry III's 149 notes are pasted
articles; the other 130 are short and carry real citations.

## What this model does not yet cover

- **`_MARNM`** at 82% is non-standard and undefined here. It is the second most
  filled name subtag and nothing says what it means in Geni's export.
- **Language.** Zero `LANG` subtags corpus-wide. Names in four scripts with
  nothing marking which is which. Parked by Emma.
- **`BURI/DATE`** at 11,921 has no obvious Wikidata target.
- **Ranked statements.** Wikidata expresses uncertainty with multiple values and
  ranks — `Q3056729` carries three `P569`s, one deprecated with `P1319`/`P1326`
  bounds. Geni expresses it as prose inside a single field. No mapping decided.
