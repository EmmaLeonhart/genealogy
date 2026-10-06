"""A Hepburn reading of a Japanese name -> Russian (Polivanov) and Korean (National Institute of Korean Language).

`to_ru("Nakayama Atsuchika")` -> "Накаяма Ацутика"; `to_ko(...)` -> "나카야마 아쓰치카". Long vowels are not
marked in either (Tōkyō -> Токио, 도쿄). The particle `no` joins the word before it (Фудзивара-но, 후지와라노).
A word that does not parse as Hepburn gives None for the whole name, so a caller writes nothing.
"""
import re
import unicodedata

VOWELS = "aiueo"
CONS = ["ky", "gy", "ny", "hy", "by", "py", "my", "ry", "sh", "ch", "ts", "j", "k", "g", "s", "z", "t", "d",
        "n", "h", "f", "b", "p", "m", "y", "r", "w"]


def _syllables(word):
    """Hepburn word -> kana-like syllables: 'ka', 'shi', 'kyo', 'N' (ん), 'Q' (っ). None if it does not parse."""
    w = unicodedata.normalize("NFD", word.lower().replace("'", "|"))
    w = "".join(c for c in w if unicodedata.category(c) != "Mn")  # ō -> o: long vowels are not marked
    out, i = [], 0
    while i < len(w):
        c = w[i]
        if c == "|":
            i += 1; continue
        if c in VOWELS:
            out.append(c); i += 1; continue
        if c == "n" and (i + 1 == len(w) or w[i + 1] not in VOWELS + "y"):
            out.append("N"); i += 1; continue
        if c == "m" and i + 1 < len(w) and w[i + 1] in "bpm":  # Hepburn variant: Kamba, Homma
            out.append("N"); i += 1; continue
        if i + 1 < len(w) and (w[i + 1] == c or (c == "t" and w[i + 1:i + 3] == "ch")) and c not in VOWELS + "n":
            out.append("Q"); i += 1; continue
        for cons in CONS:
            if w.startswith(cons, i) and i + len(cons) < len(w) and w[i + len(cons)] in VOWELS:
                v = w[i + len(cons)]
                syl = cons + v
                if syl in VALID:
                    out.append(syl); i += len(syl); break
        else:
            return None
    return out


VALID = set()
for _c, _vs in {"k": "aiueo", "g": "aiueo", "s": "aueo", "sh": "aiuo", "z": "aueo", "j": "aiuo", "t": "aeo",
                "ch": "aiuo", "ts": "u", "d": "aeo", "n": "aiueo", "h": "aieo", "f": "u", "b": "aiueo",
                "p": "aiueo", "m": "aiueo", "y": "auo", "r": "aiueo", "w": "ao", "ky": "auo", "gy": "auo",
                "ny": "auo", "hy": "auo", "by": "auo", "py": "auo", "my": "auo", "ry": "auo"}.items():
    for _v in _vs:
        VALID.add(_c + _v)

# ---- Russian, Polivanov ----
RU_V = {"a": "а", "i": "и", "u": "у", "e": "э", "o": "о"}
RU_C = {"k": "к", "g": "г", "s": "с", "z": "дз", "t": "т", "d": "д", "n": "н", "h": "х", "f": "ф", "b": "б",
        "p": "п", "m": "м", "r": "р", "w": "в", "j": "дз", "ch": "т", "sh": "с", "ts": "ц"}
RU_YO = {"a": "я", "u": "ю", "o": "ё", "i": "и"}


def _ru_syl(s, prev, nxt):
    if s == "N":
        return "м" if nxt and nxt[0] in "bpm" else ("нъ" if nxt and (nxt[0] in VOWELS or nxt[0] == "y") else "н")
    if s == "Q":
        return {"ch": "т", "ts": "т"}.get(nxt[:2], RU_C.get(nxt[:2]) or RU_C.get(nxt[0], "")) if nxt else ""
    if s in RU_V:
        # い after a vowel is й in Polivanov (ai -> ай); other vowels stand.
        return "й" if s == "i" and prev and prev[-1] in "aueo" and prev not in ("N", "Q") and nxt != "N" else RU_V[s]
    cons, v = s[:-1], s[-1]
    if cons == "y":
        return {"a": "я", "u": "ю", "o": "ё"}[v]
    if cons == "w":
        return "ва" if v == "a" else "о"
    if cons in ("sh", "ch", "j") or (len(cons) == 2 and cons[1] == "y"):
        base = {"sh": "с", "ch": "т", "j": "дз"}.get(cons) or RU_C[cons[0]]
        return base + ("и" if v == "i" else RU_YO[v])
    if cons == "ts":
        return "цу"
    if cons == "f":
        return "фу"
    if cons == "z" and v == "u":
        return "дзу"
    return RU_C[cons] + RU_V[v]


def _ru_word(word):
    syl = _syllables(word)
    if syl is None:
        return None
    out = ""
    for k, s in enumerate(syl):
        out += _ru_syl(s, syl[k - 1] if k else "", syl[k + 1] if k + 1 < len(syl) else "")
    return out[:1].upper() + out[1:]


# ---- Korean, 국립국어원 일본어 표기 ----
L_INIT = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
V_MED = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"
T_FIN = " ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ"


def _hangul(init, vowel, fin=" "):
    return chr(0xAC00 + (L_INIT.index(init) * 21 + V_MED.index(vowel)) * 28 + T_FIN.index(fin))


KO_V = {"a": "ㅏ", "i": "ㅣ", "u": "ㅜ", "e": "ㅔ", "o": "ㅗ"}
KO_YV = {"a": "ㅑ", "u": "ㅠ", "o": "ㅛ"}
KO_C_INITIAL = {"k": "ㄱ", "g": "ㄱ", "s": "ㅅ", "z": "ㅈ", "j": "ㅈ", "t": "ㄷ", "d": "ㄷ", "ch": "ㅈ",
                "ts": "ㅆ", "n": "ㄴ", "h": "ㅎ", "f": "ㅎ", "b": "ㅂ", "p": "ㅍ", "m": "ㅁ", "r": "ㄹ",
                "w": "ㅇ", "y": "ㅇ", "sh": "ㅅ"}
KO_C_MEDIAL = dict(KO_C_INITIAL, k="ㅋ", t="ㅌ", ch="ㅊ")


def _ko_word(word):
    syl = _syllables(word)
    if syl is None:
        return None
    out = []
    for k, s in enumerate(syl):
        if s in ("N", "Q"):
            if not out:
                return None
            last = out[-1]
            code = ord(last) - 0xAC00
            out[-1] = chr(ord(last) + T_FIN.index("ㄴ" if s == "N" else "ㅅ")) if code % 28 == 0 else last
            continue
        if s in KO_V:
            out.append(_hangul("ㅇ", KO_V[s])); continue
        cons, v = s[:-1], s[-1]
        table = KO_C_INITIAL if k == 0 else KO_C_MEDIAL
        if cons in ("sh", "ch", "j") or (len(cons) == 2 and cons[1] == "y"):
            base = cons if cons in ("sh", "ch", "j") else cons[0]
            vow = "ㅣ" if v == "i" else (KO_V[v] if base in ("sh", "ch", "j") else KO_YV[v])
            if base in ("sh", "ch", "j") and v != "i":
                vow = KO_YV[v] if base == "sh" else KO_V[v]  # sha 샤, cha 자/차, ja 자
            out.append(_hangul(table[base], vow)); continue
        if cons == "y":
            out.append(_hangul("ㅇ", KO_YV[v])); continue
        if cons == "w":
            out.append(_hangul("ㅇ", "ㅘ" if v == "a" else "ㅗ")); continue
        if cons in ("ts", "z", "s") and v == "u":
            out.append(_hangul(table[cons], "ㅡ")); continue  # 쓰, 즈, 스
        if cons == "f":
            out.append(_hangul("ㅎ", "ㅜ")); continue
        out.append(_hangul(table[cons], KO_V[v]))
    return "".join(out)


def _name(reading, word_fn, particle):
    words = reading.split()
    if not words:
        return None
    out = []
    for w in words:
        if w.lower() == "no" and out:
            out[-1] += particle
            continue
        got = word_fn(w)
        if not got:
            return None
        out.append(got)
    return " ".join(out)


def to_ru(reading):
    return _name(reading, _ru_word, "-но")


def to_ko(reading):
    return _name(reading, _ko_word, "노")
