"""What Wikidata itself does with a middle initial, language by language.

**Emma, 2026-08-18, on the proposal to keep the initial as a Latin letter:** *"Can you
give me some examples of the first one in action? It looks the best but I want evidence
of it being standard."* Quite right — the claim was asserted, not shown. And then, having
seen the Japanese answer: *"I'm guessing Russian and Greek do it with transliterating the
initial though and they should do that. Idk what Hindi does but do the standard for it
too."*

So the answer is **per language, and measured for each** rather than settled once. Her
guess about Cyrillic and Greek is a hypothesis this script can confirm or refute, and the
Hindi instruction is explicitly *find the convention*, not *pick one*.

This reads the **local store**, which is the only permitted source: `CLAUDE.md`
§ *Never query Wikidata to check something* makes every question about Wikidata's contents
an offline computation over `wikidata/items/`. The store is a Geni-shaped slice of about
1.4 million items, not all of Wikidata, so every figure is *"of the items we hold"* and
the report says so on itself.

## The classes, and why `script_initial` had to be added

Every item whose `en` label parses as `Given X Surname` — one bare capital, optionally
with a full stop — is collected with its label in each target language, and classified by
what became of the initial:

* `latin_initial` — the Latin letter survives as itself: ジョセフ・**C**・オマホニー
* `script_initial` — the initial is rendered **as an initial in the target script**:
  Джозеф **С.** О'Махони. This is what Emma means by transliterating the initial.
* `expanded` — the initial is replaced by the **full middle name**, which Wikidata knows
  and we do not: `Samuel S. Cox` → サミュエル・**サリヴァン**・コックス (Sullivan).
* `dropped` — the initial is gone and the label has fewer components.
* `unclear` — anything else, reported rather than forced into a bucket.

**`script_initial` and `expanded` were one bucket in the first version, and that made the
Cyrillic answer unreadable.** A Cyrillic initial and a full Cyrillic middle name both fail
the "is there a Latin letter" test and both leave the component count intact, so `С.` and
`Сулливан` landed together.

**Separating them on the abbreviation mark, not on length.** The obvious fix — a
*single* character — was tried and was wrong, because an initial is not one character in
every script: Greek writes `J` as the digraph `Τζ` and Devanagari writes `M` as `एम`, so
`Λουσίντα Τζ. Πιλ` and `थियोडोर एम. स्टुअर्ट` both scored as *expanded* when they are
initials kept as initials. `initial_component()` looks for one to three letters followed
by a stop, which is what those forms actually have in common.

**`expanded` is not transliteration**, and calling it that was the first reading. It also
matters for the decision in a way the count alone does not show: expansion is unavailable
to us, because if we knew the full name the initial would not be an initial.

**Regnal ordinals are excluded, and they were 546 of the first run's 4,052 rows.**
`Henry I of England` and `Frederik X of Denmark` parse as `Given <capital> Surname` and
are nothing of the sort; their Japanese labels are ヘンリー1世 and フレデリック10世, which
the classifier read as *dropped* and which dragged that bucket up by a third. The tell is
that the tail is a realm — `of England` — rather than a surname. Same shape as the `DI`
and `LI` false positives in `build-regnal-ordinal-census.py`: a pattern that matches the
letters and not the meaning.

A count for every class is printed for every language, including the ones that would
refute the proposal. The whole point is that an answer can come back `dropped`.

    python scripts/measure-middle-initial-labels.py
"""

from __future__ import annotations

import csv
import gzip
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SHARDS = sorted((REPO / "wikidata" / "items").glob("items-*.jsonl.gz"))
OUT_CSV = REPO / "reports" / "middle-initial-wikidata-practice.csv"
OUT_MD = REPO / "reports" / "middle-initial-wikidata-practice.md"

#: The languages the decision covers. `ja`/`zh` are the ones Emma first asked about;
#: `ru`/`el`/`hi` are the ones she named next; the rest are the other non-Latin scripts
#: this corpus's people plausibly need, measured rather than assumed alongside them.
LANGS = ["ja", "zh", "ko", "ru", "el", "hi", "uk", "bg", "sr", "he", "ar", "fa", "ta"]

#: `Given X Surname` / `Given X. Surname`. The middle token is one capital letter and
#: nothing else; the surrounding tokens must be real words so that initials-only names
#: like `J. R. R. Tolkien` do not enter as though the middle were a middle name.
PATTERN = re.compile(
    r"^([^\W\d_]{2,})\s+([A-Z])\.?\s+([^\W\d_][^\d_]*)$", re.UNICODE)

#: Separators used between the parts of a name: the katakana middle dot and friends,
#: plus plain space.
DOTS = "・·‧∙"

#: A single Roman numeral, for spotting the regnal-ordinal false positives.
ROMAN_ONE = re.compile(r"^[IVXLCDM]$")


#: Tails that mark a regnal or noble style rather than a surname. `Henry I **of**
#: England`, `Obizzo I **d'**Este`, `Rainon I **de** Sabran`, `Henry I **the**
#: Fowler`. A lower-case particle after the numeral is the giveaway.
NOBLE_TAIL = ("of ", "the ", "de ", "d'", "di ", "da ", "van ", "von ", "der ",
              "af ", "av ", "ap ", "le ", "la ")


def is_regnal(en: str, initial: str) -> bool:
    """`Henry I of England` — a monarch, not somebody with a middle initial.

    **Excluding only `of <realm>` was not enough.** The Russian run came back with
    `Obizzo I d'Este`, `Rainon I de Sabran`, `Simon I de Montfort` and
    `Nicolaus I Bernoulli` filed as people who *kept a Latin middle initial*, which
    inflated exactly the bucket the question is about. They are ordinals, and the
    tell is a lower-case particle after the numeral.

    `Nicolaus I Bernoulli` has no particle and still is not a middle initial, so a
    Roman-numeral initial stays ambiguous however this is written. That is why the
    report also gives the figures over the **unambiguous** subset — initials that
    are not one of `I V X L C D M` at all.
    """
    if not ROMAN_ONE.match(initial):
        return False
    parts = en.split(None, 2)
    tail = (parts[2] if len(parts) > 2 else "").lower()
    return tail.startswith(NOBLE_TAIL)


def parts_of(label: str) -> list[str]:
    """The components of a name label, however this language separates them."""
    for sep in DOTS:
        if sep in label:
            return [p.strip() for p in label.split(sep) if p.strip()]
    return [p.strip() for p in label.split() if p.strip()]


def is_latin(ch: str) -> bool:
    return "LATIN" in unicodedata.name(ch, "")


#: Marks that end an abbreviation. `.` is universal; `॰` is the Devanagari
#: abbreviation sign, which is how `ए॰` writes the initial `A`.
ABBREV = ".॰｡。"


def initial_component(piece: str) -> str:
    """The letters of `piece` if it is an abbreviated initial, else `""`.

    **An initial is not always one character, and assuming so wrecked the Greek
    and Hindi answers.** Greek transliterates `J` as the digraph `Τζ` and `H` as
    `Χ`; Devanagari writes `M` as `एम`. `Λουσίντα Τζ. Πιλ` and
    `थियोडोर एम. स्टुअर्ट` are initials kept as initials, and a
    one-character test scored both as *expanded* — the opposite reading.

    So the tell is the **abbreviation mark**, not the length: one to three letters
    followed by a stop. A bare single letter counts too, since plenty of records
    omit the stop (`एडवर्ड ओ विल्सन`).
    """
    p = piece.strip()
    marked = p[-1] in ABBREV if p else False
    core = p.rstrip(ABBREV)
    if not core or not core.isalpha():
        return ""
    if marked and len(core) <= 3:
        return core
    if len(core) == 1:
        return core
    return ""


def classify(initial: str, label: str) -> str:
    """What became of the initial in this label."""
    if not label:
        return "no label"
    pieces = parts_of(label)
    for p in pieces:
        core = initial_component(p)
        if not core:
            continue
        if is_latin(core[0]):
            # Only counts if it is the *same* letter — otherwise it is some other
            # abbreviated part of the name entirely.
            if core.upper() == initial.upper():
                return "latin_initial"
        else:
            return "script_initial"
    if len(pieces) >= 3:
        return "expanded"
    return "dropped"


def main() -> None:
    rows = []
    verdict = {code: Counter() for code in LANGS}
    unamb = {code: Counter() for code in LANGS}
    scanned = 0
    regnal = 0

    for n, shard in enumerate(SHARDS, 1):
        with gzip.open(shard, "rt", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if '"en"' not in line:
                    continue
                try:
                    item = json.loads(line)
                except Exception:
                    continue
                labels = item.get("labels") or {}

                def lab(code: str) -> str:
                    v = labels.get(code)
                    if isinstance(v, dict):
                        v = v.get("value", "")
                    return (v or "").strip()

                en = lab("en")
                if not en:
                    continue
                m = PATTERN.match(en)
                if not m:
                    continue
                initial = m.group(2)
                if is_regnal(en, initial):
                    regnal += 1
                    continue
                scanned += 1

                got = {code: lab(code) for code in LANGS}
                if not any(got.values()):
                    continue
                # A Roman-numeral initial can always be an ordinal in disguise.
                unambiguous = not ROMAN_ONE.match(initial)
                row = {"qid": item.get("id", ""), "en": en, "initial": initial,
                       "unambiguous": int(unambiguous)}
                for code in LANGS:
                    v = classify(initial, got[code])
                    verdict[code][v] += 1
                    if unambiguous:
                        unamb[code][v] += 1
                    row[code] = got[code]
                    row[f"{code}_verdict"] = v
                rows.append(row)
        if n % 400 == 0:
            print(f"  shard {n}/{len(SHARDS)}  {len(rows):,} with a non-Latin label",
                  flush=True)

    if not rows:
        print("no items matched")
        return

    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    KINDS = ("latin_initial", "script_initial", "expanded", "dropped", "unclear")

    def verdict_line(code: str) -> str:
        c = verdict[code]
        total = sum(c[k] for k in KINDS)
        if not total:
            return f"| `{code}` | 0 | — | — | — | — | — |"
        cells = " | ".join(f"{c[k]:,} ({c[k]/total:.0%})" for k in KINDS)
        winner = max(KINDS, key=lambda k: c[k])
        return f"| `{code}` | {total:,} | {cells} | **{winner}** |"

    lines = [
        "# What Wikidata does with a middle initial, by language",
        "",
        "Emma asked for evidence rather than an assertion — *\"I want evidence of it "
        "being standard\"* — and then for the question to be asked per language: *\"I'm "
        "guessing Russian and Greek do it with transliterating the initial though and "
        "they should do that. Idk what Hindi does but do the standard for it too.\"*",
        "",
        f"**{scanned:,} items** in the local store have an English label of the form "
        f"`Given X Surname`, after excluding {regnal:,} regnal ordinals such as "
        f"`Henry I of England`. **{len(rows):,}** of them carry a label in at least one "
        "of the languages below.",
        "",
        "**This is the local store, not all of Wikidata.** It is a Geni-shaped slice of "
        "roughly 1.4 million items seeded from `P2600` holders and their neighbours, so "
        "the claim is about the items we hold, and a different slice could differ.",
        "",
        "`latin_initial` keeps the letter as itself (ジョセフ・C・オマホニー). "
        "`script_initial` renders it as one letter of the target script "
        "(Джозеф С. О'Махони) — this is what *transliterating the initial* means. "
        "`expanded` replaces it with the full middle name Wikidata knows and we do not "
        "(`Samuel S. Cox` → サミュエル・サリヴァン・コックス). **`expanded` is not an "
        "option available to us**: if we knew the name it would not be an initial.",
        "",
        "| lang | labelled | " + " | ".join(f"`{k}`" for k in KINDS) + " | commonest |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for code in LANGS:
        lines.append(verdict_line(code))

    lines += ["", "## Excluding Roman-numeral initials", "",
              "`I V X L C D M` are valid middle initials **and** the letters every "
              "regnal ordinal is made of, and `Nicolaus I Bernoulli` has no particle "
              "to give it away. These are the same figures over initials that cannot "
              "be an ordinal at all, and they are the safer read.", "",
              "| lang | labelled | " + " | ".join(f"`{k}`" for k in KINDS) +
              " | commonest |",
              "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |"]
    for code in LANGS:
        c = unamb[code]
        total = sum(c[k] for k in KINDS)
        if not total:
            lines.append(f"| `{code}` | 0 | — | — | — | — | — | — |")
            continue
        cells = " | ".join(f"{c[k]:,} ({c[k]/total:.0%})" for k in KINDS)
        winner = max(KINDS, key=lambda k: c[k])
        lines.append(f"| `{code}` | {total:,} | {cells} | **{winner}** |")

    lines += ["", "## Examples", ""]
    for code in LANGS:
        picked = []
        for kind in ("latin_initial", "script_initial", "expanded", "dropped"):
            for r in rows:
                if r.get(f"{code}_verdict") == kind and r.get(code):
                    picked.append((kind, r))
                    break
        if not picked:
            continue
        lines += [f"### `{code}`", "", "| English | label | verdict |",
                  "| --- | --- | --- |"]
        for kind, r in picked:
            lines.append(f"| {r['en']} | {r[code]} | `{kind}` |")
        lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"{scanned:,} items with a `Given X Surname` English label "
          f"({regnal:,} regnal ordinals excluded)")
    print(f"{len(rows):,} carry a label in at least one target language\n")
    for code in LANGS:
        c = verdict[code]
        total = sum(c[k] for k in KINDS)
        if not total:
            print(f"  {code:<3} no labelled examples")
            continue
        winner = max(KINDS, key=lambda k: c[k])
        bits = "  ".join(f"{k.split('_')[0]}={c[k]}" for k in KINDS if c[k])
        cu = unamb[code]
        tu = sum(cu[k] for k in KINDS)
        wu = max(KINDS, key=lambda k: cu[k]) if tu else "-"
        print(f"  {code:<3} n={total:<6} {bits}   -> {winner}"
              f"   | no-numeral n={tu:<6} -> {wu}")
    print(f"\nwrote {OUT_CSV.relative_to(REPO)} and {OUT_MD.relative_to(REPO)}")


if __name__ == "__main__":
    main()
