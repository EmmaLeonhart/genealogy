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

## ⛔ NO EDITS WHILE THE ADMINISTRATORS' NOTICEBOARD MENTIONS 日巫女; NO CRON JOBS TO 2026-10-01

Ruled 2026-09-24, replacing the two-week hold: *"as long as there is any mention of 日巫女 at
Wikidata:Administrators' noticeboard then there will be no edits ever ... No updating
quickstatements no editing at all."* Read live on every run and fails closed:
`wikidata-edits.yml` gate, `pipeline.yml` gate (every event), `daily-batch-email.yml`, and
the sender's live path (`scripts/wikidata_lockout.py` § NOTICEBOARD). **No cron job runs for a
week**: `wikidata-edits`, `pipeline`, `ci`, `daily-batch-email`, `pages`, `tree`, `review-decks`
stay DISABLED in GitHub until 2026-10-01; after that `gh workflow enable <file>` and the
noticeboard gate governs. **No exception, no one-off run**: ruled the same evening, *"no run at
all only runs of even generations of quickstatements happen only after the string is not present
on that page"* -- the gate in `pipeline.yml` stops every event, dispatch and `force` included.
*"This is indication I was editing too aggressively but it was mostly a quickstatements issue of
the tool not being throttled correctly."*


## Now

- **Run `split-path-chains.py` and `build-tiny-gedcoms.py` over the chains already fetched.** The
  paused walk left 31,819 chains held (192,556 distinct people) and neither script was run after
  it; no workflow calls either. `build-tiny-gedcoms.py` writes corpus `.ged` files under
  `exports/tiny-paths/`, so run it as its own deliberate step and never overwrite an existing
  `.ged`. No Geni needed.
- **Record the missing parent link between the owner's ancestry and the Rømer ring seed.** It is
  one unrecorded link; `Q141450322` Olfvir / Ølver Rømer (`6000000002621242041`) is a
  `PRIORITY_ANCESTOR_SEEDS` ring seed. Work it from data on disk or FamilySearch; no Geni fetch.
  Also owed: the ledger row for `Q141450322` pairs the husk id `6000000227289508960`, which
  redirects to `6000000002621242041`.
- **The FamilySearch zipper, done properly.** Checked on one family and a 16-pair Wikidata
  cross-check only. Measure it across all 4,863 pairs, work out what the 1,351 ambiguous slots
  need, and handle FamilySearch's own duplicate records (two ids, one person).
- **The name-model fixes, measured across the whole tree.** Latin patronymics
  (`LATIN_VERNACULAR`), `Jonæ` (`-ae`), the lone-letter surname rule (`N.`) and the marker rule
  were each checked on handfuls of examples. Census every one over `display-names.csv` before and
  after, and look at what each newly classifies.
- **The ration and the pacing, seen working end to end.** Edit run `36054472568` (dispatched
  2026-09-24, 500, live) is the first test: confirm names -> 30 people -> ring go out in order,
  20-50 s apart, and what stops it.
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
