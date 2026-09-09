"""Which 'absent' people on the Charlemagne route already have a Wikidata item?

    python scripts/find-absent-on-wikidata.py

**Emma, 2026-08-25:** *"I want you to do a manual exploration to see in that line goin down from
Charlemagne to Arne and me, which of the supposed absent members are actually just present on
wikidata without ids."*

`reports/charlemagne-route.csv` marks 16 of its 399 steps `create`, meaning no Geni id of theirs
appears on any Wikidata item. **That is not the same as having no item.** `Q2183430` *Benedicta
Ebbesdotter of Hvide* carries thirty properties and no `P2600`, so the route called her absent —
and a batch built from it created a second item for her. She is step 127.

## The search is structural, never a name lookup

For an absent person, take the relatives who **do** have a QID, and look at the reciprocal slot on
their item:

| the relative is their… | so look at the relative's… |
| --- | --- |
| father or mother | `P40` *child* |
| child | `P22` *father* / `P25` *mother* |
| spouse | `P26` *spouse* |

Any item in that slot **not already matched to one of our Geni ids** is a candidate: Wikidata says
this person's father has a child we cannot account for, and the person we think is missing is the
obvious explanation.

This is the same evidence the duplicate guard uses, run as a search rather than a veto. It never
asks whether a label looks similar — `CLAUDE.md` deleted a module for that. Names and dates are
printed **beside** each candidate so a human can judge, and play no part in finding it.

## What a candidate is and is not

A candidate is a **question**, not a match. A father with four children on Wikidata and three
matched leaves one unexplained item, and that item may be a sibling we have never held rather than
the person being sought. So every candidate is reported with its label, dates, and which relative
produced it, and **nothing is emitted** — no `P2600`, no creation, no merge.

The one thing it does settle firmly: **a `create` row with a candidate must not be created** until
somebody has looked. That is the whole point.

Writes `reports/absent-but-present.tsv`.
"""
from __future__ import annotations

import collections
import csv
import gzip
import json
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

ROOT = Path(__file__).resolve().parent.parent


def main():
    route = list(csv.DictReader(open(ROOT / "reports" / "charlemagne-route.csv",
                                     encoding="utf-8")))
    absent = [r for r in route if r["action"] == "create"]
    print(f"{len(route)} steps on the route, {len(absent)} marked absent")

    # Every Geni id Wikidata carries, and the reverse.
    q_of_g, g_of_q = {}, collections.defaultdict(set)
    with open(ROOT / "out" / "wikidata" / "p2600-all.tsv", encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) >= 2 and row[0].startswith("Q") and row[1].strip().isdigit():
                q_of_g.setdefault(row[1].strip(), row[0])
                g_of_q[row[0]].add(row[1].strip())
    # The route's own qid column covers people whose item predates the P2600 dump.
    for r in route:
        if r.get("qid") and r["geni_id"] not in q_of_g:
            q_of_g[r["geni_id"]] = r["qid"]
            g_of_q[r["qid"]].add(r["geni_id"])
    print(f"{len(q_of_g):,} Geni ids with a known item")

    rel = {}
    with open(ROOT / "out" / "wikidata" / "relations.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            rel[row["qid"]] = row
    print(f"{len(rel):,} items with relationships")

    want = {r["geni_id"] for r in absent}
    fam = {}
    with open(ROOT / "reports" / "derived-family.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in want:
                fam[row["geni_id"]] = row
    # children of the absent people, so a child's P22/P25 can be walked back
    kids_of = collections.defaultdict(set)
    with open(ROOT / "reports" / "derived-family.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for parent in (row.get("father"), row.get("mother")):
                if parent in want:
                    kids_of[parent].add(row["geni_id"])

    def split(cell):
        return [x for x in (cell or "").replace(",", ";").split(";") if x.strip()]

    rows = []
    for r in absent:
        g = r["geni_id"]
        mine = fam.get(g, {})
        cands = {}
        # parents -> their P40
        for slot, col in (("father", "father"), ("mother", "mother")):
            p = (mine.get(col) or "").strip()
            pq = q_of_g.get(p)
            if not pq:
                continue
            for k in split(rel.get(pq, {}).get("p40")):
                if not g_of_q.get(k):
                    cands.setdefault(k, []).append(f"{slot} {pq} lists it as a child")
        # children -> their P22 / P25
        for c in kids_of.get(g, ()):
            cq = q_of_g.get(c)
            if not cq:
                continue
            for prop, word in (("p22", "father"), ("p25", "mother")):
                for x in split(rel.get(cq, {}).get(prop)):
                    if not g_of_q.get(x):
                        cands.setdefault(x, []).append(f"child {cq} names it as {word}")
        # spouses -> their P26
        for sp in split(mine.get("spouses")):
            sq = q_of_g.get(sp)
            if not sq:
                continue
            for x in split(rel.get(sq, {}).get("p26")):
                if not g_of_q.get(x):
                    cands.setdefault(x, []).append(f"spouse {sq} names it as a spouse")
        for q, why in cands.items():
            rows.append({"step": r["step"], "geni_id": g, "geni_name": r["name"],
                         "geni_born": r["born"], "candidate_qid": q,
                         "why": " | ".join(why)})

    # Labels and dates for the candidates, so a human can judge them.
    con = sqlite3.connect(str(ROOT / "out" / "wikidata" / "store-index.sqlite3"))
    by_shard = collections.defaultdict(set)
    for r in rows:
        hit = con.execute("SELECT shard FROM items WHERE qid=?",
                          (r["candidate_qid"],)).fetchone()
        if hit:
            by_shard[hit[0]].add(r["candidate_qid"])
    info = {}
    for shard, wanted in by_shard.items():
        path = ROOT / "wikidata" / "items" / f"items-{shard:05d}.jsonl.gz"
        if not path.exists():
            continue
        with gzip.open(path, "rt", encoding="utf-8") as f:
            for line in f:
                if not wanted:
                    break
                for q in list(wanted):
                    if f'"{q}"' not in line:
                        continue
                    d = json.loads(line)
                    if d.get("id") != q:
                        continue
                    wanted.discard(q)
                    L = d.get("labels", {})
                    def yr(p):
                        for st in d.get("claims", {}).get(p, []):
                            t = (st["mainsnak"].get("datavalue", {})
                                 .get("value", {}).get("time", ""))
                            if t:
                                return ("-" if t.startswith("-") else "") + t[1:5].lstrip("0")
                        return ""
                    info[q] = {
                        "label": (L.get("en", {}).get("value")
                                  or next((v["value"] for v in L.values()), "")),
                        "born": yr("P569"), "died": yr("P570"),
                        "props": len(d.get("claims", {})),
                    }
                    break
    for r in rows:
        i = info.get(r["candidate_qid"], {})
        r["candidate_label"] = i.get("label", "")
        r["candidate_born"] = i.get("born", "")
        r["candidate_died"] = i.get("died", "")
        r["candidate_properties"] = i.get("props", "")

    rows.sort(key=lambda r: (int(r["step"]), r["candidate_qid"]))
    dest = ROOT / "reports" / "absent-but-present.tsv"
    with open(dest, "w", encoding="utf-8", newline="") as f:
        cols = ["step", "geni_id", "geni_name", "geni_born", "candidate_qid",
                "candidate_label", "candidate_born", "candidate_died",
                "candidate_properties", "why"]
        w = csv.DictWriter(f, fieldnames=cols, delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    withc = {r["geni_id"] for r in rows}
    print(f"\nwrote {dest.relative_to(ROOT)}")
    print(f"{len(withc)} of {len(absent)} absent people have at least one candidate item")
    print(f"{len(rows)} candidates in total\n")
    for r in rows:
        print(f"  step {r['step']:>3}  {r['geni_name'][:34]:<34} b.{r['geni_born'] or '?':<6}")
        print(f"          -> {r['candidate_qid']:<12} \"{r['candidate_label'][:34]}\" "
              f"b.{r['candidate_born'] or '?'} d.{r['candidate_died'] or '?'} "
              f"({r['candidate_properties']} props)")
        print(f"          {r['why'][:110]}")


if __name__ == "__main__":
    main()
