"""Every description in a batch is one of the shapes that is allowed, and nothing sets a summary.

**The description ban is dead and the summary ban is not.** `CLAUDE.md` § *NO edit summaries,
categorically* still holds and `test_nothing_sets_an_edit_summary` is still its guard.

⛔ **Descriptions were un-banned on 2026-09-19** -- `CLAUDE.md` § *DESCRIPTIONS ARE WRITTEN NOW,
AND THE REASON IS THE DEDUPLICATION*, reversing 2026-08-30 -- **because a blank description is
not a guard, it is the absence of one.** Wikibase refuses a creation only when the label AND a
NON-EMPTY description both match, so blank descriptions never stopped a duplicate; they stopped
Wikidata catching ours. Measured that day: eleven live items labelled `Margareta` with no
description, and four labelled `Hans Larsson`, all coexisting.

So this test is not deleted and not loosened to nothing. It still answers *is this description
one of the shapes we emit* -- the three name strings, or an individual's life description -- and
a sentence somebody wrote by hand still fails it.

A `#` comment inside a `.qs` file is not an edit summary -- it never reaches Wikidata -- so the
description check reads statement lines only.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

#: QuickStatements sets a description with `D<lang>`, exactly as it sets a label with `L<lang>`.
DESCRIPTION = re.compile(r"^(?:LAST|-?Q[1-9][0-9]*)\t(D[a-z][a-z-]*)\t")

#: Ways an edit summary reaches WIKIDATA -- an API parameter or a QuickStatements flag.
#:
#: **Narrowed on a false positive, deliberately named here.** `build-orderlife-batch.py` takes
#: `--summary reports/orderlife-batch-summary.csv`: a local CSV of what the run did, which
#: never leaves the disk. Matching that would have made the guard noisy enough to be disabled,
#: which is how a categorical rule stops being enforced. A line is only an offence when the
#: summary is being SENT -- a URL parameter, a request payload key, or an assignment whose
#: value is not a path.
SUMMARY = re.compile(r"&summary=|[?&]summary|summary\s*=\s*[\"']"
                     r"|[\"']summary[\"']\s*:|EDIT_SUMMARY")
#: A match is forgiven when the line is plainly about a local file.
LOCAL_FILE = re.compile(r"\.csv|\.tsv|\.json|\.md|reports/|out/|add_argument")


#: **The one exception, and it is narrow.** All patronymics get the description
#: *patronymic* so they deduplicate properly, because duplicate patronymics were being
#: created to the point of intolerability. All surnames get *family name*, and any
#: matronymics get *matronymic*.
#:
#: The description is what makes Wikidata itself refuse the duplicate -- a label and description
#: must be unique together per language. So this test is NARROWED rather than weakened: exactly
#: these three strings, only in `Den`, and nothing else anywhere.
#:
#: ⛔ **`given name` JOINED THEM ON 2026-09-21, because it was the one kind going out blank.**
#: `CLASS_FOR` in `build-garborg-name-items.py` has had a `given` entry all along and
#: `DESCRIPTION_FOR` did not, so every given-name item was created with no description —
#: `Berete`, labelled in five languages, `P31 Q202444`, and nothing to stop a second one.
#: The argument is the one that put `patronymic` here: duplicates to the point of
#: intolerability, and the description is the only thing Wikibase refuses on.
ALLOWED_DESCRIPTIONS = {"patronymic", "family name", "matronymic", "given name"}

#: ⛔ **`Den` ON AN EXISTING ITEM COUNTS, NOT ONLY ON A `CREATE`.** This was `^LAST	Den	...`,
#: which reads the exception too narrowly: a name item ALREADY on Wikidata is described now, and
#: the four rows that do it -- `Q112261760`, `Q124785549`, `Q131994301`, `Q98139923` -- were ruled
#: intentional on 2026-09-09, asked directly: *"both are intentional lol and matronymic too"*.
DEN = re.compile(r'^(?:LAST|Q[1-9][0-9]*)	Den	"([^"]*)"$')

#: ⛔ **THE DAILY BATCH IS NOT A `.qs` FILE, AND IT WAS OUTSIDE EVERY DESCRIPTION GUARD.**
#: This test globbed `reports/*.qs`; the batch the pipeline actually composes and sends is
#: `reports/wikidata-garborg-day.txt`, so a description in it -- intentional or not -- was
#: unchecked. Found 2026-09-09 while reading why the batch carried `Den "family name"`.
#: Measured before widening: all 16 `Den` lines in today's batch are already allowed, so this
#: catches nothing today and would catch the next one.
#:
#: ⛔ **AND THE TWO HALVES ARE WHAT IS ACTUALLY SENT.** `wikidata-edits.yml` sends
#: `-auto.txt` every morning and the Pages site publishes `-manual.txt` for a person to paste;
#: the day batch is the composition neither of them is. Adding them on 2026-09-21 found **16
#: and 25 blank descriptions** sitting in the files that go out.
BATCHES = ["reports/*.qs", "reports/wikidata-garborg-day.txt",
           "reports/wikidata-garborg-day-auto.txt",
           "reports/wikidata-garborg-day-manual.txt",
           "reports/wikidata-familysearch-day.txt"]

#: ⛔ **AND INDIVIDUALS CARRY ONE TOO, SINCE 2026-09-19.** `life_description` in
#: `build-garborg-day.py` is the authority and `DATE_WORDS` beside it is where these words come
#: from; `ABT` reads out as `circa`, ruled the same day.
#:
#: The shape is what is asserted, because the facts behind it are not in this test's reach: a
#: life description opens with `born`, `died`, a digit or a GEDCOM qualifier, and carries a year.
#: That admits `circa 1518 Bergen, Norway - 1580` and `died 1590`, and refuses a hand-written
#: sentence, which is the failure this guard exists for.
#:
#: ⛔ **A SIDE MAY BE A PLACE WITH NO DATE, and the year lookahead refused those.** The
#: FamilySearch corpus carries places far more often than dates, so `life_description` produces
#: `born Wollin, Potsdam-Mittelmark, Brandenburg, Germany`, `died Rygge Kirke, Rygge, Østfold,
#: Norge` and `Norway - 1471` — all of them real descriptions built by the one function that is
#: allowed to build them. So the year is required only where the string does not open with
#: `born `/`died ` and does not carry the ` - ` that separates the two sides. A hand-written
#: sentence still fails, which is what this guard is for.
LIFE_WORD = (r"Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec"
             r"|circa|Aft|Bef|Est|Cal|Int|Bet|From|and|to|BC|AD")
LIFE_DESCRIPTION = re.compile(
    rf"^(?:(?:born |died ).+"
    rf"|(?=.*\b\d{{3,4}}\b)(?:\d|(?:{LIFE_WORD})\b).*"
    rf"|.+ - .+)$")

#: ⛔ **AND THE THIRD SHAPE IS THE IDENTIFIER. Ruled 2026-09-21:** *"no description info means
#: geni id referencing description not no description"*, and *"base it on the other id
#: referencing descriptions"* for FamilySearch. `scripts/descriptions.py` writes it, either as
#: the whole description for a person nothing is known about, or in brackets on the end of a
#: life description that collided with another one.
#:
#: **It exists because a blank description is the absence of the guard**, and the guard is the
#: only thing Wikibase refuses a creation on. Measured the same day across the composed
#: batches: **28 blank descriptions and 5 duplicate `(label, description)` pairs** in
#: `wikidata-garborg-day.txt` alone.
ID_DESCRIPTION = re.compile(r"^(?:Geni \d+|FamilySearch [A-Z0-9-]+)$")

#: ⛔ **AND THE SECOND RUNG WAS NEVER IN THIS LIST EITHER.** `describe_all` writes
#: `son of Anders Hök, adlad Hedersköld`, `wife of Kristian Noraeus`,
#: `daughter of Mårten Pedersson Gavelius` — the formulaic relationship phrase the redacted
#: branch has written as a LABEL since 2026-08-16, promoted to a description on 2026-09-19 for
#: anyone with no dates. It went unnoticed because this test read only
#: `wikidata-garborg-day.txt`; adding the two halves, which are what is actually sent, is what
#: surfaced it. `labels.AS_CHILD`/`AS_SPOUSE`/`AS_PARENT` are where the words come from.
#:
#: ⛔ **AND THE PHRASE MAY LEAD WITH THE PERSON'S OWN GIVEN NAME, SEPARATED BY A COMMA.**
#: Ruled 2026-09-21 — *"SETTLED: A COMMA. `Tora, mother of Brita`"* — and
#: `namemodel.lead_with_given_name` is what writes it. The batch carries
#: `Agmund Unge Dans, son of Hallkel Agmundssøn Krøkedans` and
#: `Anna Kornelia, wife of Carl Gökman`; a regex anchored on the relation word alone called
#: every one of them a hand-written sentence.
RELATION_WORD = r"son|daughter|child|husband|wife|spouse|father|mother|parent"
RELATIONSHIP_DESCRIPTION = re.compile(
    rf"^(?:[^,]{{1,120}}, )?(?:{RELATION_WORD}) of \S")
#: The bracketed form on the end of an otherwise ordinary description.
ID_SUFFIX = re.compile(r" \((?:Geni \d+|FamilySearch [A-Z0-9-]+)\)$")

#: `DESC_MAX` in `build-garborg-day.py`. A description longer than this did not come from there.
#: The bracketed identifier is added AFTER the truncation, so it is allowed past the limit.
DESC_MAX = 240


def test_no_batch_carries_a_description():
    offenders = []
    for path in sorted({p for pattern in BATCHES for p in REPO.glob(pattern)}):
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith("#"):
                continue
            m = DESCRIPTION.match(line)
            if not m:
                continue
            allowed = DEN.match(line)
            if allowed:
                text = allowed.group(1)
                if text in ALLOWED_DESCRIPTIONS:
                    continue
                if ID_DESCRIPTION.match(text):
                    continue
                stem = ID_SUFFIX.sub("", text)
                if len(stem) <= DESC_MAX and (stem in ALLOWED_DESCRIPTIONS
                                              or LIFE_DESCRIPTION.match(stem)
                                              or RELATIONSHIP_DESCRIPTION.match(stem)):
                    continue
            offenders.append(f"{path.name}:{n} sets {m.group(1)}  {line.strip()[:60]}")
    assert not offenders, (
        "a description is Den, and is either a name string "
        f"{sorted(ALLOWED_DESCRIPTIONS)} or a life description from life_description "
        f"-- ruled 2026-09-19: {offenders[:8]}")


def test_nothing_sets_an_edit_summary():
    offenders = []
    for pattern in ("scripts/*.py", "src/genimerge/*.py", ".github/workflows/*.yml"):
        for path in sorted(REPO.glob(pattern)):
            # This file names the thing it forbids, which is not the same as setting one.
            if path.name == Path(__file__).name:
                continue
            for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if line.lstrip().startswith(("#", "*")) or '"""' in line:
                    continue
                if SUMMARY.search(line) and not LOCAL_FILE.search(line):
                    offenders.append(f"{path.relative_to(REPO)}:{n}  {line.strip()[:80]}")
    assert not offenders, (
        "an edit summary is never set, categorically -- ruled 2026-08-30. "
        f"{offenders[:8]}")


#: ⛔ **THE FILES A RUN ACTUALLY PRODUCES AND SENDS**, which is narrower than `BATCHES` above
#: on purpose. `reports/*.qs` also holds the record of batches already RUN —
#: `wikidata-garborg-day-1.qs`, `wikidata-garborg-day-2026-08-25-run.qs`,
#: `wikidata-jon-parents.qs` — and rewriting a sent batch's descriptions would falsify the
#: record of what went out. They carry 15 undescribed creations between them and those items
#: exist; the fix for them is on Wikidata, not in a file that describes history.
LIVE_BATCHES = ["reports/wikidata-garborg-day.txt",
                "reports/wikidata-garborg-day-auto.txt",
                "reports/wikidata-garborg-day-manual.txt",
                "reports/wikidata-familysearch-day.txt"]

#: `CREATE`, then the label and description lines inside the block that follows it.
_LABEL_LINE = re.compile(r'^LAST\t(?:Lmul|Len)\t"(.*)"$')
_DEN_LINE = re.compile(r'^LAST\tDen\t"(.*)"$')


def _creation_blocks(path):
    """`[(label, description)]` for every `CREATE` in the file, either half possibly `None`."""
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [n for n, l in enumerate(lines) if l.strip() == "CREATE"]
    out = []
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(lines)
        label = desc = None
        for n in range(start + 1, end):
            m = _LABEL_LINE.match(lines[n])
            if m and label is None:
                label = m.group(1)
            m = _DEN_LINE.match(lines[n])
            if m and desc is None:
                desc = m.group(1)
        out.append((label, desc))
    return out


def test_no_creation_goes_out_without_a_description():
    """⛔ *"no description info means geni id referencing description not no description"*.

    Ruled 2026-09-21, with the duplicates still coming: *"we're making too many duplicates and
    it's bothersome"*. **Wikibase refuses a creation only when the label AND a NON-EMPTY
    description both match**, so a blank description is not a weak guard, it is the absence of
    one. `Anders Jørgensen Heier` exists as both `Q141504247` and `Q141502696` through this
    exact hole.

    The ladder has no bottom rung that emits nothing: the life description, then the
    relationship phrase, then **the identifier** — `Geni <id>`, `FamilySearch <id>` — which is
    unique by construction because it is the primary key of the source the person came from.
    `scripts/descriptions.py` is the authority and it runs over the ASSEMBLED batch, because a
    guard the composer alone applies is one appended section away from being no guard.
    """
    offenders = []
    for path in sorted({p for pattern in LIVE_BATCHES for p in REPO.glob(pattern)}):
        for label, desc in _creation_blocks(path):
            if label is not None and not desc:
                offenders.append(f"{path.name}: CREATE labelled {label!r} has no description")
    assert not offenders, (
        f"{len(offenders)} creations carry no deduplication guard at all: {offenders[:8]}")


def test_no_two_creations_share_a_label_and_a_description():
    """⛔ The other half of the same failure, and the commoner one in this corpus.

    Two people with the same name and the same dates produce the same string — which in a
    Scandinavian corpus is the ordinary case, not the odd one — and Wikibase refuses only on
    the PAIR, so an identical pair is a duplicate we mint ourselves and then merge by hand.
    The second one takes its identifier AS the description (ruled 2026-09-23).

    Measured 2026-09-21 before the guard: **5 duplicate pairs in `wikidata-garborg-day.txt`,
    4 in the auto half, 5 in the manual half**, on top of 28, 16 and 25 blank descriptions.
    """
    offenders = []
    for path in sorted({p for pattern in LIVE_BATCHES for p in REPO.glob(pattern)}):
        seen = set()
        for label, desc in _creation_blocks(path):
            if label is None or not desc:
                continue
            if (label, desc) in seen:
                offenders.append(f"{path.name}: {label!r} + {desc!r} twice")
            seen.add((label, desc))
    assert not offenders, (
        f"{len(offenders)} creations duplicate an earlier one in the same file: "
        f"{offenders[:8]}")


def test_a_collision_takes_the_geni_id_alone():
    """Ruled 2026-09-23: *"when there is a collision we give only the geni id as the fallback
    description"* -- the id REPLACES the colliding description, it is not appended, and a
    person the corpus-wide audit lists as colliding gets it even when the batch holds no twin.
    """
    import sys
    sys.path.insert(0, str(REPO / "scripts"))
    import descriptions

    def block(label, desc, geni):
        return ["CREATE", f'LAST	Lmul	"{label}"', f'LAST	Den	"{desc}"',
                f'LAST	P2600	"{geni}"']

    lines = block("Erik Ersson", "born 1728", "1") + block("Erik Ersson", "born 1728", "2")         + block("Anna", "born 1700", "3") + block("Anna", "born 1701", "4")
    assert descriptions.deduplicate(lines, "P2600", {"3"}) == 2
    assert [l for l in lines if "	Den	" in l] == [
        'LAST	Den	"born 1728"', 'LAST	Den	"Geni 2"',
        'LAST	Den	"Geni 3"', 'LAST	Den	"born 1701"']
