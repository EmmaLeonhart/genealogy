"""Keep the four big derived CSVs in git, gzipped, because they no longer fit.

    python scripts/pack-derived.py            # csv -> csv.gz, for committing
    python scripts/pack-derived.py --unpack   # csv.gz -> csv, after a clean clone

**Emma's call, 2026-08-24:** *"Imo gzip because this is long term and we aren't adding
any more data into our tree. Just processing."*

Regenerated from the 546-export merge, all four exceed GitHub's **100 MiB** per-file
limit — 183.6, 175.9, 127.7 and 108.6 MiB, against 37–68 MiB at ~250 exports. Nothing
could be pushed. The alternative of gitignoring them as regenerable was rejected: they
take about an hour to rebuild and a clean checkout would be unable to run any emitter
until it had.

**The plain `.csv` stays the thing every reader opens.** Forty-four scripts read these
files by name, and rewriting all of them to handle two extensions would be a large
change for no benefit — so the `.csv` is gitignored, the `.csv.gz` is committed, and a
clean checkout runs `--unpack` once. `tests/test_derived_packing.py` fails if a `.gz`
goes missing or a plain `.csv` gets tracked, so the two cannot drift apart silently.

Gzip level 6: level 9 took materially longer for about a percent, on files this size.
"""
from __future__ import annotations

import argparse
import gzip
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent

#: The four the merge grew past the limit. Named rather than globbed: a new large
#: report should be a decision, not something this quietly swallows.
DERIVED = [
    "reports/display-names.csv",
    "reports/derived-facts.csv",
    "reports/derived-family.csv",
    "reports/derived-labels.csv",
]

LIMIT = 100 * 1024 * 1024


def mib(n):
    return f"{n / 1048576:.1f} MiB"


def pack():
    for rel in DERIVED:
        src = ROOT / rel
        dst = ROOT / (rel + ".gz")
        if not src.exists():
            print(f"  {rel}: missing, skipped")
            continue
        with open(src, "rb") as fin, gzip.open(dst, "wb", compresslevel=6) as fout:
            shutil.copyfileobj(fin, fout, length=1 << 20)
        a, b = src.stat().st_size, dst.stat().st_size
        flag = "" if b < LIMIT else "  ** STILL OVER 100 MiB **"
        print(f"  {rel}: {mib(a)} -> {mib(b)}  ({a / b:.1f}x){flag}")


def unpack():
    for rel in DERIVED:
        src = ROOT / (rel + ".gz")
        dst = ROOT / rel
        if not src.exists():
            print(f"  {rel}.gz: missing, skipped")
            continue
        with gzip.open(src, "rb") as fin, open(dst, "wb") as fout:
            shutil.copyfileobj(fin, fout, length=1 << 20)
        print(f"  {rel}: {mib(dst.stat().st_size)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--unpack", action="store_true",
                    help="restore the plain CSVs from the committed .gz")
    args = ap.parse_args()
    if args.unpack:
        print("unpacking:")
        unpack()
    else:
        print("packing:")
        pack()


if __name__ == "__main__":
    main()
