"""Formulaic labels for the CJK people whose Geni name is a marker, a clan and a place.

    python scripts/build-cjk-clan-labels.py

**Emma's ruling, 2026-08-28**, worked out on `Q10864996` and then generalised by her:
*"I think this formulation should be 'woman of the Li clan, from Longxi Didao' as the English
label and all languages have a similar thing but NN is the right mul."*

## The shape, and it is almost universal

Geni records these people as `某 /隴西狄道/` with `_MARNM 李`:

| field | value | what it is |
| --- | --- | --- |
| `GIVN` | `某` | the marker — Chinese *"a certain one"*, the sense of `NN` |
| `SURN` | `隴西狄道` | **a place** — Longxi commandery, Didao county |
| `_MARNM` | `李` | **the real clan surname** |

**348 of 354 records have exactly that shape**, and **every `_MARNM` is one character** (351 of
351) — which is what settles it: a one-character CJK value in the married-name field is a clan
surname, never a farm or a married name. This is `CLAUDE.md` § *`SURN` is not reliably a surname*
in its second instance, after `陳郡陽夏` / `謝`.

The three-way degradation is natural: clan and place, clan alone, place alone.

## Sex comes from the data, and assuming would have been wrong

**338 of the 354 records are male.** The case the formula was designed on — Wanshou — is one of
only 16 women, and printing the first ten rows gave an all-female sample that read as
representative. Emma, asked whether the men take the same formula: *"Yes — same formula, sex word
from the data."*

## `mul` is bare `NN`

Not `NN 隴西狄道`. The place is not the person's name, and splicing a Latin marker into a Han
label produces neither a Chinese label nor an English one. Her words: *"NN is the right mul."*

## `ja` and `zh` are deliberately absent

The Han material is right there and it would be easy to assemble something like `京兆長安李氏`.
It is left out because the idiomatic form of *"a man of the Li clan, of Jingzhao Chang'an"* in
Chinese or Japanese is a question about those languages, not about this data, and `CLAUDE.md`
holds that a half-right label is worse than none. Raise it rather than guess.

Writes `reports/cjk-clan-labels.tsv`.

## `CJK_CLAN_BLOCK` has a hand-written tail this script does not produce

`build-garborg-day.CJK_CLAN_BLOCK` is a pasted literal, and since 2026-08-29 it ends with a
short section for **`Q11443857` Mononobe no Futohime** — a *named* woman of a named clan, which
is a different case from the 177 unnamed ones here and comes from `entity_resolution.md` rather
than from any measurement. **Regenerating the block from this script's output and pasting over
the literal would silently drop her.** Keep the tail.
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
TRANSLIT = ROOT / "reports" / "cjk-clan-place-transliterations.tsv"
PARTIAL = ROOT / "reports" / "partial-nn.csv"
FACTS = ROOT / "reports" / "derived-facts.csv"
OUT = ROOT / "reports" / "cjk-clan-labels.tsv"

CJK = re.compile(r"[぀-ヿ一-鿿가-힯]")

#: `{lang: (man, woman, "of the {clan} clan", "from {place}")}` — the two halves are kept apart
#: so a record with only a clan, or only a place, degrades without a second table.
PHRASES = {
    "en": ("man", "woman", "of the {clan} clan", "from {place}"),
    "nb": ("mann", "kvinne", "av {clan}-slekten", "fra {place}"),
    "da": ("mand", "kvinde", "af {clan}-slægten", "fra {place}"),
    "sv": ("man", "kvinna", "av {clan}-ätten", "från {place}"),
    "de": ("Mann", "Frau", "des Klans {clan}", "aus {place}"),
    "nl": ("man", "vrouw", "van de {clan}-clan", "uit {place}"),
    "es": ("hombre", "mujer", "del clan {clan}", "de {place}"),
    "it": ("uomo", "donna", "del clan {clan}", "da {place}"),
    "pt": ("homem", "mulher", "do clã {clan}", "de {place}"),
    "ca": ("home", "dona", "del clan {clan}", "de {place}"),
}


def main() -> None:
    tr = {}
    with open(TRANSLIT, encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            tr[row["han"]] = row["latin"]

    sex_of = {}
    with open(FACTS, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            sex_of[row["geni_id"]] = (row.get("sex") or "").strip()

    people, missing = {}, collections.Counter()
    with open(PARTIAL, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["shape"].startswith("nothing survives"):
                continue
            if not (row.get("qid") or "").startswith("Q"):
                continue
            if not CJK.search(row["display_name"]):
                continue
            clan = (row.get("marnm") or "").strip()
            place = (row.get("surn") or "").strip()
            if clan and clan not in tr:
                missing[clan] += 1
            if place and place not in tr:
                missing[place] += 1
            people.setdefault(row["qid"], (row["geni_id"], clan, place))

    if not people:
        sys.exit("no CJK partial-NN people matched at all — that is a broken read of "
                 f"{PARTIAL.name}, not a corpus without them")
    if missing:
        sys.exit(f"untransliterated tokens, so some label would come out half Han: "
                 f"{dict(missing)}. Add them to {TRANSLIT.name} rather than emitting a "
                 f"partial label.")

    rows, by_sex = [], collections.Counter()
    for qid, (geni_id, clan, place) in sorted(people.items()):
        sex = sex_of.get(geni_id, "")
        by_sex[sex or "(unrecorded)"] += 1
        out = {"qid": qid, "geni_id": geni_id, "clan_han": clan, "place_han": place,
               "clan": tr.get(clan, ""), "place": tr.get(place, ""), "sex": sex, "mul": "NN"}
        for lang, (male, female, clan_part, place_part) in PHRASES.items():
            # **No label at all when the sex is unrecorded.** The sentence cannot be built
            # without it, and `man`/`woman` is not something to default.
            if not sex:
                continue
            who = male if sex == "M" else female
            parts = []
            if clan:
                parts.append(clan_part.format(clan=tr[clan]))
            if place:
                parts.append(place_part.format(place=tr[place]))
            out[lang] = f"{who} {', '.join(parts)}" if parts else ""
        rows.append(out)

    fields = (["qid", "geni_id", "clan_han", "place_han", "clan", "place", "sex", "mul"]
              + list(PHRASES))
    with open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t")
        w.writeheader()
        w.writerows([{k: r.get(k, "") for k in fields} for r in rows])

    print(f"{len(rows)} people; sex {dict(by_sex)}")
    print(f"{sum(1 for r in rows if r.get('en'))} get a description in "
          f"{len(PHRASES)} languages; the rest have no recorded sex")
    print(f"\nwrote {OUT.resolve().relative_to(ROOT)}\n")
    for r in rows[:6]:
        print(f"   {r['qid']:<12} mul=NN   en={r.get('en', '')}")


if __name__ == "__main__":
    main()
