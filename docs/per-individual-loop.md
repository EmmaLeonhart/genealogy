# The per-individual loop — three things, in her order

**Emma, 2026-09-06, dictating the whole of it:**

> *"There's three things: forest from created individual, making a path from Charlemagne to the
> individual, and getting the family members from the page only.*
>
> *Generally on each individual we always grab the html family members and save them first, then
> try to get the Charlemagne path, and if it succeeds then good, if not then we do the forest
> thing out of the isolated geni individuals.*
>
> *We also do the immediate family scrape on sibling pairs in paths because parents are needed and
> this is the quickest way to get them."*

## The order, and the order is the specification

    1.  ALWAYS scrape the immediate family from the page's HTML, and SAVE it.   <- every individual
    2.  Then try the Charlemagne path.
    3a.   path found      -> done.
    3b.   path not found  -> create a placeholder and run a Forest export from it.

**Step 1 happens for everybody, unconditionally, and before anything else.** It is the cheap
thing: no search is requested, no export is spent, nothing is created. It is one page load that
is going to happen anyway, because steps 2 and 3 both start from that same profile page — so the
family members are free, and taking them first means a person who later fails at step 2 has still
yielded something.

## ⛔ STEP 3b IS GATED ON THE STATISTICS. A tiny profile gets NO export

**Emma, 2026-09-06**, on bishop Camillo Ballin -- Family Tree 11, Blood Relatives 10, Ancestors 5,
whose Charlemagne search resolved to a genuine *"No path found"*:
*"this guy has pretty much no relatives so he shouldn't get an export lol"*.

This is the mirror of `CLAUDE.md` § *THE STATISTICS BLOCK IS THE REAL INSTRUMENT*. A **saturated**
figure beside a *"no relationship found"* means a database failure, so the miss is not real and an
export is worth spending. A **tiny** figure beside the same sentence means the miss IS real: the
whole neighbourhood is the handful already on the page, and an export seeded there returns that
handful. Ballin's would have come back with about eleven people.

**Every figure carries a threshold, not just one, and `blood_relatives` was never her idea.**
The question put to her offered four floors all written in blood relatives, so the **number**
1,000 is hers and the **figure** was mine. Her replies: *"why the fuck did you choose blood
relatives"*, *"All of them need thresholds not just blood relatives"*, and *"I didn't tell you to
do blood relatives."* `family_tree` is the component size -- what an export can actually reach --
and a `Forest` export follows spouse links precisely to cross the in-law edges `blood_relatives`
excludes.

`scripts/export_gate.py` is the single place. The test is **disjunctive**: any one figure clearing
the floor clears the gate, because they measure different things and a person can be evidently
connected by any of them.

**⛔ ONE FLOOR, 300, ACROSS EVERY FIGURE.** Emma, 2026-09-06: *"Any number over 1,000 is a sure
export, i say even any number over 300 lol"*. That replaced five per-figure thresholds — 1,000 /
1,000 / 100 / 100 / 10 — which were mine. Her sentence is not five judgements, it is one reading
of when the block says there is more there than the page shows, so whichever figure carries the
number, over 300 is enough.

    family_tree  ·  blood_relatives  ·  ancestors  ·  descendants  ·  followers   >= 300

Note both directions. The two big figures came **down** from 1,000, which is the point — Valentine
Eisner reads Family Tree 914 and was skipped by 86. The three small ones went **up**, so a profile
with 12 followers no longer clears on that alone: it is a floor on the evidence, not a licence for
the weakest figure. Measured over the twelve readings held, **exactly one changes** — Valentine
Eisner, SKIP to EXPORT — and Ballin still skips at 11.

**The case that proves `family_tree` is the right primary figure** is Dorothy Jeakins:
Family Tree 1,405, Blood Relatives **1**. She is connected through in-laws, and a blood-relative
gate would have thrown away the one export that could reach her. Of the eight readings we hold,
Ballin is the only skip.

**Step 3 is the expensive fallback and only fires on failure.** A `Forest` export costs a Geni
slot, runs one at a time and cannot be cancelled; a created placeholder is a write to a live
site. Neither is spent on somebody the path already reached.

**"Out of the isolated geni individuals"** is what step 3b operates on: the people for whom no
Charlemagne path came back. `CLAUDE.md` § *THE STATISTICS BLOCK IS THE REAL INSTRUMENT* is the
caution that goes with it — a *"no relationship found"* beside a saturated Blood Relatives figure
is a database failure, not a negative result, which is why the statistics are read at step 1 and
not inferred later.

## ⛔ STEP 3b IS A `Forest` EXPORT. Her 2026-09-03 `Ancestors` instruction is WRONG

**Emma, 2026-09-06, ruling on the contradiction directly: _"9-03 is wrong"_.**

`queue.md`'s tail section, written 2026-09-03, gives a precedence order whose first case is
*connected to Charlemagne, no relationship found after the query* → **run a full `Ancestors`
export**, and calls it the common case. Her 2026-09-06 dictation says the opposite —
*"if not then we do the forest thing out of the isolated geni individuals"* — and `Forest` is what
the collector implements.

**She has now settled it: `Forest`.** The reason it matters rather than being a label: `Forest`
follows spouse links and `Ancestors` walks straight up, so on a person connected through in-laws
an `Ancestors` export goes past the join entirely. Her own tail notes name Moshe Bar Nissim as
failing *"because of large in-law chains"* — exactly the case `Ancestors` cannot reach.

The tail's precedence order is left as she wrote it; this supersedes its first case.

## ⛔ THE PHASE ORDER. The sibling scrape is LAST, and its input is the INTEGRATED tree

**Emma, 2026-09-06, correcting a mass sibling scrape I had already started:**

> *"Run the wikidata isolate connecting operation on all wikidata isolates, then you will have a
> very large number of paths plus immediate family object things from such people, with occasional
> forest exports. Then you integrate all of this into the synoptic tree, then on the people who are
> sibling pairs on the synoptic tree without parents, you do the scrape object thing on each member
> of the pair lol. So again jumping to the mass action was really bad because you skipped over a
> lot."*

    PHASE 1  run the isolate-connecting operation over ALL Wikidata isolates
             -> the per-individual loop below, on each: family scrape, then Charlemagne path,
                then a Forest export only where the path fails
             -> yields many paths, many immediate-family objects, OCCASIONAL forest exports

    PHASE 2  INTEGRATE all of it into the synoptic tree
             -> the new GEDCOMs merged, the family objects folded in

    PHASE 3  in THAT tree, find the people who are sibling pairs WITHOUT PARENTS
             -> scrape each member of each such pair

**The input to phase 3 is the integrated tree, not `paths/*.tsv`.** That is the whole correction.
The sibling pairs worth scraping are the ones still lacking parents *after* everything phase 1
collected has been merged — a set that cannot be known until phase 2 has run, and which will be
much smaller than the 1,321 pairs the current path files name, because phase 1 supplies parents
for many of them as a side effect.

**What jumping to phase 3 actually skipped:** the whole isolate campaign, its paths, its family
objects, its exports, and the merge. Scraping 2,525 people off today's path files would have spent
2,525 page loads to answer a question that phase 2 was going to answer for free, on a list that
phase 1 was going to shrink.

**Four scrapes were taken before she stopped it** — Arne Garborg, Jon Eivindson Garborg, Maria
Carlberg, Sara Carlberg. Read-only, and out of order.

## The second rule: sibling pairs in paths get the same scrape

**Because parents are what a sibling step needs, and the scrape is the fastest way to get them.**
Geni records **no sibling edge** — `CLAUDE.md` § *A sibling step is the worked example* — so two
siblings are joined only through a shared parent, and a path that steps sideways between them
names a parent that may be in nothing we hold. Scraping both members' immediate family is a
single page load each and yields exactly that parent.

**Scale, already measured:** 2,125 sibling steps of 30,329, across 662 of 696 path files. So this
is not an edge case; it is most paths.

## What this changes about what was being done

Three placeholders were created on 2026-09-05/06 with **no export run from any of them**, and
with no family scrape taken first. Under this loop both are wrong in the same way: the placeholder
is step 3b, reached only after step 2 fails, and step 1 should already have banked the family
members regardless.

## Status of the three, in the extension

| step | job | built? | verified? |
| --- | --- | --- | --- |
| 1. immediate family, saved | — | **no** | — |
| 2. Charlemagne path | `path` | yes | states and statistics yes; a saved capture of a resolved chain, no |
| 3b. create placeholder | `seed` | yes | **yes** — created unaided |
| 3b. Forest export | `export` | yes | submits yes; its own download click, no |

**Step 1 is the missing job**, and it is the one that runs on every individual.
