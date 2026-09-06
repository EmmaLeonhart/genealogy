# Which QuickStatements batches are produced by anything?

**Emma asked for this on 2026-09-05**, after noticing that `BURE_PER_DAY` — a *per-day* cap —
sat on a script no schedule ran: *"Uhh I'm just confused why are these segregated in code?"*

**No deletions were made from this audit.** Her instruction was to check and report.

## The result

    27 .qs files in reports/
     0  produced by anything the pipeline runs
     9  have a generator that exists but is not scheduled
    18  have no generator in scripts/ at all

**The one live batch is not among them.** `.github/workflows/pipeline.yml` runs exactly one
generator, `build-garborg-day.py --compose`, and it writes `reports/wikidata-garborg-day.txt`.
Every `.qs` in `reports/` is a relic of a hand-run.

## A generator exists, nothing schedules it

| file | generator | last commit |
| --- | --- | --- |
| `wikidata-add-p2600.qs` | `build-add-p2600-batch.py` | 2026-08-31 |
| `wikidata-from-diff.qs` | `build-from-diff.py` | 2026-08-26 |
| `wikidata-spine-add-p2600.qs` | `build-from-diff.py` | 2026-08-26 |
| `wikidata-garborg-label-fixes.qs` | `build-label-corrections.py` | 2026-08-26 |
| `wikidata-geni-qid-p2600.qs` | `build-qid-link-p2600.py`, `build-izumo-beyond-chart.py` | 2026-08-23 |
| `wikidata-reciprocals.qs` | `build-missing-reciprocals.py`, `build-sibling-batch.py` | 2026-08-31 |
| `wikidata-reciprocals-siblings-held.qs` | `build-missing-reciprocals.py` | 2026-08-31 |
| `wikidata-siblings-oneoff.qs` | `build-sibling-batch.py` | 2026-08-27 |
| `wikidata-regnal-ordinals.qs` | `build-regnal-ordinals.py` | 2026-09-01 |

**These are the ones that matter**, because a generator nothing calls is the failure she named on
2026-08-30 — *"name creations were always segregated into a different Quick Statements generation
pipeline that was never run"* — and `CLAUDE.md` § *Code that is WRITTEN but never CALLED is not
done* is the rule. Whether each should be folded into the daily batch, run on its own schedule,
or deleted is hers; nothing here assumes.

Two carry the caps that were doubled on 2026-09-05 and so pace nothing today:
`build-missing-reciprocals.py` (`SIBLING_CAP`) and `build-from-diff.py` (`SIBLING_CAP`).

## No generator at all — 18 files

`wikidata-add-geni-id.qs` · `wikidata-bureatten-p2600.qs` · `wikidata-charlemagne-last-bond.qs` ·
`wikidata-edited-not-created.qs` · `wikidata-from-diff-izumo.qs` · `wikidata-garborg-day-1.qs` ·
`wikidata-garborg-day-2026-08-25-run.qs` · `wikidata-garborg-links.qs` ·
`wikidata-garborg-role-fixes.qs` · `wikidata-join-garborg-links.qs` · `wikidata-join-izumo.qs` ·
`wikidata-jon-parents.qs` · `wikidata-lave-jonsen.qs` · `wikidata-q141198548-nn.qs` ·
`wikidata-q4411612-mul.qs` · `wikidata-remove-collapsed-generation-p2600.qs` ·
`wikidata-signe-close.qs` · `wikidata-touched-not-created.qs`

**Most of these look like records rather than dead pipelines** — one-off fixes aimed at a named
item (`q4411612-mul`, `q141198548-nn`, `signe-close`, `jon-parents`, `lave-jonsen`), or a dated
run kept as a record (`garborg-day-2026-08-25-run`). A record of what was sent is worth keeping
and is not what the legacy rule is about. Some are the output of scripts since deleted, which is
a different thing again.

## Method

`scripts/audit-qs-generators.py`. A file counts as *produced* when some script under `scripts/`
names it, and as *scheduled* when that script is named in `.github/workflows/*.yml`.
