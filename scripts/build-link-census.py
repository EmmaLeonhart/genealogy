"""Every P2600 link, and how far the two sides agree — the census behind the
"links worth re-checking" question.

Emma, 2026-08-11, on the two links flagged as suspect (Canute I Erikska
`Q442876`, Bengt Folkesson `Q1621801`): **"Analyse them like the dates."**

The dates analysis worked because it censused *every* instance rather than
reading the two worst. So this does the same: one row per comparison and one row
per linked person, for all of them, so the two suspects can be located in a
distribution instead of admired in isolation.

Mirrors `genimerge crosscheck --offline` exactly — links from the P2600 map,
claims from the downloaded store — and reuses `crosscheck.cross_check` and
`crosscheck.link_balances` rather than restating their comparison rules. Nothing
is queried.

Writes:

* `reports/link-findings.csv` — one row per property comparison
* `reports/link-balance.csv` — one row per linked person

    py scripts/build-link-census.py
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from genimerge import crosscheck, doubles, gedcom, model, wikistore  # noqa: E402

MERGED = REPO_ROOT / "out" / "merged.ged"
PAIRS = REPO_ROOT / "out" / "wikidata" / "p2600-all.tsv"
STORE = REPO_ROOT / "wikidata" / "items"
INDEX = REPO_ROOT / "out" / "wikidata" / "store-index.sqlite3"
OUT_FINDINGS = REPO_ROOT / "reports" / "link-findings.csv"
OUT_BALANCE = REPO_ROOT / "reports" / "link-balance.csv"

#: The two the earlier report singled out, carried here so the census says where
#: they actually sit rather than leaving that to be eyeballed.
FLAGGED = {"Q442876": "Canute I Erikska", "Q1621801": "Bengt Folkesson"}


def main() -> int:
    print(f"loading {MERGED}", flush=True)
    tree = model.build_tree(gedcom.stream_file(MERGED))
    print(f"{len(tree.people):,} people", flush=True)

    qids_for: dict[str, set[str]] = {}
    for qid, geni_id in doubles.load_pairs(PAIRS):
        if geni_id in tree.people:
            qids_for.setdefault(geni_id, set()).add(qid)
    # A Geni ID claimed by more than one item is skipped, never chosen between —
    # the rule reports/wikidata-doubles.md exists to enforce.
    linked = {g: next(iter(q)) for g, q in qids_for.items() if len(q) == 1}
    skipped = len(qids_for) - len(linked)
    print(f"{len(linked):,} linked people, {skipped:,} skipped for claiming several items", flush=True)

    print("reading claims from the store", flush=True)
    with wikistore.StoreReader(STORE, INDEX) as reader:
        claims = crosscheck.claims_from_store(reader, linked.values())
    print(f"{len(claims):,} items returned claims", flush=True)

    print("comparing", flush=True)
    check = crosscheck.cross_check(tree, linked, claims)
    print(f"{len(check.findings):,} comparisons over {check.people_checked:,} people", flush=True)

    OUT_FINDINGS.parent.mkdir(parents=True, exist_ok=True)
    verdicts: Counter[str] = Counter()
    by_prop: Counter[tuple[str, str]] = Counter()
    with open(OUT_FINDINGS, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            ["geni_id", "qid", "person", "property", "property_label", "verdict", "ours", "theirs", "detail"]
        )
        for f in check.findings:
            label = crosscheck.PROPERTIES.get(f.prop, (f.prop, ""))[0]
            verdicts[f.verdict] += 1
            by_prop[(f.prop, f.verdict)] += 1
            writer.writerow(
                [f.geni_id, f.qid, f.person, f.prop, label, f.verdict, f.ours, f.theirs, f.detail]
            )

    balances = crosscheck.link_balances(check)
    with open(OUT_BALANCE, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["geni_id", "qid", "person", "agrees", "conflicts", "comparable", "margin"])
        for b in balances:
            writer.writerow([b.geni_id, b.qid, b.person, b.agrees, b.conflicts, b.comparable, b.margin])

    suspects = crosscheck.suspect_links(check)
    print()
    print(f"wrote {OUT_FINDINGS} ({len(check.findings):,} rows)")
    print(f"wrote {OUT_BALANCE} ({len(balances):,} rows)")
    print()
    print("verdicts:", dict(verdicts))
    print()
    print("per property (agrees / gap / conflict / not comparable):")
    for prop, (label, _) in crosscheck.PROPERTIES.items():
        cells = " / ".join(
            f"{by_prop[(prop, v)]:,}"
            for v in (crosscheck.AGREES, crosscheck.GAP, crosscheck.CONFLICT, crosscheck.NOT_COMPARABLE)
        )
        print(f"  {prop} {label:<16} {cells}")
    print()
    print(f"{len(suspects):,} suspect links (conflicts >= 2 and conflicts > agrees)")
    print("  margin distribution over all linked people:")
    for margin, n in sorted(Counter(b.margin for b in balances).items(), reverse=True):
        print(f"    margin {margin:+3}: {n:,}")
    print()
    print("the two the earlier report flagged:")
    for b in balances:
        if b.qid in FLAGGED:
            print(
                f"  {b.qid} {FLAGGED[b.qid]:<20} agrees {b.agrees}  conflicts {b.conflicts}  "
                f"margin {b.margin:+}  rank {balances.index(b) + 1} of {len(balances):,}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
