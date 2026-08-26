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

**The ideal state is the union of the synoptic tree and the Geni tree.** Not the Geni tree alone
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

## Step 1 — creation of individuals

| what | how many |
| --- | ---: |
| parent pairs, chosen at random from the ideal state | 4 |
| an **ancestral** pair, from the high up-going ancestry | 1 |
| **shuffled together**, so the batch shows five pairs and the ancestral one is not first | **5 pairs** |
| people whose spouse and children are filled in at random | 4 |

*"It creates four parent pairs plus one person who is a part of the high-upgoing ancestry, like
one ancestral pair and four random pairs. The ancestral pair is shuffled in, so there are five
pairs generated. There are also four people whose spouse and children are randomly filled in."*

**The shuffle is load-bearing**, not cosmetic: the ancestral pair is mixed into the five so the
batch is not ordered by importance.

## Step 1b — the descendant chain, once far enough along

*"Once we get to a certain point, the descendant chain that we're actually trying to put in gets
built. From there, we're doing a bit of a step further: we are randomly finding five parent pairs
and then filling them in with their entire children. This is an additional step, although it could
be in the same line as the descendants one."*

So: **5 parent pairs picked at random, each filled in with their ENTIRE set of children** — not a
sample of the children. This may be emitted alongside the descendant chain rather than after it.

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
day* is the same rule, and it is a presentation rule: the links are correct, there are simply too
many arriving at once for a watchlist to read as anything but noise.

## What this supersedes

The one-hop-a-day ring in `scripts/build-garborg-day.py` is not this algorithm. It picks by
distance from Arne; this picks **five parent pairs, four spouse-and-children fills, ten names and
ten sibling pairs** from the model-vs-ideal diff, in a fixed order, with the ancestral pair
shuffled in. The hyperlocal target is unchanged — `CLAUDE.md` § *The programme is HYPERLOCAL* —
and *"in the arnie area, it's really clear"* is where the ideal state is well enough known to run
this.
