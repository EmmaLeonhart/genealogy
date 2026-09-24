"""Run edit objects in an order their own `requires` allows.

**The design, 2026-08-23:** an edit object is selected at random; if its requirements
are present it runs, and if not another is selected at random and run instead.

That is a randomised topological execution, and randomised is a feature rather than a
concession: nothing about the batches implies an order beyond `requires`, so imposing
one would be inventing a claim. Picking at random and checking makes the only real
constraint the only constraint applied.

**Why it matters at all.** 284,125 edit objects declare a `requires` list and, until
this module, nothing read it. `CLAUDE.md` leans on that ordering where it is most
dangerous: the `NN` fix is two edits per item, the `mul` one declared as a dependency
of the `en` one, *"so the marker is written before the slot holding it is reused"*.
On the **1,271** items whose only `NN` lives in `en`, running the `en` edit first
erases the marker. The dependency is already written down; this is what honours it.

**Nothing here sends anything.** It orders edits and reports what it cannot order.
Whoever executes them supplies the `run` callable, so this stays testable and stays
offline.
"""
from __future__ import annotations

import random
from typing import Callable, Iterable, Sequence

__all__ = ["Blocked", "runnable_order", "run_when_ready"]


class Blocked(Exception):
    """Raised when edits remain but none of them can ever be unblocked.

    Distinct from finishing: an executor that treats "nothing runnable" as "done"
    would silently drop the tail, which is the failure mode this module exists to
    prevent.
    """

    def __init__(self, remaining: Sequence[dict]) -> None:
        self.remaining = list(remaining)
        ids = [e.get("id") for e in self.remaining[:5]]
        super().__init__(
            f"{len(self.remaining)} edits cannot be unblocked, e.g. {ids}")


def _needs(edit: dict) -> list:
    return [r for r in (edit.get("requires") or [])]


def runnable_order(edits: Iterable[dict], *, seed: int | None = None,
                   satisfied: Iterable | None = None, ordered: bool = False) -> list[dict]:
    """The edits, in an order where no edit precedes anything it requires.

    ``satisfied`` names ids already applied in an earlier run, so a resumed batch
    does not deadlock on work that is genuinely done.

    A dependency naming an id **no edit in this set carries** is treated as
    unsatisfiable, not ignored. Pretending otherwise is how 55,776 dangling
    dependencies sat unnoticed until 2026-08-23: the batches looked ordered
    because nothing checked.

    **The pick is random, from the set that is ready.** The design is to select an
    edit object at random, run it if its requirements are present, and otherwise
    select another at random -- and a first
    implementation did exactly that literally, rescanning every pending edit on every
    pick. That is O(n^2): over the real 284,125 objects it ran for **ten minutes
    without finishing**. Choosing at random from the ready set gives the same
    distribution of outcomes in O(V+E), because an edit that is not ready would have
    been rejected anyway.
    """
    pending = list(edits)
    # ``ordered``: the earliest ready edit by its position in the batch instead of a random
    # one. Ruled 2026-09-24 for the daily automatic half, which `split-daily-batch.py` writes
    # in the order it must be sent -- names, 30 individuals, the ring, then the rest -- so the
    # rate limit, when it bites, cuts the tail and never the rings.
    position = {id(e): n for n, e in enumerate(pending)}
    done = set(satisfied or ())
    by_id = {e.get("id"): e for e in pending}

    # How many unmet requirements each edit still has, and who is waiting on each id.
    outstanding: dict = {}
    waiting: dict = {}
    ready = []
    for e in pending:
        need = [r for r in _needs(e) if r not in done]
        outstanding[id(e)] = len(need)
        if need:
            for r in need:
                waiting.setdefault(r, []).append(e)
        else:
            ready.append(e)

    rng = random.Random(seed)
    out: list[dict] = []
    placed = 0
    # ⛔ **WHAT AN EDIT UNBLOCKS RUNS NEXT, NOT WHENEVER THE DICE SAY.** Ruled 2026-09-18:
    # *"Whenever you create an individual or an item or whatever, it's always supposed to be
    # linked immediately after its creation."*
    #
    # A `CREATE` fuses with its `LAST`-SUBJECT lines already, but a line whose subject is a QID
    # and whose value is `LAST` -- `Q... P40 LAST`, an existing person pointing at the new one --
    # is its own edit object carrying `requires`. Dropping it back into the random pool let it
    # land arbitrarily later, so the run emitted a block of creations and linked them afterwards.
    # Measured on the 18:57 burst: 11 `wbeditentity-create-item` interleaved with only 11
    # `wbsetclaim`, creations running two and three deep before a link followed.
    #
    # **A new item with nothing pointing at it is what gets an account flagged**, and the gap is
    # the whole risk: the item is live and orphaned for as long as the ordering leaves it that
    # way. Randomness was chosen because *"nothing about the batches implies an order beyond
    # `requires`"* -- but this is an order the batches DO imply, written down in
    # docs/rules/wikidata-editing.md, and it was simply not being read.
    #
    # `urgent` is FIFO so several links behind one create keep the order they were written in,
    # and the random pool still governs everything genuinely independent.
    from collections import deque
    urgent: deque = deque()
    while ready or urgent:
        if urgent:
            chosen = urgent.popleft()
        elif ordered:
            i = min(range(len(ready)), key=lambda k: position[id(ready[k])])
            chosen = ready.pop(i)
        else:
            # Random index, swapped with the last element: O(1) removal, and the same
            # uniform choice a scan-and-pick would have made.
            i = rng.randrange(len(ready))
            ready[i], ready[-1] = ready[-1], ready[i]
            chosen = ready.pop()
        out.append(chosen)
        placed += 1
        for waiter in waiting.pop(chosen.get("id"), ()):
            outstanding[id(waiter)] -= 1
            if outstanding[id(waiter)] == 0:
                urgent.append(waiter)

    if placed != len(pending):
        stuck = [e for e in pending if outstanding[id(e)] > 0]
        raise Blocked(stuck)

    del by_id      # named above so a caller reading the source sees the id space
    return out


def run_when_ready(edits: Iterable[dict], run: Callable[[dict], object], *,
                   seed: int | None = None,
                   satisfied: Iterable | None = None) -> list:
    """Apply `run` to each edit once its requirements have been applied.

    Returns whatever `run` returned, in execution order. Raises `Blocked` before
    running anything if the set cannot be ordered at all — better to refuse the
    whole batch than to half-apply one and leave a wiki mid-edit.
    """
    order = runnable_order(edits, seed=seed, satisfied=satisfied)
    return [run(e) for e in order]
