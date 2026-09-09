"""Does step 3b fire? The statistics block decides, and EVERY figure carries a threshold.

**Emma, 2026-09-06**, on bishop Camillo Ballin -- Family Tree 11, Blood Relatives 10,
Ancestors 5 -- whose Charlemagne search resolved to a genuine *"No path found"*:
*"this guy has pretty much no relatives so he shouldn't get an export lol"*.

**⛔ SHE NEVER ASKED FOR BLOOD RELATIVES. That was mine, twice over.** The question put to her
offered four floors and every one of them was written in `blood_relatives`, so the only thing she
chose out of it was the **number**, 1,000. Her replies: *"why the fuck did you choose blood
relatives"*, and then *"All of them need thresholds not just blood relatives"* -- and afterwards,
reading a report that described it as a gate she had struck out: *"I didn't tell you to do blood
relatives."*

She is right and the distinction matters for the record: a question whose options share a wrong
premise does not become her decision because she answered it. `CLAUDE.md` § *She answers
`AskUserQuestion`* says every option must be one she could actually pick; it needs the other half
too -- **the axis is part of the question, and offering only one is choosing it for her.**

## Why this is the mirror of a rule that already existed

`CLAUDE.md` § *THE STATISTICS BLOCK IS THE REAL INSTRUMENT* says a **saturated** figure beside a
*"no relationship found"* means a database failure rather than a real negative -- her words,
*"15,000 blood relatives or really any of these numbers being high on this scale indicates that
they are in the world tree but it was a database failure."*

This is the other end of the same instrument. A **tiny** figure beside the same sentence means the
miss is REAL: the person's whole neighbourhood is the handful already on the page, and a `Forest`
export seeded there returns that handful and connects nothing. Ballin's export would have come
back with about eleven people.

## Disjunctive, because each figure is independent evidence

A person clears the gate if **any one** figure clears its own threshold. They measure different
things and a person can be evidently connected by any of them: deep ancestry with few living
relatives, wide descent with a shallow line, a heavily-followed profile in a managed region.
Requiring all five would gate on the smallest number, which is the one that says least.

**`family_tree` is the component size and is the primary figure** -- that is what an export can
actually reach, and a `Forest` export follows spouse links precisely to cross the in-law edges
`blood_relatives` excludes. Her own Drouillard reading led with it.

**A MISSING ROW MEANS ZERO, never unknown** -- Emma, 2026-09-03, on Dorothy Jeakins having no
Ancestors row at all: *"geni is weird and gives zero as not an option there"*. So a `None` here
is read as 0 and fails its threshold, which is the conservative direction: it withholds an
export rather than spending one.

**The numbers are hers where she gave one and a recorded guess where she did not.** She chose
1,000 for `blood_relatives` explicitly. The rest are set on the same scale as the figures they
read, and every one is a threshold to be corrected by measurement rather than a law.
"""

from __future__ import annotations

#: ⛔ ONE FLOOR, ACROSS EVERY FIGURE. Emma, 2026-09-06: *"Any number over 1,000 is a sure export,
#: i say even any number over 300 lol"*.
#:
#: This replaced five separate thresholds — 1,000 / 1,000 / 100 / 100 / 10, one per figure, which
#: were mine. Her sentence collapses them: it is not a per-figure judgement at all, it is a single
#: reading of when the statistics block says there is more there than the page shows. **Whichever
#: figure carries the number, over 300 is enough.**
#:
#: Note what moved and what did not. The two big figures came DOWN from 1,000, which is the point
#: — Valentine Eisner reads Family Tree 914 and was skipped by 86 under the old floor. The three
#: small ones went UP, from 100 / 100 / 10, so a profile with 12 followers no longer clears on
#: that alone; her sentence is a floor on the evidence, not a licence for the weakest figure.
FLOOR = 300

#: Geni's query ceilings. A figure at one of these is a FLOOR on the true value, not a count --
#: Emma, 2026-09-03: *"15,000 on any number there is a flag that the query number exceeded the
#: maximum it can do"*. Recorded so a reading can say `saturated` rather than quoting a number
#: as though it were measured.
CEILINGS = (5000, 15000)

#: The figures the block carries, in the order Geni prints them.
FIGURES = ("family_tree", "blood_relatives", "ancestors", "descendants", "followers")


def decide(stats: dict) -> dict:
    """Fire step 3b, or not, with the figure that decided it named.

    `stats` is the collector's statistics block: `family_tree`, `blood_relatives`, `ancestors`,
    `descendants`, `followers`. A missing key is zero. Any one figure at or above `FLOOR` clears.
    """
    read = {k: int(stats.get(k) or 0) for k in FIGURES}
    cleared = [k for k, v in read.items() if v >= FLOOR]
    saturated = [k for k, v in read.items() if v in CEILINGS]
    return {
        "export": bool(cleared),
        "cleared": cleared,
        "saturated": saturated,
        "read": read,
        "why": (
            "no figure clears its threshold; the miss is real and an export would return "
            "only what is already on the page"
            if not cleared else
            "cleared by " + ", ".join("%s=%d>=%d" % (k, read[k], FLOOR) for k in cleared)
        ),
    }
