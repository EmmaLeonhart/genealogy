"""The four family maps `build-garborg-day.read_tree` needs, without the 409 MB GEDCOM.

    py scripts/build-family-structure.py

**Why this exists.** The scheduled pipeline (`.github/workflows/pipeline.yml`) rebuilds the batch
on a runner. `--compose` was believed to read only the derived CSVs -- that is what
`rebuild-everything.py` says and what the CI checkout was scoped for -- and the first pipeline run
died in two seconds with `FileNotFoundError: out/merged.ged`. That file is 409 MB and gitignored
because GitHub refuses it, so no runner can ever have it.

**All four maps are written, not two of them inverted.** `fam_p`/`fam_c` come from a FAMILY's
`HUSB`/`WIFE`/`CHIL`; `fams`/`famc` come from a PERSON's `FAMS`/`FAMC`. Inverting one pair to get
the other looks equivalent and is not -- measured 2026-09-01, it gave 842,548 against 833,632 and
1,182,519 against 1,177,873, because the two sides disagree wherever one half of a pair is
missing. Storing all four makes `read_tree` return byte-identical maps from either source, which
was checked rather than assumed.

155 MB plain, 14 MB gzipped; `pack-derived.py` carries it.
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
TAB = chr(9)
NL = chr(10)
MERGED = ROOT / "out" / "merged.ged"
OUT = ROOT / "out" / "family-structure.tsv"


def main() -> int:
    if not MERGED.exists():
        print(f"REFUSING: {MERGED} is absent. This script reads the merge; it cannot "
              f"reconstruct it.")
        return 1
    fam_p, fam_c, fams, famc = {}, {}, {}, {}
    cur = kind = None
    with io.open(MERGED, encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith("0 @"):
                p = line.split()
                cur, kind = p[1][2:-1], (p[2].strip() if len(p) > 2 else "")
            elif cur and line.startswith("1 "):
                tag, _, val = line[2:].strip().partition(" ")
                if kind == "FAM":
                    if tag in ("HUSB", "WIFE"):
                        fam_p.setdefault(cur, []).append(val[2:-1])
                    elif tag == "CHIL":
                        fam_c.setdefault(cur, []).append(val[2:-1])
                elif kind == "INDI":
                    if tag == "FAMS":
                        fams.setdefault(cur, []).append(val[2:-1])
                    elif tag == "FAMC":
                        famc.setdefault(cur, []).append(val[2:-1])
    with io.open(OUT, "w", encoding="utf-8", newline=NL) as fh:
        fh.write(TAB.join(("map", "key", "values")) + NL)
        for name, d in (("fam_p", fam_p), ("fam_c", fam_c), ("fams", fams), ("famc", famc)):
            for k, v in d.items():
                fh.write(name + TAB + k + TAB + " ".join(v) + NL)
    print(f"fam_p {len(fam_p):,}  fam_c {len(fam_c):,}  "
          f"fams {len(fams):,}  famc {len(famc):,}")
    print(f"wrote {OUT.relative_to(ROOT)} - {OUT.stat().st_size // 1048576} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
