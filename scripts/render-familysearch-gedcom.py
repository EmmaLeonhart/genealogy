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

⛔ **AND A BRIDGED PERSON IS WRITTEN ON THEIR GENI XREF, OR THE TREE NEVER ATTACHES.** Found
2026-09-24 on `Q141539855` Emma Olivia Andersdotter, who is in the owner's FamilySearch tree
and appeared nowhere: the first render numbered everyone `@IFS<n>@`, so not one line of it
could fuse with the corpus, and the 3,103 people of `MBW7-P7H` sat in `merged.ged` as a
component of their own. A person the bridge resolves is now `@I<geni id>@` with
`1 RFN geni:<id>` -- the same record key the Geni exports use, so the merge joins them exactly
and everybody else in the FamilySearch file hangs off them.

⛔ **AND THE XREF IS THE FAMILYSEARCH ID, NOT A PER-FILE COUNTER.** The merge keys records on
the xref string, and every `getmyancestors` file numbers from 1 -- so `@IFS1@` is the owner in
`PFR5-LDS` and Inger in `MBW7-P7H`, and two renders would have fused them. `@IFS<id>@` (hyphen
dropped) is the same person in every file. Records with no `_FSFTID`, and every `NOTE` and
`SOUR`, carry the file's own seed id instead, which keeps them apart.

Usage:
    python scripts/render-familysearch-gedcom.py <in.ged> <out.ged>     one file, never overwrites
    python scripts/render-familysearch-gedcom.py --all                  every download, for CI

`--all` renders each `gedcom/familysearch/*.ged` into `exports/familysearch/` and DOES replace
its own previous output: the render is a function of an original that is never rewritten and of
the bridge, which grows, so a stale render is the one thing it must not keep.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "gedcom" / "familysearch"
OUT_DIR = ROOT / "exports" / "familysearch"
BRIDGE = ROOT / "reports" / "familysearch-qid-bridge.tsv"

#: The four record kinds `getmyancestors` emits, each mapped to the namespaced prefix. The
#: letter pair is what makes the xref unparseable as a Geni id -- verified against
#: `identity.GENI_ID_RE` by `tests/test_familysearch_gedcom.py`.
PREFIX = {"I": "IFS", "F": "FFS", "N": "NFS", "S": "SFS"}

#: An xref definition: `0 @I1@ INDI`.
#:
#: ⛔ **THE RECORD TYPE IS NOT THE END OF THE LINE.** This was anchored `(\w+)\s*$` and
#: counted **19** NOTE records where the file holds **6,490**, because a `NOTE` carries its
#: text inline -- `0 @N1@ NOTE 31 March 2015 by DA Cooper`. Only the rare empty one matched.
DEF_RE = re.compile(r"^0 @([IFNS])(\d+)@ (\w+)")

#: An xref used as a VALUE: `1 FAMS @F376@`, `2 NOTE @N2@`, `1 SOUR @S9@`. Also matches the
#: `0 @SUBM@ SUBM` head record's pointer, which carries no digits and is left alone.
PTR_RE = re.compile(r"@([IFNS])(\d+)@")

FSID_RE = re.compile(r"^1 _FSFTID (\S+)\s*$")


def clean(fs_id: str) -> str:
    """`GF2B-NKG` -> `GF2BNKG`: an xref is letters and digits."""
    return re.sub(r"[^0-9A-Za-z]", "", fs_id).upper()


def load_bridge(path: Path = BRIDGE) -> dict[str, str]:
    """`{fs_id: geni_id}` for every FamilySearch person the bridge resolves to a Geni id."""
    if not path.exists():
        return {}
    with open(path, encoding="utf-8", newline="") as fh:
        return {r["fs_id"]: r["geni_id"] for r in csv.DictReader(fh, delimiter="\t")
                if r.get("fs_id") and r.get("geni_id")}


def rewrite(text: str, bridge: dict[str, str] | None = None,
            seed: str = "") -> tuple[str, dict[str, int]]:
    """Every xref renumbered onto a key that means the same thing in every file.

    `bridge` is `{fs_id: geni_id}`; `seed` is the file's own FamilySearch id, used for the
    records that have none of their own.
    """
    bridge = bridge or {}
    seed = clean(seed)
    counts = {"INDI": 0, "FAM": 0, "NOTE": 0, "SOUR": 0, "REFN added": 0, "bridged": 0}

    # Pass 1: which FamilySearch id each INDI and FAM record carries.
    fs_of, current = {}, None
    for line in text.splitlines():
        m = DEF_RE.match(line)
        if m:
            current = (m.group(1), m.group(2))
            if m.group(3) in counts:
                counts[m.group(3)] += 1
            continue
        if line.startswith("0 "):
            current = None
            continue
        f = FSID_RE.match(line)
        if f and current and current[0] in "IF":
            fs_of.setdefault(current, f.group(1))

    # One Geni id may be claimed by one record only; a second FamilySearch person bridged to
    # the same profile keeps its own key rather than colliding.
    target, used = {}, set()
    for (kind, n), fs in fs_of.items():
        g = bridge.get(fs) if kind == "I" else None
        if g and g not in used:
            used.add(g)
            target[(kind, n)] = f"I{g}"
            counts["bridged"] += 1
        else:
            target[(kind, n)] = f"{PREFIX[kind]}{clean(fs)}"

    def key(kind: str, n: str) -> str:
        return target.get((kind, n)) or f"{PREFIX[kind]}{seed}X{n}"

    def sub(m: re.Match) -> str:
        return f"@{key(m.group(1), m.group(2))}@"

    out = []
    for line in text.splitlines():
        d = DEF_RE.match(line)
        out.append(PTR_RE.sub(sub, line))
        if d and d.group(1) == "I" and key("I", d.group(2)).startswith("I") \
                and key("I", d.group(2))[1:].isdigit():
            out.append(f"1 RFN geni:{key('I', d.group(2))[1:]}")
        # `1 _FSFTID MBW7-P7H` -> add `1 REFN fs:MBW7-P7H` at the same level, so the
        # identifier is legible to anything reading `REFN` without teaching it `_FSFTID`.
        fs = re.match(r"^(\d) _FSFTID (\S+)\s*$", line)
        if fs:
            out.append(f"{fs.group(1)} REFN fs:{fs.group(2)}")
            counts["REFN added"] += 1
    return "\n".join(out) + "\n", counts


def leaks(rendered: str) -> list[str]:
    """Xrefs that parse as Geni ids WITHOUT being a person the bridge put there on purpose."""
    sys.path.insert(0, str(ROOT / "src"))
    from genimerge.identity import GENI_ID_RE
    meant = set(re.findall(r"^0 (@I\d+@) INDI\n1 RFN geni:", rendered, re.M))
    return sorted({tok for tok in re.findall(r"@[^@\s]+@", rendered)
                   if GENI_ID_RE.match(tok) and tok not in meant})


def render(src: Path, dst: Path, bridge: dict[str, str]) -> dict[str, int]:
    seed = src.name.split("-a")[0] if re.search(r"-a\d+-d\d+", src.name) else src.stem
    rendered, counts = rewrite(src.read_text(encoding="utf-8"), bridge, seed)
    bad = leaks(rendered)
    if bad:
        sys.exit(f"REFUSING {src.name}: {len(bad)} xrefs still parse as Geni ids, e.g. {bad[:5]}")
    dst.write_text(rendered, encoding="utf-8")
    return counts


def out_name(src: Path) -> str:
    """`MBW7-P7H-a12-d2.ged` -> `MBW7-P7H-ancestors12-descendants2.ged`."""
    m = re.match(r"^(.*)-a(\d+)-d(\d+)$", src.stem)
    return f"{m.group(1)}-ancestors{m.group(2)}-descendants{m.group(3)}.ged" if m \
        else f"{src.stem}.ged"


def main() -> int:
    if sys.argv[1:] == ["--all"]:
        bridge = load_bridge()
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        for src in sorted(SRC_DIR.glob("*.ged")):
            if "-test" in src.stem:
                continue
            counts = render(src, OUT_DIR / out_name(src), bridge)
            print(f"  {src.name} -> {out_name(src)}: {counts['INDI']:,} people, "
                  f"{counts['bridged']:,} on their Geni id")
        return 0
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    if dst.exists():
        # ⛔ `CLAUDE.md` § *Never overwrite an existing `.ged`*. A one-off render is a new file.
        sys.exit(f"{dst} exists. Never overwrite an existing .ged -- pick a new path.")
    counts = render(src, dst, load_bridge())
    for k, v in counts.items():
        print(f"  {k:<12} {v:,}")
    print(f"\n  no stray xref parses as a Geni id -> {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
