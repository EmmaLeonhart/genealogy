"""Who still needs the immediate-family scrape. EVERY member of EVERY sibling pair.

**Every member of every sibling pair gets the small immediate-relatives scrape.** The redundancy
is deliberate and instructed; it is not an oversight to optimise away.

**Why both members and not one.** A path names a sibling hop and never names the parents -- Geni
records no sibling edge, so a path can only say *these two are siblings*. Under the rule that an
unknown parent is an absent slot, the path GEDCOM writes them as a family with two `CHIL` and no
partners. The parents arrive from the members' own profile pages, and scraping only one of the
pair gets one side's account of them. Each member yields a GEDCOM linking the pair as siblings
with their parents, alongside the sibling link the path GEDCOMs already carry.

The merge fuses the three on the Geni id, so the parentless sibling family and the two parented
families become one family with real parents.

**Scale, and why it is not optional:** `CLAUDE.md` § *A sibling step is the worked example* --
sibling hops are **7% of all path rows, present in 662 of 698 paths**. Dropping them puts a hole
in almost every path.

## ⛔ THE PHASE ORDER STILL GOVERNS WHAT THIS LIST IS FOR

`docs/per-individual-loop.md`: phase 3 scrapes the sibling pairs that are **still parentless in
the integrated tree**, not the ones a path file happens to name today. Jumping straight to the
mass action skips over a great deal and is the failure this ordering exists against.

So this script reports both, and never conflates them:

  * **from the paths** -- every sibling pair the path GEDCOMs contain, which is the full
    population and the thing to be covered;
  * **still parentless** -- of those, the ones the SYNOPTIC TREE has no parent for, which is
    the actual work queue.

⛔ **PARENTLESS MEANS PARENTLESS IN THE TREE, NOT "NO SCRAPE FILE".** This script tested
`geni-families/<id>-family.tsv` for existence and called that the queue. Emma, 2026-09-16:
*"it does not just need to read the tiny-paths, it needs the entire synoptic tree to ensure that
the parents are not present anywhere."* A sibling pair's parents can arrive from any ordinary
export under `exports/`, from a Wikidata identification, or from another path entirely, and none
of those leaves a file in `geni-families/`. The proxy would have sent the collector to re-scrape
people whose parents the tree already knew -- the expensive half of a campaign that costs a real
page load per person.

`reports/derived-family.csv` is the test: `father` and `mother`, derived from `out/merged.ged`.
Empty in both means nobody in the union tree knows who this person's parents are. **Which is why
this belongs in `tree.yml` and cannot be pulled out of it** -- the derived layer is what the
rebuild has just produced, and a workflow reading only `exports/tiny-paths/` answers quickly and
wrongly.

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
#: The derived layer, from the merged tree. Committed gzipped; a rebuild leaves the plain file.
DERIVED = ROOT / "reports" / "derived-family.csv"


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


def parented(wanted):
    """Of `wanted`, the geni ids the synoptic tree records a father or a mother for.

    Streamed: the file is ~190 MB. Falls back to the committed `.gz` so a clean clone works.
    """
    if DERIVED.exists():
        open_it = lambda: DERIVED.open(encoding="utf-8", newline="")
    elif DERIVED.with_name(DERIVED.name + ".gz").exists():
        import gzip
        gz = DERIVED.with_name(DERIVED.name + ".gz")
        open_it = lambda: gzip.open(gz, "rt", encoding="utf-8", newline="")
    else:
        # ⛔ FAIL LOUD AND CLAIM NOTHING. With no derived layer the honest answer is "unknown",
        # and calling everybody parentless would send the collector at all of them.
        raise SystemExit("%s is absent -- run pack-derived.py --unpack or rebuild the tree"
                         % DERIVED.relative_to(ROOT))
    have = set()
    with open_it() as fh:
        for row in csv.DictReader(fh):
            gid = (row.get("geni_id") or "").strip()
            if gid in wanted and ((row.get("father") or "").strip()
                                  or (row.get("mother") or "").strip()):
                have.add(gid)
    return have


def main():
    scraped = {q.name.split("-")[0] for q in FAMILIES.glob("*-family.tsv")}
    pairs = sibling_pairs()

    people = {gid for _p, chil, _n in pairs for gid in chil}
    has_parent = parented(people)

    rows = []
    for path_name, chil, names in pairs:
        for gid in chil:
            rows.append({
                "geni_id": gid,
                "name": names.get(gid, ""),
                "path": path_name,
                "pair_with": ";".join(c for c in chil if c != gid),
                # Informational only. The QUEUE is `parent_in_tree`.
                "scraped": "yes" if gid in scraped else "",
                "parent_in_tree": "yes" if gid in has_parent else "",
            })

    # Deterministic and total: the geni id is unique per row within a path.
    rows.sort(key=lambda r: (r["geni_id"], r["path"]))
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, delimiter="\t",
                           fieldnames=["geni_id", "name", "path", "pair_with", "scraped",
                                       "parent_in_tree"])
        w.writeheader()
        w.writerows(rows)

    todo = sorted({r["geni_id"] for r in rows if not r["parent_in_tree"]})
    print("sibling pairs found in the path gedcoms : %d" % len(pairs))
    print("distinct people in a sibling pair       : %d" % len(people))
    print("  the tree already knows a parent       : %d" % len(has_parent))
    print("  STILL PARENTLESS -- the work queue    : %d" % len(todo))
    print("  (of those, scraped once already       : %d)" % len(set(todo) & scraped))
    print("wrote %s" % OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
