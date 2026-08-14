"""Walk Emma's ancestry across every export in the corpus and report where it stops.

Answers "which of my ancestors are missing?" without touching a saved HTML page:
the only evidence used is the GEDCOMs under ``exports/``. A person is *missing*
here in exactly one sense — an ancestor we hold has no father and/or no mother
recorded anywhere in the corpus, so the line ends at them. Whether Geni holds a
parent there is what an export from that person answers.

Reads the exports directly rather than ``out/merged.ged`` so a fresh download
counts the moment it is extracted.

    py scripts/build-ancestry-deadends.py
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from genimerge.sources import find_exports  # noqa: E402

EMMA = "6000000087535357291"
OUT = REPO_ROOT / "reports" / "ancestry-deadends.csv"
OUT_ALL = REPO_ROOT / "reports" / "ancestry-held.csv"


def scan(path: Path, name, birth, death, father, mother):
    """Fold one GEDCOM into the shared name/date/parent maps."""
    fam_parents: dict[str, list[str]] = {}
    fam_children: dict[str, list[str]] = {}
    cur_indi = None
    cur_fam = None
    in_name = in_birt = in_deat = False
    pending_famc: dict[str, list[str]] = {}

    with path.open(encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            line = raw.rstrip("\r\n")
            if not line:
                continue
            parts = line.split(" ", 2)
            level = parts[0]
            if level == "0":
                cur_indi = cur_fam = None
                in_name = in_birt = in_deat = False
                if len(parts) == 3 and parts[1].startswith("@") and parts[2] == "INDI":
                    cur_indi = parts[1].strip("@")[1:]
                elif len(parts) == 3 and parts[1].startswith("@") and parts[2] == "FAM":
                    cur_fam = parts[1].strip("@")[1:]
                continue
            tag = parts[1] if len(parts) > 1 else ""
            val = parts[2] if len(parts) > 2 else ""
            if level == "1":
                in_name = in_birt = in_deat = False
            if cur_indi:
                if level == "1" and tag == "NAME":
                    if cur_indi not in name:
                        name[cur_indi] = val.replace("/", "").strip()
                    in_name = True
                elif level == "1" and tag == "BIRT":
                    in_birt = True
                elif level == "1" and tag == "DEAT":
                    in_deat = True
                elif level == "1" and tag == "FAMC":
                    pending_famc.setdefault(val.strip("@")[1:], []).append(cur_indi)
                elif level == "2" and tag == "DATE":
                    if in_birt and cur_indi not in birth:
                        birth[cur_indi] = val
                    elif in_deat and cur_indi not in death:
                        death[cur_indi] = val
                elif level == "2" and in_name and tag in ("GIVN", "SURN"):
                    pass
            elif cur_fam:
                if level == "1" and tag in ("HUSB", "WIFE"):
                    fam_parents.setdefault(cur_fam, []).append(
                        ("F" if tag == "HUSB" else "M") + val.strip("@")[1:]
                    )
                elif level == "1" and tag == "CHIL":
                    fam_children.setdefault(cur_fam, []).append(val.strip("@")[1:])

    for fam, kids in fam_children.items():
        for kid in kids:
            for slot in fam_parents.get(fam, []):
                role, pid = slot[0], slot[1:]
                (father if role == "F" else mother).setdefault(kid, pid)
    for fam, kids in pending_famc.items():
        for kid in kids:
            for slot in fam_parents.get(fam, []):
                role, pid = slot[0], slot[1:]
                (father if role == "F" else mother).setdefault(kid, pid)


def year(text: str) -> str:
    from genimerge.dates import parse_date

    parsed = parse_date(text) if text else None
    if parsed is None:
        return ""
    y = getattr(parsed, "year", None)
    return "" if y is None else str(y)


def main() -> int:
    name: dict[str, str] = {}
    birth: dict[str, str] = {}
    death: dict[str, str] = {}
    father: dict[str, str] = {}
    mother: dict[str, str] = {}

    files = list(find_exports(REPO_ROOT / "exports"))
    for n, path in enumerate(files, 1):
        scan(path, name, birth, death, father, mother)
        if n % 20 == 0:
            print(f"  {n}/{len(files)} exports", file=sys.stderr)
    print(f"{len(files)} exports, {len(name)} people", file=sys.stderr)

    # Breadth-first up from Emma, keeping the shallowest generation for anyone
    # reached by more than one line (pedigree collapse is dense here).
    gen: dict[str, int] = {EMMA: 0}
    order = [EMMA]
    i = 0
    while i < len(order):
        person = order[i]
        i += 1
        for parent in (father.get(person), mother.get(person)):
            if parent and parent not in gen:
                gen[parent] = gen[person] + 1
                order.append(parent)

    deadends = []
    for person in order:
        missing = []
        if person not in father:
            missing.append("father")
        if person not in mother:
            missing.append("mother")
        if missing:
            deadends.append((person, missing))

    OUT_ALL.parent.mkdir(parents=True, exist_ok=True)
    with OUT_ALL.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["generations_up", "geni_id", "name", "born", "died",
                    "has_father", "has_mother", "geni_url"])
        for person in sorted(order, key=lambda p: (gen[p], name.get(p, ""))):
            w.writerow([gen[person], person, name.get(person, ""),
                        year(birth.get(person, "")), year(death.get(person, "")),
                        "yes" if person in father else "no",
                        "yes" if person in mother else "no",
                        f"https://www.geni.com/people/x/{person}"])

    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["generations_up", "geni_id", "name", "born", "died",
                    "missing", "geni_url"])
        for person, missing in sorted(deadends, key=lambda t: (gen[t[0]], name.get(t[0], ""))):
            w.writerow([gen[person], person, name.get(person, ""),
                        year(birth.get(person, "")), year(death.get(person, "")),
                        "+".join(missing),
                        f"https://www.geni.com/people/x/{person}"])

    both = sum(1 for _, m in deadends if len(m) == 2)
    print(f"ancestors held: {len(order)}")
    print(f"lines that stop: {len(deadends)}  (no parent at all: {both})")
    print(f"wrote {OUT.relative_to(REPO_ROOT)} and {OUT_ALL.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
