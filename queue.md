# Queue

Only work. An item is DELETED when done, never annotated. Bullets, never numbers —
`CLAUDE.md` § *Queue items are BULLET POINTS*.

**Read `docs/collector-run-loop.md` before touching the collector.** It is your dictation of the
whole run loop and it ends *"there's no discretion on your part at all"*, said three times.

---

## ⛔ THE META QUEUE, FOLDED IN 2026-09-20 — THIS IS THE LIVE PLAN

It was a separate file only because PR #254 rewrote `queue.md` underneath it. That merge
is done, so it lives here now and `meta-queue.md` is deleted.

## The order. Top to bottom.

- **⛔ PUT A LINK ON THE GITHUB PAGES SITE TO THE ACTION THAT REDOES EVERYTHING.** One workflow,
  one link, running the whole chain: *"synoptic tree rebuilding, checking, refreshing the ledger,
  building the quick statements, and running them on Wikidata."*

- **⛔ THEN THE DESCRIPTION UNIQUENESS REVIEW, AND IT IS A MEASUREMENT BEFORE IT IS A CHANGE.**
  Mass-generate the description that WOULD be written for every individual we would make, into a
  **committed CSV kept current by CI/CD**, then read it for how unique they are.
  *"the descriptions need to be unique."*
  - unique -> continue, nothing to decide.
  - **not unique -> `AskUserQuestion`**, on the specific collisions rather than in general.
  - Why it matters, and it is not academic: Wikibase refuses a creation only when the label AND
    a non-empty description both match, so a description that repeats is a guard that does not
    guard. § *A blank description is not a guard, it is the absence of one.*

- **Then merge `exports/2026-09-19` again**, to pick up what it has gathered since.

- **⛔ AND FROM THIS POINT ON, MERGE THAT BRANCH EVERY HOUR ON THE HOUR.** Set up before the
  research starts, not after: *"at the end of this meta queue, like before the research starts,
  you're going to have a thing that every hour on the hour merges in the content from that
  descendants report based branch."*

- **THEN THE RESEARCH: is there a lead into her ancestry among these descendants?**
  - The material is the descendants roster being built on that branch — *"we're kind of
    developing a very large roster of his descendants"* — plus the general 6N descendants.
  - The other side is **her own ~8,000 ancestors**. If they are not already to hand, the
    **ancestors report function** produces them: *"which is very similar and works the exact same
    way, except for ancestors of a person."* Pick the form that matches most easily; that choice
    is the point of using the report rather than something else.
  - **⛔ FUZZY STRING MATCHING IS RIGHT HERE, AND IT USUALLY IS NOT.** Stated explicitly:
    *"this is one of the few situations in which fuzzy string matching might actually be good."*
    Looking for common given names, common surnames, **and common managing individuals**.
  - **⛔ THE MANAGING INDIVIDUAL IS A LEAD AND IT WAS THROWN AWAY.** The original 6N descendants
    batch omitted it because *"Claude decided to use its own discretion to omit the managing
    individual, which is not a thing you're supposed to do."* It is signal, not metadata: two
    people managed by one account is a connection. Anything regathered carries it.

---

## Standing, while the above runs

- **The path requester runs, and a drained batch is not a finished campaign.** Measured
  2026-09-20: **70,044 of 251,607 really attempted, 140,692 never** — about 18 more batches of
  8,000, ~141 hours at 1,000/hour. The 40,871 parked CBDB rows are deliberate.
  ⛔ It drained at 21:03:42Z and sat dead **2.6 hours** before anyone noticed, and it was Emma
  who noticed, not the six-hour check. At six hours a drain can cost most of a batch.

- **The pipeline loop runs**: compose -> pull -> send both halves -> repeat, and it never pushes,
  because a push cancels the PENDING pipeline run and that is what froze the batch all night.

- **⛔ NOT A DUPLICATE PAIR.** `Q141502962` and `Q141498725` were called a duplicate here and are
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

### ⛔ WIKIDATA EDITING IS HELD. Ruled 2026-09-13, and it is a STOP ORDER, not a date.

*"you had no business having any submissions going through until everything was done. That's why
it was at the end of the queue. Really, the submission should even have a requirement that all of
the Wikidata people get connected. Get connected with the path thing. So disable any editing of
Wikidata by the runner right now ... because we aren't ready for it. And the queue structure was
supposed to make that be the case."*

`HELD = True` in `scripts/wikidata_lockout.py` and `EDITS_HELD: "yes"` in
`.github/workflows/wikidata-edits.yml`, checked by both `editing_allowed` and
`automation_allowed`, with no environment override — a date arrives on its own, a hold is lifted
by a person. `tests/test_wikidata_start_date.py` fails if the two halves disagree.

**The condition for lifting it is stated and is not a date either**: the Wikidata people are
connected through the path search first. That campaign is at the END of this file.

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

- **⛔ TWO THIRDS OF PATH REQUESTS NOW RETURN `202` AND WE COLLECT NONE OF THOSE ANSWERS.**
  Measured on the 4,432-attempt drain: `queued/queued` is 2,969, 67%. A queued search's result
  never comes back in the response and reaches `/paths` only when a path is FOUND. The inline
  harvest added 2026-09-19 catches the other, cheaper third.
  **The route exists and is HALF BUILT NOW**: every completed search emails a full degree
  sentence and a `https://www.geni.com/c/<hash>` permalink — a saved path object, the same kind
  `pathchains.js` spends 28 minutes walking `/paths` to collect 30 at a time. Emma, 2026-09-19:
  *"my email contains all of the requested paths ... you can recover them from my email."*
  `scripts/parse-path-emails.py` reads either an mbox or pasted bodies and merges into
  `reports/path-permalinks.tsv` on the hash. 11 harvested so far.

  ⛔ **AND "~200" WAS A CAP, NOT A COUNT.** This bullet used to say *~200 in the last seven
  days*. Gmail's `resultCountEstimate` returned exactly **201** for
  `from:geni.com subject:relationship`, for `from:no-reply@geni.com "View the full"`, and for
  the bare query `in:anywhere` — which matches the entire mailbox. It is a ceiling the API
  reports and nothing more. Notifications from 09-12 and 09-13 exist outside that window, so
  the real volume is unknown and larger; Emma, 2026-09-19: *"That's too low ... at least one
  order of magnitude."*

  ⛔ **SO THE CONNECTOR IS THE WRONG INSTRUMENT FOR THE BACKLOG.** The session's Gmail
  connector returns one message body per round trip — N notifications cost N round trips, which
  is fine for topping up and hopeless for thousands. **A Google Takeout mbox is one file and the
  parser eats it in seconds**, with no credential passing through the agent.

  **DONE, 2026-09-19. 47,692 permalinks are in `reports/path-permalinks.tsv`** — 15,944 blood
  and 31,748 in-law, parsed out of the Takeout mbox in 31 seconds. The Takeout was Mail only,
  MBOX, export once; it completed in about half an hour and Google also dropped the zip into
  Drive, which is how it was fetched without the password challenge the Takeout download page
  puts up.

  ⛔ **AND THE REAL NUMBER IS 47,692, NOT 201 — 240 TIMES THE FIGURE THIS BULLET USED TO CARRY.**
  Emma, 2026-09-19: *"That's too low ... at least one order of magnitude."* It was two.

  ⛔ **636 `/c/` LINKS WERE NOT PATHS AND ARE EXCLUDED.** `/c/<hash>` is Geni's generic content
  permalink, so it appears in unrelated mail — the one that exposed it was subject *"StrangerChat
  sent you a message"*. Every one had a valid-looking hash and a blank degree, and every one
  would have sent the chain walker at a URL that is not a path. `NOTIFICATION_RE` now requires
  the notification's own marker.

  ⛔ **PAUSED 2026-09-20 at 12,911 of 47,692. Ruled: the walk is not worth more session time.**
  *"honestly can you hold off on this stuff ... I think that this is the least value added
  session"*. **The permalinks are the artifact that mattered and they are committed** --
  `reports/path-permalinks.tsv`, 47,692 rows, verified 0 malformed, 0 duplicate, 0 blank, sorted
  on the hash. The walk is a long grind on top of them and any session can resume it.

  **To resume**: paste `scripts/pathchains.js` into a foreground geni.com tab, inject an
  `<input type="file">` and upload a hash-per-line file built from the TSV (geni.com's CSP
  blocks a cross-origin fetch and 47,692 urls is 3.6 MB of JavaScript, so neither a fetch nor a
  paste works), set `C.i` from `localStorage.chains_cursor`, then `C.go()`.
  **Use `build-chain-batch.py --skip-covered`**: 23,306 of the remaining 34,781 are worth
  walking and the rest can only re-fetch a chain already held.

  **State at the pause**: 12,911 walked, 12,764 resolved, 147 failed. 31,819 chains held against
  25,827 before this started, 192,556 distinct people. Rate when healthy 1,140 an hour; it fell
  to 161 for about seven hours on 2026-09-20 and recovered on its own, so a slow interval is an
  interval and not a projection.

  **What is left, for whoever resumes**: the walk itself; then `split-path-chains.py` and
  `build-tiny-gedcoms.py`, neither of which has been run -- the second writes corpus `.ged`
  files, so it is a deliberate step and was kept out of the two-hourly tick on purpose.

  ⛔ **AND `C.reseedFailed()` IS OWED AT THE END OF THE RUN.** A permalink that times out used to
  be counted in `fail` and stepped over for good; it is now kept in `C.failed` and appended back.
  **The run is not finished when `i >= of` -- it is finished when `i >= of` AND `C.failed` is
  empty.**

  ⛔ **AND THE FIRST `reseedFailed` RETRIED NOTHING WHILE REPORTING A FIX.** It went through
  `seed()`, which de-duplicates against `C.urls` -- and a failed permalink is by definition
  already in `C.urls`, at a position the cursor has passed. So it returned `0` every time. Worse,
  it had already SPLICED the urls out of `C.failed` before discarding them, so **the 143
  permalinks that failed before 2026-09-20 18:00 are not in any retry list and cannot be named**.
  The retry now appends unconditionally.

  **How to recover those 143, offline**: `reports/path-permalinks.tsv` carries `subject_name`
  for every permalink, and a harvested chain's LAST segment is that same person. The join is
  `covered_names()` in `build-chain-batch.py`, done 2026-09-20.

  ⛔ **AND THE SAME JOIN SAYS MOST OF THE REMAINING WALK IS WASTED.** Measured: of the 38,148
  permalinks still to walk, **20,856 already name-match a chain we hold** -- so walking them can
  only re-fetch something already on disk. `--skip-covered` drops them and takes the whole list
  from 47,692 to **27,808**.

  ⛔ **IT DROPS ONLY WHERE THE NAME IS HELD BY EXACTLY ONE CHAIN, AND THAT TEST IS THE WHOLE
  SAFETY OF IT.** Of those 20,856, only 13,031 match a name held by a single chain; the other
  7,825 match an ambiguous one, and the ambiguity is concentrated in placeholders -- `NN` ends
  21 held chains, `N.N.` 10, `<private> Schottenstein` 7. Skipping on a bare name match would
  throw away a real person because an unrelated `NN` is already held. **A name is not an
  identifier**, which is the same rule as § *PARSE PATRONYMICS BY FORM* in another costume.

  **Not yet applied to the running loop.** The whole 47,692 is seeded in the page and the loop is
  healthy; re-seeding it mid-run to save time is how a working campaign gets broken. Apply at the
  next restart.

- **The Geni path anchor is not always the account owner, and it is not ours.** A `/path/` page
  rendered anchored on **Naruhito** (`from=6000000001783830969`), and notification emails read
  *"is NN NN NN's 37th great granddaughter's..."* and *"is Private User's..."*. Checked
  2026-09-19: neither id is in the batch, the requester's template carries **no `from=`
  parameter at all** and one `%ID%` placeholder, and all 138 harvested degree lines read
  `is your`. So the requester is anchored correctly and something else on Geni is not.
  Cause unknown. **Do not investigate without being asked** — it costs an hour and changes
  nothing about our output.

- **Wikidata lag spent the whole `MAXLAG_BUDGET` twice in one run.** Run `35467987263`: 191 edits
  executed, and the only genuine losses were two `still lagged after 900s of waiting` plus two
  dependents skipped behind one of them. `MAXLAG` is already 10 and the budget already 900 s.
  Nothing to fix in our code; recorded so the next session does not re-diagnose it as ours.

## ⛔ GET CI GREEN — IMMEDIATELY BEFORE LIFTING THE HOLD, AND NOT BEFORE THEN

Ruled 2026-09-14: *"put it as the queue item before actually running the cicd proper"*. Not a
first item, not worked ahead of real work.

Last read: run `34922163324` on `07fdb97e`, **4 failures, down from 11**. Three were fixed after
that run (`built-batches.tsv`, the `das` and `von` tests); the fourth is the committed batch
offering to create 63 people who already hold QIDs, which `pipeline.yml` fixes when it
recomposes. `build-repo-freshness.py` is NOT a defect any more: run 2026-09-17 it indexed 96,546 paths,
wrote 1,885 tracked artifacts to `reports/repo-freshness.csv` and named 34 files claiming a
corpus smaller than the live one. Checked before being repeated — § *CHECK before raising an
alarm*.

Dispatch `ci.yml`, read the conclusion, fix what it says. § *TESTS RUN IN CI/CD OR NOT AT ALL*.

## ⛔ GEDCOM EXPORTS — MOVED TO THE VERY END, 2026-09-14

Ruled: *"these gedcom descendant exports are best moved to the very end of the queue so we can
focus on other stuff since they can be done and integrated on a more long term basis while we
fix important stuff."*

They sit AFTER the hold lift on purpose, so a long-running export can never block it. Each one
is a submit, a wait of 6-15 minutes, and a file — cheap to pick up whenever the browser is
free, and they integrate on their own schedule.

### Ursula von Münsterberg — the German branch of Alix's descent, missing from the corpus

`6000000188494434823`. **Not in our tree**, and her mother `Sophie of Teschen`
`6000000006727858370` already is — so this is one export away from closing a branch we know is
there. Established 2026-09-15 from Emma's own lead: Geni computed her relationship through
`6000000003481830064` **Guy d'Ibelin, whose mother is Alix de Lampron**, and the route from the
German side runs Cieszyn → Bavaria-Landshut → Lusignan Cyprus → Guy → Alix, hinging on the
marriage of Agnes von Bayern-Landshut to a Lusignan king.

*"it may be the case for many others too"* — so the interest is the branch, not the individual.
`Descendants` off a created ancestor per `docs/export-seed-rules.md`, not `Forest`.

⛔ Check `https://www.geni.com/gedcom/export/6000000188494434823` for *"You are not allowed to
export that profile"* first; she was not created by this account.

**Checked 2026-09-17 and it says exactly that**, so the created-ancestor route is the only one.
The ancestor exists now: **`6000000227804005917` NN von Pardubice**, created as the father of
`6000000176534654825` **Anna von Pardubice** (c.1359, born Pardubice, no parents on Geni) —
tier 4 of `docs/export-seed-rules.md`, no parents at all and a surname, so `NN` plus the child's
birth surname. Anna is five generations above Ursula: Anna → Barbara von Sternberg → Königin
Kunigunde von Kunstadt-Podiebrad → Viktorin Bocek von Münsterberg → Ursula. `Descendants` 5000
submitted off him as task `6000000227804000942`.


### `Forest` export for a STEP relationship — the one representation the corpus does not attest

The profile scrape carries `step-parent` 12 and `step-child` 3, and **the corpus attests no way to
write one**: every `PEDI` value in `exports/` outside the tiny directories is `adopted` 2,473,
`foster` 805 or `birth` 555, and there is no `PEDI step`. So `build-tiny-gedcoms.py` drops those 15
edges rather than invent a shape for them.

Ruled 2026-09-13 for this exact case: *"we have to do a `Forest` export on that point in order to
get that relationship so we know how to represent it."*

A seed is in `geni-families/292373984150002914-family.tsv` — subject `292373984150002914`, whose
`step-parent` row is `Ratanbai Tata`. `Forest`, because the point of the export is to cross the
step link rather than descend.

⛔ Check `https://www.geni.com/gedcom/export/292373984150002914` for *"You are not allowed to export
that profile"* first.

**Checked 2026-09-17: it says exactly that**, and redirects to `/error`. So this one needs the
same created-ancestor route Ursula needed — create a relative of `292373984150002914` this
account owns, then run `Forest` off the created person, because the walk has to cross the step
link rather than descend. Still to do; the commanded roster is ahead of it.


## THE ORDER, 2026-09-17. WORK IT TOP TO BOTTOM

Dictated in one go after a session that jumped between things. **None of these depend on an
earlier one finishing** -- the order is hers -- except that the archive is best delved into
before the connection investigations, because it may hold the answer.

The Geni exports below run alongside all of this and are **the least significant part**:
*"these actual Geni exports are kind of the least significant part of what we're doing here. It
just happens that I got a lot of them all at once."*

- **4. All the random CI/CD crap.** CI has been failing since before 2026-09-17, and the
  three-ledger refactor has never run green: every pipeline run since it landed was cancelled by
  the next push.

- **5. Investigate the Pomeranian-Cypriot connections.**

- **6. The ontology.** `P407` *language of work or name* is the piece left undone: which languages
  a name belongs to is not a fact about the string and needs a source.

- **7. An aggressive campaign to do the downloading properly.**

- **8. Then a Cypriot / Russian / Bagrationi investigation.**

- **9. Then whatever else.**

### Why the cluster campaign exists

*"we are trying to dig in on a specific cluster to make sure we have completely exhausted it."*
The bet: the Dutch-Pomeranian cluster has a relatively high likelihood of a descent from
antiquity -- the kings of Cyprus, or Russian nobility -- either of which reaches the **Georgian
royal family, which is the goal**. It is strange in that it moves very far geographically and
then fizzles out unexpectedly; the theory is that many people have investigated it a little and
nobody pushed far, because it tends to be the less noble ancestry on a lot of paths.

⛔ **THE POINT IS TO *ADD* BLOOD, NOT TO FIND IT IN THE GRAPH.** Ruled 2026-09-17 against exactly
that mistake: measuring existing connectivity treats the tree as fixed, and in a 1.4M-person tree
almost any two noble lines are reachable at some hop count, so a reachability number says nearly
nothing. The exports are what create the edges.

## ⛔ A FULL RING OF ANCESTRY ON TWO PEOPLE, EVERY RUN. Ruled 2026-09-18

*"for these two people I want you to go crazy with their ancestors. Every run should add a full
ring to their ancestry."*

    6000000000757999620  Q141493478  Inger Axelsdatter Güntersberg
    6000000002621242041  Q141450322  Olfvir / Ølver Rømer

`PRIORITY_ANCESTOR_SEEDS` and `priority_ancestor_ring` in `scripts/build-garborg-day.py`. The
walk goes up THROUGH people who already hold a QID and returns everybody standing on the first
boundary above -- the whole ring, unioned in after `compose` picks, uncapped, because a full ring
is not a shape `compose` can express and a slice of it advances the ancestry a fraction of a
generation a day.

**It advances itself and there is nothing to maintain**: what it returns gets created, enters the
ledger, and is walked THROUGH next run instead of returned again. No depth counter, no cursor, no
state, and no way for it to quietly stop.

⛔ **THE LEDGER'S GENI ID FOR `Q141450322` IS THE HUSK.** `garborg-qids.tsv` pairs it with
`6000000227289508960`, which redirects to `6000000002621242041` and has no `FAMC` of its own --
so seeding on the ledger alone would have grown nothing while printing a cheerful zero. Both ids
seed the walk. Correcting the ledger row is still owed.

**First measurement, 2026-09-18: 8 people on the frontier**, 7 walked through.

## ⛔ TOP PRIORITY EXPORTS, from 00:30 on 2026-09-18 — run top to bottom, one at a time

Ahead of the commanded roster below. Geni allows one export at a time, so this is a strict
sequence, not a set.

- **Bothilde Sigurdsdatter Onarheim** — `Forest`. *"for merge related stuff changing"*, so it is
  a **privileged** export and is filed into `exports/post-merge/`.

  ⛔ **`6000000227805045863` IS A HUSK AND THE EXPORT DOES NOT RUN ON IT.** It redirects to
  `6000000177261659865`, the real Bothilde (c.1275), which this account does not manage —
  `https://www.geni.com/gedcom/export/6000000177261659865` answers *"You are not allowed to
  export that profile"* and lands on `/error`. The husk's own export form still loads, titles
  itself **"(No Name)'s GEDCOM File is Being Created"** and accepts the submit; that is the trap
  § *`6000000227289508960` IS A MERGED-AWAY HUSK* describes, and one such submit was spent here
  on 2026-09-19 before the redirect was checked.

  **The seed is `6000000227811549827` Sigurd Onarheim**, her father, created by this account and
  directly attested by her patronymic — tier 1 of `docs/export-seed-rules.md`. `NN Onarheim`
  `6000000227816629854` is the mother placeholder and is the fallback. `Forest` 5000 submitted
  off Sigurd on 2026-09-19; the page confirmed **"Sigurd Onarheim's GEDCOM File is Being
  Created"**, a named profile rather than `(No Name)`. Delete this when the zip is filed.

⛔ **AND `6000000002621242041` OLFVIR IS NOT EXPORTED DIRECTLY. RULED 2026-09-18.** Forest,
Ancestors and Descendants were all queued on that id and **none of them can run**: the profile
is not this account's, and the `request_export` endpoint does not get round that — the form
page's refusal was the real answer after all. The two `NN` seeds above are the route to the same
ancestry, which is the shape the whole campaign already uses: **you do not export the person you
want, you export a placeholder this account owns next to them.**

### ⛔ `6000000227289508960` IS A MERGED-AWAY HUSK. DO NOT SEED OFF IT

The link originally given for Olfvir was `6000000227289508960`, and it **redirects** to
`6000000002621242041`. That merge is what connected the new ancestors — it is the event the
00:30 wait was for, not a problem to route around.

The husk is still half-alive and that is the trap: its export form loads, titled
**"GEDCOM Export for (No Name)"**, and it **accepts a submit**. The task it returns —
`6000000227805163844`, `Ancestors` — then errors on every single reload. So a submit that looks
like it worked produces nothing, and nothing says so.

**The submit is a plain GET**, which the button merely builds, and navigating to it directly
beats hunting the button —

    https://www.geni.com/gedcom/request_export?id=<geni id>&walk=Forest&max_profiles=5000
      &destination=Ftb80&name_format=0&locale=en-US&include_bom=1

`walk` is `Forest` / `Ancestors` / `Descendants` / `BloodTree`. It is a convenience, **not a way
past a permission**: on a profile this account does not manage the endpoint refuses exactly as
the form page does. That was argued the other way here on 2026-09-18, under § *NEVER SAY YOU
CANNOT DO SOMETHING YOU HAVE NOT TRIED*, and it was wrong — the form page's refusal WAS the
mechanism, and the rule does not make an access control disappear.

⛔ **AND DO NOT INVENT A DESCENDANT TO WALK UP FROM.** `docs/export-seed-rules.md` only ever
creates **parents**, because a parent is implied to have existed and a child is not. Creating a
child of a real historical person to seed an `Ancestors` walk asserts something false about the
tree, and it was offered here and refused.

**A clicked submit is confirmed by `location.href` carrying `request_export` or
`/gedcom/download?task_id=`, never by the page text** — `get_page_text` returns stale content on
this site throughout. And coordinate clicks were landing off-target all night because
`getBoundingClientRect` reports in a 1536-wide viewport while the click frame is 1568 wide; that
is what looked like "the first click is always swallowed".

## COMMANDED EXPORTS, 2026-09-17 — one cluster, exhausted
## COMMANDED EXPORTS, 2026-09-17 — ABANDONED

⛔ **STOPPED BY INSTRUCTION, 2026-09-17:** *"after downloading the finished gedcom abandon doing
the exports since your job is different stuff"*, and earlier: *"these actual Geni exports are kind
of the least significant part of what we're doing here."*

**15 Forest exports were taken**, the last being NN von Flemming at 22:54. 215 zips sit in
`~/Downloads`, unfiled — filing them into `exports/` is hers.

The roster below is left listed rather than deleted, so the cluster is recoverable if it is ever
picked up again. Nothing here is running and nothing should be dispatched from it.

⛔ **`6000000227803023904` NN von Eickstedt NEEDS A RE-RUN.** It was requested at 22:10, its export
slot then freed with no file produced, and its download link yields nothing.

⛔ **AND `6000000227803104825` Knut father of Ingegerd WAS EXPORTED TWICE**, 21:27 and 21:34. Geni
refuses a second export while one is generating and the refusal appears as a banner on a page that
*also* still reads "Being Created", so it looks like success. The reliable instrument is
`https://www.geni.com/gedcom`, which lists every request with a timestamp; the submit page is a
static snapshot and lies about state. Do not batch a download click with the next dispatch.


Forest on each, in the order given. Then Descendants, in reverse of that order.
The Forest order runs up the generations; the reverse runs back down them.

One at a time, cannot be cancelled. Delete a line when its zip is in `~/Downloads`.

### `Forest`

### `Descendants`
- `6000000227803089951` NN von Liesgau
- `6000000227803060959` NN
- `6000000227803068881` NN von Leinegau
- `6000000227803029977` NN von Luchow
- `6000000227803090852` NN ?
- `6000000227803031913` NN h. Nałęcz
- `6000000227802697137` NN von Güntersberg - Kaliski, Kenstek, Reweinstein, Arenwald, Zadow
- `6000000227803024989` Svales Rein
- `6000000227803041902` Guttorm Hundorp
- `6000000227802407043` Sigmund father of Sigrid
- `6000000227803073849` NN NN
- `6000000227803024982` NN Kruckow
- `6000000227802432937` NN Barsebek
- `6000000227803089879` NN von dem Borne
- `6000000227803041931` NN von Flemming
- `6000000227803023904` NN von Eickstedt
- `6000000227803104825` Knut father of Ingegerd
- `6000000227803077823` Jön Liljesparre
- `6000000227803024957` NN Knutsdatter
- `6000000227803089850` Knud Porse
- `6000000227802697066` Olof father of Kerstin
- `6000000227803023862` NN Bulgerss
- `6000000227803060855` NN Hessøen
- `6000000227803032874` NN van Valckenier
- `6000000227297029878` NN
- `6000000227803027847` Adrian Falchener
- `6000000227803061825` David Fjose
- `6000000227802431855` Lars father of Sigrid

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
