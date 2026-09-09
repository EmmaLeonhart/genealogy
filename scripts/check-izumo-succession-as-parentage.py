"""Where does Wikidata record an Izumo BROTHER as a FATHER?

    python scripts/check-izumo-succession-as-parentage.py

**Emma's ruling, 2026-08-24:** the Izumo chart edges are **succession, not parentage**. Two things
forced it — Takanori 81 and Takatomi 80 held consecutive seats and were brothers, and the sister
repo's raw wiki says *"solid lines indicate biological children, dotted lines indicate adopted
children"* while `reports/izumo-chart-edges.tsv` had flattened all of it to `kind=child`.

**On 2026-08-26 the same confusion turned up on Wikidata's side.** The model-vs-reality diff
flagged Otoyama 26 `Q95161949`: Geni gives his father as Izumo no Hatayasu `Q95161958`, the chart
agrees — Hatayasu#24 → Hiroshima#25 **and** Hatayasu#24 → Otoyama#26 — so Hiroshima and Otoyama
are **brothers**. Wikidata gives Otoyama's father as **Hiroshima**: his brother, and his immediate
predecessor in the succession.

That is one confirmed instance. The chart holds 88 **ordered** sibling pairs, which is **10
unordered pairs** holding consecutive seat numbers -- an earlier note said twenty, counting each
pair from both ends. Ten places the confusion is possible. This checks all of them.

## The test

For each pair of chart siblings `(earlier, later)` whose seat numbers differ by one: does
Wikidata's `P22` *father* on the later one name the earlier one?

* **yes** — succession recorded as parentage. Wikidata says a man's brother is his father.
* **no, and it names their shared parent** — correct.
* **no `P22` at all** — nothing to say; the gap is a gap.

**Report, never correct.** `CLAUDE.md`: the purpose is to ADD, a disagreement is a note, and Izumo
identity calls are Emma's. Nothing here is emitted.

Needs `out/izumo-items.json`, written by
`scripts/model-vs-reality.py --roster reports/izumo-p2600-pairs.tsv --items out/izumo-items.json`.

Writes `reports/izumo-succession-as-parentage.tsv`.
"""
from __future__ import annotations

import collections
import csv
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)
ROOT = Path(__file__).resolve().parent.parent
R = ROOT / "reports"
ITEMS = ROOT / "out" / "izumo-items.json"

SEAT = re.compile(r"#(\d+)\s*$")


def base(name):
    """`Izumo no Otoyama#26` -> `Izumo no Otoyama`, which is how the roster spells it."""
    return SEAT.sub("", name or "").strip()


def seat(name):
    m = SEAT.search(name or "")
    return int(m.group(1)) if m else None


def main():
    if not ITEMS.exists():
        sys.exit(f"missing {ITEMS} - run scripts/model-vs-reality.py over the Izumo roster first")
    items = json.load(open(ITEMS, encoding="utf-8"))

    edges = [(r["parent"], r["child"]) for r in
             csv.DictReader(open(R / "izumo-chart-edges.tsv", encoding="utf-8"), delimiter="\t")]
    kids = collections.defaultdict(list)
    for p, c in edges:
        kids[p].append(c)
    print(f"{len(edges)} chart edges over {len(kids)} parents")

    # The roster maps a chart NAME to a QID. `izumo-chart-roster.tsv` is the join.
    # **The join is on the BASE name, and the seat lives in its own column.**
    # `izumo-chart-edges.tsv` writes `Izumo no Otoyama#26`; `izumo-chart-roster.tsv` writes
    # `english = Izumo no Otoyama` with `succession = 26`. Looking for a `chart_name` column
    # that does not exist matched nothing, and every pair then came back "no item held" --
    # an empty join reads exactly like an absence of data, which is the failure this file is
    # about in the first place.
    name2qid = {}
    roster = R / "izumo-chart-roster.tsv"
    with open(roster, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            q = (row.get("qid") or "").strip()
            nm = (row.get("english") or "").strip()
            if nm and q.startswith("Q"):
                name2qid[nm] = q
    print(f"{len(name2qid)} chart names carry a QID in {roster.name}")

    labels = {}
    with open(ROOT / "out" / "wikidata" / "labels.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row["qid"] in items:
                labels[row["qid"]] = row["en"] or row["mul"] or row["ja"]

    rows, tally = [], collections.Counter()

    # **Every consecutive-seat sibling pair, collected first and judged after.**
    #
    # Two bugs preceded this, and both produced a plausible number. Taking
    # `zip(numbered, numbered[1:])` compares only neighbours in the sorted list and silently
    # dropped `Kiyotaka#54 / Takamune#55` -- 9 of the 10 real pairs. Replacing it with a nested
    # loop but leaving the body at the OUTER indentation ran the judgement once per `a`, with
    # `b` holding whatever the inner loop last touched, and produced 98 rows including
    # self-pairs like `Takatoki#53 -> Takatoki#53`.
    #
    # Building the list, then judging it, makes both impossible to write.
    pairs = {}
    for parent, children in kids.items():
        numbered = sorted((s, c) for s, c in ((seat(c), c) for c in children) if s is not None)
        for sa, a in numbered:
            for sb, b in numbered:
                if sb - sa == 1 and a != b:
                    pairs.setdefault((a, b), parent)
    print(f"{len(pairs)} consecutive-seat sibling pairs on the chart")

    for (a, b), parent in sorted(pairs.items()):
        qa, qb = name2qid.get(base(a)), name2qid.get(base(b))
        item = items.get(qb or "")
        if not qa or not qb or not item:
            verdict, stated = "one of the pair has no item held", ""
        else:
            p22 = [s["mainsnak"].get("datavalue", {}).get("value", {}).get("id")
                   for s in (item.get("claims", {}).get("P22") or [])
                   if s.get("rank") != "deprecated"]
            p22 = [x for x in p22 if x]
            stated = ";".join(f"{x} {labels.get(x, '')}".strip() for x in p22)
            if not p22:
                verdict = "no P22 on the later one"
            elif qa in p22:
                verdict = "SUCCESSION AS PARENTAGE - his brother is recorded as his father"
            elif name2qid.get(base(parent)) and name2qid[base(parent)] in p22:
                verdict = "correct - names their shared parent"
            else:
                verdict = "names somebody else"
        tally[verdict] += 1
        rows.append({"earlier": a, "later": b, "earlier_qid": qa or "", "later_qid": qb or "",
                     "shared_parent": parent, "verdict": verdict, "wikidata_p22": stated})


    with open(R / "izumo-succession-as-parentage.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["earlier"], delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    print(f"\n{len(rows)} consecutive-seat sibling pairs checked:\n")
    for v, n in tally.most_common():
        print(f"   {n:>3}  {v}")
    bad = [r for r in rows if r["verdict"].startswith("SUCCESSION")]
    if bad:
        print("\nthe ones where a brother is recorded as a father:")
        for r in bad:
            print(f"   {r['earlier']} -> {r['later']}   {r['later_qid']} P22 = {r['wikidata_p22']}")
    print("\nwrote reports/izumo-succession-as-parentage.tsv")
    print("NOTHING CORRECTED. The purpose is to add; a disagreement is a note.")


if __name__ == "__main__":
    main()
