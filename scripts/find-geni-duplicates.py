"""Actual duplicate Geni profiles: same name, same parent.

    python scripts/find-geni-duplicates.py

**Emma, 2026-08-24:** *"Find profiles that look similar like shared parents, plus look
over basically all Japanese items with higher scrutiny."*

**The signal is two children of one parent bearing the same name.** Parents do not
normally give two surviving children the same name, so a shared parent plus a shared
name is a duplicate far more often than it is a coincidence — and unlike a name match
alone it cannot fire across the whole corpus, because the parent pins it to one family.
`CLAUDE.md` bans name matching as a *merge* mechanism; this is a name match **inside a
structural bracket**, producing candidates for a human, which is the same shape as the
Bureätten anchor walk.

A second, weaker pass finds **same name and same birth year with no parent recorded**,
because an unparented duplicate is exactly what a re-created biblical or clan profile
looks like — `CLAUDE.md` § *A second Geni ID on one Wikidata item*. Those are reported
separately and never mixed in with the strong ones.

**Nothing is merged and nothing is rewritten.** Emma's standing rule: the duplicate
merges are hers, flag and never perform. This writes records.

**Japanese profiles are marked, not filtered.** She asked for higher scrutiny over them,
so the report carries a `script` column and sorts them first; it does not drop the rest.

Writes `reports/geni-duplicate-candidates.tsv`.
"""
from __future__ import annotations

import collections
import csv
import sys
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

ROOT = Path(__file__).resolve().parent.parent

#: Placeholder names. Two children called `NN` are not evidence of anything — a parent
#: with several unnamed children is ordinary, and treating them as duplicates would
#: bury the real cases. `CLAUDE.md`: NN is *nomen nescio*, a real statement that the
#: name is unknown.
NOT_A_NAME = {"", "nn", "n n", "n.n.", "private", "unknown", "?", "??", "???",
              "ukjent", "okänd", "ukendt"}


def is_placeholder(name):
    """True for a redaction marker, however much surname is attached to it.

    **The first run got this wrong and it buried everything.** `NOT_A_NAME` matched only
    bare markers, so `<private> SOERIANAGARA` sailed through and seventeen redacted
    children of one man came out as the top "duplicate" — they are seventeen living
    people Geni is withholding, which is the opposite of one person recorded twice.
    All fifteen of the first run's leading rows were this.
    """
    low = normalise(name)
    if low in NOT_A_NAME:
        return True
    if "<private>" in low:
        return True
    # A placeholder GIVEN name with a real surname attached is still a placeholder:
    # `NN Steele`, `N.N. Schnelle`, `nn Busch`, `FNU Seligmann`, `Infant Swartzentruber`.
    # Eight children of one man all recorded `NN Steele` are eight unnamed children,
    # not one child recorded eight times -- the same error as `<private> SOERIANAGARA`,
    # one layer in. `FNU` is "first name unknown" and `Infant` names a died-in-infancy
    # child, which is a statement about the person rather than a name.
    first = low.split()[0] if low.split() else ""
    return first in NOT_A_NAME | {"fnu", "lnu", "infant", "baby", "stillborn",
                                  "twin", "son", "daughter", "child"}


def normalise(name):
    """Case and whitespace fold only.

    **Diacritics are kept.** `CLAUDE.md` § *A diacritic makes a different name*: folding
    them manufactured ambiguity for 1,312 names once already, and here it would pair
    siblings who are genuinely differently named.
    """
    return " ".join(unicodedata.normalize("NFC", (name or "")).lower().split())


def script_of(name):
    """`Han`, `Kana`, `Latin` or `mixed` — for the higher-scrutiny Japanese pass."""
    kinds = set()
    for ch in name or "":
        if not ch.isalpha():
            continue
        try:
            block = unicodedata.name(ch).split()[0]
        except ValueError:
            continue
        kinds.add({"CJK": "Han", "HIRAGANA": "Kana", "KATAKANA": "Kana"}.get(
            block, "Latin"))
    if not kinds:
        return ""
    return kinds.pop() if len(kinds) == 1 else "mixed"


def main():
    labels, years = {}, {}
    with open(ROOT / "reports" / "derived-labels.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            labels[row["geni_id"]] = row.get("label_en") or row.get("label_mul") or ""
    print(f"{len(labels):,} people")

    with open(ROOT / "reports" / "derived-facts.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("birth_date_year"):
                years[row["geni_id"]] = row["birth_date_year"]

    # -- the strong signal: same parent, same name --------------------------
    children = collections.defaultdict(list)
    parentless = []
    with open(ROOT / "reports" / "derived-family.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            father = (row.get("father") or "").strip()
            mother = (row.get("mother") or "").strip()
            if father or mother:
                children[(father, mother)].append(row["geni_id"])
            else:
                parentless.append(row["geni_id"])
    print(f"{len(children):,} distinct parent pairs; {len(parentless):,} with no parent")

    rows = []
    for (father, mother), kids in children.items():
        if len(kids) < 2:
            continue
        by_name = collections.defaultdict(list)
        for kid in kids:
            raw = labels.get(kid, "")
            key = normalise(raw)
            if key and not is_placeholder(raw):
                by_name[key].append(kid)
        for key, group in by_name.items():
            if len(group) < 2:
                continue
            name = labels.get(group[0], "")
            rows.append({
                "signal": "same parent, same name",
                "script": script_of(name),
                "name": name,
                "geni_ids": ";".join(sorted(group)),
                "count": len(group),
                "shared_father": father,
                "shared_mother": mother,
                "father_name": labels.get(father, ""),
                "mother_name": labels.get(mother, ""),
                "birth_years": ";".join(sorted({years.get(g, "") for g in group}) - {""})
                if False else ";".join(sorted({years.get(g, "") for g in group if
                                               years.get(g)})),
            })

    # -- the weak signal: no parent, same name AND same birth year ----------
    unparented = collections.defaultdict(list)
    for gid in parentless:
        raw = labels.get(gid, "")
        key = normalise(raw)
        year = years.get(gid)
        if key and not is_placeholder(raw) and year:
            unparented[(key, year)].append(gid)
    for (key, year), group in unparented.items():
        if len(group) < 2:
            continue
        name = labels.get(group[0], "")
        rows.append({
            "signal": "no parent, same name and birth year",
            "script": script_of(name),
            "name": name,
            "geni_ids": ";".join(sorted(group)),
            "count": len(group),
            "shared_father": "", "shared_mother": "",
            "father_name": "", "mother_name": "",
            "birth_years": year,
        })

    # Japanese first, then the biggest groups. Her instruction was higher scrutiny on
    # the Japanese ones, so they sort to the top rather than being filtered out.
    rows.sort(key=lambda r: (r["script"] not in ("Han", "Kana", "mixed"),
                             r["signal"] != "same parent, same name",
                             -r["count"], r["name"]))

    dest = ROOT / "reports" / "geni-duplicate-candidates.tsv"
    with open(dest, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    strong = [r for r in rows if r["signal"] == "same parent, same name"]
    cjk = [r for r in strong if r["script"] in ("Han", "Kana", "mixed")]
    print(f"\nwrote {dest.relative_to(ROOT)}")
    print(f"  {len(strong):,} same parent, same name  ({len(cjk):,} CJK)")
    print(f"  {len(rows) - len(strong):,} no parent, same name and birth year")
    print(f"  {sum(r['count'] for r in strong):,} profiles in the strong groups\n")
    for row in strong[:15]:
        who = row["father_name"] or row["mother_name"]
        print(f"  [{row['script'] or '?':<5}] {row['name'][:34]:<34} ×{row['count']}"
              f"  child of {who[:26]}")


if __name__ == "__main__":
    main()
