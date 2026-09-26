"""Latin names into Cyrillic, Greek, Devanagari and Arabic.

The seven languages are `en` · `ja` · `zh` · `hi` · `ar` · `ru` · `el` plus `mul`. `ja`/`zh`
are `scripts/translit_no.py`; this is the other four, authorised 2026-08-31 to run in parallel
rather than behind them.

**The standard that governs, and the reason this is allowed to exist:** *"Incorrect romanization or
incorrect representations in katakana are totally acceptable. An incorrect name is not, because
half these words, nobody knows how they're pronounced anyway."* A transcription that a native
reader would spell differently is acceptable; a different *name* is not. So every mapping here is
letter-for-letter from the Latin form and nothing is invented, guessed from language, or looked up.

## The four are not equally safe, and the differences are real

| | script | what it costs |
| --- | --- | --- |
| `ru` | Cyrillic | alphabetic, near-lossless. The only real choice is `v`/`w` -> `в` |
| `el` | Greek | alphabetic. Latin `b`,`d`,`g` have no exact Greek match; digraphs are used |
| `hi` | Devanagari | an **abugida**: every consonant carries an inherent `a`, so a cluster needs a virama and a vowel needs a matra. Structural, not lossy |
| `ar` | Arabic | an **abjad**: short vowels are not written. `Arne` and `Aren` collide |

**`ar` loses information and that is a property of the script, not of this code.** Long vowels are
written with `ا`/`و`/`ي` -- the ordinary convention for foreign names -- so the loss is bounded to
short vowels rather than all of them. It is flagged here so nobody later reads an Arabic label as
round-trippable.

**No language is inferred.** `CLAUDE.md` forbids guessing what language a name is, and nothing
here does: the same letters produce the same output whoever the person was.
"""

import re
import unicodedata

# ---------------------------------------------------------------------------------------
# Cyrillic. Digraphs first, longest match. `щ` needs `shch` before `sh` sees it.
RU_DIGRAPHS = [
    ("shch", "щ"), ("sch", "щ"), ("sh", "ш"), ("ch", "ч"), ("zh", "ж"), ("ts", "ц"),
    ("kh", "х"), ("ph", "ф"), ("th", "т"), ("ck", "к"), ("qu", "кв"),
    # **A consonant + `j` + vowel is a SOFT consonant, not two letters.** `Bjørn` is `Бьёрн`
    # in Russian, and reading `bj` letter by letter gave `бйёрн`, which is not a word. Found by
    # printing the output; the table looked complete.
    ("bj", "бь"), ("dj", "дь"), ("fj", "фь"), ("gj", "гь"), ("kj", "кь"), ("lj", "ль"),
    ("mj", "мь"), ("nj", "нь"), ("pj", "пь"), ("rj", "рь"), ("sj", "сь"), ("tj", "ть"),
    ("vj", "вь"),
    ("ya", "я"), ("ja", "я"), ("yu", "ю"), ("ju", "ю"), ("yo", "ё"), ("ye", "е"),
    ("je", "е"), ("ee", "и"), ("oo", "у"), ("aa", "а"), ("ij", "ий"),
    # `-ia` and `-ya` end a name in `-ия`: `Maria` is `Мария`, not `Мариа`.
    ("ia", "ия"), ("iya", "ия"),
]
RU_SINGLE = {
    "a": "а", "b": "б", "c": "к", "d": "д", "e": "е", "f": "ф", "g": "г", "h": "х",
    "i": "и", "j": "й", "k": "к", "l": "л", "m": "м", "n": "н", "o": "о", "p": "п",
    "q": "к", "r": "р", "s": "с", "t": "т", "u": "у", "v": "в", "w": "в", "x": "кс",
    "y": "й", "z": "з",
    "æ": "э", "ä": "э", "ø": "ё", "ö": "ё", "å": "о", "é": "е", "è": "е", "ü": "ю",
    "á": "а", "à": "а", "í": "и", "ó": "о", "ú": "у", "ñ": "нь", "ç": "с", "ß": "сс",
}

# ---------------------------------------------------------------------------------------
# Greek. `b`, `d` and `g` have no single Greek letter with those sounds in modern usage;
# `μπ`, `ντ`, `γκ` are what Greek itself uses for foreign names, so they are used here.
EL_DIGRAPHS = [
    ("th", "θ"), ("ph", "φ"), ("ch", "χ"), ("kh", "χ"), ("ps", "ψ"), ("ks", "ξ"),
    ("sh", "σ"), ("zh", "ζ"), ("ck", "κ"), ("qu", "κου"), ("ou", "ου"), ("oo", "ου"),
    ("ee", "ι"), ("b", "μπ"), ("d", "ντ"), ("g", "γκ"),
]
EL_SINGLE = {
    "a": "α", "c": "κ", "e": "ε", "f": "φ", "h": "", "i": "ι", "j": "ι", "k": "κ",
    "l": "λ", "m": "μ", "n": "ν", "o": "ο", "p": "π", "q": "κ", "r": "ρ", "s": "σ",
    "t": "τ", "u": "ου", "v": "β", "w": "β", "x": "ξ", "y": "υ", "z": "ζ",
    "æ": "αι", "ä": "α", "ø": "ε", "ö": "ε", "å": "ο", "é": "ε", "è": "ε", "ü": "υ",
    "á": "α", "à": "α", "í": "ι", "ó": "ο", "ú": "ου", "ñ": "ν", "ç": "σ", "ß": "σσ",
}

# ---------------------------------------------------------------------------------------
# Devanagari. An abugida: a bare consonant already says `a`, so a following vowel replaces
# that with a matra, and a following consonant needs a virama to suppress it.
HI_CONS = {
    "k": "क", "kh": "ख", "g": "ग", "gh": "घ", "ch": "च", "j": "ज", "jh": "झ",
    "t": "त", "th": "थ", "d": "द", "dh": "ध", "n": "न", "p": "प", "ph": "फ",
    "f": "फ़", "b": "ब", "bh": "भ", "m": "म", "y": "य", "r": "र", "l": "ल",
    "v": "व", "w": "व", "sh": "श", "s": "स", "h": "ह", "z": "ज़", "c": "क",
    "q": "क़", "x": "क्स", "ñ": "न",
}
#: independent form (word-initial), then the matra (after a consonant)
HI_VOWEL = {
    "a": ("अ", ""), "aa": ("आ", "ा"), "i": ("इ", "ि"), "ee": ("ई", "ी"),
    "u": ("उ", "ु"), "oo": ("ऊ", "ू"), "e": ("ए", "े"), "ai": ("ऐ", "ै"),
    "o": ("ओ", "ो"), "au": ("औ", "ौ"),
    # `ia` is `i` plus the `ya` glide in Devanagari -- `Maria` is `मारिया`. Read as two
    # separate vowels it gave `मरिअ`, with a bare independent `अ` stranded after a matra.
    "ia": ("इया", "िया"), "ea": ("इया", "िया"),
}
HI_VOWEL_ALIAS = {"y": "i", "æ": "ai", "ä": "e", "ø": "e", "ö": "e", "å": "o",
                  "é": "e", "è": "e", "ü": "u", "á": "aa", "à": "aa", "í": "ee",
                  "ó": "o", "ú": "oo"}
VIRAMA = "्"

# ---------------------------------------------------------------------------------------
# Arabic. An abjad. Long vowels get `ا`/`و`/`ي`, which is the ordinary convention for
# foreign names; short vowels are simply not written, and that loss is the script's.
#: `ia` and `ea` are written out in Arabic for a foreign name -- `Maria` is `ماريا`. Without
#: them the vowel-dropping rule reduced it to `مرا`, which has lost the name rather than its
#: short vowels, and that is where the standard actually draws the line.
AR_DIGRAPHS = [("kh", "خ"), ("gh", "غ"), ("sh", "ش"), ("th", "ث"), ("ch", "تش"),
               ("ph", "ف"), ("dh", "ذ"), ("ck", "ك"), ("qu", "كو"),
               ("ia", "يا"), ("ea", "يا"), ("ie", "ي"), ("ae", "ا")]
AR_SINGLE = {
    "a": "ا", "b": "ب", "c": "ك", "d": "د", "e": "ي", "f": "ف", "g": "غ", "h": "ه",
    "i": "ي", "j": "ج", "k": "ك", "l": "ل", "m": "م", "n": "ن", "o": "و", "p": "ب",
    "q": "ق", "r": "ر", "s": "س", "t": "ت", "u": "و", "v": "ف", "w": "و", "x": "كس",
    "y": "ي", "z": "ز",
    "æ": "ا", "ä": "ا", "ø": "و", "ö": "و", "å": "و", "é": "ي", "è": "ي", "ü": "و",
    "á": "ا", "à": "ا", "í": "ي", "ó": "و", "ú": "و", "ñ": "ن", "ç": "س", "ß": "س",
}
AR_VOWELS = set("aeiouyæäøöåéèüáàíóú")


def _prepare(token):
    """Lowercase, and drop combining marks the tables do not name."""
    t = unicodedata.normalize("NFC", token).lower()
    return re.sub(r"[^\w'’\-]", "", t, flags=re.UNICODE)


def _walk(token, digraphs, single):
    """Longest-match over `digraphs`, then `single`. Unknown letters are dropped."""
    out, i = [], 0
    t = _prepare(token)
    while i < len(t):
        for src, dst in digraphs:
            if t.startswith(src, i):
                out.append(dst)
                i += len(src)
                break
        else:
            out.append(single.get(t[i], ""))
            i += 1
    return "".join(out)


def to_ru(token):
    """Cyrillic. Word-initial `jo`/`yo` is `йо`, not `ё`.

    `Johannes` came out `Ёханнес`, which no Russian writes -- `ё` carries the glide only inside a
    word, and at the start the glide is spelled out. Handled before the digraph walk because the
    table has no notion of position.
    """
    t = _prepare(token)
    head = ""
    if t[:2] in ("jo", "yo"):
        head, t = "йо", t[2:]
    return head + _walk(t, RU_DIGRAPHS, RU_SINGLE)


def to_el(token):
    """Greek, with final sigma. `σ` at the end of a word is written `ς`."""
    s = _walk(token, EL_DIGRAPHS, EL_SINGLE)
    return s[:-1] + "ς" if s.endswith("σ") else s


def to_ar(token):
    """Arabic. A leading vowel takes `أ`; short vowels inside the word are dropped.

    Keeping every vowel would produce `ا` after every consonant and read as nonsense; keeping
    none would lose the shape of the name. The convention taken is the usual one for foreign
    names: **a vowel is written when it opens the word or follows another vowel, and dropped
    between consonants.**
    """
    t = _prepare(token)
    out, i, prev_was_vowel = [], 0, False
    while i < len(t):
        for src, dst in AR_DIGRAPHS:
            if t.startswith(src, i):
                out.append(dst)
                i += len(src)
                prev_was_vowel = False
                break
        else:
            ch = t[i]
            if ch in AR_VOWELS:
                # **Word-initial, doubled, and word-FINAL vowels are written.** Dropping the
                # final one turned `Maria` into `مرا`, which has lost the name rather than its
                # short vowels. A final vowel is the one an abjad conventionally keeps for a
                # foreign name, so it stays.
                last = i == len(t) - 1
                if not out or prev_was_vowel or last:
                    out.append("أ" if not out else AR_SINGLE.get(ch, ""))
                prev_was_vowel = True
            else:
                out.append(AR_SINGLE.get(ch, ""))
                prev_was_vowel = False
            i += 1
    return "".join(out)


def to_hi(token):
    """Devanagari. Consonants carry an inherent `a`; a vowel becomes a matra, a cluster a virama."""
    t = _prepare(token)
    out, i, after_cons = [], 0, False
    while i < len(t):
        two = t[i:i + 2]
        if two in HI_VOWEL or (two in HI_CONS and len(two) == 2):
            pass
        # vowels first: a digraph vowel beats a single consonant reading
        if two in HI_VOWEL:
            ind, matra = HI_VOWEL[two]
            out.append(matra if after_cons else ind)
            i += 2
            after_cons = False
            continue
        if two in HI_CONS:
            if after_cons:
                out.append(VIRAMA)
            out.append(HI_CONS[two])
            i += 2
            after_cons = True
            continue
        ch = t[i]
        key = HI_VOWEL_ALIAS.get(ch, ch)
        if key in HI_VOWEL:
            ind, matra = HI_VOWEL[key]
            out.append(matra if after_cons else ind)
            after_cons = False
        elif ch in HI_CONS:
            if after_cons:
                out.append(VIRAMA)
            out.append(HI_CONS[ch])
            after_cons = True
        i += 1
    return "".join(out)


SCRIPTS = {"ru": to_ru, "el": to_el, "hi": to_hi, "ar": to_ar}


#: Scripts that HAVE upper case and use it for proper names. Devanagari and Arabic have
#: no case at all, so nothing is done to them.
_CASED = {"ru", "el"}


#: Latin clusters the per-letter tables read wrongly. `chr` is a hard k followed by an r,
#: not the `ch` digraph -- `Christina` came out `чристина` in Cyrillic where it is
#: `Кристина`, and `χριστινα` in Greek. The same fix was needed in `translit_ko_latin`,
#: which is what made it worth looking for here.
_CLUSTERS = (("chr", "kr"), ("sch", "sh"))



# =======================================================================================
# THE TWELVE MORE, 2026-09-26. `queue.md`: *"Finally implement standardized labels in Russian,
# Ukrainian, Greek, Hindi, Arabic, Persian, Bengali, Hebrew, Tamil, Cherokee, Inuktitut,
# Ethiopian, Maldivian, Armenian, Georgian and zgh."* Four were here; these are the other twelve,
# under the same standard: letter for letter from the Latin form, nothing looked up, no language
# inferred. A transcription a native reader would spell differently is acceptable; a different
# name is not.
#
# Four kinds of script, so four shapes of engine:
#
#   alphabet     uk hy ka zgh     the `_walk` longest-match table, as `ru` and `el`
#   abjad        fa he            as `ar`: short vowels between consonants are not written
#   abugida      bn ta            as `hi`: a consonant carries `a`, a vowel is a matra
#   syllabary    chr iu am dv     a (consonant, vowel) pair is ONE sign, so the Latin is first
#                                 cut into syllables and each syllable is looked up whole

#: Accented and Nordic letters, folded to the plain vowel the syllabaries and the new
#: alphabets know. The four older engines carry their own entries and do not use this.
_FOLD = {"æ": "e", "ä": "e", "ø": "o", "ö": "o", "å": "o", "ü": "u", "é": "e", "è": "e",
         "ê": "e", "ë": "e", "á": "a", "à": "a", "â": "a", "í": "i", "ì": "i", "î": "i",
         "ï": "i", "ó": "o", "ò": "o", "ô": "o", "ú": "u", "ù": "u", "û": "u", "ñ": "n",
         "ç": "s", "ß": "ss", "ð": "d", "þ": "th", "œ": "e", "ł": "l"}


def _fold(token):
    t = "".join(_FOLD.get(ch, ch) for ch in _prepare(token))
    t = unicodedata.normalize("NFD", t)
    return "".join(ch for ch in t if ch.isascii() and (ch.isalpha() or ch in "-'"))


# ---------------------------------------------------------------------------------------
# Ukrainian. Cyrillic as `ru`, with Ukrainian's own letters: `і` for i, `и` for y, `є`/`ї` for
# the iotated e and i, `г` for h and `ґ` for g. No `ё`: the glide is written `йо`.
UK_DIGRAPHS = [
    ("shch", "щ"), ("sch", "щ"), ("sh", "ш"), ("ch", "ч"), ("zh", "ж"), ("ts", "ц"),
    ("tz", "ц"), ("kh", "х"), ("ph", "ф"), ("th", "т"), ("ck", "к"), ("qu", "кв"),
    ("ja", "я"), ("ya", "я"), ("ju", "ю"), ("yu", "ю"), ("je", "є"), ("ye", "є"),
    ("ji", "ї"), ("yi", "ї"), ("jo", "йо"), ("yo", "йо"), ("ee", "і"), ("oo", "у"),
    ("ia", "ія"),
]
UK_SINGLE = {
    "a": "а", "b": "б", "c": "к", "d": "д", "e": "е", "f": "ф", "g": "ґ", "h": "г",
    "i": "і", "j": "й", "k": "к", "l": "л", "m": "м", "n": "н", "o": "о", "p": "п",
    "q": "к", "r": "р", "s": "с", "t": "т", "u": "у", "v": "в", "w": "в", "x": "кс",
    "y": "и", "z": "з",
}


def to_uk(token):
    return _walk(_fold(token), UK_DIGRAPHS, UK_SINGLE)


# ---------------------------------------------------------------------------------------
# Armenian. Alphabetic and cased. `o` opens a word as `օ` and `e` as `է`; `u` is the digraph
# `ու`, which is how Armenian writes it.
HY_DIGRAPHS = [
    ("sh", "շ"), ("ch", "չ"), ("zh", "ժ"), ("kh", "խ"), ("gh", "ղ"), ("ts", "ց"),
    ("tz", "ց"), ("dz", "ձ"), ("th", "թ"), ("ph", "փ"), ("ck", "կ"), ("qu", "քվ"),
    ("ee", "ի"), ("oo", "ու"),
]
HY_SINGLE = {
    "a": "ա", "b": "բ", "c": "կ", "d": "դ", "e": "ե", "f": "ֆ", "g": "գ", "h": "հ",
    "i": "ի", "j": "յ", "k": "կ", "l": "լ", "m": "մ", "n": "ն", "o": "ո", "p": "պ",
    "q": "ք", "r": "ր", "s": "ս", "t": "տ", "u": "ու", "v": "վ", "w": "վ", "x": "քս",
    "y": "ի", "z": "զ",
}


def to_hy(token):
    t = _fold(token)
    head = ""
    if t[:1] == "o":
        head, t = "օ", t[1:]
    elif t[:1] == "e":
        head, t = "է", t[1:]
    return head + _walk(t, HY_DIGRAPHS, HY_SINGLE)


# ---------------------------------------------------------------------------------------
# Georgian, Mkhedruli. Unicameral in ordinary writing: Python would upper-case it into
# Mtavruli, which is a display style and not how a name is written, so `ka` is never cased.
KA_DIGRAPHS = [
    ("sh", "შ"), ("ch", "ჩ"), ("zh", "ჟ"), ("kh", "ხ"), ("gh", "ღ"), ("ts", "ც"),
    ("tz", "ც"), ("dz", "ძ"), ("th", "თ"), ("ph", "ფ"), ("ck", "კ"), ("qu", "კვ"),
    ("ee", "ი"), ("oo", "უ"),
]
KA_SINGLE = {
    "a": "ა", "b": "ბ", "c": "კ", "d": "დ", "e": "ე", "f": "ფ", "g": "გ", "h": "ჰ",
    "i": "ი", "j": "ი", "k": "კ", "l": "ლ", "m": "მ", "n": "ნ", "o": "ო", "p": "პ",
    "q": "ქ", "r": "რ", "s": "ს", "t": "ტ", "u": "უ", "v": "ვ", "w": "ვ", "x": "ქს",
    "y": "ი", "z": "ზ",
}


def to_ka(token):
    return _walk(_fold(token), KA_DIGRAPHS, KA_SINGLE)


# ---------------------------------------------------------------------------------------
# Standard Moroccan Tamazight (`zgh`), Neo-Tifinagh. Alphabetic with written vowels; there is
# no `o`, so it is `ⵓ`, and Latin `j` in these names is the /j/ glide, `ⵢ`.
ZGH_DIGRAPHS = [
    ("sh", "ⵛ"), ("ch", "ⵛ"), ("zh", "ⵊ"), ("kh", "ⵅ"), ("gh", "ⵖ"), ("th", "ⵜ"),
    ("ph", "ⴼ"), ("ts", "ⵜⵙ"), ("tz", "ⵜⵣ"), ("ck", "ⴽ"), ("qu", "ⴽⵡ"),
    ("ee", "ⵉ"), ("oo", "ⵓ"),
]
ZGH_SINGLE = {
    "a": "ⴰ", "b": "ⴱ", "c": "ⴽ", "d": "ⴷ", "e": "ⴻ", "f": "ⴼ", "g": "ⴳ", "h": "ⵀ",
    "i": "ⵉ", "j": "ⵢ", "k": "ⴽ", "l": "ⵍ", "m": "ⵎ", "n": "ⵏ", "o": "ⵓ", "p": "ⴱ",
    "q": "ⵇ", "r": "ⵔ", "s": "ⵙ", "t": "ⵜ", "u": "ⵓ", "v": "ⴼ", "w": "ⵡ", "x": "ⴽⵙ",
    "y": "ⵢ", "z": "ⵣ",
}


def to_zgh(token):
    # `y` with no vowel after it is the vowel i (`Yngve`, `Sylvia`), not the glide `ⵢ`.
    t = re.sub(r"y(?![aeiou])", "i", _fold(token))
    return _walk(t, ZGH_DIGRAPHS, ZGH_SINGLE)


# ---------------------------------------------------------------------------------------
# Persian. The Arabic engine with Persian's own letters: `پ` p, `گ` g, `چ` ch, `ژ` zh, `و` v,
# and the Persian forms of yeh and kaf (`ی`, `ک`), which are different code points from Arabic's.
FA_DIGRAPHS = [("ch", "چ"), ("zh", "ژ")] + AR_DIGRAPHS
FA_SINGLE = dict(AR_SINGLE, p="پ", g="گ", v="و")


def to_fa(token):
    global AR_DIGRAPHS, AR_SINGLE
    saved = AR_DIGRAPHS, AR_SINGLE
    AR_DIGRAPHS, AR_SINGLE = FA_DIGRAPHS, FA_SINGLE
    try:
        s = to_ar(token)
    finally:
        AR_DIGRAPHS, AR_SINGLE = saved
    s = s.replace("ي", "ی").replace("ك", "ک")
    # Persian opens a word on a bare alef, not the hamza-seated `أ` Arabic uses.
    return "ا" + s[1:] if s.startswith("أ") else s


# ---------------------------------------------------------------------------------------
# Hebrew. An abjad like Arabic, written the way Hebrew writes a foreign name: `i`/`y` take `י`,
# `o`/`u` take `ו`, `a`/`e` inside a word are not written, a vowel opening the word sits on `א`,
# and a final `a`/`e` is `ה`. Five letters take their final forms at the end of a word.
HE_DIGRAPHS = [("sch", "ש"), ("sh", "ש"), ("ch", "ח"), ("kh", "ח"), ("th", "ת"),
               ("ph", "פ"), ("ts", "צ"), ("tz", "צ"), ("ck", "ק"), ("qu", "קו"),
               ("zh", "ז'"), ("ee", "י"), ("oo", "ו")]
HE_CONS = {"b": "ב", "c": "ק", "d": "ד", "f": "פ", "g": "ג", "h": "ה", "j": "י", "k": "ק",
           "l": "ל", "m": "מ", "n": "נ", "p": "פ", "q": "ק", "r": "ר", "s": "ס", "t": "ט",
           "v": "ו", "w": "ו", "x": "קס", "z": "ז"}
HE_INITIAL = {"a": "א", "e": "א", "i": "אי", "y": "אי", "o": "או", "u": "או"}
HE_FINAL = {"כ": "ך", "מ": "ם", "נ": "ן", "פ": "ף", "צ": "ץ"}


def to_he(token):
    t = _fold(token)
    out, i = [], 0
    while i < len(t):
        for src, dst in HE_DIGRAPHS:
            if t.startswith(src, i):
                out.append(dst)
                i += len(src)
                break
        else:
            ch = t[i]
            if ch in "aeiouy":
                if not out:
                    out.append(HE_INITIAL[ch])
                elif ch in "iy":
                    out.append("י")
                elif ch in "ou":
                    out.append("ו")
                elif i == len(t) - 1:
                    out.append("ה")
            else:
                out.append(HE_CONS.get(ch, ""))
            i += 1
    s = "".join(out)
    if s and s[-1] in HE_FINAL:
        s = s[:-1] + HE_FINAL[s[-1]]
    return s


# ---------------------------------------------------------------------------------------
# Bengali and Tamil: the Devanagari engine's shape, with their own tables. Tamil has no voiced or
# aspirated stops of its own for these names, so `b`/`p`, `d`/`t`, `g`/`k` share a letter, and a
# word-final consonant takes the pulli -- without it Tamil reads an `a` that is not there.
BN_CONS = {
    "k": "ক", "kh": "খ", "g": "গ", "gh": "ঘ", "ch": "চ", "j": "জ", "jh": "ঝ",
    "t": "ট", "th": "থ", "d": "ড", "dh": "ধ", "n": "ন", "p": "প", "ph": "ফ",
    "f": "ফ", "b": "ব", "bh": "ভ", "m": "ম", "y": "য়", "r": "র", "l": "ল",
    "v": "ভ", "w": "ভ", "sh": "শ", "s": "স", "h": "হ", "z": "জ", "c": "ক",
    "q": "ক", "x": "ক্স",
}
BN_VOWEL = {
    "a": ("অ", ""), "aa": ("আ", "া"), "i": ("ই", "ি"), "ee": ("ঈ", "ী"),
    "u": ("উ", "ু"), "oo": ("ঊ", "ূ"), "e": ("এ", "ে"), "ai": ("ঐ", "ৈ"),
    "o": ("ও", "ো"), "au": ("ঔ", "ৌ"), "ia": ("ইয়া", "িয়া"), "ea": ("ইয়া", "িয়া"),
}
TA_CONS = {
    "k": "க", "kh": "க", "g": "க", "gh": "க", "ch": "ச", "j": "ஜ", "jh": "ஜ",
    "t": "ட", "th": "த", "d": "ட", "dh": "த", "n": "ன", "p": "ப", "ph": "ப",
    "f": "ஃப", "b": "ப", "bh": "ப", "m": "ம", "y": "ய", "r": "ர", "l": "ல",
    "v": "வ", "w": "வ", "sh": "ஷ", "s": "ஸ", "h": "ஹ", "z": "ஸ", "c": "க",
    "q": "க", "x": "க்ஸ",
}
TA_VOWEL = {
    "a": ("அ", ""), "aa": ("ஆ", "ா"), "i": ("இ", "ி"), "ee": ("ஈ", "ீ"),
    "u": ("உ", "ு"), "oo": ("ஊ", "ூ"), "e": ("எ", "ெ"), "ai": ("ஐ", "ை"),
    "o": ("ஒ", "ொ"), "au": ("ஔ", "ௌ"), "ia": ("இயா", "ியா"), "ea": ("இயா", "ியா"),
}


def _abugida(token, cons, vowels, virama, final_virama=False):
    t = _fold(token)
    out, i, after_cons = [], 0, False
    while i < len(t):
        two = t[i:i + 2]
        if two in vowels:
            ind, matra = vowels[two]
            out.append(matra if after_cons else ind)
            i, after_cons = i + 2, False
            continue
        if len(two) == 2 and two in cons:
            if after_cons:
                out.append(virama)
            out.append(cons[two])
            i, after_cons = i + 2, True
            continue
        ch = t[i]
        # `y` is a vowel unless a vowel follows it: `Sylvi`, but `Maya`.
        if ch == "y" and not (i + 1 < len(t) and t[i + 1] in "aeiou"):
            ch = "i"
        if ch in vowels:
            ind, matra = vowels[ch]
            out.append(matra if after_cons else ind)
            after_cons = False
        elif ch in cons:
            if after_cons:
                out.append(virama)
            out.append(cons[ch])
            after_cons = True
        i += 1
    if final_virama and after_cons:
        out.append(virama)
    return "".join(out)


def to_bn(token):
    return _abugida(token, BN_CONS, BN_VOWEL, "্")


def to_ta(token):
    return _abugida(token, TA_CONS, TA_VOWEL, "்", final_virama=True)


# ---------------------------------------------------------------------------------------
# The syllabaries. A sign is a whole (consonant, vowel) syllable, so the Latin is first cut
# into syllables over a small canonical inventory, and each engine maps that inventory onto
# the consonants its script has. A doubled consonant is one: none of the four writes length.
_SYL_CONS = ("sch", "sh", "ch", "zh", "kh", "gh", "th", "ph", "ts", "tz", "ck", "qu", "ng",
             "b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t",
             "v", "w", "x", "y", "z")
_CANON = {"sch": "sh", "tz": "ts", "ck": "k", "c": "k", "q": "k", "kh": "h", "gh": "g",
          "th": "t", "ph": "f", "zh": "z", "qu": "kw"}


def _syllables(token):
    """`[(consonant or "", vowel or "")]` -- `Arne` -> `[("", "a"), ("r", ""), ("n", "e")]`."""
    t = _fold(token).replace("-", "").replace("'", "")
    out, i = [], 0
    while i < len(t):
        c = next((cand for cand in _SYL_CONS if t.startswith(cand, i)), "")
        # `y` is a vowel unless another vowel follows it: `Sylvi`, but `Yngve` and `Maya`.
        if c == "y" and not (i + 1 < len(t) and t[i + 1] in "aeiou"):
            c = ""
        if c:
            i += len(c)
            c = _CANON.get(c, c)
            if c == "x":
                out.append(("k", ""))
                c = "s"
            if out and out[-1] == (c, ""):
                out.pop()
        v = ""
        if i < len(t) and t[i] in "aeiouy":
            v = "i" if t[i] == "y" else t[i]
            i += 1
            while i < len(t) and t[i] == v:
                i += 1
        if c or v:
            out.append((c, v))
        elif i < len(t):
            i += 1
    return out


# Cherokee. Six vowels a e i o u v; the `v` column stands in for a consonant with no vowel
# after it. Cherokee has no b, p, f, r or consonantal v, so those take the nearest row it has.
CHR = {
    "": "ᎠᎡᎢᎣᎤᎥ", "g": "ᎦᎨᎩᎪᎫᎬ", "k": "ᎧᎨᎩᎪᎫᎬ", "h": "ᎭᎮᎯᎰᎱᎲ",
    "l": "ᎳᎴᎵᎶᎷᎸ", "m": "ᎹᎺᎻᎼᎽᎽ", "n": "ᎾᏁᏂᏃᏄᏅ", "kw": "ᏆᏇᏈᏉᏊᏋ",
    "s": "ᏌᏎᏏᏐᏑᏒ", "d": "ᏓᏕᏗᏙᏚᏛ", "t": "ᏔᏖᏘᏙᏚᏛ", "ts": "ᏣᏤᏥᏦᏧᏨ",
    "w": "ᏩᏪᏫᏬᏭᏮ", "y": "ᏯᏰᏱᏲᏳᏴ",
}
CHR_ROW = {"b": "kw", "p": "kw", "f": "w", "v": "w", "r": "l", "j": "y", "z": "s",
           "sh": "s", "ch": "ts", "ng": "n"}


def to_chr(token):
    out = []
    for c, v in _syllables(token):
        if c == "s" and not v:
            out.append("Ꮝ")
            continue
        row = CHR.get(CHR_ROW.get(c, c), CHR["k"] if c else CHR[""])
        out.append(row["aeiou".index(v)] if v else row[5])
    return "".join(out)


# Inuktitut syllabics. Three vowels, a i u, with `e` read as i and `o` as u, as Inuktitut
# spells loanwords. A consonant with no vowel takes its small final.
IU = {
    "": ("ᐊ", "ᐃ", "ᐅ", ""), "p": ("ᐸ", "ᐱ", "ᐳ", "ᑉ"), "t": ("ᑕ", "ᑎ", "ᑐ", "ᑦ"),
    "k": ("ᑲ", "ᑭ", "ᑯ", "ᒃ"), "g": ("ᒐ", "ᒋ", "ᒍ", "ᒡ"), "m": ("ᒪ", "ᒥ", "ᒧ", "ᒻ"),
    "n": ("ᓇ", "ᓂ", "ᓄ", "ᓐ"), "s": ("ᓴ", "ᓯ", "ᓱ", "ᔅ"), "l": ("ᓚ", "ᓕ", "ᓗ", "ᓪ"),
    "y": ("ᔭ", "ᔨ", "ᔪ", "ᔾ"), "v": ("ᕙ", "ᕕ", "ᕗ", "ᕝ"), "r": ("ᕋ", "ᕆ", "ᕈ", "ᕐ"),
    "ng": ("ᖓ", "ᖏ", "ᖑ", "ᖕ"), "h": ("ᕼᐊ", "ᕼᐃ", "ᕼᐅ", "ᕼ"),
}
IU_ROW = {"b": "p", "d": "t", "f": "v", "w": "v", "j": "y", "z": "s", "sh": "s",
          "ch": "s", "ts": "s", "kw": "k"}
IU_VOWEL = {"a": 0, "e": 1, "i": 1, "o": 2, "u": 2}


def to_iu(token):
    out = []
    for c, v in _syllables(token):
        row = IU.get(IU_ROW.get(c, c), IU["k"] if c else IU[""])
        out.append(row[IU_VOWEL[v]] if v else row[3])
    return "".join(out)


# Ge'ez, as Amharic writes it. Seven orders a row: ä u i a e (sixth: no vowel) o. A foreign `a`
# takes the fourth order, which is how Amharic spells Maria and Anna. Latin `j` in these names is
# the /j/ glide, which is Ge'ez `y`, not `j` (/dʒ/).
AM = {
    "": "አኡኢኣኤእኦ", "h": "ሀሁሂሃሄህሆ", "l": "ለሉሊላሌልሎ", "m": "መሙሚማሜምሞ",
    "r": "ረሩሪራሬርሮ", "s": "ሰሱሲሳሴስሶ", "sh": "ሸሹሺሻሼሽሾ", "k": "ከኩኪካኬክኮ",
    "b": "በቡቢባቤብቦ", "v": "ቨቩቪቫቬቭቮ", "t": "ተቱቲታቴትቶ", "ch": "ቸቹቺቻቼችቾ",
    "n": "ነኑኒናኔንኖ", "w": "ወዉዊዋዌውዎ", "z": "ዘዙዚዛዜዝዞ", "y": "የዩዪያዬይዮ",
    "d": "ደዱዲዳዴድዶ", "g": "ገጉጊጋጌግጎ", "f": "ፈፉፊፋፌፍፎ", "p": "ፐፑፒፓፔፕፖ",
    "ts": "ጸጹጺጻጼጽጾ",
}
AM_ROW = {"ng": "n", "kw": "k", "j": "y"}
AM_ORDER = {"a": 3, "u": 1, "i": 2, "e": 4, "o": 6}


def to_am(token):
    out = []
    for c, v in _syllables(token):
        row = AM.get(AM_ROW.get(c, c), AM["k"] if c else AM[""])
        out.append(row[AM_ORDER[v]] if v else row[5])
    return "".join(out)


# Thaana (Maldivian). Every letter carries a vowel sign (fili) or the sukun; a vowel with no
# consonant rides on the alifu.
DV_CONS = {"h": "ހ", "sh": "ށ", "n": "ނ", "r": "ރ", "b": "ބ", "k": "ކ", "": "އ", "v": "ވ",
           "m": "މ", "f": "ފ", "t": "ތ", "l": "ލ", "g": "ގ", "s": "ސ", "d": "ދ", "z": "ޒ",
           "y": "ޔ", "j": "ޔ", "p": "ޕ", "ch": "ޗ", "w": "ވ", "ts": "ތސ", "ng": "ނގ",
           "kw": "ކވ"}
DV_FILI = {"a": "ަ", "i": "ި", "u": "ު", "e": "ެ", "o": "ޮ"}
DV_SUKUN = "ް"


def to_dv(token):
    out = []
    for c, v in _syllables(token):
        base = DV_CONS.get(c, DV_CONS["k"])
        # a two-letter consonant gets the sukun on its first letter
        if len(base) > 1:
            base = base[0] + DV_SUKUN + base[1:]
        out.append(base + (DV_FILI[v] if v else DV_SUKUN))
    return "".join(out)


SCRIPTS.update({"uk": to_uk, "fa": to_fa, "bn": to_bn, "he": to_he, "ta": to_ta,
                "chr": to_chr, "iu": to_iu, "am": to_am, "dv": to_dv, "hy": to_hy,
                "ka": to_ka, "zgh": to_zgh})
_CASED |= {"uk", "hy"}


def render(name, code):
    """A whole name, token by token, joined with ordinary spaces.

    **Proper names are capitalised in Cyrillic and Greek.** The per-letter tables work in
    lower case, so without this every Russian and Greek label came out `арне гарборг`
    rather than `Арне Гарборг` -- which is not how a name is written in either language
    and reads as an error to anybody who has one.
    """
    fn = SCRIPTS[code]
    out = []
    for token in str(name).split():
        low = token.lower()
        for a, b in _CLUSTERS:
            low = low.replace(a, b)
        got = fn(low)
        if not got:
            continue
        out.append(got[0].upper() + got[1:] if code in _CASED else got)
    return " ".join(out)


if __name__ == "__main__":
    import sys
    names = sys.argv[1:] or ["Arne Garborg", "Ole Hansen", "Bjørn Åsulvsson",
                             "Maria Elisabet Wærn", "Johannes Bureus"]
    for n in names:
        print(n)
        for code in SCRIPTS:
            print("   %s  %s" % (code, render(n, code)))
