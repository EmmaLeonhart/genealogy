# Handoff — 2026-08-07 (cloud session → PC)

Casual context dump so a session on Emma's PC can pick up where the cloud
session left off. Not a generated artifact; overwrite or delete freely. The
durable record is in `todo.md` (items 4 and 8), `devlog.md` (2026-08-07 entry),
and `reports/profile-names.md`.

## What this session did

Investigated **what is actually in the Geni profiles**, because it bounds what
the Wikidata authoring pipeline can emit. Built a generated report for it and
opened a PR.

- **PR #2** — <https://github.com/EmmaLeonhart/geni/pull/2>, branch
  `claude/wiki-qid-export-coverage-frykhv`. New `genimerge profile-names`
  command + `src/genimerge/profilenames.py` → `reports/profile-names.md`;
  `tests/test_profilenames.py` (11 tests). Additive only.
- At handoff the full `python -m pytest` was **still running (~14 min, real
  merges, at 99% CPU — slow, not hung)**. Every directly-affected test passed
  (`test_profilenames`, `test_cli` registration, `test_wikidata_ids_documented`,
  `test_package`). **On the PC: re-run `python -m pytest` to confirm the whole
  suite is green** before merging — the cloud run wasn't watched to completion.

## The findings (over the 257,219-person merge)

- Workhorse fields: **sex (P21) 99.9%, given name (P735) 92.1%**. Surname 58.1%,
  birth date 46.8%, death date 37.3%. Occupation 10.8%, burial 7.9%, title 2.9%
  — minority fields, don't scope a batch around them. Parents 82.6%, marriage
  63.9% (the backbone for offline superimposition / Geni-merge decisions).
- **CJK names are present in native script.** 16.6% of the tree carries a CJK
  form; **43.7% of those also carry a romanisation** (often in the `_MARNM`
  slot), rest native-only. The native label is the well-covered thing; the gap
  is the *English* label. (An earlier raw pass said 9% romanised — it skipped
  `_MARNM`; the model-based 43.7% is correct.)

## Two traps written into `todo.md` item 4

1. The **36.9% multi-token `GIVN`** figure is **not** a P1545 count — most extra
   tokens are honorifics/particles/titles ("Lady", "no", "Chanyu"), not given
   names. Real P1545 case is the Latin-script subset. Don't split `GIVN` on
   spaces naively.
2. A **NAME is Geni's display *label***, not always a name — "Unknown Wife"/"NN"
   is a description, belongs in an alias, not a P735/P734 link.

## The plan, as Emma framed it (in `todo.md` items 4 & 8)

Phase order: **(1) descendant-distribution search** to pick export seeds
(tomorrow's focus) → (2) large `Descendants` export campaign off those picks →
(3) Geni-side enrichment pipeline (QuickStatements: names, P2600, sex, dates,
name-item creation) → (4) build the **Wikidata tree offline** and superimpose it
→ (5) integrate — "for the most part a very large amount of merges". Phases 4–5
are done **offline on purpose**, only final confirmed merges go online.

- **order.life** = a deferred **third source** (Geni, Wikidata, order.life). It's
  on Emma's PC, not in the cloud session's reach. Needs a *different citation*
  from the Geni-ID-as-source. Postponed until the Wikidata side is offline.
- **Postponed Geni-side merge queue:** most two-Geni-IDs-on-one-Wikidata-item
  pairs are Geni duplicates that should be merged on Geni but can't be yet.
  `reports/wikidata-doubles.md` already lists them. Last thing, not now.

## Next concrete task (tomorrow)

**Descendant-distribution search** — a new, unbuilt capability: rank tree members
by realized documented-descendant count and use it to choose where to run the
next `Descendants` exports (reaching modern times). Complements `density.md`
(thinness) and `seeds.md` (doorways) but ranks by descendant fan-out instead.
Emma mentioned focusing on **four individuals/lines** — if she names them, their
descendant counts can be computed against the current merge immediately (the
`reports/wikidata-coverage.md` "biggest unlinked" table already ranks by
descendants, e.g. Kunino-tokotachi at 2,361, so the primitive exists).
