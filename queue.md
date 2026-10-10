# Queue (offline branch)

The queue from `main` was cleared on this branch on Emma's instruction, 2026-10-09
("You're clearing the queue completely"). `main` keeps its own queue. Take the first item,
do it, delete it, log it in `devlog.md` in the same commit. No Wikidata editing here (see the
banner in `CLAUDE.md`).

- **Language-aware name matching.** Wikidata labels are English, `test.ged` names German,
  Portuguese or Latin. Map place names and particles across languages (Thuringia/Thüringen,
  of/von/de, Saxony/Sachsen) and rerun `wd_vs_ah.py` and `compare_ah.py`; report any new matches
  with the full line down to Emma, and check each line for bridges the matching built.
