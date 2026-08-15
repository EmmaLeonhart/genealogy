"""A claim to add to a Wikidata item, with the reference it carries.

QuickStatements was deleted on 2026-08-15 — module, `genimerge quickstatements`
command, every `.qs` file, and the three `render_quickstatements` functions that
wrote them. Emma: *"we are deleting the entire thing right now."* It was built
without being asked for, against a spec (2026-08-12) that calls for **JSON edit
objects with dependency ordering**, roughly a hundred executed per day.

What survives here is the *model*, not the format. `crosscheck` and `namelinks`
both work out which claims are missing and which are safe to propose, and that
reasoning is worth keeping whatever the eventual serialisation is. A tab line
with `S`-prefixed reference columns is QuickStatements; a claim with a property,
a value and a source is not.

**The reference is plain `P854`/`P813`, not `S854`/`S813`.** The `S` prefix was
QuickStatements' way of marking a reference part inside a flat line. JSON edit
objects say where a snak belongs structurally, so the property keeps its real
number.

Nothing here renders anything. `scripts/build-edit-objects.py` owns the output
format, and `edit-objects.md` is its specification.
"""

from __future__ import annotations

from dataclasses import dataclass

from .identity import profile_url


@dataclass(frozen=True)
class Statement:
    """One claim proposed for one item.

    ``value`` is a bare ``Q123`` for an item and a quoted string or a time
    literal for anything else — the caller knows the datatype and this does not.
    """

    qid: str
    prop: str
    value: str
    #: (property, value) pairs qualifying the claim
    qualifiers: tuple[tuple[str, str], ...] = ()
    #: (property, value) pairs forming the claim's reference
    references: tuple[tuple[str, str], ...] = ()


def geni_reference(geni_id: str, retrieved: str) -> tuple[tuple[str, str], ...]:
    """The reference every Geni-sourced claim carries: where it came from, and when.

    Emma, 2026-08-12: *"in the references thing, as a reference, not a qualifier
    or reference, we have the Jenny external identifier… everything on the
    individuals that are created is going to be cited to Jenny because all of it
    is coming from"* Geni.
    """
    return (
        ("P854", f'"{profile_url(geni_id)}"'),
        ("P813", f"+{retrieved}T00:00:00Z/11"),
    )
