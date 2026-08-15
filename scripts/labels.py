"""Turning a Geni `NAME` into a Wikidata label, and refusing the ones that aren't.

**A redaction marker is not a name.** Geni writes `1 NAME Private` for a profile
it will not show, and `NN` for one recorded without a name. Neither is what the
person is called, and an item labelled "Private" asserts something false about
them while being useless to find.

**The person still goes in.** Emma, 2026-08-14: *"Even if the data is affected by
redaction, I'm not really that against the data getting onto Wikidata because it
still is informative, like the so-called private names."* The informative part is
the structure — the Geni ID, the sex, the parents and children — and none of that
is redacted. So these items are created **without a label**, carrying `P2600` and
their relationships. The Geni ID is what makes them retrievable.

Measured over the corpus, 2026-08-14: **16,402 profiles named exactly `Private`**
out of 390,560, plus **772** `NN` or blank. 4.2%.

This is the same rule as the two Samaritan "wives" in `docs/future-modelling.md`
— `daughter of Sanballat the Horonite` is a description, not a name — with one
difference that decides the outcome. Those two have no identifier and no
structure, so there is nothing to create. A `Private` profile has both.
"""

from __future__ import annotations

#: Values Geni uses in the NAME slot that are not names.
NOT_A_NAME = {"private", "nn", "n n", "unknown", "?", ""}


def display_name(gedcom_name: str) -> str:
    """`Yoseph II /ben Ab-Hisda/` -> `Yoseph II ben Ab-Hisda`; `//` -> `''`."""
    return " ".join((gedcom_name or "").replace("/", " ").split())


def label_for(gedcom_name: str) -> str:
    """The Wikidata label for this Geni name, or `''` if it must not have one.

    Returning empty is deliberate and must stay distinguishable from "not
    looked up": a caller that falls back to the raw string on empty reintroduces
    exactly the "Private" labels this exists to stop.
    """
    name = display_name(gedcom_name)
    return "" if name.strip().lower() in NOT_A_NAME else name


def is_redacted(gedcom_name: str) -> bool:
    """True for Geni's redaction marker specifically, not merely unnamed."""
    return display_name(gedcom_name).strip().lower() == "private"
