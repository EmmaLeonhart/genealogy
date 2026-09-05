# The names on Emma's items, audited against our tree

**Her instruction, 2026-08-28**, the last one before the crash: *"All the individuals that I've
worked on and any individuals that they've been merged into should basically always be all the
individuals that I've worked on, pretty much all of them. All the people that they've been merged
into should have audits done on their names to figure out the degree that we've messed them up."*

`scripts/audit-ledger-names.py` · `reports/name-audit.csv` · run 2026-08-29, **508 items fetched
live** with `full_entities`, one row per item per language, **1,657 rows**.

## The answer to "how badly did we mess them up": barely at all

| state | rows | |
| --- | ---: | --- |
| `match` | 640 | Wikidata and our tree agree |
| `absent_on_wikidata` | 578 | the item has no label in that language and we can supply one |
| `differs` | 256 | |
| `we_have_none` | 183 | Wikidata has a label, our tree has nothing |

**Of the 256 differences, only 14 are ours to fix.** Those are the ones where the live label is a
string our own tree records as an *alias* — the birth name, left behind by the 2026-08-29 flip that
made the married form primary. `_label_corrections()` in `build-garborg-day.py` already fires on
exactly that condition and nothing else, so the guard was right and the population is small.

**The other 242 must not be touched, and reading them is what shows why.** Wikidata is frequently
*better* than what we would write:

| item | Wikidata | ours |
| --- | --- | --- |
| `Q101247444` | `Ingegerd Svantepolksdotter of Viby, heiress, lady of Händelöö` | `Ingegerd Svantepolksdotter` |
| `Q109266155` | `Magdalena Bureus` | `Magdalena Johansdotter Bure` |
| `Q1168365` | `Samuel Troilius` | `Samuel Olofsson Troilius` |
| `Q11858191` | `Erik af Palén` | `Erik Johan Abrahamsson af Palén` |
| `Q12598947` | `Buyeo Taebi` | `Taebi Buyeo` |

A disambiguator we would strip; a Latinised form she chose; a patronymic Wikidata omits by
convention; and — `Q12598947` — **her own word ordering**, set by hand.
`CLAUDE.md` § *The purpose is to ADD to Wikidata, not to correct it* governs all of them, and it
names the Ingegerd case specifically as the thing not to do.

`Q116150299` *Jon Reimatsen* against our *Jon Reinmodsen* is the one shape that is neither: a plain
spelling disagreement between Geni and Wikidata. It is a **note, not a work item** — the same
ruling as every other conflict.

## Where the actual work is, and it is additive

**575 labels are simply missing** — `ja` 229, `zh` 230, `mul` 116 — on items that already exist.
These became derivable only when the transliteration table went 218 → 3,261 tokens on 2026-08-29,
so they are not damage; they are new reach. They go out through the daily batch at her cap of **15
label edits a batch**, tracked in `reports/label-edits-emitted.tsv`, which is roughly 38 batches.

## What the audit cannot see

**102 of the 508 ledger items are not in our tree at all** — they appear in
`reports/garborg-qids.tsv` but not in `reports/derived-labels.csv`, which is why `we_have_none` is
102 in `en`. Those are people she made items for whom no export has reached: Bureätten members and
the medieval end of the spine. Nothing can be said about their labels from here, and an export is
the only thing that would change that.

**No item had been merged away.** `redirected items: 0` — `wbgetentities` returns the target for a
redirected QID, so this was checked rather than assumed, and the second half of her instruction —
*"any individuals that they've been merged into"* — currently has no members.
