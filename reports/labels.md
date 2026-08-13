# Derived labels, and the catalogue behind them

Plan item 1. Emma, 2026-08-12: *"First thing is deriving labels from gedcom.
Something that's very easy."* And: *"Every individual needs an English,
Japanese, and Chinese label but really we gotta catalogue these things a bit
better too as a bulk operation."*

One row per person in `reports/derived-labels.csv` — **298,591 people**.

## What each person has to build a label from

| | people | share |
| --- | ---: | ---: |
| Latin only | 242,664 | 81.3% |
| CJK only — needs translation for en | 40,571 | 13.6% |
| mixed-script only — no clean Latin label | 6,773 | 2.3% |
| no usable name at all | 4,694 | 1.6% |
| Latin and CJK | 2,049 | 0.7% |
| other script only — needs translation for en | 1,840 | 0.6% |

**This is the catalogue.** The `en` and `mul` labels come from the Latin name,
so everyone in a *needs translation* row has no derivable English label at all —
that is the population Emma's *"if there's only a name present in some sort of
other script, we have to do a translation"* applies to, sized.

## Name records by script group

| script group | name records |
| --- | ---: |
| Latin | 296,936 |
| CJK | 101,481 |
| mixed | 25,715 |
| other | 12,779 |
| none | 276 |

Grouped by **script, never language** — her rule. `CJK` deliberately holds Han,
Hiragana, Katakana and Hangul together: **the Japanese/Chinese split is not
attempted here**, because Han characters are shared and a codepoint test would
mis-assign them. That split is what the cataloguing is *for*, and it needs a
decision rather than a rule.

## Aliases from married names — 47,125 people

Emma: *"Married name plugs into name to produce an alias."*

**Read as:** the married name takes the surname's place in the rendered name, so
`Judith /de France/` carrying `_MARNM Flandre` yields the alias `Judith Flandre`.
A `_MARNM` identical to `SURN` is ignored, per her earlier rule, which is 31% of
the 244,392 records carrying the tag.

**That reading is an interpretation of one sentence and is flagged rather than
settled.** The alternative — appending the married name to the full rendered
name — produces a different string, and nothing she has said chooses between
them.

## Against Wikidata, where both exist

8,457 people have both a derived Latin label and a Wikidata English
label. **1,554 match exactly (18.4%).**

`reports/display-names.md` has the breakdown of the rest: the failures
concentrate in royalty, where Geni holds the native birth name and Wikidata the
English regnal form, and a perfect oracle picking among a person's Latin names
reaches only 26.8%. Deriving the label is easy; the derived label disagreeing
with Wikidata's is the normal case, not the exception.

## Name corrections applied — 1

A Geni export is a snapshot: a profile renamed afterwards keeps its old name
in every GEDCOM already taken. `entity_resolution.md` records the current
name by hand, and it is applied **here, at derivation** — the exports stay
untouched as the record of what Geni actually said, and the superseded name
stays visible in `further_latin_names` rather than being erased.

| geni | corrected to |
| --- | --- |
| `6000000087535357291` | Emma Leonhart |

## Not done here

- **No Japanese/Chinese split.** Needs the catalogue above plus a decision.
- **No name items resolved.** They are *derived, never created* — and resolving
  a string to an existing item needs the download that has not run.
- **Nothing emitted to Wikidata.** This is ingestion.
