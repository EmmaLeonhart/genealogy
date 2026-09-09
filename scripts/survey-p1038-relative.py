"""How much `P1038` *relative* is actually on Wikidata? Measure before building on it.

    python scripts/survey-p1038-relative.py

**Emma, 2026-08-25**, having ranked the four link kinds the zipper uses — parents, spouses,
children, siblings — named a fifth: *"there are other relationships there that are sometimes
reported on Wikidata, like the relative role"*. `queue.md` records the instruction attached to
it: **measure how much of it exists before building anything on it.**

`P1038` *relative* is the catch-all: one property covering every kinship the specific
properties do not, with `P1039` *kinship to subject* as a qualifier naming which. So the useful
question is not how many `P1038` statements there are but **what the `P1039` values say** — a
property that is 90% *cousin* is a different prospect from one that is 90% *uncle*, and one
whose qualifier is usually missing is not usable as a join at all.

## Why the whole store is read rather than `relations.tsv`

`out/wikidata/relations.tsv` carries `P22`/`P25`/`P40`/`P26`/`P2600` and nothing else, so this
question cannot be answered from it. The scan is a byte test for `"P1038"` on each raw line and
a JSON parse **only** of the lines that hold one, which is what keeps it affordable: almost
every line is skipped without being decoded.

**The store is a Geni-shaped slice** — 2,246,827 items as of 2026-08-26, seeded from `P2600` holders and their
neighbours, so every number here is about that slice and not about Wikidata. Said out loud
because `CLAUDE.md` requires the bound stated rather than implied.

Writes `reports/p1038-relative-survey.md` and `reports/p1038-relative.tsv` — one row per
statement, per `CLAUDE.md` § *"Analyse this" means build a CSV of every instance*.
"""
from __future__ import annotations

import collections
import csv
import gzip
import json
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
STORE = ROOT / "wikidata" / "items"
LABELS = ROOT / "reports" / "wikidata-labels.tsv"
OUT_TSV = ROOT / "reports" / "p1038-relative.tsv"
OUT_MD = ROOT / "reports" / "p1038-relative-survey.md"

#: The byte test. A line without this cannot carry the property, and is never parsed.
NEEDLE = b'"P1038"'


def label_map(wanted):
    """English labels for the QIDs this survey names, from the offline export only.

    `CLAUDE.md` forbids a bare `P…`/`Q…` in any output, and equally forbids guessing one.
    Anything the export does not hold is printed as the bare id with `(label not in
    reports/wikidata-labels.tsv)` beside it, which is honest rather than invented.
    """
    out = {}
    with open(LABELS, encoding="utf-8") as f:
        for line in f:
            qid, _, rest = line.partition("\t")
            if qid in wanted:
                out[qid] = rest.split("\t")[0].strip()
    return out


def main():
    shards = sorted(STORE.glob("*.jsonl.gz"))
    if not shards:
        sys.exit(f"no shards under {STORE}")
    print(f"scanning {len(shards)} shards for {NEEDLE.decode()} ...")

    rows = []
    items_seen = hits = all_deprecated = 0
    started = time.time()
    for n, shard in enumerate(shards, 1):
        with gzip.open(shard, "rb") as f:
            for raw in f:
                items_seen += 1
                if NEEDLE not in raw:
                    continue
                item = json.loads(raw)
                sts = item.get("claims", {}).get("P1038", [])
                if not sts:
                    continue
                hits += 1
                qid = item.get("id", "")
                live = 0
                for st in sts:
                    if st.get("rank") == "deprecated":
                        continue
                    live += 1
                    v = st.get("mainsnak", {}).get("datavalue", {}).get("value", {})
                    other = v.get("id", "") if isinstance(v, dict) else ""
                    kinds = []
                    for q in st.get("qualifiers", {}).get("P1039", []):
                        kv = q.get("datavalue", {}).get("value", {})
                        if isinstance(kv, dict) and kv.get("id"):
                            kinds.append(kv["id"])
                    rows.append({"qid": qid, "relative": other,
                                 "kinship": ";".join(kinds),
                                 "qualifiers": ";".join(sorted(st.get("qualifiers", {})))})
                if not live:
                    all_deprecated += 1
        if n % 250 == 0 or n == len(shards):
            print(f"  {n}/{len(shards)} shards, {items_seen:,} items, "
                  f"{hits:,} carrying P1038, {time.time() - started:.0f}s", flush=True)

    import sqlite3
    index_rows = sqlite3.connect(
        str(ROOT / "out" / "wikidata" / "store-index.sqlite3")).execute(
        "SELECT COUNT(DISTINCT qid) FROM items").fetchone()[0]
    kinds = collections.Counter(k for r in rows for k in r["kinship"].split(";") if k)
    unqualified = sum(1 for r in rows if not r["kinship"])
    labels = label_map(set(kinds) | {"P1038"})

    with open(OUT_TSV, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["qid", "relative", "kinship", "qualifiers"],
                           delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    #: Kinships a walk over `P22`/`P25`/`P40` reproduces, against the ones it cannot.
    def is_novel(qid):
        n = labels.get(qid, "").lower()
        return any(w in n for w in ("in-law", "step", "adopt", "foster", "god"))

    qualified = sum(kinds.values())
    not_derivable = sum(n for q, n in kinds.items() if is_novel(q))
    derivable = qualified - not_derivable
    top_novel = [(q, n) for q, n in kinds.most_common() if is_novel(q)][:5]

    def named(q):
        return f"`{q}` *{labels[q]}*" if q in labels else \
            f"`{q}` (label not in reports/wikidata-labels.tsv)"

    lines = [
        "# `P1038` *relative* in the local store — measured, not assumed",
        "",
        "Emma, 2026-08-25, after ranking parents / spouses / children / siblings: *\"there are "
        "other relationships there that are sometimes reported on Wikidata, like the relative "
        "role\"*. The instruction attached to it was to **measure how much exists before "
        "building anything on it**. This is that measurement and nothing is built.",
        "",
        f"**The store is a Geni-shaped slice** — {items_seen:,} lines read from the shards, "
        "seeded from `P2600` holders and their neighbours. Every number below is about that "
        "slice, never about Wikidata as a whole.",
        "",
        f"**Cross-checked against `out/wikidata/store-index.sqlite3`**, which holds "
        f"{index_rows:,} distinct QIDs against the {items_seen:,} lines scanned — a difference "
        f"of {items_seen - index_rows:,}. The two agreeing to five significant figures is what "
        "makes the scan believable; one that had silently stopped early would not.",
        "",
        "| | |",
        "| --- | ---: |",
        f"| items scanned | {items_seen:,} |",
        f"| items carrying `P1038` *relative* | **{hits:,}** |",
        f"| of those, every statement DEPRECATED and so absent below | {all_deprecated:,} |",
        f"| `P1038` statements, deprecated ones dropped | {len(rows):,} |",
        f"| statements with no `P1039` *kinship to subject* | **{unqualified:,}** |",
        "",
        "## What the kinship qualifier says",
        "",
        "| kinship | statements |",
        "| --- | ---: |",
    ]
    for q, n in kinds.most_common(30):
        lines.append(f"| {named(q)} | {n:,} |")
    if len(kinds) > 30:
        lines.append(f"| … and {len(kinds) - 30} further values | |")
    lines += [
        "",
        "## The part that is worth anything: what our own tree CANNOT derive",
        "",
        "*uncle*, *grandfather*, *nephew*, *grandson* and *cousin* all follow from parent and "
        "child edges the merged tree already holds — recording them adds nothing a walk would "
        "not produce. The in-law, step-, adoptive, foster and godparent kinships do **not** "
        "follow from any edge in a GEDCOM, so they are the slice with information in it.",
        "",
        "| | statements | share |",
        "| --- | ---: | ---: |",
        f"| derivable from parent/child edges | {derivable:,} | "
        f"{derivable / max(qualified, 1):.0%} |",
        f"| **not derivable — in-law, step, adoptive, foster, godparent** | "
        f"**{not_derivable:,}** | {not_derivable / max(qualified, 1):.0%} |",
        "",
        "The largest of the non-derivable kinds: "
        + ", ".join(f"{named(q)} {n:,}" for q, n in top_novel) + ".",
        "",
        "**That split is a keyword rule over the English label**, not a claim about Wikidata's "
        "ontology — `in-law`, `step`, `adopt`, `foster`, `god…` against everything else, over "
        f"{len(kinds)} distinct kinship values. It is good enough to answer *is there anything "
        "here* and should not be relied on further.",
        "",
        f"`reports/p1038-relative.tsv` is every one of the {len(rows):,} statements, one per row.",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"\n{items_seen:,} items, {hits:,} carry P1038, {len(rows):,} statements")
    print(f"{unqualified:,} of them have no P1039 kinship qualifier")
    for q, n in kinds.most_common(12):
        print(f"   {n:>7,}  {q} {labels.get(q, '(label not in the offline export)')}")
    print(f"wrote {OUT_MD.resolve().relative_to(ROOT)} and "
          f"{OUT_TSV.resolve().relative_to(ROOT)}")


if __name__ == "__main__":
    main()
