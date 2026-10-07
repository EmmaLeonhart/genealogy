# Devlog

## 2026-10-03
- Wrote `wikidata_to_gedcom.py`: ancestor export for Q140568870 in en/zh/ja/ko
  at 10 generations, opened with the default program. Added `--suffix` and ran
  the `-2` and `-3` exports after the user edited labels. Raised the default to
  15 generations (`-4`).

## 2026-10-05
- 30-generation ja and ko exports (`-5`, 3,799 people), then a 50-generation
  ko export (`-6`, 5,161 people, 1,044 names left as bare QIDs).
- Work mode started: INTENT.md, private repo
  `EmmaLeonhart/wikidata-ancestor-gedcom-export`, README, update check.
- Offline pytest suite (`tests/test_gedcom.py`): label fallback, claim filtering,
  GEDCOM structure, and one test pinning the exact output text. CI runs it on
  push and pull request (`.github/workflows/ci.yml`).
- Each written file now reports on stderr how many people it has and how many
  are named only by QID. `to_gedcom` builds FAMC/FAMS links from an index instead
  of scanning every family per person; output is identical to the old code on
  the real 10-generation Q140568870 tree in all four languages.
