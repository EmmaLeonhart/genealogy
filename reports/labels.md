# Derived labels, and the catalogue behind them

Plan item 1, specified 2026-08-12: deriving labels from the GEDCOM is the
first thing and is easy. Every individual needs an English,
Japanese and Chinese label, and the material needs cataloguing a bit
better too as a bulk operation."*

One row per person in `reports/derived-labels.csv` — **1,575,997 people**.

## What each person has to build a label from

| | people | share |
| --- | ---: | ---: |
| Latin only | 1,477,776 | 93.8% |
| CJK only — needs translation for en | 45,878 | 2.9% |
| no usable name at all | 26,882 | 1.7% |
| other script only — needs translation for en | 12,603 | 0.8% |
| mixed-script only — no clean Latin label | 10,200 | 0.6% |
| Latin and CJK | 2,658 | 0.2% |

**This is the catalogue.** The `en` and `mul` labels come from the Latin name,
so everyone in a *needs translation* row has no derivable English label at all —
that is the population the translation rule applies to, sized: where only a
name in some other script is present, a translation is made.

## Name records by script group

| script group | name records |
| --- | ---: |
| Latin | 1,771,776 |
| CJK | 115,905 |
| other | 50,431 |
| mixed | 32,300 |
| none | 484 |

Grouped by **script, never language**, by rule. `CJK` deliberately holds Han,
Hiragana, Katakana and Hangul together: **the Japanese/Chinese split is not
attempted here**, because Han characters are shared and a codepoint test would
mis-assign them. That split is what the cataloguing is *for*, and it needs a
decision rather than a rule.

## Aliases from married names — 298,761 people

A married name plugs into the name to produce an alias.

**Read as:** the married name takes the surname's place in the rendered name, so
`Judith /de France/` carrying `_MARNM Flandre` yields the alias `Judith Flandre`.
A `_MARNM` identical to `SURN` is ignored, per the earlier rule, which is 31% of
the 244,392 records carrying the tag.

**That reading is an interpretation of one sentence and is flagged rather than
settled.** The alternative — appending the married name to the full rendered
name — produces a different string, and no ruling chooses between
them.

## Against Wikidata, where both exist

48,681 people have both a derived Latin label and a Wikidata English
label. **13,053 match exactly (26.8%).**

`reports/display-names.md` has the breakdown of the rest: the failures
concentrate in royalty, where Geni holds the native birth name and Wikidata the
English regnal form, and a perfect oracle picking among a person's Latin names
reaches only 26.8%. Deriving the label is easy; the derived label disagreeing
with Wikidata's is the normal case, not the exception.

## Name corrections applied — 2

A Geni export is a snapshot: a profile renamed afterwards keeps its old name
in every GEDCOM already taken. `reports/label-corrections.tsv` records the
name by hand, and it is applied **here, at derivation** — the exports stay
untouched as the record of what Geni actually said, and the superseded name
stays visible in `further_latin_names` rather than being erased.

| geni | corrected to |
| --- | --- |
| `6000000001902786893` | Mononobe no Futohime |
| `6000000059561790841` | Jacobus Bothniensis |

## Not done here

- **No Japanese/Chinese split.** Needs the catalogue above plus a decision.
- **No name items resolved.** They are *derived, never created* — and resolving
  a string to an existing item needs the download that has not run.
- **Nothing emitted to Wikidata.** This is ingestion.
