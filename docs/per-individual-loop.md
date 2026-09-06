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

**Step 3 is the expensive fallback and only fires on failure.** A `Forest` export costs a Geni
slot, runs one at a time and cannot be cancelled; a created placeholder is a write to a live
site. Neither is spent on somebody the path already reached.

**"Out of the isolated geni individuals"** is what step 3b operates on: the people for whom no
Charlemagne path came back. `CLAUDE.md` § *THE STATISTICS BLOCK IS THE REAL INSTRUMENT* is the
caution that goes with it — a *"no relationship found"* beside a saturated Blood Relatives figure
is a database failure, not a negative result, which is why the statistics are read at step 1 and
not inferred later.

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
