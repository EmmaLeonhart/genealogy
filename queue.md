# geni — Work Queue


**This file is a queue of *concrete, executable steps*, not a state snapshot.** It lists what is being worked on right now. Finished work lives in `devlog.md` (a dated entry) and `git log`; longer-horizon, *abstract* work lives in `todo.md` and gets decomposed into items here when it's ready to execute. **When an item is done, delete it from this file AND append a dated entry to `devlog.md` in the same commit, then push.** Do not add checkmarks, "done" markers, or status indicators in place. If an item is still here, it is not done.

**Why this file exists:** when a planning step (formal planning mode or just "think before doing") produces a plan, that plan is written here BEFORE execution starts. That way an interrupted session can pick up from the queue rather than from chat context that may be gone.

The purpose of this file is also to bound scope. If a task is not in this queue, it is not in scope for the current session. New ideas go at the bottom of the queue (or to `todo.md` if they are longer-term / architectural), not silently into whatever is being worked on.

See `CLAUDE.md` § "Workflow Rules" for how this file, planning mode, and the task tool stay in sync.

**Three-cron playbook.** Extensive work runs under three local `CronCreate` jobs — **work-loop at :03** (the engine that drains `queue.md` and refills it from `todo.md`), **auto-flush at :15** (commit/push backstop), and **status-report at :42** (heartbeat). On a fresh session they are **started** as the opening step; on a mid-session **large-scale re-fill** of this queue the FIRST item worked is instead to **kill** the already-running crons. Either way the **last two items are always pinned at the tail** — ensure the three crons are running, then run an end-of-session summary (see the `## Always last` section below).

---

## Active

0.001 **BLOCKED-ON-USER-ACTION — the deferred compute from the 2026-08-06
   evening ingest. Unblock signal: Emma says the machine is somewhere it can
   spin up** (the batch was handled on a hot laptop with the fan audible in
   public, under an explicit instruction to document rather than compute).

   Ingest itself is done — four new exports in `exports/edges/`, two repeats
   identified and left in `~/Downloads`, cap raised to 4020, nine path pages
   converted; see `reports/audit-downloads-2026-08-06.md` and the devlog entry.
   What is owed, in this order:

   1. `py -m pytest` — the corpus is 103 GEDCOMs now. The one assertion at risk,
      `test_export_cap_is_at_least_the_largest_real_export`, is satisfied by
      construction (largest new export 4020, constant 4020), but that is an
      argument and not a run.
   2. `python -m genimerge merge` — gives the new-people count for the four, and
      refreshes `out/merged.ged`, which still describes the 99-export tree.
   3. `python -m genimerge density` — scores the prediction recorded in item 3
      below, that region 6 yields more new people than region 4 would have.
   4. Re-run the path/gap check in `reports/path-gaps-2026-08-06.md` against the
      new merge, to score the prediction that report records about which gaps
      the four new exports close.

0.000 The "FIRST ITEM" is finished — all 19 path files re-checked against the
98-export merge, `reports/paths.md` rewritten, devlog entry dated 2026-08-06.
Emma's update to the agenda of this project:

Big priorities:

1. Algorithmically finding the most remote individuals and then connecting all of them. Earlier one was random individuals which is not helpful, but that did not disprove our hypothesis on shortest path discovering new communities, we just chose things that were pretty central
2. Import the Hata clan. Surprised it is not all there already.
3. Ideally we want to connect all wikidata items with geni into this for our world tree

   **Priority 2 is answered, and the answer is no — `reports/hata.md`,
   2026-08-06.** Emma took a `Forest` export seeded on a Hata person the same
   afternoon (`exports/Hata/export-Forest-6000000210475738822.ged`, 4004 people,
   seed 酒君/酒公 /Hata/) and it settled the question against this repo's own
   prediction. The clan went 27 → 37 people and **all ten new people are one
   unbroken descent**; siblings across the whole clan stayed at 9, marriages
   stayed at 0, branch points stayed at 1. A `Forest` export follows spouse
   links and found none to follow. The one-hop neighbourhood ignoring names
   entirely is **four people**. There is no more clan to import: Geni records
   秦氏 as a line. Emma's call — *"likely definitively showing it is just a
   line"* — was right.

   The export paid on the other target anyway: 惟宗 2 → 8, 島津 51 → 92, and
   `reports/path-hata.md` **29/55 → 39/55**, closing all eight of steps 33–40.

   **What is left of that path is not Japanese and is not clan work** — sixteen
   steps, fifteen consecutive, being the Daniels / Searle / Merrell / Vories
   families in America up to the Hitotsuyanagi marriage, IDs in
   `reports/hata.md`. Step 9 is held and step 10 is his *brother*, so the
   doorway is a sibling link. Fifteen consecutive is past the 6–9 steps a
   targeted export has been observed to span, so it is two exports at least.
   **BLOCKED-ON-USER-ACTION**, unblock signal is a new `.ged` under `exports/`;
   seed **Enok Danielson `6000000004104838733`**, style `Forest` (steps 11, 13
   and 22 are marriages).

   Also worth recording as a method note rather than a task: **a clan name is
   not a clan.** Counting Hata-named people implied a population Geni does not
   record; the measurement that answered it used no names at all.

0.0 **BLOCKED-ON-USER-ACTION — save the path pages for the 18 people in
   `reports/remote-people.md`.** The list is ranked by eccentricity, each row is
   provably 77+ hops from every other row, and each carries a one-click Geni
   path URL in blood and in-law form. `out/remote-people.html` is the page to
   work through; re-open it with
   `powershell Start-Process out\remote-people.html`. Unblock signal is a new
   `.html` under `geni_pages/`, then for each one:

   ```
   python -m genimerge path-from-html "geni_pages/<saved>.html" -o paths/<name>.tsv
   python -m genimerge path paths/<name>.tsv --source out/merged.ged
   ```

   **"Read the first three before saving many" has now been answered, and the
   answer is stop.** Nine more pages were saved on 2026-08-06 evening and
   checked in `reports/path-gaps-2026-08-06.md`: across all 26 paths, **3 199 of
   3 464 steps held (92.3%) and 11 paths are complete end to end**, `gong-liu`
   at 249/249 among them. No path ends in a gap — every break is an interior
   bridge and the remote endpoint is already held. The stated fallback applies:
   **this instrument measures our tree's shape, not Geni's gaps**, and the
   effort belongs on `reports/density.md`.

   Emma's reading of *why* is supported by the concentration: 265 absent
   step-slots sit on 196 people, but 29 people carry 98 of them, and five
   separate paths break at the *same ten* Alemannians. Sparse ancient graph,
   connectivity through few individuals. **Saving more path pages is not the
   work; closing the two shared bridges is** — see item 2.5, now measured at
   five paths rather than the five it predicted, and the
   'A'idhullah al-'Ashiri `6000000226741965864` bridge, which is new.

0.05 **The P2600 overlap is measured — `reports/wikidata-overlap.md`,
   2026-08-06.** Emma's ask, answered: **9,026 in both — 4.44% of our tree,
   1.75% of Wikidata's 516,913 Geni-linked IDs.** 507,859 people have a Geni
   profile Wikidata names and no export here has reached. `genimerge overlap`
   pulls all of P2600 in sixteen MD5 partitions rather than asking about our own
   IDs, which is the only way to see that second number at all.

   **What came out of it that is work rather than a number: 44 Wikidata items
   carry two Geni IDs that are *both* people in our tree.** Our merge keys on
   the profile ID, so it cannot see this — two IDs are two people to it, by
   construction. Reviewing those 44 is a human job and is genuinely open:

   - It is **not** a duplicate list. `Брячислав Васильевич` against
     `Bracheslav Vasylkovich Polozki` is one person in two languages;
     `Scribonia` against `Clodia Pulchra` is two of Octavian's wives and one of
     those P2600 statements is just wrong. Both readings occur and nothing in
     this repo separates them.
   - **NEEDS-DECISION — what should happen to a confirmed pair.** Options are:
     record it in `entity_resolution.md` (Emma's scratchpad, which already holds
     hand-made identities); teach the merge an alias table keyed on profile ID;
     or leave it as a report and merge the profiles on Geni instead. The third
     fixes it at the source and the other two paper over it. Emma decides.
   - None of the 44 are Japanese emperors, so this instrument did **not** catch
     the Emperor Ojin duplicates in item 0.2 below. Worth knowing why: it can
     only see a duplicate that Wikidata has already noticed and linked twice.

   Smaller, and both are read-only findings rather than tasks: 67 Geni IDs sit
   on two Wikidata items (5 of them ours), and 28 P2600 values are not profile
   IDs at all — mostly pasted `geni.com/people/…` URLs. 24 have an ID inside,
   and recovering it is **UNSAFE-TO-GUESS** in one specific way the report
   names: a URL with `?through=` carries two IDs and the one after the `?` is a
   different person, so the obvious "take the last digit-run" links the wrong
   human.

0.1 I have done a large amount of exports that definitely fleshed out the trees based off of your suggestions, although geni seems to have crapped out a bit, so it's probably gonna be tomorrow. Integrate these things when they arrive. I feel like they're probably going to be the last because I don't know what's going on with geni right now, but it's a bit difficult to get things to run. 

   **Four of them arrived and are in, 2026-08-06 evening** — `exports/edges/`,
   seeds `…085797849`, `…085766947`, `…085871850`, `…085828865`, none of them in
   any earlier export. Two further zips in the same batch were byte-identical
   repeats of committed files. The *measuring* of what they added is item 0.001,
   which is waiting on a machine that can spin up. This item stays open because
   Emma's "probably the last" is a prediction about Geni, not a statement that
   the batch is closed.

0.2 As another thing, there were some profile merges and edits related to Japanese emperors, particularly Emperor Ojin, and I just want you to keep in mind that this is the case. You probably will be able to see it in the data somewhere. Not 100% sure you probably would, because there were duplicates of Emperor Ojin and some other people. 

1. **BLOCKED-ON-USER-ACTION — export from `NN 高円宮` `6000000209740059823`.**
   The one individual on `individuals I can easily export.txt` that is **not in
   the tree**, and it is not merely unmerged: grepping the whole repo finds that
   ID in no export, not even as somebody's relative. The other 17 are all held.
   That makes it the only entry on the list that is certain to bring material we
   have none of. Everything else there is a re-sample of a neighbourhood we
   already touched.

2. **Review and run `out/wikidata/entity-resolution.qs`.** Six P2600 statements
   and three English label edits from `entity_resolution.md`. All six Geni
   profiles are in the tree. **BLOCKED-ON-USER-ACTION** — nothing here sends
   anything to Wikidata, and label edits overwrite other editors' work.

2.5 **BLOCKED-ON-USER-ACTION — export from Louis I, The Pious
   `6000000001266578142`, style `Forest`. This now outranks the density picks
   below.** Measured 2026-08-05 in `reports/paths.md`: fifteen Geni relationship
   chains checked against the 186,551-person merge hold 1,095 of 1,227 steps
   (89.2%), and **50 of the 132 missing steps are the same ten people** — the
   Alemannian ducal line ascending into the Carolingians, blocking five separate
   paths that each run unbroken to step 34 and stop there. All ten verified
   absent by profile ID against `out/merged.ged`.

   **Re-measured 2026-08-06 over 26 paths and it holds up exactly** —
   `reports/path-gaps-2026-08-06.md`. The same ten people block five paths at
   the *identical* steps 35–44, doorway **Gisela of Friuli
   `6000000008592343633`**, first absent Berengar I (her father), resuming at
   Leutharis II. 50 step-slots for one export. **A second bridge of the same
   kind is now known and is not yet queued elsewhere: 'A'idhullah al-'Ashiri
   `6000000226741965864`**, 19 Jurhumid/Qahtani people, ~48 slots across
   `scorpion-i`, `pasuti` and `psamtik-ii`. Take it `Forest` for the same reason.

   It beats the density picks because the payoff is *observed*: Geni has already
   named who is behind this door. `Forest` because Giséle of Cysoing and Emma of
   Alemannia enter through marriages and a blood-only style walks past them.
   Ten people is at the edge of the 6–9 steps a targeted export has actually
   reached here, so it may take two.

3. **BLOCKED-ON-USER-ACTION — the next four exports, picked 2026-08-05 from
   `reports/density.md`.** Unblock signal is a new `.ged` under `exports/`. All
   four seeds were checked against `out/people.jsonl`: every one is in the tree
   and every one has empty `parent_ids`, so all four are doorways. **Take them
   as `Forest`.** These regions are runs of people linked by marriage as well as
   descent, and a doorway opens *upward*, so `Descendants` walks the wrong way
   and `Ancestors`/`BloodTree` walk past the spouse links — the same trap that
   nearly cost the Jimmu bridge.

   | order | region | people | doorways | density | ball fit | seed |
   | ---: | ---: | ---: | ---: | ---: | ---: | --- |
   | 1 | 6 | 2561 | 957 | 37.4% | 0.66× | [Christen Pedersen Thrane](https://www.geni.com/people/x/5132829956720138378) `5132829956720138378` |
   | 2 | 3 | 3588 | 977 | 27.2% | 0.93× | [William "Bill" Rankin Monk](https://www.geni.com/people/x/6000000005965721836) `6000000005965721836` |
   | 3 | 1 | 6475 | 1757 | 27.1% | 1.68× | [Juan Andrés](https://www.geni.com/people/x/6000000014746707044) `6000000014746707044` |
   | 4 | 2 | 3858 | 854 | 22.1% | 1.00× | [Mercy Swetland](https://www.geni.com/people/x/6000000014643729729) `6000000014643729729` |

   **Why this order and not simply largest-first.** An export is a ball of at
   most ~3860 people (`GENI_EXPORT_CAP`, largest yet seen), so a region bigger
   than that cannot be covered by one take — the "ball fit" column is
   people ÷ 3860. Region 6 is ranked first because the *whole* region fits
   inside one ball with room to spare and it has the highest doorway density in
   the report at 37.4%: the largest share of the budget converts into walking
   somewhere new rather than re-fetching people we hold. Region 3 is second on
   raw doorways (977, the most of any region that fits in a single ball).
   Region 1 has the most doorways of all, 1757, but at 1.68× it needs at least
   two exports and only one seed exists for it — take one now and **re-run
   `python -m genimerge density` before choosing the second**, so the second
   seed is picked knowing where the first ball landed.

   **What to skip, and why it is in the report at all.** Regions 35, 38, 40, 42
   and 47 have **zero** doorways — nothing there opens outward, so an export
   buys only people we already have. Region 8 (Fakhita القشيري, 2355 people) is
   the large low-density case at 9.8%: a whole ball spent to reach few new
   places. Region 4 (Jøran Svensdatter, 3563/612, 17.2%) is the weakest of the
   big four and is the one to drop if only three exports get taken.

   **This is the first pick density has ever made, and it is untested** — the
   same standing objection as `reports/seeds.md`, which has also never been
   scored against an outcome. It resolves by measuring: after the export lands,
   `python -m genimerge merge` gives the new-people count and re-running
   `density` should show region 6 shrink or split. Recording the prediction here
   so `git show` supplies it later — **region 6 is predicted to yield more new
   people than region 4 would have**, on the density argument alone.

6. **The Wikidata reports are stale.** `reports/wikidata-coverage.md`,
   `wikidata-crosscheck.md` and `names.md` describe the 16266-person tree; it is
   now 105349. Refreshing means `reconcile` against the live SPARQL endpoint,
   the only networked step here.

7. **`density` emits one seed per region, which under-serves regions larger
   than one export ball.** `_representative` in `src/genimerge/density.py`
   returns a single person; region 1 is 6475 people, 1.68× the ~3860 an export
   holds, so one seed cannot cover it and the report gives no second. The fix is
   to emit `ceil(size / GENI_EXPORT_CAP)` seeds per region, chosen far apart in
   the region rather than greedily by degree — otherwise two seeds land as
   neighbours and their balls are the same ball. Low priority: it only pays if
   more exports get taken, and queue item 0.1 says the current batch may be the
   last. Do not build it on the assumption exports continue.

### Standing context

- **BLOCKED-ON-USER-ACTION — impossible dates in the tree, listed in
  `reports/consistency.md`.** Someone born before a parent, or after their
  mother died. Every one is an error in Geni's data rather than in the merge, so
  fixing them means editing profiles on Geni; this repo will not change them.
  A further set are implausible rather than impossible — a parent under 12, a
  lifespan over 120 — and some of those will turn out to be correct.

  **This entry said 96 impossible and 89 implausible, "re-measured 2026-08-02
  over the five-export merge", until 2026-08-06.** The report says **3,189** and
  **1,966** over 202,433 people. The number was not wrong when written; it was
  left behind by 94 exports, which is what a count copied into prose does. It is
  not restated here now — **read `reports/consistency.md`**, the same rule
  `todo.md` § 3a already applies to `reports/frontier.md`.

  Worth doing before the QuickStatements batches rather than after:
  `add-claims.qs` carries P569 and P570 statements built from these same dates,
  so an uncorrected year here becomes a wrong year on Wikidata.



- **The Jimmu chain, 62/83 → 77/83 → 83/83, is finished and its long note is
  deleted (2026-08-06).** The note ended by saying it could go once nobody
  thought it load-bearing; the 99-export re-run holds both jimmu path files at
  **83 of 83**, so the arc is closed. What it taught survives in `CLAUDE.md` —
  read the relation column before choosing an export style, because two of the
  six bridging steps are reachable only through a marriage — and the numbers are
  in `devlog.md` and `git log`. A 21-step gap took four exports, not the one
  originally planned; that is the part worth remembering.

- **Not doing: centralising the per-module property constants.**
  `crosscheck`, `reconcile`, `namelinks`, `names` and `quickstatements` each
  declare the property IDs they use at the top of the file. That is local and
  readable, and a shared registry would move them away from the code explaining
  why they are there; `CLAUDE.md` already serves as the cross-module reference.
  Recorded so a later sweep does not re-open it as though it were an oversight.



- **NEEDS-INVESTIGATION — smallest-ball is the only ordering that surfaces the
  known-good seed, and it rests on one observation.** Hågen Iversen placed 38 of
  2336 by smallest ball, against 2261 by the shipped doorway count and 1303 by
  openness. The mechanism is plausible — a tiny neighbourhood is one we know
  almost nothing about — and the obvious objection turned out to be wrong, since
  the shortlist is 66 candidates with none isolated. It is **not** adopted and
  must not be until there is more than one data point. Resolves by taking one
  export from a top-ranked pick and one from the small-ball shortlist and
  comparing new-people counts. Not blocking anything.

- **NEEDS-INVESTIGATION — the seed ranking has never been tested.** No export
  has been taken from a seed `reports/seeds.md` chose. The one export with
  measured results was seeded on the parent of Hågen Iversen, who placed 2255 of
  2336 (ball 5, one doorway), and returned 3656 new people. That is a reason to
  doubt ranking by absolute doorway count — a large ball is a densely recorded
  neighbourhood, which is the opposite of where Geni has most to add — but it is
  n=1 and the ranking never scored the actual seed, who was not in our data. It
  resolves by taking the next export from a top-ranked pick and comparing. The
  prediction is already committed in `reports/seeds.md`, so `git show` will
  supply it when the fifth export lands. Not blocking anything.

- **UNSAFE-TO-GUESS — two links flagged as worth re-checking, both exact P2600.**
  `reports/wikidata-crosscheck.md` § "Links worth re-checking" names Canute I
  Erikska `Q442876` (0 agreements, 4 conflicts, birth 1145 against 857) and
  Bengt Folkesson `Q1621801` (1 agreement, 2 conflicts). Both are matched by the
  Geni ID on the item, not by inference, so the ID itself is under as much
  suspicion as the match. Two readings fit and nothing in this repo separates
  them: the link is wrong, or it is right and one side's data is badly wrong.
  Resolving one means a human comparing the Geni profile against the Wikidata
  item. Nothing should edit either side on a guess.

- **NEEDS-DECISION — how out-of-tree export seeds are found.** `reports/seeds.md`
  can only rank people already in the merged tree. Iver Mellegård, who seeded
  the best export so far, was in none of the three earlier exports, so the
  ranking could not have proposed him. Whatever route found him is one this repo
  cannot see or reproduce. **Seen twice now:** the 2026-08-02 seed
  `6000000226989731860` was likewise in none of the four earlier exports, and
  produced an export that overlaps them by zero people. Two of the five exports
  came from seeds this repo had no way to name. The question is with the user;
  the answer decides whether to build out-of-tree candidate ranking or something
  else. Not blocking anything currently queued.

- **Take the pipeline order from `README.md`, not from a list written by hand.**
  The README's "before pushing" block already gives every command in dependency
  order, and it says `expand --search`, not bare `expand`. Both details matter.
  `expand` writes `matched_all.csv` and `candidates.csv`, which `coverage`,
  `crosscheck`, `name-links` and `quickstatements` all read, so omitting it
  leaves four reports generated from a previous tree. And bare `expand` skips
  the label-index lookup that produces the `name-match` proposals — running it
  without `--search` silently drops 100 of them and rewrites
  `reports/wikidata-coverage.md` with 30 proposals instead of 87. That is not
  hypothetical: it happened on 2026-08-01 and was caught only by diffing the
  regenerated report.

- **`python` on PATH is not the interpreter.** Python 3.13.14 is installed at
  `C:\Program Files\Python313\python.exe`, but the Microsoft Store stub aliases
  in `WindowsApps\` come first on PATH, so the bare `python -m pytest` written
  throughout `CLAUDE.md` exits 9009 with "Python was not found". Use `py -m
  pytest` or the full path. The package is not pip-installed either; the CLI
  needs `PYTHONPATH=src` (pytest gets this from `pythonpath = ["src"]` in
  `pyproject.toml`, which is why the suite runs but `python -m genimerge` does
  not). Not worth changing the user's PATH over, but worth not rediscovering.
- **NEEDS-INVESTIGATION — what actually bounds a Geni export is still unknown.**
  The code does not claim to know: `GENI_EXPORT_CAP` is documented as the largest
  export *observed* — **4008** since 2026-08-05 — rather than a limit Geni
  enforces, and `tests/test_seeds.py` fails if one exceeds it, which is how 3840,
  3844, 3856 and the 4008 were each caught. What is unresolved is the underlying
  fact. Ninety-nine exports still cannot separate a raised limit from a
  per-account limit from a limit on something other than head count from a walk
  that overshoots a floor. **The even spacing was a trap and the data has since
  said so**: three numbers four apart looked like a step of four, then eleven
  exports in a row held 3860 exactly, then a pair taken seven minutes apart held
  3972 and 4008. Nothing in the code encodes any arithmetic. This advances as
  data arrives rather than by being worked on, and is not blocking anything —
  being off by a few people out of ~4000 does not move the seed ranking.

- **CI is off on purpose, and stays off.** Not a blocker — a decision. This is a
  private repo, where Actions minutes are billable rather than free, and
  push-triggered CI was never worth that risk. `ci.yml` is now
  `workflow_dispatch:` only and the workflow is disabled at the GitHub end.
  Verification is `python -m pytest` before pushing. The cost of that choice is
  named rather than hidden: **the Python version matrix does not run**, so 3.10
  is exercised only by the static check in `tests/test_python_floor.py`, and no
  commit should be described as CI-verified.
- **NEEDS-DECISION** — `todo.md` items 4 and 5: creating Wikidata items, for
  people who have none and for the **1540 surnames and 4986 given-name tokens**
  that have none. Sized in `reports/names.md` over the five-export merge: 1167
  of 2707 distinct surnames (43.1%) and 2419 of 7405 distinct given-name tokens
  (32.7%) have an item, so the rest do not. Whole given-name strings as Geni
  stores them are far worse — 1186 of 11772 (10.1%) — because Geni packs
  multiple names into one field. The fifth export roughly doubled the
  given-token pool and dropped coverage from 56.1% to 32.7%: the Japanese
  component's names are much less represented on Wikidata than the Norwegian
  ones. The decision is the user's.

---

## Always last — restart the three crons and summarize

**These two items stay pinned to the tail of the queue at all times** — below every real work item:

A. **Ensure the three crons are running** — start them if this session never did, restart them if a planning burst / queue re-fill killed them: work-loop (`3 * * * *`), auto-flush (`15 * * * *`), status-report (`42 * * * *`).
B. **Run the status-report action once more, independently** — an end-of-session summary of everything that happened this session.

---

## Pointers

- Long-horizon backlog (abstract goals, source of future queue items): `todo.md`.
- Completed work (chronological, with releases): `devlog.md`.
- Narrative history: `git log`.
