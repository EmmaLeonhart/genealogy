"""Parse GEDCOM dates into something a Wikidata statement can be built from.

Across the whole merged tree there are only fifteen distinct date shapes, all of
them standard GEDCOM 5.5.1: an exact ``23 APR 2021``, a bare year, a month and
year, and those three again behind ``ABT`` / ``BEF`` / ``AFT``, plus
``BET x AND y``. So this is a small parser rather than a general one, and
anything it does not recognise keeps its raw text and reports no structured
value — a date we cannot read must not become a date we guessed.

Precision follows Wikidata's own scale (9 year, 10 month, 11 day), because that
is where these values are going.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

__all__ = [
    "GedcomDate",
    "parse_date",
    "PRECISION_DAY",
    "PRECISION_MONTH",
    "PRECISION_YEAR",
]

PRECISION_YEAR = 9
PRECISION_MONTH = 10
PRECISION_DAY = 11

_MONTHS = {
    m: i
    for i, m in enumerate(
        "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split(), start=1
    )
}

#: GEDCOM date modifiers, mapped to a plain word. ``EST`` and ``CAL`` do not
#: occur in this corpus but cost nothing to accept.
_MODIFIERS = {
    "ABT": "about",
    "EST": "about",
    "CAL": "about",
    "BEF": "before",
    "AFT": "after",
    "FROM": "after",
    "TO": "before",
}

_TOKEN = re.compile(r"^(?:(\d{1,2})\s+)?(?:([A-Z]{3})\s+)?(\d{3,4})$")


@dataclass(frozen=True)
class GedcomDate:
    """One parsed date. ``year is None`` means it could not be read."""

    raw: str
    year: int | None = None
    month: int | None = None
    day: int | None = None
    #: ``"about"``, ``"before"``, ``"after"``, ``"between"``, or ``None``
    modifier: str | None = None
    #: the far end of a ``BET x AND y`` range
    year_end: int | None = None

    @property
    def precision(self) -> int | None:
        if self.year is None:
            return None
        if self.day is not None:
            return PRECISION_DAY
        if self.month is not None:
            return PRECISION_MONTH
        return PRECISION_YEAR

    @property
    def is_exact(self) -> bool:
        """No modifier and no range — a date we can assert plainly."""
        return self.year is not None and self.modifier is None

    def iso(self) -> str | None:
        """``+1996-02-26T00:00:00Z`` style, the form Wikidata time values take.

        Unknown month and day are written as ``00``, which is how Wikidata
        represents "this year, no finer".
        """
        if self.year is None:
            return None
        return (
            f"{'+' if self.year > 0 else '-'}{abs(self.year):04d}"
            f"-{self.month or 0:02d}-{self.day or 0:02d}T00:00:00Z"
        )

    def __str__(self) -> str:
        return self.raw


def _parse_plain(text: str) -> tuple[int, int | None, int | None] | None:
    match = _TOKEN.match(text.strip())
    if match is None:
        return None
    day, month_name, year = match.groups()
    if month_name is not None and month_name not in _MONTHS:
        return None
    month = _MONTHS[month_name] if month_name else None
    # "7  2011" — a day with no month tells us nothing we can place in a year,
    # so the day is dropped rather than attached to an unknown month.
    if day is not None and month is None:
        return (int(year), None, None)
    return (int(year), month, int(day) if day else None)


def parse_date(value: str | None) -> GedcomDate:
    """Parse one GEDCOM ``DATE`` value. Never raises."""
    raw = (value or "").strip()
    if not raw:
        return GedcomDate(raw="")

    text = raw.upper()

    between = re.match(r"^BET\s+(.+?)\s+AND\s+(.+)$", text)
    if between:
        start = _parse_plain(between.group(1))
        end = _parse_plain(between.group(2))
        if start:
            return GedcomDate(
                raw=raw,
                year=start[0],
                month=start[1],
                day=start[2],
                modifier="between",
                year_end=end[0] if end else None,
            )
        return GedcomDate(raw=raw)

    modifier = None
    head, _, rest = text.partition(" ")
    if head in _MODIFIERS and rest:
        modifier = _MODIFIERS[head]
        text = rest

    parsed = _parse_plain(text)
    if parsed is None:
        return GedcomDate(raw=raw)
    year, month, day = parsed
    return GedcomDate(raw=raw, year=year, month=month, day=day, modifier=modifier)
