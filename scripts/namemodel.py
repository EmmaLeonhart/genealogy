"""Split a Norwegian name into the properties `name modelling.txt` asks for.

Emma, 2026-08-24, on the Garborg batches: *"we should be modelling the names
properly, which he didn't do."* The batches carried labels and no `P735`, `P734` or
`P5056` at all.

**Her model, from `name modelling.txt`, not invented here:**

    P735  given name            first token, + P1545 ordinal 1
                                                + P7452 -> Q3409033 usual forename
    P735  given name            later tokens, + P1545 ordinal n
                                              + P3831 -> Q245025 middle name
    P5056 patronym or matronym  a -sen/-son/-datter token, its own property
                                and NOT a P735 with a qualifier
    P734  family name           the last token

`CLAUDE.md`: *"A middle name is a given name after the first that is NOT a
patronymic."* So the order of the tests matters — patronymic first, then position.

**Both fields, always — and that means READING the fields.** Until 2026-08-24 this
module took `label_en`, a rendered display string, and guessed by whitespace position.
Emma caught it: *"I thought we were resolving name objects but now we're determining
which name field to use as a source of the label?"* The GEDCOM fields are in
`reports/display-names.csv` — `givn`, `surn`, `nick`, `marnm` — and the label is a
separate output that happens to describe the same person.

What positional parsing got wrong, on four real people:

* `surn` is **recorded**; the parser inferred it as "the last token unless it looks
  patronymic". Agreeing by luck is not the same as reading it.
* `Stine "Stena" Eivindsdatter` → *Stena* came out a second given name carrying
  `P1545` *series ordinal* 2 and `P3831` → `Q245025` *middle name*. It is a nickname.
* `marnm` was never read at all, so Stena's *Jacobson* and Inger Marie's *Ronneberg*
  did not exist to the model.

**Emma's rulings, 2026-08-24.** A quoted token inside `givn` becomes `P1449`
*nickname*. A `_MARNM` becomes a **second** `P734` *family name*, emitted only where it
differs from `surn` and where `surn` is actually populated.

**Sex screens the ROLE, not the statement.** She first said sex was not a screen, then
corrected on seeing a man carrying `Q28418670` *married name*: *"ontologically married
name on a man means more like adopted surname. So men's 'married names' should not have
the role of married name."* So a man still gets the second `P734`; it simply carries no
`P3831` role. Not `Q118383793` *adoptive name* either — in this material the second
surname is usually a **farm name** taken by residence, and `Q141169072` is the case:
*Ådne Olsen Grøtheim* became *Ådne Olsen Garborg* by moving to the Garborg farm.

**CJK stays out of scope and is a known hazard.** `CLAUDE.md` records `SURN` holding a
place name (`陳郡陽夏`) while `_MARNM` held the real clan name. Reading `surn` as a
surname is right for this material and is not established corpus-wide.

**Nothing is guessed.** A token's item comes from `reports/name-item-plan.csv`, which
carries `existing_qid` where Wikidata already has one and `create` where it does not.
A token the plan calls `AMBIGUOUS` is **emitted as a note and never as a statement** —
that is the `Maria` case, where nine items exist and only the person's sex separates
the two that matter.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

#: `CLAUDE.md` § Wikidata properties and items. Written out so a reader never meets
#: a bare Q-number.
GIVEN_NAME = "P735"          # given name
FAMILY_NAME = "P734"         # family name
PATRONYM = "P5056"           # patronym or matronym
SERIES_ORDINAL = "P1545"     # series ordinal
PREFERRED_REASON = "P7452"   # reason for preferred rank
USUAL_FORENAME = "Q3409033"  # usual forename
HAS_ROLE = "P3831"           # object of statement has role
MIDDLE_NAME = "Q245025"      # middle name
PATRONYMIC_CLASS = "Q110874"  # patronymic
NICKNAME = "P1449"           # nickname
BIRTH_NAME_ROLE = "Q2507958"   # birth name
MARRIED_NAME_ROLE = "Q28418670"  # married name

#: `-sen`, `-son`, `-sson`, `-datter`, `-sdatter`. Emma, on the Norwegian material:
#: *"The daughter and son would be the same thing"* — one category, not two.
#: **`dotter` is the Swedish form and was missing.** `datter` is Norwegian and Danish;
#: `-dotter` is Swedish and means the same thing. Leaving it out classified **60,085 people**
#: as carrying a family name -- `Johansdotter` 5,612 bearers, `Andersdotter` 5,472,
#: `Olofsdotter` 3,157, `Nilsdotter` 2,868 -- when every one is a patronymic.
#:
#: The disagreement was internal: `scripts/build-name-item-batch.py`'s `RELIABLE_PATRONYMIC`
#: has listed `dotter` and `sdotter` all along, so the plan builder and the classifier have
#: been reading the same token two different ways. Found because `PATRONYMIC_PARTS` below
#: included it and this did not, and the father test disagreed with itself on
#: `Jakobsdotter`.
PATRONYMIC = re.compile(r".+(sen|son|sson|datter|sdatter|dotter)$", re.I)

#: A token wholly inside brackets, as Geni writes an alternative or a house:
#: `Turesson (Bielke)`, `Weirman (Weyerman)`, `Levine (?)`.
PAREN = re.compile(r"^\((.+)\)$")

#: **Particles and honorifics go into the LABEL and never become items.** Emma, 2026-08-26:
#: *"These should be parts of the mul labels because they are integral parts of what the
#: people are called."* The nine bracketed ones are the whole bracketed population measured in
#: `reports/paren-tokens.md`; the unbracketed forms are far commoner -- bare `de` occurs
#: **125,328** times and bare `von` 60,951 -- and until now every one of them became a `P734`
#: *family name* lookup of its own.
PARTICLES = {
    "de", "d.", "du", "des", "del", "della", "di", "da", "das", "dos", "van", "von",
    "vander", "le", "la", "el", "af", "av", "ap", "ben", "ibn", "bin", "mac", "mc",
    "st.", "san", "santa", "dom", "don",
}

#: **Words meaning the name is not known.** They join `Private`/`NN`/`Ukjent`, which
#: `scripts/labels.py` owns -- `CLAUDE.md` § *`NN` is PRESERVED in `mul`*. Emma, 2026-08-26,
#: shown `(anonyma)`, `(incognita)` and `(?)`: *"Treat as NN markers."*
#:
#: **`ben` is in `PARTICLES`, not here.** It is the Samaritan patronymic particle --
#: `Abisha III ben Phinhas` -- so it belongs in the label and must never become a `P734`
#: *family name* item of its own, which is what it used to do.
UNKNOWN_MARKERS = {
    "?", "??", "???", "anonyma", "anonymus", "anonym", "incognita", "incognito",
    "okänd", "ukjent", "ukendt", "unknown", "n.n.", "nn", "no name", "namn okänt",
}


def name_shape(token):
    """`(bare_token, usage_or_None)` -- brackets stripped, particles and markers named.

    Emma's rulings of 2026-08-26, `CLAUDE.md` § *A parenthesised token in `SURN`/`_MARNM` is
    THREE different things*. A `usage` of `None` means "an ordinary name token, carry on";
    `particle` and `unknown` are terminal and never reach the name plan.

    The brackets are stripped whether or not the token is a particle, because
    `(de) Worms` and `de Worms` are the same name written twice.
    """
    m = PAREN.match(token)
    bare = m.group(1) if m else token
    low = bare.casefold()
    if low in UNKNOWN_MARKERS:
        return bare, "unknown"
    if low in PARTICLES:
        return bare, "particle"
    return bare, None


def load_plan(path: Path | None = None) -> dict:
    """(token, usage) -> (existing_qid or '', action).

    `reports/ambiguous-names-resolved.tsv` is overlaid on top, where it has an answer.
    Those are the tokens the plan marks AMBIGUOUS and therefore refuses to emit;
    `scripts/resolve-ambiguous-names.py` settles them by the bearer's sex (Emma's rule)
    and then by which candidate's `mul` label is the token itself, which is what
    separates the Russian `Мартин` from the Latin `Martin`. A token it cannot settle
    stays AMBIGUOUS and is still not emitted.
    """
    path = path or ROOT / "reports" / "name-item-plan.csv"
    out = {}
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[(row["token"], row["usage"])] = (
                (row.get("existing_qid") or "").strip(),
                (row.get("action") or "").strip(),
            )

    resolved = ROOT / "reports" / "ambiguous-names-resolved.tsv"
    if resolved.exists():
        with open(resolved, encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                qid = (row.get("qid") or "").strip()
                if qid:
                    out[(row["token"], "given")] = (qid, "link (ambiguity resolved)")
    return out


#: A token Geni wrapped in quotes inside `GIVN` — `Stine "Stena" Eivindsdatter`.
QUOTED = re.compile(r'["“”\'](?P<token>[^"“”\']+)["“”\']|\((?P<paren>[^)]+)\)')


#: A `-sen`/`-son`/`-datter` token, split into stem and suffix.
PATRONYMIC_PARTS = re.compile(r"^(.+?)(sen|son|sson|datter|sdatter|dotter)$", re.I)


def patronymic_or_surname(token: str, father_name: str) -> str:
    """`"patronymic"` or `"family"` for a `-sen`/`-son` token, using the FATHER.

    **Emma's test, 2026-08-26:** *"If father has -son or -sen then it's a surname lol that's
    the test same with other patronymic surnames."*

    **The literal reading of that is 91% wrong** and measuring it is what caught it. In a
    patronymic-naming society the father almost always carries one too: `Einar Jonsen Vestad`
    has father `John Kristiansen Jevne`, and `Maria Christina Jakobsdotter` has father `Jakob
    Jakobsson`. Both are textbook patronymics, and "father has a `-sen`" is true of nearly
    everybody, so it discriminates nothing.

    **What discriminates is whether the father carries the SAME token.** Over the 286,536
    people who have such a token and a known father:

    | | tokens | share |
    | --- | ---: | ---: |
    | father has the same token -> inherited **surname** | 40,872 | 14% |
    | stem matches the father's **given** name -> **patronymic** | 213,898 | 75% |
    | neither -> undecided, kept as patronymic | 31,766 | 11% |

    `James Slawson` son of `James Slawson`, whose children are all `Slawson`, is the surname
    case. `John Kristiansen` son of `Kristian` is the patronymic case. The undecided 11% are
    mostly spelling variants -- `Jonsen`/`John`, `Jakobsdotter`/`Jacob` -- and they keep
    today's morphological answer rather than being guessed at the other way.

    Without a father this returns `"patronymic"`, which is the behaviour every existing caller
    already has.
    """
    if not father_name:
        return "patronymic"
    parts = [t for t in re.split(r"\s+", father_name.strip()) if t]
    fathers_patronymics = {t.casefold() for t in parts if PATRONYMIC.match(t)}
    if token.casefold() in fathers_patronymics:
        return "family"
    m = PATRONYMIC_PARTS.match(token)
    if not m:
        return "patronymic"
    stem = m.group(1).casefold().rstrip("s")
    givens = [t.casefold() for t in parts if not PATRONYMIC.match(t)]
    for given in givens:
        g = given.rstrip("s")
        if g == stem or (len(stem) >= 4 and g.startswith(stem[:4])):
            return "patronymic"
    return "patronymic"


def classify_fields(givn: str, surn: str, nick: str = "",
                    marnm: str = "", father_name: str = "") -> list[tuple[str, str, int]]:
    """`(token, usage, ordinal)` from the GEDCOM name FIELDS.

    This is the one to call. `classify()` below takes a rendered label and survives
    only for callers that have nothing else; it guesses where this reads.

    Usages emitted:

    * `given`      — a `GIVN` token that is not quoted and not patronymic
    * `patronymic` — a `-sen`/`-son`/`-datter` token, **from either field**
    * `family`     — `SURN`, the birth family name
    * `married`    — `_MARNM`, only where it differs from `SURN`
    * `nickname`   — a quoted token inside `GIVN`, or the `NICK` field

    Emma, 2026-08-24, on the quoted case: it becomes `P1449` *nickname*, not a given
    name and not a middle name. `Stena` is what `Stine` was called, not her second
    forename.

    The married name carries no ordinal. Sex does not decide whether it is emitted --
    it decides only whether the `P3831` role says *married name*; see `statements_for`.
    """
    out: list[tuple[str, str, int]] = []

    raw_givn = givn or ""
    nicknames = [m.group("token") or m.group("paren")
                 for m in QUOTED.finditer(raw_givn)]
    plain = QUOTED.sub(" ", raw_givn)

    ordinal = 0
    for token in [t for t in re.split(r"\s+", plain.strip()) if t]:
        if PATRONYMIC.match(token):
            out.append((token, patronymic_or_surname(token, father_name), 0))
        else:
            ordinal += 1
            out.append((token, "given", ordinal))

    # `SURN` is data, not the last whitespace token of anything. It can still hold a
    # patronym -- `name modelling.txt`: *"We have to check in the given names and in
    # the surname whether it is a patronym"* -- so the same test runs on it.
    for raw in [t for t in re.split(r"\s+", (surn or "").strip()) if t]:
        token, shape = name_shape(raw)
        if shape:
            out.append((token, shape, 0))
            continue
        if PATRONYMIC.match(token):
            out.append((token, patronymic_or_surname(token, father_name), 0))
        else:
            out.append((token, "family", 0))

    married = " ".join((marnm or "").split())
    if married and married.casefold() != " ".join((surn or "").split()).casefold():
        for raw in married.split():
            token, shape = name_shape(raw)
            out.append((token, shape or "married", 0))

    for token in nicknames + [t for t in [" ".join((nick or "").split())] if t]:
        out.append((token, "nickname", 0))

    return out


def classify(label: str) -> list[tuple[str, str, int]]:
    """`(token, usage, ordinal)` for each token of a rendered LABEL.

    **Prefer `classify_fields`.** This guesses what that reads: it takes the last
    token as the family name and cannot see `_MARNM`, `NICK`, or which field a
    patronym came from. It is kept for callers holding only a display string — the
    relationship-label work, and any report keyed on `label_en`.

    `Ane Oline Jonsdatter Raugstad` ->
        (Ane, given, 1) (Oline, given, 2) (Jonsdatter, patronymic, 0)
        (Raugstad, family, 0)

    The last token is the family name **unless it is itself patronymic**, which is
    the ordinary Norwegian case one generation earlier: `Jon Samuelsen` has no family
    name at all and `Samuelsen` must not become one.
    """
    # Geni wraps a nickname in quotes -- `Stine "Stena" Eivindsdatter Garborg` -- and
    # sometimes in parentheses: `Ingvold (Pinkie) Remmie`. The punctuation is Geni's
    # formatting and the name inside it is real, so it is stripped and the token kept.
    # `CLAUDE.md` on Stena: Emma took the nickname, not the quotes.
    cleaned = re.sub(r'[\"“”()]', " ", label or "")
    tokens = [t for t in re.split(r"\s+", cleaned.strip()) if t]
    if not tokens:
        return []

    # A single token is a GIVEN name, not a family name. `Amaterasu`, `Ninigi`,
    # `NN` -- a mononym is a forename, and calling it a surname would put a personal
    # name in `P734` and leave the person with no `P735` at all. A family name needs
    # something in front of it to be the family name OF.
    if len(tokens) == 1:
        return [(tokens[0], "patronymic" if PATRONYMIC.match(tokens[0]) else "given",
                 0 if PATRONYMIC.match(tokens[0]) else 1)]

    out: list[tuple[str, str, int]] = []
    last = tokens[-1]
    family = last if not PATRONYMIC.match(last) else None
    body = tokens[:-1] if family else tokens

    ordinal = 0
    for token in body:
        if PATRONYMIC.match(token):
            out.append((token, "patronymic", 0))
        else:
            ordinal += 1
            out.append((token, "given", ordinal))
    if family:
        out.append((family, "family", 0))
    return out


def statements_for(label, plan, geni_id, father_qid=None, fields=None,
                   sex="", father_name=""):
    """(statement lines, notes) for one person's name.

    Each line is `(property, value, qualifiers)` with qualifiers as
    `[(property, value), ...]`, ready for whatever emitter wants them.

    Pass `fields` -- a mapping with `givn`, `surn` and optionally `nick`, `marnm` --
    and the name is read from the GEDCOM fields. Without it the rendered `label` is
    parsed positionally, which is the old behaviour and is worse; see `classify`.

    `father_qid` is the `P144` *based on* target for a patronym -- `name
    modelling.txt` points it at **the person the link names**, not at a name item.
    Omitted when the father has no item yet rather than guessed.

    A `nickname` becomes `P1449`, which takes **text, not an item**, so it needs no
    entry in the name plan and can never be blocked by a missing one.

    `sex` is `"M"` or `"F"` and decides one thing only: whether a `_MARNM` family name
    carries `P3831` -> `Q28418670` *married name*. On a man it does not -- see below.
    """
    lines, notes = [], []
    aliases = []
    given_count = 0

    if fields:
        # **`father_name` is what turns a `-sen` token into the right kind of statement.**
        # Emma's test: the same token as the father means an inherited surname (`P734`), a
        # stem matching the father's GIVEN name means a patronymic (`P5056`). Without it the
        # morphology alone decides, which is what every caller did until 2026-08-27 and is
        # still the answer when the father is unknown.
        tokens = classify_fields(fields.get("givn", ""), fields.get("surn", ""),
                                 fields.get("nick", ""), fields.get("marnm", ""),
                                 father_name=father_name)
    else:
        tokens = classify(label)

    given_count = sum(1 for _t, u, _o in tokens if u == "given")

    for token, usage, ordinal in tokens:
        # **A particle and an unknown marker never reach the name plan.** Emma, 2026-08-26:
        # a particle is *"integral parts of what the people are called"* and so belongs in
        # the LABEL, and a marker joins the `NN` population `scripts/labels.py` owns. Looking
        # either up would find nothing and file a spurious "not in the plan" note; emitting
        # either would mint an item for `de` or for `?`.
        if usage in ("particle", "unknown"):
            continue

        # A nickname is free text on the item, so it is emitted regardless of whether
        # any name item exists for it.
        if usage == "nickname":
            lines.append((NICKNAME, token, []))
            aliases.append(token)
            continue

        # The married name is looked up as a family name -- it IS one, just a later
        # one -- so it shares Garborg's or Jacobson's item rather than needing a
        # separate "married" kind.
        lookup = "family" if usage == "married" else usage
        qid, action = plan.get((token, lookup), ("", "not in the plan"))
        if not qid:
            notes.append(f"{token} ({usage}): {action or 'no item'}")
            continue

        if usage == "given":
            # **`P1545` *series ordinal* only where there is more than one given name.**
            # Emma, 2026-08-25, on why she has been running batches only in part:
            # *"they have consistently included things I did not want, such as the series
            # orginal 1 on peoples given names when there is only one given name"*.
            #
            # It orders a person's several given names against each other. On somebody with
            # one, there is nothing to order and the qualifier asserts a sequence that does
            # not exist -- the same objection that already restricts `P7452` *reason for
            # preferred rank* to people who have a middle name.
            quals = [(SERIES_ORDINAL, str(ordinal))] if given_count > 1 else []
            # **`P7452` -> `Q3409033` *usual forename* only where there IS a middle
            # name.** Emma, 2026-08-24: *"usual forename only applies when there is a
            # middle name"*. It exists to say which of several given names is the one
            # actually used, so on a person with a single given name it distinguishes
            # nothing and asserts a contrast that does not exist.
            if ordinal == 1:
                if given_count > 1:
                    quals.append((PREFERRED_REASON, USUAL_FORENAME))
            else:
                quals.append((HAS_ROLE, MIDDLE_NAME))
            lines.append((GIVEN_NAME, qid, quals))
        elif usage == "patronymic":
            quals = [("P144", father_qid)] if father_qid else []
            lines.append((PATRONYM, qid, quals))
        elif usage == "married":
            # Emma, 2026-08-24: a SECOND `P734`, qualified married against birth.
            # **`Q28418670` *married name* only on a woman.** Emma, 2026-08-24:
            # *"married name on a man ... ontologically married name on a man means
            # more like adopted surname. So men's 'married names' should not have the
            # role of married name."*
            #
            # And it gets **no role at all** rather than `Q118383793` *adoptive name*,
            # because in this material the second surname is usually a **farm name**
            # taken by residence, not by adoption or marriage. `Q141169072` is the
            # case: *Ådne Olsen Grøtheim* became *Ådne Olsen Garborg* by moving to the
            # Garborg farm. Calling that adoption asserts something false, and
            # `reports/garborg-name-transliterations.tsv` already marks Aabø, Fjørtoft,
            # Heigre and Raugstad as farm names. An unqualified `P734` says only that
            # he bore the name, which is all we know.
            if sex == "F":
                lines.append((FAMILY_NAME, qid, [(HAS_ROLE, MARRIED_NAME_ROLE)]))
            else:
                lines.append((FAMILY_NAME, qid, []))
        else:
            # Only qualify the birth family name when a married one sits beside it;
            # a lone surname needs no role and none of her items carries one.
            has_married = any(u == "married" for _t, u, _o in tokens)
            quals = [(HAS_ROLE, BIRTH_NAME_ROLE)] if has_married else []
            lines.append((FAMILY_NAME, qid, quals))

    return lines, notes


def aliases_for(fields, surn="", marnm=""):
    """Alias strings for an item: the nicknames, and the married full name.

    Emma asked for aliases alongside the second `P734` *family name*. A married
    surname makes the person findable under a name no statement spells out, which is
    what an alias is for.
    """
    out = []
    tokens = classify_fields(fields.get("givn", ""), fields.get("surn", ""),
                             fields.get("nick", ""), fields.get("marnm", ""))
    surn = surn or fields.get("surn", "")
    marnm = marnm or fields.get("marnm", "")
    given = [t for t, u, _o in tokens if u == "given"]

    # **A nickname alias carries the SURNAME, or it finds nobody.** Emma, 2026-08-26, on
    # `Q141189102`: *"this person was given an alias of 'Sally' instead of 'Sally Ekman'"*.
    # Her record is `GIVN 'Sigrid "Sally" Manilva'`, `SURN Tunheim`, `_MARNM Ekman`, and a
    # bare `Sally` is not a name anybody could look her up by.
    #
    # The surname used is the **married** one where there is one, because § *The MARRIED
    # name is the real name* makes that the form her primary label takes -- so the alias is
    # the same person's name with the nickname swapped in, not a different person's.
    #
    # `P1449` *nickname* keeps the BARE token, and must: `Sally` is the nickname. It is the
    # alias, whose job is retrieval, that needs the full form.
    surname = " ".join((marnm or surn or "").split())
    for token, usage, _ordinal in tokens:
        if usage == "nickname":
            full = f"{token} {surname}".strip()
            if full not in out:
                out.append(full)
    married = " ".join((fields.get("marnm") or "").split())
    if married and married.casefold() != " ".join(
            (fields.get("surn") or "").split()).casefold():
        if given:
            out.append(f"{' '.join(given)} {married}")

    # **The bracketed form itself is an alias.** Emma, 2026-08-26: *"Amul for the brackets"*.
    # The two `P734` *family name* statements are coequal and unqualified, so nothing in the
    # statements records how Geni actually writes the name; the alias does, and it is what
    # makes the person findable by what is on their profile page.
    for field in ("surn", "marnm"):
        raw = " ".join((fields.get(field) or "").split())
        if raw and any(PAREN.match(t) for t in raw.split()):
            full = f"{' '.join(given)} {raw}".strip() if given else raw
            if full not in out:
                out.append(full)
    return out
