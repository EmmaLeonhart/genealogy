"""Pinyin (toneless, as in a Wikidata `en` label) -> Russian Palladius transcription.

`to_palladius("Yang Zhirou")` -> "Ян Чжижоу". Each word is split into pinyin syllables; a word that splits in more
than one way, or not at all, gives None, so a caller writes nothing rather than a guess.
"""
import functools

INITIALS = {"b": "б", "p": "п", "m": "м", "f": "ф", "d": "д", "t": "т", "n": "н", "l": "л", "g": "г",
            "k": "к", "h": "х", "j": "цз", "q": "ц", "x": "с", "zh": "чж", "ch": "ч", "sh": "ш", "r": "ж",
            "z": "цз", "c": "ц", "s": "с"}
# Finals after a consonant initial.
FINALS = {"a": "а", "o": "о", "e": "э", "ai": "ай", "ei": "эй", "ao": "ао", "ou": "оу", "an": "ань",
          "en": "энь", "ang": "ан", "eng": "эн", "ong": "ун", "i": "и", "ia": "я", "ie": "е", "iao": "яо",
          "iu": "ю", "ian": "янь", "in": "инь", "iang": "ян", "ing": "ин", "iong": "юн", "u": "у", "ua": "уа",
          "uo": "о", "uai": "уай", "ui": "уй", "uan": "уань", "un": "унь", "uang": "уан", "ue": "юэ",
          "v": "юй", "ve": "юэ"}
ZERO = {"a": "а", "ai": "ай", "an": "ань", "ang": "ан", "ao": "ао", "e": "э", "ei": "эй", "en": "энь",
        "eng": "эн", "er": "эр", "o": "о", "ou": "оу", "yi": "и", "ya": "я", "yao": "яо", "ye": "е", "you": "ю",
        "yan": "янь", "yin": "инь", "yang": "ян", "ying": "ин", "yong": "юн", "yu": "юй", "yue": "юэ",
        "yuan": "юань", "yun": "юнь", "wu": "у", "wa": "ва", "wo": "во", "wai": "вай", "wei": "вэй",
        "wan": "вань", "wen": "вэнь", "wang": "ван", "weng": "вэн"}
VALID_AFTER = {  # which finals each initial takes in standard pinyin
    "b": "a o ai ei ao an en ang eng i ie iao ian in ing u", "p": "a o ai ei ao ou an en ang eng i ie iao ian in ing u",
    "m": "a o e ai ei ao ou an en ang eng i ie iao iu ian in ing u", "f": "a o ei ou an en ang eng u",
    "d": "a e ai ei ao ou an en ang eng ong i ia ie iao iu ian ing u uo ui uan un",
    "t": "a e ai ao ou an ang eng ong i ie iao ian ing u uo ui uan un",
    "n": "a e ai ei ao ou an en ang eng ong i ie iao iu ian in iang ing u uo uan v ve",
    "l": "a o e ai ei ao ou an ang eng ong i ia ie iao iu ian in iang ing u uo uan un v ve",
    "g": "a e ai ei ao ou an en ang eng ong u ua uo uai ui uan un uang",
    "k": "a e ai ao ou an en ang eng ong u ua uo uai ui uan un uang",
    "h": "a e ai ei ao ou an en ang eng ong u ua uo uai ui uan un uang",
    "j": "i ia ie iao iu ian in iang ing iong u ue uan un", "q": "i ia ie iao iu ian in iang ing iong u ue uan un",
    "x": "i ia ie iao iu ian in iang ing iong u ue uan un",
    "zh": "a e ai ei ao ou an en ang eng ong i u ua uo uai ui uan un uang",
    "ch": "a e ai ao ou an en ang eng ong i u ua uo uai ui uan un uang",
    "sh": "a e ai ei ao ou an en ang eng i u ua uo uai ui uan un uang",
    "r": "e ao ou an en ang eng ong i u uo ui uan un", "z": "a e ai ei ao ou an en ang eng ong i u uo ui uan un",
    "c": "a e ai ao ou an en ang eng ong i u uo ui uan un", "s": "a e ai ao ou an en ang eng ong i u uo ui uan un"}


def _syllables():
    out = dict(ZERO)
    for ini, finals in VALID_AFTER.items():
        for fin in finals.split():
            cyr = FINALS[fin]
            if fin == "i" and ini in ("z", "c", "s"):
                cyr = "ы"
            if fin in ("u", "ue", "uan", "un") and ini in ("j", "q", "x"):
                cyr = {"u": "юй", "ue": "юэ", "uan": "юань", "un": "юнь"}[fin]
            out[ini + fin.replace("v", "ü")] = INITIALS[ini] + cyr
    return out


SYL = _syllables()


@functools.lru_cache(None)
def _splits(word, first=True):
    if not word:
        return [[]]
    got = []
    for n in range(min(6, len(word)), 0, -1):
        head = word[:n]
        # Pinyin writes an apostrophe before a/e/o inside a word (Xi'an), so without one it is never a
        # syllable boundary: Xian is xian, Kuan is kuan.
        if head in SYL and (first or head[0] not in "aeo"):
            got += [[head] + rest for rest in _splits(word[n:], False)]
    return got


def to_palladius(name):
    words = []
    for w in name.split():
        if not w.isascii() or not w.isalpha():
            return None
        splits = _splits(w.lower())
        if len(splits) != 1:
            return None
        cyr = ""
        for s in splits[0]:
            part = SYL[s]
            if cyr.endswith("н") and (part[0] in "яюеё" or s == "yi"):
                cyr += "ъ"  # Palladius: Чэнъю, not Чэню
            cyr += part
        words.append(cyr[0].upper() + cyr[1:])
    return " ".join(words) or None
