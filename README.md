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
python -m pytest                       # run the tests
PYTHONPATH=src python -m genimerge inventory   # re-measure the exports
```

On Windows PowerShell, `$env:PYTHONPATH="src"` instead of the inline prefix.
