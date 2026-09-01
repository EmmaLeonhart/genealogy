"""Print the ancestry we actually hold above a person, so a divergence is visible.

Written because the Charlemagne blood line resolved only 4 of 38 steps and the
question "what is there instead?" needs the tree's own answer, not a guess.

    py scripts/show-ancestry.py [geni_id] [generations]
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FAMILY = REPO_ROOT / "reports" / "derived-family.csv"
LABELS = REPO_ROOT / "reports" / "derived-labels.csv"
FACTS = REPO_ROOT / "reports" / "derived-facts.csv"

csv.field_size_limit(10_000_000)
EMMA = "6000000001846508982"


def main() -> int:
    start = sys.argv[1] if len(sys.argv) > 1 else EMMA
    depth = int(sys.argv[2]) if len(sys.argv) > 2 else 8

    fam = {r["geni_id"]: r for r in csv.DictReader(open(FAMILY, encoding="utf-8"))}
    lab = {r["geni_id"]: r for r in csv.DictReader(open(LABELS, encoding="utf-8"))}
    fac = {r["geni_id"]: r for r in csv.DictReader(open(FACTS, encoding="utf-8"))}

    kids: dict[str, list[str]] = {}
    for geni_id, row in fam.items():
        for parent in (row.get("father"), row.get("mother")):
            if parent:
                kids.setdefault(parent, []).append(geni_id)

    def show(g: str) -> str:
        name = (lab.get(g, {}).get("label_en") or "(no label)")
        born = fac.get(g, {}).get("birth_date_year", "") or "?"
        died = fac.get(g, {}).get("death_date_year", "") or "?"
        qid = lab.get(g, {}).get("qid", "")
        return (f"{name}  b.{born} d.{died}  {g}"
                f"{'  ' + qid if qid else ''}  [{len(kids.get(g, []))} children]")

    def walk(g: str, level: int, ahn: int, label: str) -> None:
        if level > depth or g not in fam:
            return
        print(f"{'  ' * level}{ahn:>5} {label:<7} {show(g)}")
        row = fam[g]
        for role, tag in (("father", "father"), ("mother", "mother")):
            parent = row.get(role)
            if parent:
                walk(parent, level + 1, ahn * 2 + (0 if role == "father" else 1), tag)
            else:
                print(f"{'  ' * (level+1)}{ahn*2 + (0 if role=='father' else 1):>5} "
                      f"{tag:<7} — none recorded")

    print(f"ancestry above {start}, {depth} generations\n")
    walk(start, 0, 1, "self")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
