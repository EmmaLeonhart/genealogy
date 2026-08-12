"""Plan items 3 and 4 — occupation, and the dates and places, per person.

Emma, 2026-08-12: *"Occupation can be done with string stuff"* and *"Birthplace
birth date death date death place burial date burial place all can be done with
string."*

They come off the same `INDI` record, so this is one pass.

**Rules already settled, applied here:**

* **`PLAC` only; `ADDR` is ignored.** Her decision of 2026-08-11, chosen over
  "use ADDR when PLAC is absent". The structured block is dropped even where it
  is the better-filled of the two — recorded because it is a real loss, counted
  below rather than left implicit.
* **Dates go through `genimerge.dates.parse_date`, never a regex.** The corpus
  writes BC years as a minus and two hand-rolled parsers have already silently
  dropped all 4,750 of them. Anything the grammar does not recognise keeps its
  raw text and reports no year.
* **Burial is two properties**, `P119` place and `P4602` date, not qualifiers —
  so the two are carried separately rather than as one event.

**Nothing is emitted to Wikidata.** This is ingestion: the derived values land in
a CSV beside the Geni ID and, where there is one, the QID.

Writes `reports/derived-facts.csv` and `reports/facts.md`.

    py scripts/derive-facts.py
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
OUT_CSV = REPO_ROOT / "reports" / "derived-facts.csv"
OUT_MD = REPO_ROOT / "reports" / "facts.md"

#: The events this pass carries, and the column prefix each gets.
EVENTS = {"BIRT": "birth", "DEAT": "death", "BURI": "burial"}

COLUMNS = ["geni_id", "qid", "sex", "occupations"]
for _prefix in EVENTS.values():
    COLUMNS += [f"{_prefix}_date_raw", f"{_prefix}_year", f"{_prefix}_modifier",
                f"{_prefix}_place"]
COLUMNS += ["addr_dropped"]


def main() -> int:
    qids: dict[str, str] = {}
    if PAIRS.exists():
        seen: dict[str, set[str]] = {}
        for qid, geni_id in doubles.load_pairs(PAIRS):
            seen.setdefault(geni_id, set()).add(qid)
        qids = {g: next(iter(q)) for g, q in seen.items() if len(q) == 1}
    print(f"{len(qids):,} unambiguous Geni->Wikidata links", flush=True)

    rows: list[list] = []
    have = Counter()
    unreadable_dates = Counter()
    addr_without_plac = 0
    people = 0

    current: dict | None = None
    event: str | None = None

    def flush() -> None:
        nonlocal current
        if current is None:
            return
        row = [current["id"], qids.get(current["id"], ""), current["sex"],
               " | ".join(current["occu"])]
        for tag, prefix in EVENTS.items():
            data = current["events"].get(tag, {})
            raw = data.get("date", "")
            parsed = dates.parse_date(raw) if raw else None
            year = "" if parsed is None or parsed.year is None else str(parsed.year)
            if raw and not year:
                unreadable_dates[raw] += 1
            place = data.get("plac", "")
            if raw:
                have[f"{prefix} date"] += 1
            if place:
                have[f"{prefix} place"] += 1
            row += [raw, year, (parsed.modifier or "") if parsed else "", place]
        row.append(current["addr_dropped"])
        rows.append(row)

    print(f"reading {MERGED}", flush=True)
    with open(MERGED, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.startswith("0 "):
                flush()
                current = None
                event = None
                parts = line.split()
                if len(parts) >= 3 and parts[2] == "INDI":
                    xref = parts[1]
                    if xref.startswith("@I") and xref.endswith("@"):
                        people += 1
                        current = {"id": xref[2:-1], "sex": "", "occu": [],
                                   "events": {}, "addr_dropped": 0}
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
                elif tag == "SEX" and value:
                    current["sex"] = value
                elif tag == "OCCU" and value:
                    if value not in current["occu"]:
                        current["occu"].append(value)
                continue

            if level == "2" and event:
                data = current["events"][event]
                if tag == "DATE" and value and "date" not in data:
                    data["date"] = value
                elif tag == "PLAC" and value and "plac" not in data:
                    data["plac"] = value
                elif tag == "ADDR":
                    # Emma's rule: PLAC only. Counted, not used.
                    current["addr_dropped"] += 1
                    if "plac" not in data:
                        addr_without_plac += 1
    flush()

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(COLUMNS)
        writer.writerows(rows)

    with_occu = sum(1 for r in rows if r[3])
    with_sex = sum(1 for r in rows if r[2])
    linked = sum(1 for r in rows if r[1])

    L: list[str] = []
    add = L.append
    add("# Derived facts: occupation, dates, places")
    add("")
    add("Plan items 3 and 4. Emma, 2026-08-12: *\"Occupation can be done with string")
    add("stuff\"* and *\"Birthplace birth date death date death place burial date burial")
    add("place all can be done with string.\"*")
    add("")
    add(f"One row per person in `reports/derived-facts.csv` — **{len(rows):,} people**, ")
    add(f"of whom {linked:,} carry a Wikidata item.")
    add("")
    add("## What is actually present")
    add("")
    add("| field | people | share |")
    add("| --- | ---: | ---: |")
    add(f"| sex | {with_sex:,} | {100.0*with_sex/max(len(rows),1):.1f}% |")
    add(f"| occupation | {with_occu:,} | {100.0*with_occu/max(len(rows),1):.1f}% |")
    for prefix in EVENTS.values():
        for kind in ("date", "place"):
            n = have[f"{prefix} {kind}"]
            add(f"| {prefix} {kind} | {n:,} | {100.0*n/max(len(rows),1):.1f}% |")
    add("")
    add("## The cost of `PLAC` only")
    add("")
    add("Emma chose *ignore `ADDR`, use `PLAC` only* on 2026-08-11. That is applied here,")
    add("and the loss is counted rather than left implicit:")
    add("")
    places_kept = sum(have[f"{p} place"] for p in EVENTS.values())
    add(f"**{addr_without_plac:,} events carry an `ADDR` block and no `PLAC` at all**, "
        f"against **{places_kept:,}** events where `PLAC` supplied a place.")
    add("")
    add("So the rule is not costing precision on those events — it is costing the place")
    add(f"entirely, and it applies to {100.0*addr_without_plac/max(addr_without_plac+places_kept,1):.0f}% "
        "of the events that have any location information at all.")
    add("")
    add("**The rule stands; this is the size of it.** It was chosen over *\"use `ADDR`")
    add("only when `PLAC` is absent\"*, which is exactly the population counted here —")
    add("that alternative would roughly double the places available and never override a")
    add("`PLAC`. Recorded so the choice is re-openable on a number rather than on a")
    add("recollection.")
    add("")
    add("## Dates the grammar could not read")
    add("")
    if unreadable_dates:
        add(f"**{sum(unreadable_dates.values()):,} date values**, "
            f"{len(unreadable_dates):,} distinct, parsed to no year. They keep their raw")
        add("text in the CSV rather than being dropped — a date we cannot read must not")
        add("become a date we guessed.")
        add("")
        add("| raw value | times |")
        add("| --- | ---: |")
        for raw, n in unreadable_dates.most_common(15):
            add(f"| `{raw}` | {n:,} |")
    else:
        add("None.")
    add("")
    add("`reports/impossible-years.md` has the full account of these: bare modifiers with")
    add("no operand, and cosmological years in the hundreds of millions belonging to")
    add("Shinto creation deities.")
    add("")
    add("## Not done here")
    add("")
    add("- **No place string is resolved to a Wikidata item.** Geni gives a comma-chain,")
    add("  Wikidata gives one item at one level of nesting, and which level a string")
    add("  resolves to is undecided — `PLAC Anda` against `P19 = Klepp Municipality`.")
    add("- **No occupation string is resolved to an item** either.")
    add("- **Nothing is emitted.** This is ingestion.")

    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {OUT_CSV} ({len(rows):,} rows)")
    print(f"wrote {OUT_MD}")
    print()
    print(f"  sex {with_sex:,}   occupation {with_occu:,}")
    for prefix in EVENTS.values():
        print(f"  {prefix:<8} date {have[f'{prefix} date']:>7,}   place {have[f'{prefix} place']:>7,}")
    print(f"  {addr_without_plac:,} events have an ADDR block and no PLAC")
    print(f"  {sum(unreadable_dates.values()):,} unreadable date values")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
