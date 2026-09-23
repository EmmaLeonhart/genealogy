# Geni-blocked campaign laundry list — archive part 2 (2026-09-22)

Continuation of `docs/queue-archive/geni-blocked-campaigns-2026-09.md`.
Do **not** start any of this under the Geni moratorium (≥2026-10-21).
Parked here so `queue.md` stays work-only.

---

## Forest exports

These are people I want exports on but they are not in the priority in the same way. Often cover possibly underserved people but their significance is unclear

Forest https://www.geni.com/people/NN-Fuca/6000000227739821875

Descendants https://www.geni.com/people/NN/6000000227739695943

## Ancestor Exports

At the end of the queue after all other things are done I want to do some specific ancestor export campaigns. 

Ancestor exports from certain specific people to get their ancestors

try this one https://www.geni.com/people/Reformatorin-Ursula-von-M%C3%BCnsterberg/6000000188494434823?through=6000000003481830064

## `Forest` exports centred on people carrying the TAIL relationships in the TSVs

Ruled 2026-09-13: *"put it at the end of the queue that... to do forest exports centred on people
with the tail relationships for the TSV files."* Written down and not started **yet**.

**Last in order, and it gets done.** Emma, immediately after: *"it's at the very terminal end of
it. And it's NOT parked. It's gonna be addressed later."*

**Why a `Forest` and not a lookup:** a relationship we have never seen in a real Geni export has
no attested representation, and § *no guessing on the representations* forbids composing one.
The export centred on a person who **has** that relationship is what shows how Geni writes it.

**The tail, counted off `paths/harvested-path-geni-*.tsv` on 2026-09-13.** The whole distribution
is 33 distinct strings; these are the ones below the common six and their gender variants:

    134  her adoptive mother        3  her child            2  his/her father
     18  her ex-husband             3  his ex-wife          2  his parent
     15  your relative?             3  his fiancée          2  her ex-partner
     11  his partner                1  his child            1  his adoptive mother
      5  his/her parent             1  her partner          1  his adoptive father
      4  her fiancé

**⛔ THE URGENT ONES ARE THE UNATTESTED ONES, and there are two kinds.**

* **fiancé / fiancée — 7 rows, and `ENGA` occurs ZERO times in this corpus.** There is no shape to
  copy, so they are currently emitted as a couple with no marriage event. This is the case Emma
  described exactly: *"if there's some relationship that is only present in one spot, we have to
  do a `Forest` export on that point in order to get that relationship so we know how to
  represent it."*
* **`your relative?` — 15 rows.** Geni itself is not naming the relationship, so a `Forest` on
  those people is the only way to find out what the link actually is.

**Already attested and needing no export** (`devlog.md` 2026-09-13 carries the measurements):
adoptive → `FAMC` + `2 PEDI adopted` + `1 ADOP` + `3 ADOP BOTH`; ex- → bare `1 MARR` with bare
`1 DIV`; partner → a `FAM` with no `MARR`. `foster` is attested 781 times in the corpus and
appears in **no** path string, so it needs nothing until one turns up.

Pairs with these relations are in `reports/path-chains.tsv`; the person to centre the export on
is the one the tail word describes.

## Names

Remember that this is not something to be done out of order, it is the second last item in the queue for a reason

We are still generating non-name items as names such as numbers, and I think https://www.wikidata.org/wiki/Special:Contributions/OBender12 is likely pretty pissed at this point, but no talk page messages yet. idk why you did not fix it and seem to have completely overlooked the error that he constantly corrects. There are plenty of non-name things that need to be parsed not as names.

Read "address_this.html"

### Examples

Even in the current batch one exists lol

# und -- family, 8 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "und"
LAST	Len	"und"
#   set the mul label to "und"
LAST	Lmul	"und"
#   set the en description to "family name"
LAST	Den	"family name"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q61139384 Mangold von Thurgau und Nellenburg III: P734 family name = the item just created
Q61139384	P734	LAST	S2600	"6000000004106003883"
#   Q81827036 Adalbert von Saffenberg und Norvenich: P734 family name = the item just created
Q81827036	P734	LAST	S2600	"6000000009305060696"
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
overrides other things"* -- <https://www.geni.com/people/Ingemund-Grimsson-I-R/6000000227816621867>

All three submitted 2026-09-18, confirmed by his own name in the
*"... GEDCOM File is Being Created"* heading rather than by the page text, which lies:

    Forest       23:09Z   went out inside the created-today batch
    Ancestors    23:16Z
    Descendants  23:17Z

None of the three returns a task id -- see § A FOREST SUBMIT HANDS BACK NO HANDLE in
`scripts/forest-created-today.js`. They come off <https://www.geni.com/gedcom> when rows appear.

## Descendants campaign on Inal Kut Chor `6000000035218736073` -- QUEUED, starts when the
## created-today Forests are dispatched

Ruled 2026-09-18, in the same breath as the Ingemund elevation:
*"once this is finished start a descendants campaign on ... Inal-Kut-Chor"*. So it follows the
batch rather than interrupting it, and Ingemund overrides both.

`docs/monte-carlo-procedure.md` unchanged: frame, denylist, 40 candidates, every reading at or
above 4,000 exported off a created ancestor, the root stops on a round that returns none.

⛔ **AND THE FRAME IS BUILT FRESH, NOT READ OFF DISK.** `reports/descent-from-6000000035218690155.csv`
is a DIFFERENT person. Abul Hamza's roster was six days stale on 2026-09-18 and hid 71
generations -- round 3 read zero against a top of 618, and the same sweep on the rebuilt frame
returned a 15,000 cap hit. A stale frame reports a root as finished when it is not.

### ⛔ THE COLLECTOR IS LEFT WITH `mcThreshold` 99999999. RESET IT TO 4000 BEFORE ANY SWEEP

Set 2026-09-18 so the Inal Kut Chor census could run readings-only while Geni refused every
export. **A sweep dispatched on top of it will read forty pages, fire no climb, and report no
hits -- which is indistinguishable from a root that is finished.** That is the exact shape of
failure that closed Abul Hamza twice on a stale frame the same day.

`{type:"montecarlo"}` sets it from `threshold`, so any normal dispatch clears it. Nothing else does.

### Owed on Inal Kut Chor `6000000035218736073`, round 1

- `6000000048540306833` read **5,174** -- owed a climb and a `Descendants` export off a created
  ancestor. Round 1 is NOT closed; round 2 follows once this is worked.

### Owed from 2026-09-18, blocked on the export refusal

- **Ingemund Grimsson `6000000227816621867`** -- Ancestors, Descendants, Forest. ELEVATED.
- **14 of the 19 created-today Forests** -- `reports/created-today-2026-09-18.tsv`.
- Check the year counter on <https://www.geni.com/gedcom> first. A submit that does not move it
  was refused, whatever the page says.

## ⛔ NEXT CAMPAIGN AFTER THE CURRENT WORK -- `NN NN` `6000000227822546944`

Ruled 2026-09-19: *"future campaign after these is forest + descendant + descendant campaign
monte carlo on is one ... remember monte carlo on all recorded descendants of them in the
synoptic tree and building over time the ultimate one"*.
<https://www.geni.com/people/NN-NN/6000000227822546944>

Three steps, in this order:

- **`Forest`** on `6000000227822546944`
- **`Descendants`** on `6000000227822546944`
- **the Monte Carlo**, `docs/monte-carlo-procedure.md` unchanged -- 40 candidates a round,
  threshold 4,000, every hit climbed and exported off a created ancestor, the root stops on a
  round that returns none.

⛔ **THE FRAME IS EVERY RECORDED DESCENDANT IN THE SYNOPTIC TREE, NOT THE BALL.** The sample is
drawn from `scripts/descent-from.py` over the corpus -- all of them, as the tree holds them --
and the trunk cut applies if it comes back DEEP. It is built FRESH at the time, never read off
disk: Abul Hamza was sampled for three rounds against a roster six days stale that held 45
generations where the corpus held 116, and closed twice on it.

⛔ **AND IT ACCUMULATES.** *"building over time the ultimate one"* -- the frame grows as balls
land, so each round is drawn against a larger descent than the last. The denylist rebuild in
step 2 of the procedure is what keeps that from re-sampling ground already taken.

---

