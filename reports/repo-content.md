# What the repo holds, 2026-09-24

Measured at `bdfd04c`: **115,651 tracked files, 20.00 GB.** Sizes come from the GitHub tree API
for every file. "Read" means named in `scripts/`, `src/`, `.github/` or `geni-extension/`, not
counting tests, docs or a workflow's sparse-checkout exclusion list. `repo-content.csv` beside
this file has every directory (to two levels) and every root file, with its file count, bytes and
reference counts.

## Read by the pipeline: keep

| path | size | files | what it is |
| --- | ---: | ---: | --- |
| `exports/` | 6.58 GB | 22,807 | the Geni corpus, read recursively. Most subdirectories are named by no script, and that is expected: every `.ged` under it is merged |
| `wikidata/items/` | 4.55 GB | 2,427 | the offline Wikidata store, 29 references |
| `reports/sweep/` | 1.50 GB | 8,959 | the `exports/2026-09-19` sweep rows |
| `reports/path-chains/` | 128 MB | 372 | the path runner's drains |
| `reports/` (loose) | 2.02 GB | 1,885 | derived CSVs, batches, measurements. See below |
| `out/` | 468 MB | 206 | `out/wikidata/` (the batches), `out/site/` (Pages), the decks |
| `orderlife/` | 144 MB | 325 | the Order of Life items, analysis and images |
| `harvested-paths/`, `paths/` | 59 MB | 25,804 | path TSVs, read by `build-tiny-gedcoms.py` |
| `gedcom/` | 47 MB | 10 | the owner's tree and the FamilySearch downloads |
| `frisk_geni/` | 55 MB | 12 | `frisk-correspondence.py` reads `Cameron Frisk.ged` |
| `geni-families/`, `geni-paths/`, `samaritans/`, `research-exports/` | 9 MB | 216 | each read by one or more scripts |
| code, tests, docs | 25 MB | 574 | `scripts/` 379, `src/` 36, `tests/` 79, `docs/` 46, `.github/` 14, `geni-extension/` 13, `.claude/` 7 |

## Kept as records, read by nothing

| path | size | files | what it is |
| --- | ---: | ---: | --- |
| `preservation/` | 1.38 GB | 13,001 | an old family archive (MyHeritage, Family Historian, Dropbox: 12,189 `.jpg`). `ftb-to-gedcom.py` converts from `extracted-databases/` |
| `paths_for_wikidata_isolates/` pages | 117 MB | 666 | saved Geni path pages, harvested into `paths/` on 2026-09-02 |
| `geni_pages/` pages | 10 MB | 29 | saved Geni profile pages, cited by `src/genimerge/remote.py` |
| `chats/` | 4 MB | 33 | saved conversations that decided things (`chats/README.md`) |
| `docs/queued-analysis/` | 18.5 MB | 9 | screenshots of the 2026-09-11 reverts |
| `reports/sources/` | 1 MB | 3 | Samaritan source PDFs |
| `reports/path-<person>.json`/`.md` | 2 MB | 58 | the named relationship paths (Scorpion I, Makeda, Jimmu, Hata, Gong Liu and others), written by `genimerge path`. **Among the most important files in the repo** (ruled 2026-09-24), although nothing reads them and they were measured against older trees. Read-by-nothing is not junk |

## Junk, deleted 2026-09-24

**Root leftovers.** No code reads them.

| file | size | what it is |
| --- | ---: | --- |
| `_regions.pkl` | 1.3 MB | a pickled dict with one entry. Nothing loads it |
| `compose-garborg.log` | 65 KB | one run's console output, in UTF-16 |
| `address the problem in this image.PNG` | 110 KB | a QuickStatements screenshot. Handled 2026-09-14 (devlog: *the refused descriptions were duplicate name items*) |
| `address_this.html` + `address_this_files/` | 1.1 MB | a saved page given as input to the archived *Names* item |

**`out/` leftovers**: 34 loose one-off lists and logs (`open-*.txt`, `*-blocked-parents.txt`,
`rebuild-2026-09-01.log`, `garborg-2026-08-25.zip` and others), 6 MB. Some script wrote each of
them, and nothing reads any of them. `out/name-item-qids/` is not junk: it is the cache for
`collect-name-item-qids.py`.

**The saved pages' `*_files/` folders: 35,199 of 38,276 files, 2.88 GB, deleted on a yes.**
Saving a page in the browser writes `Name.html` plus a folder holding every file the page loaded.
No code reads the folders, and every CI workflow leaves them out of its checkout. The first draft
of this page called them junk as one lump without opening them. They were then opened, **every
file classified by its content rather than its name**, one row per distinct content in
`saved-page-assets.csv`:

| content | size | files | distinct | verdict |
| --- | ---: | ---: | ---: | --- |
| site code (Geni's JavaScript and CSS, a saved Claude chat's app bundle) | 2.84 GB | 20,405 | 351 | deleted |
| Facebook like-button frames | 20.5 MB | 693 | 692 | deleted |
| icons and interface images | 17.7 MB | 11,956 | 58 | deleted |
| reCAPTCHA frames | 1.2 MB | 36 | 34 | deleted |
| blank or stub frames | 0.3 MB | 1,416 | 4 | deleted |
| empty files | 0 | 693 | 1 | deleted |
| **profile photo thumbnails** | 9.1 MB | 3,077 | 2,074 | **kept** |

The `.html` pages and `chats/` `.md` extracts are untouched. The pages lose their styling in a
browser, and none of their text.

**`reports/path-isolate-*.md` and `.json`: 1,120 files, 11.8 MB, deleted on a yes.** One pair per
saved path in `paths/`, written by `genimerge connectors --write-paths` (`src/genimerge/cli.py`),
which no workflow runs. They were measured against a 472,655-person tree, far smaller than
today's, and nothing reads them. Rerunning that command regenerates them.

**`wikidata_isolates_to_clear/`** held one file of 19 Geni URLs. Moved verbatim into
`undigested.md`, and the folder deleted.

## Not settled

- **`_plan.tsv`** is half-applied: the `exports/archive/` files were moved into `export-geni/`
  under counter names, and never renamed to the seed-id names it lists. Ruled 2026-09-24:
  finish it. Queued.
- **227 loose `reports/` files** (58 of them the named path reports above, kept) match no literal name in the pipeline code, and 97 of them are
  cited in `devlog.md` or `docs/`. A literal search is not proof a file is unread:
  `descent-from-*-trunk.csv` matched nothing and `monte-carlo-pick.py` reads it through a built
  name. Each one needs its writer found. Queued.
- **Deleting a file removes it from checkouts, not from history.** A full clone stays about
  20 GB until history is rewritten, and rewriting history is a separate decision.
