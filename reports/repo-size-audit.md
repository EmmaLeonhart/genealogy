# Repository size audit, 2026-10-02

Measurement only. Nothing was deleted, moved, repacked, rewritten, committed or pushed while
making this report. Every removal, `.gitignore` change, workflow change or history rewrite
proposed at the end needs Emma's explicit go-ahead before anyone does it.

Sizes are MiB/GiB (1 MB here = 1,048,576 bytes). "On disk" is the compressed size inside the
pack; "raw" is the uncompressed blob size. History figures count each distinct blob once.

## 1. The totals

| what | size |
| --- | --- |
| GitHub's reported size of `EmmaLeonhart/genealogy` (`gh api`, `.size`) | 22.8 GiB |
| local alternate store `..\genealogy\.git` (2 packs, 138,018 objects) | 22.03 GiB packed, 23 GB on disk |
| submodule's own store `ontology-harness\.git\modules\genealogy` (21 packs, 85,838 objects) | 9.85 GiB packed, 11 GB on disk |
| commits reachable from all refs | 5,008 (first 2026-07-30) |
| distinct blobs reachable | 118,290: 24,431 MB on disk, 86,000 MB raw |
| trees, commits | 14 MB, 3 MB on disk |
| blobs in the HEAD tree (on disk) | 7,213 MB |
| blobs only in history (on disk) | 17,217 MB (70%) |
| HEAD checkout, tracked (raw) | 16,825 MB in 95,537 files |
| ignored files in the working tree (unpacked derived files) | about 2,040 MB |

No reachable blob is missing locally: `rev-list --missing=print` reported 0 missing objects,
because the alternate store holds the full history.

**The two local stores overlap almost completely.** Of the 80,703 objects in the submodule's own
packs, 79,814 (98.9%) are also in the alternate. Only 889 are unique to the submodule store. Its
largest pack (6.70 GB, written 2026-10-01 14:28) and five more of 0.37 to 0.74 GB each (written
2026-10-01 to 2026-10-02) are copies of objects the alternate already has, so about 9.8 GiB of
local disk is duplicate. This is a local-disk matter only; GitHub does not see it.

## 2. Where the history goes

### By top-level directory (all versions, distinct blobs)

| directory | on disk MB | raw MB | blobs |
| --- | ---: | ---: | ---: |
| reports | 13,803 | 52,826 | 12,882 |
| wikidata | 4,393 | 4,507 | 2,560 |
| out | 3,153 | 11,869 | 1,618 |
| exports | 2,385 | 11,391 | 45,882 |
| preservation | 409 | 961 | 5,491 |
| orderlife | 101 | 138 | 325 |
| rootsmagic | 51 | 132 | 3 |
| (root files) | 35 | 3,309 | 4,175 |
| harvested-paths | 19 | 79 | 34,444 |
| docs | 18 | 20 | 183 |
| everything else | about 65 | | |

### By extension

| extension | on disk MB | raw MB | blobs |
| --- | ---: | ---: | ---: |
| .csv.gz | 10,976 | 13,354 | 334 |
| .gz (the `wikidata/items/*.jsonl.gz` shards) | 4,488 | 4,602 | 2,726 |
| .tsv.gz | 2,942 | 3,084 | 245 |
| .ged | 2,433 | 11,712 | 45,923 |
| .json | 954 | 28,984 | 3,679 |
| .json.gz | 807 | 953 | 95 |
| .tsv | 665 | 11,586 | 40,272 |
| .csv | 480 | 4,933 | 1,243 |
| .jpg | 204 | 209 | 6,981 |
| .html | 82 | 1,557 | 3,708 |
| .md | 48 | 3,526 | 6,206 |

Already-gzipped files are the problem: git cannot delta one gzip stream against the next, so each
rewrite of a 35 to 50 MB `.gz` stores a whole new 35 to 50 MB. Plain text (`.json`, `.tsv`, `.md`)
deltas well: 29 GB of raw `.json` costs 954 MB.

### Top 25 paths by cumulative on-disk size

"versions" is the number of distinct blobs; "commits (bot)" is how many commits touched the path
and how many of those were `github-actions[bot]`.

| path | MB on disk | versions | first added | commits (bot) |
| --- | ---: | ---: | --- | --- |
| reports/display-names.csv.gz | 3,252 | 79 | 0e6b71ee8 2026-08-24 | 79 (60) |
| out/family-structure.tsv.gz | 2,807 | 68 | 5a9724069 2026-09-01 | 68 (62) |
| reports/derived-family.csv.gz | 2,619 | 83 | 0e6b71ee8 2026-08-24 | 83 (64) |
| reports/derived-facts.csv.gz | 2,541 | 80 | 0e6b71ee8 2026-08-24 | 80 (61) |
| reports/derived-labels.csv.gz | 2,537 | 90 | 0e6b71ee8 2026-08-24 | 89 (61) |
| reports/wikidata-placeholder-labels.json.gz | 786 | 81 | 38f136d9a 2026-09-01 | 81 (69) |
| reports/wikidata-en-labels.json | 73 | 65 | a2f487e74 2026-08-19 | 65 (57) |
| reports/relationship-label-preview.csv | 70 | 83 | 5bc7d4fa4 2026-08-14 | 81 (62) |
| out/gui-data.json | 63 | 196 | 74ed7f384 2026-08-31 | 200 (176) |
| reports/label-mul.tsv.gz | 57 | 2 | 730b6e529 2026-09-02 | 2 (0) |
| reports/garborg-live-items-13.json (one of 16 shards, 00 to 15) | 49 | 69 | 98be1c099 2026-09-19 | 69 (60) |
| reports/label-ja.tsv.gz | 48 | 2 | e61612dd5 2026-09-02 | 2 (0) |
| out/model-vs-reality-items.json | 43 | 139 | e0b9f7eed 2026-08-26 | 141 (128) |
| exports/familysearch/PFR5-LDS-ancestors12-descendants2.ged | 36 | 7 | 33e690337 2026-09-24 | 7 (6) |
| out/wikidata/store-index.sqlite3 (deleted 2026-08-15, now ignored) | 36 | 1 | 01875c88d 2026-08-14 | 2 (0) |
| preservation/.../Descent from Antiquity - 2024-09-15 15-33-33.zip (deleted 2026-09-18) | 35 | 1 | 15b7c6fb9 2026-09-17 | 2 (0) |
| rootsmagic/second_attempt.rmtree | 34 | 1 | 6f01cd01d 2026-10-01 | 1 (0) |
| exports/hoknes-kingo/export-Ancestors-6000000177921459114.ged | 30 | 2 | f7bb2f4fd 2026-09-06 | 2 (0) |
| out/wikidata/relations.tsv | 28 | 2 | d9344fcd4 2026-08-25 | 2 (0) |
| reports/display-names.csv (pre-gzip, deleted 2026-08-24) | 28 | 5 | c297481f8 2026-08-11 | 6 (0) |
| reports/path-chains-1.tsv to -6.tsv | 23 to 28 each | 20 each | 0106bac8f 2026-09-19 | 11 (0) each |
| devlog.md | 27 | 1,823 | eebb9c29e 2026-07-30 | 1,751 (0) |
| preservation/genealogy/dropbox/Mannus.ged.gz | 27 | 1 | 7c073cc35 2026-09-17 | 1 (0) |
| preservation/genealogy/dropbox/Theogrammaticus.ged.gz | 27 | 1 | 7c073cc35 2026-09-17 | 1 (0) |
| reports/tree-eccentricity.csv and .csv.gz (both in history) | 23 + 23 | 1 + 1 | 994d4c503 2026-09-03 | |

### By kind of file

| group | MB on disk | blobs |
| --- | ---: | ---: |
| the five derived CSVs, gzipped (`display-names`, `derived-family/-facts/-labels`, places) | 10,949 | 332 |
| `wikidata/items/*.jsonl.gz` (the Wikidata item store, read offline by the pipeline) | 4,393 | 2,560 |
| `out/family-structure.tsv.gz` | 2,807 | 68 |
| `exports/` (Geni GEDCOM corpus) | 2,385 | 45,882 |
| `reports/wikidata-placeholder-labels.json.gz` | 793 | 91 |
| `reports/garborg-live-items-*.json` (16 shards) | 675 | 1,090 |
| `preservation/` | 409 | 5,491 |
| `reports/path-chains*` | 199 | 571 |
| `reports/sweep/` | 176 | 737 |
| `out/*.json` (`gui-data`, `model-vs-reality-items`, the other deck data) | 134 | 478 |
| `reports/label-*.tsv.gz` | 105 | 4 |
| `reports/patronymic-*` | 76 | 58 |
| review decks and site pages, `out/*.html` and `out/site/*.html` | 62 | 641 |
| `.rmtree` files and `rootsmagic/` | 53 | 5 |
| QuickStatements batches (`reports/wikidata-*.txt`, `*.qs`) | 26 | 1,450 |
| `harvested-paths/` | 19 | 34,444 |

**Files that are regenerated and rewritten on every run** (the derived CSVs, family structure,
placeholder labels, live items, path chains, en-labels, relationship preview, deck data, label
packs, `out/wikidata/`) account for **16,452 MB of the 24,431 MB**, and 15,705 MB of that is
superseded versions no checkout uses any more.

### Who put it there, and when

- Blobs first introduced by `github-actions[bot]` commits: 13,996 MB (57%). By other commits
  (Emma and agent sessions): 10,291 MB.
- Of the five derived CSVs: 9,437 MB came from bot commits, 1,484 MB from session commits.
  `out/family-structure.tsv.gz`: 2,689 MB bot, 118 MB session. Placeholder labels: 715 bot, 78
  session. `wikidata/items/`: all 4,393 MB from session commits.
- By month of introduction: July 6 MB, August 6,846 MB, September 16,407 MB, October (two days)
  1,028 MB. The heaviest days were 2026-09-17 (2,621 MB), 09-13 (2,188), 08-07 (2,106), 09-14
  (1,909), 09-12 (1,874). At the September rate the repository grows by about 0.5 GB a day.

## 3. What CI writes and commits

| workflow | commit step | what it commits |
| --- | --- | --- |
| `pipeline.yml` (push, 4 schedules a day, dispatch) | `pack-derived.py` then `git add -A` (two places) | everything the run regenerated: the batch files, inventories, decks, `out/site`, and the `.gz` packs of the derived files |
| `tree.yml` | `pack-derived.py` then `git add -A` | the derived CSVs (as `.gz`), `out/family-structure.tsv.gz`, `p2600-all`, the unconnected worklist, sibling worklist, FamilySearch renders |
| `review-decks.yml` | explicit list | `out/{parent,family,pick-one,familysearch}-review.html`, their `*-gui-data.json`, `out/site`, three candidate TSVs |
| `wikidata-edits.yml` | explicit | the day's receipt and `reports/runner-ips.tsv` |
| `places.yml` | explicit | `reports/place-qids.tsv`, `reports/occupation-qids.tsv` |
| `check-cluster-items.yml` | explicit | `reports/eccentric-cluster-candidates.tsv` |
| `emit-research-ancestor-gedcoms.yml` | explicit | two `research-exports/*.ged` |
| `union-tree.yml` | none | uploads an Actions artifact instead |

`pack-derived.py` packs these into tracked `.gz` (the plain files are ignored): the four derived
CSVs and `display-names.csv`, `wikidata-placeholder-labels.json`, `label-mul.tsv`, `label-ja.tsv`,
`wikidata-four-script-labels.json`, `out/wikidata/edits.json`, `out/family-structure.tsv`. Its
own docstring notes that gzip embeds a timestamp, so a repack can rewrite a `.gz` with no content
change unless that is suppressed.

Every one of these is rebuilt by a workflow from inputs that are themselves tracked
(`exports/`, `wikidata/items/`, the hand tables). They are committed because later jobs and
sessions read them from the checkout rather than rebuilding (the slim tree build needs about 17 GB
of RAM, more than a standard runner has).

## 4. Duplication

- **Two local object stores** holding the same 79,814 objects (section 1): about 9.8 GiB.
- **Derived data in two forms on the working copy:** each tracked `.gz` has an ignored unpacked
  copy beside it (`display-names.csv` 307 MB, `derived-family.csv` 271, `wikidata-placeholder-labels.json`
  256, `family-structure.tsv` 252, `derived-facts.csv` 217, `out/wikidata/edits.json` 199,
  `derived-labels.csv` 183, `label-mul.tsv` 160, `label-ja.tsv` 111,
  `wikidata-four-script-labels.json` 61). That is by design and only on disk. No `.csv` and
  `.csv.gz` pair is tracked together in HEAD, but history holds both forms of `display-names`,
  `derived-facts` and `tree-eccentricity`.
- **The derived files restate `exports/` and `wikidata/items/`.** `derived-*`, `display-names`
  and `family-structure` are projections of the merged tree, which is built from `exports/`;
  `garborg-live-items-*`, `wikidata-en-labels.json` and the placeholder labels are projections of
  the Wikidata store or of live Wikidata.
- **Identical blobs at more than one path in HEAD:** 3,797 blobs, 451 MB of redundant checkout.
  402 MB of that is inside `preservation/` (MyHeritage `.ftb` databases and photos copied between
  `Descent from Antiquity`, its `archive`, `export-Ancestors` and `export-Ancestors1`). Others:
  `out/*-review.html` and the same file under `out/site/` (17 MB), `exports/frisk/export-Ancestors-6000000227892448837.ged`
  and `frisk_geni/Cameron Frisk geni ancestors.ged` (14.5 MB), `gedcom/familysearch/rootsmagic-PFR5-LDS-2026-09-25.ged`
  and `rootsmagic/potentially_corrupted_file.ged` (11.7 MB).
- **Two RootsMagic databases tracked:** `copy of second attempt.rmtree` at the root (79 MB raw)
  and `rootsmagic/second_attempt.rmtree` (81 MB raw); both are also archived outside the repo in
  `Documents\rootsmagic-archive\2026-09-30\`.
- **Review decks** are committed in `out/`, again in `out/site/`, published to GitHub Pages from
  `out/site`, and published as claude.ai artifacts.
- **The `exports/` corpus was rewritten in place**, although new exports are meant to be new
  files: 11,593 modifications and 2,632 deletions of `exports/**/*.ged` in history, about 1,016 MB
  of superseded corpus blobs. The largest: `9eb9ec4c7` 2026-09-17 "Expand the abbreviated
  patronymics in the source gedcoms" (6,910 files), `49d9a8974` 2026-09-27 harvested paths
  regenerated (1,953), `1c72b1ada` 2026-09-10 deleting `exports/tiny-profiles/` (1,704), and two
  tiny-path GEDCOM rewrites on 2026-09-13 (1,007 and 911).

## 5. The working tree

Tracked content at HEAD, by directory (raw):

| directory | MB | files |
| --- | ---: | ---: |
| exports | 6,367 | 32,270 |
| wikidata | 4,338 | 2,427 |
| reports | 3,670 | 10,205 |
| preservation | 1,318 | 13,001 |
| out | 490 | 178 |
| rootsmagic | 144 | 4 |
| orderlife | 138 | 325 |
| (root files) | 82 | 18 |
| harvested-paths | 73 | 32,412 |
| gedcom | 70 | 12 |
| frisk_geni | 52 | 12 |
| everything else | about 90 | |

Largest single tracked files: `preservation/genealogy/dropbox/ITIS.ged` 91 MB,
`rootsmagic/second_attempt.rmtree` 81 MB, `copy of second attempt.rmtree` 79 MB,
`out/wikidata/relations.tsv` 74 MB, `reports/display-names.csv.gz` 69 MB, two `Perkwunos.ftb`
67 MB each, `exports/post-merge/export-Ancestors-6000000227739381826.ged` 67 MB,
`out/family-structure.tsv.gz` 63 MB, `reports/patronymic-classification-wikidata-{1,2,3}.csv`
62 to 63 MB each, `reports/wikidata-en-labels.json` 62 MB. Several sit within 10 to 40 MB of
GitHub's 100 MB per-file limit.

Untracked files: none outside `.gitignore`. Ignored: the unpacked derived files listed in
section 4 (about 2,040 MB) and 53 `__pycache__` directories.

## 6. Proposals (not done; each needs Emma's go-ahead)

**A. Stop committing what CI regenerates on every run.** The candidates are the `.gz` packs from
`pack-derived.py`, `out/family-structure.tsv.gz`, `reports/garborg-live-items-*.json`,
`reports/wikidata-en-labels.json`, `reports/relationship-label-preview.csv`, the deck data in
`out/*-gui-data.json` and `out/model-vs-reality-items.json`, and `out/site/`. They are 16.5 GB of
the 24.4 GB of history and are growing about 0.5 GB a day. Ways to keep them available without
committing them: an Actions cache or artifact handed from `tree.yml` to `pipeline.yml`; a GitHub
Release asset or a separate data branch overwritten in place (a branch force-pushed with one
commit keeps one version); or rebuilding in each job. The cost is that a session reading
`reports/derived-*.csv` locally would have to download them, and the tests that police these files
(`test_derived_packing.py`, the inventories) would need to change. At minimum, committing these
less often (once a day rather than on every push and every tree run) would slow the growth.

**B. Make the `.gz` repacks byte-stable**, so an unchanged file is not a new blob. `gzip` with a
zero mtime (`gzip.GzipFile(mtime=0)`) produces identical bytes for identical input. This saves
only the runs where content did not change; it does not help when content changes, since gzip
output does not delta.

**C. Move `wikidata/items/` (4.3 GB, 2,427 shards) out of the repo.** It is a cache of Wikidata
items read offline by the pipeline, not source. It changes rarely (2,560 blobs for 2,427 paths),
so it costs checkout size more than history growth. It could live as a release asset, an Actions
cache, or a separate repository.

**D. Move `preservation/` (1.3 GB checkout, 402 MB of it duplicate copies), the two `.rmtree`
files and other personal archives out of the repo**, or at least drop the duplicate copies. The
`.rmtree` files are already archived in `Documents\rootsmagic-archive\2026-09-30\`. The rule that
RootsMagic files are archived before anything touches them applies first.

**E. Free about 9.8 GiB of local disk** by letting the submodule store rely on its alternate
instead of holding copies of the same objects. That is a `git repack`/`gc` in the submodule's
git directory and falls under the rule against running git in the genealogy submodule, so it is
listed here only as a measured fact.

**F. A history rewrite**, with `git filter-repo`, dropping every superseded version of the
generated files in A (keeping only the current one):

- Saves about **15.7 GB**: history would fall from about 24.4 GB to about 8.7 GB on disk.
  Also removing `wikidata/items/` from all of history (after C) saves another 4.4 GB, to about
  4.3 GB. Dropping superseded `exports/` versions would save about 1.0 GB more, but that rewrites
  the history of the corpus itself and is not proposed.
- Costs: every commit hash changes, so `main` is force-pushed; every clone (the alternate at
  `..\genealogy`, the submodule store, any CI cache) has to be re-cloned or rebuilt; running
  sessions working in the submodule lose their base and must be stopped first; open PRs and links
  to old commit hashes (devlog references, `Claude-Session` trailers, receipts naming shas, the
  `ring-watch.yml` input that takes a commit) stop resolving; the submodule pointer recorded in
  ontology-harness names a commit that no longer exists and has to be moved in a commit there.
  GitHub does not reclaim the space at once: old objects stay reachable through cached PR refs
  until GitHub Support runs a gc.
- Without A first, a rewrite is undone in about a month at the current rate. A without F stops
  the growth but leaves the 24 GB.

Nothing in this report was removed or changed. Every item in this section, including stopping a
file from being committed, requires Emma's explicit go-ahead.

## What could not be measured

- `du` over the whole working tree did not finish in about 30 minutes, so the tracked-checkout
  figures come from `git ls-tree -r -l HEAD` (raw sizes) plus `du` on each ignored file. NTFS
  allocation overhead on the 95,537 small files is not included.
- On-disk sizes are per pack. An object stored in both local stores is counted once, with the
  size of whichever copy `cat-file` read.
- Commit attribution follows first parents (`--first-parent -m`) and attributes each blob to the
  first commit that introduced it; 144 MB of the 24,431 MB was not attributed by that walk.
- GitHub-side storage beyond the reported `size` (Pages deployments, Actions artifacts and caches,
  PR refs) was not measured.
- The contents of `exports/` were not read, as instructed; section 4 reports only counts and
  commit subjects for the corpus rewrites.
