"""Resolve the ambiguous given-name tokens: by the bearer's sex, then by script.

    python scripts/resolve-ambiguous-names.py

**Emma, 2026-08-24**, asked how the batch should handle the tokens that resolve to more
than one Wikidata item: *resolve by the person's sex, emit*.

**Her rule settles two of the seven, and the reason the other four resist it is worth
stating rather than working around.** `Martin`, `Anton`, `Emil` and `Eliza` each have two
candidates *of the same sex*, so sex has nothing to separate. What separates them is the
`mul` label:

    Martin   Q118322765  mul = Мартин     <- the Russian name
             Q18002399   mul = Martin     <- the Latin-script name

That is `CLAUDE.md` § *A diacritic makes a different name* taken one step further. If
`María`, `Mária` and `Marià` are three items on purpose, then `Мартин` and `Martin` are
certainly two, and picking the Cyrillic item for a Norwegian farmer would be wrong in the
same way. So the second rule is: **the candidate whose `mul` label is the token itself.**

Both rules are conservative — where neither decides, the token is left unresolved and
reported, never guessed. `Olga` comes out that way here: it is not in
`reports/name-ambiguity-resolved.csv` at all, so this has no candidates to choose between.

Reads `reports/name-ambiguity-resolved.csv`, `reports/name-item-qids.tsv` and
`reports/name-item-languages.csv`. Writes `reports/ambiguous-names-resolved.tsv`.
Entirely offline.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

#: `CLAUDE.md` § Wikidata properties and items.
MALE_GIVEN = "Q12308941"     # male given name
FEMALE_GIVEN = "Q11879590"   # female given name
UNISEX_GIVEN = "Q3409032"    # unisex given name


def load_classes():
    out = {}
    path = ROOT / "reports" / "name-item-qids.tsv"
    if path.exists():
        with open(path, encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                out[row["qid"]] = set(row["classes"].split())
    with open(ROOT / "reports" / "name-item-languages.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out.setdefault(row["qid"], set(row["classes"].split()))
    return out


def load_mul():
    out = {}
    with open(ROOT / "reports" / "name-item-languages.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[row["qid"]] = (row.get("mul") or "").strip()
    return out


def resolve(token, candidates, sex, classes, mul):
    """`(qid, why)` or `(None, why not)`. Sex first — it is Emma's rule."""
    if sex in ("M", "F"):
        wanted = MALE_GIVEN if sex == "M" else FEMALE_GIVEN
        exact = [q for q in candidates if wanted in classes.get(q, set())]
        others = [q for q in candidates if q not in exact]
        # Only decisive when it actually narrows to one AND the rejected candidate is
        # not simply unisex, which would fit this person too.
        if len(exact) == 1 and not any(UNISEX_GIVEN in classes.get(q, set())
                                       and len(candidates) == 2 for q in exact):
            return exact[0], f"sex {sex} selects the {'male' if sex == 'M' else 'female'} item"
        if len(exact) == 1 and all(UNISEX_GIVEN in classes.get(q, set()) or
                                   wanted in classes.get(q, set()) for q in others):
            return exact[0], f"sex {sex} selects the sex-specific item over the unisex one"

    # Script: the candidate whose `mul` label IS the token.
    same = [q for q in candidates if mul.get(q, "") == token]
    if len(same) == 1:
        rejected = [f"{q} mul={mul.get(q) or '(none)'}"
                    for q in candidates if q != same[0]]
        return same[0], f"mul label matches the token; rejected {', '.join(rejected)}"

    return None, ("no rule decides: "
                  + ", ".join(f"{q} mul={mul.get(q) or '(none)'}" for q in candidates))


def main():
    classes, mul = load_classes(), load_mul()

    # The tokens this frontier actually needs, and the sex of their bearer.
    needed = {"Marie": "F", "Ola": "M", "Martin": "M", "Anton": "M",
              "Emil": "M", "Eliza": "F", "Olga": "F"}

    found = {}
    with open(ROOT / "reports" / "name-ambiguity-resolved.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["kind"] == "given" and row["name"] in needed:
                found[row["name"]] = [q.strip() for q in row["qid"].split("|")
                                      if q.strip()]

    out = []
    for token, sex in sorted(needed.items()):
        candidates = found.get(token, [])
        if not candidates:
            out.append((token, sex, "", "", "no candidates recorded for this token"))
            continue
        qid, why = resolve(token, candidates, sex, classes, mul)
        out.append((token, sex, qid or "", " | ".join(candidates), why))

    dest = ROOT / "reports" / "ambiguous-names-resolved.tsv"
    with open(dest, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["token", "bearer_sex", "qid", "candidates", "why"])
        w.writerows(out)

    got = sum(1 for r in out if r[2])
    print(f"wrote {dest.relative_to(ROOT)}: {got} of {len(out)} resolved\n")
    for token, sex, qid, cands, why in out:
        mark = qid or "UNRESOLVED"
        print(f"  {token:<8} {sex}  {mark:<14} {why}")


if __name__ == "__main__":
    main()
