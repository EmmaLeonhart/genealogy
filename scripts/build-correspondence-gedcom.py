"""The manual parental zipper correspondences, as a gitignored GEDCOM the merge consumes.

    PYTHONPATH=src python scripts/build-correspondence-gedcom.py

**Emma's design, 2026-09-05, and this is the experiment she put at the tail of the queue:**

> *"I think the manual zipper parents are wired in correctly and well, and I do not want to break
> the pipeline, but I actually think a good long term architectural smoothing would make it so
> that in the pipeline they are generated into a gitignored gedcom that is part of the synoptic
> tree merge, with qids in bios being a fundamental part of the pipeline. But for now pipeline
> works well and that will be a thing to experiment with at the end of the queue."*

`docs/correspondence-merge-proposal.md` is the proposal. This is its first half: the file is
generated **in addition**, and `build-garborg-day.ledger()` still reads
`reports/manual-identifications.csv` directly. The direct read goes only once the tree route is
shown to carry the same pairs, which is her *"do not want to break the pipeline"*.

## Why `out/` and not `exports/`

`exports/` is the corpus and **every `.ged` in it is committed** --- `tests/test_repo_invariants.py`
compares `git ls-files` against `find`, so a generated file there fails the suite the moment it is
written. This one is derived from a tracked CSV on every run, so tracking it would be a second
copy that can disagree with the first. It goes to `out/`, gitignored by its own explicit line, and
the merge is told about it with `genimerge merge --also`.

That is also why it is not simply dropped into `exports/post-merge/` beside
`wikidata-qid-links.ged`: that file is **29 hand-written pairs she named**, corpus by her choice,
and its own docstring says *"Do not let it become an architecture."* 314 rows regenerated every
run is a different kind of thing.

## ⛔ THE SLIM TREE DROPS `NOTE`, AND THAT IS THE FINDING THIS RUN PRODUCED

`genimerge.slim.DROP_INSIDE` holds `NOTE`, and `tree.yml` --- the only thing that rebuilds the
synoptic tree in Actions --- runs `--slim`. So a QID written into a bio **survives a plain merge
and does not survive the slim one**, measured rather than reasoned: see `devlog.md` 2026-09-08.

This does not make the design wrong; it names what has to change before the tree route can
replace the CSV read. It is recorded here rather than worked around, because widening the
whitelist is a memory decision (§ *the tree BUILDS in Actions* --- `NOTE` is most of what slim
removes) and quietly moving the correspondence onto a surviving tag would be writing a more
intuitive version of her program.

## The three open decisions, and the readings taken

`CLAUDE.md` § *Working the queue: GUESS. Do not ask* --- so each is decided and recorded rather
than put to her.

* **The pair only, not the verdict.** Every row of the CSV is affirmed (`SAME` 297, `RIGHT` 17)
  and `ledger()` already reads them all regardless of batch, so a verdict `NOTE` would carry no
  distinction anything acts on --- while adding a second `NOTE` per person to a merge whose size
  is the binding constraint. The provenance stays in the CSV, which is tracked and is where she
  reads it. What would switch this: a tree consumer that wants to know a pair came from the parent
  deck rather than from a bio.
* **Everything in the file, because none of it is a rejection.** The proposal called
  `rejected-parents` (24) and `blocked-creations` (12) rejections; reading the rows says otherwise
  --- all 36 carry `SAME`, and the batch name records what was rejected (a parent *link*, a
  *creation*), not the identification. So there is nothing here to filter out.
* **`bio-qids.tsv` stays a separate extract.** Turning it into a query over the merged tree is a
  second change and is not needed for *"generated in addition"*.

## Every record must already be in the tree

An `INDI` whose xref the merge has not seen is a **new person**, so an unfiltered emit would mint
people rather than annotate them --- the same guard `build-qid-links-gedcom.py` carries, and the
same failure `exports/0-scraped/` was deleted for. Checked against `reports/derived-labels.csv`,
one row per person in the merged tree; an id that fails is printed as a finding rather than
skipped quietly.
"""
from __future__ import annotations

import collections
import csv
import gzip
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

SOURCE = ROOT / "reports" / "manual-identifications.csv"
IN_TREE = ROOT / "reports" / "derived-labels.csv"
OUT = ROOT / "out" / "manual-parental-correspondences.ged"

LINK = "https://www.wikidata.org/wiki/{qid}"


def pairs_from_csv(path: Path = SOURCE) -> dict[str, set[str]]:
    """Geni id -> the QIDs it is identified with, read the way `ledger()` reads it.

    Deliberately the same test as `build-garborg-day.ledger()`: a numeric Geni id and a
    `Q`-prefixed QID. Filtering on `verdict` or `batch` here would make the tree route carry a
    different set from the CSV route, and the whole point of the experiment is that the two agree.
    """
    pairs: dict[str, set[str]] = collections.defaultdict(set)
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            g = (row.get("geni_id") or "").strip()
            q = (row.get("qid") or "").strip()
            if g.isdigit() and q.startswith("Q"):
                pairs[g].add(q)
    return dict(pairs)


def render(pairs: dict[str, set[str]]) -> str:
    """The 5.5.1 shape `wikidata-qid-links.ged` uses, because the merge is proven on it.

    Records are keyed on the xref, which is the Geni profile id, so each `INDI` here is the SAME
    record as that person in every export and its `NOTE` joins theirs. `merge.ALWAYS_REPEATABLE`
    holds `NOTE`: an identical line collapses, a different one is kept alongside, and nothing is
    overwritten. Re-generating and re-merging is idempotent.
    """
    lines = [
        "0 HEAD",
        "1 SOUR genimerge",
        "2 NAME scripts/build-correspondence-gedcom.py",
        "1 GEDC",
        "2 VERS 5.5.1",
        "2 FORM LINEAGE-LINKED",
        "1 CHAR UTF-8",
    ]
    for geni_id in sorted(pairs):
        lines.append(f"0 @I{geni_id}@ INDI")
        for qid in sorted(pairs[geni_id]):
            lines.append(f"1 NOTE {LINK.format(qid=qid)}")
    lines.append("0 TRLR")
    return "\n".join(lines) + "\n"


def people_in_tree() -> set[str] | None:
    """Everyone the merged tree holds, from the plain CSV or from the tracked `.gz` beside it.

    **The `.gz` fallback is not a nicety.** `tree.yml` runs `pack-derived.py --unpack ||
    echo "nothing to unpack"`, so a full rebuild can reach this step with no plain CSV at all
    --- and the guard below is the only thing standing between a bad id and a person invented in
    the tree. The gzipped copies are tracked, so they are there whenever the repo is.
    """
    for path, opener in ((IN_TREE, lambda p: p.open(encoding="utf-8")),
                         (IN_TREE.with_suffix(".csv.gz"),
                          lambda p: io.TextIOWrapper(gzip.open(p, "rb"), encoding="utf-8"))):
        if not path.exists():
            continue
        out = set()
        with opener(path) as fh:
            for row in csv.DictReader(fh):
                if row.get("geni_id"):
                    out.add(row["geni_id"].strip())
        print(f"{len(out):,} people in the merged tree, per {path.name}")
        return out
    return None


def main() -> int:
    pairs = pairs_from_csv()
    print(f"{len(pairs):,} pairs in {SOURCE.relative_to(ROOT)}")

    in_tree = people_in_tree()
    if in_tree is None:
        # **Write the empty file rather than failing the run.** Her constraint on this whole
        # experiment is *"I do not want to break the pipeline"*, and this step sits in front of
        # the merge in `rebuild-everything.py`. A header-only GEDCOM merges as nothing, which is
        # exactly today's behaviour: `build-garborg-day.ledger()` still reads the CSV directly,
        # so no correspondence is lost --- only the tree route is empty for this run, loudly.
        print("WARNING -- neither reports/derived-labels.csv nor its .gz is present, so no id "
              "can be checked against the tree. Emitting 0 pairs rather than minting people.")
        pairs = {}
    else:
        absent = sorted(g for g in pairs if g not in in_tree)
        if absent:
            # Never silently: emitting one of these CREATES the person rather than annotating
            # them. Printed in full because the finding is which of her verdicts names somebody
            # no export has reached.
            print(f"HELD -- not in the merged tree, would be minted as new people: {len(absent)}")
            for g in absent:
                print(f"  {g}")
            for g in absent:
                pairs.pop(g)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(pairs), encoding="utf-8", newline="\n")
    links = sum(len(qs) for qs in pairs.values())
    multi = sum(1 for qs in pairs.values() if len(qs) > 1)
    print(f"{links:,} NOTE links over {len(pairs):,} individuals; {multi} carry more than one QID")
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
