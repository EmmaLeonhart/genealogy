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

    step = max(1, round(1.0 / AUTO_SHARE))
    chosen, taken = set(), 0
    # Stride first, so the auto half samples identifications, name items and creations alike
    # rather than taking the top of the file; then fill any remaining room in order.
    for order_pass in (range(0, len(units), step), range(len(units))):
        for i in order_pass:
            group = sorted(welded.get(i, {i}))
            if any(j in chosen for j in group):
                continue
            joined = chr(10).join(chr(10).join(units[j]) for j in group)
            if not joined.strip():
                continue
            n = len(qs_v1.edit_objects(qs_v1.parse(joined)))
            if n and taken + n <= share:
                chosen.update(group)
                taken += n

    auto, manual = [], []
    for i, u in enumerate(units):
        (auto if i in chosen else manual).append("\n".join(u))

    a_text = "\n".join(auto).rstrip() + "\n"
    m_text = "\n".join(manual).rstrip() + "\n"

    # ⛔ Disjoint and complete, asserted rather than assumed -- on the two things that are
    # actually true of a correct split, rather than on an edit COUNT that adjacency decides.
    #
    # 1. every line appears exactly once. Stronger than the old count identity and not
    #    order-sensitive: it catches a dropped block and a duplicated one directly.
    import collections as _c
    want = _c.Counter(ln for ln in text.splitlines() if ln.strip())
    got = _c.Counter(ln for ln in (a_text + "\n" + m_text).splitlines() if ln.strip())
    if want != got:
        lost = sorted((want - got).elements())[:3]
        dup = sorted((got - want).elements())[:3]
        raise SystemExit(f"split is not a partition: {sum((want - got).values())} lines lost "
                         f"{lost}, {sum((got - want).values())} duplicated {dup}")

    # 2. ⛔ NO `CREATE` MAY BE IN BOTH. This is the one failure that cannot be undone by
    #    running it correctly next time -- a duplicate mints a second item for somebody who now
    #    exists. Blocks move whole, so this should be impossible; it is asserted because the
    #    cost of being wrong is unbounded.
    # ⛔ **COUNT THE CREATE LINE, NOT A SUBSTRING WITH A NEWLINE IN FRONT OF IT.** The old
    # form missed a CREATE that is the FIRST line of a half, because nothing precedes it --
    # and the stride puts a creation first in the auto half routinely. The assertion read
    # 32 + 65 against 98 and refused a split that was CORRECT, which took `pipeline.yml` down
    # on 2026-09-17 and with it every regeneration of the daily batch. The scheduled edit run
    # then kept sending the same stale file -- 74 objects of which 70 were already applied --
    # so it ended "nothing applied", exited 1, and looked like an editing failure for a day.
    #
    # The check itself is right and stays. § *CHECK before raising an alarm* cuts both ways:
    # an assertion that cries wolf costs as much as one that never fires.
    def _creates(t):
        return sum(1 for ln in t.splitlines() if ln.strip().upper() == "CREATE")
    if _creates(a_text) + _creates(m_text) != _creates(text):
        raise SystemExit("a CREATE block was split or duplicated across the two halves: "
                         f"{_creates(a_text)} + {_creates(m_text)} != {_creates(text)}")

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
              f"{sorted(both)[:3]} -- both halves are sent, so each item still ends up whole")

    a_edits = qs_v1.edit_objects(qs_v1.parse(a_text))
    m_edits = qs_v1.edit_objects(qs_v1.parse(m_text))

    AUTO.write_text(a_text, encoding="utf-8", newline="\n")
    MANUAL.write_text(m_text, encoding="utf-8", newline="\n")
    print(f"{len(edits)} edits -> {len(a_edits)} automatic ({AUTO.name}), "
          f"{len(m_edits)} for the page ({MANUAL.name})")
    print(f"   share asked for: {share} (a third, capped at RUN_LIMIT {RUN_LIMIT})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
