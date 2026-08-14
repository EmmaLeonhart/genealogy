"""Every family record touching the Samaritan priestly families, one row each.

Emma's rule (CLAUDE.md § *"Analyse this" means build a CSV of every instance*):
build the census first, commit it, then analyse it. So this writes two CSVs and
draws no conclusions.

**The set is the priestly families as Geni holds them**, seeded from the two
runs of priests found in the corpus and then grown **one hop** along every
parent, child and spouse edge, so a wife recorded anywhere is caught even though
she is not a priest:

  * the post-1624 Itamar component rooted at Tabia ha'Abta'i;
  * the pre-1624 chain whose profiles carry `Samaritan High Priest` in the
    surname field.

The seeds are found by **profile ID**, never by name — `Shalma` matches
`Shalmaneser V` and `Abisha` matches `Abishai`, and both of those have already
cost this project a wrong answer.

Dates go through `genimerge.dates`, which is the only thing here allowed to read
a GEDCOM date. Every part of every date is written, because a caller that writes
a subset silently discards what the grammar recovered.

    py scripts/build-samaritan-marriage-census.py
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from genimerge import sources  # noqa: E402
from genimerge.dates import DATE_FIELDS, date_fields  # noqa: E402

#: Tabia ha'Abta'i - the root of the post-1624 component.
TABIA = "6000000220294810877"

#: The pre-1624 chain is recognised by this string in the GEDCOM surname slot.
#: It is an OFFICE sitting in the surname field, not a family name - the same
#: shape as `SURN 秦州成紀` in CLAUDE.md. Used here only to find the seeds.
PRIEST_SURNAME = "Samaritan High Priest"

LINE = re.compile(r"^(\d+) (?:(@[^@]+@) )?(\w+)(?: (.*))?$")


def scan(path: Path):
    """One export -> (individuals, families). Flat dicts, no merging."""
    indi: dict[str, dict] = {}
    fam: dict[str, dict] = {}
    cur = kind = None
    sub = None
    for raw in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        m = LINE.match(raw.rstrip("\n"))
        if not m:
            continue
        level, xref, tag, val = m.group(1), m.group(2), m.group(3), (m.group(4) or "")
        if level == "0":
            sub = None
            if tag == "INDI":
                cur, kind = xref, "indi"
                indi[xref] = {"id": xref, "name": "", "sex": "", "occu": "",
                              "birt": "", "deat": "", "famc": [], "fams": []}
            elif tag == "FAM":
                cur, kind = xref, "fam"
                fam[xref] = {"id": xref, "husb": "", "wife": "", "chil": [],
                             "marr": "", "marr_plac": "", "div": ""}
            else:
                cur = kind = None
            continue
        if cur is None:
            continue
        if kind == "indi":
            rec = indi[cur]
            if level == "1":
                sub = tag
                if tag == "NAME" and not rec["name"]:
                    rec["name"] = val
                elif tag in ("SEX", "OCCU"):
                    rec[tag.lower()] = val
                elif tag == "FAMC":
                    rec["famc"].append(val)
                elif tag == "FAMS":
                    rec["fams"].append(val)
            elif level == "2" and tag == "DATE" and sub in ("BIRT", "DEAT"):
                rec[sub.lower()] = rec[sub.lower()] or val
        else:
            rec = fam[cur]
            if level == "1":
                sub = tag
                if tag == "HUSB":
                    rec["husb"] = val
                elif tag == "WIFE":
                    rec["wife"] = val
                elif tag == "CHIL":
                    rec["chil"].append(val)
            elif level == "2" and sub in ("MARR", "DIV"):
                if tag == "DATE":
                    key = "marr" if sub == "MARR" else "div"
                    rec[key] = rec[key] or val
                elif tag == "PLAC" and sub == "MARR":
                    rec["marr_plac"] = rec["marr_plac"] or val
    return indi, fam


def gid(xref: str) -> str:
    return xref.strip("@")[1:] if xref else ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--people-out", default="reports/samaritan-people.csv")
    ap.add_argument("--families-out", default="reports/samaritan-marriages.csv")
    ap.add_argument("--hops", type=int, default=1,
                    help="family-edge hops out from the seeds (1 = the priests "
                         "plus everyone directly attached to them)")
    args = ap.parse_args()

    exports = sources.find_exports()
    print(f"{len(exports)} distinct exports")

    # ---- pass 1: read everything once, keep it -----------------------------
    per_export = []
    for n, path in enumerate(exports, 1):
        per_export.append((path, *scan(path)))
        if n % 20 == 0:
            print(f"  read {n}/{len(exports)}")

    # ---- seeds, by profile ID and by the office-in-surname marker ----------
    seeds: set[str] = set()
    for path, indi, fam in per_export:
        for x, rec in indi.items():
            if gid(x) == TABIA or PRIEST_SURNAME in rec["name"]:
                seeds.add(x)
    print(f"{len(seeds)} seed profiles")

    # ---- grow the set: the seeds' whole connected runs, then one hop out ---
    # Walking families rather than a name screen is the CLAUDE.md rule about
    # measuring the neighbourhood instead of the surname.
    # One adjacency over the whole corpus, then a single breadth-first walk.
    # Re-scanning every export once per round instead was quadratic and did not
    # finish; the family memberships are the same however often they are read.
    from collections import deque
    person_fams: dict[str, set[str]] = {}
    fam_people: dict[str, set[str]] = {}
    for path, indi, fam in per_export:
        for f, frec in fam.items():
            people = {frec["husb"], frec["wife"], *frec["chil"]} - {""}
            fam_people.setdefault(f, set()).update(people)
            for p in people:
                person_fams.setdefault(p, set()).add(f)

    # **Bounded, and the bound is load-bearing.** An unbounded walk is not "the
    # priestly families" - the pre-1624 chain sits inside a 4056-person ball that
    # is part of the world tree, so closing over family edges returned 394,890
    # people and answered a question nobody asked. `--hops 1` is the priests plus
    # everyone directly attached to them, which is what a question about their
    # wives, mothers and children means.
    # Tabia's descendants are the modern priestly family and none of them carry
    # the office in their surname, so they are not seeds. Walk DOWN from every
    # seed first, unbounded: descent is the lineage and is what "the priestly
    # families" means. (Walking up as well would leave via the pre-1624 chain's
    # neighbours into the world tree, which is the runaway this replaced.)
    children_of: dict[str, set[str]] = {}
    for path, indi, fam in per_export:
        for f, frec in fam.items():
            for parent in (frec["husb"], frec["wife"]):
                if parent:
                    children_of.setdefault(parent, set()).update(frec["chil"])
    line = set(seeds)
    todo = deque(seeds)
    while todo:
        p = todo.popleft()
        for c in children_of.get(p, ()):
            if c not in line:
                line.add(c)
                todo.append(c)
    print(f"{len(line)} people in the seeds' descent")

    members = set(line)
    frontier = set(line)
    for _ in range(args.hops):
        nxt: set[str] = set()
        for p in frontier:
            for f in person_fams.get(p, ()):
                nxt |= fam_people.get(f, set())
        nxt -= members
        members |= nxt
        frontier = nxt
        if not nxt:
            break
    print(f"{len(members)} people within {args.hops} hop(s) of a seed")

    # ---- families involving any of them, one row per (export, family) ------
    frows = []
    prows = []
    for path, indi, fam in per_export:
        rel = str(path.relative_to(REPO))
        for f, frec in fam.items():
            people = {frec["husb"], frec["wife"], *frec["chil"]} - {""}
            if not (people & members):
                continue
            h = indi.get(frec["husb"], {})
            w = indi.get(frec["wife"], {})
            row = {
                "export": rel,
                "family_id": gid(f),
                "husband_geni_id": gid(frec["husb"]),
                "husband_name": h.get("name", ""),
                "wife_geni_id": gid(frec["wife"]),
                "wife_name": w.get("name", ""),
                "has_wife": "yes" if frec["wife"] else "no",
                "n_children": len(frec["chil"]),
                "children_geni_ids": " ".join(gid(c) for c in frec["chil"]),
                "children_names": " | ".join(
                    indi.get(c, {}).get("name", "") for c in frec["chil"]),
                "marr_place": frec["marr_plac"],
                "div_raw": frec["div"],
            }
            row.update({f"marr_{k}": v for k, v in date_fields(frec["marr"]).items()})
            frows.append(row)

        for x in members & set(indi):
            rec = indi[x]
            row = {
                "export": rel,
                "geni_id": gid(x),
                "name": rec["name"],
                "sex": rec["sex"],
                "occupation": rec["occu"],
                "n_parent_families": len(rec["famc"]),
                "n_spouse_families": len(rec["fams"]),
            }
            row.update({f"birt_{k}": v for k, v in date_fields(rec["birt"]).items()})
            row.update({f"deat_{k}": v for k, v in date_fields(rec["deat"]).items()})
            prows.append(row)

    fcols = ["export", "family_id", "husband_geni_id", "husband_name",
             "wife_geni_id", "wife_name", "has_wife", "n_children",
             "children_geni_ids", "children_names", "marr_place", "div_raw"] + \
            [f"marr_{k}" for k in DATE_FIELDS]
    pcols = ["export", "geni_id", "name", "sex", "occupation",
             "n_parent_families", "n_spouse_families"] + \
            [f"birt_{k}" for k in DATE_FIELDS] + [f"deat_{k}" for k in DATE_FIELDS]

    for out, cols, rows in ((args.families_out, fcols, frows),
                            (args.people_out, pcols, prows)):
        p = REPO / out
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)
        print(f"wrote {p}  ({len(rows):,} rows)")

    distinct_f = {r["family_id"] for r in frows}
    with_wife = {r["family_id"] for r in frows if r["has_wife"] == "yes"}
    print(f"\n{len(distinct_f):,} distinct families; {len(with_wife):,} record a wife")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
