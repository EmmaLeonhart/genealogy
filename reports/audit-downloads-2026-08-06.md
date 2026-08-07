# Preservation audit — the 2026-08-06 evening downloads

Written 2026-08-06. Emma's ask: *"I want to make sure no issue occurred with
GEDCOM preservation — these ones I think are all new except maybe one, in the
Downloads folder, as the last bunch of GEDCOMs to flesh out around the edge
people."*

**Answer: nothing was lost.** Six zips were in `~/Downloads`. Four held GEDCOMs
this repo did not have and are now committed under `exports/edges/`. Two held
GEDCOMs **byte-identical** to files already in git, so there was nothing to
preserve. Emma's guess was right in kind and off by one in count — it was two
repeats, not one.

This audit was run under a standing instruction to keep CPU low (laptop hot, fan
audible in public). What that cost is stated in § What was not run, rather than
left to be discovered later.

## Method

Every claim below is a hash or a byte count, not an inspection by eye.

1. Zip entries were listed via `System.IO.Compression` **without extracting**, to
   see the payload names and sizes first.
2. Payloads were extracted to a scratch directory *outside the repo*, so nothing
   entered `exports/` before it had been identified.
3. Each payload's size was compared against all 99 corpus GEDCOMs; only the two
   size collisions were hashed. SHA-256 on 200 MB was avoided deliberately —
   a size mismatch already proves non-identity, so hashing every file would have
   burned CPU to learn nothing.
4. `HEAD.DATE` / `HEAD.TIME`, the seed (first `INDI`), record counts and xref
   prefixes were read in one streaming pass per file.

**One method error, corrected before it reached a conclusion.** The first scan
took the first `2 DATE` line in each file as the export date. `HEAD.DATE` is at
level **1**, not 2, so that read some later record's date and reported
`export-geni (1).zip` as *31 OCT 2024*. Re-reading the actual `HEAD` blocks gave
06 AUG 2026. Every date in this report comes from a `1 DATE` line.

## The six zips

| zip | payload | HEAD | seed | INDI | verdict |
| --- | ---: | --- | --- | ---: | --- |
| `export-geni.zip` | 1 749 528 B | 02 AUG 2026 08:36:20 | `6000000226989731860` unknown grandfather | 3844 | **repeat** of `exports/originals/export-Forest-6000000226989731860.ged` |
| `export-geni (1).zip` | 2 677 355 B | 06 AUG 2026 15:13:08 | `6000000210475738822` 酒君/酒公 /Hata/ | 4004 | **repeat** of `exports/Hata/export-Forest-6000000210475738822.ged` |
| `export-geni (2).zip` | 1 960 634 B | 06 AUG 2026 18:10:37 | `6000000227085797849` NN /斎部/ | 4016 | **new** |
| `export-geni (3).zip` | 2 878 048 B | 06 AUG 2026 18:13:25 | `6000000227085766947` NN | 4020 | **new** |
| `export-geni (4).zip` | 2 555 470 B | 06 AUG 2026 18:17:26 | `6000000227085871850` NN /譚/ | 4020 | **new** |
| `export-geni (5).zip` | 3 731 863 B | 06 AUG 2026 18:19:40 | `6000000227085828865` NN /Ubay/ | 4020 | **new** |

All six are style `Forest`. All six carry `SUBM @S6000000087535357291@`, the
account owner, as always — which is why the `SUBM` xref cannot disambiguate a
filename and the seed ID is used instead.

The two repeats are **SHA-256 identical**, not merely same-size. They were left
in `~/Downloads` rather than moved into the repo: adding them would have put a
second copy of committed content in git and a second zip line in `.gitignore`
for no gain. They are safe to delete whenever Emma wants; the content is in git
either way. `genimerge.sources` drops byte-identical repeats, so even ingesting
them would not have changed a single number — but it would have changed the
apparent corpus size, which is exactly the confusion `audit-corpus-sync.md`
exists about.

## Where the four new ones went

`exports/edges/`, a new directory, because the download numbers `(2)`–`(5)`
already exist in `exports/fleshing-out/` and that `N` is a per-directory label
with no meaning across directories.

Named by **seed profile ID**, not by the bulk `export-geni/export-<style>-<N>.ged`
pattern: all four are the same style with four distinct seeds, so the seed ID is
the disambiguator `CLAUDE.md` already prescribes, and it is stable where `N` is
not.

```
exports/edges/export-Forest-6000000227085797849.ged
exports/edges/export-Forest-6000000227085766947.ged
exports/edges/export-Forest-6000000227085871850.ged
exports/edges/export-Forest-6000000227085828865.ged
exports/edges/export-geni (2..5).zip          # gitignored, one line each
```

### Integrity checks that passed

- **xref prefixes.** Only `I`/`INDI`, `F`/`FAM`, `N`/`NOTE`, `S`/`SUBM` across
  all four. No fifth letter, no letter spanning two record types.
- **`RFN` corroboration.** Zero mismatches between the `INDI` xref and its
  `1 RFN geni:` line, over all 16 076 individuals in the four files.
- **Seeds are new profiles.** None of the four seed IDs appears in **any** of
  the 99 prior exports — not as a seed, not as anybody's relative. That matches
  the documented technique of creating a placeholder at the frontier and
  exporting from it, and it is why these are "edge people".
- **Repo invariants.** `git status` shows the four `.ged` as untracked and **no
  zips**; all 51 zips under `exports/` resolve under `git check-ignore`.

## The export ceiling moved again: 4008 → 4020

`GENI_EXPORT_CAP` is raised to **4020**. Without that, `tests/test_seeds.py`
fails on the next run — which is the test working as designed.

The shape of the movement is worth more than the number:

| time | INDI |
| --- | ---: |
| 18:10:37 | 4016 |
| 18:13:25 | 4020 |
| 18:17:26 | 4020 |
| 18:19:40 | 4020 |

It rose **within a single nine-minute sitting** and then held for three
consecutive exports, having been 4004 the previous day — a number Geni's own
export UI displayed as its maximum. So the ceiling has now been observed to go
up, to go down (4008 → 4004), and to move mid-session.

**Do not read 4016 → 4020 as a step of four.** That inference has been made
twice in this repo's history and falsified twice. A flat run is evidence the
number sits still while it sits still, and nothing more.

## Paths: nine pages saved, seven new chains

Separately from the GEDCOMs, nine profile pages saved at 17:46–17:48 today were
sitting in `geni_pages/` with no converted path. All nine converted cleanly:

| path | steps |
| --- | ---: |
| `paths/gong-liu.tsv` | 249 |
| `paths/scorpion-i.tsv` | 267 |
| `paths/tadlaf-al-qaydari.tsv` | 192 |
| `paths/hou-zhang.tsv` | 193 |
| `paths/zeng-yuan.tsv` | 218 |
| `paths/hao-huang.tsv` | 193 |
| `paths/pasuti.tsv` | 243 |

**Every step in all nine carries a profile ID.** The name-matching fallback —
the one `CLAUDE.md` warns must never become load-bearing — is not used at all
here, so these are exact-join evidence throughout.

Two of the nine were the same chain saved twice, detected by diffing rather than
assumed from the title: `公劉 (Gōng Liú)s` differs from `公劉 (Gōng Liú)` in
**one line**, the `# Source:` comment, and `Matthew, 8th Apostle to Makeda`
likewise differs from the already-converted `makeda-to-matthew.tsv` in that one
line only. The two redundant TSVs were removed; **both HTML pages were kept**,
since a saved page is external evidence and is never the thing to delete.

All nine start at Makeda Queen of Sheba, so they are the eccentricity list from
`reports/remote-people.md` being worked through, as queue item 0.0 asks.

## What was not run

Named plainly because each is a real gap, not a formality:

- **`py -m pytest`.** The suite re-parses every export in `exports/` — now 103
  files, ~200 MB. The one assertion at risk from this change is
  `test_export_cap_is_at_least_the_largest_real_export`, and it is satisfied by
  construction: the largest new file holds 4020 and the constant is now 4020.
  That is an argument, not a run.
- **`python -m genimerge merge`.** So there is no new-people count for these
  four exports, and `out/merged.ged` still describes the 99-export tree.
- **`python -m genimerge density`.** The prediction recorded in queue item 3 —
  that region 6 yields more than region 4 would have — is still unscored.
- **Anything networked.** No Wikidata query was made.

Unblock signal for all four: Emma saying the machine is somewhere it can spin
up. This is a standing instruction from the user for this session, not an
unknown and not a deferral.
