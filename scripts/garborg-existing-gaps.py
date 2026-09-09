"""What the Garborg people who ALREADY have items are missing on Wikidata.

    python scripts/garborg-existing-gaps.py

Emma, 2026-08-24, answering whether to add properties to items that already exist:
**yes**. The daily batch only ever closed *links* between existing items — the
reciprocal `P40` and the `P3373` among siblings — and never asked whether an item that
exists is missing a date, a sex, a name statement or a label in another language.

Two very different sources of truth, and the difference matters:

* **Items in the local store** (`Q467497` *Arne Garborg* and the other long-standing
  ones) can be read exactly, offline. `CLAUDE.md`: *"Every question about Wikidata's
  contents is answered offline, against the local store."*
* **Items Emma created herself** in the last two days are **not** in the store, which
  was downloaded before they existed. What they hold is whatever their `CREATE` block
  carried, and that is knowable from the batch — but only approximately, because she
  ran *some* of the file: *"I only ran some of the quick statements because many of
  them required links that couldn't exist."*

So this report states, per person, which of the two it is. An unknown is reported as
unknown rather than assumed empty.

**The label rule that comes out of this, and it is the reason to measure before
emitting.** `Len` on an existing item **replaces** its label. `Q467497` is labelled
*Arne Garborg* on Wikidata and our derived label is *Aadne (Arne) Eivindson Garborg* --
emitting ours would overwrite the better one with a Geni display string. So a label is
only ever added in a language the item does **not** have.

Writes `reports/garborg-existing-gaps.tsv`.
"""
from __future__ import annotations

import csv
import gzip
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
csv.field_size_limit(1 << 30)
sys.stdout.reconfigure(encoding="utf-8")

from namemodel import classify  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
STORE = ROOT / "wikidata" / "items"
INDEX = ROOT / "out" / "wikidata" / "store-index.sqlite3"

#: Properties the Geni tree can support, with their English labels, per `CLAUDE.md`
#: § *Always write the English label next to a property or item ID*.
WATCHED = [
    ("P31", "instance of"), ("P21", "sex or gender"), ("P2600", "Geni.com profile ID"),
    ("P569", "date of birth"), ("P570", "date of death"),
    ("P735", "given name"), ("P734", "family name"), ("P5056", "patronym or matronym"),
    ("P22", "father"), ("P25", "mother"), ("P26", "spouse"),
    ("P40", "child"), ("P3373", "sibling"),
]


def load_item(qid, con):
    row = con.execute("SELECT shard FROM items WHERE qid=?", (qid,)).fetchone()
    if not row:
        return None
    shard = STORE / f"items-{row[0]:05d}.jsonl.gz"
    if not shard.exists():
        return None
    needle = f'"{qid}"'
    with gzip.open(shard, "rt", encoding="utf-8") as f:
        for line in f:
            if needle in line:
                item = json.loads(line)
                if item.get("id") == qid:
                    return item
    return None


def existing_state(qids):
    """`{qid: (label languages, claim properties)}` for the items the store holds.

    A QID **absent from the result** is one the store has never seen. For the Garborg
    ledger that means Emma created it in the last two days, after the download — so
    what it holds is whatever our own batch wrote, which is knowable from the batch
    rather than from here. Callers must not read absence as "the item is empty".
    """
    # **The store index is gitignored, so a CI runner does not have it.** `CLAUDE.md` lists
    # `out/wikidata/store-index.sqlite3` among the files GitHub physically refuses, and
    # `sqlite3.connect` on a missing path silently CREATES an empty database rather than
    # raising — so the failure surfaced four steps later as `no such table: items` and killed
    # the 2026-09-01 21:50 pipeline run *after* it had already built the batch.
    #
    # **Returning `{}` is this function's own documented contract, not new behaviour.** The
    # docstring above says a QID absent from the result is one the store has never seen, and
    # both callers already handle exactly that: `absent()` returns True and emits a statement
    # QuickStatements merges away if redundant, and the label site reads `langs` from
    # `reports/garborg-live-labels.tsv` because the store predates every item Emma has made.
    # An offline enrichment that is unavailable must not fail a run that has its answer.
    if not INDEX.exists():
        print(f"WARNING: {INDEX} is absent — every item reads as 'not in the store', which is "
              "this function's documented unknown. Statements are emitted and merged; labels "
              "come from the live fetch.", file=sys.stderr)
        return {}
    con = sqlite3.connect(str(INDEX))
    try:
        con.execute("SELECT 1 FROM items LIMIT 1")
    except sqlite3.OperationalError as exc:
        print(f"WARNING: {INDEX} has no `items` table ({exc}) — treating the store as unseen.",
              file=sys.stderr)
        return {}
    out = {}
    for qid in qids:
        item = load_item(qid, con)
        if item:
            out[qid] = (set(item.get("labels", {})), set(item.get("claims", {})))
    return out


def main():
    # Run directly, this script IS the report and the store is its whole point — so unlike
    # `existing_state`, which is an optional enrichment inside a larger run, there is nothing
    # to degrade to. Say so and stop, rather than emitting a report of empty rows.
    if not INDEX.exists():
        print(f"{INDEX} is absent; this report reads the offline store and has nothing to say "
              "without it. Rebuild it with `genimerge.wikistore.build_index(STORE, INDEX)` — "
              "`scripts/import-item.py` calls it that way.",
              file=sys.stderr)
        return 1
    con = sqlite3.connect(str(INDEX))
    ledger = list(csv.DictReader(open(ROOT / "reports" / "garborg-qids.tsv",
                                      encoding="utf-8"), delimiter="\t"))

    labels, facts = {}, {}
    ids = {r["geni_id"] for r in ledger}
    with open(ROOT / "reports" / "derived-labels.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in ids:
                labels[row["geni_id"]] = row["label_en"] or row["label_mul"]
    with open(ROOT / "reports" / "derived-facts.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in ids:
                facts[row["geni_id"]] = row

    out = []
    for row in ledger:
        qid, geni = row["qid"], row["geni_id"]
        item = load_item(qid, con)
        known = "store" if item else "unknown - created after the download"
        have_props = set(item.get("claims", {})) if item else set()
        have_langs = set(item.get("labels", {})) if item else set()

        missing = [p for p, _lab in WATCHED if item and p not in have_props]
        # What the tree could supply for each, so a gap that we cannot fill is not
        # reported as one.
        f = facts.get(geni, {})
        supportable = set()
        if f.get("sex") in ("M", "F"):
            supportable.add("P21")
        if f.get("birth_date_iso"):
            supportable.add("P569")
        if f.get("death_date_iso"):
            supportable.add("P570")
        supportable |= {"P31", "P2600"}
        for _t, usage, _o in classify(labels.get(geni, "")):
            supportable.add({"given": "P735", "family": "P734",
                             "patronymic": "P5056"}[usage])

        fillable = sorted(set(missing) & supportable)
        out.append({
            "geni_id": geni,
            "qid": qid,
            "label": labels.get(geni, ""),
            "knowledge": known,
            "label_langs": len(have_langs) if item else "",
            "has_ja": "yes" if "ja" in have_langs else ("no" if item else ""),
            "has_zh": "yes" if "zh" in have_langs else ("no" if item else ""),
            "missing_and_fillable": " ".join(fillable),
            "missing_but_tree_is_silent": " ".join(sorted(set(missing) - supportable)),
        })

    dest = ROOT / "reports" / "garborg-existing-gaps.tsv"
    with open(dest, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]), delimiter="\t")
        w.writeheader()
        w.writerows(out)

    print(f"wrote {dest.relative_to(ROOT)}\n")
    for r in out:
        print(f"{r['qid']:<12} {r['label'][:34]:<34} {r['knowledge']}")
        if r["knowledge"] == "store":
            print(f"             langs={r['label_langs']} ja={r['has_ja']} zh={r['has_zh']}"
                  f"  fillable: {r['missing_and_fillable'] or '(none)'}")
    n = sum(1 for r in out if r["knowledge"] == "store")
    print(f"\n{n}/{len(out)} readable offline; the rest were created after the download")


if __name__ == "__main__":
    main()
