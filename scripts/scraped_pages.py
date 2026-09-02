"""Read the immediate family out of a saved Geni profile page.

**Emma, 2026-08-29**, on the 1,555 pages in `geni-scraping/` and the 698 files in `paths/`:
*"My suggestion would be for us to convert these things into GEDCOM files that would go into a
special GEDCOM directory... so that it will save both the paths and the saved pages because they
are different. It turns them into things that are usable and would be merged into the Geni union — the synoptic
tree as GEDCOM stuff."*

**What a saved page actually carries.** Not a structured family list -- prose with links:

    <a data-profile-id="...">Brita Henriksdotter Uddman</a> <br>
    Wife of <a data-profile-id="...">Isak Henricsson Peldan</a> and <a ...>Johan Mathesius</a> <br>
    Mother of <a data-profile-id="...">Brita Helena Peldan</a> ...

So every edge is an English phrase followed by the anchors it governs, and the anchors carry the
Geni id. That is what makes this an exact join rather than a name match, which is the same reason
`genimerge.genipage` reads the relationship panel from `href`s instead of from the visible text.

**Names arrive as one string and stay that way.** Emma is explicit that this is the cost:
*"the names being present as strings makes things significantly harder"*, and *"You'd probably be
using spacing to figure out what the last name is or something. It would work in most cases, but
not all."* This module therefore emits `1 NAME <string>` and **no `GIVN`/`SURN` split at all** --
guessing a surname from spacing is exactly the fuzzy inference this repo refuses everywhere else,
and `reports/names-spec.md` shows how badly Geni's own fields behave. A later pass can split them
with a rule she has approved; inventing one here would bake a guess into the corpus.

`<li>` is never closed on these pages, so nesting-based scoping does not work and this reads the
document linearly instead.
"""
from __future__ import annotations

import re
from html.parser import HTMLParser

#: The relationship phrases Geni writes, mapped to (role of the SUBJECT, role of the TARGET).
#: `Son of A and B` makes the subject a child; `Mother of X` makes the subject a parent.
PHRASES = {
    "son of": ("child", "parent"),
    "daughter of": ("child", "parent"),
    "child of": ("child", "parent"),
    "father of": ("parent", "child"),
    "mother of": ("parent", "child"),
    "husband of": ("spouse", "spouse"),
    "wife of": ("spouse", "spouse"),
    "partner of": ("spouse", "spouse"),
    "brother of": ("sibling", "sibling"),
    "sister of": ("sibling", "sibling"),
    "half brother of": ("sibling", "sibling"),
    "half sister of": ("sibling", "sibling"),
}
_PHRASE_RE = re.compile(
    r"\b(" + "|".join(sorted((re.escape(p) for p in PHRASES), key=len, reverse=True)) + r")\s*$",
    re.I)


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
            self._pid = d["data-profile-id"]
            self._buf = []
        elif tag == "br":
            self._text = []

    def handle_endtag(self, tag: str) -> None:
        if not self._depth:
            return
        if tag == "a" and self._pid:
            name = " ".join("".join(self._buf).split())
            if name:
                self.names[self._pid] = name
                if self._phrase and self.edges:
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
