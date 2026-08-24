"""Where our Geni tree and the Izumo chart disagree about a parent.

    python scripts/izumo-tree-vs-chart.py

**Emma, 2026-08-24**, asked which source the relationship links should come from and
chose: *show me the disagreements first*. So this asserts nothing and emits no batch. It
lines the two sources up on the roster and prints the rows where they differ.

Three sources meet here and each is joined by an identifier, never by a name:

* `reports/izumo-chart-edges.tsv` — the chart's own parent/child edges, keyed on
  `<name>#<regnal>` because that is how the page identifies a seat-holder.
* `reports/izumo-p2600-pairs.tsv` — the 111 QID↔Geni joins, built from the Wikidata link
  Emma wrote into each Geni About Me. This is the join the whole programme rests on.
* `reports/derived-family.csv` — our merged tree's father and mother per Geni profile.

**A disagreement is not automatically the chart being right.** Geni carries people the
chart does not, and the chart records a *succession*, which is not always a descent —
`CLAUDE.md` records the refutation: Takanori 81 and Takatomi 80 held the seat in
sequence and were **brothers**, so a father→son reading of the chart was wrong. That is
exactly why this prints records rather than picking.

Writes `reports/izumo-tree-vs-chart.tsv`.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

ROOT = Path(__file__).resolve().parent.parent


def read(path, **kw):
    with open(ROOT / path, encoding="utf-8") as f:
        return list(csv.DictReader(f, **kw))


def main():
    roster = read("reports/izumo-roster.tsv", delimiter="\t")
    edges = read("reports/izumo-chart-edges.tsv", delimiter="\t")
    pairs = read("reports/izumo-p2600-pairs.tsv", delimiter="\t")

    # regnal number -> the roster row. The chart labels a node `<name>#<regnal>`, and
    # the regnal number is the only stable key: `CLAUDE.md` records that the numbers
    # are regnal ordinals ordering the office-holders, not part of the name.
    by_regnal = {r["regnal"].strip(): r for r in roster if r.get("regnal", "").strip()}

    def regnal_of(node):
        m = re.search(r"#(\d+)$", node or "")
        return m.group(1) if m else None

    # The chart's father, by regnal number.
    chart_father = {}
    for e in edges:
        if e.get("kind") != "child":
            continue
        parent, child = regnal_of(e["parent"]), regnal_of(e["child"])
        if parent and child:
            chart_father.setdefault(child, set()).add(parent)

    # Our side: the Geni profile for each roster person, then its father.
    geni_of = {}
    for p in pairs:
        if p.get("regnal", "").strip():
            # **`geni_ids` is SEMICOLON-delimited.** A bare `.split()` turned a
            # multi-id cell into one bogus id matching nobody, which is why roster #63
            # read "tree has no father" when the tree records Naokiyo Hiraoka as his
            # father. Exactly one row carried two ids when this was found.
            for gid in re.split(r"[;\s]+", (p.get("geni_ids") or "").strip()):
                if gid:
                    geni_of.setdefault(p["regnal"].strip(), set()).add(gid)

    wanted = {g for ids in geni_of.values() for g in ids}
    father_of, name_of = {}, {}
    for row in read("reports/derived-family.csv"):
        if row["geni_id"] in wanted:
            father_of[row["geni_id"]] = (row.get("father") or "").strip()
    for row in read("reports/derived-labels.csv"):
        gid = row["geni_id"]
        if gid in wanted or gid in set(father_of.values()):
            name_of[gid] = row.get("label_en") or row.get("label_mul") or ""

    out = []
    for regnal, row in sorted(by_regnal.items(), key=lambda kv: int(kv[0])):
        chart = chart_father.get(regnal, set())
        gids = geni_of.get(regnal, set())
        if not chart or not gids:
            continue
        chart_names = " | ".join(
            f"{by_regnal.get(c, {}).get('name', '?')}#{c}" for c in sorted(chart))
        for gid in sorted(gids):
            dad = father_of.get(gid, "")
            # Which regnal number, if any, is our father?
            dad_regnal = next((r for r, ids in geni_of.items() if dad in ids), None)
            agrees = dad_regnal in chart if dad_regnal else False
            if agrees:
                continue
            out.append({
                "regnal": regnal,
                "person": row.get("name", ""),
                "qid": row.get("qid", ""),
                "geni_id": gid,
                "chart_father": chart_names,
                "tree_father": name_of.get(dad, "") if dad else "(none recorded)",
                "tree_father_geni_id": dad,
                "tree_father_regnal": dad_regnal or "",
                "kind": ("tree has no father" if not dad
                         else "tree father is off the roster" if not dad_regnal
                         else "different seat"),
            })

    dest = ROOT / "reports" / "izumo-tree-vs-chart.tsv"
    with open(dest, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]) if out else ["regnal"],
                           delimiter="\t")
        w.writeheader()
        w.writerows(out)

    checked = sum(1 for r, _ in by_regnal.items()
                  if chart_father.get(r) and geni_of.get(r))
    print(f"{checked} roster people have BOTH a chart father and a Geni profile")
    print(f"{len(out)} of them disagree\n")
    for row in out:
        print(f"  #{row['regnal']:<4} {row['person'][:28]:<28} {row['kind']}")
        print(f"        chart: {row['chart_father']}")
        print(f"        tree:  {row['tree_father']}")
    print(f"\nwrote {dest.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
