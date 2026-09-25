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

- **Moved up to 12:00 2026-09-25 (ruled that morning): re-enable the seven workflows and lift the
  noticeboard gate.** A one-shot session cron does both; if the session is gone by then, do it by hand.

## Now

- **Ask Emma about the Administrators' noticeboard matter with AskUserQuestion, now, before anything else.** Put the open questions on the noticeboard matter to her through the AskUserQuestion tool, not as prose in chat. Also, from now on, whenever a classifier refusal happens, consistently ask Emma with AskUserQuestion. Record that standing rule in `CLAUDE.md` (rulings live there, not in the queue).
- **Lift the Administrators' noticeboard hold so today's edits go through (Emma, 2026-09-25).** Remove the noticeboard rule, or at least hold it, so that today's (2026-09-25) Wikidata edits go through. If the noon edits did not happen, make them happen by fixing the pipeline. The current noticeboard matter is considered done. Set it up so that in ten days, on 2026-10-05, the noticeboard check starts acting as a filter again.
- **Finish `_plan.tsv`: rename the 34 `exports/archive/export-geni/` files to their seed ids.**
  Ruled 2026-09-24. The move into `export-geni/` happened; the rename to
  `export-<Kind>-<seed id>.ged` did not. `git mv` each file, confirm the id in its new name is
  the file's first `INDI`, never overwrite an existing path, then delete `_plan.tsv`.
- **The descendant reports are NOT yet a full family tree.** Closed too early on 2026-09-24,
  reopened. Done since: the exact-generation tie-break, the report subject at generation 1, and
  parents placed by ROW ORDER (8,446) -- couples with no parent resolved 74,440 -> 33,059.
  Left: those **33,059** (mostly `<private>` living people and spelling variants whose block sits
  between anchors with several candidates), **1,817 conflicting parent slots**, 1,605 parent
  strings with no split, and the `immediate_family` siblings/spouses, unused.
- **CI slow lane red: 11 failures, all `exports/sweep-parsed/`** (run `36011859223`).
  `test_gedcom_real_exports.py` does not know the `sweep-parsed` header or its `IL`/`FL` label
  prefixes. Fast lane green on 3.10 and 3.13.

- **Restore the open work the queue rewrite archived.** `docs/queue-archive/queue-before-2026-09-24-rewrite.md`
  holds real, unfinished items that left view on 2026-09-24. Re-read it end to end and bring back
  every open work item (not rulings, not history) into this list.
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
