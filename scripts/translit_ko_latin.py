"""Latin names to Hangul — the other half of Korean, and the half the creation gate needs.

`translit_ko.py` reads Han characters. That covers the 46,452 people with a CJK name and none of
the 1.39 million with a Latin one — including every person the Garborg ring creates. The creation
gate is `ja` + `zh` + `ko` now, and `ja`/`zh` reach Latin names through `translit_no`, so `ko`
needs the same road.

**Emma's standard, which is what makes a rule-based rendering acceptable at all:** *"incorrect
romanization or incorrect representations in katakana are totally acceptable. An incorrect name is
not."* A Hangul spelling of `Garborg` may not be the one a Korean newspaper would choose; it is
still that person's name, written in Korean letters. Inventing a different *name* is the thing
that is forbidden, and nothing here does that.

## How Hangul is built, which is why this is composition and not a lookup

A Hangul syllable is a single code point computed from three slots:

    U+AC00 + (initial * 21 + vowel) * 28 + final

19 initial consonants, 21 vowels, 28 finals (index 0 being *no final*). So the renderer's job is
to turn a Latin word into a sequence of (initial, vowel, final) triples and compose them. That is
also why the vowel is mandatory: Korean has no bare consonant syllable, and a consonant with
nothing to attach to takes **으**, which is the standard epenthetic vowel in 외래어 표기법 (the
loanword transcription rules). `Garborg` therefore comes out 가르보르그 rather than anything
shorter — the trailing `g` gets its own syllable.

## What is deliberately NOT attempted

**No language guessing.** `CLAUDE.md` bans inferring a language or a region from a name, so the
same table is applied whatever the name looks like. A Norwegian `Bjørn` and a French `Bernard` go
through identical rules.

**No silent partial output.** One unrenderable character returns `''`, per the rule in `CLAUDE.md`
§ *A middle initial keeps its Latin letter in every language*: an unknown name blocks the whole
label, because half a name is worse than none. A middle initial is the single exception there and
is handled by the caller, not here.
"""

from __future__ import annotations

import re
import unicodedata

_BASE = 0xAC00

#: The 19 initial consonants (초성), in Unicode order.
_INITIALS = ["g", "kk", "n", "d", "tt", "r", "m", "b", "pp", "s", "ss",
             "", "j", "jj", "ch", "k", "t", "p", "h"]
_I = {name: i for i, name in enumerate(_INITIALS)}

#: The 21 vowels (중성), in Unicode order.
_VOWELS = ["a", "ae", "ya", "yae", "eo", "e", "yeo", "ye", "o", "wa", "wae",
           "oe", "yo", "u", "wo", "we", "wi", "yu", "eu", "ui", "i"]
_V = {name: i for i, name in enumerate(_VOWELS)}

#: The 28 finals (종성); index 0 is "no final consonant".
_FINALS = ["", "g", "kk", "gs", "n", "nj", "nh", "d", "l", "lg", "lm", "lb",
           "ls", "lt", "lp", "lh", "m", "b", "bs", "s", "ss", "ng", "j",
           "ch", "k", "t", "p", "h"]
_F = {name: i for i, name in enumerate(_FINALS)}

#: Only these consonants may sit in the final slot of a loanword syllable. Anything else takes
#: its own syllable with the epenthetic vowel 으, which is what makes `Garborg` four syllables.
_CAN_BE_FINAL = {"g", "n", "l", "m", "b", "ng"}   # note: "r_" is deliberately absent

#: A stop before a liquid does NOT close the syllable -- 외래어 표기법 gives it 으.
#: `Sigrid` is 시그리드, not 식리드, and the same applies to `Ingrid` and every -gr-,
#: -br- and -dr- cluster, which are common in this corpus.
_STOPS = {"g", "b", "d", "k", "t", "p"}
_LIQUIDS = {"r_", "l"}

#: Latin letter (or digraph) to the Korean consonant it transcribes as.
_CONS = {
    "b": "b", "c": "k", "d": "d", "f": "p", "g": "g", "h": "h", "j": "j",
    "k": "k", "l": "l", "m": "m", "n": "n", "p": "p", "q": "k", "r": "r_",
    "s": "s", "t": "t", "v": "b", "w": "w", "x": "ks", "y": "y", "z": "j",
    "ç": "s", "ć": "ch", "č": "ch", "ď": "d", "ğ": "g", "ł": "l", "ń": "n",
    "ñ": "n", "ň": "n", "ř": "l", "ś": "s", "š": "s", "ş": "s", "ť": "t",
    "ż": "j", "ź": "j", "ž": "j", "ķ": "k", "ļ": "l", "ņ": "n", "ģ": "g",
    "þ": "t", "ð": "d", "ß": "s",
    # Digraphs, longest first when matching.
    "ch": "ch", "sh": "s", "th": "t", "ph": "p", "kh": "k", "gh": "g",
    "ck": "k", "ng": "ng", "qu": "kw", "ts": "ch", "sch": "s", "sz": "s",

    "cz": "ch", "rz": "j", "zh": "j", "kj": "k", "gj": "g", "sj": "s",
    "skj": "s", "hj": "h", "lj": "l", "nj": "n", "dj": "j", "tj": "ch",
}

#: Latin vowel (or digraph) to the Korean vowel it transcribes as. Nordic vowels are here
#: because this corpus is overwhelmingly Norwegian and Swedish and they are not decoration:
#: `ø` and `å` appear in tens of thousands of names.
_VOW = {
    "a": "a", "e": "e", "i": "i", "o": "o", "u": "u", "y": "i",
    "á": "a", "à": "a", "â": "a", "ä": "e", "å": "o", "æ": "ae",
    "é": "e", "è": "e", "ê": "e", "ë": "e",
    "í": "i", "ì": "i", "î": "i", "ï": "i",
    "ó": "o", "ò": "o", "ô": "o", "ö": "oe", "ø": "oe", "õ": "o",
    "ú": "u", "ù": "u", "û": "u", "ü": "wi", "ý": "i",
    # Letters the first pass missed, found by reading the tokens that rendered as nothing.
    "ã": "a", "ą": "a", "ā": "a", "ă": "a", "ǎ": "a",
    "ē": "e", "ě": "e", "ę": "e", "ė": "e",
    "ī": "i", "į": "i", "ı": "i",
    "ō": "o", "ǫ": "o", "ő": "o", "œ": "oe",
    "ū": "u", "ų": "u", "ů": "u", "ű": "wi",
    "ÿ": "i", "ỳ": "i",
    # Digraphs.
    "ae": "ae", "oe": "oe", "ei": "ei", "ai": "ai", "au": "au", "ou": "u", "eo": "eo", "ea": "ea", "ie": "ie", "oa": "oa",
    "ee": "i", "oo": "u", "eu": "yu", "iu": "yu", "ua": "wa", "ue": "we", "ui": "wi", "uo": "wo",
    "yu": "yu", "ya": "ya", "yo": "yo", "ye": "ye",
}

#: Vowel sequences that are two Korean vowels rather than one, so they become two syllables.
#: Vowel pairs that are two Korean vowels. `ie`, `ea`, `eo`, `ia` and `io` were single
#: vowels until 2026-09-01 and produced `Leonhart` -> 런할트; in a personal name they are
#: almost always two syllables, so they split.
_SPLIT_VOWEL = {"ei": ("e", "i"), "ai": ("a", "i"), "au": ("a", "u"),
                "ia": ("i", "a"), "io": ("i", "o"), "ie": ("i", "e"),
                "ea": ("e", "a"), "eo": ("e", "o"), "oa": ("o", "a")}


#: **The same consonant is named differently in the two slots.** U+3139 is `r` in the initial
#: list and `l` in the final list -- one letter, two names -- and mapping `r`/`l` to "l" without
#: translating for the initial slot made every name containing an R or an L render as nothing.
#: `Arne`, `Karl`, `Leonhart` and `Bureus` all failed on this alone.
#: `r` and `l` are ONE Korean letter and two different behaviours. An `l` before a
#: consonant closes the syllable -- `Karl` is 칼 -- while an `r` there opens its own
#: with 으, per 외래어 표기법: `Arne` is 아르네, not 알네. Treating both as "l" gave the
#: wrong one for every R in the corpus, which is most Norwegian surnames.
_INITIAL_ALIAS = {"l": "r", "r_": "r",
                  # `ng` can only CLOSE a Korean syllable, never open one -- the initial
                  # slot for that letter is silent. Without this, a word whose `ng`
                  # had no preceding vowel to attach to (`-Kalingga`) rendered as
                  # nothing at all.
                  "ng": ""}


def _compose(initial, vowel, final=""):
    """One Hangul syllable from its three slots, or `''` if any slot is unknown."""
    initial = _INITIAL_ALIAS.get(initial, initial)
    if initial not in _I or vowel not in _V or final not in _F:
        return ""
    return chr(_BASE + (_I[initial] * 21 + _V[vowel]) * 28 + _F[final])


def _tokens(word):
    """`word` split into consonant and vowel units, longest match first, or `None`."""
    out, i = [], 0
    keys = sorted(set(_CONS) | set(_VOW), key=len, reverse=True)
    while i < len(word):
        for k in keys:
            if word.startswith(k, i):
                out.append(("V", _VOW[k]) if k in _VOW else ("C", _CONS[k]))
                i += len(k)
                break
        else:
            return None
    return out


def render_word(word):
    """Hangul for one Latin word, or `''` when a character cannot be transcribed."""
    word = word.strip().lower()
    if not word:
        return ""
    # Strip combining marks the tables do not name, but keep the precomposed Nordic letters,
    # which ARE named -- `CLAUDE.md`: a diacritic makes a different name and is not folded away.
    word = "".join(c for c in word if not unicodedata.combining(c))
    # **Punctuation is dropped, not refused.** 716 of the 18,536 tokens in the shared table had
    # no Korean reading and every one was Latin: `.Peder`, `A.B.D.`, `'Sans-Peur'`, `-Kalingga`.
    # `ja` and `zh` render all of them, because their engine strips punctuation and this one
    # rejected the whole token on it -- so the gap was never about Korean at all.
    word = "".join(c for c in word if c.isalpha())
    if not word:
        return ""
    # **`chr` is a hard k followed by an r, not the `ch` digraph.** Mapping the cluster
    # to a single consonant swallowed the r and gave `Christina` -> 키스티나; rewriting it
    # to `kr` before tokenising gives 크리스티나. `Christian`, `Christoffer` and `Christen`
    # are a large family of names here, so this is not one word.
    word = word.replace("chr", "kr").replace("sch", "sh")
    # `rl` is one Korean letter twice over. `Karlsson` came out 카르르손 -- the r took its
    # own epenthetic syllable and the l then started another. Collapsed, it is 칼손, and
    # `Karl` stays 칼.
    word = word.replace("rl", "l")
    # **A doubled consonant behaves two different ways and collapsing all of them was wrong.**
    # A doubled STOP or sibilant is written once -- `Svensson` is 스벤손, `Hansdotter` 한스도테르 --
    # while a doubled LIQUID or NASAL keeps both, the first closing the syllable: `Lilly` is 릴리
    # and `Heller` 헬레르. Collapsing everything gave 리리 and 헤레르; keeping everything gave
    # 한스도트테르.
    word = re.sub(r"([bcdfgkpqstvxz])\1", r"\1", word)
    units = _tokens(word)
    if not units:
        return ""

    out, i = [], 0
    while i < len(units):
        kind, value = units[i]
        if kind == "V":
            pieces = _SPLIT_VOWEL.get(value, (value,))
            for v in pieces:
                if v not in _V:
                    return ""
            # A syllable with no initial consonant still has a final slot. Without this,
            # `Emma` came out 에므마 instead of 엠마 -- the M had nowhere to attach and took
            # its own epenthetic syllable.
            final = ""
            j = i + 1
            if j < len(units) and units[j][0] == "C":
                c = units[j][1]
                after = units[j + 1] if j + 1 < len(units) else None
                if c in _CAN_BE_FINAL and not (after and after[0] == "V"):
                    final = c
                    j += 1
            # The final belongs to the LAST piece. Attaching it only when the vowel did not
            # split gave `Leonhart` -> 레오느하르트 and `Tunheim` -> 툰헤이므, because `eo` and
            # `ei` are two vowels and the N and the M then had nowhere to go.
            for k, v in enumerate(pieces):
                out.append(_compose("", v, final if k == len(pieces) - 1 else ""))
            i = j
            continue
        # A consonant. Take the following vowel if there is one, else the epenthetic 으.
        initial = value
        if initial == "w":
            # `w` is not an initial consonant in Korean; it lives in the vowel. `wa`, `we`...
            nxt = units[i + 1] if i + 1 < len(units) else None
            if nxt and nxt[0] == "V":
                merged = "w" + nxt[1]
                if merged in _V:
                    out.append(_compose("", merged))
                    i += 2
                    continue
            out.append(_compose("", "u"))
            i += 1
            continue
        if initial == "y":
            nxt = units[i + 1] if i + 1 < len(units) else None
            if nxt and nxt[0] == "V":
                merged = "y" + nxt[1]
                if merged in _V:
                    out.append(_compose("", merged))
                    i += 2
                    continue
            out.append(_compose("", "i"))
            i += 1
            continue
        if initial == "ks":
            # `x`. Two consonants: a final `g` if it can attach, then `s`.
            initial = "g"
            units = units[:i] + [("C", "g"), ("C", "s")] + units[i + 1:]
            continue
        if initial == "kw":
            units = units[:i] + [("C", "k"), ("C", "w")] + units[i + 1:]
            continue
        if _INITIAL_ALIAS.get(initial, initial) not in _I:
            return ""
        nxt = units[i + 1] if i + 1 < len(units) else None
        if nxt and nxt[0] == "V":
            vowel = nxt[1]
            for v in _SPLIT_VOWEL.get(vowel, (vowel,)):
                if v not in _V:
                    return ""
            first = _SPLIT_VOWEL.get(vowel, (vowel,))[0]
            rest = _SPLIT_VOWEL.get(vowel, (vowel,))[1:]
            # A following consonant becomes this syllable's final when it legally can and is
            # not itself followed by a vowel -- otherwise it starts the next syllable.
            final = ""
            j = i + 2
            if j < len(units) and units[j][0] == "C":
                c = units[j][1]
                after = units[j + 1] if j + 1 < len(units) else None
                if (c in _CAN_BE_FINAL and not (after and after[0] == "V")
                        and not (c in _STOPS and after and after[1] in _LIQUIDS)):
                    final = c
                    j += 1
            pieces = (first,) + tuple(rest)
            for k, v in enumerate(pieces):
                syl = (_compose(initial, v, final if k == len(pieces) - 1 else "") if k == 0
                       else _compose("", v, final if k == len(pieces) - 1 else ""))
                if not syl:
                    return ""
                out.append(syl)
            i = j
            continue
        # No vowel follows: the consonant takes 으.
        syl = _compose(initial, "eu")
        if not syl:
            return ""
        out.append(syl)
        i += 1
    return "".join(out) if all(out) else ""


def render(name):
    """Hangul for a whole Latin name, or `''` when any word cannot be transcribed."""
    name = (name or "").strip()
    if not name:
        return ""
    words = []
    for word in name.split():
        got = render_word(word)
        if not got:
            return ""
        words.append(got)
    return " ".join(words)


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    for probe in ("Arne Garborg", "Empress Jingū", "Bjørn Olsen", "Aagot Nyvold",
                  "Johannes Bureus", "Karl Gustav", "Sigrid Tunheim", "Per Nilsson"):
        print(f"{probe:<22} -> {render(probe)!r}")
