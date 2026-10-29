"""Names in Cyrillic, Greek (with Bactrian ϸ), Georgian, Armenian, Hebrew, Arabic, Devanagari, Ethiopic, Gothic,
Kharosthi and Nabataean into Latin.

The other direction of `scripts/translit_scripts.py`, which writes Latin names into those scripts. This reads them
back, so a person whose only name is `Θεόδωρος /Κομνηνὸς Λάσκαρις/` or `عِيْسَى /بن لُبّ بن مُوسَى/` gets a Latin form, and
through it the `ja`/`zh`/`ko` the label composer makes from Latin (Emma, 2026-10-17, for gaiad.ged: "try wikidata
but then build readers"). Nothing in the repo read these scripts before: 646 primary names in gaiad.ged, 405 of
them Arabic.

The standard is `translit_scripts.py`'s: a transcription a native reader would spell differently is acceptable; a
different name is not. Every mapping is letter by letter from the written form; no language is guessed.

| script | system | what it costs |
| --- | --- | --- |
| Cyrillic | BGN/PCGN-style, plus the Serbian and Ukrainian letters | near-lossless |
| Greek | ELOT 743-style (θ th, χ ch, υ y), Greek numerals as Roman | near-lossless |
| Georgian | the national romanization, ejectives unmarked | near-lossless |
| Armenian | Hübschmann-Meillet without diacritics, letter numerals as Roman | near-lossless |
| Devanagari | inherent `a`, matras, virama, final schwa dropped | structural |
| Arabic | consonants plus the vowel marks when written; `بن` ibn, `ال` al-; an unvocalised word Wikidata's name items spell (reports/arabic-name-words.tsv: هنري Henry, مالك Malik) takes that spelling | an abjad: short vowels are lost in words the table lacks |
| Hebrew | consonants with the Yiddish vowel letters (ו u, יי ey); an acronym (כ"ץ) with an a between consonants, Katz | an abjad: vowels mostly lost |
| Nabataean | as the Hebrew letter of the same name | an abjad, as Hebrew |
| Gothic | the standard transliteration (𐍂𐌴𐌹𐌺𐍃 reiks) | near-lossless |
| Kharosthi | inherent `a`, kept at the end; vowel signs, virama | structural |
| Ethiopic | Ge'ez syllables read off their Unicode names; first order `e` (`a` on the laryngeals), sixth order `e` inside a word and nothing at its end | the sixth order's vowel is a guess: ማክዳ Makeda, ንግሥተ Negesete |

`romanize(text)` keeps the GEDCOM `/surname/` marks and any Latin already in the text, and returns `None` when a
letter it does not know is left, so a half-read name is never emitted.
"""

import re
import unicodedata

CYRL = {"а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo", "ж": "zh", "з": "z", "и": "i",
        "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t",
        "у": "u", "ф": "f", "х": "kh", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "shch", "ъ": "", "ы": "y", "ь": "",
        "э": "e", "ю": "yu", "я": "ya", "і": "i", "ї": "yi", "є": "ye", "ґ": "g", "ў": "w", "ђ": "dj", "ј": "j",
        "љ": "lj", "њ": "nj", "ћ": "c", "џ": "dz", "ѣ": "e", "ѳ": "f", "ѵ": "i"}

GREK2 = {"ου": "ou", "αι": "ai", "ει": "ei", "οι": "oi", "υι": "yi", "αυ": "av", "ευ": "ev", "γγ": "ng", "γκ": "gk",
         "μπ": "mp", "ντ": "nt", "τσ": "ts", "τζ": "tz"}
GREK = {"α": "a", "β": "v", "γ": "g", "δ": "d", "ε": "e", "ζ": "z", "η": "i", "θ": "th", "ι": "i", "κ": "k",
        "λ": "l", "μ": "m", "ν": "n", "ξ": "x", "ο": "o", "π": "p", "ρ": "r", "σ": "s", "ς": "s", "τ": "t",
        "υ": "y", "φ": "f", "χ": "ch", "ψ": "ps", "ω": "o", "ϸ": "sh"}   # ϸ: Bactrian sho (ϷΑΟΝΑΝΟϷΑΟ)
GREK_NUM = {"α": 1, "β": 2, "γ": 3, "δ": 4, "ε": 5, "ϛ": 6, "στ": 6, "ζ": 7, "η": 8, "θ": 9, "ι": 10}

GEOR = {"ა": "a", "ბ": "b", "გ": "g", "დ": "d", "ე": "e", "ვ": "v", "ზ": "z", "თ": "t", "ი": "i", "კ": "k",
        "ლ": "l", "მ": "m", "ნ": "n", "ო": "o", "პ": "p", "ჟ": "zh", "რ": "r", "ს": "s", "ტ": "t", "უ": "u",
        "ფ": "p", "ქ": "k", "ღ": "gh", "ყ": "q", "შ": "sh", "ჩ": "ch", "ც": "ts", "ძ": "dz", "წ": "ts", "ჭ": "ch",
        "ხ": "kh", "ჯ": "j", "ჰ": "h", "ჱ": "e", "ჲ": "y", "ჳ": "w", "ჴ": "q", "ჵ": "o"}

ARMN = {"ա": "a", "բ": "b", "գ": "g", "դ": "d", "ե": "e", "զ": "z", "է": "e", "ը": "y", "թ": "t", "ժ": "zh",
        "ի": "i", "լ": "l", "խ": "kh", "ծ": "ts", "կ": "k", "հ": "h", "ձ": "dz", "ղ": "gh", "ճ": "ch", "մ": "m",
        "յ": "y", "ն": "n", "շ": "sh", "ո": "o", "չ": "ch", "պ": "p", "ջ": "j", "ռ": "r", "ս": "s", "վ": "v",
        "տ": "t", "ր": "r", "ց": "ts", "փ": "p", "ք": "k", "օ": "o", "ֆ": "f", "և": "ev"}
ARMN_NUM = dict(zip("աբգդեզէըթ", range(1, 10)))

DEVA_CONS = {"क": "k", "ख": "kh", "ग": "g", "घ": "gh", "ङ": "ng", "च": "c", "छ": "ch", "ज": "j", "झ": "jh",
             "ञ": "ny", "ट": "t", "ठ": "th", "ड": "d", "ढ": "dh", "ण": "n", "त": "t", "थ": "th", "द": "d",
             "ध": "dh", "न": "n", "प": "p", "फ": "ph", "ब": "b", "भ": "bh", "म": "m", "य": "y", "र": "r",
             "ल": "l", "व": "v", "श": "sh", "ष": "sh", "स": "s", "ह": "h"}
DEVA_VOW = {"अ": "a", "आ": "a", "इ": "i", "ई": "i", "उ": "u", "ऊ": "u", "ऋ": "ri", "ए": "e", "ऐ": "ai", "ओ": "o",
            "औ": "au"}
DEVA_MATRA = {"ा": "a", "ि": "i", "ी": "i", "ु": "u", "ू": "u", "ृ": "ri", "े": "e", "ै": "ai", "ो": "o", "ौ": "au"}

ARAB = {"ب": "b", "ت": "t", "ث": "th", "ج": "j", "ح": "h", "خ": "kh", "د": "d", "ذ": "dh", "ر": "r", "ز": "z",
        "س": "s", "ش": "sh", "ص": "s", "ض": "d", "ط": "t", "ظ": "z", "ع": "'", "غ": "gh", "ف": "f", "ق": "q",
        "ك": "k", "ل": "l", "م": "m", "ن": "n", "ه": "h", "ء": "'", "ئ": "'", "ؤ": "'", "پ": "p", "چ": "ch",
        "ژ": "zh", "گ": "g", "ک": "k", "ی": "y", "ڤ": "v"}
ARAB_VOW = {"َ": "a", "ِ": "i", "ُ": "u", "ً": "an", "ٍ": "in", "ٌ": "un"}
ARAB_WORDS = {"بن": "ibn", "ابن": "ibn", "بنت": "bint", "أبو": "abu", "ابو": "abu", "عبد": "abd",
              # titles and ordinals in royal names (الملك أرتازركسيس الأول): the king, the queen, the first, the second
              "الملك": "al-Malik", "الملكة": "al-Malika", "الأول": "al-Awwal", "الثاني": "al-Thani"}

HEBR = {"ב": "b", "ג": "g", "ד": "d", "ה": "h", "ז": "z", "ח": "ch", "ט": "t", "כ": "k", "ך": "kh", "ל": "l",
        "מ": "m", "ם": "m", "נ": "n", "ן": "n", "ס": "s", "פ": "p", "ף": "f", "צ": "tz", "ץ": "tz", "ק": "k",
        "ר": "r", "ש": "sh", "ת": "t", "א": "a", "ע": "e"}


def _roman(n):
    out = ""
    for v, s in ((10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")):
        while n >= v:
            out, n = out + s, n - v
    return out


def _cyrl(w):
    w = "".join(c for c in unicodedata.normalize("NFD", w) if not unicodedata.combining(c))   # stress marks
    w = unicodedata.normalize("NFC", w.replace("й", "й"))
    out = []
    for ch in w:
        low = ch.lower()
        if low not in CYRL:
            return None
        r = CYRL[low]
        out.append(r.capitalize() if ch != low and r else r)
    return "".join(out)


def _grek(w):
    bare = "".join(c for c in unicodedata.normalize("NFD", w) if not unicodedata.combining(c))
    if bare.endswith(("ʹ", "'", "΄")):   # a Greek numeral: Αʹ is 1
        n = GREK_NUM.get(bare[:-1].lower())
        return _roman(n) if n else None
    low, out, i = bare.lower(), [], 0
    while i < len(low):
        two = low[i:i + 2]
        if two in GREK2:
            out.append(GREK2[two]); i += 2; continue
        if low[i] not in GREK:
            return None
        out.append(GREK[low[i]]); i += 1
    s = "".join(out)
    return s[:1].upper() + s[1:] if bare[:1].isupper() else s


def _geor(w):
    if not all(c in GEOR for c in w):
        return None
    return "".join(GEOR[c] for c in w).capitalize()


def _armn(w):
    low = w.lower()
    if len(low) == 1 and low in ARMN_NUM:   # a letter alone after a name is a numeral: Աշոտ Ա is Ashot I
        return _roman(ARMN_NUM[low])
    low = low.replace("ու", "u")
    if not all(c in ARMN or c == "u" for c in low):
        return None
    return "".join(ARMN.get(c, c) for c in low).capitalize()


def _deva(w):
    out, i = [], 0
    while i < len(w):
        c = w[i]
        if c in DEVA_VOW:
            out.append(DEVA_VOW[c]); i += 1; continue
        if c in DEVA_CONS:
            out.append(DEVA_CONS[c])
            nxt = w[i + 1] if i + 1 < len(w) else ""
            if nxt in DEVA_MATRA:
                out.append(DEVA_MATRA[nxt]); i += 2; continue
            if nxt == "्":
                i += 2; continue
            out.append("a"); i += 1; continue
        if c in "ंँ":
            out.append("n"); i += 1; continue
        if c == "ः":
            out.append("h"); i += 1; continue
        return None
    s = "".join(out)
    if s.endswith("a") and len(s) > 2:   # the final inherent vowel is not spoken
        s = s[:-1]
    return s.capitalize()


_ARAB_NAMES = {}


def arab_names():
    """{unvocalised word: usual Latin spelling} from Wikidata's name items (build-arabic-name-words.py)."""
    if not _ARAB_NAMES:
        from pathlib import Path
        path = Path(__file__).resolve().parent.parent / "reports" / "arabic-name-words.tsv"
        if path.exists():
            for row in path.read_text(encoding="utf-8").splitlines()[1:]:
                ar, latin = row.split("\t")[:2]
                _ARAB_NAMES[ar] = latin
    return _ARAB_NAMES


def _arab(w):
    w = w.replace("ـ", "").replace("ٱ", "ا")   # tatweel; alef wasla reads as alef
    w = w.rstrip("ًٌٍَُِْ")   # case endings (a final shadda stays: لُبّ is Lubb) are not part of a name
    bare = "".join(c for c in w if c not in ARAB_VOW and c not in "ّْٰ")
    if bare in ARAB_WORDS:
        return ARAB_WORDS[bare]
    prefix = ""
    if bare.startswith("ال") and len(bare) > 3:
        prefix, w = "al-", w[w.index("ل") + 1:]
    if not any(c in ARAB_VOW for c in w) and w in arab_names():   # unvocalised: the spelling people use (Henry)
        return prefix + arab_names()[w]
    out, i, prev_cons = [], 0, False
    while i < len(w):
        c = w[i]
        if c in ARAB_VOW:
            out.append(ARAB_VOW[c]); prev_cons = False
        elif c == "ّ" and out:   # shadda: the consonant doubled
            out.append(out[-1] if out[-1] not in "aiu" else "")
        elif c in "ْٰ":
            pass
        elif c in "اأإآىٱ":
            if out and out[-1] == "a" and c in "اى":
                pass   # a long a after its fatha is one vowel
            else:
                out.append("i" if c == "إ" else "a")
            prev_cons = False
        elif c == "ة":
            out.append("a"); prev_cons = False
        elif c == "و":
            if out and out[-1] == "u":
                pass   # a long u after its damma is one vowel
            else:
                out.append("u" if prev_cons else "w")
            prev_cons = not prev_cons and not (out and out[-1] == "u")
        elif c in "يی":
            if out and out[-1] == "i":
                pass   # a long i after its kasra is one vowel
            else:
                out.append("i" if prev_cons else "y")
            prev_cons = not prev_cons and not (out and out[-1] == "i")
        elif c in ARAB:
            out.append(ARAB[c]); prev_cons = True
        else:
            return None
        i += 1
    s = "".join(out).strip("'")
    if not s:
        return None
    return prefix + s.capitalize()


def _hebr(w):
    w = "".join(c for c in w if not ("֑" <= c <= "ׇ"))   # points and cantillation
    acronym = any(m in w for m in "\"'״׳")   # a quote mark inside a word makes it an acronym: כ"ץ, ש"ץ
    w = "".join(c for c in w if c not in "\"'״׳")
    s = w.replace("וו", "v").replace("וי", "oy").replace("יי", "ey").replace("ו", "u").replace("י", "i")
    out = []
    for i, c in enumerate(s):
        if c in "vuoiey":
            out.append(c)
        elif c == "ה" and i == len(s) - 1 and not acronym:
            out.append("e")
        elif c == "א" and i + 1 < len(s) and s[i + 1] in "uoiey":
            continue   # an alef before a vowel letter carries it
        elif c in HEBR:
            out.append(HEBR[c])
        else:
            return None
    if acronym:   # read as it is said, an a between two consonants: כ"ץ Katz, ש"ץ Shatz, ריב"ש Ribash
        vowel = lambda o: o[-1] in "aeiouy"
        out = [o + ("a" if k + 1 < len(out) and not vowel(o) and not vowel(out[k + 1]) else "")
               for k, o in enumerate(out)]
    r = "".join(out)
    return r.capitalize() if r else None


# Nabataean is read as the Hebrew letter of the same name (NABATAEAN LETTER LAMEDH is ל).
HEBR_BY_NAME = {"ALEPH": "א", "BETH": "ב", "GIMEL": "ג", "DALETH": "ד", "HE": "ה", "WAW": "ו", "ZAYIN": "ז",
                "HETH": "ח", "TETH": "ט", "YODH": "י", "KAPH": "כ", "FINAL KAPH": "ך", "LAMEDH": "ל", "MEM": "מ",
                "FINAL MEM": "ם", "NUN": "נ", "FINAL NUN": "ן", "SAMEKH": "ס", "AYIN": "ע", "PE": "פ", "SADHE": "צ",
                "QOPH": "ק", "RESH": "ר", "SHIN": "ש", "TAW": "ת", "FINAL SHIN": "ש", "FINAL HE": "ה",
                "FINAL LAMEDH": "ל", "FINAL BETH": "ב"}


def _nbat(w):
    import unicodedata as u
    heb = []
    for c in w:
        name = u.name(c, "")
        if not name.startswith("NABATAEAN LETTER ") or name[17:] not in HEBR_BY_NAME:
            return None
        heb.append(HEBR_BY_NAME[name[17:]])
    return _hebr("".join(heb))


# Gothic, in the standard transliteration (þ as th, ƕ as hw, q as kw); the two numeral letters are not names.
GOTH = {"AHSA": "a", "BAIRKAN": "b", "GIBA": "g", "DAGS": "d", "AIHVUS": "e", "QAIRTHRA": "q", "IUJA": "z",
        "HAGL": "h", "THIUTH": "th", "EIS": "i", "KUSMA": "k", "LAGUS": "l", "MANNA": "m", "NAUTHS": "n", "JER": "j",
        "URUS": "u", "PAIRTHRA": "p", "RAIDA": "r", "SAUIL": "s", "TEIWS": "t", "WINJA": "w", "FAIHU": "f",
        "IGGWS": "x", "HWAIR": "hw", "OTHAL": "o"}


def _goth(w):
    import unicodedata as u
    out = []
    for c in w:
        name = u.name(c, "")
        if not name.startswith("GOTHIC LETTER ") or name[14:] not in GOTH:
            return None
        out.append(GOTH[name[14:]])
    return "".join(out).capitalize()


# Kharosthi, the Gandhari abugida: an inherent a (kept at the end, as Gandhari names end in it), vowel signs, virama.
KHAR_VOW = {"I": "i", "U": "u", "VOCALIC R": "ri", "E": "e", "O": "o"}


def _khar(w):
    import unicodedata as u
    out, pending = [], False
    for c in w:
        name = u.name(c, "")
        if name.startswith("KHAROSHTHI LETTER "):
            if pending:
                out.append("a")
            letter = name[18:].lower()   # KHAROSHTHI LETTER KA: the consonant is k
            out.append(letter[:-1] if letter.endswith("a") else letter)
            pending = True
        elif name.startswith("KHAROSHTHI VOWEL SIGN ") and name[22:] in KHAR_VOW and pending:
            out.append(KHAR_VOW[name[22:]])
            pending = False
        elif name == "KHAROSHTHI VIRAMA" and pending:
            pending = False
        else:
            return None
    if pending:
        out.append("a")
    s = "".join(out)
    return s.capitalize() if s else None


# Ge'ez consonants as Unicode names them (ETHIOPIC SYLLABLE MAA is m + the fourth order), longest first so SH is
# not read as S. The ejectives and the second h/s/ts lose their marks, as in Georgian above.
ETHI_CONS = {"HH": "h", "SZ": "s", "SH": "sh", "QH": "q", "NY": "ny", "KX": "kh", "ZH": "zh", "DD": "d", "GG": "g",
             "TH": "t", "CH": "ch", "PH": "p", "TS": "ts", "TZ": "ts", "H": "h", "L": "l", "M": "m", "R": "r",
             "S": "s", "Q": "q", "B": "b", "V": "v", "T": "t", "C": "ch", "X": "h", "N": "n", "K": "k", "W": "w",
             "Z": "z", "Y": "y", "D": "d", "J": "j", "G": "g", "F": "f", "P": "p"}
# The orders: A first (ä), U, I, AA fourth (a), EE fifth (e), E sixth (none), O, and the labialised forms.
ETHI_VOW = {"WAA": "wa", "WEE": "we", "WA": "wa", "WI": "wi", "WE": "we", "OA": "wa", "YA": "ya", "AA": "a",
            "EE": "e", "A": "ä", "U": "u", "I": "i", "E": "", "O": "o"}
ETHI_LARYNGEAL = {"GLOTTAL", "PHARYNGEAL", "H", "HH", "X"}


def _ethi_syllable(c):
    import unicodedata as u
    name = u.name(c, "")
    if not name.startswith("ETHIOPIC SYLLABLE "):
        return None
    rest = name[len("ETHIOPIC SYLLABLE "):]
    if rest.startswith(("GLOTTAL ", "PHARYNGEAL ")):
        row, vow = rest.split(" ", 1)
        return row, "", ETHI_VOW.get(vow)
    for k in sorted(ETHI_CONS, key=len, reverse=True):
        if rest.startswith(k) and rest[len(k):] in ETHI_VOW:
            return k, ETHI_CONS[k], ETHI_VOW[rest[len(k):]]
    return None


def _ethi(w):
    sylls = [_ethi_syllable(c) for c in w]
    if any(s is None or s[2] is None for s in sylls):
        return None
    out = []
    for i, (row, cons, vow) in enumerate(sylls):
        last = i == len(sylls) - 1
        if vow == "ä":   # the first order: e as Amharic is written in Latin (ተ te), a on the laryngeals (ሀ ha, አ a)
            vow = "a" if row in ETHI_LARYNGEAL else "e"
        if vow == "":   # the sixth order: the spoken ə inside a word (ማክዳ Makeda), nothing at its end
            prev_vowel = bool(out) and out[-1][-1:] in "aeiou"
            if cons in ("y", "w") and prev_vowel:   # ይ, ው after a vowel close it: ሀይለ Haile
                out.append("i" if cons == "y" else "u")
                continue
            vow = "" if last else "e"
        out.append(cons + vow)
    s = "".join(out)
    return s.capitalize() if s else None


READERS = [("Ѐ", "ӿ", _cyrl), ("Ͱ", "Ͽ", _grek), ("ἀ", "῿", _grek),
           ("Ⴀ", "ჿ", _geor), ("԰", "֏", _armn), ("ऀ", "ॿ", _deva),
           ("؀", "ۿ", _arab), ("֐", "׿", _hebr), ("ሀ", "፿", _ethi),
           ("\U00010330", "\U0001034f", _goth), ("\U00010a00", "\U00010a5f", _khar),
           ("\U00010880", "\U000108af", _nbat)]
LANG = {_cyrl: "und-Cyrl", _grek: "el", _geor: "ka", _armn: "hy", _deva: "und-Deva", _arab: "und-Arab",
        _hebr: "und-Hebr", _ethi: "und-Ethi", _goth: "got", _khar: "und-Khar", _nbat: "und-Nbat"}


def reader_for(text):
    for lo, hi, f in READERS:
        if any(lo <= c <= hi for c in text):
            return f
    return None


def romanize(text):
    """`(latin, lang)` for a name in one of these scripts, the /surname/ marks kept; `(None, None)` if unreadable."""
    f = reader_for(text)
    if not f:
        return None, None
    out = []
    # A hyphen joins two words and is kept (Бага-шад, Baga-shad); a bracket is dropped and parts the words it stood
    # between; an underscore from a Wikipedia title (نيلوس_(الأساطير)) is a space.
    for part in re.split(r"(\s+|/|[-‐‑()])", text.replace("_", " ")):
        if part in ("-", "‐", "‑"):
            out.append("-")
            continue
        if part in ("(", ")"):   # שור(ריב"ש") is two words, Shur Ribash
            out.append(" ")
            continue
        if not part or part.isspace() or part == "/":
            out.append(part)
            continue
        core = part.strip("\"'()[]{},;:.!?«»“”،؛")
        if not core:
            continue
        if not reader_for(core):   # Latin or digits already: kept
            out.append(core)
            continue
        r = f(core)
        if r is None:
            return None, None
        out.append(r)
    s = " ".join("".join(out).split())
    if s.count("/") == 2:   # a bracket at the edge of the surname leaves no space inside its slashes
        a, sur, b = s.split("/")
        s = f"{a}/{sur.strip()}/{b}"
    return s, LANG[f]


def check(samples=None):
    """Print the reading of each sample name, the measurement this file is judged on."""
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    for s in samples or ["Феодосия Ярославна /Рюриковна/", "Θεόδωρος Αʹ /Κομνηνὸς Λάσκαρις/", "ვახტანგ I //",
                         "Աշոտ Ա /Բագրատունի/", "वासुदेव /कुषाण/", "عِيْسَى /بن لُبّ بن مُوسَى/", "אריה לייב /HaKohen Rapaport/",
                         "ማክዳ /ንግሥተ ሳእ/", "ኃይለ ሥላሴ", "ምኒልክ", "ቴዎድሮስ", "ዘርአ ያዕቆብ", "ልብነ ድንግል",
                         "Avraham /כ\"ץ/ of Porto", "ϷΑΟΝΑΝΟϷΑΟ /ΚΑΝΗϷΚΟ/", "Бага-шад //", "Vultulf // 𐍂𐌴𐌹𐌺𐍃",
                         "𐨬𐨁𐨬 /𐨐𐨿𐨪𐨥𐨁𐨱𐨿𐨪/", "𐢗𐢑𐢍𐢔 //", "مارغريت، بنت بيتر"]:
        print(f"{s:<40} {romanize(s)}")


if __name__ == "__main__":
    check()
