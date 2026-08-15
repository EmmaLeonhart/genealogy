# Possible future modelling

**Everything this project has decided *not* to model, with why, and what would
unblock it.** Created 2026-08-14 at Emma's request, alongside the batches that
*are* being generated, so that a decision to defer is recorded rather than
becoming a silent gap.

A thing belongs here when it was looked at and set aside. A thing that was never
considered does not belong here — that is what `todo.md` is for.

---

## order.life properties not mapped

Full survey in `reports/orderlife-properties.md`. These are the ones deliberately
left out of `scripts/build-orderlife-batch.py`.

| property | decision | what would unblock it |
| --- | --- | --- |
| **P59 Cladoplast of** | **Not mapped, not emitted, no item created.** Emma, 2026-08-14: *"we don't do anything with it until there is a Cladoplast object on Wikidata, which there currently is not. I do not have any intention of making it right now."* | a Cladoplast item existing on Wikidata — and that is her call to make, not something to propose |
| **P12 Occupation** (monolingual text) | **Dropped.** *"The only monolingual text that we just don't do is the P12 and P13 occupation and residence."* | a decision to reverse it; the technical blocker would be normalising free text to `P106` items |
| **P13 Residence** (monolingual text) | **Dropped**, same instruction | as above, target would be `P551` |
| P49 ordinal within year, P50 ordinal within month, P51 ISO week number, P52 ISO weekday number | Not mapped — this is `calendar-lib`, not genealogy | nothing; there is no Wikidata target and no reason to invent one |
| P41 GEDCOM REFN, P40 Reference number | Not mapped — GEDCOM import plumbing, meaningless off-wiki | nothing |
| P5 Gedcom Full Name | Not mapped as a claim; it is the raw `Given /Surname/` string | it feeds labels instead |
| P7 Birth date, P8 Death date (both *deprecated*, monolingual **text**) | Not mapped — superseded inside order.life by P56/P57, which are proper `time` and *are* mapped | nothing |
| P15 Notes page, P45 Described at url, P46 notes page, P54 suffix, P65 Blazon | Not mapped — local editorial fields | a case-by-case decision if any turns out to carry sourcing |
| **P39 instance of** | Recorded as the Gaiad flag, **never emitted** | nothing; it is a classifier, not a statement |

**Address is the monolingual-text property that IS done** — `P6375 street
address`, per `CLAUDE.md` § Life events. P12 and P13 are the exceptions, not the
rule.

## Gaiad characters

**Undecided, and deliberately so.** Wikidata does carry genealogies of fictional
characters, so there is a real target; how these should be modelled has not been
worked out.

What is settled: they are **flagged, not excluded**, and every entry carries
`"gaiad": true`/`false`.

What is *not* settled, and is the blocker: **the flag marks essentially
everything.** `Q153802` is on 105,720 of 106,908 order.life persons and on 400 of
400 sampled people who also carry a Wikidata QID — real historical people. The
epic runs through the whole genealogy rather than beside it. So there is
currently **no way to separate the epic from the genealogy**, and any modelling
decision needs that discriminator first.

Tiering therefore uses identifiers instead: a person with neither a Geni ID nor a
Wikidata QID is order.life-only, and goes last.

## The `P155`-and-above external identifiers

**Not deferred on purpose — simply not built yet, and it is the easiest
remaining win.** Fifty-nine order.life properties from P155 up are mirrored from
Wikidata with the same numbers and meanings, almost all `external-id`: Rodovid,
FamilySearch, WikiTree, Roglo, Geneanet, The Peerage, JewAge, DAR/SAR, Find a
Grave, and a large Swedish cluster.

These are identifiers Wikidata has properties for and frequently lacks values
for, on items that already exist. No creation, no ambiguity, no normalisation.

## The Samaritan priestly office

**`Samaritan High Priest` is currently an item *description* and nothing else.**
`reports/wikidata-samaritan-priests.json` emits no `P106` and no position
property for the 78 pre-1624 priests.

Two reasons it is unresolved:

1. **The office must never become `P734`.** It sits in the GEDCOM surname slot,
   which is an office in a name field — the `SURN 秦州成紀` shape from
   `CLAUDE.md`.
2. **Choosing the target property means choosing an item**, and confirming a
   Wikidata item means asking Wikidata, which is the 429 rule. The check runs
   offline against `wikidata/items/` or not at all.

Existing items are described "**120th/121st/122nd Samaritan High Priest**", so
consistency argues for the description; a structured claim is the thing missing.

## Samaritan women who must not become items

**`daughter of Sanballat the Horonite`** and **`daughter of the king of
Assyria`** are the only two wives in 99 family records across the priestly tree.
Both are **descriptions, not names** — the field holds a relationship.

**Creating items labelled that would invent two people.** If either is ever
wanted she is a qualifier or a described statement, never an item. See
`reports/samaritan-marriages.md`.

## Contradiction resolution

**Worth doing, explicitly not a priority** — `CLAUDE.md` § *The purpose is to ADD
to Wikidata, not to correct it*. 24,957 addable statements against 930 conflicts,
twenty-seven to one.

Settled and no longer a contradiction at all: **a second Geni ID on one item.**
Geni forbids connecting biblical people to living people, so unmergeable
duplicates are permanent and correct — they are emitted as an additional `P2600`.

## `P1545` series ordinal

Documented in `CLAUDE.md`, emitted by `genimerge.namelinks`, and **never yet
present in a generated batch** because no matched person has had more than one
given-name token. Correct by confirmation rather than by observation. The first
batch containing one is worth reading closely.

## Name and surname items

From `todo.md`: creating Wikidata items for **surnames that have none**, so
people can be linked to them, and queued edits adding name links to people who
already have items. Named by Emma as one of the harder pieces from the outset.
Not started.

## The Itamar spine's invented generation count

`gedcom/samaritan-itamar-spine.ged` places Tabia ha'Abta'i at **generation 121**,
derived from "the 132nd High Priest since Aaron". That number is an **office
count** — 112 Phinhas high priests plus 20 Itamar ones — and the office passes
sideways to brothers, so it is not a generation depth. Wikidata's own
descriptions number the same men 120th/121st/122nd on the same scheme,
independently confirming it counts offices.

**The Itamar line's generation depth is not recorded anywhere.** The file
currently asserts a count no source makes, and a single "distance not recorded"
link between Itamar and Shalma is the honest replacement. Not applied — Emma has
not said which way to take it.
