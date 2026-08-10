"""Every crosscheck conflict, with the evidence that can be gathered offline — queue item 2.D.

`reports/wikidata-crosscheck.md` lists the worst 100 of 930 conflicts, which is
right for reading and useless for measuring. This writes all of them to
`reports/conflicts.tsv`, one row per disagreement, with the axes that bear on
*which side is right* and can be answered without asking anyone.

**This does not adjudicate.** It counts disagreements and attaches evidence.
Emma's instruction for 2.D is to measure per property and assume no global
winner — Geni may be better at relationships and worse at dates — so nothing
here decides a winner, and the columns are deliberately raw.

The columns that are actually evidence:

``their_referenced``
    Whether Wikidata's disputed statement carries a reference. Emma declined
    "whichever cites a source" as a *rule*, and it is still the strongest
    offline signal available about one side's confidence in its own claim.
``their_rank``
    ``preferred`` on a disputed statement means a Wikidata editor chose it over
    a competing value — a human already adjudicated something there.
``their_other_values``
    How many other values that property holds on the item. A person with three
    recorded fathers is a different problem from one with a single wrong father.
``apart``
    Years between the two dates, or ``structural`` for a relationship.

Offline: the store, the P2600 map and `out/merged.ged`.
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from genimerge import crosscheck, wikistore  # noqa: E402
from genimerge.doubles import load_pairs  # noqa: E402
from genimerge.gedcom import stream_file  # noqa: E402
from genimerge.model import build_tree  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / "wikidata" / "items"
INDEX = ROOT / "out" / "wikidata" / "store-index.sqlite3"
MERGED = ROOT / "out" / "merged.ged"
PAIRS = ROOT / "out" / "wikidata" / "p2600-all.tsv"


def linked_people(tree) -> dict[str, str]:
    qids_for: dict[str, set[str]] = {}
    for qid, geni_id in load_pairs(PAIRS):
        if geni_id in tree.people:
            qids_for.setdefault(geni_id, set()).add(qid)
    return {g: next(iter(q)) for g, q in qids_for.items() if len(q) == 1}


def _year_of(time: str) -> int | None:
    """The year in a Wikidata time literal, sign included."""
    if not isinstance(time, str) or len(time) < 5:
        return None
    try:
        year = int(time[1:5])
    except ValueError:
        return None
    return -year if time[0] == "-" else year


def statement_evidence(entity: dict, finding) -> tuple[str, str, int]:
    """``(referenced, rank, other_values)`` for the statement **Wikidata** disputes with.

    Matched against `finding.theirs`, not `finding.target_qid`. `target_qid` and
    `target_time` are what *we* would point at — in a conflict those are by
    definition the values Wikidata does **not** hold, so matching on them found
    nothing for 926 of 930 rows and filled the evidence columns with `?`.

    Item values compare as QIDs. Time values compare by **year**, because
    `theirs` is the rendered year list rather than the raw literal, and the
    conflict is about the year anyway — a day-precision difference never
    reached this table.

    Still `?` when nothing matches, rather than a guess: a wrong attribution
    here is worse than a gap, since these columns are the entire point.
    """
    statements = (entity.get("claims") or {}).get(finding.prop) or []
    live = [s for s in statements if s.get("rank") != "deprecated"]
    wanted = {t.strip() for t in finding.theirs.split(",") if t.strip()}
    for statement in live:
        snak = statement.get("mainsnak") or {}
        if snak.get("snaktype") != "value":
            continue
        raw = (snak.get("datavalue") or {}).get("value")
        if isinstance(raw, dict) and "id" in raw:
            text = raw["id"]
        elif isinstance(raw, dict) and "time" in raw:
            year = _year_of(raw["time"])
            text = str(year) if year is not None else None
        else:
            text = raw if isinstance(raw, str) else None
        if text is not None and text in wanted:
            return (
                "yes" if statement.get("references") else "no",
                statement.get("rank") or "normal",
                len(live) - 1,
            )
    return ("?", "?", max(0, len(live) - 1))



#: Item properties are structural; a relationship has no distance.
_ITEM_PROPS = {"P22", "P25", "P26"}


def _apart(finding) -> str:
    """Years between the two dates, or ``structural``.

    Computed here rather than read from `Finding.detail`, which is empty on the
    conflict path — trusting it stamped every one of the 930 rows `structural`,
    including 638 date conflicts whose whole interest is how far apart they are.
    """
    if finding.prop in _ITEM_PROPS:
        return "structural"
    ours = _tail_year(finding.ours)
    theirs = [int(t) for t in finding.theirs.replace("-", " -").split() if _is_int(t)]
    if ours is None or not theirs:
        return "?"
    return str(min(abs(ours - t) for t in theirs))


def _is_int(text: str) -> bool:
    try:
        int(text)
        return True
    except ValueError:
        return False


def _tail_year(text: str) -> int | None:
    """The year in a GEDCOM-ish date string like ``3 OCT 270`` or ``1080``."""
    for token in reversed(str(text).replace(",", " ").split()):
        if _is_int(token):
            return int(token)
    return None


def main() -> int:
    for path in (INDEX, MERGED, PAIRS):
        if not path.exists():
            print(f"{path} not found", file=sys.stderr)
            return 1

    tree = build_tree(stream_file(MERGED))
    linked = linked_people(tree)
    print(f"tree: {len(tree.people):,} people; linked: {len(linked):,}")

    with wikistore.StoreReader(STORE, INDEX) as reader:
        claims = crosscheck.claims_from_store(reader, linked.values())
        check = crosscheck.cross_check(tree, linked, claims)
        conflicts = check.by_verdict(crosscheck.CONFLICT)
        entities = reader.entities({f.qid for f in conflicts})

    rows = []
    for f in conflicts:
        entity = entities.get(f.qid) or {}
        referenced, rank, others = statement_evidence(entity, f)
        apart = _apart(f)
        rows.append((f.geni_id, f.qid, f.prop, f.ours, f.theirs, apart, referenced, rank, others))

    out = ROOT / "reports" / "conflicts.tsv"
    with io.open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("geni_id\tqid\tproperty\tours\ttheirs\tapart\ttheir_referenced\ttheir_rank\ttheir_other_values\n")
        for row in rows:
            fh.write("\t".join(str(c) for c in row) + "\n")

    from collections import Counter

    per_prop = Counter(r[2] for r in rows)
    referenced = Counter((r[2], r[6]) for r in rows)
    print(f"conflicts: {len(rows):,}")
    for prop in sorted(per_prop):
        yes = referenced[(prop, "yes")]
        no = referenced[(prop, "no")]
        unknown = referenced[(prop, "?")]
        print(f"  {prop:<20} {per_prop[prop]:>4}   wikidata sourced: {yes:>4}  unsourced: {no:>4}  unmatched: {unknown:>4}")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
