"""The description a created item carries, and the one rule it exists to enforce.

⛔ **THERE IS NO SUCH THING AS "NO DESCRIPTION", AND NO TWO OF OURS MAY MATCH.** Ruled
2026-09-21, while duplicates were still coming out of the batches: *"no description info means
geni id referencing description not no description"*, and *"we're making too many duplicates and
it's bothersome"*.

**Wikibase refuses a creation only when the label AND a NON-EMPTY description both match.** So a
blank description is not a weak guard, it is the absence of one — and two items of ours carrying
the same label and the same description are a duplicate we create and then have to merge by
hand. `Anders Jørgensen Heier` exists as both `Q141504247` and `Q141502696` through exactly that
hole, and the `Den` that would have refused the second was emitted so late that the duplicate
was already fully furnished before the guard fired.

Two failures, one fix:

* **the empty description** — a person with no dates, no places and no named relative used to
  get nothing at all.
* **the colliding description** — two people with the same name and the same dates get the same
  string, which is the commonest shape in a Scandinavian corpus and no guard at all.

Both are closed by falling through to **the identifier**, which is unique by construction
because it is the primary key of whichever source the person came from:

    Geni 6000000000757999620
    FamilySearch MBW7-P7H

It is a pointer rather than a sentence, deliberately. When nothing is known about the person, it
describes the RECORD we hold instead of describing nobody — and it is what the person doing a
merge needs to see anyway.

**This module is shared because a guard in one emitter is not a guard.** `CLAUDE.md` says so of
the name rules and it is the same argument here: there are two emitters writing `CREATE` blocks
and there would have been two copies of this, diverging.
"""
from __future__ import annotations

import re

#: How an identifier is written into a description. The source name first, because the
#: description is read by a person deciding whether two items are the same human, and a bare
#: number says nothing about which database it is a key in.
SOURCE_WORD = {"P2600": "Geni", "P2889": "FamilySearch"}

#: `LAST<TAB>Den<TAB>"..."` — the description line inside a `CREATE` block.
_DEN = re.compile(r'^LAST\tDen\t"(.*)"$')
#: `LAST<TAB>Lmul<TAB>"..."` — the label the duplication is judged on, with `Len` as the
#: fallback for a block that carries no `mul` label.
_LABEL = re.compile(r'^LAST\t(?:Lmul|Len)\t"(.*)"$')


def id_description(prop: str, value: str) -> str:
    """`id_description("P2889", "MBW7-P7H")` -> `"FamilySearch MBW7-P7H"`.

    An unknown property falls back to the property id itself rather than to nothing, because
    nothing is the one answer this module exists to refuse.
    """
    value = (value or "").strip()
    if not value:
        return ""
    return f"{SOURCE_WORD.get(prop, prop)} {value}"


def deduplicate(lines, id_prop):
    """Give every `CREATE` block a description, and make no two of them the same pair.

    `lines` is the assembled batch; `id_prop` is the identifier property its `CREATE` blocks
    carry — `P2600` for the Geni batch, `P2889` for the FamilySearch one. Two things happen,
    and they are the two halves of the same failure:

    * **a block with NO `Den` gets one**, inserted straight after its label, reading
      `Geni <id>` / `FamilySearch <id>`. A blank description is the absence of the guard.
    * **a block whose `(label, description)` pair has already been seen** has the identifier
      appended to its description: `1400 Bergen - 1460 (Geni 6000000001234567890)`.

    ⛔ **It reads the ASSEMBLED file rather than the loop that built it**, for the reason
    `check-batch-locality.py` gives about the locality gate: passes run after the composer,
    and a guard the composer alone applies is one appended section away from being no guard.

    ⛔ **The description must land beside the LABEL, not at the end of the block.**
    QuickStatements applies a `CREATE` line by line, so a `Den` emitted last means the item is
    born label-only and is fully furnished before the guard can refuse anything —
    `Anders Jørgensen Heier` is `Q141504247` and `Q141502696` for exactly that reason. An
    inserted description therefore goes immediately after the label line it was missing from.

    Returns how many blocks it had to touch.
    """
    edits = []                 # (index, replacement_line) or (index, None, inserted_line)
    seen = set()
    changed = 0

    def block_bounds():
        """`[(start, end)]` for every `CREATE` block, end exclusive."""
        starts = [n for n, l in enumerate(lines) if l == "CREATE"]
        return [(s, starts[i + 1] if i + 1 < len(starts) else len(lines))
                for i, s in enumerate(starts)]

    for start, end in block_bounds():
        label = desc = ident = None
        label_at = desc_at = None
        for n in range(start + 1, end):
            line = lines[n]
            m = _LABEL.match(line)
            if m and label is None:
                label, label_at = m.group(1), n
            m = _DEN.match(line)
            if m and desc is None:
                desc, desc_at = m.group(1), n
            if line.startswith(f"LAST\t{id_prop}\t\""):
                ident = line.split("\t")[2].strip('"')
        if label is None or not ident:
            # Nothing to key on, or no identifier to fall back to. Left exactly as it was
            # rather than guessed at — this function never invents a description out of a
            # label it does not understand.
            continue
        if desc is None:
            edits.append((label_at + 1, None, f'LAST\tDen\t"{id_description(id_prop, ident)}"'))
            desc = id_description(id_prop, ident)
            changed += 1
        elif (label, desc) in seen:
            edits.append((desc_at, f'LAST\tDen\t"{desc} ({id_description(id_prop, ident)})"',
                          None))
            desc = f"{desc} ({id_description(id_prop, ident)})"
            changed += 1
        seen.add((label, desc))

    # Applied back to front so an insertion never moves an index still to be used.
    for edit in sorted(edits, key=lambda e: -e[0]):
        at, replacement, insertion = edit
        if replacement is not None:
            lines[at] = replacement
        else:
            lines.insert(at, insertion)
    return changed
