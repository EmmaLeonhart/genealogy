"""One QID↔Geni correspondence, gathered from every place one currently lives.

    python scripts/build-synoptic-correspondence.py

**Emma, 2026-08-23:** *"there was a tsv qid correspondence quickstatement thing is
that represented in our data?... I'm afraid it isn't properly represented in our
synoptic tree."*

She was right to be afraid. Five files hold QID↔Geni pairings and **nothing joined
them**, which is precisely the artefact `CLAUDE.md` says the synoptic tree is for:
*"we definitely need to… be essentially building up our own correspondence of the
QIDs and Jenny IDs for these ones."*

| source | what it is |
| --- | --- |
| `out/wikidata/p2600-all.tsv` | what **Wikidata already states**, from the bulk download |
| `reports/geni-qid-links.tsv` | the Wikidata URL **Emma wrote into the Geni About Me** |
| `reports/structural-correspondence.csv` | found by walking relationships, not names |
| `reports/geni-wikidata-pairs.csv` | the Geni↔Wikidata pairing pass |
| `reports/izumo-p2600-pairs.tsv` | the Izumo roster join |

Every pair keeps its provenance, so a row can be read back to why we believe it.

**Two kinds of multiplicity, and only one is a problem.**

*One QID, several Geni ids* is **ordinary and correct** — `CLAUDE.md`: two Geni
profiles for one person is a permanent structural feature of Geni, `P2600` is
multi-valued, and 2,861 stored items already carry more than one. Not flagged.

*One Geni id, several QIDs* is a **contradiction**: one person cannot be two Wikidata
items. Those are counted and listed, never resolved here — merges and identity calls
are Emma's.

Writes `reports/synoptic-correspondence.tsv` and `reports/synoptic-conflicts.tsv`.
Offline throughout.
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

csv.field_size_limit(1 << 30)
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent


def date_refuted():
    """`{(qid, geni_id)}` the structural walk proposed and dates prove impossible.

    **Emma, 2026-08-24, on the walk's date conflicts:** *"All these ones look easy."*
    They are: `Eufemia von Hirscher` 1166-1229 paired with `Margaret of Nuremberg`
    1359-1390 is not a judgement call, it is a pairing that cannot be right. So they are
    dropped here rather than carried into the synoptic tree and left for a human to
    re-notice.

    **Only `structural` pairs are dropped.** A `wikidata-p2600` pair whose dates disagree
    is Wikidata stating an identifier we do not get to overrule -- that is a
    disagreement to record, not a pair to delete. This filter refutes our own inference
    and nothing else, which is why it keys on the pair rather than on the Geni id.

    Absent validation file -> empty set, so the build still runs.
    """
    path = ROOT / "reports" / "structural-walk-validation.tsv"
    if not path.exists():
        print("  (no structural-walk-validation.tsv; keeping every structural pair)")
        return set()
    with open(path, encoding="utf-8") as f:
        return {(r["qid"], r["geni_id"])
                for r in csv.DictReader(f, delimiter="\t")
                if r["verdict"] == "conflict"}


def rows_from(path, qid_col, geni_col, delim=","):
    if not path.exists():
        print(f"  (missing: {path.relative_to(ROOT)})")
        return
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=delim):
            q = (row.get(qid_col) or "").strip()
            for g in (row.get(geni_col) or "").split(";"):
                g = g.strip()
                if q.startswith("Q") and g.isdigit():
                    yield q, g


def wikidata_snapshot(path):
    if not path.exists():
        print(f"  (missing: {path.relative_to(ROOT)})")
        return
    with open(path, encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) >= 2 and row[0].startswith("Q") and row[1].strip().isdigit():
                yield row[0].strip(), row[1].strip()


def main():
    pairs = defaultdict(set)          # (qid, geni) -> {sources}
    R = ROOT / "reports"

    sources = [
        ("wikidata-p2600", wikidata_snapshot(ROOT / "out" / "wikidata" / "p2600-all.tsv")),
        ("geni-about-me", rows_from(R / "geni-qid-links.tsv", "qids", "geni_id", "\t")),
        ("structural", rows_from(R / "structural-correspondence.csv", "qid", "geni_id")),
        ("geni-wikidata-pairs", rows_from(R / "geni-wikidata-pairs.csv", "qid", "geni_id")),
        ("izumo-roster", rows_from(R / "izumo-p2600-pairs.tsv", "qid", "geni_ids", "\t")),
        # Emma, 2026-08-24: *"the tanba onakatomi izumo stuff is a prerequisite for the
        # synoptic rebuild"*. Tanba and the sister repo's fuller Izumo roster had joins
        # that nothing read, so a whole clan was invisible here despite every one of its
        # people carrying a Wikidata item. Onakatomi is deliberately absent: 0 of its 97
        # QIDs has an About Me link yet, so there is nothing to join on.
        ("tanba-roster", rows_from(R / "tanba-p2600-pairs.tsv", "qid", "geni_ids", "\t")),
        ("izumo-sister-roster",
         rows_from(R / "izumo-sister-p2600-pairs.tsv", "qid", "geni_ids", "\t")),
    ]
    refuted = date_refuted()
    dropped = 0
    for label, stream in sources:
        n = 0
        for q, g in stream:
            # Our own inference, and dates say it is impossible. See `date_refuted`.
            if label == "structural" and (q, g) in refuted:
                dropped += 1
                continue
            pairs[(q, g)].add(label)
            n += 1
        print(f"{label:<22} {n:>7} pairs")
    if refuted:
        print(f"{'(date-refuted)':<22} {dropped:>7} structural pairs dropped")

    print(f"\n{len(pairs)} distinct (qid, geni) pairs")

    by_geni = defaultdict(set)
    by_qid = defaultdict(set)
    for q, g in pairs:
        by_geni[g].add(q)
        by_qid[q].add(g)

    multi_geni = {q: gs for q, gs in by_qid.items() if len(gs) > 1}
    conflicts = {g: qs for g, qs in by_geni.items() if len(qs) > 1}
    print(f"{len(by_qid)} QIDs, {len(by_geni)} Geni profiles")
    print(f"{len(multi_geni)} QIDs carry more than one Geni id "
          f"- ordinary, P2600 is multi-valued")
    print(f"{len(conflicts)} Geni profiles claim more than one QID - CONTRADICTIONS")

    out = R / "synoptic-correspondence.tsv"
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["qid", "geni_id", "sources", "qid_has_other_geni_ids",
                    "geni_id_has_other_qids"])
        for (q, g), src in sorted(pairs.items()):
            w.writerow([q, g, ";".join(sorted(src)),
                        len(by_qid[q]) - 1, len(by_geni[g]) - 1])
    print(f"\nwrote {out.relative_to(ROOT)}")

    # **One row per competing QID, so each carries its OWN provenance.**
    #
    # This used to write one row per Geni profile with the sources of every candidate
    # flattened into a single set: `structural;wikidata-p2600` told you the conflict
    # involved both, but not *which* source proposed *which* QID. That is the whole
    # question, because `wikidata-p2600` is a statement Wikidata carries while
    # `structural` is our own inference from tree position, and where they disagree
    # the recorded identifier wins.
    #
    # It misled twice on 2026-08-24 alone. Katharina von Braunschweig-Wolfenbüttel was
    # reported as the structural walk pairing a woman with `Q567039` *Henry IV, Duke of
    # Brunswick* -- a man. The walk never touched her: `P2600` supplied the correct
    # `Q434771` and the wrong candidate came from `geni-wikidata-pairs`. The flattened
    # column made an ordinary aggregate look like per-candidate provenance.
    conf = R / "synoptic-conflicts.tsv"
    with open(conf, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["geni_id", "qid", "sources", "competing_qids", "shape"])
        for g, qs in sorted(conflicts.items()):
            per = {q: sorted(pairs[(q, g)]) for q in qs}
            # Name the common case so it can be filtered without re-deriving it: our
            # inference standing against Wikidata's own identifier.
            flat = {s for src in per.values() for s in src}
            shape = ("inference vs recorded id"
                     if {"structural", "wikidata-p2600"} <= flat
                     else "both from Wikidata" if flat == {"wikidata-p2600"}
                     else "other")
            for q in sorted(qs):
                w.writerow([g, q, ";".join(per[q]),
                            ";".join(sorted(qs - {q})), shape])
    print(f"wrote {conf.relative_to(ROOT)} - {len(conflicts)} conflicts, "
          f"one row per candidate, Emma's to settle")


if __name__ == "__main__":
    main()
