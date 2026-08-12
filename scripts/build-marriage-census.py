"""Marriages, both sides — the cases Emma asked for before any P26 shape is chosen.

Emma, 2026-08-10: **"Marriage mapping: not decided. Show me marriage cases
first."** Walk more `FAM` records before choosing any `P26`-qualifier shape.

Still unfulfilled a day later, so this is it. Nothing here proposes a mapping.

**Qualifiers are read, not just the value.** `CLAUDE.md` records the Henry III
case: his `P26` mainsnak is bare `Q228885`, and the marriage date, place, end
date, end cause and four references all hang off it as qualifiers. A pass that
read mainsnaks only reported that Wikidata held nothing when it held the answer.
So this reads the whole statement.

Writes `reports/marriages.csv`, one row per Geni `FAM` carrying a marriage event
where both spouses are identified. For the subset where both spouses also carry a
Wikidata item, it records what Wikidata's `P26` says — including whether the
statement exists at all.

Offline throughout.

    py scripts/build-marriage-census.py
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from genimerge import doubles, gedcom, model, wikistore  # noqa: E402

MERGED = REPO_ROOT / "out" / "merged.ged"
PAIRS = REPO_ROOT / "out" / "wikidata" / "p2600-all.tsv"
STORE = REPO_ROOT / "wikidata" / "items"
INDEX = REPO_ROOT / "out" / "wikidata" / "store-index.sqlite3"
OUTPUT = REPO_ROOT / "reports" / "marriages.csv"

#: The qualifiers a marriage statement can carry, and what each is. Taken from
#: the Henry III statement in CLAUDE.md rather than invented.
MARRIAGE_QUALIFIERS = {
    "P580": "start time",
    "P582": "end time",
    "P2842": "place of marriage",
    "P1534": "end cause",
    "P1545": "series ordinal",
}


def snak_value(snak: dict) -> str:
    kind = snak.get("snaktype")
    if kind == "somevalue":
        return "SOME VALUE"
    if kind == "novalue":
        return "NO VALUE"
    value = (snak.get("datavalue") or {}).get("value")
    if isinstance(value, dict):
        if "id" in value:
            return value["id"]
        if "time" in value:
            precision = value.get("precision")
            return f"{value.get('time','')}/p{precision}"
        if "text" in value:
            return value["text"]
    return str(value) if value is not None else ""


def main() -> int:
    print(f"loading {MERGED}", flush=True)
    tree = model.build_tree(gedcom.stream_file(MERGED))
    print(f"{len(tree.people):,} people, {len(tree.families):,} families", flush=True)

    qids_for: dict[str, set[str]] = {}
    for qid, geni_id in doubles.load_pairs(PAIRS):
        if geni_id in tree.people:
            qids_for.setdefault(geni_id, set()).add(qid)
    linked = {g: next(iter(q)) for g, q in qids_for.items() if len(q) == 1}
    print(f"{len(linked):,} linked people", flush=True)

    # Only families where both spouses are named are comparable at all: with no
    # spouse there is no P26 to qualify, which Emma already settled about the
    # 16,229 spouse-less dated families.
    candidates = []
    for family in tree.families.values():
        if not (family.husband_id and family.wife_id):
            continue
        if family.marriage is None:
            continue
        candidates.append(family)
    print(f"{len(candidates):,} families with both spouses and a marriage event", flush=True)

    wanted = {
        linked[f.husband_id]
        for f in candidates
        if f.husband_id in linked and f.wife_id in linked
    }
    print(f"{len(wanted):,} husband items to read", flush=True)
    with wikistore.StoreReader(STORE, INDEX) as reader:
        entities = reader.entities(sorted(wanted))
    print(f"{len(entities):,} returned", flush=True)

    rows = []
    verdicts: Counter[str] = Counter()
    qualifier_use: Counter[str] = Counter()
    both_linked = 0

    for family in candidates:
        husband = tree.people.get(family.husband_id)
        wife = tree.people.get(family.wife_id)
        marriage = family.marriage
        date = marriage.date if marriage else None

        hq = linked.get(family.husband_id, "")
        wq = linked.get(family.wife_id, "")
        verdict = "not comparable — a spouse has no item"
        quals: dict[str, str] = {}
        refs = 0

        if hq and wq:
            both_linked += 1
            entity = entities.get(hq)
            if entity is None:
                verdict = "husband item not in the store"
            else:
                statements = (entity.get("claims") or {}).get("P26") or []
                match = None
                for statement in statements:
                    if snak_value(statement.get("mainsnak") or {}) == wq:
                        match = statement
                        break
                if match is None:
                    verdict = (
                        "Wikidata states no P26 to this spouse"
                        if statements
                        else "Wikidata states no P26 at all"
                    )
                else:
                    for prop, snaks in (match.get("qualifiers") or {}).items():
                        if prop in MARRIAGE_QUALIFIERS:
                            quals[prop] = "; ".join(snak_value(s) for s in snaks)
                            qualifier_use[prop] += 1
                    refs = len(match.get("references") or [])
                    verdict = "P26 present, with qualifiers" if quals else "P26 present, bare"
        verdicts[verdict] += 1

        rows.append(
            [
                family.geni_id,
                family.husband_id,
                husband.display_name if husband else "",
                hq,
                family.wife_id,
                wife.display_name if wife else "",
                wq,
                date.raw if date else "",
                date.year if date else "",
                date.modifier if date else "",
                marriage.where or "" if marriage else "",
                len(family.child_ids),
                verdict,
                quals.get("P580", ""),
                quals.get("P582", ""),
                quals.get("P2842", ""),
                quals.get("P1534", ""),
                quals.get("P1545", ""),
                refs,
            ]
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "family", "husband", "husband_name", "husband_qid",
                "wife", "wife_name", "wife_qid",
                "geni_marriage_date", "geni_marriage_year", "geni_date_modifier",
                "geni_marriage_place", "children", "verdict",
                "wd_start_time", "wd_end_time", "wd_place_of_marriage",
                "wd_end_cause", "wd_series_ordinal", "wd_reference_count",
            ]
        )
        writer.writerows(rows)

    print(f"\nwrote {OUTPUT} — {len(rows):,} rows")
    print(f"{both_linked:,} have both spouses carrying a Wikidata item\n")
    for verdict, n in verdicts.most_common():
        print(f"  {n:>7,}  {verdict}")
    print("\nqualifiers used, where P26 exists:")
    for prop, n in qualifier_use.most_common():
        print(f"  {prop} {MARRIAGE_QUALIFIERS[prop]:<20} {n:,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
