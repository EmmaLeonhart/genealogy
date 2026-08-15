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

**There are TWO markers and they redact different amounts.** Measured over the
corpus, 2026-08-14, of 390,560 profiles:

| form | count | what survives |
| --- | ---: | --- |
| `Private` | **16,402** | nothing; the whole name is gone |
| `<private> /Surname/` | **3,605** | **the surname is real data** |
| `NN` or blank | 772 | nothing |

`<private> /HUÁNG 黃/`, `<private> /Rådestad/`, `<private> /KOESOEMAH ADINATA/`,
`<private> /Larsson/` — Geni withholds the **given name** and leaves the family
name. Treating those as fully redacted throws away 3,605 surnames, which is
exactly the material Emma called valuable: *"these private names are still worth
inclusion because they still do flush out the wiki data, and they flush it out by
a substantial amount."*

So `<private>` is stripped rather than rejected, and `surname_of()` exposes what
is left. A bare surname is **not** a person's label — it is the input to the
`P734` family-name work in `todo.md`, which needs surname items to link to.

This is the same rule as the two Samaritan "wives" in `docs/future-modelling.md`
— `daughter of Sanballat the Horonite` is a description, not a name — with one
difference that decides the outcome. Those two have no identifier and no
structure, so there is nothing to create. A `Private` profile has both.
"""

from __future__ import annotations

#: **Only Geni's redaction markers, and only because Emma named them.**
#:
#: An earlier version of this set also held `nn`, `n n`, `unknown` and `?`. Emma,
#: 2026-08-14: *"I didn't tell you to do that. I didn't tell you to avoid the NN
#: people."* She specified `Private` and `<private>`; the rest was added here
#: unasked and silently suppressed labels on people nobody had decided about.
#:
#: `NN` is *nomen nescio* — a genealogist recording that the name is unknown. It
#: is a real thing to say about a person, and it is not Geni withholding data.
#: Whether it should become a Wikidata label is a decision, and not one to make
#: by quietly adding a string to a set.
NOT_A_NAME = {"private", ""}

#: The given-name marker. Unlike `Private`, what follows it is real.
GIVEN_REDACTED = "<private>"


def display_name(gedcom_name: str) -> str:
    """`Yoseph II /ben Ab-Hisda/` -> `Yoseph II ben Ab-Hisda`; `//` -> `''`."""
    return " ".join((gedcom_name or "").replace("/", " ").split())


def surname_of(gedcom_name: str) -> str:
    """The `/.../` slot, `''` if empty.

    `.` is dropped here and only here: `<private> /./` occurs 286 times and a
    lone full stop is not a family name to link a P734 item to. That is a
    judgement about this one string, not a general rule about placeholders.
    """
    parts = (gedcom_name or "").split("/")
    surname = " ".join(parts[1].split()) if len(parts) > 2 else ""
    return "" if surname.strip() in ("", ".") else surname


def label_for(gedcom_name: str) -> str:
    """The Wikidata label for this Geni name, or `''` if it must not have one.

    Returning empty is deliberate and must stay distinguishable from "not
    looked up": a caller that falls back to the raw string on empty reintroduces
    exactly the "Private" labels this exists to stop.

    A `<private>` given name leaves only a surname, and a bare surname is not a
    label for a person — so that returns `''` too, and the surname is carried by
    `surname_of()` instead of being smuggled into the label.
    """
    raw = (gedcom_name or "")
    if GIVEN_REDACTED in raw.lower():
        return ""
    name = display_name(raw)
    return "" if name.strip().lower() in NOT_A_NAME else name


def is_redacted(gedcom_name: str) -> bool:
    """True for either of Geni's redaction markers."""
    raw = (gedcom_name or "").lower()
    return (GIVEN_REDACTED in raw
            or display_name(raw).strip() == "private")
