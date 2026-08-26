"""What is each kind of zipper evidence actually worth? Measured, not ranked from intuition.

    python scripts/measure-zipper-reliability.py

**Emma, 2026-08-25, on the cascade being presented as her design:** *"solo -> date -> name isn't
really a thing I asked for lol it's a hallucination on your part."* She had said dates-then-names
about the **2x2 sibling** case specifically; it was generalised into an architecture and then
attributed back to her.

And the substantive half: *"Solo child says nothing unless there's some reason to match them lol"*
-- a single unmatched person on each side is trivially unique and therefore carries no
information. Uniqueness is not evidence when the set has one element.

Then the standard she set for all of it: *"a lot of these rules are empirical and we need to
empirically study our data to figure out what to make of it. Don't jump to conclusions based on
what sounds like it might be true. Even parents isn't certain."*

So this measures, per **(slot, method)** cell, three things a proposal can be checked against
without asking Wikidata anything:

* **date disagreement** -- both sides carry a birth year and they are more than ten years apart.
  A floor on wrongness, not a measure of rightness: agreeing dates prove very little, and the
  `date` method selects on the year so its own column is circular by construction and is marked.
* **independent corroboration** -- some source that is not the zipper puts the same pair together
  (Emma's About Me links, `entity_resolution.md`, the structural walk, the Izumo and Tanba
  rosters, her hand verdicts in `reports/emma-judgments.tsv`).
* **independent contradiction** -- such a source puts one of them with somebody else.

**The reliability order in `zipper-join.py`'s `SLOTS` is Emma's spoken ranking and is a hypothesis
this file exists to test.** She said parents are the most reliable and then immediately warned
*"even parents isn't certain"*. Nothing here assumes she is right and nothing assumes she is
wrong; the table is the answer.

Writes `reports/zipper-reliability.md`. Offline.
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
R = ROOT / "reports"

#: More than this many years apart and the two cannot be one person.
YEAR_GAP = 10

INDEPENDENT = (
    ("emma-hand-verdict", R / "emma-judgments.tsv", "qid", "geni_id", "\t"),
    ("geni-about-me", R / "geni-qid-links.tsv", "qids", "geni_id", "\t"),
    ("structural-walk", R / "structural-correspondence.csv", "qid", "geni_id", ","),
    ("geni-wikidata-pairs", R / "geni-wikidata-pairs.csv", "qid", "geni_id", ","),
    ("izumo-roster", R / "izumo-p2600-pairs.tsv", "qid", "geni_ids", "\t"),
    ("tanba-roster", R / "tanba-p2600-pairs.tsv", "qid", "geni_ids", "\t"),
)


def read_pairs(path, qcol, gcol, delim):
    if not path.exists():
        return
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=delim):
            q = (row.get(qcol) or "").strip()
            if row.get("verdict") in ("WRONG", "BROWSER"):
                continue
            for g in re.split(r"[;,|]", row.get(gcol) or ""):
                g = g.strip()
                if q.startswith("Q") and g.isdigit():
                    yield q, g


def pct(a, b):
    return f"{100 * a / b:.1f}%" if b else "--"


def main():
    oy, ty = {}, {}
    with open(R / "derived-facts.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["birth_date_year"]:
                try:
                    oy[row["geni_id"]] = int(row["birth_date_year"])
                except ValueError:
                    pass
    with open(ROOT / "out" / "wikidata" / "dates.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row["birth_year"]:
                ty[row["qid"]] = int(row["birth_year"])

    independent = collections.defaultdict(dict)
    for label, path, qcol, gcol, delim in INDEPENDENT:
        for q, g in read_pairs(path, qcol, gcol, delim):
            independent[g][label] = q

    rows = list(csv.DictReader(open(R / "zipper-pairs.tsv", encoding="utf-8"), delimiter="\t"))
    if not rows or "method" not in rows[0]:
        sys.exit("zipper-pairs.tsv has no provenance columns - re-run scripts/zipper-join.py")

    cells = collections.defaultdict(lambda: collections.Counter())
    for row in rows:
        g, q = row["geni_id"], row["qid"]
        c = cells[(row["slot"], row["method"])]
        c["n"] += 1
        c[f"round{min(int(row['round']), 4)}"] += 1
        a, b = oy.get(g), ty.get(q)
        if a is not None and b is not None:
            c["dated"] += 1
            if abs(a - b) > YEAR_GAP:
                c["date_bad"] += 1
        for _label, iq in independent.get(g, {}).items():
            c["checked"] += 1
            if iq == q:
                c["agree"] += 1
            else:
                c["disagree"] += 1

    order = sorted(cells, key=lambda k: -cells[k]["n"])
    out = []
    out.append("# What each kind of zipper evidence is actually worth\n")
    out.append("Generated by `scripts/measure-zipper-reliability.py`. **Nothing here is "
               "reasoned from what sounds right.** Emma, 2026-08-25: *\"a lot of these rules "
               "are empirical and we need to empirically study our data to figure out what to "
               "make of it. Don't jump to conclusions based on what sounds like it might be "
               "true. Even parents isn't certain.\"*\n")
    out.append("Two independent checks, neither of which asks Wikidata anything: whether the "
               "two birth years are more than ten years apart, and whether a source that is "
               "**not** the zipper puts the same pair together or pulls it apart.\n")
    out.append("`date` selects on the birth year, so its date column is circular by "
               "construction and is marked `--`. Read it against `solo` and `name`, not "
               "alongside them.\n")
    out.append("| slot | method | pairs | dated | dates >10y apart | independently checked | "
               "agree | disagree |")
    out.append("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for slot, method in order:
        c = cells[(slot, method)]
        db = "--" if method == "date" else pct(c["date_bad"], c["dated"])
        out.append(f"| {slot} | {method} | {c['n']:,} | {c['dated']:,} | {db} | "
                   f"{c['checked']:,} | {pct(c['agree'], c['checked'])} | "
                   f"{pct(c['disagree'], c['checked'])} |")

    # Per-slot and per-method margins, so the two questions can be read apart.
    for axis, idx in (("slot", 0), ("method", 1)):
        agg = collections.defaultdict(collections.Counter)
        for k, c in cells.items():
            agg[k[idx]].update(c)
        out.append(f"\n## By {axis}\n")
        out.append(f"| {axis} | pairs | dates >10y apart | independently checked | disagree |")
        out.append("| --- | ---: | ---: | ---: | ---: |")
        for k in sorted(agg, key=lambda x: -agg[x]["n"]):
            c = agg[k]
            db = "--" if k == "date" else pct(c["date_bad"], c["dated"])
            out.append(f"| {k} | {c['n']:,} | {db} | {c['checked']:,} | "
                       f"{pct(c['disagree'], c['checked'])} |")

    text = "\n".join(out) + "\n"
    (R / "zipper-reliability.md").write_text(text, encoding="utf-8")
    print(text)
    print(f"wrote {(R / 'zipper-reliability.md').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
