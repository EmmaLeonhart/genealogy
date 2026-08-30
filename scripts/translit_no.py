"""Norwegian name -> katakana and Chinese, syllable by syllable.

**Emma, 2026-08-25:** *"did you kinda bullshit these instead of selecting from an actual
pipeline? It should no be that hard. Why is this so inconsistent?"*

The first attempt at a rule engine mapped **one letter at a time** and produced `Anna` →
`アンンア`. Katakana is syllabic: `Anna` is `アンナ`, three kana for four letters, because `nn`
is a geminate coda plus a `na` syllable. Letter-by-letter is not a transliteration, it is a
spelling-out, and shipping it would have put a wrong name on 64 people in two languages.

**The 113 hand-written rows are the test set**, and `--check` scores this module against them.
They were typed by a human against real usage — `Arne` → `アルネ` *"as zh.wikipedia writes Arne
Garborg"*, `Garborg` → `ガルボルグ` *"the farm in Time, Rogaland"* — so agreeing with them is the
only evidence available that the rules are right. An engine that cannot reproduce a table someone
checked has no business extending it.

## The rules, read off those 113

* **Syllables are onset + nucleus.** A consonant cluster before a vowel is split so each consonant
  gets its own kana, the last one carrying the vowel: `Stine` → `ス` + `ティ` + `ネ`.
* **`r` before a consonant is `ル`, always.** `Olsen` → `オルセン`, `Garborg` → `ガルボルグ`,
  `Arne` → `アルネ`. This is the single most frequent rule in the table.
* **Final `n` is `ン`**, never `ヌ`.
* **A consonant with no vowel takes `u`**, except `t`/`d` which take `o`: `Garborg` ends `ルグ`.
* **`å` and `aa` are `オー`**; `ø` is `オ` in an onset and `エ` finally; `æ` is `エ`.
* **`ei` is `エイ`, `au` is `アウ`, `øy` is `オイ`.**
* **`j` before a vowel is a glide** — `Jon` → `ヨン`, not `ジョン`.

Chinese uses the standard transcription characters for the same syllables, which is what the hand
rows do: `オルセン` ↔ `奥尔森`, `ガルボルグ` ↔ `加尔博格`.

**What it refuses:** a token containing a character it has no rule for returns `(None, None)`.
A missing row means no `ja`/`zh` for that name, which is the current behaviour and is honest.
A guessed row is a wrong name in two languages at once.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

#: **Swedish `ö` and `ä` read as Norwegian `ø` and `æ`.** This engine is a Norwegian
#: orthography reader and had no rule for them, so every Swedish name containing one returned
#: `(None, None)` and lost its `ja`/`zh` label entirely -- `Mörner`, `Köhler`, `Törnflycht`,
#: `Gennäs`, `Leckö`, `Tärnö`. The readings are not invented here: the table this file replaced
#: already carried `ö -> オ/奥` and `ä -> エ/埃`, the same values as `ø` and `æ`, which is also
#: what the phonology gives. `ü` follows `y`, and `é` follows `e`.
VOWELS = "aeiouyæøåöäüé"

#: onset -> (kana row a,i,u,e,o) and the Chinese character for each.
ROWS = {
    "":   (("ア", "イ", "ウ", "エ", "オ"), ("阿", "伊", "乌", "埃", "奥")),
    "k":  (("カ", "キ", "ク", "ケ", "コ"), ("卡", "基", "库", "凯", "科")),
    "g":  (("ガ", "ギ", "グ", "ゲ", "ゴ"), ("加", "吉", "古", "盖", "戈")),
    "s":  (("サ", "シ", "ス", "セ", "ソ"), ("萨", "西", "苏", "塞", "索")),
    "z":  (("ザ", "ジ", "ズ", "ゼ", "ゾ"), ("扎", "吉", "祖", "泽", "佐")),
    "t":  (("タ", "ティ", "ト", "テ", "ト"), ("塔", "蒂", "图", "特", "托")),
    "d":  (("ダ", "ディ", "ド", "デ", "ド"), ("达", "迪", "杜", "德", "多")),
    "n":  (("ナ", "ニ", "ヌ", "ネ", "ノ"), ("纳", "尼", "努", "内", "诺")),
    "h":  (("ハ", "ヒ", "フ", "ヘ", "ホ"), ("哈", "希", "胡", "赫", "霍")),
    "b":  (("バ", "ビ", "ブ", "ベ", "ボ"), ("巴", "比", "布", "贝", "博")),
    "p":  (("パ", "ピ", "プ", "ペ", "ポ"), ("帕", "皮", "普", "佩", "波")),
    "m":  (("マ", "ミ", "ム", "メ", "モ"), ("马", "米", "穆", "梅", "莫")),
    "r":  (("ラ", "リ", "ル", "レ", "ロ"), ("拉", "里", "鲁", "雷", "罗")),
    "l":  (("ラ", "リ", "ル", "レ", "ロ"), ("拉", "利", "卢", "莱", "洛")),
    "v":  (("ヴァ", "ヴィ", "ヴ", "ヴェ", "ヴォ"), ("瓦", "维", "武", "韦", "沃")),
    "w":  (("ヴァ", "ヴィ", "ヴ", "ヴェ", "ヴォ"), ("瓦", "维", "武", "韦", "沃")),
    "f":  (("ファ", "フィ", "フ", "フェ", "フォ"), ("法", "菲", "富", "费", "福")),
    "j":  (("ヤ", "イ", "ユ", "イェ", "ヨ"), ("雅", "伊", "尤", "耶", "永")),
    "y":  (("ヤ", "イ", "ユ", "イェ", "ヨ"), ("雅", "伊", "尤", "耶", "永")),
    "c":  (("カ", "シ", "ク", "セ", "コ"), ("卡", "西", "库", "塞", "科")),
    "kj": (("ヒャ", "ヒ", "ヒュ", "ヒェ", "ヒョ"), ("希", "希", "休", "谢", "肖")),
    "sj": (("シャ", "シ", "シュ", "シェ", "ショ"), ("沙", "西", "舒", "谢", "肖")),
    "skj": (("シャ", "シ", "シュ", "シェ", "ショ"), ("沙", "西", "舒", "谢", "肖")),
    "sk": (("スカ", "スキ", "スク", "スケ", "スコ"), ("斯卡", "斯基", "斯库", "斯凯", "斯科")),
    "gj": (("ヤ", "イ", "ユ", "イェ", "ヨ"), ("雅", "伊", "尤", "耶", "永")),
    "hj": (("ヤ", "イ", "ユ", "イェ", "ヨ"), ("雅", "伊", "尤", "耶", "永")),
    "th": (("タ", "ティ", "ト", "テ", "ト"), ("塔", "蒂", "图", "特", "托")),
    "ch": (("カ", "キ", "ク", "ケ", "コ"), ("卡", "基", "库", "凯", "科")),
    "sch": (("シャ", "シ", "シュ", "シェ", "ショ"), ("沙", "西", "舒", "谢", "肖")),
}

#: vowel -> column, plus the ones that carry their own length.
VOWEL_COL = {"a": 0, "i": 1, "u": 2, "e": 3, "o": 4, "y": 1, "æ": 3, "ø": 4, "å": 4,
             "ö": 4, "ä": 3, "ü": 1, "é": 3}
LONG = {"å": ("ー", ""), "aa": ("ー", "")}

#: a consonant with no vowel after it
CODA = {
    "n": ("ン", "恩"), "r": ("ル", "尔"), "l": ("ル", "尔"), "s": ("ス", "斯"),
    "k": ("ク", "克"), "g": ("グ", "格"), "t": ("ト", "特"), "d": ("ド", "德"),
    "m": ("ム", "姆"), "b": ("ブ", "布"), "p": ("プ", "普"), "v": ("ヴ", "夫"),
    "f": ("フ", "夫"), "h": ("", ""), "z": ("ズ", "兹"), "c": ("ク", "克"),
    "j": ("イ", "伊"), "w": ("ヴ", "夫"), "y": ("イ", "伊"), "x": ("クス", "克斯"),
}

DIPHTHONGS = {"ei": ("エイ", "艾"), "ai": ("アイ", "艾"), "au": ("アウ", "奥"),
              "øy": ("オイ", "奥伊"), "oy": ("オイ", "奥伊"), "eu": ("エウ", "厄")}


def _onsets():
    return sorted((o for o in ROWS if o), key=len, reverse=True)


ONSETS = _onsets()


#: **Accented VOWELS fold to their base vowel. Accented CONSONANTS do not.**
#:
#: Measured over `reports/derived-labels.csv`: these carry ~51,700 occurrences in `mul` labels --
#: `á` 14,206, `í` 14,138, `ó` 10,885, `ã` 4,852, `è` 3,029, `ú` 2,458, `â` 1,195, `ë` 952 -- and
#: every name containing one returned `(None, None)`, losing its `ja`/`zh` label entirely.
#:
#: The acute, grave, circumflex and diaeresis on a vowel mark stress or length in these languages,
#: and **katakana cannot represent the distinction in any case**: `ó` and `o` are both オ. So the
#: fold loses nothing that could have been written down.
#:
#: **`ñ` (6,874), `ç` (4,898), `ł` (2,213), `ć` (2,050), `š` (1,385) and `č` (1,012) are
#: deliberately NOT folded.** Those diacritics change the consonant -- `ñ` is *ny*, `ł` is *w*,
#: `š` is *sh* -- so mapping them to the bare letter would invent a reading rather than simplify
#: one. Those names keep returning `(None, None)` and get no `ja`/`zh`, which is the
#: *partial is worse than absent* rule doing its job.
BARE_VOWEL = str.maketrans({
    "á": "a", "à": "a", "â": "a", "ã": "a",
    "é": "e", "è": "e", "ê": "e", "ë": "e",
    "í": "i", "ì": "i", "î": "i", "ï": "i",
    "ó": "o", "ò": "o", "ô": "o", "õ": "o",
    "ú": "u", "ù": "u", "û": "u",
    "ý": "y", "ÿ": "y",
})


#: **Patronymic and married-name suffixes, with their conventional readings.** Longest first,
#: so `sson` is not read as `son` and `datter` not as `dtr`.
#:
#: **This lives here because it is a READING RULE, and it lived in two places until
#: 2026-08-30.** `extend-transliterations.py` composed `Arnesen` as *stem + `-sen`* and got
#: `アルネセン` / `阿尔内森`; this engine walked the same token letter by letter and got
#: `阿尔内塞恩`, spelling the coda `n` out as `恩`. Both paths are in one pipeline and they
#: disagreed on 99 of the table's rows.
#:
#: Applying it here moved the engine's agreement with rows it did not write from
#: **ja 38.8% -> 46.1% and zh 11.7% -> 41.3%**, measured over those 317 rows. The Chinese
#: figure more than tripled, because `-sen`/`-son` are the commonest endings in this corpus and
#: `森`/`松` are the standard characters for them.
SUFFIXES = [
    ("datter", "ダッテル", "达特"), ("dotter", "ドッテル", "多特"),
    ("dtr.", "ダッテル", "达特"), ("dtr", "ダッテル", "达特"),
    ("sson", "ソン", "松"), ("ssen", "セン", "森"),
    ("sen", "セン", "森"), ("son", "ソン", "松"),
]


def translit(token):
    """`(katakana, chinese)` for one Norwegian name token, or `(None, None)`."""
    # **A patronymic suffix is read as a unit, not spelled out.** See `SUFFIXES` above: the
    # composer already did this and the letter walk did not, so one pipeline gave two answers.
    #
    # **The stem CAN itself end in a suffix, and one row in the table does.** `Samsonson`
    # splits to `Samson` + `-son` and then `Sam` + `-son`, giving `萨姆松松` where the letter
    # walk gave `萨姆索恩松`. That is a patronymic built on a patronymic and reading it twice
    # is defensible, but it is a consequence rather than a design, so it is written down here
    # rather than guarded against. Recursion terminates because each step removes at least
    # three characters.
    low = (token or "").casefold()
    for suf, sja, szh in SUFFIXES:
        if low.endswith(suf) and len(token) > len(suf) + 1:
            stem_ja, stem_zh = translit(token[: len(token) - len(suf)])
            if stem_ja is None:
                return None, None
            return stem_ja + sja, stem_zh + szh

    # **`ck` is ONE sound spelled with two letters.** The geminate rule below handles
    # *identical* adjacent letters (`nn` in `Anna`); it cannot see a digraph of *different*
    # letters spelling one phoneme, so `Mørck` walked m-ø, r, c, k and produced `モルクク`.
    # Emma hand-corrected that item to `モルク` on 2026-08-29. Normalising here, the same way
    # `aa` normalises to `å`, fixes the coda (`Falck`, `Munck`) and the onset (`Sacken`
    # `サクケン` -> `サケン`) in one place. 47 tokens were affected.
    s = (token.casefold().translate(BARE_VOWEL).replace("aa", "å")
         .replace("ck", "k"))
    if not s or any(c not in VOWELS + "bcdfghjklmnpqrstvwxz-'’." for c in s):
        return None, None
    ja, zh, i = [], [], 0
    while i < len(s):
        if s[i] in "-'’.":
            i += 1
            continue
        # diphthong standing alone (no onset consumed yet this step)
        for d, (dj, dz) in DIPHTHONGS.items():
            if s.startswith(d, i):
                ja.append(dj)
                zh.append(dz)
                i += len(d)
                break
        else:
            onset = ""
            for o in ONSETS:
                if s.startswith(o, i) and i + len(o) < len(s) and s[i + len(o)] in VOWELS:
                    onset = o
                    break
            if onset:
                i += len(onset)
            elif s[i] not in VOWELS:
                c = s[i]
                if c in CODA:
                    # geminate: `nn` in Anna is one coda, then the `na` syllable
                    if i + 1 < len(s) and s[i + 1] == c:
                        i += 1
                        continue
                    kj, kz = CODA[c]
                    ja.append(kj)
                    zh.append(kz)
                    i += 1
                    continue
                return None, None
            if i >= len(s):
                break
            v = s[i]
            if v not in VOWEL_COL:
                return None, None
            col = VOWEL_COL[v]
            kana, hans = ROWS.get(onset, ROWS[""])
            ja.append(kana[col])
            zh.append(hans[col])
            if v == "å":
                ja.append("ー")
            i += 1
    return "".join(ja), "".join(zh)


def _wrote_by_engine(row):
    """Did this engine write the row? Then scoring against it is scoring against itself."""
    note = (row.get("note") or "").strip()
    return note == "by rule" or note.startswith("composed by rule:")


def check():
    """Score the rules against the rows this engine did NOT write.

    **The docstring said "the 113 hand-written rows" and the loop scored all 4,017.** By
    2026-08-30, 3,700 of those were this engine's own output, so the headline read
    *86% katakana, 75% chinese* — the engine agreeing with itself. Against the 317 rows a
    person wrote, or that were composed off a hand stem, it is **38.8% and 11.7%**.

    That is the failure `queue.md` § *A join that matches NOTHING must fail loudly* is written
    against: a plausible number measured over the wrong population, indistinguishable from a
    good result. Both are printed now, and the honest one leads.
    """
    sys.stdout.reconfigure(encoding="utf-8")
    path = Path(__file__).resolve().parent.parent / "reports" / "garborg-name-transliterations.tsv"
    every = list(csv.DictReader(open(path, encoding="utf-8"), delimiter="\t"))
    rows = [r for r in every if not _wrote_by_engine(r)]
    print(f"{len(every):,} rows in the table; {len(every) - len(rows):,} were written by this "
          f"engine and are not evidence about it. Scoring against the other {len(rows):,}:\n")
    ja_ok = zh_ok = both = n = 0
    misses = []
    for r in rows:
        gj, gz = translit(r["token"])
        if gj is None:
            misses.append((r["token"], "-", r["ja"]))
            n += 1
            continue
        n += 1
        ja_ok += gj == r["ja"]
        zh_ok += gz == r["zh"]
        both += gj == r["ja"] and gz == r["zh"]
        if gj != r["ja"]:
            misses.append((r["token"], gj, r["ja"]))
    print(f"{n} rows this engine did not write")
    print(f"  katakana matches exactly : {ja_ok:>3}  ({100*ja_ok/n:.0f}%)")
    print(f"  chinese  matches exactly : {zh_ok:>3}  ({100*zh_ok/n:.0f}%)")
    print(f"  both                     : {both:>3}  ({100*both/n:.0f}%)")
    print(f"\nfirst 25 katakana disagreements (rule vs hand):")
    for t, got, want in misses[:25]:
        print(f"   {t:<16} {got:<18} {want}")


if __name__ == "__main__":
    check()
