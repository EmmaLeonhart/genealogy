"""Read a relationship path out of a Geni profile page saved from the browser.

Geni's profile page shows a chain of relationships from the signed-in user to
the person being viewed. Copying that panel as text loses the links, and the
links are the only place the Geni profile IDs appear — which matters because the
ID is this repo's primary key and the names are not. Saving the page keeps them.

So: save the profile page (Ctrl-S, "complete"), commit the HTML, and this module
turns it into a path file whose every row carries a real ID. `genimerge.paths`
prefers an ID over a name wherever one is present, so doing this retires the
name matching that module otherwise has to fall back on.

**Scoping is the whole difficulty.** A Geni profile page is full of profile
links that are not on the path — immediate family, profile managers, followers,
"recently viewed by". Taking every anchor with a `data-profile-id` yields
several hundred people in page order, which looks like a path and is not one.
The path proper is exactly the anchors inside ``span.segment > span.name``, and
this parser tracks that nesting rather than matching anchors directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path

__all__ = [
    "PathLink",
    "parse_relationship_path",
    "read_relationship_path",
    "relation_description",
    "to_tsv",
]


@dataclass(frozen=True)
class PathLink:
    """One step of the path, as the page states it."""

    geni_id: str
    name: str
    relation: str = ""

    @property
    def url(self) -> str:
        from .identity import profile_url

        return profile_url(self.geni_id)


class _PathParser(HTMLParser):
    """Anchors inside ``span.segment > span.name``, in document order.

    The relation ("her mother") lives in a sibling ``span.subtext`` and is
    wrapped in parentheses by ``span.clipboard-only`` elements that exist so a
    copy-paste reads as prose. Those parentheses are markup, not part of the
    relation, so they come off.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[PathLink] = []
        self._spans: list[str] = []
        self._id: str | None = None
        self._name: list[str] = []
        self._subtext_at: int | None = None
        self._relation: list[str] = []

    def _in(self, klass: str) -> bool:
        return any(klass in c.split() for c in self._spans)

    def handle_starttag(self, tag: str, attrs) -> None:
        attributes = dict(attrs)
        if tag == "span":
            klass = attributes.get("class") or ""
            self._spans.append(klass)
            if self._subtext_at is None and "subtext" in klass.split():
                self._subtext_at = len(self._spans)
                self._relation = []
        elif tag == "a":
            profile = attributes.get("data-profile-id")
            if profile and self._in("segment") and self._in("name"):
                self._id = profile
                self._name = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._id is not None:
            self.links.append(
                PathLink(geni_id=self._id, name="".join(self._name).strip())
            )
            self._id = None
        elif tag == "span" and self._spans:
            depth = len(self._spans)
            self._spans.pop()
            if self._subtext_at == depth:
                self._subtext_at = None
                self._finish_relation()

    def _finish_relation(self) -> None:
        text = "".join(self._relation).replace("\xa0", " ")
        text = " ".join(text.split()).strip()
        if text.startswith("(") and text.endswith(")"):
            text = text[1:-1].strip()
        # The first step's subtext is a non-breaking space rather than a
        # relation — Geni prints "You" with nothing to relate it to.
        if text and self.links:
            self.links[-1] = PathLink(
                geni_id=self.links[-1].geni_id,
                name=self.links[-1].name,
                relation=text,
            )

    def handle_data(self, data: str) -> None:
        if self._id is not None:
            self._name.append(data)
        if self._subtext_at is not None:
            self._relation.append(data)


def parse_relationship_path(html: str) -> list[PathLink]:
    parser = _PathParser()
    parser.feed(html)
    parser.close()
    return parser.links


def relation_description(html: str) -> str:
    """Geni's own prose summary of the path --- the RESIDUAL the step parser drops.

    **Emma, 2026-09-03:** *"our parser I think was weird because structurally so much weird shit
    happens we need to grab residuals all the time."* This is the first of those residuals, and
    it is not decoration: the per-step `span.segment` words flatten distinctions the prose keeps.

    Measured over 30,329 steps in 696 path files, the step words never say *half* --- only
    `his brother` / `her sister`. The prose does. One in-law page reads *"…partner's son's wife's
    ex-husband's half sister's ex-husband's second cousin twice removed's wife's father."*
    `Half brother` / `Half sister` occurs 325 times across the saved pages, all of it outside the
    segments. Ex-spouses survive both ways (`her ex-husband` is a step word too); half-siblings
    survive only here.

    Two shapes share the id: a short verdict (*"X is your 28th cousin once removed"*) and the
    long possessive chain. Both are returned as-is --- **this is a residual, not a parse.** It is
    kept beside the path so nothing that was on the page is lost, and aligning it against the
    steps is a separate job that nothing does yet: the in-law prose is a possessive chain that
    does not map one-to-one onto segments.
    """
    import re

    out: list[str] = []
    for m in re.finditer(r'<div[^>]*(?:id|class)="relation_description"[^>]*>', html):
        # **The block must be found by BALANCING `<div>`, not by the first `</div>`.** Its first
        # child is an expand/collapse image wrapper, so a non-greedy `.*?</div>` stops there and
        # returns whitespace --- which reads as "the page has no description" on every page. It
        # measured 0 of 200 before this was fixed, the same shape of silent narrowing as the date
        # parser and the ` | ` separator in `CLAUDE.md`.
        depth, i = 0, m.start()
        for tag in re.finditer(r"</?div\b", html[m.start():]):
            depth += 1 if tag.group(0) == "<div" else -1
            if depth == 0:
                # `tag.start()`, not `tag.end()`: the pattern matches `</div` without its `>`,
                # so ending at `end()` leaves a dangling `</div` that the tag-stripper cannot
                # remove and that lands in the text.
                i = m.start() + tag.start()
                break
        else:
            continue
        text = re.sub(r"<[^>]+>", " ", html[m.end():i])
        text = re.sub(r"\s+", " ", text).strip()
        # "Generate Diagram" is a button label that sits inside the same block.
        text = text.replace("Generate Diagram", "").strip()
        if text and text not in out:
            out.append(text)
    return " | ".join(out)


def html_of_saved_page(raw: str) -> str:
    """The HTML out of a saved page, whether it is plain HTML or a **single-file MHTML**.

    **Chrome's "Webpage, Single File" is MIME, and its HTML part is quoted-printable**, so every
    `href="..."` is stored as `href=3D"..."` and every `=` in the markup is `=3D`. The parser
    reads that as attributes it does not recognise and finds no path at all — which comes out as
    *"no relationship path found"*, indistinguishable from a page saved while signed out or of
    two people Geni cannot connect. Two of Emma's saved pages failed that way on 2026-08-27, and
    the markup was in them the whole time: 48 `segment` classes, 68 `data-profile-id` anchors,
    2,378 `=3D` sequences.

    A plain HTML file is returned untouched, so this is additive.
    """
    if not raw.lstrip().startswith(("From:", "MIME-Version:", "Content-Type: multipart")):
        return raw
    import email
    import email.policy

    msg = email.message_from_string(raw, policy=email.policy.default)
    parts = [p for p in msg.walk() if p.get_content_type() == "text/html"]
    if not parts:
        return raw
    # The first text/html part is the page itself; later ones are framed content.
    payload = parts[0].get_payload(decode=True)
    if payload is None:
        return raw
    charset = parts[0].get_content_charset() or "utf-8"
    return payload.decode(charset, errors="replace")


def read_relationship_path(path: str | Path) -> list[PathLink]:
    """Read a saved page. Geni's pages are UTF-8; the CJK names prove it."""
    raw = Path(path).read_text(encoding="utf-8", errors="replace")
    return parse_relationship_path(html_of_saved_page(raw))


def to_tsv(links: list[PathLink], *, header: str = "") -> str:
    """A path file of the shape `genimerge.paths` reads.

    Every row gets its `geni:<id>` in the note column, which is what makes the
    resulting check an exact join instead of a name match.
    """
    lines = [line for line in header.splitlines()] if header else []
    lines.append("step\tname\trelation_to_previous\tnote")
    for index, link in enumerate(links, start=1):
        relation = link.relation or "-"
        lines.append(f"{index}\t{link.name}\t{relation}\tgeni:{link.geni_id}")
    return "\n".join(lines) + "\n"
