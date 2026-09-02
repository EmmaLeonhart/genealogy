"""How much of the `exports/post-merge/` campaign is left, by its own stopping rule.

    py scripts/post-merge-coverage.py

**Emma's stopping rule, 2026-08-24:** *"Export until every first-degree relative of every merged
individual is present"* in `exports/post-merge/` — *"that is the stopping rule, not a count of
exports."* Nothing measured it, so the campaign had no way to end except by someone deciding it
felt done.

**And the economy is hers too:** *"merged individuals cluster together so we will not need to run
an export on every one of them"* — one `Forest` ball covers many. That is exactly what this
measures: how many of the 29 survivors are already covered by the six balls already taken.

## What "present" means, and why it is the post-merge directory specifically

`exports/post-merge/` has special merge logic — a Geni record there **overwrites** the same Geni ID
from any other export, because post-merge is newest and therefore right. So a relative sitting in
some older export does **not** count: the whole point is to have a *fresh* record of that person,
taken after Geni did the merge.

## What this does NOT do

**It does not judge whether a merge was justified.** `CLAUDE.md` § *The question is whether OUR
TREE MATCHES GENI* — the only question a duplicate raises is whether our snapshot is current, and
a post-merge export is worth running even when the pair turns out not to be a duplicate at all.
The `evidence` column is for **ordering** the work, never for filtering it.

Writes `reports/post-merge-coverage.tsv`, one row per survivor, and prints the seeds still needed.
"""
from __future__ import annotations

import collections
import csv
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
csv.field_size_limit(1 << 30)

TAB = chr(9)
DUPES = ROOT / "reports" / "geni-stale-duplicates.tsv"
FAMILY = ROOT / "reports" / "derived-family.csv"
LABELS = ROOT / "reports" / "derived-labels.csv"
POST_MERGE = ROOT / "exports" / "post-merge"
OUT = ROOT / "reports" / "post-merge-coverage.tsv"
MERGED_AWAY = ROOT / "reports" / "geni-merged-away.tsv"

#: `derived-family.csv` separates multi-valued cells with ` | `. `CLAUDE.md` records what
#: splitting on the wrong thing cost: 379,251 people arrived childless because a consumer
#: split on "," and ";" only.
SEP = " | "

#: `0 @I6000000087535357291@ INDI` — the individual record header, and the only line that
#: declares a person is IN a GEDCOM rather than merely mentioned by one.
INDI = re.compile(r"^0 @I(\d+)@ INDI", re.M)


def ids_in_post_merge():
    """Every Geni id that has an `INDI` record in `exports/post-merge/`."""
    found = set()
    for path in sorted(POST_MERGE.glob("*.ged")):
        text = path.read_text(encoding="utf-8", errors="replace")
        found |= set(INDI.findall(text))
    return found


def merged_away():
    """`{stale id: survivor id}` for profiles Geni has merged out of existence.

    **A merged-away relative can NEVER appear in an export**, so the stopping rule cannot be
    satisfied for it however many exports run. Both of the last two open survivors were this:
    Jingū-kōgō was short `6000000179131744821`, a second Ōjin profile now redirecting to
    `6000000001829492981`; Obito Haji-no-muraji was short `6000000001893090174`, which redirects
    to `6000000012789981728` Eguni Haji-no-muraji. In both cases the SURVIVOR is present.

    Our tree keeps both ids because the merge unions relationships and never drops one, which is
    exactly the behaviour `CLAUDE.md` records. So the relative is covered when its survivor is.

    Observed by following the profile URL, not looked up: `reports/geni-stale-duplicates.tsv`
    carries neither pair.
    """
    out = {}
    if not MERGED_AWAY.exists():
        return out
    with io.open(MERGED_AWAY, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=TAB):
            if r.get("stale_id") and r.get("survivor_id"):
                out[r["stale_id"].strip()] = r["survivor_id"].strip()
    return out


def cell(row, key):
    return [x.strip() for x in (row.get(key) or "").split(SEP) if x.strip()]


def main() -> int:
    if not DUPES.exists():
        print("no %s; run the duplicate census first" % DUPES.relative_to(ROOT), file=sys.stderr)
        return 1
    with io.open(DUPES, encoding="utf-8", newline="") as fh:
        dupes = list(csv.DictReader(fh, delimiter=TAB))
    survivors = {r["merged_survivor"]: r for r in dupes if r.get("merged_survivor")}
    print("%d stale duplicates, %d distinct survivors" % (len(dupes), len(survivors)))

    have = ids_in_post_merge()
    gone = merged_away()
    if gone:
        print("%d merged-away ids resolved to their survivor" % len(gone))
    print("%s carries %s distinct people" % (POST_MERGE.name, format(len(have), ",")))

    # First-degree relatives, from the merged tree.
    want = set(survivors)
    kin = {}
    with io.open(FAMILY, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            g = row["geni_id"]
            if g in want:
                kin[g] = ([x for x in (row.get("father"), row.get("mother")) if x]
                          + cell(row, "spouses") + cell(row, "children"))
    labels = {}
    everyone = set(survivors) | {x for v in kin.values() for x in v}
    with io.open(LABELS, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if row["geni_id"] in everyone:
                labels[row["geni_id"]] = (row.get("label_en") or row.get("label_mul")
                                          or row.get("cjk_names") or "")

    rows, need, tally = [], [], collections.Counter()
    for g, r in sorted(survivors.items()):
        relatives = kin.get(g, [])
        # A relative Geni has merged away is covered by its survivor -- see `merged_away`.
        missing = [x for x in relatives
                   if x not in have and gone.get(x) not in have]
        covered = g in have and not missing
        state = ("no relatives recorded" if not relatives
                 else "covered" if covered
                 else "survivor absent" if g not in have
                 else "%d of %d relatives missing" % (len(missing), len(relatives)))
        tally[state.split(" of ")[0] if "of" in state else state] += 1
        if not covered:
            need.append((r.get("evidence", ""), g, labels.get(g, r.get("name", ""))))
        rows.append([r.get("evidence", ""), g, labels.get(g, r.get("name", "")),
                     r.get("stale_twin", ""), len(relatives), len(missing),
                     "yes" if g in have else "no", state])

    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=TAB, lineterminator="\n")
        w.writerow(["evidence", "merged_survivor", "name", "stale_twin", "relatives",
                    "relatives_missing", "survivor_in_post_merge", "state"])
        w.writerows(sorted(rows, key=lambda x: (x[7] == "covered", x[0], -x[5])))

    print("\nwrote %s" % OUT.relative_to(ROOT))
    for k, v in tally.most_common():
        print("   %-30s %3d" % (k, v))
    order = {"strong": 0, "medium": 1, "weak": 2}
    need.sort(key=lambda x: order.get(x[0], 9))
    print("\n%d survivors still need an export, strongest evidence first:" % len(need))
    for ev, g, name in need[:20]:
        print("   %-8s %-22s %s" % (ev, g, name[:40]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
