# Queue

Work only. Take the first item under **Now** and do it. When it is done, delete it and append a
dated `devlog.md` entry in the same commit. Bullets, never numbers. Nothing here is marked
priority: the order IS the priority, and a new item goes where it belongs in the order, not on
top with a banner. Rulings go in `CLAUDE.md`; history goes in `devlog.md`; everything else that is
not an action goes in `docs/queue-archive/`. The file this replaced, verbatim, is
`docs/queue-archive/queue-before-2026-09-24-rewrite.md`.

**Standing, not items:** no contact with geni.com until at least 2026-10-21, and only Emma lifts
it. Each session re-creates the hourly `exports/2026-09-19` merge cron and starts with
`CLAUDE.md` § *FIRST OF ALL, THE FAMILYSEARCH ZIPPER*.

## Now

- **FamilySearch step, first real run.** Tree rebuild `35970905635` (dispatched 2026-09-24) is the
  first with bridge -> zipper -> render. Check it went green and that
  `exports/familysearch/PFR5-LDS-ancestors12-descendants2.ged` puts `GF2B-NKG` (Emma Olivia
  Andersdotter) on `@I6000000178279770847@`.
- **CI green.** The fast lane's last 3 failures are `test_generated_inventories.py` naming files
  deleted in `f2e0082f8`; `pipeline.yml` regenerates both inventories. Once a pipeline run on a
  sha after that deletion finishes, dispatch `ci.yml`; green on 3.10 and 3.13 closes it.
- **CI slow lane.** `tests/test_gedcom_real_exports.py` failed on run `35714896690`, the only time
  the slow lane has run. Read the failure and fix it.
- **The CJK half of the relational labels already sent.** The Latin half is wired
  (`_label_corrections`). A `ja`/`zh`/`ko` relational label needs the given name rendered
  natively and placed LAST (`namemodel._DESCRIBE_TRAILS`); a kanji `ja` is Sinosphere and is
  never touched.
- **Sweep-parsed people have a display name and no `GIVN`/`SURN`.** `exports/sweep-parsed/`
  writes `1 NAME <Geni display name>` unsplit, so 208,043 people carry titles in the name
  (`…, Markgraf`) and get no name items. Split by form, never by position.
- **FamilySearch ids on entry points should generate people too** — seed from `P2889` where the
  Geni column is empty.
- **`Grimus von von Rügen`** (`6000000012966007622`, father of `Q660913` Kruto the Wend) carries a
  doubled `von` in our label.

## Last — placed here by Emma, not before everything above is done

- **Review the middle-initial items**, because of roman-numeral confusions. *"Losses are a bigger
  threat than the gains are positive here."*
- **`Q660913` Kruto the Wend and FamilySearch `MBW7-P7H`** are Emma's own investigation. The job
  here is only to hold the identifiers and what the tree says (the archived queue has both).

## Blocked on the Geni moratorium

- **The research, manager half.** The ancestors report off Geni supplies `managed_by` for the
  owner's ~8,254 ancestors; then join managers in `match-descendants-to-ancestry.py`.
- **The path requester.** 140,692 never attempted at the last count; `scripts/pathrun.js`,
  `CLAUDE.md` § *THE PATH CAMPAIGN*.
- **The chain walk.** 12,911 of 47,692 permalinks walked. Resume with
  `build-chain-batch.py --skip-covered`, finish with `C.reseedFailed()`, then run
  `split-path-chains.py` and `build-tiny-gedcoms.py`.
- **The sibling scrape.** A loop over `reports/sibling-pair-worklist.tsv` at the extension's
  pace, never alongside the path campaign.
- **The descendants sweep.** Cursor 8,993 in `reports/sweep-queue-6000000227822546944.txt`; the
  209 people in `reports/sweep-partial-incapsula-2026-09-21.txt` are the WAF's output and are
  redone.
- **`Slavina` / `Slawina von Rügen`**, Kruto's mother and spouse, one letter apart: checked
  against Geni, not reasoned about.
- **The Rømer ring seed** is one unrecorded parent link from the owner's ancestry.
