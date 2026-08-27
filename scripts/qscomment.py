"""A comment above every line of a QuickStatements batch, saying what it changes.

**Emma, 2026-08-26:** *"With comments as headings and comments. Every line has a comment the
line above it saying what change is happening."*

Shared by `build-garborg-day.py` and `build-garborg-name-items.py` so the two files read the
same way, and so the rule is applied in ONE place. It runs as a **post-pass over the assembled
batch**, not at each `lines.append`: those files emit statements from a dozen sites, and a rule
applied at every call site is one that will be missed at the thirteenth. Here it is structural
-- anything that is not a comment and not blank gets a comment -- and
`tests/test_p2600_batches.py` asserts exactly that.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


#: English labels for every property this file can emit, so a comment can name one.
#: `CLAUDE.md` § *Always write the English label next to a property or item ID* -- and
#: `reports/wikidata-labels.tsv` holds 5,637 of them, so there is no reason to guess.
def property_labels():
    out = {}
    path = ROOT / "reports" / "wikidata-labels.tsv"
    with open(path, encoding="utf-8") as f:
        for line in f:
            pid, _, rest = line.partition("	")
            if pid.startswith("P"):
                out[pid] = rest.split("	")[0].strip()
    return out


#: What each QuickStatements label/alias code does, in words.
SLOT_WORDS = {
    "L": "set the {lang} label to",
    "A": "add a {lang} alias",
    "D": "set the {lang} description to",
}


def qid_labels(wanted):
    """English labels for the QIDs a batch mentions, from the offline export only.

    `CLAUDE.md` § *Always write the English label next to a property or item ID*, and it
    applies to a comment as much as to prose: `P31 instance of = Q5` is half a sentence.
    One pass over `reports/wikidata-labels.tsv` for the ids actually present, so the 882k
    rows are read once and nothing is guessed -- an id the export does not hold stays bare
    rather than being invented.
    """
    out = {}
    with open(ROOT / "reports" / "wikidata-labels.tsv", encoding="utf-8") as f:
        for line in f:
            qid, _, rest = line.partition("	")
            if qid in wanted:
                out[qid] = rest.split("	")[0].strip()
    return out


def annotate(lines, name_of):
    """A comment above EVERY statement line, saying what that line changes.

    **Emma, 2026-08-26:** *"With comments as headings and comments. Every line has a
    comment the line above it saying what change is happening."*

    Written as a post-pass over the assembled batch rather than at each `lines.append`,
    because this file emits statements from a dozen places and a rule applied at every
    call site is a rule that will be missed at the thirteenth. Here it is structural:
    anything that is not a comment and not blank gets a comment, and
    `tests/test_p2600_batches.py` asserts it.

    `name_of` maps a QID or a Geni id to something human, so a comment reads
    *father: Q141152600 Stine Eivindsdatter Jacobson* rather than two opaque numbers.
    """
    props = property_labels()
    mentioned = {t.strip('"') for line in lines for t in line.split(chr(9))
                 if re.fullmatch(r"Q\d+", t.strip('"'))}
    known = qid_labels(mentioned)
    out, last_subject = [], None

    def human(token):
        # A monolingual value is `en:"Sally"` and stripping quotes off it ate the closing
        # one, so the comment read `= en:"Sally`. Leave anything language-tagged alone.
        if re.match(r'^[a-z]{2,3}(-[a-z]+)?:"', token):
            return token
        token = token.strip('"')
        if token == "LAST":
            return "the item just created"
        name = name_of(token) or known.get(token, "")
        return f"{token} {name}" if name else token

    for line in lines:
        if not line or line.startswith("#"):
            out.append(line)
            continue
        if line == "CREATE":
            out.append("# create a new item")
            out.append(line)
            continue
        parts = line.split(chr(9))
        subject, prop = parts[0], parts[1] if len(parts) > 1 else ""
        value = parts[2] if len(parts) > 2 else ""
        if prop[:1] in SLOT_WORDS and len(prop) > 1 and not prop[1:].isdigit():
            what = SLOT_WORDS[prop[0]].format(lang=prop[1:]) + f" {value}"
        elif prop.startswith("P"):
            label = props.get(prop, "")
            named = f"{prop} {label}".strip()
            what = f"{named} = {human(value)}"
            extra = [f"{props.get(parts[i], parts[i])} {human(parts[i + 1])}"
                     for i in range(3, len(parts) - 1, 2)
                     if parts[i].startswith("P")]
            if extra:
                what += ", qualified " + ", ".join(extra)
        else:
            what = line.replace(T, " ")
        who = human(subject)
        prefix = "" if who == last_subject else f"{who}: "
        last_subject = who
        out.append(f"#   {prefix}{what}")
        out.append(line)
    return out
