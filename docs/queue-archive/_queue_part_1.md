** `Q141502962` and `Q141498725` were called a duplicate here and are
  not one. Ruled 2026-09-20: *"that duplicate pair is not a duplicate pair. It seems to me that
  you kind of assume I'm not changing things when I am changing things. To my knowledge, there's
  no duplicate pairs anymore."* **The judgment that those become entry points stands** and is
  done. The error was reading a cached ledger as the live state.

---

## ⛔ EMMA'S OWN ITEMS, AND THEY COME FIRST

### ⛔ THE PATH COLLECTION IS A BACKGROUND ASSUMPTION, NOT THE FIRST ITEM. Ruled 2026-09-14

*"I think the paths collection being the first item made it so that you had a tendency to not do
other stuff... change up the queue item to make it be a background assumption that we are running
the path collection."*

**It runs. It needs no attention. It is not the thing you work on.** The requester and the chain
fetcher live in the geni.com tab, read their target lists off disk in chunks, and resume
themselves. Checking on them is not work; the only queue item about them is the restart check
pinned at the very end of this file.

State as of 2026-09-14: 8,000+ people requested with 12 failures, 2,150 chains fetched, 2,807
tiny path GEDCOMs, 773 isolates reached.

⛔ **PACE IT.** 500+ back-to-back census reads got the account CAPTCHAd on 2026-09-12. The stagger
is the extension's, never a sleep in the agent.

### ⛔ SKJALGSSON IS DROPPED. Ruled 2026-09-13: *"Drop skjalgsson please"*.

Not paused and not finished-by-measurement — dropped. Three balls are filed under
`exports/skjalgsson/` and they stay in the corpus; nothing further is seeded, sampled or
re-swept there, and its banked hit is spent. Do not re-derive it from `reports/density.md` or
from any roster.


They were sitting BELOW two sections headed *ALWAYS LAST* and *THE END OF THE
QUEUE*, which is how a list gets ordered by when a thing was appended instead of by
what it is. Ruled 2026-09-13: *"uhh why did you shit the bed so hard with queue
ordering lol"*. Anything typed here by hand outranks anything derived.

## Reference moved out of the queue, 2026-09-15

Three sections were **over half this file** and none of them were work. They are reference and
they now live in `docs/queue-archive/`:

    docs/queue-archive/always-last-the-tail.md       461 lines
    docs/queue-archive/the-algorithms.md             204 lines
    docs/queue-archive/the-end-of-the-queue.md       155 lines

Nothing was deleted. `queue.md` is work only — which is the whole reason § *Queue items are
BULLET POINTS* and the delete-on-done rule exist, and a file that is half reference defeats both.

## `emmas-files/` — HERS, AND NOT TO BE TOUCHED

She saves interesting paths by hand into `emmas-files/` and changes the anchor as she goes.
**Neither is to be reconciled, renamed or reorganised**, and an anchor change is not an event.
Explaining what is in there and how it relates to `geni-paths/` is still owed and is a long way
out; the prohibition holds until then.

This clause used to live inside the `/paths` harvest item. That item is finished, and the
prohibition is not, so it keeps its own place rather than leaving with it.

## Wikidata isolate connection — the standing background job

*"Actually connect the wikidata isolates I think we can just zoom through them by this point
with our pipeline we have"*

**It runs continuously.** `scripts/pathrun.js` in the geni.com tab, topped up every work-loop
tick; `CLAUDE.md` § *THE PATH CAMPAIGN RUNS IN EVERY SESSION, NO MATTER WHAT*. `attempt` is the
word, not `connect`: an isolate with no path is attempted and done.

⛔ **THE STAGE-3 GATE IS SUPERSEDED.** This section used to say Wikidata editing stayed held
until every isolate was attempted. Emma changed that 2026-09-14 — at ~900 requests an hour it is
months, and the isolate sweep needs a browser while the edits do not, so it made the slow half
the pacemaker for the fast one. The hold is lifted and CI/CD sends daily.

⛔ **AND THE "ATTEMPTED" COUNT WAS FICTION UNTIL 2026-09-15.** The roster read **262,908 of
262,908 attempted**; the real figure was **248**. `SEED_NEVER = 2026-01-01` marks *never
attempted* and fills the column, so a non-empty `last_attempted` never meant what it looked like.
Worse, 41,212 rows carried `2026-10-31` — which read as a date the script never writes, and the
30-day cooldown made every one ineligible until 2026-11-30.

⛔ **AND THE FIX FOR THAT HALF WAS WRONG AND IS REVERSED.** `2026-10-31` is
`park-cbdb-attempts.py` parking every CBDB person ON PURPOSE, because those profiles cannot be
edited — ruled 2026-09-15, *"If it's a stable two months into the future, for some reason, just
keep it."* `load_previous` reset them anyway, wiping all 41,212, and it incremented an undefined
name while doing it, so the first parked row it met raised `NameError` and took the whole rebuild
down. Parked dates are now carried through untouched and only an UNPARSEABLE value resets.
`attempt_ledger.stamp` still refuses to write a future date, which is the half that was right.

**Progress is measured by counting real dates, never by the column being filled.**

## ⛔ THE SIBLING SCRAPE CAMPAIGN — the next mass browser job. Ruled 2026-09-16

*"the list is something that we can do mass scraping on in the same way as the relationship
paths, although much more agentically due to dumb rules by the site."*

**What the list is.** `reports/sibling-pair-worklist.tsv`, now regenerated by `tree.yml` after
every rebuild. A path GEDCOM writes a sibling pair as a family with two `CHIL` and **no
partners** — Geni records no sibling edge, so a path can only ever say *these two are siblings* —
and the parents arrive from the members' own profile pages. The list is who still needs that.

**Why every member and not one of each pair.** Instructed, and it is not an oversight to optimise
away: scraping one side gets one side's account of the parents. Each member yields a GEDCOM
linking the pair as siblings *with* their parents, and the merge fuses the three on the Geni id
so the parentless family and the two parented ones become one family with real parents.

**⛔ AND IT IS NOT THE PATH CAMPAIGN'S SHAPE.** The path requester is one `fetch` per person
against a search endpoint, which is why 1,040 an hour is safe. This is a **real page load per
person** — `CLAUDE.md` § *a census read costs a real page load*, `fetch` returns zeros because
the stats block renders after load — and 500-odd back-to-back reads is what got the account
CAPTCHAd on 2026-09-12 and again on 2026-09-15. So it runs at the extension's pace, through the
extension, and the agent navigates and nothing else.

**What already exists to build on**: `scripts/write-family-scrape.py` writes the family file and
stamps `last_attempted` through `attempt_ledger`, and `build-tiny-gedcoms.py` turns
`geni-families/*-family.tsv` into `exports/tiny-profiles/*.ged`. The missing piece is the loop
that drives it over the worklist, which is the path campaign's `pathrun.js` equivalent.

⛔ **Do not start it while the path campaign is running.** Two browser loops against Geni is the
current load; a third doing full page loads is how the account gets CAPTCHAd.

## More items at the end

Do not fucking do this until after everything else is done but I want to review middle initial items since there are roman numeral related confusions with it. Middle initials do actually deserve their own items, but we are only gonna analyze this after everything else is done, so we can focus solely on this. Losses are a bigger threat than the gains are positive here.


## ⛔ RULINGS FROM 2026-09-15 — read these before working anything above

**⛔ DO NOT MEASURE THE VOLUME BEFORE DOING A SMALL THING.** *"don't measure the volume. We don't
need to measure the volume, and you measuring the volume is just going to waste time and cause
stress."* A census is for a question somebody asked, not a warm-up before every change.

**⛔ STOP GUESSING CONSERVATIVELY.** *"generally speaking, for most of your guesses, you've tended
to always guess the more conservative thing that I don't really fucking care about."* The Dutch
patronymics are the worked example: 90 occurrences, refused as too small, and the ruling was
*"under 100 total, do it."* When the choice is do-it or leave-it, do it.

**⛔ PATRONYMICS ARE DECIDED FROM THE FAMILY TREE, NOT FROM THE FORM.** *"patronymics are actually
extremely difficult to get wrong if you actually audit them ... I've been constantly telling you
that we have to be doing modeling based upon the family tree ... you just kind of never did it."*
`Eric` is a patronymic only if the father is `Er`, and he never is; `Nemanjić` is one because the
father is `Nemanja`. Refusing a whole family because its FORM is ambiguous is the error — 160 real
Slavic patronymics were being thrown away that way.

**⛔ A FUTURE `last_attempted` IS A DELIBERATE PARK, NOT CORRUPTION.** `park-cbdb-attempts.py`
writes `2026-10-31` on every CBDB person on purpose, because those profiles cannot be edited.
A previous version of `build-unconnected-worklist.load_previous` reset every future date to
`SEED_NEVER` and wiped all 41,212. Restored and re-parked 2026-09-15. *"If it's a stable two
months into the future, for some reason, just keep it."*

**⛔ DO NOT PANIC ABOUT ITEMS WE GOT WRONG.** *"it kind of sucks that we got some stuff wrong. It
would be nice if we make stuff self-healing, but don't fucking panic about it. These things can be
healed by other people."*

**⛔ TESTS DO NOT COUNT UNTIL THE QUEUE IS FINISHED.** *"literally test passing doesn't count, that
doesn't matter."* Do not dispatch CI, do not wait on it, do not report on it.

**⛔ THE FIRST THING IN A SESSION IS TURNING ON THE RELATIONSHIP REQUESTING**, and every even hour
at :45 the requested paths become TSVs in the repo. Both are in `CLAUDE.md`.

**⛔ `Q320139` ZERUBBABEL TAKES NO `mul` LABEL OR ALIAS** until 2027-09-15. `MUL_BLOCKED` in
`build-garborg-day.py`. The lapse is silent and that is intentional.

**⛔ `Q70899` ADAM HAS TWO GENI IDS ON PURPOSE.** `6000000201847373856` is qualified `P2868`
*subject has role* `Q2001710` **Adam in Islam**. Biblical figures accumulate profiles because Geni
disconnects them. We hold one profile; that one IS the profile and the other is never a conflict.

**CJK FROM THE PARTS OF A `mul` LABEL IS ON HOLD.** *"probably we put a lot of the CJK from parts
on hold generally. Because I don't think it's worth it."* The investigation is
`docs/cjk-from-name-parts.md`; do not build it.

## Owed explanations, 2026-09-15

Two answers Emma asked for and did not get:

* **Why the relationship-source backfill is stricter than the `P1810` one.** `S2600` means *Geni
  states this*. `P1810` copies a name Geni already gave, so it cannot be false. A source on a
  relationship Geni does not record WOULD be false, and it renders as a tidy Geni link either way,
  so nobody can see it is wrong. That is why every line is checked against `derived-family.csv`
  first.
* **What `ADJACENT_FLOOR` is.** The universe grows by editing its neighbours, and the pass queried
  our own 4,430 items before the neighbours — so the 60-a-day quota filled before a single
  neighbour was ever reached, and all four emitted files contained **zero**. The floor reserves 10
  neighbours per run so "our own items first" cannot mean "our own items only".

## ⛔ ERRORS FOUND 2026-09-19 — written down instead of chased. Ruled the same day

*"for every error that came up organize them into a queue"* — said after a session that
context-switched between five threads and cancelled 21 pipeline runs doing it. **These are
findings, not work in progress. Nothing here is started.**

- **`out/model-vs-reality-items.json` is 57.9 MB, tracked, and regenerated by the pipeline**
  (`model-vs-reality.py --refetch`). Already draws the 50 MB warning on every push. Needs +72%,
  so it is behind `name-item-languages.csv` in the queue and not behind it in kind.

- **`reports/tree-eccentricity.csv` is 84.3 MB, the largest tracked file in the repo.** Nothing
  `pipeline.yml` runs writes it, so it sits harmless until whoever runs `measure-eccentricity.py`
  pushes the result. That is a trap for a future session, not a live fault.

- **The repo-wide picture, measured 2026-09-19: nothing is over 100 MB anywhere.** The largest
  tracked file is **`preservation/genealogy/dropbox/ITIS.ged` at 91.3 MB** -- closer to the limit
  than anything above, and **harmless**, because preserved GEDCOMs are static and no workflow
  rewrites them. **Size alone is the wrong sort key.** What matters is whether something
  regenerates the file: one nothing rewrites sits at whatever size the last person left it,
  and one a workflow rewrites crosses the limit unattended, between two runs, with nobody
  watching.
  ⛔ **BUT THAT SAYS WHICH FILE WILL CROSS, NOT WHO IT KILLS.** Measured 2026-09-19 while
  building the check: **no workflow runs `refresh-live-values.py`, and nothing in `pipeline.yml`
  calls it** -- its six mentions in `build-garborg-day.py` are all prose telling a person to run
  it. So `garborg-live-items.json`, the 100.32 MB file that took the pipeline down, was never
  regenerated in CI at all. A session refreshed it and committed it, and from then on the
  pre-receive hook refused the pipeline's pushes, this repo's pushes, everyone's -- because the
  hook rejects a push for what the repository CONTAINS, not for what the push changed. Size
  alone is the failing condition; who writes it only says whether it will cross unwatched.

- **⛔ `CLAUDE.md` § *THE 45-MINUTE PATH TICK PUSHES* IS INCOMPLETE AND IT MISLED TWICE.** It
  explains cancelled pipeline runs as push contention, which is true and was not the whole
  story: a `timeout-minutes` kill and a supersede-on-push cancellation are **the same word in
  every listing**, and only the job's start and end times tell them apart. Two confident wrong
  diagnoses came out of reading the conclusion word on 2026-09-19. The section needs the
  distinction written into it.

-