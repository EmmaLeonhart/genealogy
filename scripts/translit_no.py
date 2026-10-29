"""Norwegian name -> katakana and Chinese, syllable by syllable.

**These readings come from a real pipeline, not from improvisation, and they have to be
consistent.**

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

import re
import unicodedata
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
    # `jo` is 约, not 永. 永 is the *yong* syllable, and using it for `jo` gave `Johan` 永汉
    # against the standard 约翰, `Johanne` 永哈内, `Jon` 永. Measured over the 318 rows this
    # engine did not write: zh 148 -> 152.
    #
    # **The same change to the nasal final was tried and REFUTED**: `jon` 永 -> 约恩 took zh
    # 152 -> 145, so `NASAL_FINAL["j"]` keeps 永 in the `on` column. Recorded because the
    # reasoning that produced the good change predicts the bad one just as confidently.
    "j":  (("ヤ", "イ", "ユ", "イェ", "ヨ"), ("雅", "伊", "尤", "耶", "约")),
    "y":  (("ヤ", "イ", "ユ", "イェ", "ヨ"), ("雅", "伊", "尤", "耶", "约")),
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

#: **A syllable-final nasal is part of the syllable in Chinese. It is not its own character.**
#:
#: `塞恩` for `sen` is wrong: a coda `-n` was being made its own character instead of merged,
#: which Chinese does not do. That is exactly what `CODA` did: onset+vowel gave one character and the `n` gave another, so `sen`
#: came out 塞 + 恩 instead of **森**. Measured before the fix: **1,701 rows of
#: `garborg-name-transliterations.tsv` carry a vowel + nasal coda and 1,201 carry a standalone
#: 恩** — `Absalon` 阿布萨洛恩, `Aanenson` 奥内恩松.
#:
#: `{onset: (an, en, in, on, un)}`, matching `ROWS`' column order for a/i/u/e/o reordered to
#: the finals' own order. These are the standard transcription characters, and the whole table
#: is **validated against the rows this engine did not write and against real `zh` labels in
#: `out/wikidata/labels.tsv`** rather than trusted — `python scripts/translit_no.py` prints the
#: score, and it is the only reason to believe any cell of it.
#:
#: **`-ng` is read as the same final as `-n`.** Norwegian and Swedish names in this corpus end
#: `-ing`, `-ung`, `-ong` where the transcription tables give the same character as the plain
#: nasal often enough that a separate table would be inventing a distinction to no measured
#: gain. Declared here rather than hidden: if a later measurement separates them, this is the
#: line to change.
NASAL_FINAL = {
    "":  ("安", "恩", "因", "翁", "温"),
    "b": ("班", "本", "宾", "邦", "本"),
    "p": ("潘", "彭", "平", "蓬", "蓬"),
    "m": ("曼", "门", "明", "蒙", "蒙"),
    "f": ("凡", "芬", "芬", "丰", "丰"),
    "v": ("万", "文", "文", "翁", "文"),
    "w": ("万", "文", "文", "翁", "文"),
    "d": ("丹", "登", "丁", "东", "敦"),
    "t": ("坦", "滕", "廷", "通", "通"),
    "n": ("南", "嫩", "宁", "农", "农"),
    "l": ("兰", "伦", "林", "隆", "伦"),
    "r": ("兰", "伦", "林", "龙", "伦"),
    "g": ("甘", "根", "金", "贡", "贡"),
    "k": ("坎", "肯", "金", "孔", "昆"),
    "h": ("汉", "亨", "欣", "洪", "洪"),
    "s": ("桑", "森", "辛", "松", "孙"),
    "z": ("赞", "曾", "津", "宗", "尊"),
    "j": ("扬", "延", "因", "永", "云"),
    "y": ("扬", "延", "因", "永", "云"),
    "c": ("坎", "森", "辛", "孔", "昆"),
    "sk": ("斯坎", "斯肯", "斯金", "斯孔", "斯昆"),
    "th": ("坦", "滕", "廷", "通", "通"),
    "ch": ("坎", "肯", "金", "孔", "昆"),
    "kj": ("希安", "希恩", "希因", "希翁", "希温"),
    "sj": ("尚", "申", "辛", "雄", "顺"),
    "skj": ("尚", "申", "辛", "雄", "顺"),
    "gj": ("扬", "延", "因", "永", "云"),
    "hj": ("扬", "延", "因", "永", "云"),
    "sch": ("尚", "申", "辛", "雄", "顺"),
}

#: vowel -> its column in `NASAL_FINAL`. Norwegian `æ`/`ä` follow `e`, `ø`/`ö`/`å` follow `o`,
#: `y`/`ü` follow `i` — the same folding `VOWEL_COL` already does, in the finals' order.
NASAL_COL = {"a": 0, "e": 1, "i": 2, "o": 3, "u": 4, "y": 2, "æ": 1, "ø": 3, "å": 3,
             "ö": 3, "ä": 1, "ü": 2, "é": 1}


#: **Cj is ONE palatalised onset, and only `sj kj gj hj skj` were listed.** So `Bjørn` found no
#: onset, fell through to the coda branch, and came out `ブヨルン` -- while the *attested*
#: Wikidata value for the same token is `ビョルン` (ja 5x). The rule disagreed with the corpus
#: on a name this tree is full of.
#:
#: Built from each base row's `i` column, which is what palatalisation does in katakana:
#: `b` -> `ビ` gives `ビャ ビ ビュ ビェ ビョ`. `dj` and `lj` are Norwegian /j/ -- the consonant is
#: silent, exactly as `gj` and `hj` already are -- so they take the ya-row.
#:
#: **`tj` and `vj` are deliberately absent.** Norwegian `tj` is /ç/ and Japanese writes it as
#: both `チ` (Tjøme) and `ヒ`/`シ`; nothing here settles which, so it keeps the old reading
#: rather than gaining a guessed one. `CLAUDE.md` § *Do not guess these*.
_PALATAL = {}
for _c in ("b", "f", "m", "n", "p", "r"):
    _i = ROWS[_c][0][1]
    _PALATAL[_c + "j"] = ((_i + "ャ", _i, _i + "ュ", _i + "ェ", _i + "ョ"),
                          ROWS[_c][1])
# **`dj` and `lj` are OUT for the same reason as `tj`.** Norwegian `dj` is /j/ -- the `d` is
# silent, as in `Djupvik` -- but the corpus also holds Indonesian names where `dj` is /dʒ/, the
# old spelling of `j`. The refresh made `AMIDJAJA` read `アミヤヤ`, dropping a consonant from a
# name that is not Norwegian at all. One rule cannot serve both and nothing here says which a
# given token is, so neither is added.
ROWS.update(_PALATAL)


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
    # **NFC first, or a decomposed diacritic reads as nothing.** `Ånon` written as `A` +
    # U+030A is five characters, not four; the walk does not know a bare combining mark and
    # returns no reading at all. Measured 2026-09-01: **3,378 tokens** in
    # `reports/derived-labels.csv` are not NFC -- `Adnoy`, `Hedstrom`, `Engstrom`,
    # `Sparrskold`, `Austratt` -- and every one silently got no `ja`/`zh`.
    token = unicodedata.normalize("NFC", token)

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
    # That item was hand-corrected to `モルク` on 2026-08-29. Normalising here, the same way
    # `aa` normalises to `å`, fixes the coda (`Falck`, `Munck`) and the onset (`Sacken`
    # `サクケン` -> `サケン`) in one place. 47 tokens were affected.
    s = (token.casefold().translate(BARE_VOWEL).replace("aa", "å")
         .replace("ck", "k"))
    # **A doubled nasal with no vowel after it is one mora nasal.** `Finn` came out `フィンン`
    # and `Gunnbjørn` `グンンブヨルン`: the nasal-final block consumed one `n` and the geminate
    # branch below then emitted the other. Collapsing here, the same way `ck` collapses above,
    # leaves the geminate branch to handle only the case it was written for -- `nn` BEFORE a
    # vowel, which is `Anna` -> `アンナ`.
    #
    # **`n` ONLY, and `m` is deliberately NOT here.** You, 2026-09-09: *"mu is the cluster
    # resolver lol not a geminate marker"*, with `Mommsen` -> `モンムセン`. For `n` the mora
    # nasal and the coda are the SAME character, so collapsing is right and `Finn` -> `フィン`.
    # For `m` they are two DIFFERENT characters -- `ン` marks the geminate and `ム` resolves
    # the `mms` cluster -- so both belong, and collapsing here destroyed one of them.
    s = re.sub(r"(?P<c>n)(?P=c)(?![aeiouyæøåöäü])", lambda m: m.group("c"), s)
    # **`dt` is ONE /t/**, in German, Danish, Norwegian and Swedish alike -- and the corpus
    # settles it rather than anyone's opinion: of the 24 `-dt` tokens carrying an ATTESTED
    # Wikidata rendering, **0 end in `ドト`** (`Schmidt` シュミット ja 33x, `Brandt` ブラント 14x,
    # `Arndt` アルント, `Mundt` ムント), while **201 of 201** rule-made ones did. Chinese agrees
    # independently: of the 4 with a real `zh` attestation, 0 contain 德特.
    # Same shape as `ck` above -- two letters, one phoneme, normalised before the walk.
    s = s.replace("dt", "t")
    # ⛔ **A SILENT WORD-FINAL `e` WAS TRIED AND REFUTED, 2026-09-09. Do not add it.**
    #
    # `Anne` renders `アンネ` where Wikidata attests `アン` 233x, and it is a whole class: 10
    # attested tokens where the rule adds a tail the attestation drops — `Christie` クリスティエ
    # against クリスティ 10x, `Lynne` リンネ against リン 5x, `Amelie`, `Petrie`, `Holcombe`.
    #
    # Dropping a word-final `e` after a consonant scores **733 against the current 734** — worse
    # than doing nothing. 55 gained, 56 lost, and the two lists are a language boundary:
    #
    #     gained   Adele, Adeline, Anne, Babette, Belle, Berthe, Cecile, Clotilde   French/English
    #     lost     Abbe, Andre, Arne, Atte, Bagge, Bakke, Beate, Birgitte, Bosse    Norwegian et al
    #
    # **Norwegian, Swedish and Danish PRONOUNCE that `e`**, and they are the corpus majority. This
    # is the `dj`/`lj` refutation again — right for `Djupvik`, wrong for Indonesian `AMIDJAJA` —
    # and its lesson is the same: nothing in the token says which language it belongs to.
    #
    # The 55 are already right in the emitted output, because the attested column beats the rule
    # per token. So the class needs no rule; it needs attestations, which it has.
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
                        # **A geminate is THREE different things and the branch emitted
                        # nothing at all**, so `Anna` came out `アナ` and `Gunnar` `グナル` --
                        # a mora short, and a different name. Emitting the plain coda for all
                        # of them is wrong the other way: it gave `Abba` -> `アブバ` where the
                        # attested value is `アッバ`. Measured against the 5,902 attested `ja`
                        # values, undifferentiated emission scored WORSE than emitting nothing
                        # (803 against 809), which is what caught it.
                        #
                        #   nasal      `nn` `mm`  -> `ン`   Anna -> アンナ, Emma -> エンマ
                        #   liquid     `ll` `rr`  -> nothing  Aall -> オール
                        #   otherwise             -> `ッ`   Abba  -> アッバ
                        # ⛔ **`ム` IS THE CLUSTER RESOLVER, NOT A GEMINATE MARKER.** You,
                        # 2026-09-09: *"mu is the cluster resolver lol not a geminate marker.
                        # Mommsen should be もんむせん and Hammerstein はんめルすタイン"*, and
                        # *"Emma would not be Emuma it would be Enma or Ema."*
                        #
                        # `CODA["m"]` is `ム`, which is right when an `m` has no vowel after it
                        # and has to be resolved into its own mora -- `Momm|sen` -> `モンムセン`,
                        # where the `ム` is resolving `mms` and the `ン` is the geminate. Reaching
                        # for `CODA[c]` HERE emitted the resolver in the geminate's place, so
                        # `Emma` came out `エムマ` -- a form that is neither of the two readings
                        # you named.
                        #
                        # A nasal geminate is `ン` for BOTH letters. It is the same mora nasal
                        # `nn` already took, and `mm` was only ever different by accident of
                        # indexing into a table that answers a different question.
                        if c in "nm":
                            ja.append("ン")
                        elif c not in "lr":
                            ja.append("ッ")
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
            if v == "å":
                ja.append("ー")
            i += 1

            # **The nasal belongs INSIDE the Chinese syllable.** See `NASAL_FINAL`. A nasal
            # here is a coda only if no vowel follows it -- `Anna` is `an` + `na`, not a
            # nasal final, and `Anders` is. `ng` is consumed with the `n`; katakana takes
            # `ン` (and `ング`) as it always did, because a mora nasal is correct there and
            # only the Chinese side was wrong.
            nasal = _nasal_coda_len(s, i)
            if nasal and onset in NASAL_FINAL and v in NASAL_COL:
                zh.append(NASAL_FINAL[onset][NASAL_COL[v]])
                for ch in s[i:i + nasal]:
                    ja.append(CODA[ch][0])
                i += nasal
            else:
                zh.append(hans[col])
    return "".join(ja), "".join(zh)


def _nasal_coda_len(s, i):
    """How many characters of a syllable-final nasal start at `i`: 0, 1 (`n`) or 2 (`ng`).

    A nasal is *final* only when no vowel follows it. `Anna` -> `an` + `na` has a vowel after
    the second `n`, so the first is a geminate and not a final; `Anders` has a consonant after
    it and is. A doubled `nn` is one nasal, matching the geminate rule below the coda branch.
    """
    if i >= len(s) or s[i] != "n":
        return 0
    end = i + 1
    if end < len(s) and s[end] == "n":       # `nn` is one nasal, not two
        end += 1
    if end < len(s) and s[end] == "g" and (end + 1 >= len(s) or s[end + 1] not in VOWELS):
        end += 1
    if end < len(s) and s[end] in VOWELS:
        return 0
    return end - i


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


def table_sort_key(row):
    """Total ordering for a row of `reports/garborg-name-transliterations.tsv`.

    **Sorting has to be deterministic**, ruled 2026-09-01.

    `sorted(key=str.casefold)` is NOT total on this table: **738 tokens collide under
    casefold** -- `A`/`a`, `Aarne`/`AARNE`, `'Le'`/`'le'`. Python's sort is stable, so a tie
    keeps the order it arrived in, which is whatever the previous writer left. Three scripts
    write this file and two of them do not sort at all, so every hand-off reshuffled the ties
    and a content-identical rewrite came out as **36,901 changed lines** in `git diff`.

    Appending the raw token breaks every tie, because the token is unique per row.
    """
    token = row["token"] if isinstance(row, dict) else row
    return (token.casefold(), token)
