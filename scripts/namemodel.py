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

**Both fields, always.** A patronym can sit in `GIVN` or in `SURN` and which one
decides nothing. Here the whole label is tokenised and each token classified on its
own shape, which is the same rule applied to a flat string.

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


def classify(label: str) -> list[tuple[str, str, int]]:
    """`(token, usage, ordinal)` for each token of a name.

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


def statements_for(label: str, plan: dict, geni_id: str,
                   father_qid: str | None = None) -> tuple[list, list]:
    """(statement lines, notes) for one person's name.

    Each line is `(property, value, qualifiers)` with qualifiers as
    `[(property, value), ...]`, ready for whatever emitter wants them.

    `father_qid` is the `P144` *based on* target for a patronym — `name
    modelling.txt` points it at **the person the link names**, not at a name item.
    Omitted when the father has no item yet rather than guessed.
    """
    lines, notes = [], []
    for token, usage, ordinal in classify(label):
        qid, action = plan.get((token, usage), ("", "not in the plan"))
        if not qid:
            notes.append(f"{token} ({usage}): {action or 'no item'}")
            continue

        if usage == "given":
            quals = [(SERIES_ORDINAL, str(ordinal))]
            quals.append((PREFERRED_REASON, USUAL_FORENAME) if ordinal == 1
                         else (HAS_ROLE, MIDDLE_NAME))
            lines.append((GIVEN_NAME, qid, quals))
        elif usage == "patronymic":
            quals = [("P144", father_qid)] if father_qid else []
            lines.append((PATRONYM, qid, quals))
        else:
            lines.append((FAMILY_NAME, qid, []))
    return lines, notes
