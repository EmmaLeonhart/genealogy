"""What `NSFX` actually contains, and whether Wikidata's own labels keep it.

`correspondence.md` marks `NSFX` **TO ANALYSE**: *"assuming it is always a title
is exactly the kind of guess Emma has stopped."*

It bears directly on a rule she did give, 2026-08-11: *"a noble suffix or a noble
particle is a legitimately common thing in English, to the point that it makes it
useless to do that rule on Latin names"* — so the suffix stays in, and the Latin
display name becomes both the `mul` and the `en` label.

That is checkable rather than arguable. For the people carrying both IDs,
Wikidata already holds an English label a human chose. **Does it contain the
suffix?** If Wikidata writes `Henry III of England` where Geni writes `Henry III
King of England`, keeping the suffix produces a label Wikidata would not have
written — which does not make the rule wrong, but is worth knowing before it
ships.

Reads `reports/display-names.csv`. Writes:

* `reports/nsfx-census.csv` — one row per `NAME` record carrying an `NSFX`
* `reports/nsfx.md` — the finding

    py scripts/analyse-nsfx.py
"""

from __future__ import annotations

import csv
import sys
import unicodedata
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE = REPO_ROOT / "reports" / "display-names.csv"
OUT_CSV = REPO_ROOT / "reports" / "nsfx-census.csv"
OUT_MD = REPO_ROOT / "reports" / "nsfx.md"

csv.field_size_limit(10_000_000)


def fold(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    for ch in ".,;:()":
        text = text.replace(ch, " ")
    return " ".join(text.casefold().split())


def main() -> int:
    rows = []
    values: Counter[str] = Counter()
    by_script: Counter[str] = Counter()
    total_names = 0
    in_display = 0
    linked = 0
    label_has_all = 0
    label_has_some = 0
    label_has_none = 0
    examples: dict[str, list[tuple[str, str, str, str]]] = {"all": [], "some": [], "none": []}
    base_kinds: dict[str, Counter[str]] = {"all": Counter(), "some": Counter(), "none": Counter()}

    with open(SOURCE, encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            total_names += 1
            nsfx = (row["nsfx"] or "").strip()
            if not nsfx:
                continue

            values[nsfx] += 1
            by_script[row["scripts"] or "(none)"] += 1

            display = row["display_name"] or ""
            # GEDCOM renders NPFX GIVN /SPFX SURN/ NSFX, so the suffix should be
            # in the rendered line. Measured rather than assumed.
            present = fold(nsfx) in fold(display)
            in_display += present

            en = (row["wikidata_en"] or "").strip()
            verdict = ""
            base_kind = ""
            if row["qid"] and en:
                linked += 1
                label_tokens = set(fold(en).split())
                nsfx_tokens = [t for t in fold(nsfx).split() if t]
                kept = sum(1 for t in nsfx_tokens if t in label_tokens)
                if nsfx_tokens and kept == len(nsfx_tokens):
                    verdict, label_has_all = "all", label_has_all + 1
                elif kept:
                    verdict, label_has_some = "some", label_has_some + 1
                else:
                    verdict, label_has_none = "none", label_has_none + 1

                # "Keeps none" conflates two very different things: Wikidata
                # dropping the suffix from the same name, and Wikidata using a
                # different name altogether. The display-name report hit exactly
                # this — `Vittorio Emanuele … di Savoia` against `Victor
                # Emmanuel II of Italy` is not a stripped suffix. Separate them
                # by asking whether the name *without* the suffix survives.
                base = [t for t in fold(display).split() if t not in set(nsfx_tokens)]
                shared = sum(1 for t in base if t in label_tokens)
                if not base:
                    base_kind = "suffix was the whole name"
                elif shared == 0:
                    base_kind = "different name entirely"
                elif shared == len(base):
                    base_kind = "same name, suffix dropped"
                else:
                    base_kind = "name partly shared"
                base_kinds[verdict][base_kind] += 1
                if len(examples[verdict]) < 12:
                    examples[verdict].append((row["geni_id"], row["qid"], display, en))

            rows.append(
                [
                    row["geni_id"],
                    row["name_index"],
                    row["scripts"],
                    row["name_raw"],
                    display,
                    nsfx,
                    "yes" if present else "no",
                    row["qid"],
                    en,
                    verdict,
                ]
            )

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "geni_id", "name_index", "scripts", "name_raw", "display_name",
                "nsfx", "nsfx_in_display_name", "qid", "wikidata_en", "label_keeps_nsfx",
            ]
        )
        writer.writerows(rows)

    n = len(rows)
    L: list[str] = []
    add = L.append
    add("# `NSFX`: what is in it, and whether Wikidata's labels keep it")
    add("")
    add("`correspondence.md` marked this **TO ANALYSE** rather than guessing that the")
    add("field always holds a title. Censused from `reports/display-names.csv`; every")
    add("instance is a row in `reports/nsfx-census.csv`.")
    add("")
    add(f"**{n:,} of {total_names:,} `NAME` records carry an `NSFX`** "
        f"({100.0*n/max(total_names,1):.1f}%), holding **{len(values):,} distinct values**.")
    add("")
    add(f"`NSFX` appears inside the rendered display name in **{in_display:,} of {n:,}** "
        f"({100.0*in_display/max(n,1):.1f}%) — GEDCOM renders `NPFX GIVN /SPFX SURN/ NSFX`,")
    add("so this is the specification holding, measured rather than assumed.")
    add("")
    add("## What is actually in the field — top 40 by frequency")
    add("")
    add("| value | records |")
    add("| --- | ---: |")
    for value, count in values.most_common(40):
        add(f"| `{value}` | {count:,} |")
    add("")
    add("## By script")
    add("")
    add("| script | records |")
    add("| --- | ---: |")
    for script, count in by_script.most_common(10):
        add(f"| {script} | {count:,} |")
    add("")
    add("## Does Wikidata's own English label keep the suffix?")
    add("")
    add("Emma's rule, 2026-08-11, is that the Latin display name becomes the `en` label")
    add("**with the suffix left in**, because a noble suffix is how the name is written")
    add("in English. This measures what Wikidata did for the people carrying both IDs.")
    add("")
    add(f"Of the {linked:,} `NSFX`-carrying records whose person has an English label:")
    add("")
    add("| Wikidata's label | records | share |")
    add("| --- | ---: | ---: |")
    for key, label in (("all", "keeps every suffix token"), ("some", "keeps part"), ("none", "keeps none")):
        count = {"all": label_has_all, "some": label_has_some, "none": label_has_none}[key]
        add(f"| {label} | {count:,} | {100.0*count/max(linked,1):.1f}% |")
    add("")
    none_kinds = base_kinds["none"]
    none_total = sum(none_kinds.values()) or 1
    add("### And \"keeps none\" is two different things")
    add("")
    add("A label sharing no suffix token may have **dropped the suffix** from the same")
    add("name, or may be a **different name entirely** — the trap")
    add("`reports/display-names.md` already hit, where `Vittorio Emanuele … di Savoia`")
    add("against `Victor Emmanuel II of Italy` is not a stripped suffix at all. Splitting")
    add("the bucket by whether the name *without* its suffix survives into the label:")
    add("")
    add("| | records | share of \"keeps none\" |")
    add("| --- | ---: | ---: |")
    for kind, count in none_kinds.most_common():
        add(f"| {kind} | {count:,} | {100.0*count/none_total:.1f}% |")
    add("")
    add("**This does not overturn the rule.** Wikidata's label is what Wikidata chose;")
    add("Emma's rule is about what *we* produce for people who have no label yet, and")
    add("`correspondence.md` already records that labels are only in scope for people")
    add("carrying both IDs and that Wikidata is definitive where it has one. What the")
    add("table sizes is how far the two conventions differ where both exist.")
    add("")
    for key, heading in (
        ("none", "Where Wikidata keeps none of the suffix"),
        ("some", "Where Wikidata keeps part of it"),
        ("all", "Where Wikidata keeps all of it"),
    ):
        if not examples[key]:
            continue
        add(f"### {heading}")
        add("")
        add("| geni | item | Geni display name | Wikidata `en` |")
        add("| --- | --- | --- | --- |")
        for geni_id, qid, display, en in examples[key]:
            add(f"| `{geni_id}` | {qid} | {display} | {en} |")
        add("")

    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"{n:,} NSFX records of {total_names:,} NAME records, {len(values):,} distinct values")
    print(f"in the rendered display name: {in_display:,} ({100.0*in_display/max(n,1):.1f}%)")
    print(f"linked with an en label: {linked:,}")
    print(f"  keeps all: {label_has_all:,}  part: {label_has_some:,}  none: {label_has_none:,}")
    print(f"wrote {OUT_CSV} and {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
