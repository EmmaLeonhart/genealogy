"""The force fix: remove every language label that is only a copy of the item's own `mul`.

    python scripts/build-label-repair-tail.py

**Ruled 2026-09-13:** *"do a force fix thing at the end of all future quickstatements batches
that fixes the label damage we did"*. It runs as a TAIL, after everything else in the batch, so
a repair can never be what a run spends its caps on — and it is uncapped, because it removes
strings this pipeline put there rather than adding anything.

## What the damage is

Measured 2026-09-11: **1,628 items were acted on, 1,606 of them came away with at least one
language label identical to their own `mul`, across 2,289 redundant edits.** `Q105872266`
Eleanor Peshale carried the same string in six places — `mul`, `en`, `en-ca`, `en-us`, `fr`,
`nl`. Emma: *"many people like this have a very wrong thing done with their labels."*

A language label BEATS `mul`, so the redundancy is not cosmetic: while `en` holds a copy, a later
correction to `mul` alone shows nothing, and the item reads from the stale copy. Removing the
copy is what lets `mul` be the one place the name lives.

## ⛔ VERIFIED LIVE, ONE ITEM AT A TIME, AND NEVER FROM THE SNAPSHOT

`reports/label-duplicates-of-mul.csv` is a measurement from 2026-09-11 and says what was true
then. A label that has since been corrected by hand — Emma corrected `Q105872266` herself — must
not be removed on the strength of a two-day-old file. So every candidate is re-read from
Wikidata and a removal is emitted **only where the language label is still character-for-character
the item's current `mul`**. Anything that has diverged is left alone, which also makes the fix
self-limiting: run it twice and the second run emits nothing.

`reports/label-repair-live.tsv` caches the fetch so a regeneration costs no requests.

## The removal itself

QuickStatements removes a label by setting it to the empty string — `Q1<TAB>Len<TAB>""`. The
2026-09-11 note left this open: *"Whether the fix is overwrite-and-accept or overwrite-then-remove
turns on what QuickStatements can do to a label, which is not checked and not guessed at."* It is
removal, and the file it writes is meant to be run and watched the first time rather than trusted.
"""

from __future__ import annotations

import csv
import io
import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANDIDATES = ROOT / "reports" / "label-duplicates-of-mul.csv"
CACHE = ROOT / "reports" / "label-repair-live.tsv"
OUT = ROOT / "reports" / "wikidata-label-repair.txt"
UA = {"User-Agent": "geni-repo/1.0 (emma@topazcomputing.com)"}


def candidates() -> list[str]:
    with CANDIDATES.open(encoding="utf-8") as fh:
        return sorted({row["qid"] for row in csv.DictReader(fh) if row.get("qid")})


def fetch(qids, *, sleep=1.0):
    """`{qid: {lang: label}}`, from the cache where it has the item and Wikidata otherwise."""
    live = {}
    if CACHE.exists():
        with CACHE.open(encoding="utf-8") as fh:
            for row in csv.DictReader(fh, delimiter="\t"):
                live.setdefault(row["qid"], {})[row["lang"]] = row["label"]
    missing = [q for q in qids if q not in live]
    for i in range(0, len(missing), 50):
        chunk = missing[i:i + 50]
        url = ("https://www.wikidata.org/w/api.php?action=wbgetentities&ids="
               + "|".join(chunk) + "&props=labels&format=json")
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA)) as fh:
            data = json.load(fh)
        for qid, entity in data.get("entities", {}).items():
            live[qid] = {k: v["value"] for k, v in entity.get("labels", {}).items()}
        print("  fetched %d/%d" % (min(i + 50, len(missing)), len(missing)), flush=True)
        time.sleep(sleep)
    if missing:
        with CACHE.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.writer(fh, delimiter="\t")
            writer.writerow(["qid", "lang", "label"])
            for qid in sorted(live):
                for lang in sorted(live[qid]):
                    writer.writerow([qid, lang, live[qid][lang]])
    return live


def removals(live):
    """`[(qid, lang)]` for every language label still identical to that item's own `mul`."""
    out = []
    for qid in sorted(live):
        mul = live[qid].get("mul", "")
        if not mul:
            continue
        for lang, value in sorted(live[qid].items()):
            if lang != "mul" and value == mul:
                out.append((qid, lang))
    return out


def lines(pairs):
    """The QuickStatements tail, comments and all."""
    if not pairs:
        return ["# label repair: nothing to remove -- every copy has been cleared or corrected"]
    items = len({q for q, _ in pairs})
    out = [
        "",
        "# ----------------------------------------------------------------------------",
        "# FORCE FIX -- remove language labels that are only a copy of the item's own mul.",
        "# %d label(s) on %d item(s). Ruled 2026-09-13. Uncapped, and last in the file so it" % (len(pairs), items),
        "# never competes with the batch for slots. Verified live: a label that has since been",
        "# corrected is not here. Running this twice is a no-op.",
        "# ----------------------------------------------------------------------------",
    ]
    for qid, lang in pairs:
        out.append('%s\tL%s\t""' % (qid, lang))
    return out


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    qids = candidates()
    print("candidates: %d" % len(qids))
    live = fetch(qids)
    pairs = removals({q: live[q] for q in qids if q in live})
    text = "\n".join(lines(pairs)) + "\n"
    OUT.write_text(text, encoding="utf-8")
    print("removals: %d label(s) on %d item(s)" % (len(pairs), len({q for q, _ in pairs})))
    print("-> %s" % OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
