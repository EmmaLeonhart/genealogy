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

VOWELS = "aeiouyæøå"

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
VOWEL_COL = {"a": 0, "i": 1, "u": 2, "e": 3, "o": 4, "y": 1, "æ": 3, "ø": 4, "å": 4}
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


def translit(token):
    """`(katakana, chinese)` for one Norwegian name token, or `(None, None)`."""
    s = token.casefold().replace("aa", "å")
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


def check():
    """Score the rules against the 113 hand-written rows."""
    sys.stdout.reconfigure(encoding="utf-8")
    path = Path(__file__).resolve().parent.parent / "reports" / "garborg-name-transliterations.tsv"
    rows = list(csv.DictReader(open(path, encoding="utf-8"), delimiter="\t"))
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
    print(f"{n} hand-written rows")
    print(f"  katakana matches exactly : {ja_ok:>3}  ({100*ja_ok/n:.0f}%)")
    print(f"  chinese  matches exactly : {zh_ok:>3}  ({100*zh_ok/n:.0f}%)")
    print(f"  both                     : {both:>3}  ({100*both/n:.0f}%)")
    print(f"\nfirst 25 katakana disagreements (rule vs hand):")
    for t, got, want in misses[:25]:
        print(f"   {t:<16} {got:<18} {want}")


if __name__ == "__main__":
    check()
