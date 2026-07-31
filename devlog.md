# geni — Devlog

**This file is where "done" lives.** `queue.md` is delete-only: when a queue
item is finished, the item is **deleted from `queue.md`** and a dated entry
is **appended here**, in the same commit as the work, then pushed. Never
tick a box in place — a checked box left in `queue.md` is the failure mode
this file exists to prevent.

Also record releases (tag + a one-line note), notable milestones, and
anything else worth a chronological trail. Newest entries at the bottom.

This is the **same convention as the cleanvibe repo's own `devlog.md`** —
every cleanvibe-scaffolded project gets one for the same reason.

See `CLAUDE.md` § "Workflow Rules" and `queue.md`'s preamble.

---

## 2026-07-30 — cleanvibe onboarding started

Onboarded with `cleanvibe clone` (cleanvibe v1.17.0). This is an
**existing repository**, so the very first onboarding task is to **backfill
the rest of this devlog from `git log`** (tagged releases, milestone
commits, merged feature branches). After that, every finished queue item
appends a new dated entry here.

Backfill from `git log` is two commits long and holds no releases or
feature branches: `31e2b19` (the user's dropped Geni export archives) and
`eebb9c2` (the cleanvibe v1.17.0 scaffold). Nothing further to recover.

## 2026-07-30 — data lake triage, and the real plan

Five zip archives at the repo root turned out to be three distinct GEDCOM
exports plus two byte-identical duplicates (SHA-256 confirmed):
`export-geni.zip` == `export-geni (1).zip`, `export-geni2.zip` ==
`export-geni (2).zip`. Extracted the three distinct files into
`data_lake/`, moved all five archives in alongside them, and added `*.zip`
to `.gitignore` — the extracted GEDCOMs are what git tracks.

| file | size | INDI | FAM |
| --- | ---: | ---: | ---: |
| `export-Ancestors.ged` | 16.3 MB | 3836 | 2281 |
| `export-Forest.ged` | 4.2 MB | 3836 | 2020 |
| `export-BloodTree.ged` | 4.0 MB | 3836 | 1054 |

The load-bearing find: **Geni writes the profile ID as the GEDCOM xref
itself** — `0 @I6000000087535357291@ INDI` — and repeats it as `1 RFN
geni:6000000087535357291`. So the merge has a real primary key across all
three exports and does not need name/date fuzzy matching to unify them.
All three report exactly 3836 individuals, which the inventory step has to
confirm is the *same* 3836 rather than a coincidence of size.

Also confirmed the Wikidata property for the Geni profile ID: **P2600**.

Wrote `todo.md` (seven long-horizon items, from the canonical merge through
Wikidata authoring and name-item creation) and replaced the cleanvibe
bootstrap queue in `queue.md` with the real thirteen-item work queue,
mirrored into the task tool.

## 2026-07-30 — three-cron playbook running

Started the three session-local crons: work-loop `a58ec58b` at :03,
auto-flush `680ee058` at :15, status-report `9f6681e1` at :42. They are
`durable: false`, so they die with this session and are recreated at the
start of the next one; they also auto-expire after 7 days.

## 2026-07-30 — `genimerge` package skeleton

`src/genimerge/` behind a src-layout `pyproject.toml`, `tests/` on
`pytest` (`pythonpath = ["src"]`, so no install step is needed to run
them), and `.gitattributes` normalising line endings to LF while marking
`*.ged` binary so the exports we were given are never rewritten.

The package is **stdlib-only on purpose**. `urllib` is enough for the
Wikidata SPARQL endpoint, and a zero-dependency package keeps CI and cold
clones trivial. `pytest`: 1 passed.

## 2026-07-30 — GEDCOM reader/writer

`genimerge/gedcom.py`: a streaming GEDCOM 5.5.1 parser that folds `CONC`
and `CONT` away on read and re-creates them on write, so callers deal in
whole values and never in line wrapping. Malformed lines land on
`Gedcom.warnings` instead of raising, and a level that jumps past its
parent is clamped rather than dropped — a real export is not a
conformance test, and refusing to read a 16 MB file over one odd line
would be useless.

All three exports parse with **zero warnings**, which was not a given.
Record counts:

| file | INDI | FAM | NOTE | SUBM |
| --- | ---: | ---: | ---: | ---: |
| `export-Ancestors.ged` | 3836 | 2281 | 1026 | 578 |
| `export-Forest.ged` | 3836 | 2020 | 8 | 395 |
| `export-BloodTree.ged` | 3836 | 1054 | 6 | 398 |

**One real bug, found by the round trip and not by the unit tests.**
Round-tripping Ancestors was not a fixpoint: one `INDI` note came back
different. The cause was `parse()` splitting input with
`str.splitlines()`, which breaks on `\v`, `\f`, `\x1c`–`\x1e`, `\x85`,
`U+2028` and `U+2029` in addition to `\n` — while `parse_file()`, reading
with `newline=""`, breaks only on `\n`. The Ancestors export carries a
literal **U+2028 inside five note values**, so the two entry points
disagreed on exactly those records and the round trip silently rewrote
them. `parse()` now splits on `\n` alone. The regression test spells the
character as an escape rather than embedding it, because a bare U+2028 in
source is exactly the kind of thing an editor quietly normalises away.

`tests/test_gedcom.py` covers the parser on hand-written fixtures;
`tests/test_gedcom_real_exports.py` runs against the actual exports and
asserts the load-bearing invariant — every `INDI` xref is `@I<digits>@`
and `RFN` repeats the same ID — so if Geni ever changes that, the merge
fails loudly instead of quietly mis-keying. `pytest`: 35 passed.

Dropped the `[project.scripts]` entry point from `pyproject.toml`; it
pointed at a `genimerge.cli` that does not exist yet.

## 2026-07-30 — export inventory, and the finding that reframes the project

`genimerge/inventory.py` plus `python -m genimerge inventory` measure the
exports and write `reports/inventory.md`. Also added
`genimerge/identity.py`, the one place that knows a Geni profile ID comes
from the xref and is cross-checked against `RFN` — it raises
`IdentityMismatch` rather than picking a winner, because guessing there
would silently merge the wrong people.

**The exports are capped, and they barely overlap.** All three contain
exactly 3836 individuals, which is not a coincidence — it is Geni
truncating each export. What they contain is mostly *different* people:

| | individuals | families |
| --- | ---: | ---: |
| union of all three | **8766** | **4056** |
| largest single export | 3836 | 2281 |
| present in all three | 354 (4.0%) | 245 (6.0%) |

Pairwise, BloodTree∩Forest is 2300 individuals, Ancestors∩BloodTree is
442, and Ancestors∩Forest is 354. Every family in BloodTree is also in
Forest (1054 of 1054), so BloodTree's families add nothing that Forest
does not already have — its value is in its individuals.

This changes the shape of the work: merging is worth **4930 individuals**
over the best single export, and reaching the whole tree means many more
exports rather than a few. It makes the frontier analysis load-bearing
rather than a nicety. Recorded in `README.md` and `CLAUDE.md`.

The tag vocabulary in the report is the field list the canonical model
will be built from. Worth noting from it: `INDI.NAME` occurs 5498 times
across 3836 people in Ancestors, so **people carry multiple name
records** — directly useful for the multilingual labels the Wikidata work
wants. `_MARNM` (married name) is populated on roughly 80% of people,
`NICK` on 1837, and `OBJE` (photos) on 3520.

`pytest`: 42 passed.
