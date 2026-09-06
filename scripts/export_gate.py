"""Does step 3b fire? The statistics block decides, and EVERY figure carries a threshold.

**Emma, 2026-09-06**, on bishop Camillo Ballin -- Family Tree 11, Blood Relatives 10,
Ancestors 5 -- whose Charlemagne search resolved to a genuine *"No path found"*:
*"this guy has pretty much no relatives so he shouldn't get an export lol"*.

And, when the gate was first written on Blood Relatives alone:
*"why the fuck did you choose blood relatives"*, then *"All of them need thresholds not just
blood relatives"*.

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

#: The floor per figure. Clearing ANY of these clears the gate.
#:
#: blood_relatives  -- 1,000, HER NUMBER, chosen 2026-09-06.
#: family_tree      -- the same scale: it is the component size and is never smaller than the
#:                     blood count in the readings we hold.
#: ancestors        -- 100 generations-worth of recorded line is a deep tree, not a stub.
#:                     Readings: Ballin 5, Drouillard 61, Kann 72, Anna Rood 216, Sara 396,
#:                     Arne Garborg 3,154.
#: descendants      -- 100, the same reasoning downward. Almost every isolate reads 0.
#: followers        -- 10. Followers are OTHER GENI USERS watching the profile, so a followed
#:                     profile sits in a maintained region even when its own counts are small.
#:                     Readings: Ballin 1, Arne 32.
THRESHOLDS = {
    "family_tree": 1000,
    "blood_relatives": 1000,
    "ancestors": 100,
    "descendants": 100,
    "followers": 10,
}

#: Geni's query ceilings. A figure at one of these is a FLOOR on the true value, not a count --
#: Emma, 2026-09-03: *"15,000 on any number there is a flag that the query number exceeded the
#: maximum it can do"*. Recorded so a reading can say `saturated` rather than quoting a number
#: as though it were measured.
CEILINGS = (5000, 15000)


def decide(stats: dict) -> dict:
    """Fire step 3b, or not, with the figure that decided it named.

    `stats` is the collector's statistics block: `family_tree`, `blood_relatives`, `ancestors`,
    `descendants`, `followers`. A missing key is zero.
    """
    read = {k: int(stats.get(k) or 0) for k in THRESHOLDS}
    cleared = [k for k, v in read.items() if v >= THRESHOLDS[k]]
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
            "cleared by " + ", ".join("%s=%d>=%d" % (k, read[k], THRESHOLDS[k]) for k in cleared)
        ),
    }
