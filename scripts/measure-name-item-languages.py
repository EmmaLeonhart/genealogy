"""Which languages do the downloaded name items actually carry labels in?

**This is the ceiling on mechanical name translation.** *"there should
be a sizable amount of individuals for whom we're effectively able to just translate the
names, really, based off of the existing labels… I think in Japanese there's a standard
katakana rendering of the name Jack. There's a standard katakana rendering of the name
John."* If `John` (`Q4925477`) carries `ja` = ジョン, then a person called John gets a
Japanese label without anybody transliterating anything. If it does not, no amount of
assembling helps and the gap has to be filled by adding labels **to the name item**,
which is the second half of the target: labels in other languages have to be added to
the name objects.

So the question this answers is not "how many name items do we hold" — that is settled,
`scripts/collect-name-item-qids.py` enumerated 824,358 by `P31` and 99.9% are in the
store. It is **how many of them are usable in each target language**.

**Reads the local store only.** No Wikidata request is made or possible here; the shards
under `wikidata/items/` are the whole input. `CLAUDE.md` § *Never query Wikidata*.

Writes `reports/name-item-languages-NN.csv` — one row per name item, its classes, and a
column per target language holding the label if present. The per-language totals go to
`reports/name-item-languages.md`.

⛔ **SIXTEEN FILES, AND THE RULE IS PER-QID.** This was one 83.1 MB
`name-item-languages.csv` until 2026-09-19. GitHub's pre-receive hook declines a push
containing a file over 100 MB — and it declines it for what the repository CONTAINS, so
one oversized file refuses **everyone's** pushes, not just the one that wrote it. That
cost `pipeline.yml` 68 minutes a run for four hours when `garborg-live-items.json`
crossed, and this file was the next one up at 17 MB of headroom on a store that grows.

`int(qid[1:]) % SHARD_COUNT` depends on the qid alone, never on how many items exist or
what order the store yields them in, so **one new name item dirties exactly one shard**.
A size-based split would reshuffle every row after the insertion point and emit sixteen
garbage diffs a run — `CLAUDE.md` § *SORTING MUST BE DETERMINISTIC*. Rows are sorted
numerically within a shard for the same reason: the store's own shard order used to
decide row order here, which made the diff depend on something nobody controls.

    python scripts/measure-name-item-languages.py
"""

from __future__ import annotations

import csv
import gzip
import io
import json
import sys
import zlib
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SEEDS = REPO / "reports" / "name-item-qids.tsv"
SHARDS = sorted((REPO / "wikidata" / "items").glob("items-*.jsonl.gz"))
OUT_MD = REPO / "reports" / "name-item-languages.md"

#: Sixteen, as `refresh-live-values.py` uses for the same reason and at a similar size.
SHARD_COUNT = 16


def shard_of(qid) -> int:
    """Which shard `qid` belongs in. A pure function of the qid, by construction."""
    text = str(qid)
    try:
        n = int(text[1:])
    except (TypeError, ValueError):
        # Never a real qid. `hash()` is NOT usable -- it is salted per process, so the
        # same key would land in a different shard on every run and churn the diff forever.
        n = zlib.crc32(text.encode("utf-8"))
    return n % SHARD_COUNT


def shard_csv(n: int) -> Path:
    return REPO / "reports" / ("name-item-languages-%02d.csv" % n)


def shard_paths() -> list[Path]:
    return [shard_csv(n) for n in range(SHARD_COUNT)]


def read_rows():
    """Every row across every shard, as `csv.DictReader` dicts.

    **The readers all scan the whole census**, so they need the concatenation and not the
    shard rule -- `build-name-item-cjk.py`, `build-name-label-gaps.py`,
    `resolve-ambiguous-names.py` and `measure-mechanical-translation.py`. A missing shard
    is skipped rather than raising, so a clone that has not run the measurement degrades
    instead of crashing.
    """
    for path in shard_paths():
        if not path.exists():
            continue
        with path.open(encoding="utf-8", newline="") as fh:
            yield from csv.DictReader(fh)


class _Fanout:
    """`writerow` that routes each row to its qid's shard.

    A class rather than a closure so the loop below keeps reading `writer.writerow(...)`
    -- the one line of the measurement that had nothing to do with this change.
    """

    def __init__(self, writers):
        self._writers = writers

    def writerow(self, row):
        self._writers[shard_of(row[0])].writerow(row)


def sort_shards(header) -> None:
    """Sort each shard in place, one at a time.

    The store decides what order rows arrive in, and that is not a property anyone here
    controls -- re-downloading the items reshuffles the file and every line reads as
    changed. Sorting on the qid makes the same input produce the same bytes.
    """
    for n in range(SHARD_COUNT):
        path = shard_csv(n)
        with path.open(encoding="utf-8", newline="") as fh:
            rows = list(csv.reader(fh))[1:]
        rows.sort(key=_sort_key)
        tmp = path.with_suffix(".csv.tmp")
        with tmp.open("w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh, lineterminator="\n")
            w.writerow(header)
            w.writerows(rows)
        tmp.replace(path)


def _sort_key(row):
    """Numeric on the qid. `casefold` alone is not a total order and neither is string
    sort on `Q10` against `Q9` -- `CLAUDE.md` § *SORTING MUST BE DETERMINISTIC*."""
    qid = row[0]
    try:
        return (0, int(qid[1:]), "")
    except (TypeError, ValueError):
        return (1, 0, qid)

#: The seven-language target from `emission-spec.md`, plus the Nordic and Iberian
#: languages the tree is actually full of, plus `mul`.
LANGS = ["mul", "en", "ja", "zh", "ko", "ar", "he", "ru",
         "de", "fr", "es", "pt", "it", "nl", "sv", "nb", "da", "fi", "pl"]

CLASS_NAMES = {
    "Q101352": "family name",
    "Q12308941": "male given name",
    "Q11879590": "female given name",
    "Q202444": "given name",
    "Q3409032": "unisex given name",
    "Q110874": "patronymic",
}


def load_seeds() -> dict[str, str]:
    seeds: dict[str, str] = {}
    with SEEDS.open(encoding="utf-8") as fh:
        for i, line in enumerate(fh):
            parts = line.rstrip("\n").split("\t")
            if not parts or not parts[0].startswith("Q"):
                continue
            seeds[parts[0]] = parts[1] if len(parts) > 1 else ""
    return seeds


def main() -> None:
    seeds = load_seeds()
    print(f"{len(seeds):,} name-item QIDs to look for", flush=True)

    have = Counter()
    per_class_have: dict[str, Counter] = {c: Counter() for c in CLASS_NAMES}
    seen = 0
    rows_written = 0

    header = ["qid", "classes"] + LANGS
    shard_csv(0).parent.mkdir(parents=True, exist_ok=True)
    # Sixteen handles open at once, streamed, then each shard sorted on its own. Buffering
    # all 823,908 rows to sort them once would be the obvious shape and it is hundreds of
    # megabytes of Python lists; one shard at a time is ~5 MB of text.
    handles = [shard_csv(n).open("w", encoding="utf-8", newline="")
               for n in range(SHARD_COUNT)]
    writers = [csv.writer(fh, lineterminator="\n") for fh in handles]
    for w in writers:
        w.writerow(header)
    try:
        writer = _Fanout(writers)
        for n, shard in enumerate(SHARDS, 1):
            with gzip.open(shard, "rt", encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    if '"Q' not in line:
                        continue
                    try:
                        item = json.loads(line)
                    except Exception:
                        continue
                    qid = item.get("id") or item.get("qid")
                    if qid not in seeds:
                        continue
                    seen += 1
                    labels = item.get("labels") or {}
                    cells = []
                    for lang in LANGS:
                        v = labels.get(lang)
                        if isinstance(v, dict):
                            v = v.get("value", "")
                        cells.append(v or "")
                        if v:
                            have[lang] += 1
                    classes = seeds.get(qid, "")
                    for cls in classes.split(","):
                        if cls in per_class_have:
                            for lang, cell in zip(LANGS, cells):
                                if cell:
                                    per_class_have[cls][lang] += 1
                    writer.writerow([qid, classes] + cells)
                    rows_written += 1
            if n % 200 == 0:
                print(f"  shard {n}/{len(SHARDS)}  matched {seen:,}", flush=True)
    finally:
        for fh in handles:
            fh.close()
    sort_shards(header)

    lines = ["# What languages the name items carry labels in", "",
             f"**{seen:,} of {len(seeds):,} enumerated name items were found in the "
             f"local store** and are the basis of every figure here.", "",
             "This is the ceiling on mechanical translation: a person's label in a "
             "language can only be assembled from name items that have a label in "
             "that language.", "",
             "| language | items with a label | share |", "| --- | ---: | ---: |"]
    for lang in LANGS:
        n = have[lang]
        lines.append(f"| `{lang}` | {n:,} | {n / seen:.1%} |" if seen else f"| `{lang}` | 0 | |")
    lines += ["", "## By name class", "",
              "| class | " + " | ".join(f"`{l}`" for l in LANGS[:8]) + " |",
              "| --- | " + " | ".join("---:" for _ in LANGS[:8]) + " |"]
    for cls, name in CLASS_NAMES.items():
        c = per_class_have[cls]
        lines.append(f"| {name} | " + " | ".join(f"{c[l]:,}" for l in LANGS[:8]) + " |")
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"matched {seen:,} items; wrote {SHARD_COUNT} shards and {OUT_MD.name}")
    for lang in LANGS:
        print(f"  {lang:<4} {have[lang]:>8,}  {have[lang]/seen:.1%}" if seen else lang)


if __name__ == "__main__":
    main()
