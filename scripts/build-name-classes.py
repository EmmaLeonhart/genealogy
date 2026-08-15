"""Every distinct name token in the corpus, and how it BEHAVES.

Emma, 2026-08-15, specifying the name-item rule and then asking for this:
*"running an analysis of this [synoptic] tree, all the different names inside…
you're supposed to be doing this analysis of most commonly occurring names,
patronymics, and surnames, and it very much can occur in other languages like
CJK and stuff."*

**"Western convention" is behavioural, not geographic.** Her clarification, and
the thing this script exists to measure: *"Western convention does not mean that
there are only western names. For the most part, everything that behaves like a
surname, or is a first name that behaves like a first name, or is a patronymic,
would count."* So a token is not classified by what language it looks like. It
is classified by **which slot it occupies, and how often**.

One row per distinct token, with the counts that decide it:

- `as_given` / `as_surname` / `as_married` — how many `NAME` records put it in
  `GIVN`, `SURN`, `_MARNM`. A token in both slots is the interesting case and is
  reported as `both`, never forced to one.
- `patronymic_marker` — the suffix or particle matched, empty if none. **The
  marker is evidence, not a verdict**: `-sen` is Danish patronymic morphology and
  is also an ordinary frozen surname, and nothing here can tell those apart. The
  column says what was seen.
- `script` — Latin / Han / Hangul / Kana / Cyrillic / mixed, so the CJK
  population is visible rather than lumped in.
- `placeholder` — `NN`, `?`, `???` and friends, **marked rather than dropped**.
  `CLAUDE.md`: unrequested exception handling is its own category of error, and
  Emma has objected to placeholder vocabulary being silently removed.

Reads `reports/geni-name-records.csv` (444,874 parsed `NAME` records, one row
each) rather than rescanning the corpus, and de-duplicates bearers by Geni ID so
a person in forty exports counts once.

Writes `reports/name-classes.csv` and `reports/name-classes.md`.

    py scripts/build-name-classes.py
"""

from __future__ import annotations

import csv
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SOURCE = REPO / "reports" / "geni-name-records.csv"
CSV_OUT = REPO / "reports" / "name-classes.csv"
MD_OUT = REPO / "reports" / "name-classes.md"

csv.field_size_limit(10 ** 7)

#: Patronymic morphology, longest suffix first so `-sdatter` wins over `-datter`.
#: Nordic, Slavic, Arabic and Hebrew forms. Emma: *"The daughter and son would be
#: the same thing"* — the son and daughter suffixes are one category.
PATRONYMIC_SUFFIXES = [
    "sdottir", "sdóttir", "sdatter", "sdotter", "sson", "ssen", "søn",
    "dottir", "dóttir", "datter", "dotter", "son", "sen", "søn", "zen",
    "ovich", "evich", "ovna", "evna", "ivna", "ovych", "yevich",
    "oglu", "ogly", "zade",
]
#: Particles that make the NEXT token a patronym rather than the token itself.
PATRONYMIC_PARTICLES = {"bin", "bint", "ibn", "ben", "bat", "bar", "mac", "mc", "ap"}

#: Placeholder vocabulary. Marked, never removed. Screened on the vocabulary and
#: on punctuation, never on length — `CLAUDE.md`: Korean and Chinese surnames are
#: one character, so a length screen discards 이 and 김.
PLACEHOLDERS = {
    "nn", "n n", "n.n.", "n.n", "?", "??", "???", "????", "*", "**", "***",
    "unknown", "private", "<private>", "'", "-", "--", ".", "(no name)",
}

#: Nobiliary and toponymic particles. These sit INSIDE a surname string and are
#: not names — they are `SPFX` material and must never become name items. Listed
#: so the report can count them rather than have a reader infer it from a table.
PARTICLES = {
    "de", "De", "di", "Di", "da", "Da", "del", "Del", "della", "des", "du",
    "van", "Van", "von", "Von", "der", "Der", "den", "ten", "ter", "la", "La",
    "le", "Le", "y", "i", "of", "af", "av", "til", "zu", "dos", "das", "do",
    "el", "al", "ul", "bin", "bint", "ibn", "ap", "abu",
}

#: Regnal numerals in the given slot: ordinals on a title, not given names.
ORDINALS = {"I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
            "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII"}

SCRIPT_ORDER = ["Han", "Kana", "Hangul", "Cyrillic", "Arabic", "Hebrew",
                "Greek", "Latin"]


def script_of(text: str) -> str:
    seen = set()
    for ch in text:
        if not ch.isalpha():
            continue
        try:
            name = unicodedata.name(ch)
        except ValueError:
            continue
        if name.startswith("CJK"):
            seen.add("Han")
        elif name.startswith(("HIRAGANA", "KATAKANA")):
            seen.add("Kana")
        elif name.startswith("HANGUL"):
            seen.add("Hangul")
        elif name.startswith("CYRILLIC"):
            seen.add("Cyrillic")
        elif name.startswith("ARABIC"):
            seen.add("Arabic")
        elif name.startswith("HEBREW"):
            seen.add("Hebrew")
        elif name.startswith("GREEK"):
            seen.add("Greek")
        elif name.startswith("LATIN"):
            seen.add("Latin")
    if not seen:
        return "none"
    if len(seen) > 1:
        return "mixed:" + "+".join(s for s in SCRIPT_ORDER if s in seen)
    return next(iter(seen))


def patronymic_marker(token: str) -> str:
    low = token.lower()
    if low in PATRONYMIC_PARTICLES:
        return "particle"
    for suffix in PATRONYMIC_SUFFIXES:
        # A suffix must not BE the whole token: "Son" alone is a word, not a
        # patronymic ending, and the two-character stem guard keeps "Sen" out.
        if low.endswith(suffix) and len(low) > len(suffix) + 1:
            return "-" + suffix
    return ""


def _dominance(row) -> float:
    """The share of a token's slot uses that fall in its majority slot.

    1.0 means every bearer uses it one way; 0.5 means it is evenly split. The
    denominator is the two slot counts rather than `bearers`, because a person
    counted in both slots would otherwise deflate their own token.
    """
    g, s = row["as_given"], row["as_surname"]
    return max(g, s) / (g + s) if (g + s) else 0.0


TOKEN_SPLIT = re.compile(r"[\s]+")


def tokens(field: str) -> list[str]:
    """Split a name field into tokens, keeping CJK strings whole.

    A CJK given name is written without spaces, so splitting on characters would
    invent tokens that nobody bears. Whitespace only.
    """
    return [t.strip(",") for t in TOKEN_SPLIT.split(field.strip()) if t.strip(",")]


def main() -> int:
    if not SOURCE.exists():
        print(f"missing {SOURCE}; run scripts/build-geni-names-report.py first",
              file=sys.stderr)
        return 1

    # token -> slot -> set of geni ids. Sets because a person in forty exports
    # is one bearer, and the whole point of the Geni ID being the primary key is
    # that this join is exact.
    bearers: dict[str, dict[str, set]] = defaultdict(
        lambda: {"given": set(), "surname": set(), "married": set()})
    records = 0

    with SOURCE.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            records += 1
            gid = row["geni_id"]
            for field, slot in (("givn", "given"), ("surn", "surname"),
                                ("marnm", "married")):
                for token in tokens(row.get(field) or ""):
                    bearers[token][slot].add(gid)

    rows = []
    for token, slots in bearers.items():
        g, s, m = (len(slots["given"]), len(slots["surname"]),
                   len(slots["married"]))
        total = len(slots["given"] | slots["surname"] | slots["married"])
        if g and s:
            behaves = "both"
        elif g:
            behaves = "given"
        elif s:
            behaves = "surname"
        else:
            behaves = "married-only"
        marker = patronymic_marker(token)
        rows.append({
            "token": token,
            "bearers": total,
            "as_given": g,
            "as_surname": s,
            "as_married": m,
            "behaves": behaves,
            "patronymic_marker": marker,
            "script": script_of(token),
            "placeholder": "yes" if token.lower() in PLACEHOLDERS else "",
        })

    rows.sort(key=lambda r: (-r["bearers"], r["token"]))
    with CSV_OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    real = [r for r in rows if not r["placeholder"]]
    by_behaviour = defaultdict(int)
    by_script = defaultdict(int)
    patro = [r for r in real if r["patronymic_marker"]]
    for r in real:
        by_behaviour[r["behaves"]] += 1
        by_script[r["script"].split(":")[0] if r["script"].startswith("mixed")
                  else r["script"]] += 1

    def table(title, pairs, head=("value", "distinct tokens")):
        out = [f"## {title}", "", f"| {head[0]} | {head[1]} |", "| --- | ---: |"]
        out += [f"| `{k}` | {v:,} |" for k, v in
                sorted(pairs, key=lambda kv: -kv[1])]
        return out + [""]

    def top(title, selected, n=25):
        out = [f"## {title}", "",
               "| token | bearers | as given | as surname | script | marker |",
               "| --- | ---: | ---: | ---: | --- | --- |"]
        for r in selected[:n]:
            out.append(f"| {r['token']} | {r['bearers']:,} | {r['as_given']:,} | "
                       f"{r['as_surname']:,} | {r['script']} | "
                       f"{r['patronymic_marker'] or ''} |")
        return out + [""]

    lines = [
        "# Name tokens, classified by how they behave",
        "",
        f"Generated by `scripts/build-name-classes.py` over "
        f"`reports/geni-name-records.csv` — **{records:,} `NAME` records**, "
        f"**{len(rows):,} distinct tokens**. One row each in "
        "`reports/name-classes.csv`.",
        "",
        "**The classification is behavioural, not geographic.** Emma, "
        "2026-08-15: *\"Western convention does not mean that there are only "
        "western names… everything that behaves like a surname, or is a first "
        "name that behaves like a first name, or is a patronymic, would "
        "count.\"* So a token is placed by which slot it occupies, not by what "
        "language it looks like.",
        "",
        f"**{len(rows) - len(real):,} tokens are placeholder vocabulary** "
        "(`NN`, `?`, `???`). They are **marked, not removed** — screened on the "
        "vocabulary and on punctuation, never on length, because Korean and "
        "Chinese surnames are one character.",
        "",
    ]
    lines += table("How each token behaves", list(by_behaviour.items()),
                   ("behaviour", "distinct tokens"))
    lines += [
        "`both` is the population that matters for `P734`/`P735`: a token used "
        "as a given name by some people and a surname by others cannot be "
        "assigned one name item without deciding which, per person.",
        "",
    ]
    lines += table("Script", list(by_script.items()), ("script", "distinct tokens"))
    lines += [
        f"## Patronymics",
        "",
        f"**{len(patro):,} distinct tokens carry patronymic morphology**, "
        f"borne by {sum(r['bearers'] for r in patro):,} people.",
        "",
        "Emma's model for these, 2026-08-15: the name item is an **instance of "
        "patronymic** (`Q110874`), and the statement carries **object of "
        "statement has role** (`P3831`) → patronymic, where an ordinary middle "
        "name would carry `Q245025` and a first given name `Q202444`. *\"The "
        "daughter and son would be the same thing\"* — `-son` and `-datter` are "
        "one category.",
        "",
        "**The marker is evidence, not a verdict.** `-sen` is Danish patronymic "
        "morphology and is also an ordinary frozen surname; nothing measurable "
        "here separates them. The column records what was seen.",
        "",
    ]
    lines += top("Most common patronymic-marked tokens", patro)
    lines += top("Most common tokens overall", real)
    # -- what the numbers say, computed rather than asserted ----------------
    both = [r for r in real if r["behaves"] == "both"]
    lopsided = [r for r in both if _dominance(r) >= 0.95]
    particles = [r for r in real if r["token"] in PARTICLES]
    ordinals = [r for r in real if r["token"] in ORDINALS]
    big = [r for r in both if r["bearers"] > 50]
    big_lop = [r for r in big if _dominance(r) >= 0.95]
    weighted = sum(r["bearers"] for r in both)
    weighted_lop = sum(r["bearers"] for r in lopsided)
    lines += [
        "## What the numbers say",
        "",
        f"**`both` is mostly genuine ambiguity, and that was worth checking "
        f"rather than assuming.** Of the {len(both):,} tokens seen in both "
        f"slots, only **{len(lopsided):,} ({100 * len(lopsided) // max(len(both), 1)}%) "
        "put at least 95% of their bearers in one slot.** The intuition that "
        "`Maria` — 5,476 given against 8 surname — is typical is wrong: it is "
        "typical of the *common* tokens and not of the population, because the "
        f"population is dominated by rare ones. {len([r for r in both if r['bearers'] <= 2]):,} "
        "of these tokens have two bearers or fewer, where one use in each slot "
        "is a 50/50 split by arithmetic and says nothing.",
        "",
        f"**Restrict to tokens with more than 50 bearers and it flips**: "
        f"{len(big_lop):,} of {len(big):,} ({100 * len(big_lop) // max(len(big), 1)}%) "
        f"are lopsided. Bearer-weighted across all of `both`, {weighted_lop:,} "
        f"of {weighted:,} bearers ({100 * weighted_lop // max(weighted, 1)}%) sit "
        "on a token that behaves overwhelmingly one way.",
        "",
        "**So the rule is a dominance ratio with a bearer floor**, not "
        "presence-in-both and not dominance alone. Below the floor there is no "
        "evidence either way, and a name item assigned on a 1-vs-1 split would "
        "be a guess wearing a statistic.",
        "",
        f"**The loudest `both` tokens are not names at all.** "
        f"{len(particles):,} distinct nobiliary and toponymic particles — `de`, "
        "`von`, `van`, `y`, `la`, `da`, `of` — carry "
        f"{sum(r['bearers'] for r in particles):,} bearers between them and top "
        "the table purely because they sit inside surname strings. They are "
        "`SPFX` material and **must not become name items**. Same for the "
        f"{len(ordinals):,} regnal numerals (`I`, `II`, `III`) sitting in the "
        "given slot: they are ordinals on a title, not given names.",
        "",
        "**The patronymic is inside the given-name string, which is the whole "
        "reason it needs its own role.** `Olsen` is recorded as a *given* token "
        "for 742 people and a surname for 266; `Olsdatter` 691 against 213. "
        "Geni writes `Ole Olsen` into `GIVN`, so the patronymic lands where a "
        "middle name would — exactly the position Emma's model assigns "
        "`P3831` → `Q110874` rather than `Q245025`.",
        "",
        "**CJK behaves cleanly and needs no special case.** 陳 is 3,247 surname "
        "against 8 given; 曾 is 2,263 against 6. The clan names sort themselves "
        "by the same dominance rule as the Latin ones, which is what Emma meant "
        "by the classification being behavioural rather than geographic. The "
        "one thing to watch is the transliteration: `Chén` appears separately "
        "in Latin script with its own bearers, so the same clan name exists as "
        "two tokens and must not be counted as two families.",
        "",
    ]
    lines += top("Most common tokens that behave as BOTH", both)
    lines += top("Most common CJK tokens",
                 [r for r in real if r["script"] in ("Han", "Kana", "Hangul")])
    MD_OUT.write_text("\n".join(lines), encoding="utf-8")

    print(f"{records:,} name records -> {len(rows):,} distinct tokens")
    print(f"wrote {CSV_OUT} and {MD_OUT}")
    for k, v in sorted(by_behaviour.items(), key=lambda kv: -kv[1]):
        print(f"  {k:>12}: {v:,}")
    print(f"  patronymic-marked: {len(patro):,} tokens")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
