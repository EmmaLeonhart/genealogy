"""The fathers the patronymics imply, named from the fathers we actually have.

**Emma, 2026-08-15:** *"Whether something is or is not a patronymic here is determined by
completely offline information related to the person's father's name."* That was already
built. `scripts/classify-patronymics.py` decides every token against the father, with her
three ambiguity classes. **This consumes that classification; it does not redo it.**

An earlier version of this file re-derived everything from suffix stripping and named the
father of an `Olsen` **`Ols`**. Emma: *"We already addressed this. Read through the
transcripts."* She was right, and the answer was in the classification: across 2,609
confirmed `Olsen`/`Olsson` patronymics the recorded fathers are **Ole 1,809, Ola 795,
Olof 73, Olav 69, Oluf 17**. The name is read off real fathers, never off the string.

ONE FATHER PER PERSON, WITH THE ONE EXCEPTION SHE NAMED

**Emma, 2026-08-19:** *"If you don't know the people are siblings you create one per
individual."* And: *"In the event of two people being linked, having the same patronym, and
being linked, that's a thing that's worth giving them the same father, but my guess is I
don't think that exists."*

**It exists.** Same mother, no father, same implied name -- 124 mothers and 404 people, one
of them with eleven children all `Halvorsen`/`Halvorsdatter`. Where the implied names differ
under one mother they are *not* merged: one mother's children imply `Jon` **and** `Ols`.

    py scripts/build-patronymic-fathers.py

Offline. Writes reports/patronymic-fathers.{md,csv}. Emits no edit.
"""

from __future__ import annotations

import csv
import io
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CLASS = REPO / "reports" / "patronymic-classification.csv"
FAMILY = REPO / "reports" / "derived-family.csv"
OUT_MD = REPO / "reports" / "patronymic-fathers.md"
OUT_CSV = REPO / "reports" / "patronymic-fathers.csv"

csv.field_size_limit(10 ** 7)
INFERRED = "patronymic (inferred, no father recorded)"


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    named = defaultdict(Counter)
    inferred = {}
    with io.open(CLASS, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            v = r["verdict"]
            if v == "patronymic" and r.get("father_given"):
                named[r["token"]][r["father_given"].split()[0]] += 1
            elif v == INFERRED:
                inferred.setdefault(r["geni_id"], r["token"])
    print("tokens with confirmed fathers: %d; bearers needing one: %d"
          % (len(named), len(inferred)))

    mother = {}
    with io.open(FAMILY, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            if r["geni_id"] in inferred:
                mother[r["geni_id"]] = (r.get("mother") or "").strip()

    rows, unnamed = [], Counter()
    for g, tok in sorted(inferred.items()):
        c = named.get(tok)
        if not c:
            unnamed[tok] += 1
            continue
        name, n = c.most_common(1)[0]
        rows.append([g, tok, name, n, sum(c.values()), mother.get(g, "")])

    groups = defaultdict(list)
    for r in rows:
        if r[5]:
            groups[(r[5], r[2])].append(r[0])
    merged = {}
    for (m, nm), gs in groups.items():
        if len(gs) > 1:
            for g in gs:
                merged[g] = "%s:%s" % (m, nm)
    for r in rows:
        r.append(merged.get(r[0], "own"))
    shared = len(set(merged.values()))
    people_merged = len(merged)
    fathers = len(rows) - people_merged + shared

    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["geni_id", "token", "implied_father_given_name", "modal_count",
                    "confirmed_fathers_for_token", "mother_geni_id", "father_group"])
        w.writerows(rows)

    top = Counter(r[2] for r in rows)
    md = ["# The fathers the patronymics imply", "",
          "Built by `scripts/build-patronymic-fathers.py` on top of "
          "`reports/patronymic-classification.csv`, which decides what is a patronymic from "
          "the father, per Emma 2026-08-15. **It emits no edit.**", "",
          "- bearers classified `patronymic (inferred, no father recorded)`: **%d**" % len(inferred),
          "- of those, a name is available from confirmed fathers: **%d**" % len(rows),
          "- token has no confirmed father anywhere, so no name: **%d**" % sum(unnamed.values()),
          "- **fathers to create: %d**" % fathers,
          "  (%d people merged into %d shared fathers under her same-mother rule)"
          % (people_merged, shared), "",
          "## The name comes from real fathers, never from the string", "",
          "`Olsen` implies **Ole** because that is what 1,809 confirmed `Olsen` fathers are "
          "called. An earlier version stripped the suffix and produced a father called "
          "**`Ols`**, which is what Emma meant by *\"we already addressed this\"*.", "",
          "| implied father | bearers |", "| --- | ---: |"]
    md += ["| %s | %d |" % (k, v) for k, v in top.most_common(25)]
    md += ["", "## One per person, with the exception she named", "",
           "*\"If you don't know the people are siblings you create one per individual.\"* "
           "The exception is a shared mother plus the same implied name, and it fires for "
           "**%d people forming %d shared fathers**. Where the names differ under one "
           "mother they are not merged." % (people_merged, shared), "",
           "## Sourcing", "",
           "Each created father is sourced to **the Geni profile of the child whose "
           "patronymic attests him** (Emma, 2026-08-19)."]
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("  named from confirmed fathers: %d; no confirmed father for token: %d"
          % (len(rows), sum(unnamed.values())))
    print("  fathers to create: %d (%d merged into %d shared)"
          % (fathers, people_merged, shared))
    print("  commonest: " + ", ".join("%s %d" % (k, v) for k, v in top.most_common(8)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
