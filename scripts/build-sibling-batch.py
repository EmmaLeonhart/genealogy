"""Every `P3373` sibling link among the people Emma has created or touched. One-off.

    BOT_CONTACT=you@example.com python scripts/build-sibling-batch.py

**Emma, 2026-08-28:** *"at this point I want to do an unbound sibling link generation of
quickstatements, a one time thing due to a technical issue I am trying to resolve."* Asked which
population, she chose the **ledger** — `reports/garborg-qids.tsv`, the people she has created or
edited, where both ends of every pair already carry a QID.

**This deliberately ignores `SIBLING_CAP`**, and that is the whole point of it existing as a
separate script rather than a flag on the daily builder. `CLAUDE.md` § *`P3373` sibling is capped
at 10 a day* is a **presentation** rule — *"siblin relationships are too numerous and imo come
off as too numerous"* — not a correctness one. The cap stays exactly as it is for the daily batch; a
one-off she has asked for by name is not the daily batch.

## Why the population matters so much

Sibling links grow as the **square** of a family's size: nine children is 72 statements on its
own, and `reports/wikidata-reciprocals.qs` once came out 62% `P3373` by statement count for that
reason. Scoping to the ledger keeps this bounded and keeps every statement between two items that
already exist — no `CREATE`, nothing that needs `LAST`, nothing that can duplicate a person.

## What counts as a sibling

Sharing **at least one recorded parent** in `reports/derived-family.csv`, which is the same test
`build-garborg-day.py` uses. Both directions are emitted, because `P3373` is symmetric and a
one-way sibling link is the documented past failure this repo keeps repairing.

**Already-present statements are dropped** against `reports/garborg-live-values.tsv`, refreshed
by `scripts/refresh-live-values.py`. QuickStatements merges a duplicate rather than failing, so
without that check three-quarters of a batch can be things she has already done and nothing
visibly breaks.

**Excluded ids are refused, not filtered** — the same rule the daily builder uses, for the same
reason: `CLAUDE.md` § *she must not be in the traversable graph*.

Writes `reports/wikidata-siblings-oneoff.qs`.
"""
from __future__ import annotations

import collections
import csv
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
LEDGER = ROOT / "reports" / "garborg-qids.tsv"
FAMILY = ROOT / "reports" / "derived-family.csv"
LIVE = ROOT / "reports" / "garborg-live-values.tsv"
OUT = ROOT / "reports" / "wikidata-siblings-oneoff.qs"

#: `P3373` *sibling*. Symmetric, so every pair is emitted twice.
SIBLING = "P3373"
#: `S2600` — the reference is the Geni profile the claim comes from.
SOURCE = "S2600"


def split_multi(cell):
    """` | ` with spaces, and the strip is load-bearing — 379,251 people once read as
    childless because it was missed."""
    return [x.strip() for x in re.split(r"[,;|]", cell or "") if x.strip()]


def main() -> None:
    # The exclusion sets live in the day builder, which is hyphenated and so must be loaded
    # by path. Restating them here would be a second copy to keep in step.
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_gday", ROOT / "scripts" / "build-garborg-day.py")
    gday = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gday)
    NEVER_TOUCH_GENI, NEVER_TOUCH_QID = gday.NEVER_TOUCH_GENI, gday.NEVER_TOUCH_QID

    have = {}
    with open(LEDGER, encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            if (row.get("qid") or "").startswith("Q"):
                have[row["geni_id"]] = row["qid"]
    print(f"{len(have)} people in the ledger with a QID")
    if not have:
        sys.exit("the ledger produced nobody — that is a broken read, not an empty ledger")

    fam = {}
    with open(FAMILY, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            fam[row["geni_id"]] = row

    # parent -> children, over the whole tree, so a sibling is found even when the other
    # child is reached from the parent's side rather than our own row.
    by_parent = collections.defaultdict(set)
    for gid, row in fam.items():
        for col in ("fathers", "mothers", "father", "mother"):
            for p in split_multi(row.get(col)):
                by_parent[p].add(gid)

    live = set()
    if LIVE.exists():
        with open(LIVE, encoding="utf-8") as fh:
            for row in csv.DictReader(fh, delimiter="\t"):
                live.add((row["qid"], row["property"], row["value"]))
    print(f"{len(live):,} statements already on those items")

    pairs = set()
    for gid in have:
        row = fam.get(gid)
        if not row:
            continue
        for col in ("fathers", "mothers", "father", "mother"):
            for p in split_multi(row.get(col)):
                for other in by_parent.get(p, ()):
                    if other != gid and other in have:
                        pairs.add((gid, other))

    print(f"{len(pairs):,} ordered sibling pairs where BOTH ends are in the ledger")
    if not pairs:
        sys.exit("no sibling pair matched — check the ` | ` split before believing this")

    lines, emitted, already, refused = [], 0, 0, 0
    lines.append("# P3373 sibling — one-off, uncapped, over the ledger only.")
    lines.append("#    Emma, 2026-08-28: \"an unbound sibling link generation ... a one time")
    lines.append("#    thing\". The 10-a-day cap is a presentation rule for the DAILY batch and")
    lines.append("#    is untouched by this file. Both ends already exist; there is no CREATE.")
    lines.append("")
    for gid, other in sorted(pairs):
        q, oq = have[gid], have[other]
        if (gid in NEVER_TOUCH_GENI or other in NEVER_TOUCH_GENI
                or q in NEVER_TOUCH_QID or oq in NEVER_TOUCH_QID):
            refused += 1
            continue
        if (q, SIBLING, oq) in live:
            already += 1
            continue
        lines.append(f"#   {q} {SIBLING} sibling = {oq} (Geni {other})")
        lines.append(f"{q}\t{SIBLING}\t{oq}\t{SOURCE}\t\"{gid}\"")
        emitted += 1

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"\n{emitted:,} statements written to {OUT.relative_to(ROOT)}")
    print(f"{already:,} dropped: the item already holds them")
    print(f"{refused:,} refused: an excluded id")


if __name__ == "__main__":
    main()
