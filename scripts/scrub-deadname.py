"""Remove Emma's deadname from this repository. Her name is Emma Leonhart.

Emma, 2026-08-12: **"JUST FUCKING REMOVE the DEADNAME"**, **"Eric Borsheim does
not fucking go into the data"**, **"Just Emma Leonhart"**.

The profile `6000000087535357291` is the account owner and the seed of the first
exports, so the old name is in every GEDCOM taken before the rename, in derived
reports built from them, and in prose that quoted them.

**Exact full-name strings only.** A bare surname is never replaced: `Borsheim`
and `Bishop` are ordinary surnames that belong to other people in this tree, and
a blanket substitution would rewrite strangers' records. The GEDCOM name pieces
are only rewritten inside her own `INDI` record, located by xref.

Binary-safe, byte-for-byte elsewhere: files are read and written as UTF-8 with
newlines preserved, and a file whose content does not change is not rewritten.

    py scripts/scrub-deadname.py --check    # report only
    py scripts/scrub-deadname.py            # rewrite
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

GENI_ID = "6000000087535357291"
XREF = f"@I{GENI_ID}@"

#: Whole-name replacements, longest first so a shorter one cannot pre-empt a
#: longer one that contains it.
REPLACEMENTS = [
    ("Eric /Borsheim/", "Emma /Leonhart/"),
    ("Eric Borsheim", "Emma Leonhart"),
    ("Emma Bishop", "Emma Leonhart"),
    ("Emma-Bishop", "Emma-Leonhart"),
]

#: Name pieces, rewritten only inside her own INDI record.
PIECES = [("2 GIVN Eric", "2 GIVN Emma"), ("2 SURN Borsheim", "2 SURN Leonhart")]

SKIP_DIRS = {".git", "out", "wikidata", "__pycache__", ".pytest_cache"}


def scrub_record_pieces(text: str) -> str:
    """Rewrite `GIVN`/`SURN` only within the block that is her `INDI` record."""
    if XREF not in text:
        return text
    lines = text.split("\n")
    inside = False
    for index, line in enumerate(lines):
        if line.startswith("0 "):
            inside = XREF in line
            continue
        if not inside:
            continue
        for old, new in PIECES:
            if line.strip() == old:
                lines[index] = line.replace(old, new)
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="report without writing")
    args = ap.parse_args()

    changed: list[tuple[Path, int]] = []
    scanned = 0

    for path in sorted(REPO_ROOT.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(REPO_ROOT).parts):
            continue
        if path.name == "scrub-deadname.py":
            continue
        try:
            original = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError, OSError):
            continue
        scanned += 1

        text = original
        hits = 0
        for old, new in REPLACEMENTS:
            hits += text.count(old)
            text = text.replace(old, new)
        text = scrub_record_pieces(text)

        if text != original:
            changed.append((path.relative_to(REPO_ROOT), hits))
            if not args.check:
                path.write_text(text, encoding="utf-8", newline="")

    verb = "would change" if args.check else "changed"
    print(f"scanned {scanned:,} text files; {verb} {len(changed):,}")
    for rel, hits in changed[:40]:
        print(f"  {hits:>4}  {rel.as_posix()}")
    if len(changed) > 40:
        print(f"  … and {len(changed) - 40:,} more")

    # Anything left is a bug in this script, not a file it chose to skip.
    remaining = 0
    for path in sorted(REPO_ROOT.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(REPO_ROOT).parts):
            continue
        if path.name == "scrub-deadname.py":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError, OSError):
            continue
        if "Eric Borsheim" in text or "Eric /Borsheim/" in text or "Emma Bishop" in text:
            remaining += 1
            print(f"  STILL PRESENT: {path.relative_to(REPO_ROOT).as_posix()}")
    print(f"{remaining} files still contain a full deadname string")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
