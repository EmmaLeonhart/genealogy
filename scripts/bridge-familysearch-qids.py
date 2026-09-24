"""`_FSFTID` -> `P2889` -> QID -> `P2600` -> geni id. The exact join, no name matching.

**The FamilySearch GEDCOM carries no Geni id at all** — measured 2026-09-21 on
`MBW7-P7H-a12-d2.ged`: 3,103 individuals, every one with `_FSFTID`, and **zero `RFN`**. So the
corpus cannot be joined directly and something has to bridge the two identifier spaces.

`P2889` *FamilySearch person ID* is that bridge, and it is a property Wikidata already holds
values for. Two exact joins:

    _FSFTID  ->  P2889  ->  QID          this script, from Wikidata
    QID      ->  P2600  ->  geni id      out/wikidata/p2600-all.tsv, 518,975 rows

⛔ **NO NAME MATCHING ANYWHERE.** `CLAUDE.md` § *The primary key*: merging is an exact join,
never fuzzy name matching. A FamilySearch person who does not resolve through `P2889` stays
unjoined and that is the correct outcome — it is not a cue to try the name.

**It reads the roster, never the query service.** `out/wikidata/p2889-all.tsv` is every item
carrying `P2889`, refreshed by `refresh-p2600-all.py --p2889` beside the `P2600` roster -- ruled
2026-09-24, *"we need to update our rosters of these since they change a lot"*. This used to ask
the query service about the people in hand, 250 at a time, and on 2026-09-24 it was answered
403 and 429 and reached 12 people. What is written is still only the people in the downloads.

Writes `reports/familysearch-qid-bridge.tsv` — `fs_id`, `qid`, `geni_id`.

Usage:
    python scripts/bridge-familysearch-qids.py [<download.ged> ...]   default: every gedcom/familysearch/*.ged
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "familysearch-qid-bridge.tsv"
ROSTER = ROOT / "out" / "wikidata" / "p2889-all.tsv"


def fs_ids(path: Path) -> list[str]:
    """Every `_FSFTID` in the file, in first-seen order and deduplicated.

    Read off `_FSFTID` rather than the `REFN fs:` line the renderer adds, so this works on a
    raw `getmyancestors` file as well as a namespaced one.
    """
    seen = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\d _FSFTID (\S+)\s*$", line)
        if m:
            seen.setdefault(m.group(1), None)
    return list(seen)


def qid_by_fs() -> dict[str, str]:
    """`{fs_id: qid}` from the roster. An id on several items keeps the first, sorted."""
    if not ROSTER.exists():
        sys.exit(f"{ROSTER.relative_to(ROOT)} is missing; "
                 f"run scripts/refresh-p2600-all.py --p2889")
    out = {}
    with open(ROSTER, encoding="utf-8") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2 and parts[0].startswith("Q"):
                out.setdefault(parts[1], parts[0])
    return out


def geni_by_qid() -> dict[str, str]:
    """QID -> geni id, from BOTH stores, the way `build-garborg-day.ledger` does.

    ⛔ **`p2600-all.tsv` ALONE IS NOT THE LEDGER.** The first version of this read only the
    master correspondence and reported `Q141493478` -- Inger Axelsdatter Güntersberg, the
    person this export is rooted on and the first of the two `PRIORITY_ANCESTOR_SEEDS` -- as
    reaching no geni id, while `reports/garborg-qids.tsv` pairs her with
    `6000000000757999620` perfectly well. `ledger()` in `build-garborg-day.py` folds the two
    together for exactly this reason: the ledger knows about items carrying no `P2600` on
    Wikidata yet, which is the shape of everything this campaign has created.

    The master wins where both hold a value, because it is what Wikidata actually states.
    """
    out = {}
    ledger = ROOT / "reports" / "garborg-qids.tsv"
    if ledger.exists():
        with open(ledger, encoding="utf-8") as fh:
            for row in csv.DictReader(fh, delimiter="\t"):
                q = (row.get("qid") or "").strip()
                g = (row.get("geni_id") or "").strip()
                if q.startswith("Q") and g:
                    out.setdefault(q, g)
    path = ROOT / "out" / "wikidata" / "p2600-all.tsv"
    if not path.exists():
        sys.exit(f"{path.relative_to(ROOT)} is missing; it is the second hop of the join.")
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2 and parts[0].startswith("Q"):
                out[parts[0]] = parts[1]
    return out


def main() -> int:
    # ⛔ **EVERY DOWNLOAD, INTO ONE BRIDGE.** It took one file and rewrote the bridge from it,
    # so bridging the owner's tree would have erased Inger's eleven. With no argument it reads
    # every raw download in `gedcom/familysearch/`, which is what `tree.yml` runs.
    srcs = [Path(a) for a in sys.argv[1:]] or sorted(
        p for p in (ROOT / "gedcom" / "familysearch").glob("*.ged") if "-test" not in p.stem)
    dst = OUT

    ids = list(dict.fromkeys(i for src in srcs for i in fs_ids(src)))
    print(f"{len(ids):,} distinct FamilySearch ids in {', '.join(s.name for s in srcs)}")
    roster = qid_by_fs()
    found = {fs: roster[fs] for fs in ids if fs in roster}

    geni = geni_by_qid()
    rows = []
    for fs in ids:
        qid = found.get(fs, "")
        rows.append({"fs_id": fs, "qid": qid, "geni_id": geni.get(qid, "") if qid else ""})

    dst.parent.mkdir(parents=True, exist_ok=True)
    with open(dst, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["fs_id", "qid", "geni_id"], delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    with_qid = sum(1 for r in rows if r["qid"])
    with_geni = sum(1 for r in rows if r["geni_id"])
    print(f"\n  {len(rows):,} FamilySearch people")
    print(f"  {with_qid:,} resolve to a QID via P2889")
    print(f"  {with_geni:,} reach a geni id, and those are the ones that FUSE with the corpus")
    print(f"  -> {dst.relative_to(ROOT) if dst.is_relative_to(ROOT) else dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
