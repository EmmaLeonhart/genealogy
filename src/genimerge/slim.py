"""What the editing pipeline reads, and nothing else — the merge's input filter.

**Anything that does not go into the editing pipeline is not needed in the synoptic tree.**

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
`find_exports()` — the raw corpus — not the merged tree, so the Wikidata links in Geni
*About Me* survive whatever this drops. `exports/` is never touched by any of this.
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
    # ⛔ **THE STRUCTURED ADDRESS BLOCK IS GONE, 2026-09-10.** It was kept on the grounds that
    # *"every one of these is read by derive-facts.py"* — true, and the wrong test. `derive-facts`
    # reads them and writes `birth_address` / `death_address` / `burial_address`, and **NOTHING
    # READS THOSE COLUMNS.** Nor does any place statement exist: `grep P19|P20|P119` over every
    # `.qs` and the daily batch returns **nothing**, so a place has never reached Wikidata.
    #
    # Measured over 3,477 exports rather than guessed:
    #
    #     ADDR ADR1 ADR2 ADR3 CITY CTRY POST STAE   124,880,269 bytes  3.03%  8,741,947 lines
    #     PLAC                                        42,280,646 bytes  1.02%  1,536,400 lines
    #
    # The address block is THREE TIMES the size of `PLAC` and has no consumer at all. Against the
    # slim union merge's 15,428 MB peak that is roughly **467 MB** returned for nothing given up.
    #
    # ⛔ **AND `PLAC` GOES TOO. RULED 2026-09-10: places do not belong in the synoptic tree.**
    # *"I genuinely think keeping the places in the synoptic tree is a horrible idea"*, and on
    # the one thing that read them: *"there was an algorithm, and it failed miserably"*.
    #
    # The place words were **culture evidence 1** in `build-cjk-romanisation.py`, matched against
    # country and region words to decide whether a CJK person is `ja`, `zh` or `ko`. Keeping
    # `PLAC` for that was argued here yesterday and the argument is WITHDRAWN: the classifier is
    # judged not to have worked, and the replacement is a person reading them --
    # *"best thing will just be me manually reviewing these people"*.
    #
    # **It is evidence 1 of five and the other four are untouched** -- the `NAME`'s own form,
    # graph traversal over relatives, what the surname is judged by the settled records, and
    # export provenance. So this narrows the classifier rather than disabling it, and its
    # evidence 0 was already withdrawn on 2026-08-19 for being wrong in the same way.
    #
    # 42,280,646 bytes over 1,536,400 lines. Nothing else reads a place at all: no `P19`, `P20`
    # or `P119` statement has ever been emitted, which `tests/test_slim.py` pins.
    # what the Wikidata model emits: P106 occupation, P97 noble title
    "OCCU", "TITL",
    # relationships — derive-family.py
    "FAMC", "FAMS", "HUSB", "WIFE", "CHIL",
    # CLAUDE.md "Later sources win": INDI.CHAN.DATE is the tiebreaker
    "CHAN",
    # continuation of a KEPT value only — a dropped node takes its children, so these survive
    # under a kept value and never under NOTE. **They used to be described as surviving "under
    # ADDR", and ADDR is gone**: what they hang off now is a long NAME or TITL.
    "CONT", "CONC",
    # header fields the parser expects to find
    "SOUR", "VERS", "GEDC", "FORM", "CHAR", "LANG", "DEST", "FILE",
})

#: Dropped with everything nested under them, inside `INDI`/`FAM` only.
#: `SOUR` and `FILE` are legitimate in `HEAD`, which is why this is separate
#: from `KEEP_TAGS` rather than carved out of it.
DROP_INSIDE = frozenset({"NOTE", "SOUR", "OBJE", "FILE", "TEXT", "REPO", "PAGE", "DATA"})


#: ⛔ CONNECTIVITY ONLY -- the tightest the tree can be and still answer the campaign's question.
#:
#: The campaign asks one thing of the tree: **is this person connected to Charlemagne**. That
#: needs the primary key, the sex (a `FAM` slot is sex-typed) and the five structural pointers,
#: and nothing else. Measured over a 60-export sample: the ordinary slim keeps ~73% of corpus
#: bytes and this keeps **~19%**, roughly a four-fold reduction on top of the slim.
#:
#: **It is a DIFFERENT TREE, not a smaller one, and that is why it is its own flag.** Names,
#: dates, places, occupations and titles are gone, so `build-display-names.py`, `derive-labels.py`
#: and `derive-facts.py` cannot run against it and the QuickStatements pipeline cannot be built
#: from it. It exists to answer connectivity at a size where the Wikidata union fits, and the
#: derive scripts keep using the ordinary slim.
#:
#: `SEX` is kept deliberately: `HUSB`/`WIFE` are sex-typed slots, so dropping it would make a
#: single-parent family unplaceable.
CONNECTIVITY_TAGS = frozenset({
    "RFN", "REFN", "SEX",
    "FAMC", "FAMS", "HUSB", "WIFE", "CHIL",
    # header fields the parser expects to find
    "SOUR", "VERS", "GEDC", "FORM", "CHAR", "LANG", "DEST", "FILE",
})


def _prune(node: Node, inside_record: bool, keep=KEEP_TAGS) -> None:
    """Drop non-whitelisted children, in place, depth first."""
    kept = []
    for child in node.children:
        if inside_record and child.tag in DROP_INSIDE:
            continue
        if child.tag not in keep:
            continue
        _prune(child, inside_record, keep)
        kept.append(child)
    node.children = kept


def prune_record(record: Node, keep=KEEP_TAGS) -> Node | None:
    """The record with everything the pipeline never reads removed, or `None` to drop it."""
    if record.tag not in KEEP_RECORDS:
        return None
    _prune(record, record.tag in ("INDI", "FAM"), keep)
    return record


def prune_stream(records, keep=KEEP_TAGS):
    """Wrap a record iterator, dropping what the pipeline never reads."""
    for record in records:
        pruned = prune_record(record, keep)
        if pruned is not None:
            yield pruned
