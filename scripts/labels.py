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

import re

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


# --------------------------------------------------------------------------
# THE MARKER VOCABULARY — one set, replacing three
#
# Emma's item said the vocabularies *"should end up as one"*, and there were
# three: this module's, and a copy of a wider set in
# `build-relationship-label-preview.py` and `walk-structural-merge.py`. They are
# folded here because `CLAUDE.md` names this module as the single place that
# decides what a label may be.
#
# **`NOT_A_NAME` above is untouched, and that is the whole point.** Two different
# questions were being conflated. `NOT_A_NAME` decides what `label_for()`
# **empties**, and Emma has ruled on it twice — `Private` and `<private>` and
# nothing else. The sets below decide what a **marker** is, for finding and
# normalising labels that carry one. Widening detection is not widening
# suppression: an `unknown Bloomfield` is detected here and still keeps a label,
# it just becomes `NN Bloomfield` instead of reading as a name.
# --------------------------------------------------------------------------

#: The forms all three vocabularies already agreed on.
NARROW_MARKERS = _NN_FORMS | {"private", "<private>"}

#: Words meaning *unknown*, in any language. **Emma's ruling, 2026-08-17: words
#: yes, punctuation no.** Somebody who typed a word meaning *I don't know* is
#: making the statement `NN` makes.
#:
#: The nine non-English forms were found by **measurement**: ranking every label in
#: the corpus by how many *different* people carry it, where a real name repeats a
#: little and a placeholder repeats hundreds of times. Bulgarian `Без име` sat
#: above most genuine names at 52 people. Counts are in the corpus.
#: A stillborn description, removed as a phrase by `strip_markers`. The optional article and
#: the optional kinship word after it are part of the description, not part of a name:
#: `En dödfödd son`, `Dødfødt`, `Stillborn daughter 2`, `Stillborn Twins`.
#:
#: **The stillborn word itself is required**, which is what keeps `En Olsen` a real name.
_STILLBORN_PHRASE = re.compile(
    r"\b(?:en|ett|et|a|the)\s+(?=\S*(?:d[öo]df|d[øo]df|stillborn))"
    r"|\b(?:d[öo]df[öo]dd?t?|d[øo]df[øo]dt?|stillborn)"
    r"(?:\s+(?:son|s[øo]nn|sen|datter|dotter|daughter|child|barn|twins?|infant|baby))?"
    r"(?:\s+\d+)?\b", re.I)

WORDS_MEANING_UNKNOWN = {
    # **Stillborn is a DESCRIPTION, not a name.** Emma, 2026-08-30, on `Q141224141`:
    # *"please stop trying to assign names to this person who does not in fact have any names
    # at all."* Geni records him as `En dödfödd son Bielke` -- Swedish for *a stillborn son* --
    # and the batch emitted `P735` given name `En` with `P7452` *usual forename*, so the
    # indefinite article became his first name.
    #
    # **505 people in `display-names.csv` carry one of these**: `dødfødt` 216, `stillborn` 148,
    # `dödfödd` 116, `dödfött` 21, `dødfød` 4. Her standing rule -- § *An obvious unknown-word
    # marker goes straight in* -- covers this without asking.
    "unknown",        # 2,127
    "ukjent",         #   188  Norwegian
    "no name",        #    92
    "name not known", #    45  Emma, 2026-08-18, asked which of two phrases the
                      #        mononym census turned up were markers: "Both are
                      #        markers". This one slipped through only because
                      #        matching is whole-label and exact, so the `not
                      #        known` already listed never fired on the longer
                      #        phrase.
    "unknown wife",   #    37  A description of a relationship rather than a name,
                      #        and her ruling puts it here: not a `P735` given
                      #        name, `NN` in `mul`, descriptive labels elsewhere.
    "без име",        #    52  Bulgarian / Macedonian
    "ukendt",         #    18  Danish
    "okänd",          #    17  Swedish
    "not known",      #    15
    "desconocida",    #    13  Spanish
    "desconocido",
    "inconnu",        #     9  French
    "inconnue",       #     4
    "неизвестна",     #     6  Russian
    "неизвестно",
    "unbekannt",      #     6  German
    "ignota",         #     3  Italian
    "ignoto",
    "noname",         #     3
    "佚名",            #     3  Chinese
    "onbekend",       #     1  Dutch
    "namn okänt",     #        Swedish
    "(no name)",
    "ukj.",           #        Norwegian, abbreviating ukjent
    "未知",            #   204  Chinese, "unknown" — Emma, 2026-08-18: "Ukjent and
                      #        未知 get the mul NN treatment". `ukjent` was already
                      #        here at 188; this one was the gap, and it was found
                      #        by the mononym census ranking it among Anna and Lars.
    "未詳",            #     1  Japanese, "details unknown"
    "無名",            #        Japanese / Chinese, "nameless"
    "某",              #   252  Chinese, "a certain one" -- the exact sense of `NN`.
                      #        Emma, 2026-08-19, asked whether it belonged here
                      #        beside 未知 and ukjent: *"Add it"*. It is the whole
                      #        given name on 252 Han-only records and there is no
                      #        surname 某 and no given name containing it, so it
                      #        never collides with a real name.
}

#: Punctuation, a marker **only as the whole label** — the other half of her
#: ruling. `George Clark, II - farmer` is prose and `Nechama (?) Heller` is a name
#: with a bracketed hole; neither is rewritten. A label that is *nothing but*
#: punctuation has no name in it, which `derive-labels.ABSENT` has always said.
PUNCTUATION_MARKERS = {"-", "--", ".", "..", "_", "*", "**", "***", "'",
                       "?", "??", "???", "????"}

#: `n` alone — a marker at the **start** of a label, never inside or at the end.
#: `N Пузына` is a placeholder given name before a real surname, 917 of them;
#: `Laura N` is a **middle initial**, 205, and this repo has already nearly
#: invented 283 of those (`f9b9f86`). Neither a word nor punctuation, so her
#: ruling does not reach it and this is a judgement recorded rather than asked.
SINGLE_LETTER_MARKERS = {"n"}

#: **Words that look like markers and are not**, each measured before exclusion:
#:
#: * `anon` — 89 people, and `Anon Olsen Syverstad` is a Norwegian given name, not
#:   an abbreviation of *anonymous*.
#: * `子` — 2,091 people; it ends ordinary Japanese given names like `多恵子`.
#:
#: Explicit rather than merely absent, so adding either back is an argument
#: somebody has to make.
NOT_MARKERS = {"anon", "子"}

#: Every form that means *absent* when it stands as a whole field or label. This
#: is what the given-name screens want: `PLACEHOLDER_GIVEN` in the preview and
#: `PLACEHOLDER_LABELS` in the structural walk were both copies of a narrower
#: version of this.
PLACEHOLDER_FORMS = (
    {""} | NARROW_MARKERS | WORDS_MEANING_UNKNOWN
    | PUNCTUATION_MARKERS | SINGLE_LETTER_MARKERS
) - NOT_MARKERS


def is_placeholder_form(text: str) -> bool:
    """Whether this whole field or label means *no name here*.

    **A label every component of which is a marker is a marker.** Emma's rule,
    2026-08-18, chosen over listing the spellings one at a time: *"All-marker
    components rule"*. Matching whole labels exactly had let `? ?` (13 rows),
    `N.N. N.N.` (8) and `NN .` (3) through, each of them two markers with a space
    between, while `?`, `n.n.` and `.` were all listed individually.

    The generalisation is what makes it worth having — the next such spelling is
    caught the day it appears rather than after somebody notices it in a batch.

    **It stops exactly where real data starts.** `NN Barba` splits to
    `["nn", "barba"]`, `barba` is not a marker, so the label is not one and the
    surname is not thrown away. That is the 3,605-surname rule in `CLAUDE.md`, and
    `leads_with_a_marker()` below is what the caller uses to handle that case.
    """
    low = (text or "").strip().lower()
    if low in PLACEHOLDER_FORMS:
        return True
    parts = low.split()
    return len(parts) > 1 and all(p in PLACEHOLDER_FORMS for p in parts)


def leads_with_a_marker(text: str) -> bool:
    """Whether a label opens with a marker and continues with something else.

    `NN Hildesheim`, `unknown Bloomfield`, `N Пузына`. The surname after it is real
    data — `CLAUDE.md` records that discarding these loses 3,605 surnames — so the
    caller keeps it rather than collapsing the label to bare `NN`.
    """
    tokens = (text or "").split()
    if len(tokens) < 2:
        return False
    head = tokens[0].strip(",;:()[]").lower()
    if head in NOT_MARKERS:
        return False
    return head in NARROW_MARKERS | WORDS_MEANING_UNKNOWN | SINGLE_LETTER_MARKERS


#: Quote characters a label may be wrapped in. Stripped before matching, because a
#: marker in quotation marks is still a marker: `"unknown"` and `"unbekannt"` were both
#: reading as names, 4 records, found 2026-08-18 while checking Emma's instruction that
#: `unbekannt` be treated as an NN substitute — it already was, and the quoting was what
#: defeated it. Straight and typographic, single and double, plus the European guillemets
#: and the German low-9 forms, since the corpus is Norwegian, German and Swedish.
SURROUNDING_QUOTES = "\"“”‘’«»„‚'"


def is_marker_label(label: str) -> bool:
    """Whether this string is a marker rather than a name, for LABEL emission.

    The one definition. It lived in `walk-structural-merge.py` as
    `is_placeholder_label` and `build-edit-objects.py` had no copy at all, which is
    the whole defect: the same guard was needed at six emission sites across two
    scripts and existed at four of them. Two of the faults already recorded in this
    repo are that shape -- the `ja`/`zh` branch of `walk-structural-merge.py` wrote
    22 edits carrying `未知` because it was not consulting the vocabulary its
    neighbours consulted, and `build-edit-objects.py` still writes `label_en`
    straight into `en` and `mul`. A predicate copied per caller is a predicate that
    will disagree with itself.

    Three tests, in order:

    * `is_placeholder_form` -- the whole label means *no name here*, including the
      all-components case `? ?` and `NN .`.
    * `private` anywhere -- `CLAUDE.md`: *"'Private' is a redaction marker, not a
      name, and an item labelled that asserts something false while being impossible
      to find"*. The marker those people get is `NN` in `mul`.
    * `leads_with_a_marker` -- `NN Hildesheim` opens with a marker and continues
      with a real surname, so the label is not written to a local language, but the
      surname is not thrown away either; that is the 3,605-surname rule.

    **Words yes, punctuation no** for the head test -- Emma, 2026-08-17 -- so
    `. Weill` and `Nechama (?) Heller` are left alone. Punctuation is a marker only
    as the whole label, which is the first test's business.
    """
    low = (label or "").strip().strip(SURROUNDING_QUOTES).strip().lower()
    if not low or is_placeholder_form(low):
        return True
    if "private" in low:
        return True
    return leads_with_a_marker(low)


def is_unnamed(gedcom_name: str) -> bool:
    """True when there is no usable name here — redacted, `NN`, or blank.

    This is what `labels_for()` branches on, and it is **wider than
    `is_redacted()`** on purpose: `NN` is not a redaction, but it is equally not
    a name, and Emma settled on 2026-08-16 that the two get one treatment. It is
    **narrower than suppression**: an unnamed person is still created, still gets
    `NN` in `mul`, and still gets a descriptive `en` where a relative supplies
    one. Nobody is dropped, which is what she objected to when `nn` was quietly
    added to `NOT_A_NAME`.

    **It consults the whole marker vocabulary, not `_NN_FORMS`.** It used to test
    the six `nn` spellings alone, so a person whose entire recorded name was
    `Unknown Wife` — or `Ukjent`, or `未知` — was treated as *named* and their
    marker was written into `mul` **and** `en` as though it were what they were
    called. Five items in `reports/wikidata-orderlife.json` carried
    `Unknown Wife` in both slots that way.

    Emma settled it on 2026-08-18, asked which of two such phrases counted:
    *"Both are markers"*, alongside her earlier *"Ukjent and 未知 get the mul NN
    treatment"*. That treatment is precisely this branch — `NN` in `mul`, a
    descriptive phrase in `en` — so routing these here is what her rule asks for,
    and keeping a second narrower list next to `PLACEHOLDER_FORMS` is the
    duplication this module's *one set, replacing three* note exists against.

    Note this widens **routing**, not suppression: every one of these people is
    still created and still readable through `mul`. That distinction is the one
    she objected to losing when `nn` was quietly added to `NOT_A_NAME`.
    """
    if is_redacted(gedcom_name):
        return True
    return is_placeholder_form(display_name(gedcom_name))


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

    **A marker with a real surname behind it keeps the surname — in `mul` only.**
    `N.N. binti Lubb` and `NN (Wife of Marcus Aemilius Lepidus)` are the shape, and
    they were reaching `en` verbatim, marker and all, on 575 rows. Emma chose the
    split on 2026-08-18: *generated description in `en` instead*, so

        N.N. binti Lubb   ->  mul  NN binti Lubb
                              en   daughter of Lubb        (ours, from relatives)

    `mul` keeps `NN <surname>` because the surname is real data and
    `CLAUDE.md` records that discarding these loses 3,605 surnames. `en` gets the
    phrase this project builds, never Geni's string — which is what stops the
    marker appearing in a local language at all.

    Without a `descriptive` from the caller, `en` is simply absent. That is the
    honest outcome: the item is still readable through `mul`, and inventing an
    English label out of the marker is the thing being prevented.
    """
    if not is_unnamed(gedcom_name):
        name = display_name(gedcom_name)
        if leads_with_a_marker(name):
            rest = " ".join(name.split()[1:]).strip()
            # **A parenthetical is a description, not a surname.**
            # `NN (Wife of Marcus Aemilius Lepidus)` carries no family name at all
            # — somebody wrote the relationship into the name field. Her model for
            # `mul` is `NN` or `NN <surname>`, so a bracketed phrase is dropped
            # rather than promoted into the multilingual label, and the same fact
            # reaches `en` properly through `descriptive`.
            if rest.startswith("(") and rest.endswith(")"):
                rest = ""
            out = {"mul": f"{UNNAMED_MARKER} {rest}".strip()}
            if descriptive.strip():
                out["en"] = descriptive.strip()
            return out
        label = label_for(gedcom_name)
        if label:
            return {"mul": label, "en": label}
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




#: A middle initial: an UPPERCASE Latin letter, or any single letter carrying a full stop.
#:
#: **A bare lowercase letter is a word, not an initial.** `^[A-Za-z]\.?$` was the first version
#: and it turned `Ragnhild Toresdatter Håland i Gjesdal` into
#: `ラグンヒル・トーレスダッテル・ホーランド・I・イェスダール` — Norwegian `i` means *in*, so a
#: preposition was upper-cased into somebody's initial and planted in a Japanese label. Found by
#: reading the emitted batch, not by reasoning about the rule.
INITIAL_RE = re.compile(r"^(?:[A-Z]|[A-Za-z]\.)$")


def transliterate_token(token, table):
    """`(ja, zh)` for one name token, or `(None, None)` if it cannot be rendered.

    **An initial keeps its Latin letter in every language.** Emma, 2026-08-27, asked what
    `John F. Smith` should become in Japanese and Chinese: *keep it Latin inside the label* —
    ジョン・F・スミス, 约翰·F·史密斯. The alternatives she was shown and did not take were
    dropping it (loses information the Latin label carries) and transliterating the letter as
    エフ (invents a reading nobody uses).

    This is the ONE exception to *partial is worse than absent*, and it is not really a
    partial: the initial is not a name being half-rendered, it is a letter that is the same
    letter in every script. 12,805 tokens sit in the middle-initial position across the
    corpus, and every name containing one was getting no `ja`/`zh` label at all.
    """
    pair = table.get(token)
    if pair:
        return pair[0], pair[1]
    if INITIAL_RE.match(token or ""):
        # **Never change case.** `.upper()` was here and it is what made Norwegian `i` read as
        # an initial `I`; an initial that is already capitalised needs no help, and one that is
        # not is not an initial.
        letter = token.rstrip(".")
        return letter, letter
    return None, None


#: The two forms Geni uses to say *this name is withheld*, as opposed to *this name is unknown*.
#: `CLAUDE.md` § *Redacted people go in* counts them: `Private` **99,645** and
#: `<private> /Surname/` **19,945** across the corpus.
REDACTION_MARKERS = {"private", "<private>"}


def normalise_marker_spelling(label: str) -> str:
    """`strip_markers`, but **never touching a redaction marker**.

    **The screen exists because one call decides two different questions.** Applying
    `strip_markers` to every `mul` label would change **102,284** of them, measured 2026-08-31 --
    and **94,231** are `Private` or `<private>` becoming `NN`, which is a decision about
    redaction rather than about spelling. Two sections of `CLAUDE.md` can be read against each
    other on it: § *Redacted people go in* has `label_for()` empty `Private` and `<private>`
    **and nothing else**, while § *`NN` is PRESERVED in `mul`* has `Private` and `NN` as one
    population getting the same treatment. Emma has corrected an attempt to settle that twice,
    once sharply -- *"I didn't tell you to do that. I didn't tell you to avoid the NN people."*
    So it stays hers.

    What is left is uncontroversial and is what the queue item actually wanted: **6,515** labels
    where the marker is written inconsistently -- `nn`, `N.N.`, `unknown`, `ukjent`, `某`,
    `dødfødt` -- and `NN` is the form `CLAUDE.md` already says the marker takes.

    A label whose FIRST token is a redaction marker is returned untouched, so
    `Private Paulson` stays exactly as Geni wrote it and `nn Gunnarsdatter Frafjord` becomes
    `NN Gunnarsdatter Frafjord`.
    """
    first = (label or "").split()
    if first and first[0].casefold().strip(".,") in REDACTION_MARKERS:
        return label
    return strip_markers(label)


def strip_markers(label: str) -> str:
    """Normalise an unknown-name marker to `NN`. **Never delete it.**

    **Emma, 2026-08-27**, on `Q141198538`: *"clearly has 'nn' as its first name however it was
    not produced as an NN person, so what happened, can you please fix the algorithm so it does
    no do this in the future?"* Geni records her as `nn Gunnarsdatter /Frafjord/` — the marker
    sits inside `GIVN`, in front of a real patronymic — and the label went out as
    `nn Gunnarsdatter Frafjord`, reading as a name.

    **The marker stays.** `CLAUDE.md` § *`NN` is PRESERVED in `mul`* is explicit — *"NN is always
    preserved in the multi-language label. It just has more descriptive labels added in some
    languages for the relationships"* — and its worked example is exactly this shape:

        mul  NN Garborg                              <- marker where the unknown part is
        en   son of Arne Olaus Fjørtoft Garborg      <- formulaic, from the nearest relative

    So `nn Gunnarsdatter Frafjord` becomes **`NN Gunnarsdatter Frafjord`**, and `Sara NN` — given
    name known, surname unknown — is already right and is left alone but for the case.

    **This replaces a deletion that ran for part of 2026-08-27 and was wrong both ways.** It
    turned `nn Gunnarsdatter Frafjord` into `Gunnarsdatter Frafjord` and `Sara NN` into `Sara`,
    each of which asserts a name the person is not recorded as having, and each of which erases
    the one thing the record actually says: that part of the name is unknown. A bare surname is
    explicitly not a label — § *Redacted people go in. `Private` never becomes a label*.

    A label that is nothing but markers collapses to the bare marker `NN`.

    **A stillborn DESCRIPTION is removed whole, article and kinship word included.** Emma,
    2026-08-30, on `Q141224141`: *"please stop trying to assign names to this person who does
    not in fact have any names at all."* Geni records him `En dödfödd son Bielke` — Swedish for
    *a stillborn son* — and the batch emitted `P735` given name `En`, the indefinite article,
    carrying `P7452` *usual forename*.

    Word-by-word marking cannot fix that: it gives `NN NN son Bielke`, because `son` sits
    between the two markers and survives. And putting a bare `en` in the marker set turns
    `En Olsen` into `NN Olsen`, swallowing a real name. So the phrase goes as a phrase, and
    only where a stillborn word actually appears.
    """
    # The phrase becomes the MARKER, not nothing: a person with no name still gets `NN`,
    # and `CLAUDE.md` is explicit that a bare surname is not a label. `En dodfodd son
    # Bielke` -> `NN Bielke`. The collapse below folds a run of markers into one.
    label = _STILLBORN_PHRASE.sub(" " + UNNAMED_MARKER + " ", label or "").strip() or label
    # The pattern can match twice on one phrase -- the article, then the word -- giving
    # `NN NN Bielke`. A run of markers is one marker.
    _t = label.split()
    label = " ".join(t for i, t in enumerate(_t)
                     if not (t == UNNAMED_MARKER and i and _t[i - 1] == UNNAMED_MARKER))
    tokens = (label or "").split()
    if not tokens:
        return label
    markers = NARROW_MARKERS | WORDS_MEANING_UNKNOWN
    out, seen_marker = [], False
    for tok in tokens:
        if tok.casefold().strip(".,") in markers:
            # **Collapse a run of markers to one, so `NN NN Garborg` is not a thing.**
            #
            # The condition was `if not seen_marker or out`, which appends whenever `out` is
            # non-empty -- almost always -- so a run of two DIFFERENT markers survived as two.
            # `nn N.N. Countess of Worms` came out `NN NN Countess of Worms`, and the function
            # was not idempotent: running it twice gave a different answer from running it once.
            # **24 people carried a doubled marker**, found by asserting the fixpoint over
            # `derived-labels.csv` rather than by reading the loop.
            #
            # Looking at the previous EMITTED token is what the comment always described.
            if not out or out[-1] != UNNAMED_MARKER:
                out.append(UNNAMED_MARKER)
            seen_marker = True
        else:
            out.append(tok)
    if all(x == UNNAMED_MARKER for x in out):
        return UNNAMED_MARKER
    return " ".join(out)



def drop_marker_surname(label: str, *surnames: str) -> str:
    """Strip a trailing unknown-name marker that Geni put in the SURNAME field.

    **Emma, 2026-08-29**, shown `Q141217396` labelled *Maria No name*:
    *"I would say I just use it by its first name."* So `Maria /No name/` is labelled
    **Maria** -- the given name alone -- and the marker never reaches a label, which is the
    same rule as `Private`.

    **Why `is_marker_label` did not already catch it, because the gap is specific.**
    That predicate tests the WHOLE label, or a LEADING marker: `unknown Bloomfield` is
    `True`, `Bloomfield unknown` is `False`. Geni writes the marker into `SURN`, which lands
    at the END, and that position was never tested. The vocabulary was never the problem --
    `no name` has been in `WORDS_MEANING_UNKNOWN` all along. Emma: *"I'm not sure how it is
    that no name didn't get through our detection thing, because that seems like such an
    obvious one."*

    **2,167 people in the corpus carry this shape**, and exactly one of them had reached
    Wikidata when it was found (`reports/marker-surname-audit.tsv`).

    This does not empty the label the way a fully-redacted person's is emptied -- the given
    name is real and survives. A person left with nothing after the strip keeps their label
    unchanged, so the caller's existing marker handling still decides that case.
    """
    if not label:
        return label
    tokens = label.split()
    for surname in surnames:
        surname = (surname or "").strip()
        if not surname or not is_marker_label(surname):
            continue
        tail = surname.split()
        if len(tokens) > len(tail) and [t.casefold() for t in tokens[-len(tail):]] == [
                t.casefold() for t in tail]:
            tokens = tokens[:-len(tail)]
    # **The surname fields are not always populated**, and the marker is still there.
    # `Segrid /NN/` reaches the batch with an empty `SURN` and `_MARNM`, so there was no
    # string to match against and the marker survived into `Lmul "Segrid NN"`. So: failing a
    # field match, strip trailing tokens that are markers in their own right. A name is never
    # only its last token, so the guard is simply that something real must remain.
    while len(tokens) > 1 and is_marker_label(tokens[-1]):
        tokens = tokens[:-1]

    return " ".join(tokens) if tokens else label
