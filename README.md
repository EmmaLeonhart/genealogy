# geni

Merge Geni.com genealogy exports into one canonical tree, then connect that tree
to Wikidata.

> Scaffolded with [cleanvibe](https://github.com/Immanuelle/cleanvibe).

## What this is

Geni.com exports a family tree as GEDCOM, but **each export is capped** — every
one of the three exports in `data_lake/` contains exactly 3836 individuals, and
they overlap far less than that suggests:

| | individuals | families |
| --- | ---: | ---: |
| largest single export | 3836 | 2281 |
| all three merged | **8766** | **4056** |
| present in all three | 354 | 245 |

So the exports are overlapping slices of one tree rather than copies of it, and
getting the whole tree means merging many slices. That is the first half of this
project. The second half is reconciling the merged tree against Wikidata, and
eventually generating the edits that would put the missing people *into*
Wikidata.

Merging is exact, not fuzzy. Geni writes the profile ID as the GEDCOM xref
itself:

```
0 @I6000000087535357291@ INDI
1 RFN geni:6000000087535357291
```

so every record carries a stable primary key across exports, and the same ID is
the join key to Wikidata via **P2600 (Geni.com profile ID)**.

The merge of all three currently produces 8766 individuals and 4056 families
with **zero conflicts and no lost lines** — see `reports/merge.md`.

## Layout

```
data_lake/     the exports as received (zips gitignored, .ged files tracked)
src/genimerge/ the package
reports/       generated reports that are worth reviewing and keeping
out/           generated data (gitignored)
tests/         pytest
```

- `queue.md` — concrete steps currently in scope
- `todo.md` — the long-horizon backlog
- `devlog.md` — what has been finished, dated

## Usage

Nothing to install; the package is stdlib-only and `pytest` is wired to find it
via `pythonpath`.

```bash
python -m pytest                     # run the tests

export PYTHONPATH=src                # on PowerShell: $env:PYTHONPATH="src"
python -m genimerge inventory        # measure the exports  -> reports/inventory.md
python -m genimerge merge            # merge them           -> out/merged.ged
python -m genimerge export           # canonical dataset    -> out/people.jsonl
python -m genimerge reconcile        # match by P2600       -> out/wikidata/
python -m genimerge expand --search  # propose more links   -> out/wikidata/candidates.csv
python -m genimerge coverage         # what is linked       -> reports/wikidata-coverage.md
python -m genimerge frontier         # what to export next  -> reports/frontier.md
python -m genimerge quickstatements  # edits to review      -> out/wikidata/add-p2600.qs
```

Every command is re-runnable and reads the previous stage's output. Wikidata
responses are cached under `out/wikidata/cache/`, so re-running a report costs
nothing; delete that directory to force a refresh.

## Reports

Generated, and worth reading in this order:

- `reports/inventory.md` — what is in each export, and how little they overlap
- `reports/merge.md` — what merged, what conflicted, what did not resolve
- `reports/wikidata-coverage.md` — how much of the tree reaches Wikidata
- `reports/frontier.md` — where the tree stops, and which profiles to export from next

## Editing Wikidata

This project **never writes to Wikidata**. `genimerge quickstatements` produces
`out/wikidata/add-p2600.qs` — a batch adding the Geni profile ID to items that
should carry one — plus a readable `add-p2600.md` listing every edit with links
to both sides. Review it, then run it yourself at
[QuickStatements](https://quickstatements.toolforge.org/) if you agree with it.

Only structure-confirmed links get into the batch. Name-search proposals stay in
`out/wikidata/candidates.csv` no matter how good their score looked, because a
matching string is not evidence that two records describe the same person.
