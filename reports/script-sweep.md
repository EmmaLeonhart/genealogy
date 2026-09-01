# The 264-script sweep

Her ruling, 2026-09-01: **"Sweep and delete"**, over reporting first. The sweep ran. What it
found is that there is very little to delete, and that is the finding.

| | scripts |
| --- | ---: |
| total in `scripts/` | 264 |
| named by another script, a test, a workflow, `CLAUDE.md`, `queue.md` or `docs/` | 206 |
| **orphaned by reference** | **58** |
| …of those, generating or reading a report the prose cites | 40 |
| …of those, generating a report **still on disk** | 15 |
| **no reference, no surviving output** | **3** |

The three are `browser-sink.py`, `convert-new-saved-pages.py` and `split-scrape-bundle.py`.

## Why almost nothing is deletable, against expectation

Her test is *"does the pipeline read this?"*, and for most of these the answer is no — but the
**report is the deliverable**, not the script. `CLAUDE.md` § *"Analyse this" means build a CSV*
makes a one-off census a first-class output: build the CSV, commit it, analyse it. A script that
ran once, wrote `reports/mononyms.csv`, and was never called again is not legacy under that rule.
It is how a committed report is reproducible.

Deleting it does not remove code the pipeline reaches. It removes the only record of how a
tracked file was made.

**`classify-patronymics-wikidata.py` is the sharpest case.** Nothing references it. It also
generates the four `reports/patronymic-classification-wikidata-*.csv` files — 64 MB each, all
committed. Deleting it leaves 256 MB of tracked data nobody can rebuild.

## Two detector failures worth recording, because both nearly caused a wrong deletion

- **Output paths built with `/`.** The first detector matched `"reports/x.csv"` only, so
  `REPO / "reports" / "wikidata-isolates.md"` was invisible and
  `measure-wikidata-isolates.py` was marked dead — a script whose report `CLAUDE.md` calls
  *"the analysis"*.
- **Markdown backticks are not quotes.** The reader scan required a quoted path, so a report
  cited in prose as `` `reports/x.md` `` counted as read by nobody.

Both are the same shape as the defects `CLAUDE.md` records elsewhere: **a screen that silently
narrows its input, producing a plausible number about the instrument rather than the data.** The
first run said 58 dead. The correct answer is 3.

## The judgement that is hers

Whether a one-off census script counts as legacy. The measurement cannot answer it: they are
unreferenced by construction and their outputs are committed by instruction. **The 15 that still
have a report on disk are listed in `out/dead-scripts.txt`'s sibling output** and are the
population to rule on.
