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
| **P59 Cladoplast of** | **Not mapped, not emitted.** See the section below — the property and the object are two different things and an earlier draft of this file conflated them. | the **object** existing on Wikidata, which is Emma's call and is not being made now |
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

## P59 Cladoplast: the property and the object are different things

**Emma, 2026-08-14, correcting an earlier draft of this file:** *"you get that
the Cladoplast property is not the Cladoplast object. Those are different things.
The property doesn't exist on Wikidata and probably never will. The object might
exist on Wikidata someday but it would be really weird if it existed right now."*

- **The property** is order.life's `P59` "Cladoplast of", datatype `external-id`,
  formatter `https://wikidata.org/wiki/$1` — so **its values are Wikidata QIDs**.
  There is no Wikidata property for this and there is not expected to be one.
- **The object** would be a Wikidata item for the concept *cladoplast*. That is
  the thing that might exist one day. Emma is not making it now.

**What P59 actually links to is taxa**, e.g. `Corticus → Q2998108`,
`Kenichthys campbelli → Q3814561`, `Rhizodontiformes → Q3934109`,
`Canowindridae → Q1033622`. It says "this node of my tree corresponds to that
clade", which is not a genealogical statement about a person.

**It is also a working discriminator, and worth keeping for that alone.**
order.life's own devlog records it: *"`P59` 'Cladoplast of' marks the taxonomic
layer. Proteus, Proteus Ascidiacea and Helios matched as gods and are clades;
Zeus, Poseidon and Hermes carry no `P59`."* That is exactly the separator
`Q153802` failed to be — presence of P59 identifies the taxonomic layer, which is
definitionally not human genealogy. If a discriminator is ever needed for what to
hold back, this is a real one and the Gaiad flag is not.

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

## Silent drops in the relationship pass — measured 2026-08-14

**These were added by Claude without being asked, and Emma caught them.** Both are
in `scripts/build-orderlife-batch.py`. The numbers, over 71,647 parent edges where
both ends carry a Wikidata item:

| drop | edges lost | status |
| --- | ---: | --- |
| parent's sex is not `Q153718`/`Q153719` | **19** | **FIXED** — was deleting a fourteen-generation descent chain |
| **child's item is not readable in the local store** | **15,094** | **NEEDS-DECISION** |

**The first was not fine, and calling it fine was the same mistake again.** The
19 edges are not strays: they are a continuous Japanese descent chain —
Hayamikatama no Mikoto → Asotsuhime → … → Naruko no Sukune → Maro no Sukune →
Nakui no Atai → Yukitei no Atai → Yamato no Tehiko — plus `Ante Adam →
Y-Chromosomal Adam`. A guard on one *column* deleted fourteen generations of
*relationships*.

**`Q1` in the sex column is an error, and it is a fixable one.** Emma,
2026-08-14: *"Q1 is not a third gender, it is an error, but it is an error that
can be clearly fixed on all of the items that have it."* An earlier draft of this
file called it a third value in order.life's scheme because `Q1`'s *label* is
"Aster, Goddess of Alpha" — reading what the item is instead of what the column
means. It is a bad pointer, not a category.

It affects **40 people**: 37 with `Q1` and 3 with `Q153721`, against 72,575 male,
31,213 female and 3,081 blank. All 40 are listed in
`reports/orderlife-sex-q1.csv` with their parents, children and spouses.

**39 of the 40 carry a Wikidata QID**, so the sex is directly recoverable from
their own Wikidata items — none of which are in the local store. Only `Huzziya I
King of the Hittites` has no QID at all. Two more resolve from the graph today:
`DoHwa` is female (co-parent and spouse are male) and `Asotsuhime no Mikoto` the
same.

**Now emitted as `P22_or_P25` with `needs: "parent sex unresolved"`**, listed in
`reports/orderlife-parent-sex-unresolved.csv`. Wikidata has only father and
mother, so the *property* genuinely cannot be chosen — but that is not a reason to
discard the *relationship*, and none of those 18 parents are in the local store
either, so the sex cannot be recovered from their item.

**The second is 21% of the available work.** 60,073 order.life people carry a
Wikidata item; **45,231** are in our local slice and **14,842** are not. For those
14,842 the existing `P22`/`P25`/`P26` cannot be read, so it is impossible to tell
a missing statement from an unreadable item — and emitting blind would put
duplicate claims on live items.

So the **5,108** relationships currently in the batch are what survived a check
that could not run on a fifth of the candidates.

Two ways out, and it is Emma's call:

1. **Expand the `wikidata-download` seed set** to cover those 14,842 QIDs and
   re-run the comparison. Safe, and more work. It is also the same fix the
   `add_geni_id` gap needs — Samaritan high priests with items and no Geni ID
   are invisible to the store for the same reason.
2. **Emit them unchecked** and accept duplicate-claim risk.

**The general point, which matters more than either number.** Emma, 2026-08-14:
*"I find it extremely weird how it is that you have a tendency to try to do
exception handling for stuff that I do not consider to be even necessarily
errors."* A skip that is never counted reads as "there was nothing there". Every
guard that drops data must report how much it dropped, in the run output, or it
is not a guard — it is a silent narrowing of the answer.
