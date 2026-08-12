"""Find people whose Geni record AND Wikidata item are both small.

Emma, 2026-08-11: *"find an example of something that has a Wikidata item and a
Geni item that are both pretty small and are connected to each other, and then go
through the data structure of both of them so we can actually establish stuff."*

The point is to look at two whole records side by side without either being so
large that the structure disappears into the volume. Henry III is 2,686 lines;
nothing can be established from that.

Offline only. The Geni side is scanned straight out of the merged GEDCOM; the
Wikidata side comes from the downloaded store. Nothing here queries anything.

Usage:
    py scripts/find-small-pair.py                 # rank candidates
    py scripts/find-small-pair.py --dump GENI_ID  # print both records whole
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from genimerge import wikistore  # noqa: E402

MERGED = REPO_ROOT / "out" / "merged.ged"
PAIRS = REPO_ROOT / "out" / "wikidata" / "p2600-all.tsv"
STORE = REPO_ROOT / "wikidata" / "items"
INDEX = REPO_ROOT / "out" / "wikidata" / "store-index.sqlite3"


def read_pairs() -> dict[str, str]:
    """geni_id -> qid, skipping any Geni ID that sits on more than one item.

    `p2600-all.tsv` is ``qid<TAB>geni_id`` with no header — the opposite column
    order from `p2600-map.tsv`, and crossing them fails silently, so the first
    token is asserted to start with Q rather than trusted from the path.
    """
    qids_for: dict[str, set[str]] = {}
    with open(PAIRS, encoding="utf-8") as handle:
        first = True
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) != 2:
                continue
            qid, geni_id = parts
            if first:
                if not qid.startswith("Q"):
                    raise SystemExit(f"{PAIRS}: first column is not a QID ({qid!r})")
                first = False
            qids_for.setdefault(geni_id, set()).add(qid)
    return {g: next(iter(q)) for g, q in qids_for.items() if len(q) == 1}


#: Tags whose presence says the record has something in it worth reading. Kept
#: as a count per record rather than a boolean so a record can be screened on
#: "has a date AND a place" without a second pass over 450 MB.
INTERESTING_TAGS = ("BIRT", "DEAT", "BURI", "DATE", "PLAC", "ADDR", "NAME", "OCCU", "FAMC", "FAMS")

SCAN_CACHE = REPO_ROOT / "out" / "small-pair-scan.tsv"


def scan_gedcom(wanted: set[str]) -> dict[str, dict[str, int]]:
    """Per INDI record whose Geni ID is in ``wanted``: line count and tag counts.

    One pass over the merged GEDCOM, cached to ``out/small-pair-scan.tsv``,
    because the file is 450 MB and picking a second example should not cost a
    second read of it. Delete the cache after a re-merge.
    """
    if SCAN_CACHE.exists():
        out: dict[str, dict[str, int]] = {}
        with open(SCAN_CACHE, encoding="utf-8") as handle:
            header = handle.readline().rstrip("\n").split("\t")
            for line in handle:
                cells = line.rstrip("\n").split("\t")
                row = dict(zip(header[1:], (int(c) for c in cells[1:])))
                out[cells[0]] = row
        print(f"scan cache: {len(out):,} records ({SCAN_CACHE})", file=sys.stderr)
        return out

    counts: dict[str, dict[str, int]] = {}
    current: str | None = None
    row: dict[str, int] = {}
    with open(MERGED, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.startswith("0 "):
                if current is not None:
                    counts[current] = row
                current = None
                row = {}
                parts = line.split()
                if len(parts) >= 3 and parts[2] == "INDI":
                    xref = parts[1]
                    if xref.startswith("@I") and xref.endswith("@"):
                        geni_id = xref[2:-1]
                        if geni_id in wanted:
                            current = geni_id
                            row = {"lines": 0, **{t: 0 for t in INTERESTING_TAGS}}
            if current is not None:
                row["lines"] += 1
                parts = line.split(None, 2)
                if len(parts) >= 2 and parts[1] in row:
                    row[parts[1]] += 1
    if current is not None:
        counts[current] = row

    SCAN_CACHE.parent.mkdir(parents=True, exist_ok=True)
    columns = ["lines", *INTERESTING_TAGS]
    with open(SCAN_CACHE, "w", encoding="utf-8") as handle:
        handle.write("geni_id\t" + "\t".join(columns) + "\n")
        for geni_id, row in counts.items():
            handle.write(geni_id + "\t" + "\t".join(str(row[c]) for c in columns) + "\n")
    print(f"wrote scan cache {SCAN_CACHE}", file=sys.stderr)
    return counts


def statement_count(entity: dict) -> tuple[int, int]:
    """(properties, statements) on a stored item."""
    claims = entity.get("claims") or {}
    return len(claims), sum(len(v) for v in claims.values())


def extract_record(geni_id: str) -> list[str]:
    """The raw lines of one INDI record, verbatim."""
    target = f"@I{geni_id}@"
    out: list[str] = []
    grabbing = False
    with open(MERGED, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.startswith("0 "):
                if grabbing:
                    break
                parts = line.split()
                grabbing = len(parts) >= 3 and parts[1] == target and parts[2] == "INDI"
            if grabbing:
                out.append(line.rstrip("\n"))
    return out


def extract_families(xrefs: set[str]) -> dict[str, list[str]]:
    """The raw lines of the named FAM records."""
    out: dict[str, list[str]] = {}
    current: str | None = None
    with open(MERGED, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.startswith("0 "):
                current = None
                parts = line.split()
                if len(parts) >= 3 and parts[2] == "FAM" and parts[1] in xrefs:
                    current = parts[1]
                    out[current] = []
            if current is not None:
                out[current].append(line.rstrip("\n"))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dump", metavar="GENI_ID", help="print both records for one person")
    ap.add_argument("--min-lines", type=int, default=12)
    ap.add_argument("--max-lines", type=int, default=30)
    ap.add_argument("--min-statements", type=int, default=0)
    ap.add_argument("--max-statements", type=int, default=18)
    ap.add_argument("--limit", type=int, default=40)
    ap.add_argument(
        "--require-geni",
        default="",
        help="comma-separated GEDCOM tags the record must all carry, e.g. BIRT,DEAT,PLAC",
    )
    ap.add_argument(
        "--require-wd",
        default="",
        help="comma-separated Wikidata properties the item must all carry, e.g. P569,P22",
    )
    # Emma, 2026-08-11: a pre-modern non-Western record is the worst thing to
    # model from, because the Geni profile was authored by someone fitting a
    # Western name/date shape onto a person it does not fit. The 1800s are where
    # both sides are most likely to be doing what they were designed for.
    ap.add_argument("--birth-from", type=int, default=None)
    ap.add_argument("--birth-to", type=int, default=None)
    args = ap.parse_args()

    pairs = read_pairs()
    print(f"{len(pairs):,} unambiguous Geni->Wikidata links", file=sys.stderr)

    if args.dump:
        qid = pairs.get(args.dump)
        print(f"GENI {args.dump}   WIKIDATA {qid or '(no link)'}")
        print()
        print("=" * 74)
        print("GENI — the whole INDI record, verbatim")
        print("=" * 74)
        lines = extract_record(args.dump)
        for line in lines:
            print(line)
        fams = {
            parts[1]
            for parts in (l.split() for l in lines)
            if len(parts) >= 2 and parts[0] == "1" and parts[1].startswith("@F")
        }
        fams |= {
            parts[2]
            for parts in (l.split() for l in lines)
            if len(parts) >= 3 and parts[1] in {"FAMS", "FAMC"}
        }
        for xref, body in extract_families({f for f in fams if f.startswith("@F")}).items():
            print()
            print("=" * 74)
            print(f"GENI — {xref}, verbatim")
            print("=" * 74)
            for line in body:
                print(line)
        if qid:
            with wikistore.StoreReader(STORE, INDEX) as reader:
                entity = reader.entities([qid]).get(qid)
            print()
            print("=" * 74)
            print(f"WIKIDATA — {qid}, every field")
            print("=" * 74)
            if entity is None:
                print("(not in the store)")
            else:
                import json

                print(json.dumps(entity, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    print("scanning the merged GEDCOM", file=sys.stderr)
    counts = scan_gedcom(set(pairs))
    need_geni = [t for t in args.require_geni.split(",") if t]
    small = {
        g: row["lines"]
        for g, row in counts.items()
        if args.min_lines <= row["lines"] <= args.max_lines
        and all(row.get(t, 0) for t in need_geni)
    }
    print(
        f"{len(counts):,} linked people in the tree; "
        f"{len(small):,} with a {args.min_lines}-{args.max_lines} line record"
        + (f" carrying {'+'.join(need_geni)}" if need_geni else ""),
        file=sys.stderr,
    )

    ordered = sorted(small, key=lambda g: (small[g], g))
    qids = [pairs[g] for g in ordered]
    print(f"reading {len(qids):,} items from the store", file=sys.stderr)

    need_wd = [p for p in args.require_wd.split(",") if p]
    rows = []
    with wikistore.StoreReader(STORE, INDEX) as reader:
        entities = reader.entities(qids)
    for geni_id in ordered:
        qid = pairs[geni_id]
        entity = entities.get(qid)
        if entity is None:
            continue
        props, stmts = statement_count(entity)
        if not (args.min_statements <= stmts <= args.max_statements):
            continue
        claims = entity.get("claims") or {}
        if any(p not in claims for p in need_wd):
            continue

        birth_year = None
        for statement in claims.get("P569") or []:
            value = ((statement.get("mainsnak") or {}).get("datavalue") or {}).get("value")
            time_text = value.get("time") if isinstance(value, dict) else None
            if not time_text:
                continue
            # ``+1837-00-00T00:00:00Z`` / ``-0073-...`` — the sign is the era and
            # the year is the four digits after it, whatever the precision says.
            sign, digits = time_text[0], time_text[1:5]
            try:
                birth_year = int(digits) * (-1 if sign == "-" else 1)
            except ValueError:
                birth_year = None
            break
        if args.birth_from is not None and (birth_year is None or birth_year < args.birth_from):
            continue
        if args.birth_to is not None and (birth_year is None or birth_year > args.birth_to):
            continue
        labels = entity.get("labels") or {}
        rows.append(
            (
                small[geni_id] + stmts,
                geni_id,
                qid,
                small[geni_id],
                props,
                stmts,
                len(labels),
                len(entity.get("sitelinks") or {}),
                birth_year if birth_year is not None else "",
                (labels.get("en") or {}).get("value", ""),
            )
        )

    rows.sort()
    print()
    print("geni_id\tqid\tged_lines\tprops\tstatements\tlabels\tsitelinks\tborn\ten_label")
    for row in rows[: args.limit]:
        print("\t".join(str(x) for x in row[1:]))
    print(f"\n{len(rows):,} pairs both small", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
