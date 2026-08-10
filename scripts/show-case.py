"""Show one person, both sides, in full — for case-by-case review with Emma.

`python scripts/show-case.py <geni_id>`

**This exists because the reports were the wrong shape.** Emma, 2026-08-10:
*"You give me the information, and I'll look over it and confirm... you're just
aggressively jumping into the database modelling and skipping the
interpretation."* So this prints records, not statistics. It decides nothing,
scores nothing, and proposes no rule. One person, what Geni says, what Wikidata
says, and where they differ — enough to make a judgement from.

Rules are meant to come *out* of a run of these, not be applied to them.

Walking order for ancestors is ahnentafel: father, mother, then father's father,
father's mother, mother's father, mother's mother, and so on — `--up N` prints
the first N positions.
"""

from __future__ import annotations

import io
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

# Names in this corpus are Japanese, Chinese, Arabic and accented Latin. The
# Windows console is cp1252 and raises on all of it, so stdout is forced to
# UTF-8 rather than the script dying halfway through a record.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from genimerge import wikistore  # noqa: E402
from genimerge.dates import parse_date  # noqa: E402
from genimerge.doubles import load_pairs  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / "wikidata" / "items"
INDEX = ROOT / "out" / "wikidata" / "store-index.sqlite3"
MERGED = ROOT / "out" / "merged.ged"
PAIRS = ROOT / "out" / "wikidata" / "p2600-all.tsv"

RELATIONS = {"P22": "father", "P25": "mother", "P26": "spouse", "P40": "child", "P3373": "sibling"}


def read_gedcom(path: Path):
    """Everything this script needs, in one pass. Records, not aggregates."""
    people: dict[str, dict] = defaultdict(lambda: {"names": [], "events": {}, "fams": [], "famc": [], "raw": []})
    fams: dict[str, dict] = defaultdict(lambda: {"husb": [], "wife": [], "chil": []})
    who = kind = tag = None
    for line in io.open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("0 "):
            parts = line.split(" ")
            ref = parts[1] if len(parts) > 2 else ""
            who, kind = (ref, "I") if ref.startswith("@I") else (ref, "F") if ref.startswith("@F") else (None, None)
            tag = None
        elif kind == "I" and who:
            people[who]["raw"].append(line)
            if line.startswith("1 NAME"):
                people[who]["names"].append(line[7:])
                tag = None
            elif line.startswith(("1 BIRT", "1 DEAT", "1 BURI")):
                tag = line[2:6]
            elif line.startswith("1 FAMS"):
                people[who]["fams"].append(line.split(" ")[2])
                tag = None
            elif line.startswith("1 FAMC"):
                people[who]["famc"].append(line.split(" ")[2])
                tag = None
            elif line.startswith("1 OCCU") and len(line) > 7:
                people[who]["events"]["occupation"] = line[7:]
                tag = None
            elif line.startswith("1 "):
                tag = None
            elif line.startswith("2 DATE") and tag:
                people[who]["events"].setdefault(tag, line[7:])
            elif line.startswith("2 PLAC") and tag:
                people[who]["events"].setdefault(tag + "_place", line[7:])
        elif kind == "F" and who:
            for prefix, key in (("1 HUSB", "husb"), ("1 WIFE", "wife"), ("1 CHIL", "chil")):
                if line.startswith(prefix):
                    fams[who][key].append(line.split(" ")[2])
    return people, fams


def geni_id(xref: str) -> str:
    return xref.strip("@").lstrip("I")


def parents_of(person: str, people, fams) -> tuple[str | None, str | None]:
    for family in people[person]["famc"]:
        f = fams.get(family)
        if f:
            return (f["husb"][0] if f["husb"] else None, f["wife"][0] if f["wife"] else None)
    return (None, None)


def _label(entity: dict) -> str:
    labels = entity.get("labels") or {}
    for lang in ("en", "mul", "ja", "de", "fr"):
        v = (labels.get(lang) or {}).get("value")
        if v:
            return v
    for v in labels.values():
        if v:
            return v.get("value", "")
    return ""


def _truthy(entity: dict, prop: str) -> list:
    st = (entity.get("claims") or {}).get(prop) or []
    live = [s for s in st if s.get("rank") != "deprecated"]
    for s in [x for x in live if x.get("rank") == "preferred"] or live:
        snak = s.get("mainsnak") or {}
        if snak.get("snaktype") == "value":
            yield (snak.get("datavalue") or {}).get("value")


def wd_year(entity: dict, prop: str) -> str:
    for v in _truthy(entity, prop):
        if isinstance(v, dict) and v.get("time"):
            t = v["time"]
            return f"{'-' if t[0] == '-' else ''}{int(t[1:5])}"
    return ""


def show(person: str, people, fams, reader, qid_by_geni, position: str) -> None:
    rec = people[person]
    gid = geni_id(person)
    qid = qid_by_geni.get(gid)
    entity = reader.entities([qid]).get(qid, {}) if qid else {}

    print("=" * 78)
    print(f"{position}   geni {gid}" + (f"   wikidata {qid}" if qid else "   wikidata: NOT LINKED"))
    print("=" * 78)

    print("\n  GENI")
    for n in rec["names"]:
        print(f"    name       {n}")
    for key, label in (("BIRT", "born"), ("DEAT", "died"), ("BURI", "buried")):
        if key in rec["events"]:
            d = parse_date(rec["events"][key])
            print(f"    {label:<10} {rec['events'][key]}" + (f"   (year {d.year})" if d.year is not None else "   (unparsed)"))
        if key + "_place" in rec["events"]:
            print(f"    {'':<10} at {rec['events'][key + '_place']}")
    if "occupation" in rec["events"]:
        print(f"    occupation {rec['events']['occupation']}")
    father, mother = parents_of(person, people, fams)
    for role, ref in (("father", father), ("mother", mother)):
        if ref:
            nm = people[ref]["names"][0] if people[ref]["names"] else "?"
            print(f"    {role:<10} {nm}   [{geni_id(ref)}]")
    spouses = [s for f in rec["fams"] for s in (fams[f]["husb"] + fams[f]["wife"]) if s != person]
    kids = [c for f in rec["fams"] for c in fams[f]["chil"]]
    print(f"    spouses    {len(spouses)}   children {len(kids)}")

    print("\n  WIKIDATA")
    if not qid:
        print("    no P2600 link to this profile")
    elif not entity:
        print(f"    {qid} is not in the downloaded store")
    else:
        print(f"    label      {_label(entity)}")
        descs = entity.get("descriptions") or {}
        if (descs.get("en") or {}).get("value"):
            print(f"    described  {descs['en']['value']}")
        b, d = wd_year(entity, "P569"), wd_year(entity, "P570")
        print(f"    born       {b or '-'}        died {d or '-'}")
        print(f"    sitelinks  {len(entity.get('sitelinks') or {})}")
        for prop, name in RELATIONS.items():
            targets = [v.get("id") for v in _truthy(entity, prop) if isinstance(v, dict) and v.get("id")]
            if targets:
                print(f"    {name:<10} {', '.join(targets)}")
    print()


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    seed = sys.argv[1].strip()
    up = int(sys.argv[sys.argv.index("--up") + 1]) if "--up" in sys.argv else 1

    people, fams = read_gedcom(MERGED)
    xref = f"@I{seed}@"
    if xref not in people:
        print(f"{seed} is not in the merged tree", file=sys.stderr)
        return 1

    qid_by_geni: dict[str, str] = {}
    counts: dict[str, set] = defaultdict(set)
    for qid, gid in load_pairs(PAIRS):
        counts[gid].add(qid)
    qid_by_geni = {g: next(iter(q)) for g, q in counts.items() if len(q) == 1}

    # Ahnentafel: 1 self, 2 father, 3 mother, 4 father's father, ...
    order: list[tuple[int, str]] = [(1, xref)]
    labels = {1: "SELF"}
    i = 0
    while i < len(order) and len(order) < up:
        n, ref = order[i]
        i += 1
        father, mother = parents_of(ref, people, fams)
        for slot, parent, word in ((2 * n, father, "father"), (2 * n + 1, mother, "mother")):
            if parent:
                order.append((slot, parent))
                labels[slot] = f"{labels[n]} -> {word}" if n > 1 else word.upper()

    with wikistore.StoreReader(STORE, INDEX) as reader:
        for n, ref in order[:up]:
            show(ref, people, fams, reader, qid_by_geni, f"[{n}] {labels.get(n, '')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
