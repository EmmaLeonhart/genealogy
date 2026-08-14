"""Find upward links out of a cut-off component, using Wikidata as the evidence.

The Baruch Jafe component has never met the main tree, and four exports seeded
*inside* it only made it bigger — a ball seeded in a component stays in that
component. Escaping needs a link we have not followed, and in-law links cannot
be one: a spouse edge joins two people already in the same component, or it
would not be in it.

So look upward, and look where there is independent evidence. Some people in the
cluster carry a Wikidata QID, and Wikidata records `P22`/`P25` for some of them.
If a parent's QID maps to a Geni profile that sits in the **main** component,
that is a genealogical link Wikidata asserts and our exports have not followed —
a bridge, with a citation.

Everything here is offline: the corpus for connectivity, `out/wikidata/p2600-all.tsv`
for the Geni↔QID mapping, and the local item store for the statements. Nothing
queries Wikidata.

    py scripts/find-cluster-escapes.py
"""

from __future__ import annotations

import gzip
import json
import re
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from genimerge import sources  # noqa: E402

P2600 = REPO / "out" / "wikidata" / "p2600-all.tsv"
INDEX = REPO / "out" / "wikidata" / "store-index.sqlite3"
SHARDS = REPO / "wikidata" / "items"
OUT = REPO / "reports" / "cluster-escapes.csv"

UPWARD = {"P22": "father", "P25": "mother"}


class DSU:
    def __init__(self) -> None:
        self.p: dict[str, str] = {}

    def find(self, x: str) -> str:
        r = x
        while self.p.setdefault(r, r) != r:
            r = self.p[r]
        while self.p[x] != r:
            self.p[x], x = r, self.p[x]
        return r

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[ra] = rb


def components() -> tuple[dict[str, str], dict[str, str], list[list[str]]]:
    dsu = DSU()
    name: dict[str, str] = {}
    indi = re.compile(r"^0 @I(\d+)@ INDI", re.M)
    named = re.compile(r"^0 @I(\d+)@ INDI\r?\n1 NAME ([^\r\n]*)", re.M)
    fam = re.compile(r"^0 @F(\d+)@ FAM$")
    mem = re.compile(r"^1 (?:HUSB|WIFE|CHIL) @I(\d+)@$")
    files = sources.find_exports()
    for n, path in enumerate(files, 1):
        text = Path(path).read_text(encoding="utf-8", errors="replace")
        for gid in indi.findall(text):
            dsu.find(gid)
        for m in named.finditer(text):
            name.setdefault(m.group(1), m.group(2).replace("/", "").strip())
        members: list[str] = []
        in_fam = False
        for line in text.split("\n"):
            line = line.rstrip("\r")
            if line.startswith("0 "):
                if in_fam and len(members) > 1:
                    for x in members[1:]:
                        dsu.union(members[0], x)
                members = []
                in_fam = bool(fam.match(line))
                continue
            if in_fam:
                g = mem.match(line)
                if g:
                    members.append(g.group(1))
        if in_fam and len(members) > 1:
            for x in members[1:]:
                dsu.union(members[0], x)
        if n % 60 == 0:
            print(f"  {n}/{len(files)} exports", file=sys.stderr)
    groups: dict[str, list[str]] = defaultdict(list)
    for g in dsu.p:
        groups[dsu.find(g)].append(g)
    ordered = sorted(groups.values(), key=len, reverse=True)
    comp_of = {g: str(i + 1) for i, grp in enumerate(ordered) for g in grp}
    return comp_of, name, ordered


def main() -> int:
    comp_of, name, ordered = components()
    print(f"\n{len(ordered)} components: {[len(c) for c in ordered]}")

    geni_to_qid: dict[str, str] = {}
    qid_to_geni: dict[str, str] = {}
    with P2600.open(encoding="utf-8") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 2:
                continue
            qid, gid = parts[0], parts[1]
            if not qid.startswith("Q"):
                qid, gid = gid, qid
            geni_to_qid.setdefault(gid, qid)
            qid_to_geni.setdefault(qid, gid)
    print(f"{len(geni_to_qid)} Geni↔QID pairs")

    main_comp = "1"
    targets = [g for g in ordered[1] if g in geni_to_qid]
    print(f"component #2: {len(ordered[1])} people, {len(targets)} carrying a QID")

    con = sqlite3.connect(INDEX)
    shard_of = {q: s for q, s in con.execute("select qid, shard from items")}
    want = {geni_to_qid[g]: g for g in targets}
    by_shard: dict[int, set[str]] = defaultdict(set)
    for q in want:
        if q in shard_of:
            by_shard[shard_of[q]].add(q)
    print(f"{sum(len(v) for v in by_shard.values())} of those items are in the store, "
          f"across {len(by_shard)} shards")

    rows = []
    for n, (shard, qids) in enumerate(sorted(by_shard.items()), 1):
        path = SHARDS / f"items-{shard:05d}.jsonl.gz"
        if not path.exists():
            continue
        with gzip.open(path, "rt", encoding="utf-8") as fh:
            for line in fh:
                if '"id":"' not in line and '"id": "' not in line:
                    continue
                d = json.loads(line)
                qid = d.get("id")
                if qid not in qids:
                    continue
                for prop, role in UPWARD.items():
                    for st in d.get("claims", {}).get(prop, []):
                        v = st["mainsnak"].get("datavalue", {}).get("value")
                        pq = v.get("id") if isinstance(v, dict) else None
                        if not pq:
                            continue
                        pg = qid_to_geni.get(pq)
                        where = comp_of.get(pg) if pg else None
                        rows.append({
                            "cluster_geni_id": want[qid],
                            "cluster_name": name.get(want[qid], ""),
                            "cluster_qid": qid,
                            "role": role,
                            "parent_qid": pq,
                            "parent_geni_id": pg or "",
                            "parent_component": where or ("no P2600" if not pg else "not in corpus"),
                            "bridges": "YES" if where == main_comp else "",
                        })
        if n % 20 == 0:
            print(f"  {n}/{len(by_shard)} shards", file=sys.stderr)

    import csv
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]) if rows else
                           ["cluster_geni_id", "cluster_name", "cluster_qid", "role",
                            "parent_qid", "parent_geni_id", "parent_component", "bridges"])
        w.writeheader()
        w.writerows(rows)

    bridges = [r for r in rows if r["bridges"]]
    print(f"\n{len(rows)} upward statements on cluster members")
    print(f"{len(bridges)} of them point at somebody in component #{main_comp}\n")
    for r in bridges:
        print(f"  {r['cluster_name'][:34]:<34} {r['cluster_geni_id']}  {r['role']:<6} "
              f"-> {r['parent_qid']} = {r['parent_geni_id']}")
    if not bridges:
        outside = [r for r in rows if r["parent_component"] == "not in corpus"]
        print(f"none. {len(outside)} parents have a Geni profile we do not hold — "
              f"those are the export seeds:")
        seen = set()
        for r in outside:
            if r["parent_geni_id"] in seen:
                continue
            seen.add(r["parent_geni_id"])
            print(f"  {r['cluster_name'][:34]:<34} {r['role']:<6} -> "
                  f"{r['parent_qid']}  geni {r['parent_geni_id']}")
    print(f"\nwrote {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
