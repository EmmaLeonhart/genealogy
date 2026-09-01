"""Who is the fewest hops from Emma to a person who could hold a Wikidata item.

Emma, 2026-08-18: *"I didn't ask you to give me the closest linked person. I asked you to
give me the closest person… I only want sideways counts. The main thing is that just a
sibling is considered two hops, not one hop."*

**So: hops are edges in the parent/child graph, and nothing else.** A sibling is two — up
to the shared parent and back down. A first cousin is four. An uncle is three. This is the
plain graph distance, not a kinship degree, and `build-path-to-wikidata-report.py` does not
answer it: that one walks **ancestors only** and reports 14 generations, which is the wrong
question for finding a living relative.

WHY IT IS THE WRONG QUESTION. The point, in her words, is that *"I can make an individual
who is considered notable by publication… if they are close enough to me, that's great."*
The item does not have to exist yet. So the search is not for the nearest existing QID —
it is for the nearest **person**, with the QID noted where there is one, because a
publishing second cousin at six hops beats an ancestor at fourteen.

Spouse edges are deliberately excluded. Marriage is a real relationship and not a hop
between blood relatives, and counting it would make an in-law's cousin look closer than a
sibling. `spouses` is still read so the report can say who is reachable only by marriage.

    py scripts/build-nearest-wikidata.py [geni_id] [--max-hops N]

Offline: `reports/derived-family.csv`, `reports/derived-labels.csv`,
`reports/derived-facts.csv`. Nothing is fetched.
"""

from __future__ import annotations

import csv
import sys
from collections import defaultdict, deque
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FAMILY = REPO / "reports" / "derived-family.csv"
LABELS = REPO / "reports" / "derived-labels.csv"
FACTS = REPO / "reports" / "derived-facts.csv"
OUT = REPO / "reports" / "nearest-wikidata.md"

csv.field_size_limit(10_000_000)
EMMA = "6000000001846508982"


def _ids(field: str | None) -> list[str]:
    """Geni ids out of a `` | ``-separated column.

    **This is the bug that made the first run useless.** The column is pipe-separated
    with spaces around the pipes, and splitting on whitespace turned every ``|`` into a
    person. Every record with more than one child then linked to that one fake node, so
    it reached degree **119,472** and the graph collapsed through it: 1 person at zero
    hops, 2 at one, 6 at two, and 119,472 at three.

    A separator is not a person, and the shape of the failure said so plainly -- a family
    graph does not multiply by twenty thousand in one step. Ids are all digits, so
    anything else is dropped rather than trusted.
    """
    out = []
    for tok in (field or "").replace("|", " ").split():
        tok = tok.strip()
        if tok.isdigit():
            out.append(tok)
    return out


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    start = args[0] if args else EMMA
    max_hops = 12
    if "--max-hops" in sys.argv:
        max_hops = int(sys.argv[sys.argv.index("--max-hops") + 1])

    # --- the parent/child graph, undirected -------------------------------
    adj: dict[str, set[str]] = defaultdict(set)
    qid: dict[str, str] = {}
    spouse: dict[str, set[str]] = defaultdict(set)
    with open(FAMILY, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            me = r["geni_id"]
            if r.get("qid"):
                qid[me] = r["qid"]
            for parent in (r.get("father"), r.get("mother")):
                if parent:
                    adj[me].add(parent)
                    adj[parent].add(me)
            for kid in _ids(r.get("children")):
                adj[me].add(kid)
                adj[kid].add(me)
            for sp in _ids(r.get("spouses")):
                spouse[me].add(sp)

    if start not in adj:
        print(f"{start} has no parent or child edge in derived-family.csv")
        return 1

    # --- BFS ---------------------------------------------------------------
    dist = {start: 0}
    prev: dict[str, str] = {}
    q = deque([start])
    while q:
        cur = q.popleft()
        if dist[cur] >= max_hops:
            continue
        for nxt in adj[cur]:
            if nxt not in dist:
                dist[nxt] = dist[cur] + 1
                prev[nxt] = cur
                q.append(nxt)

    label = {}
    with open(LABELS, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            if r["geni_id"] in dist:
                label[r["geni_id"]] = r.get("label_en") or ""
    born = {}
    with open(FACTS, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            if r["geni_id"] in dist:
                born[r["geni_id"]] = (r.get("birth_date_year") or "").strip()

    reached = len(dist)
    with_item = sorted(((dist[g], g) for g in dist if g in qid))

    def chain(g: str) -> str:
        out, cur = [], g
        while cur in prev:
            out.append(label.get(cur) or cur)
            cur = prev[cur]
        out.append(label.get(start) or start)
        return " ← ".join(reversed(out))

    lines = [f"# Nearest people to `{start}` by hops in the parent/child graph", ""]
    lines += [
        "**A sibling is two hops**, up to the shared parent and back down; a first cousin "
        "is four. Spouse edges are excluded — marriage is not a hop between blood "
        "relatives.", "",
        f"Reached **{reached:,} people** within {max_hops} hops. "
        f"**{len(with_item):,}** of them carry a Wikidata item.", "",
        "## The nearest people who already carry an item", "",
        "| hops | born | qid | name |", "| ---: | ---: | --- | --- |",
    ]
    for d, g in with_item[:30]:
        lines.append(f"| {d} | {born.get(g) or '?'} | {qid[g]} | {label.get(g) or g} |")

    lines += ["", "## How many people sit at each distance", "",
              "| hops | people | of them with an item |", "| ---: | ---: | ---: |"]
    per = defaultdict(int)
    per_item = defaultdict(int)
    for g, d in dist.items():
        per[d] += 1
        if g in qid:
            per_item[d] += 1
    for d in sorted(per):
        lines.append(f"| {d} | {per[d]:,} | {per_item[d]:,} |")

    if with_item:
        d, g = with_item[0]
        lines += ["", "## The nearest one, and the route", "",
                  f"**{label.get(g) or g}** [{qid[g]}] — **{d} hops**", "",
                  "    " + chain(g)]

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"  reached {reached:,} people within {max_hops} hops; {len(with_item):,} carry an item")
    if with_item:
        d, g = with_item[0]
        print(f"  nearest with an item: {d} hops - {label.get(g) or g} [{qid[g]}]")
    for d in sorted(per)[:9]:
        print(f"    {d} hops: {per[d]:,} people, {per_item[d]:,} with an item")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
