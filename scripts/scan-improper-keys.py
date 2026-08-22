"""Census every INDI record in the corpus whose *key* is not a proper Geni ID.

The Geni profile ID is this repo's primary key, and it is written twice on
every individual: once as the GEDCOM xref (`0 @I6000000087535357291@ INDI`)
and once as `1 RFN geni:6000000087535357291`. This script finds every INDI
where that pair does not hold up, and every *pointer* to an individual whose
target xref is not a readable Geni ID.

It is a line scan rather than a parse: at 531 files and 3.7 GB the full
parser is minutes of work for information that lives on two line shapes.
RFN is always level 1 under INDI in Geni's output, which is what makes the
scan exact rather than approximate.

Output: reports/improper-keys.csv, one row per finding.
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from genimerge.identity import GENI_ID_RE, RFN_PREFIX  # noqa: E402
from genimerge.sources import REPO_ROOT, find_exports  # noqa: E402

#: Every Geni profile ID seen in the corpus so far is 19 digits opening
#: `6000000`. That is an observation about Geni's ID allocation, not a
#: documented format, so a departure is reported and never rejected.
CANONICAL_ID = re.compile(r"^6000000\d{12}$")

LEVEL0 = re.compile(r"^0\s+(?P<xref>@[^@\s]+@)\s+(?P<tag>[A-Za-z0-9_]+)\s*$")
LEVEL1 = re.compile(r"^1\s+(?P<tag>[A-Za-z0-9_]+)(?:\s(?P<value>.*))?$")
POINTER = re.compile(r"^\d+\s+(?P<tag>[A-Za-z0-9_]+)\s+(?P<ptr>@[^@\s]+@)\s*$")

#: Level-1 tags whose value points at an individual.
INDI_POINTER_TAGS = {"CHIL", "HUSB", "WIFE", "ASSO", "ALIA", "SUBM"}


def flush(path, xref, rfns, names, out):
    """Judge one finished INDI record and append any findings to `out`."""
    match = GENI_ID_RE.match(xref or "")
    from_xref = match["geni_id"] if match else None
    kind = match["kind"] if match else None
    name = names[0] if names else ""

    geni_rfns = [r[len(RFN_PREFIX):].strip() for r in rfns if r.startswith(RFN_PREFIX)]
    other_rfns = [r for r in rfns if not r.startswith(RFN_PREFIX)]
    from_rfn = geni_rfns[0] if geni_rfns else None

    def add(kind_, detail):
        out.append(
            {
                "fault": kind_,
                "geni_id": from_xref or from_rfn or "",
                "xref": xref or "",
                "rfn": "; ".join(rfns),
                "name": name,
                "export": path,
                "detail": detail,
            }
        )

    if match is None:
        add("xref-unreadable",
            "xref is not @[IFNS]<digits>@, so no Geni ID can be read from it")
    elif kind != "I":
        add("xref-wrong-record-letter",
            f"INDI record carries the {kind!r} letter, which belongs to another record type")

    if not rfns:
        add("rfn-absent", "INDI carries no RFN line to corroborate the xref")
    if other_rfns:
        add("rfn-not-geni",
            f"RFN does not start with {RFN_PREFIX!r}: {other_rfns[0]!r}")
    if len(geni_rfns) > 1:
        add("rfn-repeated", f"{len(geni_rfns)} geni: RFN lines on one record")
    if geni_rfns and not geni_rfns[0]:
        add("rfn-empty", "RFN says geni: with no ID after it")

    if from_xref and from_rfn and from_xref != from_rfn:
        add("xref-rfn-mismatch",
            f"xref says {from_xref} but RFN says {from_rfn}")

    for value, source in ((from_xref, "xref"), (from_rfn, "RFN")):
        if value and not CANONICAL_ID.match(value):
            add("non-canonical-shape",
                f"{source} ID {value!r} is not 19 digits opening 6000000 — a legacy "
                f"allocation rather than a broken key; see reports/improper-keys.html")


def main() -> None:
    exports = find_exports()
    findings: list[dict] = []
    pointer_faults: dict[tuple[str, str], Counter] = defaultdict(Counter)
    indi_total = 0
    declared: dict[str, set[str]] = defaultdict(set)

    for n, path in enumerate(exports, 1):
        rel = str(path.relative_to(REPO_ROOT))
        print(f"[{n}/{len(exports)}] {rel}", file=sys.stderr)
        xref = tag = None
        rfns: list[str] = []
        names: list[str] = []
        with path.open(encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.rstrip("\r\n")
                head = LEVEL0.match(line)
                if head:
                    if tag == "INDI":
                        indi_total += 1
                        flush(rel, xref, rfns, names, findings)
                    xref, tag = head["xref"], head["tag"]
                    declared[rel].add(xref)
                    rfns, names = [], []
                    continue
                if line[:1] == "0":
                    if tag == "INDI":
                        indi_total += 1
                        flush(rel, xref, rfns, names, findings)
                    xref, tag = None, None
                    continue
                if tag == "INDI":
                    one = LEVEL1.match(line)
                    if one:
                        if one["tag"] == "RFN":
                            rfns.append((one["value"] or "").strip())
                        elif one["tag"] == "NAME":
                            names.append((one["value"] or "").strip())
                ptr = POINTER.match(line)
                if ptr and ptr["tag"] in INDI_POINTER_TAGS:
                    target = ptr["ptr"]
                    if not GENI_ID_RE.match(target):
                        pointer_faults[(rel, target)][ptr["tag"]] += 1
        if tag == "INDI":
            indi_total += 1
            flush(rel, xref, rfns, names, findings)

    for (rel, target), tags in sorted(pointer_faults.items()):
        findings.append(
            {
                "fault": "pointer-unreadable",
                "geni_id": "",
                "xref": target,
                "rfn": "",
                "name": "",
                "export": rel,
                "detail": "pointed at as an individual by "
                + ", ".join(f"{t}×{c}" for t, c in sorted(tags.items()))
                + (" — no such record in this file"
                   if target not in declared[rel] else " — record exists"),
            }
        )

    out = REPO_ROOT / "reports" / "improper-keys.csv"
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(
            fh, ["fault", "geni_id", "xref", "rfn", "name", "export", "detail"]
        )
        w.writeheader()
        w.writerows(findings)

    print(f"\nINDI records scanned: {indi_total:,}", file=sys.stderr)
    print(f"exports: {len(exports)}", file=sys.stderr)
    for fault, count in Counter(f["fault"] for f in findings).most_common():
        print(f"  {fault:26} {count:,}", file=sys.stderr)
    print(f"wrote {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
