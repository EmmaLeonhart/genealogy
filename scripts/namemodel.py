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

**Emma's two rulings, 2026-08-24.** A quoted token inside `givn` becomes `P1449`
*nickname*. A married name becomes a **second** `P734` *family name*, qualified birth
against married with `P3831` *object of statement has role*, plus an alias — emitted
only where it differs from `surn`, and **sex is not a screen**.

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
PATRONYMIC = re.compile(r".+(sen|son|sson|datter|sdatter)$", re.I)


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


def classify_fields(givn: str, surn: str, nick: str = "",
                    marnm: str = "") -> list[tuple[str, str, int]]:
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

    The married name carries no ordinal and is *not* a screen on sex — her ruling,
    against the corpus measurement's suggestion, and it is her data model to set.
    """
    out: list[tuple[str, str, int]] = []

    raw_givn = givn or ""
    nicknames = [m.group("token") or m.group("paren")
                 for m in QUOTED.finditer(raw_givn)]
    plain = QUOTED.sub(" ", raw_givn)

    ordinal = 0
    for token in [t for t in re.split(r"\s+", plain.strip()) if t]:
        if PATRONYMIC.match(token):
            out.append((token, "patronymic", 0))
        else:
            ordinal += 1
            out.append((token, "given", ordinal))

    # `SURN` is data, not the last whitespace token of anything. It can still hold a
    # patronym -- `name modelling.txt`: *"We have to check in the given names and in
    # the surname whether it is a patronym"* -- so the same test runs on it.
    for token in [t for t in re.split(r"\s+", (surn or "").strip()) if t]:
        out.append((token, "patronymic" if PATRONYMIC.match(token) else "family", 0))

    married = " ".join((marnm or "").split())
    if married and married.casefold() != " ".join((surn or "").split()).casefold():
        for token in married.split():
            out.append((token, "married", 0))

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


def statements_for(label, plan, geni_id, father_qid=None, fields=None):
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
    """
    lines, notes = [], []
    aliases = []
    given_count = 0

    if fields:
        tokens = classify_fields(fields.get("givn", ""), fields.get("surn", ""),
                                 fields.get("nick", ""), fields.get("marnm", ""))
    else:
        tokens = classify(label)

    given_count = sum(1 for _t, u, _o in tokens if u == "given")

    for token, usage, ordinal in tokens:
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
            quals = [(SERIES_ORDINAL, str(ordinal))]
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
            lines.append((FAMILY_NAME, qid, [(HAS_ROLE, MARRIED_NAME_ROLE)]))
        else:
            # Only qualify the birth family name when a married one sits beside it;
            # a lone surname needs no role and none of her items carries one.
            has_married = any(u == "married" for _t, u, _o in tokens)
            quals = [(HAS_ROLE, BIRTH_NAME_ROLE)] if has_married else []
            lines.append((FAMILY_NAME, qid, quals))

    return lines, notes


def aliases_for(fields):
    """Alias strings for an item: the nicknames, and the married full name.

    Emma asked for aliases alongside the second `P734` *family name*. A married
    surname makes the person findable under a name no statement spells out, which is
    what an alias is for.
    """
    out = []
    tokens = classify_fields(fields.get("givn", ""), fields.get("surn", ""),
                             fields.get("nick", ""), fields.get("marnm", ""))
    given = [t for t, u, _o in tokens if u == "given"]
    for token, usage, _ordinal in tokens:
        if usage == "nickname":
            out.append(token)
    married = " ".join((fields.get("marnm") or "").split())
    if married and married.casefold() != " ".join(
            (fields.get("surn") or "").split()).casefold():
        if given:
            out.append(f"{' '.join(given)} {married}")
    return out
