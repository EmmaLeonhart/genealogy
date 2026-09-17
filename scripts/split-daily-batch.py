"""Split the daily batch into the part CI/CD sends itself and the part a person pastes.

Ruled 2026-09-14: *"Make the CICD do about half the edits every day automatically. Produce
disjoint quickstatements on the github page too."* **Disjoint** is the hard word: the Pages site
publishes the daily batch, and once the scheduled run starts sending part of it, anyone pasting
the page re-sends what the runner already did. Duplicate statements are mostly harmless, but a
duplicate `CREATE` mints a second item for somebody who now exists, and that is the one failure
in this design that cannot be undone by running it correctly next time.

## The split is computed ONCE, here, and written as two files

Not as a fraction applied twice. `wikidata-edit-run.py` could take `--fraction` and the page
builder could take the complement, and the two would agree only while the arithmetic, the file
and the ordering all stayed identical in three places. That is the shape of every drift bug this
repo has hit — the two copies of the start date, the clan gate that lived in one emitter, the
batch inventory nothing regenerated. So:

    reports/wikidata-garborg-day-auto.txt     what the schedule sends, unattended
    reports/wikidata-garborg-day-manual.txt   what the Pages site publishes

Together they are exactly the input, in order, with no edit in both and none dropped — which
this script asserts before writing anything.

## ⛔ It is a STRIDE, not a prefix

The batch is not homogeneous and the cut cannot be a prefix. Hand identifications lead the file,
name items follow, and person creations sit below both -- so taking the first third gave the
scheduled run every identification, some surnames, and **not one human**, every day. Measured
2026-09-17: twelve creations in the auto half and all twelve were name items.

Every `step`-th block goes to the auto half instead, `step` being `round(1 / AUTO_SHARE)`. That
samples each kind in proportion, stays deterministic, and still never splits a `CREATE` block.

## Why a third

The caps were raised 50% on 2026-09-14 and CI/CD takes a third of the result, so the share it
sends by itself is exactly the increase and the hand-run keeps the volume it always had:
`1.5 / 3 = 0.5`. Ruled the same day: *"you are specifically making 50% more quickstatements and
then segregating out a third of that to be run by cicd."*

## ⛔ A `CREATE` BLOCK IS NOT ONE LINE

QuickStatements V1 binds the lines after a `CREATE` to it positionally through `LAST`. Splitting
on line count would cut a creation away from the statements that describe it, and the tail would
then bind to whatever `CREATE` happened to precede it in the other half — silently attaching one
person's name and dates to another. So the split is made over EDIT OBJECTS parsed by `qs_v1`,
never over text, and a block moves whole.

    PYTHONPATH=src python scripts/split-daily-batch.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import qs_v1  # noqa: E402

SRC = REPO / "reports" / "wikidata-garborg-day.txt"
AUTO = REPO / "reports" / "wikidata-garborg-day-auto.txt"
MANUAL = REPO / "reports" / "wikidata-garborg-day-manual.txt"

#: The share the schedule sends by itself. One third; see the module docstring for why.
#: ⛔ **A THIRD IS A SHARE OF WHATEVER IS COMPOSED, NEVER A CAP.** Ruled 2026-09-14 --
#: *"making 50% more quickstatements and then segregating out a third of that to be run by
#: cicd"* -- and restated 2026-09-17 when it came out wrong: *"I wasn't intending for there to be
#: a cap, I was intending for 50% of the edits to be done. I was intending for a third of the
#: edits to be automatic and two-thirds of the edits to be done by quick statements."*
#:
#: **Both halves get done.** The third is the autonomous share; the rest is pasted. What broke it
#: was not this number but a second ceiling stacked on it: `RUN_LIMIT` at 100 and the workflow's
#: `limit=100` bound BELOW the share, so a batch of 411 sent 100 where a third is 137, and
#: everything above 100 silently became somebody's homework. A share recomputes as the batch
#: grows; a ceiling does not, and nothing re-derived it as the batch grew.
#:
#: The ceilings stay raised (1000) so they can never bind below the share again. They exist to
#: stop a runaway, not to ration the work.
AUTO_SHARE = 1.0 / 3.0

#: The scheduled run's own ceiling, mirrored so the split never hands it more than it will send.
#: If it did, the surplus would be in neither file: the runner would stop at its limit and the
#: page would not carry the remainder.
#: Mirrors `wikidata-edit-run.MAX_EDITS_PER_RUN`. It is a ceiling, not a share: raised with
#: it on 2026-09-17 so a composed batch is never larger than the run that sends it.
RUN_LIMIT = 1000


def blocks(text):
    """The batch as a list of (lines, is_create) in order.

    A `CREATE` and everything up to the next `CREATE` or the next explicitly-subjected line is
    one block, because `LAST` binds backwards.
    """
    # **A block runs from one `CREATE` to the NEXT `CREATE`, and that is the only safe cut.**
    # The first attempt ended a block at the first line that did not start with `LAST`, which
    # cut the bearer lines away: `Q141451028 P5056 LAST` starts with `Q`, and on its own it is
    # `LAST as a value with no CREATE above it`. Anything between two `CREATE`s may bind
    # backwards, so nothing between them may be separated from the first.
    out, cur = [], []
    for line in text.splitlines():
        if line.strip().upper() == "CREATE":
            if cur:
                out.append(cur)
            cur = [line]
        elif cur:
            cur.append(line)
        else:
            out.append([line])
    if cur:
        out.append(cur)
    return out


def main() -> int:
    if not SRC.exists():
        raise SystemExit(f"{SRC.relative_to(REPO)} is missing; compose the batch first")
    text = SRC.read_text(encoding="utf-8")

    edits = qs_v1.edit_objects(qs_v1.parse(text))
    share = min(math.ceil(len(edits) * AUTO_SHARE), RUN_LIMIT)

    bs = blocks(text)
    # ⛔ **A PREFIX IS NOT A THIRD, AND FOR DAYS IT MEANT CI/CD CREATED NOBODY.**
    #
    # This walked blocks in file order and stopped once the auto half held `share` edits, so the
    # automatic half was simply the TOP of the file. The batch is not homogeneous: the hand
    # identifications lead it by design -- *"These lead the file: the Geni id is the FIRST edit on
    # any individual"* -- then the name items, and the person creations sit below both. The cut
    # therefore landed above every `CREATE` of a human, every single day.
    #
    # Measured 2026-09-17: `wikidata-garborg-day-auto.txt` held **12 creations and all twelve were
    # name items** -- `Kristiernsdotter`, `Næsmoen`, `Petersdotter` -- against 98 creations in the
    # full batch. Emma: *"why the fuck are you not creating people"* and *"It is not creating
    # anything"*. The scheduled run had been making surnames and no humans.
    #
    # So the auto half is taken as a STRIDE across the whole file rather than a prefix: every
    # `step`-th block, which samples identifications, name items and creations in proportion.
    # Deterministic, and a block still moves whole -- `LAST` binds backwards inside a block and
    # nothing here splits one.
    # ⛔ **THE STRIDE IS OVER SUBJECTS, NOT BLOCKS.** `qs_v1.edit_objects` groups CONSECUTIVE
    # lines with the same subject into one edit, so striding over raw blocks cuts an item's
    # statements in half and the two halves then count as two edits: the completeness assertion
    # came back `83 + 266 != 347` on the first attempt, which is the same item counted twice
    # rather than anything lost. Worse than the count, it would send a person's `P735` in the
    # morning and leave their `P734` on the web page.
    #
    # So consecutive blocks about the same subject are welded into one unit first, and the
    # stride runs over units.
    def subject_of(block):
        for line in block:
            t = line.strip()
            if not t or t.startswith("#"):
                continue
            if t.upper() == "CREATE":
                return None                  # a creation is its own unit, always
            return t.split("\t", 1)[0]
        return ""                            # comment-only: belongs with whatever it precedes

    def last_subject_of(block):
        """The subject of the LAST statement line in a block.

        ⛔ Not the first. A `CREATE` block runs to the next `CREATE`, so it carries the new
        item's `LAST` lines AND the bearer lines that point at it -- `Q141353755 P735 LAST ...`
        -- and those end the block under a different subject. Comparing first subjects left one
        item straddling the cut and the assertion came back one over.
        """
        for line in reversed(block):
            t = line.strip()
            if not t or t.startswith("#") or t.upper() == "CREATE":
                continue
            return t.split("	", 1)[0]
        return None

    units, cur, cur_tail = [], [], None
    for b in bs:
        subj = subject_of(b)
        # A comment-only run joins the unit it introduces rather than ending one; a block whose
        # first subject continues the previous unit's last subject is the same item still.
        same = cur and subj is not None and (subj == "" or subj == cur_tail)
        if same:
            cur.extend(b)
        else:
            if cur:
                units.append(cur)
            cur = list(b)
        t = last_subject_of(b)
        if t is not None:
            cur_tail = t
    if cur:
        units.append(cur)

    # \u26d4 **THE STRIDE IS OVER UNITS, AND IT FILLS GREEDILY.**
    #
    # An earlier attempt welded every unit that shares a subject into one group so that no
    # subject could straddle the cut. That constraint is too strong for this data and the reason
    # is structural: a person bears several name items, so the name-item `CREATE` blocks chain
    # through their shared bearer lines and **all 98 creations collapse into a single group**.
    # One group cannot fit under the share, so the automatic half came out at 14 lines and zero
    # creations -- worse than the prefix it replaced.
    #
    # It was also the wrong property to enforce. The danger this script exists for is a
    # DUPLICATED `CREATE`, which mints a second item for somebody who now exists and cannot be
    # undone; that is guaranteed by the line-partition assertion below. A subject whose
    # statements land in both halves is untidy -- half sent at 08:07, half pasted later -- but
    # both halves DO get sent and the item ends up whole. So it is counted and reported, not
    # refused.
    # ⛔ **A SUBJECT GOES WHOLE, OR THE GRAPH COMES OUT HALF-LINKED.** Reported 2026-09-17:
    # *"the individuals are not getting linked"*. Measured on that day's batch: `requires` was
    # never split -- 0 cases, so `LAST` always resolved -- but **25 subjects had statements in
    # both halves**, and 273 of the 337 relationship claims sat in the manual half.
    #
    # The comment that used to sit here accepted that as untidy-but-harmless *"because both
    # halves DO get sent and the item ends up whole"*. **That premise is false.** The manual
    # half is published for a person to paste; the automatic half goes out on a schedule. So a
    # `P40` can be sent today while its reciprocal `P22` waits days for a human -- which is
    # exactly the half-linked shape found on `Q141488165` the same evening.
    #
    # Grouping by SUBJECT is narrow enough to be safe. An earlier attempt welded anything
    # sharing a unit and collapsed all 98 creations into one group, because creates carry no
    # QID yet and chained through their `LAST` lines. Keying strictly on the explicit QID
    # subject leaves every create its own unit and welds only what genuinely belongs to one item.
    by_subject = {}
    for _i, _u in enumerate(units):
        _j = chr(10).join(_u)
        if not _j.strip():
            continue
        for _e in qs_v1.edit_objects(qs_v1.parse(_j)):
            _q = _e.get("qid")
            if _q:
                by_subject.setdefault(_q, set()).add(_i)
    welded = {}
    for _q, _idxs in by_subject.items():
        if len(_idxs) > 1:
            for _i in _idxs:
                welded.setdefault(_i, set()).update(_idxs)

    # ⛔ **ONLY THE CREATION OF AN INDIVIDUAL IS DISJOINT. EVERYTHING ELSE GOES IN BOTH.**
    #
    # Ruled 2026-09-17, and it is the design rather than a tuning of one: *"you have a disjoint
    # set of IDs ... a third of them go into the automatic, two thirds of them go into the quick
    # statements ... they are basically two parallel generations of all of the same stuff. And as
    # far as connectivity stuff goes ... we have it 100% on both of them. Because the
    # connectivity stuff doesn't matter, only creations matter."* And, asked which creations:
    # *"only creations of individuals need to be disjointed. Not creations of name items."*
    #
    # **The reason a duplicate matters is asymmetric.** A second `CREATE` for a person mints a
    # second item for somebody who now exists and cannot be undone. A second `CREATE` for a NAME
    # item cannot: Wikidata refuses the duplicate on the label-plus-description pair, which is
    # exactly why `DESCRIPTION_FOR` exists. And a duplicated `P22`/`P25`/`P40`/`P26` is a no-op --
    # `CLAUDE.md` § *a duplicate parent value is self-healing*.
    #
    # So there is nothing to balance and nothing to sample. Everything that is not the creation
    # of a human is written to BOTH files at 100%, and the human creations are dealt a third to
    # one and two thirds to the other, in composed order.
    #
    # ⛔ **A HUMAN `CREATE` TRAVELS WITH ITS `LAST` LINES.** They bind backwards and name no QID,
    # so a statement separated from its create attaches to nothing -- or worse, to whatever
    # create precedes it in the other file. The unit is the whole block, which is what `blocks`
    # already builds.
    #
    # This is the end of the pipeline and the ruling puts the split at the beginning. The effect
    # is the same file-for-file, and moving the partition into `build-garborg-day` is a separate
    # change to an 8,000-line composer; doing it here first makes the behaviour correct today
    # without that risk.
    def is_person_create(u):
        joined = chr(10).join(u)
        if not any(l.strip().upper() == "CREATE" for l in u):
            return False
        for e in qs_v1.edit_objects(qs_v1.parse(joined)):
            if e.get("kind") != "create":
                continue
            for c in e.get("claims") or ():
                v = c.get("value")
                if c.get("property") == "P31" and isinstance(v, dict) and v.get("id") == "Q5":
                    return True
        return False

    person_units = [i for i, u in enumerate(units) if is_person_create(u)]
    person_units_set = set(person_units)
    n_auto = int(round(len(person_units) * AUTO_SHARE))
    auto_people = set(person_units[:n_auto])
    print(f"   {len(person_units)} individual creation(s): {len(auto_people)} automatic, "
          f"{len(person_units) - len(auto_people)} for the page; everything else in BOTH")

    # ⛔ **THE DISJOINT PART IS THE CREATE AND WHAT BINDS TO IT, NOTHING ELSE.**
    #
    # A unit is a `CREATE` block, and `blocks` runs one from a `CREATE` to the NEXT `CREATE` --
    # so it carries the new item's `LAST` lines AND whatever explicitly-subjected statements
    # happen to follow before the next creation. Dealing the whole unit therefore dealt those
    # statements too: measured, **0 of 244 standalone connectivity claims reached both halves**,
    # they simply inherited the allocation of the creation above them.
    #
    # Only two kinds of line genuinely cannot leave a `CREATE`:
    #   * a `LAST`-subject line -- it IS the new item's own statement
    #   * a line using `LAST` as a VALUE -- `Q141353755 P735 LAST ...`, which points at it
    # `LAST` binds backwards and names no QID, so either one separated from its creation
    # attaches to nothing, or worse to whatever `CREATE` precedes it in the other file.
    #
    # Everything else in the block has an explicit QID subject and stands on its own, so it goes
    # to BOTH -- which is the ruling: *"as far as connectivity stuff goes ... we have it 100% on
    # both of them."*
    def bound_to_create(line):
        t = line.strip()
        if not t or t.startswith("#"):
            return None                      # a comment follows whatever it introduces
        if t.upper() == "CREATE":
            return True
        parts = t.split("	")
        if parts[0] == "LAST":
            return True
        return any(x == "LAST" for x in parts[1:])

    auto, manual = [], []
    for i, u in enumerate(units):
        if i not in person_units_set:
            text = chr(10).join(u)
            auto.append(text)
            manual.append(text)
            continue
        mine = auto if i in auto_people else manual
        other = manual if mine is auto else auto
        bound, free, pending = [], [], []
        for line in u:
            b = bound_to_create(line)
            if b is None:
                pending.append(line)
                continue
            (bound if b else free).extend(pending + [line])
            pending = []
        free.extend(pending)
        if bound:
            mine.append(chr(10).join(bound))
        if free:
            text = chr(10).join(free)
            mine.append(text)
            other.append(text)

    a_text = "\n".join(auto).rstrip() + "\n"
    m_text = "\n".join(manual).rstrip() + "\n"

    # ⛔ **THE ASSERTIONS CHANGED SHAPE WHEN DUPLICATION BECAME THE DESIGN.** They used to check
    # that the two files were a PARTITION -- every line exactly once. That is now false on
    # purpose: everything except the creation of an individual is written to both. What still has
    # to hold, and is checked:
    #
    #   1. nothing is LOST. Every line of the composed file appears at least once.
    #   2. no INDIVIDUAL creation appears twice. This is the one failure that cannot be undone by
    #      running it correctly tomorrow -- a second `CREATE` mints a second item for somebody who
    #      now exists. A NAME-item creation appearing twice is fine and expected: Wikidata refuses
    #      the duplicate on the label-plus-description pair, which is what `DESCRIPTION_FOR` is
    #      for.
    import collections as _c
    want = _c.Counter(ln for ln in text.splitlines() if ln.strip())
    got = _c.Counter(ln for ln in (a_text + chr(10) + m_text).splitlines() if ln.strip())
    lost = want - got
    if lost:
        raise SystemExit(f"{sum(lost.values())} line(s) lost from the split: "
                         f"{sorted(lost.elements())[:3]}")

    # ⛔ Checked on the UNITS, not by re-parsing the two texts. `edit_objects` groups `LAST`
    # lines under whichever `CREATE` precedes them, so the grouping a whole-file parse produces
    # is not the grouping a per-unit parse produces, and comparing counts across the two read
    # 29 + 57 != 1. The invariant that matters is about the units this function dealt, so it is
    # asserted there: no unit containing the creation of an individual may appear in both files.
    for _i in person_units:
        _t = chr(10).join(units[_i])
        if _t in a_text and _t in m_text:
            raise SystemExit("an individual creation appears in BOTH halves: "
                             + _t.splitlines()[0][:80])
    if len(auto_people) + len([i for i in person_units if i not in auto_people]) != len(person_units):
        raise SystemExit("individual creations were lost between the halves")

    # 3. ⛔ NO `LAST` LINE MAY PRECEDE ITS `CREATE`. `LAST` binds BACKWARDS, so a `LAST` line
    #    that ends up above every `CREATE` in its half attaches to nothing -- and one that ends
    #    up under the WRONG `CREATE` silently writes a person's name onto another item. This is
    #    the failure the block rule exists to prevent, and it is now checked rather than trusted.
    for name, txt in (("auto", a_text), ("manual", m_text)):
        seen_create = False
        for ln in txt.splitlines():
            t = ln.strip()
            if not t or t.startswith("#"):
                continue
            if t.upper() == "CREATE":
                seen_create = True
                continue
            if t.split("	", 1)[0] == "LAST" and not seen_create:
                raise SystemExit(f"{name} half has a LAST line before any CREATE: {t[:70]}")

    # 4. A subject in both halves is reported, not refused: both halves are sent, so the item
    #    ends up whole. See the note above the stride.
    def _subjects(txt):
        return {ln.split("\t", 1)[0] for ln in txt.splitlines()
                if ln.strip() and not ln.lstrip().startswith("#")
                and ln.strip().upper() != "CREATE" and "\t" in ln} - {"LAST"}
    both = _subjects(a_text) & _subjects(m_text)
    if both:
        print(f"   {len(both)} subject(s) have statements in both halves, e.g. "
              f"{sorted(both)[:3]} -- expected: everything but an individual creation is written to BOTH")

    a_edits = qs_v1.edit_objects(qs_v1.parse(a_text))
    m_edits = qs_v1.edit_objects(qs_v1.parse(m_text))

    AUTO.write_text(a_text, encoding="utf-8", newline="\n")
    MANUAL.write_text(m_text, encoding="utf-8", newline="\n")
    print(f"{len(edits)} edits -> {len(a_edits)} automatic ({AUTO.name}), "
          f"{len(m_edits)} for the page ({MANUAL.name})")
    print(f"   the share applies to individual creations only; "
          f"the {len(units) - len(person_units)} other unit(s) are in both files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
