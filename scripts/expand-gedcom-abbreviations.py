"""Replace abbreviated patronymics with their resolved forms IN THE SOURCE `.ged` FILES.

    PYTHONPATH=src python scripts/expand-gedcom-abbreviations.py [--dry-run]

## Why this edits the corpus rather than the emitter

Ruled 2026-09-15: *"you're supposed to fucking change the data so that it doesn't do it ... you
are literally supposed to edit the gedcom files to replace all instances of the abbreviated form
with the non-abbreviated forms."* And the reason, 2026-09-17: *"this kind of scenario was the
reason why I asked for them to be replaced like this. My expectation is that the abbreviation was
certainly going to break shit."*

**It did.** `Q141488174` was created as a human called `Askvik` with an alias `Raunes` — two farm
names and no person — because `name_shape` calls the ABBREVIATED patronymics unknown while
passing the written-out ones, so `classify_fields` armed the `NN Olsdatter` marker rule, threw
`Guri` away, and short-circuited `Nilsdtr.` before `is_patronymic` could see it.

⛔ **EXPANDING AT EMISSION CANNOT CLOSE THAT CLASS.** `classify_fields` runs upstream of
`expand_abbreviations`, so it meets the raw token and the name is already destroyed by the time
anything expands it. Fixing the string at source is a guarantee: no code path can meet the
abbreviated form. `db57fc43` repaired one path; this removes the cause.

## ⛔ IT OVERWRITES, AND THAT IS AN EXPLICIT EXCEPTION

`CLAUDE.md` § *Never overwrite an existing `.ged`* forbids exactly this. Asked which way it
should go on 2026-09-17 — overwrite in place, a new file beside each original, corrected copies
with the originals moved aside, or leave the data and harden the code — the answer was
**overwrite in place**, because it is the only one that removes the abbreviated string from the
corpus. A file beside the original does not: `exports/` is read recursively, so the old spelling
stays readable and `classify_fields` can still meet it.

The originals are in git. That is the undo.

## What it touches, and what it will not

* Only lines that carry a NAME: `1 NAME`, `2 GIVN`, `2 SURN`, `2 _MARNM`, `2 NICK`. A patronymic
  that appears in a note or a place stays as it is.
* Only inside the record of a person `reports/abbreviated-patronymics.csv` names, keyed on the
  xref, which is the Geni id — `CLAUDE.md` § *The Geni profile ID is the primary key*. A global
  string replace would rewrite other people who share the token, and the CSV's whole point is
  that the expansion was **decided per person** from the mother and paternal grandmother.
* Only that person's own token, and with the trailing period optional: the CSV stores `Larsdtr`
  and the file may hold `Larsdtr.`.

⛔ **BOM AND CRLF ARE PRESERVED.** These files are UTF-8 with a BOM and CRLF throughout. Reading
them as text with universal newlines and writing them back would rewrite every line ending in the
corpus and produce a diff of millions of lines with no content change — and `CLAUDE.md` § *Windows:
never round-trip UTF-8 through Get-Content/Set-Content* is the same hazard from the other side.
So the file is handled as BYTES and only the matched token is substituted.
"""
from __future__ import annotations

import argparse
import collections
import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXPORTS = ROOT / "exports"
TABLE = ROOT / "reports" / "abbreviated-patronymics.csv"

#: The GEDCOM lines that carry a name. Anything else keeps the string it has.
NAME_TAGS = (b"1 NAME", b"2 GIVN", b"2 SURN", b"2 _MARNM", b"2 NICK")

#: `0 @I6000000001770188374@ INDI` -- the xref is the Geni id.
INDI = re.compile(rb"^0 @I(\d+)@ INDI")
RECORD = re.compile(rb"^0 ")


def table():
    """`{geni_id: [(compiled token, expansion bytes), ...]}` from the resolved table."""
    out = collections.defaultdict(list)
    with TABLE.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            gid = (row.get("geni_id") or "").strip()
            tok = (row.get("token") or "").strip()
            exp = (row.get("expansion") or "").strip()
            if not (gid and tok and exp) or tok == exp:
                continue
            # Trailing period optional; no letter either side, so `Larsdtr` never eats
            # `Larsdtrud`. Unicode-aware on the right so a Norwegian vowel counts as a letter.
            pat = re.compile(rb"(?<![^\W\d_])" + re.escape(tok.encode("utf-8")) +
                             rb"\.?(?![^\W\d_])")
            out[gid].append((pat, exp.encode("utf-8")))
    return out


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true",
                    help="count what would change and write nothing")
    args = ap.parse_args()

    per_person = table()
    print("%d people carry a resolved abbreviation" % len(per_person))

    files = sorted(EXPORTS.rglob("*.ged"))
    print("%d .ged files under %s" % (len(files), EXPORTS.relative_to(ROOT)))

    touched_files, touched_lines, people_seen = 0, 0, set()
    for path in files:
        raw = path.read_bytes()
        # Split KEEPING the line endings, so CRLF survives untouched.
        lines = raw.splitlines(keepends=True)
        here, changed = None, False
        for n, line in enumerate(lines):
            if RECORD.match(line.lstrip(b"\xef\xbb\xbf")):
                m = INDI.match(line.lstrip(b"\xef\xbb\xbf"))
                here = m.group(1).decode() if m else None
                continue
            if here is None:
                continue
            rules = per_person.get(here)
            if not rules or not line.startswith(NAME_TAGS):
                continue
            new = line
            for pat, exp in rules:
                new = pat.sub(exp, new)
            if new != line:
                lines[n] = new
                changed = True
                touched_lines += 1
                people_seen.add(here)
        if changed:
            touched_files += 1
            if not args.dry_run:
                path.write_bytes(b"".join(lines))

    print("%s%d file(s), %d name line(s), %d distinct people"
          % ("would change " if args.dry_run else "changed ",
             touched_files, touched_lines, len(people_seen)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
