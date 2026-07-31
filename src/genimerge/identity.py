"""Where a record's Geni profile ID comes from, in one place.

Geni's GEDCOM export puts the profile ID in two places at once::

    0 @I6000000087535357291@ INDI
    1 RFN geni:6000000087535357291

The xref prefix is a type letter (``I`` individual, ``F`` family, ``S``
submitter, ``N`` note), and the digits are the Geni ID. Everything in the
package that needs to know "which person is this" comes through here, so if the
export format ever changes there is exactly one thing to fix.
"""

from __future__ import annotations

import re

from .gedcom import Node

__all__ = [
    "GENI_ID_RE",
    "RFN_PREFIX",
    "geni_id_of",
    "geni_id_from_xref",
    "geni_id_from_pointer",
    "xref_for",
    "profile_url",
    "IdentityMismatch",
]

GENI_ID_RE = re.compile(r"^@(?P<kind>[A-Za-z_]+)(?P<geni_id>\d+)@$")
RFN_PREFIX = "geni:"


class IdentityMismatch(ValueError):
    """The xref and the ``RFN`` disagree about which profile a record is.

    Raised rather than resolved: if the two identifiers ever diverge, guessing
    which one is right would silently merge the wrong people together.
    """


def geni_id_from_xref(xref: str | None) -> str | None:
    """``"@I6000000087535357291@"`` -> ``"6000000087535357291"``."""
    if not xref:
        return None
    match = GENI_ID_RE.match(xref)
    return match["geni_id"] if match else None


def geni_id_from_pointer(node: Node | None) -> str | None:
    """The Geni ID a pointer line (``1 FAMC @F123@``) points at."""
    if node is None:
        return None
    return geni_id_from_xref(node.pointer)


def geni_id_of(record: Node, *, strict: bool = True) -> str | None:
    """The Geni profile ID of a level-0 record, cross-checked against ``RFN``.

    Returns ``None`` when the xref carries no usable ID. With ``strict`` (the
    default), a present-but-disagreeing ``RFN`` raises
    :class:`IdentityMismatch`; an *absent* ``RFN`` is fine, since only ``INDI``
    records carry one.
    """
    from_xref = geni_id_from_xref(record.xref)

    rfn = record.value_of("RFN")
    if strict and rfn.startswith(RFN_PREFIX):
        from_rfn = rfn[len(RFN_PREFIX) :].strip()
        if from_xref is not None and from_rfn != from_xref:
            raise IdentityMismatch(
                f"{record.tag} {record.xref}: xref says {from_xref!r} "
                f"but RFN says {from_rfn!r}"
            )
        if from_xref is None:
            return from_rfn or None

    return from_xref


def xref_for(kind: str, geni_id: str) -> str:
    """``("I", "123")`` -> ``"@I123@"``."""
    return f"@{kind}{geni_id}@"


def profile_url(geni_id: str) -> str:
    """The public Geni profile URL, which is also the P2600 formatter target."""
    return f"https://www.geni.com/people/x/{geni_id}"
