"""Every ancestor of the account owner, off the synoptic tree.

    PYTHONPATH=src python scripts/build-owner-ancestors.py

⛔ **THIS IS THE TREE-DERIVED HALF, NOT THE SCRAPED ONE.** Ruled 2026-09-20 to do both: this
runs instantly and carries the Geni id, so a match against it can be EXACT rather than fuzzy --
but it carries **no `managed_by`**, and the managing individual is one of the three axes the
research actually wants. The scraped ancestors list supplies that; this does not pretend to.

**Why both, rather than picking one.** The descendants roster
(`reports/list-descendants-*.tsv`) came off Geni list pages, so its name strings are Geni's own
rendering. Matching those against tree-derived labels compares two different renderings of the
same person and understates the overlap. The scrape is what makes the two sides comparable; this
is what makes the work start now instead of after it.

⛔ `reports/derived-family.csv` separates with ` | ` -- **spaces included**. Splitting it wrong
made 379,251 people arrive childless once and published a clean-looking distribution.

Writes `reports/owner-ancestors.tsv`: `geni_id,qid,generation`.
"""
from __future__ import annotations

import collections
import csv
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OWNER = "6000000087535357291"
OUT = os.path.join(ROOT, "reports", "owner-ancestors.tsv")

csv.field_size_limit(10 ** 9)
SEP = " | "


def main() -> int:
    parents: dict[str, list[str]] = {}
    qids: dict[str, str] = {}
    with io.open(os.path.join(ROOT, "reports", "derived-family.csv"),
                 encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            g = (row.get("geni_id") or "").strip()
            if not g:
                continue
            if row.get("qid"):
                qids[g] = row["qid"].strip()
            ps = []
            # `fathers`/`mothers` are the multi-valued columns; father/mother are the singular
            # convenience ones. Both are read, because a person may have either shape.
            for col in ("fathers", "mothers", "father", "mother"):
                v = (row.get(col) or "").strip()
                if v:
                    ps.extend(x.strip() for x in v.split(SEP) if x.strip())
            if ps:
                parents[g] = ps

    seen = {OWNER: 0}
    q = collections.deque([OWNER])
    while q:
        g = q.popleft()
        for p in parents.get(g, ()):
            if p not in seen:
                seen[p] = seen[g] + 1
                q.append(p)
    del seen[OWNER]

    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["geni_id", "qid", "generation"])
        for g, gen in sorted(seen.items(), key=lambda kv: (kv[1], kv[0])):
            w.writerow([g, qids.get(g, ""), gen])

    by_gen = collections.Counter(seen.values())
    with_qid = sum(1 for g in seen if g in qids)
    print(f"{os.path.relpath(OUT, ROOT)}: {len(seen):,} ancestors of {OWNER}")
    print(f"  carrying a QID: {with_qid:,}")
    print(f"  deepest generation: {max(by_gen) if by_gen else 0}")
    print("  by generation:", ", ".join(f"g{k}={v}" for k, v in sorted(by_gen.items())[:12]), "...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
