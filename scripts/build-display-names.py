"""Every display name of every person in the merged tree, one row per NAME record.

Emma, 2026-08-11: *"you're supposed to be making giant CSV files of all of these
things that we are observing and then analysing them. You should be doing this,
and you should be committing and pushing these CSV files. 1. CSV file: the display
name of every single person. Every single display name that the person has goes
into it as different entries in the CSV file. 2. You commit and push it.
3. You analyse it."*

And: *"We're not trying to make the repo small. We don't care about repo size. We
care about actually getting results."* So the output is committed.

A person with four `NAME` records produces four rows. The rendered display name
is the `NAME` line with the slashes removed — GEDCOM 5.5.1 puts the name in
spoken order with the surname enclosed in slashes, and the spec says systems must
construct the name from this line rather than from the optional pieces. The
pieces are carried alongside anyway, because the question of which field feeds
what is exactly what is being modelled.

Script is recorded, never language. Emma: *"we are sorting by scripts. We are not
sorting by languages. We will sort by languages later."*

Offline: the merged GEDCOM plus the downloaded Wikidata store. Nothing is
queried.

    py scripts/build-display-names.py
"""

from __future__ import annotations

import csv
import sys
import unicodedata
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from genimerge import wikistore  # noqa: E402

MERGED = REPO_ROOT / "out" / "merged.ged"
PAIRS = REPO_ROOT / "out" / "wikidata" / "p2600-all.tsv"
STORE = REPO_ROOT / "wikidata" / "items"
INDEX = REPO_ROOT / "out" / "wikidata" / "store-index.sqlite3"
OUTPUT = REPO_ROOT / "reports" / "display-names.csv"

#: The level-2 tags under a NAME record that Geni actually emits. Measured over
#: the corpus, not assumed: GIVN, _MARNM, SURN, NICK, NSFX, CONC.
NAME_PIECES = ("NPFX", "GIVN", "NICK", "SPFX", "SURN", "NSFX", "_MARNM")

COLUMNS = [
    "geni_id",
    "name_index",
    "name_count",
    "name_raw",
    "display_name",
    "scripts",
    "npfx",
    "givn",
    "nick",
    "spfx",
    "surn",
    "nsfx",
    "marnm",
    "marnm_equals_surn",
    "qid",
    "wikidata_en",
    "wikidata_mul",
]

#: Unicode script names as they appear in `unicodedata.name`, folded to a short
#: label. Anything unlisted is reported by its own first word rather than being
#: bucketed as "other" — an unlabelled script is a finding, not noise.
SCRIPT_WORDS = {
    "LATIN": "Latin",
    "CJK": "Han",
    "HIRAGANA": "Hiragana",
    "KATAKANA": "Katakana",
    "HANGUL": "Hangul",
    "CYRILLIC": "Cyrillic",
    "GREEK": "Greek",
    "ARABIC": "Arabic",
    "HEBREW": "Hebrew",
    "DEVANAGARI": "Devanagari",
    "THAI": "Thai",
    "ARMENIAN": "Armenian",
    "GEORGIAN": "Georgian",
    "BENGALI": "Bengali",
    "TAMIL": "Tamil",
    "ETHIOPIC": "Ethiopic",
    "MYANMAR": "Myanmar",
    "KHMER": "Khmer",
    "LAO": "Lao",
    "TIBETAN": "Tibetan",
    "SYRIAC": "Syriac",
    "THAANA": "Thaana",
    "SINHALA": "Sinhala",
    "TELUGU": "Telugu",
    "KANNADA": "Kannada",
    "MALAYALAM": "Malayalam",
    "GUJARATI": "Gujarati",
    "GURMUKHI": "Gurmukhi",
    "ORIYA": "Oriya",
}

#: First words of Unicode character names that are **not writing systems**, and
#: therefore contribute no script at all.
#:
#: **This cost 646 people their label.** `str.isalpha()` is `True` for `º`
#: (`MASCULINE ORDINAL INDICATOR`), so the classifier below invented a script
#: called `Masculine`; `derive-labels.py` then read `scripts = Latin+Masculine`,
#: called the name mixed-script, and refused it as an `en` or `mul` label. Every
#: one of the 646 is an Iberian noble whose title carries an ordinal —
#: `Afonso de Bragança 1º conde de Faro e 2º de Odemira`,
#: `Maria da Cunha 3ª senhora de Basto`, `Mª Manuela Fernández de Córdoba`.
#:
#: **Contributing nothing is right, and calling them Latin would be wrong.** `º`
#: says nothing about which script a name is written in; it is a typographic sign
#: that happens to be a letter to Python. A string of nothing but ordinals
#: classifies as `none`, which is the truth about it.
#:
#: Counted over the corpus, 943 `NAME` records carry one: Masculine 739,
#: Modifier 105, Feminine 86, plus single Superscript and Micro. `Unnamed` stays
#: out of this set on purpose — a character with no Unicode name at all is a
#: finding worth surfacing, not a typographic sign to skip.
NOT_A_SCRIPT = {
    "MASCULINE",   # º ordinal indicator
    "FEMININE",    # ª ordinal indicator
    "MODIFIER",    # ʹ ˈ ʼ modifier letters
    "SUPERSCRIPT",
    "MICRO",       # µ
    "OHM",
    "KELVIN",
    "ANGSTROM",
    "ESTIMATED",
    "INFORMATION",
}


def scripts_of(text: str) -> str:
    """Every script present among the letters, alphabetical, `+`-joined.

    Mixed-script names stay visible as mixed rather than being forced into one
    bucket — `Izabelė iš Angulemo` and `誉田別命 /応神天皇/` are different
    problems and a single dominant-script label would hide the first kind.

    A character that is a letter to Python but not part of a writing system —
    see `NOT_A_SCRIPT` — contributes nothing, so `1º senhor de Baião` is Latin.
    """
    found: set[str] = set()
    for char in text:
        if not char.isalpha():
            continue
        name = unicodedata.name(char, "")
        if not name:
            found.add("Unnamed")
            continue
        word = name.split()[0]
        if word in NOT_A_SCRIPT:
            continue
        found.add(SCRIPT_WORDS.get(word, word.title()))
    return "+".join(sorted(found))


def display_name(name_value: str) -> str:
    """The NAME line rendered: slashes dropped, whitespace normalised."""
    return " ".join(name_value.replace("/", " ").split())


def read_pairs() -> dict[str, str]:
    """geni_id -> qid, skipping any Geni ID sitting on more than one item.

    `p2600-all.tsv` is `qid<TAB>geni_id` with no header, the opposite order from
    `p2600-map.tsv`; the first token is checked rather than the path trusted.
    """
    if not PAIRS.exists():
        return {}
    qids_for: dict[str, set[str]] = {}
    with open(PAIRS, encoding="utf-8") as handle:
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) == 2 and parts[0].startswith("Q"):
                qids_for.setdefault(parts[1], set()).add(parts[0])
    return {g: next(iter(q)) for g, q in qids_for.items() if len(q) == 1}


def read_names() -> dict[str, list[dict[str, str]]]:
    """Every NAME record of every INDI, with its pieces, in file order."""
    people: dict[str, list[dict[str, str]]] = {}
    current: str | None = None
    record: dict[str, str] | None = None

    with open(MERGED, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.startswith("0 "):
                current = None
                record = None
                parts = line.split()
                if len(parts) >= 3 and parts[2] == "INDI":
                    xref = parts[1]
                    if xref.startswith("@I") and xref.endswith("@"):
                        current = xref[2:-1]
                        people.setdefault(current, [])
                continue
            if current is None:
                continue
            if line.startswith("1 "):
                record = None
                if line.startswith("1 NAME"):
                    record = {"name_raw": line[6:].strip()}
                    people[current].append(record)
                continue
            if record is not None and line.startswith("2 "):
                parts = line[2:].rstrip("\n").split(None, 1)
                if parts and parts[0] in NAME_PIECES:
                    record[parts[0]] = parts[1].strip() if len(parts) > 1 else ""
    return people


def main() -> int:
    print("reading the merged GEDCOM", flush=True)
    people = read_names()
    rows = sum(len(v) for v in people.values())
    print(f"{len(people):,} people, {rows:,} NAME records", flush=True)

    pairs = read_pairs()
    print(f"{len(pairs):,} unambiguous Geni->Wikidata links", flush=True)

    linked = {g: q for g, q in pairs.items() if g in people}
    print(f"{len(linked):,} of our people carry an item; reading their labels", flush=True)
    labels: dict[str, tuple[str, str]] = {}
    if linked:
        with wikistore.StoreReader(STORE, INDEX) as reader:
            entities = reader.entities(sorted(set(linked.values())))
        for qid, entity in entities.items():
            item_labels = entity.get("labels") or {}
            labels[qid] = (
                (item_labels.get("en") or {}).get("value", ""),
                (item_labels.get("mul") or {}).get("value", ""),
            )
        print(f"{len(labels):,} items found in the store", flush=True)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    with open(OUTPUT, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(COLUMNS)
        for geni_id in sorted(people):
            records = people[geni_id]
            qid = linked.get(geni_id, "")
            en, mul = labels.get(qid, ("", ""))
            for index, record in enumerate(records):
                raw = record.get("name_raw", "")
                surn = record.get("SURN", "")
                marnm = record.get("_MARNM", "")
                writer.writerow(
                    [
                        geni_id,
                        index,
                        len(records),
                        raw,
                        display_name(raw),
                        scripts_of(raw),
                        record.get("NPFX", ""),
                        record.get("GIVN", ""),
                        record.get("NICK", ""),
                        record.get("SPFX", ""),
                        surn,
                        record.get("NSFX", ""),
                        marnm,
                        "yes" if marnm and marnm == surn else "no",
                        qid,
                        en,
                        mul,
                    ]
                )
                written += 1

    size = OUTPUT.stat().st_size
    print(f"wrote {OUTPUT} — {written:,} rows, {size / 1024 / 1024:.1f} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
