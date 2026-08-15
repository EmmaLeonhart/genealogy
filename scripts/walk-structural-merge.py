"""Walk up the parental lines, matching Geni's parents against Wikidata's.

Emma, 2026-08-15: *"For the synoptic tree, we're supposed to be specifically
going up the parental lines and stuff like that and merging the parents on Jenny
and Wikidata if there are ones on both. Same with all the other relationships.
That is a critical part of building up this synoptic tree."*

**This shows cases. It does not build a pipeline.** `CLAUDE.md` § *How this
project works now*: show records one by one, derive the rule from them, never the
other way round. It writes no edits and merges nothing.

**The structure picks the pair; the label only confirms it.** Start from somebody
holding **both** a Geni ID and a QID. Our father of that Geni ID and Wikidata's
`P22` of that QID are the *same position in the same family*, so they are the
same person unless something says otherwise — Emma's 2026-08-12 rule: *"we merge
them based off of whether something is the mother on both sides of an individual.
We merge them together unless the mothers really conflict."*

**What this must never become:** searching Wikidata for a name. That is the
matcher Emma killed on 2026-08-12 and whose module was deleted on 2026-08-15.
`correspondence.md`: *"No name similarity, ever. Not as a tiebreak, not as
corroboration, not as a candidate list for a human."* Every comparison here is
between two people the structure already placed opposite each other.

**Four outcomes at each position**, and they are reported separately because they
need different decisions:

* `AGREE`    — both sides name a parent and they are already the same item.
* `MERGE`    — both sides name a parent, ours has no QID: **this is the
  correspondence to record.**
* `GENI ONLY`— we have a parent, Wikidata does not. A creation, later.
* `WD ONLY`  — Wikidata has a parent, we do not. Nothing to do here.

Offline: `reports/derived-family.csv` for our side, the downloaded store for
Wikidata's. Nothing is asked of the network.

    py scripts/walk-structural-merge.py --start <geni id> --lines 5
"""

from __future__ import annotations

import argparse
import csv
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from genimerge import wikistore  # noqa: E402

FAMILY = REPO / "reports" / "derived-family.csv"
LABELS = REPO / "reports" / "derived-labels.csv"
INDEX = REPO / "out" / "wikidata" / "store-index.sqlite3"
STORE = REPO / "wikidata" / "items"

csv.field_size_limit(10 ** 7)

FATHER, MOTHER = "P22", "P25"


def wd_parent(entity, prop):
    """The QIDs Wikidata states for this parent property, truthy ranks only."""
    out = []
    for st in (entity.get("claims") or {}).get(prop, []):
        if st.get("rank") == "deprecated":
            continue
        snak = st.get("mainsnak") or {}
        if snak.get("snaktype") != "value":
            continue
        v = snak.get("datavalue", {}).get("value")
        if isinstance(v, dict) and v.get("id"):
            out.append(v["id"])
    return out


def label_of(entity, lang="en"):
    if not entity:
        return None
    lab = (entity.get("labels") or {}).get(lang)
    return lab.get("value") if isinstance(lab, dict) else lab


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", help="one Geni ID to walk from")
    ap.add_argument("--lines", type=int, default=5, help="how many lines to show")
    ap.add_argument("--depth", type=int, default=8, help="generations up")
    args = ap.parse_args()

    fam, ourqid = {}, {}
    with FAMILY.open(encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            fam[r["geni_id"]] = r
            if (r.get("qid") or "").strip():
                ourqid[r["geni_id"]] = r["qid"].strip()
    print(f"{len(fam):,} people in reports/derived-family.csv, "
          f"{len(ourqid):,} carry a QID")

    names = {}
    with LABELS.open(encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            names[r["geni_id"]] = (r.get("label_en") or "").strip()

    # Anchors: people with BOTH identifiers AND a parent on our side.
    anchors = [g for g, q in ourqid.items()
               if fam[g].get("father") or fam[g].get("mother")]
    anchors.sort(key=lambda g: -(len(fam[g].get("father", ""))
                                 + len(fam[g].get("mother", ""))))
    if args.start:
        anchors = [args.start] + [a for a in anchors if a != args.start]
    print(f"{len(anchors):,} anchors hold both identifiers and a recorded parent\n")

    wanted = set()
    for g in anchors[:args.lines]:
        cur = g
        for _ in range(args.depth):
            if cur in ourqid:
                wanted.add(ourqid[cur])
            row = fam.get(cur)
            if not row:
                break
            cur = row.get("father") or row.get("mother") or ""
            if not cur:
                break

    with wikistore.StoreReader(STORE, INDEX) as reader:
        # Two passes: the anchors' own items, then the parents those name.
        ents = reader.entities(sorted(wanted))
        more = set()
        for e in ents.values():
            more.update(wd_parent(e, FATHER) + wd_parent(e, MOTHER))
        ents.update(reader.entities(sorted(more - set(ents))))

    tally = {"AGREE": 0, "MERGE": 0, "GENI ONLY": 0, "WD ONLY": 0}
    for n, start in enumerate(anchors[:args.lines], 1):
        print("=" * 78)
        print(f"LINE {n}: {names.get(start, '(no label)')}   geni {start}   "
              f"{ourqid.get(start, '(no qid)')}")
        print("=" * 78)
        cur = start
        for gen in range(args.depth):
            row = fam.get(cur)
            if not row:
                break
            qid = ourqid.get(cur)
            ent = ents.get(qid) if qid else None
            for prop, key, word in ((FATHER, "father", "father"),
                                    (MOTHER, "mother", "mother")):
                ours_id = (row.get(key) or "").strip()
                theirs = wd_parent(ent, prop) if ent else []
                if not ours_id and not theirs:
                    continue
                ours_qid = ourqid.get(ours_id, "")
                if ours_id and theirs:
                    if ours_qid and ours_qid in theirs:
                        verdict = "AGREE"
                    else:
                        verdict = "MERGE"
                elif ours_id:
                    verdict = "GENI ONLY"
                else:
                    verdict = "WD ONLY"
                tally[verdict] += 1
                geni_side = (f"{names.get(ours_id, '(no label)')} [{ours_id}"
                             f"{'/' + ours_qid if ours_qid else ''}]"
                             if ours_id else "-")
                wd_side = " ; ".join(
                    f"{label_of(ents.get(t)) or '(not in store)'} [{t}]"
                    for t in theirs) or "-"
                print(f"  gen {gen}  {word:<6} {verdict:<10}")
                print(f"           geni:     {geni_side}")
                print(f"           wikidata: {wd_side}")
            nxt = (row.get("father") or row.get("mother") or "").strip()
            if not nxt:
                print(f"  gen {gen}  line ends - no parent recorded on our side")
                break
            cur = nxt
        print()

    print("across these lines:", ", ".join(f"{k} {v}" for k, v in tally.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
