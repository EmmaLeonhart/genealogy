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

__all__ = ["PathLink", "parse_relationship_path", "read_relationship_path", "to_tsv"]


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


def read_relationship_path(path: str | Path) -> list[PathLink]:
    """Read a saved page. Geni's pages are UTF-8; the CJK names prove it."""
    return parse_relationship_path(Path(path).read_text(encoding="utf-8", errors="replace"))


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
