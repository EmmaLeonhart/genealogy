"""Latin names into Cyrillic, Greek, Devanagari and Arabic.

Emma's seven languages are `en` · `ja` · `zh` · `hi` · `ar` · `ru` · `el` plus `mul`. `ja`/`zh`
are `scripts/translit_no.py`; this is the other four, authorised 2026-08-31 to run in parallel
rather than behind them.

**Her standard governs and is the reason this is allowed to exist:** *"Incorrect romanization or
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
#: them the vowel-dropping rule reduced her to `مرا`, which has lost the name rather than its
#: short vowels, and that is the line her standard actually draws.
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
        for code in ("ru", "el", "hi", "ar"):
            print("   %s  %s" % (code, render(n, code)))
