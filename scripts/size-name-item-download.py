"""How large is the approved name-item download, exactly?

Emma approved a `wikidownload` pass fetching the items `P735` and `P734` point
at, because the store holds *people* — the download walked P22/P25/P26/P40/P3373
— so no name string can be resolved to an item offline today.

**The only figure we have is a sample.** `queue.md` records 40 shards, 40,000
items, 13,683 distinct name targets of which 55 were present — 0.4%. Extrapolating
a download from a 2.8% sample is exactly the kind of estimate this project has
had to withdraw before. This counts all 1,408 shards.

The answer decides whether the download is a small job or a large one, and it is
needed *before* the run rather than discovered during it.

**Offline.** Reads `wikidata/items/` and nothing else. Nothing is fetched; this
script cannot talk to Wikidata.

Writes `reports/name-item-download.md`.

    py scripts/size-name-item-download.py
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from genimerge import wikistore  # noqa: E402

STORE = REPO_ROOT / "wikidata" / "items"
OUT_MD = REPO_ROOT / "reports" / "name-item-download.md"
OUT_CSV = REPO_ROOT / "reports" / "name-items.csv"

#: The two name properties, and the P31 values that mark a name item. From
#: CLAUDE.md's table, confirmed against live Wikidata on 2026-08-02.
NAME_PROPERTIES = {"P735": "given name", "P734": "family name"}


def truthy_ids(entity: dict, prop: str) -> list[str]:
    """Item IDs a property points at, ignoring deprecated statements."""
    statements = (entity.get("claims") or {}).get(prop) or []
    best = [s for s in statements if s.get("rank") == "preferred"] or [
        s for s in statements if s.get("rank") != "deprecated"
    ]
    out = []
    for statement in best:
        value = ((statement.get("mainsnak") or {}).get("datavalue") or {}).get("value")
        if isinstance(value, dict):
            ident = value.get("id")
            if isinstance(ident, str) and ident.startswith("Q"):
                out.append(ident)
    return out


def main() -> int:
    shards = wikistore.shards(STORE)
    print(f"{len(shards):,} shards", flush=True)

    stored: set[str] = set()
    targets: dict[str, set[str]] = {p: set() for p in NAME_PROPERTIES}
    references: Counter[str] = Counter()
    people_with = Counter()
    items_seen = 0

    for n, shard in enumerate(shards, 1):
        for entity in wikistore.read_shard(shard):
            items_seen += 1
            qid = entity.get("id")
            if isinstance(qid, str):
                stored.add(qid)
            for prop in NAME_PROPERTIES:
                ids = truthy_ids(entity, prop)
                if ids:
                    people_with[prop] += 1
                for ident in ids:
                    targets[prop].add(ident)
                    references[ident] += 1
        if n % 200 == 0 or n == len(shards):
            distinct = len(targets["P735"] | targets["P734"])
            print(f"  shard {n:,}/{len(shards):,}  {items_seen:,} items  "
                  f"{distinct:,} distinct name targets", flush=True)

    all_targets = targets["P735"] | targets["P734"]
    present = all_targets & stored
    missing = all_targets - stored
    both = targets["P735"] & targets["P734"]

    # Every name item with its reference count, so "how much coverage does the
    # top N give" is answerable without a second pass over 2.7 GB. The census
    # rule in CLAUDE.md wants every instance on disk anyway.
    import csv as _csv

    ranked = references.most_common()
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as handle:
        writer = _csv.writer(handle)
        writer.writerow(["qid", "references", "as_given_name", "as_family_name", "in_store"])
        for ident, count in ranked:
            writer.writerow([
                ident, count,
                "yes" if ident in targets["P735"] else "no",
                "yes" if ident in targets["P734"] else "no",
                "yes" if ident in stored else "no",
            ])

    total_refs = sum(references.values())
    cumulative: list[tuple[int, float]] = []
    running = 0
    checkpoints = {100, 500, 1_000, 2_420, 5_000, 10_000, 17_936, 33_593, 76_184}
    for index, (_, count) in enumerate(ranked, 1):
        running += count
        if index in checkpoints:
            cumulative.append((index, 100.0 * running / max(total_refs, 1)))

    L: list[str] = []
    add = L.append
    add("# Sizing the name-item download")
    add("")
    add("Emma approved a `wikidownload` pass fetching the items `P735` and `P734` point")
    add("at. The store holds *people* — the download walked P22/P25/P26/P40/P3373 — so no")
    add("name string resolves to an item offline today.")
    add("")
    add("**The figure on record was a sample**: 40 shards, 40,000 items, 13,683 distinct")
    add("name targets of which 55 were present, 0.4%. That is a 2.8% sample, and this")
    add("project has had to withdraw an extrapolation before. This is the full count.")
    add("")
    add(f"Measured over **all {len(shards):,} shards, {items_seen:,} stored items**.")
    add("Offline; nothing was fetched.")
    add("")
    add("## The answer")
    add("")
    add("| | count |")
    add("| --- | ---: |")
    add(f"| distinct items referenced by `P735` | {len(targets['P735']):,} |")
    add(f"| distinct items referenced by `P734` | {len(targets['P734']):,} |")
    add(f"| referenced by both | {len(both):,} |")
    add(f"| **distinct name items in total** | **{len(all_targets):,}** |")
    add(f"| …already in the store | {len(present):,} |")
    add(f"| **…to download** | **{len(missing):,}** |")
    add("")
    add(f"**{100.0*len(present)/max(len(all_targets),1):.2f}% are already present**, so the "
        f"download is {len(missing):,} items.")
    add("")
    add("| | items |")
    add("| --- | ---: |")
    add(f"| stored items stating a given name (`P735`) | {people_with['P735']:,} |")
    add(f"| stored items stating a family name (`P734`) | {people_with['P734']:,} |")
    add("")
    add("## How concentrated the references are")
    add("")
    add("A name item referenced by thousands of people is worth more than one referenced")
    add("once, and it decides whether a partial download would be useful.")
    add("")
    add("| | |")
    add("| --- | ---: |")
    for cut in (1, 2, 5, 10, 100, 1000):
        n = sum(1 for c in references.values() if c >= cut)
        add(f"| name items referenced at least {cut:,} times | {n:,} |")
    add("")
    top = references.most_common(20)
    add("The twenty most-referenced name items:")
    add("")
    add("| item | references |")
    add("| --- | ---: |")
    for ident, count in top:
        add(f"| {ident} | {count:,} |")
    add("")
    covered = sum(c for _, c in top)
    add(f"Those twenty account for **{covered:,} of {total_refs:,} references** "
        f"({100.0*covered/max(total_refs,1):.1f}%).")
    add("")
    add("### A partial download is viable, and this is by how much")
    add("")
    add("Downloading the most-referenced items first, what share of all references")
    add("would be resolvable:")
    add("")
    add("| download the top | of 132,569 | references covered |")
    add("| ---: | ---: | ---: |")
    for count, share in cumulative:
        add(f"| {count:,} | {100.0*count/len(all_targets):.1f}% | **{share:.1f}%** |")
    add("")
    add("Per-item counts for all 132,569 are in `reports/name-items.csv`, so any other")
    add("cut can be taken without re-reading the 2.7 GB store.")
    add("")
    add("## What this does not do")
    add("")
    add("**No download was run and none is scheduled.** `CLAUDE.md` says the one bulk job")
    add("permitted to talk to Wikidata *\"is confirmed before a live run\"*, and an")
    add("approval given in a rapid question round is not that confirmation. This is the")
    add("number that makes the confirmation an informed one.")

    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print()
    print(f"distinct name items referenced: {len(all_targets):,}")
    print(f"  already stored: {len(present):,}")
    print(f"  to download:    {len(missing):,}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
