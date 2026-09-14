# The descendants campaign — the only task

**⛔ COMPLETE, 2026-09-14. ALL SEVEN ROOTS CLOSED ON THE STOPPING CONDITION.** Each one had a
round of forty that returned **zero** candidates at or above 4,000 — the given condition, not a
read of a distribution and not a judgement that a root looked finished.

    root         closing round                     what it gave
    Aztec        round 2, top 1,800                10,861 new over four balls
    Inca         round 1, top 2,204                nothing -- 85% already held
    ben Ovadya   round 2, top 1,555                 8,340 new over two balls
    Adasi        round 2, top 1,119                   830 new over one ball
    Abul Hamza   round 2, top 1,662                 4,241 + 2,874 = 7,115 new
    Jimmu        one reading of 3,190               nothing -- trunk 99.5% blocked
    Chinese      round 2, top 228                   1,208 new over two balls

    plus Emma's two ad-hoc requests: NN Sanches 951, NN 6000000227739695943 412

    corpus 1,645,725 -> 1,675,442        29,717 new people

**The cron that drove this is deleted.** What follows is the record of how it ran, kept because
the same loop will be wanted again.

**Ruled 2026-09-13.** *"Your entire purpose is now to complete the descendants campaigns... All
you are doing is the descendants campaign. And the descendants campaign is relatively simple, and
it's something that should be done essentially without much intervention from me, without much
judgment. All it is is you simply do this thing. You download them, put them in, and each file
that you put in, you commit and push to the remote. That is all that we are doing in this task."*

---

## ⛔ WHY THE GENERAL-PURPOSE CRONS WERE KILLED

*"The cron jobs are not specialized to this task and they are going to be giving bullshit... for
the more agentic tasks, the general purpose cron jobs just kinda fail. The big problem is
essentially the cron job tells you to look at the queue, and then you look at the queue and you
find something unrelated, and it distracts you from it."*

Four recurring jobs — work-loop, auto-flush, status report, dead-queue sweep — were deleted on
2026-09-13 and replaced with **one**, firing on the hour and the half hour, which says only:
*here is the task, continue it.* The failure it fixes is real and happened repeatedly this
session: a cron that says *read `queue.md` and take the top item* sends the reader into a
1,600-line file, and the reader comes out working on something else.

**When the campaign is finished, that cron is deleted and the normal workload resumes.** That is
part of the instruction, not an afterthought.

## THE LOOP

    1  take the top owed row of reports/export-queue.csv
    2  refusal-check it: fetch https://www.geni.com/gedcom/export/<id> and confirm it does
       NOT say "You are not allowed to export that profile" -- a refusal holds the serial
       slot for an hour. Skip for a profile created this session.
    3  submit it
    4  POLL https://www.geni.com/gedcom/download?task_id=<task id> every 20 seconds
    5  when it says "Download My GEDCOM File", click it -- a real mouse event, see below
    6  unzip, file under exports/ as a NEW file, never overwriting
    7  scripts/measure-export-newness.py on it
    8  append the row to reports/descendants-export-log.csv
    9  commit and push -- ONE COMMIT PER BALL
    10 back to 1

## ⛔ AN EXPORT TAKES 6 TO 15 MINUTES

*"Exports are supposed to take about six to fifteen minutes, and climbs should be taking maybe
five minutes tops."* Measured against that on 2026-09-13:

    Chinese Forest        requested 18:51   downloaded 19:25   34 min
    Chinese Descendants   submitted ~19:29  downloaded 20:21   52 min

**Both balls were ready long before they were fetched.** The extension's watcher captures the
`task_id` and hands off; nothing polled afterwards, so the ball sat finished while the clock ran.
*"The issue is that you weren't paying attention, and all of these exports are really quick."*
**An export that appears to take longer than fifteen minutes means nobody is looking.**

**The download is a URL, not a hunt.** The dashboard icon is bound to
`downloadGedcom('<task_id>')` and resolves to `https://www.geni.com/gedcom/download?task_id=<id>`.
A JS `.click()` fires nothing — the handler is bound through `data-onclick-bound` and needs a
real mouse event.

## ⛔ A LONG CLIMB IS A PROPERTY OF THE SUBJECT

The climb walks up looking for somewhere to attach a created ancestor and declines anyone who
already has both parents (`both_present`). A densely documented line never stops declining:

    279  Marguerite de Valois, duchesse de Berri      95  Victor Amadeus I of Savoy
    239  Christine de Medici                          90  Benedicta Henrietta of the Palatinate
    162  Eleonore d'Orleans                           72  Sophia Dorothea of Hanover
    113  Katharina von Honstein-Klettenberg           64  Charles Emmanuel I of Savoy

Every one is European royalty. An ordinary person climbs in a few steps, which is the five
minutes expected. **A climb still running after that is walking an aristocratic line, and it must
not be waited on silently.** A stalled climb shows as `running: false` with `creating` still set;
only `{type:"load"}` clears it, never `{type:"stop"}`.

## THE ORDER

Re-ruled 2026-09-13: *"the Aztec and the Inca are probably highest value added. And then after
those ones are complete, then the Jewish one, the ben Ovadya one."*

    1  Aztec           Forest on 6000000209721868822, then Monte Carlo; plus the 5,086 banked
                       hit 6000000021665410212
    2  Inca            more Monte Carlo rounds
    3  NN ben Ovadya   more rounds, pool 28,124
    4  Adasi           the 15,000 cap hit 6000000008826548841 and the 6,975 6000000015507447504
    5  Abul Hamza      d'Esneval 6000000227739018883, Bettencourt 6000000227738961944,
                       then a Monte Carlo on her
    6  Jimmu           its first Monte Carlo
    7  Chinese root    further Monte Carlo rounds only

**The Chinese root is done for the purpose it was urgent for.** *"The important part of the
Chinese stuff was just putting all this stuff into the privileged section."* Both its `Forest`
and its `Descendants` are in `exports/post-merge/` as of 2026-09-13, so it drops to last.

**Dropped and not to be re-derived:** Genghis, Confucius, NN Näf, `no-name`
`6000000000183188387`, Dál Fiatach. **Postponed below the seven:** Hermenegildo, Narayana, Fihr.

## ⛔ THE EXPORTS ARE WORTH LESS ATTENTION THAN THEY HAVE BEEN GETTING

*"The exports are good, but... these exports are probably worth a bit less than you are putting
attention onto them."* File it, measure it, commit it, next. A ball arriving is not an event.

## WHAT IS NOT IN SCOPE

Not `queue.md`, not queue sweeps, not status reports, not the tiny-GEDCOM relationship work,
which is at the end of `queue.md` and stays there. **The path request and chain harvest run
themselves** — 1,028 people and 2,056 HTTP requests with zero failures, 1,486 chains with zero
errors, reading their own target lists off disk in chunks — and need nothing.

## THE MONTE CARLO ROUND

`docs/monte-carlo-procedure.md`, unchanged: 40 candidates, the trunk cut as the frame,
`--list-saturated` as the denylist, **every reading at or above 4,000** gets a climb and a
`Descendants` export off the created ancestor, and the root stops when a round returns none.

**⛔ DUMP A SWEEP'S CENSUS RESULTS TO DISK BEFORE ANY `{type:"load"}`.** It clears `results`. One
round's readings were lost that way on 2026-09-13 and the 4,459 candidate went with them.
