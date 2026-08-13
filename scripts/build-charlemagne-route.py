"""The cheapest route from a person into the Wikidata world tree.

Emma defined the target, 2026-08-13: *"The large contiguous tree of many
interconnected individuals. We can colloquially define it based on link to
charlemagne. Let's just do link to charlemagne. I have multiple links so the one
with the least required new individuals to create."*

So the cost being minimised is **people we would have to create**, not hops.
Stepping onto someone who already has a Wikidata item is free; stepping onto
someone who does not costs one `create_individual`. That is a 0-1 shortest path,
and it gives a very different answer from fewest-hops: the cheapest route runs
398 steps and needs 16 creations, because after the first fifteen it rides the
existing Wikidata network the whole way.

**Why "world tree" needed defining.** Earlier passes reported "nearest ancestor
with a Wikidata item" and got Jørgen Erikssøn at 14 generations — whose component
is one person. Trond Benkestok at 15, component three. Those are hamlets. The
component containing Charlemagne holds **1,116,499** people, and that difference
is the whole point.

Reads `reports/wikidata-components.csv` for component sizes.

    py scripts/build-charlemagne-route.py [geni_id]
"""

from __future__ import annotations

import csv
import sys
from collections import deque
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from genimerge import entities  # noqa: E402

FAMILY = REPO_ROOT / "reports" / "derived-family.csv"
LABELS = REPO_ROOT / "reports" / "derived-labels.csv"
FACTS = REPO_ROOT / "reports" / "derived-facts.csv"
COMPONENTS = REPO_ROOT / "reports" / "wikidata-components.csv"
OUT_MD = REPO_ROOT / "reports" / "charlemagne-route.md"
OUT_CSV = REPO_ROOT / "reports" / "charlemagne-route.csv"

csv.field_size_limit(10_000_000)
EMMA = "6000000087535357291"
CHARLEMAGNE_QID = "Q3044"


def main() -> int:
    start = sys.argv[1] if len(sys.argv) > 1 else EMMA
    fam = {r["geni_id"]: r for r in csv.DictReader(open(FAMILY, encoding="utf-8"))}
    lab = {r["geni_id"]: r for r in csv.DictReader(open(LABELS, encoding="utf-8"))}
    fac = {r["geni_id"]: r for r in csv.DictReader(open(FACTS, encoding="utf-8"))}

    qid = {g: r["qid"] for g, r in lab.items() if r["qid"]}
    parsed = entities.parse((REPO_ROOT / "entity_resolution.md").read_text(encoding="utf-8"))
    qid.update({r.geni_id: r.qid for r in parsed.resolutions if r.geni_id not in qid})

    sizes: dict[str, int] = {}
    if COMPONENTS.exists():
        for row in csv.DictReader(open(COMPONENTS, encoding="utf-8")):
            sizes[row["qid"]] = int(row["component_size"])

    target = next((g for g, q in qid.items() if q == CHARLEMAGNE_QID), None)
    if target is None:
        print(f"{CHARLEMAGNE_QID} is not linked to anyone in the tree")
        return 1

    kids: dict[str, list[str]] = {}
    for geni_id, row in fam.items():
        for parent in (row.get("father"), row.get("mother")):
            if parent:
                kids.setdefault(parent, []).append(geni_id)

    def neighbours(g: str):
        row = fam.get(g)
        if row:
            for parent, role in ((row.get("father"), "father"), (row.get("mother"), "mother")):
                if parent:
                    yield parent, role
            for other in (row.get("spouses") or "").split(" | "):
                if other:
                    yield other, "spouse"
        for child in kids.get(g, []):
            yield child, "child"

    # 0-1 BFS. Weight is "does this person need creating", so the distance to the
    # target is exactly the number of create_individual objects required.
    dist = {start: 0}
    prev: dict[str, tuple[str, str]] = {}
    queue = deque([start])
    while queue:
        g = queue.popleft()
        for other, role in neighbours(g):
            weight = 0 if other in qid else 1
            nd = dist[g] + weight
            if nd < dist.get(other, 1 << 30):
                dist[other] = nd
                prev[other] = (g, role)
                (queue.appendleft if weight == 0 else queue.append)(other)

    if target not in dist:
        print("no route found")
        return 1

    path = []
    cur = target
    while cur != start:
        parent, role = prev[cur]
        path.append((cur, role))
        cur = parent
    path.append((start, ""))
    path.reverse()
    to_create = [g for g, _ in path if g not in qid]

    def name(g):
        return lab.get(g, {}).get("label_en") or "(no name)"

    def born(g):
        return fac.get(g, {}).get("birth_date_year", "") or "?"

    with open(OUT_CSV, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["step", "geni_id", "name", "born", "qid", "action", "component"])
        for i, (g, role) in enumerate(path):
            writer.writerow([i, g, name(g), born(g), qid.get(g, ""),
                             "create" if g not in qid else "already on Wikidata",
                             sizes.get(qid.get(g, ""), "")])

    L: list[str] = []
    add = L.append
    add(f"# Cheapest route from `{start}` into the Wikidata world tree")
    add("")
    add("Emma, 2026-08-13: *\"We can colloquially define it based on link to charlemagne …")
    add("the one with the least required new individuals to create.\"*")
    add("")
    add("The cost minimised is **people to create**, not hops. Stepping onto someone who")
    add("already has an item is free; stepping onto someone who does not costs one")
    add("`create_individual`.")
    add("")
    add(f"**{len(path)-1} steps, {len(to_create)} people to create.**")
    add("")
    add("## The people who would have to be created")
    add("")
    add("| step | born | name |")
    add("| ---: | ---: | --- |")
    for i, (g, _) in enumerate(path):
        if g not in qid:
            add(f"| {i} | {born(g)} | {name(g)} |")
    add("")
    add("## Where it joins the existing network")
    add("")
    first_linked = next((i for i, (g, _) in enumerate(path) if i and g in qid), None)
    if first_linked is not None:
        g = path[first_linked][0]
        add(f"Step {first_linked}: **{name(g)}** {born(g)} — `{qid[g]}`, in a component of")
        add(f"**{sizes.get(qid[g], '?'):,}** people. Everything from here to Charlemagne is")
        add("already on Wikidata.")
    add("")
    add("## Why not the nearer ancestors")
    add("")
    add("| ancestor | gens up | component |")
    add("| --- | ---: | ---: |")
    add("| Jørgen Erikssøn 1535 `Q11979685` | 14 | 1 |")
    add("| Trond Benkestok 1495 `Q7845461` | 15 | 3 |")
    add("| Aadne Garborg 1851 `Q467497` | 9 by any relation | 3 |")
    add("| Racin Kolnes 1898 `Q30019076` | 9 by any relation | 2 |")
    add("")
    add("Those are islands. Linking to them joins one, three or two people. The route")
    add("above joins 1,116,499.")
    add("")
    add("Full step-by-step in `reports/charlemagne-route.csv`.")

    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {OUT_MD} and {OUT_CSV}")
    print(f"  {len(path)-1} steps, {len(to_create)} to create")
    for g in to_create:
        print(f"    {born(g):>6}  {name(g)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
