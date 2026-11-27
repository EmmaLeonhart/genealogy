# Inputs of order.life's ancestor days

Read by order.life's `.github/workflows/ancestor-days.yml` (Emma, 2026-11-26: "Everything works through the public
repo"), with `rootsmagic/second_attempt.rmtree`:

- `merged.ged.gz.part00-03`: the Geni union GEDCOM (the synoptic tree from `exports/`), gzip in 45 MB parts, as of
  2026-11-10. Rebuild: `cat merged.ged.gz.part* | gzip -dc > merged.ged`.
- `abu-hamza-hourglass.rmtree.gz.part00-01`: the Abu Hamza hourglass, RootsMagic 11's "Import a Tree from
  FamilySearch" breadth-first from Abu Hamza (2026-10-09/10, 168,902 people), gzip in 45 MB parts.

Replace a file here with a fresher export (a new name or new parts) and the next ancestor-days run builds from it.
