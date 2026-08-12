"""Every DATE line in the corpus whose year cannot be right.

Emma, 2026-08-11, on the five pharaohs whose BCE minus sign is missing and whose
birth years therefore read as later than today: **"Fix them in the fucking
data."**

Before fixing anything, census every instance — the CLAUDE.md rule, and in this
case also the only way to know *which export files* carry the lines, since a fix
has to land somewhere specific.

**Dates are parsed by `genimerge.dates.parse_date`, never by hand.** That module
exists because two hand-rolled parsers have already silently dropped all 4,750
negative-year lines in this corpus; `"-73".isdigit()` is `False`.

Scanned over `exports/` rather than `out/merged.ged`, because the merged file is
generated and a correction has to be made where the data actually lives.

Writes `reports/impossible-years.csv`, one row per offending DATE line.

    py scripts/build-impossible-years-census.py
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from genimerge import dates, identity, sources  # noqa: E402

OUTPUT = REPO_ROOT / "reports" / "impossible-years.csv"

#: A birth or death later than today cannot be right. Taken from the clock rather
#: than hardcoded, so the screen does not rot.
THIS_YEAR = date.today().year

COLUMNS = [
    "export",
    "line_number",
    "record_xref",
    "geni_id",
    "record_type",
    "event_tag",
    "raw_date",
    "parsed_year",
    "modifier",
    "reason",
    "name",
]


def main() -> int:
    exports = sources.find_exports()
    print(f"{len(exports)} distinct exports", flush=True)

    rows: list[list] = []
    reasons: Counter[str] = Counter()
    total_dates = 0
    unparsed = 0

    for path in exports:
        xref = ""
        record_type = ""
        geni_id = ""
        name = ""
        event_tag = ""
        with open(path, encoding="utf-8", errors="replace") as handle:
            for number, line in enumerate(handle, 1):
                if line.startswith("0 "):
                    parts = line.split()
                    xref = parts[1] if len(parts) >= 2 else ""
                    record_type = parts[2] if len(parts) >= 3 else ""
                    name = ""
                    event_tag = ""
                    geni_id = ""
                    if xref.startswith("@") and xref.endswith("@"):
                        match = identity.GENI_ID_RE.match(xref)
                        if match:
                            geni_id = match.group("geni_id")
                    continue
                if line.startswith("1 "):
                    event_tag = line[2:].split(None, 1)[0].strip()
                    if event_tag == "NAME":
                        name = line[6:].strip()
                    continue
                stripped = line.rstrip("\n")
                if not stripped.startswith("2 DATE "):
                    continue

                total_dates += 1
                raw = stripped[7:].strip()
                parsed = dates.parse_date(raw)
                if parsed is None or parsed.year is None:
                    # A date we cannot read is a finding about the corpus, not
                    # something to widen a pattern until it swallows. Recorded
                    # with its raw text rather than counted and dropped.
                    unparsed += 1
                    reasons["unreadable"] += 1
                    rows.append(
                        [
                            path.relative_to(REPO_ROOT).as_posix(),
                            number,
                            xref,
                            geni_id,
                            record_type,
                            event_tag,
                            raw,
                            "",
                            "",
                            "unreadable",
                            name,
                        ]
                    )
                    continue

                year = parsed.year
                reason = ""
                if year > THIS_YEAR:
                    reason = f"later than {THIS_YEAR}"
                elif year == 0:
                    # There is no year zero in the proleptic Julian calendar and
                    # GEDCOM has no way to write one; if it appears it is a
                    # parsing or data artefact worth seeing.
                    reason = "year zero"
                if not reason:
                    continue

                reasons[reason] += 1
                rows.append(
                    [
                        path.relative_to(REPO_ROOT).as_posix(),
                        number,
                        xref,
                        geni_id,
                        record_type,
                        event_tag,
                        raw,
                        year,
                        parsed.modifier or "",
                        reason,
                        name,
                    ]
                )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(COLUMNS)
        writer.writerows(sorted(rows, key=lambda r: (r[3], r[0], r[1])))

    people = {r[3] for r in rows if r[3]}
    print(f"{total_dates:,} DATE lines read, {unparsed:,} with no readable year")
    print(f"wrote {OUTPUT} — {len(rows):,} rows over {len(people):,} distinct people")
    print(f"reasons: {dict(reasons)}")
    print(f"export files affected: {len({r[0] for r in rows})}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
