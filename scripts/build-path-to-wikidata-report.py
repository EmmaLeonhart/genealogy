"""How a person connects to Wikidata's family graph, and by what route.

Emma asked for this by name, 2026-08-12: *"find the earliest one of my ancestors
that has a Wikidata item … It would just be the least amount of hops in the
family tree to somebody with a Wikidata item."* Then, after the first answer
turned out to be an isolate: *"we will do a similar thing with other ancestors of
mine instead."*

Four measures, because the first three each looked like the answer and were not:

1. **Fewest hops to any Wikidata item**, ancestors only.
2. **Fewest hops by any relation** — sideways is allowed and is never longer.
3. **Whether that item is attached to anything on Wikidata.** Most are not. An
   item with no `P22`/`P25`/`P26`/`P40`/`P3373` is an island, and linking to it
   joins nothing.
4. **Every ancestor carrying an item**, and how many of *their* descendants
   carry one — which is what actually identifies a hub.

QIDs come from the P2600 map **and** from `entity_resolution.md`, because an item
without `P2600` is invisible to the map and still a Wikidata item.

    py scripts/build-path-to-wikidata-report.py [geni_id]
"""

from __future__ import annotations

import csv
import sys
from collections import deque
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from genimerge import entities, wikistore  # noqa: E402

FAMILY = REPO_ROOT / "reports" / "derived-family.csv"
LABELS = REPO_ROOT / "reports" / "derived-labels.csv"
FACTS = REPO_ROOT / "reports" / "derived-facts.csv"
STORE = REPO_ROOT / "wikidata" / "items"
INDEX = REPO_ROOT / "out" / "wikidata" / "store-index.sqlite3"
OUT_MD = REPO_ROOT / "reports" / "path-to-wikidata.md"

csv.field_size_limit(10_000_000)
EMMA = "6000000001846508982"
RELATION_PROPS = ("P22", "P25", "P26", "P40", "P3373")


def main() -> int:
    start = sys.argv[1] if len(sys.argv) > 1 else EMMA
    fam = {r["geni_id"]: r for r in csv.DictReader(open(FAMILY, encoding="utf-8"))}
    lab = {r["geni_id"]: r for r in csv.DictReader(open(LABELS, encoding="utf-8"))}
    fac = {r["geni_id"]: r for r in csv.DictReader(open(FACTS, encoding="utf-8"))}

    qid = {g: r["qid"] for g, r in lab.items() if r["qid"]}
    # **`entity_resolution.md` is gone and nothing may read it.** Emma, 2026-08-31: *"no
    # files should read it lol."* Deleted in `12f3134a`; the readers were not, and each
    # either crashed or degraded silently.

    kids: dict[str, list[str]] = {}
    for geni_id, row in fam.items():
        for parent in (row.get("father"), row.get("mother")):
            if parent:
                kids.setdefault(parent, []).append(geni_id)

    def name(g: str) -> str:
        return lab.get(g, {}).get("label_en") or \
            (lab.get(g, {}).get("cjk_names") or "").split(" | ")[0] or "(no name)"

    def born(g: str) -> str:
        return fac.get(g, {}).get("birth_date_year", "") or "?"

    # ancestors, with generation distance
    ancestors: dict[str, int] = {}
    seen = {start}
    queue = deque([(start, 0)])
    while queue:
        g, d = queue.popleft()
        if g != start:
            ancestors[g] = d
        row = fam.get(g)
        if not row:
            continue
        for parent in (row.get("father"), row.get("mother")):
            if parent and parent not in seen:
                seen.add(parent)
                queue.append((parent, d + 1))

    carrying = sorted((d, g) for g, d in ancestors.items() if g in qid)

    # how connected is each of those items on Wikidata?
    with wikistore.StoreReader(STORE, INDEX) as reader:
        items = reader.entities(sorted({qid[g] for _, g in carrying}))

    def links(g: str) -> list[str]:
        entity = items.get(qid[g])
        if entity is None:
            return []
        claims = entity.get("claims") or {}
        out = []
        for prop in RELATION_PROPS:
            for statement in claims.get(prop, []):
                value = ((statement.get("mainsnak") or {}).get("datavalue") or {}).get("value") or {}
                if value.get("id"):
                    out.append(f"{prop}:{value['id']}")
        return out

    def descendants_with_items(root: str) -> tuple[int, int]:
        """Descendants, and how many carry an item — **excluding the subject**.

        Counting the subject makes every one of their ancestors look connected,
        because they are all ancestors of somebody with an item by definition.
        The first version of this did exactly that and reported "0 of 572 have no
        Wikidata descendants", which is a tautology rather than a finding.
        """
        s = {root}
        q = deque([root])
        found = 0
        while q:
            g = q.popleft()
            for c in kids.get(g, []):
                if c in s:
                    continue
                s.add(c)
                q.append(c)
                if c in qid and c != start:
                    found += 1
        return len(s) - 1, found

    L: list[str] = []
    add = L.append
    add(f"# Connecting `{start}` to Wikidata's family graph")
    add("")
    add(f"**{name(start)} {born(start)}** — "
        f"{'carries ' + qid[start] if start in qid else 'no Wikidata item'}.")
    add("")
    add(f"{len(ancestors):,} ancestors in the tree; **{len(carrying)} of them carry a")
    add("Wikidata item**.")
    add("")
    add("## The nearest ones, and whether they are attached to anything")
    add("")
    add("An item with no `P22`/`P25`/`P26`/`P40`/`P3373` is an island on Wikidata.")
    add("Linking to it joins nothing, which is why the nearest is not automatically the")
    add("best target.")
    add("")
    add("| gens up | born | qid | name | links on Wikidata |")
    add("| ---: | ---: | --- | --- | --- |")
    for d, g in carrying[:25]:
        edges = links(g)
        state = ", ".join(edges[:3]) if edges else "**isolate**"
        add(f"| {d} | {born(g)} | {qid[g]} | {name(g)} | {state} |")
    add("")
    add("## Which ancestors are hubs")
    add("")
    add("Counting, for each ancestor carrying an item, how many of **their** descendants")
    add("also carry one. A hub is what connects to the world tree; an isolate with no")
    add("Wikidata descendants is a dead end however close it is.")
    add("")
    add("| descendants with items | descendants | gens up | born | ancestor |")
    add("| ---: | ---: | ---: | ---: | --- |")
    ranked = []
    for d, g in carrying:
        total, found = descendants_with_items(g)
        ranked.append((found, total, d, g))
    ranked.sort(reverse=True)
    for found, total, d, g in ranked[:20]:
        add(f"| {found:,} | {total:,} | {d} | {born(g)} | {name(g)} [{qid[g]}] |")
    add("")
    dead = [r for r in ranked if r[0] == 0]
    add(f"**{len(dead)} of the {len(ranked)} carry no Wikidata descendants at all.**")
    add("")
    add("## What this changes")
    add("")
    add("The nearest ancestor with an item is not necessarily the way in. The route that")
    add("joins the world tree is the one through a hub — and the hubs here are far older")
    add("and far better connected than the nearest.")

    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {OUT_MD}")
    print(f"  {len(ancestors):,} ancestors, {len(carrying)} carrying an item")
    print(f"  nearest: {carrying[0][0]} generations — {name(carrying[0][1])} "
          f"[{qid[carrying[0][1]]}]")
    top = ranked[0]
    print(f"  biggest hub: {name(top[3])} [{qid[top[3]]}] — {top[0]:,} descendants with items")
    print(f"  {len(dead)} of {len(ranked)} have no Wikidata descendants")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
