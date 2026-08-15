"""Build the reviewable Wikidata batch for the pre-1624 Samaritan High Priests.

**This generates a batch. It executes nothing.** Review before execute is
load-bearing (`docs/wikidata-bot.md`), and no Wikidata edit happens before
1 September 2026 regardless.

The line is the 78 profiles Geni holds in one father-to-son chain from `Uzzi ben
Bakhi` down through Baba Rabba — the **pre-1624 Phinhas** high priesthood. None
of the 78 carries a Wikidata item, joined on the Geni ID.

**It is kept separate from the post-1624 Itamar items on purpose.** Emma,
2026-08-14: *"on wikidata explicitly, they are going to be different lines… two
parallel lines on Wikidata"*. The Phinhas line ended in 1624 and the Itamar
priests replaced it; they are not one descent, and nothing here links them.

**`Samaritan High Priest` never becomes a family name.** It sits in the GEDCOM
surname slot, which is an office in the surname field — CLAUDE.md § *A clan name
is not a clan*, and the same shape as `SURN 秦州成紀`. It is emitted as the item
**description** and nowhere else. No `P734` is generated.

**The two recorded "wives" are excluded.** `daughter of Sanballat the Horonite`
and `daughter of the king of Assyria` are descriptions, not names; creating items
labelled that would invent two people. See `reports/samaritan-marriages.md`.

    py scripts/build-samaritan-priest-batch.py
"""

from __future__ import annotations

import argparse
import csv
import json
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from labels import label_for  # noqa: E402

CENSUS_PEOPLE = REPO / "reports" / "samaritan-people.csv"
CENSUS_FAMS = REPO / "reports" / "samaritan-marriages.csv"
INDEX = REPO / "out" / "wikidata" / "store-index.sqlite3"

OFFICE = "Samaritan High Priest"
MALE = "Q6581097"          # sex or gender -> male
HUMAN = "Q5"               # instance of -> human


def strip_office(name: str) -> str:
    """`Hezekiah IV /Samaritan High Priest/` -> `Hezekiah IV`."""
    head, _, _ = name.partition("/")
    return " ".join(head.split())


def load_census():
    people, fams = {}, {}
    for r in csv.DictReader(CENSUS_PEOPLE.open(encoding="utf-8")):
        people.setdefault(r["geni_id"], r)
    for r in csv.DictReader(CENSUS_FAMS.open(encoding="utf-8")):
        fams.setdefault(r["family_id"], r)
    return people, fams


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default="out/wikidata/samaritan-priests.json")
    ap.add_argument("--qs", default="out/wikidata/samaritan-priests.qs")
    args = ap.parse_args()

    people, fams = load_census()

    # father edges, from the census
    father = {}
    for f in fams.values():
        if not f["husband_geni_id"]:
            continue
        for c in f["children_geni_ids"].split():
            father[c] = f["husband_geni_id"]

    line = {g for g, r in people.items() if OFFICE in r["name"]}
    # Uzzi ben Bakhi heads the chain and his own record says `/High Priest/`
    # rather than the Samaritan form, so he is added by being somebody's father.
    for g in list(line):
        p = father.get(g)
        while p and p not in line:
            line.add(p)
            p = father.get(p)
    print(f"{len(line)} profiles in the pre-1624 line")

    # Anything already on Wikidata is not a creation. Joined on the Geni ID.
    #
    # **Two sources, and missing the second one was a real bug.** The store index
    # only knows a link once *Wikidata* states the `P2600`. Emma also writes the
    # Wikidata URL onto the **Geni profile**, which is a hand-made identity claim
    # that Wikidata has not been told about yet — and those were invisible here.
    # The batch therefore proposed creating `Jonathan I` (`Q20502598`) and
    # `Baba Rabba` (`Q2911644`), both of which already exist and both of which
    # she had linked herself. Emma, 2026-08-16: *"I literally have an entire file
    # dedicated to samaritan high priest qids that you ignored."* Duplicate items
    # are the one failure mode here that damages Wikidata rather than wasting a
    # run, so this reads both sources.
    linked = {}
    if INDEX.exists():
        conn = sqlite3.connect(INDEX)
        for g in line:
            row = conn.execute(
                "select qid from geni where geni_id=?", (g,)).fetchone()
            if row:
                linked[g] = row[0]
    from_wikidata = len(linked)

    pairs_csv = REPO / "reports" / "geni-wikidata-pairs.csv"
    embedded = {}
    if pairs_csv.exists():
        with pairs_csv.open(encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                g, q = row.get("geni_id", ""), row.get("qid", "")
                if g in line and q and g not in linked:
                    embedded[g] = q
    linked.update(embedded)
    print(f"{from_wikidata} already carry a Wikidata item; "
          f"{len(embedded)} more are linked by a QID on the Geni profile")
    for g, q in sorted(embedded.items()):
        print(f"  NOT creating {people[g]['name']!r} - it is {q}")

    # Order parents before children so `requires` is satisfiable in sequence.
    ordered, placed = [], set()

    def place(g):
        if g in placed:
            return
        p = father.get(g)
        if p in line:
            place(p)
        placed.add(g)
        ordered.append(g)

    for g in sorted(line, key=lambda g: people[g]["name"]):
        place(g)

    batch = []
    for g in ordered:
        if g in linked:
            continue
        rec = people[g]
        label = label_for(strip_office(rec["name"]))
        ref = [{"property": "P2600", "value": g}]
        entry = {
            "id": f"create_individual:{g}",
            "type": "create_individual",
            "priority": False,
            "subject": {"qid": None, "geni_id": g},
            "requires": [],
            "anchor": None,
            "labels": {"en": label, "mul": label},
            "descriptions": {"en": OFFICE},
            "statements": [
                {"property": "P31", "value": HUMAN, "references": ref},
                {"property": "P2600", "value": g, "references": []},
                {"property": "P21", "value": MALE, "references": ref},
            ],
            "links": [],
        }
        p = father.get(g)
        if p in line:
            entry["requires"] = [f"create_individual:{p}"] if p not in linked else []
            entry["links"].append({
                "property": "P22",
                "value": linked.get(p) or f"@create_individual:{p}",
                "references": ref + [{"property": "P2600", "value": p}],
            })
        batch.append(entry)

    out = REPO / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(batch, indent=1, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    print(f"wrote {out} ({len(batch)} create_individual entries)")

    # QuickStatements, for eyeballing. LAST is QuickStatements' back-reference to
    # the item the preceding CREATE made; a father created earlier in the run is
    # not LAST, so those P22 lines are left as a marker rather than emitted wrong.
    lines = []
    for e in batch:
        g = e["subject"]["geni_id"]
        lines.append("CREATE")
        # An empty label is deliberate - see scripts/labels.py. Emitting
        # `Len ""` would set a blank label rather than leaving it unset.
        if e["labels"]["en"]:
            lines.append(f'LAST\tLen\t"{e["labels"]["en"]}"')
            lines.append(f'LAST\tLmul\t"{e["labels"]["mul"]}"')
        lines.append(f'LAST\tDen\t"{e["descriptions"]["en"]}"')
        lines.append(f"LAST\tP31\t{HUMAN}\tS2600\t\"{g}\"")
        lines.append(f'LAST\tP2600\t"{g}"')
        lines.append(f"LAST\tP21\t{MALE}\tS2600\t\"{g}\"")
        for link in e["links"]:
            val = link["value"]
            if val.startswith("@"):
                lines.append(f"# P22 -> {val[1:]} (resolve after that item exists)")
            else:
                lines.append(f"LAST\tP22\t{val}\tS2600\t\"{g}\"")
    qs = REPO / args.qs
    qs.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {qs} ({len(lines)} lines)")

    print("\nfirst three, in order:")
    for e in batch[:3]:
        print(f'  {e["labels"]["en"]}  requires={e["requires"]}')
    print("last:", batch[-1]["labels"]["en"] if batch else "(none)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
