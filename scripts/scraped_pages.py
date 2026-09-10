"""Read the immediate family out of a saved Geni profile page.

**The 1,555 pages in `geni-scraping/` and the 698 files in `paths/` become GEDCOMs.** They go
into a special GEDCOM directory, saving both the paths and the saved pages, which are different
things. That turns them into something usable, merged into the Geni union — the synoptic tree —
as ordinary GEDCOM content.

**What a saved page actually carries.** Not a structured family list -- prose with links:

    <a data-profile-id="...">Brita Henriksdotter Uddman</a> <br>
    Wife of <a data-profile-id="...">Isak Henricsson Peldan</a> and <a ...>Johan Mathesius</a> <br>
    Mother of <a data-profile-id="...">Brita Helena Peldan</a> ...

So every edge is an English phrase followed by the anchors it governs, and the anchors carry the
Geni id. That is what makes this an exact join rather than a name match, which is the same reason
`genimerge.genipage` reads the relationship panel from `href`s instead of from the visible text.

**Names arrive as one string and stay that way**, and that cost is accepted deliberately:
names present as strings make things significantly harder, and the alternative is guessing the
surname from spacing, which works in most cases and not all. This module therefore emits `1 NAME <string>` and **no `GIVN`/`SURN` split at all** --
guessing a surname from spacing is exactly the fuzzy inference this repo refuses everywhere else,
and `reports/names-spec.md` shows how badly Geni's own fields behave. A later pass can split them
with an approved rule; inventing one here would bake a guess into the corpus.

`<li>` is never closed on these pages, so nesting-based scoping does not work and this reads the
document linearly instead.
"""
from __future__ import annotations

import pathlib
import re
from html.parser import HTMLParser

#: ⛔ THE PHRASE TABLE IS NOT WRITTEN HERE. It is lifted out of `geni-extension/content/family.js`,
#: which is the live scraper and therefore the authority on what a page says.
#:
#: **Two hand-maintained copies of one rule drift, and the drift is silent.** This module carried
#: its own list of 12 phrases while `GC.family.PHRASES` carried 24, and the twelve missing ones
#: were not obscure: `ex-husband of`, `ex-wife of`, `fiancé(e) of`, all six `step*`,
#: `adopted son/daughter of` and `foster son/daughter of`. `scripts/family-scrape-js.py` already
#: solved this for the injected snippet by parsing the extension source rather than restating it;
#: this is the same fix for the offline reader, and it is what lets the two be *proved* equal
#: instead of asserted equal -- `scripts/prove-saved-page-equivalence.py`.
#:
#: The subject/target roles stay here, because `family.js` maps a phrase to ONE token (`parent`,
#: `sibling`) while this module needs both ends. A phrase in the extension table with no entry
#: below is still recognised as an opener -- it just carries no role, which keeps an unknown
#: phrase from being mis-attributed rather than silently classified.
_ROLES = {
    "parent": ("child", "parent"),          # "Son of A"      -> subject is the child
    "child": ("parent", "child"),           # "Father of A"   -> subject is the parent
    "spouse": ("spouse", "spouse"),
    "partner": ("spouse", "spouse"),
    "ex-spouse": ("ex-spouse", "ex-spouse"),
    "fiance": ("fiance", "fiance"),
    "sibling": ("sibling", "sibling"),
    "half-sibling": ("sibling", "sibling"),
    "step-parent": ("step-child", "step-parent"),
    "step-child": ("step-parent", "step-child"),
    "step-sibling": ("step-sibling", "step-sibling"),
    "adoptive-parent": ("adopted-child", "adoptive-parent"),
    "foster-parent": ("foster-child", "foster-parent"),
}

_FAMILY_JS = (pathlib.Path(__file__).resolve().parent.parent
              / "geni-extension" / "content" / "family.js")
#: `[/^son of/i, "parent"],` -- the entries of `GC.family.PHRASES`, in source order.
_ENTRY_RE = re.compile(r"\[\s*/\^(?P<pat>[^/]+)/i\s*,\s*\"(?P<kind>[^\"]+)\"\s*\]")


def _load_phrases() -> dict:
    text = _FAMILY_JS.read_text(encoding="utf-8")
    start = text.index("GC.family.PHRASES = [")
    block = text[start:text.index("];", start)]
    out = {}
    for m in _ENTRY_RE.finditer(block):
        # `fianc(é|e)e? of` is a real alternation in the extension table; expand it rather than
        # dropping it, because a regex kept as a literal string would never match the page text.
        pats = [m.group("pat")]
        if "(" in m.group("pat"):
            head, rest = m.group("pat").split("(", 1)
            alts, tail = rest.split(")", 1)
            pats = [head + a + tail for a in alts.split("|")]
        for pat in pats:
            out[pat.replace("?", "").lower()] = _ROLES.get(m.group("kind"), ())
    return out


#: The relationship phrases Geni writes, mapped to (role of the SUBJECT, role of the TARGET).
#: `Son of A and B` makes the subject a child; `Mother of X` makes the subject a parent.
PHRASES = _load_phrases()
#: ⛔ `\b` IS THE WRONG BOUNDARY: A HYPHEN IS A WORD BOUNDARY, SO `Ex-partner of` MATCHED
#: `partner of` AND TURNED AN EX-PARTNER INTO A SPOUSE.
#:
#: Found by the differential on Christoffer Arntzen `6000000007210899736`, whose page reads
#: *"Ex-partner of Hanna Marie Carstensdatter and Dorthea Johanna Hansdatter"*. `ex-partner of` is
#: in NEITHER table — not here and not in `family.js` — and the two readers then disagreed in the
#: most damaging possible direction: the live scraper anchors its patterns with `/^partner of/i`
#: against the line, so it did not match, fell through to `LOOKS_LIKE_OPENER` and recorded the two
#: women with an EMPTY relation; this module matched mid-string and called them partners.
#:
#: Inventing a marriage is exactly what `build-scraped-gedcom.py` was deleted for. The lookbehind
#: makes the match start at a real opener boundary, the way `^` does for the extension.
_PHRASE_RE = re.compile(
    r"(?<![-\w])(" + "|".join(sorted((re.escape(p) for p in PHRASES), key=len, reverse=True))
    + r")\s*$", re.I)

#: ⛔ AN UNRECOGNISED OPENER MUST BREAK THE RUN, NOT INHERIT THE ONE ABOVE IT.
#:
#: Anchors are attributed to the nearest phrase above them, so an opener this table does not know
#: leaves `_phrase` pointing at the previous line and hands that line's role to the wrong people.
#: `family.js` records the worked case: Anna Throndsen `296165995120003655` reads "Daughter of A
#: and B" then "Fiancée of James Hepburn", and Hepburn was scraped as her THIRD PARENT.
#:
#: `GC.family.LOOKS_LIKE_OPENER` is the extension's guard for the CLASS rather than the instance,
#: and this is the same shape against the tail of the accumulated text: a short run of letters,
#: spaces and hyphens ending in ` of`, which no name looks like.
_LOOKS_LIKE_OPENER = re.compile(r"(?:^|[>.;]|\s)([A-Za-z][A-Za-zÀ-ɏ' -]{1,30} of)\s*$", re.I)


class _FamilyParser(HTMLParser):
    """Read the page subject's family out of `tr#family_handprint`.

    **That element is the whole answer to the scoping problem.** A saved page carries hovercards
    for dozens of other people, each with its own *"Wife of ... Mother of ..."* prose, so reading
    relationship phrases from the document at large attributes one person's marriage to another's
    page. Two earlier attempts here did exactly that -- the first gave Rebecka Berg's page
    Brita Henriksdotter Uddman's family, the second handed the same three edges to Walborg
    Finsell as well. `genimerge.genipage` records the identical failure for the relationship
    panel and solves it the same way: scope to the element, do not match anchors at large.

    Inside that block the subject is **the person whose page it is**, never an anchor -- every
    anchor in there is a relative.
    """

    def __init__(self) -> None:
        super().__init__()
        self.edges: list[tuple[str, list[tuple[str, str]]]] = []
        self.names: dict[str, str] = {}
        self._depth = 0
        self._text: list[str] = []
        self._pid: str | None = None
        self._buf: list[str] = []
        self._phrase: str | None = None

    def handle_starttag(self, tag: str, attrs) -> None:
        d = dict(attrs)
        if d.get("id") == "family_handprint":
            self._depth = 1
            return
        if not self._depth:
            return
        if tag == "tr":
            self._depth = 0          # the next row is a different field
            return
        if tag == "a" and d.get("data-profile-id"):
            tail = " ".join("".join(self._text).split())[-40:]
            m = _PHRASE_RE.search(tail)
            if m:
                self._phrase = m.group(1).lower()
                self.edges.append((self._phrase, []))
            elif _LOOKS_LIKE_OPENER.search(tail):
                # ⛔ AN UNKNOWN OPENER STARTS AN EMPTY-PHRASE GROUP, exactly as `family.js` does.
                # Not `None`: the live scraper *records* these people with an empty relation
                # rather than dropping them — "an anchor before any phrase is recorded with an
                # empty relation rather than guessed at" — so dropping them here would make the
                # two readers differ about people they both saw. An empty phrase asserts no
                # relationship, and `saved_page_gedcom` matches none of its cases against it, so
                # nothing reaches the corpus either way.
                self._phrase = ""
                self.edges.append(("", []))
            self._pid = d["data-profile-id"]
            self._buf = []
        elif tag == "br":
            self._text = []

    def handle_endtag(self, tag: str) -> None:
        if not self._depth:
            return
        # ⛔ THE SCOPE ENDS AT `</td>`, AND CLOSING ONLY ON THE NEXT `<tr>` NEVER ENDED IT.
        #
        # `handle_starttag` drops out of the block when it meets the next `<tr>` START tag, and on
        # a saved page there is not always another one: the family row is the last in its table,
        # so the walk ran on through the rest of the document and handed every later anchor to
        # the last opener it had seen. Measured on Brendan Robert Walsh `365315518800010569` --
        # the block holds 6 relatives, the walk returned 11, and the 5 extras were his spouse,
        # both parents and a child all re-emitted as `Brother`.
        #
        # `family.js` never had this: it scopes to the `<td>` beside `<th>Immediate Family:</th>`
        # and reads only inside that cell. Closing here on `</td>` is that same boundary, and
        # `</tr>` closes the row for any page that renders the block without a cell.
        if tag in ("td", "tr"):
            self._depth = 0
            self._pid = None
            self._phrase = None
            return
        if tag == "a" and self._pid:
            name = " ".join("".join(self._buf).split())
            if name:
                self.names[self._pid] = name
                # `is not None`, not truthiness: an unknown opener sets the phrase to the EMPTY
                # STRING deliberately, and `if self._phrase` silently dropped every person under
                # one -- which is the same people the live scraper records with a blank relation.
                if self._phrase is not None and self.edges:
                    self.edges[-1][1].append((self._pid, name))
            self._pid = None
            self._text = []

    def handle_data(self, data: str) -> None:
        if not self._depth:
            return
        (self._buf if self._pid else self._text).append(data)


def parse_family(html: str):
    """`(names_by_id, [(phrase, [(id, name)])])` for the subject of one saved page."""
    p = _FamilyParser()
    p.feed(html)
    return p.names, [e for e in p.edges if e[1]]
