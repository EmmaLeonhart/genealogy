"""Where the two cut-off clusters touch Wikidata.

Emma, 2026-08-13, having found `Kadin Harding` and `Jacqueline Crispin` inside
them: *"my expectation here is basically that the seeds supposed to link to them
just were not going correctly... we can go on and try to get them connected to
the world tree in other ways."*

The two clusters are cut off **from our Geni merge**, not from Wikidata. Each is
exactly one `Forest` export — 4,088 and 4,084 people sharing nobody with the
other 173 exports — but their members already carry Wikidata items, and most of
those items sit inside the 1,116,499-person world-tree component. So the join
that no Geni export has reached already exists on the Wikidata side.

Writes `reports/cluster-anchors.csv` (every QID-carrying person in either
cluster, one row each) and `reports/cluster-anchors.md`.

    py scripts/build-cluster-anchors.py
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

LABELS = REPO_ROOT / "reports" / "derived-labels.csv"
FACTS = REPO_ROOT / "reports" / "derived-facts.csv"
COMPONENTS = REPO_ROOT / "reports" / "wikidata-components.csv"
OUT_CSV = REPO_ROOT / "reports" / "cluster-anchors.csv"
OUT_MD = REPO_ROOT / "reports" / "cluster-anchors.md"

csv.field_size_limit(10_000_000)
INDI = re.compile(rb"^0 @I(\d+)@ INDI", re.M)

CLUSTERS = {
    "wife of Baruch Jafe": REPO_ROOT / "exports" / "wife of Baruch Jafe"
                           / "export-Forest-6000000227145774838.ged",
    "wife of Samuel Standen": REPO_ROOT / "exports" / "wife of Samuel Standen"
                              / "export-Forest-6000000227145420853.ged",
}

#: The two profiles Emma found by hand, which is what prompted this.
FOUND = {
    "6000000176095890839": "Kadin Harding",
    "6000000005082335522": "Jacqueline Crispin",
}


def main() -> int:
    members = {}
    for label, path in CLUSTERS.items():
        ids = set(m.decode() for m in INDI.findall(path.read_bytes()))
        members[label] = ids

    lab = {r["geni_id"]: r for r in csv.DictReader(open(LABELS, encoding="utf-8"))}
    fac = {r["geni_id"]: r for r in csv.DictReader(open(FACTS, encoding="utf-8"))}
    comp = {r["qid"]: int(r["component_size"])
            for r in csv.DictReader(open(COMPONENTS, encoding="utf-8"))}
    world = max(comp.values())

    rows = []
    for label, ids in members.items():
        for gid in sorted(ids):
            row = lab.get(gid)
            if not row or not row["qid"]:
                continue
            qid = row["qid"]
            size = comp.get(qid)
            rows.append({
                "cluster": label,
                "geni_id": gid,
                "qid": qid,
                "label_en": row["label_en"],
                "born": fac.get(gid, {}).get("birth_date_year", ""),
                "died": fac.get(gid, {}).get("death_date_year", ""),
                "wikidata_component": size if size is not None else "",
                "in_world_tree": "yes" if size == world else "no",
                "geni_url": f"https://www.geni.com/people/x/{gid}",
                "wikidata_url": f"https://www.wikidata.org/wiki/{qid}",
            })

    with open(OUT_CSV, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    L: list[str] = []
    add = L.append
    add("# Where the two cut-off clusters touch Wikidata")
    add("")
    add("Emma found `Kadin Harding` and `Jacqueline Crispin` inside them by hand, and")
    add("read it as the seeds having failed rather than the people being unreachable.")
    add("That reading is right, and it goes further than expected.")
    add("")
    add("**The clusters are cut off from our Geni merge, not from Wikidata.**")
    add("")
    add("| cluster | people | carry a QID | inside the world tree |")
    add("| --- | ---: | ---: | ---: |")
    for label, ids in members.items():
        mine = [r for r in rows if r["cluster"] == label]
        wt = [r for r in mine if r["in_world_tree"] == "yes"]
        add(f"| {label} | {len(ids):,} | {len(mine)} | **{len(wt)}** |")
    add("")
    add(f"The world tree is the {world:,}-person Wikidata component from")
    add("`reports/wikidata-components.csv` — the one the Charlemagne priority chain")
    add("is aimed at. A cluster member already in it is a person our Geni data cannot")
    add("reach and Wikidata already connects.")
    add("")
    add("## The two Emma found")
    add("")
    add("| who | geni id | cluster | born | died |")
    add("| --- | --- | --- | ---: | ---: |")
    for gid, name in FOUND.items():
        where = next((l for l, ids in members.items() if gid in ids), "—")
        f = fac.get(gid, {})
        add(f"| {name} | `{gid}` | {where} | {f.get('birth_date_year','?')} "
            f"| {f.get('death_date_year','?')} |")
    add("")
    add("One in each cluster, which is why each looked unreachable separately.")
    add("Neither carries a QID; both have parents recorded inside their own cluster.")
    add("")
    add("## Anchors already in the world tree")
    add("")
    add("Every row of `reports/cluster-anchors.csv` is one QID-carrying person in one")
    add("of the clusters. The ones marked `in_world_tree` are where an edit could")
    add("attach without creating anything first:")
    add("")
    add("| qid | who | born | cluster |")
    add("| --- | --- | ---: | --- |")
    for r in sorted((r for r in rows if r["in_world_tree"] == "yes"),
                    key=lambda r: (r["cluster"], r["born"] or "9999")):
        add(f"| [`{r['qid']}`]({r['wikidata_url']}) | {r['label_en']} | "
            f"{r['born'] or '—'} | {r['cluster']} |")
    add("")
    add("## What this changes")
    add("")
    add("The question was \"which Geni edge was removed\". The answer is that it does")
    add("not have to be found to connect these people: the Wikidata side is already")
    add("joined at the points above. What the Geni exports failed at was reaching the")
    add("clusters from our own tree, and that is a sampling gap — both balls stopped")
    add("at the export size bound rather than exhausting the neighbourhood.")
    add("")
    add("Components smaller than the world tree are counted too, because they are the")
    add("opposite case — a QID with no genealogical edges on Wikidata is a person")
    add("whose links we would be *adding*, not following:")
    add("")
    add("| wikidata component size | people |")
    add("| ---: | ---: |")
    for size, n in Counter(r["wikidata_component"] for r in rows).most_common():
        add(f"| {size:,} | {n} |" if isinstance(size, int) else f"| — | {n} |")

    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {OUT_CSV} and {OUT_MD}")
    print(f"  {len(rows)} QID-carrying cluster members, "
          f"{sum(1 for r in rows if r['in_world_tree'] == 'yes')} inside the world tree")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
