"""The one-time ring around the FamilySearch-keyed super entry points (queue item, Emma 2026-10-07).

Runs `build-familysearch-day.py` itself, the normal creation path, with two changes made for this run only:
the pause is off, and the 8 super entry points' items are added to the bridge so their relatives link to
them. The output is then cut to the ring: the parents, spouses, children and siblings of a super entry point.

`LHJY-2G1` is Cendfindan mac Maith himself (a second, male FamilySearch record married to the female-marked
`L7J5-NNV`), so it maps to his item and is not created; `L7J5-NNV` is left out of the bridge so his child
links to him as father only.

Writes `reports/super-entry-ring-fs.txt` and `reports/super-entry-ring-fs-carry.tsv`. Sends nothing.

    python scripts/session-2026-10-09/super-entry-ring-fs.py
"""
import csv
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("fsday", ROOT / "scripts" / "build-familysearch-day.py")
fsday = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fsday)

OUT = ROOT / "reports" / "super-entry-ring-fs.txt"
SAME_AS_SUPER = {"LHJY-2G1": "Q141654625"}
LEFT_OUT = {"L7J5-NNV"}


def main():
    rows = list(csv.DictReader(open(ROOT / "reports" / "super-entry-points.tsv", encoding="utf-8"),
                               delimiter="\t"))
    supers = {r["key"][2:6] + "-" + r["key"][6:]: r["qid"] for r in rows if r["key"].startswith("FS")}
    extra = {f: q for f, q in supers.items() if f not in LEFT_OUT} | SAME_AS_SUPER

    people, father, mother, spouses, children = fsday.read_corpus(sorted(fsday.CORPUS.rglob("*.ged")))
    ring = set()
    for k, rec in people.items():
        if rec["fs_id"] not in supers:
            continue
        near = [father.get(k), mother.get(k), *spouses.get(k, ()), *children.get(k, ())]
        near += [s for p in (father.get(k), mother.get(k)) if p for s in children.get(p, ())]
        ring |= {people[o]["fs_id"] for o in near if o and people.get(o, {}).get("fs_id")}
    ring -= set(supers) | set(SAME_AS_SUPER)

    bridge = fsday.read_bridge
    fsday.read_bridge = lambda: bridge() | extra
    fsday.CREATIONS_PAUSED = False
    fsday.OUT = ROOT / "out" / "super-entry-ring-fs-all.txt"
    fsday.CARRY = ROOT / "reports" / "super-entry-ring-fs-carry-all.tsv"
    fsday.build(type("A", (), {"gedcom": [], "limit": 0})())

    blocks, cur = [], []
    for ln in fsday.OUT.read_text(encoding="utf-8").splitlines() + [""]:
        if ln.strip() == "":
            if cur:
                blocks.append(cur)
            cur = []
        else:
            cur.append(ln)
    kept, made = [], set()
    for b in blocks:
        ids = [m.group(1) for ln in b for m in [re.match(r'^LAST\tP2889\t"([^"]+)"', ln)] if m]
        if "CREATE" in b and ids and ids[0] in ring:
            kept.append(b)
            made.add(ids[0])
    head = ["# The one-time ring around the FamilySearch-keyed super entry points (queue item, Emma 2026-10-07).",
            f"# {len(made)} of {len(ring)} ring people; the rest are in super-entry-ring-fs-carry.tsv. Run with Run."]
    OUT.write_text("\n".join(head + [""] + ["\n".join(b) + "\n" for b in kept]), encoding="utf-8", newline="\n")
    with open(fsday.CARRY, encoding="utf-8") as f, \
            open(ROOT / "reports" / "super-entry-ring-fs-carry.tsv", "w", encoding="utf-8", newline="") as g:
        r = csv.reader(f, delimiter="\t")
        w = csv.writer(g, delimiter="\t")
        w.writerow(next(r))
        w.writerows(row for row in r if row[0] in ring)
    fsday.CARRY.unlink()
    fsday.OUT.unlink()
    print(f"ring {len(ring)}, created {len(made)}: {sorted(made)}")
    print("not created:", sorted(ring - made))


if __name__ == "__main__":
    main()
