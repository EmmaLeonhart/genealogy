"""How much of the merged tree is BCE recorded as positive years.

`out/merged.ged` contains **zero** `BC` strings, so BCE is not rare in this
corpus — it is unrepresentable. Five people give themselves away by carrying a
birth year later than 2026 (all Egyptian pharaohs), but a BCE person born in a
year below 2026 is indistinguishable from a CE one by looking at the number.

So this does not look at the numbers. It looks at **direction**, which BCE
inverts:

``birth after death``
    A BCE lifespan runs 2111 → 2046. Noisy on its own: a truncated date
    (``2 DATE 12``, a day with no year) trips it too, so those are separated
    rather than counted together.

``parent born after child``
    The structural one. In CE a parent's year is smaller than their child's; in
    BCE-as-positive it is larger. This catches whole lineages rather than
    individuals, which is what makes it a size estimate instead of a list.

``ancestors of a confirmed BCE person``
    The one certainty available. Everyone above a pharaoh is BCE, whatever their
    recorded year says, so this is a **lower bound** that needs no inference.

Nothing here corrects a date. Deciding what the corpus should hold is Emma's,
and this exists to put a number in front of that decision.
"""

from __future__ import annotations

import io
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MERGED = ROOT / "out" / "merged.ged"

#: Years after this cannot be a birth, so the era marker is certainly missing.
TODAY = 2026


def _year(text: str) -> int | None:
    for token in reversed(text.replace(",", " ").split()):
        if token.isdigit():
            return int(token)
    return None


def read_tree(path: Path):
    """``(births, deaths, names, raw_birth, child_to_parents)``."""
    births: dict[str, int] = {}
    deaths: dict[str, int] = {}
    names: dict[str, str] = {}
    raw_birth: dict[str, str] = {}
    famc: dict[str, str] = {}
    fam_parents: dict[str, list[str]] = defaultdict(list)
    fam_children: dict[str, list[str]] = defaultdict(list)

    person = fam = None
    tag = None
    with io.open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith("0 "):
                parts = line.split(" ")
                ref = parts[1] if len(parts) > 2 else ""
                person = ref if ref.startswith("@I") else None
                fam = ref if ref.startswith("@F") else None
                tag = None
            elif person:
                if line.startswith("1 NAME") and person not in names:
                    names[person] = line[7:]
                elif line.startswith("1 BIRT"):
                    tag = "B"
                elif line.startswith("1 DEAT"):
                    tag = "D"
                elif line.startswith("1 FAMC"):
                    famc.setdefault(person, line.split(" ")[2])
                    tag = None
                elif line.startswith("1 "):
                    tag = None
                elif line.startswith("2 DATE") and tag:
                    value = line[7:]
                    if tag == "B" and person not in births:
                        year = _year(value)
                        if year is not None:
                            births[person] = year
                            raw_birth[person] = value
                    elif tag == "D" and person not in deaths:
                        year = _year(value)
                        if year is not None:
                            deaths[person] = year
            elif fam:
                if line.startswith("1 HUSB") or line.startswith("1 WIFE"):
                    fam_parents[fam].append(line.split(" ")[2])
                elif line.startswith("1 CHIL"):
                    fam_children[fam].append(line.split(" ")[2])

    parents_of: dict[str, list[str]] = defaultdict(list)
    for child, family in famc.items():
        parents_of[child].extend(fam_parents.get(family, ()))
    for family, kids in fam_children.items():
        for kid in kids:
            for parent in fam_parents.get(family, ()):
                if parent not in parents_of[kid]:
                    parents_of[kid].append(parent)
    return births, deaths, names, raw_birth, parents_of


def main() -> int:
    if not MERGED.exists():
        print(f"{MERGED} not found", file=sys.stderr)
        return 1

    births, deaths, names, raw_birth, parents_of = read_tree(MERGED)
    print(f"tree: {len(names):,} named, {len(births):,} with a birth year")

    certain = sorted((y, p) for p, y in births.items() if y > TODAY)
    print(f"\ncertainly BCE (birth year after {TODAY}): {len(certain)}")
    for year, person in sorted(certain, reverse=True):
        print(f"  {year}  {names.get(person, '?')}")

    # Everyone above a confirmed BCE person is BCE too, whatever their year says.
    seen: set[str] = set()
    stack = [p for _, p in certain]
    while stack:
        person = stack.pop()
        for parent in parents_of.get(person, ()):
            if parent not in seen:
                seen.add(parent)
                stack.append(parent)
    print(f"\nancestors of those five (certainly BCE, a lower bound): {len(seen):,}")
    dated = [p for p in seen if p in births]
    if dated:
        years = sorted(births[p] for p in dated)
        print(f"  of which dated: {len(dated):,}   year range {years[0]}-{years[-1]}")

    # Direction, not magnitude.
    inverted = [
        (p, births[p], deaths[p])
        for p in births
        if p in deaths and births[p] > deaths[p]
    ]
    truncated = [t for t in inverted if t[2] < 100 <= t[1]]
    print(f"\nbirth year after death year: {len(inverted):,}")
    print(f"  of those, a truncated death date (death < 100, birth >= 100): {len(truncated):,}")
    print(f"  remainder, BCE-shaped: {len(inverted) - len(truncated):,}")

    pairs = 0
    people_in_pairs: set[str] = set()
    for child, parents in parents_of.items():
        if child not in births:
            continue
        for parent in parents:
            if parent in births and births[parent] > births[child]:
                pairs += 1
                people_in_pairs.update((parent, child))
    print(f"\nparent born after child: {pairs:,} pairs, {len(people_in_pairs):,} people")
    print("  (BCE inverts this direction; it also catches ordinary data errors)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
