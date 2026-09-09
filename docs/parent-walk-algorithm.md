# The parent walk — the algorithm, dictated 2026-09-05

The walk that fills in missing parents by going **up** the ancestry, adding whoever is absent
and enqueuing whoever is present. It replaces hunting for an open slot on the canvas tree: it
needs no ghost `+` node and no pixels, because every step is a profile page and an add link.

**The ordering is very specific and was given as such.** So the order below is the
specification, not a suggestion, and `CLAUDE.md` § *Long command
series run in strict order* governs — do not reorder it because another order looks equivalent.

**The queue here is the ALGORITHM's queue**, not the development queue. Nothing in this file
is a `queue.md` item.

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

## ⛔ THE FULL RULE, dictated 2026-09-05. This supersedes the sketch above where they differ

The surname source is the part that changes what was built:

> From any individual the mother and father get added in order to the queue if both exist.
>
> If neither exists and the person has a recognised patronymic then the father is created using
> a first name taken from the patronymic plus the suggested surname; if the suggested surname is
> the patronymic it is replaced with `NN`, and if it contains but is not entirely the patronymic
> then the patronymic is removed from the suggested surname.
>
> If there is no patronymic then the father is `NN` + suggested surname.
>
> If there is a father but no mother then the mother is `NN` + suggested surname. If a matronymic
> existed it would go through all the patronymic rules, but matronymics are not supported yet.
>
> If both parents exist, or an error prevented adding a new parent, move on to the next in the
> queue.

| state of the person | who is created | first name | surname |
| --- | --- | --- | --- |
| both parents exist | nobody | — | — (enqueue mother, then father) |
| no parents, has a patronymic | **father** | from the patronymic | **suggested**, minus the patronymic |
| no parents, no patronymic | **father** | `NN` | **suggested** |
| father present, mother absent | **mother** | `NN` | **suggested** |
| an add fails for any reason | nobody | — | move to the next in the queue |

**⛔ THE SURNAME IS GENI'S SUGGESTION, not ours.** This is the correction: the walk was computing
a surname by parsing the child's own name tokens, which is why it had a Spanish two-surname
problem and a `last token` heuristic at all. It does not need one. Geni's *Suggest surnames*
offers something plausible for a parent, and the rule is applied to **that string**:

    suggested == the patronymic          ->  "NN"
    suggested contains the patronymic    ->  strip the patronymic out of it
    otherwise                            ->  use it as offered

**SUGGEST SURNAMES IS ALWAYS ON.** Suggested surnames are always a good thing and were
disabled for no reason (2026-09-05). It was ticked off in the first implementation on the
strength of `docs/export-seed-rules.md` tier 3, which said Geni would offer the child's surname
*"which would be invented"*. That reading is reversed: a plausible surname is a better handle
than none, and the patronymic-stripping rules above are what keep it honest.

**Matronymics are NOT supported.** If one existed it would go through all the patronymic
rules. Nothing infers one today, and nothing should start.

## Why the queue is shaped this way — it optimises for the least documented lineages

**The justification for mother-first:** mothers are the most likely to be unrecorded, then
maternal grandparents, and so on outward — the ordering is structured to optimise for that. So
the ordering is not arbitrary politeness; it walks toward the sparsest part of the
record first.

**And the father is created preferentially** because the evidence is better there: a patronymic
sometimes gives his first name, and suggested surnames tend to give something plausible for the
father even where there is no patronymic.

**It is greedy best-first, and that is a deliberate change from the older method.** The earlier
algorithms saw several generations up and chose the most optimal person to add from a displayed
family tree; this one simply goes up through a queue, which is the same basic thing. So a
worse-but-cheaper pick each step, rather than reading a whole tree view to find the best one --
which is also what lets it run without the canvas.

## Failure is a skip, and that is the whole master-profile handling

**If the add fails for any reason the walk moves on to the next member of the queue**, and
that is the whole of how master profiles are resolved.

So a locked master profile, a dialog that will not open, an id that will not come off the page
— none of them is a special case and none needs detecting. The add fails, the walk takes the
next person, and nothing is recorded about why. This is
`docs/export-seed-rules.md` § *Bail on anything weird* arriving at the same place from a
different direction, and it is why the walk needs no error taxonomy.

**No hold list.** A person skipped is not excluded — the same rule as § *A BAIL IS PER-ATTEMPT,
NEVER PER-PERSON*. The walk is self-healing because the queue keeps producing work.

## ⛔ IT ADDS ONE ANCESTOR AND RETURNS ITS ID. It is not a campaign

**Ruled 2026-09-05**, on whether the walk should give parents to the placeholders it had just
created: it is not an unbound method. It technically uses recursion, and the rule is simple —
`addAncestor(start_id)` adds one ancestor of `start_id` and returns its id as `end_id`, and a
subsequent method uses `end_id`, generally for a `Forest` or `Descendants` export. Blood-relative
and ancestor exports are of questionable use at this time.

So the loop above is a **search for one open slot**, not a programme of filling in a tree. The
moment a person is created the walk ends, its remaining queue is dropped, and `end_id` is the
handle the next step uses.

**Why the bound matters rather than being tidiness.** Every created `NN` has no parents of its
own, so without this it immediately becomes a candidate for its own `NN` mother, and the next
pass for that one's. That is an unbounded chain of invented people on a live site carrying other
people's trees. Two such proposals were sitting in front of a dry run when the question was put.

**The export that follows is `Forest` or `Descendants`.** Blood-relative and ancestor walks are
of questionable use at this time, so they are not what an `addAncestor` result is spent on.

## The zero-parent case takes the FATHER

**Ruled 2026-09-05**, on who is created for somebody with no parents at all and no patronymic:
**the father, per the seed rules** -- `docs/export-seed-rules.md` tiers 4 and 5, `NN`
plus the birth surname, or `NN /father of X/`.

That settles the divergence this file flagged when it was written. **The mother-first ordering
above governs the case where one parent already exists**; the empty case is the seed rules'.
A patronymic still takes the father first either way, because it names him.

## What the walk does NOT decide: the name

Which parent to add, and in what order, is this file. **What that parent is CALLED is
`docs/export-seed-rules.md`** — the five tiers, the patronymic resolving to a proper nominative
(`Olsen` → `Ole`, not `Ols`), the farm name that is a surname, and `Suggest surnames` staying
off so a created `NN` does not acquire an invented family name.

**That divergence is SETTLED** -- see § *The zero-parent case takes the FATHER* above. A person
with no parents and no patronymic gets the father, per the seed rules, and the mother-first order
governs the one-parent case (2026-09-05).

## Why this shape gets round the canvas

The tree view draws its `+` affordances on a canvas with no scene graph — measured 2026-09-05,
`stage.current.find('Group')` returns 0 — so there is nothing in the DOM to click and no node
position to read. The agentic loop found them by screenshot.

**The extension can see** — `chrome.tabs.captureVisibleTab`, and the canvas itself through
`getImageData` — and the point stands that it should: the extension has to have eyes, or really
should have them, and that it would was the assumption to make. This walk is the route that does not need them, taken because it is simpler, not
because eyes are impossible.
