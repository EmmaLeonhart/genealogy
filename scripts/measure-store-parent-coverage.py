"""How often is an item's parent on Wikidata missing from our local store?

**Emma's question, 2026-08-15:** *"I was under the assumption that, because of the
fact that we did such a large amount of wikidata exports, we would have
effectively covered the entirety of the wikidata network that would ever run into
this issue… How pervasive is this issue where, say, ancestors on wikidata are not
covered or are not imported? My impression was it was pretty much entirely
20th-century people who are not like this."*

It came out of the structural walk, where 91 of 3,668 correspondences could not be
labelled because the parent item was not held. That is a symptom; this measures
the thing itself.

**The measurement.** One streaming pass over all 1,424 shards. For every item,
take its `P22` father and `P25` mother. A parent is **missing** when that QID is
not itself an item in the store. Every missing one is a row in
`reports/store-parent-coverage.csv`.

**Dating a missing parent uses the CHILD's date, and that is the only honest
option.** We do not hold the parent — that is what missing means — so the parent
has no date to read. The child's `P569` is the proxy, and it is a *lower* bound
on the parent's era rather than an estimate of it: a parent of somebody born 1950
belongs to the 20th century, a parent of somebody born 1200 does not. That is
exactly the resolution Emma's question needs, and no date is ever inferred for
the parent itself.

**Undated children are reported as their own bucket, never distributed.** They
are a large share and quietly folding them into the dated distribution would
manufacture whatever answer the dated part already suggested.

    py scripts/measure-store-parent-coverage.py
"""

from __future__ import annotations

import csv
import gzip
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from genimerge.matching import year_of  # noqa: E402

ITEMS = REPO / "wikidata" / "items"
OUT_CSV = REPO / "reports" / "store-parent-coverage.csv"
OUT_MD = REPO / "reports" / "store-parent-coverage.md"

FATHER, MOTHER, BIRTH = "P22", "P25", "P569"


def claims_of(entity: dict, prop: str) -> list[str]:
    """Item-valued claim targets, mainsnak only.

    Qualifiers carry a lot in this project (`CLAUDE.md` § *Reading a Wikidata
    statement*) but the question here is only *which item is named in the parent
    position*, which is the mainsnak.
    """
    out = []
    for claim in (entity.get("claims") or {}).get(prop, []):
        snak = claim.get("mainsnak") or {}
        if snak.get("snaktype") != "value":
            continue
        value = (snak.get("datavalue") or {}).get("value")
        if isinstance(value, dict) and value.get("id"):
            out.append(value["id"])
    return out


def birth_year(entity: dict) -> int | None:
    for claim in (entity.get("claims") or {}).get(BIRTH, []):
        snak = claim.get("mainsnak") or {}
        if snak.get("snaktype") != "value":
            continue
        value = (snak.get("datavalue") or {}).get("value")
        if isinstance(value, dict):
            year = year_of(value.get("time"))
            if year is not None:
                return year
    return None


def label_of(entity: dict) -> str:
    labels = entity.get("labels") or {}
    for lang in ("en", "mul"):
        if lang in labels:
            return (labels[lang] or {}).get("value", "") or ""
    for value in labels.values():
        got = (value or {}).get("value", "")
        if got:
            return got
    return ""


def bucket(year: int | None) -> str:
    if year is None:
        return "no birth date"
    if year < 0:
        return "BCE"
    return f"{(year // 100) * 100 + 1}s"


def main() -> int:
    shards = sorted(ITEMS.glob("*.jsonl.gz"))
    if not shards:
        print("no shards under wikidata/items/", file=sys.stderr)
        return 1
    print(f"streaming {len(shards):,} shards", flush=True)

    held: set[str] = set()
    #: parent qid -> list of (child qid, child year, child label, position)
    edges: list[tuple[str, str, int | None, str, str]] = []

    for n, shard in enumerate(shards, 1):
        with gzip.open(shard, "rt", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    entity = json.loads(line)
                except json.JSONDecodeError:
                    continue
                qid = entity.get("id")
                if not qid:
                    continue
                held.add(qid)
                fathers = claims_of(entity, FATHER)
                mothers = claims_of(entity, MOTHER)
                if not fathers and not mothers:
                    continue
                year = birth_year(entity)
                label = label_of(entity)
                for parent in fathers:
                    edges.append((parent, qid, year, label, "father"))
                for parent in mothers:
                    edges.append((parent, qid, year, label, "mother"))
        if n % 200 == 0:
            print(f"  {n:,}/{len(shards):,} shards, {len(held):,} items, "
                  f"{len(edges):,} parent statements", flush=True)

    print(f"\n{len(held):,} items in the store")
    print(f"{len(edges):,} parent statements (P22 + P25)")

    missing = [e for e in edges if e[0] not in held]
    print(f"{len(missing):,} of them point at an item the store does NOT hold")

    distinct_missing = {e[0] for e in missing}
    print(f"{len(distinct_missing):,} distinct missing parents")

    # Per child: does it have a complete set of recorded parents?
    children = defaultdict(lambda: [0, 0])
    for parent, child, _year, _label, _pos in edges:
        children[child][0] += 1
        if parent not in held:
            children[child][1] += 1
    incomplete = sum(1 for v in children.values() if v[1])
    print(f"{incomplete:,} of {len(children):,} items with a recorded parent "
          f"have at least one we do not hold")

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["missing_parent_qid", "position", "child_qid",
                         "child_label", "child_birth_year", "child_century"])
        for parent, child, year, label, pos in sorted(missing):
            writer.writerow([parent, pos, child, label,
                             "" if year is None else year, bucket(year)])
    print(f"\nwrote {OUT_CSV} ({len(missing):,} rows)")

    # -- the distribution, which is the actual question --------------------
    by_bucket_missing: Counter[str] = Counter()
    by_bucket_all: Counter[str] = Counter()
    for parent, child, year, label, pos in edges:
        b = bucket(year)
        by_bucket_all[b] += 1
        if parent not in held:
            by_bucket_missing[b] += 1

    def order(key: str) -> tuple[int, int]:
        if key == "BCE":
            return (0, 0)
        if key == "no birth date":
            return (2, 0)
        return (1, int(key.rstrip("s").rstrip("1") or 0))

    L: list[str] = []
    add = L.append
    add("# Are the parents on Wikidata actually in our store?")
    add("")
    add("**Emma, 2026-08-15:** *\"I was under the assumption that… we would have")
    add("effectively covered the entirety of the wikidata network that would ever run")
    add("into this issue… My impression was it was pretty much entirely 20th-century")
    add("people who are not like this.\"*")
    add("")
    add("Every missing parent is a row in `reports/store-parent-coverage.csv`.")
    add("")
    add("## The answer")
    add("")
    add(f"- **{len(held):,}** items in the store")
    add(f"- **{len(edges):,}** parent statements (`P22` + `P25`) across them")
    add(f"- **{len(missing):,}** point at an item the store does not hold "
        f"(**{100.0*len(missing)/max(len(edges),1):.1f}%**)")
    add(f"- **{len(distinct_missing):,}** distinct people are named as a parent and "
        "not held")
    add(f"- **{incomplete:,}** of **{len(children):,}** items with any recorded parent "
        f"are missing at least one (**{100.0*incomplete/max(len(children),1):.1f}%**)")
    add("")
    add("## By the CHILD's century")
    add("")
    add("**The child's date, not the parent's** — we do not hold the parent, so the")
    add("parent has no date to read. This is a *lower bound* on the parent's era, not")
    add("an estimate of it: a missing parent of somebody born 1950 is a 20th-century")
    add("case, a missing parent of somebody born 1200 is not. No date is inferred.")
    add("")
    add("| child's century | parent statements | missing | missing rate |")
    add("| --- | ---: | ---: | ---: |")
    for key in sorted(by_bucket_all, key=order):
        total, miss = by_bucket_all[key], by_bucket_missing[key]
        add(f"| {key} | {total:,} | {miss:,} | {100.0*miss/max(total,1):.1f}% |")
    add("")
    add("Undated children are their own row and are never distributed across the")
    add("dated ones — they are a large share, and folding them in would manufacture")
    add("whatever the dated part already suggested.")
    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {OUT_MD}")

    print("\nby the child's century:")
    for key in sorted(by_bucket_all, key=order):
        total, miss = by_bucket_all[key], by_bucket_missing[key]
        print(f"  {key:<14} {total:>9,} statements  {miss:>8,} missing  "
              f"{100.0*miss/max(total,1):>5.1f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
