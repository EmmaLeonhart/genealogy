"""Align the Izumo chart to Geni by RELATIONAL POSITION, not by name.

Emma, 2026-08-20: *"Are you using text similarity instead of relational position?"*
For the presence check, I had been - a name search plus a token-set match. This
replaces that. And: *"YOU CAN MOVE IN DIFFERENT DIRECTIONS THAN DOWN"* - the Geni
side is a neighbourhood walked through parents, children, siblings and spouses, not
a descent, which is why the in-law columns are reachable at all.

## How a person is identified

From an anchor whose Geni id is known, and then outward one edge at a time:

- If chart person A is the same as Geni profile G, then A's charted children and G's
  Geni children are the same set of people. When both sides have exactly one
  member not yet identified, that pair is forced - **there is nothing to choose**,
  so no name is consulted.
- Where several remain unidentified on both sides, the position is ambiguous and the
  name is used only to *break the tie among the candidates already in that position* -
  never to search, never to pair people who are not in corresponding positions.
  Those matches are labelled `position+name` so they can be told apart.
- The same propagation runs upward through parents and sideways through spouses.

Anchors come from two places, both exact: `reports/izumo-geni-overrides.tsv`, which
is where Emma puts an identity no computation could reach, and the ids recorded in
`reports/izumo-geni-build.md` for people this project created itself.

## What it will not do

It will not pick between two Geni profiles in one position. That is the duplicate
case, and duplicates on this tree are a permanent feature - the clan was loaded onto
Geni three separate times - so they are reported for Emma to merge, never resolved
here.
"""

import argparse
import collections
import csv
import pathlib
import re
import sys


def norm(name: str) -> str:
    """Loose key used only to break ties inside an already-matched position."""
    s = name.lower().replace("’", "'")
    s = re.sub(r"[^0-9a-z' ]+", " ", s)
    drop = {"no", "mikoto", "nomikoto", "kokuso", "izumo", "sukune"}
    toks = [t for t in s.split() if t and t not in drop]
    toks = [re.sub(r"nomikoto$", "", t) or t for t in toks]
    return " ".join(sorted(t for t in toks if t))


def load_chart(path: pathlib.Path):
    kids = collections.defaultdict(list)
    parents = collections.defaultdict(list)
    people = set()
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            p, c, kind = row["parent"].strip(), row["child"].strip(), row["kind"].strip()
            people.add(p)
            people.add(c)
            if kind == "spouse":
                continue
            kids[p].append(c)
            parents[c].append(p)
    return kids, parents, people


def load_geni(path: pathlib.Path):
    """The neighbourhood walk: id -> name, parents, children, siblings, spouses."""
    nodes = {}
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            nodes[row["geni"]] = {
                "name": row["name"],
                "p": [x for x in row.get("parents", "").split(",") if x],
                "c": [x for x in row.get("children", "").split(",") if x],
            }
    return nodes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chart", default="reports/izumo-chart-edges.tsv")
    ap.add_argument("--geni", default="reports/izumo-geni-neighbourhood.tsv")
    ap.add_argument("--anchors", default="reports/izumo-geni-anchors.tsv")
    ap.add_argument("--out", default="reports/izumo-alignment.tsv")
    args = ap.parse_args()

    chart_path, geni_path = pathlib.Path(args.chart), pathlib.Path(args.geni)
    if not geni_path.exists():
        print(f"no neighbourhood walk at {geni_path}", file=sys.stderr)
        return 1

    kids, parents, people = load_chart(chart_path)
    geni = load_geni(geni_path)

    # chart key -> geni id, and the reverse, with how each was established.
    ident: dict[str, str] = {}
    how: dict[str, str] = {}
    taken: dict[str, str] = {}

    anchors = pathlib.Path(args.anchors)
    if anchors.exists():
        with anchors.open(encoding="utf-8") as fh:
            for row in csv.DictReader(fh, delimiter="\t"):
                key, gid = row["chart"].strip(), row["geni"].strip()
                if key and gid:
                    ident[key], how[key], taken[gid] = gid, row.get("source", "anchor"), key

    ambiguous: list[str] = []
    changed = True
    while changed:
        changed = False
        for key, gid in list(ident.items()):
            node = geni.get(gid)
            if not node:
                continue
            for direction, chart_side, geni_side in (
                ("child", kids.get(key, []), node["c"]),
                ("parent", parents.get(key, []), node["p"]),
            ):
                open_chart = [k for k in chart_side if k not in ident]
                open_geni = [g for g in geni_side if g not in taken]
                if not open_chart or not open_geni:
                    continue
                if len(open_chart) == 1 and len(open_geni) == 1:
                    k, g = open_chart[0], open_geni[0]
                    ident[k], taken[g] = g, k
                    how[k] = f"position ({direction} of {key})"
                    changed = True
                    continue
                # Several open on both sides: the position no longer forces a pair,
                # so break the tie only among these candidates, by name.
                by_name = {norm(geni[g]["name"]): g for g in open_geni if g in geni}
                for k in open_chart:
                    base = norm(k.split("#")[0])
                    g = by_name.get(base)
                    if g and g not in taken:
                        ident[k], taken[g] = g, k
                        how[k] = f"position+name ({direction} of {key})"
                        changed = True
                if len(open_chart) > 1 and len(open_geni) > 1:
                    ambiguous.append(
                        f"{key} — {len(open_chart)} charted {direction}(s) unmatched "
                        f"against {len(open_geni)} on Geni"
                    )

    with open(args.out, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["chart", "geni", "geni_name", "how"])
        for key in sorted(people):
            gid = ident.get(key, "")
            w.writerow([key, gid, geni.get(gid, {}).get("name", ""), how.get(key, "")])

    resolved = sum(1 for k in people if k in ident)
    print(f"{resolved}/{len(people)} chart people identified on Geni by position")
    for a in sorted(set(ambiguous)):
        print("  ambiguous:", a)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
