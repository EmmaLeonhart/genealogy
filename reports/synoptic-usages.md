# Every use of "synoptic tree", and which of the two things it means

Emma, 2026-08-29: *"it is consistently conflated between the union of all the geni gedcoms
and the union of that tree with all data sources."* Built by
`scripts/census-synoptic-usages.py`; the raw rows are `reports/synoptic-usages.tsv`.

**182 occurrences across 46 files.** 98 of them are in files that GOVERN — `CLAUDE.md`, `queue.md`, `docs/`, `scripts/`, `src/`, `todo.md`. The rest are in `devlog.md` and `reports/`, which are the record of what happened and are not rewritten.

| verdict | governing usages |
| --- | ---: |
| geni | 3 |
| full | 10 |
| both named | 1 |
| unclear | 84 |

**A line is classified only on words in the line itself** — `merged.ged`, `exports/`,
`.ged` for the Geni union; Wikidata, a QID, `P2600`, `zipper` for the full one. Anything
else is `unclear`, deliberately, because the failure this exists against is somebody
deciding a usage means whatever is convenient.

## The unclear ones are not 84 decisions. They are these classes

### her own quoted words — 14

A line quoting Emma. Not ours to redefine; it stays verbatim whatever the answer is.

* `CLAUDE.md:1800` — **The method is structural.** *"For the synoptic tree, we're supposed to be
* `CLAUDE.md:1976` — > the IDs to ensure that they haven't been merged or anything... Forcing them into this Synoptic
* `CLAUDE.md:1977` — > tree like this makes it so that the Synoptic tree, when it starts being used as an input, does
* `CLAUDE.md:1988` — **What the bio link is FOR, in her words, 2026-08-29:** *"When the synoptic tree is merged we
* `queue.md:1235` — **Her words:** *"Put into the queue also an analysis of how the synoptic tree is actually made."*
* `queue.md:1382` — *"No fuck you you didn't get the later discussion. When the synoptic tree is merged we change all
* `queue.md:1701` — **Emma, 2026-08-29:** *"don't test it now but make the last queue item rebuilding the synoptic
* `scripts/build-clan-p2600-pairs.py:5` — **Emma, 2026-08-24:** *"the tanba onakatomi izumo stuff is a prerequisite for the synoptic
* … and 6 more

### the correspondence artefact — 18

`synoptic-correspondence.tsv` and the scripts that write or read it — a Geni-to-Wikidata correspondence, so this reads as the FULL union.

* `queue.md:1241` — So **nothing waits on this.** Write down what `scripts/build-synoptic-correspondence.py` actually
* `queue.md:1723` — number; the first version emitted 83,988 people off `reports/synoptic-correspondence.tsv` and that
* `scripts/build-clan-p2600-pairs.py:6` — rebuild"* — these joins are **inputs** to `reports/synoptic-correspondence.tsv`, so
* `scripts/build-join-batch.py:1` — "The thing that consumes the synoptic correspondence: Geni facts onto joined items.
scripts/build-join-batch.p
* `scripts/build-qid-links-gedcom.py:22` — this script emitted every pairing in `reports/synoptic-correspondence.tsv` that landed on somebody
* `scripts/build-qid-links-gedcom.py:59` — Reading `reports/synoptic-correspondence.tsv` and filtering it to the three returned **0 of 3** —
* `scripts/build-synoptic-correspondence.py:3` — python scripts/build-synoptic-correspondence.py
* `scripts/build-synoptic-correspondence.py:34` — Writes `reports/synoptic-correspondence.tsv` and `reports/synoptic-conflicts.tsv`.
* … and 10 more

### the build/rebuild chain — 13

`rebuild-everything.py` and the things that say 'rebuild the synoptic tree'. What that script actually produces is `out/merged.ged`, the GENI union.

* `CLAUDE.md:1988` — **What the bio link is FOR, in her words, 2026-08-29:** *"When the synoptic tree is merged we
* `docs/mass-export-run.md:37` — tree and then rebuild the synoptic tree, and then generate the quickstatements with the
* `queue.md:988` — ## Fix the surnames of the tier-2 placeholders before the synoptic tree is built
* `queue.md:1047` — **Emma, 2026-08-18. Do this BEFORE the synoptic tree is built. Not an investigation
* `queue.md:1382` — *"No fuck you you didn't get the later discussion. When the synoptic tree is merged we change all
* `queue.md:1701` — **Emma, 2026-08-29:** *"don't test it now but make the last queue item rebuilding the synoptic
* `scripts/audit-farmname-seeds.py:5` — the synoptic tree is built. I will do the editing on geni for this."*
* `scripts/build-clan-p2600-pairs.py:6` — rebuild"* — these joins are **inputs** to `reports/synoptic-correspondence.tsv`, so
* … and 5 more

### everything else — 46

* `CLAUDE.md:1803` — relationships. That is a critical part of building up this synoptic tree."* Start
* `CLAUDE.md:2277` — the people as we add more since we want all these bureatten people in the geni synoptic tree and
* `docs/daily-algorithm.md:32` — **The ideal state is the union of the synoptic tree and the Geni tree.** Not the Geni tree alone
* `docs/dictation/2026-08-26-daily-algorithm.md:18` — the synoptic tree and the janny tree. In the arnie area, it's really clear. It finds, within this
* `docs/mass-export-run.md:36` — https://www.geni.com/profile/index/6000000227464556886 and incorporate them into the synoptic
* `docs/mass-export-run.md:172` — injection into the synoptic tree build. Both the novelty and the purpose are gone.
* `queue.md:36` — `Link reliability order`, `The chain of provenance`, `How the synoptic tree is actually made`,
* `queue.md:189` — - **The ideal state is still the Geni tree alone.** Her spec says the **union of the synoptic
* `queue.md:190` — tree and the Geni tree**; the synoptic half does not exist yet, which is the § *PREREQUISITE
* `queue.md:931` — export alone. If it does then that'll be great. We'll have a synoptically
* `queue.md:1135` — thing so that we can deal with more important stuff."* Read as the synoptic-tree build
* `queue.md:1157` — ## Build the synoptic tree
* `queue.md:1233` — ## How the synoptic tree is actually made — Emma, 2026-08-25
* `queue.md:1237` — over the synoptic tree stuff sufficiently, but I'm going to treat it as though it's all good. I'm
* `queue.md:1238` — going to treat the synoptic tree as though it is perfect, and we are going to address whether the
* `queue.md:1239` — synoptic tree is well functioning later."*
* `queue.md:1818` — ## "Synoptic tree" means two different things — resolve it usage by usage
* `queue.md:2047` — Geni record in there overwrites the same Geni ID from any other export** in the synoptic
* `queue.md:2176` — runner, so the synoptic tree still cannot be rebuilt in Actions without a larger runner.
* `scripts/audit-farmname-seeds.py:90` — task in the queue to fix the surnames of these people before the synoptic tree 
* … and 26 more
