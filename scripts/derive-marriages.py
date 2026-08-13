"""Plan item 6 — marriage date, place and end, per family.

Emma, 2026-08-12: *"Marriage date and place and end and whatever will be
easy-ish."*

**"End" is measured rather than assumed.** The `FAM`-level tags in this corpus
are exactly: `CHIL` 267,517, `HUSB` 126,894, `WIFE` 89,543, `MARR` 36,314,
`DIV` 483, `NOTE` 73. There is no annulment, no engagement, no separation. So a
Geni marriage ends only by divorce, and only 483 times.

That matters for the conversion, because Wikidata's `P582` end time is recorded
far more often than that — a marriage ending at a death is an end Wikidata states
and Geni has no family-level way to express. This script counts the asymmetry
rather than glossing it.

`reports/marriages.csv` already holds the Wikidata comparison for the linked
subset; this is the derivation over **every** family, which is the ingestion
output the plan asks for.

Dates go through `genimerge.dates.parse_date`, never a regex.

Writes `reports/derived-marriages.csv` and `reports/marriage-derivation.md`.

    py scripts/derive-marriages.py
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from genimerge import dates, doubles  # noqa: E402

MERGED = REPO_ROOT / "out" / "merged.ged"
PAIRS = REPO_ROOT / "out" / "wikidata" / "p2600-all.tsv"
OUT_CSV = REPO_ROOT / "reports" / "derived-marriages.csv"
OUT_MD = REPO_ROOT / "reports" / "marriage-derivation.md"

EVENTS = {"MARR": "marriage", "DIV": "divorce"}


def main() -> int:
    qids: dict[str, str] = {}
    if PAIRS.exists():
        seen: dict[str, set[str]] = {}
        for qid, geni_id in doubles.load_pairs(PAIRS):
            seen.setdefault(geni_id, set()).add(qid)
        qids = {g: next(iter(q)) for g, q in seen.items() if len(q) == 1}

    rows: list[list] = []
    have: Counter[str] = Counter()
    unreadable: Counter[str] = Counter()

    current: dict | None = None
    event: str | None = None
    families = 0

    def flush() -> None:
        nonlocal current
        if current is None:
            return
        if not (current["events"] or current["husb"] or current["wife"]):
            current = None
            return
        # Only families that say something about a marriage are rows here.
        if not current["events"]:
            current = None
            return
        families_row = [current["id"]]
        husb, wife = current["husb"], current["wife"]
        families_row += [husb, qids.get(husb, "") if husb else "",
                         wife, qids.get(wife, "") if wife else ""]
        for tag, prefix in EVENTS.items():
            data = current["events"].get(tag, {})
            raw = data.get("date", "")
            fields = dates.date_fields(raw)
            if raw and not fields["year"]:
                unreadable[raw] += 1
            if raw:
                have[f"{prefix} date"] += 1
            if data.get("plac"):
                have[f"{prefix} place"] += 1
            if tag in current["events"]:
                have[prefix] += 1
            families_row += [fields[f] for f in dates.DATE_FIELDS]
            families_row.append(data.get("plac", ""))
        families_row.append(current["children"])
        both = bool(husb and wife)
        families_row.append("yes" if both else "no")
        families_row.append("yes" if (husb in qids and wife in qids) else "no")
        rows.append(families_row)
        current = None

    print(f"reading {MERGED}", flush=True)
    with open(MERGED, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.startswith("0 "):
                flush()
                current, event = None, None
                parts = line.split()
                if len(parts) >= 3 and parts[2] == "FAM" and parts[1].startswith("@F"):
                    families += 1
                    current = {"id": parts[1][2:-1], "husb": "", "wife": "",
                               "events": {}, "children": 0}
                continue
            if current is None:
                continue
            parts = line.rstrip("\n").split(None, 2)
            if len(parts) < 2:
                continue
            level, tag = parts[0], parts[1]
            value = parts[2].strip() if len(parts) > 2 else ""

            if level == "1":
                event = tag if tag in EVENTS else None
                if event:
                    current["events"].setdefault(event, {})
                elif tag in {"HUSB", "WIFE"} and value.startswith("@I"):
                    current["husb" if tag == "HUSB" else "wife"] = value[2:-1]
                elif tag == "CHIL":
                    current["children"] += 1
                continue
            if level == "2" and event:
                data = current["events"][event]
                if tag == "DATE" and value and "date" not in data:
                    data["date"] = value
                elif tag == "PLAC" and value and "plac" not in data:
                    data["plac"] = value
    flush()

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    columns = ["family", "husband", "husband_qid", "wife", "wife_qid"]
    for prefix in EVENTS.values():
        columns += [f"{prefix}_date_{f}" for f in dates.DATE_FIELDS]
        columns.append(f"{prefix}_place")
    columns += ["children", "both_spouses_named", "both_spouses_linked"]
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(columns)
        writer.writerows(rows)

    # Counted from the end, not by position: the date columns grew from 4 to 8
    # when `DATE_FIELDS` became canonical, and a fixed index silently read the
    # wrong column rather than failing.
    both_named = sum(1 for r in rows if r[-2] == "yes")
    both_linked = sum(1 for r in rows if r[-1] == "yes")
    divorced = have["divorce"]

    L: list[str] = []
    add = L.append
    add("# Marriage: date, place and end, derived")
    add("")
    add("Plan item 6. Emma, 2026-08-12: *\"Marriage date and place and end and whatever")
    add("will be easy-ish.\"*")
    add("")
    add(f"`reports/derived-marriages.csv` — **{len(rows):,} families** that say something")
    add(f"about a marriage, out of {families:,}.")
    add("")
    add("## \"End\" is divorce, and only divorce")
    add("")
    add("The `FAM`-level tags in this corpus are exactly:")
    add("")
    add("| tag | count |")
    add("| --- | ---: |")
    add("| `CHIL` | 267,517 |")
    add("| `HUSB` | 126,894 |")
    add("| `WIFE` | 89,543 |")
    add("| `MARR` | 36,314 |")
    add("| `DIV` | 483 |")
    add("| `NOTE` | 73 |")
    add("")
    add("**No annulment, no engagement, no separation.** A Geni marriage ends only by")
    add(f"divorce, and it does so **{divorced:,} times**.")
    add("")
    add("**This is the one field where the direction reverses.** Everywhere else in this")
    add("project Geni has more than Wikidata; here Wikidata's `P582` end time was")
    add("recorded on **257 of the 981** comparable marriages")
    add("(`reports/marriages.md`), because a marriage ending at a death is an end")
    add("Wikidata states and Geni has no family-level way to express. Deriving \"end\"")
    add("from Geni therefore supplies almost nothing.")
    add("")
    add("## What is present")
    add("")
    add("| | families | share of rows |")
    add("| --- | ---: | ---: |")
    for prefix in EVENTS.values():
        for kind in ("date", "place"):
            n = have[f"{prefix} {kind}"]
            add(f"| {prefix} {kind} | {n:,} | {100.0*n/max(len(rows),1):.1f}% |")
    add(f"| both spouses named | {both_named:,} | {100.0*both_named/max(len(rows),1):.1f}% |")
    add(f"| both spouses carry a Wikidata item | {both_linked:,} | "
        f"{100.0*both_linked/max(len(rows),1):.1f}% |")
    add("")
    add("**A marriage is only emittable when both spouses exist on Wikidata**, since")
    add("`P26` needs something to point at. That is the last row, and it is the real")
    add("size of what item 6 can currently produce.")
    add("")
    if unreadable:
        add("## Dates the grammar could not read")
        add("")
        add(f"{sum(unreadable.values()):,} values, {len(unreadable):,} distinct. Raw text")
        add("kept rather than dropped.")
        add("")
        add("| raw | times |")
        add("| --- | ---: |")
        for raw, n in unreadable.most_common(10):
            add(f"| `{raw}` | {n:,} |")
        add("")
    add("## Not done here")
    add("")
    add("- **No `P26` shape chosen.** Emma asked to see cases before deciding and")
    add("  `reports/marriages.md` holds them; this is the derivation, not the mapping.")
    add("- **No place resolved to an item.**")
    add("- **The 30 families where Wikidata names a different spouse are untouched** —")
    add("  Christian IV's mistress is among them, so they are not gaps.")

    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {OUT_CSV} ({len(rows):,} rows)")
    print(f"wrote {OUT_MD}")
    print()
    for prefix in EVENTS.values():
        print(f"  {prefix:<9} {have[prefix]:>7,}   date {have[f'{prefix} date']:>7,}"
              f"   place {have[f'{prefix} place']:>7,}")
    print(f"  both spouses named  {both_named:,}")
    print(f"  both spouses linked {both_linked:,}")
    print(f"  {sum(unreadable.values()):,} unreadable date values")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
