"""The Geni name records: how many, which fields, which scripts.

Emma asked for this one by name, 2026-08-12. The requirements, in her words:

* *"the portion of them that have one name object or one name field versus many"*
* *"the amount of name fields that have different things, like the married name,
  surname, first name, name suffix, and prefix"* and *"the rate of the fields"*
* *"the distribution between scripts"*, and the script split must be real:
  *"Latin versus Korean versus Chinese versus CJK versus CJK with kana versus
  Cyrillic versus whatever"*
* **the two mixed-script questions, which are different from each other**:
  *"A mixed script name often indicates some sort of attempt at a commentary or
  disambiguation within the name, whereas … a name that suggests multiple names
  and multiple scripts, just indicates multiple languages."*

So the report separates:

* **a mixed-script NAME record** — one string containing two writing systems,
  which is usually a gloss inside the name; and
* **a person carrying several single-script names** — which is usually the same
  person written in several languages.

Nothing here is a label. Geni names are language-agnostic strings; a Han name is
not Chinese, it is Han, and turning any of this into a label is a separate
pipeline that does not exist yet.

Reads `reports/display-names.csv`. Writes `reports/geni-names.md` and
`out/geni-name-records.csv`.

    py scripts/build-geni-names-report.py
"""

from __future__ import annotations

import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE = REPO_ROOT / "reports" / "display-names.csv"
OUT_MD = REPO_ROOT / "reports" / "geni-names.md"
#: **Deleted 2026-08-15**: `reports/geni-name-records.csv` duplicated
#: `display-names.csv` on all 11 shared columns across all 444,875 rows, and
#: its one extra column `script_class` is a pure function of `scripts`. Emma
#: approved removing it. This writes to `out/` now, so re-running the report
#: does not reintroduce the 41 MB duplicate into git.
OUT_CSV = REPO_ROOT / "out" / "geni-name-records.csv"

csv.field_size_limit(10_000_000)

#: Unicode "scripts" that are really symbols or marks and must not make a name
#: look mixed. `º` and `ª` are Spanish ordinal indicators; combining marks belong
#: to whatever they sit on. Counting these as scripts inflated an earlier pass by
#: 820 records.
NOT_A_SCRIPT = {"Masculine", "Feminine", "Modifier", "Combining", "Unnamed",
                "Ideographic", "Fullwidth", "Halfwidth"}

#: Han is deliberately *not* resolved to a language. Emma, 2026-08-12: if a name
#: is written solely in kanji the Japanese and Chinese labels are the same string,
#: so there is nothing to decide. Kana and Hangul do resolve, because they are
#: exclusive to one language.
def classify(scripts: str) -> str:
    parts = {p for p in scripts.split("+") if p and p not in NOT_A_SCRIPT}
    if not parts:
        return "no letters"
    kana = parts & {"Hiragana", "Katakana"}
    han = "Han" in parts
    hangul = "Hangul" in parts
    other = parts - {"Hiragana", "Katakana", "Han", "Hangul"}

    if len(parts) == 1:
        only = next(iter(parts))
        if only == "Han":
            return "Han only (Chinese or Japanese kanji)"
        if only in {"Hiragana", "Katakana"}:
            return "kana only (Japanese)"
        if only == "Hangul":
            return "Hangul (Korean)"
        return only
    if kana and han and not other:
        return "Han + kana (Japanese)"
    if hangul and han and not other:
        return "Han + Hangul (Korean)"
    if kana and not other:
        return "kana (Japanese)"
    return "MIXED: " + "+".join(sorted(parts))


def main() -> int:
    per_person: dict[str, list[dict]] = defaultdict(list)
    with open(SOURCE, encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            per_person[row["geni_id"]].append(row)

    people = len(per_person)
    records = sum(len(v) for v in per_person.values())

    names_per_person: Counter[int] = Counter()
    field_records: Counter[str] = Counter()
    field_people: Counter[str] = Counter()
    classes: Counter[str] = Counter()
    mixed_combos: Counter[str] = Counter()
    mixed_examples: dict[str, list[str]] = defaultdict(list)
    person_profile: Counter[str] = Counter()
    multi_script_combos: Counter[str] = Counter()
    first_class: Counter[str] = Counter()
    first_differs = 0
    marnm_rel: Counter[str] = Counter()

    fields = ("givn", "surn", "marnm", "nsfx", "npfx", "nick", "spfx")
    out_rows = []

    for geni_id, rows in per_person.items():
        names_per_person[len(rows)] += 1
        seen_fields: set[str] = set()
        classes_here: list[str] = []

        for row in rows:
            cls = classify(row["scripts"])
            classes[cls] += 1
            classes_here.append(cls)
            if cls.startswith("MIXED"):
                combo = cls.removeprefix("MIXED: ")
                mixed_combos[combo] += 1
                if len(mixed_examples[combo]) < 5 and row["display_name"]:
                    mixed_examples[combo].append(row["display_name"])

            for field in fields:
                if row.get(field, "").strip():
                    field_records[field] += 1
                    seen_fields.add(field)

            surn = (row.get("surn") or "").strip()
            marnm = (row.get("marnm") or "").strip()
            if marnm and not surn:
                marnm_rel["_MARNM only, SURN empty"] += 1
            elif marnm and marnm == surn:
                marnm_rel["identical"] += 1
            elif marnm and surn:
                marnm_rel["differ"] += 1
            elif surn:
                marnm_rel["SURN only"] += 1
            else:
                marnm_rel["neither"] += 1

            out_rows.append([geni_id, row["name_index"], row["name_raw"],
                             row["scripts"], cls,
                             *[row.get(f, "") for f in fields]])

        for field in seen_fields:
            field_people[field] += 1

        distinct = {c for c in classes_here if c != "no letters"}
        pure = {c for c in distinct if not c.startswith("MIXED")}
        if any(c.startswith("MIXED") for c in distinct):
            person_profile["has a mixed-script name"] += 1
        if len(pure) > 1:
            person_profile["several names, several scripts"] += 1
            multi_script_combos[" + ".join(sorted(pure))] += 1
        elif len(pure) == 1 and len(rows) > 1:
            person_profile["several names, all one script"] += 1
        elif len(rows) == 1:
            person_profile["one name only"] += 1

        first_class[classes_here[0] if classes_here else "no letters"] += 1
        if len(distinct) > 1:
            first_differs += 1

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["geni_id", "name_index", "name_raw", "scripts",
                         "script_class", *fields])
        writer.writerows(out_rows)

    # Is the first-listed name systematically Latin? Only people carrying both a
    # pure-Latin and a pure non-Latin name can answer that; for everyone else the
    # ordering has nothing to choose between.
    def bucket(cls: str) -> str:
        if cls == "Latin":
            return "Latin"
        if cls.startswith("MIXED"):
            return "mixed"
        if cls == "no letters":
            return "none"
        return "non-Latin"

    order_first: Counter[str] = Counter()
    order_idx: Counter[int] = Counter()
    shares: list[float] = []
    for rows in per_person.values():
        ordered = sorted(rows, key=lambda r: int(r["name_index"]))
        buckets = [bucket(classify(r["scripts"])) for r in ordered]
        if "Latin" not in buckets or "non-Latin" not in buckets:
            continue
        order_first[f"{buckets[0]} first"] += 1
        order_idx[min(buckets.index("Latin"), 5)] += 1
        pure = [b for b in buckets if b in ("Latin", "non-Latin")]
        shares.append(pure.count("Latin") / len(pure))
    order_total = sum(order_first.values())
    order_observed = order_first["Latin first"] / max(order_total, 1)
    order_expected = sum(shares) / max(len(shares), 1)

    L: list[str] = []
    add = L.append
    add("# Geni name records: how many, which fields, which scripts")
    add("")
    add("Asked for by Emma, 2026-08-12. Every `NAME` record is a row in")
    add("`out/geni-name-records.csv`.")
    add("")
    add(f"**{people:,} people, {records:,} `NAME` records.**")
    add("")
    add("**Nothing here is a label.** Geni names are language-agnostic strings. A Han")
    add("name is not Chinese, it is Han — and per Emma, if a name is written solely in")
    add("kanji the Japanese and Chinese labels are the *same string*, so there is nothing")
    add("to decide. Only kana and Hangul resolve to a language, because only they are")
    add("exclusive to one.")
    add("")
    add("## How many names each person has")
    add("")
    add("| names | people | share |")
    add("| ---: | ---: | ---: |")
    for count in sorted(names_per_person):
        if count <= 8 or names_per_person[count] > 50:
            n = names_per_person[count]
            add(f"| {count} | {n:,} | {100.0*n/people:.1f}% |")
    many = sum(v for k, v in names_per_person.items() if k > 8)
    add(f"| 9 or more | {many:,} | {100.0*many/people:.1f}% |")
    add("")
    one = names_per_person[1]
    add(f"**{one:,} people ({100.0*one/people:.1f}%) have exactly one name record**; "
        f"{people-one:,} have several.")
    add("")
    add("## Which fields are filled")
    add("")
    add("| field | records | share of records | people | share of people |")
    add("| --- | ---: | ---: | ---: | ---: |")
    labels = {"givn": "GIVN given name", "surn": "SURN surname",
              "marnm": "_MARNM married name", "nsfx": "NSFX suffix",
              "npfx": "NPFX prefix", "nick": "NICK nickname",
              "spfx": "SPFX surname prefix"}
    for field in fields:
        add(f"| {labels[field]} | {field_records[field]:,} | "
            f"{100.0*field_records[field]/records:.1f}% | {field_people[field]:,} | "
            f"{100.0*field_people[field]/people:.1f}% |")
    add("")
    add("### `_MARNM` against `SURN`, per record")
    add("")
    add("| | records | share |")
    add("| --- | ---: | ---: |")
    for kind, n in marnm_rel.most_common():
        add(f"| {kind} | {n:,} | {100.0*n/records:.1f}% |")
    add("")
    add("## Scripts, per name record")
    add("")
    add("| script class | records | share |")
    add("| --- | ---: | ---: |")
    for cls, n in classes.most_common(24):
        add(f"| {cls} | {n:,} | {100.0*n/records:.2f}% |")
    add("")
    add("## The two mixed-script questions, which are different")
    add("")
    add("Emma: *\"A mixed script name often indicates some sort of attempt at a")
    add("commentary or disambiguation within the name, whereas … a name that suggests")
    add("multiple names and multiple scripts, just indicates multiple languages.\"*")
    add("")
    mixed_total = sum(mixed_combos.values())
    add(f"### One record, two scripts inside it — {mixed_total:,} records")
    add("")
    add("| scripts in one name | records |")
    add("| --- | ---: |")
    for combo, n in mixed_combos.most_common(15):
        add(f"| {combo} | {n:,} |")
    add("")
    add("Examples, which show the gloss-inside-the-name pattern:")
    add("")
    for combo, n in mixed_combos.most_common(5):
        for example in mixed_examples[combo][:3]:
            add(f"- `{combo}` — {example}")
    add("")
    add("### One person, several names in different scripts")
    add("")
    add("| | people | share |")
    add("| --- | ---: | ---: |")
    for kind, n in person_profile.most_common():
        add(f"| {kind} | {n:,} | {100.0*n/people:.1f}% |")
    add("")
    add("| script combination across a person's names | people |")
    add("| --- | ---: |")
    for combo, n in multi_script_combos.most_common(15):
        add(f"| {combo} | {n:,} |")
    add("")
    add("## The first-listed name")
    add("")
    add("Emma: *\"I believe that the first listed name in the files is usually the one")
    add("that is treated as being in English and taking priority, but Geni is weird about")
    add("English names. A lot of stuff is recorded as being English when it's not.\"*")
    add("")
    add("Whatever the first record means, this is what script it is in:")
    add("")
    add("| script class of the first name | people | share |")
    add("| --- | ---: | ---: |")
    for cls, n in first_class.most_common(12):
        add(f"| {cls} | {n:,} | {100.0*n/people:.1f}% |")
    add("")
    add(f"**{first_differs:,} people ({100.0*first_differs/people:.1f}%) have names in")
    add("more than one script class**, so for them the first record is a choice among")
    add("scripts rather than the only option.")
    add("")
    add("### The first slot is privileged, and this is by how much")
    add("")
    add("Over the people carrying **both** a pure-Latin and a pure non-Latin name — the")
    add("only ones where the ordering can mean anything:")
    add("")
    add("| the first record is | people | share |")
    add("| --- | ---: | ---: |")
    for kind, n in sorted(order_first.items(), key=lambda kv: -kv[1]):
        add(f"| {kind} | {n:,} | {100.0*n/max(order_total,1):.1f}% |")
    add("")
    add(f"Against a null model — order random, weighted by how many Latin and non-Latin")
    add("names each person actually has:")
    add("")
    add(f"    observed  P(first record is Latin) = {order_observed:.3f}")
    add(f"    random    expected                 = {order_expected:.3f}")
    add("")
    add("So the first slot is **not** arbitrary. And a Latin name sits at position 0 or 1")
    add(f"for {100.0*(order_idx[0]+order_idx[1])/max(order_total,1):.1f}% of them.")
    add("")
    add("**What leads when Latin does not** is the informative part: almost every such")
    add("case is a *mixed-script* record in front — `Constantine /Δούκας/` ahead of")
    add("`Constantine Doukas Byzantine Co-emperor`. So slot 0 holds the primary name, and")
    add("when that primary is itself a Latin-plus-native hybrid the pure Latin form is")
    add("pushed to second.")
    add("")
    add("**This does not establish that slot 0 is English.** Temüjin's first record is")
    add("Cyrillic+Latin. The corpus carries **zero `LANG` subtags**, so what it")
    add("establishes is that the slot is privileged, not what language it claims.")

    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {OUT_MD} and {OUT_CSV} ({len(out_rows):,} rows)")
    print(f"  {people:,} people, {records:,} name records")
    print(f"  one name only: {one:,} ({100.0*one/people:.1f}%)")
    print(f"  mixed-script records: {mixed_total:,}")
    print(f"  people with names in >1 script class: {first_differs:,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
