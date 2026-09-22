"""Renumber a `getmyancestors` GEDCOM so it can sit in the corpus without lying.

⛔ **getmyancestors USES OUR FOUR XREF PREFIXES WITH SEQUENTIAL INTEGERS.** Measured on
`MBW7-P7H-a12-d2.ged`, 2026-09-21: `@I1@`, `@F1@`, `@N1@`, `@S1@` — and `identity.GENI_ID_RE`
is `^@[IFNS](\\d+)@$`, so **`@I1@` parses as Geni profile 1** and `@F376@` as Geni family 376.
Small Geni ids are real people (`1015359` is one), so merging the file as written would fuse
3,103 Norwegians onto whoever happens to hold ids 1..3103.

That is the `@NI04461@` trap `CLAUDE.md` § *The primary key* records, and the `@F9<n>@` bug
`build-wikidata-gedcom.py` already hit and fixed. The answer is the same one: a prefix letter
that cannot parse.

    @I<n>@  ->  @IFS<n>@     with  1 REFN fs:<FamilySearch id>
    @F<n>@  ->  @FFS<n>@
    @N<n>@  ->  @NFS<n>@
    @S<n>@  ->  @SFS<n>@

**`_FSFTID` is where the real identifier lives** — 3,103 of 3,103 individuals carry one, and
1,339 of 1,456 families do. There is **no `RFN` anywhere in the file**, so nothing carries a
Geni id and the join to the corpus cannot be direct. `REFN fs:<id>` is added so the identifier
is readable by the same convention `build-wikidata-gedcom.py` uses for `REFN Q<digits>`, and
`_FSFTID` is left in place rather than moved, because it is what FamilySearch itself writes.

**The bridge to the corpus is `P2889` *FamilySearch person ID*:**

    _FSFTID  ->  P2889  ->  QID  ->  P2600  ->  geni id

Two exact joins through Wikidata and no name matching anywhere —
`CLAUDE.md` § *Merging is an exact join, never fuzzy name matching*.
`scripts/bridge-familysearch-qids.py` builds the first hop.

Usage:
    python scripts/render-familysearch-gedcom.py <in.ged> <out.ged>
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

#: The four record kinds `getmyancestors` emits, each mapped to the namespaced prefix. The
#: letter pair is what makes the xref unparseable as a Geni id -- verified against
#: `identity.GENI_ID_RE` by `tests/test_familysearch_gedcom.py`.
PREFIX = {"I": "IFS", "F": "FFS", "N": "NFS", "S": "SFS"}

#: An xref definition: `0 @I1@ INDI`.
#:
#: ⛔ **THE RECORD TYPE IS NOT THE END OF THE LINE.** This was anchored `(\w+)\s*$` and
#: counted **19** NOTE records where the file holds **6,490**, because a `NOTE` carries its
#: text inline -- `0 @N1@ NOTE 31 March 2015 by DA Cooper`. Only the rare empty one matched.
#: The rewriting was never affected (`PTR_RE` does not care what follows) and the leak guard
#: proved it, but a summary that under-reports by 341x is how a bad render gets waved through.
DEF_RE = re.compile(r"^0 @([IFNS])(\d+)@ (\w+)")

#: An xref used as a VALUE: `1 FAMS @F376@`, `2 NOTE @N2@`, `1 SOUR @S9@`. Also matches the
#: `0 @SUBM@ SUBM` head record's pointer, which carries no digits and is left alone.
PTR_RE = re.compile(r"@([IFNS])(\d+)@")


def rewrite(text: str) -> tuple[str, dict[str, int]]:
    """Every xref renumbered, and `REFN fs:<id>` added beside each `_FSFTID`.

    One pass for the pointers, because a definition and a reference have the same shape and
    the mapping is total: `@I1@` becomes `@IFS1@` wherever it appears, so nothing has to know
    whether it is being defined or referenced.
    """
    counts = {"INDI": 0, "FAM": 0, "NOTE": 0, "SOUR": 0, "REFN added": 0}
    for line in text.splitlines():
        m = DEF_RE.match(line)
        if m and m.group(3) in counts:
            counts[m.group(3)] += 1

    def sub(m: re.Match) -> str:
        return f"@{PREFIX[m.group(1)]}{m.group(2)}@"

    out = []
    for line in text.splitlines():
        line = PTR_RE.sub(sub, line)
        out.append(line)
        # `1 _FSFTID MBW7-P7H` -> add `1 REFN fs:MBW7-P7H` at the same level, so the
        # identifier is legible to anything reading `REFN` without teaching it `_FSFTID`.
        fs = re.match(r"^(\d) _FSFTID (\S+)\s*$", line)
        if fs:
            out.append(f"{fs.group(1)} REFN fs:{fs.group(2)}")
            counts["REFN added"] += 1
    return "\n".join(out) + "\n", counts


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    if dst.exists():
        # ⛔ `CLAUDE.md` § *Never overwrite an existing `.ged`*. A new render is a new file.
        sys.exit(f"{dst} exists. Never overwrite an existing .ged -- pick a new path.")
    text = src.read_text(encoding="utf-8")
    rendered, counts = rewrite(text)

    # The guard is checked here rather than trusted: not one xref may survive that
    # `GENI_ID_RE` would accept.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    from genimerge.identity import GENI_ID_RE
    leaked = sorted({
        tok for tok in re.findall(r"@[^@\s]+@", rendered) if GENI_ID_RE.match(tok)
    })
    if leaked:
        sys.exit(f"REFUSING: {len(leaked)} xrefs still parse as Geni ids, e.g. {leaked[:5]}")

    dst.write_text(rendered, encoding="utf-8")
    for k, v in counts.items():
        print(f"  {k:<12} {v:,}")
    print(f"\n  no xref parses as a Geni id -> {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
