"""The 1500s-and-later export seeds from `wikidata-ancestors` — queue item 2.A.

Emma, 2026-08-09, choosing between the whole 2,123 and tighter cuts: seed the
campaign from the **829 targets born 1500s or later**.

The reasoning that makes a backwards step worth taking, kept here because the
list is meaningless without it: these people are parents Wikidata names for
somebody we already hold, and no export has reached them. A `Descendants` export
seeded on one returns *that parent's whole descent* — the siblings of the person
we hold, and their lines, which we do not have. So the target is useful exactly
when it is late enough for its descent to arrive where the campaign is going,
which is modern times. Pre-1500 targets are excluded for that reason, not
because they are uninteresting.

**Ranked newest first**, then by how many of our people the target is a parent
of — a target naming three of our children is a better single export than one
naming one. The 723 targets carrying no birth date are **not** here and are not
discarded either; they are a separate question, since undated does not mean
early.

Offline: `out/merged.ged`, `out/wikidata/p2600-all.tsv` and the store index.
"""

from __future__ import annotations

import io
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from genimerge import wikiancestors, wikistore  # noqa: E402
from genimerge.gedcom import stream_file  # noqa: E402
from genimerge.model import build_tree  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / "wikidata" / "items"
INDEX = ROOT / "out" / "wikidata" / "store-index.sqlite3"
MERGED = ROOT / "out" / "merged.ged"
PAIRS = ROOT / "out" / "wikidata" / "p2600-all.tsv"

#: Emma's cut. A `Descendants` export from a 1400s parent lands in the 1400s.
EARLIEST = 1500


def load_pairs(path: Path) -> dict[str, str]:
    """``geni_id -> qid``, skipping Geni IDs claimed by more than one item.

    Same rule `_cmd_wikidata_ancestors` uses: a Geni ID on two items cannot be
    joined without choosing, and choosing silently is what
    `reports/wikidata-doubles.md` exists to prevent.
    """
    qids_for: dict[str, set[str]] = {}
    with io.open(path, encoding="utf-8") as fh:
        first = fh.readline()
        if not first.startswith("Q"):
            raise SystemExit(
                f"{path} should be qid<TAB>geni_id with no header; got {first!r}. "
                "Rebuild it with scripts/build-p2600-all.py."
            )
        fh.seek(0)
        for line in fh:
            qid, _, geni_id = line.rstrip("\n").partition("\t")
            if qid and geni_id:
                qids_for.setdefault(geni_id, set()).add(qid)
    return {g: next(iter(q)) for g, q in qids_for.items() if len(q) == 1}


def main() -> int:
    for path in (INDEX, MERGED, PAIRS):
        if not path.exists():
            print(f"{path} not found", file=sys.stderr)
            return 1

    tree = build_tree(stream_file(MERGED))
    qid_by_geni_id = load_pairs(PAIRS)
    print(f"tree: {len(tree.people):,} people; pairs: {len(qid_by_geni_id):,}")

    with wikistore.StoreReader(STORE, INDEX) as reader:
        result = wikiancestors.find_missing_parents(tree, reader, qid_by_geni_id)
        result.years = wikiancestors.parent_birth_years(reader, result.findings)

    exportable = result.by_status(wikiancestors.EXPORTABLE)
    children = Counter(f.parent_qid for f in exportable)
    geni_of: dict[str, tuple[str, ...]] = {}
    for finding in exportable:
        geni_of.setdefault(finding.parent_qid, finding.parent_geni_ids)

    rows = []
    undated = early = 0
    for qid in children:
        year = result.years.get(qid)
        if year is None:
            undated += 1
            continue
        if year < EARLIEST:
            early += 1
            continue
        rows.append((year, children[qid], qid, geni_of.get(qid, ())))

    # Newest first; a target naming more of our children breaks ties.
    rows.sort(key=lambda r: (-r[0], -r[1], r[2]))

    out = ROOT / "reports" / "ancestor-seeds.tsv"
    with io.open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("birth_year\tour_children\tqid\tgeni_id\n")
        for year, count, qid, geni_ids in rows:
            fh.write(f"{year}\t{count}\t{qid}\t{geni_ids[0] if geni_ids else ''}\n")

    print(f"exportable targets : {len(children):,}")
    print(f"  dated {EARLIEST}+   : {len(rows):,}  <- written")
    print(f"  dated pre-{EARLIEST} : {early:,}")
    print(f"  undated          : {undated:,}")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
