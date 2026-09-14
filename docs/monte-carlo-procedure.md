# The Monte Carlo round — the procedure, with no discretion in it

**Written 2026-09-13, after the campaign was diagnosed:** *"I think the failure mode of the
Monte Carlo campaign was that you did too much of your own judgment, because it was supposed to
be strictly organized and scope limited."*

This is the sibling of `docs/collector-run-loop.md` and it is load-bearing for the same reason:
`scripts/monte-carlo-pick.py` was kept dumb by an explicit rule — *⛔ THIS SCRIPT MUST NOT GET
CLEVERER* — and **the judgment moved out of the script and into the campaign around it**, where
no rule was watching. Every step below is fixed. Where a number appears, it is the number; where
a choice would appear, there is none.

---

## What went wrong, named, so the procedure can be read against it

**Seven properties were invented here as yield predictors and all seven were refuted:**

    descent already held            refuted -- Charlemagne is complete for being documented,
                                    not for being large; ruled by Emma
    the first two steps' returns    refuted
    pool size                       refuted
    the first sweep's top reading   refuted -- uniform framing, see below
    the census count                refuted
    the climb's decline count       refuted -- Corday declined 2 and returned 2 new
    `--descent` reading zero        refuted -- Sayaluna cleared at 0 held and her ball
                                    returned 20 new; zero means we lack the STRUCTURE

**Effort went where a judgement sent it, not where the roster did.** Of 27 Monte Carlo balls,
**19 went to three roots** — no-name 8, Dál Fiatach 7, Hermenegildo 4 — while Genghis, the Aztec,
Confucius and Jimmu had **zero**, because half the roster had fallen out of `queue.md` and
nothing checked the file against the roster.

**Roots were declared finished from one slice.** § *A LONG-HORIZON INSTRUCTION IS NOT ANSWERED
FROM THE FIRST SLICE* already says this and it happened anyway.

**And an instruction was replaced by a derivation**: told *full three-step* on the Chinese root,
I read the directory, found balls, and wrote that it "now means more Monte Carlo rounds".

---

## THE ROUND

**A round is 40 candidates. Not 30, not 60, not "until it looks done".**

    1  FRAME       the trunk cut, always -- scripts/trunk-roster.py over the root's descent.
                   Never the raw descent. Uniform sampling of a deep root reads the tail:
                   Huaxu's 156-generation descent read `top 43, zero hits` uniform and
                   9,265 / 6,802 / 6,793 trunk-restricted, same person, same day.

    2  DENYLIST    scripts/ball-collision-check.py --list-saturated <the root's export dir>.
                   --list is NOT enough: --list-saturated adds every ancestor of everyone in
                   those balls, which is what makes a fresh-looking pick actually fresh.

    3  PICK        scripts/monte-carlo-pick.py <trunk csv> 200, then drop denylist members and
                   duplicates and take the first 40. The filtering happens OUTSIDE the picker,
                   which is what `avoidFile` does inside the worker. The picker never learns
                   about it.

    4  CENSUS      enqueue 40 `stats` jobs, stagger 12000. A census read costs a real page
                   load -- `fetch` returns zeros because the stats block renders after load --
                   so a round is about eight minutes of page loads and that is the floor.

    5  EXPORT      every candidate reading >= 5000 descendants gets a climb and a `Descendants`
                   export off the CREATED ANCESTOR, per docs/export-seed-rules.md. Not the
                   candidate. Every one of them, in census order, no selection.

    6  FILE        each ball measured with scripts/measure-export-newness.py, appended to
                   reports/descendants-export-log.csv, committed.

    7  REPEAT      the next round runs with the denylist rebuilt from step 2. Nothing else
                   changes between rounds.

## ⛔ THE STOPPING CONDITION IS GIVEN, NOT DERIVED

**A round stops the root when it returns ZERO candidates at or above 5000.** That is the whole
test. It is not "the distribution looks like a cliff", not "the top reading is down", not
"the pool is exhausted", not a count of rounds — every one of those is a judgement and every
judgement of that shape made here has been wrong.

**A root is otherwise dropped only by Emma**, by name, and a dropped root is dropped and not
paused: nothing further is seeded, sampled or swept on it and it does not come back from
`reports/density.md` or any other derived list.

## ⛔ WHICH ROOT IS NEVER THE AGENT'S CHOICE

The order is `queue.md` § *THE WHOLE PROGRAM*, top to bottom, and `reports/export-queue.csv`
sorted by `priority` then campaign then walk. **If the queue and the roster disagree, that is a
bug in the queue and it is fixed by restoring the roster, not by picking.**

## ⛔ NEWNESS IS NOT ALWAYS THE YARDSTICK

On the Chinese root it is explicitly not: *"the forest export and descendants exports are both
probably going to be mostly the same and not introducing new people, but they are correcting
errors in the people."* A 0%-new ball there is a success. The newness column is recorded on every
ball and **acted on nowhere** — it does not gate a round, end a root, or choose a seed.
