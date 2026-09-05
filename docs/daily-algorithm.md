# The daily QuickStatements algorithm

**`docs/dictation/2026-08-26-daily-algorithm.md` is the authority.** This file is a reading of
it and loses in any disagreement. Emma, 2026-08-26, on why the spec is dictated so rigidly:
*"The order itself is structurally rigid because it depends on certain things being capable of
being referenced in certain situations."*

## The weirdness is the design. Do not sand it off

**Emma, 2026-08-26:** *"The algorithm is a bit weird, and the weirdness isn't something to be
sanded off and tried to be made sensible. The weirdness exists because we are structurally forced
into the weirdness by the nature of the API that we're using."*

The output will contain arrangements that look wrong and are not:

* Somebody with reciprocal links to every child and to every spouse, **whose spouses are linked
  to none of those children**.
* A person with two parents **who are not linked to each other as spouses**.

Her words: *"These things aren't how things should work. They're not sensible, but specifically,
they are very intentional."* They are what falls out of a path-dependent order optimised for
**the fastest creation possible within QuickStatements batches**. A later day closes them. Do not
add a pass that "fixes" them mid-run, and do not treat one as a bug report.

## Step 0 — read her Wikidata contributions, then diff against the ideal

1. **Check her Wikidata profile for everything she has edited**, and add it to the ledger.
   `Special:Contributions/日巫女`, never a bulk download — `CLAUDE.md` § *Emma edits the tree and
   the items BY HAND, continuously*, and git records what a batch *offered*, not what exists.
2. **Take those out**, and check the actual state of what remains against **the ideal state**.

**The ideal state is what Wikidata already holds plus what Geni supports** — her ruling,
2026-09-01. It used to read *"the union of the synoptic tree and the Geni tree"*, which is a
tautology if *synoptic* means the Geni union and a redundancy if it means the full union; neither
was what she meant. Not the Geni tree alone
and not Wikidata's current contents: the model says what each item *should* hold, and the diff
against reality says what is emittable. `scripts/model-vs-reality.py` is the existing half of
this; its `missing` column is the emittable set and its `CONFLICT` column goes out beside what is
already there, cited `S2600`.

## The order is structurally rigid, and it is the whole point

    1. creation of individuals
    2. creation of names
    3. relationships between individuals

**Why**: *"You need an individual to exist for their name object to be linked to them."* The one
real API limit is that **two items created in the same batch cannot point at each other**; an
existing item may point at a new one and a new one at an existing one. Everything in this order
follows from that.

## Step 1 — creation of individuals. REVISED 2026-08-26, after she stopped a run

**She terminated a 50-creation run partway through**: *"I had to terminate that round early
because of the unbounded behaviour."* The cause was the old step 1b — five couples with their
**entire** children, one of which had eleven — which supplied 28 of the 50.
*"Creating individuals with all of their children is just crazy talk."*

| | per run |
| --- | ---: |
| **children** — a random person gets **ONE** child | **10** |
| **spouse instead**, where the couple has no child left to add | inside the 10 |
| **parents** — a random person missing one gets **ONE** | **10** |
| **free parents** — half-attached people, `10 + half the remainder` | uncapped by design |
| **the spine**, one step on EACH of the two paths | outside every cap |

**Spouses have no bucket of their own.** Her first version said *"10 parents, 10 spouses, 10
children"*; she revised it in the same message — *"spouses are only added through the 10
parents and 10 children"*. They arrive two ways, both subordinate to children: as the **free
parent** of a child just added (which is that child's other parent, i.e. somebody's spouse), and
as the **substitution** when a picked person's marriage has no child left. Her words: *"spouses
are going to be added at the same rate as children, but they're added in a way that is, in a
sense, subordinate to the adding of children. The only reason we substitute in childless
marriages is just because, without substituting in childless marriages, there's no way to access
spouses from childless marriages."*

**The free-parent budget is a formula, not a cap**: *"10 free parents plus half of the
remaining."* Of the eligible half-attached people, the first ten come free and half of whatever
is left beyond ten comes too. Two earlier readings were wrong — a flat ceiling of 40 (mine), and
scoping it to this run's children alone, which gave 5 and under-served the backlog.

**The spine advances on BOTH paths, one step each.** `paths/charlemagne-to-arne-garborg.tsv` and
`paths/bergitte-to-emma.tsv`. Walking a concatenation advances only the first, which is how the
line down to her stayed at **0 of 16 steps** — the *"critical path going to me"* she doubted the
last run produced. It had not.

**Her hand identifications are folded into the ledger**, because they are the only record of an item
that carries no `P2600` yet. Without it the spine walk hit step 1 of the Bergitte path — **Emma
herself** — and emitted a `CREATE` that would have minted her a second item beside `Q232803`.

## Step 2 — creation of names

**10 name items** per run, taken from the name items missing in the ideal state, **with their
links made in the same run**. `scripts/build-garborg-name-items.py` does this: each `CREATE` is
followed by `Qperson Pprop LAST` for every bearer who already holds a QID. A person the same run
is *creating* cannot be linked here — `LAST` would then name the person — and waits for the next
run. That is the sequence working, not a gate.

## Step 3 — relationships between existing items

| relationship | per run |
| --- | ---: |
| `P3373` *sibling* pairs | **10** |
| `P26` *spouse*, `P22` *father*, `P25` *mother*, `P40` *child* between existing items | **all of them** |

*"We do 10 sibling pair relationships and all of the spouse, parent, etc., relationships between
existing items… Because siblings is really massive, these ones are not."*

Siblings grow as the **square** of a family's size — one family of nine children is 72 `P3373`
statements — which is why they alone are capped. `CLAUDE.md` § *`P3373` sibling is capped at 10 a
day* is the same rule, and it is a pacing rule: the links are correct, there are simply too many
of them to send in one batch.

## What this supersedes

The one-hop-a-day ring in `scripts/build-garborg-day.py` is not this algorithm, and neither is
the first version of this file. That one had **five parent pairs with their entire children**;
she stopped a run over it and it is gone. What stands is above: ten children, ten parents, free
parents at `10 + half the remainder`, one spine step per path, spouses only as a consequence.

The hyperlocal target is unchanged — `CLAUDE.md` § *The programme is HYPERLOCAL* — and *"in the
arnie area, it's really clear"* is where the ideal state is well enough known to run this.
