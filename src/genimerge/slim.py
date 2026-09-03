"""What the editing pipeline reads, and nothing else — the merge's input filter.

**Emma, 2026-09-03:** *"realistically anything that doesn't go into the editing pipeline isn't
needed in the synoptic tree."*

**Measured, and it is what makes the tree buildable in Actions:**

    full corpus   peak RSS 13.30 GB, KILLED at 13.3 min  (runner: 15.92 GB, killed at 21.6 min)
    slimmed       peak RSS  8.79 GB, done in 7.7 min
    same tree     1,451,993 people · 630,053 families

**Why the merge is that expensive, so nobody re-derives it.** `Merger.records` holds the whole
tree as Python objects at once — it must, because merging is keyed on the xref and any of the 607
exports can add to any record, so nothing is releasable until the last file is read. A tree of
small Python objects costs 20-40x its source text: 409 MB of GEDCOM against a 13-16 GB peak. It is
not a leak, and no amount of tuning the merge fixes it. **The input is the only lever.**

**What is dropped, measured over 121,922,222 corpus lines:** `CONT` 31.8%, `CONC` 20.7%,
`FILE` 7.3%, `NOTE` 4.5%, `TEXT` 1.5% — about **67% of corpus bytes**, against ~6% for names and
~6% for relationships. `Node` folds `CONC`/`CONT` into `value`, so that half is not node overhead
but raw string payload sitting inside records the merge holds anyway.

**`KEEP_TAGS` is the union of the four derive scripts' own tag lists**, read out of them rather
than guessed: `build-display-names.py`, `derive-labels.py`, `derive-family.py`,
`derive-facts.py`. It is a WHITELIST on purpose — a tag nobody named is dropped with its whole
subtree, so a Geni tag added next month is excluded loudly by omission instead of silently
swelling the merge again.

**This is OPT-IN and the default is unchanged.** `genimerge merge --slim` and `tree.yml` use it;
a plain `genimerge merge` still produces the complete tree. That reading was taken rather than
asked: `prepare-cases.py` and `samaritan_spine.py` read `NOTE` out of the merged tree, and a
default that silently removed it would break them for a benefit only CI needs. What would falsify
it is those two moving off the merged tree, after which the flag could become the default.

**Bio QIDs are NOT lost, checked rather than assumed.** `scripts/extract-bio-qids.py` reads
`find_exports()` — the raw corpus — not the merged tree, so her Wikidata links in Geni *About Me*
survive whatever this drops. `exports/` is never touched by any of this.
"""

from __future__ import annotations

from .gedcom import Node

#: Level-0 records kept. `NOTE` and `SOUR` records are dropped whole.
KEEP_RECORDS = frozenset({"HEAD", "INDI", "FAM", "SUBM", "TRLR"})

#: Kept inside a kept record. Grouped by which derive script needs them.
KEEP_TAGS = frozenset({
    # names — build-display-names.py
    "NAME", "GIVN", "SURN", "_MARNM", "NICK", "NPFX", "NSFX", "SPFX",
    # identity and sex — the Geni id is the primary key, RFN corroborates it
    "SEX", "RFN", "REFN",
    # events and dates — derive-facts.py
    "BIRT", "DEAT", "BURI", "CHR", "CREM", "MARR", "DIV", "DATE",
    # places — every one of these is read by derive-facts.py
    "PLAC", "ADDR", "ADR1", "ADR2", "ADR3", "CITY", "CTRY", "POST", "STAE",
    # what the Wikidata model emits: P106 occupation, P97 noble title
    "OCCU", "TITL",
    # relationships — derive-family.py
    "FAMC", "FAMS", "HUSB", "WIFE", "CHIL",
    # CLAUDE.md "Later sources win": INDI.CHAN.DATE is the tiebreaker
    "CHAN",
    # continuation of a KEPT value only — a dropped node takes its children,
    # so these survive under ADDR and never under NOTE
    "CONT", "CONC",
    # header fields the parser expects to find
    "SOUR", "VERS", "GEDC", "FORM", "CHAR", "LANG", "DEST", "FILE",
})

#: Dropped with everything nested under them, inside `INDI`/`FAM` only.
#: `SOUR` and `FILE` are legitimate in `HEAD`, which is why this is separate
#: from `KEEP_TAGS` rather than carved out of it.
DROP_INSIDE = frozenset({"NOTE", "SOUR", "OBJE", "FILE", "TEXT", "REPO", "PAGE", "DATA"})


def _prune(node: Node, inside_record: bool) -> None:
    """Drop non-whitelisted children, in place, depth first."""
    kept = []
    for child in node.children:
        if inside_record and child.tag in DROP_INSIDE:
            continue
        if child.tag not in KEEP_TAGS:
            continue
        _prune(child, inside_record)
        kept.append(child)
    node.children = kept


def prune_record(record: Node) -> Node | None:
    """The record with everything the pipeline never reads removed, or `None` to drop it."""
    if record.tag not in KEEP_RECORDS:
        return None
    _prune(record, record.tag in ("INDI", "FAM"))
    return record


def prune_stream(records):
    """Wrap a record iterator, dropping what the pipeline never reads."""
    for record in records:
        pruned = prune_record(record)
        if pruned is not None:
            yield pruned
