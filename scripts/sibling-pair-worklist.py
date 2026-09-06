"""Who still needs the immediate-family scrape. EVERY member of EVERY sibling pair.

**Emma, 2026-09-06, and she said it twice because it looks redundant and is not:** *"every single
sibling pair gets the small scrape done on it. The one that just gets their immediate relatives is
something that needs to be done on every single person, every single person in sibling pairs. And,
yes, I know this is slightly redundant, but I'm telling you to do it. I'm telling you to do it."*

**Why both members and not one.** A path names a sibling hop and never names the parents -- Geni
records no sibling edge, so a path can only say *these two are siblings*. Under her ruling that an
unknown parent is an absent slot, the path GEDCOM writes them as a family with two `CHIL` and no
partners. The parents arrive from the members' own profile pages, and scraping only one of the
pair gets one side's account of them. Her words: *"it'll create a gedcom for each one of the
members of the sibling pair, and then this links them as siblings with their parents in this new
gedcom file, but they're also linked as siblings in the path gedcom files."*

The merge fuses the three on the Geni id, so the parentless sibling family and the two parented
families become one family with real parents.

**Scale, and why it is not optional:** `CLAUDE.md` § *A sibling step is the worked example* --
sibling hops are **7% of all path rows, present in 662 of 698 paths**. Dropping them puts a hole
in almost every path.

## ⛔ THE PHASE ORDER STILL GOVERNS WHAT THIS LIST IS FOR

`docs/per-individual-loop.md`: phase 3 scrapes the sibling pairs that are **still parentless in
the integrated tree**, not the ones a path file happens to name today. Her correction of
2026-09-06: *"jumping to the mass action was really bad because you skipped over a lot."*

So this script reports both, and never conflates them:

  * **from the paths** -- every sibling pair the path GEDCOMs contain, which is the full
    population and the thing she has just asked to be covered;
  * **still parentless** -- of those, the ones for whom no profile scrape yet exists, which is
    the actual work queue.

It writes `reports/sibling-pair-worklist.tsv` and prints the counts.
"""

from __future__ import annotations

import csv
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
TINY_PATHS = ROOT / "exports" / "tiny-paths"
FAMILIES = ROOT / "geni-families"
OUT = ROOT / "reports" / "sibling-pair-worklist.tsv"


def sibling_pairs():
    """Every CHIL-only family in the path GEDCOMs -- that is exactly a sibling hop."""
    pairs = []
    for p in sorted(TINY_PATHS.glob("*.ged")):
        text = p.read_text(encoding="utf-8")
        names = dict(re.findall(r"0 @I(\d+)@ INDI\n1 NAME ([^\n]*)", text))
        for block in re.split(r"\n(?=0 @F)", text):
            if not block.startswith("0 @F"):
                continue
            if "1 HUSB" in block or "1 WIFE" in block:
                continue
            chil = re.findall(r"1 CHIL @I(\d+)@", block)
            if len(chil) >= 2:
                pairs.append((p.stem, chil, names))
    return pairs


def main():
    scraped = {q.name.split("-")[0] for q in FAMILIES.glob("*-family.tsv")}
    pairs = sibling_pairs()

    rows = []
    people = set()
    for path_name, chil, names in pairs:
        for gid in chil:
            people.add(gid)
            rows.append({
                "geni_id": gid,
                "name": names.get(gid, ""),
                "path": path_name,
                "pair_with": ";".join(c for c in chil if c != gid),
                "scraped": "yes" if gid in scraped else "",
            })

    # Deterministic and total: the geni id is unique per row within a path.
    rows.sort(key=lambda r: (r["geni_id"], r["path"]))
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, delimiter="\t",
                           fieldnames=["geni_id", "name", "path", "pair_with", "scraped"])
        w.writeheader()
        w.writerows(rows)

    todo = sorted({r["geni_id"] for r in rows if not r["scraped"]})
    print("sibling pairs found in the path gedcoms : %d" % len(pairs))
    print("distinct people in a sibling pair       : %d" % len(people))
    print("  already have a profile scrape         : %d" % len(people - set(todo)))
    print("  STILL NEED ONE                        : %d" % len(todo))
    print("wrote %s" % OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
