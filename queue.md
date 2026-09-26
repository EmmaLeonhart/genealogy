# Queue

Work only. Take the first item under **Now** and do it. When it is done, delete it and append a
dated `devlog.md` entry in the same commit. Bullets, never numbers. Nothing here is marked
priority: the order IS the priority, and a new item goes where it belongs in the order, not on
top with a banner. Rulings go in `CLAUDE.md`; history goes in `devlog.md`; everything else that is
not an action goes in `docs/queue-archive/`. The file this replaced, verbatim, is
`docs/queue-archive/queue-before-2026-09-24-rewrite.md`.

**Standing, not items:** no contact with geni.com until at least 2026-10-21, and only Emma lifts
it. Each session re-creates the hourly `exports/2026-09-19` merge cron and starts with
`CLAUDE.md` § *FIRST OF ALL, THE FAMILYSEARCH ZIPPER*.

## Now

- **The ration and the pacing, seen working end to end (BLOCKED-ON-EXTERNAL: the 08:07 UTC
  scheduled `wikidata-edits` run of 2026-09-26).** Run `36054472568` (2026-09-24) sent nothing: its
  first create waited out maxlag for 900 s (`still lagged after 900s of waiting`, the day of the
  WDQS lag) and the run was cancelled at 20:45. Read the next run's log for: names -> 30 people ->
  ring going out in that order, 20-50 s apart, and what stops it.
- **`Q660913` Kruto the Wend and FamilySearch `MBW7-P7H`** are Emma's own investigation. The job
  here is only to hold the identifiers and what the tree says (the archived queue has both).

- build a gedcom exporter from wikidata
- **Review what actually happened on Wikidata's Administrators' noticeboard.** Research it and determine the course of action.
- **Check out the RootsMagic GEDCOM exports.** The earlier FamilySearch GEDCOM export failed to get a lot of individuals, so a RootsMagic export should be better. If access to it can be gained, use it.
- **Research what the known French ancestry adds.** With it, the family tree is substantially larger than previously believed. Research whether the larger number of relatives gives matches that weren't there before.
- **CJK names through the name combinatorics: feasibility assessment, then implement.** Earlier in the project's history we were trying to switch to CJK versions of names as what the label gets derived from. In a sense the items do not get immediate CJK labels, but they are added through the name combinatorics. Do a feasibility assessment on that and try to implement it.
- **Actually create patronymics (and matronymics, where they exist) in male/female pairs, and connect each pair.** Emma asked for the workflow to make them in pairs and link them, and this does not appear to have been happening at all: there is no "Helgesson", for example. Look in particular at https://www.wikidata.org/wiki/Q141515178; Emma is not sure what is going on with it. Also make clear which language each patronymic is from. That is a significant problem in itself, but the forms are consistent within a language: -datter vs -dotter vs -dottir, -sson vs -ssen, and so on.
- **Analyse why https://www.wikidata.org/wiki/Q141550395 and https://www.wikidata.org/wiki/Q141550315 were created with such weird labels, and fix the cause.** Find what in the pipeline produced those labels, fix it so it does not happen again, and correct these two items.
- **Look over https://www.wikidata.org/wiki/Q141550971 for two errors, and fix both.** First, American English (en-us) labels should be put on items where the mul and en labels differ. Second, the Chinese, Japanese and Korean labels do not have the role in them, and that needs to be fixed.
- **Clone shintowiki-scripts, queue the fix that gets its edits through, and start a session for it.** Clone https://github.com/EmmaLeonhart/shintowiki-scripts to `C:\Users\Emma\Documents\GitHub\shintowiki-scripts` (there is no local clone yet). Add an item to its `queue.md` to get things fixed so its edits go through, then commit and push that. Then open a Claude session in it the standard way: its startup launcher started through explorer.exe, with the usual boot prompt.
- **Adopt shintowiki-scripts' editing pacing.** After the item above, analyse how shintowiki-scripts edits Wikidata (its editing algorithms: pacing, throttling, batching and the like) and adopt those in this repo. Creation stays unchanged; only the pacing and how edits are sent change.
- **Finally implement standardized labels in Russian, Ukrainian, Greek, Hindi, Arabic, Persian, Bengali, Hebrew, Tamil, Cherokee, Inuktitut, Ethiopian, Maldivian, Armenian, Georgian and zgh.**
- **Link an individual's names at the moment the individual is created.** When a person is created and their name objects (given name, family name) already exist, the new item should carry those name links from the start, not have them added later. Emma believes they are linked later today but is not sure how the algorithm actually works, so first establish how it works now, then change it. The pipeline already creates name objects and links them to people as part of creation; the point is to link any name objects that already exist at creation time. Also check a clarification Emma thinks already holds: noble particles are always kept in the name, and the surname clearly gives them priority (Emma described them as being at the end of the name; confirm how the pipeline treats them). Why: this is part of the gradual shift toward the name objects' different-language versions being what takes priority for a person's names.
- **Resume the descendants sweep from its cursor (needs Geni; not before 2026-10-21).** The queue
  is `reports/sweep-queue-6000000227822546944.txt` and the cursor stood at 8,993 of 29,366 when
  Geni's WAF began answering 403 on 2026-09-21. The 209 people in
  `reports/sweep-partial-incapsula-2026-09-21.txt` have empty or truncated captures from the
  block and need capturing again; their archived files are the WAF's output, not Geni's.
- **Join common managing accounts across the descendants and the owner's ancestors (needs Geni;
  not before 2026-10-21).** The name halves are done (`reports/descendant-ancestry-leads.csv`,
  1,874 shared tokens; `reports/fuzzy-name-matches.csv`, 943 pairs >= 0.82). The roster carries
  `managed_by`, the ~8,254 ancestors in `owner-ancestors.tsv` do not; only a Geni ancestors
  report supplies it. Then join managers in `match-descendants-to-ancestry.py`, keeping the
  manager (the first 6N batch dropped it).
- **Run the sibling scrape over `reports/sibling-pair-worklist.tsv` (needs Geni; not before
  2026-10-21).** Every member of a pair, not one of each, so each side's account of the parents
  merges on the Geni id. The driver is `scripts/siblingscrape.js` with
  `build-sibling-scrape-batch.py` and `write-sibling-scrapes.py`; it is a real page load per
  person at the extension's pace, and not while the path requester is running.
- **Resume the permalink chain walk (needs Geni; not before 2026-10-21).** `scripts/pathchains.js`
  over `reports/path-permalinks.tsv` (47,692), paused 2026-09-20 at 12,911. At the restart, build
  the list with `build-chain-batch.py --skip-covered` (27,808 left) and upload it as a file; set
  `C.i` from `localStorage.chains_cursor`. The run is finished when `i >= of` and `C.failed` is
  empty, so `C.reseedFailed()` is owed at the end.
- **Reframe the repo: a family tree for Wikidata, and later for the Gaiad at genealogy.order.life.** Rewrite how the repo describes itself (README, Pages site): it builds a family tree for Wikidata, and later one for the Gaiad at genealogy.order.life (GitHub Pages; Emma will point the subdomain there soon). The QuickStatements stay the main part of the Pages site for now and become less prominent over time, as the repo moves away from QuickStatements as its purpose. Add per-individual pages, adapted from how order.life already generates its pages. Make the repo less Geni-branded and move it towards FamilySearch.
- **Add order.life as a submodule of this repo, on its own `genealogy` branch.** A full clone, not a shallow one (Emma will ask about its revision history). Branch `genealogy` and make this repo's edits there only; narrative_identity works on order.life's `main`. Longer term, the Order of Life issues genealogical IDs.
- **RootsMagic: extract directly from the `.rmtree` files and fold them into the synoptic tree.** There are two `.rmtree` files (likely SQLite) and a GEDCOM exported from RootsMagic. Build direct `.rmtree` extraction, and parse the older, non-git-ignored one first. The younger one, `rootsmagic/second_attempt.rmtree`, may still be being written by a slow FamilySearch export (running since about 4-6 a.m. on 2026-09-25; it exports whole ancestral families, siblings included). Set up an hourly check: once it has not been modified for over an hour, copy it to `copy of second attempt.rmtree` and work only from the copy. Emma expects it to be git-ignored, but it currently shows as untracked, so check `.gitignore` and do not commit it. Extract GEDCOMs from the copy and from the first attempt, and integrate them into the synoptic tree alongside the existing FamilySearch GEDCOM work; re-export if the earlier export proves broken. Then go on to the analysis item below. First read this repo's own rules on how its data may be read, and read it only that way.
- **Analyse what the repo holds, then the synoptic tree.** A real analysis of where individuals are in the repository and what the distribution is. Then analyse the synoptic tree: how the descendant exports and the rest relate to Emma's newfound ancestors, who are far more widespread across Europe through Emma's mother's side, the Bure clan. That is the line Emma wants the story told through, though both sides matter. First read this repo's own rules on how its data may be read, and read it only that way.
- **Resolve places to Wikidata items.** A later pipeline stage: take the places of birth, death, marriage and so on (FamilySearch standardises them) and resolve each to its Wikidata item so they link properly, as part of a comprehensive ontology.
- **Reverse pipeline: from Wikidata to GEDCOM.** Query Wikidata with SPARQL to find individuals and build GEDCOMs from them, the reverse of the GEDCOM-to-Wikidata work.
- **File these in `todo.md` as context for later, not as work now:** Chinese surnames and their bottlenecks, for the Gaiad writing; shrines.order.life for the Shinto wiki scripts, with temples.order.life redirecting there; a religious-buildings database beyond Wikidata; every deity treated as having a genealogy.
- **Last: a comprehensive pass through order.life to move all its genealogy material into this project.** On the `genealogy` branch, go through the whole order.life repository (grep the repo; don't read the website), find all the genealogy material, and move it here. It is decent in places and haphazard in others. First read this repo's own rules on how its data may be read, and read it only that way.
- **Fix the patronymic error on https://www.wikidata.org/wiki/Q141550288, and the same error everywhere else it occurs.** Work out what is wrong with this item's patronymic, fix it here, then find every other item with the same error and fix those too, including the cause in the pipeline so it does not recur.
- **Merge this repo's order.life work back into order.life `master`, then work on `master` from then on.** Open a pull request from order.life's `genealogy` branch to `master` (order.life's default branch) and auto-merge it. After that, make order.life edits on `master`, not on a separate branch. This replaces the "own `genealogy` branch" part of the order.life submodule item above (Emma via narrative_identity, 2026-09-25). Context: ontology-harness `inbox/2026-09-25-narrative-identity-handoff/`; Emma's verdicts in it outrank the rest.
- **Then write this repo's own handoff directory, committed and pushed.** Summarise what decisions this repo made, how it differed from its instructions, where it disagreed, and why, so narrative_identity and Emma can read it later and act on it.
- **Attempt more Baltic German investigation on Emma's mother's side.** Emma's working guess is that the line runs through Baltic Germans (the French ancestry found there earlier was a surprise), and that it may reach the Rurikids (Yuri Dolgoruky), from where a Caucasus link would put descent from antiquity within reach. Treat the Rurikid and Caucasus links as leads to test, not facts. Read this repo's own rules on how its data may be read first, and read it only that way.
- **Look into Alfheid: the person created and then merged soon after.** The Alfheid item was placed very oddly, in a way that suggests the run may have been reading from the wrong source, or not treating the privileged directory as prominently as it should. Emma thinks it was an isolated case, possibly from a merge that was not done properly, but it is worth checking: find how Alfheid was created and placed, whether the privileged directory was read with the priority it should have, and whether any other person was affected the same way.
