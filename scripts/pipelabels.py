"""Read a `|` in an imported label. `name modelling.txt` is the authority for every rule here.

1,640 imported labels carry a pipe and they were never one question. Three shapes, ruled
separately on 2026-09-09, and the bracketed one has fourteen situations of its own.

    1,372   Mary|Maria Butler            two given names, one surname
      136   Daniel Tichenor|Titchenal    the pipe inside one name, nothing anchoring it
      132   Ann Bincks (Benckes|Bench)   a bracketed variant group

`read(text)` returns `Reading(mul, en, aliases, note)`. `en` is `None` unless it differs from
`mul`, which happens only where a comma phrase is carried.

## ⛔ THE DISCRIMINATOR BETWEEN THE FIRST TWO SHAPES IS WHETHER THE RIGHT SIDE HAS A SPACE

`Mary|Maria Butler` splits at the TOKEN: the pipe offers two given names and `Butler` is shared,
so both alternatives keep the surname. `Daniel Tichenor|Titchenal` splits the WHOLE STRING: the
label is `Daniel Tichenor` and the alias is the bare `Titchenal`.

**That difference is the ruling, not an inference.** The consequence was put up before the second
was decided -- *"an alias missing its given name"* -- and taken anyway. The two shapes were
counted and ruled as separate populations by exactly this test: 1,372 where the text after the
pipe group contains a space, 136 where it does not.

## THE BRACKET RULES, in the order they are applied

    negation      `(not Cecily)` is a description marker: dropped, and never emitted as an alias
    comma tail    `, of Norbury` stays in `en` and never enters `mul`. THE COMMA IS THE TELL --
                  an un-comma'd `of X` is part of the name and stays in both
    square        `[Husu]` reads as an ordinary bracket
    slots         every alternative in every slot, multiplied out; the first of each is the label

## HOW A BRACKET BINDS, which is the only part that needed working out

A bracket group is either a REPLACEMENT for the token in front of it or a SLOT OF ITS OWN, and
the ruled outputs settle which:

    Ann Bincks (Benckes|Bench)              -> Ann Benckes      REPLACES `Bincks`
    Purcirto (Artinide|Hartneid) de Attems  -> Purcirto Artinide de Attems   INSERTS
    Kone (|Kunigunda) of (Hastevere)        -> Kunigunda of Hastevere        REPLACES `Kone`

So: a bracket at the END of the name replaces what precedes it, a bracket with an EMPTY first
alternative replaces what precedes it wherever it sits, and any other bracket is its own slot.
The empty alternative is what `(|Kunigunda)` means -- *this token, or Kunigunda* -- and it is the
reason that row could be ruled at all.
"""

from __future__ import annotations

import itertools
import re


#: `(not Cecily)`, and only this shape. A description marker comes out of the label; a title
#: stays in it. Nothing else in the 132 is a negation and nothing here guesses at one.
NEGATION = re.compile(r"\s*\(\s*not\s+[^)]*\)", re.I)

#: A bracket group carrying alternatives. Square brackets read as round ones -- ruled on
#: `(Teppana|Tahvana) of [Husu]`, the only row in the corpus that uses them.
BRACKET = re.compile(r"[(\[]([^)\]]*)[)\]]")

#: A comma phrase at the very end: `, of Norbury`, `, Heiress of Giffords Hall`. It is a byname
#: or a title and it belongs in `en` alone.
COMMA_TAIL = re.compile(r",\s*([^,]+)$")


class Reading:
    """What a piped label becomes. `en` is None when it is the same string as `mul`.

    ⛔ **A PLAIN CLASS, NOT A `@dataclass`, AND THAT IS NOT A STYLE CHOICE.** Every script in
    this repo is loaded by path -- the filenames have hyphens and are not importable -- and
    `dataclasses` resolves annotations through `sys.modules[cls.__module__]`, which is `None`
    for a module loaded that way. The decorator raises `AttributeError: 'NoneType' object has
    no attribute '__dict__'` before a single test runs.
    """

    def __init__(self, mul, en=None, aliases=None, note=""):
        self.mul = mul
        self.en = en
        self.aliases = list(aliases or [])
        self.note = note

    def labels(self):
        return [self.mul] + self.aliases

    def __repr__(self):
        return "Reading(mul=%r, en=%r, aliases=%r)" % (self.mul, self.en, self.aliases)


def _clean(text: str) -> str:
    return " ".join((text or "").split())


def _expand(slots: list[list[str]]) -> list[str]:
    """Every combination, first-of-each first.

    ⛔ **THE CROSS PRODUCT IS THE RULING FOR SHAPE B** -- `Judith|Godith Bosom (Bozon|Bosun)`
    gives all six, not four. `itertools.product` walks the last slot fastest and the first
    combination is every slot's first alternative, which is exactly the label.
    """
    out = []
    for combination in itertools.product(*slots):
        rendered = _clean(" ".join(part for part in combination if part))
        if rendered and rendered not in out:
            out.append(rendered)
    return out


def _slots(text: str) -> list[list[str]]:
    """The name as a list of slots, each holding its alternatives in ruled order."""
    slots: list[list[str]] = []
    position = 0
    for match in BRACKET.finditer(text):
        before = text[position:match.start()]
        variants = [_clean(v) for v in match.group(1).split("|")]
        # a bracket with no pipe is not a variant group at all -- `(Hastevere)` is just the word
        if len(variants) == 1:
            slots.extend(_pipe_slots(before + " " + variants[0]))
            position = match.end()
            continue
        tail = text[match.end():].strip()
        empty_first = variants[0] == ""
        at_end = tail == "" or tail.startswith(",")
        words = before.split()
        if (at_end or empty_first) and words:
            # REPLACES the token in front of it: that token becomes the first alternative
            slots.extend(_pipe_slots(" ".join(words[:-1])))
            alternatives = [words[-1]] + [v for v in variants if v]
            slots.append(alternatives)
        else:
            slots.extend(_pipe_slots(before))
            slots.append([v for v in variants if v])
        position = match.end()
    slots.extend(_pipe_slots(text[position:]))
    return [s for s in slots if s]


def _pipe_slots(text: str) -> list[list[str]]:
    """Plain text outside any bracket, split into slots on a bare `|`.

    `Judith|Godith Bosom` is the slot `[Judith, Godith]` followed by `Bosom`: the pipe binds to
    the token on each side of it and nothing further.
    """
    text = _clean(text)
    if not text:
        return []
    if "|" not in text:
        return [[word] for word in text.split()]
    out: list[list[str]] = []
    for chunk in re.split(r"(\S*\|\S*)", text):
        chunk = _clean(chunk)
        if not chunk:
            continue
        if "|" in chunk:
            out.append([c for c in (x.strip() for x in chunk.split("|")) if c])
        else:
            out.extend([[word] for word in chunk.split()])
    return out


#: Anything a finished label must never still contain. A leftover pipe or bracket means the
#: string was not understood, and emitting it would put punctuation on Wikidata.
UNRESOLVED = re.compile(r"[|()\[\]]")


def read(text: str) -> Reading:
    """Apply the rulings to one imported label, or refuse and say so.

    ⛔ **A LABEL THAT STILL CARRIES A BRACKET OR A PIPE IS HELD, NEVER EMITTED.** Measured over
    all 1,640: exactly one row survives every rule with punctuation still in it, `Q99707312`
    `Alice Willisham (Wellasham|Wyllasham` -- an **unclosed bracket**, which is a fifteenth
    situation nobody ruled on. Without this guard it emits `Alice Willisham (Wellasham`, a label
    with half a bracket, and it looks like a success in every count.

    The other 1,639 are unaffected: the guard fires on output, not on input, so it cannot change
    a reading that already resolved.
    """
    original = _clean(text)
    if "|" not in original:
        return Reading(mul=original, note="no pipe")

    working = _clean(NEGATION.sub("", original))
    note = "negation dropped" if working != original else ""

    tail = ""
    match = COMMA_TAIL.search(working)
    if match:
        tail = _clean(match.group(1))
        working = _clean(working[:match.start()])

    if not BRACKET.search(working):
        return _plain_pipe(working, tail, note)

    names = _expand(_slots(working))
    return _finish(names, original, tail, _clean(f"{note} bracket".strip()))


def _plain_pipe(text: str, tail: str, note: str) -> Reading:
    """Shapes one and two: a pipe with no bracket anywhere.

    ⛔ **THE SPACE ON THE RIGHT IS THE WHOLE DISCRIMINATOR.** With one, the pipe offers two
    given names over a shared surname and both alternatives keep it. Without one, the string is
    split whole and the alias is bare -- ruled with that consequence stated.
    """
    head, _, rest = text.partition("|")
    if " " in rest.strip():
        names = _expand(_slots(text))
        shape = "two given names"
    else:
        names = [_clean(head)] + [_clean(part) for part in rest.split("|")]
        names = [n for i, n in enumerate(names) if n and n not in names[:i]]
        shape = "whole-string split"
    return _finish(names, text, tail, _clean(f"{note} {shape}".strip()))

def _finish(names, original, tail, note):
    """The one exit. Refuses anything still carrying punctuation -- see `read`."""
    if not names:
        return Reading(mul=original, note="HELD: nothing readable")
    unresolved = [n for n in names if UNRESOLVED.search(n)]
    if unresolved:
        return Reading(mul=original,
                       note="HELD: unresolved punctuation in %r" % unresolved[0])
    mul = names[0]
    return Reading(mul=mul,
                   en=_clean("%s, %s" % (mul, tail)) if tail else None,
                   aliases=names[1:],
                   note=note)


def statements(qid, reading):
    """The reading as QuickStatements rows, in protocol form.

    ⛔ **`mul` IS THE LABEL AND EVERY ALTERNATIVE IS AN `Amul`.** `CLAUDE.md` § *The MARRIED name
    is the real name*: `mul` carries the real name and the others go on as `Amul` aliases,
    **never as an `Aen`**. A variant spelling is not an English fact, it is another way the same
    person's name is written, so it belongs in the language-neutral slot beside the label.

    `Len` is emitted ONLY where the comma tail makes English differ from `mul` -- 34 rows of the
    1,640. Everywhere else English inherits `mul` and writing it again would be a second copy
    that can drift.

    ⛔ **A HELD READING EMITS NOTHING.** `read` refuses anything still carrying a bracket or a
    pipe, and this must not paper over that by writing the raw string as a label.
    """
    if not reading.mul or reading.note.startswith("HELD"):
        return []
    rows = [(qid, "Lmul", reading.mul)]
    if reading.en and reading.en != reading.mul:
        rows.append((qid, "Len", reading.en))
    for alias in reading.aliases:
        rows.append((qid, "Amul", alias))
    return rows


def render(rows):
    """QuickStatements text. Values are quoted; nothing here can contain a quote."""
    return "".join('%s\t%s\t"%s"\n' % row for row in rows)
