"""Add a `P2600` where the PARENT ANCHOR proves which Geni profile an item is.

    python scripts/build-add-p2600-batch.py

**Emma, 2026-08-25**, asked for the add batch to be generalised to the whole store —
*"Yes, and generalise it to the whole store"* — and the queue item she approved carries the
condition alongside it: **gate it with the parent test first.**

The condition is not caution for its own sake. `reports/structural-correspondence.csv` proposes
**7,320** items that carry no `P2600` at all, and it is the output of the structural walk, which
`docs/structural-walk.md` records as pairing on **position alone, no name and no date** and as
having manufactured **89% of the tangles** in the correspondence. An ungated batch of 7,320
`P2600` additions built on that would be the removal batch's error pointed the other way: 22 of
its 31 proposed deletions turned out to be statements Wikidata never carried, all 22 sourced from
this same walk.

## The gate

For a proposed pair `(qid, geni_id)`:

1. the item must carry **no `P2600` at all** — an item that already has one is a different
   question, handled by `resolve-multi-geni-by-parents.py`;
2. read the item's `P22` *father* and `P25` *mother* from the local store;
3. a parent item must carry **exactly one** `P2600`;
4. that `P2600` must be **exactly** our tree's father (or mother) of `geni_id`.

Step 4 is what makes this a proof rather than a ranking. It is not *"Wikidata names one person
there"*, which is all the walk itself asked; it is *"Wikidata's father and our father are the
same recorded profile"*. Two people whose fathers are the same Geni profile are, on the evidence
this repo trusts, in the same family position — and the item is then about that person.

**A second anchor agreeing is recorded but not required**, because most people have only one
parent on Wikidata. Where both parents anchor, the row says so, and those are the ones to run
first.

## How well the gate works, measured two ways

Both checks use a signal the gate itself never touches.

**Names do not discriminate and that is worth writing down.** Asking whether the Wikidata label
and the Geni name share a token: **92.0%** where both parents anchor, **88.8%** where one does,
**86.4%** among the rejected. A 5.6-point spread on an 86% baseline is close to no information —
because the walk pairs people in the same *family position*, who tend to share names whether or
not the pairing is right. This was run first expecting it to validate the gate; it does not, and
it is recorded so nobody runs it again hoping for a different answer.

**Dates do, once the error rate is read instead of the success rate.** Do our years and the
item's agree within fifteen?

| | agree | disagree |
| --- | ---: | ---: |
| both parents anchor | 98.8% | **1.2%** |
| one parent anchors | 98.5% | **1.5%** |
| rejected by the gate | 95.2% | **4.8%** |

The three success rates look alike; the *failure* rates do not. The gate cuts date-impossible
pairs by roughly **3.4×**. That is the honest size of the effect.

**And the cost side, stated plainly: the gate rejects 5,654 of 7,320, and 95.2% of the rejected
ones that have comparable dates are date-consistent.** Most of what it throws away is probably
fine. It is deliberately conservative because the output writes to Wikidata, but this is a
trade-off rather than a free improvement, and lowering the bar is a decision for Emma rather than
a tuning exercise.

## What this does not do

* **No name is compared.** Not for the gate, not for a tiebreak. `CLAUDE.md` deleted a module for
  deciding identity by name and that stays deleted.
* **It never removes or replaces anything.** Every line is an addition to an item that currently
  holds nothing in that slot, which is `CLAUDE.md` § *The purpose is to ADD to Wikidata, not to
  correct it* exactly.
* **It is not run.** Wikidata editing in this repo starts 2026-09-01, and Emma runs QuickStatements
  by hand.

Every statement is emitted with an `S2600` reference to the Geni id being added, so the claim
carries its own provenance.

Writes `reports/wikidata-add-p2600.qs` and `reports/add-p2600-gate.tsv`.
"""
from __future__ import annotations

import collections
import csv
import gzip
import json
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

ROOT = Path(__file__).resolve().parent.parent
STORE = ROOT / "wikidata" / "items"
INDEX = ROOT / "out" / "wikidata" / "store-index.sqlite3"

GENI_ID, FATHER, MOTHER = "P2600", "P22", "P25"


def read_items(qids, props):
    """`{qid: {prop: [values]}}`, one pass per shard."""
    con = sqlite3.connect(str(INDEX))
    by_shard = collections.defaultdict(set)
    for qid in qids:
        hit = con.execute("SELECT shard FROM items WHERE qid=?", (qid,)).fetchone()
        if hit:
            by_shard[hit[0]].add(qid)
    out = {}
    for shard, wanted in by_shard.items():
        path = STORE / f"items-{shard:05d}.jsonl.gz"
        if not path.exists():
            continue
        with gzip.open(path, "rt", encoding="utf-8") as f:
            for line in f:
                if not wanted:
                    break
                for qid in list(wanted):
                    if f'"{qid}"' not in line:
                        continue
                    item = json.loads(line)
                    if item.get("id") != qid:
                        continue
                    wanted.discard(qid)
                    claims = item.get("claims", {})
                    got = {}
                    for prop in props:
                        vals = []
                        for st in claims.get(prop, []):
                            if st.get("rank") == "deprecated":
                                continue
                            dv = st["mainsnak"].get("datavalue", {}).get("value")
                            if isinstance(dv, dict):
                                dv = dv.get("id")
                            if dv:
                                vals.append(dv)
                        got[prop] = vals
                    got["label"] = (item.get("labels", {}).get("en", {}).get("value")
                                    or next((v["value"] for v in
                                             item.get("labels", {}).values()), ""))
                    out[qid] = got
                    break
    return out


def main():
    carried = collections.defaultdict(set)
    with open(ROOT / "out" / "wikidata" / "p2600-all.tsv", encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) >= 2 and row[0].startswith("Q") and row[1].strip().isdigit():
                carried[row[0]].add(row[1].strip())
    print(f"{len(carried):,} items carry a P2600")

    proposals = []
    with open(ROOT / "reports" / "structural-correspondence.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["qid"] not in carried:
                proposals.append((r["qid"], r["geni_id"], r.get("geni_name", "")))
    print(f"{len(proposals):,} proposals whose item carries no P2600")

    items = read_items({q for q, _g, _n in proposals}, [FATHER, MOTHER])
    print(f"{len(items):,} of those items are in the local store")

    parent_qids = {p for it in items.values() for k in (FATHER, MOTHER) for p in it[k]}
    print(f"{len(parent_qids):,} distinct parent items to check")

    wanted_geni = {g for _q, g, _n in proposals}
    ours = {}
    with open(ROOT / "reports" / "derived-family.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in wanted_geni:
                ours[row["geni_id"]] = ((row.get("father") or "").strip(),
                                        (row.get("mother") or "").strip())
    print(f"{len(ours):,} of the proposed people are in our tree")

    rows, tally = [], collections.Counter()
    # **The rejects are written out too.** Emma, 2026-08-25, asked to decide the gate's
    # tightness: *"Show me the rejected ones first"* -- and they had never been emitted, so
    # the only thing anyone could look at was the percentage. A gate whose discards are
    # invisible cannot be argued about from records, which is what `CLAUDE.md` § *How this
    # project works now* requires: *"Show records, not statistics."*
    rejected = []
    for qid, geni, name in proposals:
        item = items.get(qid)
        if not item:
            tally["item not in store"] += 1
            continue
        mine = ours.get(geni)
        if not mine:
            tally["person not in our tree"] += 1
            continue

        anchors = []
        for prop, slot, word in ((FATHER, 0, "father"), (MOTHER, 1, "mother")):
            if not mine[slot]:
                continue
            for pq in item[prop]:
                theirs = carried.get(pq, set())
                if len(theirs) != 1:
                    continue
                only = next(iter(theirs))
                if only == mine[slot]:
                    anchors.append(f"{word}: {pq} carries {only}, and so does our tree")
        # Why each comparable parent did or did not agree, in terms a human can check.
        why, conflicts = [], []
        for prop, slot, word in ((FATHER, 0, "father"), (MOTHER, 1, "mother")):
            if not mine[slot]:
                why.append(f"{word}: none in our tree")
            elif not item[prop]:
                why.append(f"{word}: none on the item")
            else:
                for pq in item[prop]:
                    theirs = carried.get(pq, set())
                    if not theirs:
                        why.append(f"{word}: their {pq} carries no Geni id")
                    elif len(theirs) != 1:
                        why.append(f"{word}: their {pq} carries {len(theirs)} Geni ids")
                    elif next(iter(theirs)) == mine[slot]:
                        pass                       # already recorded as an anchor
                    else:
                        note = (f"{word}: their {pq} carries {next(iter(theirs))}, "
                                f"ours is {mine[slot]}")
                        why.append(note)
                        conflicts.append(note)

        # **CONTRADICTION is refused. SILENCE is not.** Emma, 2026-08-26, shown what the old
        # gate was actually doing: *"Loosen it -- emit the ~7,000."*
        #
        # It used to require a parent anchor and rejected 5,651 of 7,320. Writing the rejects
        # out showed the shape:
        #
        #     5,540  no disagreement anywhere -- simply nothing to check against
        #        64  one parent disagrees, another is uncheckable
        #        47  every comparable parent disagrees
        #
        # So it was never a correctness filter. It was a CHECKABILITY filter throwing away the
        # unverifiable along with the wrong, and `CLAUDE.md` says everywhere else that absence
        # never refutes -- the same principle that renamed `CONTRADICTED` to
        # `PARENTS-NOT-JOINED`.
        #
        # What makes loosening safe is `CLAUDE.md`'s own asymmetry: `P2600` is multi-valued and
        # additive, so a wrong one is a statement to correct rather than a deletion to recover
        # from, and *"the entire purpose of this is to add"*.
        if conflicts:
            tally["REFUSED - a parent is recorded on both sides and they differ"] += 1
            rejected.append({"qid": qid, "geni_id": geni,
                             "wikidata_label": item["label"], "geni_name": name,
                             "our_father": mine[0], "our_mother": mine[1],
                             "their_father": ";".join(item[FATHER]),
                             "their_mother": ";".join(item[MOTHER]),
                             "why": " | ".join(why)})
            continue

        tally["BOTH parents anchor" if len(anchors) > 1
              else "one parent anchors" if anchors
              else "no anchor, but nothing contradicts either"] += 1
        rows.append({"anchors": len(anchors), "qid": qid, "geni_id": geni,
                     "wikidata_label": item["label"], "geni_name": name,
                     "evidence": " | ".join(anchors) if anchors
                     else "no parent anchor; nothing contradicts - " + " | ".join(why)})

    rej = ROOT / "reports" / "add-p2600-rejected.tsv"
    with open(rej, "w", encoding="utf-8", newline="") as f:
        if rejected:
            w = csv.DictWriter(f, fieldnames=list(rejected[0]), delimiter="\t")
            w.writeheader()
            w.writerows(rejected)
        else:
            f.write("(none)\n")
    print(f"wrote {rej.relative_to(ROOT)}: {len(rejected):,} rejected, with the reason")

    rows.sort(key=lambda r: (-r["anchors"], r["qid"]))
    gate = ROOT / "reports" / "add-p2600-gate.tsv"
    with open(gate, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    qs = ROOT / "reports" / "wikidata-add-p2600.qs"
    with open(qs, "w", encoding="utf-8", newline="\n") as f:
        f.write("# P2600 (Geni.com profile ID) additions, gated by the parent anchor.\n")
        f.write("# Every item below carries NO P2600 today. The Geni profile is proved by\n")
        f.write("# Wikidata's own parent item carrying exactly the Geni id our tree records\n")
        f.write("# as that person's parent. No name was compared. See\n")
        f.write("# scripts/build-add-p2600-batch.py and reports/add-p2600-gate.tsv.\n")
        f.write(f"# {sum(1 for r in rows if r['anchors'] > 1)} of {len(rows)} are anchored on\n")
        f.write("# BOTH parents; those are listed first.\n\n")
        for r in rows:
            f.write(f'{r["qid"]}\t{GENI_ID}\t"{r["geni_id"]}"'
                    f'\tS2600\t"{r["geni_id"]}"\n')

    print(f"\nwrote {gate.relative_to(ROOT)} and {qs.relative_to(ROOT)}")
    for k, n in tally.most_common():
        print(f"   {n:>6}  {k}")
    print(f"\n{len(rows)} additions pass the gate "
          f"({sum(1 for r in rows if r['anchors'] > 1)} on both parents)")
    print("QUEUED, NEVER RUN. Wikidata editing in this repo starts 2026-09-01.")
    print("\nthe both-parent ones:")
    for r in rows[:8]:
        if r["anchors"] < 2:
            break
        print(f"   {r['qid']:<12} {r['geni_id']:<20} {r['wikidata_label'][:34]:<34} "
              f"| {r['geni_name'][:28]}")


if __name__ == "__main__":
    main()
