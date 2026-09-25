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

## Not settled

- **The saved pages' `*_files/` folders: 2.89 GB, 38,276 files, 14% of the repo. Kept.** A
  browser's *save page* writes `Name.html` plus a `Name_files/` folder. No code reads the
  folders, and every CI workflow leaves them out of its checkout. The first draft of this page
  called them junk as one lump, which was not earned. Broken down for
  `paths_for_wikidata_isolates/`:

  | type | size | files | what it is |
  | --- | ---: | ---: | --- |
  | `.download` | 1.67 GB | 13,985 | Geni's JavaScript (`all.js`, `common.js`, `geni-loader-*.js`), the same files saved again with every page |
  | `.css` | 945 MB | 3,996 | Geni's stylesheets, likewise repeated |
  | no extension | 103 MB | 2,284 | **not opened** |
  | `.html` | 20 MB | 1,998 | frames inside the page (`blank.html` and others), **not opened** |
  | images | 25 MB | 14,447 | icons and silhouettes (`void.png`, `close.gif`), plus 2,948 `.jpg` that may be profile photos |

  The JavaScript and stylesheets (2.6 GB) are Geni's own site code. The extensionless files, the
  inner `.html` frames and the `.jpg`s have not been looked at, so nothing here is called junk
  until they have. The pages themselves were harvested into `paths/` on 2026-09-02, so whether
  the saved pages need to stay at all is a separate question. `geni_pages/*_files/` (126 MB) and
  `chats/*_files/` (4 MB) have the same shape.
- **`_plan.tsv`** (3 KB): renames `exports/archive/export-geni (N)/export-<Kind>.ged` to
  `export-<Kind>-<seed id>.ged`. It was never applied: the archive is named
  `export-geni/export-<Kind>-<N>.ged`, and none of the planned names exist. It is either pending
  work (CLAUDE.md: *disambiguate with the seed id*) or a plan that was replaced.
- **`wikidata_isolates_to_clear/New Text Document.txt`**: 18 Geni URLs (Ovid, Aesop, Horace,
  Hobbes and others). It is an unprocessed work list, not junk. It belongs in the queue or in
  `undigested.md`.
- **1,347 loose `reports/` files (48 MB)** match no name or pattern in the pipeline code. Most
  are one-off measurements that `devlog.md` cites as evidence. Deciding each one is a separate
  pass.
- **Deleting a file removes it from checkouts, not from history.** A full clone stays about
  20 GB until history is rewritten, and rewriting history is a separate decision.
