/6000000227816621867>

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

