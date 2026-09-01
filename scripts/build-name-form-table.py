"""Scandinavian given-name FORMS, read off the corpus rather than invented.

    py scripts/build-name-form-table.py

**The residue the letter rules cannot reach.** `namemodel`'s skeleton match folds spellings --
`d`/`t`, the inner `h`, `th`/`t` -- and each fold was sampled by hand before it shipped. What it
cannot do is join `Nilsson` to a father named `Nicolaus`: the skeletons are `nls` and `nkls`, and
no fold that joins those leaves anything else apart. `Nils` is a **form** of `Nicolaus`, not a
spelling of it, and the same is true of `Lars`/`Laurentius`, `Ola`/`Olaus`, `Jon`/`Johannes`.

**So it has to be data, and the queue item says where the data comes from:** *"take fathers whose
given name is Latinate and whose children carry a vernacular patronymic, and read off the pairs
rather than inventing them."* That is what this does. Nothing is proposed from a dictionary of
Scandinavian names; a pair is only recorded when the corpus shows a father called X whose child
carries a patronymic built on Y.

## Why this is not name similarity

`CLAUDE.md` bans matching people by name resemblance, and this does not do that. The father is
already known -- he is the `father` column of `reports/derived-family.csv`, established by the
GEDCOM's own `FAMC`/`FAMS` structure. The only question asked is *what is this already-identified
man's given name, and what stem does his child's patronymic carry*. That is reading a
correspondence off a fixed pair, which is the same thing `zipper-join`'s name step is allowed to
do inside a slot the structure has already chosen.

**A pair is kept only when several unrelated families attest it**, because one family is a
transcription error and a hundred is a naming convention. `MIN_FAMILIES` is that floor and the
count is emitted so the threshold can be argued with.

Writes `reports/name-form-pairs.tsv`.
"""

from __future__ import annotations

import collections
import csv
import io
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "scripts"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
csv.field_size_limit(1 << 30)

import namemodel as nm  # noqa: E402

FAMILY = REPO / "reports" / "derived-family.csv"
LABELS = REPO / "reports" / "derived-labels.csv"
OUT = REPO / "reports" / "name-form-pairs.tsv"

#: How many distinct fathers must attest a pair before it is written down. One is a typo.
MIN_FAMILIES = 5


def main() -> int:
    print("reading labels ...")
    label = {}
    with LABELS.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            v = (r["label_en"] or "").strip()
            if v:
                label[r["geni_id"]] = v
    print(f"  {len(label):,} people with a label")

    print("reading fathers ...")
    father = {}
    with FAMILY.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            fa = (r.get("father") or "").strip()
            if fa:
                father[r["geni_id"]] = fa
    print(f"  {len(father):,} people with a recorded father")

    print("pairing patronymic stems against the father's given name ...")
    pairs = collections.defaultdict(set)
    same = miss = 0
    for child, fa in father.items():
        cl, fl = label.get(child), label.get(fa)
        if not cl or not fl:
            continue
        # **Every one of the father's name tokens, not just the first.** Checking only the
        # first given name produced `johan -> ander`, 82 fathers, which is not a form pair at
        # all: the father is `Johan Anders...` and the child's patronymic is built on his
        # SECOND name. Same for `karl -> ander` and `johan -> nil`. A patronymic names one of
        # the father's names and nothing says it is the first.
        ftokens = [t.casefold() for t in fl.split() if t]
        if not ftokens:
            continue
        for token in cl.split():
            m = nm.PATRONYMIC_PARTS.match(token.casefold())
            if not m:
                continue
            stem = m.group(1)
            if not stem:
                continue
            # Already joined by the letter rules -- nothing for a form table to add.
            if any(nm._same_name(stem, ft) or nm._skeleton(stem) == nm._skeleton(ft)
                   for ft in ftokens):
                same += 1
                continue
            # **A truncation is not a form.** `olof -> ol` and `olof -> ols` were the two
            # commonest pairs and both are the genitive s being split off differently, not
            # `Ol` being a form of `Olof`. A stem that is a prefix of one of the father's
            # names, or the other way round, is the same name spelled shorter.
            if any(ft.startswith(stem) or stem.startswith(ft) for ft in ftokens):
                same += 1
                continue
            miss += 1
            pairs[(ftokens[0], stem)].add(fa)

    print(f"  {same:,} already joined by the letter rules")
    print(f"  {miss:,} not joined -- the population a form table would serve")

    rows = []
    for (latin, vernacular), fathers in pairs.items():
        if len(fathers) < MIN_FAMILIES:
            continue
        rows.append({"father_given": latin, "patronymic_stem": vernacular,
                     "distinct_fathers": len(fathers)})
    rows.sort(key=lambda r: -r["distinct_fathers"])

    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, delimiter="\t",
                           fieldnames=["father_given", "patronymic_stem", "distinct_fathers"])
        w.writeheader()
        w.writerows(rows)

    print(f"\nwrote {OUT.relative_to(REPO)} - {len(rows)} pairs attested by "
          f"{MIN_FAMILIES}+ distinct fathers")
    for r in rows[:30]:
        print(f"   {r['father_given']:<16} -> {r['patronymic_stem']:<16} "
              f"{r['distinct_fathers']:>6} fathers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
