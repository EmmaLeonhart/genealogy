"""A GEDCOM 5.5.1 reader and writer, sized for what Geni.com actually emits.

GEDCOM is a line-oriented tree format. Every line is::

    LEVEL [@XREF@] TAG [value]

and a line's level says how deep it hangs off the line before it. Two tags,
``CONC`` and ``CONT``, are not real structure — they are how the format wraps
long values across physical lines (``CONT`` = a newline, ``CONC`` = a straight
join). This module **folds them away on read and re-creates them on write**, so
callers deal in whole values and never in wrapping.

The parser is deliberately lenient about everything else: a real-world export is
not a conformance test, and refusing to read a file because one line is odd
would be useless here. Unreadable lines are collected on
:attr:`Gedcom.warnings` rather than raised.

Reading is streaming (:func:`iter_records`) so the 16 MB export never has to sit
in memory as one object graph unless a caller asks for that.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Iterator

__all__ = [
    "Node",
    "Gedcom",
    "iter_records",
    "parse",
    "parse_file",
    "serialize",
    "write_file",
    "MAX_VALUE_LEN",
]

# GEDCOM 5.5.1 caps a physical line at 255 bytes including level and tag. We
# wrap well under that so multi-byte characters (this tree is full of æ, ø, å)
# cannot push a line over the limit.
MAX_VALUE_LEN = 200

_LINE_RE = re.compile(
    r"""^﻿?\s*
        (?P<level>\d+)\s+
        (?:(?P<xref>@[^@\s]+@)\s+)?
        (?P<tag>[A-Za-z0-9_]+)
        (?:\s(?P<value>.*))?
        \s*$""",
    re.VERBOSE,
)

_POINTER_RE = re.compile(r"^@[^@\s]+@$")


@dataclass
class Node:
    """One GEDCOM line plus everything nested under it.

    ``value`` is the *folded* value: ``CONC``/``CONT`` children have already
    been merged into it, and embedded newlines mean what ``CONT`` meant.
    """

    tag: str
    value: str = ""
    xref: str | None = None
    children: list["Node"] = field(default_factory=list)

    # -- reading -------------------------------------------------------

    def get(self, tag: str) -> "Node | None":
        """First direct child with ``tag``, or ``None``."""
        for child in self.children:
            if child.tag == tag:
                return child
        return None

    def all(self, tag: str) -> list["Node"]:
        """Every direct child with ``tag``, in file order."""
        return [child for child in self.children if child.tag == tag]

    def value_of(self, tag: str, default: str = "") -> str:
        """Value of the first direct child with ``tag``."""
        child = self.get(tag)
        return child.value if child is not None else default

    def path(self, *tags: str) -> "Node | None":
        """Follow a chain of first-matching children, e.g. ``path("BIRT", "DATE")``."""
        node: Node | None = self
        for tag in tags:
            if node is None:
                return None
            node = node.get(tag)
        return node

    def path_value(self, *tags: str, default: str = "") -> str:
        node = self.path(*tags)
        return node.value if node is not None else default

    def walk(self) -> Iterator["Node"]:
        """This node, then every descendant, depth-first in file order."""
        yield self
        for child in self.children:
            yield from child.walk()

    @property
    def pointer(self) -> str | None:
        """The xref this line points *at*, if its value is a pointer like ``@F1@``."""
        return self.value if _POINTER_RE.match(self.value) else None

    # -- writing -------------------------------------------------------

    def add(self, tag: str, value: str = "", xref: str | None = None) -> "Node":
        """Append a child and return it."""
        child = Node(tag=tag, value=value, xref=xref)
        self.children.append(child)
        return child

    def copy(self) -> "Node":
        """A deep copy — merging rearranges trees, and sharing nodes would alias."""
        return Node(
            tag=self.tag,
            value=self.value,
            xref=self.xref,
            children=[c.copy() for c in self.children],
        )


@dataclass
class Gedcom:
    """A whole file: its ``HEAD``, its records, and anything we could not read."""

    header: Node | None = None
    records: list[Node] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def by_tag(self, tag: str) -> list[Node]:
        return [r for r in self.records if r.tag == tag]

    def by_xref(self) -> dict[str, Node]:
        return {r.xref: r for r in self.records if r.xref}


def _parse_line(raw: str) -> tuple[int, str | None, str, str] | None:
    match = _LINE_RE.match(raw)
    if match is None:
        return None
    return (
        int(match["level"]),
        match["xref"],
        match["tag"],
        match["value"] or "",
    )


def iter_records(
    lines: Iterable[str],
    warnings: list[str] | None = None,
) -> Iterator[Node]:
    """Yield each level-0 record as a folded :class:`Node`, one at a time.

    ``HEAD`` and ``TRLR`` come through like any other record; it is the caller's
    job to recognise them. Malformed lines are appended to ``warnings`` (with a
    1-based line number) and skipped — a single bad line loses that line, not
    the file.
    """
    warnings = warnings if warnings is not None else []
    stack: list[Node] = []
    current: Node | None = None

    for lineno, raw in enumerate(lines, start=1):
        raw = raw.rstrip("\r\n")
        if not raw.strip():
            continue

        parsed = _parse_line(raw)
        if parsed is None:
            warnings.append(f"line {lineno}: unparseable, skipped: {raw[:120]!r}")
            continue
        level, xref, tag, value = parsed

        if level == 0:
            if current is not None:
                yield current
            current = Node(tag=tag, value=value, xref=xref)
            stack = [current]
            continue

        if current is None:
            warnings.append(f"line {lineno}: level {level} before any level-0 record, skipped")
            continue

        # A level deeper than "one below the previous line" is malformed. Clamp
        # rather than drop: the payload is still worth having, and Geni's notes
        # are the only place this shows up.
        if level > len(stack):
            warnings.append(
                f"line {lineno}: level {level} jumps past depth {len(stack) - 1}, clamped"
            )
            level = len(stack)

        parent = stack[level - 1]

        if tag == "CONT":
            parent.value = f"{parent.value}\n{value}"
            continue
        if tag == "CONC":
            parent.value = f"{parent.value}{value}"
            continue

        node = Node(tag=tag, value=value, xref=xref)
        parent.children.append(node)
        del stack[level:]
        stack.append(node)

    if current is not None:
        yield current


def parse(text: str) -> Gedcom:
    """Parse a whole GEDCOM held in a string.

    Splits on ``\\n`` alone rather than :meth:`str.splitlines`. ``splitlines``
    also breaks on ``\\v``, ``\\f``, ``\\x1c``-``\\x1e``, ``\\x85``, ``U+2028``
    and ``U+2029``, none of which end a line in a file read with
    ``newline=""`` — and the Ancestors export really does carry ``U+2028``
    inside five note values. Using ``splitlines`` here made :func:`parse`
    disagree with :func:`parse_file` on exactly those records.
    """
    return _collect(iter_records, text.split("\n"))


def parse_file(path: str | Path, encoding: str = "utf-8-sig") -> Gedcom:
    """Parse a whole GEDCOM file.

    Defaults to ``utf-8-sig`` because Geni declares ``1 CHAR UTF-8`` and some
    exports carry a BOM; ``errors="replace"`` keeps one bad byte from taking
    down a 16 MB file.
    """
    with open(path, "r", encoding=encoding, errors="replace", newline="") as handle:
        return _collect(iter_records, handle)


def _collect(reader, source) -> Gedcom:
    warnings: list[str] = []
    doc = Gedcom(warnings=warnings)
    for record in reader(source, warnings):
        if record.tag == "HEAD":
            doc.header = record
        elif record.tag == "TRLR":
            continue  # re-created on write; carrying it around is noise
        else:
            doc.records.append(record)
    return doc


def _emit(node: Node, level: int, out: list[str]) -> None:
    head = f"{level}"
    if node.xref:
        head = f"{head} {node.xref}"
    head = f"{head} {node.tag}"

    segments = node.value.split("\n") if node.value else [""]
    first = True
    for segment in segments:
        # The first physical line of the first segment carries the real tag;
        # everything after is CONT (a newline) or CONC (an over-long value).
        chunks = _chunk(segment) or [""]
        for index, chunk in enumerate(chunks):
            if first:
                prefix, first = head, False
            elif index == 0:
                prefix = f"{level + 1} CONT"
            else:
                prefix = f"{level + 1} CONC"
            # Only join with a space when there is a value; otherwise a tagless
            # line would pick up a trailing space, and a value's own trailing
            # space would be indistinguishable from it.
            out.append(f"{prefix} {chunk}" if chunk else prefix)

    for child in node.children:
        _emit(child, level + 1, out)


def _chunk(text: str) -> list[str]:
    if len(text) <= MAX_VALUE_LEN:
        return [text]
    return [text[i : i + MAX_VALUE_LEN] for i in range(0, len(text), MAX_VALUE_LEN)]


def serialize(doc: Gedcom) -> str:
    """Render back to GEDCOM text, re-creating ``CONC``/``CONT`` wrapping.

    This is *semantic* round-tripping, not byte-for-byte: re-parsing the output
    gives back an equal tree, but the wrapping points may differ from the input.
    """
    out: list[str] = []
    if doc.header is not None:
        _emit(doc.header, 0, out)
    for record in doc.records:
        _emit(record, 0, out)
    out.append("0 TRLR")
    return "\n".join(out) + "\n"


def write_file(doc: Gedcom, path: str | Path) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(serialize(doc))


def stream_file(path: str | Path, encoding: str = "utf-8-sig") -> Iterator[Node]:
    """Iterate a file's level-0 records without building the whole document.

    Warnings are dropped on this path — use :func:`parse_file` when they matter.
    """
    with open(path, "r", encoding=encoding, errors="replace", newline="") as handle:
        yield from iter_records(handle)
