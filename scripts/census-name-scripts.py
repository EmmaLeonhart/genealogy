"""Which writing systems does our tree actually carry names in? Census before labelling.

    python scripts/census-name-scripts.py

**Emma, 2026-08-26:** *"really I think the ideal thing was supposed to be that we do a census of
all languages in the synoptic tree (our geni stuff) and we add labels in all of them. And I don't
think we fully did that."* She is right — nothing enumerated it.

## Script, not language, and the difference is the point

A name's **script** is determinable from the characters. Its **language** is not: `Иван` is
Russian, Ukrainian, Bulgarian or Serbian and the string cannot say which; `李` is Chinese,
Japanese or Korean. So this censuses scripts and names the languages each one *implies*, leaving
the choice to whoever writes the labels.

`CLAUDE.md` already records the cost of guessing here — `Q28513` was written down as *Empire of
Japan* when it is **Austria-Hungary**, which produced 1,406 fake Japanese isolates. A script
census that pretended to be a language census would be the same mistake with more rows.

## Where the names are

`reports/derived-labels.csv` splits them across four columns and the emitters read two:

* `label_en` and `label_mul` — the Latin forms, which every batch uses.
* `cjk_names` — **44,028 people**, read by nothing until 2026-08-26.
* `other_script_names` — **11,519 people**, still read by nothing.

The census covers all four, counts people rather than strings, and reports how many of each
script currently reach a Wikidata label at all.

Writes `reports/name-scripts.tsv` — one row per script — and `reports/name-scripts.md`.
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
LABELS = ROOT / "reports" / "derived-labels.csv"
OUT_TSV = ROOT / "reports" / "name-scripts.tsv"
OUT_MD = ROOT / "reports" / "name-scripts.md"

#: Unicode block prefix -> (script, the languages it implies). The languages are a
#: SUGGESTION for whoever writes labels, never a claim about the person.
BLOCKS = (
    ("CJK", "Han", "zh, ja, ko (hanja)"),
    ("HIRAGANA", "Kana", "ja"),
    ("KATAKANA", "Kana", "ja"),
    ("HANGUL", "Hangul", "ko"),
    ("CYRILLIC", "Cyrillic", "ru, uk, be, bg, sr, mk"),
    ("ARABIC", "Arabic", "ar, fa, ur"),
    ("HEBREW", "Hebrew", "he, yi"),
    ("GREEK", "Greek", "el"),
    ("DEVANAGARI", "Devanagari", "hi, mr, ne, sa"),
    ("THAI", "Thai", "th"),
    ("ARMENIAN", "Armenian", "hy"),
    ("GEORGIAN", "Georgian", "ka"),
    ("ETHIOPIC", "Ethiopic", "am, ti"),
    ("BENGALI", "Bengali", "bn"),
    ("TAMIL", "Tamil", "ta"),
    ("TELUGU", "Telugu", "te"),
    ("MYANMAR", "Myanmar", "my"),
    ("KHMER", "Khmer", "km"),
    ("LAO", "Lao", "lo"),
    ("SINHALA", "Sinhala", "si"),
    ("TIBETAN", "Tibetan", "bo"),
    ("MONGOLIAN", "Mongolian", "mn"),
    ("SYRIAC", "Syriac", "syc"),
    ("THAANA", "Thaana", "dv"),
    ("CHEROKEE", "Cherokee", "chr"),
    ("LATIN", "Latin", "en, no, sv, da, de, nl, fr, es, it"),
    # **Not scripts. Latin-script decoration that `unicodedata.name()` blocks separately.**
    # The first run reported `other (Masculine)` for 1,287 people, which is the ordinal
    # indicator in `Afonso de Braganca 1º conde`, and `other (Feminine)` for the `ª` in a
    # Portuguese name. Reporting those as writing systems would be inventing five scripts
    # the corpus does not have -- the same shape as `Q28513` becoming *Empire of Japan*.
    ("MASCULINE", "Latin", "en, no, sv, da, de, nl, fr, es, it"),
    ("FEMININE", "Latin", "en, no, sv, da, de, nl, fr, es, it"),
    ("MODIFIER", "Latin", "en, no, sv, da, de, nl, fr, es, it"),
    ("SUPERSCRIPT", "Latin", "en, no, sv, da, de, nl, fr, es, it"),
    ("MICRO", "Latin", "en, no, sv, da, de, nl, fr, es, it"),
)
LANG_OF = {name: langs for _prefix, name, langs in BLOCKS}


def scripts_in(text):
    """Every script present in a string, by Unicode block."""
    found = set()
    for ch in text or "":
        if not ch.isalpha():
            continue
        try:
            block = unicodedata.name(ch).split()[0]
        except ValueError:
            continue
        for prefix, script, _langs in BLOCKS:
            if block == prefix:
                found.add(script)
                break
        else:
            found.add(f"other ({block.title()})")
    return found


def main():
    people = collections.Counter()          # script -> people carrying it
    labelled = collections.Counter()        # script -> of those, reaching a Latin label
    sample = {}
    total = 0

    with open(LABELS, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            total += 1
            latin_label = bool((row.get("label_en") or "").strip()
                               or (row.get("label_mul") or "").strip())
            here = set()
            for col in ("label_en", "label_mul", "cjk_names", "other_script_names",
                        "further_latin_names"):
                here |= scripts_in(row.get(col) or "")
            for script in here:
                people[script] += 1
                if latin_label:
                    labelled[script] += 1
                if script not in sample and script != "Latin":
                    for col in ("cjk_names", "other_script_names", "label_mul"):
                        v = (row.get(col) or "").split(" | ")[0].strip()
                        if v and script in scripts_in(v):
                            sample[script] = (row["geni_id"], v[:30])
                            break

    if not people:
        sys.exit("no scripts detected at all -- that is a broken read of "
                 f"{LABELS.name}, not a corpus with no names in it")
    print(f"{total:,} people; {len(people)} scripts present\n")

    rows = []
    for script, n in people.most_common():
        gid, ex = sample.get(script, ("", ""))
        rows.append({
            "script": script, "people": n,
            "share": f"{n / total:.2%}",
            "with_a_latin_label": labelled[script],
            "without": n - labelled[script],
            "implies_languages": LANG_OF.get(script, ""),
            "example_geni_id": gid, "example": ex,
        })
    with open(OUT_TSV, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    lines = [
        "# Writing systems in the tree — a census, not a guess",
        "",
        f"{total:,} people in `reports/derived-labels.csv`, **{len(people)} scripts**.",
        "",
        "**Script is determinable; language is not.** `Иван` is Russian, Ukrainian, Bulgarian "
        "or Serbian and the string cannot say which; `李` is Chinese, Japanese or Korean. The "
        "`implies languages` column is a suggestion for whoever writes the labels, never a "
        "claim about the person. `CLAUDE.md` records what guessing costs here: `Q28513` was "
        "written down as *Empire of Japan* when it is **Austria-Hungary**, and that produced "
        "1,406 fake Japanese isolates.",
        "",
        "**`without a Latin label` is the column that matters.** Those people reach no batch "
        "at all today unless the non-Latin fallback catches them.",
        "",
        "| script | people | share | with a Latin label | without | implies | example |",
        "| --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for r in rows:
        lines.append(f"| {r['script']} | {r['people']:,} | {r['share']} | "
                     f"{r['with_a_latin_label']:,} | **{r['without']:,}** | "
                     f"{r['implies_languages']} | `{r['example']}` |")
    lines += ["", f"`{OUT_TSV.name}` is the same table, one row per script.", ""]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"{'script':<22}{'people':>10}{'no latin label':>16}  implies")
    for r in rows:
        print(f"{r['script']:<22}{r['people']:>10,}{r['without']:>16,}  "
              f"{r['implies_languages']}")
    print(f"\nwrote {OUT_MD.resolve().relative_to(ROOT)} and "
          f"{OUT_TSV.resolve().relative_to(ROOT)}")


if __name__ == "__main__":
    main()
