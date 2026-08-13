"""How many family-tree hops from a person to somebody who has a Wikidata item?

Emma, 2026-08-12: *"I'd like you to look through my ancestry and ascend through
my ancestry to find the earliest one of my ancestors that has a Wikidata item …
It wouldn't necessarily be the earliest ancestor. It would just be the least
amount of hops in the family tree to somebody with a Wikidata item."*

So this is a breadth-first search over the family graph, not a climb up the
ancestral line. Two runs, because they answer different questions:

* **ancestors only** — parents, then grandparents, and so on. The literal
  "ascend through my ancestry".
* **any relation** — parents, children, spouses and siblings. The literal "least
  amount of hops in the family tree", which can go sideways and is never longer.

Every step is reported, so the path can be read rather than trusted.

    py scripts/nearest-wikidata-relative.py                    # Emma
    py scripts/nearest-wikidata-relative.py <geni_id>
"""

from __future__ import annotations

import csv
import sys
from collections import deque
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

FAMILY = REPO_ROOT / "reports" / "derived-family.csv"
LABELS = REPO_ROOT / "reports" / "derived-labels.csv"
FACTS = REPO_ROOT / "reports" / "derived-facts.csv"

csv.field_size_limit(10_000_000)

EMMA = "6000000087535357291"


def load():
    fam = {r["geni_id"]: r for r in csv.DictReader(open(FAMILY, encoding="utf-8"))}
    lab = {r["geni_id"]: r for r in csv.DictReader(open(LABELS, encoding="utf-8"))}
    fac = {r["geni_id"]: r for r in csv.DictReader(open(FACTS, encoding="utf-8"))}
    return fam, lab, fac


def neighbours(fam: dict, geni_id: str, ancestors_only: bool):
    row = fam.get(geni_id)
    if not row:
        return
    for parent, role in ((row.get("father"), "father"), (row.get("mother"), "mother")):
        if parent:
            yield parent, role
    if ancestors_only:
        return
    for column, role in (("children", "child"), ("spouses", "spouse")):
        for other in (row.get(column) or "").split(" | "):
            if other:
                yield other, role


def search(fam: dict, lab: dict, start: str, ancestors_only: bool):
    """BFS to the nearest person carrying a QID. Returns the path, or None."""
    seen = {start}
    queue = deque([(start, [])])
    visited = 0
    while queue:
        current, path = queue.popleft()
        visited += 1
        if current != start and lab.get(current, {}).get("qid"):
            return path + [(current, "")], visited
        for other, role in neighbours(fam, current, ancestors_only):
            if other in seen:
                continue
            seen.add(other)
            queue.append((other, path + [(current, role)]))
    return None, visited


def describe(lab: dict, fac: dict, geni_id: str) -> str:
    name = lab.get(geni_id, {}).get("label_en") or \
        (lab.get(geni_id, {}).get("cjk_names") or "").split(" | ")[0] or "(no name)"
    born = fac.get(geni_id, {}).get("birth_date_year", "")
    died = fac.get(geni_id, {}).get("death_date_year", "")
    span = f" {born}–{died}" if born or died else ""
    qid = lab.get(geni_id, {}).get("qid", "")
    return f"{name}{span}" + (f"  [{qid}]" if qid else "")


def main() -> int:
    start = sys.argv[1] if len(sys.argv) > 1 else EMMA
    fam, lab, fac = load()
    if start not in fam:
        print(f"{start} is not in the tree")
        return 1

    print(f"start: {start}  {describe(lab, fac, start)}")
    print(f"       carries an item already: {'yes' if lab.get(start,{}).get('qid') else 'no'}\n")

    for ancestors_only, title in ((True, "ancestors only (parents upward)"),
                                  (False, "any relation (parents, children, spouses)")):
        path, visited = search(fam, lab, start, ancestors_only)
        print(f"--- {title}")
        if path is None:
            print(f"    no relative with a Wikidata item found; {visited:,} people reached\n")
            continue
        print(f"    {len(path)-1} hops, {visited:,} people searched")
        for step, (geni_id, role) in enumerate(path):
            arrow = f"  --{role}-->" if role else ""
            print(f"      {step}. {describe(lab, fac, geni_id)}{arrow}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
