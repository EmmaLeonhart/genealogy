	"6000000009305060696"
#   Q55068638 Friedrich zu Schwarzenberg und Hohenlandsberg: P734 family name = the item just created
Q55068638	P734	LAST	S2600	"6000000014784646061"
#   Q110261972 Johann I von Tengen und Nellenburg: P734 family name = the item just created
Q110261972	P734	LAST	S2600	"6000000017758205608"
#   Q110415677 Georg III von der Leyen zu Eltz und Leiningen: P734 family name = the item just created
Q110415677	P734	LAST	S2600	"6000000019797018175"
#   Q828346 Berthold Graf von Neuffen und Achalm: P734 family name = the item just created
Q828346	P734	LAST	S2600	"6000000082813823834"
#   Q110410743 Nicolaus* Andreas Graf von Maltzahn, Freiherr zu Wartenberg und Penzlin: P734 family name = the item just created
Q110410743	P734	LAST	S2600	"6000000105706792946"

## PINNED LAST -- RESTART THE PATH COLLECTION IF IT HAS STOPPED

Ruled 2026-09-14: *"have the very last queue item be one that would be to restart the path
collection in the event that the path collection ended up stopping."* And the standing rule is
now in `CLAUDE.md` § *THE PATH CAMPAIGN RUNS IN EVERY SESSION, NO MATTER WHAT*.

    check    ls -lt ~/Downloads/path-chains-*.tsv  -- a gap means it is dead
             window.__pathrun in the geni.com tab: {running, i, ok, fail}
    restart  open an UNCONNECTED profile, paste the DERIVE block of scripts/pathrun.js,
             then the RUN block with ids from scripts/build-pathrun-batch.py
    stop     window.__pathrun.stop()

**Its stopping is not an emergency and not a reason to work on it.** Restart it, go back to the
first item.

- **DECIDE: what happens to `build-add-p2600-batch`.** <!-- requeued-add-p2600-2026-09-13 -->
  Deferred on 2026-09-06 for want of context to decide on, and re-queued on 2026-09-13 by
  `.github/workflows/requeue-add-p2600.yml`.

  It writes **7,166 `P2600` statements** inferred from parent-anchor proof into
  `reports/wikidata-add-p2600.qs`, and **nothing runs it**. The four options as they stood: fold
  it into the daily batch under a cap; give it its own scheduled workflow; delete it; or leave it
  as a hand-run tool. `reports/qs-batch-audit.md` carries the measurement.

  The other five generators in that audit were settled on 2026-09-06 —
  `build-missing-reciprocals`, `build-qid-link-p2600`, `build-label-corrections` and
  `build-sibling-batch` deleted by instruction, `build-from-diff` given its own review item.
  This is the last one open.

## ⛔ MAKE THE REPO MINIMALIST. NOT YET — SEE THE PIPELINE RUN FIRST

Ruled 2026-09-17: *"this repo ought to be extremely minimalist. Smallest it can possibly be."*
And immediately after, on being shown the first measurement: *"Hold the fuck off on this. Add the
item to the queue to work on making it more minimalist. I want to actually see the repo editing
in the current state before you torch the current state."*

**So this is queued, not started.** The current state has to be observed running before anything
is removed — a thing nobody has watched work is a thing nobody can tell was load-bearing.

What is known so far, and it is one measurement, not a plan:

    scripts    342 .py/.js
    reports  1,805 files
    docs        41
    workflows   12

`CLAUDE.md` § *LEGACY CODE IS DELETED* already gives the test — *does the pipeline read this*,
not *might this be useful* — so the work is applying it, not deciding it.

⛔ **AND THE OBVIOUS FIRST CUT IS NOT OBVIOUS.** The roster TSVs look like the thing to scrub now
that `5feda3d6` folded all 441 pairs into the identifications GEDCOM — but they are still READ,
by `build-qid-links-gedcom.py`, so by the repo's own test they are not legacy. Making them legacy
means moving their pairs into the generator's constant first. That is a decision with an order to
it, which is exactly why it is queued rather than done.

⛔ **NOTHING IN THE PIPELINE IS TRIVIAL**, ruled the same day: *"even if I tell you something is
trivial, it is probably not trivial"*, and *"if there's anything in the pipeline that makes it
slower, that is intentional."* A minimalism pass is the most dangerous possible shape for that
failure, so it does not start until the pipeline has been watched end to end in its current form.

## Ingemund Grimsson is ELEVATED, 2026-09-18

Ruled: *"immediately run an ancestors export desendants export and forest export on this
person ... they are top priority and their export is gonna be elevated in importance a it
overrides other things"* -- <https://www.geni.com/people/Ingemund-Grimsson-I-R