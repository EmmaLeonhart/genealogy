# The parent walk — Emma's algorithm, dictated 2026-09-05

The walk that fills in missing parents by going **up** the ancestry, adding whoever is absent
and enqueuing whoever is present. It replaces hunting for an open slot on the canvas tree: it
needs no ghost `+` node and no pixels, because every step is a profile page and an add link.

**Her framing of the ordering:** *"I am giving you a very, very specific ordering of things."*
So the order below is the specification, not a suggestion, and `CLAUDE.md` § *Long command
series run in strict order* governs — do not reorder it because another order looks equivalent.

**The queue here is the ALGORITHM's queue.** Her words: *"just to be clear, this is the queue of
the algorithm. This isn't the queue of our development."* Nothing in this file is a `queue.md`
item.

## The loop

Take a person off the queue and, for that person:

1. **Is a patronymic present in their name?**

   - **Yes** — this *overrides* the default order. **Check the father first.**
     - Father absent → **add the father**, named from the patronymic.
     - Father present → fall through to step 2.
   - **No** — **check the mother first**, then the father.

2. **Add whichever parent is absent.**

   - No mother → **add the mother**.
   - No father → **add the father**.

3. **If both parents already exist**, add neither. **Enqueue the mother, then the father** —
   in that order — and carry on up.

4. **Repeat.** *"And it keeps on going like this, going up going up and trying to add people."*

## Failure is a skip, and that is the whole master-profile handling

**Her words:** *"If it fails to add somebody for some reason, then it's pretty simple. It just
moves on to the next member of the queue. And that's how we resolve master profiles."*

So a locked master profile, a dialog that will not open, an id that will not come off the page
— none of them is a special case and none needs detecting. The add fails, the walk takes the
next person, and nothing is recorded about why. This is
`docs/export-seed-rules.md` § *Bail on anything weird* arriving at the same place from a
different direction, and it is why the walk needs no error taxonomy.

**No hold list.** A person skipped is not excluded — the same rule as § *A BAIL IS PER-ATTEMPT,
NEVER PER-PERSON*. The walk is self-healing because the queue keeps producing work.

## What the walk does NOT decide: the name

Which parent to add, and in what order, is this file. **What that parent is CALLED is
`docs/export-seed-rules.md`** — the five tiers, the patronymic resolving to a proper nominative
(`Olsen` → `Ole`, not `Ols`), the farm name that is a surname, and `Suggest surnames` staying
off so a created `NN` does not acquire an invented family name.

**One divergence to settle with her, flagged rather than silently resolved.** For a person with
**no parents at all and no patronymic**, this algorithm checks the mother first and so adds the
**mother**; the seed rules' tiers 4 and 5 create the **father** (`NN` plus the birth surname, or
`NN /father of X/`). Both are hers, this one is later and is explicitly about ordering, so the
walk follows this file — but the tiers were written about the same situation and the two should
be reconciled rather than left to whichever code runs.

## Why this shape gets round the canvas

The tree view draws its `+` affordances on a canvas with no scene graph — measured 2026-09-05,
`stage.current.find('Group')` returns 0 — so there is nothing in the DOM to click and no node
position to read. The agentic loop found them by screenshot.

**The extension can see** — `chrome.tabs.captureVisibleTab`, and the canvas itself through
`getImageData` — and Emma's point stands that it should: *"the extension has to have eyes or it
really should have eyes, and I don't understand why it is that you did not assume that it
would."* This walk is the route that does not need them, taken because it is simpler, not
because eyes are impossible.
