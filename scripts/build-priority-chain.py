"""The prioritised, ordered chain of edits that links a person to the world tree.

Emma, 2026-08-13: *"Great save this path it's important. This one is a priority
and it has an ordering."*

The ordering is forced, not chosen:

1. **`add_geni_id` on the subject's own item comes first.** Nothing can be cited
   to a Geni ID that is not on the item yet.
2. **Creations run from the Wikidata end inward.** `create_individual` links to a
   parent or child *already on Wikidata*, so the person adjacent to the existing
   network is created first and each creation becomes the anchor for the next.
3. **The subject is linked last**, to the newly created parent.

**15 creations, not 16.** The route search found a 16th — Bengta Ebbesdotter
Galen — but she sits *inside* the 1,116,499-person component, between two people
who are both already in it. She is connected to Charlemagne by other edges
whatever we do, so the path does not need her; the search routed through her on a
cost tie. Only the run of people between the subject and the first person already
in the component is required.

Writes `out/wikidata/priority-chain.json` and `reports/priority-chain.md`.

    py scripts/build-priority-chain.py
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

ROUTE = REPO_ROOT / "reports" / "charlemagne-route.csv"
COMPONENTS = REPO_ROOT / "reports" / "wikidata-components.csv"
LABELS = REPO_ROOT / "reports" / "derived-labels.csv"
FACTS = REPO_ROOT / "reports" / "derived-facts.csv"
FAMILY = REPO_ROOT / "reports" / "derived-family.csv"
OUT_JSON = REPO_ROOT / "out" / "wikidata" / "priority-chain.json"
OUT_MD = REPO_ROOT / "reports" / "priority-chain.md"

csv.field_size_limit(10_000_000)
WORLD_TREE = 1_116_499
SEX = {"M": "Q6581097", "F": "Q6581072"}


def geni_ref(*ids: str) -> list[dict]:
    return [{"property": "P2600", "value": i} for i in ids if i]


def main() -> int:
    route = list(csv.DictReader(open(ROUTE, encoding="utf-8")))
    comp = {r["qid"]: int(r["component_size"])
            for r in csv.DictReader(open(COMPONENTS, encoding="utf-8"))}
    lab = {r["geni_id"]: r for r in csv.DictReader(open(LABELS, encoding="utf-8"))}
    fac = {r["geni_id"]: r for r in csv.DictReader(open(FACTS, encoding="utf-8"))}
    fam = {r["geni_id"]: r for r in csv.DictReader(open(FAMILY, encoding="utf-8"))}

    # The first person on the route who is already inside the world tree. Anyone
    # beyond them is connected to Charlemagne without our help.
    entry = next(i for i, r in enumerate(route)
                 if r["qid"] and comp.get(r["qid"], 0) == WORLD_TREE)
    subject = route[0]
    needed = route[1:entry]          # the people to create, subject-ward first
    anchor = route[entry]

    objects: list[dict] = []
    # 1. the subject's Geni ID
    objects.append({
        "id": f"add_geni_id:{subject['qid']}",
        "type": "add_geni_id",
        "priority": True,
        "subject": {"qid": subject["qid"], "geni_id": subject["geni_id"]},
        "requires": [],
        "statement": {"property": "P2600", "value": subject["geni_id"],
                      "references": []},
    })

    # 2. creations, from the anchor inward
    previous_anchor_qid = anchor["qid"]
    previous_anchor_geni = anchor["geni_id"]
    for step in reversed(needed):
        geni_id = step["geni_id"]
        row = fam.get(geni_id, {})
        rel = "P22" if row.get("father") == previous_anchor_geni else \
              "P25" if row.get("mother") == previous_anchor_geni else "P40"
        statements = [
            {"property": "P31", "value": "Q5", "references": geni_ref(geni_id)},
            {"property": "P2600", "value": geni_id, "references": []},
        ]
        sex = SEX.get(fac.get(geni_id, {}).get("sex", ""))
        if sex:
            statements.append({"property": "P21", "value": sex,
                               "references": geni_ref(geni_id)})
        label = lab.get(geni_id, {}).get("label_en", "")
        objects.append({
            "id": f"create_individual:{geni_id}",
            "type": "create_individual",
            "priority": True,
            "subject": {"qid": None, "geni_id": geni_id},
            "requires": ([f"create_individual:{previous_anchor_geni}"]
                         if previous_anchor_qid is None else []),
            "anchor": {"qid": previous_anchor_qid, "geni_id": previous_anchor_geni,
                       "property": rel},
            "labels": {"en": label, "mul": label} if label else {},
            "statements": statements,
            "links": [{"property": rel, "value": previous_anchor_qid,
                       "references": geni_ref(geni_id, previous_anchor_geni)}],
        })
        previous_anchor_qid = None
        previous_anchor_geni = geni_id

    # 3. link the subject to the last created person
    last = needed[0]["geni_id"]
    row = fam.get(subject["geni_id"], {})
    rel = "P22" if row.get("father") == last else "P25" if row.get("mother") == last else "P40"
    objects.append({
        "id": f"add_statement:{subject['qid']}:{rel}",
        "type": "add_statement",
        "priority": True,
        "subject": {"qid": subject["qid"], "geni_id": subject["geni_id"]},
        "requires": [f"add_geni_id:{subject['qid']}",
                     f"create_individual:{last}"],
        "statement": {"property": rel, "value": None,
                      "value_from": f"create_individual:{last}",
                      "references": geni_ref(subject["geni_id"], last)},
    })

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(objects, ensure_ascii=False, indent=1), encoding="utf-8")

    L: list[str] = []
    add = L.append
    add("# Priority chain: linking Emma into the Wikidata world tree")
    add("")
    add("Emma, 2026-08-13: *\"This one is a priority and it has an ordering.\"*")
    add("")
    add(f"**{len(objects)} edits, executed in this order.** The ordering is forced: the")
    add("Geni ID must exist before anything cites it, and a creation must have a")
    add("Wikidata-linked relative to attach to — so creations run from the existing")
    add("network inward, each becoming the anchor for the next.")
    add("")
    add(f"Entry point: **{anchor['name']}** {anchor['born']} `{anchor['qid']}`, already in")
    add(f"the {WORLD_TREE:,}-person component.")
    add("")
    add("| # | edit | who | born |")
    add("| ---: | --- | --- | ---: |")
    for i, o in enumerate(objects, 1):
        gid = o["subject"]["geni_id"]
        who = lab.get(gid, {}).get("label_en") or gid
        add(f"| {i} | `{o['type']}` | {who} | {fac.get(gid, {}).get('birth_date_year', '?')} |")
    add("")
    add("## Why 15 creations and not 16")
    add("")
    add("The route search reported 16. The extra one — Bengta Ebbesdotter Galen, born")
    add("1170 — sits **inside** the world-tree component, between two people who are both")
    add("already in it. She is connected to Charlemagne by other edges regardless; the")
    add("search routed through her on a cost tie. Only the unbroken run between Emma and")
    add("the first person already in the component is actually required.")
    add("")
    add("## What this buys")
    add("")
    add("| target | component |")
    add("| --- | ---: |")
    add("| this chain | **1,116,499** |")
    add("| Trond Benkestok `Q7845461` | 3 |")
    add("| Aadne Garborg `Q467497` | 3 |")
    add("| Racin Kolnes `Q30019076` | 2 |")
    add("| Jørgen Erikssøn `Q11979685` | 1 |")

    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {OUT_JSON} and {OUT_MD}")
    print(f"  {len(objects)} edits: 1 add_geni_id, {len(needed)} creations, 1 link")
    print(f"  entry point: {anchor['name']} {anchor['born']} {anchor['qid']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
