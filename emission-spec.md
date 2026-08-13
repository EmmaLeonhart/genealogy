# What we emit to Wikidata

**Every row here comes from something Emma said in this project.** This is the
list of what the pipeline is *for*; `reports/` holds the derived data, and the
"emitter" column says whether anything can currently write it.

It exists because that question was asked and could not be answered from the
repo: the code emits six properties, the plan names far more, and nothing wrote
the difference down.

**Nothing is emitted automatically.** Batches are generated for review.

---

## 1. Labels and aliases

Emma, 2026-08-12: *"Every individual needs an English, Japanese, and Chinese
label."* And: *"the multi-language label comes from the Latin alphabet name, and
the English language label will come from it too."*

| target | source | derived | emitter |
| --- | --- | --- | --- |
| `mul` label | the Latin-alphabet display name, suffix included | `derived-labels.csv` · `label_mul` · 244,713 | **none** |
| `en` label | same string as `mul` | `derived-labels.csv` · `label_en` · 244,713 | **none** |
| `ja` label | the Han/kanji name **as written** | `derived-labels.csv` · `cjk_names` · 42,620 | **none** |
| `zh` label | **the same string as `ja`** | same | **none** |
| aliases | the married name substituted into the name | `derived-labels.csv` · `aliases_from_married_name` · 47,125 | **none** |

**Han-only names need no ja/zh decision.** Emma: *"If the name is solely in
kanji, then the Chinese and Japanese labels are both the same for it."* Only a
name carrying **kana** would need translating into Chinese — 291 people.

**A Geni name is not a label.** It is a language-agnostic string. Converting
agnostic forms into labels is the pipeline Emma described as still needed, and
`reports/geni-names.md` is the measurement it has to be built against.

**Other languages later** — *"possibly going to be wanting you to do this for
other languages that are some of the most commonly used ones on wikidata, like
Russian."*

## 2. Name items

*"We derive name items but never create name items"* — then, on 2026-08-12:
*"I'm open to the creation of name objects … we probably are going to be
creating name objects."*

| target | source | derived | emitter |
| --- | --- | --- | --- |
| `P735` given name | `GIVN` tokens → existing name item | `reports/name-resolution.csv` · 30.7% of occurrences resolve | `namelinks.py`, blocked on resolution |
| `P734` family name | `SURN` → existing name item | same · 27.3% resolve | `namelinks.py`, blocked |
| `P1545` series ordinal | position of the given name | — | `namelinks.py` |
| **new name items** | names with no existing item | `reports/name-items-to-create.csv` · 128,668 candidates | **none** |

The 128,668 is an upper bound contaminated three ways — names that exist but are
unreferenced, places misfiled as surnames, abbreviations misfiled as names.

## 3. Identity and structure

| target | source | derived | emitter |
| --- | --- | --- | --- |
| `P31` = `Q5` human | every person | — | on creation only |
| `P21` sex or gender | `SEX` | `derived-facts.csv` · **298,130** | **none** |
| `P2600` Geni profile ID | the xref | every person | `quickstatements.py` |

**`P21` is the largest unwired gap** — 99.8% coverage, the best-covered field in
the corpus, and nothing writes it.

## 4. Family links

*"Mother father spouse and child is easier."*

| target | source | derived | emitter |
| --- | --- | --- | --- |
| `P22` father | `FAM` `HUSB` | `derived-family.csv` · 231,472 | `crosscheck.py` |
| `P25` mother | `FAM` `WIFE` | 178,656 | `crosscheck.py` |
| `P26` spouse | `FAM` `HUSB`+`WIFE` | 125,890 | `crosscheck.py` |
| `P40` child | `FAM` `CHIL` | 138,511 | **none** |
| `P3373` sibling | — | **deliberately not emitted** | — |

**No `P3373`.** Emma routes siblings through invented parents instead, which is
Wikidata's preferred shape.

**Invented parents.** *"Sibling relationships without parents need to get two
parents that are 'father of x and y' and 'mother of x and y' and geni linked if
possible."* 250 families, 500 placeholders — `reports/invented-parents.csv`.
Confirmed 2026-08-12 as the **no-parent case only**; the 40,884 single-parent
families get nothing.

## 5. Life events

*"Birthplace birth date death date death place burial date burial place all can
be done with string."*

| target | source | derived | emitter |
| --- | --- | --- | --- |
| `P569` date of birth | `BIRT` `DATE` | `derived-facts.csv` · 150,203 | `crosscheck.py` |
| `P570` date of death | `DEAT` `DATE` | 118,918 | `crosscheck.py` |
| `P4602` date of burial | `BURI` `DATE` | 11,907 | **none** |
| `P19` place of birth | `BIRT` `PLAC` → item | 58,562 strings | **none** — unresolved |
| `P20` place of death | `DEAT` `PLAC` → item | 38,990 strings | **none** — unresolved |
| `P119` place of burial | `BURI` `PLAC` → item | 16,360 strings | **none** — unresolved |
| `P6375` street address | `ADDR` block, monolingual text | 71,735 birth · 51,681 death · 16,328 burial | **none** |
| `P106` occupation | `OCCU` → item | 31,401 strings | **none** — unresolved |

**Burial is two properties, never qualifiers** — Emma: *"the date of burial and
the place of burial have their own properties."*

**Addresses stay text.** *"Do addresses with the address property (multilingual
text)."* That is why `P6375` needs no resolution while `P19` does.

**Dates carry their full grammar** — `raw, iso, precision, year, month, day,
year_end, modifier`. 56,193 `about`, 6,828 `after`, 4,013 `before`, 2,134
`between` ranges with both ends.

| GEDCOM modifier | Wikidata |
| --- | --- |
| `ABT` / `EST` / `CAL` | `P1480` sourcing circumstances = `Q5727902` circa |
| `BEF` | `P1326` latest date |
| `AFT` | `P1319` earliest date |
| `BET x AND y` | `P1319` + `P1326` |

## 6. Marriage

*"Marriage date and place and end and whatever will be easy-ish."* These are
**qualifiers on `P26`**, not standalone claims — which is why no current emitter
can write them; `build_claim_batch` writes bare claims only.

| target | source | derived | emitter |
| --- | --- | --- | --- |
| `P580` start time | `FAM` `MARR` `DATE` | `derived-marriages.csv` · 36,257 | **none** |
| `P2842` place of marriage | `FAM` `MARR` `PLAC` | 10,779 strings | **none** — unresolved |
| `P582` end time | `FAM` `DIV` `DATE` | 323 | **none** |
| `P1545` series ordinal | derived from dates | — | **none** |

**"End" is divorce and only divorce** — 483 families. Geni has no way to express
a marriage ending at a death, which Wikidata records on `P582` far more often.
This is the one field where Wikidata has more than we do.

## 7. Creating people

Emma, 2026-08-12: *"we are explicitly creating new people. There was no doubt
about that."*

262,587 of our people have no Wikidata item. A created person carries `P31` =
`Q5`, labels, `P21`, `P2600`, and their relationship links.

Her sketch of the eventual pipeline: *"a series of edits that it could possibly
do, and it'll do like a hundred random minutes every day"* — creating and linking
an individual with all its properties; adding a single thing; adding a property
to an individual. Created individuals may gain properties gradually over time.

## 8. Conflicts

*"You add the date as a conflicting fact on Wikidata cited to Geni, citations to
Geni use the reference thing (not a qualifier) and the property Geni ID and the
id."*

    <property> = <Geni's value>
        reference:  P2600 = <the Geni profile ID>

A **reference**, not a qualifier. The existing statement is left alone. This is
the general mechanism for every disagreement, not a date rule.

---

## What blocks each unwired row

| blocker | affects |
| --- | --- |
| **no emitter written** | `P21`, `P40`, `P4602`, `P6375`, labels, aliases |
| **string → item resolution missing** | `P19`, `P20`, `P119`, `P106`, `P2842` |
| **name → item resolution partial** | `P735`, `P734` — 30.7% / 27.3% |
| **qualifiers unsupported** | `P580`, `P582`, `P2842`, `P1545`, and every date modifier |
| **item creation unbuilt** | new people, new name items |

**Six properties emit today** — `P22`, `P25`, `P26`, `P569`, `P570` via
`crosscheck`, and `P2600` via `quickstatements`. Everything else in this document
is derived and unwired, or blocked on one of the five rows above.
