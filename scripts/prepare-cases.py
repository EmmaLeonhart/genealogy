"""Lay out the next N ancestor cases for review — data only, no conclusions.

`python scripts/prepare-cases.py 979118 --count 10`

Writes one file per person into `out/cases/`, in ahnentafel order from the seed:
2 father, 3 mother, 4 father's father, 5 father's mother, and so on. Each file
holds, verbatim:

* the person's raw GEDCOM record, with `NOTE` blocks over 20 lines and `OBJE`
  blocks withheld and **counted** — those are pasted articles and image
  attachments, and Emma asked for the structured data without them;
* every `FAM` record they appear in, whole, since that is where marriage dates
  and places live;
* their Wikidata item's statements printed with **qualifiers and references**,
  because reading `mainsnak` alone is how this project twice reported that
  Wikidata held nothing when it held the answer.

Every QID mentioned anywhere across all cases is resolved to an English label in
**one** batched SPARQL query at the end, via `scripts/fetch-labels.py`'s query
shape. Labels for items already in the store come from the store.

**This decides nothing.** It draws no comparison and flags no disagreement. It
exists so the records are in front of Emma when she is ready to look at them.
"""

from __future__ import annotations

import io
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from genimerge import wikistore  # noqa: E402
from genimerge.doubles import load_pairs  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / "wikidata" / "items"
INDEX = ROOT / "out" / "wikidata" / "store-index.sqlite3"
MERGED = ROOT / "out" / "merged.ged"
PAIRS = ROOT / "out" / "wikidata" / "p2600-all.tsv"
OUT = ROOT / "out" / "cases"

LONG_NOTE = 20


def read_records(path: Path):
    """Raw top-level records, keyed by xref, exactly as they appear."""
    records: dict[str, list[str]] = {}
    cur = None
    buf: list[str] = []
    for line in io.open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("0 "):
            if cur:
                records[cur] = buf
            parts = line.split(" ")
            cur = parts[1] if len(parts) > 2 and parts[1].startswith("@") else None
            buf = [line]
        else:
            buf.append(line)
    if cur:
        records[cur] = buf
    return records


def blocks_of(record: list[str]):
    out = [[record[0]]]
    for line in record[1:]:
        if line.startswith("1 "):
            out.append([line])
        else:
            out[-1].append(line)
    return out


def structured(record: list[str]) -> tuple[list[str], int, int]:
    kept, notes, media = [record[0]], 0, 0
    for block in blocks_of(record)[1:]:
        tag = block[0].split(" ")[1] if len(block[0].split(" ")) > 1 else ""
        if tag == "OBJE":
            media += 1
            continue
        if tag == "NOTE" and len(block) > LONG_NOTE:
            notes += 1
            continue
        kept.extend(l for l in block if l.strip())
    return kept, notes, media


def families_of(record: list[str]) -> list[str]:
    return [l.split(" ")[2] for l in record if l.startswith(("1 FAMS", "1 FAMC"))]


def parents(xref: str, records) -> tuple[str | None, str | None]:
    for fam in (l.split(" ")[2] for l in records.get(xref, []) if l.startswith("1 FAMC")):
        rec = records.get(fam, [])
        h = next((l.split(" ")[2] for l in rec if l.startswith("1 HUSB")), None)
        w = next((l.split(" ")[2] for l in rec if l.startswith("1 WIFE")), None)
        return h, w
    return None, None


def statements(entity: dict) -> list[str]:
    """Every claim, with qualifiers and reference snaks. Nothing summarised."""
    out: list[str] = []
    for prop, sts in sorted((entity.get("claims") or {}).items()):
        for st in sts:
            snak = st.get("mainsnak") or {}
            v = (snak.get("datavalue") or {}).get("value")
            if isinstance(v, dict):
                v = v.get("id") or v.get("time") or v.get("amount") or str(v)[:70]
            out.append(f"  {prop} = {v}   [rank {st.get('rank')}]")
            for qp, snaks in (st.get("qualifiers") or {}).items():
                for s in snaks:
                    qv = (s.get("datavalue") or {}).get("value")
                    if isinstance(qv, dict):
                        qv = qv.get("id") or qv.get("time") or str(qv)[:60]
                    out.append(f"      qualifier {qp} = {qv}")
            for i, ref in enumerate(st.get("references") or [], 1):
                for rp, snaks in (ref.get("snaks") or {}).items():
                    for s in snaks:
                        rv = (s.get("datavalue") or {}).get("value")
                        if isinstance(rv, dict):
                            rv = rv.get("id") or rv.get("time") or str(rv)[:60]
                        out.append(f"      ref{i} {rp} = {rv}")
    return out


def main() -> int:
    seed = sys.argv[1] if len(sys.argv) > 1 else "979118"
    count = int(sys.argv[sys.argv.index("--count") + 1]) if "--count" in sys.argv else 10

    records = read_records(MERGED)
    qids_for: dict[str, set] = defaultdict(set)
    for qid, gid in load_pairs(PAIRS):
        qids_for[gid].add(qid)
    qid_by_geni = {g: next(iter(q)) for g, q in qids_for.items() if len(q) == 1}

    # Ahnentafel, skipping position 1 (the seed, already reviewed).
    order: list[tuple[int, str]] = [(1, f"@I{seed}@")]
    i = 0
    while i < len(order) and len(order) < count + 1:
        n, ref = order[i]
        i += 1
        f, m = parents(ref, records)
        for slot, p in ((2 * n, f), (2 * n + 1, m)):
            if p:
                order.append((slot, p))
    cases = order[1 : count + 1]

    OUT.mkdir(parents=True, exist_ok=True)
    mentioned: set[str] = set()
    written = []

    with wikistore.StoreReader(STORE, INDEX) as reader:
        for n, ref in cases:
            gid = ref.strip("@").lstrip("I")
            qid = qid_by_geni.get(gid)
            entity = reader.entities([qid]).get(qid, {}) if qid else {}
            rec = records.get(ref, [])
            kept, notes, media = structured(rec)

            lines = [f"CASE [{n}]   geni {gid}   " + (f"wikidata {qid}" if qid else "wikidata: NOT LINKED"), ""]
            lines += ["=" * 74, "GENI - structured record", "=" * 74] + kept
            lines += ["", f"(withheld: {notes} NOTE blocks over {LONG_NOTE} lines, {media} OBJE blocks)", ""]
            for fam in families_of(rec):
                lines += ["=" * 74, f"GENI - {fam}", "=" * 74] + [l for l in records.get(fam, []) if l.strip()] + [""]
            lines += ["=" * 74, "WIKIDATA - every statement, with qualifiers and references", "=" * 74]
            if not qid:
                lines.append("  no P2600 link")
            elif not entity:
                lines.append(f"  {qid} not in the downloaded store")
            else:
                st = statements(entity)
                lines += st
                # Keep the "Q". An earlier version stored `w[1:]`, so 366 of
                # 376 collected ids were bare digits, silently dropped by
                # fetch-labels.py's `startswith("Q")` filter, and the run
                # reported "10/10 resolved" as though that were the whole set.
                mentioned.update(w for line in st for w in line.split() if w.startswith("Q") and w[1:].isdigit())
            if qid:
                mentioned.add(qid)

            path = OUT / f"case-{n:02d}-{gid}.txt"
            io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
            written.append((n, path, len(rec)))

    for n, path, size in written:
        print(f"  [{n:>2}] {path.name}   (source record {size:,} lines)")

    # One query for every QID any case mentions.
    todo = sorted(mentioned)
    print(f"\n{len(todo):,} distinct QIDs mentioned across {len(written)} cases")
    if todo:
        labels = ROOT / "out" / "cases" / "labels.txt"
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "fetch-labels.py"), *todo],
            capture_output=True, text=True, encoding="utf-8",
        )
        io.open(labels, "w", encoding="utf-8", newline="\n").write(result.stdout)
        print(f"wrote {labels}   ({result.stderr.strip()})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
