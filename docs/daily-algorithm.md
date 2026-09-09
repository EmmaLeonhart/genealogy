# The daily QuickStatements algorithm

**`docs/dictation/2026-08-26-daily-algorithm.md` is the authority.** This file is a reading of
it and loses in any disagreement. The order is structurally rigid because it depends on certain
things being referenceable in certain situations.

## The weirdness is the design. Do not sand it off

**The algorithm is weird, and the weirdness is not to be sanded off into something sensible.**
It exists because the API structurally forces it.

The output will contain arrangements that look wrong and are not:

* Somebody with reciprocal links to every child and to every spouse, **whose spouses are linked
  to none of those children**.
* A person with two parents **who are not linked to each other as spouses**.

These are not how things should work and they are not sensible, and they are very
intentional. They are what falls out of a path-dependent order optimised for
**the fastest creation possible within QuickStatements batches**. A later day closes them. Do not
add a pass that "fixes" them mid-run, and do not treat one as a bug report.

## Step 0 — read the account's Wikidata contributions, then diff against the ideal

1. **Check the Wikidata account for everything it has edited**, and add it to the ledger.
   `Special:Contributions/日巫女`, never a bulk download — `CLAUDE.md` § *The tree and the items are edited BY HAND, continuously*, and git records what a batch *offered*, not what exists.
2. **Take those out**, and check the actual state of what remains against **the ideal state**.

**The ideal state is what Wikidata already holds plus what Geni supports** — ruled 2026-09-01.
It used to read *"the union of the synoptic tree and the Geni tree"*, which is a tautology if
*synoptic* means the Geni union and a redundancy if it means the full union; neither was the
thing meant. Not the Geni tree alone
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

## Step 1 — creation of individuals. REVISED 2026-08-26, after a run was stopped

**A 50-creation run was terminated partway through, for unbounded behaviour.** The cause was
the old step 1b — five couples with their **entire** children, one of which had eleven — which
supplied 28 of the 50. Creating individuals with all of their children is not a thing to do.

**The dictated numbers were 10s. They have been doubled twice since** — 2026-09-05 and
2026-09-07, both times every per-run number in the repo at once. The shape below is the
specified one; the figures are the current constants, which live in
`scripts/build-garborg-day.py` and are the authority on their own values.

| | per run | constant |
| --- | ---: | --- |
| **children** — a random person gets **ONE** child | **40** | `CHILDREN_PER_RUN` |
| **spouse instead**, where the couple has no child left to add | inside the 40 | — |
| **parents** — a random person missing one gets **ONE** | **40** | `PARENTS_PER_RUN` |
| **free parents** — half-attached people, `20 + half the remainder` | uncapped by design | `FREE_PARENTS_FREE` |
| **the spine**, one step on EACH of the two paths | outside every cap | — |

**Spouses have no bucket of their own.** The first version of the spec gave them one and it was
revised in the same message: spouses are added only through the parents and children buckets.
They arrive two ways, both subordinate to children: as the **free parent** of a child just added
(that child's other parent, i.e. somebody's spouse), and as the **substitution** when a picked
person's marriage has no child left. So spouses are added at the same rate as children, in a way
subordinate to them, and the substitution exists only because without it a childless marriage
gives no route to its spouses at all.

**The free-parent budget is a formula, not a cap**: ten free parents plus half of the
remainder. Of the eligible half-attached people, the first `FREE_PARENTS_FREE` come free and
half of whatever is left beyond that comes too — 20 since the 2026-09-07 doubling. Two earlier readings were wrong — a flat ceiling of 40 (mine), and
scoping it to this run's children alone, which gave 5 and under-served the backlog.

**The spine advances on BOTH paths, one step each.** `paths/charlemagne-to-arne-garborg.tsv` and
`paths/bergitte-to-emma.tsv`. Walking a concatenation advances only the first, which is how the
second path stayed at **0 of 16 steps** while appearing to run.

**The hand identifications are folded into the ledger**, because they are the only record of an
item that carries no `P2600` yet. Without it the spine walk hit step 1 of the Bergitte path — a
person who already has `Q232803` — and emitted a `CREATE` that would have minted a second item
beside it.

## Step 2 — creation of names

**`NAME_ITEMS_PER_RUN` name items** per run — 40, or 12 while a hold runs — taken from the
name items missing in the ideal state, **with their
links made in the same run**. `scripts/build-garborg-name-items.py` does this: each `CREATE` is
followed by `Qperson Pprop LAST` for every bearer who already holds a QID. A person the same run
is *creating* cannot be linked here — `LAST` would then name the person — and waits for the next
run. That is the sequence working, not a gate.

## Step 3 — relationships between existing items

| relationship | per run |
| --- | ---: |
| `P3373` *sibling* pairs | **10** |
| `P26` *spouse*, `P22` *father*, `P25` *mother*, `P40` *child* between existing items | **all of them** |

Ten sibling pairs and all of the spouse, parent and child relationships between existing items,
because siblings are massive in number and the others are not.

Siblings grow as the **square** of a family's size — one family of nine children is 72 `P3373`
statements — which is why they alone are capped. `CLAUDE.md` § *`P3373` sibling is capped at 10 a
day* is the same rule, and it is a pacing rule: the links are correct, there are simply too many
of them to send in one batch.

## What this supersedes

The one-hop-a-day ring in `scripts/build-garborg-day.py` is not this algorithm, and neither is
the first version of this file. That one had **five parent pairs with their entire children**; a run was stopped over it and it
is gone. What stands is above: ten children, ten parents, free
parents at `10 + half the remainder`, one spine step per path, spouses only as a consequence.

The hyperlocal target is unchanged — `CLAUDE.md` § *The programme is HYPERLOCAL*. The Arne
neighbourhood is where the ideal state is known well enough to run this.
