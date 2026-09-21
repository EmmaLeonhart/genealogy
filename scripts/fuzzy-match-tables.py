"""Fuzzy text similarity between two tables of people. Ranked pairs, nothing else.

    PYTHONPATH=src python scripts/fuzzy-match-tables.py

⛔ **IT RANKS PAIRS. IT DOES NOT INTERPRET THEM.** Ruled 2026-09-20 after a first attempt that
read history into the output instead of producing it: *"I feel like that's a bit of a random
misunderstanding, like you're doing more inferences than I'm expecting you to do. I'm looking
for fuzzy text similarity search between two tables."*

Left table  `reports/list-descendants-6000000227822546944.tsv`   14,897 scraped descendants
Right table `reports/owner-ancestors.tsv` + `derived-labels.csv`  8,254 ancestors of the owner

**Blocking, because the full product is 123 million pairs.** Only pairs sharing at least one
normalised token of 4+ characters are scored, which is what makes this finish. A pair sharing no
such token cannot score highly on `SequenceMatcher` anyway, so the blocking costs recall it was
never going to have.

**Scored on the whole cleaned name**, not on tokens, so word order and spelling both count.
`difflib.SequenceMatcher` rather than an external library: no dependency, and the ratio is
stable across runs, which matters because this file is committed.

Writes `reports/fuzzy-name-matches.csv`, sorted by score: every pair at or above `FLOOR`.
"""
from __future__ import annotations

import collections
import csv
import difflib
import io
import os
import re
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reports", "fuzzy-name-matches.csv")
csv.field_size_limit(10 ** 9)

#: Below this the pairs are noise at this scale. 0.82 keeps a spelling variant and drops a
#: coincidence; it is a floor on a committed file, not a claim about what is a real match.
FLOOR = 0.82

#: Tokens that block on nothing useful. `NN` alone is thousands of rows on both sides, so
#: blocking on it would restore the full product this exists to avoid.
STOP = {"nn", "unknown", "private", "de", "van", "von", "der", "den", "di", "da", "of", "the",
        "ibn", "bin", "al", "el", "and", "jr", "sr", "king", "queen", "prince", "princess",
        "duke", "count", "lord", "lady", "saint", "name", "managed"}


def clean(name: str) -> str:
    """The comparable form: no `Name:` prefix, no dates, no nicknames, accent-folded."""
    n = re.sub(r"^\s*Name:\s*", "", name or "")
    n = re.sub(r"\([^)]*\)", " ", n)
    n = re.sub(r'"[^"]*"', " ", n)
    n = re.sub(r"[0-9]", " ", n)
    n = unicodedata.normalize("NFKD", n)
    n = "".join(c for c in n if not unicodedata.combining(c))
    return " ".join(n.casefold().split())


def toks(cleaned: str) -> set[str]:
    return {t for t in re.split(r"[^\w'À-ɏ]+", cleaned)
            if len(t) >= 4 and t not in STOP}


def main() -> int:
    left = []
    p = os.path.join(ROOT, "reports", "list-descendants-6000000227822546944.tsv")
    with io.open(p, encoding="utf-8", errors="replace", newline="") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            g = (r.get("geni_id") or "").strip()
            c = clean(r.get("name", ""))
            if g and c:
                left.append((g, r.get("name", "").strip(), c,
                             re.sub(r"^\s*Managed By:\s*", "", (r.get("managed_by") or "").strip())))

    want = {r["geni_id"] for r in csv.DictReader(
        io.open(os.path.join(ROOT, "reports", "owner-ancestors.tsv"), encoding="utf-8"),
        delimiter="\t")}
    right = []
    with io.open(os.path.join(ROOT, "reports", "derived-labels.csv"),
                 encoding="utf-8", errors="replace", newline="") as fh:
        for r in csv.DictReader(fh):
            g = (r.get("geni_id") or "").strip()
            if g in want:
                raw = (r.get("label_mul") or r.get("label_en") or "").strip()
                c = clean(raw)
                if c:
                    right.append((g, raw, c))

    index = collections.defaultdict(list)
    for i, (_g, _raw, c) in enumerate(right):
        for t in toks(c):
            index[t].append(i)

    seen, rows = set(), []
    for lg, lraw, lc, mgr in left:
        cands = set()
        for t in toks(lc):
            cands.update(index.get(t, ()))
        for j in cands:
            rg, rraw, rc = right[j]
            key = (lg, rg)
            if key in seen:
                continue
            seen.add(key)
            s = difflib.SequenceMatcher(None, lc, rc).ratio()
            if s >= FLOOR:
                rows.append((round(s, 4), lg, lraw, rg, rraw, mgr))

    rows.sort(reverse=True)
    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["score", "descendant_geni_id", "descendant_name",
                    "ancestor_geni_id", "ancestor_name", "descendant_managed_by"])
        w.writerows(rows)

    print(f"{os.path.relpath(OUT, ROOT)}")
    print(f"  left {len(left):,} x right {len(right):,}, {len(seen):,} pairs scored after blocking")
    print(f"  at or above {FLOOR}: {len(rows):,}")
    for s, _lg, lraw, _rg, rraw, _m in rows[:15]:
        print(f"   {s:.3f}  {clean(lraw)[:44]:44s} | {clean(rraw)[:44]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
