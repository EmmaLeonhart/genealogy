"""Derive the Garborg modelling from FULL downloaded items, not from a summary.

    python scripts/garborg-modelling.py

**Emma, 2026-08-24:** *"you're supposed to download the full wikidata items for the
people I've edited to get the modelling not look at my edit history to see what's in
them."*

The first pass read each item through a fetch-and-summarise channel. That is not the
same as holding the item: it truncated `Q467497` — 126 properties arrived as a partial
list ending out of numeric order — and it invented property labels, calling `P2600`
"Peruvian NLB" and `P1411` "Nobel Prize recipient". Neither error would survive a look
at the real JSON, and both went into a report.

`out/garborg-full-items.json` is the whole items, fetched once through
`genimerge.wikidata.full_entities` — the sanctioned client, one batched request. Every
number below is counted from that file offline, so it is re-checkable without touching
the network again.

Writes `reports/garborg-live-state.tsv` (what each item holds, for the batch builder to
consult) and prints the modelling summary.
"""
from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
ITEMS = ROOT / "out" / "garborg-full-items.json"
OUT = ROOT / "reports" / "garborg-live-state.tsv"

#: The properties this programme emits, so "does she use it" is answerable per item.
#: Labels from `reports/wikidata-labels.tsv` / `CLAUDE.md`; never guessed.
OURS = {
    "P31": "instance of", "P21": "sex or gender", "P2600": "Geni.com profile ID",
    "P569": "date of birth", "P570": "date of death", "P22": "father", "P25": "mother",
    "P26": "spouse", "P40": "child", "P3373": "sibling", "P735": "given name",
    "P734": "family name", "P5056": "patronym or matronym", "P19": "place of birth",
    "P20": "place of death", "P119": "place of burial", "P1477": "birth name",
}


def value_of(snak):
    dv = snak.get("datavalue", {}).get("value")
    if isinstance(dv, dict):
        return dv.get("id") or dv.get("time") or dv.get("text") or json.dumps(dv)
    return str(dv)


def main():
    data = json.loads(ITEMS.read_text(encoding="utf-8"))
    print(f"{len(data)} full items\n")

    rows, qualifier_use, ref_use = [], collections.Counter(), collections.Counter()
    for qid, item in data.items():
        claims = item.get("claims", {})
        labels = item.get("labels", {})
        rows.append({
            "qid": qid,
            "verified": "2026-08-24",
            "langs": " ".join(sorted(labels)),
            "props": " ".join(sorted(claims, key=lambda p: int(p[1:]))),
        })
        for prop, statements in claims.items():
            for st in statements:
                for qprop in st.get("qualifiers", {}):
                    qualifier_use[(prop, qprop)] += 1
                for ref in st.get("references", []):
                    for rprop in ref.get("snaks", {}):
                        ref_use[(prop, rprop)] += 1

    OUT.write_text(
        "#\tWhat each Garborg item holds, counted from the FULL downloaded items\n"
        "#\t(out/garborg-full-items.json, fetched 2026-08-24 via full_entities).\n"
        "#\n"
        "#\tThis replaces a version built from a summarising read, which truncated\n"
        "#\tQ467497 and could not see six of the fourteen at all. Every row here is\n"
        "#\tthe complete property and label set.\n"
        "#\n"
        "#\tThe batch builder consults this because the local store predates most of\n"
        "#\tthese items and Emma edits by hand.\n"
        + "qid\tverified\tlangs\tprops\n"
        + "".join(f"{r['qid']}\t{r['verified']}\t{r['langs']}\t{r['props']}\n"
                 for r in rows),
        encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(rows)} items, all complete\n")

    # -- which of our properties each item carries --------------------------
    hers = [q for q in data if q.startswith("Q1411")]
    print("Items Emma created (Q1411…):", len(hers))
    header = ["P31", "P21", "P2600", "P569", "P570", "P22", "P25", "P26", "P40",
              "P3373", "P735", "P734", "P5056"]
    print("             " + " ".join(f"{p:>6}" for p in header))
    for qid in ["Q467497", "Q3143008", "Q11959067"] + sorted(hers):
        claims = data[qid].get("claims", {})
        marks = " ".join(f"{('yes' if p in claims else '-'):>6}" for p in header)
        print(f"{qid:<12} {marks}")

    print("\nQualifiers actually used, by property:")
    if not qualifier_use:
        print("   none anywhere")
    for (prop, qprop), n in sorted(qualifier_use.items(), key=lambda kv: -kv[1]):
        if prop in OURS:
            print(f"   {prop} {OURS[prop]:<22} + {qprop}   ×{n}")

    print("\nReference properties used, by statement property:")
    for (prop, rprop), n in sorted(ref_use.items(), key=lambda kv: -kv[1]):
        if prop in OURS:
            print(f"   {prop} {OURS[prop]:<22} ref {rprop}   ×{n}")

    print("\nProperties we emit that appear on NONE of her items:")
    used = set()
    for qid in hers:
        used |= set(data[qid].get("claims", {}))
    for prop in OURS:
        if prop not in used:
            print(f"   {prop}  {OURS[prop]}")


if __name__ == "__main__":
    main()
