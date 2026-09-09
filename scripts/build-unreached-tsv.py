"""Rebuild `reports/wikidata-unreached.tsv` — the P2600 pairs we have never exported.

A pair is "unreached" when Wikidata names a Geni profile and that profile is not
in our merged tree. Inputs are both local: `out/wikidata/p2600-all.tsv` (written
from the store by `genimerge wikidata-index --map`, or by `write_p2600_map`
against an existing index) and `out/merged.ged`.

**Nothing here touches the network.** The pair list used to come from a SPARQL
cache; when that cache was lost with `out/` on 2026-08-09 the obvious repair was
to re-query Wikidata, which CLAUDE.md forbids. Every P2600 claim is already in
`wikidata/items/`, so the list is reconstructed from the store instead.

Our side is read by streaming the INDI xref lines through `identity.GENI_ID_RE`
rather than parsing the GEDCOM — same answer, a fraction of the CPU, which
matters on a laptop Emma is watching the heat of.

Malformed P2600 values are written to `reports/wikidata-p2600-malformed.tsv` and
never parsed for an ID. They are URLs pasted into a field that should hold an ID;
recovering an ID by parsing one out is the fuzzy matching this repo refuses
everywhere else, and the defect belongs on Wikidata.
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from genimerge.identity import GENI_ID_RE  # noqa: E402
from genimerge.overlap import NUMERIC  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def tree_geni_ids(merged: Path) -> set[str]:
    """Every Geni ID in the merged tree, from the INDI xref lines alone."""
    ids: set[str] = set()
    with io.open(merged, encoding="utf-8") as fh:
        for line in fh:
            if not line.startswith("0 @I"):
                continue
            xref = line.split(" ", 2)[1].strip()
            match = GENI_ID_RE.match(xref)
            if match:
                ids.add(match.group("geni_id"))
    return ids


def main() -> int:
    pairs_path = ROOT / "out" / "wikidata" / "p2600-all.tsv"
    merged = ROOT / "out" / "merged.ged"
    for path in (pairs_path, merged):
        if not path.exists():
            print(f"{path} not found", file=sys.stderr)
            return 1

    ours = tree_geni_ids(merged)

    # `p2600-all.tsv` is `qid<TAB>geni_id` with NO header — the format
    # `genimerge overlap` writes and every consumer reads positionally. It is
    # *not* `p2600-map.tsv`, which is `geni_id<TAB>qid` with a header. Getting
    # these two crossed is silent in both directions: it once classified all
    # 517,878 pairs as malformed here, and separately made
    # `genimerge wikidata-ancestors` report `0 of our people carry an item`
    # while exiting 0. Assert the shape rather than trusting the filename.
    numeric: list[tuple[str, str]] = []
    malformed: list[tuple[str, str]] = []
    with io.open(pairs_path, encoding="utf-8") as fh:
        first = fh.readline().rstrip("\n")
        if not first.startswith("Q"):
            print(
                f"{pairs_path} does not start with a QID (got {first!r}). "
                "Expected qid<TAB>geni_id with no header - rebuild it with "
                "scripts/build-p2600-all.py.",
                file=sys.stderr,
            )
            return 1
        fh.seek(0)
        for line in fh:
            line = line.rstrip("\n")
            if not line:
                continue
            qid, _, geni_id = line.partition("\t")
            (numeric if NUMERIC.match(geni_id) else malformed).append((qid, geni_id))

    unreached = sorted({(q, g) for q, g in numeric if g not in ours})
    held = len(numeric) - len(unreached)

    out = ROOT / "reports" / "wikidata-unreached.tsv"
    with io.open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("qid\tgeni_id\n")
        for qid, geni_id in unreached:
            fh.write(f"{qid}\t{geni_id}\n")

    bad = ROOT / "reports" / "wikidata-p2600-malformed.tsv"
    with io.open(bad, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("qid\tvalue\n")
        for qid, value in sorted(set(malformed)):
            fh.write(f"{qid}\t{value}\n")

    print(f"tree: {len(ours):,} Geni IDs")
    print(f"P2600 pairs: {len(numeric):,} numeric, {len(malformed):,} malformed")
    print(f"unreached: {len(unreached):,}  held: {held:,}")
    print(f"wrote {out} and {bad}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
