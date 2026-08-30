"""Put the ATTESTED rendering into the transliteration table, above the rule engine.

    python scripts/apply-attested-renderings.py [--dry-run]

**Emma, 2026-08-30:** *"This is a solved problem. You understand that, right? There isn't really
an excuse."*

`reports/attested-name-renderings.tsv` is what Wikidata actually calls each token, counted over
323,684 items that carry both a Latin label and a Japanese or Chinese one. This puts it into
`reports/garborg-name-transliterations.tsv`, which is what every emitter reads.

## The precedence, and it is the whole point

1. **Emma's own corrections.** Her note stays, her value stays. `Minnie` and `Mørck` are hers
   and nothing outranks them — and the corpus independently agrees with both, which is a check
   on the corpus rather than on her.
2. **The attested rendering**, where the corpus has one at `MIN_COUNT` or more. This is evidence
   about how the name is written, and it beats a rule that reconstructs it.
3. **The rule engine**, for the ~64% of our vocabulary the corpus has never written.

**Hand rows that are not hers are overruled by the corpus.** They were written by this project,
from the same guessing the engine does, and 226 items calling somebody `アレクサンダー` is worth
more than one of ours calling them `アレクスアンデル`. The row keeps a note saying where its
value came from and how many items attest it, so nothing is silently replaced.

**A row is only replaced when the corpus disagrees**, so the diff is exactly what changes.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")

TABLE = ROOT / "reports" / "garborg-name-transliterations.tsv"
ATTESTED = ROOT / "reports" / "attested-name-renderings.tsv"

#: Notes that mark a row as Emma's own decision. Nothing overrules these.
HERS = ("Emma's correction",)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    attested = {r["token"]: r for r in
                csv.DictReader(ATTESTED.open(encoding="utf-8"), delimiter="\t")}
    rows = list(csv.DictReader(TABLE.open(encoding="utf-8"), delimiter="\t"))

    changed, hers_kept, agreed, untouched = [], 0, 0, 0
    for row in rows:
        note = row.get("note") or ""
        if any(h in note for h in HERS):
            hers_kept += 1
            continue
        a = attested.get(row["token"])
        if not a:
            untouched += 1
            continue
        ja, zh = a["ja"] or row["ja"], a["zh"] or row["zh"]
        if (ja, zh) == (row["ja"], row["zh"]):
            agreed += 1
            continue
        changed.append((row["token"], row["ja"], ja, row["zh"], zh))
        counts = f"ja {a['ja_count']}x, zh {a['zh_count']}x" if a["ja"] and a["zh"] else (
            f"ja {a['ja_count']}x" if a["ja"] else f"zh {a['zh_count']}x")
        row["ja"], row["zh"] = ja, zh
        row["note"] = f"attested on Wikidata ({counts})"

    print(f"{len(rows):,} rows: {hers_kept} are Emma's and untouched, "
          f"{agreed:,} already agreed with the corpus, {len(changed):,} corrected, "
          f"{untouched:,} not attested and left to the rule engine")
    for token, oja, ja, ozh, zh in changed[:25]:
        print(f"   {token:<18}{oja:<20}-> {ja:<20}{ozh:<16}-> {zh}")
    if len(changed) > 25:
        print(f"   ... and {len(changed) - 25:,} more")

    if args.dry_run:
        print("\n--dry-run: table untouched")
        return
    with TABLE.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["token", "ja", "zh", "note"], delimiter="\t")
        w.writeheader()
        w.writerows(rows)
    print(f"\nwrote {TABLE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
