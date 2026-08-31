"""Why does each still-ambiguous name string have two items? All of them, reproducibly.

    python scripts/classify-name-ambiguity.py

`reports/name-ambiguity-causes.md` sorted the 769 still-ambiguous strings into four buckets and
then said of the largest residue: *"### 231 · other. Mixed."* That bucket has never been broken
down, and it is the only one where the answer was not already known -- the other three are
`CLAUDE.md`-level rulings (a native-script pair and a romanisation collision are not ours to
resolve; identical descriptions are a Wikidata duplicate).

**It also had no script.** The causes report was written by hand, so nothing could re-derive it
after the store grew. This does the whole classification, so the residue is enumerable rather
than a number in prose.

**Entirely offline.** All 1,543 competing items are in `wikidata/items/`; the shard for each
comes from the download index. Nothing is fetched -- `CLAUDE.md` § *Querying Wikidata is
ALLOWED* still says the store is the right first place to look.

The buckets, in the order they are tested, most specific first:

  * **native script** -- one item's description or label names a script the other's does not
    (`Landau` vs `family name (לנדאו)`). Not ours: picking one is Wikidata modelling.
  * **same romanisation** -- both are CJK family names with different native characters
    (`Tu` is 涂 and 屠). Unresolvable from a Latin string; the information was destroyed before
    the data reached us.
  * **duplicate** -- identical, non-empty descriptions and nothing else to separate them.
    `scripts/find-duplicate-name-items.py` lists these for `reports/merges-to-do.md`.
  * **sex split** -- male vs female given name. Already ruled on and resolved per BEARER from
    the person's sex, not per string.
  * **no description** -- at least one side has no English description at all. A gap in
    Wikidata, not an ambiguity.
  * **language split** -- both describe a given name but in different languages
    (`Juan` Chinese vs Spanish).
  * **other** -- what is left, and the point of the exercise.

Writes `reports/name-ambiguity-buckets.tsv` and prints the counts.
"""

import collections
import csv
import gzip
import io
import json
import pathlib
import re
import sqlite3
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "reports" / "name-ambiguity-resolved.csv"
INDEX = ROOT / "out" / "wikidata" / "download-state.sqlite3"
STORE = ROOT / "wikidata" / "items"
OUT = ROOT / "reports" / "name-ambiguity-buckets.tsv"

#: A description naming a script or a language, e.g. `family name (לנדאו)`,
#: `Korean family name (이)`. The bracketed part is the native form.
NATIVE = re.compile(r"\(([^)]+)\)")
CJK = re.compile(r"[㐀-䶿一-鿿豈-﫿]")
HANGUL = re.compile(r"[가-힯ᄀ-ᇿ]")

SEX_WORDS = ("male given name", "female given name")


def ambiguous_rows():
    out = []
    with io.open(SRC, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            qids = [q.strip() for q in (row.get("qid") or "").split("|") if q.strip()]
            if len(qids) > 1:
                out.append((row["kind"], row["name"], row["occurrences"], qids))
    return out


def load_items(qids):
    """`{qid: {label, description, native}}` read straight out of the gzipped shards."""
    con = sqlite3.connect(f"file:{INDEX}?mode=ro", uri=True)
    shard_of = {}
    ids = sorted(set(qids))
    for i in range(0, len(ids), 900):
        chunk = ids[i:i + 900]
        marks = ",".join("?" * len(chunk))
        for qid, shard in con.execute(
                f"SELECT qid, shard FROM items WHERE qid IN ({marks})", chunk):
            shard_of[qid] = shard

    wanted = collections.defaultdict(set)
    for qid, shard in shard_of.items():
        if shard:
            wanted[shard].add(qid)

    out = {}
    for shard, qids_here in wanted.items():
        path = STORE / shard
        if not path.exists():
            continue
        with gzip.open(path, "rt", encoding="utf-8") as fh:
            for line in fh:
                if not line.strip():
                    continue
                try:
                    item = json.loads(line)
                except ValueError:
                    continue
                qid = item.get("id")
                if qid not in qids_here:
                    continue
                labels = item.get("labels") or {}
                descs = item.get("descriptions") or {}
                out[qid] = {
                    "label": (labels.get("en") or {}).get("value", ""),
                    "description": (descs.get("en") or {}).get("value", ""),
                    # every label, so a native-script form on any language is visible
                    "forms": {v.get("value", "") for v in labels.values()},
                }
    return out


def has_native_marker(info):
    """A bracketed native form in the description, or a CJK/Hangul label anywhere."""
    for chunk in NATIVE.findall(info["description"]):
        if CJK.search(chunk) or HANGUL.search(chunk) or not chunk.isascii():
            return True
    return any(CJK.search(f) or HANGUL.search(f) for f in info["forms"])


def bucket(qids, info):
    """The most specific bucket that fits. Order matters; see the module docstring."""
    have = [info.get(q) for q in qids]
    if any(x is None for x in have):
        return "not in store"
    descs = [x["description"] for x in have]

    native = [has_native_marker(x) for x in have]
    if any(native) and not all(native):
        return "native script"
    if all(native) and any(CJK.search(f) for x in have for f in x["forms"]):
        return "same romanisation"
    if not all(descs):
        return "no description"
    if len(set(descs)) == 1:
        return "duplicate"
    lowered = [d.lower() for d in descs]
    if any(w in d for d in lowered for w in SEX_WORDS) and len(set(lowered)) > 1:
        if all(any(w in d for w in SEX_WORDS) for d in lowered):
            return "sex split"
    # both say "given name"/"family name" but qualified by different languages
    if len({re.sub(r"^[a-z\- ]*?(given|family) name", "", d).strip()
            for d in lowered}) > 1:
        return "language split"
    return "other"


def main():
    rows = ambiguous_rows()
    every = [q for _k, _n, _o, qids in rows for q in qids]
    sys.stderr.write(f"{len(rows)} ambiguous strings, {len(set(every))} items\n")
    info = load_items(every)
    sys.stderr.write(f"{len(info)} read from the local shards\n")
    if not info:
        sys.exit("no item resolved from the store -- check the download index and shards")

    counts = collections.Counter()
    out_rows = []
    for kind, name, occurrences, qids in rows:
        which = bucket(qids, info)
        counts[which] += 1
        out_rows.append({
            "bucket": which,
            "kind": kind,
            "name": name,
            "occurrences": occurrences,
            "descriptions": " | ".join(info.get(q, {}).get("description", "") for q in qids),
            "qids": " | ".join(qids),
        })

    out_rows.sort(key=lambda r: (r["bucket"], -int(r["occurrences"] or 0)))
    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh, delimiter="\t",
            fieldnames=["bucket", "kind", "name", "occurrences", "descriptions", "qids"])
        writer.writeheader()
        writer.writerows(out_rows)

    print(f"wrote {OUT}")
    total = sum(counts.values())
    for name, count in counts.most_common():
        print(f"  {name:18s} {count:5d}  {count / total:5.1%}")


if __name__ == "__main__":
    main()
