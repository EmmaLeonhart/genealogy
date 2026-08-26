"""`P21` sex or gender out of the store, so a pairing can be REFUTED for free.

    python scripts/extract-wikidata-sex.py

**Nothing had extracted it.** `out/wikidata/relations.tsv` carries `P22`/`P25`/`P40`/`P26`/`P2600`,
`labels.tsv` carries labels and identifiers, `dates.tsv` carries years — and `scripts/zipper-join.py`
contains no reference to sex anywhere. So a join that pairs a man with a woman had no way to
notice, across 44,725 correspondences.

**This is the cheapest refutation available and the only one that is nearly complete on our side.**
Our `sex` column is populated for 1,327,295 of 1,329,328 people — **99.85%** — where birth years
reach only 69%. A sex disagreement is also unambiguous in a way a ten-year date gap is not: two
soft medieval dates can differ by a decade and still be one person, but `Q6581097` *male* against
a `F` is either a wrong pair or a wrong record, never a rounding difference.

**It refutes; it never confirms.** Agreeing sexes are worth almost nothing — roughly half of all
random pairs agree by chance — so this must never be added as *evidence for* a pairing. That
asymmetry is the same one `CLAUDE.md` states for absence, in the other direction.

Values kept, and only these two: `Q6581097` *male* and `Q6581072` *female*, mapped to `M` and `F`
to match our own column. **Anything else is emitted as its own raw QID rather than folded into a
binary** — Wikidata carries `Q1097630` *intersex*, `Q1052281` *transgender female* and others, and
flattening them would both misrepresent people and manufacture false refutations against a Geni
`M`/`F` that means something narrower. A caller comparing sexes must decide what to do with those
rather than have this file decide silently.

**Deprecated statements are dropped**, matching the other extractors: a deprecated `P21` is
Wikidata saying "not this one".

Output, one row per item that states `P21`:

    qid  sex        # M, F, or a raw QID

Writes `out/wikidata/sex.tsv`. Reads only the store; makes no request.
"""
from __future__ import annotations

import gzip
import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
STORE = ROOT / "wikidata" / "items"
DEST = ROOT / "out" / "wikidata" / "sex.tsv"

#: `CLAUDE.md` § *Wikidata properties and items* — confirmed against live Wikidata 2026-08-02.
MALE = "Q6581097"
FEMALE = "Q6581072"
BINARY = {MALE: "M", FEMALE: "F"}


def sex_of(claims):
    """`M`, `F`, a raw QID, or `''`. Preferred rank wins; deprecated never counts."""
    best = ""
    for st in claims.get("P21", []):
        if st.get("rank") == "deprecated":
            continue
        dv = st.get("mainsnak", {}).get("datavalue", {}).get("value")
        if not isinstance(dv, dict):
            continue
        qid = dv.get("id")
        if not qid:
            continue
        value = BINARY.get(qid, qid)
        if st.get("rank") == "preferred":
            return value
        best = best or value
    return best


def main():
    shards = sorted(STORE.glob("items-*.jsonl.gz"))
    print(f"{len(shards)} shards")
    DEST.parent.mkdir(parents=True, exist_ok=True)
    started = time.time()
    items = rows = 0
    seen = Counter()
    with open(DEST, "w", encoding="utf-8", newline="\n") as out:
        out.write("qid\tsex\n")
        for n, shard in enumerate(shards, 1):
            with gzip.open(shard, "rt", encoding="utf-8") as f:
                for line in f:
                    if not line.startswith("{"):
                        continue
                    try:
                        item = json.loads(line)
                    except ValueError:
                        continue
                    qid = item.get("id")
                    if not qid:
                        continue
                    items += 1
                    value = sex_of(item.get("claims", {}))
                    if not value:
                        continue
                    seen[value] += 1
                    out.write(f"{qid}\t{value}\n")
                    rows += 1
            if n % 400 == 0:
                print(f"  {n}/{len(shards)} shards, {items:,} items, {rows:,} with P21",
                      flush=True)
    print(f"\n{items:,} items read, {rows:,} state P21")
    for value, n in seen.most_common(8):
        label = {"M": "male", "F": "female"}.get(value, "other — NOT folded into M/F")
        print(f"   {n:>9,}  {value:<12} {label}")
    print(f"wrote {DEST} in {time.time() - started:.0f}s")


if __name__ == "__main__":
    main()
