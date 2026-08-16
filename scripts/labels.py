"""Turning a Geni `NAME` into a Wikidata label, and refusing the ones that aren't.

**A redaction marker is not a name.** Geni writes `1 NAME Private` for a profile
it will not show, and `NN` for one recorded without a name. Neither is what the
person is called, and an item labelled "Private" asserts something false about
them while being useless to find.

**A redacted person is NOT left unlabelled either.** Emma, 2026-08-16: *"NN is
always preserved in the multi-language label. It just has more descriptive labels
added in some languages for the relationships."* — and, in the same message,
*"NN and private are the same thing here, because if there's a private individual
whose name is not exported, it comes out as an NN."* So `Private` and `NN` are one
population reached by two routes and take one treatment:

    mul  NN                       <- the marker, always present, never a person's name
    en   daughter of Gerard Spencer   <- descriptive, from a named relative

**Emptying the label was half the rule and the wrong half.** Until 2026-08-16
`label_for` returned `''` for `Private` and every caller wrote that straight into
both `en` and `mul`, so **1,109 order.life creations** were set to be created with
no label in any language. An item labelled "Private" asserts something false; an
item labelled nothing at all cannot be read or found, which is the same objection
this module exists to raise. `labels_for()` is the function callers should use;
`label_for()` remains the narrow "is this string a name" test it always was.

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

#: **What goes in `mul` for anybody with no usable name.** *nomen nescio* — the
#: genealogist's marker, and the one Wikidata already carries on 1,588 items in
#: this slice. A redacted Geni profile and an `NN` Geni profile are the same
#: person-shaped hole and get the same marker; see the module docstring.
UNNAMED_MARKER = "NN"

def is_redacted(gedcom_name: str) -> bool:
    """True for either of Geni's redaction markers."""
    raw = (gedcom_name or "").lower()
    return (GIVEN_REDACTED in raw
            or display_name(raw).strip() == "private")

#: The `NN` spellings that mean *nomen nescio*. **Deliberately narrow** — it does
#: not include `unknown` or `?`, which Emma refused when they were added to
#: `NOT_A_NAME` unasked, and which are somebody's editorial choice rather than a
#: marker this project owns.
_NN_FORMS = {"nn", "n n", "n.n.", "n. n.", "n.n", "n-n"}


def is_unnamed(gedcom_name: str) -> bool:
    """True when there is no usable name here — redacted, `NN`, or blank.

    This is what `labels_for()` branches on, and it is **wider than
    `is_redacted()`** on purpose: `NN` is not a redaction, but it is equally not
    a name, and Emma settled on 2026-08-16 that the two get one treatment. It is
    **narrower than suppression**: an unnamed person is still created, still gets
    `NN` in `mul`, and still gets a descriptive `en` where a relative supplies
    one. Nobody is dropped, which is what she objected to when `nn` was quietly
    added to `NOT_A_NAME`.
    """
    if is_redacted(gedcom_name):
        return True
    return display_name(gedcom_name).strip().lower() in _NN_FORMS | {""}


def labels_for(gedcom_name: str, descriptive: str = "") -> dict[str, str]:
    """The `mul` and `en` labels for this Geni name.

    A named person carries their name in both. An unnamed or redacted one carries
    `NN` in `mul` — always, whether or not anything else is known — and the
    caller's `descriptive` string in `en`, which is a relationship phrase such as
    `"daughter of Gerard Spencer"`.

    `descriptive` is the caller's job because it needs relatives, which this
    module does not see. Omitting it leaves `en` unset rather than empty: the item
    is still readable through `mul`, and a later pass can fill `en` in.

    **`en` never falls back to the raw string.** That is the "Private" label this
    module exists to stop, and it is why the marker goes in `mul` instead of
    leaving the item blank enough to tempt someone into it.
    """
    if not is_unnamed(gedcom_name):
        name = label_for(gedcom_name)
        if name:
            return {"mul": name, "en": name}
    out = {"mul": UNNAMED_MARKER}
    if descriptive.strip():
        out["en"] = descriptive.strip()
    return out


#: The relationship words, by the sex of the person being named. Unknown sex takes
#: the neutral form rather than a guess.
AS_CHILD = {"M": "son", "F": "daughter", "": "child"}
AS_SPOUSE = {"M": "husband", "F": "wife", "": "spouse"}
AS_PARENT = {"M": "father", "F": "mother", "": "parent"}


def describe(sex: str, relation: str, other: str) -> str:
    """`describe("F", "parent", "Gerard Spencer")` -> `"daughter of Gerard Spencer"`.

    `relation` is what the *other* person is to them: `parent`, `spouse`, `child`.
    Returns `''` when the other person has no usable name, so a caller can fall
    through to the next candidate rather than emitting `"mother of NN"`, which
    names nobody.
    """
    words = {"parent": AS_CHILD, "spouse": AS_SPOUSE, "child": AS_PARENT}[relation]
    other = (other or "").strip()
    if not other or other.strip().lower() in ("nn", "n n", "n.n.", "private",
                                              "unknown", "?"):
        return ""
    return f"{words.get(sex, words[''])} of {other}"


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


