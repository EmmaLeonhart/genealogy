"""Fill the Japanese and Chinese transliteration table from rules instead of by hand.

    python scripts/extend-transliterations.py

**Emma, 2026-08-25, looking at a built batch:** *"Also no Chinese or Japanese names for them? I am
confused did you kinda bullshit these instead of selecting from an actual pipeline? It should no
be that hard. Why is this so inconsistent?"*

She is right on all three counts. `reports/garborg-name-transliterations.tsv` was **113 tokens
typed out by hand** for an earlier, smaller batch, and `label_in()` emits `ja`/`zh` only when
**every** token of a name is in it. So a name containing one unlisted token silently loses both
labels — **64 of 83 creations** in the batch she was looking at, missing **90 distinct tokens**,
most of them ordinary: `Anna`, `Lars`, `Maren`, `Rakel`, `Olsdatter`, `Gundersen`. That is not a
judgement about those people, it is a table that stopped where somebody's typing stopped.

## Two rules, in order

**1. Patronymics and farm-derived surnames COMPOSE.** `Olsdatter` is `Ols` + `datter`;
`Gundersen` is `Gunder` + `sen`. Where the stem is already known — from the hand table or from
rule 2 — the whole token is built from it, so the suffix is transliterated once and consistently
rather than 40 times by hand. Suffixes handled: `-datter`, `-dotter`, `-dtr.`, `-sen`, `-son`,
`-sson`, `-ssen`.

**2. Everything else goes through a Norwegian orthography reader.** Longest-match over a digraph
table — `kj`, `sj`, `skj`, `gj`, `hj`, `ei`, `øy`, `au`, `aa` — then single letters, into katakana.
The Chinese form uses the standard transcription characters for the same syllables.

**Rule 1 runs first and rule 2 is the fallback**, so a composed name inherits its stem's
transliteration rather than being re-read letter by letter and coming out different from the stem
it contains. That inconsistency is the bug she was pointing at.

## What it will not do

**The hand table always wins.** Every existing row is preserved untouched: those were checked by a
human and several encode real judgements — `Aabø` noting `Aa = å`, `Aadne` as a variant of `Ådne`.
Rules fill gaps; they never overwrite.

**Structural words are skipped, not transliterated.** `NN`, `of`, `son`, `daughter` appear in the
token census because the NN descriptive labels are built from a different template, which already
emits its own `ja` and `zh` (`…の息子`, `…之子`). Feeding them here would produce a katakana
rendering of the English word "son".

**A token it cannot read is left out and reported.** A missing row means no `ja`/`zh` for that
name, which is the current behaviour and is honest; a guessed row would put a wrong name on a
person in two languages at once.

Writes `reports/garborg-name-transliterations.tsv` in place, appending only.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
TABLE = ROOT / "reports" / "garborg-name-transliterations.tsv"

#: Not names. The NN descriptive labels carry their own `ja`/`zh` from a template.
SKIP = {"nn", "of", "son", "daughter", "the", "and", "n.n.", "private", "unknown"}

#: Norwegian orthography, longest match first. Katakana, then the standard Chinese
#: transcription character for the same syllable.
DIGRAPHS = [
    ("skj", "シ", "希"), ("kj", "ヒ", "希"), ("sj", "シ", "希"), ("gj", "ユ", "尤"),
    ("hj", "ユ", "尤"), ("ei", "エイ", "艾"), ("øy", "オイ", "奥伊"), ("au", "アウ", "奥"),
    ("aa", "オー", "奥"), ("th", "ト", "特"), ("ch", "ク", "克"), ("ng", "ング", "恩格"),
    ("nd", "ンド", "恩德"), ("rs", "ルシュ", "尔斯"), ("ll", "ッル", "尔"),
]
LETTERS = {
    "a": ("ア", "阿"), "b": ("ブ", "布"), "c": ("ク", "克"), "d": ("ド", "德"),
    "e": ("エ", "埃"), "f": ("フ", "夫"), "g": ("グ", "格"), "h": ("ハ", "哈"),
    "i": ("イ", "伊"), "j": ("ヤ", "雅"), "k": ("ク", "克"), "l": ("ル", "尔"),
    "m": ("ム", "姆"), "n": ("ン", "恩"), "o": ("オ", "奥"), "p": ("プ", "普"),
    "q": ("ク", "克"), "r": ("ル", "尔"), "s": ("ス", "斯"), "t": ("ト", "特"),
    "u": ("ウ", "乌"), "v": ("ヴ", "夫"), "w": ("ヴ", "夫"), "x": ("クス", "克斯"),
    "y": ("イ", "伊"), "z": ("ズ", "兹"), "æ": ("エ", "埃"), "ø": ("オ", "奥"),
    "å": ("オー", "奥"), "ä": ("エ", "埃"), "ö": ("オ", "奥"), "ü": ("ウ", "乌"),
}

SUFFIXES = [
    ("datter", "ダッテル", "达特"), ("dotter", "ドッテル", "多特"),
    ("dtr.", "ダッテル", "达特"), ("dtr", "ダッテル", "达特"),
    ("sson", "ソン", "松"), ("ssen", "セン", "森"),
    ("sen", "セン", "森"), ("son", "ソン", "松"),
]


def by_rule(token):
    """Read a token through the orthography table. Returns `(ja, zh)`."""
    low = token.casefold()
    ja, zh, i = [], [], 0
    while i < len(low):
        for d, j, z in DIGRAPHS:
            if low.startswith(d, i):
                ja.append(j)
                zh.append(z)
                i += len(d)
                break
        else:
            ch = low[i]
            if ch in LETTERS:
                j, z = LETTERS[ch]
                ja.append(j)
                zh.append(z)
            elif ch in "-'’.":
                pass
            else:
                return None, None      # unreadable: leave it out, do not guess
            i += 1
    return "".join(ja), "".join(zh)


def main():
    rows = list(csv.DictReader(open(TABLE, encoding="utf-8"), delimiter="\t"))
    have = {r["token"]: r for r in rows}
    print(f"{len(have)} tokens in the hand table - preserved untouched")

    # Every token any Garborg-batch label needs.
    need = set()
    for path in (ROOT / "reports" / "wikidata-garborg-day.qs",
                 ROOT / "reports" / "garborg-carry-forward.tsv"):
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for m in re.finditer(r'\tL(?:en|mul)\t"([^"]+)"', text):
            need |= set(m.group(1).split())
        for m in re.finditer(r"^\d+\t([^\t]+)\t", text, re.M):
            need |= set(m.group(1).split())
    need = {t for t in need if t.casefold() not in SKIP and not t.isdigit()}
    missing = sorted(t for t in need if t not in have)
    print(f"{len(need)} tokens needed, {len(missing)} missing")

    added, composed, unreadable = [], 0, []
    for token in missing:
        ja = zh = None
        # Rule 1: compose off a known stem so the part matches the whole.
        for suf, sja, szh in SUFFIXES:
            if token.casefold().endswith(suf) and len(token) > len(suf) + 1:
                stem = token[: len(token) - len(suf)]
                src = have.get(stem) or have.get(stem.capitalize())
                if src:
                    ja, zh = src["ja"] + sja, src["zh"] + szh
                    note = f"composed: {stem} + -{suf}"
                else:
                    sja_, szh_ = by_rule(stem)
                    if sja_:
                        ja, zh = sja_ + sja, szh_ + szh
                        note = f"composed by rule: {stem} + -{suf}"
                break
        if ja is None:
            ja, zh = by_rule(token)
            note = "by rule"
        if ja is None:
            unreadable.append(token)
            continue
        if note.startswith("composed"):
            composed += 1
        added.append({"token": token, "ja": ja, "zh": zh, "note": note})

    rows.extend(added)
    rows.sort(key=lambda r: r["token"].casefold())
    with open(TABLE, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["token", "ja", "zh", "note"], delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    print(f"\n{len(added)} added ({composed} composed off a stem), "
          f"{len(unreadable)} left out as unreadable")
    print(f"table is now {len(rows)} tokens -> {TABLE.relative_to(ROOT)}")
    if unreadable:
        print(f"  unreadable: {unreadable[:12]}")
    print("\nsample of what was added:")
    for r in added[:12]:
        print(f"   {r['token']:<18} {r['ja']:<16} {r['zh']:<12} {r['note']}")


if __name__ == "__main__":
    main()
