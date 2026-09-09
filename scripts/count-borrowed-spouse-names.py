"""People whose only name is their spouse's name, with no parents of their own.

    python scripts/count-borrowed-spouse-names.py

**Emma, 2026-08-29**, after `Q141198548` turned out to be Buyeo Deokjang's wife carrying *his*
name rather than a duplicate of him: *"queue the general detection."*

**The shape.** A person whose label equals their spouse's, who has **no parents recorded**, and
who exists on Geni only to hold the marriage. They are the `NN` population wearing a borrowed
name, and nothing detects them — `_carries_marker` looks for marker words and this name contains
none.

**Count them; propose nothing.** Her instruction: *"Report the number; do not fold it into the
NN detection until she has seen it."* So this writes a census and stops. No label is changed, no
batch is emitted, and `labels.py` is untouched.

## What counts as "the same name", and why the bar is where it is

Three bands, reported separately, because they are different claims:

* **identical** — the two labels are equal after case-folding and whitespace collapse. This is
  the `Q141198548` shape: `덕장 부여` against `Buyeo Deokjang`'s Korean form, or plain
  `Hans Olsen` against `Hans Olsen`.
* **surname only** — the person's whole label is a *proper subset* of their spouse's tokens,
  and is the trailing part of it. `Olsen` married to `Hans Olsen`. This is weaker: a wife
  recorded under her married surname alone is ordinary Norwegian practice, not necessarily a
  placeholder.
* **given name shared** — reported for scale and deliberately NOT counted as borrowed, because
  two people with the same given name is a coincidence, not a borrowing.

**No fuzzy matching.** `CLAUDE.md` forbids it and there is no reason for it here: a borrowed
name is a copied string, not a similar one. Case folds and runs of whitespace collapse; nothing
else.

**Parentlessness is the discriminator, not the name.** A person with parents recorded has a
place in the tree of their own; the population Emma named is the one that exists solely to hold
a marriage. Both halves are reported so the effect of the filter is visible.

Writes `reports/borrowed-spouse-names.csv` — one row per instance, per her rule that an analysis
is a CSV of every instance and then an analysis of that.
"""
from __future__ import annotations

import csv
import sys
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

FAMILY = ROOT / "reports" / "derived-family.csv"
LABELS = ROOT / "reports" / "derived-labels.csv"
OUT = ROOT / "reports" / "borrowed-spouse-names.csv"

#: `derived-family.csv` separates multi-valued cells with ` | `, spaces included.
#: `CLAUDE.md` § *Our side could never have two children* is what splitting on the wrong
#: thing costs: 379,251 people arrived childless and the bug was invisible for days.
SEP = " | "


def cells(value):
    return [v.strip() for v in (value or "").split(SEP) if v.strip()]


def fold(text):
    return " ".join(unicodedata.normalize("NFC", text or "").casefold().split())


def main():
    label = {}
    for row in csv.DictReader(LABELS.open(encoding="utf-8", newline="")):
        label[row["geni_id"]] = row["label_mul"] or row["label_en"] or ""
    print(f"{len(label):,} people carry a label")

    rows, counts = [], Counter()
    seen_pairs = set()
    for row in csv.DictReader(FAMILY.open(encoding="utf-8", newline="")):
        me = row["geni_id"]
        mine = fold(label.get(me, ""))
        if not mine:
            continue
        has_parents = bool(cells(row["father"]) or cells(row["mother"])
                           or cells(row.get("fathers")) or cells(row.get("mothers")))
        for spouse in cells(row["spouses"]):
            theirs = fold(label.get(spouse, ""))
            if not theirs or spouse == me:
                continue
            my_tokens, their_tokens = mine.split(), theirs.split()
            if mine == theirs:
                band = "identical"
            elif (len(my_tokens) < len(their_tokens)
                  and their_tokens[-len(my_tokens):] == my_tokens):
                band = "surname only"
            elif set(my_tokens) & set(their_tokens):
                band = "shares a token"
            else:
                continue
            key = (min(me, spouse), max(me, spouse), band)
            if key in seen_pairs:
                continue
            seen_pairs.add(key)
            counts[(band, has_parents)] += 1
            if band != "shares a token":
                rows.append({"geni_id": me, "label": label.get(me, ""),
                             "spouse_geni_id": spouse, "spouse_label": label.get(spouse, ""),
                             "band": band,
                             "has_parents": "yes" if has_parents else "no",
                             "children": row["child_count"], "qid": row["qid"]})

    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["geni_id", "label", "spouse_geni_id", "spouse_label",
                                           "band", "has_parents", "children", "qid"])
        w.writeheader()
        w.writerows(sorted(rows, key=lambda r: (r["band"], r["has_parents"], r["label"])))

    print(f"\n{'band':<16}{'no parents':>12}{'has parents':>13}{'total':>9}")
    for band in ("identical", "surname only", "shares a token"):
        no = counts[(band, False)]
        yes = counts[(band, True)]
        print(f"{band:<16}{no:>12,}{yes:>13,}{no + yes:>9,}")
    borrowed = counts[("identical", False)] + counts[("surname only", False)]
    print(f"\nthe population Emma named -- name taken from the spouse AND no parents "
          f"recorded: {borrowed:,}")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(rows):,} rows)")
    print("NOTHING IS PROPOSED. This is a count, per the queue item.")


if __name__ == "__main__":
    main()
