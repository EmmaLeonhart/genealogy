"""Plan item 5 — family links, and the parents that have to be invented.

Emma, 2026-08-12: *"And family links. Noting that sibling relationships without
parents need to get two parents that are 'father of x and y' and 'mother of x and
y' and geni linked if possible. Mother father spouse and child is easier."*

Two halves, and they are very different in kind:

* **Derived links** — father, mother, spouse, child, read straight off the `FAM`
  records. Conversion, not invention.
* **Invented parents** — a sibling group with no parent recorded needs two
  placeholder people so the siblings hang off something. **This is the first
  step in the plan that creates data rather than converting it**, so the shapes
  are counted before anything is generated, and the generated rows are kept in
  their own file rather than mixed in with derived ones.

Matching is genealogical only — her governing rule — so nothing here uses a name
to decide anything. Names are used solely to *label* an invented parent.

Writes `reports/derived-family.csv` (one row per person) and
`reports/invented-parents.csv` (one row per placeholder). Offline.

    py scripts/derive-family.py
"""

from __future__ import annotations

import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from genimerge import doubles  # noqa: E402

MERGED = REPO_ROOT / "out" / "merged.ged"
PAIRS = REPO_ROOT / "out" / "wikidata" / "p2600-all.tsv"
LABELS = REPO_ROOT / "reports" / "derived-labels.csv"
OUT_PEOPLE = REPO_ROOT / "reports" / "derived-family.csv"
OUT_INVENTED = REPO_ROOT / "reports" / "invented-parents.csv"

csv.field_size_limit(10_000_000)


def main() -> int:
    qids: dict[str, str] = {}
    if PAIRS.exists():
        seen: dict[str, set[str]] = {}
        for qid, geni_id in doubles.load_pairs(PAIRS):
            seen.setdefault(geni_id, set()).add(qid)
        qids = {g: next(iter(q)) for g, q in seen.items() if len(q) == 1}

    labels: dict[str, str] = {}
    if LABELS.exists():
        with open(LABELS, encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                labels[row["geni_id"]] = row["label_en"] or row["cjk_names"].split(" | ")[0]

    print(f"reading {MERGED}", flush=True)
    families: dict[str, dict] = {}
    people: set[str] = set()
    current: str | None = None
    kind = ""

    with open(MERGED, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.startswith("0 "):
                parts = line.split()
                current, kind = None, ""
                if len(parts) >= 3 and parts[1].startswith("@") and parts[1].endswith("@"):
                    xref = parts[1]
                    if parts[2] == "FAM" and xref.startswith("@F"):
                        current, kind = xref[2:-1], "FAM"
                        families[current] = {"husb": "", "wife": "", "chil": []}
                    elif parts[2] == "INDI" and xref.startswith("@I"):
                        people.add(xref[2:-1])
                continue
            if kind != "FAM" or current is None:
                continue
            parts = line.rstrip("\n").split(None, 2)
            if len(parts) < 3 or parts[0] != "1":
                continue
            tag, value = parts[1], parts[2].strip()
            if not (value.startswith("@I") and value.endswith("@")):
                continue
            other = value[2:-1]
            if tag == "HUSB":
                families[current]["husb"] = other
            elif tag == "WIFE":
                families[current]["wife"] = other
            elif tag == "CHIL":
                families[current]["chil"].append(other)

    print(f"{len(people):,} people, {len(families):,} families", flush=True)

    father: dict[str, str] = {}
    mother: dict[str, str] = {}
    spouses: dict[str, list[str]] = defaultdict(list)
    children: dict[str, list[str]] = defaultdict(list)

    shapes: Counter[str] = Counter()
    needs_parents: list[tuple[str, list[str]]] = []

    for fam_id, fam in families.items():
        husb, wife, chil = fam["husb"], fam["wife"], fam["chil"]

        if husb and wife:
            if wife not in spouses[husb]:
                spouses[husb].append(wife)
            if husb not in spouses[wife]:
                spouses[wife].append(husb)

        for child in chil:
            if husb:
                father[child] = husb
                if child not in children[husb]:
                    children[husb].append(child)
            if wife:
                mother[child] = wife
                if child not in children[wife]:
                    children[wife].append(child)

        # The shape census. Counted before anything is invented.
        if chil and not husb and not wife:
            shapes["children, no parent recorded" if len(chil) > 1
                   else "one child, no parent recorded"] += 1
            if len(chil) > 1:
                needs_parents.append((fam_id, chil))
        elif chil and (husb and not wife):
            shapes["children, father only"] += 1
        elif chil and (wife and not husb):
            shapes["children, mother only"] += 1
        elif chil:
            shapes["children, both parents"] += 1
        elif husb and wife:
            shapes["couple, no children"] += 1
        elif husb or wife:
            shapes["one spouse alone"] += 1
        else:
            shapes["empty"] += 1

    OUT_PEOPLE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PEOPLE, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["geni_id", "qid", "father", "father_qid", "mother", "mother_qid",
                         "spouses", "spouse_qids", "children", "child_count"])
        for person in sorted(people):
            f, m = father.get(person, ""), mother.get(person, "")
            sp = spouses.get(person, [])
            ch = children.get(person, [])
            writer.writerow([
                person, qids.get(person, ""),
                f, qids.get(f, "") if f else "",
                m, qids.get(m, "") if m else "",
                " | ".join(sp), " | ".join(qids.get(s, "") for s in sp),
                " | ".join(ch), len(ch),
            ])

    def name_of(geni_id: str) -> str:
        return labels.get(geni_id) or geni_id

    with open(OUT_INVENTED, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["family", "role", "proposed_label", "children", "child_count",
                         "children_with_qid"])
        for fam_id, chil in needs_parents:
            names = [name_of(c) for c in chil]
            joined = " and ".join(names) if len(names) <= 3 else (
                ", ".join(names[:-1]) + " and " + names[-1])
            linked = sum(1 for c in chil if c in qids)
            for role in ("father", "mother"):
                writer.writerow([fam_id, role, f"{role} of {joined}",
                                 " | ".join(chil), len(chil), linked])

    with_father = sum(1 for p in people if p in father)
    with_mother = sum(1 for p in people if p in mother)
    with_spouse = sum(1 for p in people if spouses.get(p))
    with_child = sum(1 for p in people if children.get(p))

    print(f"wrote {OUT_PEOPLE} ({len(people):,} rows)")
    print(f"wrote {OUT_INVENTED} ({2*len(needs_parents):,} rows, "
          f"{len(needs_parents):,} families)")
    print()
    print(f"  father recorded  {with_father:>8,}")
    print(f"  mother recorded  {with_mother:>8,}")
    print(f"  spouse recorded  {with_spouse:>8,}")
    print(f"  children         {with_child:>8,}")
    print()
    print("family shapes:")
    for shape, n in shapes.most_common():
        print(f"  {n:>8,}  {shape}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
