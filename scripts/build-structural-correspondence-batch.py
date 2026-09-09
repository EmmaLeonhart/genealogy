"""The structural correspondences as `P2600` *Geni.com profile ID* edits.

**This is the step that was missing.** `scripts/walk-structural-merge.py` has been
writing `reports/structural-correspondence.csv` since 2026-08-15 and nothing consumed
it. Emma, 2026-08-16: *"What even was the issue that you came across? The structural
cases you were going to do and then you didn't do."*

**Her order is fixed and this is step one of it**, 2026-08-15: *"The Jenny ID needs to
be present before any properties derived from Jenny can be taken from it, or before
any relationships can be added."* So the only thing emitted here is the identifier.
Everything Geni-derived about these people — the parents, the dates, the sex — comes
in a later batch that declares `requires: structural_correspondence:<qid>`.

**Where the pairing comes from, and why it is not name matching.** The walk starts
from somebody holding *both* a Geni ID and a QID, and compares our father of that
person against Wikidata's `P22` *father* of that item. Those are the same position in
the same family, so they are the same person unless something contradicts it — Emma's
2026-08-12 rule: *"we merge them based off of whether something is the mother on both
sides of an individual."* The label is carried through so a human can see the pair is
not absurd; it never chooses one. `correspondence.md`: *no name similarity, ever*.

**Four states, and only one of them is an edit.** Checked against the store index
rather than against `out/wikidata/p2600-all.tsv`, which is a month older than the
store:

* **emit** — the item states no Geni ID, and our person is linked to no other item.
* **already stated** — the item already carries this exact Geni ID. Nothing to do;
  the walk found a pair Wikidata had recorded all along.
* **a second Geni ID on the item** — the item carries a *different* Geni ID. Still
  emitted, and flagged. `CLAUDE.md`: *"a second `P2600` on a Wikidata item is the
  correct representation"* of two unmergeable Geni profiles for one person, and 2,861
  items in the store already carry more than one. Never held back as a conflict.
* **our person is already linked elsewhere** — our Geni person has a QID of their own
  and it is not this one. **Not emitted.** Two items claiming one Geni profile is a
  disagreement about identity, not an addition, and the walk's `MERGE` branch fires on
  it because it only checks whether our parent's QID is among Wikidata's — not whether
  our parent has a QID at all. Every one is written to
  `reports/structural-correspondence-disagreements.csv` rather than being counted and
  dropped.

Writes `reports/wikidata-structural-correspondence.json`. Offline; nothing is asked of
the network. Emits nothing to Wikidata — execution begins 1 September, which is Emma's
own start date and not a blocker.

    py scripts/build-structural-correspondence-batch.py
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from genimerge import wikistore  # noqa: E402

CORR = REPO / "reports" / "structural-correspondence.csv"
INDEX = REPO / "out" / "wikidata" / "store-index.sqlite3"
STORE = REPO / "wikidata" / "items"
OUT = REPO / "reports" / "wikidata-structural-correspondence.json"
OUT_DISAGREE = REPO / "reports" / "structural-correspondence-disagreements.csv"

csv.field_size_limit(10 ** 7)

#: `P2600` *Geni.com profile ID*, `P854` *reference URL*, `P813` *retrieved*.
GENI_ID = "P2600"
REFERENCE_URL = "P854"
RETRIEVED = "P813"


def shared_name_tokens(geni_name: str, label: str) -> int:
    """How many name tokens the two sides happen to share.

    **A review aid, and nothing filters on it.** Emma's method is *"the structure
    picks the pair; the label only confirms it"* — so this exists so a reviewer can
    sort the batch and look at the pairs whose labels have nothing in common first.
    It never decides whether an edit is emitted, which is the line
    `correspondence.md` draws: *no name similarity, ever. Not as a tiebreak, not as
    corroboration.* Zero shared tokens is normal here, not suspicious: `Regintrude
    I de Bourgogne` and `Ragnétrude` are the same woman under two spellings.
    """
    def toks(s: str) -> set[str]:
        return {t for t in "".join(c if c.isalnum() else " "
                                  for c in s.casefold()).split() if len(t) > 2}

    return len(toks(geni_name) & toks(label))


def main() -> int:
    ap = argparse.ArgumentParser()
    # **Default to when the correspondence was actually computed, not to a date typed
    # once.** `P813` *retrieved* is a factual claim about when the source was consulted,
    # and a literal `2026-08-17` meant every rebuild after that day stamped a false one --
    # this batch was rebuilt on 2026-08-27 and would have said the 17th. The input file's
    # mtime is the honest answer and keeps a rebuild from the same input deterministic,
    # which is what the hardcoded value was presumably protecting.
    _computed = _dt.date.fromtimestamp(
        CORR.stat().st_mtime) if CORR.exists() else _dt.date.today()
    ap.add_argument("--retrieved", default=_computed.isoformat(),
                    help="the P813 retrieved date on every reference. Defaults to when "
                         "reports/structural-correspondence.csv was written.")
    args = ap.parse_args()

    if not CORR.exists():
        print(f"no {CORR}; run scripts/walk-structural-merge.py --all first",
              file=sys.stderr)
        return 1

    rows = list(csv.DictReader(CORR.open(encoding="utf-8", newline="")))
    print(f"{len(rows):,} structural correspondences")

    geni_ids = sorted({r["geni_id"] for r in rows})
    qids = sorted({r["qid"] for r in rows})
    with wikistore.StoreReader(STORE, INDEX) as reader:
        stated = reader.geni_ids_of_qids(qids)
        ours = reader.qids_for_geni_ids(geni_ids)
    print(f"{sum(1 for q in qids if stated.get(q)):,} of {len(qids):,} target items "
          f"already state a Geni ID")

    edits, disagreements, tally = [], [], Counter()
    for r in rows:
        gid, qid = r["geni_id"], r["qid"]
        on_item = stated.get(qid) or []
        elsewhere = [q for q in (ours.get(gid) or []) if q != qid]

        if gid in on_item:
            tally["already stated on the item"] += 1
            continue
        if elsewhere:
            # Our person is linked to a different item. Emitting would give two
            # items one Geni profile, which is a claim about identity rather than
            # an addition to it.
            tally["our person is already linked elsewhere"] += 1
            disagreements.append({
                "geni_id": gid,
                "structural_qid": qid,
                "already_linked_to": " | ".join(elsewhere),
                "position": r["position"],
                "geni_name": r["geni_name"],
                "structural_label": r["wikidata_label"],
                "anchor_geni_id": r["anchor_geni_id"],
                "anchor_qid": r["anchor_qid"],
                "anchor_name": r["anchor_name"],
            })
            continue

        second = bool(on_item)
        tally["a second Geni ID on the item" if second else "emit"] += 1
        edits.append({
            # The Geni id is part of the name because one Wikidata item can
            # correspond to TWO Geni profiles -- the multi-valued `P2600` case
            # `CLAUDE.md` describes, where both statements are correct. Keyed on
            # the QID alone, 20 pairs collided: `structural_correspondence:Q2001541`
            # named two different edits. Nothing declares a `requires` on this
            # prefix yet, so widening the key breaks no dependency.
            "id": f"structural_correspondence:{qid}:{gid}",
            "type": "add_geni_id",
            "source": "structural merge walk",
            "subject": {"qid": qid, "geni_id": gid},
            "requires": [],
            "statements": [{
                "property": GENI_ID,
                "value": gid,
                "references": [
                    {"property": REFERENCE_URL,
                     "value": f"https://www.geni.com/people/x/{gid}"},
                    {"property": RETRIEVED,
                     "value": f"+{args.retrieved}T00:00:00Z/11"},
                ],
            }],
            # The evidence for the pair, so a reviewer can check it rather than
            # take it. Both people sit at the same parent position of the same
            # child, and that child is the anchor.
            "matched_at": r["position"],
            "anchor": {"geni_id": r["anchor_geni_id"], "qid": r["anchor_qid"],
                       "name": r["anchor_name"]},
            "geni_name": r["geni_name"],
            "wikidata_label": r["wikidata_label"],
            "adds_a_second_geni_id": second,
            "geni_ids_already_on_item": on_item,
            # Review aid only. Nothing above filters on it.
            "label_tokens_shared": shared_name_tokens(r["geni_name"],
                                                      r["wikidata_label"]),
        })

    OUT.write_text(json.dumps(edits, ensure_ascii=False, indent=1), encoding="utf-8")
    if disagreements:
        with OUT_DISAGREE.open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(disagreements[0]))
            w.writeheader()
            w.writerows(disagreements)

    for k, v in tally.most_common():
        print(f"  {v:>7,}  {k}")
    unlabelled = sum(1 for e in edits if not e["wikidata_label"])
    nothing_shared = sum(1 for e in edits
                         if e["wikidata_label"] and not e["label_tokens_shared"])
    print(f"\nwrote {OUT} ({len(edits):,} add_geni_id edits)")
    print(f"  {unlabelled:,} of them carry no Wikidata label to review against")
    print(f"  {nothing_shared:,} share no name token with their label — read first, "
          "not filtered out")
    if disagreements:
        print(f"wrote {OUT_DISAGREE} ({len(disagreements):,} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
