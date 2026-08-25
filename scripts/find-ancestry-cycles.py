"""People who are their own ancestor — the one defect Emma wants gone.

    python scripts/find-ancestry-cycles.py

**Emma, 2026-08-24:** *"The Samaritan High Priests are a bit of a tangle in that period,
and my approach to it is more or less that I don't want a cycle, but I'm basically willing
to accept clutter."*

That is the whole rule, and it is sharper than it looks. **Duplicate profiles are
clutter and stay.** A person appearing twice, a name recurring down a priestly line, two
profiles either side of a third — all fine, none of it is worth an edit. **A cycle is
different**: it says somebody is their own ancestor, which is impossible in life and
quietly corrupts every generational measure that walks upward.

**A chain through two same-named profiles is NOT a cycle**, which is why this measures
rather than assumes. The Samaritan case looked like one — *Amram V* recorded as son of one
*Aaron III* and father of another — and it is not, because the two Aaron III profiles are
distinct nodes. It is a chain, therefore clutter, therefore left alone.

Reads `reports/derived-family.csv` and walks parent links with a three-colour DFS: a grey
node reached again is a cycle, and the path back to it is the cycle itself. Offline.

**Fixes belong on Geni, not here.** Emma: *"We're just going to fix it on Geni."* This
report names the people and their profile ids so she can.

Writes `reports/ancestry-cycles.tsv`.
"""
from __future__ import annotations

import collections
import csv
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

ROOT = Path(__file__).resolve().parent.parent
WHITE, GREY, BLACK = 0, 1, 2


def main():
    parent = collections.defaultdict(set)
    with open(ROOT / "reports" / "derived-family.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for column in ("father", "mother"):
                value = (row.get(column) or "").strip()
                if value:
                    parent[row["geni_id"]].add(value)
    print(f"{len(parent):,} people with a recorded parent")

    state: dict[str, int] = {}
    cycles: list[list[str]] = []
    for start in list(parent):
        if state.get(start, WHITE) != WHITE:
            continue
        state[start] = GREY
        path = [start]
        stack = [(start, iter(parent.get(start, ())))]
        while stack:
            node, walker = stack[-1]
            nxt = next(walker, None)
            if nxt is None:
                state[node] = BLACK
                stack.pop()
                path.pop()
                continue
            colour = state.get(nxt, WHITE)
            if colour == GREY:
                cycles.append(path[path.index(nxt):] + [nxt])
            elif colour == WHITE:
                state[nxt] = GREY
                path.append(nxt)
                stack.append((nxt, iter(parent.get(nxt, ()))))

    people = {p for cycle in cycles for p in cycle}
    labels = {}
    with open(ROOT / "reports" / "derived-labels.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in people:
                labels[row["geni_id"]] = (row["label_en"] or row["label_mul"] or "")

    rows = []
    for n, cycle in enumerate(cycles, 1):
        # The cycle repeats its first person at the end; drop that for the listing.
        members = cycle[:-1] if len(cycle) > 1 and cycle[0] == cycle[-1] else cycle
        named = [labels.get(p, "") for p in members]
        if not any(named):
            continue          # every member unnamed: nothing a human could act on
        for step, person in enumerate(members):
            rows.append({
                "cycle": n,
                "length": len(members),
                "step": step,
                "geni_id": person,
                "name": labels.get(person, ""),
                "url": f"https://www.geni.com/people/x/{person}",
                "next_in_cycle": labels.get(members[(step + 1) % len(members)], ""),
            })

    dest = ROOT / "reports" / "ancestry-cycles.tsv"
    with open(dest, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    shown = len({r["cycle"] for r in rows})
    print(f"\n{len(cycles)} cycles over {len(people)} people; "
          f"{shown} have at least one named member")
    print(f"wrote {dest.relative_to(ROOT)}\n")
    seen = set()
    for row in rows:
        if row["cycle"] in seen:
            continue
        seen.add(row["cycle"])
        members = [r["name"] for r in rows if r["cycle"] == row["cycle"]]
        print(f"  cycle {row['cycle']:>2} ({row['length']}): "
              + " -> ".join(m[:22] or "?" for m in members))


if __name__ == "__main__":
    main()
