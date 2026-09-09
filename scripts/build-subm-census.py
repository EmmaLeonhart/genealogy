"""Every SUBM record and every reference to one, so we can say what SUBM is.

Emma parked `SUBM` on 2026-08-11 — *"may theoretically exist, may theoretically
be useful. I have no idea how it's going to be useful"* — then unparked it the
same day with *"agentic RAG to figure it out"*.

Looking at the records first: they carry a person's name, and occasionally a
postal address. So the hypothesis is that a `SUBM` is the Geni **user** who
manages the profile.

**The decisive test is in the xrefs.** They come in two shapes — `@S2043333@` and
`@S6000000002973566792@` — which are exactly the two shapes Geni profile IDs come
in. If a `SUBM` id also occurs as an `INDI` id, then a manager is a profile in
the same namespace and `SUBM` is a link into the tree rather than an opaque
label. This counts that rather than assuming it either way.

Writes `reports/subm-census.csv`, one row per distinct SUBM. Offline; reads only
the merged GEDCOM.

    py scripts/build-subm-census.py
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MERGED = REPO_ROOT / "out" / "merged.ged"
OUTPUT = REPO_ROOT / "reports" / "subm-census.csv"

COLUMNS = [
    "subm_xref",
    "subm_id",
    "id_shape",
    "name",
    "addr_city",
    "addr_stae",
    "addr_post",
    "addr_ctry",
    "other_subtags",
    "referenced_by_indi",
    "referenced_by_head",
    "id_also_an_indi",
]


def main() -> int:
    records: dict[str, dict[str, str]] = {}
    order: list[str] = []
    indi_ids: set[str] = set()
    refs: Counter[str] = Counter()
    head_refs: Counter[str] = Counter()

    current_subm: str | None = None
    in_addr = False
    in_head = False
    total_lines = 0

    print(f"reading {MERGED}", flush=True)
    with open(MERGED, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            total_lines += 1
            if line.startswith("0 "):
                current_subm = None
                in_addr = False
                parts = line.split()
                in_head = len(parts) >= 2 and parts[1] == "HEAD"
                if len(parts) >= 3 and parts[2] == "SUBM":
                    xref = parts[1]
                    current_subm = xref
                    if xref not in records:
                        records[xref] = {"subm_xref": xref}
                        order.append(xref)
                elif len(parts) >= 3 and parts[2] == "INDI":
                    xref = parts[1]
                    if xref.startswith("@I") and xref.endswith("@"):
                        indi_ids.add(xref[2:-1])
                continue

            # A reference to a submitter, from anywhere.
            stripped = line.rstrip("\n")
            if " SUBM " in stripped or stripped.endswith(" SUBM"):
                parts = stripped.split()
                if len(parts) >= 3 and parts[1] == "SUBM" and parts[2].startswith("@S"):
                    (head_refs if in_head else refs)[parts[2]] += 1
                    continue

            if current_subm is None:
                continue
            record = records[current_subm]
            parts = line.rstrip("\n").split(None, 2)
            if not parts:
                continue
            if parts[0] == "1":
                in_addr = parts[1] == "ADDR"
                tag, value = parts[1], (parts[2] if len(parts) > 2 else "")
                if tag == "NAME":
                    record["name"] = value
                elif tag != "ADDR":
                    record["other_subtags"] = (
                        record.get("other_subtags", "") + ("+" if record.get("other_subtags") else "") + tag
                    )
            elif parts[0] == "2" and in_addr:
                tag, value = parts[1], (parts[2] if len(parts) > 2 else "")
                if tag in {"CITY", "STAE", "POST", "CTRY"}:
                    record[f"addr_{tag.lower()}"] = value

    print(f"{total_lines:,} lines, {len(records):,} distinct SUBM records", flush=True)
    print(f"{len(indi_ids):,} INDI ids", flush=True)

    shared = 0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(COLUMNS)
        for xref in order:
            record = records[xref]
            ident = xref[2:-1] if xref.startswith("@S") and xref.endswith("@") else ""
            also = ident in indi_ids
            shared += also
            writer.writerow(
                [
                    xref,
                    ident,
                    "long" if len(ident) > 12 else "short",
                    record.get("name", ""),
                    record.get("addr_city", ""),
                    record.get("addr_stae", ""),
                    record.get("addr_post", ""),
                    record.get("addr_ctry", ""),
                    record.get("other_subtags", ""),
                    refs.get(xref, 0),
                    head_refs.get(xref, 0),
                    "yes" if also else "no",
                ]
            )

    with_addr = sum(1 for r in records.values() if any(k.startswith("addr_") for k in r))
    referenced = sum(1 for x in records if refs.get(x))
    print(f"wrote {OUTPUT}")
    print(f"  {with_addr:,} carry a postal address")
    print(f"  {referenced:,} are referenced by at least one INDI")
    print(f"  {sum(refs.values()):,} INDI references in total")
    print(f"  {sum(head_refs.values()):,} HEAD references")
    print(f"  {shared:,} SUBM ids also occur as an INDI id")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
