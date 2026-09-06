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

## ⛔ IT ADDS ONE ANCESTOR AND RETURNS ITS ID. It is not a campaign

**Emma, 2026-09-05**, asked whether the walk should give parents to the placeholders it had just
created: *"Uhh. No this is not an unbound method. I think it technically uses recursion but the
rule is simple: it runs like `addAncestor(start_id);` and then it adds an ancestor of `start_id`
and returns the id of it as `end_id` and then a subsequent method will use `end_id`, generally
doing a forest export, or descendants export. Blood relatives exports and ancestor exports are of
questionable use for this time."*

So the loop above is a **search for one open slot**, not a programme of filling in a tree. The
moment a person is created the walk ends, its remaining queue is dropped, and `end_id` is the
handle the next step uses.

**Why the bound matters rather than being tidiness.** Every created `NN` has no parents of its
own, so without this it immediately becomes a candidate for its own `NN` mother, and the next
pass for that one's. That is an unbounded chain of invented people on a live site carrying other
people's trees. Two such proposals were sitting in front of a dry run when she was asked.

**The export that follows is `Forest` or `Descendants`.** Her words, same message: blood-relatives
and ancestors walks are *"of questionable use for this time"* -- so they are not what an
`addAncestor` result is spent on.

## The zero-parent case takes the FATHER

**Her ruling, 2026-09-05**, asked who is created for somebody with no parents at all and no
patronymic: **"Father, per the seed rules"** -- `docs/export-seed-rules.md` tiers 4 and 5, `NN`
plus the birth surname, or `NN /father of X/`.

That settles the divergence this file flagged when it was written. **The mother-first ordering
above governs the case where one parent already exists**; the empty case is the seed rules'.
A patronymic still takes the father first either way, because it names him.

## What the walk does NOT decide: the name

Which parent to add, and in what order, is this file. **What that parent is CALLED is
`docs/export-seed-rules.md`** — the five tiers, the patronymic resolving to a proper nominative
(`Olsen` → `Ole`, not `Ols`), the farm name that is a surname, and `Suggest surnames` staying
off so a created `NN` does not acquire an invented family name.

**That divergence is SETTLED** -- see § *The zero-parent case takes the FATHER* above. She ruled on 2026-09-05 that a person with no parents and no patronymic gets the father, per the seed rules, and that the mother-first order governs the one-parent case.

## Why this shape gets round the canvas

The tree view draws its `+` affordances on a canvas with no scene graph — measured 2026-09-05,
`stage.current.find('Group')` returns 0 — so there is nothing in the DOM to click and no node
position to read. The agentic loop found them by screenshot.

**The extension can see** — `chrome.tabs.captureVisibleTab`, and the canvas itself through
`getImageData` — and Emma's point stands that it should: *"the extension has to have eyes or it
really should have eyes, and I don't understand why it is that you did not assume that it
would."* This walk is the route that does not need them, taken because it is simpler, not
because eyes are impossible.
