# The algorithms — specifications, not steps

Moved out of `CLAUDE.md` on 2026-09-09 in the ruthless cut. These describe **how a thing is
done** rather than asking for it to be done, so they are reference and not instructions.
`CLAUDE.md` cites this file; nothing here was reworded in the move.

### ⛔ THE DAILY ALGORITHM — the full spec. SPECIFICATION, not a step

`docs/dictation/2026-08-26-daily-algorithm.md` is the dictation verbatim;
`docs/daily-algorithm.md` is the reading. **The order is structurally rigid and the weirdness is
intentional** — *"the weirdness isn't something to be sanded off"*.

**One command**: `python scripts/build-daily-batch.py [--refresh-ledger]` runs step 0, then the
three steps in the specified order, and prints the run order with each file's position. Step 0 is off by
default because it is the day's one network call.

Steps 1, 1b, 2 and 3 live in `scripts/build-garborg-day.py` and
`scripts/build-garborg-name-items.py`; the caps are in those files and are the authority on
their own values, not this section. `devlog.md` 2026-08-26 has how they were built.

**The one thing still outstanding: the ideal state is what the item already holds on Wikidata
plus what Geni supports** — replacing a sentence that used to read *"the union of
the synoptic tree and the Geni tree"* and was a tautology under either meaning of the term. That is the § *PREREQUISITE ORDER* item,
not this one.

**Do not "fix" the artefacts.** Spouses unlinked to their partner's children, and parents not
linked to each other as spouses, are intentional consequences of the order and are closed by later
days.

**Two readings taken rather than asked, both recorded where the code is:** which name items —
most-borne first, so each earns the most links; and step 1b runs every time rather than behind a
gate for *once we get to a certain point*, because it belongs in the same line as the descendants
one, and an invented gate that never opens is the failure mode § *The batches are a SEQUENCE* is
written against.


### The daily Garborg batch — one QuickStatements run per day

`scripts/build-garborg-day.py` → `reports/wikidata-garborg-day.qs`.
`reports/garborg-qids.tsv` is the ledger of who has a QID, filled from **the account's Wikidata
contributions** (日巫女), never a bulk download.

**The rule: a statement goes in only if BOTH ends already have a QID.** A batch whose statements
require links that cannot exist yet is only partly runnable, and that is the practical limitation
of what QuickStatements can do. Nothing deferred, nothing commented out. What cannot
run today is tomorrow's batch, because tomorrow those items exist.

Each day: close the links yesterday's creations made possible, create the next ring, link
the new people only to what already exists.

**Nothing is outstanding on this item.** Three bullets sat here reading *NOT a blocker*,
*handled, not blocked* and *out of scope* — the name-items file (`LAST` does point at a fresh
`CREATE`), the ambiguous tokens like `Olga` (listed in the batch's own trailer, so the batch
runs without them), and CJK `SURN` (which belongs to the corpus-wide name work). They were
resolved statements rather than steps, and are removed 2026-08-30.

This item is the **standing daily process**, not a step to finish: one batch a day, for as long
as the programme runs.


### THE EDIT ALGORITHM — the specification, recorded in substance

**The bias toward the account owner's own neighbourhood is deliberate.** The specification
favours it heavily, and going against that to make it favour it less is the failure this section
guards.

**Checked 2026-08-15: nothing implements it yet.** `scripts/wikidata-edit-run.py`
is a batch executor with `MAX_EDITS_PER_RUN = 100` and a reviewed-batch allowlist.
There is no random selection and no service-area gate, so there was nothing to
alter. **When it is built, it is built to this spec — do not normalise the bias away.**

**The rate.** 100 JSONs executed per day, chosen at random from the eligible set.

**The service area — what makes an edit eligible.** An edit needs a *service
area*: something that has a Geni ID, or an item that has a Geni ID, or an item
that is getting one added. *"Something that, in our version, has a GeniID but on
Wikidata gets it. That's a service area… particularly something that has a GeniID
but is otherwise isolated."*

**Why it favours that neighbourhood, and why that is the design.** The owner's own item can add a
mother or a father with equal probability. Once one is added, **each of them can add the other**,
either can add the brother, and the brother can add back as a sibling.
Each addition creates new surface area for the next.

**So the growth rate depends on saturation, not on size.** *"There's a very large
amount of saturated relationships in the very dense areas. The most ideal situation
for lots of people being added is a bunch of individuals that are not linked to
each other and are relatively close to each other, so that each of them has a
relatively high probability of growing out more individuals."* A dense, fully-linked
region has nothing left to add; a cluster of near-but-unlinked people compounds.

**That is why the researchers and the Nordic cluster come out on top** — not
because they are ranked highest, but because *"the algorithm is most optimised to
hit these people, because they are entry points for the algorithm to function."*

**De-prioritise Geni-IDs-as-sources.** Most items are expected to receive a Geni ID and nothing
else, and if Geni IDs start being added as sources onto relationships
that already exist, **that class drops to roughly 5–25 edits a day** rather than
competing for the 100.

**Scheduled path-building runs alongside the random 100.** Deliberate edits that
build a path outward from the owner's own item, starting with the closest people who already have
Wikidata items, then filling the Charlemagne line from the medieval period
downward until it intercepts.

**The end state:** a dense region around the owner's own item, mostly of people they did not
create, which keeps accumulating because each addition raises the surface area. *"It looks like established genealogical stuff"* — and the Samaritan
high priests and the antiquity work sit inside the same region rather than beside
it.

---


### The chain of provenance

**Provenance matters, and a zipper merge should almost always carry a relatively large chain of
it** — not a single justification but a potentially very long series. That is also why the manual
verdicts are recorded: they enter the provenance too.

**BUILT — `scripts/zipper-provenance.py`, re-run 2026-08-31.** `reports/zipper-pairs.tsv` records
one step; this walks them into the **transitive closure** — a round-5 pair's justification being
its own step plus every step beneath it, down to an anchor or to a hand verdict. Chain depth **max 8, mean 2.7** over 45,898 inferred pairs. Outputs
`reports/zipper-provenance.tsv` and `reports/zipper-provenance-chains.md`.

    25,723  CORROBORATED        7,306 pairs an independent source confirms
    20,008  INFERRED            88 an independent source contradicts
       167  POISONED

Hand verdicts are first-class nodes: **103 independent pairs** from
`reports/emma-judgments.tsv`, alongside the structural walk (7,841), the Geni bio links (405) and
the clan rosters.

**This section stays as the SPECIFICATION** — the two propagation rules below are how it must keep
behaving, and they are specified rather than derivable from the code.

Two things follow:

- **Support propagates upward.** *"If you have a group of 100 people in one generation, all of
  their ancestors are all consistent. It's a really good sign... suddenly you go into the ancestors
  and you notice that somebody connected one of the ancestors. There's an entity resolution on one
  of the ancestors from our side. This supports it extremely well, and it actually supports it
  down the entire chain."*
- **Contradiction propagates the same way.** *"if you end up in a situation where there's an entity
  resolution that clearly contradicts it, this indicates a clear contradiction... it goes both
  ways."*

So the artefact is a provenance **graph** that can be walked in both directions, with the manual
RIGHT/WRONG verdicts as first-class nodes, and a report of which inferred chains an independently
recorded `P2600` confirms or refutes.


### Link reliability order — parents, spouses, children, siblings

**Ranked least messy first:**

1. **parents** — *"parents are always most reliable"*
2. **spouses** — *"can be a bit messy because sometimes people have multiple spouses"*
3. **children** — *"there's a lot of comparison stuff"*
4. **siblings** — *"sibling links are not very common"* on Wikidata

`scripts/zipper-join.py` now runs its slots in this order, which matters because the first slot to
claim a person in a round wins. Siblings are **not** a slot yet and should be added last, if at
all. **The fifth kind is surveyed** — `P1038` *relative* with `P1039` *kinship to subject*,
`reports/p1038-relative-survey.md`, 2026-08-26. 26,724 of 2,246,827 stored items carry it,
49,974 statements, 93% qualified. **71% of the kinships are ones a walk over our own parent and
child edges already produces** (uncle, grandfather, nephew, cousin); the **29%** that are not —
in-law, step, adoptive, foster, godparent — are the only part worth building on. Nothing built.

**And the point that stops a whole category of wrong stopping:** *"no ancestors isn't a point to
stop... It doesn't mean that the ancestors aren't on Wikidata. That's not what it means... at this
point, you're not really doing the zipper anymore. We'll just be adding new individuals on
Wikidata."* A slot with nothing on their side is a **creation opportunity**, which
`reports/creation-opportunities.tsv` now counts, not a failure of the join.

---


### ⛔ THE TAIL ALGORITHM — at the TAIL since 2026-08-30

*"put these at the end of the queue instead of dropping them and start on the first queue item."* **The gap-size routing below is written against a MISSING-PERSON count that now reads 0 on every path** — the scraped-page GEDCOMs were ingested, so every path member is present. Apply it to the broken-link count in `reports/broken-links.md` instead: 85 of 979 paths, 102 links.

### The original method. Supersedes how the loop picks

The tail exports were not working nearly as well as expected, and changing the approach should
get through the tail far faster.

**What the loop was doing wrong.** It seeded a placeholder near a *missing* person and exported
from there. The export goes **centred on the destination person** — the isolate at the end of the
chain — and the small gaps are handled by a different mechanism entirely.

### Work order: LONGEST paths first, then rebuild

**Target the longest paths first, then the smallest.** Run the top five longest paths, export
for each, rebuild, repeat.

**The reasoning, and checking it is explicitly forbidden.** Small paths are likely to be where
nearby exports hit significant diminishing returns; large paths are likely to be ones that have
had few exports and may be in very sparse areas, where an export is more likely to close the
whole thing. That is a bet. Running the method **is** the test.

**And it explains why the two-slot campaign underdelivered.** People in multiple paths were the
target for exactly this reason, but they were often in areas dense enough that an export did not
give the expected extension.

### Route by the size of the gap on that path

**Gap of 1–2 people — and 3 is safe too — DO NOT EXPORT.** A gap of one or two people is
basically useless as a deliverable; six minutes is not worth spending to fill in one or two
individuals on the flat tail. Instead: **open the person's page, click open the relatives section and
whatever else needs expanding, and save the page** into `geni-scraping/` — *not*
`geni_pages/`. The profiles get built from those saved pages later. *"We later on build up
the profiles from this separate thing, which won't really be a fallback thing. It'll be
another thing."*

**Gap of 4 or more — export, but from the RIGHT person.**

1. **Export centred on the destination person.** Go to the Wikidata-target/isolate at the
   end of the chain, walk their ancestors, export from there. *"I believe most of the time
   this is just going to fix it and it's going to get that person connected."*
2. **If the destination is already present and already exported from, go to the midpoint**
   of the remaining chain and attempt there.
3. **Recurse.** The worked example: a seven-person chain → export
   from the Wikidata target → it clears two → a five-chain remains → attempt at the
   midpoint → that gets the middle three → what is left is two chains of two → and those
   are finished by the page-saving method, not by more exports.

**The point is not a complete family tree.** It does not matter that the whole family tree is
consistently there; the deliverable is the chain being connected.

### Also instructed, same message

- **Retry every person previously bailed on.** A locked profile almost never means every
  individual in the tree is locked; the situation is self-healing, but they have to be attempted
  again. Four remain: Anna von Mecklenburg-Schwerin, Anna Charlotta Stenius, Ola R
  Sande (retry in flight), Artur Lidman.
- The page-saving mechanism needs the **immediate relatives** of the person being
  connected to Wikidata, which is why the relatives section must be expanded before the
  save.

**Current shape of the problem**, so the routing can be applied: 545 paths, median 8
missing each, max 33. **24 paths need 1 person, 37 need 2** — those go to page-saving.
The 4+ paths are where exports go, seeded on the destination.
